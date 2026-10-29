; BatimentPosable; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041fc40  51                       push ecx
0041fc41  56                       push esi
0041fc42  57                       push edi
0041fc43  55                       push ebp
0041fc44  83ec24                   sub esp, 0x24
0041fc47  89d1                     mov ecx, edx
0041fc49  895c2414                 mov dword ptr [esp + 0x14], ebx
0041fc4d  25ff000000               and eax, 0xff
0041fc52  89c2                     mov edx, eax
0041fc54  c1e202                   shl edx, 2
0041fc57  29c2                     sub edx, eax
0041fc59  c1e202                   shl edx, 2
0041fc5c  01c2                     add edx, eax
0041fc5e  89442404                 mov dword ptr [esp + 4], eax
0041fc62  668b04958c5d4900         mov ax, word ptr [edx*4 + 0x495d8c]
0041fc6a  89442410                 mov dword ptr [esp + 0x10], eax
0041fc6e  668b04958e5d4900         mov ax, word ptr [edx*4 + 0x495d8e]
0041fc76  8944240c                 mov dword ptr [esp + 0xc], eax
0041fc7a  81e1ffff0000             and ecx, 0xffff
0041fc80  bb00010000               mov ebx, 0x100
0041fc85  89ca                     mov edx, ecx
0041fc87  89c8                     mov eax, ecx
0041fc89  c1fa1f                   sar edx, 0x1f
0041fc8c  f7fb                     idiv ebx
0041fc8e  89542408                 mov dword ptr [esp + 8], edx
0041fc92  89ca                     mov edx, ecx
0041fc94  89c8                     mov eax, ecx
0041fc96  c1fa1f                   sar edx, 0x1f
0041fc99  f7fb                     idiv ebx
0041fc9b  89442418                 mov dword ptr [esp + 0x18], eax
0041fc9f  b401                     mov ah, 1
0041fca1  31db                     xor ebx, ebx
0041fca3  8825b8054e00             mov byte ptr [0x4e05b8], ah
0041fca9  31c0                     xor eax, eax
0041fcab  668b5c240c               mov bx, word ptr [esp + 0xc]
0041fcb0  668b442410               mov ax, word ptr [esp + 0x10]
0041fcb5  0fafd8                   imul ebx, eax
0041fcb8  ba01000000               mov edx, 1
0041fcbd  b8b9054e00               mov eax, 0x4e05b9
0041fcc2  31ff                     xor edi, edi
0041fcc4  e8e7c60600               call 0x48c3b0
0041fcc9  668b7c2410               mov di, word ptr [esp + 0x10]
0041fcce  89fa                     mov edx, edi
0041fcd0  89f8                     mov eax, edi
0041fcd2  c1fa1f                   sar edx, 0x1f
0041fcd5  2bc2                     sub eax, edx
0041fcd7  d1f8                     sar eax, 1
0041fcd9  89ce                     mov esi, ecx
0041fcdb  31c9                     xor ecx, ecx
0041fcdd  668b4c240c               mov cx, word ptr [esp + 0xc]
0041fce2  89c3                     mov ebx, eax
0041fce4  89ca                     mov edx, ecx
0041fce6  29c6                     sub esi, eax
0041fce8  89c8                     mov eax, ecx
0041fcea  c1fa1f                   sar edx, 0x1f
0041fced  2bc2                     sub eax, edx
0041fcef  d1f8                     sar eax, 1
0041fcf1  89c2                     mov edx, eax
0041fcf3  c1e208                   shl edx, 8
0041fcf6  29d6                     sub esi, edx
0041fcf8  31d2                     xor edx, edx
0041fcfa  668b542408               mov dx, word ptr [esp + 8]
0041fcff  891424                   mov dword ptr [esp], edx
0041fd02  39d3                     cmp ebx, edx
0041fd04  7f29                     jg 0x41fd2f
0041fd06  31d2                     xor edx, edx
0041fd08  668b542418               mov dx, word ptr [esp + 0x18]
0041fd0d  39c2                     cmp edx, eax
0041fd0f  7c1e                     jl 0x41fd2f
0041fd11  8b2c24                   mov ebp, dword ptr [esp]
0041fd14  29dd                     sub ebp, ebx
0041fd16  8d5c2fff                 lea ebx, [edi + ebp - 1]
0041fd1a  81fb00010000             cmp ebx, 0x100
0041fd20  7f0d                     jg 0x41fd2f
0041fd22  29c2                     sub edx, eax
0041fd24  01d1                     add ecx, edx
0041fd26  49                       dec ecx
0041fd27  81f900010000             cmp ecx, 0x100
0041fd2d  7e2f                     jle 0x41fd5e
0041fd2f  31c0                     xor eax, eax
0041fd31  31db                     xor ebx, ebx
0041fd33  668b442410               mov ax, word ptr [esp + 0x10]
0041fd38  668b5c240c               mov bx, word ptr [esp + 0xc]
0041fd3d  0fafd8                   imul ebx, eax
0041fd40  31d2                     xor edx, edx
0041fd42  b8b9054e00               mov eax, 0x4e05b9
0041fd47  e864c60600               call 0x48c3b0
0041fd4c  30d2                     xor dl, dl
0041fd4e  30c0                     xor al, al
0041fd50  8815b8054e00             mov byte ptr [0x4e05b8], dl
0041fd56  83c424                   add esp, 0x24
0041fd59  5d                       pop ebp
0041fd5a  5f                       pop edi
0041fd5b  5e                       pop esi
0041fd5c  59                       pop ecx
0041fd5d  c3                       ret
0041fd5e  837c24040c               cmp dword ptr [esp + 4], 0xc
0041fd63  0f84be000000             je 0x41fe27
0041fd69  31d2                     xor edx, edx
0041fd6b  bd01000000               mov ebp, 1
0041fd70  8954241c                 mov dword ptr [esp + 0x1c], edx
0041fd74  eb12                     jmp 0x41fd88
0041fd76  8b5c241c                 mov ebx, dword ptr [esp + 0x1c]
0041fd7a  b800010000               mov eax, 0x100
0041fd7f  43                       inc ebx
0041fd80  29f8                     sub eax, edi
0041fd82  895c241c                 mov dword ptr [esp + 0x1c], ebx
0041fd86  01c6                     add esi, eax
0041fd88  8b44241c                 mov eax, dword ptr [esp + 0x1c]
0041fd8c  663b44240c               cmp ax, word ptr [esp + 0xc]
0041fd91  0f8301010000             jae 0x41fe98
0041fd97  31c9                     xor ecx, ecx
0041fd99  eb06                     jmp 0x41fda1
0041fd9b  8b4c2420                 mov ecx, dword ptr [esp + 0x20]
0041fd9f  41                       inc ecx
0041fda0  46                       inc esi
0041fda1  894c2420                 mov dword ptr [esp + 0x20], ecx
0041fda5  8b442420                 mov eax, dword ptr [esp + 0x20]
0041fda9  8b7c2410                 mov edi, dword ptr [esp + 0x10]
0041fdad  6639f8                   cmp ax, di
0041fdb0  73c4                     jae 0x41fd76
0041fdb2  31c9                     xor ecx, ecx
0041fdb4  6689f1                   mov cx, si
0041fdb7  89c8                     mov eax, ecx
0041fdb9  e8ac650500               call 0x47636a
0041fdbe  84c0                     test al, al
0041fdc0  7439                     je 0x41fdfb
0041fdc2  31ff                     xor edi, edi
0041fdc4  668b7c2414               mov di, word ptr [esp + 0x14]
0041fdc9  89f8                     mov eax, edi
0041fdcb  31d2                     xor edx, edx
0041fdcd  e873220200               call 0x442045
0041fdd2  88c2                     mov dl, al
0041fdd4  89c8                     mov eax, ecx
0041fdd6  e815690500               call 0x4766f0
0041fddb  84c0                     test al, al
0041fddd  741c                     je 0x41fdfb
0041fddf  89ea                     mov edx, ebp
0041fde1  89c8                     mov eax, ecx
0041fde3  e8ec630500               call 0x4761d4
0041fde8  84c0                     test al, al
0041fdea  74af                     je 0x41fd9b
0041fdec  89eb                     mov ebx, ebp
0041fdee  89ca                     mov edx, ecx
0041fdf0  89f8                     mov eax, edi
0041fdf2  e877260200               call 0x44246e
0041fdf7  84c0                     test al, al
0041fdf9  75a0                     jne 0x41fd9b
0041fdfb  31d2                     xor edx, edx
0041fdfd  31c9                     xor ecx, ecx
0041fdff  668b54241c               mov dx, word ptr [esp + 0x1c]
0041fe04  668b4c2410               mov cx, word ptr [esp + 0x10]
0041fe09  0fafd1                   imul edx, ecx
0041fe0c  31c9                     xor ecx, ecx
0041fe0e  668b4c2420               mov cx, word ptr [esp + 0x20]
0041fe13  30db                     xor bl, bl
0041fe15  889c11b9054e00           mov byte ptr [ecx + edx + 0x4e05b9], bl
0041fe1c  881db8054e00             mov byte ptr [0x4e05b8], bl
0041fe22  e974ffffff               jmp 0x41fd9b
0041fe27  31db                     xor ebx, ebx
0041fe29  eb0a                     jmp 0x41fe35
0041fe2b  b800010000               mov eax, 0x100
0041fe30  29f8                     sub eax, edi
0041fe32  43                       inc ebx
0041fe33  01c6                     add esi, eax
0041fe35  663b5c240c               cmp bx, word ptr [esp + 0xc]
0041fe3a  735c                     jae 0x41fe98
0041fe3c  31c9                     xor ecx, ecx
0041fe3e  eb02                     jmp 0x41fe42
0041fe40  46                       inc esi
0041fe41  41                       inc ecx
0041fe42  8b7c2410                 mov edi, dword ptr [esp + 0x10]
0041fe46  6639f9                   cmp cx, di
0041fe49  73e0                     jae 0x41fe2b
0041fe4b  31ff                     xor edi, edi
0041fe4d  6689f7                   mov di, si
0041fe50  89f8                     mov eax, edi
0041fe52  e834aeffff               call 0x41ac8b
0041fe57  8b15747d5000             mov edx, dword ptr [0x507d74]
0041fe5d  8a243a                   mov ah, byte ptr [edx + edi]
0041fe60  3a25f85b4900             cmp ah, byte ptr [0x495bf8]
0041fe66  750c                     jne 0x41fe74
0041fe68  31d2                     xor edx, edx
0041fe6a  88c2                     mov dl, al
0041fe6c  81faff000000             cmp edx, 0xff
0041fe72  75cc                     jne 0x41fe40
0041fe74  31d2                     xor edx, edx
0041fe76  31ff                     xor edi, edi
0041fe78  668b542410               mov dx, word ptr [esp + 0x10]
0041fe7d  6689df                   mov di, bx
0041fe80  0fafd7                   imul edx, edi
0041fe83  31ff                     xor edi, edi
0041fe85  6689cf                   mov di, cx
0041fe88  30c0                     xor al, al
0041fe8a  88843ab9054e00           mov byte ptr [edx + edi + 0x4e05b9], al
0041fe91  a2b8054e00               mov byte ptr [0x4e05b8], al
0041fe96  eba8                     jmp 0x41fe40
0041fe98  a0b8054e00               mov al, byte ptr [0x4e05b8]
0041fe9d  e9b4feffff               jmp 0x41fd56
