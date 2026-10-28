; MissionPlaceTerrain unit/capacity prefix; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c122  53                       push ebx
0046c123  52                       push edx
0046c124  31db                     xor ebx, ebx
0046c126  eb01                     jmp 0x46c129
0046c128  43                       inc ebx
0046c129  31d2                     xor edx, edx
0046c12b  6689da                   mov dx, bx
0046c12e  81fa20030000             cmp edx, 0x320
0046c134  7d1f                     jge 0x46c155
0046c136  89d0                     mov eax, edx
0046c138  e8c25efdff               call 0x441fff
0046c13d  84c0                     test al, al
0046c13f  74e7                     je 0x46c128
0046c141  89d0                     mov eax, edx
0046c143  e877a4fdff               call 0x4465bf
0046c148  84c0                     test al, al
0046c14a  74dc                     je 0x46c128
0046c14c  89d0                     mov eax, edx
0046c14e  e853aefeff               call 0x456fa6
0046c153  ebd3                     jmp 0x46c128
0046c155  31db                     xor ebx, ebx
0046c157  eb0a                     jmp 0x46c163
0046c159  31c0                     xor eax, eax
0046c15b  88d8                     mov al, bl
0046c15d  e88db4fdff               call 0x4475ef
0046c162  43                       inc ebx
0046c163  31c0                     xor eax, eax
0046c165  6689d8                   mov ax, bx
0046c168  83f804                   cmp eax, 4
0046c16b  7cec                     jl 0x46c159
