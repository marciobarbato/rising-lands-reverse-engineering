# S1 next stops — 2026-10-30

Merged main `3e2ed77`; bound Economy in `377c625`, detection in `ad5147a`,
attack dispatch in `64128b5`, reload in `1ce1d6c`. Oracle is intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Indicators start after128, consume replay-checked S1 `bab6c7c`, and request
all 16,922 remaining frames. No first difference has been observed.
On `1ce1d6c`, strict/planning have no first difference. The domain gate passes
141 tests, eight explicit skips. No sound stop is bypassed.

| Equal through / stop frame | Routine / call | Owner | Exact contract / status |
|---|---|---|---|
| 2546 / 2547, resolved | SetSortEngin `0x445fbc`, CALL `0x420f8c` | Economy | AX=unit, DX=exit cell; native 4 / `0x0e0f`. Economy `dfb87bd` resolves; passes later runs. |
| 3276 / 3277, resolved | MineGetCapacite `0x475541`, CALL `0x44ca17` | AI/runtime binding, Economy query | AX=mine index; native 0 → EAX=49. `8b6f1c9`, 101 native comparisons/0 mismatches; passes later runs. |
| 3850 / 3851, resolved | SacGetCapacite `0x475736`, CALL `0x4299da` | AI/runtime binding, Economy query | Native AX=`0x1f18`, object=`0x43`, quantity4 → EAX=`0x47860004`, six other registers preserved. `377c625`, 274 native comparisons/0 mismatches; passes later runs. |
| **10800 / between_frames10801, strict** | AffGame `0x417698`, outer CALL `0x475063`, guard `0x41591f` | **Graphics** | Live monster count2; owner guard proves only0/1. Extend native display domain to2. Declared Graphics planning bypass exists; exact native observation below is at11501. |
| 11662 / frame11663, detection resolved | iabDetection_AjouteEnnemiOuAlerteConflit `0x489b5a`, indirect CALL `0x482e2e` (return `0x482e31`) | AI/runtime binding, Combat synchronous model | Native EAX17, EDX8, EBX17, ECX`0x51ac40`, ESI17, EDI19, EBP`0x2007e18`, ESP`0x2007df8`; group19/battle1 → EAX`0x512380`, EDX1, five preserved. `ad5147a`, 35 fresh native comparisons/0 mismatches; passes latest planning. |
| 11662 / frame11663, attack binding resolved | EnginNextEtape state1/24 `0x456886`; nested CalculAttaqueEngin `0x451914`, CALL `0x4568a3` | AI/runtime binding, Combat body | DI17, ESI`0x474a9254`; EAX1, EBX=EDX`0x1254`, ECX`0x474a9254`, EBP`0x14`, ESP`0x2007e2c`. Combat void body to`0x454ccd`. Bound in `64128b5`; fresh full native parent differential equals all25,197 game blocks/22 changed bytes, zero mismatches; passes planning through11741. |
| 11741 / frame11742, reload resolved | EnginNextEtape reload branch `0x454587` in `0x45442c`, CALL `0x456ead` | AI/runtime placement, Core arithmetic | Native EAX0, EBX0, ECX=ESI`0x474a9254`, EDX3, EDI17, EBP20, ESP`0x2007e2c`: unit17 reload0, limit20, modifier0 → u16`[0x474a9356]`=1. Original243-state capture `6985c60` precedes binding Core `avancar_recarga`. Fresh full parent equals all25,197 game blocks/three changed bytes, zero mismatches; the earlier attack parent is freshly equal too. Passes planning through11752. |
| **11752 / frame11753, planning** | PlaySnd_PostSound `0x48aa79`, CALL `0x4525a1`, return `0x4525a6` (`CalculAttaqueEngin+0xc92`) | **Combat emitter metadata; Audio M3 boundary** | Original pre-CALL EAX`0x50`, EDX`0x2300`, EBX`0x474a9358`, ECX0, ESI`0x474a9254`, EDI=EBP17, ESP`0x2007dbc`; pushed volume90. Forward the original CALL site with four request registers/volume to the existing scenario boundary. Public `CombateRaidVivo.som` omits that site. No declared planning bypass exists; stop here. |

Latest completed strict: **10,672 equal frames, 129–10800**, no difference,
[s1-recarga-strict.json](validacao/s1-recarga-strict.json).
Latest completed planning: **11,624 equal frames, 129–11752**, no difference,
then the sound emitter at11753; 953 declared Graphics bypasses. Report remains ignored:
`.local/m3-1/s1-recarga-planejamento.json`. Planning is diagnostic, never acceptance.

Graphics exact observed contract: [native entry](evidencias/s1-guarda-monstros-original.json)
is at **between_frames11501**, the first available native snapshot after the
strict stop. Entry`0x417698`, CALL`0x475063`: EAX=ESI=EDI=EBP=0, EBX3,
ECX`0xc01d0001`, EDX`0x2007fe8`, ESP`0x2007fe4`; u8/u32`[0x50b178]`=2,
mode`0x12`, view(10,10). Both native states11500/11501 match S1 and code is
unchanged. The display provider consumes live memory, no explicit game-register
arguments. Snapshot11500 was copied/hash-checked from Core's read-only input:
`db59fb6c15913a5ffa8474e54267e3d4b7ef0e7332b87502e73011c7baf58c94`.

The [sound parent observation](evidencias/s1-som-ataque-pai-original.json)
checks all four states11750–11753, unchanged code. Sound-library bodies remain
Missions' explicit unopened-scenario boundaries: unchanged EAX, cleanup4,
no modeled library effects. This is not Audio's real returning-EAX0 provider.
The generic routine-entry observer cannot see a boundary intercepted by the
oracle; that failed attempt is retained in the journal. The successful parent
observation hooks the real CALL before interception, recording all seven data
registers and ESP. The live M3 emitter callback needs original CALL provenance;
AI/runtime supplies the phase. Do not substitute site0 or infer it from the
request after the fact. Combat's subsequent sound requests in that same native
parent are CALL`0x45063f` (EnginInfligeDegat+0x354 return): EAX`0x50`, EDX`0x50100`,
EBX`0x474a89a4`, ECX0, volume180; and CALL`0x4510b1` (InfligeDegat+0x842 return):
EAX`0x50`, EDX`0x50700`, EBX`0x496ac8`, ECX0, volume256. Those later calls and
damage/diplomacy effects have not been consumed by the Python chain. No
undeclared game/sound boundary is suppressed. Snapshot11750 was copied and
hash-checked from Core's read-only native input:
`0399b6dcef842a37ed3a383615a75ed923d6ba7c2b5a5fe5e88000bec1d2eb54`.

New Economy routes: [native differential](validacao/donos-economia-s1-native.json),
**1,058/1,058 equal** (274 sack +273 pipe +511 technology). All seven registers,
ESP, ordered stores, live getter input registers/order/sites and x87 metadata
compare. Raw routes require all seven known registers. The scalar sack projection
marks opaque preserved carriers unknown; no carrier selects behavior/supplies
consumed EAX. Technology uses live owner getters. Detection and attack evidence
are committed before their adapters; no battle/attack algorithm is copied.
Latest completed domain gate: **141 tests, eight explicit skips, zero failures**.

S1 pass-2 manifest is absent on latest fetched main `1531678` and Missions
`7eeb395`. `fixar S1` / strict `tudo --janelas S1` have not run; no whole-state
S1 proof or part chains are claimed. Feature pushes only; no main integration.
