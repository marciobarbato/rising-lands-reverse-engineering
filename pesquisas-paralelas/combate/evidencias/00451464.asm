; EnginViseCible; intervalo [0x00451464, 0x004516d3)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00451464  53                       push     ebx
00451465  51                       push     ecx
00451466  52                       push     edx
00451467  56                       push     esi
00451468  57                       push     edi
00451469  55                       push     ebp
0045146a  83ec08                   sub      esp, 8
0045146d  89c3                     mov      ebx, eax
0045146f  31d2                     xor      edx, edx
00451471  6689c2                   mov      dx, ax
00451474  89d0                     mov      eax, edx
00451476  c1e004                   shl      eax, 4
00451479  01d0                     add      eax, edx
0045147b  c1e002                   shl      eax, 2
0045147e  01d0                     add      eax, edx
00451480  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
00451486  c1e002                   shl      eax, 2
00451489  8d3428                   lea      esi, [eax + ebp]
0045148c  895c2404                 mov      dword ptr [esp + 4], ebx
00451490  b8ffff0000               mov      eax, 0xffff
00451495  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
0045149b  89f1                     mov      ecx, esi
0045149d  80fa03                   cmp      dl, 3
004514a0  0f829a000000             jb       0x451540
004514a6  7630                     jbe      0x4514d8
004514a8  80fa05                   cmp      dl, 5
004514ab  0f8486000000             je       0x451537
004514b1  e993000000               jmp      0x451549
004514b6  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
004514bd  31d2                     xor      edx, edx
004514bf  6689c2                   mov      dx, ax
004514c2  89d0                     mov      eax, edx
004514c4  c1e004                   shl      eax, 4
004514c7  01d0                     add      eax, edx
004514c9  c1e002                   shl      eax, 2
004514cc  01d0                     add      eax, edx
004514ce  668b44857c               mov      ax, word ptr [ebp + eax*4 + 0x7c]
004514d3  e971000000               jmp      0x451549
004514d8  31d2                     xor      edx, edx
004514da  8a96b0000000             mov      dl, byte ptr [esi + 0xb0]
004514e0  85d2                     test     edx, edx
004514e2  7405                     je       0x4514e9
004514e4  83fa01                   cmp      edx, 1
004514e7  7531                     jne      0x45151a
004514e9  31d2                     xor      edx, edx
004514eb  668b542404               mov      dx, word ptr [esp + 4]
004514f0  89d0                     mov      eax, edx
004514f2  c1e004                   shl      eax, 4
004514f5  01d0                     add      eax, edx
004514f7  c1e002                   shl      eax, 2
004514fa  01d0                     add      eax, edx
004514fc  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00451502  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
00451507  31d2                     xor      edx, edx
00451509  6689c2                   mov      dx, ax
0045150c  31c0                     xor      eax, eax
0045150e  668b81b8000000           mov      ax, word ptr [ecx + 0xb8]
00451515  e88624fdff               call     0x4239a0
0045151a  31d2                     xor      edx, edx
0045151c  6689c2                   mov      dx, ax
0045151f  81faffff0000             cmp      edx, 0xffff
00451525  7522                     jne      0x451549
00451527  31c0                     xor      eax, eax
00451529  668b81b8000000           mov      ax, word ptr [ecx + 0xb8]
00451530  e8ad99fcff               call     0x41aee2
00451535  eb12                     jmp      0x451549
00451537  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045153e  eb09                     jmp      0x451549
00451540  80fa01                   cmp      dl, 1
00451543  0f846dffffff             je       0x4514b6
00451549  31d2                     xor      edx, edx
0045154b  8a5601                   mov      dl, byte ptr [esi + 1]
0045154e  83fa0f                   cmp      edx, 0xf
00451551  0f84c8000000             je       0x45161f
00451557  83fa0c                   cmp      edx, 0xc
0045155a  0f84bf000000             je       0x45161f
00451560  31db                     xor      ebx, ebx
00451562  6689c3                   mov      bx, ax
00451565  89da                     mov      edx, ebx
00451567  89d8                     mov      eax, ebx
00451569  c1fa1f                   sar      edx, 0x1f
0045156c  c1e208                   shl      edx, 8
0045156f  1bc2                     sbb      eax, edx
00451571  c1f808                   sar      eax, 8
00451574  31c9                     xor      ecx, ecx
00451576  bf00010000               mov      edi, 0x100
0045157b  6689c1                   mov      cx, ax
0045157e  89da                     mov      edx, ebx
00451580  89d8                     mov      eax, ebx
00451582  c1fa1f                   sar      edx, 0x1f
00451585  f7ff                     idiv     edi
00451587  31db                     xor      ebx, ebx
00451589  31ff                     xor      edi, edi
0045158b  668b5e08                 mov      bx, word ptr [esi + 8]
0045158f  6689d7                   mov      di, dx
00451592  89da                     mov      edx, ebx
00451594  89d8                     mov      eax, ebx
00451596  c1fa1f                   sar      edx, 0x1f
00451599  c1e208                   shl      edx, 8
0045159c  1bc2                     sbb      eax, edx
0045159e  c1f808                   sar      eax, 8
004515a1  0fb7e8                   movzx    ebp, ax
004515a4  89da                     mov      edx, ebx
004515a6  b800010000               mov      eax, 0x100
004515ab  c1fa1f                   sar      edx, 0x1f
004515ae  890424                   mov      dword ptr [esp], eax
004515b1  89d8                     mov      eax, ebx
004515b3  f73c24                   idiv     dword ptr [esp]
004515b6  6a08                     push     8
004515b8  31c0                     xor      eax, eax
004515ba  89fb                     mov      ebx, edi
004515bc  6689d0                   mov      ax, dx
004515bf  89ea                     mov      edx, ebp
004515c1  e805810200               call     0x4796cb
004515c6  31d2                     xor      edx, edx
004515c8  00c0                     add      al, al
004515ca  8a5601                   mov      dl, byte ptr [esi + 1]
004515cd  fec8                     dec      al
004515cf  83fa03                   cmp      edx, 3
004515d2  7516                     jne      0x4515ea
004515d4  31d2                     xor      edx, edx
004515d6  88c2                     mov      dl, al
004515d8  83c20b                   add      edx, 0xb
004515db  bb10000000               mov      ebx, 0x10
004515e0  89d0                     mov      eax, edx
004515e2  c1fa1f                   sar      edx, 0x1f
004515e5  f7fb                     idiv     ebx
004515e7  8d4201                   lea      eax, [edx + 1]
004515ea  3a8691000000             cmp      al, byte ptr [esi + 0x91]
004515f0  e9d6000000               jmp      0x4516cb
004515f5  31d2                     xor      edx, edx
004515f7  6689ca                   mov      dx, cx
004515fa  89d0                     mov      eax, edx
004515fc  c1e004                   shl      eax, 4
004515ff  01d0                     add      eax, edx
00451601  c1e002                   shl      eax, 2
00451604  01d0                     add      eax, edx
00451606  668b7c837c               mov      di, word ptr [ebx + eax*4 + 0x7c]
0045160b  eb50                     jmp      0x45165d
0045160d  31c0                     xor      eax, eax
0045160f  6689c8                   mov      ax, cx
00451612  e8cb98fcff               call     0x41aee2
00451617  89c7                     mov      edi, eax
00451619  eb42                     jmp      0x45165d
0045161b  89cf                     mov      edi, ecx
0045161d  eb3e                     jmp      0x45165d
0045161f  8a96b7000000             mov      dl, byte ptr [esi + 0xb7]
00451625  668b8eb8000000           mov      cx, word ptr [esi + 0xb8]
0045162c  81e3ffff0000             and      ebx, 0xffff
00451632  89d8                     mov      eax, ebx
00451634  c1e004                   shl      eax, 4
00451637  01d8                     add      eax, ebx
00451639  c1e002                   shl      eax, 2
0045163c  01d8                     add      eax, ebx
0045163e  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00451644  c1e002                   shl      eax, 2
00451647  8d2c03                   lea      ebp, [ebx + eax]
0045164a  80fa03                   cmp      dl, 3
0045164d  7209                     jb       0x451658
0045164f  76bc                     jbe      0x45160d
00451651  80fa05                   cmp      dl, 5
00451654  74c5                     je       0x45161b
00451656  eb05                     jmp      0x45165d
00451658  80fa01                   cmp      dl, 1
0045165b  7498                     je       0x4515f5
0045165d  31db                     xor      ebx, ebx
0045165f  6689fb                   mov      bx, di
00451662  89da                     mov      edx, ebx
00451664  89d8                     mov      eax, ebx
00451666  c1fa1f                   sar      edx, 0x1f
00451669  c1e208                   shl      edx, 8
0045166c  1bc2                     sbb      eax, edx
0045166e  c1f808                   sar      eax, 8
00451671  31c9                     xor      ecx, ecx
00451673  bf00010000               mov      edi, 0x100
00451678  6689c1                   mov      cx, ax
0045167b  89da                     mov      edx, ebx
0045167d  89d8                     mov      eax, ebx
0045167f  c1fa1f                   sar      edx, 0x1f
00451682  f7ff                     idiv     edi
00451684  31db                     xor      ebx, ebx
00451686  31ff                     xor      edi, edi
00451688  668b5d08                 mov      bx, word ptr [ebp + 8]
0045168c  6689d7                   mov      di, dx
0045168f  89da                     mov      edx, ebx
00451691  89d8                     mov      eax, ebx
00451693  c1fa1f                   sar      edx, 0x1f
00451696  c1e208                   shl      edx, 8
00451699  1bc2                     sbb      eax, edx
0045169b  c1f808                   sar      eax, 8
0045169e  ba00010000               mov      edx, 0x100
004516a3  0fb7e8                   movzx    ebp, ax
004516a6  891424                   mov      dword ptr [esp], edx
004516a9  89d8                     mov      eax, ebx
004516ab  89da                     mov      edx, ebx
004516ad  8b1c24                   mov      ebx, dword ptr [esp]
004516b0  c1fa1f                   sar      edx, 0x1f
004516b3  f7fb                     idiv     ebx
004516b5  6a20                     push     0x20
004516b7  31c0                     xor      eax, eax
004516b9  89fb                     mov      ebx, edi
004516bb  6689d0                   mov      ax, dx
004516be  89ea                     mov      edx, ebp
004516c0  e806800200               call     0x4796cb
004516c5  3a8694000000             cmp      al, byte ptr [esi + 0x94]
004516cb  0f94c0                   sete     al
004516ce  e969dcffff               jmp      0x44f33c
