; EnginBombeEstMax; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044841b  52                       push edx
0044841c  31d2                     xor edx, edx
0044841e  6689c2                   mov dx, ax
00448421  89d0                     mov eax, edx
00448423  c1e004                   shl eax, 4
00448426  01d0                     add eax, edx
00448428  c1e002                   shl eax, 2
0044842b  01d0                     add eax, edx
0044842d  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00448433  8a8482da000000           mov al, byte ptr [edx + eax*4 + 0xda]
0044843a  25ff000000               and eax, 0xff
0044843f  83f805                   cmp eax, 5
00448442  0f94c0                   sete al
00448445  5a                       pop edx
00448446  c3                       ret
