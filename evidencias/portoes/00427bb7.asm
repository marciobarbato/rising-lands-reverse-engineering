; BatimentNextEtape_tipo12; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00427bb7  803daf99500000           cmp byte ptr [0x5099af], 0
00427bbe  0f84e3000000             je 0x427ca7
00427bc4  803d50fb4d0000           cmp byte ptr [0x4dfb50], 0
00427bcb  0f85d6000000             jne 0x427ca7
00427bd1  31c0                     xor eax, eax
00427bd3  b101                     mov cl, 1
00427bd5  a041805000               mov al, byte ptr [0x508041]
00427bda  880d50fb4d00             mov byte ptr [0x4dfb50], cl
00427be0  e8b4ebffff               call 0x426799
00427be5  89c3                     mov ebx, eax
00427be7  31c0                     xor eax, eax
00427be9  6689d8                   mov ax, bx
00427bec  3dffff0000               cmp eax, 0xffff
00427bf1  0f84b0000000             je 0x427ca7
00427bf7  31d2                     xor edx, edx
00427bf9  6689da                   mov dx, bx
00427bfc  89d0                     mov eax, edx
00427bfe  c1e004                   shl eax, 4
00427c01  01d0                     add eax, edx
00427c03  c1e002                   shl eax, 2
00427c06  01d0                     add eax, edx
00427c08  668b0c85caa04900         mov cx, word ptr [eax*4 + 0x49a0ca]
00427c10  89d8                     mov eax, ebx
00427c12  31db                     xor ebx, ebx
00427c14  6689c3                   mov bx, ax
00427c17  89d8                     mov eax, ebx
00427c19  c1e004                   shl eax, 4
00427c1c  01d8                     add eax, ebx
00427c1e  c1e002                   shl eax, 2
00427c21  01d8                     add eax, ebx
00427c23  c1e002                   shl eax, 2
00427c26  8945cc                   mov dword ptr [ebp - 0x34], eax
00427c29  b8c8a04900               mov eax, 0x49a0c8
00427c2e  0345cc                   add eax, dword ptr [ebp - 0x34]
00427c31  31db                     xor ebx, ebx
00427c33  8a5876                   mov bl, byte ptr [eax + 0x76]
00427c36  85db                     test ebx, ebx
00427c38  741a                     je 0x427c54
00427c3a  31db                     xor ebx, ebx
00427c3c  8a5876                   mov bl, byte ptr [eax + 0x76]
00427c3f  83fb0f                   cmp ebx, 0xf
00427c42  7410                     je 0x427c54
00427c44  88d8                     mov al, bl
00427c46  25ff000000               and eax, 0xff
00427c4b  83f81f                   cmp eax, 0x1f
00427c4e  7404                     je 0x427c54
00427c50  b001                     mov al, 1
00427c52  eb02                     jmp 0x427c56
00427c54  30c0                     xor al, al
00427c56  84c0                     test al, al
00427c58  754d                     jne 0x427ca7
00427c5a  31db                     xor ebx, ebx
00427c5c  6689d3                   mov bx, dx
00427c5f  89d8                     mov eax, ebx
00427c61  c1e004                   shl eax, 4
00427c64  01d8                     add eax, ebx
00427c66  c1e002                   shl eax, 2
00427c69  01d8                     add eax, ebx
00427c6b  c1e002                   shl eax, 2
00427c6e  05c8a04900               add eax, 0x49a0c8
00427c73  8a4076                   mov al, byte ptr [eax + 0x76]
00427c76  25ff000000               and eax, 0xff
00427c7b  83f80f                   cmp eax, 0xf
00427c7e  0f94c0                   sete al
00427c81  84c0                     test al, al
00427c83  7412                     je 0x427c97
00427c85  31c0                     xor eax, eax
00427c87  81e2ffff0000             and edx, 0xffff
00427c8d  6689c8                   mov ax, cx
00427c90  e83519ffff               call 0x4195ca
00427c95  eb10                     jmp 0x427ca7
00427c97  31c0                     xor eax, eax
00427c99  81e2ffff0000             and edx, 0xffff
00427c9f  6689c8                   mov ax, cx
00427ca2  e82d17ffff               call 0x4193d4
00427ca7  31d2                     xor edx, edx
00427ca9  6689fa                   mov dx, di
00427cac  89d0                     mov eax, edx
00427cae  c1e004                   shl eax, 4
00427cb1  01d0                     add eax, edx
00427cb3  c1e002                   shl eax, 2
00427cb6  01d0                     add eax, edx
00427cb8  c1e002                   shl eax, 2
00427cbb  05c8a04900               add eax, 0x49a0c8
00427cc0  8a4076                   mov al, byte ptr [eax + 0x76]
00427cc3  25ff000000               and eax, 0xff
00427cc8  740e                     je 0x427cd8
00427cca  83f80f                   cmp eax, 0xf
00427ccd  7409                     je 0x427cd8
00427ccf  83f81f                   cmp eax, 0x1f
00427cd2  7404                     je 0x427cd8
00427cd4  b001                     mov al, 1
00427cd6  eb02                     jmp 0x427cda
00427cd8  30c0                     xor al, al
00427cda  84c0                     test al, al
00427cdc  0f84de040000             je 0x4281c0
00427ce2  8a6e76                   mov ch, byte ptr [esi + 0x76]
00427ce5  31c0                     xor eax, eax
00427ce7  fec5                     inc ch
00427ce9  88e8                     mov al, ch
00427ceb  886e76                   mov byte ptr [esi + 0x76], ch
00427cee  83f81f                   cmp eax, 0x1f
00427cf1  7c04                     jl 0x427cf7
00427cf3  c6467600                 mov byte ptr [esi + 0x76], 0
00427cf7  31c0                     xor eax, eax
00427cf9  8a4676                   mov al, byte ptr [esi + 0x76]
00427cfc  83f80f                   cmp eax, 0xf
00427cff  7532                     jne 0x427d33
00427d01  ba01000000               mov edx, 1
00427d06  31c0                     xor eax, eax
00427d08  bb01000000               mov ebx, 1
00427d0d  668b4602                 mov ax, word ptr [esi + 2]
00427d11  8d8ecc000000             lea ecx, [esi + 0xcc]
00427d17  e822e50400               call 0x47623e
00427d1c  6a00                     push 0
00427d1e  31d2                     xor edx, edx
00427d20  31c0                     xor eax, eax
00427d22  6689fa                   mov dx, di
00427d25  668b4602                 mov ax, word ptr [esi + 2]
00427d29  e80a640100               call 0x43e138
00427d2e  e98d040000               jmp 0x4281c0
00427d33  83f81f                   cmp eax, 0x1f
00427d36  7d08                     jge 0x427d40
00427d38  85c0                     test eax, eax
00427d3a  0f8580040000             jne 0x4281c0
00427d40  ba01000000               mov edx, 1
00427d45  31c0                     xor eax, eax
00427d47  bb03000000               mov ebx, 3
00427d4c  668b4602                 mov ax, word ptr [esi + 2]
00427d50  8d8ecc000000             lea ecx, [esi + 0xcc]
00427d56  e8d3e40400               call 0x47622e
00427d5b  ebbf                     jmp 0x427d1c
