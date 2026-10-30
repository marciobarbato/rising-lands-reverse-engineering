; MiniMapRecentre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046a01b  53                       push ebx
0046a01c  51                       push ecx
0046a01d  52                       push edx
0046a01e  56                       push esi
0046a01f  57                       push edi
0046a020  8b158d8f5000             mov edx, dword ptr [0x508f8d]
0046a026  31c0                     xor eax, eax
0046a028  c1fa18                   sar edx, 0x18
0046a02b  66a1687d5000             mov ax, word ptr [0x507d68]
0046a031  c1e205                   shl edx, 5
0046a034  39d0                     cmp eax, edx
0046a036  7d13                     jge 0x46a04b
0046a038  660fbe05908f5000         movsx ax, byte ptr [0x508f90]
0046a040  c1e005                   shl eax, 5
0046a043  66a3687d5000             mov word ptr [0x507d68], ax
0046a049  eb4a                     jmp 0x46a095
0046a04b  31db                     xor ebx, ebx
0046a04d  668b1d24875000           mov bx, word ptr [0x508724]
0046a054  c1e305                   shl ebx, 5
0046a057  29d3                     sub ebx, edx
0046a059  31d2                     xor edx, edx
0046a05b  668b15e06f4900           mov dx, word ptr [0x496fe0]
0046a062  01d0                     add eax, edx
0046a064  83c002                   add eax, 2
0046a067  39d8                     cmp eax, ebx
0046a069  7e2a                     jle 0x46a095
0046a06b  668b1524875000           mov dx, word ptr [0x508724]
0046a072  660fbe05908f5000         movsx ax, byte ptr [0x508f90]
0046a07a  c1e205                   shl edx, 5
0046a07d  c1e005                   shl eax, 5
0046a080  668b1de06f4900           mov bx, word ptr [0x496fe0]
0046a087  29c2                     sub edx, eax
0046a089  29da                     sub edx, ebx
0046a08b  83ea02                   sub edx, 2
0046a08e  668915687d5000           mov word ptr [0x507d68], dx
0046a095  8b158d8f5000             mov edx, dword ptr [0x508f8d]
0046a09b  31c0                     xor eax, eax
0046a09d  c1fa18                   sar edx, 0x18
0046a0a0  66a16a7d5000             mov ax, word ptr [0x507d6a]
0046a0a6  c1e205                   shl edx, 5
0046a0a9  39d0                     cmp eax, edx
0046a0ab  7d13                     jge 0x46a0c0
0046a0ad  660fbe05908f5000         movsx ax, byte ptr [0x508f90]
0046a0b5  c1e005                   shl eax, 5
0046a0b8  66a36a7d5000             mov word ptr [0x507d6a], ax
0046a0be  eb4a                     jmp 0x46a10a
0046a0c0  31db                     xor ebx, ebx
0046a0c2  668b1d26875000           mov bx, word ptr [0x508726]
0046a0c9  c1e305                   shl ebx, 5
0046a0cc  29d3                     sub ebx, edx
0046a0ce  31d2                     xor edx, edx
0046a0d0  668b15e26f4900           mov dx, word ptr [0x496fe2]
0046a0d7  01d0                     add eax, edx
0046a0d9  83c002                   add eax, 2
0046a0dc  39d8                     cmp eax, ebx
0046a0de  7e2a                     jle 0x46a10a
0046a0e0  668b1526875000           mov dx, word ptr [0x508726]
0046a0e7  660fbe05908f5000         movsx ax, byte ptr [0x508f90]
0046a0ef  c1e205                   shl edx, 5
0046a0f2  c1e005                   shl eax, 5
0046a0f5  668b0de26f4900           mov cx, word ptr [0x496fe2]
0046a0fc  29c2                     sub edx, eax
0046a0fe  29ca                     sub edx, ecx
0046a100  83ea02                   sub edx, 2
0046a103  6689156a7d5000           mov word ptr [0x507d6a], dx
0046a10a  31d2                     xor edx, edx
0046a10c  31c0                     xor eax, eax
0046a10e  668b1520875000           mov dx, word ptr [0x508720]
0046a115  66a124875000             mov ax, word ptr [0x508724]
0046a11b  01c2                     add edx, eax
0046a11d  31c0                     xor eax, eax
0046a11f  66a168714900             mov ax, word ptr [0x497168]
0046a125  39c2                     cmp edx, eax
0046a127  7c28                     jl 0x46a151
0046a129  66a120875000             mov ax, word ptr [0x508720]
0046a12f  668b3524875000           mov si, word ptr [0x508724]
0046a136  668b3d68714900           mov di, word ptr [0x497168]
0046a13d  01f0                     add eax, esi
0046a13f  668b1520875000           mov dx, word ptr [0x508720]
0046a146  29f8                     sub eax, edi
0046a148  29c2                     sub edx, eax
0046a14a  66891520875000           mov word ptr [0x508720], dx
0046a151  31d2                     xor edx, edx
0046a153  31c0                     xor eax, eax
0046a155  668b1522875000           mov dx, word ptr [0x508722]
0046a15c  66a126875000             mov ax, word ptr [0x508726]
0046a162  01c2                     add edx, eax
0046a164  31c0                     xor eax, eax
0046a166  66a16a714900             mov ax, word ptr [0x49716a]
0046a16c  39c2                     cmp edx, eax
0046a16e  7c28                     jl 0x46a198
0046a170  66a122875000             mov ax, word ptr [0x508722]
0046a176  668b1d26875000           mov bx, word ptr [0x508726]
0046a17d  668b0d6a714900           mov cx, word ptr [0x49716a]
0046a184  01d8                     add eax, ebx
0046a186  668b3522875000           mov si, word ptr [0x508722]
0046a18d  29c8                     sub eax, ecx
0046a18f  29c6                     sub esi, eax
0046a191  66893522875000           mov word ptr [0x508722], si
0046a198  5f                       pop edi
0046a199  5e                       pop esi
0046a19a  5a                       pop edx
0046a19b  59                       pop ecx
0046a19c  5b                       pop ebx
0046a19d  c3                       ret
