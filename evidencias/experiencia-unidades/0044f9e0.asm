; EnginSetNewExperience; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044f9e0  53                       push ebx
0044f9e1  51                       push ecx
0044f9e2  88d1                     mov cl, dl
0044f9e4  31d2                     xor edx, edx
0044f9e6  6689c2                   mov dx, ax
0044f9e9  89d0                     mov eax, edx
0044f9eb  c1e004                   shl eax, 4
0044f9ee  01d0                     add eax, edx
0044f9f0  c1e002                   shl eax, 2
0044f9f3  01d0                     add eax, edx
0044f9f5  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044f9fb  c1e002                   shl eax, 2
0044f9fe  01c3                     add ebx, eax
0044fa00  80f904                   cmp cl, 4
0044fa03  7782                     ja 0x44f987
0044fa05  31c0                     xor eax, eax
0044fa07  88c8                     mov al, cl
0044fa09  2eff2485ccf94400         jmp dword ptr cs:[eax*4 + 0x44f9cc]
0044fa11  8a4301                   mov al, byte ptr [ebx + 1]
0044fa14  88c4                     mov ah, al
0044fa16  3c0f                     cmp al, 0xf
0044fa18  7220                     jb 0x44fa3a
0044fa1a  761a                     jbe 0x44fa36
0044fa1c  3c14                     cmp al, 0x14
0044fa1e  720e                     jb 0x44fa2e
0044fa20  3c16                     cmp al, 0x16
0044fa22  7612                     jbe 0x44fa36
0044fa24  3c18                     cmp al, 0x18
0044fa26  760e                     jbe 0x44fa36
0044fa28  3c19                     cmp al, 0x19
0044fa2a  740a                     je 0x44fa36
0044fa2c  eb20                     jmp 0x44fa4e
0044fa2e  3c10                     cmp al, 0x10
0044fa30  7604                     jbe 0x44fa36
0044fa32  3c12                     cmp al, 0x12
0044fa34  7218                     jb 0x44fa4e
0044fa36  b001                     mov al, 1
0044fa38  eb16                     jmp 0x44fa50
0044fa3a  3c03                     cmp al, 3
0044fa3c  72f8                     jb 0x44fa36
0044fa3e  76f6                     jbe 0x44fa36
0044fa40  3c08                     cmp al, 8
0044fa42  720a                     jb 0x44fa4e
0044fa44  76f0                     jbe 0x44fa36
0044fa46  3c0b                     cmp al, 0xb
0044fa48  7204                     jb 0x44fa4e
0044fa4a  3c0c                     cmp al, 0xc
0044fa4c  76e8                     jbe 0x44fa36
0044fa4e  30c0                     xor al, al
0044fa50  84c0                     test al, al
0044fa52  740a                     je 0x44fa5e
0044fa54  c683f700000001           mov byte ptr [ebx + 0xf7], 1
0044fa5b  59                       pop ecx
0044fa5c  5b                       pop ebx
0044fa5d  c3                       ret
0044fa5e  31d2                     xor edx, edx
0044fa60  8a5301                   mov dl, byte ptr [ebx + 1]
0044fa63  89d0                     mov eax, edx
0044fa65  c1e002                   shl eax, 2
0044fa68  29d0                     sub eax, edx
0044fa6a  c1e003                   shl eax, 3
0044fa6d  01d0                     add eax, edx
0044fa6f  31d2                     xor edx, edx
0044fa71  668b1445dc654900         mov dx, word ptr [eax*2 + 0x4965dc]
0044fa79  b964000000               mov ecx, 0x64
0044fa7e  89d0                     mov eax, edx
0044fa80  c1fa1f                   sar edx, 0x1f
0044fa83  f7f9                     idiv ecx
0044fa85  8883f8000000             mov byte ptr [ebx + 0xf8], al
0044fa8b  59                       pop ecx
0044fa8c  5b                       pop ebx
0044fa8d  c3                       ret
0044fa8e  c683f600000001           mov byte ptr [ebx + 0xf6], 1
0044fa95  59                       pop ecx
0044fa96  5b                       pop ebx
0044fa97  c3                       ret
0044fa98  c683f500000001           mov byte ptr [ebx + 0xf5], 1
0044fa9f  59                       pop ecx
0044faa0  5b                       pop ebx
0044faa1  c3                       ret
0044faa2  8a4301                   mov al, byte ptr [ebx + 1]
0044faa5  3c0f                     cmp al, 0xf
0044faa7  7220                     jb 0x44fac9
0044faa9  761a                     jbe 0x44fac5
0044faab  3c14                     cmp al, 0x14
0044faad  720e                     jb 0x44fabd
0044faaf  3c16                     cmp al, 0x16
0044fab1  7612                     jbe 0x44fac5
0044fab3  3c18                     cmp al, 0x18
0044fab5  760e                     jbe 0x44fac5
0044fab7  3c19                     cmp al, 0x19
0044fab9  740a                     je 0x44fac5
0044fabb  eb20                     jmp 0x44fadd
0044fabd  3c10                     cmp al, 0x10
0044fabf  7604                     jbe 0x44fac5
0044fac1  3c12                     cmp al, 0x12
0044fac3  7218                     jb 0x44fadd
0044fac5  b001                     mov al, 1
0044fac7  eb16                     jmp 0x44fadf
0044fac9  3c03                     cmp al, 3
0044facb  72f8                     jb 0x44fac5
0044facd  76f6                     jbe 0x44fac5
0044facf  3c08                     cmp al, 8
0044fad1  720a                     jb 0x44fadd
0044fad3  76f0                     jbe 0x44fac5
0044fad5  3c0b                     cmp al, 0xb
0044fad7  7204                     jb 0x44fadd
0044fad9  3c0c                     cmp al, 0xc
0044fadb  76e8                     jbe 0x44fac5
0044fadd  30c0                     xor al, al
0044fadf  84c0                     test al, al
0044fae1  0f8577ffffff             jne 0x44fa5e
0044fae7  31d2                     xor edx, edx
0044fae9  8a5301                   mov dl, byte ptr [ebx + 1]
0044faec  89d0                     mov eax, edx
0044faee  c1e002                   shl eax, 2
0044faf1  29d0                     sub eax, edx
0044faf3  c1e003                   shl eax, 3
0044faf6  01d0                     add eax, edx
0044faf8  31d2                     xor edx, edx
0044fafa  668b1445dc654900         mov dx, word ptr [eax*2 + 0x4965dc]
0044fb02  01d2                     add edx, edx
0044fb04  e970ffffff               jmp 0x44fa79
