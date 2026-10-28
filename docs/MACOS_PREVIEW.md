# macOS research preview

Source: `apps/macos-preview/`. The app is a native Swift/AppKit/WebKit shell around an ARM64 Python research adapter. Its UI, labels, errors shown to players, mission text, and audio remain PT-BR. Documentation and maintenance instructions are English.

## Launch and rebuild

Open the existing local app with:

```sh
apps/macos-preview/abrir.command
```

The generated bundle is `apps/macos-preview/dist/RisingLands-Preview.app`. That path resolves into workspace local data. The separate top-level `Jogar.command` still launches the older Swift proof under `legacy-prototype/`.

To update from a fixed **committed** research revision:

```sh
apps/macos-preview/atualizar.command --commit HEAD
# Optional original-media override:
apps/macos-preview/atualizar.command --commit HEAD --cd /absolute/path/to/cd
```

The update fixes the commit, copies Git blobs, verifies/extracts assets, checks the snapshot/adapter, builds and signs the app locally, and runs a UI opening test. It requires Apple development tools, Git, the extracted original corpus, a local CPython 3.12 ARM64 runtime, and a graphical macOS session for UI checks. It does not download dependencies. The bundled app runs without the CD, system Python, network, Rosetta, or Unicorn. macOS 13/Apple Silicon is the declared build target; testing on other systems is not implied.

The app has a local ad hoc signature, without Developer ID notarization. Package verification uses `codesign --verify --deep --strict`. Do not present this local signature as a notarized distribution.

## Supported laboratory behavior

The lab starts paused. Select a unit, choose a destination, use `Continuar` or `Uma atualização`, and inspect position, requested/effective destination, state, and collision logs. Space toggles pause, `.` advances one update, and R resets. Drag/wheel/zoom buttons control the view. Speeds range from 0.25× to 8×. Its experimental 20 updates/second at 1× is not the complete original cadence.

The independent contour solver handles the supported synthetic wall-with-gap scenario; the local-detour-only option deliberately omits general search. Missing structure-grid/unblocking branches are explicit errors. The green dashed preview runs on a copied world with other units fixed; the blue line is actual movement. A preview may be partial and does not mutate live state.

Mission 1 is an inspection view of recovered terrain/positions. Economy exposes manual verified resource/capacity operations, not automatic recruitment/production. Targeting exposes selection, range, line, aiming, and order-on-copy queries without live damage. The game-style view uses illustrative sprites and local HUD composition. A reference screenshot guides presentation; it does not prove simulation rules or every sprite association.

## Snapshot isolation and evidence

`snapshot.json` pins a Git commit and records path, blob, size, and SHA-256. `research.json` pins independent completed economy/combat captures. Updates preserve those research captures until an explicit reviewed reconciliation. Captures, original research prose, manifests, and build logs retain their historical contents under ignored local-data directories; they are evidence, not maintained English manuals.

`scripts/conciliar_pesquisas.py` captures completed domain deliveries with two identical reads and successful source validation reports. It reads the canonical research source paths after this move. Reconciliation is a separate action from ordinary app updates and requires reviewing completed contracts and adapter support. Do not treat source-file presence as feature integration.

The original preview baseline used core commit `5dab3d82a96d7ddb1b7646301a402732983159e8`, 932 files, economy capture `05219260afe6afb13b03c2f7d1013e3b7e5c6223c8dd12c75d8e9856c28d1fa6`, and combat capture `edaa9592d7a3ba66d824a0d968f9dccd84b666285da944a5111d3c147757a38b`. Its historical validation included 23 adapter tests and 18 UI checks; the new organization check record reports what was actually rerun after the move.

## Independent checks

From `apps/macos-preview/`:

```sh
dependencies/python/bin/python3 -B scripts/testar.py
codesign --verify --deep --strict dist/RisingLands-Preview.app
```

`build/logs/tests.json` records actual suites/skips; other logs record build, opening, package, architecture, and signature checks. Source changes do not update the existing bundle until a rebuild. The preview is outside the research ownership slices; the playable consumer in [the playable manual](MACOS_PLAYABLE.md) is the milestone-triggered integration path.
