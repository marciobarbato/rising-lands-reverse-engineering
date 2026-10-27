; SauveEngin; intervalo [0x00479d7f, 0x00479e12)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00479d7f  53                       push     ebx
00479d80  52                       push     edx
00479d81  83ec08                   sub      esp, 8
00479d84  31d2                     xor      edx, edx
00479d86  89542404                 mov      dword ptr [esp + 4], edx
00479d8a  ba3f4e4900               mov      edx, 0x494e3f
00479d8f  e88ce6fdff               call     0x458420
00479d94  ba02000000               mov      edx, 2
00479d99  8d442404                 lea      eax, [esp + 4]
00479d9d  31db                     xor      ebx, ebx
00479d9f  e8d2e6fdff               call     0x458476
00479da4  891c24                   mov      dword ptr [esp], ebx
00479da7  eb03                     jmp      0x479dac
00479da9  ff0424                   inc      dword ptr [esp]
00479dac  31c0                     xor      eax, eax
00479dae  668b0424                 mov      ax, word ptr [esp]
00479db2  3d20030000               cmp      eax, 0x320
00479db7  7d38                     jge      0x479df1
00479db9  e84182fcff               call     0x441fff
00479dbe  84c0                     test     al, al
00479dc0  74e7                     je       0x479da9
00479dc2  ba02000000               mov      edx, 2
00479dc7  89e0                     mov      eax, esp
00479dc9  e8a8e6fdff               call     0x458476
00479dce  31c0                     xor      eax, eax
00479dd0  668b0424                 mov      ax, word ptr [esp]
00479dd4  69d014010000             imul     edx, eax, 0x114
00479dda  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00479ddf  01d0                     add      eax, edx
00479de1  ba14010000               mov      edx, 0x114
00479de6  e88be6fdff               call     0x458476
00479deb  ff442404                 inc      dword ptr [esp + 4]
00479def  ebb8                     jmp      0x479da9
00479df1  31d2                     xor      edx, edx
00479df3  31c0                     xor      eax, eax
00479df5  e891e6fdff               call     0x45848b
00479dfa  ba02000000               mov      edx, 2
00479dff  8d442404                 lea      eax, [esp + 4]
00479e03  e86ee6fdff               call     0x458476
00479e08  e83fe6fdff               call     0x45844c
00479e0d  e967ffffff               jmp      0x479d79
