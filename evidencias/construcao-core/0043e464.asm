; Remplit; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043e464  53                       push ebx
0043e465  51                       push ecx
0043e466  56                       push esi
0043e467  57                       push edi
0043e468  55                       push ebp
0043e469  83ec14                   sub esp, 0x14
0043e46c  88542410                 mov byte ptr [esp + 0x10], dl
0043e470  31d2                     xor edx, edx
0043e472  8a542410                 mov dl, byte ptr [esp + 0x10]
0043e476  85d2                     test edx, edx
0043e478  0f8419010000             je 0x43e597
0043e47e  31d2                     xor edx, edx
0043e480  8b1d6c154e00             mov ebx, dword ptr [0x4e156c]
0043e486  6689c2                   mov dx, ax
0043e489  8a141a                   mov dl, byte ptr [edx + ebx]
0043e48c  be01000000               mov esi, 1
0043e491  8854240c                 mov byte ptr [esp + 0xc], dl
0043e495  66a334074e00             mov word ptr [0x4e0734], ax
0043e49b  bdffff0000               mov ebp, 0xffff
0043e4a0  85f6                     test esi, esi
0043e4a2  0f84ef000000             je 0x43e597
0043e4a8  668b3c7532074e00         mov di, word ptr [esi*2 + 0x4e0732]
0043e4b0  31c0                     xor eax, eax
0043e4b2  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e4b8  6689f8                   mov ax, di
0043e4bb  01d0                     add eax, edx
0043e4bd  8a10                     mov dl, byte ptr [eax]
0043e4bf  8a74240c                 mov dh, byte ptr [esp + 0xc]
0043e4c3  4e                       dec esi
0043e4c4  38f2                     cmp dl, dh
0043e4c6  7506                     jne 0x43e4ce
0043e4c8  8a542410                 mov dl, byte ptr [esp + 0x10]
0043e4cc  8810                     mov byte ptr [eax], dl
0043e4ce  89f8                     mov eax, edi
0043e4d0  30db                     xor bl, bl
0043e4d2  8d0c36                   lea ecx, [esi + esi]
0043e4d5  885c2408                 mov byte ptr [esp + 8], bl
0043e4d9  30e4                     xor ah, ah
0043e4db  b701                     mov bh, 1
0043e4dd  890424                   mov dword ptr [esp], eax
0043e4e0  887c2404                 mov byte ptr [esp + 4], bh
0043e4e4  eb69                     jmp 0x43e54f
0043e4e6  31db                     xor ebx, ebx
0043e4e8  668b1d68714900           mov bx, word ptr [0x497168]
0043e4ef  4b                       dec ebx
0043e4f0  39da                     cmp edx, ebx
0043e4f2  0f8f8c000000             jg 0x43e584
0043e4f8  85c0                     test eax, eax
0043e4fa  0f8c84000000             jl 0x43e584
0043e500  31db                     xor ebx, ebx
0043e502  668b1d6a714900           mov bx, word ptr [0x49716a]
0043e509  4b                       dec ebx
0043e50a  39d8                     cmp eax, ebx
0043e50c  0f8f72000000             jg 0x43e584
0043e512  c1e008                   shl eax, 8
0043e515  01d0                     add eax, edx
0043e517  31d2                     xor edx, edx
0043e519  6689c2                   mov dx, ax
0043e51c  81faffff0000             cmp edx, 0xffff
0043e522  7422                     je 0x43e546
0043e524  8b1d6c154e00             mov ebx, dword ptr [0x4e156c]
0043e52a  8a141a                   mov dl, byte ptr [edx + ebx]
0043e52d  3a54240c                 cmp dl, byte ptr [esp + 0xc]
0043e531  7513                     jne 0x43e546
0043e533  81feff030000             cmp esi, 0x3ff
0043e539  7d0b                     jge 0x43e546
0043e53b  83c102                   add ecx, 2
0043e53e  46                       inc esi
0043e53f  66898132074e00           mov word ptr [ecx + 0x4e0732], ax
0043e546  8044240404               add byte ptr [esp + 4], 4
0043e54b  fe442408                 inc byte ptr [esp + 8]
0043e54f  31c0                     xor eax, eax
0043e551  8a442408                 mov al, byte ptr [esp + 8]
0043e555  83f804                   cmp eax, 4
0043e558  7d31                     jge 0x43e58b
0043e55a  31d2                     xor edx, edx
0043e55c  31c0                     xor eax, eax
0043e55e  31db                     xor ebx, ebx
0043e560  668b1424                 mov dx, word ptr [esp]
0043e564  6689f8                   mov ax, di
0043e567  8a5c2404                 mov bl, byte ptr [esp + 4]
0043e56b  c1f808                   sar eax, 8
0043e56e  0314dd08634900           add edx, dword ptr [ebx*8 + 0x496308]
0043e575  0304dd0c634900           add eax, dword ptr [ebx*8 + 0x49630c]
0043e57c  85d2                     test edx, edx
0043e57e  0f8d62ffffff             jge 0x43e4e6
0043e584  b8ffff0000               mov eax, 0xffff
0043e589  eb8c                     jmp 0x43e517
0043e58b  81feff030000             cmp esi, 0x3ff
0043e591  0f8509ffffff             jne 0x43e4a0
0043e597  83c414                   add esp, 0x14
0043e59a  5d                       pop ebp
0043e59b  5f                       pop edi
0043e59c  5e                       pop esi
0043e59d  59                       pop ecx
0043e59e  5b                       pop ebx
0043e59f  c3                       ret
