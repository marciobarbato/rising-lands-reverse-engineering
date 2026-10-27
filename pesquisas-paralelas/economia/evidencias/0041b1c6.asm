; GarageCalculCoutReparation: limite por próximo símbolo SBL, fim exclusivo 0x0041b327.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0041b1c6  53                       push     ebx
0041b1c7  51                       push     ecx
0041b1c8  52                       push     edx
0041b1c9  56                       push     esi
0041b1ca  57                       push     edi
0041b1cb  83ec1c                   sub      esp, 0x1c
0041b1ce  25ffff0000               and      eax, 0xffff
0041b1d3  89c6                     mov      esi, eax
0041b1d5  c1e604                   shl      esi, 4
0041b1d8  01c6                     add      esi, eax
0041b1da  c1e602                   shl      esi, 2
0041b1dd  01c6                     add      esi, eax
0041b1df  31d2                     xor      edx, edx
0041b1e1  c1e602                   shl      esi, 2
0041b1e4  89542410                 mov      dword ptr [esp + 0x10], edx
0041b1e8  81c6c8a04900             add      esi, 0x49a0c8
0041b1ee  89542408                 mov      dword ptr [esp + 8], edx
0041b1f2  31c0                     xor      eax, eax
0041b1f4  668b8688000000           mov      ax, word ptr [esi + 0x88]
0041b1fb  e8256e0200               call     0x442025
0041b200  8d4c2408                 lea      ecx, [esp + 8]
0041b204  8d5c2410                 lea      ebx, [esp + 0x10]
0041b208  8d54240c                 lea      edx, [esp + 0xc]
0041b20c  25ff000000               and      eax, 0xff
0041b211  e8bc5e0200               call     0x4410d2
0041b216  8b4c240c                 mov      ecx, dword ptr [esp + 0xc]
0041b21a  66d1e9                   shr      cx, 1
0041b21d  31c0                     xor      eax, eax
0041b21f  894c240c                 mov      dword ptr [esp + 0xc], ecx
0041b223  6689c8                   mov      ax, cx
0041b226  0faf868c000000           imul     eax, dword ptr [esi + 0x8c]
0041b22d  bb10270000               mov      ebx, 0x2710
0041b232  31d2                     xor      edx, edx
0041b234  f7f3                     div      ebx
0041b236  31d2                     xor      edx, edx
0041b238  8a5604                   mov      dl, byte ptr [esi + 4]
0041b23b  663b04555cfb4d00         cmp      ax, word ptr [edx*2 + 0x4dfb5c]
0041b243  0f86d6000000             jbe      0x41b31f
0041b249  b801000000               mov      eax, 1
0041b24e  52                       push     edx
0041b24f  31c9                     xor      ecx, ecx
0041b251  31db                     xor      ebx, ebx
0041b253  31d2                     xor      edx, edx
0041b255  e88bc40400               call     0x4676e5
0041b25a  84c0                     test     al, al
0041b25c  0f84b1000000             je       0x41b313
0041b262  66837c240c00             cmp      word ptr [esp + 0xc], 0
0041b268  0f86b1000000             jbe      0x41b31f
0041b26e  8a4604                   mov      al, byte ptr [esi + 4]
0041b271  31c9                     xor      ecx, ecx
0041b273  88c1                     mov      cl, al
0041b275  ba01000000               mov      edx, 1
0041b27a  89cb                     mov      ebx, ecx
0041b27c  89cf                     mov      edi, ecx
0041b27e  89d0                     mov      eax, edx
0041b280  c1e702                   shl      edi, 2
0041b283  e8a4c60400               call     0x46792c
0041b288  29cf                     sub      edi, ecx
0041b28a  89c8                     mov      eax, ecx
0041b28c  01ff                     add      edi, edi
0041b28e  31c8                     xor      eax, ecx
0041b290  668b872cfb4d00           mov      ax, word ptr [edi + 0x4dfb2c]
0041b297  85c0                     test     eax, eax
0041b299  7e4e                     jle      0x41b2e9
0041b29b  8d5c2404                 lea      ebx, [esp + 4]
0041b29f  8d542418                 lea      edx, [esp + 0x18]
0041b2a3  51                       push     ecx
0041b2a4  8d442418                 lea      eax, [esp + 0x18]
0041b2a8  8d4c2404                 lea      ecx, [esp + 4]
0041b2ac  e8ecc30400               call     0x46769d
0041b2b1  8b442414                 mov      eax, dword ptr [esp + 0x14]
0041b2b5  8b542418                 mov      edx, dword ptr [esp + 0x18]
0041b2b9  668b9f2cfb4d00           mov      bx, word ptr [edi + 0x4dfb2c]
0041b2c0  01d0                     add      eax, edx
0041b2c2  31d2                     xor      edx, edx
0041b2c4  66f7f3                   div      bx
0041b2c7  31d2                     xor      edx, edx
0041b2c9  6689c2                   mov      dx, ax
0041b2cc  89d0                     mov      eax, edx
0041b2ce  c1e003                   shl      eax, 3
0041b2d1  29d0                     sub      eax, edx
0041b2d3  31db                     xor      ebx, ebx
0041b2d5  89c2                     mov      edx, eax
0041b2d7  668b9f2efb4d00           mov      bx, word ptr [edi + 0x4dfb2e]
0041b2de  c1fa1f                   sar      edx, 0x1f
0041b2e1  f7fb                     idiv     ebx
0041b2e3  888730fb4d00             mov      byte ptr [edi + 0x4dfb30], al
0041b2e9  31c0                     xor      eax, eax
0041b2eb  8b9e8c000000             mov      ebx, dword ptr [esi + 0x8c]
0041b2f1  668b44240c               mov      ax, word ptr [esp + 0xc]
0041b2f6  0fafc3                   imul     eax, ebx
0041b2f9  31d2                     xor      edx, edx
0041b2fb  bb10270000               mov      ebx, 0x2710
0041b300  f7f3                     div      ebx
0041b302  89c2                     mov      edx, eax
0041b304  31c0                     xor      eax, eax
0041b306  8a4604                   mov      al, byte ptr [esi + 4]
0041b309  668914455cfb4d00         mov      word ptr [eax*2 + 0x4dfb5c], dx
0041b311  eb0c                     jmp      0x41b31f
0041b313  31c0                     xor      eax, eax
0041b315  8a4604                   mov      al, byte ptr [esi + 4]
0041b318  c68054fb4d0001           mov      byte ptr [eax + 0x4dfb54], 1
0041b31f  83c41c                   add      esp, 0x1c
0041b322  e9f7270000               jmp      0x41db1e
