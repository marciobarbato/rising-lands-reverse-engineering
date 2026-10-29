# macOS accepted-state consumption contract v1

Contract identifier: `rising-lands/macos-state-consumer/1`.
Implementation: [macos_state_consumer.py](src/macos_state_consumer.py).
This is an app-owned inspection boundary, not a new engine/wire format or a
runtime/Graphics contract. M3 is not accepted by this delivery.

## Inputs and inspection

`load_accepted_m1(source_root)` reads the existing acceptance record and its
exact SHA-256-pinned `captura-carga-missao-original-v2.json`. It checks acceptance,
capture identity, original executable identity, capture schema, successful real
MissionLoad return, block metadata and extent. It calls the unchanged
`mapa_memoria_m1.carregar_blocos` decoder for zlib, sizes and per-block hashes.
No ETA parsing, generated fixtures, reconstructed-state defaults, startup,
Unicorn, CD reads or engine execution is involved. The captured bytes are the
original reference which the accepted Python composition reproduced; this
consumer does not independently re-execute that composition.

The pinned capture SHA-256 is
`eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc`.
The intact executable SHA-256 is
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Original entry: MissionLoad `0x46c2cf`; return: `0x42d22d`, AL=1.
The accepted domain is only MONDE01, new campaign, original-v2 scenario,
881 blocks / 2,659,375 bytes. Other capture versions require explicit review
and a new consumer contract; v1 never silently selects the latest evidence.

`MacOSAcceptedImage.blocks` is a tuple of immutable blocks, each containing its
original name, 32-bit virtual base, exact bytes and SHA-256. Blocks are ordered
by numeric base then name. Overlap/overflow is rejected. This ordering is for
inspection only; it does not reorder provider calls, allocations or bindings.
`identity` is `(contract, source_sha256)`, not a semantic frame hash. Source
identity includes provenance and ordered effects; per-block hashes describe
memory identity. No pointer is rebased or replaced by a unit/list index.

`read(address, size)` reads within one captured block and rejects gaps and
cross-block reads. It interprets no game layout. `inspect()` returns metadata
and hashes without duplicating raw game bytes in a JSON response.

Developer command from the independent clone:

```sh
python3 -B apps/macos-preview/src/macos_state_consumer.py
python3 -B -m unittest discover -s apps/macos-preview/testes -p test_macos_state_consumer.py -v
```

For an archived app source tree, `source_root` (or CLI `--source-root`) may
select the root explicitly. Without that argument, a source checkout uses its
repository root; a deployed module uses only the relative archive declared by
`snapshot.json` beside it. Absolute paths, parent traversal and symlinks escaping
the payload are rejected. A deployed module without a declaration fails with a
clear English error instead of guessing a repository from ancestor directories.
Legacy archives without accepted M1 evidence likewise fail rather than falling
back to an external checkout. The existing playable packager archives the full
committed source tree and declares `snapshot: source`. The native shell is not switched to
this inspection module and its synthetic UI schema is unchanged. Both playable and legacy builders mirror the consumer module using the same
source-copy helper. The playable verifier imports the bundled consumer and loads
its declared M1 archive using the isolated bundled interpreter. A later shell
integration must select inspection mode explicitly. Historical preview archives without accepted M1
artifacts fail validation rather than falling back to synthetic state.

## State transitions and ownership

`MacOSStateConsumer` is called serially by one owner. `current` starts as None.
`load_m1` fully validates a candidate before publishing it. Failure leaves the
previous image untouched. Repeated successful loading of the same identity
preserves the current image object. `reset` releases it; the next load creates
a distinct object with the same captured identity and bytes. There are no
callbacks, external effects, advancing clock or mutable engine aliases.

`apply_frame(frame)` is a reserved local call site. It always raises
`RuntimeContractPending` before reading the payload or changing state, even
when no M1 is loaded. There is intentionally no fabricated payload schema,
frame counter, delta application, partial retry, provider binding or input
protocol. These semantics are tested. It does not mean an M2 transport exists.

The immutable inspection copy must never replace a live provider's bytearray,
canonical grid list or cached scalar. Future live integration must honor the
in-place binding/identity semantics documented by Missions' MapaMemoriaM1.

## Handoff requests to runtime and Graphics

Runtime must publish a validated consumer API specifying scenario identity,
initial state (M2 uses display initialization, unlike this M1 original-v2
capture), frame/phase boundaries, completeness or delta base identity,
sequence/replay/reset behavior, error/partial-effect policy and buffer lifetime.
Acceptance of M2.1/M2.2 alone does not define those delivery semantics.

Graphics must publish the app-facing frame composition API over that state:
required bindings and viewport, mutations (including shared RNG/cache effects),
callback order, supported scene domain, missing-provider stops, palette/indexed
surface format and lifetime. No renderer is added here. No render pass is
assumed to be pure, and no unsupported facade is substituted.

Input dispatch and UI timing remain later owner-defined dependencies. Do not
feed accepted snapshots into the synthetic exercise, apply its 20 Hz policy to
MONDE01, or interpret this inspection module as a validated live frame bridge.
Formal milestone documents are unchanged.
