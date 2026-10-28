; IconeReset; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045e88f  53                       push ebx
0045e890  51                       push ecx
0045e891  52                       push edx
0045e892  56                       push esi
0045e893  57                       push edi
0045e894  83ec04                   sub esp, 4
0045e897  b901000000               mov ecx, 1
0045e89c  31d2                     xor edx, edx
0045e89e  eb21                     jmp 0x45e8c1
0045e8a0  31c0                     xor eax, eax
0045e8a2  6689f0                   mov ax, si
0045e8a5  6bc006                   imul eax, eax, 6
0045e8a8  66899810244e00           mov word ptr [eax + 0x4e2410], bx
0045e8af  66898812244e00           mov word ptr [eax + 0x4e2412], cx
0045e8b6  8b1c24                   mov ebx, dword ptr [esp]
0045e8b9  42                       inc edx
0045e8ba  66899814244e00           mov word ptr [eax + 0x4e2414], bx
0045e8c1  31c0                     xor eax, eax
0045e8c3  6689d0                   mov ax, dx
0045e8c6  83f80a                   cmp eax, 0xa
0045e8c9  7d37                     jge 0x45e902
0045e8cb  6bc006                   imul eax, eax, 6
0045e8ce  31ff                     xor edi, edi
0045e8d0  bbb1290000               mov ebx, 0x29b1
0045e8d5  893c24                   mov dword ptr [esp], edi
0045e8d8  668bb810244e00           mov di, word ptr [eax + 0x4e2410]
0045e8df  89d6                     mov esi, edx
0045e8e1  6639df                   cmp di, bx
0045e8e4  7513                     jne 0x45e8f9
0045e8e6  663b8812244e00           cmp cx, word ptr [eax + 0x4e2412]
0045e8ed  750a                     jne 0x45e8f9
0045e8ef  6683b814244e0000         cmp word ptr [eax + 0x4e2414], 0
0045e8f7  74a7                     je 0x45e8a0
0045e8f9  c605a2054e0001           mov byte ptr [0x4e05a2], 1
0045e900  eb9e                     jmp 0x45e8a0
0045e902  83c404                   add esp, 4
0045e905  5f                       pop edi
0045e906  5e                       pop esi
0045e907  5a                       pop edx
0045e908  59                       pop ecx
0045e909  5b                       pop ebx
0045e90a  c3                       ret
