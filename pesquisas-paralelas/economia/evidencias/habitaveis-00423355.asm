; BatimentCalculResource: Same level formula as the inline type-3 block; exclusive end 0x004233d8.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00423355  53                       push     ebx
00423356  51                       push     ecx
00423357  52                       push     edx
00423358  56                       push     esi
00423359  83ec10                   sub      esp, 0x10
0042335c  25ff000000               and      eax, 0xff
00423361  83f804                   cmp      eax, 4
00423364  0f8dbbfcffff             jge      0x423025
0042336a  89c6                     mov      esi, eax
0042336c  c1e602                   shl      esi, 2
0042336f  29c6                     sub      esi, eax
00423371  89c2                     mov      edx, eax
00423373  01f6                     add      esi, esi
00423375  31c2                     xor      edx, eax
00423377  668b962cfb4d00           mov      dx, word ptr [esi + 0x4dfb2c]
0042337e  85d2                     test     edx, edx
00423380  0f8e9ffcffff             jle      0x423025
00423386  8d4c2404                 lea      ecx, [esp + 4]
0042338a  8d5c2408                 lea      ebx, [esp + 8]
0042338e  50                       push     eax
0042338f  8d542410                 lea      edx, [esp + 0x10]
00423393  8d442404                 lea      eax, [esp + 4]
00423397  e801430400               call     0x46769d
0042339c  8b0424                   mov      eax, dword ptr [esp]
0042339f  8b54240c                 mov      edx, dword ptr [esp + 0xc]
004233a3  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
004233aa  01d0                     add      eax, edx
004233ac  31d2                     xor      edx, edx
004233ae  66f7f3                   div      bx
004233b1  31d2                     xor      edx, edx
004233b3  6689c2                   mov      dx, ax
004233b6  89d0                     mov      eax, edx
004233b8  c1e003                   shl      eax, 3
004233bb  29d0                     sub      eax, edx
004233bd  31db                     xor      ebx, ebx
004233bf  89c2                     mov      edx, eax
004233c1  668b9e2efb4d00           mov      bx, word ptr [esi + 0x4dfb2e]
004233c8  c1fa1f                   sar      edx, 0x1f
004233cb  f7fb                     idiv     ebx
004233cd  888630fb4d00             mov      byte ptr [esi + 0x4dfb30], al
004233d3  e94dfcffff               jmp      0x423025
