; SortilegeGetTimeAprentissage: limite por próximo símbolo SBL, fim exclusivo 0x00474785.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047476a  52                       push     edx
0047476b  31d2                     xor      edx, edx
0047476d  88c2                     mov      dl, al
0047476f  89d0                     mov      eax, edx
00474771  c1e002                   shl      eax, 2
00474774  29d0                     sub      eax, edx
00474776  c1e003                   shl      eax, 3
00474779  29d0                     sub      eax, edx
0047477b  668b044574714900         mov      ax, word ptr [eax*2 + 0x497174]
00474783  5a                       pop      edx
00474784  c3                       ret
