; CalculGameReinicioContadores; intervalo [0x0042d2ab, 0x0042d2de)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042d2ab  ba12000000               mov      edx, 0x12
0042d2b0  b901000000               mov      ecx, 1
0042d2b5  31c0                     xor      eax, eax
0042d2b7  31db                     xor      ebx, ebx
0042d2b9  a041805000               mov      al, byte ptr [0x508041]
0042d2be  891d7c8f5000             mov      dword ptr [0x508f7c], ebx
0042d2c4  891d808f5000             mov      dword ptr [0x508f80], ebx
0042d2ca  891d848f5000             mov      dword ptr [0x508f84], ebx
0042d2d0  e8e6af0300               call     0x4682bb
0042d2d5  89c8                     mov      eax, ecx
0042d2d7  31d2                     xor      edx, edx
0042d2d9  e852450400               call     0x471830
