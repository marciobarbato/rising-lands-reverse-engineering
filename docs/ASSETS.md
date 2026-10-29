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
code branch. Every761 expected payload and the complete root manifest are
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
covers626 source files;143 selected game/campaign/shell resources are exported,
while483 installer/platform/program/debug files have explicit exclusion reasons.
Selection is broader than MONDE01; exact per-mission/event reachability is not
inferred from filenames.

The pack preserves12,268 frames from8 CMP banks as indexed and separate opacity
planes. Literal index0 can be opaque; anchors/clipping remain renderer inputs.
Seven palettes use the unchanged VGA6<<2,entry0-black reader. All551 original
complete-buffer audio hashes match, while only48,945,219 native-written bytes
are retained;334,880 inherited/unwritten fixture bytes are excluded from audio.
The one P/index221/variant0 PCM16 boundary keeps291,938 complete WAV bytes plus
one explicit tail byte, reproducing all291,939 native-written bytes without
padding or truncation.

Structured worlds are38 MONDE*.ETA plus5 NET maps; complete world bytes retain
inactive cells and unknown suffixes. There are33 reversible original text
files and96 preserved sources in98 parts. No payload exceeds32MiB. PIE/LZS
pixels, FNT glyphs, FLC/AVI frames and COL/MAP semantics remain explicit decoder
dependencies: their bytes are preserved, not claimed decoded. The data repo's
FORMAT, HANDOFF, manifest and validation report carry full details and sizes.
No new decoder, game behavior, rendering, input protocol or milestone is added.
