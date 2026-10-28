; TypeEnginEstArmee; exclusive end 0x00442347.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Original instruction listing; capacity refresh remains an explicit dependency.
0044230c  3c0f                     cmp      al, 0xf
0044230e  7220                     jb       0x442330
00442310  761b                     jbe      0x44232d
00442312  3c14                     cmp      al, 0x14
00442314  720f                     jb       0x442325
00442316  3c16                     cmp      al, 0x16
00442318  7613                     jbe      0x44232d
0044231a  3c18                     cmp      al, 0x18
0044231c  760f                     jbe      0x44232d
0044231e  3c19                     cmp      al, 0x19
00442320  740b                     je       0x44232d
00442322  30c0                     xor      al, al
00442324  c3                       ret
00442325  3c10                     cmp      al, 0x10
00442327  7604                     jbe      0x44232d
00442329  3c12                     cmp      al, 0x12
0044232b  7217                     jb       0x442344
0044232d  b001                     mov      al, 1
0044232f  c3                       ret
00442330  3c03                     cmp      al, 3
00442332  72f9                     jb       0x44232d
00442334  76f7                     jbe      0x44232d
00442336  3c08                     cmp      al, 8
00442338  720a                     jb       0x442344
0044233a  76f1                     jbe      0x44232d
0044233c  3c0b                     cmp      al, 0xb
0044233e  7204                     jb       0x442344
00442340  3c0c                     cmp      al, 0xc
00442342  76e9                     jbe      0x44232d
00442344  30c0                     xor      al, al
00442346  c3                       ret
