; BatimentLogeEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041f76e  53                       push ebx
0041f76f  51                       push ecx
0041f770  56                       push esi
0041f771  57                       push edi
0041f772  55                       push ebp
0041f773  83ec04                   sub esp, 4
0041f776  50                       push eax
0041f777  52                       push edx
0041f778  31db                     xor ebx, ebx
0041f77a  6689c3                   mov bx, ax
0041f77d  89d8                     mov eax, ebx
0041f77f  c1e004                   shl eax, 4
0041f782  01d8                     add eax, ebx
0041f784  c1e002                   shl eax, 2
0041f787  01d8                     add eax, ebx
0041f789  bdc8a04900               mov ebp, 0x49a0c8
0041f78e  c1e002                   shl eax, 2
0041f791  01c5                     add ebp, eax
0041f793  31c0                     xor eax, eax
0041f795  6689d0                   mov ax, dx
0041f798  e888280200               call 0x442025
0041f79d  25ff000000               and eax, 0xff
0041f7a2  83f80a                   cmp eax, 0xa
0041f7a5  0f855d010000             jne 0x41f908
0041f7ab  8a4508                   mov al, byte ptr [ebp + 8]
0041f7ae  25ff000000               and eax, 0xff
0041f7b3  83f810                   cmp eax, 0x10
0041f7b6  7409                     je 0x41f7c1
0041f7b8  83f802                   cmp eax, 2
0041f7bb  0f8547010000             jne 0x41f908
0041f7c1  31db                     xor ebx, ebx
0041f7c3  668b5c2404               mov bx, word ptr [esp + 4]
0041f7c8  89d8                     mov eax, ebx
0041f7ca  c1e004                   shl eax, 4
0041f7cd  01d8                     add eax, ebx
0041f7cf  c1e002                   shl eax, 2
0041f7d2  bec8a04900               mov esi, 0x49a0c8
0041f7d7  01d8                     add eax, ebx
0041f7d9  31db                     xor ebx, ebx
0041f7db  c1e002                   shl eax, 2
0041f7de  668b1c24                 mov bx, word ptr [esp]
0041f7e2  01c6                     add esi, eax
0041f7e4  89d8                     mov eax, ebx
0041f7e6  8a5604                   mov dl, byte ptr [esi + 4]
0041f7e9  e857280200               call 0x442045
0041f7ee  38c2                     cmp dl, al
0041f7f0  0f8412010000             je 0x41f908
0041f7f6  8a4608                   mov al, byte ptr [esi + 8]
0041f7f9  25ff000000               and eax, 0xff
0041f7fe  83f810                   cmp eax, 0x10
0041f801  0f85fa000000             jne 0x41f901
0041f807  8a4604                   mov al, byte ptr [esi + 4]
0041f80a  25ff000000               and eax, 0xff
0041f80f  8a807c2e4e00             mov al, byte ptr [eax + 0x4e2e7c]
0041f815  25ff000000               and eax, 0xff
0041f81a  0f85e8020000             jne 0x41fb08
0041f820  89d8                     mov eax, ebx
0041f822  e81e280200               call 0x442045
0041f827  25ff000000               and eax, 0xff
0041f82c  8a807c2e4e00             mov al, byte ptr [eax + 0x4e2e7c]
0041f832  25ff000000               and eax, 0xff
0041f837  0f85cb020000             jne 0x41fb08
0041f83d  8a4604                   mov al, byte ptr [esi + 4]
0041f840  25ff000000               and eax, 0xff
0041f845  e89c190400               call 0x4611e6
0041f84a  25ffff0000               and eax, 0xffff
0041f84f  3dffff0000               cmp eax, 0xffff
0041f854  0f84ae020000             je 0x41fb08
0041f85a  89d8                     mov eax, ebx
0041f85c  e8e4270200               call 0x442045
0041f861  25ff000000               and eax, 0xff
0041f866  e87b190400               call 0x4611e6
0041f86b  25ffff0000               and eax, 0xffff
0041f870  3dffff0000               cmp eax, 0xffff
0041f875  0f848d020000             je 0x41fb08
0041f87b  8a4604                   mov al, byte ptr [esi + 4]
0041f87e  31d2                     xor edx, edx
0041f880  88c2                     mov dl, al
0041f882  89d8                     mov eax, ebx
0041f884  e8bc270200               call 0x442045
0041f889  25ff000000               and eax, 0xff
0041f88e  e8843a0400               call 0x463317
0041f893  89d8                     mov eax, ebx
0041f895  e8ab270200               call 0x442045
0041f89a  25ff000000               and eax, 0xff
0041f89f  e873df0400               call 0x46d817
0041f8a4  25ff000000               and eax, 0xff
0041f8a9  83f802                   cmp eax, 2
0041f8ac  7422                     je 0x41f8d0
0041f8ae  8a4604                   mov al, byte ptr [esi + 4]
0041f8b1  25ff000000               and eax, 0xff
0041f8b6  b201                     mov dl, 1
0041f8b8  88907c2e4e00             mov byte ptr [eax + 0x4e2e7c], dl
0041f8be  89d8                     mov eax, ebx
0041f8c0  e880270200               call 0x442045
0041f8c5  25ff000000               and eax, 0xff
0041f8ca  88907c2e4e00             mov byte ptr [eax + 0x4e2e7c], dl
0041f8d0  31db                     xor ebx, ebx
0041f8d2  668b5c2404               mov bx, word ptr [esp + 4]
0041f8d7  89d8                     mov eax, ebx
0041f8d9  c1e004                   shl eax, 4
0041f8dc  01d8                     add eax, ebx
0041f8de  c1e002                   shl eax, 2
0041f8e1  01d8                     add eax, ebx
0041f8e3  c1e002                   shl eax, 2
0041f8e6  05c8a04900               add eax, 0x49a0c8
0041f8eb  8a1d41805000             mov bl, byte ptr [0x508041]
0041f8f1  3a5804                   cmp bl, byte ptr [eax + 4]
0041f8f4  750b                     jne 0x41f901
0041f8f6  31db                     xor ebx, ebx
0041f8f8  31d2                     xor edx, edx
0041f8fa  31c0                     xor eax, eax
0041f8fc  e8aba8ffff               call 0x41a1ac
0041f901  b001                     mov al, 1
0041f903  e902020000               jmp 0x41fb0a
0041f908  31db                     xor ebx, ebx
0041f90a  668b5c2404               mov bx, word ptr [esp + 4]
0041f90f  89d8                     mov eax, ebx
0041f911  c1e004                   shl eax, 4
0041f914  01d8                     add eax, ebx
0041f916  c1e002                   shl eax, 2
0041f919  01d8                     add eax, ebx
0041f91b  bbc8a04900               mov ebx, 0x49a0c8
0041f920  c1e002                   shl eax, 2
0041f923  01c3                     add ebx, eax
0041f925  31d2                     xor edx, edx
0041f927  8a4308                   mov al, byte ptr [ebx + 8]
0041f92a  88c2                     mov dl, al
0041f92c  8d430c                   lea eax, [ebx + 0xc]
0041f92f  83fa15                   cmp edx, 0x15
0041f932  750d                     jne 0x41f941
0041f934  e811790200               call 0x44724a
0041f939  84c0                     test al, al
0041f93b  7429                     je 0x41f966
0041f93d  b001                     mov al, 1
0041f93f  eb27                     jmp 0x41f968
0041f941  83fa02                   cmp edx, 2
0041f944  7509                     jne 0x41f94f
0041f946  e8ff780200               call 0x44724a
0041f94b  84c0                     test al, al
0041f94d  75ee                     jne 0x41f93d
0041f94f  8d430c                   lea eax, [ebx + 0xc]
0041f952  ba01000000               mov edx, 1
0041f957  bb09000000               mov ebx, 9
0041f95c  e857780200               call 0x4471b8
0041f961  6685c0                   test ax, ax
0041f964  ebd5                     jmp 0x41f93b
0041f966  30c0                     xor al, al
0041f968  84c0                     test al, al
0041f96a  7414                     je 0x41f980
0041f96c  31c0                     xor eax, eax
0041f96e  668b0424                 mov ax, word ptr [esp]
0041f972  e8ce260200               call 0x442045
0041f977  3a4504                   cmp al, byte ptr [ebp + 4]
0041f97a  0f8588010000             jne 0x41fb08
0041f980  31db                     xor ebx, ebx
0041f982  31c0                     xor eax, eax
0041f984  668b1c24                 mov bx, word ptr [esp]
0041f988  668b442404               mov ax, word ptr [esp + 4]
0041f98d  89da                     mov edx, ebx
0041f98f  e8befbffff               call 0x41f552
0041f994  84c0                     test al, al
0041f996  0f846e010000             je 0x41fb0a
0041f99c  89d8                     mov eax, ebx
0041f99e  e882260200               call 0x442025
0041f9a3  25ff000000               and eax, 0xff
0041f9a8  83f809                   cmp eax, 9
0041f9ab  0f84a2000000             je 0x41fa53
0041f9b1  8b7c2404                 mov edi, dword ptr [esp + 4]
0041f9b5  89d8                     mov eax, ebx
0041f9b7  895c2408                 mov dword ptr [esp + 8], ebx
0041f9bb  e8e67a0200               call 0x4474a6
0041f9c0  89c6                     mov esi, eax
0041f9c2  bb02000000               mov ebx, 2
0041f9c7  89f0                     mov eax, esi
0041f9c9  89da                     mov edx, ebx
0041f9cb  e8e8770200               call 0x4471b8
0041f9d0  6685c0                   test ax, ax
0041f9d3  7434                     je 0x41fa09
0041f9d5  ba01000000               mov edx, 1
0041f9da  31c9                     xor ecx, ecx
0041f9dc  31c0                     xor eax, eax
0041f9de  31db                     xor ebx, ebx
0041f9e0  668b442408               mov ax, word ptr [esp + 8]
0041f9e5  6689f9                   mov cx, di
0041f9e8  e858260200               call 0x442045
0041f9ed  88c3                     mov bl, al
0041f9ef  b802000000               mov eax, 2
0041f9f4  e8163a0000               call 0x42340f
0041f9f9  bb02000000               mov ebx, 2
0041f9fe  89f0                     mov eax, esi
0041fa00  89da                     mov edx, ebx
0041fa02  e8e3780200               call 0x4472ea
0041fa07  ebb9                     jmp 0x41f9c2
0041fa09  bb01000000               mov ebx, 1
0041fa0e  ba02000000               mov edx, 2
0041fa13  89f0                     mov eax, esi
0041fa15  e89e770200               call 0x4471b8
0041fa1a  6685c0                   test ax, ax
0041fa1d  7434                     je 0x41fa53
0041fa1f  ba01000000               mov edx, 1
0041fa24  31c9                     xor ecx, ecx
0041fa26  31c0                     xor eax, eax
0041fa28  31db                     xor ebx, ebx
0041fa2a  668b442408               mov ax, word ptr [esp + 8]
0041fa2f  6689f9                   mov cx, di
0041fa32  e80e260200               call 0x442045
0041fa37  88c3                     mov bl, al
0041fa39  89d0                     mov eax, edx
0041fa3b  e8cf390000               call 0x42340f
0041fa40  bb01000000               mov ebx, 1
0041fa45  ba02000000               mov edx, 2
0041fa4a  89f0                     mov eax, esi
0041fa4c  e899780200               call 0x4472ea
0041fa51  ebb6                     jmp 0x41fa09
0041fa53  31c0                     xor eax, eax
0041fa55  8a4504                   mov al, byte ptr [ebp + 4]
0041fa58  3dc8000000               cmp eax, 0xc8
0041fa5d  0f858d000000             jne 0x41faf0
0041fa63  31c9                     xor ecx, ecx
0041fa65  668b0c24                 mov cx, word ptr [esp]
0041fa69  31db                     xor ebx, ebx
0041fa6b  89c8                     mov eax, ecx
0041fa6d  668b5c2404               mov bx, word ptr [esp + 4]
0041fa72  e8ce250200               call 0x442045
0041fa77  884504                   mov byte ptr [ebp + 4], al
0041fa7a  89d8                     mov eax, ebx
0041fa7c  ba01000000               mov edx, 1
0041fa81  e8ead1ffff               call 0x41cc70
0041fa86  89d8                     mov eax, ebx
0041fa88  e80aa4ffff               call 0x419e97
0041fa8d  89c8                     mov eax, ecx
0041fa8f  31d2                     xor edx, edx
0041fa91  e8af250200               call 0x442045
0041fa96  88c2                     mov dl, al
0041fa98  89d8                     mov eax, ebx
0041fa9a  e8e9c3ffff               call 0x41be88
0041fa9f  89d8                     mov eax, ebx
0041faa1  c1e004                   shl eax, 4
0041faa4  01d8                     add eax, ebx
0041faa6  c1e002                   shl eax, 2
0041faa9  01d8                     add eax, ebx
0041faab  b9c8a04900               mov ecx, 0x49a0c8
0041fab0  c1e002                   shl eax, 2
0041fab3  01c1                     add ecx, eax
0041fab5  8a4104                   mov al, byte ptr [ecx + 4]
0041fab8  3a0541805000             cmp al, byte ptr [0x508041]
0041fabe  7530                     jne 0x41faf0
0041fac0  89d8                     mov eax, ebx
0041fac2  e8e4a5ffff               call 0x41a0ab
0041fac7  83b900010000ff           cmp dword ptr [ecx + 0x100], -1
0041face  7520                     jne 0x41faf0
0041fad0  50                       push eax
0041fad1  31c0                     xor eax, eax
0041fad3  8a4108                   mov al, byte ptr [ecx + 8]
0041fad6  c1e010                   shl eax, 0x10
0041fad9  8d9900010000             lea ebx, [ecx + 0x100]
0041fadf  80cc27                   or ah, 0x27
0041fae2  31c9                     xor ecx, ecx
0041fae4  89c2                     mov edx, eax
0041fae6  b842000000               mov eax, 0x42
0041faeb  e889af0600               call 0x48aa79
0041faf0  ba01000000               mov edx, 1
0041faf5  31db                     xor ebx, ebx
0041faf7  8d450c                   lea eax, [ebp + 0xc]
0041fafa  668b1c24                 mov bx, word ptr [esp]
0041fafe  e880790200               call 0x447483
0041fb03  e9f9fdffff               jmp 0x41f901
0041fb08  30c0                     xor al, al
0041fb0a  83c40c                   add esp, 0xc
0041fb0d  e9883e0000               jmp 0x42399a
