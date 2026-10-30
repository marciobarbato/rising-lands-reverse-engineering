# S1 next stops — 2026-10-30

Baseline: merged `origin/main` `9ae3e4d`, including Economy `dfb87bd`.
Only AI/runtime-owned changes and feature pushes are authorized. Original
oracle: intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

| Equal through / stop frame | Stop | Owner | Contract / status |
|---|---|---|---|
| 2546 / 2547 (previous run) | SetSortEngin `0x445fbc`, CALL `0x420f8c` | Economy | AX unit, DX exit cell; native S1 AX=4, DX=`0x0e0f`. Forwarding supplied by `dfb87bd`; fresh strict run now passes this frame. |
| 3276 / 3277 (fresh strict/planning) | MineGetCapacite `0x475541`, CALL `0x44ca17` in CalculWorkEngin | AI/runtime binding; Economy query | AX=u16 mine index; native S1 AX=0, EAX out=`0x31` (49), other six data registers preserved. Economy's live `RecursosTerreno.capacidade_mina` exists. Missing cross-provider route; original capture complete, binding/differential pending. |

Strict and `--diagnostico-planejamento` indicator checks use replay-checked
Missions S1 `bab6c7c`, starting after frame 128 and requesting 16,922 frames.
Fresh strict and planning: 3,148 equal frames, 129–3276, no first difference; stop in frame
3277. Report: [s1-next-strict.json](validacao/s1-next-strict.json).
Planning: `.local/m3-1/s1-next-planejamento.json`, zero Graphics bypasses.
Planning output stays under `.local/`; its only declared bypass facility is
Graphics' display-path stops. It cannot bypass a missing logic provider.

S1 pass-2 manifest is absent from fetched main `9ae3e4d` and Missions
`7eeb395`; no S1 pin, part chains or whole-state proof is claimed.

Original-only mine capture: [consulta-mina-original.json.xz](evidencias/consulta-mina-original.json.xz),
101 returns (real S1 call plus 20 indices × five reserve values); no non-stack
stores or boundaries. The real entry is EAX=0, EBX=`0x101`, ECX=1,
EDX=`0xc16`, ESI=`0x474a8cf0`, EDI=EBP=12, ESP=`0x2007db4`;
return ESP=`0x2007db8`. The only native read is u16 `[0x509956]`=`0x31`.
Snapshot 3250 was copied to ignored `.local/m3/` from Core's read-only native
inputs and hash-checked: `169488a6e34ce20586a087bf846682cdcba8cc2905efbc27f12f43125ae4a884`.
All 28 states, 3250–3277, equal the committed original trajectory; code unchanged.
