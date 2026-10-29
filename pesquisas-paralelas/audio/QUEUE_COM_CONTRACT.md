# Audio queue declared-platform contract

Current original-only evidence is
[evidencias/captura-fila-audio-original-v9.json](evidencias/captura-fila-audio-original-v9.json):
**244 original calls, 238 scenarios, 3 intentional dependency stops**. The
[provider differential](validacao/fila-audio-three-way-v2.json) compares fresh
intact execution, that frozen evidence and `fila_audio.AudioQueue`. This is a
declared platform fixture, not DirectSound initialization, hardware timing,
mission state or audible playback. Original executable SHA-256 is
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The original bytes/hashes are preserved in the existing sound inventories.

## Inherited memory and protected domain

The caller supplies the complete memory image and every ordered external
answer. `AudioQueue(memory, external)` retains those objects by identity and
never initializes a sound subsystem, bank, record or device. Memory methods are
`read(address,size)`, `write(address,bytes)`, writable contiguous `view`,
`u8/u16/u32` and `w8/w32`, using little endian widths. Addresses, IDs, flags,
volumes, counters and external result words are u32; state fields are u8,
bank-entry word+4 is u16, and logical/physical last-slot counters are signed
interpretations of u32. Scalars must be supplied in these original widths.

The fixture preserves initialized globals at 0x498f14 (88 bytes), one aliasing
BSS image at 0x521358 (3804 bytes), and caller/reference/bank/PCM memory at
0x7000000 (65536 patterned inherited bytes). Native COM object/vtable inputs
are separately mapped at 0x7100000. These synthetic fixtures are not MONDE01
snapshots. Records are 44 bytes at 0x52137c; indices 0..70, waiting maximum 19..70,
playing slots 0..19, logical slots 0..9. Waiting index 70 aliases 0x521f84: the
request-ID/dirty-flag collision is preserved, not capacity-clamped. Compaction
and permutation take aligned record addresses in that protected region; the
capture includes equal-slot and 69/70 cases. Memory outside the caller's view
is an explicit input error, not a fabricated zero page.

Captured query, admission, cancellation/replacement, compaction, logical
cleanup and bidirectional transfers use the exact input images in v9.
`sort()` implements HandlSnd_TriWaitingHandle 0x48a664: when dirty==1 it calls
the literal-RET WaitSnd_Trier 0x48b38f and clears the flag. The leaf itself does
no sorting and owns no dirty-flag store; no sorting policy is invented.

Manage supports empty state, the captured one-active-logical-slot cleanup or
volume paths, and one new file-backed PCM request with no loaded physical
slots (counter=-1). Multiple pending requests stop explicitly at 0x48a80c;
loaded physical lookup/lifecycle at 0x48acd3, dictator lifecycle at 0x48a0a1,
dictator request creation at 0x48a702, physical transfer at 0x48ac53 and
physical/logical promotion at 0x489e6d remain outside. Unsupported queue
resident/compressed data stops at 0x48aad4; Stage-1 decoding exists separately.
All earlier validated stores/calls remain visible after a stop.

## Exact declared external answers

The bench uses Core's committed declared binding facility at external backend
addresses and verified Windows IATs, with the intact original instructions.
`external.answer(method, object_u32, scalar_arguments)` must supply the next
exact answer; absent/mismatched answers stop, never default to success.
Every answer has explicit u32 `hresult`; status/output words are explicit u32.
Pointer outputs and HRESULT are independent observations. Raw native stack
pointers, argument order and output writes remain in `raw_com`. Comparison
normalizes the address of a pointed descriptor, while retaining all its bytes.

| Method | Slot | Exact declared arguments/outputs |
|---|---:|---|
| GetStatus | +0x24 | this,out_u32; explicit written u32 status even for error HRESULT |
| Stop | +0x48 | this; explicit HRESULT |
| Release | +0x08 | this; explicit returned count/result word, no inferred hardware refcount |
| SetCurrentPosition (fixture name SetPosition) | +0x34 | this,position; explicit HRESULT |
| SetVolume | +0x3c | this,raw volume word; explicit HRESULT, no guessed gain |
| Play | +0x30 | this,reserved1,reserved2,flags; explicit HRESULT |
| CreateSoundBuffer | +0x0c | this,descriptor20,output_u32,outer0; explicit output pointer and HRESULT |
| Lock | +0x2c | this,offset,size,pointer1-out,bytes1-out,pointer2-out,bytes2-out,flags; explicit first pointer/size writes; no wrapped region |
| Unlock | +0x4c | this,pointer1,bytes1,pointer2,bytes2; explicit HRESULT |
| _llseek | IAT 0x5231f8 | handle,offset,origin; explicit result |
| _hread | IAT 0x5231e8 | handle,destination,size; exact declared returned bytes and byte-count result |

The PCM creation descriptor is size 20, flags 0xe0, bytes 64, reserved 0 and a
pointer to WAVEFORMAT bytes `010001002256000044ac000002001000` (PCM, mono,
22050 Hz, 16 bit, alignment 2). Outer is 0. Null output returns Manage EAX 0 for
HRESULT 0 and 0x80004005; nonnull output proceeds for either HRESULT. Original
DSB_CreateEmptySoundBuffer ignores HRESULT and uses the output word. A device
that leaves that word unwritten is outside the declared fixture, not NULL.
The queue bridge reuses Stage-1 `criar_superficie_som`, not a second decoder.

Lock outputs are explicitly pointer 0x7004000, size 64, no wrapped region,
offset 0, flags 0. _hread writes 64, 32 or 0 explicitly declared synthetic bytes;
the remaining caller-owned bytes stay intact. Lock/Unlock error HRESULTs do
not suppress original effects. The bridge currently requires full contiguous
Lock output count==request count. Unwritten outputs, wrapped/short Lock regions,
real device allocation and asynchronous ownership are unsupported boundaries.

DSB_IsPlaying 0x48be90 tests mask 0x1; DSB_IsStopped 0x48beb9 tests `(status&5)==0`;
DSD_IsLooped 0x48bedb tests mask 0x4. Null guards are 0/1/0 respectively. The old
maintained name IsThisSoundPlaying for 0x48beb9 was wrong; original SBL and
intact instructions prove IsStopped. HRESULT does not replace the explicit
status. If a failed real GetStatus leaves stack bytes untouched, that is a
different input. DSB_Stop queries stopped status first and returns whether
Stop's HRESULT is 0. Manage's volume update ignores SetVolume HRESULT, while
DSB_Play checks SetPosition/SetVolume/Play HRESULT in order. A start error
returns 0 but the original still transfers the request to its playing record.
An already-playing status bypasses those three calls. Wrapped multiplication,
arithmetic shift and original table lookup at 0x498f14 produce volume words;
the captured lookup domain is 0..16. No linear gain model is introduced.

## Evidence chronology and diagnostics

Original-only research commits precede each translation. Frozen files remain
unchanged, including all failed/partial investigations:

| Capture | Calls/scenarios | Preserved result |
|---|---:|---|
| v1 | 188/188 | Five stops: three missing status answers and two unresolved physical-slot fixture inputs |
| v2 | 198/198 | Explicit empty slots; one unresolved _llseek-IAT native fault |
| v3 | 198/198 | Declared seek; pending path actually stops at original CRT memset 0x48c3b0 |
| v4 | 204/204 | Active Manage cases; same CRT interval stop; earlier prose's Create attribution was premature |
| v5 | 204/204 | Exact original Stage-1 memset/STOS intervals permitted; actual CreateSoundBuffer stop at caller 0x48b834 |
| v6 | 223/223 | Active request replacement/cancellation; sole missing-Create stop |
| v7 | 230/224 | Seven persistent PostSound calls, each intermediate memory image; sole missing-Create stop |
| v8 | 234/228 | Explicit creation outputs, null returns and two nonnull missing-Lock stops |
| v9 | 244/238 | Ten PCM creation/fill/start/error/short-read cases; same three intentional stops |

The intentional stops are one undeclared Create (+0x0c, caller 0x48b834) and
two undeclared Lock (+0x2c, caller 0x48c097). All other scenarios return. Before
those stops, the PSB index increments -1→0, dirty fields reset and declared
seek(s) occur; those partial effects are byte-exact in the differential.
`validacao/queue-create-run-history.json` also retains the first rejected v9
setup: the incorrect _hread IAT 0x523200 was refused by Core. The intact call
0x48c042 and Stage-1 SLOTS prove 0x5231e8; the corrected run is separate.
No original instruction, accepted snapshot, policy or mask was patched.
