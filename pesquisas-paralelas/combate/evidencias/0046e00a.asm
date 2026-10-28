; ProjectileReset; intervalo [0x0046e00a, 0x0046e02c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e00a  53                       push     ebx
0046e00b  52                       push     edx
0046e00c  31c0                     xor      eax, eax
0046e00e  eb0f                     jmp      0x46e01f
0046e010  6bda38                   imul     ebx, edx, 0x38
0046e013  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046e019  40                       inc      eax
0046e01a  c6441a0200               mov      byte ptr [edx + ebx + 2], 0
0046e01f  31d2                     xor      edx, edx
0046e021  6689c2                   mov      dx, ax
0046e024  83fa64                   cmp      edx, 0x64
0046e027  7ce7                     jl       0x46e010
0046e029  5a                       pop      edx
0046e02a  5b                       pop      ebx
0046e02b  c3                       ret
