#ifndef RISING_ENGINE_H
#define RISING_ENGINE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/* Pilot ABI1.0. No engine frame-step, rendering or asset ABI is defined here.
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
#define RL_ABI_VERSION 0x00010000u
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
#ifdef __cplusplus
}
#endif
#endif
