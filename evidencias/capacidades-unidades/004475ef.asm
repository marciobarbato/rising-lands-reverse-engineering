; EnginResetCapacite; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004475ef  53                       push ebx
004475f0  51                       push ecx
004475f1  52                       push edx
004475f2  56                       push esi
004475f3  57                       push edi
004475f4  83ec04                   sub esp, 4
004475f7  880424                   mov byte ptr [esp], al
004475fa  31c9                     xor ecx, ecx
004475fc  eb48                     jmp 0x447646
004475fe  30c0                     xor al, al
00447600  84c0                     test al, al
00447602  7441                     je 0x447645
00447604  31c0                     xor eax, eax
00447606  6689c8                   mov ax, cx
00447609  69c014010000             imul eax, eax, 0x114
0044760f  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00447615  01d8                     add eax, ebx
00447617  8a1424                   mov dl, byte ptr [esp]
0044761a  3a10                     cmp dl, byte ptr [eax]
0044761c  7527                     jne 0x447645
0044761e  8d700a                   lea esi, [eax + 0xa]
00447621  31db                     xor ebx, ebx
00447623  8a4001                   mov al, byte ptr [eax + 1]
00447626  88c3                     mov bl, al
00447628  89d8                     mov eax, ebx
0044762a  e87dffffff               call 0x4475ac
0044762f  89c7                     mov edi, eax
00447631  31c0                     xor eax, eax
00447633  88d0                     mov al, dl
00447635  ba01000000               mov edx, 1
0044763a  e88116feff               call 0x428cc0
0044763f  01f8                     add eax, edi
00447641  66894602                 mov word ptr [esi + 2], ax
00447645  41                       inc ecx
00447646  31c0                     xor eax, eax
00447648  6689c8                   mov ax, cx
0044764b  3d20030000               cmp eax, 0x320
00447650  0f8dff96ffff             jge 0x440d55
00447656  69c014010000             imul eax, eax, 0x114
0044765c  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00447662  8a440302                 mov al, byte ptr [ebx + eax + 2]
00447666  25ff000000               and eax, 0xff
0044766b  7491                     je 0x4475fe
0044766d  83f804                   cmp eax, 4
00447670  748c                     je 0x4475fe
00447672  b001                     mov al, 1
00447674  eb8a                     jmp 0x447600
