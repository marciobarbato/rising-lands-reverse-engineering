# Player-action map handoff — independent workstream C

Branch: `feat/codex-m3-player-actions`.
Clone: `/Users/marcio/git/Rising-Lands-Codex-Player-Actions`.
Fetched base: `daa6ed2da79827b2472929f7e5c82aad1d631782`.
Only `pesquisas-paralelas/mapa-acoes-jogador/**` is owned/changed. No main merge,
main push, force push, other-front edit or Claude worktree access is performed.

## Delivered scope

[Report](M3_PLAYER_ACTIONS.md), [JSON call graph](callgraph.json),
[byte evidence](evidencias/original-player-action-bytes.json) and
[MONDE01 context](evidencias/monde01-action-context.json) map Windows input,
local/remote human branches, command production/consumption, selection, movement,
construction, work/transport, recruitment, attack and the end-condition/menu
transition boundary. Original data and pointers are retained. The graph has
94 nodes, 235 selected call edges, all 40 command dispatch cases and typed
memory contracts. It supplies a next-capture checklist for the Claude owners.

Original-only research commits precede this synthesis:
- `6bfa18d8cc8bfdbff90c2e8e85ae72996f642a55`: intact input/order/function byte evidence.
- `ab05ca66d5467b81ab14b9b9c57d978a3e528ca5`: original type names and accepted-M1 condition/roster provenance.

Inputs: intact Brazilian RISING.EXE SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`,
committed imported symbols, domain contracts and immutable accepted M1 original-v2
capture SHA-256 `eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc`.
Original CD access was read-only. The normalized PE is not used. A temporary
ELF contains the exact original BEGTEXT bytes solely for LLVM disassembly.

This is static evidence and planning, **not an implemented engine API or new
input protocol**. There are no game mutations, callbacks or simulated effects.
The only code added extracts, synthesizes and validates research artifacts.

## Important findings and limits

SetPlayerOrdre writes five u16 words through `0x4e2458+4*player`. ProcessInputGame
checks tag <=39 and jumps through the exact table at `0x45ed20`; after dispatch
it clears all five words. Selection and single-unit order routines preserve their
original references and gates. Construction tag 4 uses a selected type-7 unit;
original type records prove BATISSEUR=7 and CAVE=3. Accepted M1 unit 12 is the
player-0 type-7 constructor. The loaded sanctuary's type 2 is not a cave.

The objective records contain a type-3 structure requirement and food/stone
thresholds of 50. These numbers are **condition thresholds, not initial balances**.
Initial player resources were not extracted here; no synthetic preview balance
was used. Raw zone words and the evaluator's 0x00ff wildcard remain explicit.
No additional per-cave storage rule is inferred from the briefing.

Every edge is labeled as an encoding/static claim; no node/action is marked
runtime accepted. Symbol-to-next-symbol intervals are not proven function
boundaries, linear decoding may include unreachable bytes, shared tails can
leave an interval and computed branches are incomplete except the reviewed
command table. Selection/UI context and command producers remain partly open,
notably the CAVE-button -> tag4/type3 link, transport tag8 and recruitment tag17.
No successful construction, resource delivery, combat, death or end transition
was executed. This work establishes no milestone and touches no formal status.

TestFinDeMission's AL copy, result latch, counter-100 menu request and MissionNext
calls/stores are recorded as local byte/static facts. Victory/defeat names and
complete confirmation/load behavior need native traces. The map stops before
any next mission execution. M2.3 work is not duplicated.

## Actual validation

- [Owned validator](validar_mapa_acoes_jogador.py): **passed** against the intact
  EXE. Checks 67 original byte intervals, 21,496 decoded instruction encodings,
  1,282 candidate call encodings, 235 curated graph edges, 40 table entries,
  five original type records and accepted-M1 context. These are static checks,
  not native execution totals. [Saved result](validation.json).
- [Owned tests](test_mapa_acoes_jogador.py): **6/6 passed, zero skips**. They cover
  wrong executable identity, altered/dangling edges, wrong table order/targets,
  overclaimed success/reachability and incorrect producer/transition references.
- Repository workflow tests: **8/8 passed, zero skips**.
  [Owned test log](test-results.log), [workflow log](workflow-results.log) and
  [check summary](checks.json) preserve the actual results.
- Original byte evidence and accepted-M1 context both regenerated **byte-identically**
  into separate ignored review outputs. Owned Python module basenames are unique.
- Documentation-link check and `git diff --check`: passed.
- Native emulation/native differentials: **not run; not required for static-only
  evidence**. No lease was acquired and no Mac mini job was started.
- `scripts/check.py --domain`: this new research path has no registered domain;
  no shared helper or another owner's suite/report was modified to add one.

Reproduction commands are in the report. Tests accept `RISING_ACTIONS_EXE` to
select another read-only copy of the exact intact EXE; its identity stays strict.
Original evidence regeneration should use separate review outputs, preserving
committed delivery artifacts. LLVM/Apple command-line tools are needed for
extraction; the validator and tests use the Python standard library.

## Remaining requests routed through Claude

AI/runtime and the harness owner must define/record the original scripted-input
binding before a concrete native capture command can be specified. The report's
checklist requests selection, movement, CAVE UI/type/order/placement, natural
food/stone delivery, attack and end-condition/confirmation traces, each with its
existing Core/Economy/Combat/Missions owner. No substitute protocol is proposed.

Use an existing suitable owner checkpoint for combat rather than repeating the
critical first-raid long run. A future capture with unknown or >20-minute runtime
must be submitted to Claude/Mac mini with a committed harness, exact command,
outputs and bounded estimate. No such job is requested by this static delivery.

The user communicates this pushed feature to the Claude coordinator for review
and integration. This workstream never invokes the helper that integrates main.
