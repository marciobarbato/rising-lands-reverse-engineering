; SortilegeGetTempsFin; intervalo [0x0047474f, 0x0047476a)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047474f  52                       push     edx
00474750  31d2                     xor      edx, edx
00474752  88c2                     mov      dl, al
00474754  89d0                     mov      eax, edx
00474756  c1e002                   shl      eax, 2
00474759  29d0                     sub      eax, edx
0047475b  c1e003                   shl      eax, 3
0047475e  29d0                     sub      eax, edx
00474760  668b044572714900         mov      ax, word ptr [eax*2 + 0x497172]
00474768  5a                       pop      edx
00474769  c3                       ret
