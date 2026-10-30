# Normal bitmap text — Graphics API 1.11

`renderizar_quadro(..., hud=True, texto=None)` now draws the literal tooltip with
the original bitmap provider. A supplied callable still receives `(request, pixels)`;
`texto=False` explicitly requests the former named dependency for diagnostics.
The strict historical probe adapter remains validation-only.

The native executable is intact `RISING.EXE`, SHA-256
`6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb`.
The display-v2 scenario skips `InitTextLangue 0x479383` and
`TextGetMessage 0x478a3b`. In this scenario **TEXTES.TXT is not loaded**.
Calling TextGetMessage returns the declared zero; dereferencing that as a string
would be invalid. This contract consumes actual bytes at the AffText caller,
including the original literal CAVE/builder/farmer tooltip strings. It neither
fabricates message-bank contents nor turns an opaque message pointer into empty
text. Enabling TEXTES loading is a separate Missions/Core display-scenario contract.

`AffText 0x459454` is executable independently of that lookup. The original
display scenario has already loaded the six bitmap fonts into STRAT's aggregated
bitmap table, addressed through `[0x508f6c]`. Their IDs belong to OTHERS.CMP in
the aggregate catalog. The isolated original matrix proves 270/270 full surfaces
and 7,620 glyph blits. `capturar_affgame_glifos.py` additionally reproduces complete
historical AffGame calls before removing only the AffText boundary and executing
the same calls again. It retains original text lookup declarations explicitly.

## Consumer contract (including the Rust renderer)

Use `texto_afftext_bitmap.py` as the executable specification. No native execution
or host font is needed in production. The proved input domain is fonts 1..6,
language `[0x4e1d94] = 0`, multibyte `[0x4e1d98] = 0`, colour flag 0,
clip flag 0/1, at most 127 printable single-byte characters, ending at NUL/newline.
Unsupported colour, multibyte and control paths retain addressed dependencies.

- Font bases: `23d5, 24b5, 2595, 2675, 2755, 2835` (hex). A non-space
  byte `c` draws bitmap `base + c - 32` with PasteBobCmp `0x45b247`.
- Metrics for even fonts use the preceding odd font. Height comes from `j`;
  a space advances by `l`'s width without drawing. Other advances use the
  corresponding metric glyph width.
- Rectangle x/y/right/bottom are signed 16-bit inputs. The provider preserves
  the original centering, signed widths, truncation toward zero and per-glyph
  signed position wrapping. Follow the implementation, including x==right.
- Clip words are inclusive `(left, top, right, bottom)` at
  `49a020, 49a01c, 49a022, 49a01e`. Flag 0 uses the whole 800×600 surface;
  flag 1 uses these actual words. Unclipped out-of-buffer writes are unsupported.
- Preserve CMP opacity, including opaque index zero. Keep indexed palette bytes;
  RGBA conversion uses the same loaded game palette as the rest of the frame.
- The tooltip caller saves the complete background with GetBob **before** its
  frame/shading/text. AffText runs after shading, before cursor composition.
  Export `saved_background_pixels` and replay it at the following PasteBob restore,
  along with the returned cache and ordered DGROUP effects. Rendering never mutates
  the input memory or advances logic.

S1's real objectives page uses `AffString 0x4591c8`, rather than AffText. Its
`compor_objetivos_s1` provider consumes the actual mission-loader line pointers;
the existing native proof covers seven complete page surfaces. MenuInit's opaque
message and LoadPie boundaries remain separate and are not production glyph defaults.

The macOS frame-141 report is in the **Rust C ABI**, which must adopt this contract
in its own front before normal human Test B can be rerun. Graphics owns this Python
provider, the native evidence and this contract; no Rust/app files are changed here.
