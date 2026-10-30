; MiniMapSetPos; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046a19e  53                       push ebx
0046a19f  51                       push ecx
0046a1a0  6603056c7d5000           add ax, word ptr [0x507d6c]
0046a1a7  668b0d6e7d5000           mov cx, word ptr [0x507d6e]
0046a1ae  0fbfd8                   movsx ebx, ax
0046a1b1  01ca                     add edx, ecx
0046a1b3  85db                     test ebx, ebx
0046a1b5  7d02                     jge 0x46a1b9
0046a1b7  31c0                     xor eax, eax
0046a1b9  66a3687d5000             mov word ptr [0x507d68], ax
0046a1bf  0fbfc2                   movsx eax, dx
0046a1c2  85c0                     test eax, eax
0046a1c4  7d02                     jge 0x46a1c8
0046a1c6  31d2                     xor edx, edx
0046a1c8  6689156a7d5000           mov word ptr [0x507d6a], dx
0046a1cf  e847feffff               call 0x46a01b
0046a1d4  59                       pop ecx
0046a1d5  5b                       pop ebx
0046a1d6  c3                       ret
