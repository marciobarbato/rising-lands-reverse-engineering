; I_CombienCouteBatiment: limite por próximo símbolo SBL, fim exclusivo 0x004813b8.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00481399  53                       push     ebx
0048139a  51                       push     ecx
0048139b  52                       push     edx
0048139c  56                       push     esi
0048139d  83ec08                   sub      esp, 8
004813a0  89c6                     mov      esi, eax
004813a2  8d4c2404                 lea      ecx, [esp + 4]
004813a6  8d5c2402                 lea      ebx, [esp + 2]
004813aa  31c0                     xor      eax, eax
004813ac  89e2                     mov      edx, esp
004813ae  8a4604                   mov      al, byte ptr [esi + 4]
004813b1  e81897f9ff               call     0x41aace
004813b6  ebd7                     jmp      0x48138f
