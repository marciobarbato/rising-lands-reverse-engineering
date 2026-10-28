; MissionPlaceTerrain: Structure scan after the unit scan; caller order; exclusive end 0x0046c1b8.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c16d  31db                     xor      ebx, ebx
0046c16f  eb01                     jmp      0x46c172
0046c171  43                       inc      ebx
0046c172  31d2                     xor      edx, edx
0046c174  6689da                   mov      dx, bx
0046c177  81fae8030000             cmp      edx, 0x3e8
0046c17d  0f8d72f5ffff             jge      0x46b6f5
0046c183  89d0                     mov      eax, edx
0046c185  e8abe5faff               call     0x41a735
0046c18a  84c0                     test     al, al
0046c18c  74e3                     je       0x46c171
0046c18e  89d0                     mov      eax, edx
0046c190  e81703fbff               call     0x41c4ac
0046c195  89d0                     mov      eax, edx
0046c197  e81ce4faff               call     0x41a5b8
0046c19c  84c0                     test     al, al
0046c19e  7407                     je       0x46c1a7
0046c1a0  89d0                     mov      eax, edx
0046c1a2  e8c90afbff               call     0x41cc70
0046c1a7  31c0                     xor      eax, eax
0046c1a9  ba01000000               mov      edx, 1
0046c1ae  6689d8                   mov      ax, bx
0046c1b1  e8e1dcfaff               call     0x419e97
0046c1b6  ebb9                     jmp      0x46c171
