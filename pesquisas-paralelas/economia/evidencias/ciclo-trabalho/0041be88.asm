; InitBatimentPlayer; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041be88  53                       push ebx
0041be89  51                       push ecx
0041be8a  56                       push esi
0041be8b  83ec10                   sub esp, 0x10
0041be8e  89c3                     mov ebx, eax
0041be90  88d4                     mov ah, dl
0041be92  31d2                     xor edx, edx
0041be94  6689da                   mov dx, bx
0041be97  89d6                     mov esi, edx
0041be99  c1e604                   shl esi, 4
0041be9c  01d6                     add esi, edx
0041be9e  c1e602                   shl esi, 2
0041bea1  01d6                     add esi, edx
0041bea3  bac8a04900               mov edx, 0x49a0c8
0041bea8  c1e602                   shl esi, 2
0041beab  01f2                     add edx, esi
0041bead  8a4208                   mov al, byte ptr [edx + 8]
0041beb0  3c06                     cmp al, 6
0041beb2  0f821f010000             jb 0x41bfd7
0041beb8  0f860a010000             jbe 0x41bfc8
0041bebe  3c12                     cmp al, 0x12
0041bec0  0f8519010000             jne 0x41bfdf
0041bec6  0fb6f4                   movzx esi, ah
0041bec9  89f0                     mov eax, esi
0041becb  e8da5c0200               call 0x441baa
0041bed0  fe864cfb4d00             inc byte ptr [esi + 0x4dfb4c]
0041bed6  31c0                     xor eax, eax
0041bed8  8a4204                   mov al, byte ptr [edx + 4]
0041bedb  31db                     xor ebx, ebx
0041bedd  ba10000000               mov edx, 0x10
0041bee2  8a984cfb4d00             mov bl, byte ptr [eax + 0x4dfb4c]
0041bee8  e8a5ae0300               call 0x456d92
0041beed  25ffff0000               and eax, 0xffff
0041bef2  39c3                     cmp ebx, eax
0041bef4  0f8ee5000000             jle 0x41bfdf
0041befa  89f0                     mov eax, esi
0041befc  c1e603                   shl esi, 3
0041beff  01c6                     add esi, eax
0041bf01  c1e604                   shl esi, 4
0041bf04  29c6                     sub esi, eax
0041bf06  c1e604                   shl esi, 4
0041bf09  81c6e8d64d00             add esi, 0x4dd6e8
0041bf0f  bb10000000               mov ebx, 0x10
0041bf14  81c650070000             add esi, 0x750
0041bf1a  ba06000000               mov edx, 6
0041bf1f  89f0                     mov eax, esi
0041bf21  e892b20200               call 0x4471b8
0041bf26  6685c0                   test ax, ax
0041bf29  0f85b0000000             jne 0x41bfdf
0041bf2f  ba01000000               mov edx, 1
0041bf34  89f0                     mov eax, esi
0041bf36  bb10000000               mov ebx, 0x10
0041bf3b  e808b20200               call 0x447148
0041bf40  ba06000000               mov edx, 6
0041bf45  89f0                     mov eax, esi
0041bf47  e837b50200               call 0x447483
0041bf4c  e98e000000               jmp 0x41bfdf
0041bf51  88e0                     mov al, ah
0041bf53  25ff000000               and eax, 0xff
0041bf58  89c6                     mov esi, eax
0041bf5a  c1e602                   shl esi, 2
0041bf5d  29c6                     sub esi, eax
0041bf5f  01f6                     add esi, esi
0041bf61  66ff862cfb4d00           inc word ptr [esi + 0x4dfb2c]
0041bf68  83f804                   cmp eax, 4
0041bf6b  7d72                     jge 0x41bfdf
0041bf6d  31d2                     xor edx, edx
0041bf6f  668b962cfb4d00           mov dx, word ptr [esi + 0x4dfb2c]
0041bf76  85d2                     test edx, edx
0041bf78  7e65                     jle 0x41bfdf
0041bf7a  8d4c2404                 lea ecx, [esp + 4]
0041bf7e  89e3                     mov ebx, esp
0041bf80  50                       push eax
0041bf81  8d54240c                 lea edx, [esp + 0xc]
0041bf85  8d442410                 lea eax, [esp + 0x10]
0041bf89  e80fb70400               call 0x46769d
0041bf8e  8b44240c                 mov eax, dword ptr [esp + 0xc]
0041bf92  8b5c2408                 mov ebx, dword ptr [esp + 8]
0041bf96  668b8e2cfb4d00           mov cx, word ptr [esi + 0x4dfb2c]
0041bf9d  31d2                     xor edx, edx
0041bf9f  01d8                     add eax, ebx
0041bfa1  66f7f1                   div cx
0041bfa4  31d2                     xor edx, edx
0041bfa6  6689c2                   mov dx, ax
0041bfa9  89d0                     mov eax, edx
0041bfab  c1e003                   shl eax, 3
0041bfae  29d0                     sub eax, edx
0041bfb0  31db                     xor ebx, ebx
0041bfb2  89c2                     mov edx, eax
0041bfb4  668b9e2efb4d00           mov bx, word ptr [esi + 0x4dfb2e]
0041bfbb  c1fa1f                   sar edx, 0x1f
0041bfbe  f7fb                     idiv ebx
0041bfc0  888630fb4d00             mov byte ptr [esi + 0x4dfb30], al
0041bfc6  eb17                     jmp 0x41bfdf
0041bfc8  88e0                     mov al, ah
0041bfca  25ff000000               and eax, 0xff
0041bfcf  fe8048fb4d00             inc byte ptr [eax + 0x4dfb48]
0041bfd5  eb08                     jmp 0x41bfdf
0041bfd7  3c03                     cmp al, 3
0041bfd9  0f8472ffffff             je 0x41bf51
0041bfdf  83c410                   add esp, 0x10
0041bfe2  5e                       pop esi
0041bfe3  59                       pop ecx
0041bfe4  5b                       pop ebx
0041bfe5  c3                       ret
