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
