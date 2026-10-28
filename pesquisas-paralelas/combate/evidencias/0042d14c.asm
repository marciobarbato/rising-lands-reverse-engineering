; CalculGamePortaoMenu; intervalo [0x0042d14c, 0x0042d184)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042d14c  80bc240401000010         cmp      byte ptr [esp + 0x104], 0x10
0042d154  0f8588030000             jne      0x42d4e2
0042d15a  a030074e00               mov      al, byte ptr [0x4e0730]
0042d15f  84c0                     test     al, al
0042d161  0f847b030000             je       0x42d4e2
0042d167  8a25782f4e00             mov      ah, byte ptr [0x4e2f78]
0042d16d  80fc10                   cmp      ah, 0x10
0042d170  0f8468010000             je       0x42d2de
0042d176  80fc12                   cmp      ah, 0x12
0042d179  0f845f010000             je       0x42d2de
0042d17f  e95e030000               jmp      0x42d4e2
