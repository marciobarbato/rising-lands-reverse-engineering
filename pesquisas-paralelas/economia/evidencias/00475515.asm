; MineDetruire: limite por próximo símbolo SBL, fim exclusivo 0x00475541.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00475515  52                       push     edx
00475516  25ffff0000               and      eax, 0xffff
0047551b  31d2                     xor      edx, edx
0047551d  668b048554995000         mov      ax, word ptr [eax*4 + 0x509954]
00475525  6689c2                   mov      dx, ax
00475528  a1707d5000               mov      eax, dword ptr [0x507d70]
0047552d  66c70450db01             mov      word ptr [eax + edx*2], 0x1db
00475533  a1707d5000               mov      eax, dword ptr [0x507d70]
00475538  66c7445002dc01           mov      word ptr [eax + edx*2 + 2], 0x1dc
0047553f  5a                       pop      edx
00475540  c3                       ret
