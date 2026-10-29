; BatimentGetDecalageConstruction; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041aea4  3c15                     cmp al, 0x15
0041aea6  7737                     ja 0x41aedf
0041aea8  25ff000000               and eax, 0xff
0041aead  2eff24854cae4100         jmp dword ptr cs:[eax*4 + 0x41ae4c]
0041aeb5  b801020000               mov eax, 0x201
0041aeba  c3                       ret
0041aebb  b801010000               mov eax, 0x101
0041aec0  c3                       ret
0041aec1  b802020000               mov eax, 0x202
0041aec6  c3                       ret
0041aec7  b800030000               mov eax, 0x300
0041aecc  c3                       ret
0041aecd  b800010000               mov eax, 0x100
0041aed2  c3                       ret
0041aed3  b800020000               mov eax, 0x200
0041aed8  c3                       ret
0041aed9  b801000000               mov eax, 1
0041aede  c3                       ret
0041aedf  31c0                     xor eax, eax
0041aee1  c3                       ret
