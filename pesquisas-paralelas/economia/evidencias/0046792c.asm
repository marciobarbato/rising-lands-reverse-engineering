; EnleveMatiere: limite por próximo símbolo SBL, fim exclusivo 0x0046799c.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0046792c  51                       push     ecx
0046792d  56                       push     esi
0046792e  57                       push     edi
0046792f  88c1                     mov      cl, al
00467931  31c0                     xor      eax, eax
00467933  6689d8                   mov      ax, bx
00467936  0fb6f1                   movzx    esi, cl
00467939  c1e002                   shl      eax, 2
0046793c  01f0                     add      eax, esi
0046793e  c1e003                   shl      eax, 3
00467941  668bb0aa2e4e00           mov      si, word ptr [eax + 0x4e2eaa]
00467948  6639f2                   cmp      dx, si
0046794b  760b                     jbe      0x467958
0046794d  31f6                     xor      esi, esi
0046794f  6689b0aa2e4e00           mov      word ptr [eax + 0x4e2eaa], si
00467956  eb0b                     jmp      0x467963
00467958  89f7                     mov      edi, esi
0046795a  29d7                     sub      edi, edx
0046795c  6689b8aa2e4e00           mov      word ptr [eax + 0x4e2eaa], di
00467963  31c0                     xor      eax, eax
00467965  6689d8                   mov      ax, bx
00467968  31db                     xor      ebx, ebx
0046796a  c1e002                   shl      eax, 2
0046796d  88cb                     mov      bl, cl
0046796f  01d8                     add      eax, ebx
00467971  c1e003                   shl      eax, 3
00467974  668bb8a82e4e00           mov      di, word ptr [eax + 0x4e2ea8]
0046797b  6639fa                   cmp      dx, di
0046797e  760d                     jbe      0x46798d
00467980  31c9                     xor      ecx, ecx
00467982  668988a82e4e00           mov      word ptr [eax + 0x4e2ea8], cx
00467989  5f                       pop      edi
0046798a  5e                       pop      esi
0046798b  59                       pop      ecx
0046798c  c3                       ret
0046798d  89fb                     mov      ebx, edi
0046798f  29d3                     sub      ebx, edx
00467991  668998a82e4e00           mov      word ptr [eax + 0x4e2ea8], bx
00467998  5f                       pop      edi
00467999  5e                       pop      esi
0046799a  59                       pop      ecx
0046799b  c3                       ret
