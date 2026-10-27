; StockPossible: limite por próximo símbolo SBL, fim exclusivo 0x0042302d.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00422fde  53                       push     ebx
00422fdf  51                       push     ecx
00422fe0  52                       push     edx
00422fe1  56                       push     esi
00422fe2  83ec10                   sub      esp, 0x10
00422fe5  8d4c240c                 lea      ecx, [esp + 0xc]
00422fe9  0fb6f0                   movzx    esi, al
00422fec  8d5c2408                 lea      ebx, [esp + 8]
00422ff0  56                       push     esi
00422ff1  8d542408                 lea      edx, [esp + 8]
00422ff5  8d442404                 lea      eax, [esp + 4]
00422ff9  e872460400               call     0x467670
00422ffe  89f0                     mov      eax, esi
00423000  8b1c24                   mov      ebx, dword ptr [esp]
00423003  c1e002                   shl      eax, 2
00423006  8b542404                 mov      edx, dword ptr [esp + 4]
0042300a  29f0                     sub      eax, esi
0042300c  01d3                     add      ebx, edx
0042300e  668b14452efb4d00         mov      dx, word ptr [eax*2 + 0x4dfb2e]
00423016  660faf14452cfb4d00       imul     dx, word ptr [eax*2 + 0x4dfb2c]
0042301f  6639d3                   cmp      bx, dx
00423022  0f92c0                   setb     al
00423025  83c410                   add      esp, 0x10
00423028  5e                       pop      esi
00423029  5a                       pop      edx
0042302a  59                       pop      ecx
0042302b  5b                       pop      ebx
0042302c  c3                       ret
