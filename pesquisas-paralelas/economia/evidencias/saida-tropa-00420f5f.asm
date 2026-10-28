; SortieTroupe world-call context; outside implemented prefix; exclusive end 0x00420fb7.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Capstone instruction listing, not inferred pseudocode.
00420f5f  0fb7e8                   movzx    ebp, ax
00420f62  8a4f7b                   mov      cl, byte ptr [edi + 0x7b]
00420f65  89ea                     mov      edx, ebp
00420f67  89f0                     mov      eax, esi
00420f69  e8196c0300               call     0x457b87
00420f6e  bae8030000               mov      edx, 0x3e8
00420f73  89f0                     mov      eax, esi
00420f75  e8a8610300               call     0x457122
00420f7a  89f0                     mov      eax, esi
00420f7c  e87c210300               call     0x4530fd
00420f81  89f0                     mov      eax, esi
00420f83  89ea                     mov      edx, ebp
00420f85  e8b8ee0200               call     0x44fe42
00420f8a  89f0                     mov      eax, esi
00420f8c  e82b500200               call     0x445fbc
00420f91  31d2                     xor      edx, edx
00420f93  89f0                     mov      eax, esi
00420f95  668b577c                 mov      dx, word ptr [edi + 0x7c]
00420f99  e835480200               call     0x4457d3
00420f9e  8a4704                   mov      al, byte ptr [edi + 4]
00420fa1  3a0541805000             cmp      al, byte ptr [0x508041]
00420fa7  750e                     jne      0x420fb7
00420fa9  ba06000000               mov      edx, 6
00420fae  89f0                     mov      eax, esi
00420fb0  31db                     xor      ebx, ebx
00420fb2  e8a7fd0100               call     0x440d5e
