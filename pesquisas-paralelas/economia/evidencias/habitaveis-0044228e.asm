; TypeEnginEstRealisable: Byte table 0x4e1934 + 26*owner + type; exclusive end 0x004422b0.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044228e  53                       push     ebx
0044228f  88d3                     mov      bl, dl
00442291  31d2                     xor      edx, edx
00442293  88c2                     mov      dl, al
00442295  89d0                     mov      eax, edx
00442297  c1e002                   shl      eax, 2
0044229a  29d0                     sub      eax, edx
0044229c  c1e002                   shl      eax, 2
0044229f  01c2                     add      edx, eax
004422a1  31c0                     xor      eax, eax
004422a3  01d2                     add      edx, edx
004422a5  88d8                     mov      al, bl
004422a7  8a840234194e00           mov      al, byte ptr [edx + eax + 0x4e1934]
004422ae  5b                       pop      ebx
004422af  c3                       ret
