; ChercheMurCombinaisons; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041c18a  53                       push ebx
0041c18b  51                       push ecx
0041c18c  52                       push edx
0041c18d  89c2                     mov edx, eax
0041c18f  31db                     xor ebx, ebx
0041c191  8b0d747d5000             mov ecx, dword ptr [0x507d74]
0041c197  6689d3                   mov bx, dx
0041c19a  01cb                     add ebx, ecx
0041c19c  30c0                     xor al, al
0041c19e  8a0df85b4900             mov cl, byte ptr [0x495bf8]
0041c1a4  8a63ff                   mov ah, byte ptr [ebx - 1]
0041c1a7  38cc                     cmp ah, cl
0041c1a9  7408                     je 0x41c1b3
0041c1ab  3a25f95b4900             cmp ah, byte ptr [0x495bf9]
0041c1b1  7502                     jne 0x41c1b5
0041c1b3  0c08                     or al, 8
0041c1b5  31db                     xor ebx, ebx
0041c1b7  8b0d747d5000             mov ecx, dword ptr [0x507d74]
0041c1bd  6689d3                   mov bx, dx
0041c1c0  01cb                     add ebx, ecx
0041c1c2  8a0df85b4900             mov cl, byte ptr [0x495bf8]
0041c1c8  8aa300010000             mov ah, byte ptr [ebx + 0x100]
0041c1ce  38cc                     cmp ah, cl
0041c1d0  7408                     je 0x41c1da
0041c1d2  3a25f95b4900             cmp ah, byte ptr [0x495bf9]
0041c1d8  7502                     jne 0x41c1dc
0041c1da  0c04                     or al, 4
0041c1dc  31c9                     xor ecx, ecx
0041c1de  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c1e4  6689d1                   mov cx, dx
0041c1e7  01cb                     add ebx, ecx
0041c1e9  8a0df85b4900             mov cl, byte ptr [0x495bf8]
0041c1ef  8a6301                   mov ah, byte ptr [ebx + 1]
0041c1f2  38cc                     cmp ah, cl
0041c1f4  7408                     je 0x41c1fe
0041c1f6  3a25f95b4900             cmp ah, byte ptr [0x495bf9]
0041c1fc  7502                     jne 0x41c200
0041c1fe  0c02                     or al, 2
0041c200  31db                     xor ebx, ebx
0041c202  8b0d747d5000             mov ecx, dword ptr [0x507d74]
0041c208  6689d3                   mov bx, dx
0041c20b  01cb                     add ebx, ecx
0041c20d  8a0df85b4900             mov cl, byte ptr [0x495bf8]
0041c213  8aa300ffffff             mov ah, byte ptr [ebx - 0x100]
0041c219  38cc                     cmp ah, cl
0041c21b  7408                     je 0x41c225
0041c21d  3a25f95b4900             cmp ah, byte ptr [0x495bf9]
0041c223  7502                     jne 0x41c227
0041c225  0c01                     or al, 1
0041c227  31db                     xor ebx, ebx
0041c229  8b0d747d5000             mov ecx, dword ptr [0x507d74]
0041c22f  6689d3                   mov bx, dx
0041c232  8a25f95b4900             mov ah, byte ptr [0x495bf9]
0041c238  3a2419                   cmp ah, byte ptr [ecx + ebx]
0041c23b  7506                     jne 0x41c243
0041c23d  30c0                     xor al, al
0041c23f  5a                       pop edx
0041c240  59                       pop ecx
0041c241  5b                       pop ebx
0041c242  c3                       ret
0041c243  31db                     xor ebx, ebx
0041c245  88c3                     mov bl, al
0041c247  85db                     test ebx, ebx
0041c249  7e02                     jle 0x41c24d
0041c24b  fec8                     dec al
0041c24d  5a                       pop edx
0041c24e  59                       pop ecx
0041c24f  5b                       pop ebx
0041c250  c3                       ret
