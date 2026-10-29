; BatimentEnDestruction; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a70b  52                       push edx
0041a70c  31d2                     xor edx, edx
0041a70e  6689c2                   mov dx, ax
0041a711  89d0                     mov eax, edx
0041a713  c1e004                   shl eax, 4
0041a716  01d0                     add eax, edx
0041a718  c1e002                   shl eax, 2
0041a71b  01d0                     add eax, edx
0041a71d  c1e002                   shl eax, 2
0041a720  05c8a04900               add eax, 0x49a0c8
0041a725  8a4005                   mov al, byte ptr [eax + 5]
0041a728  25ff000000               and eax, 0xff
0041a72d  83f803                   cmp eax, 3
0041a730  0f94c0                   sete al
0041a733  5a                       pop edx
0041a734  c3                       ret
