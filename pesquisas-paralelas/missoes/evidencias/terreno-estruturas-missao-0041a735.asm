; BatimentExiste; intact executable SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a735  52                       push edx
0041a736  31d2                     xor edx, edx
0041a738  6689c2                   mov dx, ax
0041a73b  89d0                     mov eax, edx
0041a73d  c1e004                   shl eax, 4
0041a740  01d0                     add eax, edx
0041a742  c1e002                   shl eax, 2
0041a745  01d0                     add eax, edx
0041a747  c1e002                   shl eax, 2
0041a74a  05c8a04900               add eax, 0x49a0c8
0041a74f  8a4005                   mov al, byte ptr [eax + 5]
0041a752  25ff000000               and eax, 0xff
0041a757  0f95c0                   setne al
0041a75a  5a                       pop edx
0041a75b  c3                       ret
