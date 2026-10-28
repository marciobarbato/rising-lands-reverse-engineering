; EnginGetVolume; [0x00440c5d, 0x00440d5e)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00440c5d  53                       push     ebx
00440c5e  51                       push     ecx
00440c5f  52                       push     edx
00440c60  56                       push     esi
00440c61  57                       push     edi
00440c62  83ec04                   sub      esp, 4
00440c65  89c6                     mov      esi, eax
00440c67  31c0                     xor      eax, eax
00440c69  6689f0                   mov      ax, si
00440c6c  89c3                     mov      ebx, eax
00440c6e  c1e304                   shl      ebx, 4
00440c71  01c3                     add      ebx, eax
00440c73  c1e302                   shl      ebx, 2
00440c76  01c3                     add      ebx, eax
00440c78  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00440c7d  668b5c9808               mov      bx, word ptr [eax + ebx*4 + 8]
00440c82  81e3ffff0000             and      ebx, 0xffff
00440c88  b900010000               mov      ecx, 0x100
00440c8d  89da                     mov      edx, ebx
00440c8f  89d8                     mov      eax, ebx
00440c91  c1fa1f                   sar      edx, 0x1f
00440c94  f7f9                     idiv     ecx
00440c96  89d7                     mov      edi, edx
00440c98  89da                     mov      edx, ebx
00440c9a  89d8                     mov      eax, ebx
00440c9c  c1fa1f                   sar      edx, 0x1f
00440c9f  f7f9                     idiv     ecx
00440ca1  31d2                     xor      edx, edx
00440ca3  668b1524875000           mov      dx, word ptr [0x508724]
00440caa  89c3                     mov      ebx, eax
00440cac  89d0                     mov      eax, edx
00440cae  c1fa1f                   sar      edx, 0x1f
00440cb1  2bc2                     sub      eax, edx
00440cb3  d1f8                     sar      eax, 1
00440cb5  31d2                     xor      edx, edx
00440cb7  668b1520875000           mov      dx, word ptr [0x508720]
00440cbe  01d0                     add      eax, edx
00440cc0  31d2                     xor      edx, edx
00440cc2  668b1526875000           mov      dx, word ptr [0x508726]
00440cc9  890424                   mov      dword ptr [esp], eax
00440ccc  89d0                     mov      eax, edx
00440cce  c1fa1f                   sar      edx, 0x1f
00440cd1  2bc2                     sub      eax, edx
00440cd3  d1f8                     sar      eax, 1
00440cd5  31d2                     xor      edx, edx
00440cd7  31c9                     xor      ecx, ecx
00440cd9  668b1522875000           mov      dx, word ptr [0x508722]
00440ce0  6689d9                   mov      cx, bx
00440ce3  01d0                     add      eax, edx
00440ce5  31d2                     xor      edx, edx
00440ce7  31db                     xor      ebx, ebx
00440ce9  6689c2                   mov      dx, ax
00440cec  31c0                     xor      eax, eax
00440cee  6689fb                   mov      bx, di
00440cf1  668b0424                 mov      ax, word ptr [esp]
00440cf5  e85b880300               call     0x479555
00440cfa  89c2                     mov      edx, eax
00440cfc  31db                     xor      ebx, ebx
00440cfe  3d91000000               cmp      eax, 0x91
00440d03  7f07                     jg       0x440d0c
00440d05  bb00010000               mov      ebx, 0x100
00440d0a  eb25                     jmp      0x440d31
00440d0c  7e0e                     jle      0x440d1c
00440d0e  3d2c010000               cmp      eax, 0x12c
00440d13  7f07                     jg       0x440d1c
00440d15  bbb4000000               mov      ebx, 0xb4
00440d1a  eb15                     jmp      0x440d31
00440d1c  81fa2c010000             cmp      edx, 0x12c
00440d22  7e0d                     jle      0x440d31
00440d24  81fa58020000             cmp      edx, 0x258
00440d2a  7d05                     jge      0x440d31
00440d2c  bb64000000               mov      ebx, 0x64
00440d31  31c0                     xor      eax, eax
00440d33  31d2                     xor      edx, edx
00440d35  a041805000               mov      al, byte ptr [0x508041]
00440d3a  6689f2                   mov      dx, si
00440d3d  e832140300               call     0x472174
00440d42  84c0                     test     al, al
00440d44  750d                     jne      0x440d53
00440d46  89da                     mov      edx, ebx
00440d48  89d8                     mov      eax, ebx
00440d4a  c1fa1f                   sar      edx, 0x1f
00440d4d  2bc2                     sub      eax, edx
00440d4f  d1f8                     sar      eax, 1
00440d51  89c3                     mov      ebx, eax
00440d53  89d8                     mov      eax, ebx
00440d55  83c404                   add      esp, 4
00440d58  5f                       pop      edi
00440d59  5e                       pop      esi
00440d5a  5a                       pop      edx
00440d5b  59                       pop      ecx
00440d5c  5b                       pop      ebx
00440d5d  c3                       ret
