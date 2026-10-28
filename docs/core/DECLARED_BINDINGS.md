# Declared native boundaries

Stage 16 API, 2026-10-28, base main `b610bfad77ffadaa0ee5f6af02160d786ccfdc7b`. This is opt-in harness infrastructure, not an implementation of Windows or an engine routine. Original executable identity remains `6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`. Fresh native validation passed; committed publication follows the domain and locked integration gates. Consumers adopt the published commit rather than a live worktree.

## Core bench API

`BancadaX86.declarar_importacao(iat, nome, quantidade_argumentos, atender)` explicitly resolves one stdcall IAT slot to a private mapped thunk. Slots must occur in the intact PE32 import descriptors/thunk tables; aligned arbitrary engine data is rejected. The thunk contains a decodable RET byte but is never executed: all bound entries are stop addresses, and the dispatcher runs only after emulation has stopped. Arguments are unsigned dwords at ESP+4, +8, etc.; cleanup is 4 bytes per argument. Only the declared data IAT slot is changed; original code bytes remain intact. Each import resolution records its old/new target and authoritative DLL/symbol metadata. Duplicate or code-overlapping slots fail. The private page is allocated only when bindings are requested.

`BancadaX86.declarar_vinculo(endereco, nome, argumentos, atender, *, desempilhar=0, natureza)` declares a known external boundary or I/O wrapper. `natureza` must be `importacao`, `io`, `relogio` or `backend`; an unknown engine body is never an appropriate binding. The caller supplies the exact boundary address and ABI from its source evidence. The return address is popped and exactly `desempilhar` additional stack bytes are removed. A register-ABI/cdecl wrapper normally uses zero cleanup.

Inside the original PE, direct declarations are restricted to the inventoried I/O entries FileOpen/FileClose/FileRead/FileSeek and CRT fopen/fread/fclose (the explicit `FRONTEIRAS_IO` table), with kind `io`. Other original engine addresses are rejected regardless of a proposed kind label. Outside the image, owners may explicitly declare mapped external backend entries. Adding an original-image boundary requires its own byte-grounded owner review; the standalone registry transport is not evidence that an arbitrary engine replacement is valid.

Argument selectors are full uppercase GPR names (EAX/EBX/ECX/EDX/ESI/EDI/EBP) or aligned byte offsets from ESP, excluding offset zero. `ArgumentoVinculo(origem, bits=32, assinado=False)` declares a consumed 8/16/32-bit register/stack width. Plain strings/integers mean unsigned 32-bit selectors. For example:

```python
b.declarar_importacao(0x5231c0, 'KERNEL32.GlobalAlloc', 2, allocator_fixture)
b.declarar_importacao(0x5231d0, 'KERNEL32.GlobalLock', 1, lock_fixture)
b.declarar_vinculo(0x48c97b, 'CRT.fread', ('EAX', 'EDX', 'EBX', 'ECX'),
                   read_fixture, natureza='io')
```

`atender(chamada)` receives a `ChamadaVinculo` with immutable argument/register snapshots, the original return address, and `ler(endereco,tamanho)` / `escrever(endereco,bytes)` for mapped fixture data. Writes are hashed/logged and may not patch original executable sections. Allocation/file adapters remain with the consuming owner; no file, clock, handle or success default is supplied.

The handler must return an explicit integer EAX or `RetornoVinculo(eax, registradores={...})`. Values truncate to u32. Extra results may name non-EAX GPRs; stack/IP changes are controlled by the dispatcher. Other registers and flags are preserved by this declared fixture. A None result is an error, never success. `ParadaVinculoDeclarado` records an unsupported/exhausted fixture; other exceptions record an error. Both propagate with prior memory/fixture effects and the unpopped native frame retained. There is no automatic rollback.

`b.vinculos_declarados.eventos` records each entry, kind, exact consumed arguments, return address, pre-call registers/ESP, memory-write hashes, status and returned registers or error. `b.importacoes_declaradas` records IAT resolutions. `b.retomadas_vinculos` counts native continuations after a handled boundary, separately from original routine calls. `b.execucoes` includes those additional bounded segments. Legacy bench `entradas_originais` maps may also contain continuation addresses; new reports must identify user routine entries separately.

`executar`/`retomar` keep their existing arguments and instruction/wall limits, adding `limite_vinculos=65536`. This explicit per-top-level budget is not reset by automatic native continuations. Before the next handler would exceed it, `LimiteVinculosDeclarados` raises with the unpopped frame and all earlier effects retained; `parada_limite_vinculos` records the address/limit/handled count. It is a failure/declared budget stop, never a successful return. Stage 16 remap fixtures use a budget of four and test exhaustion at one. Explicit user calls to `retomar` start a new requested budget.

Explicit caller stops take priority over binding invocation. Existing subclass guards and their preserved-state loop resumptions remain in use; execution resumes at the native return address with the same stack and all undeclared registers/flags intact. Nested native execution from a handler is rejected before register initialization. Data writes into original .data/.bss/DGROUP and mapped stack/arenas are allowed; only original executable sections are protected. Without registered bindings the old execution path is used directly. No bound engine body, synthetic CALL/RET, instruction patch, timeout suppression or automatic limit increase is allowed.

## Validation status

Small CPU-independent protocol tests cover argument widths, callee/caller stack cleanup, preservation, partial writes on explicit stop, forbidden code writes, invalid registration and rejected implicit success. They do not execute x86 and do not establish native ABI equivalence. Fresh native validation passed 19 tests with zero skips, native faults or instruction/wall limits: 1,073 bounded segments, including nine true remap entries, 768 original queries and two original FileOpen/FileRead wrappers over explicit CRT fixtures. The wrappers preserve EBX/ECX and read into original DGROUP data. One deliberately unavailable lock and one exhausted binding budget stop with prior effects/frame retained. The no-binding legacy path also passes seven focused tests, 45 original entries and 241 segments. See `relatorios/classificacao-remapeamento-emulada.json` and `relatorios/stage16-legacy-emulada.json`. These fixtures do not establish Windows semantics, full remap or full MissionLoad.
