; IALoadAttaqueIni; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047c24d  53                       push ebx
0047c24e  51                       push ecx
0047c24f  52                       push edx
0047c250  83ec08                   sub esp, 8
0047c253  31d2                     xor edx, edx
0047c255  b7ff                     mov bh, 0xff
0047c257  89542404                 mov dword ptr [esp + 4], edx
0047c25b  891424                   mov dword ptr [esp], edx
0047c25e  31d2                     xor edx, edx
0047c260  b9ffff0000               mov ecx, 0xffff
0047c265  89159cd95000             mov dword ptr [0x50d99c], edx
0047c26b  31d2                     xor edx, edx
0047c26d  eb33                     jmp 0x47c2a2
0047c26f  6bc00a                   imul eax, eax, 0xa
0047c272  c680b4d55000c8           mov byte ptr [eax + 0x50d5b4], 0xc8
0047c279  88b8b5d55000             mov byte ptr [eax + 0x50d5b5], bh
0047c27f  668988b6d55000           mov word ptr [eax + 0x50d5b6], cx
0047c286  88b8b8d55000             mov byte ptr [eax + 0x50d5b8], bh
0047c28c  88b8b9d55000             mov byte ptr [eax + 0x50d5b9], bh
0047c292  668988bad55000           mov word ptr [eax + 0x50d5ba], cx
0047c299  30db                     xor bl, bl
0047c29b  42                       inc edx
0047c29c  8898bcd55000             mov byte ptr [eax + 0x50d5bc], bl
0047c2a2  31c0                     xor eax, eax
0047c2a4  6689d0                   mov ax, dx
0047c2a7  83f864                   cmp eax, 0x64
0047c2aa  7cc3                     jl 0x47c26f
0047c2ac  ba02000000               mov edx, 2
0047c2b1  8d442404                 lea eax, [esp + 4]
0047c2b5  e8a7c1fdff               call 0x458461
0047c2ba  ba02000000               mov edx, 2
0047c2bf  89e0                     mov eax, esp
0047c2c1  31db                     xor ebx, ebx
0047c2c3  eb14                     jmp 0x47c2d9
0047c2c5  31c0                     xor eax, eax
0047c2c7  6689d8                   mov ax, bx
0047c2ca  6bc00a                   imul eax, eax, 0xa
0047c2cd  31d2                     xor edx, edx
0047c2cf  668b1424                 mov dx, word ptr [esp]
0047c2d3  05b4d55000               add eax, 0x50d5b4
0047c2d8  43                       inc ebx
0047c2d9  e883c1fdff               call 0x458461
0047c2de  663b5c2404               cmp bx, word ptr [esp + 4]
0047c2e3  72e0                     jb 0x47c2c5
0047c2e5  83c408                   add esp, 8
0047c2e8  5a                       pop edx
0047c2e9  59                       pop ecx
0047c2ea  5b                       pop ebx
0047c2eb  c3                       ret
