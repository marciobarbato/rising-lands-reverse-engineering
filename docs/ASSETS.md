# Asset extraction tooling and pinned external data

Code and asset payloads live in separate repositories. This code branch contains
only the extractor, tests, this document and assets/ORIGIN.json. No payload,
source inventory, FORMAT/HANDOFF or generated validation report is imported
into code history. The historical feat/codex-assets branch must not be merged
into code main; its payload is preserved separately until the coordinator
verifies the data release and explicitly deletes that old branch.

Data repository: [rising-lands-assets](https://github.com/marciobarbato/rising-lands-assets).
The release's root contains data/, manifest.json, source-inventory.json,
FORMAT.md, HANDOFF.md and validation.json. It descends from the repository's
existing README history. The code repository's main is never pushed by this
front; the data repository's main publication is separately authorized.

## Verify the immutable release

Read assets/ORIGIN.json for the exact HTTPS repository, annotated release tag,
tag-object identity, commit, manifest SHA-256 and source-inventory SHA-256.
Clone/check out that exact release in a separate directory, then run:

```sh
python3 -B assets/extract_assets.py \
  --cd-root '/Users/marcio/git/Rising Lands/source/cd' \
  --data-root /absolute/path/to/rising-lands-assets --check
python3 -B -m unittest discover -s assets/testes -v
```

Python3.9+ standard-library modules suffice. Verification is read-only: it does
not fetch, switch branches, generate missing files or replace a pin. Missing or
malformed ORIGIN, wrong repository/checkout/annotated tag, a moved tag, changed
manifest/inventory and a dirty data checkout all fail explicitly before full
regeneration. Both commit and tag-object identities are checked. The same gates
are checked again after regeneration, so the checkout cannot silently change
during a successful check. Pointer paths are not guessed from another checkout.

The source inventory is resolved only from the data repository root. Its
release pin and audited SHA must match before inputs are accepted. All626 CD
file identities are verified, including explicitly excluded installer files;
missing/extra/modified inputs fail. No source inventory is copied into this
code branch. Every 761 expected payload and the complete root manifest are
freshly regenerated through the unchanged readers and compared byte-for-byte
with the published data. A second physical pack is not written in check mode.
Extra/missing payloads also fail. Inputs and published files remain untouched;
logs belong outside the pinned data checkout.

## Publishing a new data release

Extraction without --check is a maintainer operation for a fresh destination
in the separate data repository. It requires that repository's HTTPS origin
and the audited source-inventory.json at its root, then refuses an existing
data/ directory or manifest. It runs the same native readers and original-audio
capture checks while creating the pack. This mode creates a new release; it
cannot verify or silently repair an existing published checkout.

Commit the tooling implementation before extraction. Publish the data commit
and a new immutable annotated tag, then add/update ORIGIN in a separate code
commit. This avoids a circular commit reference: the manifest records the
extractor-file commit, while ORIGIN later pins the resulting data commit/tag.
Never force-push or move an existing release tag. A new explicit release and
code pin are required for changed data/readers; there is no latest-main fallback.
The coordinator owns subsequent Rust/macOS asset consumption and app bundling.

## Provenance and byte proof

The user supplied the original download URL:
[Internet Archive BIN](https://archive.org/download/risinglandsbr/RISING_LANDS_BR_.BIN).
No download is performed by the tooling. The data README records the existing
BIN hash separately from the CD-tree inventory hashes. The complete inventory
covers 626 source files; 143 selected game/campaign/shell resources are exported,
while 483 installer/platform/program/debug files have explicit exclusion reasons.
Selection is broader than MONDE01; exact per-mission/event reachability is not
inferred from filenames.

The pack preserves 12,268 frames from 8 CMP banks as indexed and separate opacity
planes. Literal index 0 can be opaque; anchors/clipping remain renderer inputs.
Seven palettes use the unchanged VGA6<<2,entry0-black reader. All 551 original
complete-buffer audio hashes match, while only 48,945,219 native-written bytes
are retained; 334,880 inherited/unwritten fixture bytes are excluded from audio.
The one P/index221/variant0 PCM16 boundary keeps 291,938 complete WAV bytes plus
one explicit tail byte, reproducing all 291,939 native-written bytes without
padding or truncation.

Structured worlds are 38 MONDE*.ETA plus 5 NET maps; complete world bytes retain
inactive cells and unknown suffixes. There are 33 reversible original text
files and 96 preserved sources in 98 parts. No payload exceeds 32MiB. PIE/LZS
pixels, FNT glyphs, FLC/AVI frames and COL/MAP semantics remain explicit decoder
dependencies: their bytes are preserved, not claimed decoded. The data repo's
FORMAT, HANDOFF, manifest and validation report carry full details and sizes.
No new decoder, game behavior, rendering, input protocol or milestone is added.

## Published release and validation

The data release is [v1-4eb88f2](https://github.com/marciobarbato/rising-lands-assets/tree/v1-4eb88f2):
commit `c21ae6579cd0e229f718e866adc14bad25799cf9`, annotated tag object
`9846e53d7a9cc9af709c3fc90c6aac7f02fb295c`. The root manifest SHA-256 is
`2a25904128ece9c0cc8113c3820bef6b65ee7ab9f97cc215030187afa44de63e`;
source-inventory SHA-256 is
`d5057f3fae7f24d87e423856040962fdd09fbe4e80b9a0905726e9bbc7340211`.
The manifest adapter provenance points to the reachable new extractor commit
`4eb88f23b7b6c03bf1fcfcfee85ee5d53a5f548e`. Historical extractor 1288976 is
not required for reproduction. Publication extended data main 7256128 normally;
its immutable tag and the code pin were created in that order.

Actual post-publication verification ran at code commit
`7e698b3b10f98ae98f3456c4f57610925bba9b0f`, containing latest fetched code main
`5fbef8252f5f63afcdbdaba56425da479073cec8`. It verified remote refs, then
regenerated every 761 payload and manifest byte against the clean published
checkout, matching all 551 original complete-audio-buffer hashes. Sixteen tests
passed with zero failures/skips, including wrong/missing pins, a changed
checkout commit, missing/moved tag, modified manifest/inventory, wrong repository
and dirty checkout. No original emulation or native-device playback occurred.
The final documentation-only commit changes no extractor or data bytes.

Data payloads total 629,204,621 bytes; manifest 1,350,352 bytes; complete tracked
data repository content 630,776,338 bytes across 768 files. Every file is at most
33,554,432 bytes. Git reported 252.86MiB for the data publication transfer. Its
README records the user-supplied IA URL and the distinct existing BIN hash:
`c2c09e87927cf5ebbe5d17ea17bffb53c82c2e68385e9259ad0453cc15ea616f`.

The tooling was cloned with --single-branch main and never merged/cherry-picked
the historical assets branch. Full-history checks find no assets/data path and
no old e37806d/60fdbfd/3702bee/1288976 commit objects. There are no Git alternates;
only main was fetched. The feature diff has exactly four UTF8 text paths:
extractor, tests, this document and ORIGIN. Its largest new blob is 26,185 bytes;
the code Git packs are 54,688,488 bytes, consisting of main research history and
small tooling objects, rather than the 630MB data pack.

The historical feat/codex-assets remote branch and old clone remain unchanged.
Once the coordinator fetches and independently verifies the published release
through the new pinned tooling, while retaining the new tooling implementation
reachable (normally by integrating this feature), that old remote branch is
safe for the coordinator to delete. No data or implementation depends on it.
This front does not delete it or rewrite/force-push either repository's history.
