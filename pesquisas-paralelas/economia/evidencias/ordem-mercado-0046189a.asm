; MarcheEchangeDonne; exclusive end 0x00461bea.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Original instruction listing; unit branches are captured but unsupported.
0046189a  53                       push     ebx
0046189b  51                       push     ecx
0046189c  56                       push     esi
0046189d  57                       push     edi
0046189e  55                       push     ebp
0046189f  83ec2c                   sub      esp, 0x2c
004618a2  88442424                 mov      byte ptr [esp + 0x24], al
004618a6  88542410                 mov      byte ptr [esp + 0x10], dl
004618aa  30e4                     xor      ah, ah
004618ac  88642420                 mov      byte ptr [esp + 0x20], ah
004618b0  eb04                     jmp      0x4618b6
004618b2  fe442420                 inc      byte ptr [esp + 0x20]
004618b6  31c0                     xor      eax, eax
004618b8  8a442420                 mov      al, byte ptr [esp + 0x20]
004618bc  83f81a                   cmp      eax, 0x1a
004618bf  0f8d69020000             jge      0x461b2e
004618c5  31d2                     xor      edx, edx
004618c7  8a542410                 mov      dl, byte ptr [esp + 0x10]
004618cb  6bd234                   imul     edx, edx, 0x34
004618ce  01c0                     add      eax, eax
004618d0  01d0                     add      eax, edx
004618d2  31d2                     xor      edx, edx
004618d4  668b908c2a4e00           mov      dx, word ptr [eax + 0x4e2a8c]
004618db  85d2                     test     edx, edx
004618dd  7ed3                     jle      0x4618b2
004618df  8954240c                 mov      dword ptr [esp + 0xc], edx
004618e3  30f6                     xor      dh, dh
004618e5  8874241c                 mov      byte ptr [esp + 0x1c], dh
004618e9  e94c010000               jmp      0x461a3a
004618ee  fe442418                 inc      byte ptr [esp + 0x18]
004618f2  31c0                     xor      eax, eax
004618f4  8a442418                 mov      al, byte ptr [esp + 0x18]
004618f8  83f80a                   cmp      eax, 0xa
004618fb  0f8db3000000             jge      0x4619b4
00461901  0fb67c2428               movzx    edi, byte ptr [esp + 0x28]
00461906  6bff14                   imul     edi, edi, 0x14
00461909  01c0                     add      eax, eax
0046190b  01c7                     add      edi, eax
0046190d  31c0                     xor      eax, eax
0046190f  668b876c294e00           mov      ax, word ptr [edi + 0x4e296c]
00461916  3dffff0000               cmp      eax, 0xffff
0046191b  74d1                     je       0x4618ee
0046191d  89c7                     mov      edi, eax
0046191f  31c0                     xor      eax, eax
00461921  6689f8                   mov      ax, di
00461924  69d014010000             imul     edx, eax, 0x114
0046192a  81c2c8a04900             add      edx, 0x49a0c8
00461930  31c9                     xor      ecx, ecx
00461932  8d720c                   lea      esi, [edx + 0xc]
00461935  e83a71fbff               call     0x418a74
0046193a  89f0                     mov      eax, esi
0046193c  31db                     xor      ebx, ebx
0046193e  e8c457feff               call     0x447107
00461943  890424                   mov      dword ptr [esp], eax
00461946  eb01                     jmp      0x461949
00461948  43                       inc      ebx
00461949  663b1c24                 cmp      bx, word ptr [esp]
0046194d  7329                     jae      0x461978
0046194f  31d2                     xor      edx, edx
00461951  89f0                     mov      eax, esi
00461953  6689da                   mov      dx, bx
00461956  e88359feff               call     0x4472de
0046195b  25ffff0000               and      eax, 0xffff
00461960  e8e006feff               call     0x442045
00461965  88c2                     mov      dl, al
00461967  31c0                     xor      eax, eax
00461969  6689f8                   mov      ax, di
0046196c  e81b87fbff               call     0x41a08c
00461971  38c2                     cmp      dl, al
00461973  74d3                     je       0x461948
00461975  41                       inc      ecx
00461976  ebd0                     jmp      0x461948
00461978  31d2                     xor      edx, edx
0046197a  8a15e95b4900             mov      dl, byte ptr [0x495be9]
00461980  89d0                     mov      eax, edx
00461982  c1fa1f                   sar      edx, 0x1f
00461985  2bc2                     sub      eax, edx
00461987  d1f8                     sar      eax, 1
00461989  31d2                     xor      edx, edx
0046198b  6689ca                   mov      dx, cx
0046198e  39c2                     cmp      edx, eax
00461990  0f9cc0                   setl     al
00461993  84c0                     test     al, al
00461995  0f8453ffffff             je       0x4618ee
0046199b  31c0                     xor      eax, eax
0046199d  8a442428                 mov      al, byte ptr [esp + 0x28]
004619a1  6bc014                   imul     eax, eax, 0x14
004619a4  31d2                     xor      edx, edx
004619a6  8a542418                 mov      dl, byte ptr [esp + 0x18]
004619aa  668b84506c294e00         mov      ax, word ptr [eax + edx*2 + 0x4e296c]
004619b2  eb05                     jmp      0x4619b9
004619b4  b8ffff0000               mov      eax, 0xffff
004619b9  31f6                     xor      esi, esi
004619bb  6689c6                   mov      si, ax
004619be  81feffff0000             cmp      esi, 0xffff
004619c4  7470                     je       0x461a36
004619c6  69ee14010000             imul     ebp, esi, 0x114
004619cc  31c9                     xor      ecx, ecx
004619ce  8a4c2424                 mov      cl, byte ptr [esp + 0x24]
004619d2  89c8                     mov      eax, ecx
004619d4  e83ebe0000               call     0x46d817
004619d9  81c5c8a04900             add      ebp, 0x49a0c8
004619df  25ff000000               and      eax, 0xff
004619e4  83f801                   cmp      eax, 1
004619e7  7579                     jne      0x461a62
004619e9  0fb6742420               movzx    esi, byte ptr [esp + 0x20]
004619ee  8d5c2408                 lea      ebx, [esp + 8]
004619f2  89c8                     mov      eax, ecx
004619f4  89f2                     mov      edx, esi
004619f6  e803f9ffff               call     0x4612fe
004619fb  31db                     xor      ebx, ebx
004619fd  6689c3                   mov      bx, ax
00461a00  81fbffff0000             cmp      ebx, 0xffff
00461a06  742e                     je       0x461a36
00461a08  31c0                     xor      eax, eax
00461a0a  89da                     mov      edx, ebx
00461a0c  668b442408               mov      ax, word ptr [esp + 8]
00461a11  e824fbffff               call     0x46153a
00461a16  ba01000000               mov      edx, 1
00461a1b  8d450c                   lea      eax, [ebp + 0xc]
00461a1e  e8605afeff               call     0x447483
00461a23  31d2                     xor      edx, edx
00461a25  8a542410                 mov      dl, byte ptr [esp + 0x10]
00461a29  6bd234                   imul     edx, edx, 0x34
00461a2c  89f0                     mov      eax, esi
00461a2e  66ff8c428c2a4e00         dec      word ptr [edx + eax*2 + 0x4e2a8c]
00461a36  fe44241c                 inc      byte ptr [esp + 0x1c]
00461a3a  31c0                     xor      eax, eax
00461a3c  31d2                     xor      edx, edx
00461a3e  8a44241c                 mov      al, byte ptr [esp + 0x1c]
00461a42  668b54240c               mov      dx, word ptr [esp + 0xc]
00461a47  39d0                     cmp      eax, edx
00461a49  0f8d63feffff             jge      0x4618b2
00461a4f  8a442410                 mov      al, byte ptr [esp + 0x10]
00461a53  30ff                     xor      bh, bh
00461a55  88442428                 mov      byte ptr [esp + 0x28], al
00461a59  887c2418                 mov      byte ptr [esp + 0x18], bh
00461a5d  e990feffff               jmp      0x4618f2
00461a62  89c8                     mov      eax, ecx
00461a64  e8aebd0000               call     0x46d817
00461a69  25ff000000               and      eax, 0xff
00461a6e  83f802                   cmp      eax, 2
00461a71  75c3                     jne      0x461a36
00461a73  0fb67c2420               movzx    edi, byte ptr [esp + 0x20]
00461a78  89f8                     mov      eax, edi
00461a7a  e8b509feff               call     0x442434
00461a7f  84c0                     test     al, al
00461a81  745f                     je       0x461ae2
00461a83  89f0                     mov      eax, esi
00461a85  e85894fbff               call     0x41aee2
00461a8a  bb09000000               mov      ebx, 9
00461a8f  ba01000000               mov      edx, 1
00461a94  25ffff0000               and      eax, 0xffff
00461a99  e8ce63ffff               call     0x457e6c
00461a9e  89442404                 mov      dword ptr [esp + 4], eax
00461aa2  89f0                     mov      eax, esi
00461aa4  e83994fbff               call     0x41aee2
00461aa9  b9c8000000               mov      ecx, 0xc8
00461aae  ba01000000               mov      edx, 1
00461ab3  25ffff0000               and      eax, 0xffff
00461ab8  89fb                     mov      ebx, edi
00461aba  e8ad63ffff               call     0x457e6c
00461abf  31db                     xor      ebx, ebx
00461ac1  89c1                     mov      ecx, eax
00461ac3  668b5c2404               mov      bx, word ptr [esp + 4]
00461ac8  25ffff0000               and      eax, 0xffff
00461acd  89da                     mov      edx, ebx
00461acf  e8c05bfeff               call     0x447694
00461ad4  ba0e000000               mov      edx, 0xe
00461ad9  89d8                     mov      eax, ebx
00461adb  e87ff6fdff               call     0x44115f
00461ae0  eb1a                     jmp      0x461afc
00461ae2  89f0                     mov      eax, esi
00461ae4  e8f993fbff               call     0x41aee2
00461ae9  ba01000000               mov      edx, 1
00461aee  25ffff0000               and      eax, 0xffff
00461af3  89fb                     mov      ebx, edi
00461af5  e87263ffff               call     0x457e6c
00461afa  89c1                     mov      ecx, eax
00461afc  31db                     xor      ebx, ebx
00461afe  6689cb                   mov      bx, cx
00461b01  ba0e000000               mov      edx, 0xe
00461b06  89d8                     mov      eax, ebx
00461b08  e852f6fdff               call     0x44115f
00461b0d  ba01000000               mov      edx, 1
00461b12  8d450c                   lea      eax, [ebp + 0xc]
00461b15  e86959feff               call     0x447483
00461b1a  31d2                     xor      edx, edx
00461b1c  8a542410                 mov      dl, byte ptr [esp + 0x10]
00461b20  6bd234                   imul     edx, edx, 0x34
00461b23  31c0                     xor      eax, eax
00461b25  8a442420                 mov      al, byte ptr [esp + 0x20]
00461b29  e900ffffff               jmp      0x461a2e
00461b2e  30d2                     xor      dl, dl
00461b30  88542414                 mov      byte ptr [esp + 0x14], dl
00461b34  eb04                     jmp      0x461b3a
00461b36  fe442414                 inc      byte ptr [esp + 0x14]
00461b3a  31c9                     xor      ecx, ecx
00461b3c  8a4c2414                 mov      cl, byte ptr [esp + 0x14]
00461b40  83f903                   cmp      ecx, 3
00461b43  0f8d99000000             jge      0x461be2
00461b49  31c0                     xor      eax, eax
00461b4b  8a442410                 mov      al, byte ptr [esp + 0x10]
00461b4f  6bc006                   imul     eax, eax, 6
00461b52  8d1409                   lea      edx, [ecx + ecx]
00461b55  01c2                     add      edx, eax
00461b57  31c0                     xor      eax, eax
00461b59  668b82142d4e00           mov      ax, word ptr [edx + 0x4e2d14]
00461b60  85c0                     test     eax, eax
00461b62  7ed2                     jle      0x461b36
00461b64  31db                     xor      ebx, ebx
00461b66  8a5c2424                 mov      bl, byte ptr [esp + 0x24]
00461b6a  89d8                     mov      eax, ebx
00461b6c  e8a6bc0000               call     0x46d817
00461b71  25ff000000               and      eax, 0xff
00461b76  83f801                   cmp      eax, 1
00461b79  7514                     jne      0x461b8f
00461b7b  668b92142d4e00           mov      dx, word ptr [edx + 0x4e2d14]
00461b82  81e2ffff0000             and      edx, 0xffff
00461b88  89c8                     mov      eax, ecx
00461b8a  e82e1afcff               call     0x4235bd
00461b8f  31d2                     xor      edx, edx
00461b91  8a542410                 mov      dl, byte ptr [esp + 0x10]
00461b95  89d0                     mov      eax, edx
00461b97  6bd206                   imul     edx, edx, 6
00461b9a  31db                     xor      ebx, ebx
00461b9c  8a5c2414                 mov      bl, byte ptr [esp + 0x14]
00461ba0  c1e002                   shl      eax, 2
00461ba3  01d8                     add      eax, ebx
00461ba5  01db                     add      ebx, ebx
00461ba7  01da                     add      edx, ebx
00461ba9  31ff                     xor      edi, edi
00461bab  668b0cc5aa2e4e00         mov      cx, word ptr [eax*8 + 0x4e2eaa]
00461bb3  668b9a142d4e00           mov      bx, word ptr [edx + 0x4e2d14]
00461bba  668b34c5a82e4e00         mov      si, word ptr [eax*8 + 0x4e2ea8]
00461bc2  01d9                     add      ecx, ebx
00461bc4  01de                     add      esi, ebx
00461bc6  66890cc5aa2e4e00         mov      word ptr [eax*8 + 0x4e2eaa], cx
00461bce  6689ba142d4e00           mov      word ptr [edx + 0x4e2d14], di
00461bd5  668934c5a82e4e00         mov      word ptr [eax*8 + 0x4e2ea8], si
00461bdd  e954ffffff               jmp      0x461b36
00461be2  83c42c                   add      esp, 0x2c
00461be5  e92d1a0000               jmp      0x463617
