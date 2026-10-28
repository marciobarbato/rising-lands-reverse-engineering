; PlayerGetColor; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046003b  25ff000000               and eax, 0xff
00460040  3dc8000000               cmp eax, 0xc8
00460045  7503                     jne 0x46004a
00460047  b01e                     mov al, 0x1e
00460049  c3                       ret
0046004a  8a80dc244e00             mov al, byte ptr [eax + 0x4e24dc]
00460050  c3                       ret
