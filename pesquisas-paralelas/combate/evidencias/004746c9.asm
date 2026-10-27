; SortilegeGetPortee; intervalo [0x004746c9, 0x004746e4)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004746c9  52                       push     edx
004746ca  31d2                     xor      edx, edx
004746cc  88c2                     mov      dl, al
004746ce  89d0                     mov      eax, edx
004746d0  c1e002                   shl      eax, 2
004746d3  29d0                     sub      eax, edx
004746d5  c1e003                   shl      eax, 3
004746d8  29d0                     sub      eax, edx
004746da  668b04457e714900         mov      ax, word ptr [eax*2 + 0x49717e]
004746e2  5a                       pop      edx
004746e3  c3                       ret
