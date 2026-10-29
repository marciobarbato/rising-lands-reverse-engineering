#ifndef RISING_ENGINE_H
#define RISING_ENGINE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/* ABI1.2. Frame logic phases are additive; rendering/assets are separate.
 * Addresses are original u32 values, NOT host pointers. Handles are opaque
 * integer tokens, never dereferenceable; zero/stale/double-free are rejected.
 * Calls are serialized inside the library. Caller must synchronize handle use
 * with free. No Rust-owned pointers escape; all buffers are copied.
 * All nonnull pointers must be aligned, valid for their declared lengths and
 * disjoint from output storage. No call may race access to caller buffers.
 * Success0; all errors leave world/registers unchanged. Projection query writes
 * address/required metadata on RL_BUFFER_TOO_SMALL; buffer stays unchanged.
 * Load replaces ALL blocks atomically, preserving the explicit virtual clock.
 * Count<=65536 and total<=64MiB. Empty load is allowed; empty regions are not.
 */
#define RL_ABI_VERSION 0x00010002u
enum { RL_OK=0, RL_INVALID_ARGUMENT=1, RL_INVALID_HANDLE=2, RL_MEMORY_ERROR=3,
 RL_UNKNOWN_ROUTINE=4, RL_UNSUPPORTED_PATH=5, RL_BUFFER_TOO_SMALL=6,
 RL_PANIC=7, RL_POISONED=8, RL_RESOURCE_LIMIT=9, RL_VERSION_MISMATCH=10 };
enum { RL_RANDOM=1, RL_LONG_RAND=2, RL_CRT_RAND=3, RL_INT_TO_BCD=4, RL_BCD_TO_INT=5 };
typedef uint64_t RlMundo;
typedef struct { uint32_t address, length; const uint8_t *data; } RlBloco;
typedef struct { uint32_t eax, ebx, ecx, edx, esi, edi, ebp; } RlRegisters;
uint32_t rl_versao(void);
int32_t rl_criar_mundo(uint32_t abi_version, uint32_t ticks_per_second,
 uint32_t epoch_ms, RlMundo *output);
int32_t rl_liberar_mundo(RlMundo world);
int32_t rl_carregar_blocos(RlMundo world, const RlBloco *blocks, uint32_t count);
/* Isolated routine call, NOT a tick. Register map: original data GPRs, with
 * no x86 EIP/ESP/EFLAGS contract. No routine here reads a host clock. */
int32_t rl_executar_rotina(RlMundo world, uint32_t routine, RlRegisters *registers);
int32_t rl_quantidade_blocos(RlMundo world, uint32_t *output);
/* Blocks are sorted by numeric address. Query: buffer=NULL, capacity=0. */
int32_t rl_projetar_bloco(RlMundo world, uint32_t index, uint32_t *address,
 uint8_t *buffer, uint32_t capacity, uint32_t *required);
/* Clock foundation only; advances no game logic. Default pacing policy20Hz
 * (caller explicitly passes20), not a proved historical MONDE01 FPS. */
int32_t rl_avancar_ticks(RlMundo world, uint64_t ticks);
int32_t rl_relogio(RlMundo world, uint64_t *tick, uint32_t *milliseconds);
/* Thread-local error, UTF8+NUL. Does not clear error. NULL/zero size query. */
int32_t rl_erro_mensagem(uint8_t *buffer, uint32_t capacity, uint32_t *required);
/* ABI1.1 additions. Creation also accepts1.0/1.1; existing layouts/signatures retain
 * their1.0 semantics. One caller must serialize a phase plus snapshot/events.
 * Input states are explicitly declared memory blocks, including original tables.
 * Supported scenario: MONDE01 no-key display path. Unported branches fail with
 * RL_UNSUPPORTED_PATH naming the original address. All calls are transactional.
 * Phase1(load_tail/frame0) and3(frame) tick once; phase2(between) does not tick.
 * No human-input protocol, pixels or render surface is returned. */
typedef struct { uint32_t eax,ebx,ecx,edx,esi,edi,ebp,esp; } RlFrameRegisters;
typedef struct {
 int32_t cursor_x,cursor_y; uint32_t offscreen; RlFrameRegisters registers;
 uint32_t saved[3],msg[4];
} RlFrameInput;
/* saved is ProgIteration's saved EDX/ECX/EBX; msg is its four loop words.
 * registers is the declared phase entry. Phase2 returns next CalculGame entry;
 * phase3 returns preserved registers with ESP+4; EAX is unspecified for phase3.
 * Phase1's register output is unspecified. On failure input is unchanged. */
enum { RL_LOAD_TAIL=1,RL_BETWEEN_FRAMES=2,RL_FRAME=3 };
int32_t rl_passo_quadro(RlMundo world,uint32_t phase,RlFrameInput *input);
typedef struct {
 uint32_t kind,id,site,args[5],result,registers[4],stack[4],stack_mask;
} RlFrameEvent;
/* kind1 binding,2 boundary,3 free; site is original return address. Binding ids:
 *1 ShowCursor,2 GetAsyncKeyState,3 GlobalHandle,4 GlobalUnlock,5 GlobalFree,
 *6 PeekMessageA,7 GetCursorPos,8 SetCursorPos. Boundary ids101 LoadPie,
 *102 MCICD_Play,103 PlaySnd_Manage,104 MCICD_Manage. Registers EAX/EDX/EBX/ECX.
 * stack_mask selects known stack words (uninitialized locals stay unmodeled).
 * MCICD args0/1 carry music guards0x4e2f28/29. Free args0=address,result=size.
 * Unused slots are structural zero. required is record count, not byte count.
 * Successful load/isolated routine clears events; errors retain previous events.
 */
int32_t rl_eventos_quadro(RlMundo world,RlFrameEvent *buffer,uint32_t capacity,uint32_t *required);
/* Packed copied snapshot: LEu32 count then repeated LEu32 address,length,bytes.
 * No alignment padding. NULL/zero query returns RL_BUFFER_TOO_SMALL with
 * required byte count. Other buffer errors never copy a prefix. Freed snapshot
 * contains actual bytes at free, from the last successful phase, sorted by
 * numeric address; it is empty after load or isolated routine calls. */
int32_t rl_projetar_tudo(RlMundo world,uint8_t *buffer,uint32_t capacity,uint32_t *required);
int32_t rl_projetar_liberados(RlMundo world,uint8_t *buffer,uint32_t capacity,uint32_t *required);
/* Isolated provider effects, no tick. Id table: frame_{ai,units,core,economy}
 * ::isolated in rl-core. ABI1.2 adds raid/movement/Combat IDs400..599. Argument counts are exact. Returns only the published
 * semantic EAX/provider value; void adapters return0, no GPR claim. */
int32_t rl_executar_rotina_quadro(RlMundo world,uint32_t routine,const uint32_t *args,uint32_t count,uint32_t *output);
#ifdef __cplusplus
}
#endif
#endif
