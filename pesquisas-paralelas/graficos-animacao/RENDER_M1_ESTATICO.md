# Static render of the accepted MONDE01 M1 state (optional, non-blocking)

Script: `renderizar_m1_estatico.py` (pure Python, no x86/Unicorn). Output goes to the git-ignored
`.local/graficos-m1/` (`monde01_m1_estatico.png`, 800x600, plus a JSON manifest); nothing large is committed.

**Input:** `pesquisas-paralelas/missoes/evidencias/captura-carga-missao-original-v2.json`,
SHA-256 `eb7d2303e13e62d4f5692c9cb6ef302b573d138df6a8b51183a6d9b0bd703afc`, `oracle.final_state` blocks
(base64-zlib, each block hash verified). Pointer slots are resolved through the captured DGROUP block
(`0x494000`): terrain `[0x507d70]`, objects `[0x507d74]`, auxiliary `[0x507dac]`, regions `[0x4e0f38]`,
units `[0x4e19a0]`, projectiles `[0x5080f0]`, discovery `[0x507d78+4c]`, light edges `[0x507d88+4c]`; camera is the
captured `0x508041` (0). This is a different identity from the old pinned pre-structure checkpoint
(`monde01-checkpoint-quadro.*`, unchanged, hashes kept); the old synthetic zero structure pool is not used.

**View:** declared origin (0,3) cells, 25x17-cell window, so the Santuario at cell 2828 (x=12, y=11) is at
pixel (384,256). Window/clip/surface/clock/frame globals are the declared `globais_base` 800x600 values, not
read from M1 (`0x508724` clipping is intentionally not conflated with them). Palette is PLATGAME.PIE.

## Passes
Real (existing reconstructed code, unchanged): Stage 16 cache lifecycle (`CicloCacheTerreno`), `AffGame`
prefix through `CalculFrame`/`DDLockSurface`, `AffTerrain` (425 `GetNumBob`/`AffBloc` blocks) with
`AffVegetTerrain`, `AffSprite` planning, `AffVeget` (29 trees), and the `AffBatiments`/`AffBatimentOmbre`
visibility/clip walk for 278 cells with no structure occupancy. Units and projectiles: none in the window were
drawn (no unit/projectile events reached before the stop; the unit and projectile renderers were not reached).

Missing (visible, not guessed): the composition **stops at `0x407DEF`**, `AffBatiments` structure occupancy
at cell 2829 (the region word has bit 15 set), i.e. the structure lookup/facade for the Santuario is not
reconstructed in the bounded composition (see `INVENTORY_MONDE01_FACADE.md`). The Santuario facade is therefore
absent: the pale footprint at the centre is terrain only. Because AffSprite walks cells in order, the sprite
pass was cut short there; everything after it is absent too (remaining sprite cells, HUD checkpoint
`0x417B1C`, selection box, overlays, minimap, structure facades/workshops/shadow overlays, gray rendering).
The bottom strip (y >= 544) and nothing else is the declared fixture background pattern, not game content.
No new graphics system was implemented and no occupancy or structure record was fabricated.
