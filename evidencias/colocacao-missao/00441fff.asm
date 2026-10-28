; ExisteEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441fff  52                       push edx
00442000  31d2                     xor edx, edx
00442002  6689c2                   mov dx, ax
00442005  89d0                     mov eax, edx
00442007  c1e004                   shl eax, 4
0044200a  01d0                     add eax, edx
0044200c  c1e002                   shl eax, 2
0044200f  01d0                     add eax, edx
00442011  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00442017  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
0044201b  25ff000000               and eax, 0xff
00442020  0f95c0                   setne al
00442023  5a                       pop edx
00442024  c3                       ret
