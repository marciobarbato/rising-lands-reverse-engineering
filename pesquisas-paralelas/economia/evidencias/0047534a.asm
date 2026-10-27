; LoadMine: limite por próximo símbolo SBL, fim exclusivo 0x0047539c.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047534a  53                       push     ebx
0047534b  51                       push     ecx
0047534c  52                       push     edx
0047534d  83ec04                   sub      esp, 4
00475350  ba02000000               mov      edx, 2
00475355  89e0                     mov      eax, esp
00475357  e80531feff               call     0x458461
0047535c  31db                     xor      ebx, ebx
0047535e  eb18                     jmp      0x475378
00475360  31c0                     xor      eax, eax
00475362  6689d8                   mov      ax, bx
00475365  c1e002                   shl      eax, 2
00475368  ba04000000               mov      edx, 4
0047536d  0554995000               add      eax, 0x509954
00475372  43                       inc      ebx
00475373  e8e930feff               call     0x458461
00475378  663b1c24                 cmp      bx, word ptr [esp]
0047537c  730d                     jae      0x47538b
0047537e  ebe0                     jmp      0x475360
00475380  31c9                     xor      ecx, ecx
00475382  43                       inc      ebx
00475383  66890c8554995000         mov      word ptr [eax*4 + 0x509954], cx
0047538b  31c0                     xor      eax, eax
0047538d  6689d8                   mov      ax, bx
00475390  83f814                   cmp      eax, 0x14
00475393  7ceb                     jl       0x475380
00475395  83c404                   add      esp, 4
00475398  5a                       pop      edx
00475399  59                       pop      ecx
0047539a  5b                       pop      ebx
0047539b  c3                       ret
