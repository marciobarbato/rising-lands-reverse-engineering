; TypeEnginEstTroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00442347  b401                     mov ah, 1
00442349  3c0e                     cmp al, 0xe
0044234b  7217                     jb 0x442364
0044234d  7621                     jbe 0x442370
0044234f  3c12                     cmp al, 0x12
00442351  721d                     jb 0x442370
00442353  7626                     jbe 0x44237b
00442355  3c17                     cmp al, 0x17
00442357  7222                     jb 0x44237b
00442359  3c18                     cmp al, 0x18
0044235b  761e                     jbe 0x44237b
0044235d  3c19                     cmp al, 0x19
0044235f  740f                     je 0x442370
00442361  88e0                     mov al, ah
00442363  c3                       ret
00442364  3c06                     cmp al, 6
00442366  720d                     jb 0x442375
00442368  3c08                     cmp al, 8
0044236a  760f                     jbe 0x44237b
0044236c  3c0b                     cmp al, 0xb
0044236e  720b                     jb 0x44237b
00442370  30e4                     xor ah, ah
00442372  88e0                     mov al, ah
00442374  c3                       ret
00442375  3c03                     cmp al, 3
00442377  7202                     jb 0x44237b
00442379  76f5                     jbe 0x442370
0044237b  b401                     mov ah, 1
0044237d  88e0                     mov al, ah
0044237f  c3                       ret
