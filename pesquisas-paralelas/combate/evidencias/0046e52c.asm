; ProjectileAnim; intervalo [0x0046e52c, 0x0046e5fe)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e52c  53                       push     ebx
0046e52d  51                       push     ecx
0046e52e  52                       push     edx
0046e52f  31d2                     xor      edx, edx
0046e531  6689c2                   mov      dx, ax
0046e534  89d3                     mov      ebx, edx
0046e536  c1e303                   shl      ebx, 3
0046e539  29d3                     sub      ebx, edx
0046e53b  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046e541  c1e303                   shl      ebx, 3
0046e544  01d3                     add      ebx, edx
0046e546  8a03                     mov      al, byte ptr [ebx]
0046e548  3c14                     cmp      al, 0x14
0046e54a  0f8289000000             jb       0x46e5d9
0046e550  3c17                     cmp      al, 0x17
0046e552  7662                     jbe      0x46e5b6
0046e554  3c1b                     cmp      al, 0x1b
0046e556  0f828f000000             jb       0x46e5eb
0046e55c  3c1c                     cmp      al, 0x1c
0046e55e  0f8687000000             jbe      0x46e5eb
0046e564  3c1f                     cmp      al, 0x1f
0046e566  7214                     jb       0x46e57c
0046e568  3c21                     cmp      al, 0x21
0046e56a  0f867b000000             jbe      0x46e5eb
0046e570  3c22                     cmp      al, 0x22
0046e572  0f8473000000             je       0x46e5eb
0046e578  5a                       pop      edx
0046e579  59                       pop      ecx
0046e57a  5b                       pop      ebx
0046e57b  c3                       ret
0046e57c  31d2                     xor      edx, edx
0046e57e  8a5318                   mov      dl, byte ptr [ebx + 0x18]
0046e581  83fa0c                   cmp      edx, 0xc
0046e584  7d0b                     jge      0x46e591
0046e586  88d4                     mov      ah, dl
0046e588  fec4                     inc      ah
0046e58a  886318                   mov      byte ptr [ebx + 0x18], ah
0046e58d  5a                       pop      edx
0046e58e  59                       pop      ecx
0046e58f  5b                       pop      ebx
0046e590  c3                       ret
0046e591  42                       inc      edx
0046e592  b914000000               mov      ecx, 0x14
0046e597  89d0                     mov      eax, edx
0046e599  c1fa1f                   sar      edx, 0x1f
0046e59c  f7f9                     idiv     ecx
0046e59e  885318                   mov      byte ptr [ebx + 0x18], dl
0046e5a1  31d2                     xor      edx, edx
0046e5a3  8a5318                   mov      dl, byte ptr [ebx + 0x18]
0046e5a6  85d2                     test     edx, edx
0046e5a8  0f857affffff             jne      0x46e528
0046e5ae  c643180c                 mov      byte ptr [ebx + 0x18], 0xc
0046e5b2  5a                       pop      edx
0046e5b3  59                       pop      ecx
0046e5b4  5b                       pop      ebx
0046e5b5  c3                       ret
0046e5b6  8a157c8f5000             mov      dl, byte ptr [0x508f7c]
0046e5bc  8a4318                   mov      al, byte ptr [ebx + 0x18]
0046e5bf  00d0                     add      al, dl
0046e5c1  2407                     and      al, 7
0046e5c3  884318                   mov      byte ptr [ebx + 0x18], al
0046e5c6  5a                       pop      edx
0046e5c7  59                       pop      ecx
0046e5c8  5b                       pop      ebx
0046e5c9  c3                       ret
0046e5ca  8a0d7c8f5000             mov      cl, byte ptr [0x508f7c]
0046e5d0  8a4318                   mov      al, byte ptr [ebx + 0x18]
0046e5d3  00c8                     add      al, cl
0046e5d5  2403                     and      al, 3
0046e5d7  ebea                     jmp      0x46e5c3
0046e5d9  3c09                     cmp      al, 9
0046e5db  7215                     jb       0x46e5f2
0046e5dd  3c0d                     cmp      al, 0xd
0046e5df  0f8643ffffff             jbe      0x46e528
0046e5e5  3c11                     cmp      al, 0x11
0046e5e7  7202                     jb       0x46e5eb
0046e5e9  76df                     jbe      0x46e5ca
0046e5eb  fe4318                   inc      byte ptr [ebx + 0x18]
0046e5ee  5a                       pop      edx
0046e5ef  59                       pop      ecx
0046e5f0  5b                       pop      ebx
0046e5f1  c3                       ret
0046e5f2  3c01                     cmp      al, 1
0046e5f4  0f822effffff             jb       0x46e528
0046e5fa  3c05                     cmp      al, 5
0046e5fc  ebeb                     jmp      0x46e5e9
