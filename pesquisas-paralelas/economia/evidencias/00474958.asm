; SortilegeEstRealisable: limite por próximo símbolo SBL, fim exclusivo 0x00474974.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00474958  53                       push     ebx
00474959  89d3                     mov      ebx, edx
0047495b  31d2                     xor      edx, edx
0047495d  88c2                     mov      dl, al
0047495f  89d0                     mov      eax, edx
00474961  c1e002                   shl      eax, 2
00474964  01c2                     add      edx, eax
00474966  31c0                     xor      eax, eax
00474968  6689d8                   mov      ax, bx
0047496b  8a8402308f5000           mov      al, byte ptr [edx + eax + 0x508f30]
00474972  5b                       pop      ebx
00474973  c3                       ret
