; TypeBatimentEstRealisable; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x418ad3
00418a93  53                       push     ebx
00418a94  88c7                     mov      bh, al
00418a96  88d3                     mov      bl, dl
00418a98  e813390100               call     0x42c3b0
00418a9d  84c0                     test     al, al
00418a9f  7412                     je       0x418ab3
00418aa1  31c0                     xor      eax, eax
00418aa3  88d0                     mov      al, dl
00418aa5  83f808                   cmp      eax, 8
00418aa8  7405                     je       0x418aaf
00418aaa  83f80c                   cmp      eax, 0xc
00418aad  7504                     jne      0x418ab3
00418aaf  30c0                     xor      al, al
00418ab1  5b                       pop      ebx
00418ab2  c3                       ret      
00418ab3  31d2                     xor      edx, edx
00418ab5  88fa                     mov      dl, bh
00418ab7  89d0                     mov      eax, edx
00418ab9  c1e002                   shl      eax, 2
00418abc  29d0                     sub      eax, edx
00418abe  c1e002                   shl      eax, 2
00418ac1  29d0                     sub      eax, edx
00418ac3  8d1400                   lea      edx, [eax + eax]
00418ac6  31c0                     xor      eax, eax
00418ac8  88d8                     mov      al, bl
00418aca  8a8402d4fa4d00           mov      al, byte ptr [edx + eax + 0x4dfad4]
00418ad1  5b                       pop      ebx
00418ad2  c3                       ret      
