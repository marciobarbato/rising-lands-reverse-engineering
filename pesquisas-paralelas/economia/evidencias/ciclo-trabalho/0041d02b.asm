; BatimentEstNeutre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041d02b  52                       push edx
0041d02c  31d2                     xor edx, edx
0041d02e  6689c2                   mov dx, ax
0041d031  89d0                     mov eax, edx
0041d033  c1e004                   shl eax, 4
0041d036  01d0                     add eax, edx
0041d038  c1e002                   shl eax, 2
0041d03b  01d0                     add eax, edx
0041d03d  c1e002                   shl eax, 2
0041d040  05c8a04900               add eax, 0x49a0c8
0041d045  8a4004                   mov al, byte ptr [eax + 4]
0041d048  25ff000000               and eax, 0xff
0041d04d  3dc8000000               cmp eax, 0xc8
0041d052  0f94c0                   sete al
0041d055  5a                       pop edx
0041d056  c3                       ret
