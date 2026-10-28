; SortilegeSetInvention: limite por próximo símbolo SBL, fim exclusivo 0x004749ca.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004749ad  53                       push     ebx
004749ae  89d3                     mov      ebx, edx
004749b0  31d2                     xor      edx, edx
004749b2  88c2                     mov      dl, al
004749b4  89d0                     mov      eax, edx
004749b6  c1e002                   shl      eax, 2
004749b9  01d0                     add      eax, edx
004749bb  31d2                     xor      edx, edx
004749bd  6689da                   mov      dx, bx
004749c0  c68402448f500001         mov      byte ptr [edx + eax + 0x508f44], 1
004749c8  5b                       pop      ebx
004749c9  c3                       ret
