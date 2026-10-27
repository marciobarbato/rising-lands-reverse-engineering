; TerrainDeposeSac: limite por próximo símbolo SBL, fim exclusivo 0x004761d4.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004761a9  51                       push     ecx
004761aa  56                       push     esi
004761ab  83ec04                   sub      esp, 4
004761ae  89c6                     mov      esi, eax
004761b0  881424                   mov      byte ptr [esp], dl
004761b3  89d9                     mov      ecx, ebx
004761b5  31db                     xor      ebx, ebx
004761b7  eb10                     jmp      0x4761c9
004761b9  31d2                     xor      edx, edx
004761bb  31c0                     xor      eax, eax
004761bd  8a1424                   mov      dl, byte ptr [esp]
004761c0  6689f0                   mov      ax, si
004761c3  43                       inc      ebx
004761c4  e894feffff               call     0x47605d
004761c9  6639cb                   cmp      bx, cx
004761cc  72eb                     jb       0x4761b9
004761ce  83c404                   add      esp, 4
004761d1  5e                       pop      esi
004761d2  59                       pop      ecx
004761d3  c3                       ret
