; TypeEnginPeutAttaquer; intervalo [0x00453d7d, 0x00453da2)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00453d7d  81e2ff000000             and      edx, 0xff
00453d83  83fa11                   cmp      edx, 0x11
00453d86  7405                     je       0x453d8d
00453d88  83fa0a                   cmp      edx, 0xa
00453d8b  7503                     jne      0x453d90
00453d8d  30c0                     xor      al, al
00453d8f  c3                       ret
00453d90  83fa10                   cmp      edx, 0x10
00453d93  750a                     jne      0x453d9f
00453d95  3c02                     cmp      al, 2
00453d97  72f4                     jb       0x453d8d
00453d99  7604                     jbe      0x453d9f
00453d9b  3c08                     cmp      al, 8
00453d9d  75ee                     jne      0x453d8d
00453d9f  b001                     mov      al, 1
00453da1  c3                       ret
