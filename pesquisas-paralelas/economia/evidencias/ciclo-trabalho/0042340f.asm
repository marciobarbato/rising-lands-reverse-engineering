; BatimentAjouteMatiere; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042340f  56                       push esi
00423410  57                       push edi
00423411  55                       push ebp
00423412  83ec1c                   sub esp, 0x1c
00423415  88442414                 mov byte ptr [esp + 0x14], al
00423419  89d7                     mov edi, edx
0042341b  885c2418                 mov byte ptr [esp + 0x18], bl
0042341f  31db                     xor ebx, ebx
00423421  6689cb                   mov bx, cx
00423424  89de                     mov esi, ebx
00423426  c1e604                   shl esi, 4
00423429  01de                     add esi, ebx
0042342b  c1e602                   shl esi, 2
0042342e  01de                     add esi, ebx
00423430  c1e602                   shl esi, 2
00423433  89d8                     mov eax, ebx
00423435  81c6c8a04900             add esi, 0x49a0c8
0042343b  31d8                     xor eax, ebx
0042343d  31d2                     xor edx, edx
0042343f  8a4608                   mov al, byte ptr [esi + 8]
00423442  89542408                 mov dword ptr [esp + 8], edx
00423446  83f804                   cmp eax, 4
00423449  0f84c2000000             je 0x423511
0042344f  31d2                     xor edx, edx
00423451  8a542418                 mov dl, byte ptr [esp + 0x18]
00423455  89d5                     mov ebp, edx
00423457  c1e502                   shl ebp, 2
0042345a  29d5                     sub ebp, edx
0042345c  01ed                     add ebp, ebp
0042345e  6683bd2cfb4d0000         cmp word ptr [ebp + 0x4dfb2c], 0
00423466  0f849f000000             je 0x42350b
0042346c  89e1                     mov ecx, esp
0042346e  8d5c2404                 lea ebx, [esp + 4]
00423472  52                       push edx
00423473  8d442410                 lea eax, [esp + 0x10]
00423477  8d542414                 lea edx, [esp + 0x14]
0042347b  e81d420400               call 0x46769d
00423480  8b4c240c                 mov ecx, dword ptr [esp + 0xc]
00423484  8b442410                 mov eax, dword ptr [esp + 0x10]
00423488  668b952cfb4d00           mov dx, word ptr [ebp + 0x4dfb2c]
0042348f  01c1                     add ecx, eax
00423491  668b852efb4d00           mov ax, word ptr [ebp + 0x4dfb2e]
00423498  0fafc2                   imul eax, edx
0042349b  31db                     xor ebx, ebx
0042349d  31d2                     xor edx, edx
0042349f  6689cb                   mov bx, cx
004234a2  6689fa                   mov dx, di
004234a5  01da                     add edx, ebx
004234a7  31db                     xor ebx, ebx
004234a9  6689c3                   mov bx, ax
004234ac  39da                     cmp edx, ebx
004234ae  7e0c                     jle 0x4234bc
004234b0  01cf                     add edi, ecx
004234b2  29c7                     sub edi, eax
004234b4  897c2408                 mov dword ptr [esp + 8], edi
004234b8  89c7                     mov edi, eax
004234ba  29cf                     sub edi, ecx
004234bc  0fb66c2418               movzx ebp, byte ptr [esp + 0x18]
004234c1  31c0                     xor eax, eax
004234c3  31d2                     xor edx, edx
004234c5  8a442414                 mov al, byte ptr [esp + 0x14]
004234c9  6689fa                   mov dx, di
004234cc  89eb                     mov ebx, ebp
004234ce  e81f440400               call 0x4678f2
004234d3  89eb                     mov ebx, ebp
004234d5  c1e302                   shl ebx, 2
004234d8  29eb                     sub ebx, ebp
004234da  89c8                     mov eax, ecx
004234dc  01db                     add ebx, ebx
004234de  31d2                     xor edx, edx
004234e0  01f8                     add eax, edi
004234e2  66f7b32cfb4d00           div word ptr [ebx + 0x4dfb2c]
004234e9  31d2                     xor edx, edx
004234eb  6689c2                   mov dx, ax
004234ee  89d0                     mov eax, edx
004234f0  c1e003                   shl eax, 3
004234f3  29d0                     sub eax, edx
004234f5  89c2                     mov edx, eax
004234f7  0fb7ab2efb4d00           movzx ebp, word ptr [ebx + 0x4dfb2e]
004234fe  c1fa1f                   sar edx, 0x1f
00423501  f7fd                     idiv ebp
00423503  888330fb4d00             mov byte ptr [ebx + 0x4dfb30], al
00423509  eb4a                     jmp 0x423555
0042350b  897c2408                 mov dword ptr [esp + 8], edi
0042350f  eb44                     jmp 0x423555
00423511  ba01000000               mov edx, 1
00423516  8d460c                   lea eax, [esi + 0xc]
00423519  e8b43b0200               call 0x4470d2
0042351e  84c0                     test al, al
00423520  7414                     je 0x423536
00423522  31c0                     xor eax, eax
00423524  668b4678                 mov ax, word ptr [esi + 0x78]
00423528  83f805                   cmp eax, 5
0042352b  7d28                     jge 0x423555
0042352d  89c3                     mov ebx, eax
0042352f  43                       inc ebx
00423530  66895e78                 mov word ptr [esi + 0x78], bx
00423534  eb1f                     jmp 0x423555
00423536  89d8                     mov eax, ebx
00423538  e8a3a8ffff               call 0x41dde0
0042353d  668b4602                 mov ax, word ptr [esi + 2]
00423541  80c402                   add ah, 2
00423544  bb01000000               mov ebx, 1
00423549  25ffff0000               and eax, 0xffff
0042354e  89da                     mov edx, ebx
00423550  e8542c0500               call 0x4761a9
00423555  31db                     xor ebx, ebx
00423557  668b5c2408               mov bx, word ptr [esp + 8]
0042355c  85db                     test ebx, ebx
0042355e  7e56                     jle 0x4235b6
00423560  31c0                     xor eax, eax
00423562  8a4608                   mov al, byte ptr [esi + 8]
00423565  83f803                   cmp eax, 3
00423568  752e                     jne 0x423598
0042356a  31c0                     xor eax, eax
0042356c  8a442414                 mov al, byte ptr [esp + 0x14]
00423570  83f801                   cmp eax, 1
00423573  750b                     jne 0x423580
00423575  668b4602                 mov ax, word ptr [esi + 2]
00423579  0502020000               add eax, 0x202
0042357e  eb09                     jmp 0x423589
00423580  668b4602                 mov ax, word ptr [esi + 2]
00423584  0503000000               add eax, 3
00423589  31db                     xor ebx, ebx
0042358b  31d2                     xor edx, edx
0042358d  668b5c2408               mov bx, word ptr [esp + 8]
00423592  8a542414                 mov dl, byte ptr [esp + 0x14]
00423596  eb14                     jmp 0x4235ac
00423598  83f802                   cmp eax, 2
0042359b  7519                     jne 0x4235b6
0042359d  31d2                     xor edx, edx
0042359f  668b4602                 mov ax, word ptr [esi + 2]
004235a3  8a542414                 mov dl, byte ptr [esp + 0x14]
004235a7  0503030000               add eax, 0x303
004235ac  25ffff0000               and eax, 0xffff
004235b1  e8f32b0500               call 0x4761a9
004235b6  83c41c                   add esp, 0x1c
004235b9  5d                       pop ebp
004235ba  5f                       pop edi
004235bb  5e                       pop esi
004235bc  c3                       ret
