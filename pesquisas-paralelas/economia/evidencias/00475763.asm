; TerrainAccepteSac: limite por próximo símbolo SBL, fim exclusivo 0x004757af.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00475763  53                       push     ebx
00475764  51                       push     ecx
00475765  89c3                     mov      ebx, eax
00475767  31c9                     xor      ecx, ecx
00475769  6689c1                   mov      cx, ax
0047576c  a1747d5000               mov      eax, dword ptr [0x507d74]
00475771  01c8                     add      eax, ecx
00475773  8a30                     mov      dh, byte ptr [eax]
00475775  38f2                     cmp      dl, dh
00475777  7409                     je       0x475782
00475779  88f0                     mov      al, dh
0047577b  25ff000000               and      eax, 0xff
00475780  7528                     jne      0x4757aa
00475782  31c0                     xor      eax, eax
00475784  6689d8                   mov      ax, bx
00475787  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
0047578d  3a1403                   cmp      dl, byte ptr [ebx + eax]
00475790  7513                     jne      0x4757a5
00475792  8b1dac7d5000             mov      ebx, dword ptr [0x507dac]
00475798  8a0403                   mov      al, byte ptr [ebx + eax]
0047579b  25ff000000               and      eax, 0xff
004757a0  83f81f                   cmp      eax, 0x1f
004757a3  7405                     je       0x4757aa
004757a5  b001                     mov      al, 1
004757a7  59                       pop      ecx
004757a8  5b                       pop      ebx
004757a9  c3                       ret
004757aa  30c0                     xor      al, al
004757ac  59                       pop      ecx
004757ad  5b                       pop      ebx
004757ae  c3                       ret
