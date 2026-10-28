; BatimentGetPlayer; [0x41a08c,0x41a0ab)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a08c  52                       push     edx
0041a08d  31d2                     xor      edx, edx
0041a08f  6689c2                   mov      dx, ax
0041a092  89d0                     mov      eax, edx
0041a094  c1e004                   shl      eax, 4
0041a097  01d0                     add      eax, edx
0041a099  c1e002                   shl      eax, 2
0041a09c  01d0                     add      eax, edx
0041a09e  c1e002                   shl      eax, 2
0041a0a1  05c8a04900               add      eax, 0x49a0c8
0041a0a6  8a4004                   mov      al, byte ptr [eax + 4]
0041a0a9  5a                       pop      edx
0041a0aa  c3                       ret
