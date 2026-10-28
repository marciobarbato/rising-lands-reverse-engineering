; EvalueCoutProposition: limite por próximo símbolo SBL, fim exclusivo 0x00466dd1.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00466bac  53                       push     ebx
00466bad  51                       push     ecx
00466bae  52                       push     edx
00466baf  56                       push     esi
00466bb0  57                       push     edi
00466bb1  55                       push     ebp
00466bb2  88c2                     mov      dl, al
00466bb4  31db                     xor      ebx, ebx
00466bb6  31c9                     xor      ecx, ecx
00466bb8  30f6                     xor      dh, dh
00466bba  eb02                     jmp      0x466bbe
00466bbc  fec6                     inc      dh
00466bbe  31c0                     xor      eax, eax
00466bc0  88f0                     mov      al, dh
00466bc2  83f81a                   cmp      eax, 0x1a
00466bc5  7d2a                     jge      0x466bf1
00466bc7  0fb6f2                   movzx    esi, dl
00466bca  6bfe34                   imul     edi, esi, 0x34
00466bcd  89c6                     mov      esi, eax
00466bcf  668bb477bc294e00         mov      si, word ptr [edi + esi*2 + 0x4e29bc]
00466bd7  81e6ffff0000             and      esi, 0xffff
00466bdd  74dd                     je       0x466bbc
00466bdf  8a80b06f4900             mov      al, byte ptr [eax + 0x496fb0]
00466be5  25ff000000               and      eax, 0xff
00466bea  0fafc6                   imul     eax, esi
00466bed  01c3                     add      ebx, eax
00466bef  ebcb                     jmp      0x466bbc
00466bf1  30f6                     xor      dh, dh
00466bf3  eb02                     jmp      0x466bf7
00466bf5  fec6                     inc      dh
00466bf7  31c0                     xor      eax, eax
00466bf9  88f0                     mov      al, dh
00466bfb  83f803                   cmp      eax, 3
00466bfe  7d2a                     jge      0x466c2a
00466c00  0fb6f2                   movzx    esi, dl
00466c03  6bf606                   imul     esi, esi, 6
00466c06  89c7                     mov      edi, eax
00466c08  668bb47efc2c4e00         mov      si, word ptr [esi + edi*2 + 0x4e2cfc]
00466c10  81e6ffff0000             and      esi, 0xffff
00466c16  74dd                     je       0x466bf5
00466c18  8a80cc6f4900             mov      al, byte ptr [eax + 0x496fcc]
00466c1e  25ff000000               and      eax, 0xff
00466c23  0faff0                   imul     esi, eax
00466c26  01f3                     add      ebx, esi
00466c28  ebcb                     jmp      0x466bf5
00466c2a  30f6                     xor      dh, dh
00466c2c  eb02                     jmp      0x466c30
00466c2e  fec6                     inc      dh
00466c30  31c0                     xor      eax, eax
00466c32  88f0                     mov      al, dh
00466c34  83f81a                   cmp      eax, 0x1a
00466c37  7d2a                     jge      0x466c63
00466c39  0fb6f2                   movzx    esi, dl
00466c3c  6bf634                   imul     esi, esi, 0x34
00466c3f  89c7                     mov      edi, eax
00466c41  668bb47e8c2a4e00         mov      si, word ptr [esi + edi*2 + 0x4e2a8c]
00466c49  81e6ffff0000             and      esi, 0xffff
00466c4f  74dd                     je       0x466c2e
00466c51  8a80b06f4900             mov      al, byte ptr [eax + 0x496fb0]
00466c57  25ff000000               and      eax, 0xff
00466c5c  0fafc6                   imul     eax, esi
00466c5f  01c1                     add      ecx, eax
00466c61  ebcb                     jmp      0x466c2e
00466c63  30f6                     xor      dh, dh
00466c65  eb02                     jmp      0x466c69
00466c67  fec6                     inc      dh
00466c69  31c0                     xor      eax, eax
00466c6b  88f0                     mov      al, dh
00466c6d  83f803                   cmp      eax, 3
00466c70  7d2a                     jge      0x466c9c
00466c72  0fb6f2                   movzx    esi, dl
00466c75  6bfe06                   imul     edi, esi, 6
00466c78  89c6                     mov      esi, eax
00466c7a  668bb477142d4e00         mov      si, word ptr [edi + esi*2 + 0x4e2d14]
00466c82  81e6ffff0000             and      esi, 0xffff
00466c88  74dd                     je       0x466c67
00466c8a  8a80cc6f4900             mov      al, byte ptr [eax + 0x496fcc]
00466c90  25ff000000               and      eax, 0xff
00466c95  0fafc6                   imul     eax, esi
00466c98  01c1                     add      ecx, eax
00466c9a  ebcb                     jmp      0x466c67
00466c9c  0fb6f2                   movzx    esi, dl
00466c9f  89f0                     mov      eax, esi
00466ca1  e8716b0000               call     0x46d817
00466ca6  25ff000000               and      eax, 0xff
00466cab  8d3c36                   lea      edi, [esi + esi]
00466cae  83f802                   cmp      eax, 2
00466cb1  0f8492000000             je       0x466d49
00466cb7  31c0                     xor      eax, eax
00466cb9  89f2                     mov      edx, esi
00466cbb  8a868c6f4900             mov      al, byte ptr [esi + 0x496f8c]
00466cc1  e8a66f0000               call     0x46dc6c
00466cc6  0fbfe8                   movsx    ebp, ax
00466cc9  31c0                     xor      eax, eax
00466ccb  89f2                     mov      edx, esi
00466ccd  8a868c6f4900             mov      al, byte ptr [esi + 0x496f8c]
00466cd3  e8606b0000               call     0x46d838
00466cd8  31d2                     xor      edx, edx
00466cda  88c2                     mov      dl, al
00466cdc  89d0                     mov      eax, edx
00466cde  c1e002                   shl      eax, 2
00466ce1  01d0                     add      eax, edx
00466ce3  c1e003                   shl      eax, 3
00466ce6  83c564                   add      ebp, 0x64
00466ce9  83e814                   sub      eax, 0x14
00466cec  89da                     mov      edx, ebx
00466cee  01c5                     add      ebp, eax
00466cf0  0fafd5                   imul     edx, ebp
00466cf3  bb64000000               mov      ebx, 0x64
00466cf8  89d0                     mov      eax, edx
00466cfa  c1fa1f                   sar      edx, 0x1f
00466cfd  f7fb                     idiv     ebx
00466cff  89c3                     mov      ebx, eax
00466d01  85c9                     test     ecx, ecx
00466d03  741e                     je       0x466d23
00466d05  c1e002                   shl      eax, 2
00466d08  29d8                     sub      eax, ebx
00466d0a  c1e003                   shl      eax, 3
00466d0d  8d1403                   lea      edx, [ebx + eax]
00466d10  c1e202                   shl      edx, 2
00466d13  89d0                     mov      eax, edx
00466d15  c1fa1f                   sar      edx, 0x1f
00466d18  f7f9                     idiv     ecx
00466d1a  66898730294e00           mov      word ptr [edi + 0x4e2930], ax
00466d21  eb18                     jmp      0x466d3b
00466d23  85c0                     test     eax, eax
00466d25  740b                     je       0x466d32
00466d27  66c78730294e00c800       mov      word ptr [edi + 0x4e2930], 0xc8
00466d30  eb09                     jmp      0x466d3b
00466d32  31f6                     xor      esi, esi
00466d34  6689b730294e00           mov      word ptr [edi + 0x4e2930], si
00466d3b  29cb                     sub      ebx, ecx
00466d3d  66891d48294e00           mov      word ptr [0x4e2948], bx
00466d44  e98af4ffff               jmp      0x4661d3
00466d49  31d2                     xor      edx, edx
00466d4b  89f0                     mov      eax, esi
00466d4d  8a968c6f4900             mov      dl, byte ptr [esi + 0x496f8c]
00466d53  e8146f0000               call     0x46dc6c
00466d58  0fbfe8                   movsx    ebp, ax
00466d5b  31c0                     xor      eax, eax
00466d5d  89f2                     mov      edx, esi
00466d5f  8a868c6f4900             mov      al, byte ptr [esi + 0x496f8c]
00466d65  e8ce6a0000               call     0x46d838
00466d6a  31d2                     xor      edx, edx
00466d6c  88c2                     mov      dl, al
00466d6e  89d0                     mov      eax, edx
00466d70  c1e002                   shl      eax, 2
00466d73  01d0                     add      eax, edx
00466d75  89ca                     mov      edx, ecx
00466d77  c1e202                   shl      edx, 2
00466d7a  29ca                     sub      edx, ecx
00466d7c  83c564                   add      ebp, 0x64
00466d7f  c1e203                   shl      edx, 3
00466d82  c1e003                   shl      eax, 3
00466d85  01ca                     add      edx, ecx
00466d87  83e814                   sub      eax, 0x14
00466d8a  c1e202                   shl      edx, 2
00466d8d  01c5                     add      ebp, eax
00466d8f  89d0                     mov      eax, edx
00466d91  c1fa1f                   sar      edx, 0x1f
00466d94  f7fd                     idiv     ebp
00466d96  89c1                     mov      ecx, eax
00466d98  85db                     test     ebx, ebx
00466d9a  741e                     je       0x466dba
00466d9c  c1e002                   shl      eax, 2
00466d9f  29c8                     sub      eax, ecx
00466da1  c1e003                   shl      eax, 3
00466da4  8d1401                   lea      edx, [ecx + eax]
00466da7  c1e202                   shl      edx, 2
00466daa  89d0                     mov      eax, edx
00466dac  c1fa1f                   sar      edx, 0x1f
00466daf  f7fb                     idiv     ebx
00466db1  66898730294e00           mov      word ptr [edi + 0x4e2930], ax
00466db8  eb09                     jmp      0x466dc3
00466dba  66c78730294e006400       mov      word ptr [edi + 0x4e2930], 0x64
00466dc3  29d9                     sub      ecx, ebx
00466dc5  66890d48294e00           mov      word ptr [0x4e2948], cx
00466dcc  e902f4ffff               jmp      0x4661d3
