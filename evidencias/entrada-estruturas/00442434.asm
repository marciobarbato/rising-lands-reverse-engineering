; TypeEnginEstEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00442434  2c0b                     sub al, 0xb
00442436  3c06                     cmp al, 6
00442438  7710                     ja 0x44244a
0044243a  25ff000000               and eax, 0xff
0044243f  2eff248518244400         jmp dword ptr cs:[eax*4 + 0x442418]
00442447  b001                     mov al, 1
00442449  c3                       ret
0044244a  30c0                     xor al, al
0044244c  c3                       ret
