; RuntimeRaiz; intervalo [0x0048ff4a, 0x0048ff7f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048ff4a  55                       push     ebp
0048ff4b  89e5                     mov      ebp, esp
0048ff4d  d9e4                     ftst
0048ff4f  83ec10                   sub      esp, 0x10
0048ff52  9b                       wait
0048ff53  dd7df8                   fnstsw   word ptr [ebp - 8]
0048ff56  9b                       wait
0048ff57  668745f8                 xchg     word ptr [ebp - 8], ax
0048ff5b  9e                       sahf
0048ff5c  7319                     jae      0x48ff77
0048ff5e  dd5df0                   fstp     qword ptr [ebp - 0x10]
0048ff61  8b45f8                   mov      eax, dword ptr [ebp - 8]
0048ff64  3c03                     cmp      al, 3
0048ff66  7403                     je       0x48ff6b
0048ff68  dd5df0                   fstp     qword ptr [ebp - 0x10]
0048ff6b  8955fc                   mov      dword ptr [ebp - 4], edx
0048ff6e  e855150000               call     0x4914c8
0048ff73  b001                     mov      al, 1
0048ff75  eb04                     jmp      0x48ff7b
0048ff77  d9fa                     fsqrt
0048ff79  b000                     mov      al, 0
0048ff7b  89ec                     mov      esp, ebp
0048ff7d  5d                       pop      ebp
0048ff7e  c3                       ret
