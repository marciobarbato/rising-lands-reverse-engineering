; __init_8087: limite por próximo símbolo SBL, fim exclusivo 0x0048e5b9.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0048e588  53                       push     ebx
0048e589  52                       push     edx
0048e58a  803d4590490000           cmp      byte ptr [0x499045], 0
0048e591  7416                     je       0x48e5a9
0048e593  ba7fe54800               mov      edx, 0x48e57f
0048e598  bb84e54800               mov      ebx, 0x48e584
0048e59d  8915d4934900             mov      dword ptr [0x4993d4], edx
0048e5a3  891dd8934900             mov      dword ptr [0x4993d8], ebx
0048e5a9  31c0                     xor      eax, eax
0048e5ab  66a1dc934900             mov      ax, word ptr [0x4993dc]
0048e5b1  e8f01d0000               call     0x4903a6
0048e5b6  5a                       pop      edx
0048e5b7  5b                       pop      ebx
0048e5b8  c3                       ret
