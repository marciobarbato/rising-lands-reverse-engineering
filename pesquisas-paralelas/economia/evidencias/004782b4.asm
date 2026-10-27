; NouvellePatate: limite por próximo símbolo SBL, fim exclusivo 0x00478319.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004782b4  53                       push     ebx
004782b5  52                       push     edx
004782b6  89c2                     mov      edx, eax
004782b8  31db                     xor      ebx, ebx
004782ba  6689c3                   mov      bx, ax
004782bd  a1747d5000               mov      eax, dword ptr [0x507d74]
004782c2  8a0403                   mov      al, byte ptr [ebx + eax]
004782c5  25ff000000               and      eax, 0xff
004782ca  7548                     jne      0x478314
004782cc  a1a87d5000               mov      eax, dword ptr [0x507da8]
004782d1  8a0403                   mov      al, byte ptr [ebx + eax]
004782d4  25ff000000               and      eax, 0xff
004782d9  a801                     test     al, 1
004782db  0f95c0                   setne    al
004782de  84c0                     test     al, al
004782e0  7532                     jne      0x478314
004782e2  b836000000               mov      eax, 0x36
004782e7  e8f081ffff               call     0x4704dc
004782ec  a801                     test     al, 1
004782ee  7510                     jne      0x478300
004782f0  31db                     xor      ebx, ebx
004782f2  a1747d5000               mov      eax, dword ptr [0x507d74]
004782f7  6689d3                   mov      bx, dx
004782fa  c604031d                 mov      byte ptr [ebx + eax], 0x1d
004782fe  eb0f                     jmp      0x47830f
00478300  31c0                     xor      eax, eax
00478302  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
00478308  6689d0                   mov      ax, dx
0047830b  c6040329                 mov      byte ptr [ebx + eax], 0x29
0047830f  b001                     mov      al, 1
00478311  5a                       pop      edx
00478312  5b                       pop      ebx
00478313  c3                       ret
00478314  30c0                     xor      al, al
00478316  5a                       pop      edx
00478317  5b                       pop      ebx
00478318  c3                       ret
