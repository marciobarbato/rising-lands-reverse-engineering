# S1 next stops — 2026-10-30

Measured source: `377c625`, after merging main `3e2ed77`. Oracle is intact
RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Both indicators start after frame128, consume replay-checked S1 `bab6c7c` and
request all 16,922 remaining frames. Neither has a first difference.

| Equal through / stop frame | Routine / call | Owner | Contract / status |
|---|---|---|---|
| 2546 / 2547 (historical) | SetSortEngin `0x445fbc`, CALL `0x420f8c` | Economy | AX=unit, DX=exit cell; native 4 / `0x0e0f`. Resolved by `dfb87bd`; passes current runs. |
| 3276 / 3277 (historical) | MineGetCapacite `0x475541`, CALL `0x44ca17` | AI/runtime binding, Economy query | AX=mine index; native 0 → EAX=49. Fixed in `8b6f1c9`, 101 native comparisons/0 mismatches; passes current runs. |
| 3850 / 3851 (historical) | SacGetCapacite `0x475736`, CALL `0x4299da` | Economy / AI-runtime binding | Native AX=`0x1f18`, object=`0x43`, quantity=4 → EAX=`0x47860004`, six other registers preserved. Bound in `377c625`, 274 fresh native comparisons/0 mismatches; passes current runs. |
| **10800 / between_frames10801 (strict)** | AffGame `0x417698`, outer CALL `0x475063`, guard `0x41591f` | **Graphics** | Two-monster display domain; current guard supports 0/1. Extend native proof/guard for count=2; no logic difference before stop. Declared planning display bypass exists. |
| **11662 / frame11663 (planning, rerun pending)** | iabDetection_AjouteEnnemiOuAlerteConflit `0x489b5a`, indirect CALL `0x482e2e` | **AI/runtime** | Native EAX=17, EDX=8, group19/battle1 → EAX=`0x512380`, EDX=1. Original capture `a0fedec`; existing Combat synchronous model now bound, 35 fresh native comparisons/0 mismatches. |

Strict: **10,672 equal frames, 129–10800**,
[s1-economia-strict.json](validacao/s1-economia-strict.json).
Planning: **11,534 equal frames, 129–11662**,
`.local/m3-1/s1-economia-planejamento.json`; 863 declared AffGame bypasses,
starting at between_frames10801. Planning is diagnostic, never acceptance.

Graphics exact observed contract: [native entry](evidencias/s1-guarda-monstros-original.json)
is at **between_frames11501**, the first available native snapshot after the
strict stop, not a fabricated frame10801 register file. AffGame entry
`0x417698`, CALL `0x475063`: EAX=ESI=EDI=EBP=0, EBX=3, ECX=`0xc01d0001`,
EDX=`0x2007fe8`, ESP=`0x2007fe4`; u8/u32 `[0x50b178]`=2, mode `0x12`,
view (10,10). Both native states 11500/11501 match S1 and code is unchanged.
The display provider consumes live memory, no explicit game-register arguments.
Snapshot11500 was copied from Core's read-only native inputs and hash-checked:
`db59fb6c15913a5ffa8474e54267e3d4b7ef0e7332b87502e73011c7baf58c94`.

New Economy routes: [native differential](validacao/donos-economia-s1-native.json),
**1,058/1,058 equal**, no mismatches (274 sack + 273 pipe + 511 technology).
All seven registers, native ESP, ordered stores, every live foreign getter's
seven-register input, call order/sites and x87 push metadata compare.
The scalar sack projection marks preserved carriers unknown; no carrier selects
behavior or supplies the consumed EAX. Technology uses live owner getters.
Domain gate: **135 tests, eight explicit skips, zero failures/errors**.

S1 pass-2 manifest is absent on latest fetched main `1531678` and Missions
`7eeb395`. `fixar S1` / strict `tudo --janelas S1` have not run; no whole-state
S1 proof or part chains are claimed. Only feature pushes; no main integration.
