; TypeEnginEstVehicule; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00442394  2c0b                     sub al, 0xb
00442396  3c04                     cmp al, 4
00442398  7710                     ja 0x4423aa
0044239a  25ff000000               and eax, 0xff
0044239f  2eff248580234400         jmp dword ptr cs:[eax*4 + 0x442380]
004423a7  b001                     mov al, 1
004423a9  c3                       ret
004423aa  30c0                     xor al, al
004423ac  c3                       ret
004423ad  30c0                     xor al, al
004423af  c3                       ret
