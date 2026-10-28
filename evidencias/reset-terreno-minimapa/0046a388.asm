; SetMiniMap; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046a388  51                       push ecx
0046a389  56                       push esi
0046a38a  57                       push edi
0046a38b  55                       push ebp
0046a38c  83ec28                   sub esp, 0x28
0046a38f  88442424                 mov byte ptr [esp + 0x24], al
0046a393  8854241c                 mov byte ptr [esp + 0x1c], dl
0046a397  89de                     mov esi, ebx
0046a399  31c9                     xor ecx, ecx
0046a39b  6689d9                   mov cx, bx
0046a39e  bb00010000               mov ebx, 0x100
0046a3a3  89ca                     mov edx, ecx
0046a3a5  89c8                     mov eax, ecx
0046a3a7  c1fa1f                   sar edx, 0x1f
0046a3aa  f7fb                     idiv ebx
0046a3ac  89d3                     mov ebx, edx
0046a3ae  89ca                     mov edx, ecx
0046a3b0  89c8                     mov eax, ecx
0046a3b2  c1fa1f                   sar edx, 0x1f
0046a3b5  c1e208                   shl edx, 8
0046a3b8  1bc2                     sbb eax, edx
0046a3ba  c1f808                   sar eax, 8
0046a3bd  31ff                     xor edi, edi
0046a3bf  31d2                     xor edx, edx
0046a3c1  668b3de06f4900           mov di, word ptr [0x496fe0]
0046a3c8  6689da                   mov dx, bx
0046a3cb  0fafd7                   imul edx, edi
0046a3ce  0fb72d68714900           movzx ebp, word ptr [0x497168]
0046a3d5  89c1                     mov ecx, eax
0046a3d7  89d0                     mov eax, edx
0046a3d9  c1fa1f                   sar edx, 0x1f
0046a3dc  f7fd                     idiv ebp
0046a3de  31d2                     xor edx, edx
0046a3e0  6689ca                   mov dx, cx
0046a3e3  31c9                     xor ecx, ecx
0046a3e5  668b0de26f4900           mov cx, word ptr [0x496fe2]
0046a3ec  0fafd1                   imul edx, ecx
0046a3ef  31db                     xor ebx, ebx
0046a3f1  668b1d6a714900           mov bx, word ptr [0x49716a]
0046a3f8  89442410                 mov dword ptr [esp + 0x10], eax
0046a3fc  89d0                     mov eax, edx
0046a3fe  c1fa1f                   sar edx, 0x1f
0046a401  f7fb                     idiv ebx
0046a403  89442414                 mov dword ptr [esp + 0x14], eax
0046a407  89fa                     mov edx, edi
0046a409  89f8                     mov eax, edi
0046a40b  c1fa1f                   sar edx, 0x1f
0046a40e  f7fd                     idiv ebp
0046a410  89442404                 mov dword ptr [esp + 4], eax
0046a414  89ca                     mov edx, ecx
0046a416  89c8                     mov eax, ecx
0046a418  c1fa1f                   sar edx, 0x1f
0046a41b  f7fb                     idiv ebx
0046a41d  8944240c                 mov dword ptr [esp + 0xc], eax
0046a421  31c0                     xor eax, eax
0046a423  668b442404               mov ax, word ptr [esp + 4]
0046a428  85c0                     test eax, eax
0046a42a  7508                     jne 0x46a434
0046a42c  c744240401000000         mov dword ptr [esp + 4], 1
0046a434  31c0                     xor eax, eax
0046a436  668b44240c               mov ax, word ptr [esp + 0xc]
0046a43b  85c0                     test eax, eax
0046a43d  7508                     jne 0x46a447
0046a43f  c744240c01000000         mov dword ptr [esp + 0xc], 1
0046a447  8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0046a44b  660faf1de26f4900         imul bx, word ptr [0x496fe2]
0046a453  31c0                     xor eax, eax
0046a455  8b542404                 mov edx, dword ptr [esp + 4]
0046a459  890424                   mov dword ptr [esp], eax
0046a45c  b880000000               mov eax, 0x80
0046a461  29d0                     sub eax, edx
0046a463  89442418                 mov dword ptr [esp + 0x18], eax
0046a467  8a44241c                 mov al, byte ptr [esp + 0x1c]
0046a46b  8b7c2410                 mov edi, dword ptr [esp + 0x10]
0046a46f  fec8                     dec al
0046a471  01fb                     add ebx, edi
0046a473  88442420                 mov byte ptr [esp + 0x20], al
0046a477  eb0d                     jmp 0x46a486
0046a479  8b3c24                   mov edi, dword ptr [esp]
0046a47c  8b4c2418                 mov ecx, dword ptr [esp + 0x18]
0046a480  47                       inc edi
0046a481  01cb                     add ebx, ecx
0046a483  893c24                   mov dword ptr [esp], edi
0046a486  8b0424                   mov eax, dword ptr [esp]
0046a489  663b44240c               cmp ax, word ptr [esp + 0xc]
0046a48e  0f8370020000             jae 0x46a704
0046a494  31ff                     xor edi, edi
0046a496  897c2408                 mov dword ptr [esp + 8], edi
0046a49a  e984010000               jmp 0x46a623
0046a49f  8a442424                 mov al, byte ptr [esp + 0x24]
0046a4a3  3a0541805000             cmp al, byte ptr [0x508041]
0046a4a9  0f856a010000             jne 0x46a619
0046a4af  31c0                     xor eax, eax
0046a4b1  6689f0                   mov ax, si
0046a4b4  31d2                     xor edx, edx
0046a4b6  e839c10000               call 0x4765f4
0046a4bb  88c2                     mov dl, al
0046a4bd  a1b4244e00               mov eax, dword ptr [0x4e24b4]
0046a4c2  01c2                     add edx, eax
0046a4c4  31c0                     xor eax, eax
0046a4c6  8b0d5c7d5000             mov ecx, dword ptr [0x507d5c]
0046a4cc  6689d8                   mov ax, bx
0046a4cf  8a12                     mov dl, byte ptr [edx]
0046a4d1  881401                   mov byte ptr [ecx + eax], dl
0046a4d4  e940010000               jmp 0x46a619
0046a4d9  8a442424                 mov al, byte ptr [esp + 0x24]
0046a4dd  3a0541805000             cmp al, byte ptr [0x508041]
0046a4e3  0f8530010000             jne 0x46a619
0046a4e9  31c9                     xor ecx, ecx
0046a4eb  a1607d5000               mov eax, dword ptr [0x507d60]
0046a4f0  6689d9                   mov cx, bx
0046a4f3  01c8                     add eax, ecx
0046a4f5  803800                   cmp byte ptr [eax], 0
0046a4f8  7410                     je 0x46a50a
0046a4fa  8b155c7d5000             mov edx, dword ptr [0x507d5c]
0046a500  8a00                     mov al, byte ptr [eax]
0046a502  880411                   mov byte ptr [ecx + edx], al
0046a505  e90f010000               jmp 0x46a619
0046a50a  a1647d5000               mov eax, dword ptr [0x507d64]
0046a50f  01c8                     add eax, ecx
0046a511  803800                   cmp byte ptr [eax], 0
0046a514  75e4                     jne 0x46a4fa
0046a516  31c0                     xor eax, eax
0046a518  6689f0                   mov ax, si
0046a51b  e8d4c00000               call 0x4765f4
0046a520  8b155c7d5000             mov edx, dword ptr [0x507d5c]
0046a526  ebda                     jmp 0x46a502
0046a528  8a442424                 mov al, byte ptr [esp + 0x24]
0046a52c  3a0541805000             cmp al, byte ptr [0x508041]
0046a532  0f85e1000000             jne 0x46a619
0046a538  31c0                     xor eax, eax
0046a53a  6689f0                   mov ax, si
0046a53d  31d2                     xor edx, edx
0046a53f  e8b0c00000               call 0x4765f4
0046a544  88c2                     mov dl, al
0046a546  a1b4244e00               mov eax, dword ptr [0x4e24b4]
0046a54b  01d0                     add eax, edx
0046a54d  31d2                     xor edx, edx
0046a54f  8b0d5c7d5000             mov ecx, dword ptr [0x507d5c]
0046a555  6689da                   mov dx, bx
0046a558  eba6                     jmp 0x46a500
0046a55a  31c9                     xor ecx, ecx
0046a55c  8a4c2424                 mov cl, byte ptr [esp + 0x24]
0046a560  31ff                     xor edi, edi
0046a562  89c8                     mov eax, ecx
0046a564  6689df                   mov di, bx
0046a567  e8cf5affff               call 0x46003b
0046a56c  88c2                     mov dl, al
0046a56e  a1607d5000               mov eax, dword ptr [0x507d60]
0046a573  881407                   mov byte ptr [edi + eax], dl
0046a576  31d2                     xor edx, edx
0046a578  31c0                     xor eax, eax
0046a57a  8a1541805000             mov dl, byte ptr [0x508041]
0046a580  6689f0                   mov ax, si
0046a583  e8c9c30000               call 0x476951
0046a588  84c0                     test al, al
0046a58a  0f8489000000             je 0x46a619
0046a590  89c8                     mov eax, ecx
0046a592  e8a45affff               call 0x46003b
0046a597  88c2                     mov dl, al
0046a599  a15c7d5000               mov eax, dword ptr [0x507d5c]
0046a59e  881407                   mov byte ptr [edi + eax], dl
0046a5a1  e973000000               jmp 0x46a619
0046a5a6  31ff                     xor edi, edi
0046a5a8  a1607d5000               mov eax, dword ptr [0x507d60]
0046a5ad  6689df                   mov di, bx
0046a5b0  31d2                     xor edx, edx
0046a5b2  31c9                     xor ecx, ecx
0046a5b4  c6040700                 mov byte ptr [edi + eax], 0
0046a5b8  6689f1                   mov cx, si
0046a5bb  8a1541805000             mov dl, byte ptr [0x508041]
0046a5c1  89c8                     mov eax, ecx
0046a5c3  e828c10000               call 0x4766f0
0046a5c8  84c0                     test al, al
0046a5ca  744d                     je 0x46a619
0046a5cc  31d2                     xor edx, edx
0046a5ce  89c8                     mov eax, ecx
0046a5d0  8a1541805000             mov dl, byte ptr [0x508041]
0046a5d6  e876c30000               call 0x476951
0046a5db  84c0                     test al, al
0046a5dd  741b                     je 0x46a5fa
0046a5df  a1647d5000               mov eax, dword ptr [0x507d64]
0046a5e4  01f8                     add eax, edi
0046a5e6  803800                   cmp byte ptr [eax], 0
0046a5e9  7523                     jne 0x46a60e
0046a5eb  89c8                     mov eax, ecx
0046a5ed  e802c00000               call 0x4765f4
0046a5f2  8b155c7d5000             mov edx, dword ptr [0x507d5c]
0046a5f8  eb1c                     jmp 0x46a616
0046a5fa  89c8                     mov eax, ecx
0046a5fc  e8f3bf0000               call 0x4765f4
0046a601  8b15b4244e00             mov edx, dword ptr [0x4e24b4]
0046a607  25ff000000               and eax, 0xff
0046a60c  01d0                     add eax, edx
0046a60e  8b155c7d5000             mov edx, dword ptr [0x507d5c]
0046a614  8a00                     mov al, byte ptr [eax]
0046a616  88043a                   mov byte ptr [edx + edi], al
0046a619  8b442408                 mov eax, dword ptr [esp + 8]
0046a61d  40                       inc eax
0046a61e  43                       inc ebx
0046a61f  89442408                 mov dword ptr [esp + 8], eax
0046a623  8b442408                 mov eax, dword ptr [esp + 8]
0046a627  663b442404               cmp ax, word ptr [esp + 4]
0046a62c  0f8347feffff             jae 0x46a479
0046a632  807c242006               cmp byte ptr [esp + 0x20], 6
0046a637  77e0                     ja 0x46a619
0046a639  31c0                     xor eax, eax
0046a63b  8a442420                 mov al, byte ptr [esp + 0x20]
0046a63f  2eff24856ca34600         jmp dword ptr cs:[eax*4 + 0x46a36c]
0046a647  31c0                     xor eax, eax
0046a649  8a442424                 mov al, byte ptr [esp + 0x24]
0046a64d  31c9                     xor ecx, ecx
0046a64f  e8e759ffff               call 0x46003b
0046a654  6689d9                   mov cx, bx
0046a657  88c2                     mov dl, al
0046a659  a1647d5000               mov eax, dword ptr [0x507d64]
0046a65e  80c202                   add dl, 2
0046a661  881401                   mov byte ptr [ecx + eax], dl
0046a664  31d2                     xor edx, edx
0046a666  31c0                     xor eax, eax
0046a668  8a1541805000             mov dl, byte ptr [0x508041]
0046a66e  6689f0                   mov ax, si
0046a671  e8dbc20000               call 0x476951
0046a676  84c0                     test al, al
0046a678  749f                     je 0x46a619
0046a67a  a1607d5000               mov eax, dword ptr [0x507d60]
0046a67f  01c8                     add eax, ecx
0046a681  803800                   cmp byte ptr [eax], 0
0046a684  0f8570feffff             jne 0x46a4fa
0046a68a  a1647d5000               mov eax, dword ptr [0x507d64]
0046a68f  8b155c7d5000             mov edx, dword ptr [0x507d5c]
0046a695  8a0401                   mov al, byte ptr [ecx + eax]
0046a698  e965feffff               jmp 0x46a502
0046a69d  31ff                     xor edi, edi
0046a69f  a1647d5000               mov eax, dword ptr [0x507d64]
0046a6a4  6689df                   mov di, bx
0046a6a7  31d2                     xor edx, edx
0046a6a9  31c9                     xor ecx, ecx
0046a6ab  c6040700                 mov byte ptr [edi + eax], 0
0046a6af  6689f1                   mov cx, si
0046a6b2  8a1541805000             mov dl, byte ptr [0x508041]
0046a6b8  89c8                     mov eax, ecx
0046a6ba  e831c00000               call 0x4766f0
0046a6bf  84c0                     test al, al
0046a6c1  0f8452ffffff             je 0x46a619
0046a6c7  31d2                     xor edx, edx
0046a6c9  89c8                     mov eax, ecx
0046a6cb  8a1541805000             mov dl, byte ptr [0x508041]
0046a6d1  e87bc20000               call 0x476951
0046a6d6  84c0                     test al, al
0046a6d8  7415                     je 0x46a6ef
0046a6da  a1607d5000               mov eax, dword ptr [0x507d60]
0046a6df  01f8                     add eax, edi
0046a6e1  803800                   cmp byte ptr [eax], 0
0046a6e4  0f8524ffffff             jne 0x46a60e
0046a6ea  e9fcfeffff               jmp 0x46a5eb
0046a6ef  89c8                     mov eax, ecx
0046a6f1  31d2                     xor edx, edx
0046a6f3  e8fcbe0000               call 0x4765f4
0046a6f8  88c2                     mov dl, al
0046a6fa  a1b4244e00               mov eax, dword ptr [0x4e24b4]
0046a6ff  e908ffffff               jmp 0x46a60c
0046a704  83c428                   add esp, 0x28
0046a707  5d                       pop ebp
0046a708  5f                       pop edi
0046a709  5e                       pop esi
0046a70a  59                       pop ecx
0046a70b  c3                       ret
