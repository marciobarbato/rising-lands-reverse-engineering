; Engin_RetrieveExperimente (translated); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441623  53                       push ebx
00441624  51                       push ecx
00441625  52                       push edx
00441626  56                       push esi
00441627  be0a000000               mov esi, 0xa
0044162c  31c9                     xor ecx, ecx
0044162e  eb0d                     jmp 0x44163d
00441630  41                       inc ecx
00441631  83c60a                   add esi, 0xa
00441634  83f904                   cmp ecx, 4
00441637  0f8d1cf7ffff             jge 0x440d59
0044163d  89f3                     mov ebx, esi
0044163f  6bc10a                   imul eax, ecx, 0xa
00441642  83c002                   add eax, 2
00441645  668b90ea194e00           mov dx, word ptr [eax + 0x4e19ea]
0044164c  668990c2194e00           mov word ptr [eax + 0x4e19c2], dx
00441653  39d8                     cmp eax, ebx
00441655  74d9                     je 0x441630
00441657  ebe9                     jmp 0x441642
