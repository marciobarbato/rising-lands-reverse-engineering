# Independent macOS integration audit

Baseline fetched 2026-10-29: `99c0e4ec97c97700cf9081becff14dbb72a64497`.
The independent clone was created at `/Users/marcio/git/Rising-Lands-Codex`;
it had no pending files and only its own checkout. Remote macOS branch
`origin/feat/macos-playable` was `665149f77bbcfed727778969731c0840e26a9c9b`,
with no commits outside main. No Claude checkout, worktree, lease or local
coordination file was inspected. The user's isolation and feature-only push
instructions supersede the shared workstream helper and automatic integration.

Reviewed AGENTS, STATUS, PROGRESS, ROADMAP_MONDE01, PARALLEL_WORK,
MACOS_PREVIEW, MACOS_PLAYABLE and the app handoff. PROGRESS and acceptance
records supersede older milestone statements in STATUS. No milestone changes.

The native shell runs engine.py through JSON lines. Preview.state and
PlayableSession describe synthetic exercises, while the existing Mission 1
view reads ETA positions. None is a whole accepted M1 consumer. Replacing
those fields with guessed offsets would conflate two different state models.

The accepted M1 record pins the original-v2 capture SHA-256 and entry artifact.
Missions' mapa_memoria_m1.carregar_blocos already validates decoded block
sizes/hashes; expandir_captura already resolves display-scenario deltas. Reuse
that decoder without importing or executing a game engine. Original virtual
addresses and names identify blocks; presentation order should be numeric
address then name, not JSON member order.

Smallest useful implementation: a versioned, immutable read-only M1 image,
an inspector command, and a consumer slot that loads/resets atomically and
explicitly rejects future frame updates until runtime publishes their validated
contract. No synthetic-to-M1 simulation bridge, render mapping, input protocol,
new recovered behavior or new original-x86 research is needed.

Dependencies: runtime must define full/delta frame delivery, phase boundaries,
sequence/reset and live-buffer ownership; Graphics must define live-state frame
composition, mutating RNG/cache effects and output/palette lifetime. The M1
original-v2 scenario is not the M2 display scenario. Do not cross that boundary
by silently swapping snapshots. M2.1/M2.2 acceptance does not define a consumer
transport or establish M3 acceptance.
