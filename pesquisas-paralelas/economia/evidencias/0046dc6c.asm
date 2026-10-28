; PlayerGetSympathie: limite por próximo símbolo SBL, fim exclusivo 0x0046dc90.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0046dc6c  53                       push     ebx
0046dc6d  88d3                     mov      bl, dl
0046dc6f  31d2                     xor      edx, edx
0046dc71  88c2                     mov      dl, al
0046dc73  89d0                     mov      eax, edx
0046dc75  c1e002                   shl      eax, 2
0046dc78  01d0                     add      eax, edx
0046dc7a  8b15a8805000             mov      edx, dword ptr [0x5080a8]
0046dc80  c1e002                   shl      eax, 2
0046dc83  01c2                     add      edx, eax
0046dc85  31c0                     xor      eax, eax
0046dc87  88d8                     mov      al, bl
0046dc89  668b44420c               mov      ax, word ptr [edx + eax*2 + 0xc]
0046dc8e  5b                       pop      ebx
0046dc8f  c3                       ret
