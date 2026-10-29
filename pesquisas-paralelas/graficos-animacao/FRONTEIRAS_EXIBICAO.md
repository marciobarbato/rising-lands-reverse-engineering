# Declared display backend for the original oracle (M2 round 3)

The original display wrappers **execute natively**. Core16 forbids binding engine bodies, and none is needed: every wrapper's only
external boundaries are `DirectDrawCreate` and COM calls through four object pointers. `fronteiras_exibicao.py` supplies exactly those.
Inventory: [evidencias/inventario-fronteiras-exibicao.json](evidencias/inventario-fronteiras-exibicao.json) (`inventariar_fronteiras_exibicao.py`,
static, intact `RISING.EXE` 6c556520…43fb, read-only media).

## Module API (for Missions to wire)

```python
from fronteiras_exibicao import ExibicaoDeclarada
exibicao = ExibicaoDeclarada(base=0x3600000, base_superficies=0x3800000)   # defaults; both regions must be free in the bench
exibicao.instalar(bancada)       # maps both regions; declares every binding on `bancada` (Core16 BancadaX86 API)
exibicao.regiao_executavel       # (0x3600000, 0x3604000): trampoline `ret` bytes; the bench must allow fetches/stops here
exibicao.eventos / .manifesto() / .pixels('primaria'|'offscreen')
```
`instalar` uses `declarar_vinculo(..., natureza='backend')` for each COM trampoline (16 bytes apart, outside the PE) and
`declarar_importacao` for two IAT slots; it refuses to run if those slots are not `DirectDrawCreate`/`MessageBeep` in this image.
Surfaces are 8 bpp buffers in `base_superficies` (pitch = width). Declared fixture answers: surfaces are never lost, every supported call returns `DD_OK`.
Unsupported flags, unknown objects, rectangles outside a surface, locks of a locked surface or any COM slot without semantics raise
`ParadaVinculoDeclarado` naming the method. Importing executes nothing.

## Boundary table

| Boundary | Address / slot | Original ABI (from bytes) | Declared behaviour |
|---|---|---|---|
| `DirectDrawCreate` | IAT `0x5234C4`, reached by `jmp [0x5234C4]` thunk `0x493A30` from the `DDInit` call site `0x43F592` | stdcall (lpGUID=0, lplpDD=`0x4E1788`, pUnk=0), `ret 12` | writes the IDirectDraw object pointer, returns 0; stops for non-zero GUID/aggregation |
| `IDirectDraw::SetCooperativeLevel` | vtable `+0x50` | (this, hwnd, flags=0x13), 3 args | records hwnd/flags; stops if flags ≠ 0x13 |
| `IDirectDraw::SetDisplayMode` | `+0x54` | (this, w, h, bpp=8) | accepts 800×600 / 640×480 at 8 bpp only |
| `IDirectDraw::CreateSurface` | `+0x18` | (this, &DDSURFACEDESC(0x6C), &[0x4E178C or 0x4E1790], 0) | primary: flags 1, caps 0x200, size = display mode. Offscreen: flags 7 (caps/height/width read from the descriptor: 800×600), caps 0x840. Anything else stops. |
| `IDirectDraw::CreatePalette` | `+0x14` | (this, 0x44, table, &[0x4E179C], 0) | stores the 256 PALETTEENTRY bytes; flags ≠ 0x44 stops |
| `IDirectDrawPalette::SetEntries` | `+0x18` | (this, 0, 0, 0x100, table) | replaces the 256 entries |
| `IDirectDrawSurface::SetPalette` | `+0x7C` | (this, palette) | associates a known palette |
| `IsLost` / `Restore` | `+0x60` / `+0x6C` | (this) | never lost / DD_OK |
| `Lock` | `+0x64` | (this, NULL, &desc, DDLOCK_WAIT=1, 0) | writes `lPitch` (+0x10) and `lpSurface` (+0x24) only (the wrapper reads `+0x24`; pitch is the constant `0x4E17A0=0x320`); second lock stops |
| `Unlock` | `+0x80` | (this, lpSurface) | must equal the lock pointer |
| `BltFast` (DDFlipPage) | `+0x1C` | (this, x, y, src, &RECT, 0x10), retried on `0x8876021C`, restored on `0x887601C2` | copies the rectangle between declared buffers; out-of-bounds, locked or non-WAIT stops |
| `MessageBeep` | IAT `0x5232AC` (DDUtil_TreatError `0x43F145`) | stdcall 1 arg | stops: a DirectDraw call failed |
| `GetDC`, `ReleaseDC`, `FlipToGDISurface`, `Release` (DDExit), `Flip`, `Blt`, `GetAttachedSurface`, … | other vtable slots | all slots of the three v1 interfaces are present | trap: stop with `Interface::Method` |

Wrapper facts from the intact bytes (all plain `ret`, no stack cleanup): `DDInit 0x43F50B` (EAX=hwnd, DL=hi-res; sets `0x49A018/1A`=800/600,
`0x508724/26`=25/17, pitch `0x4E17A0`=0x320), `DDLockSurface 0x43F3B4` (nested lock count `0x4E17A8`, cached pointer `0x4E17A4`, AL/EAX pointer),
`DDUnlockSurface 0x43F445`, `DDFlipPage 0x43F14F` (AL=copy-HUD flag; shake counter `0x4E1D18`/`0x4DFB44` path when `[0x4DFB44]≠0`),
`DDSetPalette 0x43EE31` (EAX = 256×RGB table; first call creates the palette then sets it on both surfaces). The 640×480 mode still uses the
constant pitch 0x320 while its offscreen surface is 800×600 (not a conflict: only the offscreen surface is locked); the primary has pitch 640.

**Native proof** (`test_fronteiras_exibicao.py`, under the lease): original `DDInit`→`DDSetPalette`→`DDLockSurface`→`DDUnlockSurface`→`DDFlipPage(1)` run over a
Core16 `BancadaX86`; the observed COM sequence is `DirectDrawCreate, SetCooperativeLevel(0x1770,0x13), SetDisplayMode(800,600,8), CreateSurface×2,
CreatePalette, SetPalette×2, Lock, Unlock, BltFast [0,0,800,544], BltFast [0,544,800,600]` and the primary equals the offscreen buffer byte for byte.
`DDGetDC` stops with the `GetDC` slot name. Not yet run inside Missions' oracle.

## What the oracle can now execute instead of skipping

Native with this backend: `AffInit`, `DDInit`, `DDSetPalette`, `DDLockSurface/Unlock`, `DDLockSurfaceVideo/UnlockVideo`, `DDFlipPage`, `ResetMode`, and `AffGame` itself.
The window handle for `SetCooperativeLevel` is whatever `AppWindowInit` produced (Missions' declared value). Still needing their own boundaries or inputs:
`PlayVideo`, `CreateCredits`/`AffCredits` (FLC), `MCICD_*`, `PlaySnd_*`, `GetDC` users (`DDGetDC` callers), the cursor imports (`ShowCursor` is reached at 24 AffGame sites; Missions already answers it).

## Bank and file inventory (what startup/load tail/frame execute)

Calls (call sites in `inventario…json` → `chamadas_de_banco`): `ProgInit` runs `AffInit(0x474E01)`, `PaletteAlloc(0x474DAA)`, `LoadPie platgame.pie(0x474E82)`, `LoadSTRATBank(0x474E9B)`,
`SetBank(0x474EAA)`, `CacheAlloc(0x474EAF)`, and `LoadFonteExterieur` (via `InitTextLangue 0x479413`, opens a file with mode `rb`). `MenuInit` loads menu banks only in its menu modes
(`LoadBank 0x4685FB` Invente.cmp, `0x468BD4` menu.cmp; `LoadPie` titre/pagemis/credits/pageres.pie, `ecranfin.lzs`); the load-state invocation (mode 0x12) reaches one `LoadPie` (`0x468C56`) of `\titre.pie` per Missions' trace.
`AffGame` mode 0x12 calls **no** `SetBank`; it relies on the STRAT bank published by `ProgInit`'s `SetBank` and `CacheAlloc`/`InitCache` state. `RestoreAll` calls `LoadPie platgame.pie` twice.

| File (path as the original builds it) | Media size | Reader |
|---|---|---|
| `\Graphics\Blocs.cmp`, `Troops.cmp`, `Vehicule.cmp`, `Creature.cmp`, `Building.cmp`, `Others.cmp` | 1,426,660 / 3,171,280 / 2,027,609 / 2,585,477 / 1,272,760 / 2,927,906 | `LoadSTRATBank` (table `0x495BC8`) |
| `\Graphics\Invente.cmp`, `\Graphics\menu.cmp` | 637,625 / 1,086,250 | `LoadBank` (menu modes) |
| `\platgame.pie` (ProgInit, RestoreAll, ResetMode), `titre/pagemis/pagemis2/credits/pageres.pie`, `ecranfin.lzs`, `charge.lzs` | 50,177; 391,263/378,945/380,847/439,995/425,571; 343,821; 376,866 | `LoadPie` (extension `.lzs` → `LoadLZSAt`) |

Paths are prefix + name, with the prefix built at runtime in `0x509494` (install directory). SHA-256 of every file is in the inventory JSON; `Ia.INI` is not in the media copy.
**Cost of letting startup execute `LoadSTRATBank`** (Stage 16 capture `captura-quadro-original.json`): 12 `fopen`/12 `fclose`, **24,314 `GlobalAlloc` + 24,314 `GlobalLock`**, **48,636 `fread`**
= 97,288 binding calls; the existing bench budgeted 4,000,000 instructions for it. Against the oracle limits (60,000 allocations, 200,000 bindings, 200,000 segments), the load adds ~24.3k allocations
(~25.2k total with M1) and ~97k bindings/segments, which fits only if the other startup budgets stay as they are; Missions should raise the limits explicitly if its totals differ.
The startup also needs `CacheAlloc`/`InitCache`/`GetNumBob` state (`CicloCacheTerreno` models it; `ciclo_cache` tests are the original comparisons).

## RestoreAll (0x474B08): non-pixel DGROUP effects (static, not yet run in the oracle)

Order: `DDLockSurface → LoadPie(prefix+"\platgame.pie", surface) → AffTerrain(origin 0x508720/22) → DDUnlockSurface → DDFlipPage(1) → DDSetPalette([0x4E24B0]) →` the same lock/LoadPie/AffTerrain/unlock/flip a second time.
Absolute DGROUP stores in its 110-routine closure (25 addresses; CRT noise included): game/display relevant are
`0x508F70` (RestoreAll stores the locked pointer), `0x4E17A0` (=0x320), `0x4E17A4/0x4E17A8` (lock pointer/count; net 0/0 after the second unlock),
`0x49A04E` (GetNumBob), `0x4DFB44` and **`0x4E1D18`** (DDFlipPage; written only if `[0x4DFB44]≠0`, so untouched while it is 0), `0x4E1D1C` (FileOpen/FileClose handle), `0x4E2F3C` (MemAlloc), CRT/allocator cells
(`0x499080`, `0x4990BC..C4`, `0x49936C`, `0x499480..88`, `0x52223C..0x5223D0`). Pixel output goes to the locked/offscreen surface buffer, not DGROUP. `AffTerrain` updates the terrain cache (`CicloCacheTerreno` state), and
`DDSetPalette` creates the palette object at `[0x4E179C]` on first use. Open: the actual written values, the `LoadPie` palette side effects (`[0x4E24B0]` tables) and whether `AffTerrain`'s `AffVegetTerrain` touches the
RNG cursor: only a native run over the declared backend can answer; no value is claimed here.
