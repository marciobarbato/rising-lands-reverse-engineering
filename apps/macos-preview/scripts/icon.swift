import AppKit
let dir=URL(fileURLWithPath:CommandLine.arguments[1],isDirectory:true)
for size in [16,32,64,128,256,512,1024] {
 let rep=NSBitmapImageRep(bitmapDataPlanes:nil,pixelsWide:size,pixelsHigh:size,bitsPerSample:8,samplesPerPixel:4,hasAlpha:true,isPlanar:false,colorSpaceName:.deviceRGB,bytesPerRow:0,bitsPerPixel:0)!
 NSGraphicsContext.saveGraphicsState();NSGraphicsContext.current=NSGraphicsContext(bitmapImageRep:rep)
 let s=CGFloat(size)
 let bg=NSBezierPath(roundedRect:NSRect(x:0,y:0,width:s,height:s),xRadius:s*0.22,yRadius:s*0.22)
 NSColor(calibratedRed:0.08,green:0.12,blue:0.11,alpha:1).setFill();bg.fill()
 let p=NSBezierPath();p.move(to:NSPoint(x:s*0.18,y:s*0.22));p.line(to:NSPoint(x:s*0.18,y:s*0.72));p.line(to:NSPoint(x:s*0.78,y:s*0.72));p.lineWidth=s*0.025
 NSColor(calibratedRed:0.7,green:0.83,blue:0.43,alpha:1).setStroke();p.stroke()
 let text="RL" as NSString
 text.draw(at:NSPoint(x:s*0.25,y:s*0.23),withAttributes:[.font:NSFont.systemFont(ofSize:s*0.35,weight:.bold),.foregroundColor:NSColor(calibratedRed:0.77,green:0.9,blue:0.55,alpha:1)])
 NSGraphicsContext.restoreGraphicsState()
 let data=rep.representation(using:.png,properties:[:])!
 try data.write(to:dir.appendingPathComponent("s\(size).png"))
}
