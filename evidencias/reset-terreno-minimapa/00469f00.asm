; MiniMapReset; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00469f00  53                       push ebx
00469f01  52                       push edx
00469f02  31c0                     xor eax, eax
00469f04  31db                     xor ebx, ebx
00469f06  66a1e06f4900             mov ax, word ptr [0x496fe0]
00469f0c  668b1de26f4900           mov bx, word ptr [0x496fe2]
00469f13  0fafd8                   imul ebx, eax
00469f16  ba02000000               mov edx, 2
00469f1b  a15c7d5000               mov eax, dword ptr [0x507d5c]
00469f20  e88b240200               call 0x48c3b0
00469f25  31c0                     xor eax, eax
00469f27  31db                     xor ebx, ebx
00469f29  66a1e06f4900             mov ax, word ptr [0x496fe0]
00469f2f  668b1de26f4900           mov bx, word ptr [0x496fe2]
00469f36  0fafd8                   imul ebx, eax
00469f39  31d2                     xor edx, edx
00469f3b  a1607d5000               mov eax, dword ptr [0x507d60]
00469f40  e86b240200               call 0x48c3b0
00469f45  31c0                     xor eax, eax
00469f47  31db                     xor ebx, ebx
00469f49  66a1e06f4900             mov ax, word ptr [0x496fe0]
00469f4f  668b1de26f4900           mov bx, word ptr [0x496fe2]
00469f56  0fafd8                   imul ebx, eax
00469f59  31d2                     xor edx, edx
00469f5b  a1647d5000               mov eax, dword ptr [0x507d64]
00469f60  e84b240200               call 0x48c3b0
00469f65  5a                       pop edx
00469f66  5b                       pop ebx
00469f67  c3                       ret
