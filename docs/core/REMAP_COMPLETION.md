# Remaining Chemin_Remap lifecycle

Stage 17 static readiness, 2026-10-28, after Stage 16 was integrated and reproduced on main `b4c5a1072a2b2e494b3a6bf374bd978fc6e67b9a`. This is a continuation plan and unexecuted original-only harness, not a game translation or native result. The original full routine is already preserved in `evidencias/classificacao-remapeamento/0042ee1c.asm`, with byte hashes in its manifest. Oracle SHA-256: `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. No new native process has run. The resource fixture and seven input shapes have only syntax/pure-input checks.

## Exact remaining order

The Stage 16 handoff is before `0x42ef8b`, with the temporary class allocation live, regions already cleared, and scan index/component count zero. Continue rather than replaying the reset or classification.

1. Inspect region words in ascending cell order over the full 65,536-cell allocation. For each zero word, increment the component count, retain its low u16 label, and call GlobalAlloc `(0, 0x100000)` at `0x42efba`, then GlobalLock at `0x42efca`. The original does not test the second lock for null before its first word store at `0x42efd9`; a model must not invent a clean False return there.
2. Use the live one-megabyte allocation as a LIFO of u16 cells, starting with the scan cell. Pop, compare its class with the component seed, and skip already labeled cells. Store the component label before pushing neighbors. Neighbor push order is west, east, south, north, then northwest, southwest, northeast, southeast only for class zero. The original cell coordinates, full 256 by 256 bounds and u16 stores apply; playable dimensions do not restrict this flood fill.
3. On an empty stack, call GlobalHandle(pointer), GlobalUnlock(result), GlobalHandle(pointer), GlobalFree(result), in that order at `0x42ef4e`, `0x42ef56`, `0x42ef5e`, `0x42ef66`. Every component has a distinct allocation lifecycle even when an arena explicitly reuses the same address. Failed/missing providers retain earlier labels, stack writes and resource effects.
4. After all components, apply the original row-major edge correction at `0x42f141..0x42f199`: outside current u16 width/height, write region zero then attribute byte one. Width greater than 256 causes no horizontal writes on an in-height row; height greater than 256 includes all rows. These input values are not silently clamped.
5. Release the original class pointer through GlobalHandle, GlobalUnlock, GlobalHandle, GlobalFree at `0x42f1a0`, `0x42f1ac`, `0x42f1b4`, `0x42f1bc`. Only after all those effects does the original inspect the low u16 component count: AL is one if below `0x4000`, otherwise zero. The complete return epilogue is `0x42f1d7..0x42f1e0`.

The existing `regioes_mapa.preencher_componente` has the same normal flood-fill order and can inform the implementation, but its Python list does not expose the allocated stack bytes or resource effects. `reconstruir_regioes` raises at the label threshold before edge correction; that is not the remaining original lifecycle. `refazer_regioes` also reinserts units and must not substitute for this routine.

## Resource contract to settle before translation

The native oracle can now declare the five actual PE imports GlobalAlloc, GlobalLock, GlobalHandle, GlobalUnlock and GlobalFree through the committed Stage 16 transport. Fixture handlers must explicitly enforce supported flags/sizes, allocation state, pointer/handle identity and finite arena capacity. Unsupported allocation/locking or stale resources stop visibly; no Windows success default is appropriate.

The Python continuation must retain the same live class buffer supplied to Stage 16. GlobalHandle receives the locked pointer, not necessarily the original allocation handle. Its Python counterpart therefore needs an explicit identity mapping from each live buffer to its pointer/handle; passing the allocation handle as though it were the pointer is not a justified shortcut. The component LIFO must write the actual supplied mutable allocation with original u16 offsets, preserving untouched tail bytes. This representation and any missing-provider handoff should be agreed with the mission resource owner before publishing an API.

## Original-first capture selection

Under a new coordinator grant, capture a bounded original-only batch before implementing this continuation. Cover a single class, separated natural components, diagonal class-zero versus class-one connectivity, map edges and poisoned arena tails, plus actual MONDE01 normalized layers with the shipped TABLEAU.COL. Include a deliberate unsupported second lock and a cleanup-provider stop with retained effects. Observe allocation/lock/handle/unlock/free arguments and order, all physical world layers, both temporary allocations and complete original return or exact stop.

A component-count threshold case can require many resource calls; inventory its concrete input and cost before scheduling it. Do not turn a budget stop into a final-return claim. Same-instruction CPU/flags/stack-preserving loop resumptions may be added at original loop heads; instruction and wall limits remain unchanged. Native entry, bounded segment, binding resumption and loop resumption counts stay separate.

After capture review, translate only the evidenced domain, replay immutable observations, run the changed native differential and focused legacy checks, then the required Core/common locked integration and exact-main reproduction. Full MissionLoad and the whole loaded mission comparison remain a later missions-owned composition. The development cutoff is 18:25 BRT on 2026-10-28; 18:25–18:40 is handover only.

## Prepared harness and bounded estimate

`bancada_conclusao_remapeamento.py` extends the committed original classification bench without translating the flood fill. The original engine path remains three memset calls and their existing original leaf, plus TerrainEstObstacleNaturel; the rest of Chemin_Remap executes inline. Only the five actual Windows IAT slots are bound. The explicit fixture has a 65,536-byte class allocation and a separate 1,048,576-byte component allocation, both poisoned initially; it permits at most 1,024 component lifecycles, reuses the component address only after free, and gives fixed handle==pointer semantics explicitly. Native bodies, original instructions and original code bytes are not patched. The finite binding budget is 8,192; a budget failure is not an original return.

The seven cases are actual MONDE01; a uniform class-zero grid with width/height1 for edge correction; two diagonal class-one cells; two diagonal class-zero cells in a class-one background; unavailable second lock; literal null second lock; and unavailable first component unlock. Native null-lock acceptance is specifically UC_ERR_WRITE_UNMAPPED at0x42efd9. Unavailable-lock/unlock acceptance requires the matching exact import/caller-return checkpoint, never just any exception. Unsupported observations retain all completed world/resource effects; all other faults/limits fail the batch and are saved. Successful returns must preserve poisoned EBX/ECX/EDX/ESI/EDI/EBP, with original EAX and consumed AL retained in evidence.

The capture saves the complete 585,728-byte DGROUP+.bss, every mapped non-stack world/resource allocation including tails, and their compressed bytes/hashes before and after each run. It also records exact binding events, live/freed/locked generations, maximum stack offset, ordered u16 stack-write hash, original region-label/edge-store hash, attribute-edge-store hash, registers and the native-stack hash. Initial CRT region-fill write granularity is excluded from the logical region-store trace; its full memory effect remains included in the whole-image comparison. This distinguishes complete original-state equality from selected result counts.

The initial schedule should run MONDE01 alone and inspect its actual cost/result, then the six discriminating fixtures if the grant/time allows. Each output uses exclusive creation and preserves any failed attempt:

```sh
python3 -B ferramentas/capturar_conclusao_remapeamento.py --casos MONDE01 --relatorio relatorios/stage17-original-MONDE01.json
python3 -B ferramentas/capturar_conclusao_remapeamento.py --casos uniform_zero_edge diagonal_one diagonal_zero component_lock_unavailable component_lock_null cleanup_unavailable --relatorio relatorios/stage17-original-discriminating.json
```

Planning estimate, not measured native evidence: MONDE0145–90seconds; all seven4–7minutes including whole-memory compression and write traces. It is based on the measured Stage16 23.338-second suite and the additional full-grid LIFO work; the new write tracing may make it slower. Inspect the first actual runtime before starting the remainder. Segment caps remain one million instructions/one second, with same-instruction preserved-state resumptions at original classification, component-pop, outer-scan and edge-row loop heads. No Ghidra or concurrent native child is required. The later Python translation and fresh validation/integration need their own remaining-time review.
