; BallonPrepareArrivee: limite por próximo símbolo SBL, fim exclusivo 0x00441d4f.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00441baa  53                       push     ebx
00441bab  51                       push     ecx
00441bac  52                       push     edx
00441bad  56                       push     esi
00441bae  57                       push     edi
00441baf  83ec0c                   sub      esp, 0xc
00441bb2  88442408                 mov      byte ptr [esp + 8], al
00441bb6  31db                     xor      ebx, ebx
00441bb8  88c3                     mov      bl, al
00441bba  89d9                     mov      ecx, ebx
00441bbc  c1e103                   shl      ecx, 3
00441bbf  31c0                     xor      eax, eax
00441bc1  668b81141a4e00           mov      ax, word ptr [ecx + 0x4e1a14]
00441bc8  85c0                     test     eax, eax
00441bca  0f8569010000             jne      0x441d39
00441bd0  668b81181a4e00           mov      ax, word ptr [ecx + 0x4e1a18]
00441bd7  3dffff0000               cmp      eax, 0xffff
00441bdc  0f85fa000000             jne      0x441cdc
00441be2  b810000000               mov      eax, 0x10
00441be7  e8f0e80200               call     0x4704dc
00441bec  31f6                     xor      esi, esi
00441bee  31d2                     xor      edx, edx
00441bf0  668b3568714900           mov      si, word ptr [0x497168]
00441bf7  f7f6                     div      esi
00441bf9  31c0                     xor      eax, eax
00441bfb  6689911a1a4e00           mov      word ptr [ecx + 0x4e1a1a], dx
00441c02  6689d0                   mov      ax, dx
00441c05  89d9                     mov      ecx, ebx
00441c07  bb11000000               mov      ebx, 0x11
00441c0c  ba01000000               mov      edx, 1
00441c11  31f6                     xor      esi, esi
00441c13  e854620100               call     0x457e6c
00441c18  ba45000000               mov      edx, 0x45
00441c1d  89c7                     mov      edi, eax
00441c1f  6689c6                   mov      si, ax
00441c22  31db                     xor      ebx, ebx
00441c24  89f0                     mov      eax, esi
00441c26  e89d0d0400               call     0x4829c8
00441c2b  89f3                     mov      ebx, esi
00441c2d  c1e304                   shl      ebx, 4
00441c30  01f3                     add      ebx, esi
00441c32  c1e302                   shl      ebx, 2
00441c35  01f3                     add      ebx, esi
00441c37  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00441c3d  c1e302                   shl      ebx, 2
00441c40  31d2                     xor      edx, edx
00441c42  668b441908               mov      ax, word ptr [ecx + ebx + 8]
00441c47  6689c2                   mov      dx, ax
00441c4a  89f0                     mov      eax, esi
00441c4c  e863100000               call     0x442cb4
00441c51  c644197201               mov      byte ptr [ecx + ebx + 0x72], 1
00441c56  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00441c5c  01d9                     add      ecx, ebx
00441c5e  31db                     xor      ebx, ebx
00441c60  668b4108                 mov      ax, word ptr [ecx + 8]
00441c64  8a19                     mov      bl, byte ptr [ecx]
00441c66  89442404                 mov      dword ptr [esp + 4], eax
00441c6a  81fbc8000000             cmp      ebx, 0xc8
00441c70  7453                     je       0x441cc5
00441c72  83fb04                   cmp      ebx, 4
00441c75  744e                     je       0x441cc5
00441c77  30e4                     xor      ah, ah
00441c79  8a81bb000000             mov      al, byte ptr [ecx + 0xbb]
00441c7f  89c2                     mov      edx, eax
00441c81  83c202                   add      edx, 2
00441c84  8a81f5000000             mov      al, byte ptr [ecx + 0xf5]
00441c8a  31f6                     xor      esi, esi
00441c8c  01d0                     add      eax, edx
00441c8e  31d2                     xor      edx, edx
00441c90  668b742404               mov      si, word ptr [esp + 4]
00441c95  6689c2                   mov      dx, ax
00441c98  89f0                     mov      eax, esi
00441c9a  e8b24b0300               call     0x476851
00441c9f  30e4                     xor      ah, ah
00441ca1  8a81bb000000             mov      al, byte ptr [ecx + 0xbb]
00441ca7  890424                   mov      dword ptr [esp], eax
00441caa  8b1424                   mov      edx, dword ptr [esp]
00441cad  8a81f5000000             mov      al, byte ptr [ecx + 0xf5]
00441cb3  31db                     xor      ebx, ebx
00441cb5  01d0                     add      eax, edx
00441cb7  31d2                     xor      edx, edx
00441cb9  8a19                     mov      bl, byte ptr [ecx]
00441cbb  6689c2                   mov      dx, ax
00441cbe  89f0                     mov      eax, esi
00441cc0  e8ee4f0300               call     0x476cb3
00441cc5  ba04000000               mov      edx, 4
00441cca  31db                     xor      ebx, ebx
00441ccc  31c0                     xor      eax, eax
00441cce  668b5c2404               mov      bx, word ptr [esp + 4]
00441cd3  8a01                     mov      al, byte ptr [ecx]
00441cd5  e8ae860200               call     0x46a388
00441cda  eb02                     jmp      0x441cde
00441cdc  89c7                     mov      edi, eax
00441cde  31db                     xor      ebx, ebx
00441ce0  8a5c2408                 mov      bl, byte ptr [esp + 8]
00441ce4  b802000000               mov      eax, 2
00441ce9  89da                     mov      edx, ebx
00441ceb  e874bb0100               call     0x45d864
00441cf0  25ffff0000               and      eax, 0xffff
00441cf5  3dffff0000               cmp      eax, 0xffff
00441cfa  751b                     jne      0x441d17
00441cfc  b812000000               mov      eax, 0x12
00441d01  89da                     mov      edx, ebx
00441d03  e85cbb0100               call     0x45d864
00441d08  25ffff0000               and      eax, 0xffff
00441d0d  e8d091fdff               call     0x41aee2
00441d12  80c402                   add      ah, 2
00441d15  eb05                     jmp      0x441d1c
00441d17  e8c691fdff               call     0x41aee2
00441d1c  31d2                     xor      edx, edx
00441d1e  6689c2                   mov      dx, ax
00441d21  31c0                     xor      eax, eax
00441d23  6689f8                   mov      ax, di
00441d26  e8a83a0000               call     0x4457d3
00441d2b  31c0                     xor      eax, eax
00441d2d  8a442408                 mov      al, byte ptr [esp + 8]
00441d31  66893cc5181a4e00         mov      word ptr [eax*8 + 0x4e1a18], di
00441d39  31c9                     xor      ecx, ecx
00441d3b  8a4c2408                 mov      cl, byte ptr [esp + 8]
00441d3f  66ff04cd141a4e00         inc      word ptr [ecx*8 + 0x4e1a14]
00441d47  83c40c                   add      esp, 0xc
00441d4a  e909f0ffff               jmp      0x440d58
