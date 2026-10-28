import AppKit
import WebKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate, NSWindowDelegate {
    var window: NSWindow!
    var web: WKWebView!
    var engine: Process?
    var input: FileHandle?
    var outPipe: Pipe?
    var errPipe: Pipe?
    var outputBuffer = Data()
    var errorText = ""
    let ioQueue = DispatchQueue(label: "local.risinglands.preview.engine")
    var smokeOutput: URL?
    var screenshotOutput: URL?
    var finishedSmoke = false
    let resourceRoot = Bundle.main.resourceURL!.appendingPathComponent("preview", isDirectory: true)

    func applicationDidFinishLaunching(_ notification: Notification) {
        let args = CommandLine.arguments
        if let i = args.firstIndex(of: "--smoke-test"), args.count > i + 1 { smokeOutput = URL(fileURLWithPath: args[i+1]) }
        if let i = args.firstIndex(of: "--screenshot"), args.count > i + 1 { screenshotOutput = URL(fileURLWithPath: args[i+1]) }
        makeMenu()
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .nonPersistent()
        config.userContentController.add(self, name: "engine")
        web = WKWebView(frame: .zero, configuration: config)
        web.navigationDelegate = self
        web.setValue(false, forKey: "drawsBackground")
        window = NSWindow(contentRect: NSRect(x:0,y:0,width:1360,height:900), styleMask:[.titled,.closable,.miniaturizable,.resizable], backing:.buffered, defer:false)
        window.title = "Rising Lands — Observatório da reconstrução"
        window.minSize = NSSize(width:1080,height:740)
        window.contentView = web
        window.delegate = self
        window.backgroundColor = NSColor(calibratedRed:0.067,green:0.086,blue:0.098,alpha:1)
        window.center()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps:true)
        do { try launchEngine() }
        catch { fail("Não foi possível iniciar o Python incluído: \(error.localizedDescription)"); return }
        let page = resourceRoot.appendingPathComponent("ui/index.html")
        web.loadFileURL(page, allowingReadAccessTo:resourceRoot)
        if smokeOutput != nil {
            DispatchQueue.main.asyncAfter(deadline:.now()+45) { [weak self] in
                guard let self = self, !self.finishedSmoke else { return }
                self.finishSmoke(["passed":false,"error":"Tempo limite de 45 segundos na abertura", "pythonStderr":self.errorText])
            }
        }
    }
    func makeMenu() {
        let main = NSMenu()
        let appItem = NSMenuItem(); main.addItem(appItem)
        let appMenu = NSMenu(); appItem.submenu = appMenu
        appMenu.addItem(withTitle:"Sobre Rising Lands Preview",action:#selector(showAbout),keyEquivalent:"")
        appMenu.addItem(.separator())
        appMenu.addItem(withTitle:"Encerrar Rising Lands Preview",action:#selector(NSApplication.terminate(_:)),keyEquivalent:"q")
        let edit = NSMenuItem(); main.addItem(edit); let editMenu = NSMenu(title:"Editar"); edit.submenu = editMenu
        editMenu.addItem(withTitle:"Copiar",action:#selector(NSText.copy(_:)),keyEquivalent:"c")
        editMenu.addItem(withTitle:"Colar",action:#selector(NSText.paste(_:)),keyEquivalent:"v")
        editMenu.addItem(withTitle:"Selecionar tudo",action:#selector(NSText.selectAll(_:)),keyEquivalent:"a")
        let windowItem = NSMenuItem(); main.addItem(windowItem); let windowMenu = NSMenu(title:"Janela"); windowItem.submenu = windowMenu
        windowMenu.addItem(withTitle:"Minimizar",action:#selector(NSWindow.miniaturize(_:)),keyEquivalent:"m")
        windowMenu.addItem(withTitle:"Fechar",action:#selector(NSWindow.performClose(_:)),keyEquivalent:"w")
        NSApp.mainMenu = main
    }
    @objc func showAbout() {
        NSApp.orderFrontStandardAboutPanel(options:[.applicationName:"Rising Lands Preview", .applicationVersion:"0.1", .credits:NSAttributedString(string:"Visualizador local de pesquisa. Movimento Python reconstruído; consulte a procedência dentro do aplicativo.")])
    }
    func launchEngine() throws {
        let process = Process()
        process.executableURL = Bundle.main.resourceURL!.appendingPathComponent("Python/bin/python3")
        process.arguments = ["-I","-B","-u",resourceRoot.appendingPathComponent("engine.py").path]
        process.currentDirectoryURL = resourceRoot
        var env = ProcessInfo.processInfo.environment
        env.removeValue(forKey:"PYTHONPATH"); env.removeValue(forKey:"PYTHONHOME")
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        process.environment = env
        let stdinPipe = Pipe(); let stdoutPipe = Pipe(); let stderrPipe = Pipe()
        process.standardInput = stdinPipe; process.standardOutput = stdoutPipe; process.standardError = stderrPipe
        input = stdinPipe.fileHandleForWriting; outPipe = stdoutPipe; errPipe = stderrPipe
        stdoutPipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty else { handle.readabilityHandler = nil; return }
            self?.ioQueue.async { [weak self] in self?.consume(data) }
        }
        stderrPipe.fileHandleForReading.readabilityHandler = { [weak self] handle in
            let data = handle.availableData
            guard !data.isEmpty else { handle.readabilityHandler = nil; return }
            let text = String(data:data,encoding:.utf8) ?? ""
            DispatchQueue.main.async { [weak self] in self?.errorText = String(((self?.errorText ?? "") + text).suffix(24000)) }
        }
        process.terminationHandler = { [weak self] p in
            DispatchQueue.main.async {
                guard let self = self, !self.finishedSmoke else { return }
                if p.terminationStatus != 0 { self.fail("O motor Python encerrou com código \(p.terminationStatus).\n\(self.errorText)") }
            }
        }
        engine = process
        try process.run()
    }
    func consume(_ data:Data) {
        outputBuffer.append(data)
        while let range = outputBuffer.range(of:Data([10])) {
            let line = outputBuffer.subdata(in:0..<range.lowerBound)
            outputBuffer.removeSubrange(0..<range.upperBound)
            guard let string = String(data:line,encoding:.utf8), (try? JSONSerialization.jsonObject(with:line)) != nil else { continue }
            DispatchQueue.main.async { [weak self] in
                self?.web.evaluateJavaScript("window.receive(\(string));", completionHandler:{ _,error in
                    if let error = error { self?.errorText += "\nUI: \(error.localizedDescription)" }
                })
            }
        }
    }
    func userContentController(_ userContentController:WKUserContentController,didReceive message:WKScriptMessage) {
        guard message.frameInfo.isMainFrame, let body = message.body as? [String:Any], let action = body["action"] as? String,
              ["init","reset","select","order","pause","play","speed","step","pump","state","economy","combat"].contains(action),
              let data = try? JSONSerialization.data(withJSONObject:body) else { return }
        ioQueue.async { [weak self] in
            do { try self?.input?.write(contentsOf:data + Data([10])) }
            catch { DispatchQueue.main.async { self?.fail("Falha na comunicação com o motor: \(error.localizedDescription)") } }
        }
    }
    func webView(_ webView:WKWebView,decidePolicyFor navigationAction:WKNavigationAction,decisionHandler:@escaping(WKNavigationActionPolicy)->Void) {
        guard let url = navigationAction.request.url else { decisionHandler(.cancel); return }
        decisionHandler(url.isFileURL && url.standardizedFileURL.path.hasPrefix(resourceRoot.path + "/") ? .allow : .cancel)
    }
    func webView(_ webView:WKWebView,didFinish navigation:WKNavigation!) {
        guard smokeOutput != nil else { return }
        webView.callAsyncJavaScript("return await window.runSmokeTests();",arguments:[:],in:nil,in:.page) { [weak self] result in
            switch result {
            case .success(let value):self?.finishSmoke(value as? [String:Any] ?? ["passed":false,"error":"Resposta inválida"])
            case .failure(let error):self?.finishSmoke(["passed":false,"error":error.localizedDescription,"pythonStderr":self?.errorText ?? ""])
            }
        }
    }
    func finishSmoke(_ result:[String:Any]) {
        guard !finishedSmoke else { return }; finishedSmoke = true
        var final = result
        final["nativeWindowVisible"] = window.isVisible
        final["bundlePath"] = Bundle.main.bundlePath
        final["pythonStderr"] = errorText
        if let url = smokeOutput, let data = try? JSONSerialization.data(withJSONObject:final,options:[.prettyPrinted,.sortedKeys]) { try? data.write(to:url,options:.atomic) }
        if let url = screenshotOutput {
            web.takeSnapshot(with:nil) { image,error in
                if let image = image, let tiff = image.tiffRepresentation, let bitmap = NSBitmapImageRep(data:tiff), let png = bitmap.representation(using:.png,properties:[:]) { try? png.write(to:url) }
                NSApp.terminate(nil)
            }
        } else { NSApp.terminate(nil) }
    }
    func fail(_ message:String) {
        if smokeOutput != nil { finishSmoke(["passed":false,"error":message]); return }
        let alert = NSAlert(); alert.messageText = "Rising Lands Preview"; alert.informativeText = message; alert.alertStyle = .critical; alert.runModal()
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ sender:NSApplication)->Bool { true }
    func applicationWillTerminate(_ notification:Notification) {
        outPipe?.fileHandleForReading.readabilityHandler = nil
        errPipe?.fileHandleForReading.readabilityHandler = nil
        try? input?.close()
        if engine?.isRunning == true { engine?.terminate() }
    }
}
let app = NSApplication.shared
app.setActivationPolicy(.regular)
let delegate = AppDelegate()
app.delegate = delegate
app.run()
