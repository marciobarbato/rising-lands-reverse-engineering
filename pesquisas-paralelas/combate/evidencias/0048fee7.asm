; RuntimeAtan; intervalo [0x0048fee7, 0x0048fefc)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048fee7  d9c9                     fxch     st(1)
0048fee9  f6056c94490001           test     byte ptr [0x49946c], 1
0048fef0  7504                     jne      0x48fef6
0048fef2  d9f3                     fpatan
0048fef4  eb05                     jmp      0x48fefb
0048fef6  e899150000               call     0x491494
0048fefb  c3                       ret
