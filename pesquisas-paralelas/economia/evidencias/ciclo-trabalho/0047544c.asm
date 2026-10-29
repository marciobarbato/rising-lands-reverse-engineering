; MineGetIndice; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047544c  53                       push ebx
0047544d  51                       push ecx
0047544e  52                       push edx
0047544f  56                       push esi
00475450  89c1                     mov ecx, eax
00475452  31db                     xor ebx, ebx
00475454  eb01                     jmp 0x475457
00475456  43                       inc ebx
00475457  31c0                     xor eax, eax
00475459  6689d8                   mov ax, bx
0047545c  83f814                   cmp eax, 0x14
0047545f  7d3c                     jge 0x47549d
00475461  c1e002                   shl eax, 2
00475464  31d2                     xor edx, edx
00475466  668b9054995000           mov dx, word ptr [eax + 0x509954]
0047546d  85d2                     test edx, edx
0047546f  74e5                     je 0x475456
00475471  6639d1                   cmp cx, dx
00475474  7420                     je 0x475496
00475476  31c0                     xor eax, eax
00475478  8d7201                   lea esi, [edx + 1]
0047547b  6689c8                   mov ax, cx
0047547e  39c6                     cmp esi, eax
00475480  7414                     je 0x475496
00475482  8db200010000             lea esi, [edx + 0x100]
00475488  39c6                     cmp esi, eax
0047548a  740a                     je 0x475496
0047548c  81c201010000             add edx, 0x101
00475492  39c2                     cmp edx, eax
00475494  75c0                     jne 0x475456
00475496  89d8                     mov eax, ebx
00475498  5e                       pop esi
00475499  5a                       pop edx
0047549a  59                       pop ecx
0047549b  5b                       pop ebx
0047549c  c3                       ret
0047549d  b8ffff0000               mov eax, 0xffff
004754a2  5e                       pop esi
004754a3  5a                       pop edx
004754a4  59                       pop ecx
004754a5  5b                       pop ebx
004754a6  c3                       ret
