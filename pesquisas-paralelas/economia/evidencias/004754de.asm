; MineEndWork: limite por próximo símbolo SBL, fim exclusivo 0x00475515.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004754de  52                       push     edx
004754df  25ffff0000               and      eax, 0xffff
004754e4  e863ffffff               call     0x47544c
004754e9  25ffff0000               and      eax, 0xffff
004754ee  3dffff0000               cmp      eax, 0xffff
004754f3  741e                     je       0x475513
004754f5  668b048554995000         mov      ax, word ptr [eax*4 + 0x509954]
004754fd  31d2                     xor      edx, edx
004754ff  6689c2                   mov      dx, ax
00475502  a1ac7d5000               mov      eax, dword ptr [0x507dac]
00475507  fe0c02                   dec      byte ptr [edx + eax]
0047550a  a1ac7d5000               mov      eax, dword ptr [0x507dac]
0047550f  fe4c0201                 dec      byte ptr [edx + eax + 1]
00475513  5a                       pop      edx
00475514  c3                       ret
