; EnginEnRecrutement: limite por próximo símbolo SBL, fim exclusivo 0x00420c19.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00420bdf  53                       push     ebx
00420be0  88c3                     mov      bl, al
00420be2  31c0                     xor      eax, eax
00420be4  88d0                     mov      al, dl
00420be6  31d2                     xor      edx, edx
00420be8  668b1445e05b4900         mov      dx, word ptr [eax*2 + 0x495be0]
00420bf0  81faffff0000             cmp      edx, 0xffff
00420bf6  741d                     je       0x420c15
00420bf8  89d0                     mov      eax, edx
00420bfa  c1e004                   shl      eax, 4
00420bfd  01d0                     add      eax, edx
00420bff  c1e002                   shl      eax, 2
00420c02  01d0                     add      eax, edx
00420c04  c1e002                   shl      eax, 2
00420c07  05c8a04900               add      eax, 0x49a0c8
00420c0c  3a587b                   cmp      bl, byte ptr [eax + 0x7b]
00420c0f  7504                     jne      0x420c15
00420c11  b001                     mov      al, 1
00420c13  5b                       pop      ebx
00420c14  c3                       ret
00420c15  30c0                     xor      al, al
00420c17  5b                       pop      ebx
00420c18  c3                       ret
