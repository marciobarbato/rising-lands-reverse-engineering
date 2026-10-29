# Declared COM input contract for Audio queue captures

This is a deterministic test input contract, not DirectSound reconstruction,
playback, mixing or a statement about hardware timing. The intact code is
RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Original body bytes and hashes are already frozen in the M2.2 sound inventory.
The new original-only v1/v2/v3 captures precede any record/COM translation.

The fixtures explicitly supply every inherited global/table/reference word,
bank-header byte and ordered external answer. `QueueFixtureMemory` is only a
fixture memory view. Queue and dictator aliasing remain in one BSS byte image,
including waiting index 70 at `0x521f84`. Fields not stored by the original keep
their patterned input bytes. These synthetic fixtures are not MONDE01 snapshots.

The bench uses Core's committed `declarar_vinculo` only at mapped external
backend addresses. No sound engine body or original instruction is replaced.
COM object/vtable bytes are declared inputs; native argument order and status
writes are retained in `raw_com`. Other slots raise a named declared stop
before returning or popping the native frame. There is no default success.

| Native method | Vtable slot | Exact input/answer |
|---|---:|---|
| GetStatus | +0x24 | (this, out_u32). Fixture writes the explicitly declared status even when HRESULT is nonzero, then returns the declared HRESULT |
| Stop | +0x48 | (this), explicit HRESULT |
| Release | +0x08 | (this), explicit returned count/HRESULT word; no hardware refcount is inferred |
| SetCurrentPosition | +0x34 | (this, position), explicit HRESULT; not silently supplied |
| SetVolume | +0x3c | (this, raw volume word), explicit HRESULT; not a guessed gain |
| Play | +0x30 | (this, reserved1, reserved2, flags), explicit HRESULT; not real playback |

Only methods reached with a complete exact answer list may return in a capture.
An absent/mismatched answer is a stop, not a fabricated callback. Callback order,
object identities, scalar arguments and answers are compared between native and
Python; raw stack output-pointer addresses are ABI observation metadata.

Original query semantics, captured for null pointers and statuses 0/1/2/4/5/
0xffffffff with HRESULT 0 or 0x80004005:

- `DSB_IsPlaying 0x48be90`: null → 0; otherwise `(status & 1) != 0`.
- `DSB_IsStopped 0x48beb9`: null → 1; otherwise `(status & 5) == 0`.
- `DSD_IsLooped 0x48bedb`: null → 0; otherwise `(status & 4) != 0`.

These routines ignore the returned HRESULT and test the explicitly written
status. If an actual failing device leaves the output uninitialized, the stack
bytes would matter; that is outside this provider's declared domain, not an
implicit zero. `DSB_Stop` first queries stopped status, calls Stop only when
needed, and returns whether its HRESULT is zero. Null returns 1.

Capture v1 preserves five diagnostic stops: three missing status answers and
two intentionally unresolved/inconsistent physical-slot fixture inputs. Capture
v2 declares empty slots and explicit transfer answers but preserves a pending
Manage fault at the unresolved original _llseek IAT. Capture v3 additionally
binds that real Windows import through Core's declared import facility with the
explicit answer `(handle=0x1234, offset=0, origin=0) -> 0`. It supplies no data
or buffer ownership. All 198 v3 native calls run to return except one named
pending-Manage stop at undeclared DirectSound CreateSoundBuffer slot +0x0c. The PSB index increment before that
stop must remain visible. Stage-1 buffer/data providers exist, but their
initialization/file/buffer ownership is not substituted by this queue fixture.

The translated slice must stop before unresolved buffer creation/initialization,
DS position/volume/play branches or caller memory outside the declared image.
No initialized sound state or asynchronous response is created by a constructor.

Capture v4 adds six original Manage cases with a declared active logical slot:
stopped, playing and playing+looped statuses, each with success/error HRESULT.
The fixture supplies the exact expected volume word from the original table,
not a synthesized mixer curve. Stopped state calls the actual cleanup chain;
playing states update volume and clear dirty fields, even on the declared
SetVolume error HRESULT. All 204 v4 calls return except the one explicit
CreateSoundBuffer dependency stop; the original physical-index increment and
seek call before that stop are retained. v1/v2 diagnostics and v3 remain frozen.

Diagnostic correction: v3/v4's pending Manage path first stopped at the undeclared
native CRT memset interval 0x48c3b0, not at COM creation. v5 reuses the exact
stage-1 native memset/STOS intervals (no Python substitution). Its sole stop is
now proven at COM slot +0x0c, original caller return 0x48b834, while 203 cases
return. Earlier raw reports are unchanged and are not counted as complete
buffer-creation captures. The provider/three-way differential use v5.

Creation input extension (v8, original-only): a declared CreateSoundBuffer call
receives the 20-byte original descriptor (size20, flags0xe0, size64, reserved0,
format pointer), the pointed 16-byte PCM WAVEFORMAT (1 channel, 22050Hz,
16 bits, alignment2), and outer=NULL. The log retains the raw stack pointer;
comparison normalizes only its address, not the pointed bytes. Each fixture
explicitly writes the output pointer and returns a declared HRESULT. Null
output returns through Manage with EAX0 for both HRESULT0 and 0x80004005;
non-null output proceeds for either HRESULT and stops at undeclared Lock slot
+0x2c (original caller0x48c097), after a second declared seek. No status or
creation response is inferred from HRESULT alone. v8 has234 native calls in228
scenarios, with the original missing-Create stop plus two missing-Lock stops.

PCM extension (v9, original-only): after a nonnull creation output, Lock has
8 stdcall arguments (this, offset, size, pointer1-out, bytes1-out,
pointer2-out, bytes2-out, flags). These fixtures explicitly supply offset0,
size64, no wrapped region, flags0, and writes(pointer=0x7004000, bytes=64).
The _hread import at original IAT0x5231e8 supplies exactly the declared bytes
(64,32 or0 bytes), without inventing a sample corpus. Unlock receives
(this,0x7004000,64,0,0). Lock/Unlock HRESULT errors do not suppress those
original effects. The subsequent status/position/volume/Play calls have ordered
explicit answers; position, volume and Play errors return0 but the request is
still moved to the playing record. A status already-playing answer bypasses
position/volume/Play. These are declared external observations, not a real
initialized DirectSound device. v9 has244 original calls in238 scenarios and
3 intentional missing-Create/Lock stops. The failed first v9 setup used a wrong
IAT and is retained in validacao/queue-create-run-history.json; the verified
intact instruction and existing Stage-1 mapping determine the correction.
