; EnginNextEtape_validite; intervalo [0x0045673b, 0x004568a8)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045673b  31c0                     xor      eax, eax
0045673d  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
00456744  3dffff0000               cmp      eax, 0xffff
00456749  7427                     je       0x456772
0045674b  e8bb3ffcff               call     0x41a70b
00456750  84c0                     test     al, al
00456752  751e                     jne      0x456772
00456754  31c0                     xor      eax, eax
00456756  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045675d  e82a39fcff               call     0x41a08c
00456762  25ff000000               and      eax, 0xff
00456767  3dc8000000               cmp      eax, 0xc8
0045676c  0f852c010000             jne      0x45689e
00456772  31c9                     xor      ecx, ecx
00456774  6689f9                   mov      cx, di
00456777  89c8                     mov      eax, ecx
00456779  c1e004                   shl      eax, 4
0045677c  01c8                     add      eax, ecx
0045677e  c1e002                   shl      eax, 2
00456781  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00456787  01c8                     add      eax, ecx
00456789  8a0482                   mov      al, byte ptr [edx + eax*4]
0045678c  25ff000000               and      eax, 0xff
00456791  e881700100               call     0x46d817
00456796  25ff000000               and      eax, 0xff
0045679b  83f802                   cmp      eax, 2
0045679e  7513                     jne      0x4567b3
004567a0  ba4a000000               mov      edx, 0x4a
004567a5  89c8                     mov      eax, ecx
004567a7  31db                     xor      ebx, ebx
004567a9  e81ac20200               call     0x4829c8
004567ae  e91ae5ffff               jmp      0x454ccd
004567b3  31d2                     xor      edx, edx
004567b5  89c8                     mov      eax, ecx
004567b7  668b567e                 mov      dx, word ptr [esi + 0x7e]
004567bb  e813f0feff               call     0x4457d3
004567c0  66c786b8000000ffff       mov      word ptr [esi + 0xb8], 0xffff
004567c9  e9ffe4ffff               jmp      0x454ccd
004567ce  31c0                     xor      eax, eax
004567d0  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
004567d7  3dffff0000               cmp      eax, 0xffff
004567dc  0f846d000000             je       0x45684f
004567e2  31d2                     xor      edx, edx
004567e4  6689c2                   mov      dx, ax
004567e7  89d0                     mov      eax, edx
004567e9  c1e004                   shl      eax, 4
004567ec  01d0                     add      eax, edx
004567ee  c1e002                   shl      eax, 2
004567f1  01d0                     add      eax, edx
004567f3  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004567f9  c1e002                   shl      eax, 2
004567fc  01c2                     add      edx, eax
004567fe  31c0                     xor      eax, eax
00456800  8a4202                   mov      al, byte ptr [edx + 2]
00456803  85c0                     test     eax, eax
00456805  7409                     je       0x456810
00456807  83f804                   cmp      eax, 4
0045680a  7404                     je       0x456810
0045680c  b001                     mov      al, 1
0045680e  eb02                     jmp      0x456812
00456810  30c0                     xor      al, al
00456812  84c0                     test     al, al
00456814  7439                     je       0x45684f
00456816  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045681d  31d2                     xor      edx, edx
0045681f  6689c2                   mov      dx, ax
00456822  89d0                     mov      eax, edx
00456824  c1e004                   shl      eax, 4
00456827  01d0                     add      eax, edx
00456829  c1e002                   shl      eax, 2
0045682c  01c2                     add      edx, eax
0045682e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00456833  c1e202                   shl      edx, 2
00456836  01d0                     add      eax, edx
00456838  8a10                     mov      dl, byte ptr [eax]
0045683a  81e2ff000000             and      edx, 0xff
00456840  81fac8000000             cmp      edx, 0xc8
00456846  7407                     je       0x45684f
00456848  8a4072                   mov      al, byte ptr [eax + 0x72]
0045684b  84c0                     test     al, al
0045684d  754f                     jne      0x45689e
0045684f  31c9                     xor      ecx, ecx
00456851  6689f9                   mov      cx, di
00456854  89c8                     mov      eax, ecx
00456856  c1e004                   shl      eax, 4
00456859  01c8                     add      eax, ecx
0045685b  c1e002                   shl      eax, 2
0045685e  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00456864  01c8                     add      eax, ecx
00456866  8a0482                   mov      al, byte ptr [edx + eax*4]
00456869  25ff000000               and      eax, 0xff
0045686e  e8a46f0100               call     0x46d817
00456873  25ff000000               and      eax, 0xff
00456878  83f802                   cmp      eax, 2
0045687b  0f841fffffff             je       0x4567a0
00456881  e92dffffff               jmp      0x4567b3
00456886  8a86b7000000             mov      al, byte ptr [esi + 0xb7]
0045688c  3c01                     cmp      al, 1
0045688e  720e                     jb       0x45689e
00456890  0f8638ffffff             jbe      0x4567ce
00456896  3c03                     cmp      al, 3
00456898  0f849dfeffff             je       0x45673b
0045689e  31c0                     xor      eax, eax
004568a0  6689f8                   mov      ax, di
004568a3  e86cb0ffff               call     0x451914
