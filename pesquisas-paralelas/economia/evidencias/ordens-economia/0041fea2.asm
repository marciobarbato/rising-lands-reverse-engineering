; CreerBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041fea2  51                       push ecx
0041fea3  56                       push esi
0041fea4  57                       push edi
0041fea5  55                       push ebp
0041fea6  83ec54                   sub esp, 0x54
0041fea9  50                       push eax
0041feaa  88542454                 mov byte ptr [esp + 0x54], dl
0041feae  885c2450                 mov byte ptr [esp + 0x50], bl
0041feb2  31d2                     xor edx, edx
0041feb4  89542428                 mov dword ptr [esp + 0x28], edx
0041feb8  8954240c                 mov dword ptr [esp + 0xc], edx
0041febc  8954241c                 mov dword ptr [esp + 0x1c], edx
0041fec0  89542424                 mov dword ptr [esp + 0x24], edx
0041fec4  31c0                     xor eax, eax
0041fec6  668b442424               mov ax, word ptr [esp + 0x24]
0041fecb  3de8030000               cmp eax, 0x3e8
0041fed0  7d20                     jge 0x41fef2
0041fed2  69c014010000             imul eax, eax, 0x114
0041fed8  05c8a04900               add eax, 0x49a0c8
0041fedd  8a4005                   mov al, byte ptr [eax + 5]
0041fee0  25ff000000               and eax, 0xff
0041fee5  0f95c0                   setne al
0041fee8  84c0                     test al, al
0041feea  7406                     je 0x41fef2
0041feec  ff442424                 inc dword ptr [esp + 0x24]
0041fef0  ebd2                     jmp 0x41fec4
0041fef2  31c0                     xor eax, eax
0041fef4  668b442424               mov ax, word ptr [esp + 0x24]
0041fef9  3de8030000               cmp eax, 0x3e8
0041fefe  0f84bd030000             je 0x4202c1
0041ff04  31d2                     xor edx, edx
0041ff06  8a542454                 mov dl, byte ptr [esp + 0x54]
0041ff0a  89d0                     mov eax, edx
0041ff0c  c1e002                   shl eax, 2
0041ff0f  29d0                     sub eax, edx
0041ff11  c1e002                   shl eax, 2
0041ff14  01c2                     add edx, eax
0041ff16  c1e202                   shl edx, 2
0041ff19  0fb67c2450               movzx edi, byte ptr [esp + 0x50]
0041ff1e  668b82985d4900           mov ax, word ptr [edx + 0x495d98]
0041ff25  31c9                     xor ecx, ecx
0041ff27  89442428                 mov dword ptr [esp + 0x28], eax
0041ff2b  668b829a5d4900           mov ax, word ptr [edx + 0x495d9a]
0041ff32  31db                     xor ebx, ebx
0041ff34  8944241c                 mov dword ptr [esp + 0x1c], eax
0041ff38  668b829c5d4900           mov ax, word ptr [edx + 0x495d9c]
0041ff3f  57                       push edi
0041ff40  89442410                 mov dword ptr [esp + 0x10], eax
0041ff44  31d2                     xor edx, edx
0041ff46  31c0                     xor eax, eax
0041ff48  668b542420               mov dx, word ptr [esp + 0x20]
0041ff4d  668b44242c               mov ax, word ptr [esp + 0x2c]
0041ff52  e88e770400               call 0x4676e5
0041ff57  84c0                     test al, al
0041ff59  0f8462030000             je 0x4202c1
0041ff5f  b801000000               mov eax, 1
0041ff64  89fb                     mov ebx, edi
0041ff66  31d2                     xor edx, edx
0041ff68  89fe                     mov esi, edi
0041ff6a  668b542428               mov dx, word ptr [esp + 0x28]
0041ff6f  c1e602                   shl esi, 2
0041ff72  e8b5790400               call 0x46792c
0041ff77  29fe                     sub esi, edi
0041ff79  89f8                     mov eax, edi
0041ff7b  01f6                     add esi, esi
0041ff7d  31f8                     xor eax, edi
0041ff7f  668b862cfb4d00           mov ax, word ptr [esi + 0x4dfb2c]
0041ff86  85c0                     test eax, eax
0041ff88  7e4e                     jle 0x41ffd8
0041ff8a  8d4c2420                 lea ecx, [esp + 0x20]
0041ff8e  8d5c2404                 lea ebx, [esp + 4]
0041ff92  57                       push edi
0041ff93  8d54241c                 lea edx, [esp + 0x1c]
0041ff97  8d44240c                 lea eax, [esp + 0xc]
0041ff9b  e8fd760400               call 0x46769d
0041ffa0  8b442408                 mov eax, dword ptr [esp + 8]
0041ffa4  8b7c2418                 mov edi, dword ptr [esp + 0x18]
0041ffa8  668b9e2cfb4d00           mov bx, word ptr [esi + 0x4dfb2c]
0041ffaf  31d2                     xor edx, edx
0041ffb1  01f8                     add eax, edi
0041ffb3  66f7f3                   div bx
0041ffb6  31d2                     xor edx, edx
0041ffb8  6689c2                   mov dx, ax
0041ffbb  89d0                     mov eax, edx
0041ffbd  c1e003                   shl eax, 3
0041ffc0  29d0                     sub eax, edx
0041ffc2  31db                     xor ebx, ebx
0041ffc4  89c2                     mov edx, eax
0041ffc6  668b9e2efb4d00           mov bx, word ptr [esi + 0x4dfb2e]
0041ffcd  c1fa1f                   sar edx, 0x1f
0041ffd0  f7fb                     idiv ebx
0041ffd2  888630fb4d00             mov byte ptr [esi + 0x4dfb30], al
0041ffd8  0fb67c2450               movzx edi, byte ptr [esp + 0x50]
0041ffdd  31d2                     xor edx, edx
0041ffdf  b802000000               mov eax, 2
0041ffe4  668b54241c               mov dx, word ptr [esp + 0x1c]
0041ffe9  89fe                     mov esi, edi
0041ffeb  89fb                     mov ebx, edi
0041ffed  c1e602                   shl esi, 2
0041fff0  e837790400               call 0x46792c
0041fff5  29fe                     sub esi, edi
0041fff7  89f8                     mov eax, edi
0041fff9  01f6                     add esi, esi
0041fffb  31f8                     xor eax, edi
0041fffd  668b862cfb4d00           mov ax, word ptr [esi + 0x4dfb2c]
00420004  85c0                     test eax, eax
00420006  7e4e                     jle 0x420056
00420008  8d4c2438                 lea ecx, [esp + 0x38]
0042000c  8d5c2434                 lea ebx, [esp + 0x34]
00420010  57                       push edi
00420011  8d542434                 lea edx, [esp + 0x34]
00420015  8d442450                 lea eax, [esp + 0x50]
00420019  e87f760400               call 0x46769d
0042001e  8b44244c                 mov eax, dword ptr [esp + 0x4c]
00420022  8b4c2430                 mov ecx, dword ptr [esp + 0x30]
00420026  668bbe2cfb4d00           mov di, word ptr [esi + 0x4dfb2c]
0042002d  31d2                     xor edx, edx
0042002f  01c8                     add eax, ecx
00420031  66f7f7                   div di
00420034  31d2                     xor edx, edx
00420036  6689c2                   mov dx, ax
00420039  89d0                     mov eax, edx
0042003b  c1e003                   shl eax, 3
0042003e  29d0                     sub eax, edx
00420040  31db                     xor ebx, ebx
00420042  89c2                     mov edx, eax
00420044  668b9e2efb4d00           mov bx, word ptr [esi + 0x4dfb2e]
0042004b  c1fa1f                   sar edx, 0x1f
0042004e  f7fb                     idiv ebx
00420050  888630fb4d00             mov byte ptr [esi + 0x4dfb30], al
00420056  31db                     xor ebx, ebx
00420058  8a5c2454                 mov bl, byte ptr [esp + 0x54]
0042005c  89d8                     mov eax, ebx
0042005e  c1e002                   shl eax, 2
00420061  29d8                     sub eax, ebx
00420063  c1e002                   shl eax, 2
00420066  8d1403                   lea edx, [ebx + eax]
00420069  c1e202                   shl edx, 2
0042006c  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
00420073  89442444                 mov dword ptr [esp + 0x44], eax
00420077  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
0042007e  31d2                     xor edx, edx
00420080  668b542424               mov dx, word ptr [esp + 0x24]
00420085  89442440                 mov dword ptr [esp + 0x40], eax
00420089  89d0                     mov eax, edx
0042008b  c1e004                   shl eax, 4
0042008e  01d0                     add eax, edx
00420090  c1e002                   shl eax, 2
00420093  01d0                     add eax, edx
00420095  bdc8a04900               mov ebp, 0x49a0c8
0042009a  c1e002                   shl eax, 2
0042009d  01c5                     add ebp, eax
0042009f  c6450502                 mov byte ptr [ebp + 5], 2
004200a3  8b442440                 mov eax, dword ptr [esp + 0x40]
004200a7  8b542444                 mov edx, dword ptr [esp + 0x44]
004200ab  48                       dec eax
004200ac  4a                       dec edx
004200ad  c1e008                   shl eax, 8
004200b0  01d0                     add eax, edx
004200b2  8b1424                   mov edx, dword ptr [esp]
004200b5  c64504c8                 mov byte ptr [ebp + 4], 0xc8
004200b9  29c2                     sub edx, eax
004200bb  66895502                 mov word ptr [ebp + 2], dx
004200bf  83fb11                   cmp ebx, 0x11
004200c2  7507                     jne 0x4200cb
004200c4  8a442450                 mov al, byte ptr [esp + 0x50]
004200c8  884504                   mov byte ptr [ebp + 4], al
004200cb  31c0                     xor eax, eax
004200cd  8a442454                 mov al, byte ptr [esp + 0x54]
004200d1  83f80c                   cmp eax, 0xc
004200d4  0f857e010000             jne 0x420258
004200da  668b4502                 mov ax, word ptr [ebp + 2]
004200de  8944242c                 mov dword ptr [esp + 0x2c], eax
004200e2  31c0                     xor eax, eax
004200e4  8944243c                 mov dword ptr [esp + 0x3c], eax
004200e8  eb04                     jmp 0x4200ee
004200ea  ff44243c                 inc dword ptr [esp + 0x3c]
004200ee  31c0                     xor eax, eax
004200f0  668b44243c               mov ax, word ptr [esp + 0x3c]
004200f5  3de8030000               cmp eax, 0x3e8
004200fa  0f8db7000000             jge 0x4201b7
00420100  69c014010000             imul eax, eax, 0x114
00420106  bfc8a04900               mov edi, 0x49a0c8
0042010b  01c7                     add edi, eax
0042010d  31c0                     xor eax, eax
0042010f  8a4705                   mov al, byte ptr [edi + 5]
00420112  85c0                     test eax, eax
00420114  0f95c0                   setne al
00420117  84c0                     test al, al
00420119  74cf                     je 0x4200ea
0042011b  8a4708                   mov al, byte ptr [edi + 8]
0042011e  31d2                     xor edx, edx
00420120  88c2                     mov dl, al
00420122  83fa09                   cmp edx, 9
00420125  75c3                     jne 0x4200ea
00420127  6bd234                   imul edx, edx, 0x34
0042012a  8b44242c                 mov eax, dword ptr [esp + 0x2c]
0042012e  89fe                     mov esi, edi
00420130  89442448                 mov dword ptr [esp + 0x48], eax
00420134  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
0042013b  668b7f02                 mov di, word ptr [edi + 2]
0042013f  89442410                 mov dword ptr [esp + 0x10], eax
00420143  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
0042014a  31c9                     xor ecx, ecx
0042014c  89442414                 mov dword ptr [esp + 0x14], eax
00420150  eb01                     jmp 0x420153
00420152  41                       inc ecx
00420153  663b4c2414               cmp cx, word ptr [esp + 0x14]
00420158  734d                     jae 0x4201a7
0042015a  31db                     xor ebx, ebx
0042015c  eb01                     jmp 0x42015f
0042015e  43                       inc ebx
0042015f  663b5c2410               cmp bx, word ptr [esp + 0x10]
00420164  73ec                     jae 0x420152
00420166  31c0                     xor eax, eax
00420168  31d2                     xor edx, edx
0042016a  6689c8                   mov ax, cx
0042016d  6689fa                   mov dx, di
00420170  c1e008                   shl eax, 8
00420173  01c2                     add edx, eax
00420175  31c0                     xor eax, eax
00420177  6689d8                   mov ax, bx
0042017a  01d0                     add eax, edx
0042017c  31d2                     xor edx, edx
0042017e  668b542448               mov dx, word ptr [esp + 0x48]
00420183  39d0                     cmp eax, edx
00420185  75d7                     jne 0x42015e
00420187  8b442410                 mov eax, dword ptr [esp + 0x10]
0042018b  0fafc1                   imul eax, ecx
0042018e  31d2                     xor edx, edx
00420190  01d8                     add eax, ebx
00420192  6689c2                   mov dx, ax
00420195  31c0                     xor eax, eax
00420197  8a4608                   mov al, byte ptr [esi + 8]
0042019a  e8bda9ffff               call 0x41ab5c
0042019f  84c0                     test al, al
004201a1  74bb                     je 0x42015e
004201a3  b001                     mov al, 1
004201a5  eb02                     jmp 0x4201a9
004201a7  30c0                     xor al, al
004201a9  84c0                     test al, al
004201ab  0f8439ffffff             je 0x4200ea
004201b1  8b44243c                 mov eax, dword ptr [esp + 0x3c]
004201b5  eb05                     jmp 0x4201bc
004201b7  b8ffff0000               mov eax, 0xffff
004201bc  31d2                     xor edx, edx
004201be  6689c2                   mov dx, ax
004201c1  81faffff0000             cmp edx, 0xffff
004201c7  0f848b000000             je 0x420258
004201cd  89d0                     mov eax, edx
004201cf  c1e004                   shl eax, 4
004201d2  01d0                     add eax, edx
004201d4  c1e002                   shl eax, 2
004201d7  b9ffff0000               mov ecx, 0xffff
004201dc  01d0                     add eax, edx
004201de  30db                     xor bl, bl
004201e0  89d6                     mov esi, edx
004201e2  881c85cda04900           mov byte ptr [eax*4 + 0x49a0cd], bl
004201e9  31d6                     xor esi, edx
004201eb  66890c8540a14900         mov word ptr [eax*4 + 0x49a140], cx
004201f3  31ff                     xor edi, edi
004201f5  6689348544a14900         mov word ptr [eax*4 + 0x49a144], si
004201fd  66893c8546a14900         mov word ptr [eax*4 + 0x49a146], di
00420205  30ff                     xor bh, bh
00420207  31c9                     xor ecx, ecx
00420209  66891c85d2a04900         mov word ptr [eax*4 + 0x49a0d2], bx
00420211  66890c854aa14900         mov word ptr [eax*4 + 0x49a14a], cx
00420219  b7ff                     mov bh, 0xff
0042021b  883c85c8a04900           mov byte ptr [eax*4 + 0x49a0c8], bh
00420222  881c853ca14900           mov byte ptr [eax*4 + 0x49a13c], bl
00420229  881c853da14900           mov byte ptr [eax*4 + 0x49a13d], bl
00420230  881c853ea14900           mov byte ptr [eax*4 + 0x49a13e], bl
00420237  883c8543a14900           mov byte ptr [eax*4 + 0x49a143], bh
0042023e  30ff                     xor bh, bh
00420240  66891c8548a14900         mov word ptr [eax*4 + 0x49a148], bx
00420248  31db                     xor ebx, ebx
0042024a  891c8554a14900           mov dword ptr [eax*4 + 0x49a154], ebx
00420251  89d0                     mov eax, edx
00420253  e837b5ffff               call 0x41b78f
00420258  8a442454                 mov al, byte ptr [esp + 0x54]
0042025c  884508                   mov byte ptr [ebp + 8], al
0042025f  89e8                     mov eax, ebp
00420261  31e8                     xor eax, ebp
00420263  66c7450a0100             mov word ptr [ebp + 0xa], 1
00420269  668b442424               mov ax, word ptr [esp + 0x24]
0042026e  66c745060000             mov word ptr [ebp + 6], 0
00420274  e833c2ffff               call 0x41c4ac
00420279  8d450c                   lea eax, [ebp + 0xc]
0042027c  e88a6e0200               call 0x44710b
00420281  31c0                     xor eax, eax
00420283  8a442454                 mov al, byte ptr [esp + 0x54]
00420287  83f809                   cmp eax, 9
0042028a  7405                     je 0x420291
0042028c  83f80c                   cmp eax, 0xc
0042028f  7507                     jne 0x420298
00420291  8a442450                 mov al, byte ptr [esp + 0x50]
00420295  884504                   mov byte ptr [ebp + 4], al
00420298  31d2                     xor edx, edx
0042029a  8a542454                 mov dl, byte ptr [esp + 0x54]
0042029e  89d0                     mov eax, edx
004202a0  c1e002                   shl eax, 2
004202a3  29d0                     sub eax, edx
004202a5  c1e002                   shl eax, 2
004202a8  01d0                     add eax, edx
004202aa  31d2                     xor edx, edx
004202ac  8a14859e5d4900           mov dl, byte ptr [eax*4 + 0x495d9e]
004202b3  8d450c                   lea eax, [ebp + 0xc]
004202b6  e88d6e0200               call 0x447148
004202bb  8b442424                 mov eax, dword ptr [esp + 0x24]
004202bf  eb05                     jmp 0x4202c6
004202c1  b8ffff0000               mov eax, 0xffff
004202c6  83c458                   add esp, 0x58
004202c9  5d                       pop ebp
004202ca  5f                       pop edi
004202cb  5e                       pop esi
004202cc  59                       pop ecx
004202cd  c3                       ret
