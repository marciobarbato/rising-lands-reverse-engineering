; EnginGetTimeRecrute; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004410b7  52                       push edx
004410b8  31d2                     xor edx, edx
004410ba  88c2                     mov dl, al
004410bc  89d0                     mov eax, edx
004410be  c1e002                   shl eax, 2
004410c1  29d0                     sub eax, edx
004410c3  c1e003                   shl eax, 3
004410c6  01d0                     add eax, edx
004410c8  668b0445ae654900         mov ax, word ptr [eax*2 + 0x4965ae]
004410d0  5a                       pop edx
004410d1  c3                       ret
