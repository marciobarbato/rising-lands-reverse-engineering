import AppKit
import WebKit
import CryptoKit

final class AppDelegate: NSObject, NSApplicationDelegate, WKScriptMessageHandler, WKNavigationDelegate, NSWindowDelegate {
    var window: NSWindow!
    var web: WKWebView!
    var nativeLive: NativeLiveWindow?
    var horizonOutput: URL?
    var horizonFinished=false
    var horizonLastProgress=0.0
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
    var smokeLifecycle = SmokeReadiness(launched: ProcessInfo.processInfo.systemUptime)
    var smokeTimer: Timer?
    var preparingSmoke = false
    var smokeMode = "exercise"
    var readySignal: [String:Any]?
    var readyDelayMs = 0
    var smokeProgress: [String:Any]?
    let resourceRoot = Bundle.main.resourceURL!.appendingPathComponent("preview", isDirectory: true)

    func applicationDidFinishLaunching(_ notification: Notification) {
        let args = CommandLine.arguments
        if let i = args.firstIndex(of: "--smoke-test"), args.count > i + 1 { smokeOutput = URL(fileURLWithPath: args[i+1]) }
        if let i = args.firstIndex(of: "--screenshot"), args.count > i + 1 { screenshotOutput = URL(fileURLWithPath: args[i+1]) }
        smokeMode = args.contains("--inspection") ? "inspection" : "exercise"
        if smokeOutput != nil, let i = args.firstIndex(of: "--smoke-ready-delay-ms"), args.count > i+1,
           let delay = Int(args[i+1]), (0...80000).contains(delay) { readyDelayMs = delay }
        makeMenu()
        let config = WKWebViewConfiguration()
        config.websiteDataStore = .nonPersistent()
        config.userContentController.add(self, name: "engine")
        let smokeConfiguration = "window.nativeSmoke={enabled:\(smokeOutput != nil),readyDelayMs:\(readyDelayMs)};"
        config.userContentController.addUserScript(WKUserScript(source:smokeConfiguration,injectionTime:.atDocumentStart,forMainFrameOnly:true))
        web = WKWebView(frame: .zero, configuration: config)
        web.navigationDelegate = self
        web.setValue(false, forKey: "drawsBackground")
        window = NSWindow(contentRect: NSRect(x:0,y:0,width:1360,height:900), styleMask:[.titled,.closable,.miniaturizable,.resizable], backing:.buffered, defer:false)
        window.title = "RisingLands-ptbr — Sessão jogável"
        window.minSize = NSSize(width:1080,height:740)
        window.contentView = web
        window.delegate = self
        window.backgroundColor = NSColor(calibratedRed:0.067,green:0.086,blue:0.098,alpha:1)
        window.center()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps:true)
        if window.isVisible { smokeLifecycle.windowVisible(ProcessInfo.processInfo.systemUptime) }
        do { try launchEngine() }
        catch { fail("Não foi possível iniciar o Python incluído: \(error.localizedDescription)"); return }
        let page = resourceRoot.appendingPathComponent(args.contains("--inspection") ? "ui/playback.html" : "ui/index.html")
        web.loadFileURL(page, allowingReadAccessTo:resourceRoot)
        if let index=args.firstIndex(of:"--native-horizon"),args.count>index+1 {
            horizonOutput=URL(fileURLWithPath:args[index+1])
            DispatchQueue.main.asyncAfter(deadline:.now()+1){[weak self] in self?.startNativeHorizon()}
        }
        if let index=args.firstIndex(of:"--native-benchmark"),args.count>index+1 {
            let output=URL(fileURLWithPath:args[index+1])
            DispatchQueue.main.asyncAfter(deadline:.now()+1){[weak self] in self?.startNativeBenchmark(output,args:args)}
        }
        if smokeOutput != nil {
            smokeTimer = Timer.scheduledTimer(withTimeInterval:0.5,repeats:true) { [weak self] _ in
                guard let self = self, !self.finishedSmoke else { return }
                let now = ProcessInfo.processInfo.systemUptime
                if self.window.isVisible { self.smokeLifecycle.windowVisible(now) }
                if let reason = self.smokeLifecycle.timeout(now) {
                    self.finishSmoke(["passed":false,"error":reason])
                }
            }
        }
    }

    func makeMenu() {
        let main = NSMenu()
        let appItem = NSMenuItem(); main.addItem(appItem)
        let appMenu = NSMenu(); appItem.submenu = appMenu
        appMenu.addItem(withTitle:"Sobre RisingLands-ptbr",action:#selector(showAbout),keyEquivalent:"")
        appMenu.addItem(.separator())
        appMenu.addItem(withTitle:"Encerrar RisingLands-ptbr",action:#selector(NSApplication.terminate(_:)),keyEquivalent:"q")
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
        NSApp.orderFrontStandardAboutPanel(options:[.applicationName:"RisingLands-ptbr", .applicationVersion:"0.1", .credits:NSAttributedString(string:"Sessão interativa de pesquisa reconstruída. Consulte a procedência e os limites dentro do aplicativo.")])
    }
    func launchEngine() throws {
        let process = Process()
        process.executableURL = Bundle.main.resourceURL!.appendingPathComponent("Python/bin/python3")
        process.arguments = ["-I","-B","-u",resourceRoot.appendingPathComponent("engine.py").path]
        process.currentDirectoryURL = resourceRoot
        var env = ProcessInfo.processInfo.environment
        env.removeValue(forKey:"PYTHONPATH"); env.removeValue(forKey:"PYTHONHOME")
        env.removeValue(forKey:"RISING_APP_ROOT")
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
        if message.frameInfo.isMainFrame, smokeOutput != nil, let body = message.body as? [String:Any] {
            if body["action"] as? String == "smokeProgress" {
                smokeProgress = body
                return
            }
            if body["action"] as? String == "appInitializationFailed" {
                finishSmoke(["passed":false,"error":body["error"] as? String ?? "Initialization failed"])
                return
            }
            if body["action"] as? String == "appReady" {
                let expected = Bundle.main.object(forInfoDictionaryKey:"RisingLandsSourceCommit") as? String
                guard body["protocol"] as? Int == 1, body["mode"] as? String == smokeMode,
                      body["worker"] as? Bool == true, body["assets"] as? Bool == true,
                      body["commit"] as? String == expected, expected != nil else {
                    finishSmoke(["passed":false,"error":"Invalid app readiness signal"]); return
                }
                readySignal = body
                smokeLifecycle.ready(ProcessInfo.processInfo.systemUptime)
                startSmokeIfReady()
                return
            }
        }
        if message.frameInfo.isMainFrame, let body = message.body as? [String:Any],
           body["action"] as? String == "capture", smokeOutput != nil,
           let shot = screenshotOutput, let label = body["label"] as? String,
           ["before", "after", "paint"].contains(label), let requestID = body["id"] {
            web.takeSnapshot(with:nil) { [weak self] image,error in
                var response:[String:Any] = ["id":requestID,"ok":false,"error":"Falha na captura nativa"]
                if let image = image, let tiff = image.tiffRepresentation,
                   let bitmap = NSBitmapImageRep(data:tiff), let png = bitmap.representation(using:.png,properties:[:]) {
                    let url = shot.deletingPathExtension().appendingPathExtension(label + ".png")
                    do {
                        try png.write(to:url)
                        let hash = SHA256.hash(data:png).map { String(format:"%02x",$0) }.joined()
                        response = ["id":requestID,"ok":true,"capture":["sha256":hash,"path":url.path]]
                    } catch { response["error"] = error.localizedDescription }
                }
                if let data = try? JSONSerialization.data(withJSONObject:response), let json = String(data:data,encoding:.utf8) {
                    self?.web.evaluateJavaScript("window.receive(\(json));",completionHandler:nil)
                }
            }
            return
        }
        if message.frameInfo.isMainFrame,let body=message.body as? [String:Any],body["action"] as? String == "recordingIndicator",let active=body["active"] as? Bool {
            nativeLive?.setRecording(active);return
        }
        if message.frameInfo.isMainFrame, let body = message.body as? [String:Any],
           body["action"] as? String == "saveInput", let requestID = body["id"],
           let content = body["content"] as? [String:Any],
           let encoded = try? JSONSerialization.data(withJSONObject:content,options:[.prettyPrinted,.sortedKeys]),
           encoded.count <= 64*1024*1024 {
            let data=(body["text"] as? String).map{Data($0.utf8)} ?? (encoded + Data([10]))
            guard data.count<=64*1024*1024,(try? JSONSerialization.jsonObject(with:data)) is [String:Any] else{nativeReply(requestID,error:"Entrada exportada inválida");return}
            func save(_ url:URL) {
                do{try data.write(to:url,options:.atomic);self.nativeReply(requestID,value:["saved":true,"path":url.path,"sha256":SHA256.hash(data:data).map{String(format:"%02x",$0)}.joined()])}
                catch{self.nativeReply(requestID,error:error.localizedDescription)}
            }
            // Automated smoke uses its explicitly declared evidence directory;
            // production always asks for a destination with NSSavePanel.
            if body["smokeEvidence"] as? Bool == true,let shot=smokeOutput{save(shot.deletingPathExtension().appendingPathExtension("input.json"));return}
            let panel = NSSavePanel()
            panel.title = "Exportar entrada gravada"
            panel.nameFieldStringValue = body["script"] as? Bool == true ? "monde01-input.json" : "monde01-macos-journal.json"
            panel.beginSheetModal(for:nativeLive?.window.isVisible == true ? nativeLive!.window:window) { [weak self] answer in
                if answer == .OK,let url=panel.url{save(url)}else{self?.nativeReply(requestID,value:["saved":false])}
            }
            return
        }
        if message.frameInfo.isMainFrame, let body=message.body as? [String:Any],body["action"] as? String == "playback",let operation=body["operation"] as? String {
            if operation.hasPrefix("live-") {
                do {
                    if nativeLive == nil {
                        nativeLive=try NativeLiveWindow(root:resourceRoot,validationMode:smokeOutput != nil)
                        nativeLive?.update={ [weak self] value in self?.nativeReply(nil,value:value) }
                        nativeLive?.recordedEvent={ [weak self] value in
                            if let data=try? JSONSerialization.data(withJSONObject:value),let json=String(data:data,encoding:.utf8){self?.web.evaluateJavaScript("window.recordNativeInput(\(json));",completionHandler:nil)}
                        }
                        nativeLive?.recordingAction={ [weak self] in self?.web.evaluateJavaScript("window.toggleRecording();",completionHandler:nil) }
                        nativeLive?.exportAction={ [weak self] in self?.web.evaluateJavaScript("window.exportRecording();",completionHandler:nil) }
                        web.evaluateJavaScript("window.syncRecordingIndicator();",completionHandler:nil)
                    }
                    nativeLive?.window.makeKeyAndOrderFront(nil)
                    nativeLive?.perform(operation == "live-open" ? "live-reset":operation) { [weak self] value in self?.nativeReply(body["id"],value:value) }
                } catch { nativeReply(body["id"],error:"Falha nativa: \(error.localizedDescription)") }
                return
            }
            if operation == "record-barrier" {
                if let live=nativeLive{live.inputBarrier{[weak self] frame in self?.nativeReply(body["id"],value:["frame":frame])}}
                else{nativeReply(body["id"],value:["frame":129])};return
            }
            if operation == "record-native-smoke",smokeOutput != nil,let live=nativeLive {
                let down=body["stage"] as? String == "press"
                if !down,let event=NSEvent.keyEvent(with:.flagsChanged,location:.zero,modifierFlags:[],timestamp:0,windowNumber:live.window.windowNumber,context:nil,characters:"",charactersIgnoringModifiers:"",isARepeat:false,keyCode:59){live.window.sendEvent(event)}
                if body["stage"] as? String == "right"{live.benchmarkClick(400,272,right:true)}
                if down {
                    let p=live.metal.convert(NSPoint(x:live.metal.bounds.width/2,y:live.metal.bounds.height*(1-272.0/600.0)),to:nil)
                    for type in [NSEvent.EventType.leftMouseDown,.leftMouseUp]{if let event=NSEvent.mouseEvent(with:type,location:p,modifierFlags:.control,timestamp:0,windowNumber:live.window.windowNumber,context:nil,eventNumber:1,clickCount:1,pressure:1){live.window.sendEvent(event)}}
                }
                live.inputBarrier{[weak self] frame in self?.nativeReply(body["id"],value:["frame":frame,"recordingIndicator":live.recordButton.title])};return
            }
            if operation == "native-capture",let live=nativeLive,let shot=screenshotOutput {
                live.capture(shot.deletingPathExtension().appendingPathExtension("metal.png")){[weak self] value in self?.nativeReply(body["id"],value:value)}
                return
            }
            if operation == "read",let live=nativeLive,live.window.isVisible,
               let address=body["address"] as? String,let raw=(address.lowercased().hasPrefix("0x") ? UInt32(address.dropFirst(2),radix:16):UInt32(address,radix:10)),let size=body["size"] as? Int,(1...256).contains(size) {
                live.read(raw,size){[weak self] value in if let error=value["error"] as? String{self?.nativeReply(body["id"],error:error)}else{self?.nativeReply(body["id"],value:value)}};return
            }
            if operation == "read",let live=nativeLive,live.window.isVisible {nativeReply(body["id"],error:"Endereço ou tamanho de leitura nativa inválido.");return}
            if ["open","reset","phase","frame"].contains(operation),let live=nativeLive {live.perform("live-pause",completion:nil);live.window.orderOut(nil)}
        }
        guard message.frameInfo.isMainFrame, let body = message.body as? [String:Any], let action = body["action"] as? String,
              ["init","reset","select","order","pause","play","speed","step","pump","state","economy","combat","interact","playback"].contains(action),
              let data = try? JSONSerialization.data(withJSONObject:body) else { return }
        ioQueue.async { [weak self] in
            do { try self?.input?.write(contentsOf:data + Data([10])) }
            catch { DispatchQueue.main.async { self?.fail("Falha na comunicação com o motor: \(error.localizedDescription)") } }
        }
    }
    // Runs the production native window, worker, Metal pipeline and visible drawables.
    func startNativeBenchmark(_ output:URL,args:[String]) {
        do {
            func argument(_ key:String,_ fallback:String)->String{if let index=args.firstIndex(of:key),args.count>index+1{return args[index+1]};return fallback}
            let mode=argument("--benchmark-mode","play"),duration=Double(argument("--benchmark-seconds","65")) ?? 0
            let rate=Double(argument("--game-fps","0")) ?? -1
            guard ["play","test"].contains(mode),duration>=60,duration<=180,rate>=0,rate<=120 else{throw NSError(domain:"InvalidNativeBenchmarkArguments",code:1)}
            let live=try NativeLiveWindow(root:resourceRoot,validationMode:mode=="test");nativeLive=live
            var firstStop:[String:Any]?
            var gestures=[[String:Any]]()
            live.gameFPS=rate;live.update={value in
                if firstStop==nil,value["live_stop"] is [String:Any]{firstStop=value}
            };live.benchmarkInput=args.contains("--benchmark-orders")
            if let index=[15.0,20.0,30.0,60.0,0.0].firstIndex(of:rate){live.rateControl.selectItem(at:index)}
            live.perform("live-reset"){_ in live.perform("live-step"){_ in live.perform("live-play"){_ in
                if live.benchmarkInput{
                    // Anchor real AppKit gestures to the startup prefix, so uncapped
                    // play also receives orders before the later dependency horizon.
                    var gesture=0,lastGestureFrame=128
                    var inputTimer:Timer?
                    inputTimer=Timer.scheduledTimer(withTimeInterval:0.01,repeats:true){_ in
                        live.inputBarrier{frame in
                            guard gesture<4,frame>=lastGestureFrame+8 else{return}
                            gestures.append(["gesture":gesture,"observedNextFrame":frame])
                            switch gesture{
                            case 0:live.benchmarkClick(560,528)
                            case 1:live.benchmarkClick(624,432)
                            case 2:live.benchmarkClick(400,272,right:true)
                            default:live.benchmarkPointer(400,272);inputTimer?.invalidate()
                            }
                            gesture+=1;lastGestureFrame=frame
                        }
                    }
                }
                var lastPulse=ProcessInfo.processInfo.systemUptime,maxPulseGap=0.0,pulses=0
                let pulse=Timer.scheduledTimer(withTimeInterval:0.05,repeats:true){_ in let now=ProcessInfo.processInfo.systemUptime;maxPulseGap=max(maxPulseGap,now-lastPulse);lastPulse=now;pulses+=1}
                DispatchQueue.main.asyncAfter(deadline:.now()+duration){
                    live.perform("live-pause"){value in
                        pulse.invalidate()
                        var result=value;result["mainTimerMaxGapMS"]=maxPulseGap*1000;result["mainTimerPulses"]=pulses;result["mainTimerMaxDelayMS"]=max(0,maxPulseGap-0.05)*1000;result["commit"]=Bundle.main.object(forInfoDictionaryKey:"RisingLandsSourceCommit") as? String
                        result["native_window_visible"]=live.window.isVisible
                        result["requestedSeconds"]=duration
                        result["benchmark_gestures"]=gestures
                        result["first_stop_snapshot"]=firstStop ?? NSNull() as Any
                        result["screenMaximumFPS"]=live.window.screen?.maximumFramesPerSecond ?? 0
                        result["native_window_unoccluded"]=live.window.occlusionState.contains(.visible)
                        result["passed"]=live.window.isVisible && value["live_stop"] is NSNull
                        live.capture(output.deletingPathExtension().appendingPathExtension("png")){readback in
                            result["metal_readback"]=readback
                            if readback["error"] != nil{result["passed"]=false}
                            do{let data=try JSONSerialization.data(withJSONObject:result,options:[.sortedKeys,.prettyPrinted]);try data.write(to:output,options:.atomic)}catch{fputs("NativeBenchmarkWriteFailed: \(error)\n",stderr)}
                            self.engine?.terminate();NSApp.terminate(nil)
                        }
                    }
                }
            }}}
        }catch{
            if let data=try? JSONSerialization.data(withJSONObject:["passed":false,"error":error.localizedDescription]){try? data.write(to:output,options:.atomic)}
            NSApp.terminate(nil)
        }
    }
    func startNativeHorizon() {
        do {
            nativeLive=try NativeLiveWindow(root:resourceRoot,validationMode:true)
            nativeLive?.update={ [weak self] value in
                guard let self=self,!self.horizonFinished else{return}
                if value["live_stop"] is [String:Any] {self.finishNativeHorizon(value);return}
                let now=ProcessInfo.processInfo.systemUptime
                if now-self.horizonLastProgress>2,let path=self.horizonOutput,let data=try? JSONSerialization.data(withJSONObject:value,options:[.sortedKeys]) {
                    self.horizonLastProgress=now;try? data.write(to:path.appendingPathExtension("progress.json"),options:.atomic)
                }
            }
            nativeLive?.perform("live-reset"){[weak self] _ in
                self?.nativeLive?.work.async{[weak self] in guard let live=self?.nativeLive else{return};macos_live_audit_window(live.driver,18401)}
                self?.nativeLive?.perform("live-step"){[weak self] _ in self?.nativeLive?.perform("live-play",completion:nil)}
            }
            DispatchQueue.main.asyncAfter(deadline:.now()+1100){[weak self] in
                guard let self=self,!self.horizonFinished else{return}
                self.nativeLive?.perform("live-pause"){value in var value=value;value["horizon_pending"]=true;self.finishNativeHorizon(value)}
            }
        } catch {
            if let path=horizonOutput,let data=try? JSONSerialization.data(withJSONObject:["passed":false,"error":error.localizedDescription]){try? data.write(to:path,options:.atomic)}
            NSApp.terminate(nil)
        }
    }
    func finishNativeHorizon(_ value:[String:Any]) {
        guard !horizonFinished,let path=horizonOutput,let live=nativeLive else{return};horizonFinished=true
        live.capture(path.deletingPathExtension().appendingPathExtension("metal.png")){[weak self] readback in
            guard let self=self else{return};var result=value
            result["commit"]=Bundle.main.object(forInfoDictionaryKey:"RisingLandsSourceCommit") as? String
            result["native_window_visible"]=live.window.isVisible;result["metal_readback"]=readback
            result["passed"]=(value["verified_phases"] as? UInt64 ?? 0)>=18401 && (value["verified_surfaces"] as? UInt64 ?? 0)>=9200 && value["live_stop"] is [String:Any] && readback["error"]==nil && live.window.isVisible
            if let data=try? JSONSerialization.data(withJSONObject:result,options:[.prettyPrinted,.sortedKeys]){try? data.write(to:path,options:.atomic)}
            NSApp.terminate(nil)
        }
    }
    func nativeReply(_ id:Any?,value:[String:Any]=[:],error:String?=nil) {
        var value=value;value["commit"]=Bundle.main.object(forInfoDictionaryKey:"RisingLandsSourceCommit") as? String
        var response:[String:Any]=["ok":error==nil,"playback":value]
        if let id=id{response["id"]=id}else{response["nativeUpdate"]=true}
        if let error=error{response["error"]=error}
        if let data=try? JSONSerialization.data(withJSONObject:response),let json=String(data:data,encoding:.utf8){web.evaluateJavaScript("window.receive(\(json));",completionHandler:nil)}
    }
    func webView(_ webView:WKWebView,decidePolicyFor navigationAction:WKNavigationAction,decisionHandler:@escaping(WKNavigationActionPolicy)->Void) {
        guard let url = navigationAction.request.url else { decisionHandler(.cancel); return }
        decisionHandler(url.isFileURL && url.standardizedFileURL.path.hasPrefix(resourceRoot.path + "/") ? .allow : .cancel)
    }
    func webView(_ webView:WKWebView,didFinish navigation:WKNavigation!) {
        guard smokeOutput != nil else { return }
        smokeLifecycle.documentLoaded(ProcessInfo.processInfo.systemUptime)
        startSmokeIfReady()
    }
    func webViewWebContentProcessDidTerminate(_ webView:WKWebView) {
        fail("Web content process terminated")
    }
    func captureSmokeFrame(_ label:String, completion:@escaping()->Void) {
        guard let shot = screenshotOutput else { completion(); return }
        let url = label == "final" ? shot : shot.deletingPathExtension().appendingPathExtension(label + ".png")
        if label != "final" && FileManager.default.fileExists(atPath:url.path) { completion(); return }
        web.takeSnapshot(with:nil) { image,error in
            if let image = image, let tiff = image.tiffRepresentation,
               let bitmap = NSBitmapImageRep(data:tiff), let png = bitmap.representation(using:.png,properties:[:]) {
                try? png.write(to:url,options:.atomic)
            }
            completion()
        }
    }
    func startSmokeIfReady() {
        guard smokeOutput != nil, !finishedSmoke, !preparingSmoke,
              smokeLifecycle.readyAt != nil, smokeLifecycle.documentLoadedAt != nil else { return }
        preparingSmoke = true
        captureSmokeFrame("before") { [weak self] in
            guard let self = self, !self.finishedSmoke else { return }
            let now = ProcessInfo.processInfo.systemUptime
            guard self.smokeLifecycle.startChecks(now) else {
                self.finishSmoke(["passed":false,"error":self.smokeLifecycle.timeout(now) ?? "Smoke readiness incomplete"]); return
            }
            self.web.callAsyncJavaScript("return await window.runSmokeTests().catch(e=>({passed:false,error:String(e),stack:e.stack,diagnostics:window.smokeDiagnostics?window.smokeDiagnostics():{}}));",arguments:[:],in:nil,in:.page) { [weak self] result in
                switch result {
                case .success(let value):self?.finishSmoke(value as? [String:Any] ?? ["passed":false,"error":"Invalid smoke response"])
                case .failure(let error):self?.finishSmoke(["passed":false,"error":error.localizedDescription])
                }
            }
        }
    }
    func finishSmoke(_ result:[String:Any]) {
        guard !finishedSmoke else { return }; finishedSmoke = true
        smokeTimer?.invalidate()
        let now = ProcessInfo.processInfo.systemUptime
        var final = result
        if result["passed"] as? Bool == true {
            if let reason = smokeLifecycle.timeout(now) { final["passed"] = false; final["error"] = reason }
            if smokeLifecycle.checksStartedAt == nil { final["passed"] = false; final["error"] = "Checks started without readiness" }
        }
        final["readiness"] = smokeLifecycle.diagnostics(now)
        final["readySignal"] = readySignal
        final["lastProgress"] = smokeProgress
        final["diagnosticReadyDelayMs"] = readyDelayMs
        final["nativeWindowVisible"] = window.isVisible
        final["bundlePath"] = Bundle.main.bundlePath
        final["pythonStderr"] = errorText
        // Commit the result before attempting screenshots: even a hung WebView
        // cannot erase the phase-specific failure JSON.
        if let url = smokeOutput, let data = try? JSONSerialization.data(withJSONObject:final,options:[.prettyPrinted,.sortedKeys]) { try? data.write(to:url,options:.atomic) }
        DispatchQueue.main.asyncAfter(deadline:.now()+10) { NSApp.terminate(nil) }
        captureSmokeFrame("after") { [weak self] in
            self?.captureSmokeFrame("final") { NSApp.terminate(nil) }
        }
    }
    func fail(_ message:String) {
        if smokeOutput != nil { finishSmoke(["passed":false,"error":message]); return }
        let alert = NSAlert(); alert.messageText = "RisingLands-ptbr"; alert.informativeText = message; alert.alertStyle = .critical; alert.runModal()
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
