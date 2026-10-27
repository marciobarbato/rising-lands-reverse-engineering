; LoadMissionMine: limite por próximo símbolo SBL, fim exclusivo 0x00475402.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047539c  53                       push     ebx
0047539d  51                       push     ecx
0047539e  52                       push     edx
0047539f  83ec04                   sub      esp, 4
004753a2  baa74d4900               mov      edx, 0x494da7
004753a7  e87430feff               call     0x458420
004753ac  25ff000000               and      eax, 0xff
004753b1  83f801                   cmp      eax, 1
004753b4  75df                     jne      0x475395
004753b6  ba02000000               mov      edx, 2
004753bb  89e0                     mov      eax, esp
004753bd  e89f30feff               call     0x458461
004753c2  31db                     xor      ebx, ebx
004753c4  eb18                     jmp      0x4753de
004753c6  31c0                     xor      eax, eax
004753c8  6689d8                   mov      ax, bx
004753cb  c1e002                   shl      eax, 2
004753ce  ba04000000               mov      edx, 4
004753d3  0554995000               add      eax, 0x509954
004753d8  43                       inc      ebx
004753d9  e88330feff               call     0x458461
004753de  663b1c24                 cmp      bx, word ptr [esp]
004753e2  730d                     jae      0x4753f1
004753e4  ebe0                     jmp      0x4753c6
004753e6  31c9                     xor      ecx, ecx
004753e8  43                       inc      ebx
004753e9  66890c8554995000         mov      word ptr [eax*4 + 0x509954], cx
004753f1  31c0                     xor      eax, eax
004753f3  6689d8                   mov      ax, bx
004753f6  83f814                   cmp      eax, 0x14
004753f9  7ceb                     jl       0x4753e6
004753fb  e84c30feff               call     0x45844c
00475400  eb93                     jmp      0x475395
