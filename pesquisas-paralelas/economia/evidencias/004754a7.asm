; MineSetWork: limite por próximo símbolo SBL, fim exclusivo 0x004754de.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004754a7  52                       push     edx
004754a8  25ffff0000               and      eax, 0xffff
004754ad  e89affffff               call     0x47544c
004754b2  25ffff0000               and      eax, 0xffff
004754b7  3dffff0000               cmp      eax, 0xffff
004754bc  741e                     je       0x4754dc
004754be  668b048554995000         mov      ax, word ptr [eax*4 + 0x509954]
004754c6  31d2                     xor      edx, edx
004754c8  6689c2                   mov      dx, ax
004754cb  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004754d0  fe0402                   inc      byte ptr [edx + eax]
004754d3  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004754d8  fe440201                 inc      byte ptr [edx + eax + 1]
004754dc  5a                       pop      edx
004754dd  c3                       ret
