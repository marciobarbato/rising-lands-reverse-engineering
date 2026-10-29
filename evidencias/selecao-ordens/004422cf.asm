; TypeEnginEstAerien; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004422cf  3c10                     cmp al, 0x10
004422d1  7204                     jb 0x4422d7
004422d3  3c11                     cmp al, 0x11
004422d5  76f5                     jbe 0x4422cc
004422d7  30c0                     xor al, al
004422d9  c3                       ret
004422da  b001                     mov al, 1
004422dc  c3                       ret
