; TerrainEstChampi: limite por próximo símbolo SBL, fim exclusivo 0x0047826c.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00478247  52                       push     edx
00478248  31d2                     xor      edx, edx
0047824a  6689c2                   mov      dx, ax
0047824d  a1747d5000               mov      eax, dword ptr [0x507d74]
00478252  8a0402                   mov      al, byte ptr [edx + eax]
00478255  25ff000000               and      eax, 0xff
0047825a  83f81d                   cmp      eax, 0x1d
0047825d  7c09                     jl       0x478268
0047825f  83f834                   cmp      eax, 0x34
00478262  7f04                     jg       0x478268
00478264  b001                     mov      al, 1
00478266  5a                       pop      edx
00478267  c3                       ret
00478268  30c0                     xor      al, al
0047826a  5a                       pop      edx
0047826b  c3                       ret
