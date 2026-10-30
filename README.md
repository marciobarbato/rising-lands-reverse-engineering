# Rising Lands reverse engineering — Brazilian edition

Evidence-based reconstruction of the Brazilian PC release of Rising Lands. The project includes file readers, a Python reconstruction validated phase by phase against the original `RISING.EXE` under emulation, a native Rust engine validated against that reference, and a macOS app that runs the Rust engine. The complete game and campaign are still under reconstruction.

**Status (2026-10-30 19:10).** M1 (MONDE01 load) and M2 (frames 0–9,200 without input, first raid) are accepted. **M3.1** has its P1/P2 and P6 parts accepted (whole state per phase, reproduced on two machines); the S1 window is open, with the Python chain equal to the original through frame 10,800 of 17,050. On the original executable, the scripted session S1 **wins MONDE01** and D1 reaches the **defeat** branch (both replay-checked from F0). The macOS app plays MONDE01 live on the Rust engine with player orders and the original sound effects at 60 game frames/s, up to the engine's named coverage limits. Measured indicators are at the top of [PROGRESS](docs/PROGRESS.md); acceptance records are in [`integracao/validacao/`](integracao/validacao/); the latest coordinator handover is [HANDOVER_CLAUDE_20261030_1910](docs/HANDOVER_CLAUDE_20261030_1910.md).

**Documentation is English. All player-facing text, mission stories, objectives, unit names, and audio stay Brazilian Portuguese (PT-BR).** Original French SBL symbols and established Python identifiers remain unchanged so evidence and APIs stay traceable.

Start with [consolidated progress](docs/PROGRESS.md), [the documentation index](docs/README.md), [current status](docs/STATUS.md), [the roadmap to a running original mission](docs/ROADMAP_MONDE01.md), [the M3/M4 plan](docs/M3_PLAN.md), and [the parallel workflow](docs/PARALLEL_WORK.md). The [restart prompt](docs/RESTART_PROMPT.md) describes the coordinator's working mode and the front assignments.

## Repository map

| Path | Purpose |
|---|---|
| `docs/` | Current English manuals, contracts, ownership, handovers, and restart instructions |
| `ferramentas/` | Shared readers, simulation primitives, and x86 harnesses; stable API paths |
| `testes/` | Core unit, corpus, and differential tests |
| `evidencias/` | Original-byte assembly, decompiler exports, and provenance manifests |
| `relatorios/` | Versioned extracted data and validation results (for example the S1 coverage survey) |
| `pesquisas-paralelas/combate/` | Combat research and its own tests/evidence |
| `pesquisas-paralelas/economia/` | Economy research and its own tests/evidence |
| `pesquisas-paralelas/graficos-animacao/` | Graphics research, the render API, and its own tests/evidence |
| `pesquisas-paralelas/missoes/` | Mission loading, frame oracles, and the scripted-input captures on the original (probes P1–P7/K1, S1 victory, D1 defeat in `m3/`) |
| `pesquisas-paralelas/ia-runtime/` | Frame/unit/structure dispatchers, AI kernels, the input path, and the chain proofs (M2, M3.1) |
| `pesquisas-paralelas/audio/` | Sound banks, ADPCM decoding, the sound-request queue and provider |
| `pesquisas-paralelas/mapa-acoes-jogador/` | Static player-action map (input, command dispatch, effect entry points) used to plan M3 |
| `pesquisas-paralelas/dificuldade/` | Static check for hidden difficulty parameters |
| `motor/` | Native Rust engine (cargo workspace, C ABI for Swift and Python); validated by `motor/validate.sh` on every integration; see [ENGINE](docs/ENGINE.md) |
| `integracao/` | Coordinator-owned provider loaders for same-process consumers |
| `integracao/validacao/` | Coordinator acceptance records and main reproductions per milestone (M1, M2.1–M2.3, M3.1 P1/P2) |
| `apps/macos-preview/` | macOS app source (Swift shell on the Rust engine and renderer; live play with orders); generated payloads stay local; see [macOS playable](docs/MACOS_PLAYABLE.md) |
| `compilar-jogável` | Builds `RisingLands-ptbr.app` from one committed revision |
| `scripts/` | Worktree preparation, checks, and serialized integration (`workstream.py`) |
| `ghidra/` | Reproducible analysis scripts and manifests; projects remain local |
| `.local/` | Ignored local dependencies, toolchains, and scratch data |

The surrounding workspace is a separate directory, not a Git repository. Its [workspace guide](docs/WORKSPACE.md) explains originals, converted assets, the legacy prototype, archived releases, and worktrees. Existing Portuguese module paths are retained as API compatibility paths.

## Quick checks

Run from this repository root, with Python 3.9 or newer:

```sh
python3 -B scripts/check.py
```

Synthetic tests run without the original game. Corpus and optional x86 cases report explicit skips when their inputs or opt-in flag are unavailable. For dependencies and differential validation, see [validation](docs/VALIDATION.md). Do not interpret a skipped reference test as verified equivalence.

To prepare an isolated worktree:

```sh
python3 scripts/workstream.py start core
# Other fronts: missions, ai-runtime, economy, combat, graphics, audio, macos, maintenance
python3 scripts/workstream.py fronts   # ownership table
```

To build the playable app from a committed revision, run `./compilar-jogável` as described in [macOS playable](docs/MACOS_PLAYABLE.md); its UI remains PT-BR. The older research preview is documented in [the preview manual](docs/MACOS_PREVIEW.md). The Rust engine is checked with `sh motor/validate.sh`.

## Evidence identity

Original `RISING.EXE` SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

Fixed addresses apply only to this executable. Originals are read from `../source/cd`, a compatibility link to `../local-data/originals/cd`. Original media are local and excluded from Git. The analysis-only normalized PE has a different hash; differential tests must use the original.

See [migration and historical records](docs/MIGRATION.md) for the exact pre-organization revision and recovery instructions. Original game materials retain their existing rights; this repository does not grant them a new license.
