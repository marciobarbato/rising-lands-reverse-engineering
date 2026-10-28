; Original conditional unit request; exclusive end0x420fb7.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00420f9e  8a4704                   mov      al, byte ptr [edi + 4]
00420fa1  3a0541805000             cmp      al, byte ptr [0x508041]
00420fa7  750e                     jne      0x420fb7
00420fa9  ba06000000               mov      edx, 6
00420fae  89f0                     mov      eax, esi
00420fb0  31db                     xor      ebx, ebx
00420fb2  e8a7fd0100               call     0x440d5e
