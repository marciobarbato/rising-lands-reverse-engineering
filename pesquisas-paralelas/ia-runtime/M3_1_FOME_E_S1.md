# M3.1 — hunger wiring, window reach after the minimap fix, S1 by parts (AI/runtime)

Third M3.1 step. Main `3e0de77` (Economy's BatimentModifyMap DL = 1) and then `fcc0ba8` (Core's `fadiga_vegetacao`) merged. Python only, against Missions' committed native captures; the one new leaf is checked against the original bytes under Unicorn.

## Frame 2178 passes; P6 is equal in the whole state through 2400 (diagnostic)

`provar_entrada_janelas_ia.py janela P6 --parte N --diagnostico-planejamento` at main `3e0de77`, all three parts, under the heavy lease. A Graphics display-path stop is recorded and its drawing taken as writing no logic byte, so this is never evidence:

| Part | Frames | Phases equal | Chain |
|---|---|---|---|
| 0 | 129–1128 | 2,000 / 2,000 | `a3f35dfc7701065f…` (as before) |
| 1 | 1129–2128 | 2,000 / 2,000 | `5da71fab9ac33cb3…` (as before) |
| 2 | 2129–2400 | 544 / 544 | `c557167f801fbdc0…` |

Zero crossings. The 196 minimap bytes at frame 2178 are now equal: the cause was Economy's missing DL = 1 for BatimentModifyMap (fixed in `aef912b`). `reproduzir` reran part 2 after the Core merge and got the same chain.

## How far each window goes (main `fcc0ba8` + this branch)

P6 is compared in the whole state. The other probes have no pass-2 capture, so `provar_entrada_ia.py` compares them at indicator level, every frame (inputs, orders, RNGs, CRT seed, 0x4e1d18, view, selection, objective block, units 11..15 whole records).

| Window | Strict | Planning diagnostic | Stop, owner |
|---|---|---|---|
| P6 (whole state) | 129–220, stops at `between_frames221` | 4,544/4,544 phases, 129–2400 | AffBatiments logic effects for the CAVE states [0, 2, 5]: **Graphics** |
| P3 | 129–220, stops at `between_frames221` | 3,001/3,001 frames, to 3129 | the same guard: **Graphics** |
| P7 | 129–220, stops at `between_frames221` | 2,672 frames, stops at frame 2801 | strict: **Graphics**; planning: TerrainEstGc 0x44d8cd (object ≥ 0x1d) from CalculWorkEngin: **Core** (in progress) |
| K1 | **501/501, to 629 (complete)** | 501/501 | none |
| P4 | 331 frames, stops at frame 460 | the same | TerrainEstGc 0x44d8cd: **Core** |
| P5 | 631 frames, stops at frame 760 | the same | SetMiniMap 0x44c437 from CalculWorkEngin: **Core** |

The Graphics view-origin stops from the last round (K1 141, P4 422, P5 572) are gone on main. K1 is equal over its whole window in strict mode, and P4/P5 reach Core's stops without any Graphics stop.

## Wiring (commit `8b8c984`, then the merge)

- **Unit state 19.** `construcao_entrada_ia.proxima_etapa_entrada` continues the pinned switch's stop at 0x4554db (table 0x4543c8 entry 19) in `EnginNextEtape:state19`. That provider is Economy's `alimentacao.estado_fome`, with ESI = the record and DI = the unit. EBX, ECX and EBP enter as 0: the body overwrites EBX and EBP before reading them, and sets CX = DI before using ECX as the unit index. ECX's high word is 0 at all 231 entries of Economy's native capture.
- **Its callees** (`DonosM3._externo_fome`):
  - Core's BatimentAdjacent, DeplaceEngin, TerrainEstDecouvert and EnginGetVolume, through `provedor_entrada`;
  - BatimentGetType, BatimentGetPlayer and BatimentEnDestruction, through `EntradaEstruturas.chamar`;
  - Economy's TestRessource (`ordens_economia`), Core's ChercheVegetLibre (`fadiga_vegetacao`) and the sound boundary.

  When a callee returns a register the body did not pass, and that register comes back unchanged and fully uncertain, the body keeps its own value: the callee preserved it.
- **TerrainGetSacType 0x476038** is a 13-instruction read-only leaf, translated here with every register (`entrada_quadro_ia.terrain_get_sac_type`). Under Unicorn it equals the original bytes for all 256 object bytes and two register files (512 cases); a mutation of its range fails the test.
- **Core `fadiga_vegetacao`** (main `fcc0ba8`):
  - EnginSetFatigue at 0x45498f, installed as the pinned provider `EnginSetFatigue`;
  - ChercheVegetLibre and ChercheTypeBatimentProximite;
  - EteintTerrain, which serves Economy's SortieTroupe abandonment (0x421116).

  Its hungry voice is recorded with the CALL site 0x44b33d, which `fadiga_vegetacao` declares in its own named stop.
- **Economy's SortieTroupe abandonment** (main `3e0de77`) needs no new route: its callees are BatimentGetCase and BatimentModifyMap (DL 1) through `provedor_entrada`, and EteintTerrain through `fadiga_vegetacao`.
- **Generic route.** A Core routine reaches its caller as soon as Core exports it through `provedor_entrada` (`ROTINAS_ECONOMIA`), `EntradaEstruturas.ROTINAS` or `fadiga_vegetacao.ROTINAS`. TerrainEstGc ≥ 0x1d and the SetMiniMap mode at 0x44c437 will route the same way.
- **Still named stops on the hunger path:** BatimentEnleveMatiere 0x4235bd and EnginRestaureEtat 0x45315f (**Economy**, both not translated yet). EnginRestaureEtat ends every meal, so S1 is expected to stop there first, at about frame 8057, unless Economy lands it.

## S1 by parts (ready for the capture)

`provar_entrada_janelas_ia.py` now has an S1 entry, unpinned until the Mac mini's pass-2 capture lands on feat/re-missions. Steps:

```
python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py fixar S1 --ref origin/feat/re-missions
git commit pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py
python3 -B pesquisas-paralelas/ia-runtime/provar_entrada_janelas_ia.py tudo --janelas S1 \
    --lease "<coordination>/heavy_lease.py" --saida pesquisas-paralelas/ia-runtime/validacao/m3-1-prova-s1.json
```

- `fixar` resolves the ref to a commit and rewrites the S1 entry with the SHA-256 of the manifest, comandos and entradas plus that commit. First it checks, in that commit, every part against the manifest, the mask, the passed policy and both logs. Until the files reach the checkout they are read from that commit with `git show` and cached under `.local/m3-1/ref/S1/<commit>/`. A file is taken from the checkout only when its hash matches. The dry run on P6 reproduced P6's pinned hashes.
- `tudo` runs every part as its own process, one heavy-lease slot each, starting from that part's checkpoint (about 1.9 GB peak RSS and about 8 minutes per 1,000-frame part when the machine is idle). `--partes N …` runs a subset; `--diagnostico-planejamento` runs the Graphics planning diagnostic (`.local` only).
- **Allocation records.** The frame-128 records apply up to a part's first phase that allocates or releases a block. The part stops at the last whole frame before that phase (`allocation_stop`), and `agregar` refuses every later part. S1's result screen (MenuInit at 17032) is past any expected stop.
- `agregar` accepts missing part reports. For each window it reports a `reach` block: the parts equal from the start, the frame they reach, the first stop with its routine and site, and every equal part. It also prints each part's `phase_chain_sha256`. A proof that is not accepted goes to `.local/` with all of this.
- **Second machine.** `reproduzir <proof.json> --janela S1 [--partes …] --lease …` reruns the parts and compares each chain and result with the proof. Tried on P6 part 2: 1/1 equal.

## P6 strict

The strict proof needs Graphics' extension of the AffBatiments logic-effects guard, which is not on feat/re-graphics yet. Once it lands: merge origin/feat/re-graphics locally (never committed), run `tudo --janelas P6`, and write `validacao/m3-1-prova-p6.json` only from main-only code.
