#ifndef RISING_ENGINE_H
#define RISING_ENGINE_H
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
/* ABI1.4. Frame logic and native indexed rendering are additive.
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
#define RL_ABI_VERSION 0x00010004u
enum { RL_OK=0, RL_INVALID_ARGUMENT=1, RL_INVALID_HANDLE=2, RL_MEMORY_ERROR=3,
 RL_UNKNOWN_ROUTINE=4, RL_UNSUPPORTED_PATH=5, RL_BUFFER_TOO_SMALL=6,
 RL_PANIC=7, RL_POISONED=8, RL_RESOURCE_LIMIT=9, RL_VERSION_MISMATCH=10, RL_STALE_GENERATION=11 };
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
/* ABI 1.3: read-only Graphics render API 1.5. Indexed pixels: top-down 800x600,
 * stride 800. Palette: 256 RGB24 entries, static generation 1; no Cyclage.
 * All calls share the world registry lock. Caller serializes render/step/reset/free.
 * Creation copies and verifies nine blobs: BLOCS,TROOPS,VEHICULE,CREATURE,
 * BUILDING,OTHERS CMPs; PLATGAME.PIE; original shadow and lighting tables.
 * Asset payloads are never embedded in the code repository. Initial surface and
 * complete cache are required explicit inputs; no blank/cold defaults.
 * Generation increments on successful load/isolated routine/frame mutations.
 * Render requires phase 1 or 3 (AffGame entry), exact expected generation, and
 * hud_flags 0 or 1. Repeated generation+flags returns the same cached result.
 * Rendering NEVER applies its observed writes/RNG effects to the world: phase2
 * retains sole ownership. Ordered diagnostic observations are copied separately.
 * Success may be full(0), undrawn(1), partial(2). Partial publishes actual prefix
 * and cache, with a named stop. ABI errors publish neither surface nor cache.
 * BufferTooSmall writes result capacities/metadata only; both buffers untouched.
 * Palette equality is pinned; unsupported palette animation is outside 1.5.
 * World free invalidates bound renders/resets/diagnostic reads; renderer free
 * remains possible. Renderer handles are never reused.
 */
typedef uint64_t RlRenderer;
typedef struct { const uint8_t *data; uint32_t length; } RlRenderBytes;
typedef struct { RlRenderBytes keys,payloads; uint32_t cursor; } RlRenderCache;
typedef struct {
 int32_t abi_status; uint32_t disposition; uint64_t generation;
 uint32_t frame_counter,width,height,stride,required_pixels,required_palette;
 uint64_t palette_generation,cache_generation; uint32_t stop_address;
 uint8_t stop_callee[48],stop_reason[192];
} RlRenderResult;
typedef struct {
 uint32_t kind,address; uint8_t name[48]; uint32_t count; int32_t args[8];
 uint8_t before[8],after[8];
} RlRenderObservation;
int32_t rl_render_criar(RlMundo world,const RlRenderBytes *assets,uint32_t count,
 const RlRenderBytes *initial_surface,const RlRenderCache *initial_cache,RlRenderer *output);
int32_t rl_render_geracao(RlMundo world,uint64_t *generation,uint32_t *phase,uint32_t *frame);
int32_t rl_render_quadro(RlRenderer renderer,uint64_t expected_generation,uint32_t hud_flags,
 uint8_t *indexed_buffer,uint32_t indexed_capacity,uint8_t *palette_rgb24,uint32_t palette_capacity,
 RlRenderResult *result);
int32_t rl_render_reset(RlRenderer renderer,const RlRenderBytes *surface,const RlRenderCache *cache);
int32_t rl_render_liberar(RlRenderer renderer);
/* Observation kind1: changed bytes (count<=8); kind2: ordered raster arguments
 * (count<=8). name is UTF8+NUL. Reads do not alter last output/cache. */
int32_t rl_render_observacoes(RlRenderer renderer,RlRenderObservation *buffer,uint32_t capacity,uint32_t *required);
int32_t rl_render_cache(RlRenderer renderer,uint8_t *keys,uint32_t key_capacity,
 uint8_t *payloads,uint32_t payload_capacity,uint32_t *key_required,uint32_t *payload_required,uint32_t *cursor);
/* ABI 1.4: Graphics contract 1.7. Existing 1.3 structs/signatures remain.
 * Observation kind3: write-only saved_background_pixels; count is byte length,
 * full payload comes from rl_render_fundo_salvo (before/after are not old bytes).
 * kind4: AffText request at the named glyph dependency; args hold x,y,right,
 * bottom,font,flags0,flags1,text-length; before+after hold the single-byte text.
 * The production C ABI never substitutes text. AffText returns a partial frame
 * at 0x459454, with actual tooltip background and saved bytes available.
 * Reset clears saved background; a pending initial restore reads the explicitly
 * declared world buffer. Future restores use actual renderer-produced bytes.
 * Phase 2 still owns display logic mutations; renderer observations are read-only.
 */
uint32_t rl_render_contrato(void);
int32_t rl_render_fundo_salvo(RlRenderer renderer,uint8_t *buffer,uint32_t capacity,
 uint32_t *required,uint32_t *address,uint64_t *generation);
#ifdef __cplusplus
}
#endif
#endif
