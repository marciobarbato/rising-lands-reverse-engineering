# S1 next stops — 2026-10-30

Baseline: merged `origin/main` `9ae3e4d`, including Economy `dfb87bd`.
Only AI/runtime-owned changes and feature pushes are authorized. Original
oracle: intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

| Equal through / stop frame | Stop | Owner | Contract / status |
|---|---|---|---|
| 2546 / 2547 (previous run) | SetSortEngin `0x445fbc`, CALL `0x420f8c` | Economy | AX unit, DX exit cell; native S1 AX=4, DX=`0x0e0f`. Forwarding supplied by `dfb87bd`; fresh strict run now passes this frame. |
| 3276 / 3277 (baseline strict/planning) | MineGetCapacite `0x475541`, CALL `0x44ca17` in CalculWorkEngin | AI/runtime binding; Economy query | AX=u16 mine index; native S1 AX=0, EAX out=`0x31` (49), other six data registers preserved. Fixed in `8b6f1c9`: 101 native comparisons, zero mismatches; both chain reruns pass this frame. |
| 3850 / 3851 (current strict/planning) | SacGetCapacite `0x475736`, InputGame CALL `0x4299da` | Economy | AX=u16 cell; native AX=`0x1f18` (7960), object=`0x43`, quantity=4, EAX out=`0x47860004`. Other six data registers preserved. Exact contract below; no declared planning bypass, chain stopped. |

Strict and `--diagnostico-planejamento` indicator checks use replay-checked
Missions S1 `bab6c7c`, starting after frame 128 and requesting 16,922 frames.
Baseline strict and planning: 3,148 equal frames, 129–3276, no first difference;
stop in frame 3277. Report: [s1-next-strict.json](validacao/s1-next-strict.json).
Current source `8b6f1c9`: **3,722 equal frames, 129–3850**, no first difference;
stop in frame 3851. Report: [s1-mine-strict.json](validacao/s1-mine-strict.json).
Planning: `.local/m3-1/s1-mine-planejamento.json`, zero Graphics bypasses.
Planning output stays under `.local/`; its only declared bypass facility is
Graphics' display-path stops. It cannot bypass a missing logic provider.

S1 pass-2 manifest is absent from latest fetched main `84e4fe7` and Missions
`7eeb395`; no S1 pin, part chains or whole-state proof is claimed.

Original-only mine capture: [consulta-mina-original.json.xz](evidencias/consulta-mina-original.json.xz),
101 returns (real S1 call plus 20 indices × five reserve values); no non-stack
stores or boundaries. The real entry is EAX=0, EBX=`0x101`, ECX=1,
EDX=`0xc16`, ESI=`0x474a8cf0`, EDI=EBP=12, ESP=`0x2007db4`;
return ESP=`0x2007db8`. The only native read is u16 `[0x509956]`=`0x31`.
Snapshot 3250 was copied to ignored `.local/m3/` from Core's read-only native
inputs and hash-checked: `169488a6e34ce20586a087bf846682cdcba8cc2905efbc27f12f43125ae4a884`.
All 28 states, 3250–3277, equal the committed original trajectory; code unchanged.

Binding: `provedores_entrada_ia.consulta_capacidade_mina(m, regs, chamada)`
routes through `DonosM3.externo`, requires known AX in 0..19, returns exact
seven data registers and optional ESP+4, preserves explicit unknown bits and
rejects pushed words. It reads Economy's `RecursosTerreno.capacidade_mina`
on the live 80-byte table; no synthetic constructor or table copy. No mutations
or callbacks; earlier caller effects remain. Evidence was committed at `bb99dac`
before binding. [Native differential](validacao/consulta-mina-native.json)
freshly reproduces all 101 original cases and compares complete and partial
register routes; the real S1 ESP also agrees. Three focused tests pass.

Economy request: provide live-memory **SacGetCapacite**, known AX cell, no
pushed arguments or callbacks. Object `[u32[0x507d74]+cell]` outside `0x42..0x44`
returns EAX=0; inside returns `(u32[0x507dac] & 0xffff0000) | quantity_byte`.
All other data registers are preserved, plain RET advances ESP by four, and
no non-stack byte is written. InputGame's consumer API is
the `SacGetCapacite(celula=u16) -> EAX` callback in `Provedores`; it stores AX to
`0x49620c` at its information-panel tail. Preserve the raw register contract
in the owner provider even though this consumer uses the low word.

[Actual native S1 call](evidencias/s1-parada-saco-original.json): entry
EAX=EBX=ESI=`0x1f18`, ECX=`0x1f00`, EDX=`0x47891000`, EDI=0,
EBP=`0x2007ea4`, ESP=`0x2007e68`; exit EAX=`0x47860004`, ESP=`0x2007e6c`,
all six other data registers unchanged. Type/quantity pointers are
`0x47820000` / `0x47860000`; observed bytes are `[0x47821f18]=0x43` and
`[0x47861f18]=4`. No stores/boundaries. The leased bounded replay checks all
**602 states, 3250–3851**, against the committed native trajectory, code
unchanged (390.908 seconds). This native observation is not a Python
whole-state proof; Python remains stopped inside frame3851.

Validation: [run record](validacao/s1-next-stops-validation.json), **132 tests,
eight explicit skips, zero failures/errors**. Reproduce the contract through
the shared heavy lease with `capturar_parada_s1_ia.py --rotina SacGetCapacite
--chamada 0x4299da --de 3250 --ate 3851 --saida <new-owned-or-local-path>`.
