// Real Swift output buffers and Metal upload/conversion; no Python per frame.
import Foundation
import CoreFoundation
import CryptoKit
import Metal
import RisingEngine
func check(_ code: Int32) {
    if code != 0 {
        var n: UInt32 = 0
        _ = rl_erro_mensagem(nil, 0, &n)
        var text = [UInt8](repeating: 0, count: Int(n))
        text.withUnsafeMutableBufferPointer { _ = rl_erro_mensagem($0.baseAddress, UInt32($0.count), &n) }
        fatalError("ABI \(code): \(String(bytes: text.dropLast(), encoding: .utf8) ?? "")")
    }
}
struct Input {
    var bytes: Data
    var offset = 8
    mutating func u32() -> UInt32 {
        defer { offset += 4 }
        return bytes.withUnsafeBytes { UInt32(littleEndian: $0.loadUnaligned(fromByteOffset: offset, as: UInt32.self)) }
    }
    mutating func blob() -> Data {
        let size = Int(u32()); defer { offset += size }
        return bytes.subdata(in: offset..<offset+size)
    }
}
func descriptor(_ d: NSData) -> RlRenderBytes { RlRenderBytes(data: d.bytes.assumingMemoryBound(to: UInt8.self), length: UInt32(d.length)) }
var input = Input(bytes: try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[1])))
precondition(input.bytes.prefix(8) == Data("RLSW1300".utf8))
let assets = (0..<9).map { _ in input.blob() as NSData }
let count = Int(input.u32())
var blocks = [RlBloco](), backing = [NSData]()
for _ in 0..<count {
    let base = input.u32(), data = input.blob() as NSData
    backing.append(data); blocks.append(RlBloco(address: base, length: UInt32(data.length), data: data.bytes.assumingMemoryBound(to: UInt8.self)))
}
let frameData = input.blob(), registerData = input.blob()
var frame = frameData.withUnsafeBytes { $0.loadUnaligned(as: RlFrameInput.self) }
let firstRegisters = registerData.withUnsafeBytes { $0.loadUnaligned(as: RlFrameRegisters.self) }
let initialSurface = input.blob() as NSData, keys = input.blob() as NSData, payloads = input.blob() as NSData
let cursor = input.u32()
let hashes = String(data: input.blob(), encoding: .utf8)!.split(separator: "\n").map(String.init)
precondition(input.offset == input.bytes.count)
var world: RlMundo = 0
check(rl_criar_mundo(RL_ABI_VERSION, 20, 0, &world))
defer { check(rl_liberar_mundo(world)) }
blocks.withUnsafeBufferPointer { check(rl_carregar_blocos(world, $0.baseAddress, UInt32($0.count))) }
check(rl_passo_quadro(world, UInt32(RL_LOAD_TAIL), &frame))
frame.registers = firstRegisters
var surfaceDesc = descriptor(initialSurface), cache = RlRenderCache(keys: descriptor(keys), payloads: descriptor(payloads), cursor: cursor)
var renderer: RlRenderer = 0
let assetDescriptors = assets.map(descriptor)
assetDescriptors.withUnsafeBufferPointer { check(rl_render_criar(world, $0.baseAddress, 9, &surfaceDesc, &cache, &renderer)) }
defer { check(rl_render_liberar(renderer)) }
var pixels = [UInt8](repeating: 0, count: 480000), palette = [UInt8](repeating: 0, count: 768)
var result = RlRenderResult(), generation: UInt64 = 0, phase: UInt32 = 0, counter: UInt32 = 0
check(rl_render_geracao(world, &generation, &phase, &counter))
precondition(phase == 1 && counter == 0)
precondition(rl_render_quadro(renderer, generation, 1, nil, 0, nil, 0, &result) == RL_BUFFER_TOO_SMALL)
precondition(result.required_pixels == 480000 && result.required_palette == 768)
precondition(rl_render_quadro(renderer, generation+1, 1, nil, 0, nil, 0, &result) == RL_STALE_GENERATION)
let device = MTLCreateSystemDefaultDevice()!
let queue = device.makeCommandQueue()!
let source = """
#include <metal_stdlib>
using namespace metal;
kernel void convert(texture2d<uint,access::read> indexed [[texture(0)]],
 device const uchar *palette [[buffer(0)]], texture2d<float,access::write> rgba [[texture(1)]],
 uint2 p [[thread_position_in_grid]]) {
 if (p.x >= 800 || p.y >= 600) return;
 uint i=indexed.read(p).r*3;
 rgba.write(float4(float3(palette[i],palette[i+1],palette[i+2])/255.0,1),p);
}
"""
let library = try device.makeLibrary(source: source, options: nil)
let pipeline = try device.makeComputePipelineState(function: library.makeFunction(name: "convert")!)
let indexedDesc = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: .r8Uint, width: 800, height: 600, mipmapped: false)
indexedDesc.storageMode = .shared; indexedDesc.usage = .shaderRead
let indexed = device.makeTexture(descriptor: indexedDesc)!
let rgbaDesc = MTLTextureDescriptor.texture2DDescriptor(pixelFormat: .rgba8Unorm, width: 800, height: 600, mipmapped: false)
rgbaDesc.storageMode = .shared; rgbaDesc.usage = [.shaderWrite,.shaderRead]
let rgba = device.makeTexture(descriptor: rgbaDesc)!
let paletteBuffer = device.makeBuffer(length: 768, options: .storageModeShared)!
let region = MTLRegionMake2D(0,0,800,600)
var elapsed = 0.0, renderElapsed = 0.0, logicElapsed = 0.0, transferElapsed = 0.0
for index in 0..<hashes.count {
    let start = CFAbsoluteTimeGetCurrent()
    check(rl_render_geracao(world, &generation, &phase, &counter))
    precondition(counter == UInt32(index))
    let r0 = CFAbsoluteTimeGetCurrent()
    pixels.withUnsafeMutableBufferPointer { p in palette.withUnsafeMutableBufferPointer { pal in
        check(rl_render_quadro(renderer, generation, 1, p.baseAddress, UInt32(p.count), pal.baseAddress, UInt32(pal.count), &result))
    }}
    let r1 = CFAbsoluteTimeGetCurrent(); renderElapsed += r1-r0
    precondition(result.disposition == 0 && result.stop_address == 0 && result.generation == generation && result.palette_generation == 1)
    pixels.withUnsafeBytes { indexed.replace(region: region, mipmapLevel: 0, withBytes: $0.baseAddress!, bytesPerRow: 800) }
    palette.withUnsafeBytes { paletteBuffer.contents().copyMemory(from: $0.baseAddress!, byteCount: 768) }
    let command = queue.makeCommandBuffer()!, encoder = command.makeComputeCommandEncoder()!
    encoder.setComputePipelineState(pipeline); encoder.setTexture(indexed, index: 0); encoder.setTexture(rgba, index: 1); encoder.setBuffer(paletteBuffer, offset: 0, index: 0)
    encoder.dispatchThreads(MTLSize(width: 800,height: 600,depth: 1), threadsPerThreadgroup: MTLSize(width: 16,height: 16,depth: 1))
    encoder.endEncoding(); command.commit(); command.waitUntilCompleted()
    precondition(command.status == .completed)
    let t1 = CFAbsoluteTimeGetCurrent(); transferElapsed += t1-r1
    check(rl_passo_quadro(world, UInt32(RL_BETWEEN_FRAMES), &frame))
    check(rl_passo_quadro(world, UInt32(RL_FRAME), &frame))
    let finish = CFAbsoluteTimeGetCurrent(); logicElapsed += finish-t1; elapsed += finish-start
    let digest = SHA256.hash(data: Data(pixels)).map { String(format:"%02x",$0) }.joined()
    precondition(digest == hashes[index], "Swift pixel mismatch at \(index+1)")
    if index == 0 || index == hashes.count-1 {
        var readback = [UInt8](repeating:0,count:1920000)
        readback.withUnsafeMutableBytes { rgba.getBytes($0.baseAddress!,bytesPerRow:3200,from:region,mipmapLevel:0) }
        for p in 0..<480000 { let i=Int(pixels[p])*3; precondition(readback[p*4] == palette[i] && readback[p*4+1] == palette[i+1] && readback[p*4+2] == palette[i+2] && readback[p*4+3] == 255) }
    }
}
let report: [String:Any] = ["abi":"1.4","frames_equal":hashes.count,"render_seconds":renderElapsed,"logic_seconds":logicElapsed,"metal_upload_conversion_seconds":transferElapsed,"pipeline_seconds":elapsed,"render_fps":Double(hashes.count)/renderElapsed,"engine_render_metal_fps":Double(hashes.count)/elapsed,"metal_device":device.name,"scope":"Swift C ABI engine+render+generation+reused output buffers+Metal upload and RGBA conversion; excludes proof hashing/readback, initialization and app display pacing"]
let json = try JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys])
print(String(data:json,encoding:.utf8)!)
