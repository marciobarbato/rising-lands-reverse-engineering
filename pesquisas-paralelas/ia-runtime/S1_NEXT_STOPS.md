# S1 next stops — 2026-10-30

Merged main `3e2ed77`; bound Economy in `377c625`, detection in `ad5147a`,
attack dispatch in `64128b5`. Oracle is intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Indicators start after128, consume replay-checked S1 `bab6c7c`, and request
all 16,922 remaining frames. No first difference has been observed.
The attack-bound strict/planning indicators and 140-test gate have passed their
compared prefixes. Reload is now bound/native-proved; the next strict/planning reruns are pending.

| Equal through / stop frame | Routine / call | Owner | Exact contract / status |
|---|---|---|---|
| 2546 / 2547, resolved | SetSortEngin `0x445fbc`, CALL `0x420f8c` | Economy | AX=unit, DX=exit cell; native 4 / `0x0e0f`. Economy `dfb87bd` resolves; passes later runs. |
| 3276 / 3277, resolved | MineGetCapacite `0x475541`, CALL `0x44ca17` | AI/runtime binding, Economy query | AX=mine index; native 0 → EAX=49. `8b6f1c9`, 101 native comparisons/0 mismatches; passes later runs. |
| 3850 / 3851, resolved | SacGetCapacite `0x475736`, CALL `0x4299da` | AI/runtime binding, Economy query | Native AX=`0x1f18`, object=`0x43`, quantity4 → EAX=`0x47860004`, six other registers preserved. `377c625`, 274 native comparisons/0 mismatches; passes later runs. |
| **10800 / between_frames10801, strict** | AffGame `0x417698`, outer CALL `0x475063`, guard `0x41591f` | **Graphics** | Live monster count2; owner guard proves only0/1. Extend native display domain to2. Declared Graphics planning bypass exists; exact native observation below is at11501. |
| 11662 / frame11663, detection resolved | iabDetection_AjouteEnnemiOuAlerteConflit `0x489b5a`, indirect CALL `0x482e2e` (return `0x482e31`) | AI/runtime binding, Combat synchronous model | Native EAX17, EDX8, EBX17, ECX`0x51ac40`, ESI17, EDI19, EBP`0x2007e18`, ESP`0x2007df8`; group19/battle1 → EAX`0x512380`, EDX1, five preserved. `ad5147a`, 35 fresh native comparisons/0 mismatches; passes latest planning. |
| 11662 / frame11663, attack binding resolved | EnginNextEtape state1/24 `0x456886`; nested CalculAttaqueEngin `0x451914`, CALL `0x4568a3` | AI/runtime binding, Combat body | DI17, ESI`0x474a9254`; EAX1, EBX=EDX`0x1254`, ECX`0x474a9254`, EBP`0x14`, ESP`0x2007e2c`. Combat void body to`0x454ccd`. Bound in `64128b5`; fresh full native parent differential equals all25,197 game blocks/22 changed bytes, zero mismatches; passes planning through11741. |
| 11741 / frame11742, reload bound; rerun pending | EnginNextEtape reload branch `0x454587` in `0x45442c`, CALL `0x456ead` | AI/runtime placement, Core arithmetic | Native EAX0, EBX0, ECX=ESI`0x474a9254`, EDX3, EDI17, EBP20, ESP`0x2007e2c`: unit17 reload0, limit20, modifier0 → u16`[0x474a9356]`=1. Original243-state capture `6985c60` precedes binding Core `avancar_recarga`. Fresh full parent equals all25,197 game blocks/three changed bytes, zero mismatches; the earlier attack parent is freshly equal too. |

Latest completed strict: **10,672 equal frames, 129–10800**, no difference,
[s1-ataque-strict.json](validacao/s1-ataque-strict.json).
Latest completed planning: **11,613 equal frames, 129–11741**, no difference,
then reload at11742; 942 declared Graphics bypasses. Report remains ignored:
`.local/m3-1/s1-ataque-planejamento.json`. Planning is diagnostic, never acceptance.

Graphics exact observed contract: [native entry](evidencias/s1-guarda-monstros-original.json)
is at **between_frames11501**, the first available native snapshot after the
strict stop. Entry`0x417698`, CALL`0x475063`: EAX=ESI=EDI=EBP=0, EBX3,
ECX`0xc01d0001`, EDX`0x2007fe8`, ESP`0x2007fe4`; u8/u32`[0x50b178]`=2,
mode`0x12`, view(10,10). Both native states11500/11501 match S1 and code is
unchanged. The display provider consumes live memory, no explicit game-register
arguments. Snapshot11500 was copied/hash-checked from Core's read-only input:
`db59fb6c15913a5ffa8474e54267e3d4b7ef0e7332b87502e73011c7baf58c94`.

New Economy routes: [native differential](validacao/donos-economia-s1-native.json),
**1,058/1,058 equal** (274 sack +273 pipe +511 technology). All seven registers,
ESP, ordered stores, live getter input registers/order/sites and x87 metadata
compare. Raw routes require all seven known registers. The scalar sack projection
marks opaque preserved carriers unknown; no carrier selects behavior/supplies
consumed EAX. Technology uses live owner getters. Detection and attack evidence
are committed before their adapters; no battle/attack algorithm is copied.
Latest completed domain gate: **140 tests, eight explicit skips, zero failures**.

S1 pass-2 manifest is absent on latest fetched main `1531678` and Missions
`7eeb395`. `fixar S1` / strict `tudo --janelas S1` have not run; no whole-state
S1 proof or part chains are claimed. Feature pushes only; no main integration.
