; TypeEnginEstMonstre; intervalo [0x004422dd, 0x004422eb)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004422dd  3c14                     cmp      al, 0x14
004422df  7204                     jb       0x4422e5
004422e1  3c18                     cmp      al, 0x18
004422e3  76f5                     jbe      0x4422da
004422e5  30c0                     xor      al, al
004422e7  c3                       ret
004422e8  b001                     mov      al, 1
004422ea  c3                       ret
