; HerseEstLever; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419379  52                       push edx
0041937a  31d2                     xor edx, edx
0041937c  6689c2                   mov dx, ax
0041937f  89d0                     mov eax, edx
00419381  c1e004                   shl eax, 4
00419384  01d0                     add eax, edx
00419386  c1e002                   shl eax, 2
00419389  01d0                     add eax, edx
0041938b  c1e002                   shl eax, 2
0041938e  05c8a04900               add eax, 0x49a0c8
00419393  8a4076                   mov al, byte ptr [eax + 0x76]
00419396  25ff000000               and eax, 0xff
0041939b  83f81f                   cmp eax, 0x1f
0041939e  7404                     je 0x4193a4
004193a0  85c0                     test eax, eax
004193a2  7504                     jne 0x4193a8
004193a4  b001                     mov al, 1
004193a6  5a                       pop edx
004193a7  c3                       ret
004193a8  30c0                     xor al, al
004193aa  5a                       pop edx
004193ab  c3                       ret
