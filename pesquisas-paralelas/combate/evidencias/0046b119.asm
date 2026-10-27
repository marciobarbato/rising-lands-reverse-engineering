; SauveEngin_game; intervalo [0x0046b119, 0x0046b1fb)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046b119  53                       push     ebx
0046b11a  51                       push     ecx
0046b11b  52                       push     edx
0046b11c  56                       push     esi
0046b11d  83ec0c                   sub      esp, 0xc
0046b120  31d2                     xor      edx, edx
0046b122  89542404                 mov      dword ptr [esp + 4], edx
0046b126  89542408                 mov      dword ptr [esp + 8], edx
0046b12a  eb04                     jmp      0x46b130
0046b12c  ff442408                 inc      dword ptr [esp + 8]
0046b130  31c0                     xor      eax, eax
0046b132  668b442408               mov      ax, word ptr [esp + 8]
0046b137  3d20030000               cmp      eax, 0x320
0046b13c  7d0f                     jge      0x46b14d
0046b13e  e8bc6efdff               call     0x441fff
0046b143  84c0                     test     al, al
0046b145  74e5                     je       0x46b12c
0046b147  ff442404                 inc      dword ptr [esp + 4]
0046b14b  ebdf                     jmp      0x46b12c
0046b14d  ba02000000               mov      edx, 2
0046b152  8d442404                 lea      eax, [esp + 4]
0046b156  b914010000               mov      ecx, 0x114
0046b15b  e816d3feff               call     0x458476
0046b160  31f6                     xor      esi, esi
0046b162  ba02000000               mov      edx, 2
0046b167  89e0                     mov      eax, esp
0046b169  890c24                   mov      dword ptr [esp], ecx
0046b16c  e805d3feff               call     0x458476
0046b171  89742408                 mov      dword ptr [esp + 8], esi
0046b175  eb04                     jmp      0x46b17b
0046b177  ff442408                 inc      dword ptr [esp + 8]
0046b17b  31c0                     xor      eax, eax
0046b17d  668b442408               mov      ax, word ptr [esp + 8]
0046b182  3d20030000               cmp      eax, 0x320
0046b187  7d39                     jge      0x46b1c2
0046b189  e8716efdff               call     0x441fff
0046b18e  84c0                     test     al, al
0046b190  74e5                     je       0x46b177
0046b192  ba02000000               mov      edx, 2
0046b197  8d442408                 lea      eax, [esp + 8]
0046b19b  e8d6d2feff               call     0x458476
0046b1a0  31c0                     xor      eax, eax
0046b1a2  668b442408               mov      ax, word ptr [esp + 8]
0046b1a7  69c014010000             imul     eax, eax, 0x114
0046b1ad  31d2                     xor      edx, edx
0046b1af  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
0046b1b5  668b1424                 mov      dx, word ptr [esp]
0046b1b9  01d8                     add      eax, ebx
0046b1bb  e8b6d2feff               call     0x458476
0046b1c0  ebb5                     jmp      0x46b177
0046b1c2  31d2                     xor      edx, edx
0046b1c4  89542408                 mov      dword ptr [esp + 8], edx
0046b1c8  eb1b                     jmp      0x46b1e5
0046b1ca  89c2                     mov      edx, eax
0046b1cc  a124194e00               mov      eax, dword ptr [0x4e1924]
0046b1d1  c1e202                   shl      edx, 2
0046b1d4  8b0402                   mov      eax, dword ptr [edx + eax]
0046b1d7  ba00020000               mov      edx, 0x200
0046b1dc  e895d2feff               call     0x458476
0046b1e1  ff442408                 inc      dword ptr [esp + 8]
0046b1e5  31c0                     xor      eax, eax
0046b1e7  668b442408               mov      ax, word ptr [esp + 8]
0046b1ec  3d20030000               cmp      eax, 0x320
0046b1f1  7cd7                     jl       0x46b1ca
0046b1f3  83c40c                   add      esp, 0xc
0046b1f6  5e                       pop      esi
0046b1f7  5a                       pop      edx
0046b1f8  59                       pop      ecx
0046b1f9  5b                       pop      ebx
0046b1fa  c3                       ret
