; BatimentEnleveMatiere: limite por próximo símbolo SBL, fim exclusivo 0x00423643.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004235bd  51                       push     ecx
004235be  56                       push     esi
004235bf  83ec10                   sub      esp, 0x10
004235c2  31c9                     xor      ecx, ecx
004235c4  88d9                     mov      cl, bl
004235c6  81e2ffff0000             and      edx, 0xffff
004235cc  25ff000000               and      eax, 0xff
004235d1  89ce                     mov      esi, ecx
004235d3  89cb                     mov      ebx, ecx
004235d5  c1e602                   shl      esi, 2
004235d8  e84f430400               call     0x46792c
004235dd  29ce                     sub      esi, ecx
004235df  89c8                     mov      eax, ecx
004235e1  01f6                     add      esi, esi
004235e3  31c8                     xor      eax, ecx
004235e5  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
004235ec  85c0                     test     eax, eax
004235ee  7e4d                     jle      0x42363d
004235f0  8d5c240c                 lea      ebx, [esp + 0xc]
004235f4  8d542404                 lea      edx, [esp + 4]
004235f8  51                       push     ecx
004235f9  8d442404                 lea      eax, [esp + 4]
004235fd  8d4c240c                 lea      ecx, [esp + 0xc]
00423601  e897400400               call     0x46769d
00423606  8b0424                   mov      eax, dword ptr [esp]
00423609  8b542404                 mov      edx, dword ptr [esp + 4]
0042360d  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
00423614  01d0                     add      eax, edx
00423616  31d2                     xor      edx, edx
00423618  66f7f3                   div      bx
0042361b  31d2                     xor      edx, edx
0042361d  6689c2                   mov      dx, ax
00423620  89d0                     mov      eax, edx
00423622  c1e003                   shl      eax, 3
00423625  29d0                     sub      eax, edx
00423627  31db                     xor      ebx, ebx
00423629  89c2                     mov      edx, eax
0042362b  668b9e2efb4d00           mov      bx, word ptr [esi + 0x4dfb2e]
00423632  c1fa1f                   sar      edx, 0x1f
00423635  f7fb                     idiv     ebx
00423637  888630fb4d00             mov      byte ptr [esi + 0x4dfb30], al
0042363d  83c410                   add      esp, 0x10
00423640  5e                       pop      esi
00423641  59                       pop      ecx
00423642  c3                       ret
