# Repository organization and historical recovery

Organization date: 2026-10-28. Base: `1231ebff9463871b124d736c9e0333a6f8b5c87a` (`origin/main` after fetching). All previous economy, graphics, and core feature commits were already reachable from that base. No original-media contents or game/UI translations were changed.

## Changes

The outer workspace now separates originals, converted media, generated preview data, legacy proof code, archived releases, and worktrees. The canonical repository retains its name and established Python/API paths. Completed worktrees were moved with `git worktree move`, including the formerly nested graphics checkout, preserving their Git registration and local contents.

The untracked Mac viewer source was moved to `apps/macos-preview/` and added to version control. Generated payloads, runtime dependencies, pinned historical captures, builds, and distributions remain local and ignored. Its snapshot copier excludes app sources to prevent packaging the app recursively inside research snapshots. Its reconciliation reader now resolves domain source directories from the canonical repository.

Current documentation is consolidated in `docs/` in English. Module entry points link to the maintained manuals. The superseded scattered manuals and duplicate release copies were removed from the active documentation surface. This is an editorial consolidation, **not a line-for-line translation of every historical research log**. Detailed prior wording remains intact as primary research evidence, including Portuguese text and original symbols.

## Recovering the full prior documentation or release

All formerly tracked records remain available in Git, for example:

```sh
git show 1231ebff9463871b124d736c9e0333a6f8b5c87a:documentacao/PORTOES.md
git archive 1231ebff9463871b124d736c9e0333a6f8b5c87a pesquisas-paralelas/graficos-animacao/entregas > /tmp/rising-historical-graphics.tar
```

The local `../archive/documentation-before-organization.tar.gz` additionally preserves all 103 formerly tracked Markdown files plus the viewer manuals and outer prototype notes. `../archive/documentation-provenance.json` records every original Markdown hash, base revision, and archive hash. Seven complete immutable graphics releases remain in `../archive/graphics-releases/`; their original manifests include copied input media, private snapshots, and dependency records that Git intentionally excludes.

No historical manifest was rewritten to point at new paths or to make translated text match an old hash. The ignored compatibility link `pesquisas-paralelas/graficos-animacao/entregas` reaches the complete local archive. The release files can be reconstructed from Git history plus the separately preserved local inputs on another machine.

## Language and maintenance

Write all new maintained prose, contracts, handoffs, commit messages, and repository instructions in English. Keep the game in PT-BR, including player-visible labels, errors, mission stories/objectives, unit/resource names, and audio. Preserve original French SBL/INI evidence and established identifiers; changing these is an API or evidence migration, not a translation task.

Do not reintroduce copied complete repositories, build products, vendor packages, or frozen-release duplicates into active source directories. Append research evidence and update the owning domain's English handoff. Update shared status/index pages during serialized integration or a dedicated documentation pass so the research fronts do not compete for the same file.
