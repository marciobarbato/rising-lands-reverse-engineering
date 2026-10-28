; MessageBoxInit; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00469908  53                       push ebx
00469909  52                       push edx
0046990a  31d2                     xor edx, edx
0046990c  30e4                     xor ah, ah
0046990e  668915547d5000           mov word ptr [0x507d54], dx
00469915  668915567d5000           mov word ptr [0x507d56], dx
0046991c  8825587d5000             mov byte ptr [0x507d58], ah
00469922  8825597d5000             mov byte ptr [0x507d59], ah
00469928  30c0                     xor al, al
0046992a  eb0f                     jmp 0x46993b
0046992c  69d206020000             imul edx, edx, 0x206
00469932  30db                     xor bl, bl
00469934  40                       inc eax
00469935  889a54774e00             mov byte ptr [edx + 0x4e7754], bl
0046993b  31d2                     xor edx, edx
0046993d  6689c2                   mov dx, ax
00469940  81fa00010000             cmp edx, 0x100
00469946  7ce4                     jl 0x46992c
00469948  5a                       pop edx
00469949  5b                       pop ebx
0046994a  c3                       ret
