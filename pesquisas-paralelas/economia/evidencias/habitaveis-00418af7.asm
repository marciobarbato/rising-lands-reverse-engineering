; BatimentGetTypeName: Returns 0x495d8c + type*52 + 0x13; exclusive end 0x00418b15.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00418af7  52                       push     edx
00418af8  31d2                     xor      edx, edx
00418afa  88c2                     mov      dl, al
00418afc  89d0                     mov      eax, edx
00418afe  c1e002                   shl      eax, 2
00418b01  29d0                     sub      eax, edx
00418b03  c1e002                   shl      eax, 2
00418b06  01d0                     add      eax, edx
00418b08  c1e002                   shl      eax, 2
00418b0b  058c5d4900               add      eax, 0x495d8c
00418b10  83c013                   add      eax, 0x13
00418b13  5a                       pop      edx
00418b14  c3                       ret
