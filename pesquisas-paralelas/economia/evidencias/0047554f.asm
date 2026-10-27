; MineRetire: limite por próximo símbolo SBL, fim exclusivo 0x004755a7.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047554f  53                       push     ebx
00475550  51                       push     ecx
00475551  56                       push     esi
00475552  25ffff0000               and      eax, 0xffff
00475557  c1e002                   shl      eax, 2
0047555a  668b9856995000           mov      bx, word ptr [eax + 0x509956]
00475561  6639da                   cmp      dx, bx
00475564  730d                     jae      0x475573
00475566  89de                     mov      esi, ebx
00475568  29d6                     sub      esi, edx
0047556a  6689b056995000           mov      word ptr [eax + 0x509956], si
00475571  eb2e                     jmp      0x4755a1
00475573  31c9                     xor      ecx, ecx
00475575  89da                     mov      edx, ebx
00475577  66898856995000           mov      word ptr [eax + 0x509956], cx
0047557e  31db                     xor      ebx, ebx
00475580  668b8054995000           mov      ax, word ptr [eax + 0x509954]
00475587  6689c3                   mov      bx, ax
0047558a  a1707d5000               mov      eax, dword ptr [0x507d70]
0047558f  66c70458db01             mov      word ptr [eax + ebx*2], 0x1db
00475595  a1707d5000               mov      eax, dword ptr [0x507d70]
0047559a  66c7445802dc01           mov      word ptr [eax + ebx*2 + 2], 0x1dc
004755a1  89d0                     mov      eax, edx
004755a3  5e                       pop      esi
004755a4  59                       pop      ecx
004755a5  5b                       pop      ebx
004755a6  c3                       ret
