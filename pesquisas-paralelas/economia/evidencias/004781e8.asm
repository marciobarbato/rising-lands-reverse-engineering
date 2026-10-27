; TerrainRecolte: limite por próximo símbolo SBL, fim exclusivo 0x00478247.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004781e8  53                       push     ebx
004781e9  52                       push     edx
004781ea  89c2                     mov      edx, eax
004781ec  31db                     xor      ebx, ebx
004781ee  6689c3                   mov      bx, ax
004781f1  a1747d5000               mov      eax, dword ptr [0x507d74]
004781f6  8a0403                   mov      al, byte ptr [ebx + eax]
004781f9  25ff000000               and      eax, 0xff
004781fe  83f81d                   cmp      eax, 0x1d
00478201  7c09                     jl       0x47820c
00478203  83f835                   cmp      eax, 0x35
00478206  7d04                     jge      0x47820c
00478208  b001                     mov      al, 1
0047820a  eb02                     jmp      0x47820e
0047820c  30c0                     xor      al, al
0047820e  84c0                     test     al, al
00478210  7432                     je       0x478244
00478212  31db                     xor      ebx, ebx
00478214  a1747d5000               mov      eax, dword ptr [0x507d74]
00478219  6689d3                   mov      bx, dx
0047821c  01d8                     add      eax, ebx
0047821e  31db                     xor      ebx, ebx
00478220  8a18                     mov      bl, byte ptr [eax]
00478222  83fb27                   cmp      ebx, 0x27
00478225  7c05                     jl       0x47822c
00478227  83fb33                   cmp      ebx, 0x33
0047822a  7d11                     jge      0x47823d
0047822c  31db                     xor      ebx, ebx
0047822e  a1747d5000               mov      eax, dword ptr [0x507d74]
00478233  6689d3                   mov      bx, dx
00478236  c6040300                 mov      byte ptr [ebx + eax], 0
0047823a  5a                       pop      edx
0047823b  5b                       pop      ebx
0047823c  c3                       ret
0047823d  88da                     mov      dl, bl
0047823f  80ea0a                   sub      dl, 0xa
00478242  8810                     mov      byte ptr [eax], dl
00478244  5a                       pop      edx
00478245  5b                       pop      ebx
00478246  c3                       ret
