; TerrainDeposeMatiere: limite por próximo símbolo SBL, fim exclusivo 0x0041be88.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0041bb8a  56                       push     esi
0041bb8b  57                       push     edi
0041bb8c  55                       push     ebp
0041bb8d  83ec50                   sub      esp, 0x50
0041bb90  53                       push     ebx
0041bb91  81e2ffff0000             and      edx, 0xffff
0041bb97  89d6                     mov      esi, edx
0041bb99  c1e604                   shl      esi, 4
0041bb9c  01d6                     add      esi, edx
0041bb9e  c1e602                   shl      esi, 2
0041bba1  01d6                     add      esi, edx
0041bba3  bdc8a04900               mov      ebp, 0x49a0c8
0041bba8  c1e602                   shl      esi, 2
0041bbab  01f5                     add      ebp, esi
0041bbad  84c9                     test     cl, cl
0041bbaf  7612                     jbe      0x41bbc3
0041bbb1  80f901                   cmp      cl, 1
0041bbb4  0f8471010000             je       0x41bd2b
0041bbba  83c454                   add      esp, 0x54
0041bbbd  5d                       pop      ebp
0041bbbe  5f                       pop      edi
0041bbbf  5e                       pop      esi
0041bbc0  c20400                   ret      4
0041bbc3  8d4c2404                 lea      ecx, [esp + 4]
0041bbc7  0fb6f8                   movzx    edi, al
0041bbca  8d5c2408                 lea      ebx, [esp + 8]
0041bbce  57                       push     edi
0041bbcf  8d542410                 lea      edx, [esp + 0x10]
0041bbd3  8d442430                 lea      eax, [esp + 0x30]
0041bbd7  e8c1ba0400               call     0x46769d
0041bbdc  31d2                     xor      edx, edx
0041bbde  668b54242c               mov      dx, word ptr [esp + 0x2c]
0041bbe3  85d2                     test     edx, edx
0041bbe5  0f8eec000000             jle      0x41bcd7
0041bbeb  89fe                     mov      esi, edi
0041bbed  c1e602                   shl      esi, 2
0041bbf0  29fe                     sub      esi, edi
0041bbf2  89f8                     mov      eax, edi
0041bbf4  01f6                     add      esi, esi
0041bbf6  31f8                     xor      eax, edi
0041bbf8  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bbff  85c0                     test     eax, eax
0041bc01  7e6d                     jle      0x41bc70
0041bc03  8b44242c                 mov      eax, dword ptr [esp + 0x2c]
0041bc07  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
0041bc0e  31d2                     xor      edx, edx
0041bc10  66f7f3                   div      bx
0041bc13  8944242c                 mov      dword ptr [esp + 0x2c], eax
0041bc17  89c1                     mov      ecx, eax
0041bc19  89fb                     mov      ebx, edi
0041bc1b  31d2                     xor      edx, edx
0041bc1d  66d1e9                   shr      cx, 1
0041bc20  b801000000               mov      eax, 1
0041bc25  6689ca                   mov      dx, cx
0041bc28  894c242c                 mov      dword ptr [esp + 0x2c], ecx
0041bc2c  e8fbbc0400               call     0x46792c
0041bc31  31c0                     xor      eax, eax
0041bc33  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bc3a  85c0                     test     eax, eax
0041bc3c  0f8e95000000             jle      0x41bcd7
0041bc42  8d4c2448                 lea      ecx, [esp + 0x48]
0041bc46  8d5c2414                 lea      ebx, [esp + 0x14]
0041bc4a  57                       push     edi
0041bc4b  8d542414                 lea      edx, [esp + 0x14]
0041bc4f  8d442448                 lea      eax, [esp + 0x48]
0041bc53  e845ba0400               call     0x46769d
0041bc58  8b442444                 mov      eax, dword ptr [esp + 0x44]
0041bc5c  8b7c2410                 mov      edi, dword ptr [esp + 0x10]
0041bc60  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
0041bc67  31d2                     xor      edx, edx
0041bc69  01f8                     add      eax, edi
0041bc6b  66f7f3                   div      bx
0041bc6e  eb45                     jmp      0x41bcb5
0041bc70  b801000000               mov      eax, 1
0041bc75  89fb                     mov      ebx, edi
0041bc77  e8b0bc0400               call     0x46792c
0041bc7c  31c0                     xor      eax, eax
0041bc7e  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bc85  85c0                     test     eax, eax
0041bc87  7e4e                     jle      0x41bcd7
0041bc89  8d4c2424                 lea      ecx, [esp + 0x24]
0041bc8d  8d5c2420                 lea      ebx, [esp + 0x20]
0041bc91  57                       push     edi
0041bc92  8d542420                 lea      edx, [esp + 0x20]
0041bc96  8d44241c                 lea      eax, [esp + 0x1c]
0041bc9a  e8feb90400               call     0x46769d
0041bc9f  8b442418                 mov      eax, dword ptr [esp + 0x18]
0041bca3  8b4c241c                 mov      ecx, dword ptr [esp + 0x1c]
0041bca7  668bbe2cfb4d00           mov      di, word ptr [esi + 0x4dfb2c]
0041bcae  31d2                     xor      edx, edx
0041bcb0  01c8                     add      eax, ecx
0041bcb2  66f7f7                   div      di
0041bcb5  31db                     xor      ebx, ebx
0041bcb7  668b9e2efb4d00           mov      bx, word ptr [esi + 0x4dfb2e]
0041bcbe  25ffff0000               and      eax, 0xffff
0041bcc3  89c2                     mov      edx, eax
0041bcc5  c1e203                   shl      edx, 3
0041bcc8  29c2                     sub      edx, eax
0041bcca  89d0                     mov      eax, edx
0041bccc  c1fa1f                   sar      edx, 0x1f
0041bccf  f7fb                     idiv     ebx
0041bcd1  888630fb4d00             mov      byte ptr [esi + 0x4dfb30], al
0041bcd7  807c246400               cmp      byte ptr [esp + 0x64], 0
0041bcdc  7431                     je       0x41bd0f
0041bcde  31d2                     xor      edx, edx
0041bce0  8a5508                   mov      dl, byte ptr [ebp + 8]
0041bce3  89d6                     mov      esi, edx
0041bce5  c1e602                   shl      esi, 2
0041bce8  29d6                     sub      esi, edx
0041bcea  c1e602                   shl      esi, 2
0041bced  01d6                     add      esi, edx
0041bcef  31d2                     xor      edx, edx
0041bcf1  668b14b5985d4900         mov      dx, word ptr [esi*4 + 0x495d98]
0041bcf9  89d0                     mov      eax, edx
0041bcfb  c1fa1f                   sar      edx, 0x1f
0041bcfe  2bc2                     sub      eax, edx
0041bd00  d1f8                     sar      eax, 1
0041bd02  31d2                     xor      edx, edx
0041bd04  668b54242c               mov      dx, word ptr [esp + 0x2c]
0041bd09  01c2                     add      edx, eax
0041bd0b  8954242c                 mov      dword ptr [esp + 0x2c], edx
0041bd0f  ba01000000               mov      edx, 1
0041bd14  31db                     xor      ebx, ebx
0041bd16  31c0                     xor      eax, eax
0041bd18  668b5c242c               mov      bx, word ptr [esp + 0x2c]
0041bd1d  668b0424                 mov      ax, word ptr [esp]
0041bd21  e883a40500               call     0x4761a9
0041bd26  e98ffeffff               jmp      0x41bbba
0041bd2b  8d4c2404                 lea      ecx, [esp + 4]
0041bd2f  0fb6f8                   movzx    edi, al
0041bd32  8d5c2408                 lea      ebx, [esp + 8]
0041bd36  57                       push     edi
0041bd37  8d542410                 lea      edx, [esp + 0x10]
0041bd3b  8d442430                 lea      eax, [esp + 0x30]
0041bd3f  e859b90400               call     0x46769d
0041bd44  31d2                     xor      edx, edx
0041bd46  668b54240c               mov      dx, word ptr [esp + 0xc]
0041bd4b  85d2                     test     edx, edx
0041bd4d  0f8edc000000             jle      0x41be2f
0041bd53  89fe                     mov      esi, edi
0041bd55  c1e602                   shl      esi, 2
0041bd58  29fe                     sub      esi, edi
0041bd5a  89f8                     mov      eax, edi
0041bd5c  01f6                     add      esi, esi
0041bd5e  31f8                     xor      eax, edi
0041bd60  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bd67  85c0                     test     eax, eax
0041bd69  7e5d                     jle      0x41bdc8
0041bd6b  8b44240c                 mov      eax, dword ptr [esp + 0xc]
0041bd6f  668b8e2cfb4d00           mov      cx, word ptr [esi + 0x4dfb2c]
0041bd76  31d2                     xor      edx, edx
0041bd78  66f7f1                   div      cx
0041bd7b  89fb                     mov      ebx, edi
0041bd7d  8944240c                 mov      dword ptr [esp + 0xc], eax
0041bd81  66d1e8                   shr      ax, 1
0041bd84  31d2                     xor      edx, edx
0041bd86  8944240c                 mov      dword ptr [esp + 0xc], eax
0041bd8a  6689c2                   mov      dx, ax
0041bd8d  b802000000               mov      eax, 2
0041bd92  e895bb0400               call     0x46792c
0041bd97  31c0                     xor      eax, eax
0041bd99  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bda0  85c0                     test     eax, eax
0041bda2  0f8e87000000             jle      0x41be2f
0041bda8  8d4c2440                 lea      ecx, [esp + 0x40]
0041bdac  8d5c2438                 lea      ebx, [esp + 0x38]
0041bdb0  57                       push     edi
0041bdb1  8d542438                 lea      edx, [esp + 0x38]
0041bdb5  8d442434                 lea      eax, [esp + 0x34]
0041bdb9  e8dfb80400               call     0x46769d
0041bdbe  8b442430                 mov      eax, dword ptr [esp + 0x30]
0041bdc2  8b542434                 mov      edx, dword ptr [esp + 0x34]
0041bdc6  eb37                     jmp      0x41bdff
0041bdc8  b802000000               mov      eax, 2
0041bdcd  89fb                     mov      ebx, edi
0041bdcf  e858bb0400               call     0x46792c
0041bdd4  31c0                     xor      eax, eax
0041bdd6  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041bddd  85c0                     test     eax, eax
0041bddf  7e4e                     jle      0x41be2f
0041bde1  8d4c2428                 lea      ecx, [esp + 0x28]
0041bde5  8d5c243c                 lea      ebx, [esp + 0x3c]
0041bde9  57                       push     edi
0041bdea  8d542454                 lea      edx, [esp + 0x54]
0041bdee  8d442450                 lea      eax, [esp + 0x50]
0041bdf2  e8a6b80400               call     0x46769d
0041bdf7  8b44244c                 mov      eax, dword ptr [esp + 0x4c]
0041bdfb  8b542450                 mov      edx, dword ptr [esp + 0x50]
0041bdff  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
0041be06  01d0                     add      eax, edx
0041be08  31d2                     xor      edx, edx
0041be0a  66f7f3                   div      bx
0041be0d  31db                     xor      ebx, ebx
0041be0f  668b9e2efb4d00           mov      bx, word ptr [esi + 0x4dfb2e]
0041be16  25ffff0000               and      eax, 0xffff
0041be1b  89c2                     mov      edx, eax
0041be1d  c1e203                   shl      edx, 3
0041be20  29c2                     sub      edx, eax
0041be22  89d0                     mov      eax, edx
0041be24  c1fa1f                   sar      edx, 0x1f
0041be27  f7fb                     idiv     ebx
0041be29  888630fb4d00             mov      byte ptr [esi + 0x4dfb30], al
0041be2f  807c246400               cmp      byte ptr [esp + 0x64], 0
0041be34  7431                     je       0x41be67
0041be36  31d2                     xor      edx, edx
0041be38  8a5508                   mov      dl, byte ptr [ebp + 8]
0041be3b  89d6                     mov      esi, edx
0041be3d  c1e602                   shl      esi, 2
0041be40  29d6                     sub      esi, edx
0041be42  c1e602                   shl      esi, 2
0041be45  01d6                     add      esi, edx
0041be47  31d2                     xor      edx, edx
0041be49  668b14b59a5d4900         mov      dx, word ptr [esi*4 + 0x495d9a]
0041be51  89d0                     mov      eax, edx
0041be53  c1fa1f                   sar      edx, 0x1f
0041be56  2bc2                     sub      eax, edx
0041be58  d1f8                     sar      eax, 1
0041be5a  31d2                     xor      edx, edx
0041be5c  668b54240c               mov      dx, word ptr [esp + 0xc]
0041be61  01c2                     add      edx, eax
0041be63  8954240c                 mov      dword ptr [esp + 0xc], edx
0041be67  31d2                     xor      edx, edx
0041be69  668b54240c               mov      dx, word ptr [esp + 0xc]
0041be6e  89d0                     mov      eax, edx
0041be70  c1fa1f                   sar      edx, 0x1f
0041be73  2bc2                     sub      eax, edx
0041be75  d1f8                     sar      eax, 1
0041be77  31db                     xor      ebx, ebx
0041be79  6689c3                   mov      bx, ax
0041be7c  31c0                     xor      eax, eax
0041be7e  ba02000000               mov      edx, 2
0041be83  e995feffff               jmp      0x41bd1d
