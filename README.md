# Rising Lands reverse engineering — Brazilian edition

Evidence-based reconstruction of the Brazilian PC release of Rising Lands. The project includes file readers, Python reconstructions, bounded comparisons against original x86 instructions, and a native macOS research preview. The complete game and campaign are still under reconstruction.

**Documentation is English. All player-facing text, mission stories, objectives, unit names, and audio stay Brazilian Portuguese (PT-BR).** Original French SBL symbols and established Python identifiers remain unchanged so evidence and APIs stay traceable.

Start with [the documentation index](docs/README.md), [current research status](docs/STATUS.md), [the roadmap to a running original mission](docs/ROADMAP_MONDE01.md), and [the seven-front workflow](docs/PARALLEL_WORK.md). The [restart prompt](docs/RESTART_PROMPT.md) defines the seven fronts and their merge procedure.

## Repository map

| Path | Purpose |
|---|---|
| `docs/` | Current English manuals, contracts, ownership, and restart instructions |
| `ferramentas/` | Shared readers, simulation primitives, and x86 harnesses; stable API paths |
| `testes/` | Core unit, corpus, and differential tests |
| `evidencias/` | Original-byte assembly, decompiler exports, and provenance manifests |
| `relatorios/` | Versioned extracted data and validation results |
| `pesquisas-paralelas/combate/` | Combat research and its own tests/evidence |
| `pesquisas-paralelas/economia/` | Economy research and its own tests/evidence |
| `pesquisas-paralelas/graficos-animacao/` | Graphics research, artifacts, and its own tests/evidence |
| `pesquisas-paralelas/missoes/` | Mission loading/orchestration research and its own tests/evidence |
| `pesquisas-paralelas/ia-runtime/` | AI kernels, dispatchers and VM operations research and its own tests/evidence |
| `integracao/` | Coordinator-owned provider loaders for same-process consumers |
| `apps/macos-preview/` | Versioned macOS preview source; generated payloads stay local |
| `scripts/` | Worktree preparation, checks, and serialized integration |
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
# Other fronts: missions, ai-runtime, economy, combat, graphics, macos, maintenance
```

To open the existing local preview, run `apps/macos-preview/abrir.command`. To rebuild it from committed research, follow [the preview manual](docs/MACOS_PREVIEW.md). Its UI remains PT-BR.

## Evidence identity

Original `RISING.EXE` SHA-256:
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

Fixed addresses apply only to this executable. Originals are read from `../source/cd`, a compatibility link to `../local-data/originals/cd`. Original media are local and excluded from Git. The analysis-only normalized PE has a different hash; differential tests must use the original.

See [migration and historical records](docs/MIGRATION.md) for the exact pre-organization revision and recovery instructions. Original game materials retain their existing rights; this repository does not grant them a new license.
