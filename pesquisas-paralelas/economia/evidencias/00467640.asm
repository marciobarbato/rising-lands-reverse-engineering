; GetRessourceRMI: limite por próximo símbolo SBL, fim exclusivo 0x00467670.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00467640  56                       push     esi
00467641  57                       push     edi
00467642  89c6                     mov      esi, eax
00467644  31c0                     xor      eax, eax
00467646  8a44240c                 mov      al, byte ptr [esp + 0xc]
0046764a  c1e005                   shl      eax, 5
0046764d  668bb8b02e4e00           mov      di, word ptr [eax + 0x4e2eb0]
00467654  66893e                   mov      word ptr [esi], di
00467657  668b80b82e4e00           mov      ax, word ptr [eax + 0x4e2eb8]
0046765e  668902                   mov      word ptr [edx], ax
00467661  66c7030000               mov      word ptr [ebx], 0
00467666  66c7010000               mov      word ptr [ecx], 0
0046766b  5f                       pop      edi
0046766c  5e                       pop      esi
0046766d  c20400                   ret      4
