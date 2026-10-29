; DeselectionEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00472648  53                       push ebx
00472649  52                       push edx
0047264a  31db                     xor ebx, ebx
0047264c  6689c3                   mov bx, ax
0047264f  89d8                     mov eax, ebx
00472651  c1e004                   shl eax, 4
00472654  01d8                     add eax, ebx
00472656  c1e002                   shl eax, 2
00472659  8d1403                   lea edx, [ebx + eax]
0047265c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00472661  c1e202                   shl edx, 2
00472664  01d0                     add eax, edx
00472666  80b8bd00000000           cmp byte ptr [eax + 0xbd], 0
0047266d  7419                     je 0x472688
0047266f  c680bd00000000           mov byte ptr [eax + 0xbd], 0
00472676  89d8                     mov eax, ebx
00472678  31d2                     xor edx, edx
0047267a  e8c6f9fcff               call 0x442045
0047267f  88c2                     mov dl, al
00472681  89d8                     mov eax, ebx
00472683  e8eefeffff               call 0x472576
00472688  5a                       pop edx
00472689  5b                       pop ebx
0047268a  c3                       ret
