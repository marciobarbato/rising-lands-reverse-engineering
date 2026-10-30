; TuyauEstSortie; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x420cae
00420c7c  52                       push     edx
00420c7d  31d2                     xor      edx, edx
00420c7f  6689c2                   mov      dx, ax
00420c82  89d0                     mov      eax, edx
00420c84  c1e004                   shl      eax, 4
00420c87  01d0                     add      eax, edx
00420c89  c1e002                   shl      eax, 2
00420c8c  01d0                     add      eax, edx
00420c8e  c1e002                   shl      eax, 2
00420c91  05c8a04900               add      eax, 0x49a0c8
00420c96  31d2                     xor      edx, edx
00420c98  8a5076                   mov      dl, byte ptr [eax + 0x76]
00420c9b  83fa0f                   cmp      edx, 0xf
00420c9e  750a                     jne      0x420caa
00420ca0  80787500                 cmp      byte ptr [eax + 0x75], 0
00420ca4  7404                     je       0x420caa
00420ca6  b001                     mov      al, 1
00420ca8  5a                       pop      edx
00420ca9  c3                       ret      
00420caa  30c0                     xor      al, al
00420cac  5a                       pop      edx
00420cad  c3                       ret      
