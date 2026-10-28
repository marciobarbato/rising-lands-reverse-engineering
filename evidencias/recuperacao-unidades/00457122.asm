; EnginAddVie; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00457122  53                       push ebx
00457123  51                       push ecx
00457124  89d3                     mov ebx, edx
00457126  31d2                     xor edx, edx
00457128  6689c2                   mov dx, ax
0045712b  89d0                     mov eax, edx
0045712d  c1e004                   shl eax, 4
00457130  01d0                     add eax, edx
00457132  c1e002                   shl eax, 2
00457135  01d0                     add eax, edx
00457137  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045713d  c1e002                   shl eax, 2
00457140  01c2                     add edx, eax
00457142  668b8a9a000000           mov cx, word ptr [edx + 0x9a]
00457149  01d9                     add ecx, ebx
0045714b  66898a9a000000           mov word ptr [edx + 0x9a], cx
00457152  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00457158  8a440301                 mov al, byte ptr [ebx + eax + 1]
0045715c  31db                     xor ebx, ebx
0045715e  88c3                     mov bl, al
00457160  89d8                     mov eax, ebx
00457162  c1e002                   shl eax, 2
00457165  29d8                     sub eax, ebx
00457167  c1e003                   shl eax, 3
0045716a  01d8                     add eax, ebx
0045716c  668b0445b6654900         mov ax, word ptr [eax*2 + 0x4965b6]
00457174  6639c8                   cmp ax, cx
00457177  730c                     jae 0x457185
00457179  6689829a000000           mov word ptr [edx + 0x9a], ax
00457180  b001                     mov al, 1
00457182  59                       pop ecx
00457183  5b                       pop ebx
00457184  c3                       ret
00457185  30c0                     xor al, al
00457187  59                       pop ecx
00457188  5b                       pop ebx
00457189  c3                       ret
