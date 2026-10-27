; B_TestRessource: limite por próximo símbolo SBL, fim exclusivo 0x00481426.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00481400  53                       push     ebx
00481401  51                       push     ecx
00481402  52                       push     edx
00481403  56                       push     esi
00481404  83ec08                   sub      esp, 8
00481407  89c6                     mov      esi, eax
00481409  31c0                     xor      eax, eax
0048140b  8d4c2406                 lea      ecx, [esp + 6]
0048140f  8a461c                   mov      al, byte ptr [esi + 0x1c]
00481412  8d5c2404                 lea      ebx, [esp + 4]
00481416  50                       push     eax
00481417  8d542406                 lea      edx, [esp + 6]
0048141b  8d442404                 lea      eax, [esp + 4]
0048141f  e84c62feff               call     0x467670
00481424  ebb6                     jmp      0x4813dc
