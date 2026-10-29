; AjouteMatiere; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004678f2  81e3ffff0000             and ebx, 0xffff
004678f8  c1e302                   shl ebx, 2
004678fb  25ff000000               and eax, 0xff
00467900  01d8                     add eax, ebx
00467902  c1e003                   shl eax, 3
00467905  668b98aa2e4e00           mov bx, word ptr [eax + 0x4e2eaa]
0046790c  01d3                     add ebx, edx
0046790e  31d2                     xor edx, edx
00467910  6689da                   mov dx, bx
00467913  668998aa2e4e00           mov word ptr [eax + 0x4e2eaa], bx
0046791a  81fa0f270000             cmp edx, 0x270f
00467920  7e09                     jle 0x46792b
00467922  66c780aa2e4e000f27       mov word ptr [eax + 0x4e2eaa], 0x270f
0046792b  c3                       ret
