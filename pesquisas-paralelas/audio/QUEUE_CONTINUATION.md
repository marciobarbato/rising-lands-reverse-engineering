# Audio queue continuation — original-first contract

Base main is `8e90beb412a63d5f00965c381d21bc9a800257bc`; prior Audio `73196fc`
is integrated. Owned paths and the independent clone are unchanged. All native
runs use the unchanged shared heavy lease, a 600-second alarm and a 50,000
instruction per-call limit. Synthetic inherited memory remains explicit; this
is not a mission capture or device initialization.

## Reuse, promotion and duplicate leaves

Original-only capture `captura-continuacao-audio-original-v1.json` has 118
intact-original calls, all returned, 0.557 seconds. No translation is imported.
Input/output images cover the same globals, aliasing BSS and external reference
regions as the prior queue contract. All original bytes and symbols belong to
intact executable SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.

- PSB/LSB replacement at `0x48abdc` / `0x48ad3c`: signed last index -1,0,1,9;
  exact last/nonlast effects, moved back-pointer, and stale last-slot behavior.
- PSB/LSB identity lookup at `0x48acd3` / `0x48aeb3`: ID plus bank identity,
  counts -1,0,1,9, first/later/absent ID and wrong-bank inputs. The physical
  query returns a slot; the logical query returns a record.
- PSB destruction at `0x48ac53`: explicit GetStatus/Stop/Release sequence,
  statuses 0/1/5 and success/error HRESULT, with earlier effects preserved.
- DestroyOnlySound at `0x489e35`: physical release then logical promotion when
  the exact ID/bank is present, otherwise physical swap-with-last. Captures
  include physical last index 0/1 and logical presence/absence.
- Physical playing→waiting transfers retain copied records/reference changes
  before destroying the physical slot; they do not invent promotion.
- ClearListe at `0x489f96` exercises one active logical/physical record for
  statuses 0/1/5 with error HRESULT and explicitly written status. `0x48beb9`
  remains **DSB_IsStopped**, not the incorrect legacy IsThisSoundPlaying name.

DuplicateSoundBuffer is the only new external binding: vtable slot `+0x14`,
stdcall `(device_u32, source_buffer_u32, output_pointer_u32)`, 12-byte cleanup.
Each fixture explicitly writes a u32 output and returns an independent u32
HRESULT. There is no default output or callback. Null device/source guards
make no call. On nonzero HRESULT the original returns NULL despite any output.
On success with nonnull output it calls SetCurrentPosition(output,0); its
HRESULT does not replace the returned duplicate pointer. LSB creation reserves
its slot first, writes the result and keeps reservation on failure. Full LSB
capacity makes no duplicate call. Raw ABI arguments/output writes are retained.
These declarations prove caller behavior for those exact platform answers,
not real sharing, device allocation or asynchronous buffer lifetime.

Further request/concurrency and resident/compressed captures must precede their
translation. The earlier v1–v9 queue captures and validation reports remain
unchanged. No main push, acceptance record or milestone change occurs here.

## Concurrent requests and resident/compressed bridge (original v2)

The second original-only capture includes all 118 leaves plus 13 request cases:
131 calls, all returned, 0.646 seconds. No provider translation is imported.
New cases cover file/resident PCM and mono IMA ADPCM, two/three waiting requests
with distinct banks or shared ID/bank reuse, duplicate success/null/error,
and explicit full-LSB/physical-capacity guard images. The capacity fixture is
an explicitly aliased synthetic input whose ownership cleanup is not reached;
it does not prove a naturally initialized 20-device-buffer configuration.

Resident bytes live in caller memory at 0x7008000; file/compressed bytes are
fully declared _hread answers. The compressed scratch pointer 0x52222c is
explicitly inherited as 0x7006000. The 64-byte ADPCM input starts with predictor
1000, index0 and 60 bytes0x11, with block alignment64. The original creates256
bytes but Locks64 and decodes beyond that reported region into the created
buffer: this Stage-1 quirk must remain visible. Declared inherited output
memory includes that entire region; no pixels, audio samples from a game
capture, asynchronous device state or compressed scratch allocation are invented.

Each request is visited in descending original waiting-index order. Shared
bank/ID requests duplicate an existing physical buffer; distinct banks create
separate objects, even when IDs match. The explicit third object address is
0x7101300. Every Create/Duplicate output and Lock pointer/size, HRESULT, status,
file byte sequence and start answer is independently declared, with raw ABI
logs retained. Native success here means only that exact original branch
returned under those declared inputs; it is not hardware playback acceptance.

Original v3 adds one persistent eight-call sequence to v2: three PostSound
requests, Manage, physical-owner StopHandle (promoting a logical duplicate),
a different-bank repost, another Manage, and logical volume-zero cancellation.
Every intermediate image and EAX is frozen. All 139 calls / 132 scenarios
returned in 0.685 seconds. A fourth object is explicitly supplied at 0x7101400;
no creation or lifetime response is implicit. The initial state and platform
answers precede the whole sequence; later state is produced by original calls,
not rewritten between requests. This connects admission, simultaneous reuse,
promotion, slot compaction and cancellation across actual caller boundaries.
