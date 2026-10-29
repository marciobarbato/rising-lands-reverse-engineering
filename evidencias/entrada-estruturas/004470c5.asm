; BagPlein; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004470c5  52                       push edx
004470c6  668b10                   mov dx, word ptr [eax]
004470c9  663b5002                 cmp dx, word ptr [eax + 2]
004470cd  0f94c0                   sete al
004470d0  5a                       pop edx
004470d1  c3                       ret
