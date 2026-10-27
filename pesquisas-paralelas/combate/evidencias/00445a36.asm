; SetAttaqueEngin; intervalo [0x00445a36, 0x00445af1)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00445a36  51                       push     ecx
00445a37  56                       push     esi
00445a38  89c6                     mov      esi, eax
00445a3a  88d1                     mov      cl, dl
00445a3c  31c0                     xor      eax, eax
00445a3e  6689f0                   mov      ax, si
00445a41  89c2                     mov      edx, eax
00445a43  c1e204                   shl      edx, 4
00445a46  01c2                     add      edx, eax
00445a48  c1e202                   shl      edx, 2
00445a4b  01c2                     add      edx, eax
00445a4d  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00445a52  c1e202                   shl      edx, 2
00445a55  01c2                     add      edx, eax
00445a57  31c0                     xor      eax, eax
00445a59  8a4202                   mov      al, byte ptr [edx + 2]
00445a5c  83f801                   cmp      eax, 1
00445a5f  7515                     jne      0x445a76
00445a61  3a8ab7000000             cmp      cl, byte ptr [edx + 0xb7]
00445a67  750d                     jne      0x445a76
00445a69  663b9ab8000000           cmp      bx, word ptr [edx + 0xb8]
00445a70  0f8478000000             je       0x445aee
00445a76  31c0                     xor      eax, eax
00445a78  6689f0                   mov      ax, si
00445a7b  e8fcdaffff               call     0x44357c
00445a80  31c0                     xor      eax, eax
00445a82  8a4201                   mov      al, byte ptr [edx + 1]
00445a85  83f807                   cmp      eax, 7
00445a88  0f8460000000             je       0x445aee
00445a8e  83f806                   cmp      eax, 6
00445a91  0f8457000000             je       0x445aee
00445a97  83f805                   cmp      eax, 5
00445a9a  7452                     je       0x445aee
00445a9c  83f80d                   cmp      eax, 0xd
00445a9f  744d                     je       0x445aee
00445aa1  83f809                   cmp      eax, 9
00445aa4  7448                     je       0x445aee
00445aa6  83f80a                   cmp      eax, 0xa
00445aa9  752f                     jne      0x445ada
00445aab  5e                       pop      esi
00445aac  59                       pop      ecx
00445aad  c3                       ret
00445aae  6639de                   cmp      si, bx
00445ab1  743b                     je       0x445aee
00445ab3  c6828a00000000           mov      byte ptr [edx + 0x8a], 0
00445aba  884a02                   mov      byte ptr [edx + 2], cl
00445abd  888ab7000000             mov      byte ptr [edx + 0xb7], cl
00445ac3  66899ab8000000           mov      word ptr [edx + 0xb8], bx
00445aca  5e                       pop      esi
00445acb  59                       pop      ecx
00445acc  c3                       ret
00445acd  c6420201                 mov      byte ptr [edx + 2], 1
00445ad1  c6828a00000000           mov      byte ptr [edx + 0x8a], 0
00445ad8  ebe3                     jmp      0x445abd
00445ada  80f903                   cmp      cl, 3
00445add  720a                     jb       0x445ae9
00445adf  76ec                     jbe      0x445acd
00445ae1  80f905                   cmp      cl, 5
00445ae4  74e7                     je       0x445acd
00445ae6  5e                       pop      esi
00445ae7  59                       pop      ecx
00445ae8  c3                       ret
00445ae9  80f901                   cmp      cl, 1
00445aec  74c0                     je       0x445aae
00445aee  5e                       pop      esi
00445aef  59                       pop      ecx
00445af0  c3                       ret
