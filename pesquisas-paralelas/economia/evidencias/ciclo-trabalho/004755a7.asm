; MineRecolte; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004755a7  53                       push ebx
004755a8  51                       push ecx
004755a9  52                       push edx
004755aa  56                       push esi
004755ab  25ffff0000               and eax, 0xffff
004755b0  e897feffff               call 0x47544c
004755b5  25ffff0000               and eax, 0xffff
004755ba  3dffff0000               cmp eax, 0xffff
004755bf  7458                     je 0x475619
004755c1  c1e002                   shl eax, 2
004755c4  ba01000000               mov edx, 1
004755c9  668b9856995000           mov bx, word ptr [eax + 0x509956]
004755d0  6639d3                   cmp bx, dx
004755d3  760d                     jbe 0x4755e2
004755d5  89de                     mov esi, ebx
004755d7  29d6                     sub esi, edx
004755d9  6689b056995000           mov word ptr [eax + 0x509956], si
004755e0  eb30                     jmp 0x475612
004755e2  31c9                     xor ecx, ecx
004755e4  66898856995000           mov word ptr [eax + 0x509956], cx
004755eb  89da                     mov edx, ebx
004755ed  668b8054995000           mov ax, word ptr [eax + 0x509954]
004755f4  8b1d707d5000             mov ebx, dword ptr [0x507d70]
004755fa  25ffff0000               and eax, 0xffff
004755ff  66c70443db01             mov word ptr [ebx + eax*2], 0x1db
00475605  8b1d707d5000             mov ebx, dword ptr [0x507d70]
0047560b  66c7444302dc01           mov word ptr [ebx + eax*2 + 2], 0x1dc
00475612  89d0                     mov eax, edx
00475614  5e                       pop esi
00475615  5a                       pop edx
00475616  59                       pop ecx
00475617  5b                       pop ebx
00475618  c3                       ret
00475619  31c0                     xor eax, eax
0047561b  5e                       pop esi
0047561c  5a                       pop edx
0047561d  59                       pop ecx
0047561e  5b                       pop ebx
0047561f  c3                       ret
