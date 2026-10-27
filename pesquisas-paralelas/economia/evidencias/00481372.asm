; I_CombienCouteUnite: limite por próximo símbolo SBL, fim exclusivo 0x00481399.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00481372  53                       push     ebx
00481373  51                       push     ecx
00481374  52                       push     edx
00481375  56                       push     esi
00481376  83ec08                   sub      esp, 8
00481379  89c6                     mov      esi, eax
0048137b  8d4c2404                 lea      ecx, [esp + 4]
0048137f  8d5c2402                 lea      ebx, [esp + 2]
00481383  31c0                     xor      eax, eax
00481385  89e2                     mov      edx, esp
00481387  8a4604                   mov      al, byte ptr [esi + 4]
0048138a  e843fdfbff               call     0x4410d2
0048138f  8b16                     mov      edx, dword ptr [esi]
00481391  31c0                     xor      eax, eax
00481393  668b0454                 mov      ax, word ptr [esp + edx*2]
00481397  eb58                     jmp      0x4813f1
