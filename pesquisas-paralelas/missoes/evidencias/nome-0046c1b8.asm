; MakeMissionName; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c1b8  53                       push ebx
0046c1b9  51                       push ecx
0046c1ba  56                       push esi
0046c1bb  57                       push edi
0046c1bc  55                       push ebp
0046c1bd  83ec14                   sub esp, 0x14
0046c1c0  88442410                 mov byte ptr [esp + 0x10], al
0046c1c4  89d5                     mov ebp, edx
0046c1c6  89e7                     mov edi, esp
0046c1c8  be54714900               mov esi, 0x497154
0046c1cd  a5                       movsd dword ptr es:[edi], dword ptr [esi]
0046c1ce  a5                       movsd dword ptr es:[edi], dword ptr [esi]
0046c1cf  a5                       movsd dword ptr es:[edi], dword ptr [esi]
0046c1d0  a5                       movsd dword ptr es:[edi], dword ptr [esi]
0046c1d1  31db                     xor ebx, ebx
0046c1d3  be274b4900               mov esi, 0x494b27
0046c1d8  89d7                     mov edi, edx
0046c1da  8a5c2410                 mov bl, byte ptr [esp + 0x10]
0046c1de  57                       push edi
0046c1df  8a06                     mov al, byte ptr [esi]
0046c1e1  8807                     mov byte ptr [edi], al
0046c1e3  3c00                     cmp al, 0
0046c1e5  7410                     je 0x46c1f7
0046c1e7  8a4601                   mov al, byte ptr [esi + 1]
0046c1ea  83c602                   add esi, 2
0046c1ed  884701                   mov byte ptr [edi + 1], al
0046c1f0  83c702                   add edi, 2
0046c1f3  3c00                     cmp al, 0
0046c1f5  75e8                     jne 0x46c1df
0046c1f7  5f                       pop edi
0046c1f8  be0a000000               mov esi, 0xa
0046c1fd  89da                     mov edx, ebx
0046c1ff  89d8                     mov eax, ebx
0046c201  c1fa1f                   sar edx, 0x1f
0046c204  f7fe                     idiv esi
0046c206  89da                     mov edx, ebx
0046c208  83c030                   add eax, 0x30
0046c20b  c1fa1f                   sar edx, 0x1f
0046c20e  88450c                   mov byte ptr [ebp + 0xc], al
0046c211  89d8                     mov eax, ebx
0046c213  f7fe                     idiv esi
0046c215  b15a                     mov cl, 0x5a
0046c217  83c230                   add edx, 0x30
0046c21a  b501                     mov ch, 1
0046c21c  88550d                   mov byte ptr [ebp + 0xd], dl
0046c21f  80fb0a                   cmp bl, 0xa
0046c222  0f8270000000             jb 0x46c298
0046c228  7640                     jbe 0x46c26a
0046c22a  80fb0c                   cmp bl, 0xc
0046c22d  0f826a000000             jb 0x46c29d
0046c233  7635                     jbe 0x46c26a
0046c235  80fb11                   cmp bl, 0x11
0046c238  7430                     je 0x46c26a
0046c23a  eb61                     jmp 0x46c29d
0046c23c  31c0                     xor eax, eax
0046c23e  a0851d4e00               mov al, byte ptr [0x4e1d85]
0046c243  8b3484                   mov esi, dword ptr [esp + eax*4]
0046c246  57                       push edi
0046c247  2bc9                     sub ecx, ecx
0046c249  49                       dec ecx
0046c24a  b000                     mov al, 0
0046c24c  f2ae                     repne scasb al, byte ptr es:[edi]
0046c24e  4f                       dec edi
0046c24f  8a06                     mov al, byte ptr [esi]
0046c251  8807                     mov byte ptr [edi], al
0046c253  3c00                     cmp al, 0
0046c255  7410                     je 0x46c267
0046c257  8a4601                   mov al, byte ptr [esi + 1]
0046c25a  83c602                   add esi, 2
0046c25d  884701                   mov byte ptr [edi + 1], al
0046c260  83c702                   add edi, 2
0046c263  3c00                     cmp al, 0
0046c265  75e8                     jne 0x46c24f
0046c267  5f                       pop edi
0046c268  eb33                     jmp 0x46c29d
0046c26a  bb01000000               mov ebx, 1
0046c26f  eb06                     jmp 0x46c277
0046c271  43                       inc ebx
0046c272  83fb04                   cmp ebx, 4
0046c275  7d15                     jge 0x46c28c
0046c277  31c0                     xor eax, eax
0046c279  31d2                     xor edx, edx
0046c27b  88d8                     mov al, bl
0046c27d  e8ea190000               call 0x46dc6c
0046c282  38c1                     cmp cl, al
0046c284  7eeb                     jle 0x46c271
0046c286  88c1                     mov cl, al
0046c288  88dd                     mov ch, bl
0046c28a  ebe5                     jmp 0x46c271
0046c28c  31c0                     xor eax, eax
0046c28e  88e8                     mov al, ch
0046c290  89ef                     mov edi, ebp
0046c292  8b7484fc                 mov esi, dword ptr [esp + eax*4 - 4]
0046c296  ebae                     jmp 0x46c246
0046c298  80fb09                   cmp bl, 9
0046c29b  749f                     je 0x46c23c
0046c29d  be364b4900               mov esi, 0x494b36
0046c2a2  89ef                     mov edi, ebp
0046c2a4  57                       push edi
0046c2a5  2bc9                     sub ecx, ecx
0046c2a7  49                       dec ecx
0046c2a8  b000                     mov al, 0
0046c2aa  f2ae                     repne scasb al, byte ptr es:[edi]
0046c2ac  4f                       dec edi
0046c2ad  8a06                     mov al, byte ptr [esi]
0046c2af  8807                     mov byte ptr [edi], al
0046c2b1  3c00                     cmp al, 0
0046c2b3  7410                     je 0x46c2c5
0046c2b5  8a4601                   mov al, byte ptr [esi + 1]
0046c2b8  83c602                   add esi, 2
0046c2bb  884701                   mov byte ptr [edi + 1], al
0046c2be  83c702                   add edi, 2
0046c2c1  3c00                     cmp al, 0
0046c2c3  75e8                     jne 0x46c2ad
0046c2c5  5f                       pop edi
0046c2c6  83c414                   add esp, 0x14
0046c2c9  5d                       pop ebp
0046c2ca  5f                       pop edi
0046c2cb  5e                       pop esi
0046c2cc  59                       pop ecx
0046c2cd  5b                       pop ebx
0046c2ce  c3                       ret
