# Audio handoff

Owner: the Audio front. Branch `feat/re-audio`, worktree `worktrees/re-audio`. Owned paths: `pesquisas-paralelas/audio/` and `docs/AUDIO.md`. The macOS chat executes this front while it waits for the M1 trigger, as approved by the human on 2026-10-28.

Status: the coordinator created this front. No research stage has started. The first stage is bank format and sample decoding, as described in [docs/AUDIO.md](../../docs/AUDIO.md).

Each completed stage records here:
- original addresses and hashes;
- API inputs with widths;
- the supported domain;
- mutation/callback order and failure behavior;
- fresh native counts with stops;
- local test counts with declared skips;
- implementation, feature and merge SHAs;
- remaining gaps.

Requested contracts from other owners are listed with the original call address and the consumed widths.
