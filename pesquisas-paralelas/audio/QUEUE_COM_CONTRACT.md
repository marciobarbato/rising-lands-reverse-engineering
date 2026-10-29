# Declared COM input contract for Audio queue captures

This is a deterministic test input contract, not DirectSound reconstruction,
playback, mixing or a statement about hardware timing. The intact code is
RISING.EXE SHA-256 `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
Original body bytes and hashes are already frozen in the M2.2 sound inventory.
The new original-only v1/v2 captures precede any record/COM translation.

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
v2 declares empty slots and explicit transfer answers. It covers 198 native
calls; its one remaining declared stop is pending Manage at the undeclared
DirectSound CreateSoundBuffer slot +0x0c. The PSB index increment before that
stop must remain visible. Stage-1 buffer/data providers exist, but their
initialization/file/buffer ownership is not substituted by this queue fixture.

The translated slice must stop before unresolved buffer creation/initialization,
DS position/volume/play branches or caller memory outside the declared image.
No initialized sound state or asynchronous response is created by a constructor.
