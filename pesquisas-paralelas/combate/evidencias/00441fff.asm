; ExisteEngin_EnginGetType; intervalo [0x00441fff, 0x00442045)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441fff  52                       push     edx
00442000  31d2                     xor      edx, edx
00442002  6689c2                   mov      dx, ax
00442005  89d0                     mov      eax, edx
00442007  c1e004                   shl      eax, 4
0044200a  01d0                     add      eax, edx
0044200c  c1e002                   shl      eax, 2
0044200f  01d0                     add      eax, edx
00442011  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00442017  8a448202                 mov      al, byte ptr [edx + eax*4 + 2]
0044201b  25ff000000               and      eax, 0xff
00442020  0f95c0                   setne    al
00442023  5a                       pop      edx
00442024  c3                       ret
00442025  52                       push     edx
00442026  31d2                     xor      edx, edx
00442028  6689c2                   mov      dx, ax
0044202b  89d0                     mov      eax, edx
0044202d  c1e004                   shl      eax, 4
00442030  01d0                     add      eax, edx
00442032  c1e002                   shl      eax, 2
00442035  01c2                     add      edx, eax
00442037  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0044203c  c1e202                   shl      edx, 2
0044203f  8a440201                 mov      al, byte ptr [edx + eax + 1]
00442043  5a                       pop      edx
00442044  c3                       ret
