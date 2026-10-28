; LoadProjectile; intervalo [0x0046dfba, 0x0046dfe2)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046dfba  53                       push     ebx
0046dfbb  52                       push     edx
0046dfbc  31db                     xor      ebx, ebx
0046dfbe  eb15                     jmp      0x46dfd5
0046dfc0  6bd038                   imul     edx, eax, 0x38
0046dfc3  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046dfc8  01d0                     add      eax, edx
0046dfca  ba38000000               mov      edx, 0x38
0046dfcf  43                       inc      ebx
0046dfd0  e88ca4feff               call     0x458461
0046dfd5  31c0                     xor      eax, eax
0046dfd7  6689d8                   mov      ax, bx
0046dfda  83f864                   cmp      eax, 0x64
0046dfdd  7ce1                     jl       0x46dfc0
0046dfdf  5a                       pop      edx
0046dfe0  5b                       pop      ebx
0046dfe1  c3                       ret
