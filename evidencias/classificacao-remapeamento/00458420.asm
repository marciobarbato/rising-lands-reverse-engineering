; FileOpen; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00458420  e8fa420300               call 0x48c71f
00458425  a31c1d4e00               mov dword ptr [0x4e1d1c], eax
0045842a  85c0                     test eax, eax
0045842c  0f95c0                   setne al
0045842f  c3                       ret
00458430  52                       push edx
00458431  ba88484900               mov edx, 0x494888
00458436  e8e4420300               call 0x48c71f
0045843b  85c0                     test eax, eax
0045843d  7504                     jne 0x458443
0045843f  30c0                     xor al, al
00458441  5a                       pop edx
00458442  c3                       ret
00458443  e8c3430300               call 0x48c80b
00458448  b001                     mov al, 1
0045844a  5a                       pop edx
0045844b  c3                       ret
