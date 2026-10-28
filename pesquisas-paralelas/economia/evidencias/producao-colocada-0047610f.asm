; Movement raw-object query; exclusive end0x476134.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Context evidence; this composition does not invoke every resource-removal branch.
0047610f  52                       push     edx
00476110  31d2                     xor      edx, edx
00476112  6689c2                   mov      dx, ax
00476115  a1747d5000               mov      eax, dword ptr [0x507d74]
0047611a  8a0402                   mov      al, byte ptr [edx + eax]
0047611d  25ff000000               and      eax, 0xff
00476122  83f842                   cmp      eax, 0x42
00476125  7405                     je       0x47612c
00476127  83f836                   cmp      eax, 0x36
0047612a  7504                     jne      0x476130
0047612c  b001                     mov      al, 1
0047612e  5a                       pop      edx
0047612f  c3                       ret
00476130  30c0                     xor      al, al
00476132  5a                       pop      edx
00476133  c3                       ret
