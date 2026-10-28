; SortilegeGetRayonEffet; intervalo [0x00474734, 0x0047474f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00474734  52                       push     edx
00474735  31d2                     xor      edx, edx
00474737  88c2                     mov      dl, al
00474739  89d0                     mov      eax, edx
0047473b  c1e002                   shl      eax, 2
0047473e  29d0                     sub      eax, edx
00474740  c1e003                   shl      eax, 3
00474743  29d0                     sub      eax, edx
00474745  668b044570714900         mov      ax, word ptr [eax*2 + 0x497170]
0047474d  5a                       pop      edx
0047474e  c3                       ret
