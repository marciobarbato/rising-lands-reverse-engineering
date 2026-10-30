; CalculTroupe dispatch and exit 0x4263e5..0x426418; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004263e5  3c05                     cmp al, 5
004263e7  7218                     jb 0x426401
004263e9  0f86a1f8ffff             jbe 0x425c90
004263ef  3c06                     cmp al, 6
004263f1  0f86a2faffff             jbe 0x425e99
004263f7  3c08                     cmp al, 8
004263f9  0f846bfaffff             je 0x425e6a
004263ff  eb0c                     jmp 0x42640d
00426401  3c01                     cmp al, 1
00426403  7208                     jb 0x42640d
00426405  3c02                     cmp al, 2
00426407  0f863ef6ffff             jbe 0x425a4b
0042640d  81c49c000000             add esp, 0x9c
00426413  e90577ffff               jmp 0x41db1d
