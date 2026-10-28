; SortilegeSetRealisable: limite por próximo símbolo SBL, fim exclusivo 0x00474991.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00474974  53                       push     ebx
00474975  89d3                     mov      ebx, edx
00474977  31d2                     xor      edx, edx
00474979  88c2                     mov      dl, al
0047497b  89d0                     mov      eax, edx
0047497d  c1e002                   shl      eax, 2
00474980  01d0                     add      eax, edx
00474982  31d2                     xor      edx, edx
00474984  6689da                   mov      dx, bx
00474987  c68402308f500001         mov      byte ptr [edx + eax + 0x508f30], 1
0047498f  5b                       pop      ebx
00474990  c3                       ret
