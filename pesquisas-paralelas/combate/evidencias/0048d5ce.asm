; RuntimeAcos; intervalo [0x0048d5ce, 0x0048d5f1)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048d5ce  d9c0                     fld      st(0)
0048d5d0  d8c8                     fmul     st(0)
0048d5d2  d9e8                     fld1
0048d5d4  dee1                     fsubrp   st(1)
0048d5d6  b001                     mov      al, 1
0048d5d8  e86d290000               call     0x48ff4a
0048d5dd  3c00                     cmp      al, 0
0048d5df  750f                     jne      0x48d5f0
0048d5e1  d9c9                     fxch     st(1)
0048d5e3  e8ff280000               call     0x48fee7
0048d5e8  db2d48904900             fld      xword ptr [0x499048]
0048d5ee  dee1                     fsubrp   st(1)
0048d5f0  c3                       ret
