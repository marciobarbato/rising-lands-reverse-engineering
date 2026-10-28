; HerseEstBaisser; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041934f  52                       push edx
00419350  31d2                     xor edx, edx
00419352  6689c2                   mov dx, ax
00419355  89d0                     mov eax, edx
00419357  c1e004                   shl eax, 4
0041935a  01d0                     add eax, edx
0041935c  c1e002                   shl eax, 2
0041935f  01d0                     add eax, edx
00419361  c1e002                   shl eax, 2
00419364  05c8a04900               add eax, 0x49a0c8
00419369  8a4076                   mov al, byte ptr [eax + 0x76]
0041936c  25ff000000               and eax, 0xff
00419371  83f80f                   cmp eax, 0xf
00419374  0f94c0                   sete al
00419377  5a                       pop edx
00419378  c3                       ret
