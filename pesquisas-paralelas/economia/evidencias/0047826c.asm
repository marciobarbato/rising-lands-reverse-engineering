; PatateAugmentable: limite por próximo símbolo SBL, fim exclusivo 0x004782b4.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047826c  53                       push     ebx
0047826d  52                       push     edx
0047826e  31db                     xor      ebx, ebx
00478270  8b15747d5000             mov      edx, dword ptr [0x507d74]
00478276  6689c3                   mov      bx, ax
00478279  8a141a                   mov      dl, byte ptr [edx + ebx]
0047827c  81e2ff000000             and      edx, 0xff
00478282  83fa1d                   cmp      edx, 0x1d
00478285  7c0a                     jl       0x478291
00478287  83fa28                   cmp      edx, 0x28
0047828a  7d05                     jge      0x478291
0047828c  b001                     mov      al, 1
0047828e  5a                       pop      edx
0047828f  5b                       pop      ebx
00478290  c3                       ret
00478291  31db                     xor      ebx, ebx
00478293  8b15747d5000             mov      edx, dword ptr [0x507d74]
00478299  6689c3                   mov      bx, ax
0047829c  8a141a                   mov      dl, byte ptr [edx + ebx]
0047829f  81e2ff000000             and      edx, 0xff
004782a5  83fa29                   cmp      edx, 0x29
004782a8  7c05                     jl       0x4782af
004782aa  83fa34                   cmp      edx, 0x34
004782ad  7cdd                     jl       0x47828c
004782af  30c0                     xor      al, al
004782b1  5a                       pop      edx
004782b2  5b                       pop      ebx
004782b3  c3                       ret
