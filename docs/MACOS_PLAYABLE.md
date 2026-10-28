# Local macOS playable consumer

`compilar-jogável` builds **RisingLands-ptbr.app** for this Apple Silicon Mac.
The existing Swift/AppKit/WebKit shell and JSON-lines Python engine are reused.
The new exercise consumes current committed core, combat, economy and graphics
providers from one revision. It is a bounded interactive reconstruction, not a
complete original mission or campaign.

## Build and run

From the repository, run:

```sh
./compilar-jogável
open '/Users/marcio/git/Rising Lands/local-data/macos-playable/dist/RisingLands-ptbr.app'
```

From the workspace, use `./engenharia-reversa/compilar-jogável`. The normal build
fetches `origin/main`, resolves it once to a commit, and uses only that commit's
Git archive, including the app sources and build implementation. Uncommitted
files and other worktrees are never runtime inputs. Fetch failure stops the
build. `--offline` explicitly permits the already fetched `origin/main` object.

Before feature integration, a separate check is available:

```sh
./compilar-jogável --development-ref HEAD
```

It requires a committed revision and writes under `dist/development/`, preserving
the normal delivery. The build prints the absolute bundle path. Generated
sources, assets, runtime, compiler caches, logs and prior bundles remain under
workspace `local-data/macos-playable/`, outside tracked research folders.
Existing preview distributions and historical manifests are untouched.

Prerequisites: macOS 13+ on ARM64, Apple Swift command-line tools, Git, Python
3.9+ for the launcher, the existing extracted Brazilian CD at workspace
`source/cd`, and the existing relocatable CPython 3.12 runtime under
`local-data/macos-preview/dependencies/python`. `RISING_PYTHON_RUNTIME` may select
another compatible existing runtime. No download, Rosetta, Unicorn, system
package installation, notarization or external distribution is performed.

## Player controls and supported exercise

The app opens **Treino livre** paused. Select a friendly unit on the map or in
the left list, click an empty destination, then press **Continuar** (Space).
The destination form also issues movement orders. Drag pans, the wheel zooms,
`.` advances one update, and `R` resets. Speed controls the exercise clock.

* Move the constructor to the yellow supply cell `(4, 9)` and press **Coletar
  sacola**. Move to the cyan depot `(2, 12)` and press **Depositar carga**.
  The supply shrinks and the shared food balance increases on deposit.
* Move the soldier around the wall to `(9, 4)`. Press **Atacar adversário**
  (or right-click the adjacent adversary with the soldier selected), then
  continue. Facing, attack frames, recharge and repeated direct unit damage
  advance on the live clock. A move order interrupts attack.
* The final lethal hit pauses at the explicit missing death continuation.
  Earlier nonlethal damage remains visible; reset starts a new exercise.
* Existing obstacle/wall/free movement labs, manual resource operations and
  targeting queries remain accessible. Mission 1 shows original ETA terrain
  and positions in inspection mode, with simulation controls disabled.

All player-visible text remains Brazilian Portuguese. No replacement audio is
introduced; the original audio files are unchanged, and audio playback is not
integrated in this consumer.

## Provider and input contracts

The 16×16 exercise, wall, initial units, eight food units, one-item exercise
cargo, depot location, objective and 20-update/second clock are **synthetic app
policy**. They are not recovered transport, AI, mission or dispatch rules.
The WebView requests an update every 100 ms; the exercise engine uses monotonic
elapsed time ×20×speed, so coalesced background timers still advance the live
clock. A single response catches up at most one second (160 updates at 8×);
pause/play and speed changes reset the time anchor, preventing an unbounded
sleep/wake replay. Rendering follows current responses. Historical movement
labs retain their explicit 2×speed update quantum. Neither mode reconstructs
the original global timing loop.

| Area | Actual provider and supported inputs | Deliberate boundary |
|---|---|---|
| World | `MundoNavegacao`/`SolucionadorCaminhosPython`, 800×276 writable bytes, 256-stride cells, prepared region/occupancy arrays; three active units on a 16×16 synthetic map | No full ETA world loader or global dispatcher |
| Unit setup | `definir_tipo`, loaded 26×50 original type records, `BonusUnidades` with explicitly zero 1,872-byte fixture state, `capacidade_tipo`; inactive handles and null AI groups | No claim that original mission initialization ran |
| Orders | Committed movement/reset APIs; `ordem_ja_definida` before reset then `ordem_apos_reset` for a stationary, adjacent type-0 attacker, unit-target mode 1 | Pursuit callback is not supplied; out-of-range attacks are rejected before mutation |
| Attack | `ContextoAtaque`/`calcular_ataque`, original type recharge and animation parameters, `avancar_recarga` once per exercise update | No invented phase-2/3 producer, projectiles, magic, full combat dispatch or attack-body artwork |
| Direct damage | `encontrar_vitima_impacto` then `ConsumidorDanoUnidade.infligir`, mode 1; original 26 damage rows and explicitly zero proximity-bonus global `bonus_4965ac`; `ConsultaBonusCombate` and live packed region-grid `ConsultaProximidadeAtaque` | Intentionally excludes `InfligeDegat` reaction/diplomacy/presentation wrapper; default `LimiteMorte` stops before life-zero/death effects |
| Message callback | Only the non-AI-control or null-group no-effect guard is accepted; all other branches raise | No general AI message provider or new native differential claim |
| Audio visibility | Observer camera 3 remains hidden (`descoberto[3][cell] & 31 != 0`); the exercise UI observes the prepared scene independently | Volume/sound callbacks remain unsupported; they raise if reached |
| Economy | `RecursosTerreno.retirar_sacola` and `EconomiaConstrucoes.adicionar` mutate shared supply/balances; exercise cargo is separate UI state | No reconstructed transport caller, automatic harvesting, production completion or spawned units |
| Graphics | `graficos.Catalogo/consultar/rgba`, current original palette and explicit opacity, generated cached body frames for 0/7/9, owner 0, states 2/7, direction 1–16, raw frame 0–7, bag variant 0/1 | Other owners/states/types use labeled markers. No shadow remap, complete indexed scene ordering, lighting cycle or complete game frame |

Missing callbacks raise at their boundary; partial effects remain visible and
are not retried as though they were a continuation. The exercise locks further
actions after its death boundary. Production's partial preparation/conversion/
recovery providers are available in the source revision but are not exposed as
successful recruitment. Save/load, original event scripts, campaigns, audio,
visible death, general structure actions and full-game fidelity remain open.

## Provenance and validation

`Contents/Resources/preview/snapshot.json` records the immutable commit/tree,
requested ref, main/development mode, per-file SHA-256 and last path-changing
feature commits. `assets/fontes.json` binds generated media to the same source
revision and verified original CD hashes. `Info.plist` repeats the revision and
display name. `dist/build-manifest.json` records actual output hashes, logs and
whether the native smoke ran. Prior bundles are preserved under `previous/`.

Every build runs the app-owned consumer suite, verifies every archived source
file and mirrored app source, generated asset hashes, ARM64 executables, local
ad hoc signature, bundled isolated Python imports and a real navigation loop.
It then opens the actual AppKit/WKWebView app and exercises DOM selection,
destination submission, play/pause/speed, movement around the wall, collection,
deposit and two live-clock hits. `native-smoke.json` records the interaction,
positions, health, revision and changed native PNG hashes; `native-smoke.png`
captures the rendered window; paired `.before.png`/`.after.png` files preserve the visual interaction evidence without reading a tainted file-URL canvas. `--skip-ui-smoke` is explicitly an incomplete
headless check and records that fact.

Initial implementation baseline: `5e2bf0831d3aaa776481a6ab023be262ef0df1bd`.
Actual validation results and integration identity are recorded in the
[app handoff](../apps/macos-preview/HANDOFF.md). Historical x86 totals are not
substitutes for these consumer/runtime checks. This app adds no recovered
native algorithm and does not aggregate domain totals into a game-fidelity claim.
