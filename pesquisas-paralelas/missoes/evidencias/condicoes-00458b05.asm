; LoadFinMission; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00458b05  53                       push ebx
00458b06  51                       push ecx
00458b07  52                       push edx
00458b08  83ec08                   sub esp, 8
00458b0b  31c0                     xor eax, eax
00458b0d  eb0c                     jmp 0x458b1b
00458b0f  6bca0a                   imul ecx, edx, 0xa
00458b12  b2ff                     mov dl, 0xff
00458b14  40                       inc eax
00458b15  8891201d4e00             mov byte ptr [ecx + 0x4e1d20], dl
00458b1b  31d2                     xor edx, edx
00458b1d  6689c2                   mov dx, ax
00458b20  83fa0a                   cmp edx, 0xa
00458b23  7cea                     jl 0x458b0f
00458b25  ba02000000               mov edx, 2
00458b2a  8d442404                 lea eax, [esp + 4]
00458b2e  e82ef9ffff               call 0x458461
00458b33  ba02000000               mov edx, 2
00458b38  89e0                     mov eax, esp
00458b3a  31db                     xor ebx, ebx
00458b3c  e820f9ffff               call 0x458461
00458b41  eb21                     jmp 0x458b64
00458b43  31c9                     xor ecx, ecx
00458b45  6689d9                   mov cx, bx
00458b48  6bc10a                   imul eax, ecx, 0xa
00458b4b  31d2                     xor edx, edx
00458b4d  668b1424                 mov dx, word ptr [esp]
00458b51  05201d4e00               add eax, 0x4e1d20
00458b56  e806f9ffff               call 0x458461
00458b5b  30f6                     xor dh, dh
00458b5d  43                       inc ebx
00458b5e  88b1881d4e00             mov byte ptr [ecx + 0x4e1d88], dh
00458b64  663b5c2404               cmp bx, word ptr [esp + 4]
00458b69  72d8                     jb 0x458b43
00458b6b  83c408                   add esp, 8
00458b6e  5a                       pop edx
00458b6f  59                       pop ecx
00458b70  5b                       pop ebx
00458b71  c3                       ret
