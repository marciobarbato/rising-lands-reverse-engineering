import AppKit
import Metal
import QuartzCore
import CryptoKit

// Engine publishes to three persistent slots. The display queue owns drawables;
// a slot cannot be overwritten until every GPU reader has completed.
final class NativePlayPresenter {
    struct Slot { let image:MTLTexture;let palette:MTLBuffer;var readers=0 }
    let layer:CAMetalLayer,commands:MTLCommandQueue,pipeline:MTLRenderPipelineState
    let queue=DispatchQueue(label:"risinglands.native.display",qos:.userInteractive)
    let lock=NSLock()
    var slots=[Slot](),latest:Int?,timer:DispatchSourceTimer?
    var lastTexture:MTLTexture?,failure:String?
    var published=0,dropped=0,submitted=0
    var uploadSeconds=0.0,submitSeconds=0.0,gpuSeconds=0.0,drawableWaitSeconds=0.0
    var presented=[Double]()
    var presentedCount=0,epoch=0
    var measurementStart=0.0
    var uniqueGameFrames=0,lastPresentedFrame:UInt64?
    var latestFrame:UInt64=0
    init(layer:CAMetalLayer,device:MTLDevice,commands:MTLCommandQueue,pipeline:MTLRenderPipelineState) throws {
        self.layer=layer;self.commands=commands;self.pipeline=pipeline;presented.reserveCapacity(16384)
        let descriptor=MTLTextureDescriptor.texture2DDescriptor(pixelFormat:.r8Uint,width:800,height:600,mipmapped:false)
        descriptor.storageMode = .shared;descriptor.usage = .shaderRead
        for _ in 0..<3 {
            guard let image=device.makeTexture(descriptor:descriptor),let palette=device.makeBuffer(length:768,options:.storageModeShared) else{throw NSError(domain:"MetalPlaySlotAllocation",code:1)}
            slots.append(Slot(image:image,palette:palette))
        }
    }
    func publish(_ pixels:UnsafePointer<UInt8>,_ rgb:UnsafePointer<UInt8>,frame:UInt64) {
        let started=ProcessInfo.processInfo.systemUptime
        lock.lock()
        guard let index=slots.indices.first(where:{$0 != latest && slots[$0].readers==0}) else{dropped+=1;lock.unlock();return}
        slots[index].readers = -1 // reserved by the producer; never selected by display
        let slot=slots[index];lock.unlock()
        slot.image.replace(region:MTLRegionMake2D(0,0,800,600),mipmapLevel:0,withBytes:pixels,bytesPerRow:800)
        slot.palette.contents().copyMemory(from:rgb,byteCount:768)
        lock.lock();slots[index].readers=0;latest=index;latestFrame=frame;published+=1
        uploadSeconds+=ProcessInfo.processInfo.systemUptime-started;lock.unlock()
    }
    func start(at time:Double) {
        stop()
        lock.lock();epoch &+= 1;measurementStart=time;presentedCount=0;presented.removeAll(keepingCapacity:true);uniqueGameFrames=0;lastPresentedFrame=nil
        published=0;dropped=0;submitted=0;uploadSeconds=0;submitSeconds=0;gpuSeconds=0;drawableWaitSeconds=0;failure=nil;lock.unlock()
        let timer=DispatchSource.makeTimerSource(queue:queue)
        timer.schedule(deadline:.now(),repeating:1.0/120,leeway:.microseconds(100))
        timer.setEventHandler{[weak self] in autoreleasepool{self?.draw()}}
        self.timer=timer;timer.resume()
    }
    func stop() {
        timer?.cancel();timer=nil
        queue.sync{} // never called by the display queue
        // Drain GPU readers only at pause/reset/capture, never per game frame.
        if let barrier=commands.makeCommandBuffer(){barrier.commit();barrier.waitUntilCompleted()}
    }
    func draw() {
        lock.lock()
        guard let index=latest,failure==nil else{lock.unlock();return}
        slots[index].readers+=1;let slot=slots[index],frame=latestFrame,epoch=self.epoch;lock.unlock()
        let started=ProcessInfo.processInfo.systemUptime
        guard let drawable=layer.nextDrawable(),let command=commands.makeCommandBuffer() else{
            lock.lock();slots[index].readers-=1;failure="MetalDrawableUnavailable";lock.unlock();return
        }
        let acquired=ProcessInfo.processInfo.systemUptime
        let pass=MTLRenderPassDescriptor();pass.colorAttachments[0].texture=drawable.texture
        pass.colorAttachments[0].loadAction = .dontCare;pass.colorAttachments[0].storeAction = .store
        guard let encoder=command.makeRenderCommandEncoder(descriptor:pass) else{
            lock.lock();slots[index].readers-=1;failure="MetalEncoderUnavailable";lock.unlock();return
        }
        encoder.setRenderPipelineState(pipeline);encoder.setFragmentTexture(slot.image,index:0);encoder.setFragmentBuffer(slot.palette,offset:0,index:0)
        encoder.drawPrimitives(type:.triangle,vertexStart:0,vertexCount:3);encoder.endEncoding()
        drawable.addPresentedHandler{[weak self] drawable in
            guard let self=self else{return};self.lock.lock()
            guard self.epoch==epoch,drawable.presentedTime>=self.measurementStart else{self.lock.unlock();return}
            self.presentedCount+=1;self.presented.append(drawable.presentedTime);if self.presented.count>16384{self.presented.removeFirst(8192)};if self.lastPresentedFrame != frame{self.uniqueGameFrames+=1;self.lastPresentedFrame=frame};self.lock.unlock()
        }
        command.addCompletedHandler{[weak self] result in
            guard let self=self else{return};self.lock.lock();self.slots[index].readers-=1
            if result.status != .completed{self.failure="MetalCommandFailed: \(result.error?.localizedDescription ?? "GPU command failed")"}
            self.gpuSeconds+=max(0,result.gpuEndTime-result.gpuStartTime);self.lock.unlock()
        }
        command.present(drawable);command.commit()
        lock.lock();lastTexture=drawable.texture;submitted+=1;drawableWaitSeconds+=acquired-started;submitSeconds+=ProcessInfo.processInfo.systemUptime-acquired;lock.unlock()
    }
    func clear(){lock.lock();latest=nil;lock.unlock()}
    func currentFailure()->String?{lock.lock();defer{lock.unlock()};return failure}
    func metrics(start:Double,end:Double,detailed:Bool=false)->[String:Any] {
        lock.lock();defer{lock.unlock()}
        // Actual CAMetalDrawable presentation timestamps, not timer/submit counts.
        let times=presented.filter{$0>=start && $0<=end},seconds=max(0.000001,end-start)
        let firstBin=presentedCount>presented.count ? max(0,Int((presented.first ?? start)-start)+1):0
        let count=presentedCount-presented.filter{$0>end}.count
        let bins=(firstBin..<(detailed ? max(firstBin,Int(seconds)):firstBin)).map{b in times.filter{$0>=start+Double(b) && $0<start+Double(b+1)}.count}
        return ["presented":count,"displayFPS":Double(count)/seconds,"minOneSecondFPS":bins.min() ?? 0,"oneSecondPresentations":bins,"traceFirstSecond":firstBin,
                "uniqueGameFramesPresented":uniqueGameFrames,"published":published,"publicationDrops":dropped,"submitted":submitted,
                "uploadSeconds":uploadSeconds,"submitSeconds":submitSeconds,"drawableWaitSeconds":drawableWaitSeconds,"gpuSeconds":gpuSeconds,"displayError":failure as Any? ?? NSNull()]
    }
}

final class NativeMetalGameView: NSView {
    let device: MTLDevice
    let commands: MTLCommandQueue
    let pipeline: MTLRenderPipelineState
    let indexed: MTLTexture
    let palette: MTLBuffer
    var presentedFrames=0
    var playPresenter:NativePlayPresenter?
    var testPresented=[Double]()
    let testLock=NSLock()
    var lastTexture: MTLTexture?
    var inputEvent: (([String:Any])->Void)?
    var tracking: NSTrackingArea?
    var heldKeys=Set<Int>()
    override var acceptsFirstResponder: Bool { true }
    override func updateTrackingAreas() {
        super.updateTrackingAreas();if let area=tracking{removeTrackingArea(area)}
        let area=NSTrackingArea(rect:.zero,options:[.mouseMoved,.activeInKeyWindow,.inVisibleRect],owner:self,userInfo:nil)
        tracking=area;addTrackingArea(area)
    }
    func mouse(_ event:NSEvent,_ message:Int) {
        let p=convert(event.locationInWindow,from:nil)
        guard bounds.contains(p),bounds.width>0,bounds.height>0 else{return}
        synchronizeModifiers(event.modifierFlags)
        if message != 0x200{window?.makeFirstResponder(self)}
        let w=(event.modifierFlags.contains(.shift) ? 4:0)|(event.modifierFlags.contains(.control) ? 8:0)
        inputEvent?(["kind":"mouse","msg":message,"x":Int(p.x*800/bounds.width),"y":min(599,Int((bounds.height-p.y)*600/bounds.height)),"wParam":w])
    }
    override func mouseMoved(with event:NSEvent){mouse(event,0x200)}
    override func mouseDragged(with event:NSEvent){mouse(event,0x200)}
    override func rightMouseDragged(with event:NSEvent){mouse(event,0x200)}
    override func mouseDown(with event:NSEvent){mouse(event,event.clickCount>1 && event.clickCount%2==0 ? 0x203:0x201)}
    override func mouseUp(with event:NSEvent){mouse(event,0x202)}
    override func rightMouseDown(with event:NSEvent){mouse(event,event.buttonNumber==0 ? 0x201:0x204)}
    override func rightMouseUp(with event:NSEvent){mouse(event,event.buttonNumber==0 ? 0x202:0x205)}
    func key(_ key:Int,_ down:Bool){if down{heldKeys.insert(key)}else{heldKeys.remove(key)};inputEvent?(["kind":"key","vkey":key,"down":down])}
    override func keyDown(with event:NSEvent){synchronizeModifiers(event.modifierFlags);if let k=[36:13,76:13,53:27,49:32,123:37,126:38,124:39,125:40,117:46,7:88,29:48,18:49,19:50,20:51,21:52,23:53,22:54,26:55,28:56,25:57][Int(event.keyCode)]{key(k,true)}}
    override func keyUp(with event:NSEvent){synchronizeModifiers(event.modifierFlags);if let k=[36:13,76:13,53:27,49:32,123:37,126:38,124:39,125:40,117:46,7:88,29:48,18:49,19:50,20:51,21:52,23:53,22:54,26:55,28:56,25:57][Int(event.keyCode)]{key(k,false)}}
    func synchronizeModifiers(_ flags:NSEvent.ModifierFlags){for (flag,k) in [(NSEvent.ModifierFlags.shift,16),(.control,17),(.option,18)]{let down=flags.contains(flag);if down != heldKeys.contains(k){key(k,down)}}}
    override func flagsChanged(with event:NSEvent){synchronizeModifiers(event.modifierFlags)}
    override func resignFirstResponder()->Bool{releaseKeys();return super.resignFirstResponder()}
    func releaseKeys(){for k in heldKeys.sorted(){key(k,false)}}
    override var wantsUpdateLayer: Bool { true }
    override func makeBackingLayer() -> CALayer { CAMetalLayer() }
    init(nativeFrame:NSRect) throws {
        guard let device=MTLCreateSystemDefaultDevice(),let commands=device.makeCommandQueue() else { throw NSError(domain:"MetalUnavailable",code:1) }
        self.device=device;self.commands=commands
        let source="""
        #include <metal_stdlib>
        using namespace metal;
        struct V { float4 position [[position]]; float2 uv; };
        vertex V vert(uint id [[vertex_id]]) {
            float2 p[3]={float2(-1,-1),float2(3,-1),float2(-1,3)};
            V o;o.position=float4(p[id],0,1);o.uv=float2(p[id].x*.5+.5,.5-p[id].y*.5);return o;
        }
        fragment float4 frag(V v [[stage_in]],texture2d<uint> image [[texture(0)]],device const uchar *palette [[buffer(0)]]) {
            uint2 p=min(uint2(clamp(v.uv,0.0,1.0)*float2(800,600)),uint2(799,599));
            uint i=image.read(p).r*3;return float4(float3(palette[i],palette[i+1],palette[i+2])/255.0,1);
        }
        """
        let library=try device.makeLibrary(source:source,options:nil)
        let descriptor=MTLRenderPipelineDescriptor();descriptor.vertexFunction=library.makeFunction(name:"vert");descriptor.fragmentFunction=library.makeFunction(name:"frag");descriptor.colorAttachments[0].pixelFormat = .bgra8Unorm
        pipeline=try device.makeRenderPipelineState(descriptor:descriptor)
        let texture=MTLTextureDescriptor.texture2DDescriptor(pixelFormat:.r8Uint,width:800,height:600,mipmapped:false);texture.storageMode = .shared;texture.usage = .shaderRead
        guard let indexed=device.makeTexture(descriptor:texture),let palette=device.makeBuffer(length:768,options:.storageModeShared) else { throw NSError(domain:"MetalAllocationFailed",code:1) }
        self.indexed=indexed;self.palette=palette
        super.init(frame:nativeFrame);wantsLayer=true;isHidden=true
        guard let metal=layer as? CAMetalLayer else { throw NSError(domain:"MetalLayerUnavailable",code:1) }
        metal.device=device;metal.pixelFormat = .bgra8Unorm;metal.framebufferOnly=false;metal.displaySyncEnabled=true
    }
    override func layout(){super.layout();updateDrawableSize()}
    override func viewDidChangeBackingProperties(){super.viewDidChangeBackingProperties();updateDrawableSize()}
    func updateDrawableSize(){guard let metal=layer as? CAMetalLayer else{return};let scale=window?.backingScaleFactor ?? 1;metal.drawableSize=CGSize(width:max(1,bounds.width*scale),height:max(1,bounds.height*scale))}
    func makePlayPresenter() throws -> NativePlayPresenter {
        if let presenter=playPresenter{return presenter}
        guard let layer=layer as? CAMetalLayer else{throw NSError(domain:"MetalLayerUnavailable",code:1)}
        let presenter=try NativePlayPresenter(layer:layer,device:device,commands:commands,pipeline:pipeline);playPresenter=presenter;return presenter
    }
    required init?(coder:NSCoder){fatalError("init(coder:) unavailable")}
    func present(_ pixels:UnsafePointer<UInt8>,_ rgb:UnsafePointer<UInt8>) throws {
        guard let metal=layer as? CAMetalLayer else { throw NSError(domain:"MetalLayerUnavailable",code:1) }
        let scale=window?.backingScaleFactor ?? 1
        metal.drawableSize=CGSize(width:max(1,bounds.width*scale),height:max(1,bounds.height*scale))
        guard let drawable=metal.nextDrawable(),let command=commands.makeCommandBuffer() else { throw NSError(domain:"MetalDrawableUnavailable",code:1) }
        indexed.replace(region:MTLRegionMake2D(0,0,800,600),mipmapLevel:0,withBytes:pixels,bytesPerRow:800)
        palette.contents().copyMemory(from:rgb,byteCount:768)
        let pass=MTLRenderPassDescriptor();pass.colorAttachments[0].texture=drawable.texture;pass.colorAttachments[0].loadAction = .clear;pass.colorAttachments[0].storeAction = .store
        guard let encoder=command.makeRenderCommandEncoder(descriptor:pass) else { throw NSError(domain:"MetalEncoderUnavailable",code:1) }
        encoder.setRenderPipelineState(pipeline);encoder.setFragmentTexture(indexed,index:0);encoder.setFragmentBuffer(palette,offset:0,index:0);encoder.drawPrimitives(type:.triangle,vertexStart:0,vertexCount:3);encoder.endEncoding()
        drawable.addPresentedHandler{[weak self] d in guard let self=self else{return};self.testLock.lock();self.testPresented.append(d.presentedTime);self.testLock.unlock()}
        command.present(drawable);command.commit();command.waitUntilCompleted()
        guard command.status == .completed else { throw NSError(domain:"MetalCommandFailed",code:1,userInfo:[NSLocalizedDescriptionKey:command.error?.localizedDescription ?? "GPU command failed"]) }
        lastTexture=drawable.texture;presentedFrames+=1
    }
    func testMetrics(start:Double,end:Double,detailed:Bool)->[String:Any]{
        testLock.lock();defer{testLock.unlock()}
        let seconds=max(0.000001,end-start),times=testPresented.filter{$0>=start && $0<=end}
        let bins=(0..<(detailed ? max(0,Int(seconds)):0)).map{b in times.filter{$0>=start+Double(b) && $0<start+Double(b+1)}.count}
        return ["presented":times.count,"displayFPS":Double(times.count)/seconds,"minOneSecondFPS":bins.min() ?? 0,"oneSecondPresentations":bins]
    }
    // Actual GPU readback, only after pausing; never part of per-frame transport.
    func capture(_ url:URL,pixels:UnsafePointer<UInt8>,palette:UnsafePointer<UInt8>) throws -> [String:Any] {
        guard let texture=lastTexture,let command=commands.makeCommandBuffer(),let encoder=command.makeBlitCommandEncoder() else { throw NSError(domain:"MetalReadbackUnavailable",code:1) }
        let row=((texture.width*4+255)/256)*256
        guard let buffer=device.makeBuffer(length:row*texture.height,options:.storageModeShared) else { throw NSError(domain:"MetalReadbackAllocation",code:1) }
        encoder.copy(from:texture,sourceSlice:0,sourceLevel:0,sourceOrigin:MTLOrigin(x:0,y:0,z:0),sourceSize:MTLSize(width:texture.width,height:texture.height,depth:1),to:buffer,destinationOffset:0,destinationBytesPerRow:row,destinationBytesPerImage:row*texture.height);encoder.endEncoding();command.commit();command.waitUntilCompleted()
        guard command.status == .completed else { throw NSError(domain:"MetalReadbackFailed",code:1) }
        let actual=buffer.contents().assumingMemoryBound(to:UInt8.self)
        var checked=0
        for y in 0..<texture.height { for x in 0..<texture.width {
            let sx=min(799,Int((Double(x)+0.5)*800/Double(texture.width))),sy=min(599,Int((Double(y)+0.5)*600/Double(texture.height)))
            let i=Int(pixels[sy*800+sx])*3,a=y*row+x*4
            guard actual[a]==palette[i+2] && actual[a+1]==palette[i+1] && actual[a+2]==palette[i] && actual[a+3]==255 else { throw NSError(domain:"MetalReadbackPixelMismatch",code:a) }
            checked+=1
        }}
        guard let bitmap=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:texture.width,pixelsHigh:texture.height,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:texture.width*4,bitsPerPixel:32),let out=bitmap.bitmapData else { throw NSError(domain:"MetalEvidenceAllocation",code:1) }
        for y in 0..<texture.height { for x in 0..<texture.width { let a=y*row+x*4,b=(y*texture.width+x)*4;out[b]=actual[a+2];out[b+1]=actual[a+1];out[b+2]=actual[a];out[b+3]=255 }}
        guard let data=bitmap.representation(using:.png,properties:[:]) else { throw NSError(domain:"MetalEvidenceEncoding",code:1) }
        try data.write(to:url,options:.atomic)
        return ["pixelsChecked":checked,"path":url.path,"sha256":SHA256.hash(data:data).map{String(format:"%02x",$0)}.joined()]
    }
}

final class NativeGameLayout:NSView {
    let game:NativeMetalGameView
    init(_ game:NativeMetalGameView){self.game=game;super.init(frame:NSRect(x:0,y:0,width:800,height:705));addSubview(game)}
    required init?(coder:NSCoder){fatalError("init(coder:) unavailable")}
    override func layout(){super.layout();let width=min(bounds.width,max(1,bounds.height-105)*4/3);game.frame=NSRect(x:(bounds.width-width)/2,y:105,width:width,height:width*3/4)}
}

final class NativeLiveWindow:NSObject,NSWindowDelegate {
    let root:URL
    let work=DispatchQueue(label:"risinglands.native.live",qos:.userInitiated)
    var validationMode:Bool
    var gameFPS=0.0
    var nextGameTime=0.0
    var runID:UInt64=0
    var presenter:NativePlayPresenter?
    let modeControl=NSSegmentedControl(labels:["Jogar","Validar"],trackingMode:.selectOne,target:nil,action:nil)
    let rateControl=NSPopUpButton(frame:.zero,pullsDown:false)
    let metal:NativeMetalGameView
    let window:NSWindow
    var driver:OpaquePointer?
    var running=false
    var stoppedReason:String?
    var metalSeconds=0.0
    var playStarted=0.0,playEnded=0.0
    var startFrames:UInt64=0,startLogic:UInt64=0,startRender:UInt64=0,startProof:UInt64=0
    var startMetal=0.0
    var lastNotify=0.0
    var update:(([String:Any])->Void)?
    var recordedEvent:(([String:Any])->Void)?
    var recordingAction:(()->Void)?
    var exportAction:(()->Void)?
    var recording=false
    var benchmarkInput=false
    var benchmarkOrderTags=[UInt32]()
    var orderBuffer=[UInt32](repeating:0,count:32)
    let recordButton=NSButton(title:"Nova gravação",target:nil,action:nil)
    let resetButton=NSButton(title:"Reiniciar",target:nil,action:nil)
    let label=NSTextField(labelWithString:"MONDE01 · Rust ABI 1.6 · sem entrada aplicada")
    let button=NSButton(title:"Executar",target:nil,action:nil)
    init(root:URL,validationMode:Bool=false) throws {
        self.validationMode=validationMode;self.root=root;metal=try NativeMetalGameView(nativeFrame:NSRect(x:0,y:105,width:800,height:600))
        window=NSWindow(contentRect:NSRect(x:0,y:0,width:800,height:705),styleMask:[.titled,.closable,.miniaturizable,.resizable],backing:.buffered,defer:false)
        super.init()
        window.acceptsMouseMovedEvents=true;window.title="MONDE01 · Rust e Metal";window.minSize=NSSize(width:640,height:550);window.contentView=NativeGameLayout(metal);window.delegate=self
        button.target=self;button.action=#selector(toggle);button.frame=NSRect(x:15,y:36,width:100,height:27)
        let stepButton=NSButton(title:"Avançar quadro",target:self,action:#selector(step));stepButton.frame=NSRect(x:125,y:36,width:140,height:27)
        resetButton.target=self;resetButton.action=#selector(reset);resetButton.frame=NSRect(x:275,y:36,width:100,height:27)
        label.frame=NSRect(x:15,y:8,width:770,height:22);label.autoresizingMask = [.width]
        window.contentView?.addSubview(button);window.contentView?.addSubview(stepButton);window.contentView?.addSubview(resetButton);window.contentView?.addSubview(label)
        recordButton.target=self;recordButton.action=#selector(toggleRecording);recordButton.frame=NSRect(x:385,y:36,width:170,height:27)
        recordButton.toolTip="Gravação de cliques e teclas; arrasto contínuo indisponível"
        let exportButton=NSButton(title:"Exportar entrada",target:self,action:#selector(exportRecording));exportButton.frame=NSRect(x:565,y:36,width:160,height:27)
        window.contentView?.addSubview(recordButton);window.contentView?.addSubview(exportButton)
        metal.inputEvent={ [weak self] event in
            guard let self=self else{return};let shouldRecord=self.recording
            // Worker stamps the next game frame; presentation rate never enters mapping.
            self.work.async{[weak self] in
                guard let self=self else{return};let frame=max(129,Int(self.status().frames)+1)
                if !self.validationMode {
                    let kind=event["kind"] as? String
                    let code=macos_live_event(self.driver,kind=="mouse" ? 1:2,UInt32(event["msg"] as? Int ?? 0),Int32(event["x"] as? Int ?? 0),Int32(event["y"] as? Int ?? 0),UInt32(event["wParam"] as? Int ?? 0),UInt32(event["vkey"] as? Int ?? 0),(event["down"] as? Bool ?? false) ? 1:0)
                    if code != 0{self.running=false;self.stoppedReason="Entrada recusada: \(self.message(self.status()))";self.deliver()}
                }
                DispatchQueue.main.async{if shouldRecord{self.recordedEvent?(["frame":frame,"event":event])}}
            }
        }
        modeControl.target=self;modeControl.action=#selector(changeMode);modeControl.selectedSegment=validationMode ? 1:0
        modeControl.frame=NSRect(x:15,y:66,width:190,height:25)
        rateControl.addItems(withTitles:["15 quadros/s","20 quadros/s","30 quadros/s","60 quadros/s","Original (sem limite)"]);rateControl.selectItem(at:4)
        rateControl.target=self;rateControl.action=#selector(changeRate);rateControl.frame=NSRect(x:220,y:66,width:225,height:25)
        rateControl.isEnabled = !validationMode;window.contentView?.addSubview(modeControl);window.contentView?.addSubview(rateControl)
        presenter=try metal.makePlayPresenter()
        window.center();window.makeKeyAndOrderFront(nil)
    }
    func benchmarkClick(_ x:Double,_ y:Double,right:Bool=false){
        window.makeKeyAndOrderFront(nil);window.makeFirstResponder(metal)
        let point=metal.convert(NSPoint(x:metal.bounds.width*x/800,y:metal.bounds.height*(1-y/600)),to:nil)
        for type in (right ? [NSEvent.EventType.rightMouseDown,.rightMouseUp]:[NSEvent.EventType.leftMouseDown,.leftMouseUp]){if let event=NSEvent.mouseEvent(with:type,location:point,modifierFlags:[],timestamp:ProcessInfo.processInfo.systemUptime,windowNumber:window.windowNumber,context:nil,eventNumber:1,clickCount:1,pressure:1){window.sendEvent(event)}}
    }
    func benchmarkPointer(_ x:Double,_ y:Double){
        let point=metal.convert(NSPoint(x:metal.bounds.width*x/800,y:metal.bounds.height*(1-y/600)),to:nil)
        if let event=NSEvent.mouseEvent(with:.mouseMoved,location:point,modifierFlags:[],timestamp:ProcessInfo.processInfo.systemUptime,windowNumber:window.windowNumber,context:nil,eventNumber:3,clickCount:0,pressure:0){window.sendEvent(event)}
    }
    @objc func changeMode(){let selected=modeControl.selectedSegment==1;rateControl.isEnabled = !selected;work.async{[weak self] in guard let self=self else{return};self.running=false;self.presenter?.stop();self.validationMode=selected;self.perform("live-reset",completion:nil)}}
    @objc func changeRate(){let rate=[15.0,20.0,30.0,60.0,0.0][rateControl.indexOfSelectedItem];work.async{[weak self] in self?.gameFPS=rate;self?.nextGameTime=ProcessInfo.processInfo.systemUptime}}
    @objc func toggleRecording(){inputBarrier{[weak self] frame in guard let self=self else{return};if frame<129 && !self.recording{self.label.stringValue="Gravação disponível após o quadro 128"}else{self.recordingAction?()}}}
    @objc func exportRecording(){exportAction?()}
    func setRecording(_ active:Bool){
        let starting=active && !recording
        if starting{metal.synchronizeModifiers(NSEvent.modifierFlags)}
        recording=active;modeControl.isEnabled = !active;resetButton.isEnabled = !active;recordButton.title=active ? "● Gravando entrada":"Nova gravação";recordButton.contentTintColor=active ? .systemRed:nil
        if starting{window.makeKeyAndOrderFront(nil);window.makeFirstResponder(metal)}
        if starting{let held=metal.heldKeys.sorted();inputBarrier{[weak self] frame in for key in held{self?.recordedEvent?(["frame":frame,"event":["kind":"key","vkey":key,"down":true]])}}}
    }
    func inputBarrier(_ completion:@escaping(Int)->Void){work.async{[weak self] in guard let self=self else{return};let frame=Int(self.status().frames)+1;DispatchQueue.main.async{completion(frame)}}}
    func windowDidResignKey(_ notification:Notification){metal.releaseKeys()}
    func create() throws {
        guard macos_live_abi_version()==1,macos_live_status_size()==MemoryLayout<MacOSLiveStatus>.size else { throw NSError(domain:"NativeDriverVersionMismatch",code:1) }
        let directory=root.appendingPathComponent("native-inputs")
        let manifest=try JSONSerialization.jsonObject(with:Data(contentsOf:directory.appendingPathComponent("manifest.json"))) as! [String:Any]
        for (name,expected) in manifest["files"] as! [String:String] {
            let data=try Data(contentsOf:directory.appendingPathComponent(name))
            guard SHA256.hash(data:data).map({String(format:"%02x",$0)}).joined()==expected else { throw NSError(domain:"NativeInputHashMismatch",code:1,userInfo:[NSLocalizedDescriptionKey:name]) }
        }
        var error=[CChar](repeating:0,count:512)
        let candidate=macos_live_create(root.appendingPathComponent("librising_engine.dylib").path,directory.path,&error,512)
        guard let candidate=candidate else { throw NSError(domain:"NativeInitialization",code:1,userInfo:[NSLocalizedDescriptionKey:String(cString:error)]) }
        guard macos_live_validation(candidate,validationMode ? 1:0)==0 else{macos_live_free(candidate);throw NSError(domain:"NativeValidationModeRejected",code:1)}
        let previous=driver;driver=candidate;if let previous=previous{macos_live_free(previous)}
    }
    func status()->MacOSLiveStatus { var value=MacOSLiveStatus();macos_live_status(driver,&value);return value }
    func message(_ value:MacOSLiveStatus)->String { var s=value;return withUnsafePointer(to:&s.message){$0.withMemoryRebound(to:CChar.self,capacity:512){String(cString:$0)}} }
    func snapshot()->[String:Any] {
        let s=status(),index=s.phase_index==UInt32.max ? -1:Int(s.phase_index)
        let name=index<0 ? "state_s0":index==0 ? "load_tail":"frame\(s.frames)"
        let elapsed=max(0.000001,(running ? ProcessInfo.processInfo.systemUptime:playEnded)-playStarted)
        let frames=s.frames>=startFrames ? s.frames-startFrames:0
        var timing:[String:Any]=["frames":frames,"seconds":elapsed,"fps":playStarted>0 ? Double(frames)/elapsed:0,"rustSeconds":Double(s.logic_ns-startLogic)/1e9,"renderSeconds":Double(s.render_ns-startRender)/1e9,"proofSeconds":Double(s.proof_ns-startProof)/1e9,"metalSeconds":metalSeconds-startMetal]
        timing["humanEvents"]=macos_live_human_events(driver);timing["declaredFrames"]=macos_live_declared_frames(driver)
        timing["gameFPS"]=validationMode ? 0:gameFPS;timing["executionMode"]=validationMode ? "test":"play"
        let end=running ? ProcessInfo.processInfo.systemUptime:playEnded
        if !validationMode,let presenter=presenter{timing.merge(presenter.metrics(start:playStarted,end:end,detailed:!running)){_,new in new}}
        else{timing.merge(metal.testMetrics(start:playStarted,end:end,detailed:!running)){_,new in new}}
        let stop:Any = s.stopped != 0 || stoppedReason != nil ? ["type":"NativeStop","phase":"frame\(s.frames+1)","detail":stoppedReason ?? message(s)]:NSNull()
        let equal:Any = s.stopped==0 && stoppedReason==nil && s.frames>0 && s.frames<=9200 && s.surfaces_equal>=s.frames ? true:NSNull()
        let sha=validationMode ? withUnsafeBytes(of:s.state_sha){$0.map{String(format:"%02x",$0)}.joined()}:""
        var phases=validationMode ? ["load_tail","between_frames","frame1"]:[String]()
        if validationMode{for i in 2...128{phases += ["between_frames\(i)","frame\(i)"]}}
        if s.frames>128{phases.append(name)}
        return ["mode":"live-rust-no-input","scenario":validationMode ? "MONDE01 · validação sem entrada":"MONDE01 · ordens ao vivo","phase":name,"phase_index":index,"phases":phases,
                "summary_sha256":index>=0 && index<=256 ? sha:"", "summary_verified":validationMode && s.stopped==0 && index>=0 && index<=256,
                "checkpoint_verified":false,"verified_phases":s.phases_equal,"verified_checkpoints":s.checkpoints_equal,"verified_surfaces":s.surfaces_equal,
                "observed":["counter":["address":"0x508f7c","bytes":4,"value":s.counter]],"blocks":0,"bytes":0,"memory":[],"input_policy":validationMode ? "record-only":"live-orders","live_stop":stop,
                "benchmark_order_tags":benchmarkOrderTags,"execution_mode":validationMode ? "test":"play","native_metal":true,"native_engine_binding":macos_live_engine_binding()==1 ? "static-abi16":"dynamic-abi16","native_running":running,"native_metrics":timing,
                "render":["status":s.disposition==2 ? "partial":s.frames==0 ? "undrawn":"full","hud":true,"version":[1,9],"backend":"Rust ABI 1.6 + Metal","equals_native_phase_end":equal,"native_phase_end_sha256":NSNull()]]
    }
    func deliver(_ completion:(([String:Any])->Void)?=nil){
        let value=snapshot(),s=status(),isRunning=running
        let caption="\(validationMode ? "Validar":"Jogar · \(gameFPS==0 ? "sem limite":String(format:"%.0f q/s",gameFPS))") · Quadro \(s.frames) · \(running ? "executando":"pausado")" + (stoppedReason != nil || s.stopped != 0 ? " · Parada: \(stoppedReason ?? message(s))":validationMode ? " · sem entrada aplicada":" · ordens após q128 · áudio/texto: limites declarados")
        DispatchQueue.main.async { [weak self] in
            guard let self=self else{return};var value=value;value["native_window_visible"]=self.window.isVisible
            self.button.title=isRunning ? "Pausar":"Executar"
            let fps=(value["native_metrics"] as? [String:Any])?["displayFPS"] as? Double ?? 0
            self.label.stringValue=caption+(isRunning ? String(format:" · tela %.1f fps",fps):"")
            if let completion=completion{completion(value)}else{self.update?(value)}
        }
    }
    func advance(){
        let code=macos_live_advance(driver,nil,nil),s=status()
        if benchmarkInput && code==0 && s.frames>128 {
            let count=macos_live_order_tags(driver,&orderBuffer,32)
            if count==UInt32.max{stoppedReason="Diagnóstico de entrada: \(message(status()))";running=false}
            else if count>0{benchmarkOrderTags.append(contentsOf:orderBuffer.prefix(Int(count)))}
        }
        if code != 0 {running=false;playEnded=ProcessInfo.processInfo.systemUptime}
        if s.phase_index != UInt32.max,let pixels=macos_live_pixels(driver),let palette=macos_live_palette(driver) {
            if !validationMode {
                presenter?.publish(pixels,palette,frame:s.frames)
                if let error=presenter?.currentFailure(){stoppedReason=error;running=false;playEnded=ProcessInfo.processInfo.systemUptime}
            } else {
                let started=ProcessInfo.processInfo.systemUptime
                DispatchQueue.main.sync { [weak self] in
                    guard let self=self else{return}
                    do {self.metal.isHidden=false;try self.metal.present(pixels,palette)}catch{self.stoppedReason="Metal: \(error.localizedDescription)";self.running=false;self.playEnded=ProcessInfo.processInfo.systemUptime}
                }
                metalSeconds+=ProcessInfo.processInfo.systemUptime-started
            }
        }
    }
    func pump(_ run:UInt64){
        guard running,run==runID else{return}
        let now=ProcessInfo.processInfo.systemUptime
        if !validationMode && gameFPS>0 && now<nextGameTime{work.asyncAfter(deadline:.now()+(nextGameTime-now)){[weak self] in self?.pump(run)};return}
        advance()
        if !validationMode && gameFPS>0{nextGameTime+=1/gameFPS}
        let finished=ProcessInfo.processInfo.systemUptime
        if finished-lastNotify>=0.1 || !running{lastNotify=finished;deliver()}
        if running{work.async{[weak self] in self?.pump(run)}}else{presenter?.stop()}
    }
    @objc func toggle(){perform("live-play",completion:nil)}
    @objc func step(){perform("live-step",completion:nil)}
    @objc func reset(){perform("live-reset",completion:nil)}
    func perform(_ operation:String,completion:(([String:Any])->Void)?){
        work.async { [weak self] in
            guard let self=self else{return}
            switch operation {
            case "live-play":
                if self.running{self.running=false;self.playEnded=ProcessInfo.processInfo.systemUptime}
                else if self.status().stopped==0 && self.stoppedReason==nil{
                    let s=self.status();self.startFrames=s.frames;self.startLogic=s.logic_ns;self.startRender=s.render_ns;self.startProof=s.proof_ns;self.startMetal=self.metalSeconds;self.playStarted=ProcessInfo.processInfo.systemUptime;self.playEnded=self.playStarted;self.running=true
                    if !self.validationMode{self.presenter?.start(at:self.playStarted);DispatchQueue.main.async{self.metal.isHidden=false;self.window.makeFirstResponder(self.metal)}}
                    self.runID &+= 1;let run=self.runID;self.nextGameTime=self.playStarted;self.work.async{[weak self] in self?.pump(run)}
                }
            case "live-pause":self.running=false;self.playEnded=ProcessInfo.processInfo.systemUptime
            case "live-step":if !self.running && self.stoppedReason==nil{self.advance();if !self.validationMode,let pixels=macos_live_pixels(self.driver),let palette=macos_live_palette(self.driver){DispatchQueue.main.sync{do{self.metal.isHidden=false;try self.metal.present(pixels,palette)}catch{self.stoppedReason="Metal: \(error.localizedDescription)"}}}}
            case "live-reset":
                self.running=false;self.presenter?.stop();self.presenter?.clear()
                do{try self.create();DispatchQueue.main.async{self.metal.isHidden=true};self.stoppedReason=nil;self.playStarted=0;self.playEnded=0;self.startFrames=0;self.startLogic=0;self.startRender=0;self.startProof=0;self.startMetal=self.metalSeconds}catch{self.stoppedReason=error.localizedDescription}
            default:break
            }
            if !self.running{self.presenter?.stop()}
            self.deliver(completion)
        }
    }
    func read(_ address:UInt32,_ size:Int,completion:@escaping([String:Any])->Void){
        work.async{[weak self] in guard let self=self else{return};guard self.validationMode else{DispatchQueue.main.async{completion(["error":"Leitura de memória disponível no modo Validar."])};return};var data=[UInt8](repeating:0,count:size);let code=macos_live_read(self.driver,address,UInt32(size),&data);DispatchQueue.main.async{completion(code==0 ? ["read_hex":data.map{String(format:"%02x",$0)}.joined()]:["error":"Leitura nativa recusada: \(code)"])}}
    }
    func capture(_ url:URL,completion:@escaping([String:Any])->Void){
        work.async{[weak self] in
            guard let self=self else{return};self.running=false;self.playEnded=ProcessInfo.processInfo.systemUptime;self.presenter?.stop()
            guard let pixels=macos_live_pixels(self.driver),let palette=macos_live_palette(self.driver) else{DispatchQueue.main.async{completion(["error":"NativePixelsUnavailable"])};return}
            if !self.validationMode,let presenter=self.presenter{
                // Capture the actual play texture/upload/shader path. Draining makes a
                // free slot available even if the last timed publication was dropped.
                presenter.publish(pixels,palette,frame:self.status().frames)
                presenter.queue.sync{presenter.draw()};presenter.stop()
            }
            DispatchQueue.main.sync {
                do{
                    if !self.validationMode{
                        guard let texture=self.presenter?.lastTexture else{throw NSError(domain:"MetalPlayReadbackUnavailable",code:1)}
                        self.metal.lastTexture=texture
                    }
                    var result=try self.metal.capture(url,pixels:pixels,palette:palette)
                    result["transport"]=self.validationMode ? "validation-texture":"async-slot-texture";completion(result)
                }catch{completion(["error":error.localizedDescription])}
            }
        }
    }
    func windowShouldClose(_ sender:NSWindow)->Bool {perform("live-pause",completion:nil);window.orderOut(nil);return false}
}
