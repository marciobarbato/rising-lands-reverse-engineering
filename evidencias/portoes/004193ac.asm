; HerseEstFace; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004193ac  52                       push edx
004193ad  31d2                     xor edx, edx
004193af  6689c2                   mov dx, ax
004193b2  89d0                     mov eax, edx
004193b4  c1e004                   shl eax, 4
004193b7  01d0                     add eax, edx
004193b9  c1e002                   shl eax, 2
004193bc  01d0                     add eax, edx
004193be  c1e002                   shl eax, 2
004193c1  05c8a04900               add eax, 0x49a0c8
004193c6  668b407c                 mov ax, word ptr [eax + 0x7c]
004193ca  25ffff0000               and eax, 0xffff
004193cf  0f94c0                   sete al
004193d2  5a                       pop edx
004193d3  c3                       ret
