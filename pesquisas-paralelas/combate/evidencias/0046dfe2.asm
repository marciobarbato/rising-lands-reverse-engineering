; SaveProjectile; intervalo [0x0046dfe2, 0x0046e00a)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046dfe2  53                       push     ebx
0046dfe3  52                       push     edx
0046dfe4  31db                     xor      ebx, ebx
0046dfe6  eb15                     jmp      0x46dffd
0046dfe8  6bd038                   imul     edx, eax, 0x38
0046dfeb  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046dff0  01d0                     add      eax, edx
0046dff2  ba38000000               mov      edx, 0x38
0046dff7  43                       inc      ebx
0046dff8  e879a4feff               call     0x458476
0046dffd  31c0                     xor      eax, eax
0046dfff  6689d8                   mov      ax, bx
0046e002  83f864                   cmp      eax, 0x64
0046e005  7ce1                     jl       0x46dfe8
0046e007  5a                       pop      edx
0046e008  5b                       pop      ebx
0046e009  c3                       ret
