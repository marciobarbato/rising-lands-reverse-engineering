; EnginEstEnnemi; intervalo [0x00446fbf, 0x00447021)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00446fbf  53                       push     ebx
00446fc0  31db                     xor      ebx, ebx
00446fc2  6689c3                   mov      bx, ax
00446fc5  89d8                     mov      eax, ebx
00446fc7  c1e004                   shl      eax, 4
00446fca  01d8                     add      eax, ebx
00446fcc  c1e002                   shl      eax, 2
00446fcf  01d8                     add      eax, ebx
00446fd1  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00446fd7  8a0483                   mov      al, byte ptr [ebx + eax*4]
00446fda  88c6                     mov      dh, al
00446fdc  38c2                     cmp      dl, al
00446fde  7413                     je       0x446ff3
00446fe0  31db                     xor      ebx, ebx
00446fe2  88d3                     mov      bl, dl
00446fe4  83fb04                   cmp      ebx, 4
00446fe7  7434                     je       0x44701d
00446fe9  25ff000000               and      eax, 0xff
00446fee  83f804                   cmp      eax, 4
00446ff1  742a                     je       0x44701d
00446ff3  31c0                     xor      eax, eax
00446ff5  88d0                     mov      al, dl
00446ff7  3dc8000000               cmp      eax, 0xc8
00446ffc  740c                     je       0x44700a
00446ffe  31db                     xor      ebx, ebx
00447000  88f3                     mov      bl, dh
00447002  81fbc8000000             cmp      ebx, 0xc8
00447008  7504                     jne      0x44700e
0044700a  30c0                     xor      al, al
0044700c  5b                       pop      ebx
0044700d  c3                       ret
0044700e  38d6                     cmp      dh, dl
00447010  74f8                     je       0x44700a
00447012  89da                     mov      edx, ebx
00447014  e81f680200               call     0x46d838
00447019  84c0                     test     al, al
0044701b  75ed                     jne      0x44700a
0044701d  b001                     mov      al, 1
0044701f  5b                       pop      ebx
00447020  c3                       ret
