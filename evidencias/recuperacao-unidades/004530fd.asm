; EnginResetFatigue; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004530fd  52                       push edx
004530fe  31d2                     xor edx, edx
00453100  6689c2                   mov dx, ax
00453103  89d0                     mov eax, edx
00453105  c1e004                   shl eax, 4
00453108  01d0                     add eax, edx
0045310a  c1e002                   shl eax, 2
0045310d  01c2                     add edx, eax
0045310f  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00453114  c1e202                   shl edx, 2
00453117  01d0                     add eax, edx
00453119  66c740740000             mov word ptr [eax + 0x74], 0
0045311f  668b5076                 mov dx, word ptr [eax + 0x76]
00453123  66895004                 mov word ptr [eax + 4], dx
00453127  5a                       pop edx
00453128  c3                       ret
