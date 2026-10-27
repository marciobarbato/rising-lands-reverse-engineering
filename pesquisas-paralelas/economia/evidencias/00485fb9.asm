; iagRessGetPlayerWealth: limite por próximo símbolo SBL, fim exclusivo 0x00485ff9.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00485fb9  53                       push     ebx
00485fba  51                       push     ecx
00485fbb  52                       push     edx
00485fbc  83ec10                   sub      esp, 0x10
00485fbf  8d4c2404                 lea      ecx, [esp + 4]
00485fc3  25ff000000               and      eax, 0xff
00485fc8  8d5c2408                 lea      ebx, [esp + 8]
00485fcc  50                       push     eax
00485fcd  8d542410                 lea      edx, [esp + 0x10]
00485fd1  8d442404                 lea      eax, [esp + 4]
00485fd5  e8c316feff               call     0x46769d
00485fda  31d2                     xor      edx, edx
00485fdc  31c0                     xor      eax, eax
00485fde  668b1424                 mov      dx, word ptr [esp]
00485fe2  668b44240c               mov      ax, word ptr [esp + 0xc]
00485fe7  01c2                     add      edx, eax
00485fe9  31c0                     xor      eax, eax
00485feb  668b442408               mov      ax, word ptr [esp + 8]
00485ff0  01d0                     add      eax, edx
00485ff2  83c410                   add      esp, 0x10
00485ff5  5a                       pop      edx
00485ff6  59                       pop      ecx
00485ff7  5b                       pop      ebx
00485ff8  c3                       ret
