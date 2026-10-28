; MissionLoad_reset_prefix; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c2cf  53                       push ebx
0046c2d0  51                       push ecx
0046c2d1  52                       push edx
0046c2d2  56                       push esi
0046c2d3  57                       push edi
0046c2d4  81ec2c010000             sub esp, 0x12c
0046c2da  a0e46f4900               mov al, byte ptr [0x496fe4]
0046c2df  8d942400010000           lea edx, [esp + 0x100]
0046c2e6  88842428010000           mov byte ptr [esp + 0x128], al
0046c2ed  31c0                     xor eax, eax
0046c2ef  be94955000               mov esi, 0x509594
0046c2f4  8a842428010000           mov al, byte ptr [esp + 0x128]
0046c2fb  89e7                     mov edi, esp
0046c2fd  e8b6feffff               call 0x46c1b8
0046c302  57                       push edi
0046c303  8a06                     mov al, byte ptr [esi]
0046c305  8807                     mov byte ptr [edi], al
0046c307  3c00                     cmp al, 0
0046c309  7410                     je 0x46c31b
0046c30b  8a4601                   mov al, byte ptr [esi + 1]
0046c30e  83c602                   add esi, 2
0046c311  884701                   mov byte ptr [edi + 1], al
0046c314  83c702                   add edi, 2
0046c317  3c00                     cmp al, 0
0046c319  75e8                     jne 0x46c303
0046c31b  5f                       pop edi
0046c31c  8db42400010000           lea esi, [esp + 0x100]
0046c323  89e7                     mov edi, esp
0046c325  baffff0000               mov edx, 0xffff
0046c32a  57                       push edi
0046c32b  2bc9                     sub ecx, ecx
0046c32d  49                       dec ecx
0046c32e  b000                     mov al, 0
0046c330  f2ae                     repne scasb al, byte ptr es:[edi]
0046c332  4f                       dec edi
0046c333  8a06                     mov al, byte ptr [esi]
0046c335  8807                     mov byte ptr [edi], al
0046c337  3c00                     cmp al, 0
0046c339  7410                     je 0x46c34b
0046c33b  8a4601                   mov al, byte ptr [esi + 1]
0046c33e  83c602                   add esi, 2
0046c341  884701                   mov byte ptr [edi + 1], al
0046c344  83c702                   add edi, 2
0046c347  3c00                     cmp al, 0
0046c349  75e8                     jne 0x46c333
0046c34b  5f                       pop edi
0046c34c  668915381a4e00           mov word ptr [0x4e1a38], dx
0046c353  6689153a1a4e00           mov word ptr [0x4e1a3a], dx
0046c35a  e83025ffff               call 0x45e88f
0046c35f  e8b1efffff               call 0x46b315
0046c364  e897dbffff               call 0x469f00
0046c369  e8eee3faff               call 0x41a75c
0046c36e  e8e652fdff               call 0x441659
0046c373  e8921c0000               call 0x46e00a
0046c378  e88bd5ffff               call 0x469908
0046c37d  e8ea57fdff               call 0x441b6c
0046c382  ba3b4b4900               mov edx, 0x494b3b
0046c387  89e0                     mov eax, esp
0046c389  e892c0feff               call 0x458420
0046c38e  84c0                     test al, al
0046c390  0f8442020000             je 0x46c5d8
