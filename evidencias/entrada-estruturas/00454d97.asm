; EnginNextEtape state-13 refusal 0x454d97 (SetDeplaceEngin, +0xc0 = 0xffff); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00454d97  31c0                     xor eax, eax
00454d99  31d2                     xor edx, edx
00454d9b  6689f8                   mov ax, di
00454d9e  668b567e                 mov dx, word ptr [esi + 0x7e]
00454da2  e82c0affff               call 0x4457d3
00454da7  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
00454db0  e918ffffff               jmp 0x454ccd
