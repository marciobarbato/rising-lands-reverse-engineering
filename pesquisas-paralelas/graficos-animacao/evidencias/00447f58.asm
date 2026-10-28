; AnimWorkEngin [0x447f58, 0x448088)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447f58  53                     push     ebx
00447f59  51                     push     ecx
00447f5a  52                     push     edx
00447f5b  31d2                   xor      edx, edx
00447f5d  6689c2                 mov      dx, ax
00447f60  89d3                   mov      ebx, edx
00447f62  c1e304                 shl      ebx, 4
00447f65  01d3                   add      ebx, edx
00447f67  c1e302                 shl      ebx, 2
00447f6a  01d3                   add      ebx, edx
00447f6c  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00447f72  c1e302                 shl      ebx, 2
00447f75  01d3                   add      ebx, edx
00447f77  8a4301                 mov      al, byte ptr [ebx + 1]
00447f7a  3c06                   cmp      al, 6
00447f7c  0f82fe000000           jb       0x448080
00447f82  0f86fc000000           jbe      0x448084
00447f88  3c07                   cmp      al, 7
00447f8a  0f86d6000000           jbe      0x448066
00447f90  3c0d                   cmp      al, 0xd
00447f92  745e                   je       0x447ff2
00447f94  5a                     pop      edx
00447f95  59                     pop      ecx
00447f96  5b                     pop      ebx
00447f97  c3                     ret
00447f98  8ab3a9000000           mov      dh, byte ptr [ebx + 0xa9]
00447f9e  fec6                   inc      dh
00447fa0  8a8ba7000000           mov      cl, byte ptr [ebx + 0xa7]
00447fa6  88b3a9000000           mov      byte ptr [ebx + 0xa9], dh
00447fac  38ce                   cmp      dh, cl
00447fae  0f85d0000000           jne      0x448084
00447fb4  31d2                   xor      edx, edx
00447fb6  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447fbc  42                     inc      edx
00447fbd  b904000000             mov      ecx, 4
00447fc2  89d0                   mov      eax, edx
00447fc4  c1fa1f                 sar      edx, 0x1f
00447fc7  f7f9                   idiv     ecx
00447fc9  c683a900000000         mov      byte ptr [ebx + 0xa9], 0
00447fd0  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00447fd6  5a                     pop      edx
00447fd7  59                     pop      ecx
00447fd8  5b                     pop      ebx
00447fd9  c3                     ret
00447fda  8aa3a9000000           mov      ah, byte ptr [ebx + 0xa9]
00447fe0  fec4                   inc      ah
00447fe2  8a93a7000000           mov      dl, byte ptr [ebx + 0xa7]
00447fe8  88a3a9000000           mov      byte ptr [ebx + 0xa9], ah
00447fee  38d4                   cmp      ah, dl
00447ff0  ebbc                   jmp      0x447fae ;
00447ff2  8a8389000000           mov      al, byte ptr [ebx + 0x89]
00447ff8  3c04                   cmp      al, 4
00447ffa  0f8784000000           ja       0x448084
00448000  31d2                   xor      edx, edx
00448002  88c2                   mov      dl, al
00448004  2eff2495347f4400       jmp      dword ptr cs:[edx*4 + 0x447f34]
0044800c  8a93a9000000           mov      dl, byte ptr [ebx + 0xa9]
00448012  fec2                   inc      dl
00448014  8893a9000000           mov      byte ptr [ebx + 0xa9], dl
0044801a  3a93a7000000           cmp      dl, byte ptr [ebx + 0xa7]
00448020  eb8c                   jmp      0x447fae ;
00448022  8a8389000000           mov      al, byte ptr [ebx + 0x89]
00448028  3c03                   cmp      al, 3
0044802a  7758                   ja       0x448084
0044802c  31d2                   xor      edx, edx
0044802e  88c2                   mov      dl, al
00448030  2eff2495487f4400       jmp      dword ptr cs:[edx*4 + 0x447f48]
00448038  8aaba9000000           mov      ch, byte ptr [ebx + 0xa9]
0044803e  fec5                   inc      ch
00448040  8aa3a7000000           mov      ah, byte ptr [ebx + 0xa7]
00448046  88aba9000000           mov      byte ptr [ebx + 0xa9], ch
0044804c  38e5                   cmp      ch, ah
0044804e  7534                   jne      0x448084
00448050  31d2                   xor      edx, edx
00448052  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00448058  31c9                   xor      ecx, ecx
0044805a  42                     inc      edx
0044805b  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
00448061  e95cffffff             jmp      0x447fc2 ;
00448066  8a8389000000           mov      al, byte ptr [ebx + 0x89]
0044806c  3c02                   cmp      al, 2
0044806e  7214                   jb       0x448084
00448070  7612                   jbe      0x448084
00448072  3c04                   cmp      al, 4
00448074  720e                   jb       0x448084
00448076  760c                   jbe      0x448084
00448078  3c0c                   cmp      al, 0xc
0044807a  74bc                   je       0x448038
0044807c  5a                     pop      edx
0044807d  59                     pop      ecx
0044807e  5b                     pop      ebx
0044807f  c3                     ret
00448080  3c05                   cmp      al, 5
00448082  749e                   je       0x448022
00448084  5a                     pop      edx
00448085  59                     pop      ecx
00448086  5b                     pop      ebx
00448087  c3                     ret
