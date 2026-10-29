# Hidden difficulty check — static findings

**No general player-selectable difficulty level was established. There are
active, undocumented monster-targeting INI controls and inactive AI
configuration hooks.** Ordinary mission tuning is also present. This is static
research, not a behavior change or a claim that every UI/indirect path is known.

## Evidence labels

- **Byte fact:** hash-pinned original bytes or file fields at recorded offsets.
- **Static interpretation:** disassembled control/data flow; no new execution.
- **Existing owner proof:** published Python/native comparisons, reused read-only
  and cited separately. This front ran **zero emulated calls**.

All observations refer to intact RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The [inventory](evidence/static-scan-v1.json) records every input identity and
all file offsets. [Reviewed original instructions](evidence/reviewed-routines.asm)
and the [initial audit](RESEARCH.md) precede the reproducibility-tool commit.

## Candidates and classification

| Candidate | Storage / reader | Finding and confidence |
| --- | --- | --- |
| `HumanOnly` | u8 `0x50a9bc`; `AvanceMonstre` read at `0x47b464` | **Active hidden monster setting.** `[GENERAL]` key absent from shipped `MONSTRE.INI`, default 0. Nonzero makes pending target selection reject PlayerGetType 2 (AI). Byte facts + static interpretation; owner loader/raid proofs exist. |
| `ProbaCaveJoueur`, `ProbaCaveIA`, `ProbaEmbuscade` | u32 `0x50a9c0/c4/c8`; reads `0x47b533/54f/569` | **Active hidden targeting weights**, absent keys, defaults 5/2/2. The ordinary Random%100 branch tests cumulative thresholds: local-player cave, chosen-player cave, ambush, otherwise field. Guards, retries, fallback and the special type 0x18 branch matter. The name CaveIA does not guarantee an AI target. These are not a global economy/damage difficulty multiplier. |
| AI named configuration / modes | `iaConfigGetValue 0x47fc54`; mode tables `0x498c10`, `0x498c38`, `0x498cb0`; unit force weights `0x498cf4` | **Inactive configuration hook / tactical tuning.** Getter bytes `89d8c3` are exactly `mov eax,ebx; ret`: every caller receives its default, without reading a config file. Init tables contain survival/economy/war frequencies and weights. `iaSetMode 0x47f8b7` selects a player's city/resource/war mode; no global difficulty selector follows from its name. Static interpretation, consistent with existing AI reset proof. |
| ETA monster table | disk `(cell:u16,mask:u16,period:u16)`; `LoadEntrerMonstre 0x47ac30`, RAM `0x50a9d0+12k`; spawn `ConstruitGroupeMonstre 0x47a81d` | **Per-mission raid tuning.** Masks select fixed MONSTRE.INI group compositions at `0x50af84`, periods are multiplied by 30 into a u16 and consumed by `AvanceMonstre`. They vary across the 38 missions; they are not a second difficulty field. Byte facts + static interpretation and existing owner proof. |
| ETA 16-byte Divers area | `LoadCalculMissionDivers 0x47c30f` | **Unused on this load path.** Values vary in five patterns across 38 files, so they are not all constant. The routine reads 16 individual bytes into stack scratch and discards them without persistent stores. Their editor-era meaning remains unknown; calling them a live difficulty control is unsupported. |
| Recruitment/gathering/growth rates | `RISING.INI`; type table `0x4965ae+50*type`, structure table `0x495d8c+52*type`, growth period `0x4973ea` | **Global type/balance data, not a difficulty selector.** TMPSRECRUTE +0 and RECHARGE +0x30 are per-unit-type words loaded by EnginLoadCaract 0x44188b; structure TMPSCONSTRUCTION+4 by BatimentLoadCaract 0x418c70. DIVERS.VEGETREPOUSSE=128 goes to `0x4973ea`; SetUpdateChamp 0x475328/UpdateChamp 0x478806 consume it. No difficulty-level lookup was identified in these inspected loaders/consumers. |
| Objective thresholds / resources | ETA conditions→`0x4e1d20`; TestFinDeMission 0x458606, starting resources→`0x4e2ea8` | **Scenario objectives and starting state.** MONDE01 requires a type 3 cave and food/stone 50, per the owner evaluator. Those 50 values are objective thresholds, not initial balances or difficulty settings. Other missions supply different conditions/resources. |

## Writer and UI reachability limits

A linear scan of the original 601,088-byte text section found 19 **absolute**
operands for the four monster settings: 15 writes in InitEntrerMonstre,
ReadConfigMonstre 0x47aba9 and ChargeMonstre 0x47b796, plus four AvanceMonstre
reads. Two indexed operands with the same displacement are separately labeled;
they address the record initializer, not these absolute globals.

InitEntrerMonstre is directly called by LoadEntrerMonstre; ChargeMonstre by
IaLoad (`0x47fb95`). Both read the profile keys. ReadConfigMonstre repeats the
same profile queries, but no direct CALL/JMP to it was found. There are 78 direct
call sites to iaConfigGetValue across initialization/save routines, all pointing to
the unchanged default-return stub.

**No menu writer was found in that bounded absolute/direct-reference scan.**
This does not prove that no UI path can ever set them: pointer aliases,
indirect calls, unrecognized instruction/data boundaries and other file paths
remain outside the negative claim. Absence of a difficulty-named symbol is not
used as proof. No UI setting was invented or enabled.

## Corpus and MONDE01 examples

The unchanged `ferramentas/formatos.py:ler_eta` parsed all 38 CD WORLD/MONDE*.ETA
files, including 09/10/12/17 variants: 100 six-byte disk monster slots and 10
condition slots each; 436 slots have a non-ffff cell. Empty cells and zero-period
ambush locations are distinguished from timed raids in the inventory.
MONDE01 has two timed entries: disk offsets `0x53770` and `0x53776`, group mask1,
periods 300 and 360 → loaded 9000 and 10800 logic-counter units. Its three other
nonempty cells have period 0/mask 0; they are not three additional timed raids.

The common 0xe0000-byte ETA suffix is hash-recorded but not consumed by this
known MissionLoad path. Its existence is not proof of an unused difficulty
parameter or of global non-use by every editor/save/load path.

## Reproduce / remaining questions

```sh
python3 -m pip install --target .local/python capstone==5.0.7
PYTHONPATH=.local/python python3 -B pesquisas-paralelas/dificuldade/difficulty_scan.py \
  --cd '/Users/marcio/git/Rising Lands/source/cd'
PYTHONPATH=.local/python python3 -B -m unittest discover \
  -s pesquisas-paralelas/dificuldade/testes -v
```

Verification compares the recorded artifacts without rewriting them. No
original executable, INI or ETA is modified. The tool is a static reader,
not an engine routine. Owner references: [mission loaders](../missoes/HANDOFF.md),
[AI raid](../ia-runtime/HANDOFF.md), [rates](../../docs/ECONOMY.md),
[objective evaluator](../../docs/MISSIONS.md#supported-domain).

A complete UI/indirect-call reachability audit would be needed for a stronger
negative claim. The editor meaning of the discarded 16 bytes and remaining
suffix is open. Changing INI settings, testing their balance effect or adding
a difficulty option is deliberately outside this workstream.
