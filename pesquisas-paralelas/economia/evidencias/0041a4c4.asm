; BatimentGetColons: limite por próximo símbolo SBL, fim exclusivo 0x0041a4f4.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0041a4c4  53                       push     ebx
0041a4c5  52                       push     edx
0041a4c6  31d2                     xor      edx, edx
0041a4c8  6689c2                   mov      dx, ax
0041a4cb  89d0                     mov      eax, edx
0041a4cd  c1e004                   shl      eax, 4
0041a4d0  01d0                     add      eax, edx
0041a4d2  c1e002                   shl      eax, 2
0041a4d5  01d0                     add      eax, edx
0041a4d7  c1e002                   shl      eax, 2
0041a4da  bb09000000               mov      ebx, 9
0041a4df  05c8a04900               add      eax, 0x49a0c8
0041a4e4  ba01000000               mov      edx, 1
0041a4e9  83c00c                   add      eax, 0xc
0041a4ec  e8c7cc0200               call     0x4471b8
0041a4f1  5a                       pop      edx
0041a4f2  5b                       pop      ebx
0041a4f3  c3                       ret
