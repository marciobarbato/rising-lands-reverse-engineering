; MissionLoadName_reset_prefix; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c5e3  53                       push ebx
0046c5e4  51                       push ecx
0046c5e5  52                       push edx
0046c5e6  56                       push esi
0046c5e7  57                       push edi
0046c5e8  55                       push ebp
0046c5e9  81ec14010000             sub esp, 0x114
0046c5ef  50                       push eax
0046c5f0  bd00000100               mov ebp, 0x10000
0046c5f5  baffff0000               mov edx, 0xffff
0046c5fa  31c9                     xor ecx, ecx
0046c5fc  668915381a4e00           mov word ptr [0x4e1a38], dx
0046c603  6689153a1a4e00           mov word ptr [0x4e1a3a], dx
0046c60a  e88022ffff               call 0x45e88f
0046c60f  e801edffff               call 0x46b315
0046c614  e8e7d8ffff               call 0x469f00
0046c619  e83ee1faff               call 0x41a75c
0046c61e  e83650fdff               call 0x441659
0046c623  e8e2190000               call 0x46e00a
0046c628  e8dbd2ffff               call 0x469908
0046c62d  eb1c                     jmp 0x46c64b
0046c62f  31db                     xor ebx, ebx
0046c631  6689cb                   mov bx, cx
0046c634  6bdb1a                   imul ebx, ebx, 0x1a
0046c637  40                       inc eax
0046c638  c6841a34194e0000         mov byte ptr [edx + ebx + 0x4e1934], 0
0046c640  31d2                     xor edx, edx
0046c642  6689c2                   mov dx, ax
0046c645  83fa1a                   cmp edx, 0x1a
0046c648  7ce5                     jl 0x46c62f
0046c64a  41                       inc ecx
0046c64b  31c0                     xor eax, eax
0046c64d  6689c8                   mov ax, cx
0046c650  83f804                   cmp eax, 4
0046c653  7d04                     jge 0x46c659
0046c655  31c8                     xor eax, ecx
0046c657  ebe7                     jmp 0x46c640
0046c659  30c9                     xor cl, cl
0046c65b  eb1d                     jmp 0x46c67a
0046c65d  31db                     xor ebx, ebx
0046c65f  88cb                     mov bl, cl
0046c661  6bdb16                   imul ebx, ebx, 0x16
0046c664  30ed                     xor ch, ch
0046c666  40                       inc eax
0046c667  88ac1ad4fa4d00           mov byte ptr [edx + ebx + 0x4dfad4], ch
0046c66e  31d2                     xor edx, edx
0046c670  6689c2                   mov dx, ax
0046c673  83fa16                   cmp edx, 0x16
0046c676  7ce5                     jl 0x46c65d
0046c678  fec1                     inc cl
0046c67a  31c0                     xor eax, eax
0046c67c  88c8                     mov al, cl
0046c67e  83f804                   cmp eax, 4
0046c681  7d04                     jge 0x46c687
0046c683  31c0                     xor eax, eax
0046c685  ebe7                     jmp 0x46c66e
0046c687  e866830000               call 0x4749f2
0046c68c  e8b5440000               call 0x470b46
0046c691  e8da4dfdff               call 0x441470
0046c696  c605e46f490032           mov byte ptr [0x496fe4], 0x32
0046c69d  e80efdfbff               call 0x42c3b0
0046c6a2  84c0                     test al, al
0046c6a4  740a                     je 0x46c6b0
0046c6a6  e853500000               call 0x4716fe
0046c6ab  e8404e0000               call 0x4714f0
0046c6b0  e8b754fdff               call 0x441b6c
0046c6b5  8b3c24                   mov edi, dword ptr [esp]
0046c6b8  8b1424                   mov edx, dword ptr [esp]
0046c6bb  29c9                     sub ecx, ecx
0046c6bd  49                       dec ecx
0046c6be  31c0                     xor eax, eax
0046c6c0  f2ae                     repne scasb al, byte ptr es:[edi]
0046c6c2  f7d1                     not ecx
0046c6c4  49                       dec ecx
0046c6c5  8d41fc                   lea eax, [ecx - 4]
0046c6c8  01d0                     add eax, edx
0046c6ca  ba3e4b4900               mov edx, 0x494b3e
0046c6cf  e88d0e0200               call 0x48d561
0046c6d4  85c0                     test eax, eax
0046c6d6  7507                     jne 0x46c6df
0046c6d8  be94945000               mov esi, 0x509494
0046c6dd  eb05                     jmp 0x46c6e4
0046c6df  be94955000               mov esi, 0x509594
0046c6e4  8d7c2404                 lea edi, [esp + 4]
0046c6e8  57                       push edi
0046c6e9  8a06                     mov al, byte ptr [esi]
0046c6eb  8807                     mov byte ptr [edi], al
0046c6ed  3c00                     cmp al, 0
0046c6ef  7410                     je 0x46c701
0046c6f1  8a4601                   mov al, byte ptr [esi + 1]
0046c6f4  83c602                   add esi, 2
0046c6f7  884701                   mov byte ptr [edi + 1], al
0046c6fa  83c702                   add edi, 2
0046c6fd  3c00                     cmp al, 0
0046c6ff  75e8                     jne 0x46c6e9
0046c701  5f                       pop edi
0046c702  be434b4900               mov esi, 0x494b43
0046c707  8d7c2404                 lea edi, [esp + 4]
0046c70b  57                       push edi
0046c70c  2bc9                     sub ecx, ecx
0046c70e  49                       dec ecx
0046c70f  b000                     mov al, 0
0046c711  f2ae                     repne scasb al, byte ptr es:[edi]
0046c713  4f                       dec edi
0046c714  8a06                     mov al, byte ptr [esi]
0046c716  8807                     mov byte ptr [edi], al
0046c718  3c00                     cmp al, 0
0046c71a  7410                     je 0x46c72c
0046c71c  8a4601                   mov al, byte ptr [esi + 1]
0046c71f  83c602                   add esi, 2
0046c722  884701                   mov byte ptr [edi + 1], al
0046c725  83c702                   add edi, 2
0046c728  3c00                     cmp al, 0
0046c72a  75e8                     jne 0x46c714
0046c72c  5f                       pop edi
0046c72d  8b3424                   mov esi, dword ptr [esp]
0046c730  8d7c2404                 lea edi, [esp + 4]
0046c734  ba4b4b4900               mov edx, 0x494b4b
0046c739  57                       push edi
0046c73a  2bc9                     sub ecx, ecx
0046c73c  49                       dec ecx
0046c73d  b000                     mov al, 0
0046c73f  f2ae                     repne scasb al, byte ptr es:[edi]
0046c741  4f                       dec edi
0046c742  8a06                     mov al, byte ptr [esi]
0046c744  8807                     mov byte ptr [edi], al
0046c746  3c00                     cmp al, 0
0046c748  7410                     je 0x46c75a
0046c74a  8a4601                   mov al, byte ptr [esi + 1]
0046c74d  83c602                   add esi, 2
0046c750  884701                   mov byte ptr [edi + 1], al
0046c753  83c702                   add edi, 2
0046c756  3c00                     cmp al, 0
0046c758  75e8                     jne 0x46c742
0046c75a  5f                       pop edi
0046c75b  8d442404                 lea eax, [esp + 4]
0046c75f  e8bcbcfeff               call 0x458420
0046c764  84c0                     test al, al
0046c766  0f842e020000             je 0x46c99a
