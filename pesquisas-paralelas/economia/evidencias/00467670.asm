; GetRessource: limite por próximo símbolo SBL, fim exclusivo 0x0046769d.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00467670  56                       push     esi
00467671  57                       push     edi
00467672  89c6                     mov      esi, eax
00467674  31c0                     xor      eax, eax
00467676  8a44240c                 mov      al, byte ptr [esp + 0xc]
0046767a  c1e005                   shl      eax, 5
0046767d  668bb8b22e4e00           mov      di, word ptr [eax + 0x4e2eb2]
00467684  66893e                   mov      word ptr [esi], di
00467687  668bb0ba2e4e00           mov      si, word ptr [eax + 0x4e2eba]
0046768e  668932                   mov      word ptr [edx], si
00467691  668b80aa2e4e00           mov      ax, word ptr [eax + 0x4e2eaa]
00467698  668903                   mov      word ptr [ebx], ax
0046769b  ebc9                     jmp      0x467666
