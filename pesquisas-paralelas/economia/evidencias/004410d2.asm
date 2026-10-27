; EnginGetRessource: limite por próximo símbolo SBL, fim exclusivo 0x00441108.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004410d2  56                       push     esi
004410d3  89de                     mov      esi, ebx
004410d5  31db                     xor      ebx, ebx
004410d7  88c3                     mov      bl, al
004410d9  89d8                     mov      eax, ebx
004410db  c1e002                   shl      eax, 2
004410de  29d8                     sub      eax, ebx
004410e0  c1e003                   shl      eax, 3
004410e3  01d8                     add      eax, ebx
004410e5  668b1c45b0654900         mov      bx, word ptr [eax*2 + 0x4965b0]
004410ed  66891a                   mov      word ptr [edx], bx
004410f0  668b1445b4654900         mov      dx, word ptr [eax*2 + 0x4965b4]
004410f8  668916                   mov      word ptr [esi], dx
004410fb  668b0445b2654900         mov      ax, word ptr [eax*2 + 0x4965b2]
00441103  668901                   mov      word ptr [ecx], ax
00441106  5e                       pop      esi
00441107  c3                       ret
