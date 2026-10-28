; CalculStatusRecrute: limite por próximo símbolo SBL, fim exclusivo 0x00423fb9.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423f9d  53                       push     ebx
00423f9e  51                       push     ecx
00423f9f  88d6                     mov      dh, dl
00423fa1  31c9                     xor      ecx, ecx
00423fa3  6689c1                   mov      cx, ax
00423fa6  31db                     xor      ebx, ebx
00423fa8  81f9ffff0000             cmp      ecx, 0xffff
00423fae  0f8561ffffff             jne      0x423f15
00423fb4  89d8                     mov      eax, ebx
00423fb6  59                       pop      ecx
00423fb7  5b                       pop      ebx
00423fb8  c3                       ret
