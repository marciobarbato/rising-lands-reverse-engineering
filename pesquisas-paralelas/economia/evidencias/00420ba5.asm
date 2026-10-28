; SortEnRecrutement: limite por próximo símbolo SBL, fim exclusivo 0x00420bdf.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00420ba5  53                       push     ebx
00420ba6  88c3                     mov      bl, al
00420ba8  31c0                     xor      eax, eax
00420baa  88d0                     mov      al, dl
00420bac  31d2                     xor      edx, edx
00420bae  668b1445e05b4900         mov      dx, word ptr [eax*2 + 0x495be0]
00420bb6  81faffff0000             cmp      edx, 0xffff
00420bbc  741d                     je       0x420bdb
00420bbe  89d0                     mov      eax, edx
00420bc0  c1e004                   shl      eax, 4
00420bc3  01d0                     add      eax, edx
00420bc5  c1e002                   shl      eax, 2
00420bc8  01d0                     add      eax, edx
00420bca  c1e002                   shl      eax, 2
00420bcd  05c8a04900               add      eax, 0x49a0c8
00420bd2  3a587b                   cmp      bl, byte ptr [eax + 0x7b]
00420bd5  7504                     jne      0x420bdb
00420bd7  b001                     mov      al, 1
00420bd9  5b                       pop      ebx
00420bda  c3                       ret
00420bdb  30c0                     xor      al, al
00420bdd  5b                       pop      ebx
00420bde  c3                       ret
