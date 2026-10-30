; EnginEstBlesse; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004420a6  53                       push ebx
004420a7  52                       push edx
004420a8  31d2                     xor edx, edx
004420aa  6689c2                   mov dx, ax
004420ad  89d0                     mov eax, edx
004420af  c1e004                   shl eax, 4
004420b2  01d0                     add eax, edx
004420b4  c1e002                   shl eax, 2
004420b7  01d0                     add eax, edx
004420b9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004420bf  c1e002                   shl eax, 2
004420c2  01c2                     add edx, eax
004420c4  31db                     xor ebx, ebx
004420c6  8a4201                   mov al, byte ptr [edx + 1]
004420c9  88c3                     mov bl, al
004420cb  89d8                     mov eax, ebx
004420cd  c1e002                   shl eax, 2
004420d0  29d8                     sub eax, ebx
004420d2  c1e003                   shl eax, 3
004420d5  01d8                     add eax, ebx
004420d7  668b1c45b6654900         mov bx, word ptr [eax*2 + 0x4965b6]
004420df  668b829a000000           mov ax, word ptr [edx + 0x9a]
004420e6  6639c3                   cmp bx, ax
004420e9  0f95c0                   setne al
004420ec  5a                       pop edx
004420ed  5b                       pop ebx
004420ee  c3                       ret
