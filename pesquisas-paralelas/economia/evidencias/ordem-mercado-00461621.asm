; MarcheEchangePrend; exclusive end 0x0046189a.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Original instruction listing; unit branches are captured but unsupported.
00461621  53                       push     ebx
00461622  51                       push     ecx
00461623  56                       push     esi
00461624  57                       push     edi
00461625  55                       push     ebp
00461626  83ec28                   sub      esp, 0x28
00461629  8844240c                 mov      byte ptr [esp + 0xc], al
0046162d  88542410                 mov      byte ptr [esp + 0x10], dl
00461631  30e4                     xor      ah, ah
00461633  88642414                 mov      byte ptr [esp + 0x14], ah
00461637  bdffff0000               mov      ebp, 0xffff
0046163c  eb04                     jmp      0x461642
0046163e  fe442414                 inc      byte ptr [esp + 0x14]
00461642  31c0                     xor      eax, eax
00461644  8a442414                 mov      al, byte ptr [esp + 0x14]
00461648  83f81a                   cmp      eax, 0x1a
0046164b  0f8d97010000             jge      0x4617e8
00461651  31d2                     xor      edx, edx
00461653  8a542410                 mov      dl, byte ptr [esp + 0x10]
00461657  6bd234                   imul     edx, edx, 0x34
0046165a  01c0                     add      eax, eax
0046165c  01d0                     add      eax, edx
0046165e  31d2                     xor      edx, edx
00461660  668b90bc294e00           mov      dx, word ptr [eax + 0x4e29bc]
00461667  85d2                     test     edx, edx
00461669  7ed3                     jle      0x46163e
0046166b  89542404                 mov      dword ptr [esp + 4], edx
0046166f  30f6                     xor      dh, dh
00461671  8874241c                 mov      byte ptr [esp + 0x1c], dh
00461675  e946010000               jmp      0x4617c0
0046167a  fe442418                 inc      byte ptr [esp + 0x18]
0046167e  31c0                     xor      eax, eax
00461680  8a442418                 mov      al, byte ptr [esp + 0x18]
00461684  83f80a                   cmp      eax, 0xa
00461687  0f8db7000000             jge      0x461744
0046168d  31d2                     xor      edx, edx
0046168f  8a542420                 mov      dl, byte ptr [esp + 0x20]
00461693  6bd214                   imul     edx, edx, 0x14
00461696  01c0                     add      eax, eax
00461698  8d3c02                   lea      edi, [edx + eax]
0046169b  31c0                     xor      eax, eax
0046169d  668b876c294e00           mov      ax, word ptr [edi + 0x4e296c]
004616a4  3dffff0000               cmp      eax, 0xffff
004616a9  74cf                     je       0x46167a
004616ab  89c7                     mov      edi, eax
004616ad  31c0                     xor      eax, eax
004616af  6689f8                   mov      ax, di
004616b2  69f014010000             imul     esi, eax, 0x114
004616b8  81c6c8a04900             add      esi, 0x49a0c8
004616be  31c9                     xor      ecx, ecx
004616c0  83c60c                   add      esi, 0xc
004616c3  e8ac73fbff               call     0x418a74
004616c8  89f0                     mov      eax, esi
004616ca  31db                     xor      ebx, ebx
004616cc  e8365afeff               call     0x447107
004616d1  89442408                 mov      dword ptr [esp + 8], eax
004616d5  eb01                     jmp      0x4616d8
004616d7  43                       inc      ebx
004616d8  663b5c2408               cmp      bx, word ptr [esp + 8]
004616dd  7329                     jae      0x461708
004616df  31d2                     xor      edx, edx
004616e1  89f0                     mov      eax, esi
004616e3  6689da                   mov      dx, bx
004616e6  e8f35bfeff               call     0x4472de
004616eb  25ffff0000               and      eax, 0xffff
004616f0  e85009feff               call     0x442045
004616f5  88c2                     mov      dl, al
004616f7  31c0                     xor      eax, eax
004616f9  6689f8                   mov      ax, di
004616fc  e88b89fbff               call     0x41a08c
00461701  38c2                     cmp      dl, al
00461703  74d2                     je       0x4616d7
00461705  41                       inc      ecx
00461706  ebcf                     jmp      0x4616d7
00461708  31d2                     xor      edx, edx
0046170a  8a15e95b4900             mov      dl, byte ptr [0x495be9]
00461710  89d0                     mov      eax, edx
00461712  c1fa1f                   sar      edx, 0x1f
00461715  2bc2                     sub      eax, edx
00461717  d1f8                     sar      eax, 1
00461719  31d2                     xor      edx, edx
0046171b  6689ca                   mov      dx, cx
0046171e  39c2                     cmp      edx, eax
00461720  0f9cc0                   setl     al
00461723  84c0                     test     al, al
00461725  0f844fffffff             je       0x46167a
0046172b  31d2                     xor      edx, edx
0046172d  8a542420                 mov      dl, byte ptr [esp + 0x20]
00461731  6bd214                   imul     edx, edx, 0x14
00461734  31c0                     xor      eax, eax
00461736  8a442418                 mov      al, byte ptr [esp + 0x18]
0046173a  668b84426c294e00         mov      ax, word ptr [edx + eax*2 + 0x4e296c]
00461742  eb05                     jmp      0x461749
00461744  b8ffff0000               mov      eax, 0xffff
00461749  25ffff0000               and      eax, 0xffff
0046174e  3dffff0000               cmp      eax, 0xffff
00461753  7467                     je       0x4617bc
00461755  69c014010000             imul     eax, eax, 0x114
0046175b  b9c8a04900               mov      ecx, 0x49a0c8
00461760  0fb6742410               movzx    esi, byte ptr [esp + 0x10]
00461765  01c1                     add      ecx, eax
00461767  89f0                     mov      eax, esi
00461769  e8a9c00000               call     0x46d817
0046176e  25ff000000               and      eax, 0xff
00461773  83f801                   cmp      eax, 1
00461776  7544                     jne      0x4617bc
00461778  0fb67c2414               movzx    edi, byte ptr [esp + 0x14]
0046177d  89e3                     mov      ebx, esp
0046177f  89f0                     mov      eax, esi
00461781  89fa                     mov      edx, edi
00461783  e876fbffff               call     0x4612fe
00461788  31db                     xor      ebx, ebx
0046178a  6689c3                   mov      bx, ax
0046178d  81fbffff0000             cmp      ebx, 0xffff
00461793  7427                     je       0x4617bc
00461795  6bf634                   imul     esi, esi, 0x34
00461798  31c0                     xor      eax, eax
0046179a  89da                     mov      edx, ebx
0046179c  668b0424                 mov      ax, word ptr [esp]
004617a0  e895fdffff               call     0x46153a
004617a5  ba01000000               mov      edx, 1
004617aa  8d410c                   lea      eax, [ecx + 0xc]
004617ad  e8d15cfeff               call     0x447483
004617b2  89f8                     mov      eax, edi
004617b4  66ff8c46bc294e00         dec      word ptr [esi + eax*2 + 0x4e29bc]
004617bc  fe44241c                 inc      byte ptr [esp + 0x1c]
004617c0  31d2                     xor      edx, edx
004617c2  31c0                     xor      eax, eax
004617c4  8a54241c                 mov      dl, byte ptr [esp + 0x1c]
004617c8  668b442404               mov      ax, word ptr [esp + 4]
004617cd  39c2                     cmp      edx, eax
004617cf  0f8d69feffff             jge      0x46163e
004617d5  8a44240c                 mov      al, byte ptr [esp + 0xc]
004617d9  30ff                     xor      bh, bh
004617db  88442420                 mov      byte ptr [esp + 0x20], al
004617df  887c2418                 mov      byte ptr [esp + 0x18], bh
004617e3  e996feffff               jmp      0x46167e
004617e8  30d2                     xor      dl, dl
004617ea  88542424                 mov      byte ptr [esp + 0x24], dl
004617ee  eb04                     jmp      0x4617f4
004617f0  fe442424                 inc      byte ptr [esp + 0x24]
004617f4  31c9                     xor      ecx, ecx
004617f6  8a4c2424                 mov      cl, byte ptr [esp + 0x24]
004617fa  83f903                   cmp      ecx, 3
004617fd  0f8d9c310000             jge      0x46499f
00461803  31db                     xor      ebx, ebx
00461805  8a5c2410                 mov      bl, byte ptr [esp + 0x10]
00461809  6bc306                   imul     eax, ebx, 6
0046180c  8d1409                   lea      edx, [ecx + ecx]
0046180f  01c2                     add      edx, eax
00461811  31c0                     xor      eax, eax
00461813  668b82fc2c4e00           mov      ax, word ptr [edx + 0x4e2cfc]
0046181a  85c0                     test     eax, eax
0046181c  7ed2                     jle      0x4617f0
0046181e  89d8                     mov      eax, ebx
00461820  e8f2bf0000               call     0x46d817
00461825  25ff000000               and      eax, 0xff
0046182a  83f801                   cmp      eax, 1
0046182d  7514                     jne      0x461843
0046182f  668b92fc2c4e00           mov      dx, word ptr [edx + 0x4e2cfc]
00461836  81e2ffff0000             and      edx, 0xffff
0046183c  89c8                     mov      eax, ecx
0046183e  e87a1dfcff               call     0x4235bd
00461843  31db                     xor      ebx, ebx
00461845  8a5c2410                 mov      bl, byte ptr [esp + 0x10]
00461849  6bdb06                   imul     ebx, ebx, 6
0046184c  31c0                     xor      eax, eax
0046184e  31d2                     xor      edx, edx
00461850  8a44240c                 mov      al, byte ptr [esp + 0xc]
00461854  8a542424                 mov      dl, byte ptr [esp + 0x24]
00461858  c1e002                   shl      eax, 2
0046185b  01d0                     add      eax, edx
0046185d  01d2                     add      edx, edx
0046185f  01da                     add      edx, ebx
00461861  31ff                     xor      edi, edi
00461863  668b0cc5aa2e4e00         mov      cx, word ptr [eax*8 + 0x4e2eaa]
0046186b  668b9afc2c4e00           mov      bx, word ptr [edx + 0x4e2cfc]
00461872  668b34c5a82e4e00         mov      si, word ptr [eax*8 + 0x4e2ea8]
0046187a  01d9                     add      ecx, ebx
0046187c  01de                     add      esi, ebx
0046187e  66890cc5aa2e4e00         mov      word ptr [eax*8 + 0x4e2eaa], cx
00461886  6689bafc2c4e00           mov      word ptr [edx + 0x4e2cfc], di
0046188d  668934c5a82e4e00         mov      word ptr [eax*8 + 0x4e2ea8], si
00461895  e956ffffff               jmp      0x4617f0
