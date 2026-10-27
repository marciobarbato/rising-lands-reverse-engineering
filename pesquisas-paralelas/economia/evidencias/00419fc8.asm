; BatimentRecalculRessource: limite por próximo símbolo SBL, fim exclusivo 0x0041a05c.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00419fc8  53                       push     ebx
00419fc9  51                       push     ecx
00419fca  56                       push     esi
00419fcb  57                       push     edi
00419fcc  83ec14                   sub      esp, 0x14
00419fcf  88442410                 mov      byte ptr [esp + 0x10], al
00419fd3  8d4c240c                 lea      ecx, [esp + 0xc]
00419fd7  0fb6f0                   movzx    esi, al
00419fda  8d5c2408                 lea      ebx, [esp + 8]
00419fde  56                       push     esi
00419fdf  8d542404                 lea      edx, [esp + 4]
00419fe3  8d442408                 lea      eax, [esp + 8]
00419fe7  e8b1d60400               call     0x46769d
00419fec  8b442404                 mov      eax, dword ptr [esp + 4]
00419ff0  030424                   add      eax, dword ptr [esp]
00419ff3  89f2                     mov      edx, esi
00419ff5  c1e202                   shl      edx, 2
00419ff8  29f2                     sub      edx, esi
00419ffa  668b1c552efb4d00         mov      bx, word ptr [edx*2 + 0x4dfb2e]
0041a002  660faf1c552cfb4d00       imul     bx, word ptr [edx*2 + 0x4dfb2c]
0041a00b  6639d8                   cmp      ax, bx
0041a00e  7604                     jbe      0x41a014
0041a010  89df                     mov      edi, ebx
0041a012  29c7                     sub      edi, eax
0041a014  31db                     xor      ebx, ebx
0041a016  8a5c2410                 mov      bl, byte ptr [esp + 0x10]
0041a01a  89da                     mov      edx, ebx
0041a01c  c1e202                   shl      edx, 2
0041a01f  29da                     sub      edx, ebx
0041a021  8d1c12                   lea      ebx, [edx + edx]
0041a024  01f8                     add      eax, edi
0041a026  668bb32cfb4d00           mov      si, word ptr [ebx + 0x4dfb2c]
0041a02d  31d2                     xor      edx, edx
0041a02f  66f7f6                   div      si
0041a032  31c9                     xor      ecx, ecx
0041a034  668b8b2efb4d00           mov      cx, word ptr [ebx + 0x4dfb2e]
0041a03b  25ffff0000               and      eax, 0xffff
0041a040  89c2                     mov      edx, eax
0041a042  c1e203                   shl      edx, 3
0041a045  29c2                     sub      edx, eax
0041a047  89d0                     mov      eax, edx
0041a049  c1fa1f                   sar      edx, 0x1f
0041a04c  f7f9                     idiv     ecx
0041a04e  888330fb4d00             mov      byte ptr [ebx + 0x4dfb30], al
0041a054  83c414                   add      esp, 0x14
0041a057  5f                       pop      edi
0041a058  5e                       pop      esi
0041a059  59                       pop      ecx
0041a05a  5b                       pop      ebx
0041a05b  c3                       ret
