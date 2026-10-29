; BatimentEstEnnemi; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a61c  53                       push ebx
0041a61d  88d3                     mov bl, dl
0041a61f  31d2                     xor edx, edx
0041a621  6689c2                   mov dx, ax
0041a624  89d0                     mov eax, edx
0041a626  c1e004                   shl eax, 4
0041a629  01d0                     add eax, edx
0041a62b  c1e002                   shl eax, 2
0041a62e  01d0                     add eax, edx
0041a630  c1e002                   shl eax, 2
0041a633  05c8a04900               add eax, 0x49a0c8
0041a638  8a4004                   mov al, byte ptr [eax + 4]
0041a63b  25ff000000               and eax, 0xff
0041a640  3dc8000000               cmp eax, 0xc8
0041a645  740d                     je 0x41a654
0041a647  31d2                     xor edx, edx
0041a649  88da                     mov dl, bl
0041a64b  e8e8310500               call 0x46d838
0041a650  84c0                     test al, al
0041a652  7404                     je 0x41a658
0041a654  30c0                     xor al, al
0041a656  5b                       pop ebx
0041a657  c3                       ret
0041a658  b001                     mov al, 1
0041a65a  5b                       pop ebx
0041a65b  c3                       ret
