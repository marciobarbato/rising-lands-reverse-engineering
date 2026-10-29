# macOS accepted-state consumption contract v2

Identifier: `rising-lands/macos-state-consumer/2`. This is evidence inspection,
not live frame delivery, game simulation or milestone acceptance. Version 2
adds accepted M2.2 playback; the M1 loader remains available and explicitly
labels its different scenario.

## Immutable images and sources

`macos_state_consumer.load_accepted_m1(source_root=None)` loads the exact M1
original-v2 acceptance-pinned capture through Missions' unchanged decoder.
Its scenario is `MONDE01/original-v2/M1-accepted-inspection` (881 blocks,
2,659,375 bytes). No ETA or synthetic state substitutes for that reference.

`macos_m22_playback.MacOSM22Playback.open(source_root=None)` loads only the
accepted M2.2 display-v2 sequence. The acceptance record, compression manifest,
xz capture, display-scenario entry and MissionLoad capture are SHA-256 pinned
in `PINS`; the raw JSON hash is checked by the runtime reader too. All files
must exist and match. The initial state is reconstructed using the unchanged
`mapa_memoria_m1.expandir_captura` and `carregar_blocos`, then checked against
`state_s0.summary`. It never starts from M1 original-v2.

The capture identity is xz SHA-256
`4c8f5c14a9623131dd019eafcdc49ea63054ee358f9defde58c12cb949f59ff3`,
raw JSON SHA-256
`1ad031b96300e5c632fd5b6b7857ae30792f78e86531e4f17d1bf7124c6dd930`.
The accepted M2.2 record is pinned at
`cebbe9b33d7d15a83990d794d3f5143d54696b71faa328710b2cc2c3814bbf57`.
Both scenarios originate in intact executable SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

Default source resolution uses the source checkout root or the adjacent bundle
`snapshot.json` relative archive. Absolute archives, traversal and escaping
symlinks are rejected. A deployed consumer without a source declaration refuses
instead of guessing an external repository. Explicit roots remain supported.
The builders mirror Python/UI files using their shared helper; no other front's
implementation or evidence is rewritten.

## Playback API and verification

The constructor validates all 257 ordered phase summaries and all 11 complete
checkpoints before returning. It loads the existing CPU-only reader functions
from `comparar_quadros_ia.py` by path. Because that comparator's top-level imports
start simulation/emulation dependencies, only the unchanged pure AST definitions
(`carregar_captura`, `fases_referencia`, their decoding/summary/delta helpers and
error class) are compiled. No missing simulation provider is stubbed or replaced.
Navigation then uses the unchanged `delta_estado_missao.aplicar` and `resumo`.
Both readers' checks are exercised against real accepted evidence.

- `current`: frozen image, initially `state_s0`, phase index -1.
- `step_to_phase(index_or_name)`: zero-based index 0..256 or exact phase name;
  `state_s0` resets. The fixed order is load_tail, between_frames, frame1,
  between_frames2, frame2, through frame128. Missing/duplicate/reordered phases
  and missing/unexpected checkpoints fail at open.
- `step_to_frame(number_or_name)`: 0..128, `frameN` or decimal text; frame 0
  means the initial display-scenario MissionLoad state.
- `reset()`: restores initial bytes and identity. Repeating a selection preserves
  the current image object; revisiting/resetting produces equal captured state.
- `read(address, size)`: exact bytes inside one live captured block, rejecting
  gaps and cross-block reads. `inspect()` returns all block metadata, hashes,
  phase/scenario, verification status and observed words.
- `apply_frame(frame)`: always raises `RuntimeContractPending`; LIVE delivery
  remains reserved and is unrelated to playback navigation.

Every navigation computes and checks intermediate phase summaries and complete
checkpoint states before publishing the candidate. Exceptions retain the old
image/cursor. No callback is executed as part of playback. Blocks are immutable
bytes and ordered by numeric address then name; original names and pointer
values are preserved. This presentation order does not reorder engine effects.
Image identity includes contract, capture hash, phase name and state summary.

Observed words are read from captured memory: counter 0x508f7c (u32), view
origin 0x508720/22 (u16), RNG words 0x497164 and 0x498db4 (u32), permutation
cursor 0x4e1d18 (u32) and HUD flag 0x4e05a2 (u8). The renderer receives only
`read`/`ler_mundo` and u8/u16/u32 access, never a writable engine buffer.

## Graphics API and current dependency stop

`macos_graphics_inspection` consumes only `render_quadro.renderizar_quadro`,
with `VERSAO_RENDER_QUADRO == (1, 0)` checked both on import and returned images.
Any other version, including 1.1, is refused until an explicit tested update.
The worker has an isolated flat-module namespace so Graphics' `construcoes`
does not replace Economy's provider in the synthetic engine.

Output pixels/RGBA/PNG come exclusively from Graphics, and the UI displays them
with an image element. It preserves `parada` as an explicit partial-image state;
missing inputs are shown as stops without an invented image. No habitation
callback is fabricated; if reached, API 1.0 reports its named missing-provider
stop. Palette, supported domain and render semantics remain owned by Graphics.

**Current gap, confirmed by the coordinator:** surfaces are excluded from the
M2.2 state. Its `display_state` publishes offscreen addresses and hashes, not
pixels. API 1.0 requires a previous 800x600 indexed surface; none is supplied.
Every phase therefore reports `missing_previous_surface`, stage `consumer-input`,
`api_called: false`. These are input stops, not Graphics-returned named stops
and not successful renders. No alternate artifact or blank surface is used.
The per-phase report records 257 such stops and zero actual Graphics calls.

The render adapter has a pluggable `surface_source` call site, unset today.
Any supplied bytes must match the predecessor's accepted surface hash; the
consumer reads no external surface files. Graphics is preparing API 1.1 with
an original-first initial-surface artifact, a previous-rendered-output chaining
rule and original per-phase hash verification. That artifact and contract must
land before this stop can be closed. Partial images must remain labeled (for
example the tired-unit overlay below row 279 is outside the current domain).

## Native view and reproducible builds

`ui/playback.html` is a separate view in the existing AppKit/WKWebView shell,
reachable from the training view or launch argument `--inspection`. It exposes
phase/frame selection, reset, observed words, filtered block metadata and
bounded memory reads. A separate JSON-lines worker handles inspection only;
entering inspection pauses the synthetic exercise. Returning to training keeps
its existing controls available. This adds no game input protocol or clock.
The native build includes both exercise and inspection smoke checks.

The launcher takes `--inputs-root` (or `RISING_INPUTS_ROOT`), containing
`source/cd`. `RISING_PYTHON_RUNTIME` declares a relocatable CPython 3.12 ARM64
root. Default outputs are inside the clone at `.local/macos-playable`, with an
optional explicit `--data-root`. No Git-parent/shared-local-data inference is
used. Inputs are read-only; copied Graphics catalog assets are hash-checked and
bundled as ordinary files. Build/source/asset manifests retain provenance.

See [the playable manual](../../docs/MACOS_PLAYABLE.md) for the exact command,
[handoff](HANDOFF.md) for actual tests/build results and
[per-phase evidence report](validation/m3-m22-playback.json) for the verified
sequence and render stops. Live frame delivery, orders and broader Graphics
coverage remain external dependencies. No formal milestone status changes.
