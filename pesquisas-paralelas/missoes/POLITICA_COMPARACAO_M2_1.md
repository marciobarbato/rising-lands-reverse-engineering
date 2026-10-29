# M2.1 comparison policy: what is compared, what is masked, and why

The M2 reference is the display scenario over Graphics' declared backend:

- [entrada-carga-missao-exibicao-v2.json](evidencias/entrada-carga-missao-exibicao-v2.json)
- [captura-carga-missao-exibicao-v2.json](evidencias/captura-carga-missao-exibicao-v2.json)
- [captura-quadro1-monde01-exibicao-v2.json](evidencias/captura-quadro1-monde01-exibicao-v2.json)
- [rastro-quadro1-monde01-exibicao-v2.json](evidencias/rastro-quadro1-monde01-exibicao-v2.json)

The policy artifact is [validacao/m2-politica-comparacao-quadro1.json](validacao/m2-politica-comparacao-quadro1.json), produced by [politica_comparacao_quadro1.py](politica_comparacao_quadro1.py) (original only, passed). v1 remains historical evidence.

## Reference and backend

Graphics' `fronteiras_exibicao.ExibicaoDeclarada` (d8b1af9) replaces Missions' retired interim backend. It is installed after the bench's own imports, so every earlier trampoline keeps its address, and its surfaces live at `0x60000000`.

The v2 reference is **not byte-for-byte** equal to the Stage17 interim captures. In every state (entry, MissionLoad return, load_tail, between_frames, frame1), exactly the same 10 DGROUP bytes differ. They are the pointers the program stores from the backend:

| Address | Pointer | Interim | Graphics |
|---|---|---|---|
| `0x4e1788` | IDirectDraw | `0x03608000` | `0x03604110` |
| `0x4e178c` | primary surface object | | |
| `0x4e1790` | offscreen surface object | | |
| `0x4e179c` | palette object | | |
| `0x508f70` | offscreen pixel pointer | `0x60080000` | `0x60075000` |

The pixel pointers differ because the interim backend aligned surfaces to 64 KiB and Graphics aligns them to 4 KiB.

Everything else is identical ([m2-exibicao-v2-vs-interino.json](validacao/m2-exibicao-v2-vs-interino.json)): all other state bytes, the 25,482 allocation records, the 1,400-request MissionLoad log, the startup binding counts, the entry trace, the boundaries, the Windows answers and the binding names per phase.

The v2 reference passes the same checks as Stage17:

| Check | Report |
|---|---|
| Stage14 strict composition, whole state equal | [m2r4-m1-composition-strict-exibicao-v2.json](validacao/m2r4-m1-composition-strict-exibicao-v2.json) |
| MissionLoad original-only checks | [m2r4-missionload-exibicao-v2-x86.json](validacao/m2r4-missionload-exibicao-v2-x86.json) |
| Frames 0/1 original-only checks | [m2r4-frame1-exibicao-v2-x86.json](validacao/m2r4-frame1-exibicao-v2-x86.json) |

## Method

1. **Changed bytes.** A byte is changed if it differs from the previous state after (a) load_tail, (b) between_frames or (c) frame1. There are 78,869 such bytes over DGROUP, the CRT thread page and every allocation.
2. **Native rerun.** The reference is rerun from the program start. During the three phases, every read and every write of those bytes is hooked: ranges are widened by 3 bytes because Unicorn reports only accesses that start inside the range, the hooks filter per byte, and the translation cache is flushed. The declared surface region gets the same treatment.
3. **Context of each access:**
   - **display:** a display root is active on the call stack. A root begins at its entry and ends exactly when its RET lands on the return address with ESP = entry + 4. The roots are AffGame, RestoreAll, AffInit, DDInit, DDSetPalette, DDLockSurface/DDUnlockSurface, DDLockSurfaceVideo/DDUnlockSurfaceVideo/DDLockSurfaceTemp, DDFlipPage, DDRestoreAll, DDScreenCopy, AffTerrain, FilledBox, Box, MenuDisplay and LoadPalette.
   - **backend:** a host write by a declared DirectDraw handler.
   - **logic:** everything else, including the non-display bindings.
4. **Rule.** A byte is **display-only** when every writer **and** every reader in (a)–(c) has display or backend context. Every other changed byte is **game logic and is compared**.

## Result

- **Masked (display-only):** 78,093 bytes in 8,780 ranges.
  - **19 DGROUP bytes:**

    | Address | Content | Writer |
    |---|---|---|
    | `0x496394..96` | fps text | CalculFrame |
    | `0x4963b5` | fps text | utoa |
    | `0x49a02e/32` | saved clip rectangle | SaveCurrentClipping (read by RestaureClipping) |
    | `0x49a042/44` | cursor copy | AffGame |
    | `0x49a04e` | GetNumBob slot | GetNumBob |
    | `0x4e17b0..b6` | tick copies | CalculFrame |

  - **78 whole allocation blocks (78,074 bytes):**
    - the terrain-bob cache bitmaps, written by CopyBitmap32x32, MemOmbreCopy, PasteBitmap32x32 and GetNumBob, and read only by AffBloc, GetNumBob and MemOmbreCopy;
    - allocation 2, the palette, which Cyclage cycles and DDSetPalette reads.
  - **The surfaces** (`0x60000000..0x60200000`) are outside every state block. They received 498,980 display and 2,400 backend accesses and **0 logic-context accesses**.
- **Compared (game logic):** 776 bytes. The entries below show which routine wrote and which routine read each one:
  - **RNG `0x497164`:** Random.
  - **CRT rand seed (thread page +0xc):** rand, called by NextAnimTerrain over the 25×17 viewport.
  - **Permutation cursor `0x4e1d18`:** CalculGame, MenuInit and NextAnimVeget. It is logic state and must be modeled.
  - **NextGouttes table `0x4e1da0..`:** NextGouttes.
  - **Unit and structure bookkeeping `0x4e1928`, `0x4e1a38..4e`, `0x4dfaa8`:** CalculEnginNextEtape and CalculBatimentNextEtape.
  - **Resource presentation bits `0x4e2eb4..be`:** CalculMatiere. AffCompteurMatiere also reads them, so they stay compared.
  - **Hangar table `0x4e296c`:** ResetTableauHangar.
  - **Counters:**
    - **`0x496d40`:** GameNextFrame.
    - **`0x4973e8`, `0x509952`:** UpdateChamp/SetUpdateChamp.
    - **`0x508f7c/80/84`:** written by ProgIteration and CalculGame. Logic readers include AvanceMonstre, EnginNextEtape and CalculBatimentNextEtape.
  - **View origin `0x508720/22`:** ScrollTerrain. It is read by logic and by display.
  - **Cursor `0x5099a8..ac`:** ProgIteration and InputGame.
  - **Mouse zones `0x5099c4..0x509bb0`, `0x50a9b6/b8`:** MouseSetZone, read by MouseZone.
  - **Game state `0x4e2f78`:** MenuInit.
  - **AvanceMonstre flag `0x50a9cc`.**
  - **Unit fatigue and message bytes (allocation 24330):** CalculFatigue and iagMessTestSendMessageEngin. AffDeplaceEngin also reads the fatigue bytes.
  - **Projectile flags (allocation 25191):** ProjectileCalcul.
  - **Input queues (allocations 25192–25195):** ProcessInputGame.

**Conservative calls:**

- SetClipping's clip words `0x49a01e/22` are compared. CalculGame calls SetClipping directly in the load state, so at least one writer is logic, even though only blitters read the words.
- Any byte the display path writes that logic also reads is compared, and display readers never mask a logic writer. The only byte of this kind here is the display reader of the fatigue byte.

**Freed allocations.** In load_tail, 146 menu-bank allocations are freed (MenuInit → DeleteBank). They hold no state bytes afterwards. Their allocation records change (active = false, free event); comparing or masking those records is an open coordinator decision.

**Scope.** The proof covers the declared phases only, through frame 1. A byte masked here could be read by logic in a later frame; this policy must be re-derived before M2.2.

## How AI/runtime should compare

- Compare every state block of the reference after each phase, except the 78,093 masked bytes. The exact ranges and blocks are in `exclusion_mask`.
- Do not compare surfaces.
- Normalize the 10 backend-pointer bytes only if the composition uses a different declared backend layout. With Graphics' backend they are equal.
