# M3 sound-request provider and comparable stream

This delivery supplies Core's named sound dependency and the request-stream
transport. It does not enable device playback, change the accepted frame
boundary policy, integrate main, or record M3 acceptance.

## Original first

The only execution oracle is intact `RISING.EXE`, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The original request capture was committed in `37ad346` before the provider.
`evidencias/m3-pedidos-original-v1.json` contains 58 original calls: 56
`PlaySnd_PostSound 0x48aa79` and two `PlaySnd_StopSound 0x48aac0`.
Arguments come from Core's committed selection/order capture; inherited private
sound bytes and caller handle words come from the accepted M2.2 frame-128
state. These are explicit leaf inputs, not a new scripted-input mission run.
All 58 calls return EAX **0**, with identical final inherited memory.

There is no initialized-flag guard in PostSound or StopSound. PostSound first
moves EDX (sound ID) into EAX and dispatches full-u32 selectors `0x41/0x42/0x50`.
An invalid selector returns that sound ID. A valid selector calls
`HandlSnd_Insert 0x48a218`, forwarding ECX's low byte and the pushed volume.
On the accepted unopened banks, the free caller handle is `0xffffffff`, the
bank entry count and header pointer are zero, and the ID search returns absent.
Admission reserves waiting index 20, writes the entry-pointer word at
`0x52137c + 20*44 + 0x18` to zero, then gives back the reservation (index 19)
and returns zero. Those stores have no final difference in this image.
StopSound tail-jumps to `HandleSnd_StopHandle 0x48a438`; a free handle returns
zero without writes. The original's EAX is **not** the frame bench's unchanged
EAX declaration. Core's callback receives the actual zero result.

`PlaySnd_Manage 0x48aaca` tail-jumps to `HandlSnd_ValidateListe 0x48a7f9`:
ClearListe, AffectVolumeOut, then LaunchWaitingSound. The accepted empty image
returns EAX 1, stores zero at `0x521f88`, and clears dirty word `0x498f5c` from
1 to 0. Earlier original M2.2 pump captures already establish those effects.
The accepted display captures skip Manage and retain dirty=1; the provider
does not hide that difference or change the accepted reference/mask.

The accepted M1/M2 path never executes `PlaySnd_InitSoundLib 0x48a89f`, nor
`MCICD_Init`. No initialized mission checkpoint is claimed. Initialized queue
behavior instead reuses the original-first v9 queue, v3 continuation and v3
dictator corpora, with explicit synthetic metadata and ordered platform answers.

## Provider API and supported domain

`provedor_pedidos_m3_audio.SoundRequestProvider(memory, *, domain,
stream=None, capture=None)` is callable as
`som(nome, registradores, pilha) -> EAX`.

For Core's `u8/u16/u32(address, value=None)` and `vista(address,size)` memory,
wrap the object in `LiveAudioMemory`. This adapter retains the original live
buffers; caller handle words, request records, waiting index, PSB, LSB and
aliased globals are mutated in place. The input register mapping is not
mutated; the requested Core contract returns EAX only, not the full native
register file or arithmetic flags.

Entries and argument widths:

| Name | Registers read at the API | Stack words | Return |
|---|---|---|---|
| PlaySnd_PostSound | EAX selector, EDX ID, EBX caller word address, ECX flags; all explicit u32 | one u32 volume | original admission result, or ID for an invalid selector |
| PlaySnd_StopSound | EAX caller word address, u32 | none | 0 for a free handle, otherwise captured stop result |
| PlaySnd_Manage | none | none | original aggregate launch result |

`domain='unopened-display'` checks the complete accepted private image:
`0x498f14..0x498f6c` and `0x521358..0x522234`. Dirty word `0x498f5c` may be
either accepted 1 or manager-produced 0. Valid-selector posts and stops require
a free caller word. The bank search with count zero reads no NULL header;
`fila_audio.load_info` now preserves that original branch. It supplies no
DirectSound backend. Nonempty/private changes or busy caller words raise
`DependenciaSom`; it does not infer an initialized state from one flag.

`domain='captured-initialized', capture=(artifact, case_name)` admits only the
exact input memory, request arguments and sequence transitions in the three
named committed corpora. It uses precisely that case's platform transcript,
with independent HRESULT and output/status writes; no default backend exists.
Only successive PostSound/StopSound/Manage steps are exposed. A fixture whose
next step is another library routine stops at that dependency. The existing
`AudioQueue` remains the broader reference interface for those other helpers.
This narrow Core adapter therefore cannot silently extrapolate a synthetic
initialized queue to live mission playback.

Queue operations retain admission, caller invalidation, compaction, physical
release, logical promotion, descending waiting traversal and exact callback
order from the earlier queue/continuation contracts. Initialized replay checks
all inherited regions at every admitted entry, including physical/logical slots
and caller references. Provider/backend exceptions propagate after earlier
effects, with no rollback. Unknown entries/domains do not return a default.

## Request stream v1

`fluxo_pedidos_audio.AudioRequestStream` records
`rising-lands/audio-request-stream/1`:

```json
{"schema":"rising-lands/audio-request-stream/1","events":[
  {"sequence":0,"frame":129,"phase":"frame129",
   "routine":"PlaySnd_PostSound","caller_return":4460028,
   "registers":{"EAX":80,"EDX":460800,"EBX":1196065028,"ECX":0},
   "stack_words":[256]}
]}
```

Each event has its zero-based stream sequence, logical frame, exact phase,
routine, original caller return address, argument registers and pushed
argument words. All numeric fields are JSON integers; arguments are u32.
PostSound retains all four raw argument registers (including high ECX bits)
and one volume. StopSound retains EAX only. Manage has empty registers and
stack. The source boundary logs' four unused stack-residue words and unused
Manage registers are not routine arguments. No return EAX is part of this
input stream, since the accepted bench declares boundary returns.

The provider appends before executing, including a request that subsequently
stops. Set its `phase` and `caller_return` at every call site when using
`stream`; missing context raises. `from_boundaries(phases)` projects the same
schema from Missions' existing ordered events. Only the three named entries
are included; MCICD and other PlaySnd entries need a later schema/contract.
`compare_streams(expected,actual)` validates and compares every event exactly,
including length, call site and order. It does not sort, deduplicate or mask.

The projected original streams are committed as
`evidencias/m3-fluxo-m22-original.json.xz` and
`evidencias/m3-fluxo-m23-original.json.xz`, with input/output hashes and
projection provenance in `evidencias/m3-fluxo-original-proveniencia.json`
(evidence commit `87921d8`). They contain request arguments, not commercial
audio samples. The replay also compares against these frozen stream documents.

## Validation and practical limits

`validar_pedidos_m3_audio.py` replays **58 display calls and 111 initialized
calls in 99 scenarios**, with zero EAX or full-memory mismatches. The
initialized sequence includes posting three requests, managing shared sound
reuse, stopping the physical owner with logical promotion, reposting and
managing again. A separate reference test rejects a changed ID before effects.

Stream replay projects immutable raw Missions boundaries, feeds the requests
through the provider's recorder, and compares the output with the projection:

| Source | Phases | Events | Mismatches |
|---|---:|---:|---:|
| Accepted M2.2 frames 0..128 | 257 | 128 Manage | 0 |
| Accepted M2.3 frames 0..9200, all ten hash-checked parts | 18,401 | 9,200 Manage | 0 |
| M2.3 raid window 8991..9200 (part 9) | 420 | 210 Manage | 0 |

The M2.3 stream's 128-event prefix equals M2.2 exactly. Neither no-input
window posts/stops a sound. This is a trace-driven transport/provider check,
not an independent replay of game emitters or an S1/M3 gameplay proof. The 58
Core leaf requests and stream corruption tests cover post/stop argument fields,
missing/extra events, reordering, call-site changes and full-width flags.

The earlier `M22_SOUNDNESS.md` native chained proof establishes zero readers of
private sound state outside the sound library over 128 frames. It records the
shared game CD flag `0x4e2f28` and cursor `0x4e1d18` reads separately. Those
are game logic state; playing-CD behavior cannot be masked as private audio.
The new M2.3 native audit (`evidencias/m3-raid-leituras-original-v2.json`,
evidence commit `2c8a0b9`) re-enters all 420 phases of frames 8991..9200 from
accepted memory/registers and explicit caller stack words. All state summaries
and ordered boundary argument logs equal, in 274.484 seconds. There are no
private-library readers/writers with the accepted boundaries. This is bounded
phase re-entry, not a resumable native-stack/CPU checkpoint. The checked summary
is `validacao/m3-raid-soundness.json`.

The raid audit records 3,561 dword reads of unit `+0x104`, all -1, at 0x45446a;
210 CD-playing-byte reads at 0x42d2f0; 210 shared-cursor reads at 0x42d2f9; and
265 shared-cursor reads by NextAnimVeget at 0x47732f. It observes no structure
`+0x100` or unit `+0x10c` reads. The latter watched word is initialized to -1
by CreerEngin, then receives 0x12 from iagUnitAddToGroup at 0x48297a. It is not
treated as exclusively audio state. No state mask was added or changed.

Game-owned sound handles are a separate dependency. The intact dispatcher
prefix in [the existing original disassembly](../ia-runtime/evidencias/0045442c.asm)
loads the u32 unit `+0x104` at **0x45446a** when its state byte `+2` is nonzero.
It compares the handle with -1 at 0x454474. A free handle clears unit byte
`+0xf9` at **0x454491**. A busy handle computes EnginGetVolume and calls
`PlaySnd_PostVolume 0x48aacf` at **0x45448a**. Therefore even an unread private
library table is not proof of audio independence: library stores into caller
handles can change the game path. The accepted unopened domain retains free
handles. Selection/EnginAsk additionally tests unit `+0x104`, and structure
selection tests `+0x100`, in Core's separate leaf captures.

Core/AI-runtime handoff: bind the actual EAX provider instead of the unchanged
boundary declaration; preserve game-owned handles and `+0xf9` in logic state.
For stream recording, pass phase and original caller-return context at the
emitter. Core's present three-argument callback omits the call site; its
PostSound sites are 0x440de7 / 0x41b785 and StopSound is 0x474582 (return =
site+5). This delivery does not silently infer arbitrary caller locations.
The initialized busy-handle mission path additionally needs the PostVolume
entry wired by its owner; this adapter raises for that unsupported entry.

Gaps: real DirectSound/library initialization and asynchronous playback,
initialized mission state, busy caller handles in the unopened display domain,
S1 scripted-input emitter equality, app playback, StopAllSound at victory and
result-screen MCICD music. No long original run is required for this adapter;
the middle M2.3 frames' request transport is checked from committed evidence.
