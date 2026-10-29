# Stage 19: building-target damage inventory

Current update, 2026-10-29: the live-memory consumer/wrapper is now published in
[COMBAT.md](../../docs/COMBAT.md#real-m23-raid-memory-api-2026-10-29), with
[evidence chronology](RAID_CAPTURE_MATRIX.md) and the current
[handoff](HANDOFF.md). `dano_estrutura_raid.DanoEstruturaRaid` implements the
consumer; `combate_raid_vivo.CombateRaidVivo` composes the cell wrapper and
explicit foreign dependencies. The dated 2026-10-28 static inventory below is
retained as historical planning context; its "not started" status is superseded
by the current delivery, not by an M3/M4 acceptance.

Status on 2026-10-28: **light static readiness only**. This is a proposed contract for the next bounded implementation, not a public provider. No behavior was translated and no native execution was run in this resumption. The coordinator's exclusive heavy lease is required before original-only captures, differential comparisons, domain checks or integration.

Baseline: main `8810b3730a0fb788af3eac2b447dea65372f597f`, reached by a clean fast-forward of the existing combat worktree. Stage 18 implementation `248d0556c216d0a8161a1264525b24ccb69fe51f`, pushed feature `d24b09c1ff4e6a81356fbfecbb24bf3140309af3` and main merge `b602b07e406ced7c8c67a9f011a8899718d32a87` are already ancestors of this baseline. Their 17,509 native executions are historical evidence, not fresh validation in this turn.

The intact executable SHA-256 is `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. The normalized analysis image `26c4534b08b7fdda30c4f5c4b0d665c3f57cd24db3ab3737dd1e0e9c625464d0` was not used here. [Static manifest](evidencias/dano-batiment-stage19.json) and [assembly](evidencias/dano-batiment-stage19.asm) were exported directly from verified intact bytes by [the owned extractor](rastrear_dano_batiment.py). Predecessor captures, manifests and reports remain unchanged.

## Building selection and damage request

`InfligeDegat 0x450874` receives AX cell:u16, DL mode:u8, BX source:u16, CL direction:u8, and an entry stack flag byte at `[ESP+4]`. The original tests the flag before looking up a building: zero calls `ChercheIndiceBatiment`; every nonzero byte skips that lookup. The building branch starts at `0x4508AF`; a successful branch returns through `0x4510D5` without invoking the unit-victim scan.

The intended translated domain retains the existing mode-1/3/4 wrapper widths and explicit source pools. IDs decoded by the grid may be 1000..1023; dereferencing one must stop before access to the 1000-record structure pool. The selection query itself must keep returning those original IDs.

| Mode | Request preparation before `BatimentInfligeDegat` |
|---|---|
| 1 | Read live unit type. Read **column 26** of that type's loaded damage row, then add full `Modificateur(owner,5,type)` to ECX. Save source owner, then request `iagVilleSendMessage(target,4,source)` at `0x45091B`. No source F7 or proximity term is added. Damage passed onward is low u16. The damage row must have an explicit 27th byte. |
| 3 | Query target `BatimentGetType`, then source `BatimentGetType`. Call `TypeBatimentGetDegat(source_type,3,target_type)` at `0x45094C`, then source `BatimentGetPlayer`. Type 10 selector 3 reads byte `0x4DFB9A`; type 11 reads `0x4DFB7E`; the target type is not indexed by this selector. Every other source type returns zero. The current `ConsultaFonteBatiment` implements selector 1 only and must not silently accept selector 3. |
| 4 | Save unit-source owner. Direction 29 reads **u16** `0x49716C`; direction 30 reads **u16** `0x49716E`. Divide that nonnegative word by two, then pass low u16. This differs from the unit target's byte and type-dependent quartering. Retain the existing initialized-direction domain 29/30. |

Other modes keep the initial ECX value 2 but do not initialize the saved source-owner byte; they are not a defined building-target caller contract. Unsupported modes must remain explicit.

After damage returns, the wrapper requests `Random(0x21)` even with a full projectile pool, then allocates hit type `15+(result&1)` at the original impact cell with the other arguments zero. It queries the target's live owner again for alliance, optional sympathy flags 10 then 6, alliance resets in both directions, and the unconditional `PlayerAAttaqueSet`. Each target-owner read must occur at its original call site. The saved source owner remains the one prepared before the consumer. Missing effects retain prior accumulator/destruction writes and any allocated hit; a calling projectile has not completed its arrival just because its victim's damage consumer returned.

## Building damage consumer and defined destruction tail

`BatimentInfligeDegat [0x41A2C1,0x41A4B6)` takes AX target:u16, **full EDX damage:u32**, BL source_owner:u8. The wrapper supplies zero-extended u16 damage; a direct consumer test must distinguish that caller restriction from the callee's input width. The routine has no meaningful return value for this contract. It preserves ECX/ESI/EDI/EBP, while EAX/EBX/EDX and flags are not public results. This ABI observation is static and still needs an original execution check.

Proposed API shape: a separate building consumer over the caller's writable 1000×276 structure pool, explicit loaded 22×52 characteristic bytes, explicit live camera/global state, and `(name, arguments)` query/effect providers. It must share those buffers rather than copy them. IDs truncate to u16 and then require 0..999; interpreted types require 0..21. A zero loaded maximum-life word causes original division failure after earlier writes; the translated boundary must report it rather than substituting a denominator. Do not copy the unit consumer's experience or physical-death tail.

Original order:

1. Add damage to record `+6`, storing only its low u16 at `0x41A2FA`. This is an accumulated-damage field; no unit life word is subtracted or zeroed. There is no inactive/destroying-state guard before this write.
2. If live owner equals the local player, query `BatimentGetVolume(target)` **before** testing sound handle `+0x100`. With handle `FFFFFFFF`, request `PlaySnd_PostSound(0x42,(type<<16)|0x100,0,volume,&record[0x100])`. The writable handle pointer belongs to the structure record. An unresolved volume or sound request leaves the damage addition intact.
3. Re-read owner/local player. If local and inherited global byte `0x4DFB9B` is zero, request `VoixOffAsk(1,3,0)`, then set that byte to 1 only after return. A failing request keeps the byte unchanged.
4. Re-read live type and the loaded maximum-life word at `0x495D90+52*type`. Compute `floor(200*u16(+6)/maximum)` and `floor(200*u16(+0x0A)/maximum)`. Compare their **low u16** values unsigned. The destruction path is entered only when the scaled accumulated damage is strictly greater than the scaled `+0x0A` value. Equality returns, and low-word wrap matters. This is not a raw `damage >= life` test.
5. The code compares two owner loads of the same target record. In the stable single-threaded domain they match. It then requests `iagVilleSendMessage(target,2,0)` at `0x41A411` **before** destruction stores. After return it writes byte `+0x90=1`, reads live type, then byte `+5=3`. Except for live type 9/12 it writes presentation byte `0x4DFB44=20`; live type 20 additionally gets u16 `+0x84=0x113`. A city-message dependency retains the accumulated damage but precedes these stores.
6. Request `MAJSympathie(saved_source_owner,live_target_owner,8)` at `0x41A45A`. This argument order differs from some unit-victim requests. A dependency here retains destruction state, presentation and type-20 timer stores.
7. Re-read local player and target owner. A local target requests `VoixOffAsk(1,1,0)`. Otherwise byte `record[0x110+local_player]` controls `VoixOffAsk(1,4,0)`. This visibility-index domain must be explicit; no out-of-range camera byte or invisible-target assumption may be invented.

Callbacks may mutate live records/globals, so re-read timing must be tested with explicitly labeled synthetic mutations on both original and Python sides. The routine marks destruction; it does not invoke physical structure removal, Bag evacuation, `SetDyingEngin`, or unit experience awards. Re-entering after a dependency repeats earlier writes and is not continuation. Existing undefined mode-8/9 unit lethal owner inputs remain outside Stage 19.

## Dispatcher and turret boundary

The current committed AI-facing APIs remain [the Stage 18 contract](../../docs/COMBAT.md#live-attack-chain-from-the-unit-dispatcher): `AtaqueVivo.definir_ataque`, `.ramo(indice:u16)` for unit states 1/24, and `.calcular_projeteis()`. No second unit dispatcher is needed. Its prelude/reload and branch ordering remain AI/Core responsibilities.

The turret selector in `BatimentNextEtape` is **structure type byte +8**, not state byte +5. Table `0x426880` indexes `type-1`: type 10 enters `0x426E43`, type 11 `0x427549`, with the latter range ending at `0x427BB7`. Both branches currently remain untranslated. They use the enclosing routine's ESI record, DI index and EBP local frame; no direct fragment ABI is published from static inspection alone.

Both branches check the Bag, validate/acquire unit or structure targets, aim, advance reload/animation/orientation and emit through `RechercheDecalageProjectile 0x425100`. That helper receives AL orientation:u8, DL structure_type:u8, BX origin:u16, CX target_cell:u16, entry stack `[ESP+4]` target_reference:u16 and `[ESP+8]` source_building:u16. It emits projectile type 20 (structure type 11) or 21 (type 10), mode 3, carrying the source-building index. Type 10 reads the target reference through **unit** type/height queries even when the caller selected a structure target; do not reinterpret that input as a structure query. The helper returns with `ret 8`. Its offset tables, target-reference domain and out-of-range orientation behavior require independent captures before a callable translation. Audio, discovery, target scans/validity and angle/RNG requests stay explicit dependencies until their providers are composed.

Future dispatcher entry proposal: a combat-owned turret branch accepting a shared world and u16 structure index, called by the AI-owned structure dispatcher only for types 10/11 after its original prelude. That proposal is not implemented or validated. Stage 19 first closes building-target consumer/wrapper behavior; turret translation must not broaden this slice before that delivery is integrated.

## Capture plan and evidence state

The next granted heavy window starts with **original-only captures before translation**: direct consumer nonlethal/equality/strict-threshold/accumulator-wrap/scaled-low-word cases; types 3/9/12/20 and ID edges; local-volume/sound/voice boundaries; city-message and sympathy partial stores; mode-1/3/4 wrapper arithmetic and request order; a prepared projectile arrival with a building target. Fixtures must identify loaded characteristic/damage inputs, camera/discovery/handles and every executed original early-return guard. No unknown AI/audio/diplomacy effect is replaced by an empty callback. Snapshot full mapped world/projectile buffers and request order, with named entry stops counted separately from returns. Then translate only the captured bounded behavior and compare it freshly.

| State | Current evidence |
|---|---|
| Static inventory | Passed original SHA-256, 11 interval boundary/hash exports, 15 instruction assertions and the 21-entry type dispatch check; fresh deterministic export verification |
| Implementation | Not started |
| Original-only runtime captures | Not run; heavy slot not granted |
| New differential validation | Not run; no optional-native skip is counted as a pass |
| Domain/common checks | Not run in this light turn; heavy slot not granted |
| Commit/main integration | Pending for this inventory/current Stage 19 work; Stage 18 already integrated |
| Full flow / MONDE01 raid / cave destruction | Not run; no mission claim |

Light commands: `python3 -B pesquisas-paralelas/combate/rastrear_dano_batiment.py`, the same with `--verificar`, and `git diff --check`. No x86, Ghidra, heavy gate, integration or game rebuild runs in this readiness turn. The coordinator owns the consolidated progress estimate.
