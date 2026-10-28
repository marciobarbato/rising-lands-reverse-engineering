; InitApprentissage: limite por próximo símbolo SBL, fim exclusivo 0x00422f08.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00422d9f  53                       push     ebx
00422da0  51                       push     ecx
00422da1  56                       push     esi
00422da2  57                       push     edi
00422da3  55                       push     ebp
00422da4  83ec34                   sub      esp, 0x34
00422da7  8844242c                 mov      byte ptr [esp + 0x2c], al
00422dab  88542430                 mov      byte ptr [esp + 0x30], dl
00422daf  0fb6e8                   movzx    ebp, al
00422db2  31d2                     xor      edx, edx
00422db4  668b146de05b4900         mov      dx, word ptr [ebp*2 + 0x495be0]
00422dbc  89d0                     mov      eax, edx
00422dbe  c1e004                   shl      eax, 4
00422dc1  01d0                     add      eax, edx
00422dc3  c1e002                   shl      eax, 2
00422dc6  01d0                     add      eax, edx
00422dc8  bec8a04900               mov      esi, 0x49a0c8
00422dcd  c1e002                   shl      eax, 2
00422dd0  01c6                     add      esi, eax
00422dd2  807e7400                 cmp      byte ptr [esi + 0x74], 0
00422dd6  0f8524010000             jne      0x422f00
00422ddc  8d4c2404                 lea      ecx, [esp + 4]
00422de0  89e3                     mov      ebx, esp
00422de2  31c0                     xor      eax, eax
00422de4  8d542408                 lea      edx, [esp + 8]
00422de8  8a442430                 mov      al, byte ptr [esp + 0x30]
00422dec  89ef                     mov      edi, ebp
00422dee  e80b190500               call     0x4746fe
00422df3  c1e702                   shl      edi, 2
00422df6  b801000000               mov      eax, 1
00422dfb  31d2                     xor      edx, edx
00422dfd  89eb                     mov      ebx, ebp
00422dff  668b542408               mov      dx, word ptr [esp + 8]
00422e04  29ef                     sub      edi, ebp
00422e06  e8214b0400               call     0x46792c
00422e0b  89e8                     mov      eax, ebp
00422e0d  01ff                     add      edi, edi
00422e0f  31e8                     xor      eax, ebp
00422e11  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
00422e18  85c0                     test     eax, eax
00422e1a  7e4e                     jle      0x422e6a
00422e1c  8d4c2414                 lea      ecx, [esp + 0x14]
00422e20  8d5c2420                 lea      ebx, [esp + 0x20]
00422e24  55                       push     ebp
00422e25  8d542420                 lea      edx, [esp + 0x20]
00422e29  8d44241c                 lea      eax, [esp + 0x1c]
00422e2d  e86b480400               call     0x46769d
00422e32  8b442418                 mov      eax, dword ptr [esp + 0x18]
00422e36  8b54241c                 mov      edx, dword ptr [esp + 0x1c]
00422e3a  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
00422e41  01d0                     add      eax, edx
00422e43  31d2                     xor      edx, edx
00422e45  66f7f3                   div      bx
00422e48  31d2                     xor      edx, edx
00422e4a  6689c2                   mov      dx, ax
00422e4d  89d0                     mov      eax, edx
00422e4f  c1e003                   shl      eax, 3
00422e52  29d0                     sub      eax, edx
00422e54  31db                     xor      ebx, ebx
00422e56  89c2                     mov      edx, eax
00422e58  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
00422e5f  c1fa1f                   sar      edx, 0x1f
00422e62  f7fb                     idiv     ebx
00422e64  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
00422e6a  0fb66c242c               movzx    ebp, byte ptr [esp + 0x2c]
00422e6f  31d2                     xor      edx, edx
00422e71  b802000000               mov      eax, 2
00422e76  668b1424                 mov      dx, word ptr [esp]
00422e7a  89ef                     mov      edi, ebp
00422e7c  89eb                     mov      ebx, ebp
00422e7e  c1e702                   shl      edi, 2
00422e81  e8a64a0400               call     0x46792c
00422e86  29ef                     sub      edi, ebp
00422e88  89e8                     mov      eax, ebp
00422e8a  01ff                     add      edi, edi
00422e8c  31e8                     xor      eax, ebp
00422e8e  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
00422e95  85c0                     test     eax, eax
00422e97  7e4e                     jle      0x422ee7
00422e99  8d4c2428                 lea      ecx, [esp + 0x28]
00422e9d  8d5c2424                 lea      ebx, [esp + 0x24]
00422ea1  55                       push     ebp
00422ea2  8d542410                 lea      edx, [esp + 0x10]
00422ea6  8d442414                 lea      eax, [esp + 0x14]
00422eaa  e8ee470400               call     0x46769d
00422eaf  8b442410                 mov      eax, dword ptr [esp + 0x10]
00422eb3  8b4c240c                 mov      ecx, dword ptr [esp + 0xc]
00422eb7  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
00422ebe  31d2                     xor      edx, edx
00422ec0  01c8                     add      eax, ecx
00422ec2  66f7f3                   div      bx
00422ec5  31d2                     xor      edx, edx
00422ec7  6689c2                   mov      dx, ax
00422eca  89d0                     mov      eax, edx
00422ecc  c1e003                   shl      eax, 3
00422ecf  29d0                     sub      eax, edx
00422ed1  31db                     xor      ebx, ebx
00422ed3  89c2                     mov      edx, eax
00422ed5  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
00422edc  c1fa1f                   sar      edx, 0x1f
00422edf  f7fb                     idiv     ebx
00422ee1  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
00422ee7  c6467401                 mov      byte ptr [esi + 0x74], 1
00422eeb  c6460504                 mov      byte ptr [esi + 5], 4
00422eef  8a442430                 mov      al, byte ptr [esp + 0x30]
00422ef3  c7868c00000001000000     mov      dword ptr [esi + 0x8c], 1
00422efd  88467b                   mov      byte ptr [esi + 0x7b], al
00422f00  83c434                   add      esp, 0x34
00422f03  e9920a0000               jmp      0x42399a
