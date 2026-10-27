; EnginRestaureEtat_magia; intervalo [0x0045315f, 0x00453232)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045315f  53                       push     ebx
00453160  51                       push     ecx
00453161  52                       push     edx
00453162  56                       push     esi
00453163  57                       push     edi
00453164  55                       push     ebp
00453165  83ec28                   sub      esp, 0x28
00453168  89c6                     mov      esi, eax
0045316a  31db                     xor      ebx, ebx
0045316c  6689c3                   mov      bx, ax
0045316f  89da                     mov      edx, ebx
00453171  c1e204                   shl      edx, 4
00453174  01da                     add      edx, ebx
00453176  c1e202                   shl      edx, 2
00453179  01da                     add      edx, ebx
0045317b  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
00453181  c1e202                   shl      edx, 2
00453184  8d0c2a                   lea      ecx, [edx + ebp]
00453187  668b81a0000000           mov      ax, word ptr [ecx + 0xa0]
0045318e  663d0d00                 cmp      ax, 0xd
00453192  0f8213070000             jb       0x4538ab
00453198  0f86ee050000             jbe      0x45378c
0045319e  663d1100                 cmp      ax, 0x11
004531a2  0f8293060000             jb       0x45383b
004531a8  0f86f6020000             jbe      0x4534a4
004531ae  663d1400                 cmp      ax, 0x14
004531b2  0f8274060000             jb       0x45382c
004531b8  0f8664030000             jbe      0x453522
004531be  663d1800                 cmp      ax, 0x18
004531c2  0f851d070000             jne      0x4538e5
004531c8  89d8                     mov      eax, ebx
004531ca  8ab1f4000000             mov      dh, byte ptr [ecx + 0xf4]
004531d0  668bb9b8000000           mov      di, word ptr [ecx + 0xb8]
004531d7  8a91b7000000             mov      dl, byte ptr [ecx + 0xb7]
004531dd  e89a03ffff               call     0x44357c
004531e2  31c0                     xor      eax, eax
004531e4  8a4101                   mov      al, byte ptr [ecx + 1]
004531e7  83f804                   cmp      eax, 4
004531ea  742b                     je       0x453217
004531ec  e969feffff               jmp      0x45305a
004531f1  6639fe                   cmp      si, di
004531f4  0f8460feffff             je       0x45305a
004531fa  c6410218                 mov      byte ptr [ecx + 2], 0x18
004531fe  c6818a00000000           mov      byte ptr [ecx + 0x8a], 0
00453205  8891b7000000             mov      byte ptr [ecx + 0xb7], dl
0045320b  6689b9b8000000           mov      word ptr [ecx + 0xb8], di
00453212  e943feffff               jmp      0x45305a
00453217  88b1f4000000             mov      byte ptr [ecx + 0xf4], dh
0045321d  80fa01                   cmp      dl, 1
00453220  0f8234feffff             jb       0x45305a
00453226  76c9                     jbe      0x4531f1
00453228  80fa05                   cmp      dl, 5
0045322b  74cd                     je       0x4531fa
0045322d  e928feffff               jmp      0x45305a
