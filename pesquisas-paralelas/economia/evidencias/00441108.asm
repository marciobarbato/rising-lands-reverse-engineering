; EnginGetVieMax: limite por próximo símbolo SBL, fim exclusivo 0x0044113e.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00441108  52                       push     edx
00441109  31d2                     xor      edx, edx
0044110b  6689c2                   mov      dx, ax
0044110e  89d0                     mov      eax, edx
00441110  c1e004                   shl      eax, 4
00441113  01d0                     add      eax, edx
00441115  c1e002                   shl      eax, 2
00441118  01d0                     add      eax, edx
0044111a  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00441120  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00441124  31d2                     xor      edx, edx
00441126  88c2                     mov      dl, al
00441128  89d0                     mov      eax, edx
0044112a  c1e002                   shl      eax, 2
0044112d  29d0                     sub      eax, edx
0044112f  c1e003                   shl      eax, 3
00441132  01d0                     add      eax, edx
00441134  668b0445b6654900         mov      ax, word ptr [eax*2 + 0x4965b6]
0044113c  5a                       pop      edx
0044113d  c3                       ret
