; TypeEnginEstAPied; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004423b0  3c0c                     cmp al, 0xc
004423b2  7211                     jb 0x4423c5
004423b4  3c0d                     cmp al, 0xd
004423b6  76f5                     jbe 0x4423ad
004423b8  3c0f                     cmp al, 0xf
004423ba  72f1                     jb 0x4423ad
004423bc  76ef                     jbe 0x4423ad
004423be  3c11                     cmp al, 0x11
004423c0  76eb                     jbe 0x4423ad
004423c2  b001                     mov al, 1
004423c4  c3                       ret
004423c5  3c03                     cmp al, 3
004423c7  7206                     jb 0x4423cf
004423c9  76e2                     jbe 0x4423ad
004423cb  3c0b                     cmp al, 0xb
004423cd  74de                     je 0x4423ad
004423cf  b001                     mov al, 1
004423d1  c3                       ret
004423d2  30c0                     xor al, al
004423d4  c3                       ret
