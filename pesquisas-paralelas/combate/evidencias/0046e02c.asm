; ProjectileExiste; intervalo [0x0046e02c, 0x0046e049)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e02c  52                       push     edx
0046e02d  31d2                     xor      edx, edx
0046e02f  6689c2                   mov      dx, ax
0046e032  89d0                     mov      eax, edx
0046e034  c1e003                   shl      eax, 3
0046e037  29d0                     sub      eax, edx
0046e039  89c2                     mov      edx, eax
0046e03b  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046e040  c1e203                   shl      edx, 3
0046e043  8a440202                 mov      al, byte ptr [edx + eax + 2]
0046e047  5a                       pop      edx
0046e048  c3                       ret
