; TypeEnginEstEnLoop; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00440c44  2c0b                     sub al, 0xb
00440c46  3c05                     cmp al, 5
00440c48  7710                     ja 0x440c5a
00440c4a  25ff000000               and eax, 0xff
00440c4f  2eff24852c0c4400         jmp dword ptr cs:[eax*4 + 0x440c2c]
00440c57  b001                     mov al, 1
00440c59  c3                       ret
00440c5a  30c0                     xor al, al
00440c5c  c3                       ret
