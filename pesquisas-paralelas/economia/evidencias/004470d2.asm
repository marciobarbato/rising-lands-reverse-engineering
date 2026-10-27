; BagAccepte: limite por próximo símbolo SBL, fim exclusivo 0x00447107.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004470d2  53                       push     ebx
004470d3  80fa01                   cmp      dl, 1
004470d6  720a                     jb       0x4470e2
004470d8  80fa02                   cmp      dl, 2
004470db  7623                     jbe      0x447100
004470dd  80fa04                   cmp      dl, 4
004470e0  761e                     jbe      0x447100
004470e2  31d2                     xor      edx, edx
004470e4  668b5066                 mov      dx, word ptr [eax + 0x66]
004470e8  81e3ffff0000             and      ebx, 0xffff
004470ee  668b4002                 mov      ax, word ptr [eax + 2]
004470f2  01da                     add      edx, ebx
004470f4  25ffff0000               and      eax, 0xffff
004470f9  39c2                     cmp      edx, eax
004470fb  0f9ec0                   setle    al
004470fe  5b                       pop      ebx
004470ff  c3                       ret
00447100  bb01000000               mov      ebx, 1
00447105  ebdb                     jmp      0x4470e2
