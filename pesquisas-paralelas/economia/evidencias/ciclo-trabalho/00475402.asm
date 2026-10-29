; MineEstSurTerrain; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00475402  52                       push edx
00475403  89c2                     mov edx, eax
00475405  81e2ffff0000             and edx, 0xffff
0047540b  a1707d5000               mov eax, dword ptr [0x507d70]
00475410  01d2                     add edx, edx
00475412  668b0402                 mov ax, word ptr [edx + eax]
00475416  25ffff0000               and eax, 0xffff
0047541b  3d53020000               cmp eax, 0x253
00475420  7407                     je 0x475429
00475422  3d54020000               cmp eax, 0x254
00475427  7504                     jne 0x47542d
00475429  b001                     mov al, 1
0047542b  5a                       pop edx
0047542c  c3                       ret
0047542d  30c0                     xor al, al
0047542f  5a                       pop edx
00475430  c3                       ret
