; CalculTransporteEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044f2d4  53                       push ebx
0044f2d5  51                       push ecx
0044f2d6  52                       push edx
0044f2d7  56                       push esi
0044f2d8  57                       push edi
0044f2d9  55                       push ebp
0044f2da  83ec08                   sub esp, 8
0044f2dd  89c7                     mov edi, eax
0044f2df  31db                     xor ebx, ebx
0044f2e1  6689c3                   mov bx, ax
0044f2e4  89d8                     mov eax, ebx
0044f2e6  c1e004                   shl eax, 4
0044f2e9  01d8                     add eax, ebx
0044f2eb  c1e002                   shl eax, 2
0044f2ee  01d8                     add eax, ebx
0044f2f0  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044f2f6  c1e002                   shl eax, 2
0044f2f9  01c6                     add esi, eax
0044f2fb  30e4                     xor ah, ah
0044f2fd  88642404                 mov byte ptr [esp + 4], ah
0044f301  8a4601                   mov al, byte ptr [esi + 1]
0044f304  2c0b                     sub al, 0xb
0044f306  3c06                     cmp al, 6
0044f308  7711                     ja 0x44f31b
0044f30a  25ff000000               and eax, 0xff
0044f30f  2eff2485a4f24400         jmp dword ptr cs:[eax*4 + 0x44f2a4]
0044f317  b001                     mov al, 1
0044f319  eb02                     jmp 0x44f31d
0044f31b  30c0                     xor al, al
0044f31d  84c0                     test al, al
0044f31f  7411                     je 0x44f332
0044f321  31db                     xor ebx, ebx
0044f323  8a9e82000000             mov bl, byte ptr [esi + 0x82]
0044f329  83fb01                   cmp ebx, 1
0044f32c  0f855a050000             jne 0x44f88c
0044f332  31c0                     xor eax, eax
0044f334  6689f8                   mov ax, di
0044f337  e83cf7ffff               call 0x44ea78
0044f33c  83c408                   add esp, 8
0044f33f  e959ffffff               jmp 0x44f29d
0044f344  668b467e                 mov ax, word ptr [esi + 0x7e]
0044f348  668b4e08                 mov cx, word ptr [esi + 8]
0044f34c  6639c8                   cmp ax, cx
0044f34f  740c                     je 0x44f35d
0044f351  31c0                     xor eax, eax
0044f353  6689f8                   mov ax, di
0044f356  e8b19fffff               call 0x44930c
0044f35b  ebdf                     jmp 0x44f33c
0044f35d  31c0                     xor eax, eax
0044f35f  31d2                     xor edx, edx
0044f361  6689c8                   mov ax, cx
0044f364  668b9684000000           mov dx, word ptr [esi + 0x84]
0044f36b  e8c86c0200               call 0x476038
0044f370  25ff000000               and eax, 0xff
0044f375  39d0                     cmp eax, edx
0044f377  7517                     jne 0x44f390
0044f379  c6868900000001           mov byte ptr [esi + 0x89], 1
0044f380  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044f387  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044f38e  ebac                     jmp 0x44f33c
0044f390  ba0a000000               mov edx, 0xa
0044f395  0fb7ef                   movzx ebp, di
0044f398  8a8684000000             mov al, byte ptr [esi + 0x84]
0044f39e  31db                     xor ebx, ebx
0044f3a0  0442                     add al, 0x42
0044f3a2  55                       push ebp
0044f3a3  88c3                     mov bl, al
0044f3a5  31c0                     xor eax, eax
0044f3a7  89d9                     mov ecx, ebx
0044f3a9  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044f3b0  e8bf870200               call 0x477b74
0044f3b5  89c3                     mov ebx, eax
0044f3b7  31c0                     xor eax, eax
0044f3b9  6689d8                   mov ax, bx
0044f3bc  3dffff0000               cmp eax, 0xffff
0044f3c1  0f8475ffffff             je 0x44f33c
0044f3c7  89e8                     mov eax, ebp
0044f3c9  c1e004                   shl eax, 4
0044f3cc  01e8                     add eax, ebp
0044f3ce  c1e002                   shl eax, 2
0044f3d1  01e8                     add eax, ebp
0044f3d3  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044f3d9  c1e002                   shl eax, 2
0044f3dc  01d0                     add eax, edx
0044f3de  6689587e                 mov word ptr [eax + 0x7e], bx
0044f3e2  663b3d04634900           cmp di, word ptr [0x496304]
0044f3e9  7522                     jne 0x44f40d
0044f3eb  bfffff0000               mov edi, 0xffff
0044f3f0  30ff                     xor bh, bh
0044f3f2  31ed                     xor ebp, ebp
0044f3f4  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044f3fa  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044f400  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044f406  66893d04634900           mov word ptr [0x496304], di
0044f40d  c6808800000000           mov byte ptr [eax + 0x88], 0
0044f414  e923ffffff               jmp 0x44f33c
0044f419  8d460a                   lea eax, [esi + 0xa]
0044f41c  31d2                     xor edx, edx
0044f41e  668b5066                 mov dx, word ptr [eax + 0x66]
0044f422  42                       inc edx
0044f423  668b4002                 mov ax, word ptr [eax + 2]
0044f427  25ffff0000               and eax, 0xffff
0044f42c  39c2                     cmp edx, eax
0044f42e  0f9ec0                   setle al
0044f431  84c0                     test al, al
0044f433  0f8414010000             je 0x44f54d
0044f439  fe8e8b000000             dec byte ptr [esi + 0x8b]
0044f43f  31c0                     xor eax, eax
0044f441  8a868b000000             mov al, byte ptr [esi + 0x8b]
0044f447  85c0                     test eax, eax
0044f449  0f8503010000             jne 0x44f552
0044f44f  668b4608                 mov ax, word ptr [esi + 8]
0044f453  30ed                     xor ch, ch
0044f455  e808720200               call 0x476662
0044f45a  88c1                     mov cl, al
0044f45c  8d460a                   lea eax, [esi + 0xa]
0044f45f  66ff4066                 inc word ptr [eax + 0x66]
0044f463  31db                     xor ebx, ebx
0044f465  668b10                   mov dx, word ptr [eax]
0044f468  6689d3                   mov bx, dx
0044f46b  89da                     mov edx, ebx
0044f46d  c644034202               mov byte ptr [ebx + eax + 0x42], 2
0044f472  66894c5006               mov word ptr [eax + edx*2 + 6], cx
0044f477  66ff00                   inc word ptr [eax]
0044f47a  8a8684000000             mov al, byte ptr [esi + 0x84]
0044f480  31db                     xor ebx, ebx
0044f482  0442                     add al, 0x42
0044f484  0fb7ef                   movzx ebp, di
0044f487  88c3                     mov bl, al
0044f489  31c0                     xor eax, eax
0044f48b  55                       push ebp
0044f48c  668b4608                 mov ax, word ptr [esi + 8]
0044f490  b905000000               mov ecx, 5
0044f495  89442404                 mov dword ptr [esp + 4], eax
0044f499  b81f000000               mov eax, 0x1f
0044f49e  31d2                     xor edx, edx
0044f4a0  e837100200               call 0x4704dc
0044f4a5  f7f1                     div ecx
0044f4a7  8b442404                 mov eax, dword ptr [esp + 4]
0044f4ab  01d0                     add eax, edx
0044f4ad  89442404                 mov dword ptr [esp + 4], eax
0044f4b1  b820000000               mov eax, 0x20
0044f4b6  31d2                     xor edx, edx
0044f4b8  e81f100200               call 0x4704dc
0044f4bd  f7f1                     div ecx
0044f4bf  c1e208                   shl edx, 8
0044f4c2  8b442404                 mov eax, dword ptr [esp + 4]
0044f4c6  81ea00020000             sub edx, 0x200
0044f4cc  83e802                   sub eax, 2
0044f4cf  01d0                     add eax, edx
0044f4d1  ba0a000000               mov edx, 0xa
0044f4d6  25ffff0000               and eax, 0xffff
0044f4db  89d9                     mov ecx, ebx
0044f4dd  e892860200               call 0x477b74
0044f4e2  89c1                     mov ecx, eax
0044f4e4  31c0                     xor eax, eax
0044f4e6  6689c8                   mov ax, cx
0044f4e9  3dffff0000               cmp eax, 0xffff
0044f4ee  745d                     je 0x44f54d
0044f4f0  89e8                     mov eax, ebp
0044f4f2  c1e004                   shl eax, 4
0044f4f5  01e8                     add eax, ebp
0044f4f7  c1e002                   shl eax, 2
0044f4fa  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044f501  01e8                     add eax, ebp
0044f503  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044f509  c1e002                   shl eax, 2
0044f50c  01d0                     add eax, edx
0044f50e  6689487e                 mov word ptr [eax + 0x7e], cx
0044f512  663b3d04634900           cmp di, word ptr [0x496304]
0044f519  7522                     jne 0x44f53d
0044f51b  30d2                     xor dl, dl
0044f51d  31db                     xor ebx, ebx
0044f51f  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044f525  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044f52b  baffff0000               mov edx, 0xffff
0044f530  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044f536  66891504634900           mov word ptr [0x496304], dx
0044f53d  c6808800000000           mov byte ptr [eax + 0x88], 0
0044f544  c6868900000000           mov byte ptr [esi + 0x89], 0
0044f54b  eb05                     jmp 0x44f552
0044f54d  c644240401               mov byte ptr [esp + 4], 1
0044f552  807c240400               cmp byte ptr [esp + 4], 0
0044f557  0f84dffdffff             je 0x44f33c
0044f55d  31c0                     xor eax, eax
0044f55f  8a8682000000             mov al, byte ptr [esi + 0x82]
0044f565  83f802                   cmp eax, 2
0044f568  0f85e4000000             jne 0x44f652
0044f56e  668b8680000000           mov ax, word ptr [esi + 0x80]
0044f575  668986c0000000           mov word ptr [esi + 0xc0], ax
0044f57c  31c0                     xor eax, eax
0044f57e  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f585  3dffff0000               cmp eax, 0xffff
0044f58a  7476                     je 0x44f602
0044f58c  e84e42fdff               call 0x4237df
0044f591  31c0                     xor eax, eax
0044f593  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f59a  31db                     xor ebx, ebx
0044f59c  e88645fdff               call 0x423b27
0044f5a1  6689fb                   mov bx, di
0044f5a4  89c1                     mov ecx, eax
0044f5a6  89d8                     mov eax, ebx
0044f5a8  c1e004                   shl eax, 4
0044f5ab  01d8                     add eax, ebx
0044f5ad  c1e002                   shl eax, 2
0044f5b0  c6868900000002           mov byte ptr [esi + 0x89], 2
0044f5b7  01d8                     add eax, ebx
0044f5b9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044f5bf  c1e002                   shl eax, 2
0044f5c2  01d0                     add eax, edx
0044f5c4  81e9fe000000             sub ecx, 0xfe
0044f5ca  6689487e                 mov word ptr [eax + 0x7e], cx
0044f5ce  663b3d04634900           cmp di, word ptr [0x496304]
0044f5d5  0f8532feffff             jne 0x44f40d
0044f5db  bbffff0000               mov ebx, 0xffff
0044f5e0  30f6                     xor dh, dh
0044f5e2  31ff                     xor edi, edi
0044f5e4  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044f5ea  8835370f4e00             mov byte ptr [0x4e0f37], dh
0044f5f0  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044f5f6  66891d04634900           mov word ptr [0x496304], bx
0044f5fd  e90bfeffff               jmp 0x44f40d
0044f602  31db                     xor ebx, ebx
0044f604  6689fb                   mov bx, di
0044f607  89d8                     mov eax, ebx
0044f609  c1e004                   shl eax, 4
0044f60c  01d8                     add eax, ebx
0044f60e  c1e002                   shl eax, 2
0044f611  01c3                     add ebx, eax
0044f613  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f618  c1e302                   shl ebx, 2
0044f61b  01d8                     add eax, ebx
0044f61d  668b567c                 mov dx, word ptr [esi + 0x7c]
0044f621  6689507e                 mov word ptr [eax + 0x7e], dx
0044f625  663b3d04634900           cmp di, word ptr [0x496304]
0044f62c  0f85dbfdffff             jne 0x44f40d
0044f632  bfffff0000               mov edi, 0xffff
0044f637  30ed                     xor ch, ch
0044f639  31f6                     xor esi, esi
0044f63b  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044f641  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044f647  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044f64d  e9b4fdffff               jmp 0x44f406
0044f652  83f801                   cmp eax, 1
0044f655  0f85e1fcffff             jne 0x44f33c
0044f65b  31db                     xor ebx, ebx
0044f65d  6689fb                   mov bx, di
0044f660  89d8                     mov eax, ebx
0044f662  c1e004                   shl eax, 4
0044f665  01d8                     add eax, ebx
0044f667  c1e002                   shl eax, 2
0044f66a  c6868900000002           mov byte ptr [esi + 0x89], 2
0044f671  01d8                     add eax, ebx
0044f673  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044f679  c1e002                   shl eax, 2
0044f67c  01d0                     add eax, edx
0044f67e  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044f685  6689487e                 mov word ptr [eax + 0x7e], cx
0044f689  663b3d04634900           cmp di, word ptr [0x496304]
0044f690  0f8577fdffff             jne 0x44f40d
0044f696  30ff                     xor bh, bh
0044f698  31c9                     xor ecx, ecx
0044f69a  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044f6a0  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044f6a6  b9ffff0000               mov ecx, 0xffff
0044f6ab  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044f6b1  66890d04634900           mov word ptr [0x496304], cx
0044f6b8  e950fdffff               jmp 0x44f40d
0044f6bd  668b467e                 mov ax, word ptr [esi + 0x7e]
0044f6c1  663b4608                 cmp ax, word ptr [esi + 8]
0044f6c5  0f8586fcffff             jne 0x44f351
0044f6cb  31c0                     xor eax, eax
0044f6cd  8a8682000000             mov al, byte ptr [esi + 0x82]
0044f6d3  c6868900000003           mov byte ptr [esi + 0x89], 3
0044f6da  83f802                   cmp eax, 2
0044f6dd  7507                     jne 0x44f6e6
0044f6df  c6869000000009           mov byte ptr [esi + 0x90], 9
0044f6e6  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044f6ed  e94afcffff               jmp 0x44f33c
0044f6f2  8a8690000000             mov al, byte ptr [esi + 0x90]
0044f6f8  3a8691000000             cmp al, byte ptr [esi + 0x91]
0044f6fe  740f                     je 0x44f70f
0044f700  31c0                     xor eax, eax
0044f702  6689f8                   mov ax, di
0044f705  e88f8effff               call 0x448599
0044f70a  e92dfcffff               jmp 0x44f33c
0044f70f  83fb02                   cmp ebx, 2
0044f712  753c                     jne 0x44f750
0044f714  31c0                     xor eax, eax
0044f716  ba01000000               mov edx, 1
0044f71b  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f722  e835affcff               call 0x41a65c
0044f727  31c0                     xor eax, eax
0044f729  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f730  e84715fdff               call 0x420c7c
0044f735  84c0                     test al, al
0044f737  0f84fffbffff             je 0x44f33c
0044f73d  c6868900000004           mov byte ptr [esi + 0x89], 4
0044f744  c6868b00000032           mov byte ptr [esi + 0x8b], 0x32
0044f74b  e9ecfbffff               jmp 0x44f33c
0044f750  c6868900000004           mov byte ptr [esi + 0x89], 4
0044f757  eb8d                     jmp 0x44f6e6
0044f759  ba02000000               mov edx, 2
0044f75e  8d4e0a                   lea ecx, [esi + 0xa]
0044f761  31db                     xor ebx, ebx
0044f763  89c8                     mov eax, ecx
0044f765  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f76c  e8477affff               call 0x4471b8
0044f771  25ffff0000               and eax, 0xffff
0044f776  0f8593000000             jne 0x44f80f
0044f77c  8a8682000000             mov al, byte ptr [esi + 0x82]
0044f782  83f802                   cmp eax, 2
0044f785  751e                     jne 0x44f7a5
0044f787  31c0                     xor eax, eax
0044f789  31d2                     xor edx, edx
0044f78b  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f792  e8c5aefcff               call 0x41a65c
0044f797  31c0                     xor eax, eax
0044f799  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f7a0  e85a40fdff               call 0x4237ff
0044f7a5  31db                     xor ebx, ebx
0044f7a7  6689fb                   mov bx, di
0044f7aa  89da                     mov edx, ebx
0044f7ac  c1e204                   shl edx, 4
0044f7af  01da                     add edx, ebx
0044f7b1  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
0044f7ba  c1e202                   shl edx, 2
0044f7bd  c6868900000000           mov byte ptr [esi + 0x89], 0
0044f7c4  01da                     add edx, ebx
0044f7c6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f7cb  c1e202                   shl edx, 2
0044f7ce  01d0                     add eax, edx
0044f7d0  668b8eb2000000           mov cx, word ptr [esi + 0xb2]
0044f7d7  6689487e                 mov word ptr [eax + 0x7e], cx
0044f7db  663b3d04634900           cmp di, word ptr [0x496304]
0044f7e2  0f8525fcffff             jne 0x44f40d
0044f7e8  30f6                     xor dh, dh
0044f7ea  bbffff0000               mov ebx, 0xffff
0044f7ef  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044f7f5  8835370f4e00             mov byte ptr [0x4e0f37], dh
0044f7fb  31d2                     xor edx, edx
0044f7fd  66891d04634900           mov word ptr [0x496304], bx
0044f804  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0044f80a  e9fefbffff               jmp 0x44f40d
0044f80f  8a968b000000             mov dl, byte ptr [esi + 0x8b]
0044f815  31c0                     xor eax, eax
0044f817  feca                     dec dl
0044f819  88d0                     mov al, dl
0044f81b  88968b000000             mov byte ptr [esi + 0x8b], dl
0044f821  85c0                     test eax, eax
0044f823  0f8513fbffff             jne 0x44f33c
0044f829  ba02000000               mov edx, 2
0044f82e  31db                     xor ebx, ebx
0044f830  89c8                     mov eax, ecx
0044f832  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f839  e8ac7affff               call 0x4472ea
0044f83e  31c0                     xor eax, eax
0044f840  8a8682000000             mov al, byte ptr [esi + 0x82]
0044f846  83f802                   cmp eax, 2
0044f849  7524                     jne 0x44f86f
0044f84b  ba01000000               mov edx, 1
0044f850  31c9                     xor ecx, ecx
0044f852  31db                     xor ebx, ebx
0044f854  31c0                     xor eax, eax
0044f856  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044f85d  8a1e                     mov bl, byte ptr [esi]
0044f85f  8a8684000000             mov al, byte ptr [esi + 0x84]
0044f865  e8a53bfdff               call 0x42340f
0044f86a  e9d5feffff               jmp 0x44f744
0044f86f  ba02000000               mov edx, 2
0044f874  31c0                     xor eax, eax
0044f876  31db                     xor ebx, ebx
0044f878  6689f8                   mov ax, di
0044f87b  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f882  e85140ffff               call 0x4438d8
0044f887  e95afeffff               jmp 0x44f6e6
0044f88c  8a8689000000             mov al, byte ptr [esi + 0x89]
0044f892  3c04                     cmp al, 4
0044f894  0f87a2faffff             ja 0x44f33c
0044f89a  25ff000000               and eax, 0xff
0044f89f  2eff2485c0f24400         jmp dword ptr cs:[eax*4 + 0x44f2c0]
