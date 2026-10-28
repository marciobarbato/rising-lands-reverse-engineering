; InitRecruteTroupe: Recruitment start; exit search at 0x42863b; exclusive end 0x00428691.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004283e2  53                       push     ebx
004283e3  51                       push     ecx
004283e4  56                       push     esi
004283e5  57                       push     edi
004283e6  83ec44                   sub      esp, 0x44
004283e9  8844243c                 mov      byte ptr [esp + 0x3c], al
004283ed  88542440                 mov      byte ptr [esp + 0x40], dl
004283f1  0fb6fa                   movzx    edi, dl
004283f4  668b047de05b4900         mov      ax, word ptr [edi*2 + 0x495be0]
004283fc  8d4c240c                 lea      ecx, [esp + 0xc]
00428400  25ffff0000               and      eax, 0xffff
00428405  8d5c2428                 lea      ebx, [esp + 0x28]
00428409  89c6                     mov      esi, eax
0042840b  31d2                     xor      edx, edx
0042840d  c1e604                   shl      esi, 4
00428410  89542408                 mov      dword ptr [esp + 8], edx
00428414  01c6                     add      esi, eax
00428416  8954240c                 mov      dword ptr [esp + 0xc], edx
0042841a  c1e602                   shl      esi, 2
0042841d  89542428                 mov      dword ptr [esp + 0x28], edx
00428421  01c6                     add      esi, eax
00428423  31c0                     xor      eax, eax
00428425  8d542408                 lea      edx, [esp + 8]
00428429  8a44243c                 mov      al, byte ptr [esp + 0x3c]
0042842d  c1e602                   shl      esi, 2
00428430  e89d8c0100               call     0x4410d2
00428435  57                       push     edi
00428436  31db                     xor      ebx, ebx
00428438  31d2                     xor      edx, edx
0042843a  31c0                     xor      eax, eax
0042843c  31c9                     xor      ecx, ecx
0042843e  668b5c2410               mov      bx, word ptr [esp + 0x10]
00428443  668b54242c               mov      dx, word ptr [esp + 0x2c]
00428448  668b44240c               mov      ax, word ptr [esp + 0xc]
0042844d  81c6c8a04900             add      esi, 0x49a0c8
00428453  e88df20300               call     0x4676e5
00428458  84c0                     test     al, al
0042845a  0f85e8010000             jne      0x428648
00428460  e922020000               jmp      0x428687
00428465  807e7400                 cmp      byte ptr [esi + 0x74], 0
00428469  0f8518020000             jne      0x428687
0042846f  b801000000               mov      eax, 1
00428474  31c9                     xor      ecx, ecx
00428476  31d2                     xor      edx, edx
00428478  8a4c2440                 mov      cl, byte ptr [esp + 0x40]
0042847c  668b542408               mov      dx, word ptr [esp + 8]
00428481  89cf                     mov      edi, ecx
00428483  89cb                     mov      ebx, ecx
00428485  c1e702                   shl      edi, 2
00428488  e89ff40300               call     0x46792c
0042848d  29cf                     sub      edi, ecx
0042848f  89c8                     mov      eax, ecx
00428491  01ff                     add      edi, edi
00428493  31c8                     xor      eax, ecx
00428495  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
0042849c  85c0                     test     eax, eax
0042849e  7e4e                     jle      0x4284ee
004284a0  8d5c2414                 lea      ebx, [esp + 0x14]
004284a4  8d542410                 lea      edx, [esp + 0x10]
004284a8  51                       push     ecx
004284a9  8d442424                 lea      eax, [esp + 0x24]
004284ad  8d4c2420                 lea      ecx, [esp + 0x20]
004284b1  e8e7f10300               call     0x46769d
004284b6  8b442420                 mov      eax, dword ptr [esp + 0x20]
004284ba  8b542410                 mov      edx, dword ptr [esp + 0x10]
004284be  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
004284c5  01d0                     add      eax, edx
004284c7  31d2                     xor      edx, edx
004284c9  66f7f3                   div      bx
004284cc  31d2                     xor      edx, edx
004284ce  6689c2                   mov      dx, ax
004284d1  89d0                     mov      eax, edx
004284d3  c1e003                   shl      eax, 3
004284d6  29d0                     sub      eax, edx
004284d8  31db                     xor      ebx, ebx
004284da  89c2                     mov      edx, eax
004284dc  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
004284e3  c1fa1f                   sar      edx, 0x1f
004284e6  f7fb                     idiv     ebx
004284e8  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
004284ee  b802000000               mov      eax, 2
004284f3  31c9                     xor      ecx, ecx
004284f5  31d2                     xor      edx, edx
004284f7  8a4c2440                 mov      cl, byte ptr [esp + 0x40]
004284fb  668b542428               mov      dx, word ptr [esp + 0x28]
00428500  89cf                     mov      edi, ecx
00428502  89cb                     mov      ebx, ecx
00428504  c1e702                   shl      edi, 2
00428507  e820f40300               call     0x46792c
0042850c  29cf                     sub      edi, ecx
0042850e  89c8                     mov      eax, ecx
00428510  01ff                     add      edi, edi
00428512  31c8                     xor      eax, ecx
00428514  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
0042851b  85c0                     test     eax, eax
0042851d  7e4e                     jle      0x42856d
0042851f  8d5c2430                 lea      ebx, [esp + 0x30]
00428523  8d54242c                 lea      edx, [esp + 0x2c]
00428527  51                       push     ecx
00428528  8d44241c                 lea      eax, [esp + 0x1c]
0042852c  8d4c2428                 lea      ecx, [esp + 0x28]
00428530  e868f10300               call     0x46769d
00428535  8b442418                 mov      eax, dword ptr [esp + 0x18]
00428539  8b4c242c                 mov      ecx, dword ptr [esp + 0x2c]
0042853d  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
00428544  31d2                     xor      edx, edx
00428546  01c8                     add      eax, ecx
00428548  66f7f3                   div      bx
0042854b  31d2                     xor      edx, edx
0042854d  6689c2                   mov      dx, ax
00428550  89d0                     mov      eax, edx
00428552  c1e003                   shl      eax, 3
00428555  29d0                     sub      eax, edx
00428557  31db                     xor      ebx, ebx
00428559  89c2                     mov      edx, eax
0042855b  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
00428562  c1fa1f                   sar      edx, 0x1f
00428565  f7fb                     idiv     ebx
00428567  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
0042856d  31c9                     xor      ecx, ecx
0042856f  31d2                     xor      edx, edx
00428571  31c0                     xor      eax, eax
00428573  8a4c2440                 mov      cl, byte ptr [esp + 0x40]
00428577  668b54240c               mov      dx, word ptr [esp + 0xc]
0042857c  89cf                     mov      edi, ecx
0042857e  89cb                     mov      ebx, ecx
00428580  c1e702                   shl      edi, 2
00428583  e8a4f30300               call     0x46792c
00428588  29cf                     sub      edi, ecx
0042858a  89c8                     mov      eax, ecx
0042858c  01ff                     add      edi, edi
0042858e  31c8                     xor      eax, ecx
00428590  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
00428597  85c0                     test     eax, eax
00428599  7e4e                     jle      0x4285e9
0042859b  8d5c2404                 lea      ebx, [esp + 4]
0042859f  8d542438                 lea      edx, [esp + 0x38]
004285a3  51                       push     ecx
004285a4  8d442438                 lea      eax, [esp + 0x38]
004285a8  8d4c2404                 lea      ecx, [esp + 4]
004285ac  e8ecf00300               call     0x46769d
004285b1  8b442434                 mov      eax, dword ptr [esp + 0x34]
004285b5  8b4c2438                 mov      ecx, dword ptr [esp + 0x38]
004285b9  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
004285c0  31d2                     xor      edx, edx
004285c2  01c8                     add      eax, ecx
004285c4  66f7f3                   div      bx
004285c7  31d2                     xor      edx, edx
004285c9  6689c2                   mov      dx, ax
004285cc  89d0                     mov      eax, edx
004285ce  c1e003                   shl      eax, 3
004285d1  29d0                     sub      eax, edx
004285d3  31db                     xor      ebx, ebx
004285d5  89c2                     mov      edx, eax
004285d7  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
004285de  c1fa1f                   sar      edx, 0x1f
004285e1  f7fb                     idiv     ebx
004285e3  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
004285e9  c6467401                 mov      byte ptr [esi + 0x74], 1
004285ed  c6467a00                 mov      byte ptr [esi + 0x7a], 0
004285f1  c6460504                 mov      byte ptr [esi + 5], 4
004285f5  8a44243c                 mov      al, byte ptr [esp + 0x3c]
004285f9  c7868c00000001000000     mov      dword ptr [esi + 0x8c], 1
00428603  88467b                   mov      byte ptr [esi + 0x7b], al
00428606  31c0                     xor      eax, eax
00428608  8a4608                   mov      al, byte ptr [esi + 8]
0042860b  66c7467e0000             mov      word ptr [esi + 0x7e], 0
00428611  83f814                   cmp      eax, 0x14
00428614  7412                     je       0x428628
00428616  66c786800000000000       mov      word ptr [esi + 0x80], 0
0042861f  66c786820000000000       mov      word ptr [esi + 0x82], 0
00428628  31c0                     xor      eax, eax
0042862a  8a442440                 mov      al, byte ptr [esp + 0x40]
0042862e  668b0445e05b4900         mov      ax, word ptr [eax*2 + 0x495be0]
00428636  25ffff0000               and      eax, 0xffff
0042863b  e8904bffff               call     0x41d1d0
00428640  6689467c                 mov      word ptr [esi + 0x7c], ax
00428644  b001                     mov      al, 1
00428646  eb41                     jmp      0x428689
00428648  8a4608                   mov      al, byte ptr [esi + 8]
0042864b  3c0f                     cmp      al, 0xf
0042864d  721e                     jb       0x42866d
0042864f  0f8610feffff             jbe      0x428465
00428655  3c12                     cmp      al, 0x12
00428657  7210                     jb       0x428669
00428659  0f8606feffff             jbe      0x428465
0042865f  3c14                     cmp      al, 0x14
00428661  0f84fefdffff             je       0x428465
00428667  eb1e                     jmp      0x428687
00428669  3c10                     cmp      al, 0x10
0042866b  ebf4                     jmp      0x428661
0042866d  3c05                     cmp      al, 5
0042866f  720a                     jb       0x42867b
00428671  0f86eefdffff             jbe      0x428465
00428677  3c0d                     cmp      al, 0xd
00428679  ebe6                     jmp      0x428661
0042867b  3c01                     cmp      al, 1
0042867d  7208                     jb       0x428687
0042867f  3c02                     cmp      al, 2
00428681  0f86defdffff             jbe      0x428465
00428687  30c0                     xor      al, al
00428689  83c444                   add      esp, 0x44
0042868c  5f                       pop      edi
0042868d  5e                       pop      esi
0042868e  59                       pop      ecx
0042868f  5b                       pop      ebx
00428690  c3                       ret
