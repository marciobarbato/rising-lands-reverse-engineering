; MarcheResetAll; exclusive end 0x004602cd.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046027c  53                       push     ebx
0046027d  51                       push     ecx
0046027e  52                       push     edx
0046027f  56                       push     esi
00460280  31c0                     xor      eax, eax
00460282  31d2                     xor      edx, edx
00460284  83c202                   add      edx, 2
00460287  40                       inc      eax
00460288  30db                     xor      bl, bl
0046028a  30c9                     xor      cl, cl
0046028c  31f6                     xor      esi, esi
0046028e  b5ff                     mov      ch, 0xff
00460290  88987b2e4e00             mov      byte ptr [eax + 0x4e2e7b], bl
00460296  6689b22e294e00           mov      word ptr [edx + 0x4e292e], si
0046029d  b701                     mov      bh, 1
0046029f  88a88b6f4900             mov      byte ptr [eax + 0x496f8b], ch
004602a5  30ed                     xor      ch, ch
004602a7  88b82b294e00             mov      byte ptr [eax + 0x4e292b], bh
004602ad  889827294e00             mov      byte ptr [eax + 0x4e2927], bl
004602b3  30ff                     xor      bh, bh
004602b5  66898a3e294e00           mov      word ptr [edx + 0x4e293e], cx
004602bc  66899a36294e00           mov      word ptr [edx + 0x4e2936], bx
004602c3  83f804                   cmp      eax, 4
004602c6  7cbc                     jl       0x460284
004602c8  5e                       pop      esi
004602c9  5a                       pop      edx
004602ca  59                       pop      ecx
004602cb  5b                       pop      ebx
004602cc  c3                       ret
