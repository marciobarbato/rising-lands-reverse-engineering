; HerseEnAnimation; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004191fd  52                       push edx
004191fe  31d2                     xor edx, edx
00419200  6689c2                   mov dx, ax
00419203  89d0                     mov eax, edx
00419205  c1e004                   shl eax, 4
00419208  01d0                     add eax, edx
0041920a  c1e002                   shl eax, 2
0041920d  01d0                     add eax, edx
0041920f  c1e002                   shl eax, 2
00419212  05c8a04900               add eax, 0x49a0c8
00419217  8a4076                   mov al, byte ptr [eax + 0x76]
0041921a  25ff000000               and eax, 0xff
0041921f  740e                     je 0x41922f
00419221  83f80f                   cmp eax, 0xf
00419224  7409                     je 0x41922f
00419226  83f81f                   cmp eax, 0x1f
00419229  7404                     je 0x41922f
0041922b  b001                     mov al, 1
0041922d  5a                       pop edx
0041922e  c3                       ret
0041922f  30c0                     xor al, al
00419231  5a                       pop edx
00419232  c3                       ret
