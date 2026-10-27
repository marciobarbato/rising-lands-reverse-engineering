; Distance2d; intervalo [0x00479555, 0x004795af)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00479555  56                       push     esi
00479556  6639d8                   cmp      ax, bx
00479559  7613                     jbe      0x47956e
0047955b  31f6                     xor      esi, esi
0047955d  6689c6                   mov      si, ax
00479560  31c0                     xor      eax, eax
00479562  6689d8                   mov      ax, bx
00479565  29c6                     sub      esi, eax
00479567  89f0                     mov      eax, esi
00479569  0fafc6                   imul     eax, esi
0047956c  eb12                     jmp      0x479580
0047956e  81e3ffff0000             and      ebx, 0xffff
00479574  25ffff0000               and      eax, 0xffff
00479579  29c3                     sub      ebx, eax
0047957b  89d8                     mov      eax, ebx
0047957d  0fafc3                   imul     eax, ebx
00479580  6639ca                   cmp      dx, cx
00479583  7614                     jbe      0x479599
00479585  31db                     xor      ebx, ebx
00479587  81e2ffff0000             and      edx, 0xffff
0047958d  6689cb                   mov      bx, cx
00479590  29da                     sub      edx, ebx
00479592  0fafd2                   imul     edx, edx
00479595  01d0                     add      eax, edx
00479597  5e                       pop      esi
00479598  c3                       ret
00479599  31db                     xor      ebx, ebx
0047959b  6689cb                   mov      bx, cx
0047959e  81e2ffff0000             and      edx, 0xffff
004795a4  29d3                     sub      ebx, edx
004795a6  89da                     mov      edx, ebx
004795a8  0fafd3                   imul     edx, ebx
004795ab  01d0                     add      eax, edx
004795ad  5e                       pop      esi
004795ae  c3                       ret
