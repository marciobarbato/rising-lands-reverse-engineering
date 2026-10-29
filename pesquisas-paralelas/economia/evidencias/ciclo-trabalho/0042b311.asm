; InputGame food/stone press 0x42b311..0x42b64d; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042b311  31c0                     xor eax, eax
0042b313  8a45fc                   mov al, byte ptr [ebp - 4]
0042b316  e822720400               call 0x47253d
0042b31b  84c0                     test al, al
0042b31d  0f8431050000             je 0x42b854
0042b323  31d2                     xor edx, edx
0042b325  6689f2                   mov dx, si
0042b328  89d0                     mov eax, edx
0042b32a  e88aaf0400               call 0x4762b9
0042b32f  84c0                     test al, al
0042b331  7537                     jne 0x42b36a
0042b333  89d0                     mov eax, edx
0042b335  e8feac0400               call 0x476038
0042b33a  25ff000000               and eax, 0xff
0042b33f  83f801                   cmp eax, 1
0042b342  7426                     je 0x42b36a
0042b344  31c0                     xor eax, eax
0042b346  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b34c  3dffff0000               cmp eax, 0xffff
0042b351  0f845e010000             je 0x42b4b5
0042b357  e898f1feff               call 0x41a4f4
0042b35c  25ff000000               and eax, 0xff
0042b361  83f803                   cmp eax, 3
0042b364  0f854b010000             jne 0x42b4b5
0042b36a  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042b36e  ba01000000               mov edx, 1
0042b373  89f8                     mov eax, edi
0042b375  e815710400               call 0x47248f
0042b37a  84c0                     test al, al
0042b37c  0f8433010000             je 0x42b4b5
0042b382  31c0                     xor eax, eax
0042b384  66a1ae054e00             mov ax, word ptr [0x4e05ae]
0042b38a  83f808                   cmp eax, 8
0042b38d  0f859c000000             jne 0x42b42f
0042b393  bb03000000               mov ebx, 3
0042b398  a1848f5000               mov eax, dword ptr [0x508f84]
0042b39d  31d2                     xor edx, edx
0042b39f  f7f3                     div ebx
0042b3a1  66c70510a049003d1e       mov word ptr [0x49a010], 0x1e3d
0042b3aa  8a0dae995000             mov cl, byte ptr [0x5099ae]
0042b3b0  891514a04900             mov dword ptr [0x49a014], edx
0042b3b6  84c9                     test cl, cl
0042b3b8  0f8496040000             je 0x42b854
0042b3be  803daf99500000           cmp byte ptr [0x5099af], 0
0042b3c5  0f8489040000             je 0x42b854
0042b3cb  31c0                     xor eax, eax
0042b3cd  bf09000000               mov edi, 9
0042b3d2  6689f0                   mov ax, si
0042b3d5  66893dae054e00           mov word ptr [0x4e05ae], di
0042b3dc  e8d8ae0400               call 0x4762b9
0042b3e1  84c0                     test al, al
0042b3e3  740b                     je 0x42b3f0
0042b3e5  66c705b0054e000100       mov word ptr [0x4e05b0], 1
0042b3ee  eb31                     jmp 0x42b421
0042b3f0  31c0                     xor eax, eax
0042b3f2  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b3f8  3dffff0000               cmp eax, 0xffff
0042b3fd  7419                     je 0x42b418
0042b3ff  e8f0f0feff               call 0x41a4f4
0042b404  25ff000000               and eax, 0xff
0042b409  39d8                     cmp eax, ebx
0042b40b  750b                     jne 0x42b418
0042b40d  66c705b0054e000300       mov word ptr [0x4e05b0], 3
0042b416  eb09                     jmp 0x42b421
0042b418  66c705b0054e000200       mov word ptr [0x4e05b0], 2
0042b421  b001                     mov al, 1
0042b423  668935b2054e00           mov word ptr [0x4e05b2], si
0042b42a  e911f9ffff               jmp 0x42ad40
0042b42f  b8101e0000               mov eax, 0x1e10
0042b434  bb06000000               mov ebx, 6
0042b439  31d2                     xor edx, edx
0042b43b  66a310a04900             mov word ptr [0x49a010], ax
0042b441  a1808f5000               mov eax, dword ptr [0x508f80]
0042b446  f7f3                     div ebx
0042b448  8a1dae995000             mov bl, byte ptr [0x5099ae]
0042b44e  891514a04900             mov dword ptr [0x49a014], edx
0042b454  84db                     test bl, bl
0042b456  0f84f8030000             je 0x42b854
0042b45c  803daf99500000           cmp byte ptr [0x5099af], 0
0042b463  0f84eb030000             je 0x42b854
0042b469  31db                     xor ebx, ebx
0042b46b  6689f3                   mov bx, si
0042b46e  89d8                     mov eax, ebx
0042b470  e844ae0400               call 0x4762b9
0042b475  84c0                     test al, al
0042b477  742a                     je 0x42b4a3
0042b479  6a00                     push 0
0042b47b  ba07000000               mov edx, 7
0042b480  6a00                     push 0
0042b482  89f8                     mov eax, edi
0042b484  31c9                     xor ecx, ecx
0042b486  e849380300               call 0x45ecd4
0042b48b  bb031e0000               mov ebx, 0x1e03
0042b490  66893504624900           mov word ptr [0x496204], si
0042b497  66891dac054e00           mov word ptr [0x4e05ac], bx
0042b49e  e9b1030000               jmp 0x42b854
0042b4a3  6a00                     push 0
0042b4a5  ba12000000               mov edx, 0x12
0042b4aa  6a00                     push 0
0042b4ac  89f8                     mov eax, edi
0042b4ae  31c9                     xor ecx, ecx
0042b4b0  e9e1faffff               jmp 0x42af96
0042b4b5  31d2                     xor edx, edx
0042b4b7  6689f2                   mov dx, si
0042b4ba  89d0                     mov eax, edx
0042b4bc  e8a2ad0400               call 0x476263
0042b4c1  84c0                     test al, al
0042b4c3  7537                     jne 0x42b4fc
0042b4c5  89d0                     mov eax, edx
0042b4c7  e86cab0400               call 0x476038
0042b4cc  25ff000000               and eax, 0xff
0042b4d1  83f802                   cmp eax, 2
0042b4d4  7426                     je 0x42b4fc
0042b4d6  31c0                     xor eax, eax
0042b4d8  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b4de  3dffff0000               cmp eax, 0xffff
0042b4e3  0f8464010000             je 0x42b64d
0042b4e9  e806f0feff               call 0x41a4f4
0042b4ee  25ff000000               and eax, 0xff
0042b4f3  83f803                   cmp eax, 3
0042b4f6  0f8551010000             jne 0x42b64d
0042b4fc  0fb67dfc                 movzx edi, byte ptr [ebp - 4]
0042b500  ba02000000               mov edx, 2
0042b505  89f8                     mov eax, edi
0042b507  e8836f0400               call 0x47248f
0042b50c  84c0                     test al, al
0042b50e  0f8439010000             je 0x42b64d
0042b514  31c0                     xor eax, eax
0042b516  66a1ae054e00             mov ax, word ptr [0x4e05ae]
0042b51c  83f808                   cmp eax, 8
0042b51f  0f859f000000             jne 0x42b5c4
0042b525  bb03000000               mov ebx, 3
0042b52a  a1848f5000               mov eax, dword ptr [0x508f84]
0042b52f  31d2                     xor edx, edx
0042b531  f7f3                     div ebx
0042b533  66c70510a049003d1e       mov word ptr [0x49a010], 0x1e3d
0042b53c  8a25ae995000             mov ah, byte ptr [0x5099ae]
0042b542  891514a04900             mov dword ptr [0x49a014], edx
0042b548  84e4                     test ah, ah
0042b54a  0f8404030000             je 0x42b854
0042b550  803daf99500000           cmp byte ptr [0x5099af], 0
0042b557  0f84f7020000             je 0x42b854
0042b55d  66c705ae054e000900       mov word ptr [0x4e05ae], 9
0042b566  31c0                     xor eax, eax
0042b568  6689f0                   mov ax, si
0042b56b  e8f3ac0400               call 0x476263
0042b570  84c0                     test al, al
0042b572  740b                     je 0x42b57f
0042b574  31c9                     xor ecx, ecx
0042b576  66890db0054e00           mov word ptr [0x4e05b0], cx
0042b57d  eb31                     jmp 0x42b5b0
0042b57f  31c0                     xor eax, eax
0042b581  66a1c46a4900             mov ax, word ptr [0x496ac4]
0042b587  3dffff0000               cmp eax, 0xffff
0042b58c  7419                     je 0x42b5a7
0042b58e  e861effeff               call 0x41a4f4
0042b593  25ff000000               and eax, 0xff
0042b598  39d8                     cmp eax, ebx
0042b59a  750b                     jne 0x42b5a7
0042b59c  66c705b0054e000300       mov word ptr [0x4e05b0], 3
0042b5a5  eb09                     jmp 0x42b5b0
0042b5a7  66c705b0054e000200       mov word ptr [0x4e05b0], 2
0042b5b0  b602                     mov dh, 2
0042b5b2  668935b2054e00           mov word ptr [0x4e05b2], si
0042b5b9  8835b4054e00             mov byte ptr [0x4e05b4], dh
0042b5bf  e990020000               jmp 0x42b854
0042b5c4  bb101e0000               mov ebx, 0x1e10
0042b5c9  a1808f5000               mov eax, dword ptr [0x508f80]
0042b5ce  31d2                     xor edx, edx
0042b5d0  66891d10a04900           mov word ptr [0x49a010], bx
0042b5d7  bb06000000               mov ebx, 6
0042b5dc  f7f3                     div ebx
0042b5de  8a2dae995000             mov ch, byte ptr [0x5099ae]
0042b5e4  891514a04900             mov dword ptr [0x49a014], edx
0042b5ea  84ed                     test ch, ch
0042b5ec  0f8462020000             je 0x42b854
0042b5f2  803daf99500000           cmp byte ptr [0x5099af], 0
0042b5f9  0f8455020000             je 0x42b854
0042b5ff  31db                     xor ebx, ebx
0042b601  6689f3                   mov bx, si
0042b604  89d8                     mov eax, ebx
0042b606  e8a6b00400               call 0x4766b1
0042b60b  84c0                     test al, al
0042b60d  7427                     je 0x42b636
0042b60f  6a00                     push 0
0042b611  ba12000000               mov edx, 0x12
0042b616  6a00                     push 0
0042b618  89f8                     mov eax, edi
0042b61a  31c9                     xor ecx, ecx
0042b61c  e8b3360300               call 0x45ecd4
0042b621  66893504624900           mov word ptr [0x496204], si
0042b628  66c705ac054e00031e       mov word ptr [0x4e05ac], 0x1e03
0042b631  e91e020000               jmp 0x42b854
0042b636  6a00                     push 0
0042b638  ba06000000               mov edx, 6
0042b63d  31c0                     xor eax, eax
0042b63f  6a00                     push 0
0042b641  31c9                     xor ecx, ecx
0042b643  a041805000               mov al, byte ptr [0x508041]
0042b648  e941f7ffff               jmp 0x42ad8e
