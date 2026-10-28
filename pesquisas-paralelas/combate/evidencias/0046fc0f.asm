; ProjectileCalcul; intervalo [0x0046fc0f, 0x0046fc8b)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046fc0f  53                       push     ebx
0046fc10  51                       push     ecx
0046fc11  52                       push     edx
0046fc12  31d2                     xor      edx, edx
0046fc14  eb06                     jmp      0x46fc1c
0046fc16  e811e9ffff               call     0x46e52c
0046fc1b  42                       inc      edx
0046fc1c  31c0                     xor      eax, eax
0046fc1e  6689d0                   mov      ax, dx
0046fc21  83f864                   cmp      eax, 0x64
0046fc24  7cf0                     jl       0x46fc16
0046fc26  31c9                     xor      ecx, ecx
0046fc28  eb01                     jmp      0x46fc2b
0046fc2a  41                       inc      ecx
0046fc2b  31c0                     xor      eax, eax
0046fc2d  6689c8                   mov      ax, cx
0046fc30  83f81e                   cmp      eax, 0x1e
0046fc33  0f8dbbeeffff             jge      0x46eaf4
0046fc39  31d2                     xor      edx, edx
0046fc3b  eb01                     jmp      0x46fc3e
0046fc3d  42                       inc      edx
0046fc3e  31c0                     xor      eax, eax
0046fc40  6689d0                   mov      ax, dx
0046fc43  83f864                   cmp      eax, 0x64
0046fc46  7d1e                     jge      0x46fc66
0046fc48  6bd838                   imul     ebx, eax, 0x38
0046fc4b  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046fc50  01d8                     add      eax, ebx
0046fc52  8a5802                   mov      bl, byte ptr [eax + 2]
0046fc55  84db                     test     bl, bl
0046fc57  74e4                     je       0x46fc3d
0046fc59  80780100                 cmp      byte ptr [eax + 1], 0
0046fc5d  75de                     jne      0x46fc3d
0046fc5f  e894eeffff               call     0x46eaf8
0046fc64  ebd7                     jmp      0x46fc3d
0046fc66  31d2                     xor      edx, edx
0046fc68  eb01                     jmp      0x46fc6b
0046fc6a  42                       inc      edx
0046fc6b  31c0                     xor      eax, eax
0046fc6d  6689d0                   mov      ax, dx
0046fc70  83f864                   cmp      eax, 0x64
0046fc73  7db5                     jge      0x46fc2a
0046fc75  6bd838                   imul     ebx, eax, 0x38
0046fc78  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046fc7d  01d8                     add      eax, ebx
0046fc7f  80780100                 cmp      byte ptr [eax + 1], 0
0046fc83  74e5                     je       0x46fc6a
0046fc85  c6400100                 mov      byte ptr [eax + 1], 0
0046fc89  ebdf                     jmp      0x46fc6a
