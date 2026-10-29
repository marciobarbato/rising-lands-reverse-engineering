# MONDE01 player-action map — static preparation for M3

This delivery maps original input, command dispatch and effect entry points. It
implements no game behavior or input protocol and performs no native emulation.
**No player action, objective completion, victory/defeat sequence or M3/M4
acceptance is established.** Accepted M2.2 contains no human input.

The machine-readable [call graph](callgraph.json) contains 94 nodes, 235 selected
encoded call edges, all 40 command cases and six action groups. Its action
`stages` are processing stages, **not a claim that every adjacent pair is a
CALL or that every conditional callee executes in one action**.

## Evidence and confidence

Base: `daa6ed2da79827b2472929f7e5c82aad1d631782`, fetched 2026-10-29. Independent
clone: `/Users/marcio/git/Rising-Lands-Codex-Player-Actions`; exclusive branch:
`feat/codex-m3-player-actions`. Original-only evidence was committed first at
`6bfa18d` before this synthesis. Only this research directory is changed.

Intact `INSTALHD/RISING.EXE` SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The normalized `26c4534b...64d0` PE was not used. LLVM decodes a temporary ELF
whose `.text` is an exact `.incbin` of the intact PE's BEGTEXT section; every
recorded instruction byte and curated call/transition target is checked against the intact
file. No modified executable is run. Original CD files remain read-only.

[Original byte evidence](evidencias/original-player-action-bytes.json) retains
67 symbol-anchored intervals, raw interval hashes/hex, decoded instructions,
1,282 candidate call encodings, memory operands and the original import table.
An interval ends at the next imported symbol; this is **not a proven function
return boundary**. Linear disassembly can include unreachable bytes/padding,
and shared tails can jump outside an interval. The curated graph validates
its call encoding and target, not dynamic reachability or complete CFG closure.

Confidence labels are deliberately separate:

- **Byte-proven encoding:** exact original instruction, table entry or data
  record. It proves a local encoded reference/store, not execution.
- **Static synthesis:** possible path or field interpretation combining those
  bytes and published owner contracts. Conditions and indirect context remain.
- **Accepted reference bytes:** immutable M1 initial state, without a new
  player-action execution. [Context evidence](evidencias/monde01-action-context.json)
  pins its capture SHA-256 and records condition/roster bytes.
- **Unproven runtime:** successful MONDE01 action and subsequent effects.

Ownership below routes dependencies using existing front responsibilities; it
is not an assignment to rewrite the other fronts or a new accepted API.

## Windows input to the frame and command slot

| Stage | Exact original references | Data and scope | Owner/dependency |
|---|---|---|---|
| Message loop | `_WinMain@16 0x460170`; imports at `0x4601d1` PeekMessageA, `0x4601e4` GetMessageA, `0x4601f2` TranslateMessage, `0x4601fc` DispatchMessageA | Dispatches messages or calls ProgIteration at `0x46020d`; the Windows procedures are original platform dependencies | AI/runtime; macOS platform mapping later |
| Window procedure | `WndProc 0x4181a1..0x418590` | Message-value comparisons and flag stores; no direct KeyPressed/KeyUnPressed call was found in this interval | AI/runtime / macOS mapping |
| Mouse flags | `0x418207..0x41826b` and routing comparisons `0x41852b..0x41857d` | Message `0x200` stores low/high coordinate words at `0x5099a8/aa`; `0x201` sets `0x5099ae`, `0x202` sets `0x5099af`, `0x204` sets `0x5099b1`, `0x205` sets `0x5099b2`; the `0x203` path depends on cursor Y/window height before `0x5099b0` or `0x5099ae` | Raw message-to-flag encoding is byte-proven; held/release timing requires an input trace |
| Polling per iteration | `ProgIteration 0x47500e`; GetCursorPos IAT call `0x475044`; coordinate stores `0x47504e/58` | Increments counters including u32 `0x508f7c`; polls cursor into u16 globals `0x5099a8/aa`; calls CalculGame at `0x47505e`, then AffGame at `0x475063` | AI/runtime cadence; Graphics separately |
| Keyboard/map context | `InputGame 0x429278`; GetAsyncKeyState through original IAT slot `0x523290`; MouseZone `0x479cac` | Polling, map/toolbar zones, selected units/structure and click flags influence commands; unsupported key/click branches in the current no-input Python consumer remain explicit stops | AI/runtime |
| Local/remote branch | CalculGame calls `InputGame 0x42d33b`, InputSend `0x42d342`, or InputReceive `0x42d34b` | Existing player type/local-player `0x508041` chooses the branch; InputSend/Receive test network activation | AI/runtime; network remains out of this local-action map |
| Command production | `SetPlayerOrdre 0x45ecd4..0x45ed1c` | AL player; DX command; BX argument 1; CX argument 2; two stack arguments. Writes five u16 words at offsets 0/2/4/6/8 through `dword [0x4e2458+4*player]`; returns with `ret 8` | AI/runtime command slot; not a new transport protocol |
| Command consumption | CalculGame calls ProcessInputGame at `0x42d3b0`; entry `0x45edc0` | Reads tag u16 from the player's slot. `0x45eddb` bounds it at 39; `0x45edeb` jumps via 40 u32 addresses at `0x45ed20` | AI/runtime |
| Slot cleanup | `0x45f2de..0x45f323` | Clears every command word, including after default/out-of-range dispatch. The order slot is not an invented multi-command queue | AI/runtime |

The static keyboard helpers at `0x42c31b/339/361/396` are included for context;
this map does not infer that the in-game mouse procedure invokes them. Windows
message constants are not a macOS event mapping or a recommendation to bypass
the original InputGame path.

## Relevant command cases and arguments

The complete table is in `callgraph.json:command_dispatch`. Each case includes
its exact table-entry address, branch target and possible CALL sites obtained
by static branch traversal until the shared cleanup. Calls in that list are
not necessarily one sequential runtime trace.

| Tag | Dispatch block | Encoded consumer calls | Packet reads / interpretation |
|---:|---|---|---|
| 1 | `0x45ee46` | DeSelectionGroupe `0x45ee4b`, BatimentDeselectionner `0x45ee55`, SelectionEngin `0x45ee83` | +2/+4 u16 selection geometry; actual click/drag variant needs capture |
| 2 | `0x45eeaf` | Group/unit deselection then BatimentSelection `0x45eed8` | +2 u16 structure reference |
| 3 | `0x45ee2d` | DeSelectionGroupe and BatimentDeselectionner | Deselect |
| 4 | `0x45ef73` | SetConstruitBatimentSelect `0x45ef9b` | +2 low u8 type -> DL; +4 u16 cell -> BX; AL player |
| 5 | `0x45efc1` | SetDeplaceEnginSelect `0x45efd8` | +2 u16 destination -> DX; AL player |
| 6 | `0x45efe2` | SetMineEnginSelect `0x45eff9`, then shared SetDepotEnginSelect `0x45f037` | +2 u16 mine/cell reference; subsequent depot fields are tag-specific |
| 7 | `0x45f041` | SetRecolteEnginSelect `0x45f058`, then `0x45f037` | +2 u16 cell; shared depot call consumes +4 low u8, +6 u16, +8 low u8 |
| 8 | `0x45f05f` | SetTransporteEnginSelect `0x45f076`, then `0x45f037` | Same packet widths; local UI producer not established here |
| 14 | `0x45f0c7` | BatimentGetSelection `0x45f0cc`; SetAttaqueEnginSelect `0x45f105` or BatimentInitAttaqueSelect `0x45f13f` | +2 low u8 mode; +4 u16 target reference; selected-building branch differs |
| 17 | `0x45f19f` | InitRecruteTroupe `0x45f1a9` | +2 low u8 requested unit type -> AX; player -> EDX |
| 18 | `0x45f20f` | SetRamasseEnginSelect `0x45f217` | +2 u16 reference; not equated with general harvest |
| 19 | `0x45f07d` | SetDechargeCaveEnginSelect `0x45f085`, then `0x45f037` | Cave-related discharge/depot route; exact UI conditions remain |
| 36 | `0x45ee8d` | BatimentDeselectionner `0x45ee8f`, EnginAddSelection `0x45eea5` | +2 u16 unit reference; add-selection differs from rectangle tag 1 |

All selected-unit wrappers read the per-player selection area: count u16 at
`0x508728 + 512*player`, then u16 indices at `+2 + 2*i`. Unit records come from
u32 pointer `0x4e19a0`, with 276-byte stride, owner u8 +0, type u8 +1 and state
u8 +2. Liveness/ownership gates must be preserved, not replaced with the app's
synthetic unit list.

## Action paths and known gaps

### Selection and movement

InputGame has original SetPlayerOrdre calls at `0x42b9aa` (near a literal tag 2)
and `0x42ba20` (selection setup, including `0x4e19b2/b4` words). The graph labels
this producer mapping static: local branch conditions and register preservation
must still be traced.

Literal tag-5 producers are visible at `0x42a488`, `0x42ad8e`, `0x42b82a` and
`0x42bbd6`, under different UI/terrain conditions. The command consumer calls
SetDeplaceEnginSelect, which checks selected-unit liveness/owner, calls Core's
SetDeplaceEngin at `0x473ed2`, and writes current u32 counter `0x508f7c` to unit
+0x110 at `0x473ee2`. ResetOrdre is called inside SetDeplaceEngin. Subsequent
EnginNextEtape/movement/navigation branches retain Core and AI/runtime ownership.
A byte-proven destination store is not proof that the destination is reachable.

### Construct the objective cave

InputGame's `0x42a03c` call has a literal command 4 setup. The requested type
comes from byte `0x496207`; this research **does not prove that selecting the
CAVE button sets that byte to 3**. That is a specific next input capture.

SetConstruitBatimentSelect `0x473a07` checks selected units' type against 7 at
`0x473a71/74`, then calls SetEnginConstruitBatiment `0x473a84`. The original
50-byte type table and EnginGetTypeName getter prove type 7 is `BATISSEUR`;
accepted M1 reference bytes identify player-0 unit 12 as type 7. They also prove
type 0 `SOLDAT` and type 9 `COLON`, without guessing names from sprites.

The setter writes u8 state +2 = 11, requested type u8 +0xbe, u16 cell +0xb2,
and other order/search fields. EnginNextEtape has a possible call to
CalculConstruireBatiment at `0x456516`; that caller can invoke CreerBatiment
`0x44ad89`, BatimentConstruit `0x44b1eb`, repair `0x44b2ae` and completion
BatimentConstruction `0x44b2be`, on distinct conditional paths. CreerBatiment
contains TestRessource/EnleveMatiere and physical PlaceBatiment calls. Completion
reaches BatimentHabitable and BatimentModifyMap. Economy owns economic gates
and construction callers; Core owns order/world allocation/placement; AI/runtime
owns dispatch. No construction can be declared successful from this map.

The original 52-byte structure records and BatimentGetTypeName establish **type
2 SANCTUAIRE, type 3 CAVE**. Accepted M1 starts with the sanctuary; it must not
be renamed a cave to satisfy the objective. The context evidence includes the
first 16 unit headers, not a newly constructed or modified roster.

### Food, stone, transport and recruitment

The accepted M1 condition records at `0x4e1d20` begin with type 4 / parameter 3,
type 0 / parameter 50, and type 1 / parameter 50. These are objective
thresholds, not initial player resource balances. This context extraction does
not publish initial resource balances or import any synthetic app balance.
Their exact four-word parameter arrays remain in the JSON, including raw zone values. The briefing's summary
corroborates a cave and 50 food/50 stone bags. It is player text, not a substitute
for the evaluator.

TestFinDeMission's type-0/1 paths call TestRessource with the requested food AX
or stone DX value. Its type-4 path scans owned structures, type, cell and influence
zone. It treats zone word `0x00ff` as wildcard; do not treat the raw `0xffff`
words as that wildcard. **No additional per-cave storage rule is inferred** from
the briefing: the code queries the published player resource provider and the
separate structure condition.

InputGame emits literal tag 7 near `0x42b486` and tag 18 near `0x42b61c` in
particular map contexts. Tag 8's local producer is unresolved in this subset.
SetRecolteEngin writes state 5 and SetTransporteEngin writes state 18. The work
and transport callers have static references to TerrainRecolte, MineRecolte,
TerrainRetireMatiere, Bag operations and BatimentAjouteMatiere; calls to sound,
collision, discovery, rotation and movement are separate owner dependencies.
No harvest or natural cave deposit has been executed by this delivery.

Tag 17 goes to InitRecruteTroupe, which reads selected structure u16
`0x495be0 + 2*player`. BatimentNextEtape can call CalculTroupe and related
production routines. This is a **unit recruitment route**, not evidence that
recruitment itself manufactures food or stone. Its UI producer and MONDE01
availability require original input captures.

### Attack

InputGame has literal tag-14 setups at `0x42a52c`, `0x42a5e6` and `0x42aecf`.
The selected-unit branch calls SetAttaqueEnginSelect, then SetAttaqueEngin at
`0x473e39`. Its ResetOrdre call is at `0x445a7b`; accepted-order fields include
state +2 = 1, mode +0xb7 u8 and reference +0xb8 u16. EnginNextEtape's attack
call is at `0x4568a3`.

CalculAttaqueEngin contains alternative range/line, pursuit/movement, animation,
ProjectileInit and direct InfligeDegat branches. They must not be concatenated
into an invented mandatory firing sequence. Combat owns those effects;
Core/AI/runtime own reset, movement and dispatch. The selected-building attack
branch uses a different caller. No player attack, damage or death is validated
here, and no M2.3 raid run is started or duplicated.

## End-of-mission and transition boundary

CalculGame calls TestFinDeMission at `0x42d481` only on its non-network path.
It stores AL to byte `0x4e05a0` at `0x42d486`. On nonzero AL it increments u32
`0x4e061c`; once the signed counter reaches 100, it calls PlaySnd_StopAllSound
and requests MenuInit mode `0x13` via `0x42d4d4 -> 0x42c92c` and shared CALL
`0x42c931`. This is a byte-proven local branch/store sequence, not an observed
victory screen.

TestFinDeMission consumes ten 10-byte condition records and writes latch/result
`0x4e1d84` plus per-record marks `0x4e1d88..0x4e1d91`. A zero word at
`0x4e1a3a` forces completion AL=1 with latch 0; **the precise runtime event that
makes this word zero must not be guessed as a specific last-unit death rule**.
PartieGetResultat `0x4585e4` simply returns the result byte.

In the result screen, CalculGame calls PartieGetResultat at `0x42c9cc`; a
nonzero result can take the confirm/click route to MissionNext `0x42ca6e`.
If that returns 1, the code calls IaRechercheAjuste, Engin_StoreExperimente,
RechercheStore and PlayerStore, then requests a later menu/load state. MissionNext
itself increments mission byte `0x496fe4`, calls MakeMissionName and FileExists,
and returns whether the file exists. It does **not** call MissionLoad.

The zero/nonzero result branches are consistent with defeat/victory naming,
but their complete UI flow, event scripts and persistence/transition behavior
remain static-only. Stop the first follow-up experiment before loading another
mission; no MONDE02 or later behavior is in this delivery's scope.

## Next original scripted-input coverage requests

These are capture goals, not a proposed input serialization protocol. The
coordinator should assign Windows/message/key binding semantics to AI/runtime
and the harness owner before implementing any macOS input mapping.

1. **Selection (AI/runtime + Core):** from accepted display-v2 state, capture
   selecting existing player-0 constructor unit 12 and a soldier. Record cursor,
   mouse messages/flags, modifiers, command slot before/after SetPlayerOrdre,
   ProcessInputGame tag/arguments and all selection bytes. Distinguish rectangle,
   add-selection and selected-building paths.
2. **Movement (AI/runtime + Core):** choose a discovered reachable destination
   from actual accepted world bytes, not a fabricated coordinate. Capture the
   emitting InputGame branch, tag 5, reset effects, unit state/path/search and
   collision arrays through one natural movement/arrival interval.
3. **CAVE order (AI/runtime + Economy + Core):** capture the actual CAVE UI
   selection proving `0x496207=3`, tag 4 and type-7 gate. Retain original resource,
   realizability, placement and cell constraints. An insufficient-cost or blocked
   placement outcome is evidence, not permission to inject balances or callbacks.
4. **Natural food/stone delivery (Economy + Core):** choose actual MONDE01 food,
   stone and bag/depot cells. Capture which of tags 6/7/8/18/19 the UI emits,
   the +4/+6/+8 depot tuple, natural work/transport and resource/cave effects.
   Resolve the tag-8 producer and preserve partial effects/stops.
5. **Attack (AI/runtime + Combat + Core):** capture actual target selection,
   command mode/reference, range/pursuit and the reached damage/projectile branch.
   Reuse an owner-provided suitable raid checkpoint if needed; do not duplicate
   the critical M2.3 long capture on this workstation.
6. **Objective/end boundary (Missions + Economy + AI/runtime):** after natural
   actions satisfy the real conditions, capture TestFinDeMission reads/marks,
   result latch, counter-100 menu transition and confirmation stores. Capture
   failure separately. Stop before any next mission execution.

Long or unknown-duration native runs go to Claude/Mac mini with exact committed
harness command/output requests. This static delivery needs no lease and makes
no timing estimate or native comparison claim.

## Validation and reproducibility

```sh
python3 -B pesquisas-paralelas/mapa-acoes-jogador/extrair_mapa_acoes_bytes.py \
  --exe '/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE' \
  --output pesquisas-paralelas/mapa-acoes-jogador/evidencias/original-player-action-bytes.json
python3 -B pesquisas-paralelas/mapa-acoes-jogador/extrair_contexto_monde01_acoes.py \
  --exe '/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE' \
  --output pesquisas-paralelas/mapa-acoes-jogador/evidencias/monde01-action-context.json
python3 -B pesquisas-paralelas/mapa-acoes-jogador/gerar_grafo_acoes_jogador.py
python3 -B pesquisas-paralelas/mapa-acoes-jogador/validar_mapa_acoes_jogador.py \
  --exe '/Users/marcio/git/Rising Lands/source/cd/INSTALHD/RISING.EXE'
python3 -B -m unittest discover -s pesquisas-paralelas/mapa-acoes-jogador -p 'test_*.py' -v
```

Regeneration should target new temporary outputs when reviewing frozen delivery
artifacts. The validator checks intact identity, original interval/instruction
bytes, E8 relative targets, PE import slots, table entries, type records,
accepted-M1 context, graph integrity and explicit non-acceptance labels.
[Validation result](validation.json): passed; six owned tests passed with zero
skips. Workflow checks and final delivery identity are in [HANDOFF](HANDOFF.md).
The new workstream is not a registered `scripts/check.py --domain` value; no
shared helper was modified to pretend otherwise.
