; EnginLigneDeTir; intervalo [0x004517a2, 0x0045189c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004517a2  51                       push     ecx
004517a3  56                       push     esi
004517a4  57                       push     edi
004517a5  89c7                     mov      edi, eax
004517a7  88d4                     mov      ah, dl
004517a9  31f6                     xor      esi, esi
004517ab  6689fe                   mov      si, di
004517ae  89f2                     mov      edx, esi
004517b0  c1e204                   shl      edx, 4
004517b3  01f2                     add      edx, esi
004517b5  c1e202                   shl      edx, 2
004517b8  01d6                     add      esi, edx
004517ba  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004517c0  c1e602                   shl      esi, 2
004517c3  8a443201                 mov      al, byte ptr [edx + esi + 1]
004517c7  3c08                     cmp      al, 8
004517c9  7214                     jb       0x4517df
004517cb  760e                     jbe      0x4517db
004517cd  3c0c                     cmp      al, 0xc
004517cf  7212                     jb       0x4517e3
004517d1  7608                     jbe      0x4517db
004517d3  3c16                     cmp      al, 0x16
004517d5  720c                     jb       0x4517e3
004517d7  3c17                     cmp      al, 0x17
004517d9  7708                     ja       0x4517e3
004517db  b001                     mov      al, 1
004517dd  eb06                     jmp      0x4517e5
004517df  3c04                     cmp      al, 4
004517e1  74f8                     je       0x4517db
004517e3  30c0                     xor      al, al
004517e5  84c0                     test     al, al
004517e7  743a                     je       0x451823
004517e9  b001                     mov      al, 1
004517eb  5f                       pop      edi
004517ec  5e                       pop      esi
004517ed  59                       pop      ecx
004517ee  c3                       ret
004517ef  31c0                     xor      eax, eax
004517f1  6689d8                   mov      ax, bx
004517f4  e8e996fcff               call     0x41aee2
004517f9  89c1                     mov      ecx, eax
004517fb  eb39                     jmp      0x451836
004517fd  81e3ffff0000             and      ebx, 0xffff
00451803  89d8                     mov      eax, ebx
00451805  c1e004                   shl      eax, 4
00451808  01d8                     add      eax, ebx
0045180a  c1e002                   shl      eax, 2
0045180d  01d8                     add      eax, ebx
0045180f  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451815  c1e002                   shl      eax, 2
00451818  668b4c027c               mov      cx, word ptr [edx + eax + 0x7c]
0045181d  eb17                     jmp      0x451836
0045181f  89d9                     mov      ecx, ebx
00451821  eb13                     jmp      0x451836
00451823  80fc03                   cmp      ah, 3
00451826  7209                     jb       0x451831
00451828  76c5                     jbe      0x4517ef
0045182a  80fc05                   cmp      ah, 5
0045182d  74f0                     je       0x45181f
0045182f  eb05                     jmp      0x451836
00451831  80fc01                   cmp      ah, 1
00451834  74c7                     je       0x4517fd
00451836  31db                     xor      ebx, ebx
00451838  6689fb                   mov      bx, di
0045183b  89da                     mov      edx, ebx
0045183d  c1e204                   shl      edx, 4
00451840  01da                     add      edx, ebx
00451842  c1e202                   shl      edx, 2
00451845  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0045184a  01da                     add      edx, ebx
0045184c  668b44907c               mov      ax, word ptr [eax + edx*4 + 0x7c]
00451851  31db                     xor      ebx, ebx
00451853  31d2                     xor      edx, edx
00451855  6689c3                   mov      bx, ax
00451858  6689ca                   mov      dx, cx
0045185b  89d8                     mov      eax, ebx
0045185d  e8e0570200               call     0x477042
00451862  31d2                     xor      edx, edx
00451864  88c2                     mov      dl, al
00451866  89d8                     mov      eax, ebx
00451868  e881580200               call     0x4770ee
0045186d  89c2                     mov      edx, eax
0045186f  31db                     xor      ebx, ebx
00451871  6689d3                   mov      bx, dx
00451874  89d8                     mov      eax, ebx
00451876  e8c14c0200               call     0x47653c
0045187b  84c0                     test     al, al
0045187d  750e                     jne      0x45188d
0045187f  6639ca                   cmp      dx, cx
00451882  7409                     je       0x45188d
00451884  31d2                     xor      edx, edx
00451886  89d8                     mov      eax, ebx
00451888  6689ca                   mov      dx, cx
0045188b  ebd0                     jmp      0x45185d
0045188d  6639ca                   cmp      dx, cx
00451890  0f8453ffffff             je       0x4517e9
00451896  30c0                     xor      al, al
00451898  5f                       pop      edi
00451899  5e                       pop      esi
0045189a  59                       pop      ecx
0045189b  c3                       ret
