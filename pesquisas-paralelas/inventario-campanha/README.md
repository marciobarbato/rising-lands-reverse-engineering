# Static campaign content inventory

Recommend **MONDE23** if only one additional mission receives full validation.
It ties **MONDE17A** for the most features beyond MONDE01 and concentrates rare
units and a mission-specific monster branch. For two choose **MONDE17A + MONDE23**;
for three choose **MONDE17A + MONDE23 + MONDE25**.

| Additional missions (MONDE01 is baseline) | New static features | Excluding research declarations | Main additions |
|---|---:|---:|---|
| MONDE23 | 59 / 88 | 33 / 62 | SPEEDER, BUNKER, CEIFEIRO, BOMBARDEIRO, SUN, MECÂNICO; monsters 20–24; CRISTAL, BARRACA DE CAMPANHA; BIBLIOTECA condition; special monster path |
| MONDE17A | 59 / 88 | 33 / 62 | Broad structures, including HANGAR/ELEVADIÇA; CAPITÃO; invention/opponent-force conditions; ghost and raid-group tables |
| MONDE17A + MONDE23 | 77 / 88 | 51 / 62 | Combines the two concentrations |
| MONDE17A + MONDE23 + MONDE25 | 82 / 88 | 56 / 62 | Initial attack records and additional raid-group mask bits |

These are equally weighted **static selectors, not measured code coverage**.
The 26 additional research declarations occur in every recommended later stage;
excluding them preserves the winning sets. Greedy's lexical tie-break picks
MONDE17A first, then MONDE23 and MONDE21. The recommended triple ties that score
and prefers MONDE25 for its initial attack records. All ties are published.

**No two- or three-map complete cover exists for this feature set.** An exact
minimum is seven additional maps: **MONDE02, MONDE06, MONDE07, MONDE08, MONDE17A,
MONDE23, MONDE25**. Unique features force 02/06/07/08/23; they leave 13 features,
and any one remaining map supplies at most nine. The exhibited seven cover all.
The recommended triple still misses CASERNA/SANTUÁRIO condition parameters,
MONDE06's illumination override, MONDE08/13's owner tally, initial HELIPORTO and
initial DRUÍDA. Keep automatic checks for these exceptions.

## Files and campaign order

- [overview.json](overview.json): compact per-map sizes, entities by owner/type/state,
  starting resources, end conditions and raid/attack summaries.
- [inventory.json](inventory.json): **38 ETA files, 25 numbered stages, 2,604 campaign
  units, 25 briefing identities, plus five non-campaign NET maps**; source hashes,
  record offsets, raw conditions, auxiliary tables, layers and explicit unknowns.
- [matrix.json](matrix.json): 43 maps × binary columns in `feature_ids` order.
- [coverage.json](coverage.json): greedy steps, exhaustive optimal pairs/triples,
  exact minimum/certificate, rare features, absent initial entity types and NET-only
  features; separate analyses exclude research declarations or include all ETA files.
- [source-proof.json](source-proof.json): **73 original files** compared byte-for-byte
  with BIN sectors. BIN SHA-256:
  `c2c09e87927cf5ebbe5d17ea17bffb53c82c2e68385e9259ad0453cc15ea616f`.

`MissionNext 0x46c08c` increments stages; the existing `MakeMissionName 0x46c1b8`
reader selects 34 ETA files. Stage 9 uses A–D from the variant byte; 10/12/17
use A–C from signed sympathy. Unsuffixed MONDE09/10/12/17 exist but are never
selected by that routine; they remain fully inventoried and flagged. Excluding
them preserves the feature universe/minimum. NET maps have unknown session
controls and are excluded from campaign recommendations.

## Features present in only one or two ETA files

Full individual lists are in `coverage.json` (both all-ETA and selectable scopes).
“Initial” does not imply “only obtainable there.”

| Static feature group | Maps |
|---|---|
| Initial SPEEDER/BUNKER/SUN, ESMAGADOR/LANÇADOR, CRISTAL/BARRACA DE CAMPANHA; BIBLIOTECA condition; special monster path | MONDE23 |
| Initial DRUÍDA / HELIPORTO | MONDE07 / MONDE08 respectively |
| Initial CEIFEIRO / BOMBARDEIRO | MONDE04+23 / MONDE13+23 respectively |
| Initial BUKKA/ESTALADOR | MONDE23, MONDE24 |
| CASERNA condition / stone-threshold kind | MONDE02 / MONDE01 respectively |
| ARMAZÉM condition | MONDE01, MONDE14 |
| Illumination override / structure-owner tally | MONDE06 / MONDE08+13 respectively |

## Confidence and limits

**High confidence in bytes; moderate confidence in selection value.** All maps
and briefings match the earlier Missions inventory, ETA block boundaries match,
and all 73 consumed files match the supplied BIN. Existing ETA/unit/INI/type,
condition/objective and filename readers are reused. Reader and executable-range
hashes are recorded. Original RISING.EXE SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

Counts retain disk owner/state plus documented load-time owner overrides; lodged
state 14 is included. Player 0 human / 1–3 AI are new-campaign conventions,
**not serialized per-map controls**. Owner 200 stays an unclassified sentinel.
Actual alliances, weather, live illumination and unlocked research/buildings/spells
remain unknown. All 81 INI research declarations and five spell declarations are
recorded; MISSION/APPARITION gates do not establish per-owner invention state.

Conditions retain raw bytes and the existing evaluator's meanings; zone wildcard
is 255, not 65535. Defeat also depends on live count/latch state, not an invented
disk defeat kind. Objective-list words are all 65535 across campaign maps and
are separate from end conditions. Influence rectangles are decoded; tail words
and the 917,504-byte suffix remain unknown. Raw terrain IDs and unknown fields
do not inflate the score. Global EVENTS.INI IDs are not mission numbers.

Monster entries retain cell, mask, disk period and loader period×30 modulo 65536;
profile groups use the shipped MONSTRE.INI and original lookup at 0x498400.
Mask bit 15 references an undeclared group. Activation, RNG, compaction and actual
profile binding remain runtime dependencies; MONDE23 has a special path.
Attack records are not proven active attacks; 0x0f-filled entries in MONDE12
variants/MONDE14 remain uninterpreted. Food-field/sack summaries use documented
economy codes and account for object 54→66/quantity1 normalization.

**Next: original load + bounded short-window coverage run** for the selected
missions, with real campaign carry-over. Confirm controls, technology, visibility,
alliances, raids and reached routines; orders/longer windows must then exercise
spells, construction, production, transport and endings. Neither three nor seven
static maps proves dynamic full-game coverage. No game execution, native comparison
or fidelity acceptance is claimed here; see [validation.json](validation.json).

## Reproduce

Run in this worktree with existing dependencies. Omit `--check` to regenerate;
outputs stay beside the scripts. Original inputs and existing repo files are
never written. Format, identity and reproduction failures propagate.

```sh
python3 -B pesquisas-paralelas/inventario-campanha/campaign_inventory.py \
  --cd-root '/Users/marcio/git/Rising Lands/source/cd' --check
python3 -B pesquisas-paralelas/inventario-campanha/verify_campaign_media.py \
  --bin-image '/Users/marcio/git/Rising Lands/source/RISING_LANDS_BR_.BIN' \
  --cue '/Users/marcio/git/Rising Lands/source/RISING_LANDS_BR_.CUE' \
  --cd-root '/Users/marcio/git/Rising Lands/source/cd' \
  --cdrom-reader '/Users/marcio/git/Rising Lands/legacy-prototype/tools/cdrom.py' \
  --check
```
