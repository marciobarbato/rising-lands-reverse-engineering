; BagContient: Mode-1 type count used by the predicate; exclusive end 0x0044724a.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004471b8  51                       push     ecx
004471b9  56                       push     esi
004471ba  57                       push     edi
004471bb  55                       push     ebp
004471bc  83ec08                   sub      esp, 8
004471bf  881424                   mov      byte ptr [esp], dl
004471c2  89df                     mov      edi, ebx
004471c4  8a0c24                   mov      cl, byte ptr [esp]
004471c7  31db                     xor      ebx, ebx
004471c9  fec9                     dec      cl
004471cb  31d2                     xor      edx, edx
004471cd  884c2404                 mov      byte ptr [esp + 4], cl
004471d1  eb29                     jmp      0x4471fc
004471d3  668b747006               mov      si, word ptr [eax + esi*2 + 6]
004471d8  81e6ffff0000             and      esi, 0xffff
004471de  69ee14010000             imul     ebp, esi, 0x114
004471e4  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
004471ea  8a4c2e01                 mov      cl, byte ptr [esi + ebp + 1]
004471ee  31f6                     xor      esi, esi
004471f0  0fb6e9                   movzx    ebp, cl
004471f3  6689fe                   mov      si, di
004471f6  39f5                     cmp      ebp, esi
004471f8  7501                     jne      0x4471fb
004471fa  43                       inc      ebx
004471fb  42                       inc      edx
004471fc  663b5002                 cmp      dx, word ptr [eax + 2]
00447200  733e                     jae      0x447240
00447202  31f6                     xor      esi, esi
00447204  6689d6                   mov      si, dx
00447207  8a4c0642                 mov      cl, byte ptr [esi + eax + 0x42]
0044720b  3a0c24                   cmp      cl, byte ptr [esp]
0044720e  741c                     je       0x44722c
00447210  ebe9                     jmp      0x4471fb
00447212  663b7c7006               cmp      di, word ptr [eax + esi*2 + 6]
00447217  ebdf                     jmp      0x4471f8
00447219  31f6                     xor      esi, esi
0044721b  6689d6                   mov      si, dx
0044721e  663b7c7006               cmp      di, word ptr [eax + esi*2 + 6]
00447223  75d6                     jne      0x4471fb
00447225  b801000000               mov      eax, 1
0044722a  eb16                     jmp      0x447242
0044722c  8a4c2404                 mov      cl, byte ptr [esp + 4]
00447230  80f906                   cmp      cl, 6
00447233  77c6                     ja       0x4471fb
00447235  0fb6e9                   movzx    ebp, cl
00447238  2eff24ad9c714400         jmp      dword ptr cs:[ebp*4 + 0x44719c]
00447240  89d8                     mov      eax, ebx
00447242  83c408                   add      esp, 8
00447245  5d                       pop      ebp
00447246  5f                       pop      edi
00447247  5e                       pop      esi
00447248  59                       pop      ecx
00447249  c3                       ret
