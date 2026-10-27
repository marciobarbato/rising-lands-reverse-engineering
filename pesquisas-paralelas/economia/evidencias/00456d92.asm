; TypeEnginGetNb: limite por próximo símbolo SBL, fim exclusivo 0x00456db5.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00456d92  53                       push     ebx
00456d93  88d3                     mov      bl, dl
00456d95  31d2                     xor      edx, edx
00456d97  88c2                     mov      dl, al
00456d99  89d0                     mov      eax, edx
00456d9b  c1e002                   shl      eax, 2
00456d9e  29d0                     sub      eax, edx
00456da0  c1e002                   shl      eax, 2
00456da3  01d0                     add      eax, edx
00456da5  31d2                     xor      edx, edx
00456da7  88da                     mov      dl, bl
00456da9  01d2                     add      edx, edx
00456dab  668b84823c1a4e00         mov      ax, word ptr [edx + eax*4 + 0x4e1a3c]
00456db3  5b                       pop      ebx
00456db4  c3                       ret
