; ProjectileSet; intervalo [0x0046e208, 0x0046e422)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e208  56                       push     esi
0046e209  57                       push     edi
0046e20a  83ec04                   sub      esp, 4
0046e20d  881424                   mov      byte ptr [esp], dl
0046e210  89de                     mov      esi, ebx
0046e212  89cf                     mov      edi, ecx
0046e214  25ffff0000               and      eax, 0xffff
0046e219  89c3                     mov      ebx, eax
0046e21b  c1e303                   shl      ebx, 3
0046e21e  29c3                     sub      ebx, eax
0046e220  a1f0805000               mov      eax, dword ptr [0x5080f0]
0046e225  c1e303                   shl      ebx, 3
0046e228  01c3                     add      ebx, eax
0046e22a  8813                     mov      byte ptr [ebx], dl
0046e22c  66897314                 mov      word ptr [ebx + 0x14], si
0046e230  8a442424                 mov      al, byte ptr [esp + 0x24]
0046e234  66894b16                 mov      word ptr [ebx + 0x16], cx
0046e238  31c9                     xor      ecx, ecx
0046e23a  884323                   mov      byte ptr [ebx + 0x23], al
0046e23d  6689f1                   mov      cx, si
0046e240  be00010000               mov      esi, 0x100
0046e245  89ca                     mov      edx, ecx
0046e247  89c8                     mov      eax, ecx
0046e249  c1fa1f                   sar      edx, 0x1f
0046e24c  f7fe                     idiv     esi
0046e24e  89d0                     mov      eax, edx
0046e250  8b54241a                 mov      edx, dword ptr [esp + 0x1a]
0046e254  c1e005                   shl      eax, 5
0046e257  c1fa10                   sar      edx, 0x10
0046e25a  01d0                     add      eax, edx
0046e25c  89ca                     mov      edx, ecx
0046e25e  6689430c                 mov      word ptr [ebx + 0xc], ax
0046e262  89c8                     mov      eax, ecx
0046e264  c1fa1f                   sar      edx, 0x1f
0046e267  f7fe                     idiv     esi
0046e269  c6430101                 mov      byte ptr [ebx + 1], 1
0046e26d  c7432400000000           mov      dword ptr [ebx + 0x24], 0
0046e274  66c743280000             mov      word ptr [ebx + 0x28], 0
0046e27a  c6430201                 mov      byte ptr [ebx + 2], 1
0046e27e  c6431800                 mov      byte ptr [ebx + 0x18], 0
0046e282  c6430300                 mov      byte ptr [ebx + 3], 0
0046e286  8b54241e                 mov      edx, dword ptr [esp + 0x1e]
0046e28a  c1e005                   shl      eax, 5
0046e28d  c1fa10                   sar      edx, 0x10
0046e290  66c7431a0c00             mov      word ptr [ebx + 0x1a], 0xc
0046e296  01d0                     add      eax, edx
0046e298  6689430e                 mov      word ptr [ebx + 0xe], ax
0046e29c  8b44241c                 mov      eax, dword ptr [esp + 0x1c]
0046e2a0  66894310                 mov      word ptr [ebx + 0x10], ax
0046e2a4  8b442420                 mov      eax, dword ptr [esp + 0x20]
0046e2a8  66894312                 mov      word ptr [ebx + 0x12], ax
0046e2ac  8a442410                 mov      al, byte ptr [esp + 0x10]
0046e2b0  88431f                   mov      byte ptr [ebx + 0x1f], al
0046e2b3  8b442414                 mov      eax, dword ptr [esp + 0x14]
0046e2b7  66894320                 mov      word ptr [ebx + 0x20], ax
0046e2bb  8a442418                 mov      al, byte ptr [esp + 0x18]
0046e2bf  884322                   mov      byte ptr [ebx + 0x22], al
0046e2c2  8a0424                   mov      al, byte ptr [esp]
0046e2c5  c6431900                 mov      byte ptr [ebx + 0x19], 0
0046e2c9  fec8                     dec      al
0046e2cb  66c7431c0000             mov      word ptr [ebx + 0x1c], 0
0046e2d1  3c20                     cmp      al, 0x20
0046e2d3  0f8741010000             ja       0x46e41a
0046e2d9  31d2                     xor      edx, edx
0046e2db  88c2                     mov      dl, al
0046e2dd  2eff249584e14600         jmp      dword ptr cs:[edx*4 + 0x46e184]
0046e2e5  807b2300                 cmp      byte ptr [ebx + 0x23], 0
0046e2e9  0f842b010000             je       0x46e41a
0046e2ef  c7432400320000           mov      dword ptr [ebx + 0x24], 0x3200
0046e2f6  e91f010000               jmp      0x46e41a
0046e2fb  c6430100                 mov      byte ptr [ebx + 1], 0
0046e2ff  66c7431a0500             mov      word ptr [ebx + 0x1a], 5
0046e305  c6430402                 mov      byte ptr [ebx + 4], 2
0046e309  89d8                     mov      eax, ebx
0046e30b  c6431901                 mov      byte ptr [ebx + 0x19], 1
0046e30f  e835fdffff               call     0x46e049
0046e314  66c7431c0500             mov      word ptr [ebx + 0x1c], 5
0046e31a  e9fb000000               jmp      0x46e41a
0046e31f  66c7431a0500             mov      word ptr [ebx + 0x1a], 5
0046e325  c6430402                 mov      byte ptr [ebx + 4], 2
0046e329  89d8                     mov      eax, ebx
0046e32b  c6431901                 mov      byte ptr [ebx + 0x19], 1
0046e32f  e815fdffff               call     0x46e049
0046e334  e9e1000000               jmp      0x46e41a
0046e339  66c7431a0500             mov      word ptr [ebx + 0x1a], 5
0046e33f  c6430402                 mov      byte ptr [ebx + 4], 2
0046e343  89d8                     mov      eax, ebx
0046e345  c6431900                 mov      byte ptr [ebx + 0x19], 0
0046e349  ebe4                     jmp      0x46e32f
0046e34b  c6430100                 mov      byte ptr [ebx + 1], 0
0046e34f  c643040f                 mov      byte ptr [ebx + 4], 0xf
0046e353  89d8                     mov      eax, ebx
0046e355  c6431900                 mov      byte ptr [ebx + 0x19], 0
0046e359  e8ebfcffff               call     0x46e049
0046e35e  66c7431c0a00             mov      word ptr [ebx + 0x1c], 0xa
0046e364  e9b1000000               jmp      0x46e41a
0046e369  c6430100                 mov      byte ptr [ebx + 1], 0
0046e36d  c643040f                 mov      byte ptr [ebx + 4], 0xf
0046e371  89d8                     mov      eax, ebx
0046e373  c6431900                 mov      byte ptr [ebx + 0x19], 0
0046e377  e8cdfcffff               call     0x46e049
0046e37c  66c7431c0a00             mov      word ptr [ebx + 0x1c], 0xa
0046e382  66c7431a1400             mov      word ptr [ebx + 0x1a], 0x14
0046e388  e98d000000               jmp      0x46e41a
0046e38d  c6430100                 mov      byte ptr [ebx + 1], 0
0046e391  c643040f                 mov      byte ptr [ebx + 4], 0xf
0046e395  89d8                     mov      eax, ebx
0046e397  c6431901                 mov      byte ptr [ebx + 0x19], 1
0046e39b  ebbc                     jmp      0x46e359
0046e39d  c643040a                 mov      byte ptr [ebx + 4], 0xa
0046e3a1  eb86                     jmp      0x46e329
0046e3a3  c6430408                 mov      byte ptr [ebx + 4], 8
0046e3a7  eb80                     jmp      0x46e329
0046e3a9  c6430404                 mov      byte ptr [ebx + 4], 4
0046e3ad  e977ffffff               jmp      0x46e329
0046e3b2  89d8                     mov      eax, ebx
0046e3b4  c6431900                 mov      byte ptr [ebx + 0x19], 0
0046e3b8  e88cfcffff               call     0x46e049
0046e3bd  ebc3                     jmp      0x46e382
0046e3bf  31c0                     xor      eax, eax
0046e3c1  e86e630000               call     0x474734
0046e3c6  31c9                     xor      ecx, ecx
0046e3c8  31d2                     xor      edx, edx
0046e3ca  31f6                     xor      esi, esi
0046e3cc  8a4c2414                 mov      cl, byte ptr [esp + 0x14]
0046e3d0  0502000000               add      eax, 2
0046e3d5  6689fe                   mov      si, di
0046e3d8  6689c2                   mov      dx, ax
0046e3db  89cb                     mov      ebx, ecx
0046e3dd  89f0                     mov      eax, esi
0046e3df  e86d840000               call     0x476851
0046e3e4  31c0                     xor      eax, eax
0046e3e6  e849630000               call     0x474734
0046e3eb  31d2                     xor      edx, edx
0046e3ed  89cb                     mov      ebx, ecx
0046e3ef  6689c2                   mov      dx, ax
0046e3f2  89f0                     mov      eax, esi
0046e3f4  e8ba880000               call     0x476cb3
0046e3f9  eb1f                     jmp      0x46e41a
0046e3fb  6a00                     push     0
0046e3fd  31c9                     xor      ecx, ecx
0046e3ff  31f6                     xor      esi, esi
0046e401  31d2                     xor      edx, edx
0046e403  31c0                     xor      eax, eax
0046e405  8a4b22                   mov      cl, byte ptr [ebx + 0x22]
0046e408  668b7320                 mov      si, word ptr [ebx + 0x20]
0046e40c  8a531f                   mov      dl, byte ptr [ebx + 0x1f]
0046e40f  668b4316                 mov      ax, word ptr [ebx + 0x16]
0046e413  89f3                     mov      ebx, esi
0046e415  e85a24feff               call     0x450874
0046e41a  83c404                   add      esp, 4
0046e41d  5f                       pop      edi
0046e41e  5e                       pop      esi
0046e41f  c21800                   ret      0x18
