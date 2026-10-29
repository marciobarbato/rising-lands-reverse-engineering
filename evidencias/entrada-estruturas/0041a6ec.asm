; BatimentGetModeEtat; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a6ec  52                       push edx
0041a6ed  31d2                     xor edx, edx
0041a6ef  6689c2                   mov dx, ax
0041a6f2  89d0                     mov eax, edx
0041a6f4  c1e004                   shl eax, 4
0041a6f7  01d0                     add eax, edx
0041a6f9  c1e002                   shl eax, 2
0041a6fc  01d0                     add eax, edx
0041a6fe  c1e002                   shl eax, 2
0041a701  05c8a04900               add eax, 0x49a0c8
0041a706  8a4005                   mov al, byte ptr [eax + 5]
0041a709  5a                       pop edx
0041a70a  c3                       ret
