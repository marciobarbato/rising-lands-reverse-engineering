; BatimentTuyauCave / BatimentPorteCave (the +0x75 writers); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a65c  53                       push ebx
0041a65d  88d3                     mov bl, dl
0041a65f  31d2                     xor edx, edx
0041a661  6689c2                   mov dx, ax
0041a664  89d0                     mov eax, edx
0041a666  c1e004                   shl eax, 4
0041a669  01d0                     add eax, edx
0041a66b  c1e002                   shl eax, 2
0041a66e  01d0                     add eax, edx
0041a670  c1e002                   shl eax, 2
0041a673  05c8a04900               add eax, 0x49a0c8
0041a678  885875                   mov byte ptr [eax + 0x75], bl
0041a67b  5b                       pop ebx
0041a67c  c3                       ret
0041a67d  53                       push ebx
0041a67e  88d3                     mov bl, dl
0041a680  31d2                     xor edx, edx
0041a682  6689c2                   mov dx, ax
0041a685  89d0                     mov eax, edx
0041a687  c1e004                   shl eax, 4
0041a68a  01d0                     add eax, edx
0041a68c  c1e002                   shl eax, 2
0041a68f  01d0                     add eax, edx
0041a691  c1e002                   shl eax, 2
0041a694  05c8a04900               add eax, 0x49a0c8
0041a699  31d2                     xor edx, edx
0041a69b  8a5076                   mov dl, byte ptr [eax + 0x76]
0041a69e  85d2                     test edx, edx
0041a6a0  7503                     jne 0x41a6a5
0041a6a2  885875                   mov byte ptr [eax + 0x75], bl
0041a6a5  5b                       pop ebx
0041a6a6  c3                       ret
