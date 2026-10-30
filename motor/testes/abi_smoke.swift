// CLI interoperability proof only. This does not change the macOS app.
import RisingEngine
var world: RlMundo = 0
precondition(rl_versao() == RL_ABI_VERSION)
precondition(rl_criar_mundo(rl_versao(), 20, 0, &world) == 0)
defer { precondition(rl_liberar_mundo(world) == 0) }
let seed: [UInt8] = [1, 0, 0, 0]
seed.withUnsafeBufferPointer { bytes in
    var block = RlBloco(address: 0x497164, length: 4, data: bytes.baseAddress!)
    precondition(rl_carregar_blocos(world, &block, 1) == 0)
}
var registers = RlRegisters(eax: 0, ebx: 1, ecx: 2, edx: 3, esi: 4, edi: 5, ebp: 6)
precondition(rl_executar_rotina(world, UInt32(RL_RANDOM), &registers) == 0)
precondition(registers.eax == 16807 && registers.edx == 3)
var address: UInt32 = 0
var required: UInt32 = 0
precondition(rl_projetar_bloco(world, 0, &address, nil, 0, &required) == RL_BUFFER_TOO_SMALL)
var output = [UInt8](repeating: 0, count: Int(required))
output.withUnsafeMutableBufferPointer { bytes in
    precondition(rl_projetar_bloco(world, 0, &address, bytes.baseAddress!, UInt32(bytes.count), &required) == 0)
}
precondition(address == 0x497164 && output == [0xa7, 0x41, 0, 0])
precondition(rl_avancar_ticks(world, 20) == 0)
var tick: UInt64 = 0
var milliseconds: UInt32 = 0
precondition(rl_relogio(world, &tick, &milliseconds) == 0)
precondition(tick == 20 && milliseconds == 1000)
// A successful sparse between-frame phase exercises the new struct layouts,
// pointer contract, virtual clock, event query and copied bulk projection.
let frameBase = 0x494000
var frameBytes = [UInt8](repeating: 0, count: 0x50a000-frameBase)
frameBytes[0x4e2f78-frameBase] = 0x12
frameBytes[0x497284-frameBase] = 2
frameBytes[0x508f7c-frameBase] = 1
frameBytes[0x49a058-frameBase] = 1
frameBytes.withUnsafeBufferPointer { bytes in
    var block = RlBloco(address: UInt32(frameBase), length: UInt32(bytes.count), data: bytes.baseAddress!)
    precondition(rl_carregar_blocos(world, &block, 1) == 0)
}
var frame = RlFrameInput()
frame.cursor_x = 24; frame.cursor_y = 36
frame.registers.esp = 0x3000100
precondition(rl_passo_quadro(world, UInt32(RL_BETWEEN_FRAMES), &frame) == 0)
precondition(frame.registers.eax == 36 && frame.registers.ebx == 3)
precondition(frame.registers.edx == 0x3000100 && frame.registers.esp == 0x30000fc)
precondition(rl_relogio(world, &tick, &milliseconds) == 0 && tick == 20)
precondition(rl_eventos_quadro(world, nil, 0, &required) == RL_BUFFER_TOO_SMALL && required == 4)
var events = [RlFrameEvent](repeating: RlFrameEvent(), count: Int(required))
events.withUnsafeMutableBufferPointer { records in
    precondition(rl_eventos_quadro(world, records.baseAddress!, UInt32(records.count), &required) == 0)
}
precondition(events[0].kind == 2 && events[0].id == 103 && events[3].id == 7)
precondition(rl_projetar_tudo(world, nil, 0, &required) == RL_BUFFER_TOO_SMALL)
precondition(required == UInt32(frameBytes.count + 12))
print("Swift C ABI1.5 passed: RNG, projection, frame phase, events, clock")
