; EnginEstMiroir; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044fffe  52                       push edx
0044ffff  31d2                     xor edx, edx
00450001  6689c2                   mov dx, ax
00450004  89d0                     mov eax, edx
00450006  c1e004                   shl eax, 4
00450009  01d0                     add eax, edx
0045000b  c1e002                   shl eax, 2
0045000e  01d0                     add eax, edx
00450010  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00450016  8a8482dc000000           mov al, byte ptr [edx + eax*4 + 0xdc]
0045001d  ba02000000               mov edx, 2
00450022  25ff000000               and eax, 0xff
00450027  e86b7d0100               call 0x467d97
0045002c  5a                       pop edx
0045002d  c3                       ret
