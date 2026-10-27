; InfligeDegat; intervalo [0x00450874, 0x004510dd)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00450874  56                       push     esi
00450875  57                       push     edi
00450876  55                       push     ebp
00450877  83ec24                   sub      esp, 0x24
0045087a  50                       push     eax
0045087b  88542418                 mov      byte ptr [esp + 0x18], dl
0045087f  89de                     mov      esi, ebx
00450881  884c240c                 mov      byte ptr [esp + 0xc], cl
00450885  807c243800               cmp      byte ptr [esp + 0x38], 0
0045088a  750f                     jne      0x45089b
0045088c  31c0                     xor      eax, eax
0045088e  668b0424                 mov      ax, word ptr [esp]
00450892  e8b3acfcff               call     0x41b54a
00450897  89c7                     mov      edi, eax
00450899  eb05                     jmp      0x4508a0
0045089b  bfffff0000               mov      edi, 0xffff
004508a0  0fb7ef                   movzx    ebp, di
004508a3  81fdffff0000             cmp      ebp, 0xffff
004508a9  0f84ee010000             je       0x450a9d
004508af  31c0                     xor      eax, eax
004508b1  8a442418                 mov      al, byte ptr [esp + 0x18]
004508b5  b902000000               mov      ecx, 2
004508ba  83f801                   cmp      eax, 1
004508bd  7566                     jne      0x450925
004508bf  31c0                     xor      eax, eax
004508c1  6689f0                   mov      ax, si
004508c4  89442404                 mov      dword ptr [esp + 4], eax
004508c8  89c2                     mov      edx, eax
004508ca  c1e004                   shl      eax, 4
004508cd  01d0                     add      eax, edx
004508cf  c1e002                   shl      eax, 2
004508d2  01d0                     add      eax, edx
004508d4  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
004508da  c1e002                   shl      eax, 2
004508dd  01c6                     add      esi, eax
004508df  31db                     xor      ebx, ebx
004508e1  8a4601                   mov      al, byte ptr [esi + 1]
004508e4  88c3                     mov      bl, al
004508e6  8b159c194e00             mov      edx, dword ptr [0x4e199c]
004508ec  89d8                     mov      eax, ebx
004508ee  8b0482                   mov      eax, dword ptr [edx + eax*4]
004508f1  83c01a                   add      eax, 0x1a
004508f4  30ed                     xor      ch, ch
004508f6  8a00                     mov      al, byte ptr [eax]
004508f8  88c1                     mov      cl, al
004508fa  31c0                     xor      eax, eax
004508fc  ba05000000               mov      edx, 5
00450901  8a06                     mov      al, byte ptr [esi]
00450903  e8b883fdff               call     0x428cc0
00450908  8b5c2404                 mov      ebx, dword ptr [esp + 4]
0045090c  01c1                     add      ecx, eax
0045090e  8a06                     mov      al, byte ptr [esi]
00450910  ba04000000               mov      edx, 4
00450915  88442414                 mov      byte ptr [esp + 0x14], al
00450919  89e8                     mov      eax, ebp
0045091b  e8e83e0300               call     0x484808
00450920  e98d000000               jmp      0x4509b2
00450925  83f803                   cmp      eax, 3
00450928  7536                     jne      0x450960
0045092a  89e8                     mov      eax, ebp
0045092c  31db                     xor      ebx, ebx
0045092e  e8c19bfcff               call     0x41a4f4
00450933  88c3                     mov      bl, al
00450935  81e6ffff0000             and      esi, 0xffff
0045093b  89f0                     mov      eax, esi
0045093d  e8b29bfcff               call     0x41a4f4
00450942  ba03000000               mov      edx, 3
00450947  25ff000000               and      eax, 0xff
0045094c  e83982fcff               call     0x418b8a
00450951  89c1                     mov      ecx, eax
00450953  89f0                     mov      eax, esi
00450955  e83297fcff               call     0x41a08c
0045095a  88442414                 mov      byte ptr [esp + 0x14], al
0045095e  eb52                     jmp      0x4509b2
00450960  83f804                   cmp      eax, 4
00450963  754d                     jne      0x4509b2
00450965  31d2                     xor      edx, edx
00450967  6689f2                   mov      dx, si
0045096a  89d0                     mov      eax, edx
0045096c  c1e004                   shl      eax, 4
0045096f  01d0                     add      eax, edx
00450971  c1e002                   shl      eax, 2
00450974  01d0                     add      eax, edx
00450976  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0045097c  8a0482                   mov      al, byte ptr [edx + eax*4]
0045097f  88442414                 mov      byte ptr [esp + 0x14], al
00450983  31c0                     xor      eax, eax
00450985  8a44240c                 mov      al, byte ptr [esp + 0xc]
00450989  83f81d                   cmp      eax, 0x1d
0045098c  750b                     jne      0x450999
0045098e  31d2                     xor      edx, edx
00450990  668b156c714900           mov      dx, word ptr [0x49716c]
00450997  eb0e                     jmp      0x4509a7
00450999  83f81e                   cmp      eax, 0x1e
0045099c  7514                     jne      0x4509b2
0045099e  31d2                     xor      edx, edx
004509a0  668b156e714900           mov      dx, word ptr [0x49716e]
004509a7  89d0                     mov      eax, edx
004509a9  c1fa1f                   sar      edx, 0x1f
004509ac  2bc2                     sub      eax, edx
004509ae  d1f8                     sar      eax, 1
004509b0  89c1                     mov      ecx, eax
004509b2  31db                     xor      ebx, ebx
004509b4  31d2                     xor      edx, edx
004509b6  31c0                     xor      eax, eax
004509b8  8a5c2414                 mov      bl, byte ptr [esp + 0x14]
004509bc  6689ca                   mov      dx, cx
004509bf  6689f8                   mov      ax, di
004509c2  e8fa98fcff               call     0x41a2c1
004509c7  b821000000               mov      eax, 0x21
004509cc  e80bfb0100               call     0x4704dc
004509d1  a801                     test     al, 1
004509d3  7511                     jne      0x4509e6
004509d5  6a00                     push     0
004509d7  6a00                     push     0
004509d9  6a00                     push     0
004509db  31d2                     xor      edx, edx
004509dd  6a00                     push     0
004509df  b80f000000               mov      eax, 0xf
004509e4  eb0f                     jmp      0x4509f5
004509e6  6a00                     push     0
004509e8  6a00                     push     0
004509ea  6a00                     push     0
004509ec  31d2                     xor      edx, edx
004509ee  6a00                     push     0
004509f0  b810000000               mov      eax, 0x10
004509f5  668b542410               mov      dx, word ptr [esp + 0x10]
004509fa  6a00                     push     0
004509fc  31c9                     xor      ecx, ecx
004509fe  89d3                     mov      ebx, edx
00450a00  e847da0100               call     0x46e44c
00450a05  31c9                     xor      ecx, ecx
00450a07  6689f9                   mov      cx, di
00450a0a  0fb6742414               movzx    esi, byte ptr [esp + 0x14]
00450a0f  89c8                     mov      eax, ecx
00450a11  31d2                     xor      edx, edx
00450a13  e87496fcff               call     0x41a08c
00450a18  88c2                     mov      dl, al
00450a1a  89f0                     mov      eax, esi
00450a1c  e817ce0100               call     0x46d838
00450a21  84c0                     test     al, al
00450a23  745a                     je       0x450a7f
00450a25  89c8                     mov      eax, ecx
00450a27  0fb66c2414               movzx    ebp, byte ptr [esp + 0x14]
00450a2c  e85b96fcff               call     0x41a08c
00450a31  bb0a000000               mov      ebx, 0xa
00450a36  25ff000000               and      eax, 0xff
00450a3b  89ea                     mov      edx, ebp
00450a3d  e8d6460200               call     0x475118
00450a42  89c8                     mov      eax, ecx
00450a44  e84396fcff               call     0x41a08c
00450a49  bb06000000               mov      ebx, 6
00450a4e  25ff000000               and      eax, 0xff
00450a53  89ea                     mov      edx, ebp
00450a55  e8be460200               call     0x475118
00450a5a  89c8                     mov      eax, ecx
00450a5c  31d2                     xor      edx, edx
00450a5e  e82996fcff               call     0x41a08c
00450a63  88c2                     mov      dl, al
00450a65  89f0                     mov      eax, esi
00450a67  e85fce0100               call     0x46d8cb
00450a6c  89c8                     mov      eax, ecx
00450a6e  e81996fcff               call     0x41a08c
00450a73  25ff000000               and      eax, 0xff
00450a78  89f2                     mov      edx, esi
00450a7a  e84cce0100               call     0x46d8cb
00450a7f  31c0                     xor      eax, eax
00450a81  6689f8                   mov      ax, di
00450a84  31d2                     xor      edx, edx
00450a86  e80196fcff               call     0x41a08c
00450a8b  88c2                     mov      dl, al
00450a8d  31c0                     xor      eax, eax
00450a8f  8a442414                 mov      al, byte ptr [esp + 0x14]
00450a93  e868cb0100               call     0x46d600
00450a98  e938060000               jmp      0x4510d5
00450a9d  89ea                     mov      edx, ebp
00450a9f  31db                     xor      ebx, ebx
00450aa1  31c0                     xor      eax, eax
00450aa3  8a5c2438                 mov      bl, byte ptr [esp + 0x38]
00450aa7  668b0424                 mov      ax, word ptr [esp]
00450aab  e82f5bffff               call     0x4465df
00450ab0  31d2                     xor      edx, edx
00450ab2  6689c2                   mov      dx, ax
00450ab5  89c7                     mov      edi, eax
00450ab7  39ea                     cmp      edx, ebp
00450ab9  0f8416060000             je       0x4510d5
00450abf  89d0                     mov      eax, edx
00450ac1  c1e004                   shl      eax, 4
00450ac4  01d0                     add      eax, edx
00450ac6  c1e002                   shl      eax, 2
00450ac9  01d0                     add      eax, edx
00450acb  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00450ad1  c1e002                   shl      eax, 2
00450ad4  01c1                     add      ecx, eax
00450ad6  8a4101                   mov      al, byte ptr [ecx + 1]
00450ad9  8844241c                 mov      byte ptr [esp + 0x1c], al
00450add  8a01                     mov      al, byte ptr [ecx]
00450adf  89cb                     mov      ebx, ecx
00450ae1  88442420                 mov      byte ptr [esp + 0x20], al
00450ae5  25ff000000               and      eax, 0xff
00450aea  3dc8000000               cmp      eax, 0xc8
00450aef  7456                     je       0x450b47
00450af1  e821cd0100               call     0x46d817
00450af6  25ff000000               and      eax, 0xff
00450afb  83f801                   cmp      eax, 1
00450afe  7547                     jne      0x450b47
00450b00  31c0                     xor      eax, eax
00450b02  8a4102                   mov      al, byte ptr [ecx + 2]
00450b05  83f805                   cmp      eax, 5
00450b08  7405                     je       0x450b0f
00450b0a  83f812                   cmp      eax, 0x12
00450b0d  7538                     jne      0x450b47
00450b0f  31d2                     xor      edx, edx
00450b11  31c0                     xor      eax, eax
00450b13  8a13                     mov      dl, byte ptr [ebx]
00450b15  668b4308                 mov      ax, word ptr [ebx + 8]
00450b19  e8d52e0000               call     0x4539f3
00450b1e  25ffff0000               and      eax, 0xffff
00450b23  3dffff0000               cmp      eax, 0xffff
00450b28  0f845c020000             je       0x450d8a
00450b2e  31d2                     xor      edx, edx
00450b30  e8ada3fcff               call     0x41aee2
00450b35  6689c2                   mov      dx, ax
00450b38  31c0                     xor      eax, eax
00450b3a  6689f8                   mov      ax, di
00450b3d  e8914cffff               call     0x4457d3
00450b42  e943020000               jmp      0x450d8a
00450b47  31c0                     xor      eax, eax
00450b49  8a442420                 mov      al, byte ptr [esp + 0x20]
00450b4d  3dc8000000               cmp      eax, 0xc8
00450b52  7505                     jne      0x450b59
00450b54  e931020000               jmp      0x450d8a
00450b59  8a54241c                 mov      dl, byte ptr [esp + 0x1c]
00450b5d  80fa0f                   cmp      dl, 0xf
00450b60  7226                     jb       0x450b88
00450b62  7620                     jbe      0x450b84
00450b64  80fa14                   cmp      dl, 0x14
00450b67  7211                     jb       0x450b7a
00450b69  80fa16                   cmp      dl, 0x16
00450b6c  7616                     jbe      0x450b84
00450b6e  80fa18                   cmp      dl, 0x18
00450b71  7611                     jbe      0x450b84
00450b73  80fa19                   cmp      dl, 0x19
00450b76  740c                     je       0x450b84
00450b78  eb26                     jmp      0x450ba0
00450b7a  80fa10                   cmp      dl, 0x10
00450b7d  7605                     jbe      0x450b84
00450b7f  80fa12                   cmp      dl, 0x12
00450b82  721c                     jb       0x450ba0
00450b84  b001                     mov      al, 1
00450b86  eb1a                     jmp      0x450ba2
00450b88  80fa03                   cmp      dl, 3
00450b8b  72f7                     jb       0x450b84
00450b8d  76f5                     jbe      0x450b84
00450b8f  80fa08                   cmp      dl, 8
00450b92  720c                     jb       0x450ba0
00450b94  76ee                     jbe      0x450b84
00450b96  80fa0b                   cmp      dl, 0xb
00450b99  7205                     jb       0x450ba0
00450b9b  80fa0c                   cmp      dl, 0xc
00450b9e  76e4                     jbe      0x450b84
00450ba0  30c0                     xor      al, al
00450ba2  84c0                     test     al, al
00450ba4  0f843a010000             je       0x450ce4
00450baa  31d2                     xor      edx, edx
00450bac  6689fa                   mov      dx, di
00450baf  89d0                     mov      eax, edx
00450bb1  c1e004                   shl      eax, 4
00450bb4  01d0                     add      eax, edx
00450bb6  c1e002                   shl      eax, 2
00450bb9  01c2                     add      edx, eax
00450bbb  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450bc0  c1e202                   shl      edx, 2
00450bc3  8a8402dc000000           mov      al, byte ptr [edx + eax + 0xdc]
00450bca  ba01000000               mov      edx, 1
00450bcf  25ff000000               and      eax, 0xff
00450bd4  e8be710100               call     0x467d97
00450bd9  84c0                     test     al, al
00450bdb  0f8503010000             jne      0x450ce4
00450be1  31c0                     xor      eax, eax
00450be3  8a442418                 mov      al, byte ptr [esp + 0x18]
00450be7  83f801                   cmp      eax, 1
00450bea  0f85f4000000             jne      0x450ce4
00450bf0  31d2                     xor      edx, edx
00450bf2  6689f2                   mov      dx, si
00450bf5  89d0                     mov      eax, edx
00450bf7  c1e004                   shl      eax, 4
00450bfa  01d0                     add      eax, edx
00450bfc  c1e002                   shl      eax, 2
00450bff  01d0                     add      eax, edx
00450c01  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450c07  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
00450c0b  25ff000000               and      eax, 0xff
00450c10  83f811                   cmp      eax, 0x11
00450c13  7405                     je       0x450c1a
00450c15  83f80a                   cmp      eax, 0xa
00450c18  7504                     jne      0x450c1e
00450c1a  30c0                     xor      al, al
00450c1c  eb17                     jmp      0x450c35
00450c1e  83f810                   cmp      eax, 0x10
00450c21  7510                     jne      0x450c33
00450c23  8a4c241c                 mov      cl, byte ptr [esp + 0x1c]
00450c27  80f902                   cmp      cl, 2
00450c2a  72ee                     jb       0x450c1a
00450c2c  7605                     jbe      0x450c33
00450c2e  80f908                   cmp      cl, 8
00450c31  75e7                     jne      0x450c1a
00450c33  b001                     mov      al, 1
00450c35  84c0                     test     al, al
00450c37  0f84a7000000             je       0x450ce4
00450c3d  31c9                     xor      ecx, ecx
00450c3f  6689f1                   mov      cx, si
00450c42  89c8                     mov      eax, ecx
00450c44  c1e004                   shl      eax, 4
00450c47  01c8                     add      eax, ecx
00450c49  c1e002                   shl      eax, 2
00450c4c  8d1401                   lea      edx, [ecx + eax]
00450c4f  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450c54  c1e202                   shl      edx, 2
00450c57  8a0402                   mov      al, byte ptr [edx + eax]
00450c5a  8a642420                 mov      ah, byte ptr [esp + 0x20]
00450c5e  38e0                     cmp      al, ah
00450c60  0f847e000000             je       0x450ce4
00450c66  31d2                     xor      edx, edx
00450c68  88e2                     mov      dl, ah
00450c6a  89d0                     mov      eax, edx
00450c6c  e8a6cb0100               call     0x46d817
00450c71  25ff000000               and      eax, 0xff
00450c76  83f801                   cmp      eax, 1
00450c79  753a                     jne      0x450cb5
00450c7b  31c0                     xor      eax, eax
00450c7d  8a4302                   mov      al, byte ptr [ebx + 2]
00450c80  83f807                   cmp      eax, 7
00450c83  7416                     je       0x450c9b
00450c85  a17c8f5000               mov      eax, dword ptr [0x508f7c]
00450c8a  2b8310010000             sub      eax, dword ptr [ebx + 0x110]
00450c90  3dfa000000               cmp      eax, 0xfa
00450c95  0f86ef000000             jbe      0x450d8a
00450c9b  31db                     xor      ebx, ebx
00450c9d  31d2                     xor      edx, edx
00450c9f  31c0                     xor      eax, eax
00450ca1  8a542418                 mov      dl, byte ptr [esp + 0x18]
00450ca5  6689f3                   mov      bx, si
00450ca8  6689f8                   mov      ax, di
00450cab  e8864dffff               call     0x445a36
00450cb0  e9d5000000               jmp      0x450d8a
00450cb5  89d0                     mov      eax, edx
00450cb7  e85bcb0100               call     0x46d817
00450cbc  25ff000000               and      eax, 0xff
00450cc1  83f802                   cmp      eax, 2
00450cc4  0f85c0000000             jne      0x450d8a
00450cca  31c0                     xor      eax, eax
00450ccc  8a4302                   mov      al, byte ptr [ebx + 2]
00450ccf  83f807                   cmp      eax, 7
00450cd2  0f85b2000000             jne      0x450d8a
00450cd8  89cb                     mov      ebx, ecx
00450cda  31d2                     xor      edx, edx
00450cdc  31c0                     xor      eax, eax
00450cde  8a542418                 mov      dl, byte ptr [esp + 0x18]
00450ce2  ebc4                     jmp      0x450ca8
00450ce4  31c0                     xor      eax, eax
00450ce6  8a442418                 mov      al, byte ptr [esp + 0x18]
00450cea  83f803                   cmp      eax, 3
00450ced  7510                     jne      0x450cff
00450cef  31c0                     xor      eax, eax
00450cf1  6689f0                   mov      ax, si
00450cf4  e8e9a1fcff               call     0x41aee2
00450cf9  89442408                 mov      dword ptr [esp + 8], eax
00450cfd  eb2e                     jmp      0x450d2d
00450cff  83f801                   cmp      eax, 1
00450d02  751e                     jne      0x450d22
00450d04  31d2                     xor      edx, edx
00450d06  6689f2                   mov      dx, si
00450d09  89d0                     mov      eax, edx
00450d0b  c1e004                   shl      eax, 4
00450d0e  01d0                     add      eax, edx
00450d10  c1e002                   shl      eax, 2
00450d13  01d0                     add      eax, edx
00450d15  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450d1b  668b44827c               mov      ax, word ptr [edx + eax*4 + 0x7c]
00450d20  ebd7                     jmp      0x450cf9
00450d22  83f804                   cmp      eax, 4
00450d25  7506                     jne      0x450d2d
00450d27  31d2                     xor      edx, edx
00450d29  89542408                 mov      dword ptr [esp + 8], edx
00450d2d  31db                     xor      ebx, ebx
00450d2f  6689fb                   mov      bx, di
00450d32  89d9                     mov      ecx, ebx
00450d34  c1e104                   shl      ecx, 4
00450d37  01d9                     add      ecx, ebx
00450d39  c1e102                   shl      ecx, 2
00450d3c  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450d41  01d9                     add      ecx, ebx
00450d43  89da                     mov      edx, ebx
00450d45  c1e102                   shl      ecx, 2
00450d48  31da                     xor      edx, ebx
00450d4a  668b44017c               mov      ax, word ptr [ecx + eax + 0x7c]
00450d4f  6689c2                   mov      dx, ax
00450d52  31c0                     xor      eax, eax
00450d54  668b442408               mov      ax, word ptr [esp + 8]
00450d59  e8e4620200               call     0x477042
00450d5e  31d2                     xor      edx, edx
00450d60  88c2                     mov      dl, al
00450d62  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450d67  668b44017c               mov      ax, word ptr [ecx + eax + 0x7c]
00450d6c  25ffff0000               and      eax, 0xffff
00450d71  e878630200               call     0x4770ee
00450d76  31d2                     xor      edx, edx
00450d78  6689c2                   mov      dx, ax
00450d7b  81faffff0000             cmp      edx, 0xffff
00450d81  7407                     je       0x450d8a
00450d83  89d8                     mov      eax, ebx
00450d85  e9b3fdffff               jmp      0x450b3d
00450d8a  31c9                     xor      ecx, ecx
00450d8c  31db                     xor      ebx, ebx
00450d8e  31d2                     xor      edx, edx
00450d90  31c0                     xor      eax, eax
00450d92  8a4c240c                 mov      cl, byte ptr [esp + 0xc]
00450d96  8a542418                 mov      dl, byte ptr [esp + 0x18]
00450d9a  6689f3                   mov      bx, si
00450d9d  6689f8                   mov      ax, di
00450da0  e84bf5ffff               call     0x4502f0
00450da5  8a54241c                 mov      dl, byte ptr [esp + 0x1c]
00450da9  b001                     mov      al, 1
00450dab  80fa0e                   cmp      dl, 0xe
00450dae  721a                     jb       0x450dca
00450db0  7627                     jbe      0x450dd9
00450db2  80fa12                   cmp      dl, 0x12
00450db5  7222                     jb       0x450dd9
00450db7  762b                     jbe      0x450de4
00450db9  80fa17                   cmp      dl, 0x17
00450dbc  7226                     jb       0x450de4
00450dbe  80fa18                   cmp      dl, 0x18
00450dc1  7621                     jbe      0x450de4
00450dc3  80fa19                   cmp      dl, 0x19
00450dc6  7411                     je       0x450dd9
00450dc8  eb1c                     jmp      0x450de6
00450dca  80fa06                   cmp      dl, 6
00450dcd  720e                     jb       0x450ddd
00450dcf  80fa08                   cmp      dl, 8
00450dd2  7610                     jbe      0x450de4
00450dd4  80fa0b                   cmp      dl, 0xb
00450dd7  720b                     jb       0x450de4
00450dd9  30c0                     xor      al, al
00450ddb  eb09                     jmp      0x450de6
00450ddd  80fa03                   cmp      dl, 3
00450de0  7202                     jb       0x450de4
00450de2  76f5                     jbe      0x450dd9
00450de4  b001                     mov      al, 1
00450de6  84c0                     test     al, al
00450de8  742c                     je       0x450e16
00450dea  6a00                     push     0
00450dec  6a00                     push     0
00450dee  6a00                     push     0
00450df0  31d2                     xor      edx, edx
00450df2  6a00                     push     0
00450df4  b80e000000               mov      eax, 0xe
00450df9  668b542410               mov      dx, word ptr [esp + 0x10]
00450dfe  6a00                     push     0
00450e00  31c9                     xor      ecx, ecx
00450e02  89d3                     mov      ebx, edx
00450e04  e843d60100               call     0x46e44c
00450e09  e9aa020000               jmp      0x4510b8
00450e0e  b001                     mov      al, 1
00450e10  eb1b                     jmp      0x450e2d
00450e12  30c0                     xor      al, al
00450e14  eb17                     jmp      0x450e2d
00450e16  8a44241c                 mov      al, byte ptr [esp + 0x1c]
00450e1a  2c0b                     sub      al, 0xb
00450e1c  3c06                     cmp      al, 6
00450e1e  77f2                     ja       0x450e12
00450e20  25ff000000               and      eax, 0xff
00450e25  2eff248558084500         jmp      dword ptr cs:[eax*4 + 0x450858]
00450e2d  84c0                     test     al, al
00450e2f  0f8483020000             je       0x4510b8
00450e35  31c0                     xor      eax, eax
00450e37  8a44241c                 mov      al, byte ptr [esp + 0x1c]
00450e3b  30d2                     xor      dl, dl
00450e3d  83f810                   cmp      eax, 0x10
00450e40  7502                     jne      0x450e44
00450e42  b201                     mov      dl, 1
00450e44  b822000000               mov      eax, 0x22
00450e49  e88ef60100               call     0x4704dc
00450e4e  a801                     test     al, 1
00450e50  751d                     jne      0x450e6f
00450e52  31c0                     xor      eax, eax
00450e54  88d0                     mov      al, dl
00450e56  50                       push     eax
00450e57  6a00                     push     0
00450e59  6a00                     push     0
00450e5b  31d2                     xor      edx, edx
00450e5d  6a00                     push     0
00450e5f  31c9                     xor      ecx, ecx
00450e61  668b542410               mov      dx, word ptr [esp + 0x10]
00450e66  6a00                     push     0
00450e68  b80f000000               mov      eax, 0xf
00450e6d  eb93                     jmp      0x450e02
00450e6f  31c0                     xor      eax, eax
00450e71  88d0                     mov      al, dl
00450e73  50                       push     eax
00450e74  6a00                     push     0
00450e76  6a00                     push     0
00450e78  31d2                     xor      edx, edx
00450e7a  6a00                     push     0
00450e7c  31c9                     xor      ecx, ecx
00450e7e  668b542410               mov      dx, word ptr [esp + 0x10]
00450e83  6a00                     push     0
00450e85  b810000000               mov      eax, 0x10
00450e8a  e973ffffff               jmp      0x450e02
00450e8f  31d2                     xor      edx, edx
00450e91  31c0                     xor      eax, eax
00450e93  6689fa                   mov      dx, di
00450e96  6689f0                   mov      ax, si
00450e99  89d6                     mov      esi, edx
00450e9b  31c9                     xor      ecx, ecx
00450e9d  c1e604                   shl      esi, 4
00450ea0  e8e791fcff               call     0x41a08c
00450ea5  01d6                     add      esi, edx
00450ea7  88c3                     mov      bl, al
00450ea9  c1e602                   shl      esi, 2
00450eac  88442410                 mov      byte ptr [esp + 0x10], al
00450eb0  01d6                     add      esi, edx
00450eb2  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450eb7  c1e602                   shl      esi, 2
00450eba  31d2                     xor      edx, edx
00450ebc  8a0406                   mov      al, byte ptr [esi + eax]
00450ebf  88d9                     mov      cl, bl
00450ec1  88c2                     mov      dl, al
00450ec3  89c8                     mov      eax, ecx
00450ec5  e86ec90100               call     0x46d838
00450eca  84c0                     test     al, al
00450ecc  745c                     je       0x450f2a
00450ece  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450ed3  0fb6eb                   movzx    ebp, bl
00450ed6  8a0406                   mov      al, byte ptr [esi + eax]
00450ed9  bb0a000000               mov      ebx, 0xa
00450ede  25ff000000               and      eax, 0xff
00450ee3  89ea                     mov      edx, ebp
00450ee5  e82e420200               call     0x475118
00450eea  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450eef  8a0406                   mov      al, byte ptr [esi + eax]
00450ef2  bb06000000               mov      ebx, 6
00450ef7  25ff000000               and      eax, 0xff
00450efc  89ea                     mov      edx, ebp
00450efe  e815420200               call     0x475118
00450f03  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450f08  31d2                     xor      edx, edx
00450f0a  8a0406                   mov      al, byte ptr [esi + eax]
00450f0d  88c2                     mov      dl, al
00450f0f  89c8                     mov      eax, ecx
00450f11  e8b5c90100               call     0x46d8cb
00450f16  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450f1b  8a0406                   mov      al, byte ptr [esi + eax]
00450f1e  25ff000000               and      eax, 0xff
00450f23  89ca                     mov      edx, ecx
00450f25  e8a1c90100               call     0x46d8cb
00450f2a  31d2                     xor      edx, edx
00450f2c  6689fa                   mov      dx, di
00450f2f  89d0                     mov      eax, edx
00450f31  c1e004                   shl      eax, 4
00450f34  01d0                     add      eax, edx
00450f36  c1e002                   shl      eax, 2
00450f39  01d0                     add      eax, edx
00450f3b  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00450f41  8a0482                   mov      al, byte ptr [edx + eax*4]
00450f44  31d2                     xor      edx, edx
00450f46  88c2                     mov      dl, al
00450f48  31c0                     xor      eax, eax
00450f4a  8a442410                 mov      al, byte ptr [esp + 0x10]
00450f4e  e940fbffff               jmp      0x450a93
00450f53  31d2                     xor      edx, edx
00450f55  6689f2                   mov      dx, si
00450f58  89d0                     mov      eax, edx
00450f5a  c1e004                   shl      eax, 4
00450f5d  01d0                     add      eax, edx
00450f5f  c1e002                   shl      eax, 2
00450f62  01d0                     add      eax, edx
00450f64  31d2                     xor      edx, edx
00450f66  6689fa                   mov      dx, di
00450f69  89d6                     mov      esi, edx
00450f6b  c1e604                   shl      esi, 4
00450f6e  01d6                     add      esi, edx
00450f70  c1e602                   shl      esi, 2
00450f73  01d6                     add      esi, edx
00450f75  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00450f7b  c1e602                   shl      esi, 2
00450f7e  8a1c81                   mov      bl, byte ptr [ecx + eax*4]
00450f81  8a0431                   mov      al, byte ptr [ecx + esi]
00450f84  31c9                     xor      ecx, ecx
00450f86  31d2                     xor      edx, edx
00450f88  88d9                     mov      cl, bl
00450f8a  88c2                     mov      dl, al
00450f8c  89c8                     mov      eax, ecx
00450f8e  885c2424                 mov      byte ptr [esp + 0x24], bl
00450f92  e8a1c80100               call     0x46d838
00450f97  84c0                     test     al, al
00450f99  745c                     je       0x450ff7
00450f9b  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450fa0  0fb6eb                   movzx    ebp, bl
00450fa3  8a0406                   mov      al, byte ptr [esi + eax]
00450fa6  bb0a000000               mov      ebx, 0xa
00450fab  25ff000000               and      eax, 0xff
00450fb0  89ea                     mov      edx, ebp
00450fb2  e861410200               call     0x475118
00450fb7  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450fbc  8a0406                   mov      al, byte ptr [esi + eax]
00450fbf  bb06000000               mov      ebx, 6
00450fc4  25ff000000               and      eax, 0xff
00450fc9  89ea                     mov      edx, ebp
00450fcb  e848410200               call     0x475118
00450fd0  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450fd5  31d2                     xor      edx, edx
00450fd7  8a0406                   mov      al, byte ptr [esi + eax]
00450fda  88c2                     mov      dl, al
00450fdc  89c8                     mov      eax, ecx
00450fde  e8e8c80100               call     0x46d8cb
00450fe3  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00450fe8  8a0406                   mov      al, byte ptr [esi + eax]
00450feb  25ff000000               and      eax, 0xff
00450ff0  89ca                     mov      edx, ecx
00450ff2  e8d4c80100               call     0x46d8cb
00450ff7  31d2                     xor      edx, edx
00450ff9  6689fa                   mov      dx, di
00450ffc  89d3                     mov      ebx, edx
00450ffe  c1e304                   shl      ebx, 4
00451001  01d3                     add      ebx, edx
00451003  c1e302                   shl      ebx, 2
00451006  01d3                     add      ebx, edx
00451008  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0045100d  c1e302                   shl      ebx, 2
00451010  31d2                     xor      edx, edx
00451012  8a0403                   mov      al, byte ptr [ebx + eax]
00451015  88c2                     mov      dl, al
00451017  31c0                     xor      eax, eax
00451019  8a442424                 mov      al, byte ptr [esp + 0x24]
0045101d  e8dec50100               call     0x46d600
00451022  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00451027  01d8                     add      eax, ebx
00451029  8a10                     mov      dl, byte ptr [eax]
0045102b  3a542424                 cmp      dl, byte ptr [esp + 0x24]
0045102f  0f84a0000000             je       0x4510d5
00451035  8a0d41805000             mov      cl, byte ptr [0x508041]
0045103b  89c3                     mov      ebx, eax
0045103d  38ca                     cmp      dl, cl
0045103f  0f8590000000             jne      0x4510d5
00451045  a1c0194e00               mov      eax, dword ptr [0x4e19c0]
0045104a  8b0d7c8f5000             mov      ecx, dword ptr [0x508f7c]
00451050  39c8                     cmp      eax, ecx
00451052  7711                     ja       0x451065
00451054  8b35c0194e00             mov      esi, dword ptr [0x4e19c0]
0045105a  89c8                     mov      eax, ecx
0045105c  29f0                     sub      eax, esi
0045105e  3dc8000000               cmp      eax, 0xc8
00451063  7270                     jb       0x4510d5
00451065  31d2                     xor      edx, edx
00451067  a17c8f5000               mov      eax, dword ptr [0x508f7c]
0045106c  6689fa                   mov      dx, di
0045106f  a3c0194e00               mov      dword ptr [0x4e19c0], eax
00451074  89d0                     mov      eax, edx
00451076  c1e004                   shl      eax, 4
00451079  01d0                     add      eax, edx
0045107b  c1e002                   shl      eax, 2
0045107e  01c2                     add      edx, eax
00451080  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00451085  c1e202                   shl      edx, 2
00451088  668b44027c               mov      ax, word ptr [edx + eax + 0x7c]
0045108d  66a3cc6a4900             mov      word ptr [0x496acc], ax
00451093  31c0                     xor      eax, eax
00451095  8a4301                   mov      al, byte ptr [ebx + 1]
00451098  6800010000               push     0x100
0045109d  c1e010                   shl      eax, 0x10
004510a0  31c9                     xor      ecx, ecx
004510a2  80cc07                   or       ah, 7
004510a5  bbc86a4900               mov      ebx, 0x496ac8
004510aa  89c2                     mov      edx, eax
004510ac  b850000000               mov      eax, 0x50
004510b1  e8c3990300               call     0x48aa79
004510b6  eb1d                     jmp      0x4510d5
004510b8  8a6c2418                 mov      ch, byte ptr [esp + 0x18]
004510bc  80fd03                   cmp      ch, 3
004510bf  720b                     jb       0x4510cc
004510c1  0f86c8fdffff             jbe      0x450e8f
004510c7  80fd04                   cmp      ch, 4
004510ca  eb03                     jmp      0x4510cf
004510cc  80fd01                   cmp      ch, 1
004510cf  0f847efeffff             je       0x450f53
004510d5  83c428                   add      esp, 0x28
004510d8  e9cd51ffff               jmp      0x4462aa
