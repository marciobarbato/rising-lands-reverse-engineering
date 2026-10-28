; AffBatiments [0x407dd3, 0x40f49c)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00407dd3  51                     push     ecx
00407dd4  56                     push     esi
00407dd5  57                     push     edi
00407dd6  55                     push     ebp
00407dd7  81ec90040000           sub      esp, 0x490
00407ddd  50                     push     eax
00407dde  52                     push     edx
00407ddf  53                     push     ebx
00407de0  31c0                   xor      eax, eax
00407de2  6689d8                 mov      ax, bx
00407de5  8d1400                 lea      edx, [eax + eax]
00407de8  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
00407ded  01d0                   add      eax, edx
00407def  f6400180               test     byte ptr [eax + 1], 0x80
00407df3  7415                   je       0x407e0a
00407df5  668b00                 mov      ax, word ptr [eax]
00407df8  25e07f0000             and      eax, 0x7fe0
00407dfd  89c2                   mov      edx, eax
00407dff  81e2ffff0000           and      edx, 0xffff
00407e05  c1fa05                 sar      edx, 5
00407e08  eb05                   jmp      0x407e0f ;
00407e0a  baffff0000             mov      edx, 0xffff
00407e0f  31c9                   xor      ecx, ecx
00407e11  6689d1                 mov      cx, dx
00407e14  81f9ffff0000           cmp      ecx, 0xffff
00407e1a  7440                   je       0x407e5c
00407e1c  89c8                   mov      eax, ecx
00407e1e  e8c9280100             call     0x41a6ec ; BatimentGetModeEtat
00407e23  25ff000000             and      eax, 0xff
00407e28  83f803                 cmp      eax, 3
00407e2b  742f                   je       0x407e5c
00407e2d  89c8                   mov      eax, ecx
00407e2f  e858220100             call     0x41a08c ; BatimentGetPlayer
00407e34  8a3541805000           mov      dh, byte ptr [0x508041]
00407e3a  38f0                   cmp      al, dh
00407e3c  741e                   je       0x407e5c
00407e3e  89cd                   mov      ebp, ecx
00407e40  c1e504                 shl      ebp, 4
00407e43  01cd                   add      ebp, ecx
00407e45  31c0                   xor      eax, eax
00407e47  c1e502                 shl      ebp, 2
00407e4a  88f0                   mov      al, dh
00407e4c  01cd                   add      ebp, ecx
00407e4e  80bca8d8a1490000       cmp      byte ptr [eax + ebp*4 + 0x49a1d8], 0
00407e56  0f8435760000           je       0x40f491
00407e5c  31c9                   xor      ecx, ecx
00407e5e  baffff0000             mov      edx, 0xffff
00407e63  668b0c24               mov      cx, word ptr [esp]
00407e67  89942410020000         mov      dword ptr [esp + 0x210], edx
00407e6e  31d2                   xor      edx, edx
00407e70  89c8                   mov      eax, ecx
00407e72  8a1541805000           mov      dl, byte ptr [0x508041]
00407e78  e859e80600             call     0x4766d6 ; CaseEstDecouverte
00407e7d  84c0                   test     al, al
00407e7f  0f840c760000           je       0x40f491
00407e85  e82d760000             call     0x40f4b7 ; SaveCurrentClipping
00407e8a  8b15747d5000           mov      edx, dword ptr [0x507d74]
00407e90  01ca                   add      edx, ecx
00407e92  8a3df85b4900           mov      bh, byte ptr [0x495bf8]
00407e98  8a02                   mov      al, byte ptr [edx]
00407e9a  38f8                   cmp      al, bh
00407e9c  0f8505010000           jne      0x407fa7
00407ea2  31c0                   xor      eax, eax
00407ea4  6689c8                 mov      ax, cx
00407ea7  e89e360100             call     0x41b54a ; ChercheIndiceBatiment
00407eac  89842410020000         mov      dword ptr [esp + 0x210], eax
00407eb3  31c0                   xor      eax, eax
00407eb5  668b842410020000       mov      ax, word ptr [esp + 0x210]
00407ebd  3dffff0000             cmp      eax, 0xffff
00407ec2  0f84c9750000           je       0x40f491
00407ec8  31c0                   xor      eax, eax
00407eca  668b842410020000       mov      ax, word ptr [esp + 0x210]
00407ed2  89c5                   mov      ebp, eax
00407ed4  c1e504                 shl      ebp, 4
00407ed7  01c5                   add      ebp, eax
00407ed9  c1e502                 shl      ebp, 2
00407edc  01c5                   add      ebp, eax
00407ede  b8c8a04900             mov      eax, 0x49a0c8
00407ee3  c1e502                 shl      ebp, 2
00407ee6  8b742408               mov      esi, dword ptr [esp + 8]
00407eea  01c5                   add      ebp, eax
00407eec  31c0                   xor      eax, eax
00407eee  8b7c2404               mov      edi, dword ptr [esp + 4]
00407ef2  668b842410020000       mov      ax, word ptr [esp + 0x210]
00407efa  6689b42454020000       mov      word ptr [esp + 0x254], si
00407f02  e8de290100             call     0x41a8e5 ; BatimentGetEtat
00407f07  668b1524875000         mov      dx, word ptr [0x508724]
00407f0e  668b0d26875000         mov      cx, word ptr [0x508726]
00407f15  c1e205                 shl      edx, 5
00407f18  c1e105                 shl      ecx, 5
00407f1b  4a                     dec      edx
00407f1c  49                     dec      ecx
00407f1d  8994245c020000         mov      dword ptr [esp + 0x25c], edx
00407f24  ba64000000             mov      edx, 0x64
00407f29  25ffff0000             and      eax, 0xffff
00407f2e  29c2                   sub      edx, eax
00407f30  c1e205                 shl      edx, 5
00407f33  bb64000000             mov      ebx, 0x64
00407f38  89d0                   mov      eax, edx
00407f3a  c1fa1f                 sar      edx, 0x1f
00407f3d  f7fb                   idiv     ebx
00407f3f  0fbfd7                 movsx    edx, di
00407f42  01d0                   add      eax, edx
00407f44  89c2                   mov      edx, eax
00407f46  8b842452020000         mov      eax, dword ptr [esp + 0x252]
00407f4d  c1f810                 sar      eax, 0x10
00407f50  85c0                   test     eax, eax
00407f52  7d0a                   jge      0x407f5e
00407f54  31c0                   xor      eax, eax
00407f56  6689842454020000       mov      word ptr [esp + 0x254], ax
00407f5e  0fbfc2                 movsx    eax, dx
00407f61  85c0                   test     eax, eax
00407f63  7d02                   jge      0x407f67
00407f65  31d2                   xor      edx, edx
00407f67  31db                   xor      ebx, ebx
00407f69  81e1ffff0000           and      ecx, 0xffff
00407f6f  668b9c245c020000       mov      bx, word ptr [esp + 0x25c]
00407f77  31c0                   xor      eax, eax
00407f79  81e2ffff0000           and      edx, 0xffff
00407f7f  668b842454020000       mov      ax, word ptr [esp + 0x254]
00407f87  e88d750000             call     0x40f519 ; SetClipping
00407f8c  b901000000             mov      ecx, 1
00407f91  668b457c               mov      ax, word ptr [ebp + 0x7c]
00407f95  31db                   xor      ebx, ebx
00407f97  05c01c0000             add      eax, 0x1cc0
00407f9c  0fbfd7                 movsx    edx, di
00407f9f  6689c3                 mov      bx, ax
00407fa2  e96e040000             jmp      0x408415 ;
00407fa7  3a05f95b4900           cmp      al, byte ptr [0x495bf9]
00407fad  0f8588720000           jne      0x40f23b
00407fb3  31c0                   xor      eax, eax
00407fb5  6689c8                 mov      ax, cx
00407fb8  e88d350100             call     0x41b54a ; ChercheIndiceBatiment
00407fbd  89842410020000         mov      dword ptr [esp + 0x210], eax
00407fc4  31c0                   xor      eax, eax
00407fc6  668b842410020000       mov      ax, word ptr [esp + 0x210]
00407fce  3dffff0000             cmp      eax, 0xffff
00407fd3  0f84b8740000           je       0x40f491
00407fd9  31c0                   xor      eax, eax
00407fdb  668b842410020000       mov      ax, word ptr [esp + 0x210]
00407fe3  89c5                   mov      ebp, eax
00407fe5  c1e504                 shl      ebp, 4
00407fe8  01c5                   add      ebp, eax
00407fea  c1e502                 shl      ebp, 2
00407fed  01c5                   add      ebp, eax
00407fef  b8c8a04900             mov      eax, 0x49a0c8
00407ff4  c1e502                 shl      ebp, 2
00407ff7  8b742408               mov      esi, dword ptr [esp + 8]
00407ffb  01c5                   add      ebp, eax
00407ffd  31c0                   xor      eax, eax
00407fff  8b7c2404               mov      edi, dword ptr [esp + 4]
00408003  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040800b  6689b42470040000       mov      word ptr [esp + 0x470], si
00408013  e8cd280100             call     0x41a8e5 ; BatimentGetEtat
00408018  668b1524875000         mov      dx, word ptr [0x508724]
0040801f  668b0d26875000         mov      cx, word ptr [0x508726]
00408026  c1e205                 shl      edx, 5
00408029  c1e105                 shl      ecx, 5
0040802c  4a                     dec      edx
0040802d  49                     dec      ecx
0040802e  899424b8020000         mov      dword ptr [esp + 0x2b8], edx
00408035  ba64000000             mov      edx, 0x64
0040803a  25ffff0000             and      eax, 0xffff
0040803f  29c2                   sub      edx, eax
00408041  c1e205                 shl      edx, 5
00408044  bb64000000             mov      ebx, 0x64
00408049  89d0                   mov      eax, edx
0040804b  c1fa1f                 sar      edx, 0x1f
0040804e  f7fb                   idiv     ebx
00408050  0fbfd7                 movsx    edx, di
00408053  01d0                   add      eax, edx
00408055  89c2                   mov      edx, eax
00408057  8b84246e040000         mov      eax, dword ptr [esp + 0x46e]
0040805e  c1f810                 sar      eax, 0x10
00408061  85c0                   test     eax, eax
00408063  7d0a                   jge      0x40806f
00408065  31db                   xor      ebx, ebx
00408067  66899c2470040000       mov      word ptr [esp + 0x470], bx
0040806f  0fbfc2                 movsx    eax, dx
00408072  85c0                   test     eax, eax
00408074  7d02                   jge      0x408078
00408076  31d2                   xor      edx, edx
00408078  31db                   xor      ebx, ebx
0040807a  81e1ffff0000           and      ecx, 0xffff
00408080  668b9c24b8020000       mov      bx, word ptr [esp + 0x2b8]
00408088  31c0                   xor      eax, eax
0040808a  81e2ffff0000           and      edx, 0xffff
00408090  668b842470040000       mov      ax, word ptr [esp + 0x470]
00408098  e87c740000             call     0x40f519 ; SetClipping
0040809d  31c0                   xor      eax, eax
0040809f  668b457c               mov      ax, word ptr [ebp + 0x7c]
004080a3  85c0                   test     eax, eax
004080a5  7516                   jne      0x4080bd
004080a7  30e4                   xor      ah, ah
004080a9  b901000000             mov      ecx, 1
004080ae  8a4576                 mov      al, byte ptr [ebp + 0x76]
004080b1  31db                   xor      ebx, ebx
004080b3  05981d0000             add      eax, 0x1d98
004080b8  e9dffeffff             jmp      0x407f9c ;
004080bd  30e4                   xor      ah, ah
004080bf  8a4576                 mov      al, byte ptr [ebp + 0x76]
004080c2  31db                   xor      ebx, ebx
004080c4  05b81d0000             add      eax, 0x1db8
004080c9  6689c3                 mov      bx, ax
004080cc  89f8                   mov      eax, edi
004080ce  0504000000             add      eax, 4
004080d3  0fbfd0                 movsx    edx, ax
004080d6  89f0                   mov      eax, esi
004080d8  0505000000             add      eax, 5
004080dd  b901000000             mov      ecx, 1
004080e2  98                     cwde
004080e3  e930030000             jmp      0x408418 ;
004080e8  31c0                   xor      eax, eax
004080ea  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
004080f0  668b0424               mov      ax, word ptr [esp]
004080f4  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
004080f9  7424                   je       0x40811f
004080fb  31c0                   xor      eax, eax
004080fd  668b0424               mov      ax, word ptr [esp]
00408101  8d1400                 lea      edx, [eax + eax]
00408104  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
00408109  668b0402               mov      ax, word ptr [edx + eax]
0040810d  25e07f0000             and      eax, 0x7fe0
00408112  89c3                   mov      ebx, eax
00408114  81e3ffff0000           and      ebx, 0xffff
0040811a  c1fb05                 sar      ebx, 5
0040811d  eb05                   jmp      0x408124 ;
0040811f  bbffff0000             mov      ebx, 0xffff
00408124  31c0                   xor      eax, eax
00408126  6689d8                 mov      ax, bx
00408129  899c2410020000         mov      dword ptr [esp + 0x210], ebx
00408130  3dffff0000             cmp      eax, 0xffff
00408135  0f8456730000           je       0x40f491
0040813b  89c5                   mov      ebp, eax
0040813d  c1e504                 shl      ebp, 4
00408140  01c5                   add      ebp, eax
00408142  8b742408               mov      esi, dword ptr [esp + 8]
00408146  c1e502                 shl      ebp, 2
00408149  8b7c2404               mov      edi, dword ptr [esp + 4]
0040814d  01c5                   add      ebp, eax
0040814f  e891270100             call     0x41a8e5 ; BatimentGetEtat
00408154  c1e502                 shl      ebp, 2
00408157  89c2                   mov      edx, eax
00408159  89842424020000         mov      dword ptr [esp + 0x224], eax
00408160  81c5c8a04900           add      ebp, 0x49a0c8
00408166  31c0                   xor      eax, eax
00408168  83ee5e                 sub      esi, 0x5e
0040816b  8a4505                 mov      al, byte ptr [ebp + 5]
0040816e  81ef9a000000           sub      edi, 0x9a
00408174  83f805                 cmp      eax, 5
00408177  740e                   je       0x408187
00408179  83f803                 cmp      eax, 3
0040817c  7409                   je       0x408187
0040817e  83f804                 cmp      eax, 4
00408181  0f85e8010000           jne      0x40836f
00408187  31c0                   xor      eax, eax
00408189  8a4505                 mov      al, byte ptr [ebp + 5]
0040818c  83f803                 cmp      eax, 3
0040818f  0f8516010000           jne      0x4082ab
00408195  31c0                   xor      eax, eax
00408197  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040819f  e814240100             call     0x41a5b8 ; BatimentEstHabiter
004081a4  84c0                   test     al, al
004081a6  0f85ff000000           jne      0x4082ab
004081ac  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
004081b2  31d2                   xor      edx, edx
004081b4  88da                   mov      dl, bl
004081b6  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
004081bc  81e2ff000000           and      edx, 0xff
004081c2  b903000000             mov      ecx, 3
004081c7  89d0                   mov      eax, edx
004081c9  c1fa1f                 sar      edx, 0x1f
004081cc  f7f9                   idiv     ecx
004081ce  0fbfcf                 movsx    ecx, di
004081d1  01ca                   add      edx, ecx
004081d3  81c2bc000000           add      edx, 0xbc
004081d9  fec3                   inc      bl
004081db  668994248c020000       mov      word ptr [esp + 0x28c], dx
004081e3  31d2                   xor      edx, edx
004081e5  88da                   mov      dl, bl
004081e7  881d181d4e00           mov      byte ptr [0x4e1d18], bl
004081ed  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
004081f3  81e2ff000000           and      edx, 0xff
004081f9  bf03000000             mov      edi, 3
004081fe  89d0                   mov      eax, edx
00408200  c1fa1f                 sar      edx, 0x1f
00408203  f7ff                   idiv     edi
00408205  fec3                   inc      bl
00408207  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040820d  8d3c0a                 lea      edi, [edx + ecx]
00408210  31c0                   xor      eax, eax
00408212  81c7c8000000           add      edi, 0xc8
00408218  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040821f  29c7                   sub      edi, eax
00408221  0fbfc7                 movsx    eax, di
00408224  85c0                   test     eax, eax
00408226  7d02                   jge      0x40822a
00408228  31ff                   xor      edi, edi
0040822a  31c0                   xor      eax, eax
0040822c  66a126875000           mov      ax, word ptr [0x508726]
00408232  89c2                   mov      edx, eax
00408234  8b84248a020000         mov      eax, dword ptr [esp + 0x28a]
0040823b  c1e205                 shl      edx, 5
0040823e  c1f810                 sar      eax, 0x10
00408241  4a                     dec      edx
00408242  39d0                   cmp      eax, edx
00408244  7e12                   jle      0x408258
00408246  66a126875000           mov      ax, word ptr [0x508726]
0040824c  c1e005                 shl      eax, 5
0040824f  48                     dec      eax
00408250  668984248c020000       mov      word ptr [esp + 0x28c], ax
00408258  66a124875000           mov      ax, word ptr [0x508724]
0040825e  31c9                   xor      ecx, ecx
00408260  31db                   xor      ebx, ebx
00408262  31d2                   xor      edx, edx
00408264  668b8c248c020000       mov      cx, word ptr [esp + 0x28c]
0040826c  c1e005                 shl      eax, 5
0040826f  6689fa                 mov      dx, di
00408272  6689c3                 mov      bx, ax
00408275  31c0                   xor      eax, eax
00408277  e89d720000             call     0x40f519 ; SetClipping
0040827c  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00408282  31d2                   xor      edx, edx
00408284  88da                   mov      dl, bl
00408286  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040828c  81e2ff000000           and      edx, 0xff
00408292  b903000000             mov      ecx, 3
00408297  89d0                   mov      eax, edx
00408299  c1fa1f                 sar      edx, 0x1f
0040829c  f7f9                   idiv     ecx
0040829e  fec3                   inc      bl
004082a0  0fbff6                 movsx    esi, si
004082a3  881d181d4e00           mov      byte ptr [0x4e1d18], bl
004082a9  01d6                   add      esi, edx
004082ab  31c0                   xor      eax, eax
004082ad  668b842410020000       mov      ax, word ptr [esp + 0x210]
004082b5  e8fe220100             call     0x41a5b8 ; BatimentEstHabiter
004082ba  84c0                   test     al, al
004082bc  7451                   je       0x40830f
004082be  b901000000             mov      ecx, 1
004082c3  31c0                   xor      eax, eax
004082c5  bb761b0000             mov      ebx, 0x1b76
004082ca  8a4504                 mov      al, byte ptr [ebp + 4]
004082cd  0fbfd7                 movsx    edx, di
004082d0  50                     push     eax
004082d1  0fbfc6                 movsx    eax, si
004082d4  e87c410500             call     0x45c455 ; PastePlayerCmp
004082d9  31c0                   xor      eax, eax
004082db  8a4504                 mov      al, byte ptr [ebp + 4]
004082de  50                     push     eax
004082df  66a17c8f5000           mov      ax, word ptr [0x508f7c]
004082e5  30e4                   xor      ah, ah
004082e7  240f                   and      al, 0xf
004082e9  31db                   xor      ebx, ebx
004082eb  051d2b0000             add      eax, 0x2b1d
004082f0  6689c3                 mov      bx, ax
004082f3  89f8                   mov      eax, edi
004082f5  0504000000             add      eax, 4
004082fa  0fbfd0                 movsx    edx, ax
004082fd  89f0                   mov      eax, esi
004082ff  0548000000             add      eax, 0x48
00408304  b901000000             mov      ecx, 1
00408309  98                     cwde
0040830a  e846410500             call     0x45c455 ; PastePlayerCmp
0040830f  31c0                   xor      eax, eax
00408311  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408319  e89a220100             call     0x41a5b8 ; BatimentEstHabiter
0040831e  84c0                   test     al, al
00408320  7538                   jne      0x40835a
00408322  b901000000             mov      ecx, 1
00408327  0fbfc7                 movsx    eax, di
0040832a  bb761b0000             mov      ebx, 0x1b76
0040832f  89442458               mov      dword ptr [esp + 0x58], eax
00408333  0fbfc6                 movsx    eax, si
00408336  8b542458               mov      edx, dword ptr [esp + 0x58]
0040833a  89442454               mov      dword ptr [esp + 0x54], eax
0040833e  e8042f0500             call     0x45b247 ; PasteBobCmp
00408343  b901000000             mov      ecx, 1
00408348  bb761b0000             mov      ebx, 0x1b76
0040834d  8b542458               mov      edx, dword ptr [esp + 0x58]
00408351  8b442454               mov      eax, dword ptr [esp + 0x54]
00408355  e856390500             call     0x45bcb0 ; PasteGrisCmp
0040835a  31c0                   xor      eax, eax
0040835c  668b4506               mov      ax, word ptr [ebp + 6]
00408360  85c0                   test     eax, eax
00408362  0f8eda6f0000           jle      0x40f342
00408368  6a01                   push     1
0040836a  e973520000             jmp      0x40d5e2 ;
0040836f  31c0                   xor      eax, eax
00408371  668b0d26875000         mov      cx, word ptr [0x508726]
00408378  6689d0                 mov      ax, dx
0040837b  668b1524875000         mov      dx, word ptr [0x508724]
00408382  c1e105                 shl      ecx, 5
00408385  c1e205                 shl      edx, 5
00408388  49                     dec      ecx
00408389  4a                     dec      edx
0040838a  83f864                 cmp      eax, 0x64
0040838d  0f8d8f000000           jge      0x408422
00408393  899424d8020000         mov      dword ptr [esp + 0x2d8], edx
0040839a  ba64000000             mov      edx, 0x64
0040839f  29c2                   sub      edx, eax
004083a1  89d0                   mov      eax, edx
004083a3  c1e202                 shl      edx, 2
004083a6  29c2                   sub      edx, eax
004083a8  c1e204                 shl      edx, 4
004083ab  29c2                   sub      edx, eax
004083ad  c1e202                 shl      edx, 2
004083b0  bb64000000             mov      ebx, 0x64
004083b5  89d0                   mov      eax, edx
004083b7  c1fa1f                 sar      edx, 0x1f
004083ba  f7fb                   idiv     ebx
004083bc  0fbfd7                 movsx    edx, di
004083bf  01d0                   add      eax, edx
004083c1  89c2                   mov      edx, eax
004083c3  0fbfc6                 movsx    eax, si
004083c6  89b42454030000         mov      dword ptr [esp + 0x354], esi
004083cd  85c0                   test     eax, eax
004083cf  7d09                   jge      0x4083da
004083d1  31c0                   xor      eax, eax
004083d3  89842454030000         mov      dword ptr [esp + 0x354], eax
004083da  0fbfc2                 movsx    eax, dx
004083dd  85c0                   test     eax, eax
004083df  7d02                   jge      0x4083e3
004083e1  31d2                   xor      edx, edx
004083e3  31db                   xor      ebx, ebx
004083e5  81e1ffff0000           and      ecx, 0xffff
004083eb  668b9c24d8020000       mov      bx, word ptr [esp + 0x2d8]
004083f3  31c0                   xor      eax, eax
004083f5  81e2ffff0000           and      edx, 0xffff
004083fb  668b842454030000       mov      ax, word ptr [esp + 0x354]
00408403  e811710000             call     0x40f519 ; SetClipping
00408408  b901000000             mov      ecx, 1
0040840d  bb751b0000             mov      ebx, 0x1b75
00408412  0fbfd7                 movsx    edx, di
00408415  0fbfc6                 movsx    eax, si
00408418  e82a2e0500             call     0x45b247 ; PasteBobCmp
0040841d  e9206f0000             jmp      0x40f342 ;
00408422  89942450040000         mov      dword ptr [esp + 0x450], edx
00408429  83e864                 sub      eax, 0x64
0040842c  ba64000000             mov      edx, 0x64
00408431  29c2                   sub      edx, eax
00408433  89d0                   mov      eax, edx
00408435  c1e202                 shl      edx, 2
00408438  29c2                   sub      edx, eax
0040843a  c1e204                 shl      edx, 4
0040843d  29c2                   sub      edx, eax
0040843f  c1e202                 shl      edx, 2
00408442  bb64000000             mov      ebx, 0x64
00408447  89d0                   mov      eax, edx
00408449  c1fa1f                 sar      edx, 0x1f
0040844c  f7fb                   idiv     ebx
0040844e  0fbfd7                 movsx    edx, di
00408451  01d0                   add      eax, edx
00408453  31d2                   xor      edx, edx
00408455  668b1526875000         mov      dx, word ptr [0x508726]
0040845c  898c24f8010000         mov      dword ptr [esp + 0x1f8], ecx
00408463  c1e205                 shl      edx, 5
00408466  0fbfd8                 movsx    ebx, ax
00408469  4a                     dec      edx
0040846a  6689b42474040000       mov      word ptr [esp + 0x474], si
00408472  39d3                   cmp      ebx, edx
00408474  7e02                   jle      0x408478
00408476  89c8                   mov      eax, ecx
00408478  31c9                   xor      ecx, ecx
0040847a  31db                   xor      ebx, ebx
0040847c  31d2                   xor      edx, edx
0040847e  668b9c2450040000       mov      bx, word ptr [esp + 0x450]
00408486  6689c1                 mov      cx, ax
00408489  31c0                   xor      eax, eax
0040848b  e889700000             call     0x40f519 ; SetClipping
00408490  0fbfc7                 movsx    eax, di
00408493  b901000000             mov      ecx, 1
00408498  89442454               mov      dword ptr [esp + 0x54], eax
0040849c  bb751b0000             mov      ebx, 0x1b75
004084a1  8b542454               mov      edx, dword ptr [esp + 0x54]
004084a5  0fbfc6                 movsx    eax, si
004084a8  e89a2d0500             call     0x45b247 ; PasteBobCmp
004084ad  31c0                   xor      eax, eax
004084af  668b842424020000       mov      ax, word ptr [esp + 0x224]
004084b7  ba64000000             mov      edx, 0x64
004084bc  83e864                 sub      eax, 0x64
004084bf  29c2                   sub      edx, eax
004084c1  89d0                   mov      eax, edx
004084c3  c1e202                 shl      edx, 2
004084c6  29c2                   sub      edx, eax
004084c8  c1e204                 shl      edx, 4
004084cb  29c2                   sub      edx, eax
004084cd  c1e202                 shl      edx, 2
004084d0  bb64000000             mov      ebx, 0x64
004084d5  89d0                   mov      eax, edx
004084d7  c1fa1f                 sar      edx, 0x1f
004084da  f7fb                   idiv     ebx
004084dc  8b942472040000         mov      edx, dword ptr [esp + 0x472]
004084e3  8b5c2454               mov      ebx, dword ptr [esp + 0x54]
004084e7  c1fa10                 sar      edx, 0x10
004084ea  01d8                   add      eax, ebx
004084ec  85d2                   test     edx, edx
004084ee  7d0a                   jge      0x4084fa
004084f0  31db                   xor      ebx, ebx
004084f2  66899c2474040000       mov      word ptr [esp + 0x474], bx
004084fa  0fbfd0                 movsx    edx, ax
004084fd  85d2                   test     edx, edx
004084ff  7d02                   jge      0x408503
00408501  31c0                   xor      eax, eax
00408503  31c9                   xor      ecx, ecx
00408505  31db                   xor      ebx, ebx
00408507  31d2                   xor      edx, edx
00408509  668b8c24f8010000       mov      cx, word ptr [esp + 0x1f8]
00408511  6689c2                 mov      dx, ax
00408514  31c0                   xor      eax, eax
00408516  668b9c2450040000       mov      bx, word ptr [esp + 0x450]
0040851e  668b842474040000       mov      ax, word ptr [esp + 0x474]
00408526  0fbfef                 movsx    ebp, di
00408529  e8eb6f0000             call     0x40f519 ; SetClipping
0040852e  b901000000             mov      ecx, 1
00408533  bb761b0000             mov      ebx, 0x1b76
00408538  0fbfc6                 movsx    eax, si
0040853b  89ea                   mov      edx, ebp
0040853d  89442414               mov      dword ptr [esp + 0x14], eax
00408541  e8012d0500             call     0x45b247 ; PasteBobCmp
00408546  31c0                   xor      eax, eax
00408548  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408550  e863200100             call     0x41a5b8 ; BatimentEstHabiter
00408555  84c0                   test     al, al
00408557  0f85e56d0000           jne      0x40f342
0040855d  b901000000             mov      ecx, 1
00408562  bb761b0000             mov      ebx, 0x1b76
00408567  8b442414               mov      eax, dword ptr [esp + 0x14]
0040856b  89ea                   mov      edx, ebp
0040856d  e83e370500             call     0x45bcb0 ; PasteGrisCmp
00408572  e9cb6d0000             jmp      0x40f342 ;
00408577  31c0                   xor      eax, eax
00408579  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040857f  668b0424               mov      ax, word ptr [esp]
00408583  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
00408588  7424                   je       0x4085ae
0040858a  31c0                   xor      eax, eax
0040858c  668b0424               mov      ax, word ptr [esp]
00408590  8d1400                 lea      edx, [eax + eax]
00408593  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
00408598  668b0402               mov      ax, word ptr [edx + eax]
0040859c  25e07f0000             and      eax, 0x7fe0
004085a1  89c3                   mov      ebx, eax
004085a3  81e3ffff0000           and      ebx, 0xffff
004085a9  c1fb05                 sar      ebx, 5
004085ac  eb05                   jmp      0x4085b3 ;
004085ae  bbffff0000             mov      ebx, 0xffff
004085b3  31d2                   xor      edx, edx
004085b5  6689da                 mov      dx, bx
004085b8  899c2410020000         mov      dword ptr [esp + 0x210], ebx
004085bf  81faffff0000           cmp      edx, 0xffff
004085c5  0f84c66e0000           je       0x40f491
004085cb  89d5                   mov      ebp, edx
004085cd  8b742408               mov      esi, dword ptr [esp + 8]
004085d1  c1e504                 shl      ebp, 4
004085d4  8b7c2404               mov      edi, dword ptr [esp + 4]
004085d8  01d5                   add      ebp, edx
004085da  89d0                   mov      eax, edx
004085dc  c1e502                 shl      ebp, 2
004085df  e801230100             call     0x41a8e5 ; BatimentGetEtat
004085e4  01d5                   add      ebp, edx
004085e6  898424d8010000         mov      dword ptr [esp + 0x1d8], eax
004085ed  c1e502                 shl      ebp, 2
004085f0  89c2                   mov      edx, eax
004085f2  81c5c8a04900           add      ebp, 0x49a0c8
004085f8  31c0                   xor      eax, eax
004085fa  81ee96000000           sub      esi, 0x96
00408600  8a4505                 mov      al, byte ptr [ebp + 5]
00408603  83ef5d                 sub      edi, 0x5d
00408606  83f805                 cmp      eax, 5
00408609  740e                   je       0x408619
0040860b  83f803                 cmp      eax, 3
0040860e  7409                   je       0x408619
00408610  83f804                 cmp      eax, 4
00408613  0f85af040000           jne      0x408ac8
00408619  31c0                   xor      eax, eax
0040861b  8a4505                 mov      al, byte ptr [ebp + 5]
0040861e  83f803                 cmp      eax, 3
00408621  0f8513010000           jne      0x40873a
00408627  31c0                   xor      eax, eax
00408629  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408631  e8821f0100             call     0x41a5b8 ; BatimentEstHabiter
00408636  84c0                   test     al, al
00408638  0f85fc000000           jne      0x40873a
0040863e  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
00408644  31d2                   xor      edx, edx
00408646  88ca                   mov      dl, cl
00408648  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040864e  81e2ff000000           and      edx, 0xff
00408654  bb03000000             mov      ebx, 3
00408659  89d0                   mov      eax, edx
0040865b  c1fa1f                 sar      edx, 0x1f
0040865e  f7fb                   idiv     ebx
00408660  0fbfdf                 movsx    ebx, di
00408663  01da                   add      edx, ebx
00408665  81c299000000           add      edx, 0x99
0040866b  fec1                   inc      cl
0040866d  6689942444020000       mov      word ptr [esp + 0x244], dx
00408675  31d2                   xor      edx, edx
00408677  88ca                   mov      dl, cl
00408679  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040867f  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00408685  81e2ff000000           and      edx, 0xff
0040868b  bf03000000             mov      edi, 3
00408690  89d0                   mov      eax, edx
00408692  c1fa1f                 sar      edx, 0x1f
00408695  f7ff                   idiv     edi
00408697  fec1                   inc      cl
00408699  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040869f  8d0413                 lea      eax, [ebx + edx]
004086a2  31d2                   xor      edx, edx
004086a4  05c8000000             add      eax, 0xc8
004086a9  668b9584000000         mov      dx, word ptr [ebp + 0x84]
004086b0  29d0                   sub      eax, edx
004086b2  89c7                   mov      edi, eax
004086b4  98                     cwde
004086b5  85c0                   test     eax, eax
004086b7  7d02                   jge      0x4086bb
004086b9  31ff                   xor      edi, edi
004086bb  31c0                   xor      eax, eax
004086bd  66a126875000           mov      ax, word ptr [0x508726]
004086c3  8b942442020000         mov      edx, dword ptr [esp + 0x242]
004086ca  c1e005                 shl      eax, 5
004086cd  c1fa10                 sar      edx, 0x10
004086d0  48                     dec      eax
004086d1  39c2                   cmp      edx, eax
004086d3  7e12                   jle      0x4086e7
004086d5  66a126875000           mov      ax, word ptr [0x508726]
004086db  c1e005                 shl      eax, 5
004086de  48                     dec      eax
004086df  6689842444020000       mov      word ptr [esp + 0x244], ax
004086e7  66a124875000           mov      ax, word ptr [0x508724]
004086ed  31c9                   xor      ecx, ecx
004086ef  31db                   xor      ebx, ebx
004086f1  31d2                   xor      edx, edx
004086f3  668b8c2444020000       mov      cx, word ptr [esp + 0x244]
004086fb  c1e005                 shl      eax, 5
004086fe  6689fa                 mov      dx, di
00408701  6689c3                 mov      bx, ax
00408704  31c0                   xor      eax, eax
00408706  e80e6e0000             call     0x40f519 ; SetClipping
0040870b  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00408711  31d2                   xor      edx, edx
00408713  88da                   mov      dl, bl
00408715  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040871b  81e2ff000000           and      edx, 0xff
00408721  b903000000             mov      ecx, 3
00408726  89d0                   mov      eax, edx
00408728  c1fa1f                 sar      edx, 0x1f
0040872b  f7f9                   idiv     ecx
0040872d  fec3                   inc      bl
0040872f  0fbff6                 movsx    esi, si
00408732  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00408738  01d6                   add      esi, edx
0040873a  89f2                   mov      edx, esi
0040873c  83c212                 add      edx, 0x12
0040873f  668994241c040000       mov      word ptr [esp + 0x41c], dx
00408747  89fa                   mov      edx, edi
00408749  83c23f                 add      edx, 0x3f
0040874c  6689942428030000       mov      word ptr [esp + 0x328], dx
00408754  89f2                   mov      edx, esi
00408756  81c297000000           add      edx, 0x97
0040875c  668994246c020000       mov      word ptr [esp + 0x26c], dx
00408764  89fa                   mov      edx, edi
00408766  81c283000000           add      edx, 0x83
0040876c  668994241c030000       mov      word ptr [esp + 0x31c], dx
00408774  89f2                   mov      edx, esi
00408776  83c259                 add      edx, 0x59
00408779  6689942408040000       mov      word ptr [esp + 0x408], dx
00408781  89fa                   mov      edx, edi
00408783  83c25f                 add      edx, 0x5f
00408786  66899424d4030000       mov      word ptr [esp + 0x3d4], dx
0040878e  89f2                   mov      edx, esi
00408790  83c24a                 add      edx, 0x4a
00408793  31c0                   xor      eax, eax
00408795  6689942400040000       mov      word ptr [esp + 0x400], dx
0040879d  89fa                   mov      edx, edi
0040879f  668b842410020000       mov      ax, word ptr [esp + 0x210]
004087a7  83c205                 add      edx, 5
004087aa  e8091e0100             call     0x41a5b8 ; BatimentEstHabiter
004087af  668994240c040000       mov      word ptr [esp + 0x40c], dx
004087b7  84c0                   test     al, al
004087b9  0f846e010000           je       0x40892d
004087bf  b901000000             mov      ecx, 1
004087c4  31c0                   xor      eax, eax
004087c6  bb781b0000             mov      ebx, 0x1b78
004087cb  8a4504                 mov      al, byte ptr [ebp + 4]
004087ce  0fbfd7                 movsx    edx, di
004087d1  50                     push     eax
004087d2  0fbfc6                 movsx    eax, si
004087d5  e87b3c0500             call     0x45c455 ; PastePlayerCmp
004087da  31c0                   xor      eax, eax
004087dc  8a4504                 mov      al, byte ptr [ebp + 4]
004087df  8b1424                 mov      edx, dword ptr [esp]
004087e2  50                     push     eax
004087e3  66a1848f5000           mov      ax, word ptr [0x508f84]
004087e9  01d0                   add      eax, edx
004087eb  30e4                   xor      ah, ah
004087ed  b901000000             mov      ecx, 1
004087f2  2407                   and      al, 7
004087f4  31db                   xor      ebx, ebx
004087f6  05891b0000             add      eax, 0x1b89
004087fb  8b94240e040000         mov      edx, dword ptr [esp + 0x40e]
00408802  6689c3                 mov      bx, ax
00408805  8b842402040000         mov      eax, dword ptr [esp + 0x402]
0040880c  c1fa10                 sar      edx, 0x10
0040880f  c1f810                 sar      eax, 0x10
00408812  e83e3c0500             call     0x45c455 ; PastePlayerCmp
00408817  8b1c24                 mov      ebx, dword ptr [esp]
0040881a  66a17c8f5000           mov      ax, word ptr [0x508f7c]
00408820  01d8                   add      eax, ebx
00408822  30e4                   xor      ah, ah
00408824  8b9424d2030000         mov      edx, dword ptr [esp + 0x3d2]
0040882b  2407                   and      al, 7
0040882d  31db                   xor      ebx, ebx
0040882f  05791b0000             add      eax, 0x1b79
00408834  b901000000             mov      ecx, 1
00408839  6689c3                 mov      bx, ax
0040883c  8b842406040000         mov      eax, dword ptr [esp + 0x406]
00408843  c1fa10                 sar      edx, 0x10
00408846  c1f810                 sar      eax, 0x10
00408849  e8f9290500             call     0x45b247 ; PasteBobCmp
0040884e  8b0c24                 mov      ecx, dword ptr [esp]
00408851  66a1808f5000           mov      ax, word ptr [0x508f80]
00408857  01c8                   add      eax, ecx
00408859  30e4                   xor      ah, ah
0040885b  8b94241a030000         mov      edx, dword ptr [esp + 0x31a]
00408862  2407                   and      al, 7
00408864  31db                   xor      ebx, ebx
00408866  05811b0000             add      eax, 0x1b81
0040886b  c1fa10                 sar      edx, 0x10
0040886e  6689c3                 mov      bx, ax
00408871  8b84246a020000         mov      eax, dword ptr [esp + 0x26a]
00408878  b901000000             mov      ecx, 1
0040887d  c1f810                 sar      eax, 0x10
00408880  e8c2290500             call     0x45b247 ; PasteBobCmp
00408885  31c0                   xor      eax, eax
00408887  8a4504                 mov      al, byte ptr [ebp + 4]
0040888a  50                     push     eax
0040888b  66a17c8f5000           mov      ax, word ptr [0x508f7c]
00408891  30e4                   xor      ah, ah
00408893  2407                   and      al, 7
00408895  31db                   xor      ebx, ebx
00408897  05931b0000             add      eax, 0x1b93
0040889c  6689c3                 mov      bx, ax
0040889f  89f8                   mov      eax, edi
004088a1  0540000000             add      eax, 0x40
004088a6  0fbfd0                 movsx    edx, ax
004088a9  89f0                   mov      eax, esi
004088ab  0530000000             add      eax, 0x30
004088b0  b901000000             mov      ecx, 1
004088b5  98                     cwde
004088b6  e89a3b0500             call     0x45c455 ; PastePlayerCmp
004088bb  31c0                   xor      eax, eax
004088bd  8a4504                 mov      al, byte ptr [ebp + 4]
004088c0  50                     push     eax
004088c1  66a17c8f5000           mov      ax, word ptr [0x508f7c]
004088c7  30e4                   xor      ah, ah
004088c9  2407                   and      al, 7
004088cb  31db                   xor      ebx, ebx
004088cd  059b1b0000             add      eax, 0x1b9b
004088d2  6689c3                 mov      bx, ax
004088d5  89f8                   mov      eax, edi
004088d7  054a000000             add      eax, 0x4a
004088dc  0fbfd0                 movsx    edx, ax
004088df  89f0                   mov      eax, esi
004088e1  0590000000             add      eax, 0x90
004088e6  b901000000             mov      ecx, 1
004088eb  98                     cwde
004088ec  e8643b0500             call     0x45c455 ; PastePlayerCmp
004088f1  8b1424                 mov      edx, dword ptr [esp]
004088f4  66a17c8f5000           mov      ax, word ptr [0x508f7c]
004088fa  01d0                   add      eax, edx
004088fc  30e4                   xor      ah, ah
004088fe  b901000000             mov      ecx, 1
00408903  2401                   and      al, 1
00408905  31db                   xor      ebx, ebx
00408907  05911b0000             add      eax, 0x1b91
0040890c  8b942426030000         mov      edx, dword ptr [esp + 0x326]
00408913  6689c3                 mov      bx, ax
00408916  8b84241a040000         mov      eax, dword ptr [esp + 0x41a]
0040891d  c1fa10                 sar      edx, 0x10
00408920  c1f810                 sar      eax, 0x10
00408923  e81f290500             call     0x45b247 ; PasteBobCmp
00408928  e986010000             jmp      0x408ab3 ;
0040892d  b901000000             mov      ecx, 1
00408932  0fbfc7                 movsx    eax, di
00408935  bb781b0000             mov      ebx, 0x1b78
0040893a  8984249c000000         mov      dword ptr [esp + 0x9c], eax
00408941  0fbfc6                 movsx    eax, si
00408944  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040894b  89842498000000         mov      dword ptr [esp + 0x98], eax
00408952  e8f0280500             call     0x45b247 ; PasteBobCmp
00408957  8b84240a040000         mov      eax, dword ptr [esp + 0x40a]
0040895e  c1f810                 sar      eax, 0x10
00408961  b901000000             mov      ecx, 1
00408966  89842494000000         mov      dword ptr [esp + 0x94], eax
0040896d  8b8424fe030000         mov      eax, dword ptr [esp + 0x3fe]
00408974  bb891b0000             mov      ebx, 0x1b89
00408979  c1f810                 sar      eax, 0x10
0040897c  8b942494000000         mov      edx, dword ptr [esp + 0x94]
00408983  8944247c               mov      dword ptr [esp + 0x7c], eax
00408987  e8bb280500             call     0x45b247 ; PasteBobCmp
0040898c  8b8424d2030000         mov      eax, dword ptr [esp + 0x3d2]
00408993  c1f810                 sar      eax, 0x10
00408996  b901000000             mov      ecx, 1
0040899b  89442458               mov      dword ptr [esp + 0x58], eax
0040899f  8b842406040000         mov      eax, dword ptr [esp + 0x406]
004089a6  bb791b0000             mov      ebx, 0x1b79
004089ab  c1f810                 sar      eax, 0x10
004089ae  8b542458               mov      edx, dword ptr [esp + 0x58]
004089b2  89442454               mov      dword ptr [esp + 0x54], eax
004089b6  e88c280500             call     0x45b247 ; PasteBobCmp
004089bb  8b84241a030000         mov      eax, dword ptr [esp + 0x31a]
004089c2  c1f810                 sar      eax, 0x10
004089c5  b901000000             mov      ecx, 1
004089ca  898424c0000000         mov      dword ptr [esp + 0xc0], eax
004089d1  8b84246a020000         mov      eax, dword ptr [esp + 0x26a]
004089d8  bb811b0000             mov      ebx, 0x1b81
004089dd  c1f810                 sar      eax, 0x10
004089e0  8b9424c0000000         mov      edx, dword ptr [esp + 0xc0]
004089e7  898424b8010000         mov      dword ptr [esp + 0x1b8], eax
004089ee  e854280500             call     0x45b247 ; PasteBobCmp
004089f3  8b842426030000         mov      eax, dword ptr [esp + 0x326]
004089fa  c1f810                 sar      eax, 0x10
004089fd  b901000000             mov      ecx, 1
00408a02  8984248c000000         mov      dword ptr [esp + 0x8c], eax
00408a09  8b84241a040000         mov      eax, dword ptr [esp + 0x41a]
00408a10  bb911b0000             mov      ebx, 0x1b91
00408a15  c1f810                 sar      eax, 0x10
00408a18  8b94248c000000         mov      edx, dword ptr [esp + 0x8c]
00408a1f  89842498010000         mov      dword ptr [esp + 0x198], eax
00408a26  e81c280500             call     0x45b247 ; PasteBobCmp
00408a2b  b901000000             mov      ecx, 1
00408a30  bb781b0000             mov      ebx, 0x1b78
00408a35  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
00408a3c  8b842498000000         mov      eax, dword ptr [esp + 0x98]
00408a43  e868320500             call     0x45bcb0 ; PasteGrisCmp
00408a48  b901000000             mov      ecx, 1
00408a4d  bb891b0000             mov      ebx, 0x1b89
00408a52  8b942494000000         mov      edx, dword ptr [esp + 0x94]
00408a59  8b44247c               mov      eax, dword ptr [esp + 0x7c]
00408a5d  e84e320500             call     0x45bcb0 ; PasteGrisCmp
00408a62  b901000000             mov      ecx, 1
00408a67  bb791b0000             mov      ebx, 0x1b79
00408a6c  8b542458               mov      edx, dword ptr [esp + 0x58]
00408a70  8b442454               mov      eax, dword ptr [esp + 0x54]
00408a74  e837320500             call     0x45bcb0 ; PasteGrisCmp
00408a79  b901000000             mov      ecx, 1
00408a7e  bb811b0000             mov      ebx, 0x1b81
00408a83  8b9424c0000000         mov      edx, dword ptr [esp + 0xc0]
00408a8a  8b8424b8010000         mov      eax, dword ptr [esp + 0x1b8]
00408a91  e81a320500             call     0x45bcb0 ; PasteGrisCmp
00408a96  b901000000             mov      ecx, 1
00408a9b  bb911b0000             mov      ebx, 0x1b91
00408aa0  8b94248c000000         mov      edx, dword ptr [esp + 0x8c]
00408aa7  8b842498010000         mov      eax, dword ptr [esp + 0x198]
00408aae  e8fd310500             call     0x45bcb0 ; PasteGrisCmp
00408ab3  31c0                   xor      eax, eax
00408ab5  668b4506               mov      ax, word ptr [ebp + 6]
00408ab9  85c0                   test     eax, eax
00408abb  0f8e81680000           jle      0x40f342
00408ac1  6a02                   push     2
00408ac3  e91a4b0000             jmp      0x40d5e2 ;
00408ac8  31c0                   xor      eax, eax
00408aca  668b0d26875000         mov      cx, word ptr [0x508726]
00408ad1  6689d0                 mov      ax, dx
00408ad4  668b1524875000         mov      dx, word ptr [0x508724]
00408adb  c1e105                 shl      ecx, 5
00408ade  c1e205                 shl      edx, 5
00408ae1  49                     dec      ecx
00408ae2  4a                     dec      edx
00408ae3  83f864                 cmp      eax, 0x64
00408ae6  0f8d83000000           jge      0x408b6f
00408aec  89942448020000         mov      dword ptr [esp + 0x248], edx
00408af3  ba64000000             mov      edx, 0x64
00408af8  29c2                   sub      edx, eax
00408afa  89d5                   mov      ebp, edx
00408afc  c1e503                 shl      ebp, 3
00408aff  01d5                   add      ebp, edx
00408b01  89ea                   mov      edx, ebp
00408b03  c1e204                 shl      edx, 4
00408b06  01ea                   add      edx, ebp
00408b08  bb64000000             mov      ebx, 0x64
00408b0d  89d0                   mov      eax, edx
00408b0f  c1fa1f                 sar      edx, 0x1f
00408b12  f7fb                   idiv     ebx
00408b14  0fbfd7                 movsx    edx, di
00408b17  01d0                   add      eax, edx
00408b19  89c2                   mov      edx, eax
00408b1b  0fbfc6                 movsx    eax, si
00408b1e  89b42448040000         mov      dword ptr [esp + 0x448], esi
00408b25  85c0                   test     eax, eax
00408b27  7d09                   jge      0x408b32
00408b29  31c0                   xor      eax, eax
00408b2b  89842448040000         mov      dword ptr [esp + 0x448], eax
00408b32  0fbfc2                 movsx    eax, dx
00408b35  85c0                   test     eax, eax
00408b37  7d02                   jge      0x408b3b
00408b39  31d2                   xor      edx, edx
00408b3b  31db                   xor      ebx, ebx
00408b3d  81e1ffff0000           and      ecx, 0xffff
00408b43  668b9c2448020000       mov      bx, word ptr [esp + 0x248]
00408b4b  31c0                   xor      eax, eax
00408b4d  81e2ffff0000           and      edx, 0xffff
00408b53  668b842448040000       mov      ax, word ptr [esp + 0x448]
00408b5b  e8b9690000             call     0x40f519 ; SetClipping
00408b60  b901000000             mov      ecx, 1
00408b65  bb771b0000             mov      ebx, 0x1b77
00408b6a  e9a3f8ffff             jmp      0x408412 ;
00408b6f  8994243c030000         mov      dword ptr [esp + 0x33c], edx
00408b76  83e864                 sub      eax, 0x64
00408b79  ba64000000             mov      edx, 0x64
00408b7e  29c2                   sub      edx, eax
00408b80  89d5                   mov      ebp, edx
00408b82  c1e503                 shl      ebp, 3
00408b85  01d5                   add      ebp, edx
00408b87  89ea                   mov      edx, ebp
00408b89  c1e204                 shl      edx, 4
00408b8c  01ea                   add      edx, ebp
00408b8e  bb64000000             mov      ebx, 0x64
00408b93  89d0                   mov      eax, edx
00408b95  c1fa1f                 sar      edx, 0x1f
00408b98  f7fb                   idiv     ebx
00408b9a  0fbfd7                 movsx    edx, di
00408b9d  01d0                   add      eax, edx
00408b9f  31d2                   xor      edx, edx
00408ba1  668b1526875000         mov      dx, word ptr [0x508726]
00408ba8  898c243c020000         mov      dword ptr [esp + 0x23c], ecx
00408baf  c1e205                 shl      edx, 5
00408bb2  0fbfd8                 movsx    ebx, ax
00408bb5  4a                     dec      edx
00408bb6  6689b42490040000       mov      word ptr [esp + 0x490], si
00408bbe  39d3                   cmp      ebx, edx
00408bc0  7e02                   jle      0x408bc4
00408bc2  89c8                   mov      eax, ecx
00408bc4  31c9                   xor      ecx, ecx
00408bc6  31db                   xor      ebx, ebx
00408bc8  31d2                   xor      edx, edx
00408bca  668b9c243c030000       mov      bx, word ptr [esp + 0x33c]
00408bd2  6689c1                 mov      cx, ax
00408bd5  31c0                   xor      eax, eax
00408bd7  e83d690000             call     0x40f519 ; SetClipping
00408bdc  0fbfc7                 movsx    eax, di
00408bdf  b901000000             mov      ecx, 1
00408be4  89442454               mov      dword ptr [esp + 0x54], eax
00408be8  bb771b0000             mov      ebx, 0x1b77
00408bed  8b542454               mov      edx, dword ptr [esp + 0x54]
00408bf1  0fbfc6                 movsx    eax, si
00408bf4  e84e260500             call     0x45b247 ; PasteBobCmp
00408bf9  31c0                   xor      eax, eax
00408bfb  668b8424d8010000       mov      ax, word ptr [esp + 0x1d8]
00408c03  ba64000000             mov      edx, 0x64
00408c08  83e864                 sub      eax, 0x64
00408c0b  29c2                   sub      edx, eax
00408c0d  89d5                   mov      ebp, edx
00408c0f  c1e503                 shl      ebp, 3
00408c12  01d5                   add      ebp, edx
00408c14  89ea                   mov      edx, ebp
00408c16  c1e204                 shl      edx, 4
00408c19  01ea                   add      edx, ebp
00408c1b  bb64000000             mov      ebx, 0x64
00408c20  89d0                   mov      eax, edx
00408c22  c1fa1f                 sar      edx, 0x1f
00408c25  f7fb                   idiv     ebx
00408c27  03442454               add      eax, dword ptr [esp + 0x54]
00408c2b  8b94248e040000         mov      edx, dword ptr [esp + 0x48e]
00408c32  c1fa10                 sar      edx, 0x10
00408c35  85d2                   test     edx, edx
00408c37  7d0a                   jge      0x408c43
00408c39  31db                   xor      ebx, ebx
00408c3b  66899c2490040000       mov      word ptr [esp + 0x490], bx
00408c43  0fbfd0                 movsx    edx, ax
00408c46  85d2                   test     edx, edx
00408c48  7d02                   jge      0x408c4c
00408c4a  31c0                   xor      eax, eax
00408c4c  31c9                   xor      ecx, ecx
00408c4e  31db                   xor      ebx, ebx
00408c50  31d2                   xor      edx, edx
00408c52  668b8c243c020000       mov      cx, word ptr [esp + 0x23c]
00408c5a  6689c2                 mov      dx, ax
00408c5d  31c0                   xor      eax, eax
00408c5f  668b9c243c030000       mov      bx, word ptr [esp + 0x33c]
00408c67  668b842490040000       mov      ax, word ptr [esp + 0x490]
00408c6f  0fbfef                 movsx    ebp, di
00408c72  e8a2680000             call     0x40f519 ; SetClipping
00408c77  b901000000             mov      ecx, 1
00408c7c  bb781b0000             mov      ebx, 0x1b78
00408c81  0fbfc6                 movsx    eax, si
00408c84  89ea                   mov      edx, ebp
00408c86  89842444010000         mov      dword ptr [esp + 0x144], eax
00408c8d  e8b5250500             call     0x45b247 ; PasteBobCmp
00408c92  89f8                   mov      eax, edi
00408c94  0505000000             add      eax, 5
00408c99  98                     cwde
00408c9a  8944242c               mov      dword ptr [esp + 0x2c], eax
00408c9e  89f0                   mov      eax, esi
00408ca0  b901000000             mov      ecx, 1
00408ca5  054a000000             add      eax, 0x4a
00408caa  bb891b0000             mov      ebx, 0x1b89
00408caf  98                     cwde
00408cb0  8b54242c               mov      edx, dword ptr [esp + 0x2c]
00408cb4  89842480010000         mov      dword ptr [esp + 0x180], eax
00408cbb  e887250500             call     0x45b247 ; PasteBobCmp
00408cc0  89f8                   mov      eax, edi
00408cc2  055f000000             add      eax, 0x5f
00408cc7  98                     cwde
00408cc8  89842488000000         mov      dword ptr [esp + 0x88], eax
00408ccf  89f0                   mov      eax, esi
00408cd1  b901000000             mov      ecx, 1
00408cd6  0559000000             add      eax, 0x59
00408cdb  bb791b0000             mov      ebx, 0x1b79
00408ce0  98                     cwde
00408ce1  8b942488000000         mov      edx, dword ptr [esp + 0x88]
00408ce8  898424fc000000         mov      dword ptr [esp + 0xfc], eax
00408cef  e853250500             call     0x45b247 ; PasteBobCmp
00408cf4  89f8                   mov      eax, edi
00408cf6  0583000000             add      eax, 0x83
00408cfb  98                     cwde
00408cfc  89842448010000         mov      dword ptr [esp + 0x148], eax
00408d03  89f0                   mov      eax, esi
00408d05  b901000000             mov      ecx, 1
00408d0a  0597000000             add      eax, 0x97
00408d0f  bb811b0000             mov      ebx, 0x1b81
00408d14  98                     cwde
00408d15  8b942448010000         mov      edx, dword ptr [esp + 0x148]
00408d1c  898424c8000000         mov      dword ptr [esp + 0xc8], eax
00408d23  e81f250500             call     0x45b247 ; PasteBobCmp
00408d28  89f8                   mov      eax, edi
00408d2a  053f000000             add      eax, 0x3f
00408d2f  98                     cwde
00408d30  89842494010000         mov      dword ptr [esp + 0x194], eax
00408d37  89f0                   mov      eax, esi
00408d39  b901000000             mov      ecx, 1
00408d3e  0512000000             add      eax, 0x12
00408d43  bb911b0000             mov      ebx, 0x1b91
00408d48  98                     cwde
00408d49  8b942494010000         mov      edx, dword ptr [esp + 0x194]
00408d50  898424b8000000         mov      dword ptr [esp + 0xb8], eax
00408d57  e8eb240500             call     0x45b247 ; PasteBobCmp
00408d5c  31c0                   xor      eax, eax
00408d5e  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408d66  e84d180100             call     0x41a5b8 ; BatimentEstHabiter
00408d6b  84c0                   test     al, al
00408d6d  0f85cf650000           jne      0x40f342
00408d73  b901000000             mov      ecx, 1
00408d78  bb781b0000             mov      ebx, 0x1b78
00408d7d  8b842444010000         mov      eax, dword ptr [esp + 0x144]
00408d84  89ea                   mov      edx, ebp
00408d86  e8252f0500             call     0x45bcb0 ; PasteGrisCmp
00408d8b  b901000000             mov      ecx, 1
00408d90  bb891b0000             mov      ebx, 0x1b89
00408d95  8b54242c               mov      edx, dword ptr [esp + 0x2c]
00408d99  8b842480010000         mov      eax, dword ptr [esp + 0x180]
00408da0  e80b2f0500             call     0x45bcb0 ; PasteGrisCmp
00408da5  b901000000             mov      ecx, 1
00408daa  bb791b0000             mov      ebx, 0x1b79
00408daf  8b942488000000         mov      edx, dword ptr [esp + 0x88]
00408db6  8b8424fc000000         mov      eax, dword ptr [esp + 0xfc]
00408dbd  e8ee2e0500             call     0x45bcb0 ; PasteGrisCmp
00408dc2  b901000000             mov      ecx, 1
00408dc7  bb811b0000             mov      ebx, 0x1b81
00408dcc  8b942448010000         mov      edx, dword ptr [esp + 0x148]
00408dd3  8b8424c8000000         mov      eax, dword ptr [esp + 0xc8]
00408dda  e8d12e0500             call     0x45bcb0 ; PasteGrisCmp
00408ddf  b901000000             mov      ecx, 1
00408de4  bb911b0000             mov      ebx, 0x1b91
00408de9  8b942494010000         mov      edx, dword ptr [esp + 0x194]
00408df0  8b8424b8000000         mov      eax, dword ptr [esp + 0xb8]
00408df7  e971f7ffff             jmp      0x40856d ;
00408dfc  31d2                   xor      edx, edx
00408dfe  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
00408e03  668b1424               mov      dx, word ptr [esp]
00408e07  f644500180             test     byte ptr [eax + edx*2 + 1], 0x80
00408e0c  7423                   je       0x408e31
00408e0e  31c0                   xor      eax, eax
00408e10  6689d0                 mov      ax, dx
00408e13  8d1400                 lea      edx, [eax + eax]
00408e16  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
00408e1b  668b0402               mov      ax, word ptr [edx + eax]
00408e1f  25e07f0000             and      eax, 0x7fe0
00408e24  89c3                   mov      ebx, eax
00408e26  81e3ffff0000           and      ebx, 0xffff
00408e2c  c1fb05                 sar      ebx, 5
00408e2f  eb05                   jmp      0x408e36 ;
00408e31  bbffff0000             mov      ebx, 0xffff
00408e36  31c0                   xor      eax, eax
00408e38  6689d8                 mov      ax, bx
00408e3b  899c2410020000         mov      dword ptr [esp + 0x210], ebx
00408e42  3dffff0000             cmp      eax, 0xffff
00408e47  0f8444660000           je       0x40f491
00408e4d  89c5                   mov      ebp, eax
00408e4f  c1e504                 shl      ebp, 4
00408e52  01c5                   add      ebp, eax
00408e54  8b742408               mov      esi, dword ptr [esp + 8]
00408e58  c1e502                 shl      ebp, 2
00408e5b  8b7c2404               mov      edi, dword ptr [esp + 4]
00408e5f  01c5                   add      ebp, eax
00408e61  e87f1a0100             call     0x41a8e5 ; BatimentGetEtat
00408e66  c1e502                 shl      ebp, 2
00408e69  89c2                   mov      edx, eax
00408e6b  8984248c030000         mov      dword ptr [esp + 0x38c], eax
00408e72  81c5c8a04900           add      ebp, 0x49a0c8
00408e78  31c0                   xor      eax, eax
00408e7a  83ee1b                 sub      esi, 0x1b
00408e7d  8a4505                 mov      al, byte ptr [ebp + 5]
00408e80  83ef5d                 sub      edi, 0x5d
00408e83  83f805                 cmp      eax, 5
00408e86  740e                   je       0x408e96
00408e88  83f803                 cmp      eax, 3
00408e8b  7409                   je       0x408e96
00408e8d  83f804                 cmp      eax, 4
00408e90  0f8578020000           jne      0x40910e
00408e96  31c0                   xor      eax, eax
00408e98  8a4505                 mov      al, byte ptr [ebp + 5]
00408e9b  83f803                 cmp      eax, 3
00408e9e  0f8513010000           jne      0x408fb7
00408ea4  31c0                   xor      eax, eax
00408ea6  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408eae  e805170100             call     0x41a5b8 ; BatimentEstHabiter
00408eb3  84c0                   test     al, al
00408eb5  0f85fc000000           jne      0x408fb7
00408ebb  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
00408ec1  31d2                   xor      edx, edx
00408ec3  88ca                   mov      dl, cl
00408ec5  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00408ecb  81e2ff000000           and      edx, 0xff
00408ed1  bb03000000             mov      ebx, 3
00408ed6  89d0                   mov      eax, edx
00408ed8  c1fa1f                 sar      edx, 0x1f
00408edb  f7fb                   idiv     ebx
00408edd  0fbfdf                 movsx    ebx, di
00408ee0  01da                   add      edx, ebx
00408ee2  81c291000000           add      edx, 0x91
00408ee8  fec1                   inc      cl
00408eea  6689942474030000       mov      word ptr [esp + 0x374], dx
00408ef2  31d2                   xor      edx, edx
00408ef4  88ca                   mov      dl, cl
00408ef6  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00408efc  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00408f02  81e2ff000000           and      edx, 0xff
00408f08  bf03000000             mov      edi, 3
00408f0d  89d0                   mov      eax, edx
00408f0f  c1fa1f                 sar      edx, 0x1f
00408f12  f7ff                   idiv     edi
00408f14  fec1                   inc      cl
00408f16  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00408f1c  8d0413                 lea      eax, [ebx + edx]
00408f1f  31ff                   xor      edi, edi
00408f21  05c8000000             add      eax, 0xc8
00408f26  668bbd84000000         mov      di, word ptr [ebp + 0x84]
00408f2d  29f8                   sub      eax, edi
00408f2f  89c7                   mov      edi, eax
00408f31  98                     cwde
00408f32  85c0                   test     eax, eax
00408f34  7d02                   jge      0x408f38
00408f36  31ff                   xor      edi, edi
00408f38  31c0                   xor      eax, eax
00408f3a  66a126875000           mov      ax, word ptr [0x508726]
00408f40  8b942472030000         mov      edx, dword ptr [esp + 0x372]
00408f47  c1e005                 shl      eax, 5
00408f4a  c1fa10                 sar      edx, 0x10
00408f4d  48                     dec      eax
00408f4e  39c2                   cmp      edx, eax
00408f50  7e12                   jle      0x408f64
00408f52  66a126875000           mov      ax, word ptr [0x508726]
00408f58  c1e005                 shl      eax, 5
00408f5b  48                     dec      eax
00408f5c  6689842474030000       mov      word ptr [esp + 0x374], ax
00408f64  66a124875000           mov      ax, word ptr [0x508724]
00408f6a  31c9                   xor      ecx, ecx
00408f6c  31db                   xor      ebx, ebx
00408f6e  31d2                   xor      edx, edx
00408f70  668b8c2474030000       mov      cx, word ptr [esp + 0x374]
00408f78  c1e005                 shl      eax, 5
00408f7b  6689fa                 mov      dx, di
00408f7e  6689c3                 mov      bx, ax
00408f81  31c0                   xor      eax, eax
00408f83  e891650000             call     0x40f519 ; SetClipping
00408f88  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00408f8e  31d2                   xor      edx, edx
00408f90  88da                   mov      dl, bl
00408f92  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00408f98  81e2ff000000           and      edx, 0xff
00408f9e  b903000000             mov      ecx, 3
00408fa3  89d0                   mov      eax, edx
00408fa5  c1fa1f                 sar      edx, 0x1f
00408fa8  f7f9                   idiv     ecx
00408faa  fec3                   inc      bl
00408fac  0fbff6                 movsx    esi, si
00408faf  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00408fb5  01d6                   add      esi, edx
00408fb7  89f2                   mov      edx, esi
00408fb9  83c20d                 add      edx, 0xd
00408fbc  31c0                   xor      eax, eax
00408fbe  6689942410040000       mov      word ptr [esp + 0x410], dx
00408fc6  89fa                   mov      edx, edi
00408fc8  668b842410020000       mov      ax, word ptr [esp + 0x210]
00408fd0  83c217                 add      edx, 0x17
00408fd3  e8e0150100             call     0x41a5b8 ; BatimentEstHabiter
00408fd8  6689942420030000       mov      word ptr [esp + 0x320], dx
00408fe0  84c0                   test     al, al
00408fe2  0f848a000000           je       0x409072
00408fe8  b901000000             mov      ecx, 1
00408fed  31c0                   xor      eax, eax
00408fef  bba41b0000             mov      ebx, 0x1ba4
00408ff4  8a4504                 mov      al, byte ptr [ebp + 4]
00408ff7  0fbfd7                 movsx    edx, di
00408ffa  50                     push     eax
00408ffb  0fbfc6                 movsx    eax, si
00408ffe  e852340500             call     0x45c455 ; PastePlayerCmp
00409003  8b0c24                 mov      ecx, dword ptr [esp]
00409006  66a1808f5000           mov      ax, word ptr [0x508f80]
0040900c  01c8                   add      eax, ecx
0040900e  30e4                   xor      ah, ah
00409010  8b94241e030000         mov      edx, dword ptr [esp + 0x31e]
00409017  2407                   and      al, 7
00409019  31db                   xor      ebx, ebx
0040901b  05ad1b0000             add      eax, 0x1bad
00409020  c1fa10                 sar      edx, 0x10
00409023  6689c3                 mov      bx, ax
00409026  8b84240e040000         mov      eax, dword ptr [esp + 0x40e]
0040902d  b901000000             mov      ecx, 1
00409032  c1f810                 sar      eax, 0x10
00409035  e80d220500             call     0x45b247 ; PasteBobCmp
0040903a  8b1424                 mov      edx, dword ptr [esp]
0040903d  66a1808f5000           mov      ax, word ptr [0x508f80]
00409043  01d0                   add      eax, edx
00409045  30e4                   xor      ah, ah
00409047  2407                   and      al, 7
00409049  31db                   xor      ebx, ebx
0040904b  05a51b0000             add      eax, 0x1ba5
00409050  6689c3                 mov      bx, ax
00409053  89f8                   mov      eax, edi
00409055  0509000000             add      eax, 9
0040905a  0fbfd0                 movsx    edx, ax
0040905d  89f0                   mov      eax, esi
0040905f  83e824                 sub      eax, 0x24
00409062  b901000000             mov      ecx, 1
00409067  98                     cwde
00409068  e8b6290500             call     0x45ba23 ; PasteEclairCmp
0040906d  e987000000             jmp      0x4090f9 ;
00409072  b901000000             mov      ecx, 1
00409077  0fbfc7                 movsx    eax, di
0040907a  bba41b0000             mov      ebx, 0x1ba4
0040907f  89842494000000         mov      dword ptr [esp + 0x94], eax
00409086  0fbfc6                 movsx    eax, si
00409089  8b942494000000         mov      edx, dword ptr [esp + 0x94]
00409090  8944247c               mov      dword ptr [esp + 0x7c], eax
00409094  e8ae210500             call     0x45b247 ; PasteBobCmp
00409099  8b84241e030000         mov      eax, dword ptr [esp + 0x31e]
004090a0  c1f810                 sar      eax, 0x10
004090a3  b901000000             mov      ecx, 1
004090a8  89442458               mov      dword ptr [esp + 0x58], eax
004090ac  8b84240e040000         mov      eax, dword ptr [esp + 0x40e]
004090b3  bbad1b0000             mov      ebx, 0x1bad
004090b8  c1f810                 sar      eax, 0x10
004090bb  8b542458               mov      edx, dword ptr [esp + 0x58]
004090bf  89442454               mov      dword ptr [esp + 0x54], eax
004090c3  e87f210500             call     0x45b247 ; PasteBobCmp
004090c8  b901000000             mov      ecx, 1
004090cd  bba41b0000             mov      ebx, 0x1ba4
004090d2  8b942494000000         mov      edx, dword ptr [esp + 0x94]
004090d9  8b44247c               mov      eax, dword ptr [esp + 0x7c]
004090dd  e8ce2b0500             call     0x45bcb0 ; PasteGrisCmp
004090e2  b901000000             mov      ecx, 1
004090e7  bbad1b0000             mov      ebx, 0x1bad
004090ec  8b542458               mov      edx, dword ptr [esp + 0x58]
004090f0  8b442454               mov      eax, dword ptr [esp + 0x54]
004090f4  e8b72b0500             call     0x45bcb0 ; PasteGrisCmp
004090f9  31c0                   xor      eax, eax
004090fb  668b4506               mov      ax, word ptr [ebp + 6]
004090ff  85c0                   test     eax, eax
00409101  0f8e3b620000           jle      0x40f342
00409107  6a00                   push     0
00409109  e9d4440000             jmp      0x40d5e2 ;
0040910e  31c0                   xor      eax, eax
00409110  668b0d26875000         mov      cx, word ptr [0x508726]
00409117  6689d0                 mov      ax, dx
0040911a  668b1524875000         mov      dx, word ptr [0x508724]
00409121  c1e105                 shl      ecx, 5
00409124  c1e205                 shl      edx, 5
00409127  49                     dec      ecx
00409128  4a                     dec      edx
00409129  83f864                 cmp      eax, 0x64
0040912c  0f8d81000000           jge      0x4091b3
00409132  89942420020000         mov      dword ptr [esp + 0x220], edx
00409139  ba64000000             mov      edx, 0x64
0040913e  29c2                   sub      edx, eax
00409140  89d0                   mov      eax, edx
00409142  c1e003                 shl      eax, 3
00409145  01d0                   add      eax, edx
00409147  c1e004                 shl      eax, 4
0040914a  01c2                   add      edx, eax
0040914c  bb64000000             mov      ebx, 0x64
00409151  89d0                   mov      eax, edx
00409153  c1fa1f                 sar      edx, 0x1f
00409156  f7fb                   idiv     ebx
00409158  0fbfd7                 movsx    edx, di
0040915b  01d0                   add      eax, edx
0040915d  89c2                   mov      edx, eax
0040915f  0fbfc6                 movsx    eax, si
00409162  89b42480040000         mov      dword ptr [esp + 0x480], esi
00409169  85c0                   test     eax, eax
0040916b  7d09                   jge      0x409176
0040916d  31db                   xor      ebx, ebx
0040916f  899c2480040000         mov      dword ptr [esp + 0x480], ebx
00409176  0fbfc2                 movsx    eax, dx
00409179  85c0                   test     eax, eax
0040917b  7d02                   jge      0x40917f
0040917d  31d2                   xor      edx, edx
0040917f  31db                   xor      ebx, ebx
00409181  81e1ffff0000           and      ecx, 0xffff
00409187  668b9c2420020000       mov      bx, word ptr [esp + 0x220]
0040918f  31c0                   xor      eax, eax
00409191  81e2ffff0000           and      edx, 0xffff
00409197  668b842480040000       mov      ax, word ptr [esp + 0x480]
0040919f  e875630000             call     0x40f519 ; SetClipping
004091a4  b901000000             mov      ecx, 1
004091a9  bba31b0000             mov      ebx, 0x1ba3
004091ae  e95ff2ffff             jmp      0x408412 ;
004091b3  899424fc010000         mov      dword ptr [esp + 0x1fc], edx
004091ba  83e864                 sub      eax, 0x64
004091bd  ba64000000             mov      edx, 0x64
004091c2  29c2                   sub      edx, eax
004091c4  89d0                   mov      eax, edx
004091c6  c1e003                 shl      eax, 3
004091c9  01d0                   add      eax, edx
004091cb  c1e004                 shl      eax, 4
004091ce  01c2                   add      edx, eax
004091d0  bb64000000             mov      ebx, 0x64
004091d5  89d0                   mov      eax, edx
004091d7  c1fa1f                 sar      edx, 0x1f
004091da  f7fb                   idiv     ebx
004091dc  0fbfd7                 movsx    edx, di
004091df  01d0                   add      eax, edx
004091e1  31d2                   xor      edx, edx
004091e3  668b1526875000         mov      dx, word ptr [0x508726]
004091ea  898c24b4020000         mov      dword ptr [esp + 0x2b4], ecx
004091f1  c1e205                 shl      edx, 5
004091f4  0fbfd8                 movsx    ebx, ax
004091f7  4a                     dec      edx
004091f8  6689b42464020000       mov      word ptr [esp + 0x264], si
00409200  39d3                   cmp      ebx, edx
00409202  7e02                   jle      0x409206
00409204  89c8                   mov      eax, ecx
00409206  31c9                   xor      ecx, ecx
00409208  31db                   xor      ebx, ebx
0040920a  31d2                   xor      edx, edx
0040920c  668b9c24fc010000       mov      bx, word ptr [esp + 0x1fc]
00409214  6689c1                 mov      cx, ax
00409217  31c0                   xor      eax, eax
00409219  e8fb620000             call     0x40f519 ; SetClipping
0040921e  0fbfc7                 movsx    eax, di
00409221  b901000000             mov      ecx, 1
00409226  89442454               mov      dword ptr [esp + 0x54], eax
0040922a  bba31b0000             mov      ebx, 0x1ba3
0040922f  8b542454               mov      edx, dword ptr [esp + 0x54]
00409233  0fbfc6                 movsx    eax, si
00409236  e80c200500             call     0x45b247 ; PasteBobCmp
0040923b  31c0                   xor      eax, eax
0040923d  668b84248c030000       mov      ax, word ptr [esp + 0x38c]
00409245  ba64000000             mov      edx, 0x64
0040924a  83e864                 sub      eax, 0x64
0040924d  29c2                   sub      edx, eax
0040924f  89d0                   mov      eax, edx
00409251  c1e203                 shl      edx, 3
00409254  01c2                   add      edx, eax
00409256  c1e204                 shl      edx, 4
00409259  01c2                   add      edx, eax
0040925b  bb64000000             mov      ebx, 0x64
00409260  89d0                   mov      eax, edx
00409262  c1fa1f                 sar      edx, 0x1f
00409265  f7fb                   idiv     ebx
00409267  8b942462020000         mov      edx, dword ptr [esp + 0x262]
0040926e  8b6c2454               mov      ebp, dword ptr [esp + 0x54]
00409272  c1fa10                 sar      edx, 0x10
00409275  01e8                   add      eax, ebp
00409277  85d2                   test     edx, edx
00409279  7d0a                   jge      0x409285
0040927b  31d2                   xor      edx, edx
0040927d  6689942464020000       mov      word ptr [esp + 0x264], dx
00409285  0fbfd0                 movsx    edx, ax
00409288  85d2                   test     edx, edx
0040928a  7d02                   jge      0x40928e
0040928c  31c0                   xor      eax, eax
0040928e  31c9                   xor      ecx, ecx
00409290  31db                   xor      ebx, ebx
00409292  31d2                   xor      edx, edx
00409294  668b8c24b4020000       mov      cx, word ptr [esp + 0x2b4]
0040929c  6689c2                 mov      dx, ax
0040929f  31c0                   xor      eax, eax
004092a1  668b9c24fc010000       mov      bx, word ptr [esp + 0x1fc]
004092a9  668b842464020000       mov      ax, word ptr [esp + 0x264]
004092b1  e863620000             call     0x40f519 ; SetClipping
004092b6  b901000000             mov      ecx, 1
004092bb  0fbfc7                 movsx    eax, di
004092be  bba41b0000             mov      ebx, 0x1ba4
004092c3  898424b4010000         mov      dword ptr [esp + 0x1b4], eax
004092ca  0fbfc6                 movsx    eax, si
004092cd  8b9424b4010000         mov      edx, dword ptr [esp + 0x1b4]
004092d4  89842430010000         mov      dword ptr [esp + 0x130], eax
004092db  e8671f0500             call     0x45b247 ; PasteBobCmp
004092e0  89f8                   mov      eax, edi
004092e2  0517000000             add      eax, 0x17
004092e7  98                     cwde
004092e8  898424e4000000         mov      dword ptr [esp + 0xe4], eax
004092ef  89f0                   mov      eax, esi
004092f1  b901000000             mov      ecx, 1
004092f6  050d000000             add      eax, 0xd
004092fb  bbad1b0000             mov      ebx, 0x1bad
00409300  0fbfe8                 movsx    ebp, ax
00409303  8b9424e4000000         mov      edx, dword ptr [esp + 0xe4]
0040930a  89e8                   mov      eax, ebp
0040930c  e8361f0500             call     0x45b247 ; PasteBobCmp
00409311  31c0                   xor      eax, eax
00409313  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040931b  e898120100             call     0x41a5b8 ; BatimentEstHabiter
00409320  84c0                   test     al, al
00409322  0f851a600000           jne      0x40f342
00409328  b901000000             mov      ecx, 1
0040932d  bba41b0000             mov      ebx, 0x1ba4
00409332  8b9424b4010000         mov      edx, dword ptr [esp + 0x1b4]
00409339  8b842430010000         mov      eax, dword ptr [esp + 0x130]
00409340  e86b290500             call     0x45bcb0 ; PasteGrisCmp
00409345  b901000000             mov      ecx, 1
0040934a  bbad1b0000             mov      ebx, 0x1bad
0040934f  8b9424e4000000         mov      edx, dword ptr [esp + 0xe4]
00409356  89e8                   mov      eax, ebp
00409358  e910f2ffff             jmp      0x40856d ;
0040935d  31c0                   xor      eax, eax
0040935f  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
00409365  668b0424               mov      ax, word ptr [esp]
00409369  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
0040936e  7424                   je       0x409394
00409370  31c0                   xor      eax, eax
00409372  668b0424               mov      ax, word ptr [esp]
00409376  8d1400                 lea      edx, [eax + eax]
00409379  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040937e  668b0402               mov      ax, word ptr [edx + eax]
00409382  25e07f0000             and      eax, 0x7fe0
00409387  89c3                   mov      ebx, eax
00409389  81e3ffff0000           and      ebx, 0xffff
0040938f  c1fb05                 sar      ebx, 5
00409392  eb05                   jmp      0x409399 ;
00409394  bbffff0000             mov      ebx, 0xffff
00409399  31d2                   xor      edx, edx
0040939b  6689da                 mov      dx, bx
0040939e  899c2410020000         mov      dword ptr [esp + 0x210], ebx
004093a5  81faffff0000           cmp      edx, 0xffff
004093ab  0f84e0600000           je       0x40f491
004093b1  89d5                   mov      ebp, edx
004093b3  8b742408               mov      esi, dword ptr [esp + 8]
004093b7  c1e504                 shl      ebp, 4
004093ba  8b7c2404               mov      edi, dword ptr [esp + 4]
004093be  01d5                   add      ebp, edx
004093c0  89d0                   mov      eax, edx
004093c2  c1e502                 shl      ebp, 2
004093c5  e81b150100             call     0x41a8e5 ; BatimentGetEtat
004093ca  01d5                   add      ebp, edx
004093cc  898424bc030000         mov      dword ptr [esp + 0x3bc], eax
004093d3  c1e502                 shl      ebp, 2
004093d6  89c2                   mov      edx, eax
004093d8  81c5c8a04900           add      ebp, 0x49a0c8
004093de  31c0                   xor      eax, eax
004093e0  83ee39                 sub      esi, 0x39
004093e3  8a4505                 mov      al, byte ptr [ebp + 5]
004093e6  83ef2f                 sub      edi, 0x2f
004093e9  83f805                 cmp      eax, 5
004093ec  740e                   je       0x4093fc
004093ee  83f803                 cmp      eax, 3
004093f1  7409                   je       0x4093fc
004093f3  83f804                 cmp      eax, 4
004093f6  0f85aa050000           jne      0x4099a6
004093fc  31c0                   xor      eax, eax
004093fe  8a4505                 mov      al, byte ptr [ebp + 5]
00409401  83f803                 cmp      eax, 3
00409404  0f8512010000           jne      0x40951c
0040940a  31c0                   xor      eax, eax
0040940c  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409414  e89f110100             call     0x41a5b8 ; BatimentEstHabiter
00409419  84c0                   test     al, al
0040941b  0f85fb000000           jne      0x40951c
00409421  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00409427  31d2                   xor      edx, edx
00409429  88da                   mov      dl, bl
0040942b  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00409431  81e2ff000000           and      edx, 0xff
00409437  b903000000             mov      ecx, 3
0040943c  89d0                   mov      eax, edx
0040943e  c1fa1f                 sar      edx, 0x1f
00409441  f7f9                   idiv     ecx
00409443  0fbfcf                 movsx    ecx, di
00409446  01ca                   add      edx, ecx
00409448  83c261                 add      edx, 0x61
0040944b  fec3                   inc      bl
0040944d  6689942414030000       mov      word ptr [esp + 0x314], dx
00409455  31d2                   xor      edx, edx
00409457  88da                   mov      dl, bl
00409459  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040945f  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00409465  81e2ff000000           and      edx, 0xff
0040946b  bf03000000             mov      edi, 3
00409470  89d0                   mov      eax, edx
00409472  c1fa1f                 sar      edx, 0x1f
00409475  f7ff                   idiv     edi
00409477  fec3                   inc      bl
00409479  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040947f  01ca                   add      edx, ecx
00409481  31c0                   xor      eax, eax
00409483  81c2c8000000           add      edx, 0xc8
00409489  668b8584000000         mov      ax, word ptr [ebp + 0x84]
00409490  29c2                   sub      edx, eax
00409492  0fbfc2                 movsx    eax, dx
00409495  89d7                   mov      edi, edx
00409497  85c0                   test     eax, eax
00409499  7d02                   jge      0x40949d
0040949b  31d7                   xor      edi, edx
0040949d  31c0                   xor      eax, eax
0040949f  66a126875000           mov      ax, word ptr [0x508726]
004094a5  8b942412030000         mov      edx, dword ptr [esp + 0x312]
004094ac  c1e005                 shl      eax, 5
004094af  c1fa10                 sar      edx, 0x10
004094b2  48                     dec      eax
004094b3  39c2                   cmp      edx, eax
004094b5  7e12                   jle      0x4094c9
004094b7  66a126875000           mov      ax, word ptr [0x508726]
004094bd  c1e005                 shl      eax, 5
004094c0  48                     dec      eax
004094c1  6689842414030000       mov      word ptr [esp + 0x314], ax
004094c9  66a124875000           mov      ax, word ptr [0x508724]
004094cf  31c9                   xor      ecx, ecx
004094d1  31db                   xor      ebx, ebx
004094d3  31d2                   xor      edx, edx
004094d5  668b8c2414030000       mov      cx, word ptr [esp + 0x314]
004094dd  c1e005                 shl      eax, 5
004094e0  6689fa                 mov      dx, di
004094e3  6689c3                 mov      bx, ax
004094e6  31c0                   xor      eax, eax
004094e8  e82c600000             call     0x40f519 ; SetClipping
004094ed  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
004094f3  31d2                   xor      edx, edx
004094f5  88da                   mov      dl, bl
004094f7  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
004094fd  81e2ff000000           and      edx, 0xff
00409503  b903000000             mov      ecx, 3
00409508  89d0                   mov      eax, edx
0040950a  c1fa1f                 sar      edx, 0x1f
0040950d  f7f9                   idiv     ecx
0040950f  fec3                   inc      bl
00409511  0fbff6                 movsx    esi, si
00409514  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040951a  01d6                   add      esi, edx
0040951c  89f2                   mov      edx, esi
0040951e  83c20c                 add      edx, 0xc
00409521  668994247c020000       mov      word ptr [esp + 0x27c], dx
00409529  89fa                   mov      edx, edi
0040952b  83c22e                 add      edx, 0x2e
0040952e  6689942450020000       mov      word ptr [esp + 0x250], dx
00409536  89f2                   mov      edx, esi
00409538  83c23c                 add      edx, 0x3c
0040953b  668994244c030000       mov      word ptr [esp + 0x34c], dx
00409543  89fa                   mov      edx, edi
00409545  83c217                 add      edx, 0x17
00409548  668994243c040000       mov      word ptr [esp + 0x43c], dx
00409550  89f2                   mov      edx, esi
00409552  83c22b                 add      edx, 0x2b
00409555  6689942424040000       mov      word ptr [esp + 0x424], dx
0040955d  89f2                   mov      edx, esi
0040955f  83c203                 add      edx, 3
00409562  31c0                   xor      eax, eax
00409564  66899424f8030000       mov      word ptr [esp + 0x3f8], dx
0040956c  89fa                   mov      edx, edi
0040956e  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409576  83c20a                 add      edx, 0xa
00409579  e83a100100             call     0x41a5b8 ; BatimentEstHabiter
0040957e  66899424e4010000       mov      word ptr [esp + 0x1e4], dx
00409586  84c0                   test     al, al
00409588  0f84ec010000           je       0x40977a
0040958e  31c0                   xor      eax, eax
00409590  8a4504                 mov      al, byte ptr [ebp + 4]
00409593  50                     push     eax
00409594  0fbfc7                 movsx    eax, di
00409597  b901000000             mov      ecx, 1
0040959c  89442458               mov      dword ptr [esp + 0x58], eax
004095a0  bbb61b0000             mov      ebx, 0x1bb6
004095a5  8b542458               mov      edx, dword ptr [esp + 0x58]
004095a9  0fbfc6                 movsx    eax, si
004095ac  e8a42e0500             call     0x45c455 ; PastePlayerCmp
004095b1  8b1c24                 mov      ebx, dword ptr [esp]
004095b4  66a1808f5000           mov      ax, word ptr [0x508f80]
004095ba  01d8                   add      eax, ebx
004095bc  30e4                   xor      ah, ah
004095be  8b9424e2010000         mov      edx, dword ptr [esp + 0x1e2]
004095c5  2407                   and      al, 7
004095c7  31db                   xor      ebx, ebx
004095c9  05b71b0000             add      eax, 0x1bb7
004095ce  b901000000             mov      ecx, 1
004095d3  6689c3                 mov      bx, ax
004095d6  8b8424f6030000         mov      eax, dword ptr [esp + 0x3f6]
004095dd  c1fa10                 sar      edx, 0x10
004095e0  c1f810                 sar      eax, 0x10
004095e3  e85f1c0500             call     0x45b247 ; PasteBobCmp
004095e8  8b0c24                 mov      ecx, dword ptr [esp]
004095eb  66a1808f5000           mov      ax, word ptr [0x508f80]
004095f1  01c8                   add      eax, ecx
004095f3  30e4                   xor      ah, ah
004095f5  2407                   and      al, 7
004095f7  31db                   xor      ebx, ebx
004095f9  05bf1b0000             add      eax, 0x1bbf
004095fe  8b542454               mov      edx, dword ptr [esp + 0x54]
00409602  6689c3                 mov      bx, ax
00409605  8b842422040000         mov      eax, dword ptr [esp + 0x422]
0040960c  b901000000             mov      ecx, 1
00409611  c1f810                 sar      eax, 0x10
00409614  e82e1c0500             call     0x45b247 ; PasteBobCmp
00409619  8b1424                 mov      edx, dword ptr [esp]
0040961c  66a1808f5000           mov      ax, word ptr [0x508f80]
00409622  01d0                   add      eax, edx
00409624  30e4                   xor      ah, ah
00409626  b901000000             mov      ecx, 1
0040962b  2407                   and      al, 7
0040962d  31db                   xor      ebx, ebx
0040962f  05c71b0000             add      eax, 0x1bc7
00409634  8b94243a040000         mov      edx, dword ptr [esp + 0x43a]
0040963b  6689c3                 mov      bx, ax
0040963e  8b84244a030000         mov      eax, dword ptr [esp + 0x34a]
00409645  c1fa10                 sar      edx, 0x10
00409648  c1f810                 sar      eax, 0x10
0040964b  e8f71b0500             call     0x45b247 ; PasteBobCmp
00409650  807d7400               cmp      byte ptr [ebp + 0x74], 0
00409654  742e                   je       0x409684
00409656  8b1c24                 mov      ebx, dword ptr [esp]
00409659  66a1808f5000           mov      ax, word ptr [0x508f80]
0040965f  01d8                   add      eax, ebx
00409661  30e4                   xor      ah, ah
00409663  8b94244e020000         mov      edx, dword ptr [esp + 0x24e]
0040966a  2407                   and      al, 7
0040966c  31db                   xor      ebx, ebx
0040966e  05d71b0000             add      eax, 0x1bd7
00409673  b901000000             mov      ecx, 1
00409678  6689c3                 mov      bx, ax
0040967b  8b84247a020000         mov      eax, dword ptr [esp + 0x27a]
00409682  eb18                   jmp      0x40969c ;
00409684  8b94244e020000         mov      edx, dword ptr [esp + 0x24e]
0040968b  8b84247a020000         mov      eax, dword ptr [esp + 0x27a]
00409692  b901000000             mov      ecx, 1
00409697  bbd71b0000             mov      ebx, 0x1bd7
0040969c  c1fa10                 sar      edx, 0x10
0040969f  c1f810                 sar      eax, 0x10
004096a2  e8a01b0500             call     0x45b247 ; PasteBobCmp
004096a7  31d2                   xor      edx, edx
004096a9  8a5504                 mov      dl, byte ptr [ebp + 4]
004096ac  89d0                   mov      eax, edx
004096ae  c1e002                 shl      eax, 2
004096b1  29d0                   sub      eax, edx
004096b3  8a044530fb4d00         mov      al, byte ptr [eax*2 + 0x4dfb30]
004096ba  30e4                   xor      ah, ah
004096bc  31db                   xor      ebx, ebx
004096be  05df1b0000             add      eax, 0x1bdf
004096c3  6689c3                 mov      bx, ax
004096c6  89f8                   mov      eax, edi
004096c8  0510000000             add      eax, 0x10
004096cd  0fbfd0                 movsx    edx, ax
004096d0  89f0                   mov      eax, esi
004096d2  0515000000             add      eax, 0x15
004096d7  b901000000             mov      ecx, 1
004096dc  98                     cwde
004096dd  e8651b0500             call     0x45b247 ; PasteBobCmp
004096e2  31c0                   xor      eax, eax
004096e4  89f1                   mov      ecx, esi
004096e6  8a4576                 mov      al, byte ptr [ebp + 0x76]
004096e9  83c140                 add      ecx, 0x40
004096ec  83f808                 cmp      eax, 8
004096ef  7d15                   jge      0x409706
004096f1  30e4                   xor      ah, ah
004096f3  31db                   xor      ebx, ebx
004096f5  05cf1b0000             add      eax, 0x1bcf
004096fa  6689c3                 mov      bx, ax
004096fd  89f8                   mov      eax, edi
004096ff  0529000000             add      eax, 0x29
00409704  eb13                   jmp      0x409719 ;
00409706  30e4                   xor      ah, ah
00409708  31db                   xor      ebx, ebx
0040970a  05e11b0000             add      eax, 0x1be1
0040970f  6689c3                 mov      bx, ax
00409712  89f8                   mov      eax, edi
00409714  0526000000             add      eax, 0x26
00409719  0fbfd0                 movsx    edx, ax
0040971c  0fbfc1                 movsx    eax, cx
0040971f  b901000000             mov      ecx, 1
00409724  e81e1b0500             call     0x45b247 ; PasteBobCmp
00409729  31c0                   xor      eax, eax
0040972b  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409733  e844750100             call     0x420c7c ; TuyauEstSortie
00409738  84c0                   test     al, al
0040973a  0f8451020000           je       0x409991
00409740  8b0c24                 mov      ecx, dword ptr [esp]
00409743  66a1808f5000           mov      ax, word ptr [0x508f80]
00409749  01c8                   add      eax, ecx
0040974b  30e4                   xor      ah, ah
0040974d  2407                   and      al, 7
0040974f  31db                   xor      ebx, ebx
00409751  05ef1b0000             add      eax, 0x1bef
00409756  6689c3                 mov      bx, ax
00409759  89f8                   mov      eax, edi
0040975b  0526000000             add      eax, 0x26
00409760  0fbfd0                 movsx    edx, ax
00409763  89f0                   mov      eax, esi
00409765  0540000000             add      eax, 0x40
0040976a  b901000000             mov      ecx, 1
0040976f  98                     cwde
00409770  e8d21a0500             call     0x45b247 ; PasteBobCmp
00409775  e917020000             jmp      0x409991 ;
0040977a  b901000000             mov      ecx, 1
0040977f  0fbfc7                 movsx    eax, di
00409782  bbb61b0000             mov      ebx, 0x1bb6
00409787  898424a0000000         mov      dword ptr [esp + 0xa0], eax
0040978e  0fbfc6                 movsx    eax, si
00409791  8b9424a0000000         mov      edx, dword ptr [esp + 0xa0]
00409798  89442454               mov      dword ptr [esp + 0x54], eax
0040979c  e8a61a0500             call     0x45b247 ; PasteBobCmp
004097a1  8b8424e2010000         mov      eax, dword ptr [esp + 0x1e2]
004097a8  c1f810                 sar      eax, 0x10
004097ab  b901000000             mov      ecx, 1
004097b0  898424cc010000         mov      dword ptr [esp + 0x1cc], eax
004097b7  8b8424f6030000         mov      eax, dword ptr [esp + 0x3f6]
004097be  bbb71b0000             mov      ebx, 0x1bb7
004097c3  c1f810                 sar      eax, 0x10
004097c6  8b9424cc010000         mov      edx, dword ptr [esp + 0x1cc]
004097cd  89842428010000         mov      dword ptr [esp + 0x128], eax
004097d4  e86e1a0500             call     0x45b247 ; PasteBobCmp
004097d9  8b842422040000         mov      eax, dword ptr [esp + 0x422]
004097e0  b901000000             mov      ecx, 1
004097e5  bbbf1b0000             mov      ebx, 0x1bbf
004097ea  c1f810                 sar      eax, 0x10
004097ed  8b9424a0000000         mov      edx, dword ptr [esp + 0xa0]
004097f4  89442450               mov      dword ptr [esp + 0x50], eax
004097f8  e84a1a0500             call     0x45b247 ; PasteBobCmp
004097fd  8b84243a040000         mov      eax, dword ptr [esp + 0x43a]
00409804  c1f810                 sar      eax, 0x10
00409807  b901000000             mov      ecx, 1
0040980c  89842458010000         mov      dword ptr [esp + 0x158], eax
00409813  8b84244a030000         mov      eax, dword ptr [esp + 0x34a]
0040981a  bbc71b0000             mov      ebx, 0x1bc7
0040981f  c1f810                 sar      eax, 0x10
00409822  8b942458010000         mov      edx, dword ptr [esp + 0x158]
00409829  898424ac000000         mov      dword ptr [esp + 0xac], eax
00409830  e8121a0500             call     0x45b247 ; PasteBobCmp
00409835  89f8                   mov      eax, edi
00409837  0529000000             add      eax, 0x29
0040983c  0fbfd0                 movsx    edx, ax
0040983f  89f0                   mov      eax, esi
00409841  0540000000             add      eax, 0x40
00409846  b901000000             mov      ecx, 1
0040984b  98                     cwde
0040984c  bbcf1b0000             mov      ebx, 0x1bcf
00409851  898424cc000000         mov      dword ptr [esp + 0xcc], eax
00409858  e8ea190500             call     0x45b247 ; PasteBobCmp
0040985d  8b84244e020000         mov      eax, dword ptr [esp + 0x24e]
00409864  c1f810                 sar      eax, 0x10
00409867  b901000000             mov      ecx, 1
0040986c  898424ec000000         mov      dword ptr [esp + 0xec], eax
00409873  8b84247a020000         mov      eax, dword ptr [esp + 0x27a]
0040987a  bbd71b0000             mov      ebx, 0x1bd7
0040987f  c1f810                 sar      eax, 0x10
00409882  8b9424ec000000         mov      edx, dword ptr [esp + 0xec]
00409889  89842460010000         mov      dword ptr [esp + 0x160], eax
00409890  e8b2190500             call     0x45b247 ; PasteBobCmp
00409895  89f8                   mov      eax, edi
00409897  0510000000             add      eax, 0x10
0040989c  98                     cwde
0040989d  89842438010000         mov      dword ptr [esp + 0x138], eax
004098a4  89f0                   mov      eax, esi
004098a6  b901000000             mov      ecx, 1
004098ab  0515000000             add      eax, 0x15
004098b0  bbdf1b0000             mov      ebx, 0x1bdf
004098b5  98                     cwde
004098b6  8b942438010000         mov      edx, dword ptr [esp + 0x138]
004098bd  89842468010000         mov      dword ptr [esp + 0x168], eax
004098c4  e87e190500             call     0x45b247 ; PasteBobCmp
004098c9  b901000000             mov      ecx, 1
004098ce  bbb61b0000             mov      ebx, 0x1bb6
004098d3  8b9424a0000000         mov      edx, dword ptr [esp + 0xa0]
004098da  8b442454               mov      eax, dword ptr [esp + 0x54]
004098de  e8cd230500             call     0x45bcb0 ; PasteGrisCmp
004098e3  b901000000             mov      ecx, 1
004098e8  bbb71b0000             mov      ebx, 0x1bb7
004098ed  8b9424cc010000         mov      edx, dword ptr [esp + 0x1cc]
004098f4  8b842428010000         mov      eax, dword ptr [esp + 0x128]
004098fb  e8b0230500             call     0x45bcb0 ; PasteGrisCmp
00409900  b901000000             mov      ecx, 1
00409905  bbbf1b0000             mov      ebx, 0x1bbf
0040990a  8b9424a0000000         mov      edx, dword ptr [esp + 0xa0]
00409911  8b442450               mov      eax, dword ptr [esp + 0x50]
00409915  e896230500             call     0x45bcb0 ; PasteGrisCmp
0040991a  b901000000             mov      ecx, 1
0040991f  bbc71b0000             mov      ebx, 0x1bc7
00409924  8b942458010000         mov      edx, dword ptr [esp + 0x158]
0040992b  8b8424ac000000         mov      eax, dword ptr [esp + 0xac]
00409932  e879230500             call     0x45bcb0 ; PasteGrisCmp
00409937  89f8                   mov      eax, edi
00409939  b901000000             mov      ecx, 1
0040993e  0526000000             add      eax, 0x26
00409943  bbcf1b0000             mov      ebx, 0x1bcf
00409948  0fbfd0                 movsx    edx, ax
0040994b  8b8424cc000000         mov      eax, dword ptr [esp + 0xcc]
00409952  e859230500             call     0x45bcb0 ; PasteGrisCmp
00409957  b901000000             mov      ecx, 1
0040995c  bbd71b0000             mov      ebx, 0x1bd7
00409961  8b9424ec000000         mov      edx, dword ptr [esp + 0xec]
00409968  8b842460010000         mov      eax, dword ptr [esp + 0x160]
0040996f  e83c230500             call     0x45bcb0 ; PasteGrisCmp
00409974  b901000000             mov      ecx, 1
00409979  bbdf1b0000             mov      ebx, 0x1bdf
0040997e  8b942438010000         mov      edx, dword ptr [esp + 0x138]
00409985  8b842468010000         mov      eax, dword ptr [esp + 0x168]
0040998c  e81f230500             call     0x45bcb0 ; PasteGrisCmp
00409991  31c0                   xor      eax, eax
00409993  668b4506               mov      ax, word ptr [ebp + 6]
00409997  85c0                   test     eax, eax
00409999  0f8ea3590000           jle      0x40f342
0040999f  6a03                   push     3
004099a1  e93c3c0000             jmp      0x40d5e2 ;
004099a6  31c0                   xor      eax, eax
004099a8  668b0d26875000         mov      cx, word ptr [0x508726]
004099af  6689d0                 mov      ax, dx
004099b2  668b1524875000         mov      dx, word ptr [0x508724]
004099b9  c1e105                 shl      ecx, 5
004099bc  c1e205                 shl      edx, 5
004099bf  49                     dec      ecx
004099c0  4a                     dec      edx
004099c1  83f864                 cmp      eax, 0x64
004099c4  0f8d7e000000           jge      0x409a48
004099ca  8994245c030000         mov      dword ptr [esp + 0x35c], edx
004099d1  ba64000000             mov      edx, 0x64
004099d6  29c2                   sub      edx, eax
004099d8  89d0                   mov      eax, edx
004099da  c1e002                 shl      eax, 2
004099dd  29d0                   sub      eax, edx
004099df  c1e005                 shl      eax, 5
004099e2  01c2                   add      edx, eax
004099e4  bb64000000             mov      ebx, 0x64
004099e9  89d0                   mov      eax, edx
004099eb  c1fa1f                 sar      edx, 0x1f
004099ee  f7fb                   idiv     ebx
004099f0  0fbfd7                 movsx    edx, di
004099f3  01d0                   add      eax, edx
004099f5  0fbfd6                 movsx    edx, si
004099f8  89b424b0030000         mov      dword ptr [esp + 0x3b0], esi
004099ff  85d2                   test     edx, edx
00409a01  7d09                   jge      0x409a0c
00409a03  31d2                   xor      edx, edx
00409a05  899424b0030000         mov      dword ptr [esp + 0x3b0], edx
00409a0c  0fbfd0                 movsx    edx, ax
00409a0f  85d2                   test     edx, edx
00409a11  7d02                   jge      0x409a15
00409a13  31c0                   xor      eax, eax
00409a15  81e1ffff0000           and      ecx, 0xffff
00409a1b  31d2                   xor      edx, edx
00409a1d  31db                   xor      ebx, ebx
00409a1f  6689c2                 mov      dx, ax
00409a22  31c0                   xor      eax, eax
00409a24  668b9c245c030000       mov      bx, word ptr [esp + 0x35c]
00409a2c  668b8424b0030000       mov      ax, word ptr [esp + 0x3b0]
00409a34  e8e05a0000             call     0x40f519 ; SetClipping
00409a39  b901000000             mov      ecx, 1
00409a3e  bbb51b0000             mov      ebx, 0x1bb5
00409a43  e9cae9ffff             jmp      0x408412 ;
00409a48  89942454040000         mov      dword ptr [esp + 0x454], edx
00409a4f  8d509c                 lea      edx, [eax - 0x64]
00409a52  b864000000             mov      eax, 0x64
00409a57  29d0                   sub      eax, edx
00409a59  89c2                   mov      edx, eax
00409a5b  c1e002                 shl      eax, 2
00409a5e  29d0                   sub      eax, edx
00409a60  c1e005                 shl      eax, 5
00409a63  01c2                   add      edx, eax
00409a65  bb64000000             mov      ebx, 0x64
00409a6a  89d0                   mov      eax, edx
00409a6c  c1fa1f                 sar      edx, 0x1f
00409a6f  f7fb                   idiv     ebx
00409a71  0fbfd7                 movsx    edx, di
00409a74  01d0                   add      eax, edx
00409a76  31d2                   xor      edx, edx
00409a78  668b1526875000         mov      dx, word ptr [0x508726]
00409a7f  898c240c020000         mov      dword ptr [esp + 0x20c], ecx
00409a86  c1e205                 shl      edx, 5
00409a89  0fbfd8                 movsx    ebx, ax
00409a8c  4a                     dec      edx
00409a8d  6689b42478040000       mov      word ptr [esp + 0x478], si
00409a95  39d3                   cmp      ebx, edx
00409a97  7e02                   jle      0x409a9b
00409a99  89c8                   mov      eax, ecx
00409a9b  31c9                   xor      ecx, ecx
00409a9d  31db                   xor      ebx, ebx
00409a9f  31d2                   xor      edx, edx
00409aa1  668b9c2454040000       mov      bx, word ptr [esp + 0x454]
00409aa9  6689c1                 mov      cx, ax
00409aac  31c0                   xor      eax, eax
00409aae  e8665a0000             call     0x40f519 ; SetClipping
00409ab3  0fbfc7                 movsx    eax, di
00409ab6  b901000000             mov      ecx, 1
00409abb  89442454               mov      dword ptr [esp + 0x54], eax
00409abf  bbb51b0000             mov      ebx, 0x1bb5
00409ac4  8b542454               mov      edx, dword ptr [esp + 0x54]
00409ac8  0fbfc6                 movsx    eax, si
00409acb  e877170500             call     0x45b247 ; PasteBobCmp
00409ad0  31c0                   xor      eax, eax
00409ad2  668b8424bc030000       mov      ax, word ptr [esp + 0x3bc]
00409ada  ba64000000             mov      edx, 0x64
00409adf  83e864                 sub      eax, 0x64
00409ae2  29c2                   sub      edx, eax
00409ae4  89d0                   mov      eax, edx
00409ae6  c1e002                 shl      eax, 2
00409ae9  29d0                   sub      eax, edx
00409aeb  c1e005                 shl      eax, 5
00409aee  01c2                   add      edx, eax
00409af0  bb64000000             mov      ebx, 0x64
00409af5  89d0                   mov      eax, edx
00409af7  c1fa1f                 sar      edx, 0x1f
00409afa  f7fb                   idiv     ebx
00409afc  8b942476040000         mov      edx, dword ptr [esp + 0x476]
00409b03  8b4c2454               mov      ecx, dword ptr [esp + 0x54]
00409b07  c1fa10                 sar      edx, 0x10
00409b0a  01c8                   add      eax, ecx
00409b0c  85d2                   test     edx, edx
00409b0e  7d0a                   jge      0x409b1a
00409b10  31c9                   xor      ecx, ecx
00409b12  66898c2478040000       mov      word ptr [esp + 0x478], cx
00409b1a  0fbfd0                 movsx    edx, ax
00409b1d  85d2                   test     edx, edx
00409b1f  7d02                   jge      0x409b23
00409b21  31c0                   xor      eax, eax
00409b23  31c9                   xor      ecx, ecx
00409b25  31db                   xor      ebx, ebx
00409b27  668b8c240c020000       mov      cx, word ptr [esp + 0x20c]
00409b2f  668b9c2454040000       mov      bx, word ptr [esp + 0x454]
00409b37  31d2                   xor      edx, edx
00409b39  668b942478040000       mov      dx, word ptr [esp + 0x478]
00409b41  25ffff0000             and      eax, 0xffff
00409b46  89542454               mov      dword ptr [esp + 0x54], edx
00409b4a  89c2                   mov      edx, eax
00409b4c  8b442454               mov      eax, dword ptr [esp + 0x54]
00409b50  e8c4590000             call     0x40f519 ; SetClipping
00409b55  b901000000             mov      ecx, 1
00409b5a  0fbfc7                 movsx    eax, di
00409b5d  bbb61b0000             mov      ebx, 0x1bb6
00409b62  898424f8000000         mov      dword ptr [esp + 0xf8], eax
00409b69  0fbfc6                 movsx    eax, si
00409b6c  8b9424f8000000         mov      edx, dword ptr [esp + 0xf8]
00409b73  898424f0000000         mov      dword ptr [esp + 0xf0], eax
00409b7a  e8c8160500             call     0x45b247 ; PasteBobCmp
00409b7f  89f8                   mov      eax, edi
00409b81  050a000000             add      eax, 0xa
00409b86  98                     cwde
00409b87  8984247c010000         mov      dword ptr [esp + 0x17c], eax
00409b8e  89f0                   mov      eax, esi
00409b90  b901000000             mov      ecx, 1
00409b95  0503000000             add      eax, 3
00409b9a  bbb71b0000             mov      ebx, 0x1bb7
00409b9f  98                     cwde
00409ba0  8b94247c010000         mov      edx, dword ptr [esp + 0x17c]
00409ba7  89842490010000         mov      dword ptr [esp + 0x190], eax
00409bae  e894160500             call     0x45b247 ; PasteBobCmp
00409bb3  89f0                   mov      eax, esi
00409bb5  b901000000             mov      ecx, 1
00409bba  052b000000             add      eax, 0x2b
00409bbf  bbbf1b0000             mov      ebx, 0x1bbf
00409bc4  98                     cwde
00409bc5  8b9424f8000000         mov      edx, dword ptr [esp + 0xf8]
00409bcc  8944243c               mov      dword ptr [esp + 0x3c], eax
00409bd0  e872160500             call     0x45b247 ; PasteBobCmp
00409bd5  89f8                   mov      eax, edi
00409bd7  0517000000             add      eax, 0x17
00409bdc  98                     cwde
00409bdd  898424f4000000         mov      dword ptr [esp + 0xf4], eax
00409be4  89f0                   mov      eax, esi
00409be6  b901000000             mov      ecx, 1
00409beb  053c000000             add      eax, 0x3c
00409bf0  bbc71b0000             mov      ebx, 0x1bc7
00409bf5  98                     cwde
00409bf6  8b9424f4000000         mov      edx, dword ptr [esp + 0xf4]
00409bfd  89442438               mov      dword ptr [esp + 0x38], eax
00409c01  e841160500             call     0x45b247 ; PasteBobCmp
00409c06  30e4                   xor      ah, ah
00409c08  8a4576                 mov      al, byte ptr [ebp + 0x76]
00409c0b  31db                   xor      ebx, ebx
00409c0d  05cf1b0000             add      eax, 0x1bcf
00409c12  6689c3                 mov      bx, ax
00409c15  89f8                   mov      eax, edi
00409c17  0529000000             add      eax, 0x29
00409c1c  0fbfd0                 movsx    edx, ax
00409c1f  89f0                   mov      eax, esi
00409c21  0540000000             add      eax, 0x40
00409c26  0fbfe8                 movsx    ebp, ax
00409c29  b901000000             mov      ecx, 1
00409c2e  89e8                   mov      eax, ebp
00409c30  e812160500             call     0x45b247 ; PasteBobCmp
00409c35  89f8                   mov      eax, edi
00409c37  052e000000             add      eax, 0x2e
00409c3c  98                     cwde
00409c3d  8984242c010000         mov      dword ptr [esp + 0x12c], eax
00409c44  89f0                   mov      eax, esi
00409c46  b901000000             mov      ecx, 1
00409c4b  050c000000             add      eax, 0xc
00409c50  bbd71b0000             mov      ebx, 0x1bd7
00409c55  98                     cwde
00409c56  8b94242c010000         mov      edx, dword ptr [esp + 0x12c]
00409c5d  8984245c010000         mov      dword ptr [esp + 0x15c], eax
00409c64  e8de150500             call     0x45b247 ; PasteBobCmp
00409c69  89f8                   mov      eax, edi
00409c6b  0510000000             add      eax, 0x10
00409c70  98                     cwde
00409c71  89842478010000         mov      dword ptr [esp + 0x178], eax
00409c78  89f0                   mov      eax, esi
00409c7a  b901000000             mov      ecx, 1
00409c7f  0515000000             add      eax, 0x15
00409c84  bbdf1b0000             mov      ebx, 0x1bdf
00409c89  98                     cwde
00409c8a  8b942478010000         mov      edx, dword ptr [esp + 0x178]
00409c91  89842408010000         mov      dword ptr [esp + 0x108], eax
00409c98  e8aa150500             call     0x45b247 ; PasteBobCmp
00409c9d  31c0                   xor      eax, eax
00409c9f  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409ca7  e80c090100             call     0x41a5b8 ; BatimentEstHabiter
00409cac  84c0                   test     al, al
00409cae  0f858e560000           jne      0x40f342
00409cb4  b901000000             mov      ecx, 1
00409cb9  bbb61b0000             mov      ebx, 0x1bb6
00409cbe  8b9424f8000000         mov      edx, dword ptr [esp + 0xf8]
00409cc5  8b8424f0000000         mov      eax, dword ptr [esp + 0xf0]
00409ccc  e8df1f0500             call     0x45bcb0 ; PasteGrisCmp
00409cd1  b901000000             mov      ecx, 1
00409cd6  bbb71b0000             mov      ebx, 0x1bb7
00409cdb  8b94247c010000         mov      edx, dword ptr [esp + 0x17c]
00409ce2  8b842490010000         mov      eax, dword ptr [esp + 0x190]
00409ce9  e8c21f0500             call     0x45bcb0 ; PasteGrisCmp
00409cee  b901000000             mov      ecx, 1
00409cf3  bbbf1b0000             mov      ebx, 0x1bbf
00409cf8  8b9424f8000000         mov      edx, dword ptr [esp + 0xf8]
00409cff  8b44243c               mov      eax, dword ptr [esp + 0x3c]
00409d03  e8a81f0500             call     0x45bcb0 ; PasteGrisCmp
00409d08  b901000000             mov      ecx, 1
00409d0d  bbc71b0000             mov      ebx, 0x1bc7
00409d12  8b9424f4000000         mov      edx, dword ptr [esp + 0xf4]
00409d19  8b442438               mov      eax, dword ptr [esp + 0x38]
00409d1d  e88e1f0500             call     0x45bcb0 ; PasteGrisCmp
00409d22  89f8                   mov      eax, edi
00409d24  b901000000             mov      ecx, 1
00409d29  0526000000             add      eax, 0x26
00409d2e  bbcf1b0000             mov      ebx, 0x1bcf
00409d33  0fbfd0                 movsx    edx, ax
00409d36  89e8                   mov      eax, ebp
00409d38  e8731f0500             call     0x45bcb0 ; PasteGrisCmp
00409d3d  b901000000             mov      ecx, 1
00409d42  bbd71b0000             mov      ebx, 0x1bd7
00409d47  8b94242c010000         mov      edx, dword ptr [esp + 0x12c]
00409d4e  8b84245c010000         mov      eax, dword ptr [esp + 0x15c]
00409d55  e8561f0500             call     0x45bcb0 ; PasteGrisCmp
00409d5a  b901000000             mov      ecx, 1
00409d5f  bbdf1b0000             mov      ebx, 0x1bdf
00409d64  8b942478010000         mov      edx, dword ptr [esp + 0x178]
00409d6b  8b842408010000         mov      eax, dword ptr [esp + 0x108]
00409d72  e9f6e7ffff             jmp      0x40856d ;
00409d77  31c0                   xor      eax, eax
00409d79  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
00409d7f  668b0424               mov      ax, word ptr [esp]
00409d83  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
00409d88  741c                   je       0x409da6
00409d8a  31c0                   xor      eax, eax
00409d8c  668b0424               mov      ax, word ptr [esp]
00409d90  668b0442               mov      ax, word ptr [edx + eax*2]
00409d94  25e07f0000             and      eax, 0x7fe0
00409d99  89c3                   mov      ebx, eax
00409d9b  81e3ffff0000           and      ebx, 0xffff
00409da1  c1fb05                 sar      ebx, 5
00409da4  eb05                   jmp      0x409dab ;
00409da6  bbffff0000             mov      ebx, 0xffff
00409dab  31d2                   xor      edx, edx
00409dad  6689da                 mov      dx, bx
00409db0  899c2410020000         mov      dword ptr [esp + 0x210], ebx
00409db7  81faffff0000           cmp      edx, 0xffff
00409dbd  0f84ce560000           je       0x40f491
00409dc3  89d5                   mov      ebp, edx
00409dc5  8b742408               mov      esi, dword ptr [esp + 8]
00409dc9  c1e504                 shl      ebp, 4
00409dcc  8b7c2404               mov      edi, dword ptr [esp + 4]
00409dd0  01d5                   add      ebp, edx
00409dd2  89d0                   mov      eax, edx
00409dd4  c1e502                 shl      ebp, 2
00409dd7  e8090b0100             call     0x41a8e5 ; BatimentGetEtat
00409ddc  01d5                   add      ebp, edx
00409dde  8984241c020000         mov      dword ptr [esp + 0x21c], eax
00409de5  c1e502                 shl      ebp, 2
00409de8  89c2                   mov      edx, eax
00409dea  81c5c8a04900           add      ebp, 0x49a0c8
00409df0  31c0                   xor      eax, eax
00409df2  83ee5b                 sub      esi, 0x5b
00409df5  8a4505                 mov      al, byte ptr [ebp + 5]
00409df8  83ef63                 sub      edi, 0x63
00409dfb  83f805                 cmp      eax, 5
00409dfe  740e                   je       0x409e0e
00409e00  83f803                 cmp      eax, 3
00409e03  7409                   je       0x409e0e
00409e05  83f804                 cmp      eax, 4
00409e08  0f85eb020000           jne      0x40a0f9
00409e0e  31c0                   xor      eax, eax
00409e10  8a4505                 mov      al, byte ptr [ebp + 5]
00409e13  83f803                 cmp      eax, 3
00409e16  0f8513010000           jne      0x409f2f
00409e1c  31c0                   xor      eax, eax
00409e1e  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409e26  e88d070100             call     0x41a5b8 ; BatimentEstHabiter
00409e2b  84c0                   test     al, al
00409e2d  0f85fc000000           jne      0x409f2f
00409e33  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
00409e39  31d2                   xor      edx, edx
00409e3b  88ca                   mov      dl, cl
00409e3d  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00409e43  81e2ff000000           and      edx, 0xff
00409e49  bb03000000             mov      ebx, 3
00409e4e  89d0                   mov      eax, edx
00409e50  c1fa1f                 sar      edx, 0x1f
00409e53  f7fb                   idiv     ebx
00409e55  0fbfdf                 movsx    ebx, di
00409e58  fec1                   inc      cl
00409e5a  8d0413                 lea      eax, [ebx + edx]
00409e5d  31d2                   xor      edx, edx
00409e5f  0592000000             add      eax, 0x92
00409e64  88ca                   mov      dl, cl
00409e66  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00409e6c  6689842440020000       mov      word ptr [esp + 0x240], ax
00409e74  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00409e7a  81e2ff000000           and      edx, 0xff
00409e80  bf03000000             mov      edi, 3
00409e85  89d0                   mov      eax, edx
00409e87  c1fa1f                 sar      edx, 0x1f
00409e8a  f7ff                   idiv     edi
00409e8c  fec1                   inc      cl
00409e8e  880d181d4e00           mov      byte ptr [0x4e1d18], cl
00409e94  8d0413                 lea      eax, [ebx + edx]
00409e97  31d2                   xor      edx, edx
00409e99  05c8000000             add      eax, 0xc8
00409e9e  668b9584000000         mov      dx, word ptr [ebp + 0x84]
00409ea5  29d0                   sub      eax, edx
00409ea7  89c7                   mov      edi, eax
00409ea9  98                     cwde
00409eaa  85c0                   test     eax, eax
00409eac  7d02                   jge      0x409eb0
00409eae  31ff                   xor      edi, edi
00409eb0  31c0                   xor      eax, eax
00409eb2  66a126875000           mov      ax, word ptr [0x508726]
00409eb8  8b94243e020000         mov      edx, dword ptr [esp + 0x23e]
00409ebf  c1e005                 shl      eax, 5
00409ec2  c1fa10                 sar      edx, 0x10
00409ec5  48                     dec      eax
00409ec6  39c2                   cmp      edx, eax
00409ec8  7e12                   jle      0x409edc
00409eca  66a126875000           mov      ax, word ptr [0x508726]
00409ed0  c1e005                 shl      eax, 5
00409ed3  48                     dec      eax
00409ed4  6689842440020000       mov      word ptr [esp + 0x240], ax
00409edc  66a124875000           mov      ax, word ptr [0x508724]
00409ee2  31c9                   xor      ecx, ecx
00409ee4  31db                   xor      ebx, ebx
00409ee6  31d2                   xor      edx, edx
00409ee8  668b8c2440020000       mov      cx, word ptr [esp + 0x240]
00409ef0  c1e005                 shl      eax, 5
00409ef3  6689fa                 mov      dx, di
00409ef6  6689c3                 mov      bx, ax
00409ef9  31c0                   xor      eax, eax
00409efb  e819560000             call     0x40f519 ; SetClipping
00409f00  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00409f06  31d2                   xor      edx, edx
00409f08  88da                   mov      dl, bl
00409f0a  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00409f10  81e2ff000000           and      edx, 0xff
00409f16  b903000000             mov      ecx, 3
00409f1b  89d0                   mov      eax, edx
00409f1d  c1fa1f                 sar      edx, 0x1f
00409f20  f7f9                   idiv     ecx
00409f22  fec3                   inc      bl
00409f24  0fbff6                 movsx    esi, si
00409f27  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00409f2d  01d6                   add      esi, edx
00409f2f  89f2                   mov      edx, esi
00409f31  83c214                 add      edx, 0x14
00409f34  66899424f4030000       mov      word ptr [esp + 0x3f4], dx
00409f3c  89fa                   mov      edx, edi
00409f3e  83c261                 add      edx, 0x61
00409f41  6689942450030000       mov      word ptr [esp + 0x350], dx
00409f49  89f2                   mov      edx, esi
00409f4b  83c210                 add      edx, 0x10
00409f4e  31c0                   xor      eax, eax
00409f50  6689942430030000       mov      word ptr [esp + 0x330], dx
00409f58  89fa                   mov      edx, edi
00409f5a  668b842410020000       mov      ax, word ptr [esp + 0x210]
00409f62  83c220                 add      edx, 0x20
00409f65  e84e060100             call     0x41a5b8 ; BatimentEstHabiter
00409f6a  6689942438020000       mov      word ptr [esp + 0x238], dx
00409f72  84c0                   test     al, al
00409f74  0f848e000000           je       0x40a008
00409f7a  b901000000             mov      ecx, 1
00409f7f  bbf81b0000             mov      ebx, 0x1bf8
00409f84  0fbfd7                 movsx    edx, di
00409f87  0fbfc6                 movsx    eax, si
00409f8a  e8b8120500             call     0x45b247 ; PasteBobCmp
00409f8f  8b1424                 mov      edx, dword ptr [esp]
00409f92  66a1808f5000           mov      ax, word ptr [0x508f80]
00409f98  01d0                   add      eax, edx
00409f9a  30e4                   xor      ah, ah
00409f9c  b901000000             mov      ecx, 1
00409fa1  2407                   and      al, 7
00409fa3  31db                   xor      ebx, ebx
00409fa5  05f91b0000             add      eax, 0x1bf9
00409faa  8b942436020000         mov      edx, dword ptr [esp + 0x236]
00409fb1  6689c3                 mov      bx, ax
00409fb4  8b84242e030000         mov      eax, dword ptr [esp + 0x32e]
00409fbb  c1fa10                 sar      edx, 0x10
00409fbe  c1f810                 sar      eax, 0x10
00409fc1  e881120500             call     0x45b247 ; PasteBobCmp
00409fc6  31c0                   xor      eax, eax
00409fc8  8a4504                 mov      al, byte ptr [ebp + 4]
00409fcb  8b1c24                 mov      ebx, dword ptr [esp]
00409fce  50                     push     eax
00409fcf  66a1808f5000           mov      ax, word ptr [0x508f80]
00409fd5  01d8                   add      eax, ebx
00409fd7  30e4                   xor      ah, ah
00409fd9  8b942452030000         mov      edx, dword ptr [esp + 0x352]
00409fe0  2407                   and      al, 7
00409fe2  31db                   xor      ebx, ebx
00409fe4  05011c0000             add      eax, 0x1c01
00409fe9  b901000000             mov      ecx, 1
00409fee  6689c3                 mov      bx, ax
00409ff1  8b8424f6030000         mov      eax, dword ptr [esp + 0x3f6]
00409ff8  c1fa10                 sar      edx, 0x10
00409ffb  c1f810                 sar      eax, 0x10
00409ffe  e852240500             call     0x45c455 ; PastePlayerCmp
0040a003  e9dc000000             jmp      0x40a0e4 ;
0040a008  b901000000             mov      ecx, 1
0040a00d  0fbfc7                 movsx    eax, di
0040a010  bbf81b0000             mov      ebx, 0x1bf8
0040a015  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040a01c  0fbfc6                 movsx    eax, si
0040a01f  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040a026  89842498000000         mov      dword ptr [esp + 0x98], eax
0040a02d  e815120500             call     0x45b247 ; PasteBobCmp
0040a032  8b842436020000         mov      eax, dword ptr [esp + 0x236]
0040a039  c1f810                 sar      eax, 0x10
0040a03c  b901000000             mov      ecx, 1
0040a041  89842494000000         mov      dword ptr [esp + 0x94], eax
0040a048  8b84242e030000         mov      eax, dword ptr [esp + 0x32e]
0040a04f  bbf91b0000             mov      ebx, 0x1bf9
0040a054  c1f810                 sar      eax, 0x10
0040a057  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040a05e  8944247c               mov      dword ptr [esp + 0x7c], eax
0040a062  e8e0110500             call     0x45b247 ; PasteBobCmp
0040a067  8b84244e030000         mov      eax, dword ptr [esp + 0x34e]
0040a06e  c1f810                 sar      eax, 0x10
0040a071  b901000000             mov      ecx, 1
0040a076  89442458               mov      dword ptr [esp + 0x58], eax
0040a07a  8b8424f2030000         mov      eax, dword ptr [esp + 0x3f2]
0040a081  bb011c0000             mov      ebx, 0x1c01
0040a086  c1f810                 sar      eax, 0x10
0040a089  8b542458               mov      edx, dword ptr [esp + 0x58]
0040a08d  89442454               mov      dword ptr [esp + 0x54], eax
0040a091  e8b1110500             call     0x45b247 ; PasteBobCmp
0040a096  b901000000             mov      ecx, 1
0040a09b  bbf81b0000             mov      ebx, 0x1bf8
0040a0a0  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040a0a7  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040a0ae  e8fd1b0500             call     0x45bcb0 ; PasteGrisCmp
0040a0b3  b901000000             mov      ecx, 1
0040a0b8  bbf91b0000             mov      ebx, 0x1bf9
0040a0bd  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040a0c4  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040a0c8  e8e31b0500             call     0x45bcb0 ; PasteGrisCmp
0040a0cd  b901000000             mov      ecx, 1
0040a0d2  bb011c0000             mov      ebx, 0x1c01
0040a0d7  8b542458               mov      edx, dword ptr [esp + 0x58]
0040a0db  8b442454               mov      eax, dword ptr [esp + 0x54]
0040a0df  e8cc1b0500             call     0x45bcb0 ; PasteGrisCmp
0040a0e4  31c0                   xor      eax, eax
0040a0e6  668b4506               mov      ax, word ptr [ebp + 6]
0040a0ea  85c0                   test     eax, eax
0040a0ec  0f8e50520000           jle      0x40f342
0040a0f2  6a0d                   push     0xd
0040a0f4  e9e9340000             jmp      0x40d5e2 ;
0040a0f9  31c0                   xor      eax, eax
0040a0fb  668b0d26875000         mov      cx, word ptr [0x508726]
0040a102  6689d0                 mov      ax, dx
0040a105  668b1524875000         mov      dx, word ptr [0x508724]
0040a10c  c1e105                 shl      ecx, 5
0040a10f  c1e205                 shl      edx, 5
0040a112  49                     dec      ecx
0040a113  4a                     dec      edx
0040a114  83f864                 cmp      eax, 0x64
0040a117  0f8d83000000           jge      0x40a1a0
0040a11d  899424c0020000         mov      dword ptr [esp + 0x2c0], edx
0040a124  ba64000000             mov      edx, 0x64
0040a129  29c2                   sub      edx, eax
0040a12b  89d0                   mov      eax, edx
0040a12d  c1e203                 shl      edx, 3
0040a130  01c2                   add      edx, eax
0040a132  c1e203                 shl      edx, 3
0040a135  01c2                   add      edx, eax
0040a137  01d2                   add      edx, edx
0040a139  bb64000000             mov      ebx, 0x64
0040a13e  89d0                   mov      eax, edx
0040a140  c1fa1f                 sar      edx, 0x1f
0040a143  f7fb                   idiv     ebx
0040a145  0fbfd7                 movsx    edx, di
0040a148  01d0                   add      eax, edx
0040a14a  89c2                   mov      edx, eax
0040a14c  0fbfc6                 movsx    eax, si
0040a14f  89b42464030000         mov      dword ptr [esp + 0x364], esi
0040a156  85c0                   test     eax, eax
0040a158  7d09                   jge      0x40a163
0040a15a  31c0                   xor      eax, eax
0040a15c  89842464030000         mov      dword ptr [esp + 0x364], eax
0040a163  0fbfc2                 movsx    eax, dx
0040a166  85c0                   test     eax, eax
0040a168  7d02                   jge      0x40a16c
0040a16a  31d2                   xor      edx, edx
0040a16c  31db                   xor      ebx, ebx
0040a16e  81e1ffff0000           and      ecx, 0xffff
0040a174  668b9c24c0020000       mov      bx, word ptr [esp + 0x2c0]
0040a17c  31c0                   xor      eax, eax
0040a17e  81e2ffff0000           and      edx, 0xffff
0040a184  668b842464030000       mov      ax, word ptr [esp + 0x364]
0040a18c  e888530000             call     0x40f519 ; SetClipping
0040a191  b901000000             mov      ecx, 1
0040a196  bbf71b0000             mov      ebx, 0x1bf7
0040a19b  e972e2ffff             jmp      0x408412 ;
0040a1a0  8994245c040000         mov      dword ptr [esp + 0x45c], edx
0040a1a7  83e864                 sub      eax, 0x64
0040a1aa  ba64000000             mov      edx, 0x64
0040a1af  29c2                   sub      edx, eax
0040a1b1  69d28d000000           imul     edx, edx, 0x8d
0040a1b7  bb64000000             mov      ebx, 0x64
0040a1bc  89d0                   mov      eax, edx
0040a1be  c1fa1f                 sar      edx, 0x1f
0040a1c1  f7fb                   idiv     ebx
0040a1c3  0fbfd7                 movsx    edx, di
0040a1c6  01d0                   add      eax, edx
0040a1c8  31d2                   xor      edx, edx
0040a1ca  668b1526875000         mov      dx, word ptr [0x508726]
0040a1d1  898c24a0030000         mov      dword ptr [esp + 0x3a0], ecx
0040a1d8  c1e205                 shl      edx, 5
0040a1db  0fbfd8                 movsx    ebx, ax
0040a1de  4a                     dec      edx
0040a1df  6689b42468020000       mov      word ptr [esp + 0x268], si
0040a1e7  39d3                   cmp      ebx, edx
0040a1e9  7e02                   jle      0x40a1ed
0040a1eb  89c8                   mov      eax, ecx
0040a1ed  31c9                   xor      ecx, ecx
0040a1ef  31db                   xor      ebx, ebx
0040a1f1  31d2                   xor      edx, edx
0040a1f3  668b9c245c040000       mov      bx, word ptr [esp + 0x45c]
0040a1fb  6689c1                 mov      cx, ax
0040a1fe  31c0                   xor      eax, eax
0040a200  0fbfef                 movsx    ebp, di
0040a203  e811530000             call     0x40f519 ; SetClipping
0040a208  b901000000             mov      ecx, 1
0040a20d  bbf71b0000             mov      ebx, 0x1bf7
0040a212  0fbfc6                 movsx    eax, si
0040a215  89ea                   mov      edx, ebp
0040a217  e82b100500             call     0x45b247 ; PasteBobCmp
0040a21c  31c0                   xor      eax, eax
0040a21e  668b84241c020000       mov      ax, word ptr [esp + 0x21c]
0040a226  ba64000000             mov      edx, 0x64
0040a22b  83e864                 sub      eax, 0x64
0040a22e  29c2                   sub      edx, eax
0040a230  69d28d000000           imul     edx, edx, 0x8d
0040a236  bb64000000             mov      ebx, 0x64
0040a23b  89d0                   mov      eax, edx
0040a23d  c1fa1f                 sar      edx, 0x1f
0040a240  f7fb                   idiv     ebx
0040a242  8b942466020000         mov      edx, dword ptr [esp + 0x266]
0040a249  c1fa10                 sar      edx, 0x10
0040a24c  01e8                   add      eax, ebp
0040a24e  85d2                   test     edx, edx
0040a250  7d0a                   jge      0x40a25c
0040a252  31db                   xor      ebx, ebx
0040a254  66899c2468020000       mov      word ptr [esp + 0x268], bx
0040a25c  0fbfd0                 movsx    edx, ax
0040a25f  85d2                   test     edx, edx
0040a261  7d02                   jge      0x40a265
0040a263  31c0                   xor      eax, eax
0040a265  31c9                   xor      ecx, ecx
0040a267  31db                   xor      ebx, ebx
0040a269  31d2                   xor      edx, edx
0040a26b  668b8c24a0030000       mov      cx, word ptr [esp + 0x3a0]
0040a273  6689c2                 mov      dx, ax
0040a276  31c0                   xor      eax, eax
0040a278  668b9c245c040000       mov      bx, word ptr [esp + 0x45c]
0040a280  668b842468020000       mov      ax, word ptr [esp + 0x268]
0040a288  0fbfef                 movsx    ebp, di
0040a28b  e889520000             call     0x40f519 ; SetClipping
0040a290  b901000000             mov      ecx, 1
0040a295  bbf81b0000             mov      ebx, 0x1bf8
0040a29a  0fbfc6                 movsx    eax, si
0040a29d  89ea                   mov      edx, ebp
0040a29f  89842484000000         mov      dword ptr [esp + 0x84], eax
0040a2a6  e89c0f0500             call     0x45b247 ; PasteBobCmp
0040a2ab  89f8                   mov      eax, edi
0040a2ad  0520000000             add      eax, 0x20
0040a2b2  98                     cwde
0040a2b3  89842490000000         mov      dword ptr [esp + 0x90], eax
0040a2ba  89f0                   mov      eax, esi
0040a2bc  b901000000             mov      ecx, 1
0040a2c1  0510000000             add      eax, 0x10
0040a2c6  bbf91b0000             mov      ebx, 0x1bf9
0040a2cb  98                     cwde
0040a2cc  8b942490000000         mov      edx, dword ptr [esp + 0x90]
0040a2d3  898424e8000000         mov      dword ptr [esp + 0xe8], eax
0040a2da  e8680f0500             call     0x45b247 ; PasteBobCmp
0040a2df  89f8                   mov      eax, edi
0040a2e1  0561000000             add      eax, 0x61
0040a2e6  98                     cwde
0040a2e7  898424bc010000         mov      dword ptr [esp + 0x1bc], eax
0040a2ee  89f0                   mov      eax, esi
0040a2f0  b901000000             mov      ecx, 1
0040a2f5  0514000000             add      eax, 0x14
0040a2fa  bb011c0000             mov      ebx, 0x1c01
0040a2ff  98                     cwde
0040a300  8b9424bc010000         mov      edx, dword ptr [esp + 0x1bc]
0040a307  89442448               mov      dword ptr [esp + 0x48], eax
0040a30b  e8370f0500             call     0x45b247 ; PasteBobCmp
0040a310  31c0                   xor      eax, eax
0040a312  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040a31a  e899020100             call     0x41a5b8 ; BatimentEstHabiter
0040a31f  84c0                   test     al, al
0040a321  0f851b500000           jne      0x40f342
0040a327  b901000000             mov      ecx, 1
0040a32c  bbf81b0000             mov      ebx, 0x1bf8
0040a331  8b842484000000         mov      eax, dword ptr [esp + 0x84]
0040a338  89ea                   mov      edx, ebp
0040a33a  e871190500             call     0x45bcb0 ; PasteGrisCmp
0040a33f  b901000000             mov      ecx, 1
0040a344  bbf91b0000             mov      ebx, 0x1bf9
0040a349  8b942490000000         mov      edx, dword ptr [esp + 0x90]
0040a350  8b8424e8000000         mov      eax, dword ptr [esp + 0xe8]
0040a357  e854190500             call     0x45bcb0 ; PasteGrisCmp
0040a35c  b901000000             mov      ecx, 1
0040a361  bb011c0000             mov      ebx, 0x1c01
0040a366  8b9424bc010000         mov      edx, dword ptr [esp + 0x1bc]
0040a36d  8b442448               mov      eax, dword ptr [esp + 0x48]
0040a371  e9f7e1ffff             jmp      0x40856d ;
0040a376  31c0                   xor      eax, eax
0040a378  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040a37e  668b0424               mov      ax, word ptr [esp]
0040a382  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
0040a387  741c                   je       0x40a3a5
0040a389  31c0                   xor      eax, eax
0040a38b  668b0424               mov      ax, word ptr [esp]
0040a38f  668b0442               mov      ax, word ptr [edx + eax*2]
0040a393  25e07f0000             and      eax, 0x7fe0
0040a398  89c3                   mov      ebx, eax
0040a39a  81e3ffff0000           and      ebx, 0xffff
0040a3a0  c1fb05                 sar      ebx, 5
0040a3a3  eb05                   jmp      0x40a3aa ;
0040a3a5  bbffff0000             mov      ebx, 0xffff
0040a3aa  31d2                   xor      edx, edx
0040a3ac  6689da                 mov      dx, bx
0040a3af  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040a3b6  81faffff0000           cmp      edx, 0xffff
0040a3bc  0f84cf500000           je       0x40f491
0040a3c2  89d5                   mov      ebp, edx
0040a3c4  8b742408               mov      esi, dword ptr [esp + 8]
0040a3c8  c1e504                 shl      ebp, 4
0040a3cb  8b7c2404               mov      edi, dword ptr [esp + 4]
0040a3cf  01d5                   add      ebp, edx
0040a3d1  89d0                   mov      eax, edx
0040a3d3  c1e502                 shl      ebp, 2
0040a3d6  e80a050100             call     0x41a8e5 ; BatimentGetEtat
0040a3db  01d5                   add      ebp, edx
0040a3dd  8984242c020000         mov      dword ptr [esp + 0x22c], eax
0040a3e4  c1e502                 shl      ebp, 2
0040a3e7  89c2                   mov      edx, eax
0040a3e9  81c5c8a04900           add      ebp, 0x49a0c8
0040a3ef  31c0                   xor      eax, eax
0040a3f1  83ee7a                 sub      esi, 0x7a
0040a3f4  8a4505                 mov      al, byte ptr [ebp + 5]
0040a3f7  83ef6a                 sub      edi, 0x6a
0040a3fa  83f805                 cmp      eax, 5
0040a3fd  740e                   je       0x40a40d
0040a3ff  83f803                 cmp      eax, 3
0040a402  7409                   je       0x40a40d
0040a404  83f804                 cmp      eax, 4
0040a407  0f8570040000           jne      0x40a87d
0040a40d  31c0                   xor      eax, eax
0040a40f  8a4505                 mov      al, byte ptr [ebp + 5]
0040a412  83f803                 cmp      eax, 3
0040a415  0f8515010000           jne      0x40a530
0040a41b  31c0                   xor      eax, eax
0040a41d  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040a425  e88e010100             call     0x41a5b8 ; BatimentEstHabiter
0040a42a  84c0                   test     al, al
0040a42c  0f85fe000000           jne      0x40a530
0040a432  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040a438  31d2                   xor      edx, edx
0040a43a  88da                   mov      dl, bl
0040a43c  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040a442  81e2ff000000           and      edx, 0xff
0040a448  b903000000             mov      ecx, 3
0040a44d  89d0                   mov      eax, edx
0040a44f  c1fa1f                 sar      edx, 0x1f
0040a452  f7f9                   idiv     ecx
0040a454  0fbfcf                 movsx    ecx, di
0040a457  01ca                   add      edx, ecx
0040a459  81c292000000           add      edx, 0x92
0040a45f  fec3                   inc      bl
0040a461  6689942474020000       mov      word ptr [esp + 0x274], dx
0040a469  31d2                   xor      edx, edx
0040a46b  88da                   mov      dl, bl
0040a46d  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040a473  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040a479  81e2ff000000           and      edx, 0xff
0040a47f  bf03000000             mov      edi, 3
0040a484  89d0                   mov      eax, edx
0040a486  c1fa1f                 sar      edx, 0x1f
0040a489  f7ff                   idiv     edi
0040a48b  fec3                   inc      bl
0040a48d  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040a493  01ca                   add      edx, ecx
0040a495  31c0                   xor      eax, eax
0040a497  81c2c8000000           add      edx, 0xc8
0040a49d  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040a4a4  29c2                   sub      edx, eax
0040a4a6  0fbfc2                 movsx    eax, dx
0040a4a9  89d7                   mov      edi, edx
0040a4ab  85c0                   test     eax, eax
0040a4ad  7d02                   jge      0x40a4b1
0040a4af  31d7                   xor      edi, edx
0040a4b1  31c0                   xor      eax, eax
0040a4b3  66a126875000           mov      ax, word ptr [0x508726]
0040a4b9  8b942472020000         mov      edx, dword ptr [esp + 0x272]
0040a4c0  c1e005                 shl      eax, 5
0040a4c3  c1fa10                 sar      edx, 0x10
0040a4c6  48                     dec      eax
0040a4c7  39c2                   cmp      edx, eax
0040a4c9  7e12                   jle      0x40a4dd
0040a4cb  66a126875000           mov      ax, word ptr [0x508726]
0040a4d1  c1e005                 shl      eax, 5
0040a4d4  48                     dec      eax
0040a4d5  6689842474020000       mov      word ptr [esp + 0x274], ax
0040a4dd  66a124875000           mov      ax, word ptr [0x508724]
0040a4e3  31c9                   xor      ecx, ecx
0040a4e5  31db                   xor      ebx, ebx
0040a4e7  31d2                   xor      edx, edx
0040a4e9  668b8c2474020000       mov      cx, word ptr [esp + 0x274]
0040a4f1  c1e005                 shl      eax, 5
0040a4f4  6689fa                 mov      dx, di
0040a4f7  6689c3                 mov      bx, ax
0040a4fa  31c0                   xor      eax, eax
0040a4fc  e818500000             call     0x40f519 ; SetClipping
0040a501  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040a507  31d2                   xor      edx, edx
0040a509  88da                   mov      dl, bl
0040a50b  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040a511  81e2ff000000           and      edx, 0xff
0040a517  b903000000             mov      ecx, 3
0040a51c  89d0                   mov      eax, edx
0040a51e  c1fa1f                 sar      edx, 0x1f
0040a521  f7f9                   idiv     ecx
0040a523  fec3                   inc      bl
0040a525  0fbff6                 movsx    esi, si
0040a528  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040a52e  01d6                   add      esi, edx
0040a530  89f2                   mov      edx, esi
0040a532  83c232                 add      edx, 0x32
0040a535  6689942410030000       mov      word ptr [esp + 0x310], dx
0040a53d  89fa                   mov      edx, edi
0040a53f  83ea30                 sub      edx, 0x30
0040a542  6689942434020000       mov      word ptr [esp + 0x234], dx
0040a54a  89f2                   mov      edx, esi
0040a54c  83c207                 add      edx, 7
0040a54f  31c0                   xor      eax, eax
0040a551  66899424f0030000       mov      word ptr [esp + 0x3f0], dx
0040a559  89fa                   mov      edx, edi
0040a55b  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040a563  83c21c                 add      edx, 0x1c
0040a566  e84d000100             call     0x41a5b8 ; BatimentEstHabiter
0040a56b  66899424a0020000       mov      word ptr [esp + 0x2a0], dx
0040a573  84c0                   test     al, al
0040a575  0f8473010000           je       0x40a6ee
0040a57b  b901000000             mov      ecx, 1
0040a580  31c0                   xor      eax, eax
0040a582  bb0a1c0000             mov      ebx, 0x1c0a
0040a587  8a4504                 mov      al, byte ptr [ebp + 4]
0040a58a  0fbfd7                 movsx    edx, di
0040a58d  50                     push     eax
0040a58e  0fbfc6                 movsx    eax, si
0040a591  e8bf1e0500             call     0x45c455 ; PastePlayerCmp
0040a596  8b1424                 mov      edx, dword ptr [esp]
0040a599  66a1808f5000           mov      ax, word ptr [0x508f80]
0040a59f  01d0                   add      eax, edx
0040a5a1  30e4                   xor      ah, ah
0040a5a3  b901000000             mov      ecx, 1
0040a5a8  2407                   and      al, 7
0040a5aa  31db                   xor      ebx, ebx
0040a5ac  052b1c0000             add      eax, 0x1c2b
0040a5b1  8b94249e020000         mov      edx, dword ptr [esp + 0x29e]
0040a5b8  6689c3                 mov      bx, ax
0040a5bb  8b8424ee030000         mov      eax, dword ptr [esp + 0x3ee]
0040a5c2  c1fa10                 sar      edx, 0x10
0040a5c5  c1f810                 sar      eax, 0x10
0040a5c8  e87a0c0500             call     0x45b247 ; PasteBobCmp
0040a5cd  807d7400               cmp      byte ptr [ebp + 0x74], 0
0040a5d1  7515                   jne      0x40a5e8
0040a5d3  e843de0400             call     0x45841b ; LongRand
0040a5d8  89c2                   mov      edx, eax
0040a5da  bb20030000             mov      ebx, 0x320
0040a5df  c1fa1f                 sar      edx, 0x1f
0040a5e2  f7fb                   idiv     ebx
0040a5e4  85d2                   test     edx, edx
0040a5e6  7530                   jne      0x40a618
0040a5e8  8b1c24                 mov      ebx, dword ptr [esp]
0040a5eb  66a1808f5000           mov      ax, word ptr [0x508f80]
0040a5f1  01d8                   add      eax, ebx
0040a5f3  30e4                   xor      ah, ah
0040a5f5  241f                   and      al, 0x1f
0040a5f7  31db                   xor      ebx, ebx
0040a5f9  050b1c0000             add      eax, 0x1c0b
0040a5fe  6689c3                 mov      bx, ax
0040a601  89f8                   mov      eax, edi
0040a603  83e830                 sub      eax, 0x30
0040a606  0fbfd0                 movsx    edx, ax
0040a609  89f0                   mov      eax, esi
0040a60b  0532000000             add      eax, 0x32
0040a610  b901000000             mov      ecx, 1
0040a615  98                     cwde
0040a616  eb1e                   jmp      0x40a636 ;
0040a618  8b942432020000         mov      edx, dword ptr [esp + 0x232]
0040a61f  8b84240e030000         mov      eax, dword ptr [esp + 0x30e]
0040a626  b901000000             mov      ecx, 1
0040a62b  bb0b1c0000             mov      ebx, 0x1c0b
0040a630  c1fa10                 sar      edx, 0x10
0040a633  c1f810                 sar      eax, 0x10
0040a636  e80c0c0500             call     0x45b247 ; PasteBobCmp
0040a63b  30e4                   xor      ah, ah
0040a63d  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040a640  31db                   xor      ebx, ebx
0040a642  05351c0000             add      eax, 0x1c35
0040a647  6689c3                 mov      bx, ax
0040a64a  89f8                   mov      eax, edi
0040a64c  0530000000             add      eax, 0x30
0040a651  0fbfd0                 movsx    edx, ax
0040a654  89f0                   mov      eax, esi
0040a656  0556000000             add      eax, 0x56
0040a65b  b901000000             mov      ecx, 1
0040a660  98                     cwde
0040a661  e8e10b0500             call     0x45b247 ; PasteBobCmp
0040a666  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040a66c  31d2                   xor      edx, edx
0040a66e  88da                   mov      dl, bl
0040a670  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040a676  81e2ff000000           and      edx, 0xff
0040a67c  b914000000             mov      ecx, 0x14
0040a681  89d0                   mov      eax, edx
0040a683  c1fa1f                 sar      edx, 0x1f
0040a686  f7f9                   idiv     ecx
0040a688  fec3                   inc      bl
0040a68a  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040a690  89f0                   mov      eax, esi
0040a692  89f9                   mov      ecx, edi
0040a694  0527000000             add      eax, 0x27
0040a699  83c15c                 add      ecx, 0x5c
0040a69c  6689842488020000       mov      word ptr [esp + 0x288], ax
0040a6a4  85d2                   test     edx, edx
0040a6a6  7535                   jne      0x40a6dd
0040a6a8  8b1424                 mov      edx, dword ptr [esp]
0040a6ab  66a1808f5000           mov      ax, word ptr [0x508f80]
0040a6b1  01d0                   add      eax, edx
0040a6b3  30e4                   xor      ah, ah
0040a6b5  2401                   and      al, 1
0040a6b7  31db                   xor      ebx, ebx
0040a6b9  05331c0000             add      eax, 0x1c33
0040a6be  0fbfd1                 movsx    edx, cx
0040a6c1  6689c3                 mov      bx, ax
0040a6c4  8b842486020000         mov      eax, dword ptr [esp + 0x286]
0040a6cb  b901000000             mov      ecx, 1
0040a6d0  c1f810                 sar      eax, 0x10
0040a6d3  e86f0b0500             call     0x45b247 ; PasteBobCmp
0040a6d8  e98b010000             jmp      0x40a868 ;
0040a6dd  8b842486020000         mov      eax, dword ptr [esp + 0x286]
0040a6e4  bb331c0000             mov      ebx, 0x1c33
0040a6e9  0fbfd1                 movsx    edx, cx
0040a6ec  ebdd                   jmp      0x40a6cb ;
0040a6ee  b901000000             mov      ecx, 1
0040a6f3  0fbfc7                 movsx    eax, di
0040a6f6  bb0a1c0000             mov      ebx, 0x1c0a
0040a6fb  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040a702  0fbfc6                 movsx    eax, si
0040a705  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040a70c  89842498000000         mov      dword ptr [esp + 0x98], eax
0040a713  e82f0b0500             call     0x45b247 ; PasteBobCmp
0040a718  8b84249e020000         mov      eax, dword ptr [esp + 0x29e]
0040a71f  c1f810                 sar      eax, 0x10
0040a722  b901000000             mov      ecx, 1
0040a727  89842494000000         mov      dword ptr [esp + 0x94], eax
0040a72e  8b8424ee030000         mov      eax, dword ptr [esp + 0x3ee]
0040a735  bb2b1c0000             mov      ebx, 0x1c2b
0040a73a  c1f810                 sar      eax, 0x10
0040a73d  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040a744  8944247c               mov      dword ptr [esp + 0x7c], eax
0040a748  e8fa0a0500             call     0x45b247 ; PasteBobCmp
0040a74d  8b842432020000         mov      eax, dword ptr [esp + 0x232]
0040a754  c1f810                 sar      eax, 0x10
0040a757  b901000000             mov      ecx, 1
0040a75c  89442458               mov      dword ptr [esp + 0x58], eax
0040a760  8b84240e030000         mov      eax, dword ptr [esp + 0x30e]
0040a767  bb0b1c0000             mov      ebx, 0x1c0b
0040a76c  c1f810                 sar      eax, 0x10
0040a76f  8b542458               mov      edx, dword ptr [esp + 0x58]
0040a773  89442454               mov      dword ptr [esp + 0x54], eax
0040a777  e8cb0a0500             call     0x45b247 ; PasteBobCmp
0040a77c  30e4                   xor      ah, ah
0040a77e  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040a781  31db                   xor      ebx, ebx
0040a783  05351c0000             add      eax, 0x1c35
0040a788  6689c3                 mov      bx, ax
0040a78b  89f8                   mov      eax, edi
0040a78d  0530000000             add      eax, 0x30
0040a792  98                     cwde
0040a793  8944241c               mov      dword ptr [esp + 0x1c], eax
0040a797  89f0                   mov      eax, esi
0040a799  0556000000             add      eax, 0x56
0040a79e  b901000000             mov      ecx, 1
0040a7a3  98                     cwde
0040a7a4  8b54241c               mov      edx, dword ptr [esp + 0x1c]
0040a7a8  89442470               mov      dword ptr [esp + 0x70], eax
0040a7ac  e8960a0500             call     0x45b247 ; PasteBobCmp
0040a7b1  89f8                   mov      eax, edi
0040a7b3  055c000000             add      eax, 0x5c
0040a7b8  98                     cwde
0040a7b9  8944240c               mov      dword ptr [esp + 0xc], eax
0040a7bd  89f0                   mov      eax, esi
0040a7bf  b901000000             mov      ecx, 1
0040a7c4  0527000000             add      eax, 0x27
0040a7c9  bb331c0000             mov      ebx, 0x1c33
0040a7ce  98                     cwde
0040a7cf  8b54240c               mov      edx, dword ptr [esp + 0xc]
0040a7d3  898424c4000000         mov      dword ptr [esp + 0xc4], eax
0040a7da  e8680a0500             call     0x45b247 ; PasteBobCmp
0040a7df  b901000000             mov      ecx, 1
0040a7e4  bb0a1c0000             mov      ebx, 0x1c0a
0040a7e9  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040a7f0  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040a7f7  e8b4140500             call     0x45bcb0 ; PasteGrisCmp
0040a7fc  b901000000             mov      ecx, 1
0040a801  bb2b1c0000             mov      ebx, 0x1c2b
0040a806  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040a80d  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040a811  e89a140500             call     0x45bcb0 ; PasteGrisCmp
0040a816  b901000000             mov      ecx, 1
0040a81b  bb0b1c0000             mov      ebx, 0x1c0b
0040a820  8b542458               mov      edx, dword ptr [esp + 0x58]
0040a824  8b442454               mov      eax, dword ptr [esp + 0x54]
0040a828  e883140500             call     0x45bcb0 ; PasteGrisCmp
0040a82d  30e4                   xor      ah, ah
0040a82f  b901000000             mov      ecx, 1
0040a834  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040a837  31db                   xor      ebx, ebx
0040a839  05351c0000             add      eax, 0x1c35
0040a83e  8b54241c               mov      edx, dword ptr [esp + 0x1c]
0040a842  6689c3                 mov      bx, ax
0040a845  8b442470               mov      eax, dword ptr [esp + 0x70]
0040a849  e862140500             call     0x45bcb0 ; PasteGrisCmp
0040a84e  b901000000             mov      ecx, 1
0040a853  bb331c0000             mov      ebx, 0x1c33
0040a858  8b54240c               mov      edx, dword ptr [esp + 0xc]
0040a85c  8b8424c4000000         mov      eax, dword ptr [esp + 0xc4]
0040a863  e848140500             call     0x45bcb0 ; PasteGrisCmp
0040a868  31c0                   xor      eax, eax
0040a86a  668b4506               mov      ax, word ptr [ebp + 6]
0040a86e  85c0                   test     eax, eax
0040a870  0f8ecc4a0000           jle      0x40f342
0040a876  6a05                   push     5
0040a878  e9652d0000             jmp      0x40d5e2 ;
0040a87d  31c0                   xor      eax, eax
0040a87f  668b0d26875000         mov      cx, word ptr [0x508726]
0040a886  6689d0                 mov      ax, dx
0040a889  668b1524875000         mov      dx, word ptr [0x508724]
0040a890  c1e105                 shl      ecx, 5
0040a893  c1e205                 shl      edx, 5
0040a896  49                     dec      ecx
0040a897  4a                     dec      edx
0040a898  83f864                 cmp      eax, 0x64
0040a89b  0f8d83000000           jge      0x40a924
0040a8a1  899424e4020000         mov      dword ptr [esp + 0x2e4], edx
0040a8a8  ba64000000             mov      edx, 0x64
0040a8ad  29c2                   sub      edx, eax
0040a8af  89d0                   mov      eax, edx
0040a8b1  c1e203                 shl      edx, 3
0040a8b4  01c2                   add      edx, eax
0040a8b6  c1e203                 shl      edx, 3
0040a8b9  01c2                   add      edx, eax
0040a8bb  01d2                   add      edx, edx
0040a8bd  bb64000000             mov      ebx, 0x64
0040a8c2  89d0                   mov      eax, edx
0040a8c4  c1fa1f                 sar      edx, 0x1f
0040a8c7  f7fb                   idiv     ebx
0040a8c9  0fbfd7                 movsx    edx, di
0040a8cc  01d0                   add      eax, edx
0040a8ce  89c2                   mov      edx, eax
0040a8d0  0fbfc6                 movsx    eax, si
0040a8d3  89b4244c040000         mov      dword ptr [esp + 0x44c], esi
0040a8da  85c0                   test     eax, eax
0040a8dc  7d09                   jge      0x40a8e7
0040a8de  31c0                   xor      eax, eax
0040a8e0  8984244c040000         mov      dword ptr [esp + 0x44c], eax
0040a8e7  0fbfc2                 movsx    eax, dx
0040a8ea  85c0                   test     eax, eax
0040a8ec  7d02                   jge      0x40a8f0
0040a8ee  31d2                   xor      edx, edx
0040a8f0  31db                   xor      ebx, ebx
0040a8f2  81e1ffff0000           and      ecx, 0xffff
0040a8f8  668b9c24e4020000       mov      bx, word ptr [esp + 0x2e4]
0040a900  31c0                   xor      eax, eax
0040a902  81e2ffff0000           and      edx, 0xffff
0040a908  668b84244c040000       mov      ax, word ptr [esp + 0x44c]
0040a910  e8044c0000             call     0x40f519 ; SetClipping
0040a915  b901000000             mov      ecx, 1
0040a91a  bb091c0000             mov      ebx, 0x1c09
0040a91f  e9eedaffff             jmp      0x408412 ;
0040a924  89942460040000         mov      dword ptr [esp + 0x460], edx
0040a92b  83e864                 sub      eax, 0x64
0040a92e  ba64000000             mov      edx, 0x64
0040a933  29c2                   sub      edx, eax
0040a935  89d0                   mov      eax, edx
0040a937  c1e203                 shl      edx, 3
0040a93a  01c2                   add      edx, eax
0040a93c  c1e203                 shl      edx, 3
0040a93f  01c2                   add      edx, eax
0040a941  01d2                   add      edx, edx
0040a943  bb64000000             mov      ebx, 0x64
0040a948  89d0                   mov      eax, edx
0040a94a  c1fa1f                 sar      edx, 0x1f
0040a94d  f7fb                   idiv     ebx
0040a94f  0fbfd7                 movsx    edx, di
0040a952  01d0                   add      eax, edx
0040a954  31d2                   xor      edx, edx
0040a956  668b1526875000         mov      dx, word ptr [0x508726]
0040a95d  898c24a4030000         mov      dword ptr [esp + 0x3a4], ecx
0040a964  c1e205                 shl      edx, 5
0040a967  0fbfd8                 movsx    ebx, ax
0040a96a  4a                     dec      edx
0040a96b  6689b42440040000       mov      word ptr [esp + 0x440], si
0040a973  39d3                   cmp      ebx, edx
0040a975  7e02                   jle      0x40a979
0040a977  89c8                   mov      eax, ecx
0040a979  31c9                   xor      ecx, ecx
0040a97b  31db                   xor      ebx, ebx
0040a97d  31d2                   xor      edx, edx
0040a97f  668b9c2460040000       mov      bx, word ptr [esp + 0x460]
0040a987  6689c1                 mov      cx, ax
0040a98a  31c0                   xor      eax, eax
0040a98c  e8884b0000             call     0x40f519 ; SetClipping
0040a991  0fbfc7                 movsx    eax, di
0040a994  b901000000             mov      ecx, 1
0040a999  89442454               mov      dword ptr [esp + 0x54], eax
0040a99d  bb091c0000             mov      ebx, 0x1c09
0040a9a2  8b542454               mov      edx, dword ptr [esp + 0x54]
0040a9a6  0fbfc6                 movsx    eax, si
0040a9a9  e899080500             call     0x45b247 ; PasteBobCmp
0040a9ae  31c0                   xor      eax, eax
0040a9b0  668b84242c020000       mov      ax, word ptr [esp + 0x22c]
0040a9b8  ba64000000             mov      edx, 0x64
0040a9bd  83e864                 sub      eax, 0x64
0040a9c0  29c2                   sub      edx, eax
0040a9c2  89d0                   mov      eax, edx
0040a9c4  c1e203                 shl      edx, 3
0040a9c7  01c2                   add      edx, eax
0040a9c9  c1e203                 shl      edx, 3
0040a9cc  01c2                   add      edx, eax
0040a9ce  01d2                   add      edx, edx
0040a9d0  bb64000000             mov      ebx, 0x64
0040a9d5  89d0                   mov      eax, edx
0040a9d7  c1fa1f                 sar      edx, 0x1f
0040a9da  f7fb                   idiv     ebx
0040a9dc  8b94243e040000         mov      edx, dword ptr [esp + 0x43e]
0040a9e3  8b5c2454               mov      ebx, dword ptr [esp + 0x54]
0040a9e7  c1fa10                 sar      edx, 0x10
0040a9ea  01d8                   add      eax, ebx
0040a9ec  85d2                   test     edx, edx
0040a9ee  7d0a                   jge      0x40a9fa
0040a9f0  31c9                   xor      ecx, ecx
0040a9f2  66898c2440040000       mov      word ptr [esp + 0x440], cx
0040a9fa  0fbfd0                 movsx    edx, ax
0040a9fd  85d2                   test     edx, edx
0040a9ff  7d02                   jge      0x40aa03
0040aa01  31c0                   xor      eax, eax
0040aa03  31c9                   xor      ecx, ecx
0040aa05  31db                   xor      ebx, ebx
0040aa07  31d2                   xor      edx, edx
0040aa09  668b8c24a4030000       mov      cx, word ptr [esp + 0x3a4]
0040aa11  6689c2                 mov      dx, ax
0040aa14  31c0                   xor      eax, eax
0040aa16  668b9c2460040000       mov      bx, word ptr [esp + 0x460]
0040aa1e  668b842440040000       mov      ax, word ptr [esp + 0x440]
0040aa26  0fbfee                 movsx    ebp, si
0040aa29  e8eb4a0000             call     0x40f519 ; SetClipping
0040aa2e  b901000000             mov      ecx, 1
0040aa33  0fbfc7                 movsx    eax, di
0040aa36  bb0a1c0000             mov      ebx, 0x1c0a
0040aa3b  89842440010000         mov      dword ptr [esp + 0x140], eax
0040aa42  89c2                   mov      edx, eax
0040aa44  89e8                   mov      eax, ebp
0040aa46  e8fc070500             call     0x45b247 ; PasteBobCmp
0040aa4b  89f8                   mov      eax, edi
0040aa4d  051c000000             add      eax, 0x1c
0040aa52  98                     cwde
0040aa53  89442424               mov      dword ptr [esp + 0x24], eax
0040aa57  89f0                   mov      eax, esi
0040aa59  b901000000             mov      ecx, 1
0040aa5e  0507000000             add      eax, 7
0040aa63  bb2b1c0000             mov      ebx, 0x1c2b
0040aa68  98                     cwde
0040aa69  8b542424               mov      edx, dword ptr [esp + 0x24]
0040aa6d  89442474               mov      dword ptr [esp + 0x74], eax
0040aa71  e8d1070500             call     0x45b247 ; PasteBobCmp
0040aa76  89f8                   mov      eax, edi
0040aa78  83e830                 sub      eax, 0x30
0040aa7b  98                     cwde
0040aa7c  898424c4010000         mov      dword ptr [esp + 0x1c4], eax
0040aa83  89f0                   mov      eax, esi
0040aa85  b901000000             mov      ecx, 1
0040aa8a  0532000000             add      eax, 0x32
0040aa8f  bb0b1c0000             mov      ebx, 0x1c0b
0040aa94  98                     cwde
0040aa95  8b9424c4010000         mov      edx, dword ptr [esp + 0x1c4]
0040aa9c  898424e0000000         mov      dword ptr [esp + 0xe0], eax
0040aaa3  e89f070500             call     0x45b247 ; PasteBobCmp
0040aaa8  89f8                   mov      eax, edi
0040aaaa  0530000000             add      eax, 0x30
0040aaaf  98                     cwde
0040aab0  89842484010000         mov      dword ptr [esp + 0x184], eax
0040aab7  89f0                   mov      eax, esi
0040aab9  b901000000             mov      ecx, 1
0040aabe  0556000000             add      eax, 0x56
0040aac3  bb351c0000             mov      ebx, 0x1c35
0040aac8  98                     cwde
0040aac9  8b942484010000         mov      edx, dword ptr [esp + 0x184]
0040aad0  898424c0010000         mov      dword ptr [esp + 0x1c0], eax
0040aad7  e86b070500             call     0x45b247 ; PasteBobCmp
0040aadc  89f8                   mov      eax, edi
0040aade  055c000000             add      eax, 0x5c
0040aae3  98                     cwde
0040aae4  89842420010000         mov      dword ptr [esp + 0x120], eax
0040aaeb  89f0                   mov      eax, esi
0040aaed  b901000000             mov      ecx, 1
0040aaf2  0527000000             add      eax, 0x27
0040aaf7  bb331c0000             mov      ebx, 0x1c33
0040aafc  98                     cwde
0040aafd  8b942420010000         mov      edx, dword ptr [esp + 0x120]
0040ab04  898424c8010000         mov      dword ptr [esp + 0x1c8], eax
0040ab0b  e837070500             call     0x45b247 ; PasteBobCmp
0040ab10  31c0                   xor      eax, eax
0040ab12  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040ab1a  e899fa0000             call     0x41a5b8 ; BatimentEstHabiter
0040ab1f  84c0                   test     al, al
0040ab21  0f851b480000           jne      0x40f342
0040ab27  b901000000             mov      ecx, 1
0040ab2c  bb0a1c0000             mov      ebx, 0x1c0a
0040ab31  8b942440010000         mov      edx, dword ptr [esp + 0x140]
0040ab38  89e8                   mov      eax, ebp
0040ab3a  e871110500             call     0x45bcb0 ; PasteGrisCmp
0040ab3f  b901000000             mov      ecx, 1
0040ab44  bb2b1c0000             mov      ebx, 0x1c2b
0040ab49  8b542424               mov      edx, dword ptr [esp + 0x24]
0040ab4d  8b442474               mov      eax, dword ptr [esp + 0x74]
0040ab51  e85a110500             call     0x45bcb0 ; PasteGrisCmp
0040ab56  b901000000             mov      ecx, 1
0040ab5b  bb0b1c0000             mov      ebx, 0x1c0b
0040ab60  8b9424c4010000         mov      edx, dword ptr [esp + 0x1c4]
0040ab67  8b8424e0000000         mov      eax, dword ptr [esp + 0xe0]
0040ab6e  e83d110500             call     0x45bcb0 ; PasteGrisCmp
0040ab73  b901000000             mov      ecx, 1
0040ab78  bb351c0000             mov      ebx, 0x1c35
0040ab7d  8b942484010000         mov      edx, dword ptr [esp + 0x184]
0040ab84  8b8424c0010000         mov      eax, dword ptr [esp + 0x1c0]
0040ab8b  e820110500             call     0x45bcb0 ; PasteGrisCmp
0040ab90  b901000000             mov      ecx, 1
0040ab95  bb331c0000             mov      ebx, 0x1c33
0040ab9a  8b942420010000         mov      edx, dword ptr [esp + 0x120]
0040aba1  8b8424c8010000         mov      eax, dword ptr [esp + 0x1c8]
0040aba8  e9c0d9ffff             jmp      0x40856d ;
0040abad  31c0                   xor      eax, eax
0040abaf  668b0424               mov      ax, word ptr [esp]
0040abb3  8d1400                 lea      edx, [eax + eax]
0040abb6  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040abbb  f644020180             test     byte ptr [edx + eax + 1], 0x80
0040abc0  741c                   je       0x40abde
0040abc2  31d2                   xor      edx, edx
0040abc4  668b1424               mov      dx, word ptr [esp]
0040abc8  668b0450               mov      ax, word ptr [eax + edx*2]
0040abcc  25e07f0000             and      eax, 0x7fe0
0040abd1  89c3                   mov      ebx, eax
0040abd3  81e3ffff0000           and      ebx, 0xffff
0040abd9  c1fb05                 sar      ebx, 5
0040abdc  eb05                   jmp      0x40abe3 ;
0040abde  bbffff0000             mov      ebx, 0xffff
0040abe3  31d2                   xor      edx, edx
0040abe5  6689da                 mov      dx, bx
0040abe8  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040abef  81faffff0000           cmp      edx, 0xffff
0040abf5  0f8496480000           je       0x40f491
0040abfb  89d5                   mov      ebp, edx
0040abfd  8b742408               mov      esi, dword ptr [esp + 8]
0040ac01  c1e504                 shl      ebp, 4
0040ac04  8b7c2404               mov      edi, dword ptr [esp + 4]
0040ac08  01d5                   add      ebp, edx
0040ac0a  89d0                   mov      eax, edx
0040ac0c  c1e502                 shl      ebp, 2
0040ac0f  e8d1fc0000             call     0x41a8e5 ; BatimentGetEtat
0040ac14  01d5                   add      ebp, edx
0040ac16  898424e0020000         mov      dword ptr [esp + 0x2e0], eax
0040ac1d  c1e502                 shl      ebp, 2
0040ac20  89c2                   mov      edx, eax
0040ac22  81c5c8a04900           add      ebp, 0x49a0c8
0040ac28  31c0                   xor      eax, eax
0040ac2a  83ee4a                 sub      esi, 0x4a
0040ac2d  8a4505                 mov      al, byte ptr [ebp + 5]
0040ac30  83ef2f                 sub      edi, 0x2f
0040ac33  83f805                 cmp      eax, 5
0040ac36  740e                   je       0x40ac46
0040ac38  83f803                 cmp      eax, 3
0040ac3b  7409                   je       0x40ac46
0040ac3d  83f804                 cmp      eax, 4
0040ac40  0f857c030000           jne      0x40afc2
0040ac46  31c0                   xor      eax, eax
0040ac48  8a4505                 mov      al, byte ptr [ebp + 5]
0040ac4b  83f803                 cmp      eax, 3
0040ac4e  0f8511010000           jne      0x40ad65
0040ac54  31c0                   xor      eax, eax
0040ac56  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040ac5e  e855f90000             call     0x41a5b8 ; BatimentEstHabiter
0040ac63  84c0                   test     al, al
0040ac65  0f85fa000000           jne      0x40ad65
0040ac6b  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040ac71  31d2                   xor      edx, edx
0040ac73  88da                   mov      dl, bl
0040ac75  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040ac7b  81e2ff000000           and      edx, 0xff
0040ac81  b903000000             mov      ecx, 3
0040ac86  89d0                   mov      eax, edx
0040ac88  c1fa1f                 sar      edx, 0x1f
0040ac8b  f7f9                   idiv     ecx
0040ac8d  0fbfcf                 movsx    ecx, di
0040ac90  01ca                   add      edx, ecx
0040ac92  83c271                 add      edx, 0x71
0040ac95  fec3                   inc      bl
0040ac97  66899424d0030000       mov      word ptr [esp + 0x3d0], dx
0040ac9f  31d2                   xor      edx, edx
0040aca1  88da                   mov      dl, bl
0040aca3  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040aca9  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040acaf  81e2ff000000           and      edx, 0xff
0040acb5  bf03000000             mov      edi, 3
0040acba  89d0                   mov      eax, edx
0040acbc  c1fa1f                 sar      edx, 0x1f
0040acbf  f7ff                   idiv     edi
0040acc1  fec3                   inc      bl
0040acc3  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040acc9  8d3c0a                 lea      edi, [edx + ecx]
0040accc  31c0                   xor      eax, eax
0040acce  81c7c8000000           add      edi, 0xc8
0040acd4  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040acdb  29c7                   sub      edi, eax
0040acdd  0fbfc7                 movsx    eax, di
0040ace0  85c0                   test     eax, eax
0040ace2  7d02                   jge      0x40ace6
0040ace4  31ff                   xor      edi, edi
0040ace6  31c0                   xor      eax, eax
0040ace8  66a126875000           mov      ax, word ptr [0x508726]
0040acee  8b9424ce030000         mov      edx, dword ptr [esp + 0x3ce]
0040acf5  c1e005                 shl      eax, 5
0040acf8  c1fa10                 sar      edx, 0x10
0040acfb  48                     dec      eax
0040acfc  39c2                   cmp      edx, eax
0040acfe  7e12                   jle      0x40ad12
0040ad00  66a126875000           mov      ax, word ptr [0x508726]
0040ad06  c1e005                 shl      eax, 5
0040ad09  48                     dec      eax
0040ad0a  66898424d0030000       mov      word ptr [esp + 0x3d0], ax
0040ad12  66a124875000           mov      ax, word ptr [0x508724]
0040ad18  31c9                   xor      ecx, ecx
0040ad1a  31db                   xor      ebx, ebx
0040ad1c  31d2                   xor      edx, edx
0040ad1e  668b8c24d0030000       mov      cx, word ptr [esp + 0x3d0]
0040ad26  c1e005                 shl      eax, 5
0040ad29  6689fa                 mov      dx, di
0040ad2c  6689c3                 mov      bx, ax
0040ad2f  31c0                   xor      eax, eax
0040ad31  e8e3470000             call     0x40f519 ; SetClipping
0040ad36  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040ad3c  31d2                   xor      edx, edx
0040ad3e  88da                   mov      dl, bl
0040ad40  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040ad46  81e2ff000000           and      edx, 0xff
0040ad4c  b903000000             mov      ecx, 3
0040ad51  89d0                   mov      eax, edx
0040ad53  c1fa1f                 sar      edx, 0x1f
0040ad56  f7f9                   idiv     ecx
0040ad58  fec3                   inc      bl
0040ad5a  0fbff6                 movsx    esi, si
0040ad5d  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040ad63  01d6                   add      esi, edx
0040ad65  31db                   xor      ebx, ebx
0040ad67  668b9c2410020000       mov      bx, word ptr [esp + 0x210]
0040ad6f  89d8                   mov      eax, ebx
0040ad71  e842f80000             call     0x41a5b8 ; BatimentEstHabiter
0040ad76  84c0                   test     al, al
0040ad78  0f840a010000           je       0x40ae88
0040ad7e  31c0                   xor      eax, eax
0040ad80  8a4505                 mov      al, byte ptr [ebp + 5]
0040ad83  83f804                 cmp      eax, 4
0040ad86  7513                   jne      0x40ad9b
0040ad88  8b542402               mov      edx, dword ptr [esp + 2]
0040ad8c  8b442406               mov      eax, dword ptr [esp + 6]
0040ad90  c1fa10                 sar      edx, 0x10
0040ad93  c1f810                 sar      eax, 0x10
0040ad96  e8357cffff             call     0x4029d0 ; AffVehiculeReparer
0040ad9b  b901000000             mov      ecx, 1
0040ada0  31c0                   xor      eax, eax
0040ada2  bb3e1c0000             mov      ebx, 0x1c3e
0040ada7  8a4504                 mov      al, byte ptr [ebp + 4]
0040adaa  0fbfd7                 movsx    edx, di
0040adad  50                     push     eax
0040adae  0fbfc6                 movsx    eax, si
0040adb1  e89f160500             call     0x45c455 ; PastePlayerCmp
0040adb6  8b1c24                 mov      ebx, dword ptr [esp]
0040adb9  66a1808f5000           mov      ax, word ptr [0x508f80]
0040adbf  01d8                   add      eax, ebx
0040adc1  30e4                   xor      ah, ah
0040adc3  2407                   and      al, 7
0040adc5  31db                   xor      ebx, ebx
0040adc7  053f1c0000             add      eax, 0x1c3f
0040adcc  6689c3                 mov      bx, ax
0040adcf  89f8                   mov      eax, edi
0040add1  051f000000             add      eax, 0x1f
0040add6  0fbfd0                 movsx    edx, ax
0040add9  89f0                   mov      eax, esi
0040addb  0528000000             add      eax, 0x28
0040ade0  b901000000             mov      ecx, 1
0040ade5  98                     cwde
0040ade6  e85c040500             call     0x45b247 ; PasteBobCmp
0040adeb  30e4                   xor      ah, ah
0040aded  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040adf0  31db                   xor      ebx, ebx
0040adf2  05471c0000             add      eax, 0x1c47
0040adf7  6689c3                 mov      bx, ax
0040adfa  89f8                   mov      eax, edi
0040adfc  052e000000             add      eax, 0x2e
0040ae01  0fbfd0                 movsx    edx, ax
0040ae04  89f0                   mov      eax, esi
0040ae06  0509000000             add      eax, 9
0040ae0b  b901000000             mov      ecx, 1
0040ae10  98                     cwde
0040ae11  e831040500             call     0x45b247 ; PasteBobCmp
0040ae16  89f0                   mov      eax, esi
0040ae18  0544000000             add      eax, 0x44
0040ae1d  89f9                   mov      ecx, edi
0040ae1f  66898424e8030000       mov      word ptr [esp + 0x3e8], ax
0040ae27  8a4574                 mov      al, byte ptr [ebp + 0x74]
0040ae2a  83c103                 add      ecx, 3
0040ae2d  84c0                   test     al, al
0040ae2f  743e                   je       0x40ae6f
0040ae31  31c0                   xor      eax, eax
0040ae33  8b15808f5000           mov      edx, dword ptr [0x508f80]
0040ae39  668b0424               mov      ax, word ptr [esp]
0040ae3d  bb03000000             mov      ebx, 3
0040ae42  01d0                   add      eax, edx
0040ae44  31d2                   xor      edx, edx
0040ae46  f7f3                   div      ebx
0040ae48  81c24f1c0000           add      edx, 0x1c4f
0040ae4e  31db                   xor      ebx, ebx
0040ae50  8b8424e6030000         mov      eax, dword ptr [esp + 0x3e6]
0040ae57  6689d3                 mov      bx, dx
0040ae5a  c1f810                 sar      eax, 0x10
0040ae5d  0fbfd1                 movsx    edx, cx
0040ae60  b901000000             mov      ecx, 1
0040ae65  e8dd030500             call     0x45b247 ; PasteBobCmp
0040ae6a  e93e010000             jmp      0x40afad ;
0040ae6f  8b8424e6030000         mov      eax, dword ptr [esp + 0x3e6]
0040ae76  bb4f1c0000             mov      ebx, 0x1c4f
0040ae7b  0fbfd1                 movsx    edx, cx
0040ae7e  b901000000             mov      ecx, 1
0040ae83  c1f810                 sar      eax, 0x10
0040ae86  ebdd                   jmp      0x40ae65 ;
0040ae88  b901000000             mov      ecx, 1
0040ae8d  0fbfc7                 movsx    eax, di
0040ae90  bb3e1c0000             mov      ebx, 0x1c3e
0040ae95  89442454               mov      dword ptr [esp + 0x54], eax
0040ae99  0fbfc6                 movsx    eax, si
0040ae9c  8b542454               mov      edx, dword ptr [esp + 0x54]
0040aea0  89442458               mov      dword ptr [esp + 0x58], eax
0040aea4  e89e030500             call     0x45b247 ; PasteBobCmp
0040aea9  89f8                   mov      eax, edi
0040aeab  051f000000             add      eax, 0x1f
0040aeb0  98                     cwde
0040aeb1  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040aeb8  89f0                   mov      eax, esi
0040aeba  b901000000             mov      ecx, 1
0040aebf  0528000000             add      eax, 0x28
0040aec4  bb3f1c0000             mov      ebx, 0x1c3f
0040aec9  98                     cwde
0040aeca  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040aed1  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040aed8  e86a030500             call     0x45b247 ; PasteBobCmp
0040aedd  89f8                   mov      eax, edi
0040aedf  052e000000             add      eax, 0x2e
0040aee4  98                     cwde
0040aee5  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040aeec  89f0                   mov      eax, esi
0040aeee  b901000000             mov      ecx, 1
0040aef3  0509000000             add      eax, 9
0040aef8  bb471c0000             mov      ebx, 0x1c47
0040aefd  98                     cwde
0040aefe  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040af05  89842498000000         mov      dword ptr [esp + 0x98], eax
0040af0c  e836030500             call     0x45b247 ; PasteBobCmp
0040af11  89f8                   mov      eax, edi
0040af13  0503000000             add      eax, 3
0040af18  98                     cwde
0040af19  89842494000000         mov      dword ptr [esp + 0x94], eax
0040af20  89f0                   mov      eax, esi
0040af22  b901000000             mov      ecx, 1
0040af27  0544000000             add      eax, 0x44
0040af2c  bb4f1c0000             mov      ebx, 0x1c4f
0040af31  98                     cwde
0040af32  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040af39  8944247c               mov      dword ptr [esp + 0x7c], eax
0040af3d  e805030500             call     0x45b247 ; PasteBobCmp
0040af42  b901000000             mov      ecx, 1
0040af47  bb3e1c0000             mov      ebx, 0x1c3e
0040af4c  8b542454               mov      edx, dword ptr [esp + 0x54]
0040af50  8b442458               mov      eax, dword ptr [esp + 0x58]
0040af54  e8570d0500             call     0x45bcb0 ; PasteGrisCmp
0040af59  b901000000             mov      ecx, 1
0040af5e  bb3f1c0000             mov      ebx, 0x1c3f
0040af63  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040af6a  8b8424b4000000         mov      eax, dword ptr [esp + 0xb4]
0040af71  e83a0d0500             call     0x45bcb0 ; PasteGrisCmp
0040af76  b901000000             mov      ecx, 1
0040af7b  bb471c0000             mov      ebx, 0x1c47
0040af80  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040af87  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040af8e  e81d0d0500             call     0x45bcb0 ; PasteGrisCmp
0040af93  b901000000             mov      ecx, 1
0040af98  bb4f1c0000             mov      ebx, 0x1c4f
0040af9d  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040afa4  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040afa8  e8030d0500             call     0x45bcb0 ; PasteGrisCmp
0040afad  31c0                   xor      eax, eax
0040afaf  668b4506               mov      ax, word ptr [ebp + 6]
0040afb3  85c0                   test     eax, eax
0040afb5  0f8e87430000           jle      0x40f342
0040afbb  6a0e                   push     0xe
0040afbd  e920260000             jmp      0x40d5e2 ;
0040afc2  31c0                   xor      eax, eax
0040afc4  668b0d26875000         mov      cx, word ptr [0x508726]
0040afcb  6689d0                 mov      ax, dx
0040afce  668b1524875000         mov      dx, word ptr [0x508724]
0040afd5  c1e105                 shl      ecx, 5
0040afd8  c1e205                 shl      edx, 5
0040afdb  49                     dec      ecx
0040afdc  4a                     dec      edx
0040afdd  83f864                 cmp      eax, 0x64
0040afe0  0f8d7e000000           jge      0x40b064
0040afe6  899424c8030000         mov      dword ptr [esp + 0x3c8], edx
0040afed  ba64000000             mov      edx, 0x64
0040aff2  29c2                   sub      edx, eax
0040aff4  89d0                   mov      eax, edx
0040aff6  c1e203                 shl      edx, 3
0040aff9  29c2                   sub      edx, eax
0040affb  c1e204                 shl      edx, 4
0040affe  01c2                   add      edx, eax
0040b000  bb64000000             mov      ebx, 0x64
0040b005  89d0                   mov      eax, edx
0040b007  c1fa1f                 sar      edx, 0x1f
0040b00a  f7fb                   idiv     ebx
0040b00c  0fbfd7                 movsx    edx, di
0040b00f  01d0                   add      eax, edx
0040b011  0fbfd6                 movsx    edx, si
0040b014  89b42434040000         mov      dword ptr [esp + 0x434], esi
0040b01b  85d2                   test     edx, edx
0040b01d  7d09                   jge      0x40b028
0040b01f  31d2                   xor      edx, edx
0040b021  89942434040000         mov      dword ptr [esp + 0x434], edx
0040b028  0fbfd0                 movsx    edx, ax
0040b02b  85d2                   test     edx, edx
0040b02d  7d02                   jge      0x40b031
0040b02f  31c0                   xor      eax, eax
0040b031  81e1ffff0000           and      ecx, 0xffff
0040b037  31d2                   xor      edx, edx
0040b039  31db                   xor      ebx, ebx
0040b03b  6689c2                 mov      dx, ax
0040b03e  31c0                   xor      eax, eax
0040b040  668b9c24c8030000       mov      bx, word ptr [esp + 0x3c8]
0040b048  668b842434040000       mov      ax, word ptr [esp + 0x434]
0040b050  e8c4440000             call     0x40f519 ; SetClipping
0040b055  b901000000             mov      ecx, 1
0040b05a  bb3d1c0000             mov      ebx, 0x1c3d
0040b05f  e9aed3ffff             jmp      0x408412 ;
0040b064  8994249c030000         mov      dword ptr [esp + 0x39c], edx
0040b06b  83e864                 sub      eax, 0x64
0040b06e  ba64000000             mov      edx, 0x64
0040b073  29c2                   sub      edx, eax
0040b075  89d0                   mov      eax, edx
0040b077  c1e203                 shl      edx, 3
0040b07a  29c2                   sub      edx, eax
0040b07c  c1e204                 shl      edx, 4
0040b07f  01c2                   add      edx, eax
0040b081  bb64000000             mov      ebx, 0x64
0040b086  89d0                   mov      eax, edx
0040b088  c1fa1f                 sar      edx, 0x1f
0040b08b  f7fb                   idiv     ebx
0040b08d  0fbfd7                 movsx    edx, di
0040b090  01d0                   add      eax, edx
0040b092  31d2                   xor      edx, edx
0040b094  668b1526875000         mov      dx, word ptr [0x508726]
0040b09b  898c24a8030000         mov      dword ptr [esp + 0x3a8], ecx
0040b0a2  c1e205                 shl      edx, 5
0040b0a5  0fbfd8                 movsx    ebx, ax
0040b0a8  4a                     dec      edx
0040b0a9  6689b424d8030000       mov      word ptr [esp + 0x3d8], si
0040b0b1  39d3                   cmp      ebx, edx
0040b0b3  7e02                   jle      0x40b0b7
0040b0b5  89c8                   mov      eax, ecx
0040b0b7  31c9                   xor      ecx, ecx
0040b0b9  31db                   xor      ebx, ebx
0040b0bb  31d2                   xor      edx, edx
0040b0bd  668b9c249c030000       mov      bx, word ptr [esp + 0x39c]
0040b0c5  6689c1                 mov      cx, ax
0040b0c8  31c0                   xor      eax, eax
0040b0ca  e84a440000             call     0x40f519 ; SetClipping
0040b0cf  0fbfc7                 movsx    eax, di
0040b0d2  b901000000             mov      ecx, 1
0040b0d7  8944247c               mov      dword ptr [esp + 0x7c], eax
0040b0db  bb3d1c0000             mov      ebx, 0x1c3d
0040b0e0  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040b0e4  0fbfc6                 movsx    eax, si
0040b0e7  e85b010500             call     0x45b247 ; PasteBobCmp
0040b0ec  31c0                   xor      eax, eax
0040b0ee  668b8424e0020000       mov      ax, word ptr [esp + 0x2e0]
0040b0f6  ba64000000             mov      edx, 0x64
0040b0fb  83e864                 sub      eax, 0x64
0040b0fe  29c2                   sub      edx, eax
0040b100  89d0                   mov      eax, edx
0040b102  c1e203                 shl      edx, 3
0040b105  29c2                   sub      edx, eax
0040b107  c1e204                 shl      edx, 4
0040b10a  01c2                   add      edx, eax
0040b10c  bb64000000             mov      ebx, 0x64
0040b111  89d0                   mov      eax, edx
0040b113  c1fa1f                 sar      edx, 0x1f
0040b116  f7fb                   idiv     ebx
0040b118  8b9424d6030000         mov      edx, dword ptr [esp + 0x3d6]
0040b11f  8b5c247c               mov      ebx, dword ptr [esp + 0x7c]
0040b123  c1fa10                 sar      edx, 0x10
0040b126  01d8                   add      eax, ebx
0040b128  85d2                   test     edx, edx
0040b12a  7d0a                   jge      0x40b136
0040b12c  31db                   xor      ebx, ebx
0040b12e  66899c24d8030000       mov      word ptr [esp + 0x3d8], bx
0040b136  0fbfd0                 movsx    edx, ax
0040b139  85d2                   test     edx, edx
0040b13b  7d02                   jge      0x40b13f
0040b13d  31c0                   xor      eax, eax
0040b13f  31c9                   xor      ecx, ecx
0040b141  31db                   xor      ebx, ebx
0040b143  31d2                   xor      edx, edx
0040b145  668b8c24a8030000       mov      cx, word ptr [esp + 0x3a8]
0040b14d  6689c2                 mov      dx, ax
0040b150  31c0                   xor      eax, eax
0040b152  668b9c249c030000       mov      bx, word ptr [esp + 0x39c]
0040b15a  668b8424d8030000       mov      ax, word ptr [esp + 0x3d8]
0040b162  0fbfee                 movsx    ebp, si
0040b165  e8af430000             call     0x40f519 ; SetClipping
0040b16a  b901000000             mov      ecx, 1
0040b16f  0fbfc7                 movsx    eax, di
0040b172  bb3e1c0000             mov      ebx, 0x1c3e
0040b177  89442430               mov      dword ptr [esp + 0x30], eax
0040b17b  89c2                   mov      edx, eax
0040b17d  89e8                   mov      eax, ebp
0040b17f  e8c3000500             call     0x45b247 ; PasteBobCmp
0040b184  89f8                   mov      eax, edi
0040b186  051f000000             add      eax, 0x1f
0040b18b  98                     cwde
0040b18c  8984249c010000         mov      dword ptr [esp + 0x19c], eax
0040b193  89f0                   mov      eax, esi
0040b195  b901000000             mov      ecx, 1
0040b19a  0528000000             add      eax, 0x28
0040b19f  bb3f1c0000             mov      ebx, 0x1c3f
0040b1a4  98                     cwde
0040b1a5  8b94249c010000         mov      edx, dword ptr [esp + 0x19c]
0040b1ac  89442440               mov      dword ptr [esp + 0x40], eax
0040b1b0  e892000500             call     0x45b247 ; PasteBobCmp
0040b1b5  89f8                   mov      eax, edi
0040b1b7  052e000000             add      eax, 0x2e
0040b1bc  98                     cwde
0040b1bd  898424bc000000         mov      dword ptr [esp + 0xbc], eax
0040b1c4  89f0                   mov      eax, esi
0040b1c6  b901000000             mov      ecx, 1
0040b1cb  0509000000             add      eax, 9
0040b1d0  bb471c0000             mov      ebx, 0x1c47
0040b1d5  98                     cwde
0040b1d6  8b9424bc000000         mov      edx, dword ptr [esp + 0xbc]
0040b1dd  89842404010000         mov      dword ptr [esp + 0x104], eax
0040b1e4  e85e000500             call     0x45b247 ; PasteBobCmp
0040b1e9  89f8                   mov      eax, edi
0040b1eb  0503000000             add      eax, 3
0040b1f0  98                     cwde
0040b1f1  898424a8000000         mov      dword ptr [esp + 0xa8], eax
0040b1f8  89f0                   mov      eax, esi
0040b1fa  b901000000             mov      ecx, 1
0040b1ff  0544000000             add      eax, 0x44
0040b204  bb4f1c0000             mov      ebx, 0x1c4f
0040b209  98                     cwde
0040b20a  8b9424a8000000         mov      edx, dword ptr [esp + 0xa8]
0040b211  89842410010000         mov      dword ptr [esp + 0x110], eax
0040b218  e82a000500             call     0x45b247 ; PasteBobCmp
0040b21d  31c0                   xor      eax, eax
0040b21f  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b227  e88cf30000             call     0x41a5b8 ; BatimentEstHabiter
0040b22c  84c0                   test     al, al
0040b22e  0f850e410000           jne      0x40f342
0040b234  b901000000             mov      ecx, 1
0040b239  bb3e1c0000             mov      ebx, 0x1c3e
0040b23e  8b542430               mov      edx, dword ptr [esp + 0x30]
0040b242  89e8                   mov      eax, ebp
0040b244  e8670a0500             call     0x45bcb0 ; PasteGrisCmp
0040b249  b901000000             mov      ecx, 1
0040b24e  bb3f1c0000             mov      ebx, 0x1c3f
0040b253  8b94249c010000         mov      edx, dword ptr [esp + 0x19c]
0040b25a  8b442440               mov      eax, dword ptr [esp + 0x40]
0040b25e  e84d0a0500             call     0x45bcb0 ; PasteGrisCmp
0040b263  b901000000             mov      ecx, 1
0040b268  bb471c0000             mov      ebx, 0x1c47
0040b26d  8b9424bc000000         mov      edx, dword ptr [esp + 0xbc]
0040b274  8b842404010000         mov      eax, dword ptr [esp + 0x104]
0040b27b  e8300a0500             call     0x45bcb0 ; PasteGrisCmp
0040b280  b901000000             mov      ecx, 1
0040b285  bb4f1c0000             mov      ebx, 0x1c4f
0040b28a  8b9424a8000000         mov      edx, dword ptr [esp + 0xa8]
0040b291  8b842410010000         mov      eax, dword ptr [esp + 0x110]
0040b298  e9d0d2ffff             jmp      0x40856d ;
0040b29d  31c0                   xor      eax, eax
0040b29f  668b0424               mov      ax, word ptr [esp]
0040b2a3  8d1400                 lea      edx, [eax + eax]
0040b2a6  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040b2ab  f644020180             test     byte ptr [edx + eax + 1], 0x80
0040b2b0  7422                   je       0x40b2d4
0040b2b2  31c0                   xor      eax, eax
0040b2b4  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040b2ba  668b0424               mov      ax, word ptr [esp]
0040b2be  668b0442               mov      ax, word ptr [edx + eax*2]
0040b2c2  25e07f0000             and      eax, 0x7fe0
0040b2c7  89c3                   mov      ebx, eax
0040b2c9  81e3ffff0000           and      ebx, 0xffff
0040b2cf  c1fb05                 sar      ebx, 5
0040b2d2  eb05                   jmp      0x40b2d9 ;
0040b2d4  bbffff0000             mov      ebx, 0xffff
0040b2d9  31d2                   xor      edx, edx
0040b2db  6689da                 mov      dx, bx
0040b2de  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040b2e5  81faffff0000           cmp      edx, 0xffff
0040b2eb  0f84a0410000           je       0x40f491
0040b2f1  89d5                   mov      ebp, edx
0040b2f3  8b742408               mov      esi, dword ptr [esp + 8]
0040b2f7  c1e504                 shl      ebp, 4
0040b2fa  8b7c2404               mov      edi, dword ptr [esp + 4]
0040b2fe  01d5                   add      ebp, edx
0040b300  89d0                   mov      eax, edx
0040b302  c1e502                 shl      ebp, 2
0040b305  e8dbf50000             call     0x41a8e5 ; BatimentGetEtat
0040b30a  01d5                   add      ebp, edx
0040b30c  898424e0010000         mov      dword ptr [esp + 0x1e0], eax
0040b313  c1e502                 shl      ebp, 2
0040b316  89c2                   mov      edx, eax
0040b318  81c5c8a04900           add      ebp, 0x49a0c8
0040b31e  31c0                   xor      eax, eax
0040b320  83ee2f                 sub      esi, 0x2f
0040b323  8a4505                 mov      al, byte ptr [ebp + 5]
0040b326  83ef2e                 sub      edi, 0x2e
0040b329  83f805                 cmp      eax, 5
0040b32c  740e                   je       0x40b33c
0040b32e  83f803                 cmp      eax, 3
0040b331  7409                   je       0x40b33c
0040b333  83f804                 cmp      eax, 4
0040b336  0f857a020000           jne      0x40b5b6
0040b33c  31c0                   xor      eax, eax
0040b33e  8a4505                 mov      al, byte ptr [ebp + 5]
0040b341  83f803                 cmp      eax, 3
0040b344  0f8514010000           jne      0x40b45e
0040b34a  31c0                   xor      eax, eax
0040b34c  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b354  e85ff20000             call     0x41a5b8 ; BatimentEstHabiter
0040b359  84c0                   test     al, al
0040b35b  0f85fd000000           jne      0x40b45e
0040b361  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040b367  31d2                   xor      edx, edx
0040b369  88da                   mov      dl, bl
0040b36b  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b371  81e2ff000000           and      edx, 0xff
0040b377  b903000000             mov      ecx, 3
0040b37c  89d0                   mov      eax, edx
0040b37e  c1fa1f                 sar      edx, 0x1f
0040b381  f7f9                   idiv     ecx
0040b383  0fbfcf                 movsx    ecx, di
0040b386  01ca                   add      edx, ecx
0040b388  83c258                 add      edx, 0x58
0040b38b  fec3                   inc      bl
0040b38d  668994244c020000       mov      word ptr [esp + 0x24c], dx
0040b395  31d2                   xor      edx, edx
0040b397  88da                   mov      dl, bl
0040b399  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040b39f  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b3a5  81e2ff000000           and      edx, 0xff
0040b3ab  bf03000000             mov      edi, 3
0040b3b0  89d0                   mov      eax, edx
0040b3b2  c1fa1f                 sar      edx, 0x1f
0040b3b5  f7ff                   idiv     edi
0040b3b7  fec3                   inc      bl
0040b3b9  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040b3bf  01ca                   add      edx, ecx
0040b3c1  31ff                   xor      edi, edi
0040b3c3  81c2c8000000           add      edx, 0xc8
0040b3c9  668bbd84000000         mov      di, word ptr [ebp + 0x84]
0040b3d0  29fa                   sub      edx, edi
0040b3d2  0fbfc2                 movsx    eax, dx
0040b3d5  89d7                   mov      edi, edx
0040b3d7  85c0                   test     eax, eax
0040b3d9  7d02                   jge      0x40b3dd
0040b3db  31d7                   xor      edi, edx
0040b3dd  31c0                   xor      eax, eax
0040b3df  66a126875000           mov      ax, word ptr [0x508726]
0040b3e5  89c2                   mov      edx, eax
0040b3e7  8b84244a020000         mov      eax, dword ptr [esp + 0x24a]
0040b3ee  c1e205                 shl      edx, 5
0040b3f1  c1f810                 sar      eax, 0x10
0040b3f4  4a                     dec      edx
0040b3f5  39d0                   cmp      eax, edx
0040b3f7  7e12                   jle      0x40b40b
0040b3f9  66a126875000           mov      ax, word ptr [0x508726]
0040b3ff  c1e005                 shl      eax, 5
0040b402  48                     dec      eax
0040b403  668984244c020000       mov      word ptr [esp + 0x24c], ax
0040b40b  66a124875000           mov      ax, word ptr [0x508724]
0040b411  31c9                   xor      ecx, ecx
0040b413  31db                   xor      ebx, ebx
0040b415  31d2                   xor      edx, edx
0040b417  668b8c244c020000       mov      cx, word ptr [esp + 0x24c]
0040b41f  c1e005                 shl      eax, 5
0040b422  6689fa                 mov      dx, di
0040b425  6689c3                 mov      bx, ax
0040b428  31c0                   xor      eax, eax
0040b42a  e8ea400000             call     0x40f519 ; SetClipping
0040b42f  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040b435  31d2                   xor      edx, edx
0040b437  88da                   mov      dl, bl
0040b439  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b43f  81e2ff000000           and      edx, 0xff
0040b445  b903000000             mov      ecx, 3
0040b44a  89d0                   mov      eax, edx
0040b44c  c1fa1f                 sar      edx, 0x1f
0040b44f  f7f9                   idiv     ecx
0040b451  fec3                   inc      bl
0040b453  0fbff6                 movsx    esi, si
0040b456  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040b45c  01d6                   add      esi, edx
0040b45e  31c0                   xor      eax, eax
0040b460  89fa                   mov      edx, edi
0040b462  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b46a  83c229                 add      edx, 0x29
0040b46d  e846f10000             call     0x41a5b8 ; BatimentEstHabiter
0040b472  6689942460020000       mov      word ptr [esp + 0x260], dx
0040b47a  84c0                   test     al, al
0040b47c  0f8498000000           je       0x40b51a
0040b482  31c0                   xor      eax, eax
0040b484  8a4504                 mov      al, byte ptr [ebp + 4]
0040b487  b901000000             mov      ecx, 1
0040b48c  50                     push     eax
0040b48d  0fbfc7                 movsx    eax, di
0040b490  bb651c0000             mov      ebx, 0x1c65
0040b495  89842498000000         mov      dword ptr [esp + 0x98], eax
0040b49c  0fbfc6                 movsx    eax, si
0040b49f  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040b4a6  89842480000000         mov      dword ptr [esp + 0x80], eax
0040b4ad  e8a30f0500             call     0x45c455 ; PastePlayerCmp
0040b4b2  8b1c24                 mov      ebx, dword ptr [esp]
0040b4b5  66a1808f5000           mov      ax, word ptr [0x508f80]
0040b4bb  01d8                   add      eax, ebx
0040b4bd  8b94245e020000         mov      edx, dword ptr [esp + 0x25e]
0040b4c4  30e4                   xor      ah, ah
0040b4c6  b901000000             mov      ecx, 1
0040b4cb  2407                   and      al, 7
0040b4cd  31db                   xor      ebx, ebx
0040b4cf  05661c0000             add      eax, 0x1c66
0040b4d4  c1fa10                 sar      edx, 0x10
0040b4d7  6689c3                 mov      bx, ax
0040b4da  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040b4de  e864fd0400             call     0x45b247 ; PasteBobCmp
0040b4e3  8b0c24                 mov      ecx, dword ptr [esp]
0040b4e6  66a17c8f5000           mov      ax, word ptr [0x508f7c]
0040b4ec  01c8                   add      eax, ecx
0040b4ee  30e4                   xor      ah, ah
0040b4f0  240f                   and      al, 0xf
0040b4f2  31db                   xor      ebx, ebx
0040b4f4  052d2b0000             add      eax, 0x2b2d
0040b4f9  6689c3                 mov      bx, ax
0040b4fc  89f0                   mov      eax, esi
0040b4fe  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040b505  0526000000             add      eax, 0x26
0040b50a  b901000000             mov      ecx, 1
0040b50f  98                     cwde
0040b510  e832fd0400             call     0x45b247 ; PasteBobCmp
0040b515  e987000000             jmp      0x40b5a1 ;
0040b51a  b901000000             mov      ecx, 1
0040b51f  0fbfc7                 movsx    eax, di
0040b522  bb651c0000             mov      ebx, 0x1c65
0040b527  89842498000000         mov      dword ptr [esp + 0x98], eax
0040b52e  0fbfc6                 movsx    eax, si
0040b531  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040b538  89842494000000         mov      dword ptr [esp + 0x94], eax
0040b53f  e803fd0400             call     0x45b247 ; PasteBobCmp
0040b544  8b84245e020000         mov      eax, dword ptr [esp + 0x25e]
0040b54b  b901000000             mov      ecx, 1
0040b550  c1f810                 sar      eax, 0x10
0040b553  bb661c0000             mov      ebx, 0x1c66
0040b558  8944247c               mov      dword ptr [esp + 0x7c], eax
0040b55c  89c2                   mov      edx, eax
0040b55e  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040b565  e8ddfc0400             call     0x45b247 ; PasteBobCmp
0040b56a  b901000000             mov      ecx, 1
0040b56f  bb651c0000             mov      ebx, 0x1c65
0040b574  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040b57b  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040b582  e829070500             call     0x45bcb0 ; PasteGrisCmp
0040b587  b901000000             mov      ecx, 1
0040b58c  bb661c0000             mov      ebx, 0x1c66
0040b591  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040b595  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040b59c  e80f070500             call     0x45bcb0 ; PasteGrisCmp
0040b5a1  31c0                   xor      eax, eax
0040b5a3  668b4506               mov      ax, word ptr [ebp + 6]
0040b5a7  85c0                   test     eax, eax
0040b5a9  0f8e933d0000           jle      0x40f342
0040b5af  6a13                   push     0x13
0040b5b1  e92c200000             jmp      0x40d5e2 ;
0040b5b6  31c0                   xor      eax, eax
0040b5b8  668b0d26875000         mov      cx, word ptr [0x508726]
0040b5bf  6689d0                 mov      ax, dx
0040b5c2  668b1524875000         mov      dx, word ptr [0x508724]
0040b5c9  c1e105                 shl      ecx, 5
0040b5cc  c1e205                 shl      edx, 5
0040b5cf  49                     dec      ecx
0040b5d0  4a                     dec      edx
0040b5d1  83f864                 cmp      eax, 0x64
0040b5d4  0f8d81000000           jge      0x40b65b
0040b5da  89942494020000         mov      dword ptr [esp + 0x294], edx
0040b5e1  ba64000000             mov      edx, 0x64
0040b5e6  29c2                   sub      edx, eax
0040b5e8  89d0                   mov      eax, edx
0040b5ea  c1e202                 shl      edx, 2
0040b5ed  29c2                   sub      edx, eax
0040b5ef  c1e202                 shl      edx, 2
0040b5f2  29c2                   sub      edx, eax
0040b5f4  c1e203                 shl      edx, 3
0040b5f7  bb64000000             mov      ebx, 0x64
0040b5fc  89d0                   mov      eax, edx
0040b5fe  c1fa1f                 sar      edx, 0x1f
0040b601  f7fb                   idiv     ebx
0040b603  0fbfd7                 movsx    edx, di
0040b606  01d0                   add      eax, edx
0040b608  0fbfd6                 movsx    edx, si
0040b60b  89b42440030000         mov      dword ptr [esp + 0x340], esi
0040b612  85d2                   test     edx, edx
0040b614  7d09                   jge      0x40b61f
0040b616  31d2                   xor      edx, edx
0040b618  89942440030000         mov      dword ptr [esp + 0x340], edx
0040b61f  0fbfd0                 movsx    edx, ax
0040b622  85d2                   test     edx, edx
0040b624  7d02                   jge      0x40b628
0040b626  31c0                   xor      eax, eax
0040b628  81e1ffff0000           and      ecx, 0xffff
0040b62e  31d2                   xor      edx, edx
0040b630  31db                   xor      ebx, ebx
0040b632  6689c2                 mov      dx, ax
0040b635  31c0                   xor      eax, eax
0040b637  668b9c2494020000       mov      bx, word ptr [esp + 0x294]
0040b63f  668b842440030000       mov      ax, word ptr [esp + 0x340]
0040b647  e8cd3e0000             call     0x40f519 ; SetClipping
0040b64c  b901000000             mov      ecx, 1
0040b651  bb641c0000             mov      ebx, 0x1c64
0040b656  e9b7cdffff             jmp      0x408412 ;
0040b65b  89942430040000         mov      dword ptr [esp + 0x430], edx
0040b662  83e864                 sub      eax, 0x64
0040b665  ba64000000             mov      edx, 0x64
0040b66a  29c2                   sub      edx, eax
0040b66c  89d0                   mov      eax, edx
0040b66e  c1e202                 shl      edx, 2
0040b671  29c2                   sub      edx, eax
0040b673  c1e202                 shl      edx, 2
0040b676  29c2                   sub      edx, eax
0040b678  c1e203                 shl      edx, 3
0040b67b  bb64000000             mov      ebx, 0x64
0040b680  89d0                   mov      eax, edx
0040b682  c1fa1f                 sar      edx, 0x1f
0040b685  f7fb                   idiv     ebx
0040b687  0fbfd7                 movsx    edx, di
0040b68a  01d0                   add      eax, edx
0040b68c  31d2                   xor      edx, edx
0040b68e  668b1526875000         mov      dx, word ptr [0x508726]
0040b695  898c242c040000         mov      dword ptr [esp + 0x42c], ecx
0040b69c  c1e205                 shl      edx, 5
0040b69f  0fbfd8                 movsx    ebx, ax
0040b6a2  4a                     dec      edx
0040b6a3  6689b424e0030000       mov      word ptr [esp + 0x3e0], si
0040b6ab  39d3                   cmp      ebx, edx
0040b6ad  7e02                   jle      0x40b6b1
0040b6af  89c8                   mov      eax, ecx
0040b6b1  31c9                   xor      ecx, ecx
0040b6b3  31db                   xor      ebx, ebx
0040b6b5  31d2                   xor      edx, edx
0040b6b7  668b9c2430040000       mov      bx, word ptr [esp + 0x430]
0040b6bf  6689c1                 mov      cx, ax
0040b6c2  31c0                   xor      eax, eax
0040b6c4  e8503e0000             call     0x40f519 ; SetClipping
0040b6c9  0fbfc7                 movsx    eax, di
0040b6cc  b901000000             mov      ecx, 1
0040b6d1  8944247c               mov      dword ptr [esp + 0x7c], eax
0040b6d5  bb641c0000             mov      ebx, 0x1c64
0040b6da  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040b6de  0fbfc6                 movsx    eax, si
0040b6e1  e861fb0400             call     0x45b247 ; PasteBobCmp
0040b6e6  31c0                   xor      eax, eax
0040b6e8  668b8424e0010000       mov      ax, word ptr [esp + 0x1e0]
0040b6f0  ba64000000             mov      edx, 0x64
0040b6f5  83e864                 sub      eax, 0x64
0040b6f8  29c2                   sub      edx, eax
0040b6fa  89d0                   mov      eax, edx
0040b6fc  c1e202                 shl      edx, 2
0040b6ff  29c2                   sub      edx, eax
0040b701  c1e202                 shl      edx, 2
0040b704  29c2                   sub      edx, eax
0040b706  c1e203                 shl      edx, 3
0040b709  bb64000000             mov      ebx, 0x64
0040b70e  89d0                   mov      eax, edx
0040b710  c1fa1f                 sar      edx, 0x1f
0040b713  f7fb                   idiv     ebx
0040b715  0344247c               add      eax, dword ptr [esp + 0x7c]
0040b719  8b9424de030000         mov      edx, dword ptr [esp + 0x3de]
0040b720  c1fa10                 sar      edx, 0x10
0040b723  85d2                   test     edx, edx
0040b725  7d0a                   jge      0x40b731
0040b727  31db                   xor      ebx, ebx
0040b729  66899c24e0030000       mov      word ptr [esp + 0x3e0], bx
0040b731  0fbfd0                 movsx    edx, ax
0040b734  85d2                   test     edx, edx
0040b736  7d02                   jge      0x40b73a
0040b738  31c0                   xor      eax, eax
0040b73a  31c9                   xor      ecx, ecx
0040b73c  31db                   xor      ebx, ebx
0040b73e  31d2                   xor      edx, edx
0040b740  668b8c242c040000       mov      cx, word ptr [esp + 0x42c]
0040b748  6689c2                 mov      dx, ax
0040b74b  31c0                   xor      eax, eax
0040b74d  668b9c2430040000       mov      bx, word ptr [esp + 0x430]
0040b755  668b8424e0030000       mov      ax, word ptr [esp + 0x3e0]
0040b75d  0fbfee                 movsx    ebp, si
0040b760  e8b43d0000             call     0x40f519 ; SetClipping
0040b765  b901000000             mov      ecx, 1
0040b76a  0fbfc7                 movsx    eax, di
0040b76d  bb651c0000             mov      ebx, 0x1c65
0040b772  8944245c               mov      dword ptr [esp + 0x5c], eax
0040b776  89c2                   mov      edx, eax
0040b778  89e8                   mov      eax, ebp
0040b77a  e8c8fa0400             call     0x45b247 ; PasteBobCmp
0040b77f  89f8                   mov      eax, edi
0040b781  0529000000             add      eax, 0x29
0040b786  b901000000             mov      ecx, 1
0040b78b  98                     cwde
0040b78c  bb661c0000             mov      ebx, 0x1c66
0040b791  89442468               mov      dword ptr [esp + 0x68], eax
0040b795  89c2                   mov      edx, eax
0040b797  89e8                   mov      eax, ebp
0040b799  e8a9fa0400             call     0x45b247 ; PasteBobCmp
0040b79e  31c0                   xor      eax, eax
0040b7a0  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b7a8  e80bee0000             call     0x41a5b8 ; BatimentEstHabiter
0040b7ad  84c0                   test     al, al
0040b7af  741a                   je       0x40b7cb
0040b7b1  b901000000             mov      ecx, 1
0040b7b6  89f0                   mov      eax, esi
0040b7b8  bb2d2b0000             mov      ebx, 0x2b2d
0040b7bd  0526000000             add      eax, 0x26
0040b7c2  8b54245c               mov      edx, dword ptr [esp + 0x5c]
0040b7c6  e917c9ffff             jmp      0x4080e2 ;
0040b7cb  b901000000             mov      ecx, 1
0040b7d0  bb651c0000             mov      ebx, 0x1c65
0040b7d5  8b54245c               mov      edx, dword ptr [esp + 0x5c]
0040b7d9  89e8                   mov      eax, ebp
0040b7db  e8d0040500             call     0x45bcb0 ; PasteGrisCmp
0040b7e0  b901000000             mov      ecx, 1
0040b7e5  bb661c0000             mov      ebx, 0x1c66
0040b7ea  8b542468               mov      edx, dword ptr [esp + 0x68]
0040b7ee  e963dbffff             jmp      0x409356 ;
0040b7f3  31c0                   xor      eax, eax
0040b7f5  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040b7fb  668b0424               mov      ax, word ptr [esp]
0040b7ff  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
0040b804  741c                   je       0x40b822
0040b806  31c0                   xor      eax, eax
0040b808  668b0424               mov      ax, word ptr [esp]
0040b80c  668b0442               mov      ax, word ptr [edx + eax*2]
0040b810  25e07f0000             and      eax, 0x7fe0
0040b815  89c3                   mov      ebx, eax
0040b817  81e3ffff0000           and      ebx, 0xffff
0040b81d  c1fb05                 sar      ebx, 5
0040b820  eb05                   jmp      0x40b827 ;
0040b822  bbffff0000             mov      ebx, 0xffff
0040b827  31d2                   xor      edx, edx
0040b829  6689da                 mov      dx, bx
0040b82c  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040b833  81faffff0000           cmp      edx, 0xffff
0040b839  0f84523c0000           je       0x40f491
0040b83f  89d5                   mov      ebp, edx
0040b841  8b742408               mov      esi, dword ptr [esp + 8]
0040b845  c1e504                 shl      ebp, 4
0040b848  8b7c2404               mov      edi, dword ptr [esp + 4]
0040b84c  01d5                   add      ebp, edx
0040b84e  89d0                   mov      eax, edx
0040b850  c1e502                 shl      ebp, 2
0040b853  e88df00000             call     0x41a8e5 ; BatimentGetEtat
0040b858  01d5                   add      ebp, edx
0040b85a  898424c0030000         mov      dword ptr [esp + 0x3c0], eax
0040b861  c1e502                 shl      ebp, 2
0040b864  89c2                   mov      edx, eax
0040b866  81c5c8a04900           add      ebp, 0x49a0c8
0040b86c  31c0                   xor      eax, eax
0040b86e  83ee54                 sub      esi, 0x54
0040b871  8a4505                 mov      al, byte ptr [ebp + 5]
0040b874  83ef49                 sub      edi, 0x49
0040b877  83f805                 cmp      eax, 5
0040b87a  740e                   je       0x40b88a
0040b87c  83f803                 cmp      eax, 3
0040b87f  7409                   je       0x40b88a
0040b881  83f804                 cmp      eax, 4
0040b884  0f85f9020000           jne      0x40bb83
0040b88a  31c0                   xor      eax, eax
0040b88c  8a4505                 mov      al, byte ptr [ebp + 5]
0040b88f  83f803                 cmp      eax, 3
0040b892  0f8512010000           jne      0x40b9aa
0040b898  31c0                   xor      eax, eax
0040b89a  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b8a2  e811ed0000             call     0x41a5b8 ; BatimentEstHabiter
0040b8a7  84c0                   test     al, al
0040b8a9  0f85fb000000           jne      0x40b9aa
0040b8af  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
0040b8b5  31d2                   xor      edx, edx
0040b8b7  88ca                   mov      dl, cl
0040b8b9  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b8bf  81e2ff000000           and      edx, 0xff
0040b8c5  bb03000000             mov      ebx, 3
0040b8ca  89d0                   mov      eax, edx
0040b8cc  c1fa1f                 sar      edx, 0x1f
0040b8cf  f7fb                   idiv     ebx
0040b8d1  0fbfdf                 movsx    ebx, di
0040b8d4  01da                   add      edx, ebx
0040b8d6  83c271                 add      edx, 0x71
0040b8d9  fec1                   inc      cl
0040b8db  6689942418030000       mov      word ptr [esp + 0x318], dx
0040b8e3  31d2                   xor      edx, edx
0040b8e5  88ca                   mov      dl, cl
0040b8e7  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040b8ed  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b8f3  81e2ff000000           and      edx, 0xff
0040b8f9  bf03000000             mov      edi, 3
0040b8fe  89d0                   mov      eax, edx
0040b900  c1fa1f                 sar      edx, 0x1f
0040b903  f7ff                   idiv     edi
0040b905  fec1                   inc      cl
0040b907  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040b90d  01da                   add      edx, ebx
0040b90f  31c0                   xor      eax, eax
0040b911  81c2c8000000           add      edx, 0xc8
0040b917  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040b91e  29c2                   sub      edx, eax
0040b920  0fbfc2                 movsx    eax, dx
0040b923  89d7                   mov      edi, edx
0040b925  85c0                   test     eax, eax
0040b927  7d02                   jge      0x40b92b
0040b929  31d7                   xor      edi, edx
0040b92b  31c0                   xor      eax, eax
0040b92d  66a126875000           mov      ax, word ptr [0x508726]
0040b933  8b942416030000         mov      edx, dword ptr [esp + 0x316]
0040b93a  c1e005                 shl      eax, 5
0040b93d  c1fa10                 sar      edx, 0x10
0040b940  48                     dec      eax
0040b941  39c2                   cmp      edx, eax
0040b943  7e12                   jle      0x40b957
0040b945  66a126875000           mov      ax, word ptr [0x508726]
0040b94b  c1e005                 shl      eax, 5
0040b94e  48                     dec      eax
0040b94f  6689842418030000       mov      word ptr [esp + 0x318], ax
0040b957  66a124875000           mov      ax, word ptr [0x508724]
0040b95d  31c9                   xor      ecx, ecx
0040b95f  31db                   xor      ebx, ebx
0040b961  31d2                   xor      edx, edx
0040b963  668b8c2418030000       mov      cx, word ptr [esp + 0x318]
0040b96b  c1e005                 shl      eax, 5
0040b96e  6689fa                 mov      dx, di
0040b971  6689c3                 mov      bx, ax
0040b974  31c0                   xor      eax, eax
0040b976  e89e3b0000             call     0x40f519 ; SetClipping
0040b97b  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040b981  31d2                   xor      edx, edx
0040b983  88da                   mov      dl, bl
0040b985  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040b98b  81e2ff000000           and      edx, 0xff
0040b991  b903000000             mov      ecx, 3
0040b996  89d0                   mov      eax, edx
0040b998  c1fa1f                 sar      edx, 0x1f
0040b99b  f7f9                   idiv     ecx
0040b99d  fec3                   inc      bl
0040b99f  0fbff6                 movsx    esi, si
0040b9a2  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040b9a8  01d6                   add      esi, edx
0040b9aa  89f2                   mov      edx, esi
0040b9ac  83c256                 add      edx, 0x56
0040b9af  6689942420040000       mov      word ptr [esp + 0x420], dx
0040b9b7  89fa                   mov      edx, edi
0040b9b9  83c225                 add      edx, 0x25
0040b9bc  6689942438040000       mov      word ptr [esp + 0x438], dx
0040b9c4  89f2                   mov      edx, esi
0040b9c6  83c202                 add      edx, 2
0040b9c9  31c0                   xor      eax, eax
0040b9cb  66899424dc030000       mov      word ptr [esp + 0x3dc], dx
0040b9d3  89fa                   mov      edx, edi
0040b9d5  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040b9dd  83c21c                 add      edx, 0x1c
0040b9e0  e8d3eb0000             call     0x41a5b8 ; BatimentEstHabiter
0040b9e5  6689942418040000       mov      word ptr [esp + 0x418], dx
0040b9ed  84c0                   test     al, al
0040b9ef  0f848e000000           je       0x40ba83
0040b9f5  b901000000             mov      ecx, 1
0040b9fa  31c0                   xor      eax, eax
0040b9fc  bb531c0000             mov      ebx, 0x1c53
0040ba01  8a4504                 mov      al, byte ptr [ebp + 4]
0040ba04  0fbfd7                 movsx    edx, di
0040ba07  50                     push     eax
0040ba08  0fbfc6                 movsx    eax, si
0040ba0b  e8450a0500             call     0x45c455 ; PastePlayerCmp
0040ba10  8b0c24                 mov      ecx, dword ptr [esp]
0040ba13  66a1808f5000           mov      ax, word ptr [0x508f80]
0040ba19  01c8                   add      eax, ecx
0040ba1b  30e4                   xor      ah, ah
0040ba1d  8b942416040000         mov      edx, dword ptr [esp + 0x416]
0040ba24  2407                   and      al, 7
0040ba26  31db                   xor      ebx, ebx
0040ba28  05541c0000             add      eax, 0x1c54
0040ba2d  c1fa10                 sar      edx, 0x10
0040ba30  6689c3                 mov      bx, ax
0040ba33  8b8424da030000         mov      eax, dword ptr [esp + 0x3da]
0040ba3a  b901000000             mov      ecx, 1
0040ba3f  c1f810                 sar      eax, 0x10
0040ba42  e800f80400             call     0x45b247 ; PasteBobCmp
0040ba47  8b1424                 mov      edx, dword ptr [esp]
0040ba4a  66a1808f5000           mov      ax, word ptr [0x508f80]
0040ba50  01d0                   add      eax, edx
0040ba52  30e4                   xor      ah, ah
0040ba54  b901000000             mov      ecx, 1
0040ba59  2407                   and      al, 7
0040ba5b  31db                   xor      ebx, ebx
0040ba5d  055c1c0000             add      eax, 0x1c5c
0040ba62  8b942436040000         mov      edx, dword ptr [esp + 0x436]
0040ba69  6689c3                 mov      bx, ax
0040ba6c  8b84241e040000         mov      eax, dword ptr [esp + 0x41e]
0040ba73  c1fa10                 sar      edx, 0x10
0040ba76  c1f810                 sar      eax, 0x10
0040ba79  e8c9f70400             call     0x45b247 ; PasteBobCmp
0040ba7e  e9eb000000             jmp      0x40bb6e ;
0040ba83  b901000000             mov      ecx, 1
0040ba88  0fbfc7                 movsx    eax, di
0040ba8b  bb531c0000             mov      ebx, 0x1c53
0040ba90  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040ba97  0fbfc6                 movsx    eax, si
0040ba9a  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040baa1  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040baa8  e89af70400             call     0x45b247 ; PasteBobCmp
0040baad  8b842416040000         mov      eax, dword ptr [esp + 0x416]
0040bab4  c1f810                 sar      eax, 0x10
0040bab7  b901000000             mov      ecx, 1
0040babc  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040bac3  8b8424da030000         mov      eax, dword ptr [esp + 0x3da]
0040baca  bb541c0000             mov      ebx, 0x1c54
0040bacf  c1f810                 sar      eax, 0x10
0040bad2  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040bad9  89842498000000         mov      dword ptr [esp + 0x98], eax
0040bae0  e862f70400             call     0x45b247 ; PasteBobCmp
0040bae5  8b842436040000         mov      eax, dword ptr [esp + 0x436]
0040baec  c1f810                 sar      eax, 0x10
0040baef  b901000000             mov      ecx, 1
0040baf4  89842494000000         mov      dword ptr [esp + 0x94], eax
0040bafb  8b84241e040000         mov      eax, dword ptr [esp + 0x41e]
0040bb02  bb5c1c0000             mov      ebx, 0x1c5c
0040bb07  c1f810                 sar      eax, 0x10
0040bb0a  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040bb11  8944247c               mov      dword ptr [esp + 0x7c], eax
0040bb15  e82df70400             call     0x45b247 ; PasteBobCmp
0040bb1a  b901000000             mov      ecx, 1
0040bb1f  bb531c0000             mov      ebx, 0x1c53
0040bb24  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040bb2b  8b8424b4000000         mov      eax, dword ptr [esp + 0xb4]
0040bb32  e879010500             call     0x45bcb0 ; PasteGrisCmp
0040bb37  b901000000             mov      ecx, 1
0040bb3c  bb541c0000             mov      ebx, 0x1c54
0040bb41  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040bb48  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040bb4f  e85c010500             call     0x45bcb0 ; PasteGrisCmp
0040bb54  b901000000             mov      ecx, 1
0040bb59  bb5c1c0000             mov      ebx, 0x1c5c
0040bb5e  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040bb65  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040bb69  e842010500             call     0x45bcb0 ; PasteGrisCmp
0040bb6e  31c0                   xor      eax, eax
0040bb70  668b4506               mov      ax, word ptr [ebp + 6]
0040bb74  85c0                   test     eax, eax
0040bb76  0f8ec6370000           jle      0x40f342
0040bb7c  6a10                   push     0x10
0040bb7e  e95f1a0000             jmp      0x40d5e2 ;
0040bb83  31c0                   xor      eax, eax
0040bb85  668b0d26875000         mov      cx, word ptr [0x508726]
0040bb8c  6689d0                 mov      ax, dx
0040bb8f  668b1524875000         mov      dx, word ptr [0x508724]
0040bb96  c1e105                 shl      ecx, 5
0040bb99  c1e205                 shl      edx, 5
0040bb9c  49                     dec      ecx
0040bb9d  4a                     dec      edx
0040bb9e  83f864                 cmp      eax, 0x64
0040bba1  0f8d81000000           jge      0x40bc28
0040bba7  899424c4020000         mov      dword ptr [esp + 0x2c4], edx
0040bbae  ba64000000             mov      edx, 0x64
0040bbb3  29c2                   sub      edx, eax
0040bbb5  89d0                   mov      eax, edx
0040bbb7  c1e003                 shl      eax, 3
0040bbba  29d0                   sub      eax, edx
0040bbbc  c1e004                 shl      eax, 4
0040bbbf  01c2                   add      edx, eax
0040bbc1  bb64000000             mov      ebx, 0x64
0040bbc6  89d0                   mov      eax, edx
0040bbc8  c1fa1f                 sar      edx, 0x1f
0040bbcb  f7fb                   idiv     ebx
0040bbcd  0fbfd7                 movsx    edx, di
0040bbd0  01d0                   add      eax, edx
0040bbd2  89c2                   mov      edx, eax
0040bbd4  0fbfc6                 movsx    eax, si
0040bbd7  89b4246c030000         mov      dword ptr [esp + 0x36c], esi
0040bbde  85c0                   test     eax, eax
0040bbe0  7d09                   jge      0x40bbeb
0040bbe2  31db                   xor      ebx, ebx
0040bbe4  899c246c030000         mov      dword ptr [esp + 0x36c], ebx
0040bbeb  0fbfc2                 movsx    eax, dx
0040bbee  85c0                   test     eax, eax
0040bbf0  7d02                   jge      0x40bbf4
0040bbf2  31d2                   xor      edx, edx
0040bbf4  31db                   xor      ebx, ebx
0040bbf6  81e1ffff0000           and      ecx, 0xffff
0040bbfc  668b9c24c4020000       mov      bx, word ptr [esp + 0x2c4]
0040bc04  31c0                   xor      eax, eax
0040bc06  81e2ffff0000           and      edx, 0xffff
0040bc0c  668b84246c030000       mov      ax, word ptr [esp + 0x36c]
0040bc14  e800390000             call     0x40f519 ; SetClipping
0040bc19  b901000000             mov      ecx, 1
0040bc1e  bb521c0000             mov      ebx, 0x1c52
0040bc23  e9eac7ffff             jmp      0x408412 ;
0040bc28  89942468040000         mov      dword ptr [esp + 0x468], edx
0040bc2f  83e864                 sub      eax, 0x64
0040bc32  ba64000000             mov      edx, 0x64
0040bc37  29c2                   sub      edx, eax
0040bc39  89d0                   mov      eax, edx
0040bc3b  c1e203                 shl      edx, 3
0040bc3e  29c2                   sub      edx, eax
0040bc40  c1e204                 shl      edx, 4
0040bc43  01c2                   add      edx, eax
0040bc45  bb64000000             mov      ebx, 0x64
0040bc4a  89d0                   mov      eax, edx
0040bc4c  c1fa1f                 sar      edx, 0x1f
0040bc4f  f7fb                   idiv     ebx
0040bc51  0fbfd7                 movsx    edx, di
0040bc54  01d0                   add      eax, edx
0040bc56  31d2                   xor      edx, edx
0040bc58  668b1526875000         mov      dx, word ptr [0x508726]
0040bc5f  898c24c8020000         mov      dword ptr [esp + 0x2c8], ecx
0040bc66  c1e205                 shl      edx, 5
0040bc69  0fbfd8                 movsx    ebx, ax
0040bc6c  4a                     dec      edx
0040bc6d  6689b42458020000       mov      word ptr [esp + 0x258], si
0040bc75  39d3                   cmp      ebx, edx
0040bc77  7e02                   jle      0x40bc7b
0040bc79  89c8                   mov      eax, ecx
0040bc7b  31c9                   xor      ecx, ecx
0040bc7d  31db                   xor      ebx, ebx
0040bc7f  31d2                   xor      edx, edx
0040bc81  668b9c2468040000       mov      bx, word ptr [esp + 0x468]
0040bc89  6689c1                 mov      cx, ax
0040bc8c  31c0                   xor      eax, eax
0040bc8e  0fbfef                 movsx    ebp, di
0040bc91  e883380000             call     0x40f519 ; SetClipping
0040bc96  b901000000             mov      ecx, 1
0040bc9b  bb521c0000             mov      ebx, 0x1c52
0040bca0  0fbfc6                 movsx    eax, si
0040bca3  89ea                   mov      edx, ebp
0040bca5  e89df50400             call     0x45b247 ; PasteBobCmp
0040bcaa  31c0                   xor      eax, eax
0040bcac  668b8424c0030000       mov      ax, word ptr [esp + 0x3c0]
0040bcb4  ba64000000             mov      edx, 0x64
0040bcb9  83e864                 sub      eax, 0x64
0040bcbc  29c2                   sub      edx, eax
0040bcbe  89d0                   mov      eax, edx
0040bcc0  c1e003                 shl      eax, 3
0040bcc3  29d0                   sub      eax, edx
0040bcc5  c1e004                 shl      eax, 4
0040bcc8  01c2                   add      edx, eax
0040bcca  bb64000000             mov      ebx, 0x64
0040bccf  89d0                   mov      eax, edx
0040bcd1  c1fa1f                 sar      edx, 0x1f
0040bcd4  f7fb                   idiv     ebx
0040bcd6  8b942456020000         mov      edx, dword ptr [esp + 0x256]
0040bcdd  c1fa10                 sar      edx, 0x10
0040bce0  01e8                   add      eax, ebp
0040bce2  85d2                   test     edx, edx
0040bce4  7d0a                   jge      0x40bcf0
0040bce6  31d2                   xor      edx, edx
0040bce8  6689942458020000       mov      word ptr [esp + 0x258], dx
0040bcf0  0fbfd0                 movsx    edx, ax
0040bcf3  85d2                   test     edx, edx
0040bcf5  7d02                   jge      0x40bcf9
0040bcf7  31c0                   xor      eax, eax
0040bcf9  31c9                   xor      ecx, ecx
0040bcfb  31db                   xor      ebx, ebx
0040bcfd  31d2                   xor      edx, edx
0040bcff  668b8c24c8020000       mov      cx, word ptr [esp + 0x2c8]
0040bd07  6689c2                 mov      dx, ax
0040bd0a  31c0                   xor      eax, eax
0040bd0c  668b9c2468040000       mov      bx, word ptr [esp + 0x468]
0040bd14  668b842458020000       mov      ax, word ptr [esp + 0x258]
0040bd1c  e8f8370000             call     0x40f519 ; SetClipping
0040bd21  b901000000             mov      ecx, 1
0040bd26  0fbfc7                 movsx    eax, di
0040bd29  bb531c0000             mov      ebx, 0x1c53
0040bd2e  89442420               mov      dword ptr [esp + 0x20], eax
0040bd32  0fbfc6                 movsx    eax, si
0040bd35  8b542420               mov      edx, dword ptr [esp + 0x20]
0040bd39  898424d8000000         mov      dword ptr [esp + 0xd8], eax
0040bd40  e802f50400             call     0x45b247 ; PasteBobCmp
0040bd45  89f8                   mov      eax, edi
0040bd47  051c000000             add      eax, 0x1c
0040bd4c  0fbfe8                 movsx    ebp, ax
0040bd4f  89f0                   mov      eax, esi
0040bd51  b901000000             mov      ecx, 1
0040bd56  0502000000             add      eax, 2
0040bd5b  bb541c0000             mov      ebx, 0x1c54
0040bd60  98                     cwde
0040bd61  89ea                   mov      edx, ebp
0040bd63  898424a4000000         mov      dword ptr [esp + 0xa4], eax
0040bd6a  e8d8f40400             call     0x45b247 ; PasteBobCmp
0040bd6f  89f8                   mov      eax, edi
0040bd71  0525000000             add      eax, 0x25
0040bd76  98                     cwde
0040bd77  898424dc000000         mov      dword ptr [esp + 0xdc], eax
0040bd7e  89f0                   mov      eax, esi
0040bd80  b901000000             mov      ecx, 1
0040bd85  0556000000             add      eax, 0x56
0040bd8a  bb5c1c0000             mov      ebx, 0x1c5c
0040bd8f  98                     cwde
0040bd90  8b9424dc000000         mov      edx, dword ptr [esp + 0xdc]
0040bd97  89842464010000         mov      dword ptr [esp + 0x164], eax
0040bd9e  e8a4f40400             call     0x45b247 ; PasteBobCmp
0040bda3  31c0                   xor      eax, eax
0040bda5  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040bdad  e806e80000             call     0x41a5b8 ; BatimentEstHabiter
0040bdb2  84c0                   test     al, al
0040bdb4  0f8588350000           jne      0x40f342
0040bdba  b901000000             mov      ecx, 1
0040bdbf  bb531c0000             mov      ebx, 0x1c53
0040bdc4  8b542420               mov      edx, dword ptr [esp + 0x20]
0040bdc8  8b8424d8000000         mov      eax, dword ptr [esp + 0xd8]
0040bdcf  e8dcfe0400             call     0x45bcb0 ; PasteGrisCmp
0040bdd4  b901000000             mov      ecx, 1
0040bdd9  bb541c0000             mov      ebx, 0x1c54
0040bdde  8b8424a4000000         mov      eax, dword ptr [esp + 0xa4]
0040bde5  89ea                   mov      edx, ebp
0040bde7  e8c4fe0400             call     0x45bcb0 ; PasteGrisCmp
0040bdec  b901000000             mov      ecx, 1
0040bdf1  bb5c1c0000             mov      ebx, 0x1c5c
0040bdf6  8b9424dc000000         mov      edx, dword ptr [esp + 0xdc]
0040bdfd  8b842464010000         mov      eax, dword ptr [esp + 0x164]
0040be04  e964c7ffff             jmp      0x40856d ;
0040be09  31d2                   xor      edx, edx
0040be0b  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040be10  668b1424               mov      dx, word ptr [esp]
0040be14  f644500180             test     byte ptr [eax + edx*2 + 1], 0x80
0040be19  7421                   je       0x40be3c
0040be1b  31c0                   xor      eax, eax
0040be1d  6689d0                 mov      ax, dx
0040be20  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040be26  668b0442               mov      ax, word ptr [edx + eax*2]
0040be2a  25e07f0000             and      eax, 0x7fe0
0040be2f  89c3                   mov      ebx, eax
0040be31  81e3ffff0000           and      ebx, 0xffff
0040be37  c1fb05                 sar      ebx, 5
0040be3a  eb05                   jmp      0x40be41 ;
0040be3c  bbffff0000             mov      ebx, 0xffff
0040be41  31c0                   xor      eax, eax
0040be43  6689d8                 mov      ax, bx
0040be46  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040be4d  3dffff0000             cmp      eax, 0xffff
0040be52  0f8439360000           je       0x40f491
0040be58  89c5                   mov      ebp, eax
0040be5a  c1e504                 shl      ebp, 4
0040be5d  01c5                   add      ebp, eax
0040be5f  8b742408               mov      esi, dword ptr [esp + 8]
0040be63  c1e502                 shl      ebp, 2
0040be66  8b7c2404               mov      edi, dword ptr [esp + 4]
0040be6a  01c5                   add      ebp, eax
0040be6c  e874ea0000             call     0x41a8e5 ; BatimentGetEtat
0040be71  c1e502                 shl      ebp, 2
0040be74  89c2                   mov      edx, eax
0040be76  898424c4030000         mov      dword ptr [esp + 0x3c4], eax
0040be7d  81c5c8a04900           add      ebp, 0x49a0c8
0040be83  31c0                   xor      eax, eax
0040be85  83ee06                 sub      esi, 6
0040be88  8a4505                 mov      al, byte ptr [ebp + 5]
0040be8b  83ef21                 sub      edi, 0x21
0040be8e  83f805                 cmp      eax, 5
0040be91  740e                   je       0x40bea1
0040be93  83f803                 cmp      eax, 3
0040be96  7409                   je       0x40bea1
0040be98  83f804                 cmp      eax, 4
0040be9b  0f8544010000           jne      0x40bfe5
0040bea1  31c0                   xor      eax, eax
0040bea3  8a4505                 mov      al, byte ptr [ebp + 5]
0040bea6  83f803                 cmp      eax, 3
0040bea9  0f85f8000000           jne      0x40bfa7
0040beaf  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
0040beb5  31d2                   xor      edx, edx
0040beb7  88ca                   mov      dl, cl
0040beb9  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040bebf  81e2ff000000           and      edx, 0xff
0040bec5  89c3                   mov      ebx, eax
0040bec7  89d0                   mov      eax, edx
0040bec9  c1fa1f                 sar      edx, 0x1f
0040becc  f7fb                   idiv     ebx
0040bece  0fbfdf                 movsx    ebx, di
0040bed1  01da                   add      edx, ebx
0040bed3  83c245                 add      edx, 0x45
0040bed6  fec1                   inc      cl
0040bed8  668994247c040000       mov      word ptr [esp + 0x47c], dx
0040bee0  31d2                   xor      edx, edx
0040bee2  88ca                   mov      dl, cl
0040bee4  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040beea  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040bef0  81e2ff000000           and      edx, 0xff
0040bef6  bf03000000             mov      edi, 3
0040befb  89d0                   mov      eax, edx
0040befd  c1fa1f                 sar      edx, 0x1f
0040bf00  f7ff                   idiv     edi
0040bf02  fec1                   inc      cl
0040bf04  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040bf0a  01da                   add      edx, ebx
0040bf0c  31ff                   xor      edi, edi
0040bf0e  81c2c8000000           add      edx, 0xc8
0040bf14  668bbd84000000         mov      di, word ptr [ebp + 0x84]
0040bf1b  29fa                   sub      edx, edi
0040bf1d  0fbfc2                 movsx    eax, dx
0040bf20  89d7                   mov      edi, edx
0040bf22  85c0                   test     eax, eax
0040bf24  7d02                   jge      0x40bf28
0040bf26  31d7                   xor      edi, edx
0040bf28  31c0                   xor      eax, eax
0040bf2a  66a126875000           mov      ax, word ptr [0x508726]
0040bf30  8b94247a040000         mov      edx, dword ptr [esp + 0x47a]
0040bf37  c1e005                 shl      eax, 5
0040bf3a  c1fa10                 sar      edx, 0x10
0040bf3d  48                     dec      eax
0040bf3e  39c2                   cmp      edx, eax
0040bf40  7e12                   jle      0x40bf54
0040bf42  66a126875000           mov      ax, word ptr [0x508726]
0040bf48  c1e005                 shl      eax, 5
0040bf4b  48                     dec      eax
0040bf4c  668984247c040000       mov      word ptr [esp + 0x47c], ax
0040bf54  66a124875000           mov      ax, word ptr [0x508724]
0040bf5a  31c9                   xor      ecx, ecx
0040bf5c  31db                   xor      ebx, ebx
0040bf5e  31d2                   xor      edx, edx
0040bf60  668b8c247c040000       mov      cx, word ptr [esp + 0x47c]
0040bf68  c1e005                 shl      eax, 5
0040bf6b  6689fa                 mov      dx, di
0040bf6e  6689c3                 mov      bx, ax
0040bf71  31c0                   xor      eax, eax
0040bf73  e8a1350000             call     0x40f519 ; SetClipping
0040bf78  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040bf7e  31d2                   xor      edx, edx
0040bf80  88da                   mov      dl, bl
0040bf82  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040bf88  81e2ff000000           and      edx, 0xff
0040bf8e  b903000000             mov      ecx, 3
0040bf93  89d0                   mov      eax, edx
0040bf95  c1fa1f                 sar      edx, 0x1f
0040bf98  f7f9                   idiv     ecx
0040bf9a  fec3                   inc      bl
0040bf9c  0fbff6                 movsx    esi, si
0040bf9f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040bfa5  01d6                   add      esi, edx
0040bfa7  8b1424                 mov      edx, dword ptr [esp]
0040bfaa  66a1848f5000           mov      ax, word ptr [0x508f84]
0040bfb0  01d0                   add      eax, edx
0040bfb2  30e4                   xor      ah, ah
0040bfb4  b901000000             mov      ecx, 1
0040bfb9  2407                   and      al, 7
0040bfbb  31db                   xor      ebx, ebx
0040bfbd  05701c0000             add      eax, 0x1c70
0040bfc2  0fbfd7                 movsx    edx, di
0040bfc5  6689c3                 mov      bx, ax
0040bfc8  0fbfc6                 movsx    eax, si
0040bfcb  e877f20400             call     0x45b247 ; PasteBobCmp
0040bfd0  31c0                   xor      eax, eax
0040bfd2  668b4506               mov      ax, word ptr [ebp + 6]
0040bfd6  85c0                   test     eax, eax
0040bfd8  0f8e64330000           jle      0x40f342
0040bfde  6a11                   push     0x11
0040bfe0  e9fd150000             jmp      0x40d5e2 ;
0040bfe5  31c0                   xor      eax, eax
0040bfe7  668b0d26875000         mov      cx, word ptr [0x508726]
0040bfee  6689d0                 mov      ax, dx
0040bff1  668b1524875000         mov      dx, word ptr [0x508724]
0040bff8  c1e105                 shl      ecx, 5
0040bffb  c1e205                 shl      edx, 5
0040bffe  49                     dec      ecx
0040bfff  4a                     dec      edx
0040c000  83f864                 cmp      eax, 0x64
0040c003  0f8d81000000           jge      0x40c08a
0040c009  899424e8010000         mov      dword ptr [esp + 0x1e8], edx
0040c010  ba64000000             mov      edx, 0x64
0040c015  29c2                   sub      edx, eax
0040c017  89d0                   mov      eax, edx
0040c019  c1e204                 shl      edx, 4
0040c01c  01c2                   add      edx, eax
0040c01e  c1e202                 shl      edx, 2
0040c021  01c2                   add      edx, eax
0040c023  bb64000000             mov      ebx, 0x64
0040c028  89d0                   mov      eax, edx
0040c02a  c1fa1f                 sar      edx, 0x1f
0040c02d  f7fb                   idiv     ebx
0040c02f  0fbfd7                 movsx    edx, di
0040c032  01d0                   add      eax, edx
0040c034  89c2                   mov      edx, eax
0040c036  0fbfc6                 movsx    eax, si
0040c039  89b42444040000         mov      dword ptr [esp + 0x444], esi
0040c040  85c0                   test     eax, eax
0040c042  7d09                   jge      0x40c04d
0040c044  31c0                   xor      eax, eax
0040c046  89842444040000         mov      dword ptr [esp + 0x444], eax
0040c04d  0fbfc2                 movsx    eax, dx
0040c050  85c0                   test     eax, eax
0040c052  7d02                   jge      0x40c056
0040c054  31d2                   xor      edx, edx
0040c056  31db                   xor      ebx, ebx
0040c058  81e1ffff0000           and      ecx, 0xffff
0040c05e  668b9c24e8010000       mov      bx, word ptr [esp + 0x1e8]
0040c066  31c0                   xor      eax, eax
0040c068  81e2ffff0000           and      edx, 0xffff
0040c06e  668b842444040000       mov      ax, word ptr [esp + 0x444]
0040c076  e89e340000             call     0x40f519 ; SetClipping
0040c07b  b901000000             mov      ecx, 1
0040c080  bb6f1c0000             mov      ebx, 0x1c6f
0040c085  e988c3ffff             jmp      0x408412 ;
0040c08a  899424ec030000         mov      dword ptr [esp + 0x3ec], edx
0040c091  83e864                 sub      eax, 0x64
0040c094  ba64000000             mov      edx, 0x64
0040c099  29c2                   sub      edx, eax
0040c09b  89d0                   mov      eax, edx
0040c09d  c1e004                 shl      eax, 4
0040c0a0  01d0                   add      eax, edx
0040c0a2  c1e002                 shl      eax, 2
0040c0a5  01c2                   add      edx, eax
0040c0a7  bb64000000             mov      ebx, 0x64
0040c0ac  89d0                   mov      eax, edx
0040c0ae  c1fa1f                 sar      edx, 0x1f
0040c0b1  f7fb                   idiv     ebx
0040c0b3  0fbfd7                 movsx    edx, di
0040c0b6  01d0                   add      eax, edx
0040c0b8  31d2                   xor      edx, edx
0040c0ba  668b1526875000         mov      dx, word ptr [0x508726]
0040c0c1  898c24f4010000         mov      dword ptr [esp + 0x1f4], ecx
0040c0c8  c1e205                 shl      edx, 5
0040c0cb  0fbfd8                 movsx    ebx, ax
0040c0ce  4a                     dec      edx
0040c0cf  6689b42494040000       mov      word ptr [esp + 0x494], si
0040c0d7  39d3                   cmp      ebx, edx
0040c0d9  7e02                   jle      0x40c0dd
0040c0db  89c8                   mov      eax, ecx
0040c0dd  31c9                   xor      ecx, ecx
0040c0df  31db                   xor      ebx, ebx
0040c0e1  31d2                   xor      edx, edx
0040c0e3  668b9c24ec030000       mov      bx, word ptr [esp + 0x3ec]
0040c0eb  6689c1                 mov      cx, ax
0040c0ee  31c0                   xor      eax, eax
0040c0f0  e824340000             call     0x40f519 ; SetClipping
0040c0f5  0fbfc7                 movsx    eax, di
0040c0f8  b901000000             mov      ecx, 1
0040c0fd  8944247c               mov      dword ptr [esp + 0x7c], eax
0040c101  bb6f1c0000             mov      ebx, 0x1c6f
0040c106  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040c10a  0fbfc6                 movsx    eax, si
0040c10d  e835f10400             call     0x45b247 ; PasteBobCmp
0040c112  31c0                   xor      eax, eax
0040c114  668b8424c4030000       mov      ax, word ptr [esp + 0x3c4]
0040c11c  ba64000000             mov      edx, 0x64
0040c121  83e864                 sub      eax, 0x64
0040c124  29c2                   sub      edx, eax
0040c126  89d0                   mov      eax, edx
0040c128  c1e204                 shl      edx, 4
0040c12b  01c2                   add      edx, eax
0040c12d  c1e202                 shl      edx, 2
0040c130  01c2                   add      edx, eax
0040c132  bb64000000             mov      ebx, 0x64
0040c137  89d0                   mov      eax, edx
0040c139  c1fa1f                 sar      edx, 0x1f
0040c13c  f7fb                   idiv     ebx
0040c13e  8b942492040000         mov      edx, dword ptr [esp + 0x492]
0040c145  8b6c247c               mov      ebp, dword ptr [esp + 0x7c]
0040c149  c1fa10                 sar      edx, 0x10
0040c14c  01e8                   add      eax, ebp
0040c14e  85d2                   test     edx, edx
0040c150  7d0a                   jge      0x40c15c
0040c152  31db                   xor      ebx, ebx
0040c154  66899c2494040000       mov      word ptr [esp + 0x494], bx
0040c15c  0fbfd0                 movsx    edx, ax
0040c15f  85d2                   test     edx, edx
0040c161  7d02                   jge      0x40c165
0040c163  31c0                   xor      eax, eax
0040c165  31c9                   xor      ecx, ecx
0040c167  31db                   xor      ebx, ebx
0040c169  31d2                   xor      edx, edx
0040c16b  668b8c24f4010000       mov      cx, word ptr [esp + 0x1f4]
0040c173  6689c2                 mov      dx, ax
0040c176  31c0                   xor      eax, eax
0040c178  668b9c24ec030000       mov      bx, word ptr [esp + 0x3ec]
0040c180  668b842494040000       mov      ax, word ptr [esp + 0x494]
0040c188  e88c330000             call     0x40f519 ; SetClipping
0040c18d  b901000000             mov      ecx, 1
0040c192  bb701c0000             mov      ebx, 0x1c70
0040c197  e976c2ffff             jmp      0x408412 ;
0040c19c  31c0                   xor      eax, eax
0040c19e  668b0424               mov      ax, word ptr [esp]
0040c1a2  8d1400                 lea      edx, [eax + eax]
0040c1a5  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040c1aa  f644020180             test     byte ptr [edx + eax + 1], 0x80
0040c1af  7422                   je       0x40c1d3
0040c1b1  31c0                   xor      eax, eax
0040c1b3  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040c1b9  668b0424               mov      ax, word ptr [esp]
0040c1bd  668b0442               mov      ax, word ptr [edx + eax*2]
0040c1c1  25e07f0000             and      eax, 0x7fe0
0040c1c6  89c3                   mov      ebx, eax
0040c1c8  81e3ffff0000           and      ebx, 0xffff
0040c1ce  c1fb05                 sar      ebx, 5
0040c1d1  eb05                   jmp      0x40c1d8 ;
0040c1d3  bbffff0000             mov      ebx, 0xffff
0040c1d8  31d2                   xor      edx, edx
0040c1da  6689da                 mov      dx, bx
0040c1dd  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040c1e4  81faffff0000           cmp      edx, 0xffff
0040c1ea  0f84a1320000           je       0x40f491
0040c1f0  89d5                   mov      ebp, edx
0040c1f2  8b742408               mov      esi, dword ptr [esp + 8]
0040c1f6  c1e504                 shl      ebp, 4
0040c1f9  8b7c2404               mov      edi, dword ptr [esp + 4]
0040c1fd  01d5                   add      ebp, edx
0040c1ff  89d0                   mov      eax, edx
0040c201  c1e502                 shl      ebp, 2
0040c204  e8dce60000             call     0x41a8e5 ; BatimentGetEtat
0040c209  01d5                   add      ebp, edx
0040c20b  898424dc010000         mov      dword ptr [esp + 0x1dc], eax
0040c212  c1e502                 shl      ebp, 2
0040c215  89c2                   mov      edx, eax
0040c217  81c5c8a04900           add      ebp, 0x49a0c8
0040c21d  31c0                   xor      eax, eax
0040c21f  83ee2f                 sub      esi, 0x2f
0040c222  8a4505                 mov      al, byte ptr [ebp + 5]
0040c225  83ef2c                 sub      edi, 0x2c
0040c228  83f805                 cmp      eax, 5
0040c22b  7410                   je       0x40c23d
0040c22d  83f803                 cmp      eax, 3
0040c230  740b                   je       0x40c23d
0040c232  83f804                 cmp      eax, 4
0040c235  7406                   je       0x40c23d
0040c237  0f85a4010000           jne      0x40c3e1
0040c23d  31c0                   xor      eax, eax
0040c23f  8a4505                 mov      al, byte ptr [ebp + 5]
0040c242  83f803                 cmp      eax, 3
0040c245  0f8510010000           jne      0x40c35b
0040c24b  31c0                   xor      eax, eax
0040c24d  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040c255  e85ee30000             call     0x41a5b8 ; BatimentEstHabiter
0040c25a  84c0                   test     al, al
0040c25c  0f85f9000000           jne      0x40c35b
0040c262  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040c268  31d2                   xor      edx, edx
0040c26a  88da                   mov      dl, bl
0040c26c  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c272  81e2ff000000           and      edx, 0xff
0040c278  b903000000             mov      ecx, 3
0040c27d  89d0                   mov      eax, edx
0040c27f  c1fa1f                 sar      edx, 0x1f
0040c282  f7f9                   idiv     ecx
0040c284  0fbfcf                 movsx    ecx, di
0040c287  01ca                   add      edx, ecx
0040c289  83c24d                 add      edx, 0x4d
0040c28c  fec3                   inc      bl
0040c28e  6689942478020000       mov      word ptr [esp + 0x278], dx
0040c296  31d2                   xor      edx, edx
0040c298  88da                   mov      dl, bl
0040c29a  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040c2a0  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c2a6  81e2ff000000           and      edx, 0xff
0040c2ac  bf03000000             mov      edi, 3
0040c2b1  89d0                   mov      eax, edx
0040c2b3  c1fa1f                 sar      edx, 0x1f
0040c2b6  f7ff                   idiv     edi
0040c2b8  fec3                   inc      bl
0040c2ba  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040c2c0  01ca                   add      edx, ecx
0040c2c2  31c0                   xor      eax, eax
0040c2c4  8dbac8000000           lea      edi, [edx + 0xc8]
0040c2ca  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040c2d1  29c7                   sub      edi, eax
0040c2d3  0fbfc7                 movsx    eax, di
0040c2d6  85c0                   test     eax, eax
0040c2d8  7d02                   jge      0x40c2dc
0040c2da  31ff                   xor      edi, edi
0040c2dc  31c0                   xor      eax, eax
0040c2de  66a126875000           mov      ax, word ptr [0x508726]
0040c2e4  8b942476020000         mov      edx, dword ptr [esp + 0x276]
0040c2eb  c1e005                 shl      eax, 5
0040c2ee  c1fa10                 sar      edx, 0x10
0040c2f1  48                     dec      eax
0040c2f2  39c2                   cmp      edx, eax
0040c2f4  7e12                   jle      0x40c308
0040c2f6  66a126875000           mov      ax, word ptr [0x508726]
0040c2fc  c1e005                 shl      eax, 5
0040c2ff  48                     dec      eax
0040c300  6689842478020000       mov      word ptr [esp + 0x278], ax
0040c308  66a124875000           mov      ax, word ptr [0x508724]
0040c30e  31c9                   xor      ecx, ecx
0040c310  31db                   xor      ebx, ebx
0040c312  31d2                   xor      edx, edx
0040c314  668b8c2478020000       mov      cx, word ptr [esp + 0x278]
0040c31c  c1e005                 shl      eax, 5
0040c31f  6689fa                 mov      dx, di
0040c322  6689c3                 mov      bx, ax
0040c325  31c0                   xor      eax, eax
0040c327  e8ed310000             call     0x40f519 ; SetClipping
0040c32c  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040c332  31d2                   xor      edx, edx
0040c334  88da                   mov      dl, bl
0040c336  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c33c  81e2ff000000           and      edx, 0xff
0040c342  b903000000             mov      ecx, 3
0040c347  89d0                   mov      eax, edx
0040c349  c1fa1f                 sar      edx, 0x1f
0040c34c  f7f9                   idiv     ecx
0040c34e  fec3                   inc      bl
0040c350  0fbff6                 movsx    esi, si
0040c353  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040c359  01d6                   add      esi, edx
0040c35b  31c0                   xor      eax, eax
0040c35d  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040c365  e84ee20000             call     0x41a5b8 ; BatimentEstHabiter
0040c36a  84c0                   test     al, al
0040c36c  741d                   je       0x40c38b
0040c36e  b901000000             mov      ecx, 1
0040c373  31c0                   xor      eax, eax
0040c375  bb791c0000             mov      ebx, 0x1c79
0040c37a  8a4504                 mov      al, byte ptr [ebp + 4]
0040c37d  0fbfd7                 movsx    edx, di
0040c380  50                     push     eax
0040c381  0fbfc6                 movsx    eax, si
0040c384  e8cc000500             call     0x45c455 ; PastePlayerCmp
0040c389  eb41                   jmp      0x40c3cc ;
0040c38b  b901000000             mov      ecx, 1
0040c390  0fbfc7                 movsx    eax, di
0040c393  bb791c0000             mov      ebx, 0x1c79
0040c398  89842494000000         mov      dword ptr [esp + 0x94], eax
0040c39f  0fbfc6                 movsx    eax, si
0040c3a2  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040c3a9  8944247c               mov      dword ptr [esp + 0x7c], eax
0040c3ad  e895ee0400             call     0x45b247 ; PasteBobCmp
0040c3b2  b901000000             mov      ecx, 1
0040c3b7  bb791c0000             mov      ebx, 0x1c79
0040c3bc  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040c3c3  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040c3c7  e8e4f80400             call     0x45bcb0 ; PasteGrisCmp
0040c3cc  31c0                   xor      eax, eax
0040c3ce  668b4506               mov      ax, word ptr [ebp + 6]
0040c3d2  85c0                   test     eax, eax
0040c3d4  0f8e682f0000           jle      0x40f342
0040c3da  6a04                   push     4
0040c3dc  e901120000             jmp      0x40d5e2 ;
0040c3e1  31c0                   xor      eax, eax
0040c3e3  668b0d26875000         mov      cx, word ptr [0x508726]
0040c3ea  6689d0                 mov      ax, dx
0040c3ed  668b1524875000         mov      dx, word ptr [0x508724]
0040c3f4  c1e105                 shl      ecx, 5
0040c3f7  c1e205                 shl      edx, 5
0040c3fa  49                     dec      ecx
0040c3fb  4a                     dec      edx
0040c3fc  83f864                 cmp      eax, 0x64
0040c3ff  7d75                   jge      0x40c476
0040c401  89942400020000         mov      dword ptr [esp + 0x200], edx
0040c408  ba64000000             mov      edx, 0x64
0040c40d  29c2                   sub      edx, eax
0040c40f  6bd24d                 imul     edx, edx, 0x4d
0040c412  bb64000000             mov      ebx, 0x64
0040c417  89d0                   mov      eax, edx
0040c419  c1fa1f                 sar      edx, 0x1f
0040c41c  f7fb                   idiv     ebx
0040c41e  0fbfd7                 movsx    edx, di
0040c421  01d0                   add      eax, edx
0040c423  0fbfd6                 movsx    edx, si
0040c426  89b42470030000         mov      dword ptr [esp + 0x370], esi
0040c42d  85d2                   test     edx, edx
0040c42f  7d09                   jge      0x40c43a
0040c431  31d2                   xor      edx, edx
0040c433  89942470030000         mov      dword ptr [esp + 0x370], edx
0040c43a  0fbfd0                 movsx    edx, ax
0040c43d  85d2                   test     edx, edx
0040c43f  7d02                   jge      0x40c443
0040c441  31c0                   xor      eax, eax
0040c443  81e1ffff0000           and      ecx, 0xffff
0040c449  31d2                   xor      edx, edx
0040c44b  31db                   xor      ebx, ebx
0040c44d  6689c2                 mov      dx, ax
0040c450  31c0                   xor      eax, eax
0040c452  668b9c2400020000       mov      bx, word ptr [esp + 0x200]
0040c45a  668b842470030000       mov      ax, word ptr [esp + 0x370]
0040c462  e8b2300000             call     0x40f519 ; SetClipping
0040c467  b901000000             mov      ecx, 1
0040c46c  bb781c0000             mov      ebx, 0x1c78
0040c471  e99cbfffff             jmp      0x408412 ;
0040c476  89942444030000         mov      dword ptr [esp + 0x344], edx
0040c47d  83e864                 sub      eax, 0x64
0040c480  ba64000000             mov      edx, 0x64
0040c485  29c2                   sub      edx, eax
0040c487  6bd24d                 imul     edx, edx, 0x4d
0040c48a  bb64000000             mov      ebx, 0x64
0040c48f  89d0                   mov      eax, edx
0040c491  c1fa1f                 sar      edx, 0x1f
0040c494  f7fb                   idiv     ebx
0040c496  0fbfd7                 movsx    edx, di
0040c499  01d0                   add      eax, edx
0040c49b  31d2                   xor      edx, edx
0040c49d  668b1526875000         mov      dx, word ptr [0x508726]
0040c4a4  89d3                   mov      ebx, edx
0040c4a6  898c2498030000         mov      dword ptr [esp + 0x398], ecx
0040c4ad  c1e305                 shl      ebx, 5
0040c4b0  0fbfd0                 movsx    edx, ax
0040c4b3  4b                     dec      ebx
0040c4b4  6689b4248c040000       mov      word ptr [esp + 0x48c], si
0040c4bc  39da                   cmp      edx, ebx
0040c4be  7e02                   jle      0x40c4c2
0040c4c0  89c8                   mov      eax, ecx
0040c4c2  31c9                   xor      ecx, ecx
0040c4c4  31db                   xor      ebx, ebx
0040c4c6  31d2                   xor      edx, edx
0040c4c8  668b9c2444030000       mov      bx, word ptr [esp + 0x344]
0040c4d0  6689c1                 mov      cx, ax
0040c4d3  31c0                   xor      eax, eax
0040c4d5  0fbfef                 movsx    ebp, di
0040c4d8  e83c300000             call     0x40f519 ; SetClipping
0040c4dd  b901000000             mov      ecx, 1
0040c4e2  bb781c0000             mov      ebx, 0x1c78
0040c4e7  0fbfc6                 movsx    eax, si
0040c4ea  89ea                   mov      edx, ebp
0040c4ec  e856ed0400             call     0x45b247 ; PasteBobCmp
0040c4f1  31c0                   xor      eax, eax
0040c4f3  668b8424dc010000       mov      ax, word ptr [esp + 0x1dc]
0040c4fb  ba64000000             mov      edx, 0x64
0040c500  83e864                 sub      eax, 0x64
0040c503  29c2                   sub      edx, eax
0040c505  6bd24d                 imul     edx, edx, 0x4d
0040c508  bb64000000             mov      ebx, 0x64
0040c50d  89d0                   mov      eax, edx
0040c50f  c1fa1f                 sar      edx, 0x1f
0040c512  f7fb                   idiv     ebx
0040c514  8b94248a040000         mov      edx, dword ptr [esp + 0x48a]
0040c51b  c1fa10                 sar      edx, 0x10
0040c51e  01e8                   add      eax, ebp
0040c520  85d2                   test     edx, edx
0040c522  7d0a                   jge      0x40c52e
0040c524  31db                   xor      ebx, ebx
0040c526  66899c248c040000       mov      word ptr [esp + 0x48c], bx
0040c52e  0fbfd0                 movsx    edx, ax
0040c531  85d2                   test     edx, edx
0040c533  7d02                   jge      0x40c537
0040c535  31c0                   xor      eax, eax
0040c537  31c9                   xor      ecx, ecx
0040c539  31db                   xor      ebx, ebx
0040c53b  31d2                   xor      edx, edx
0040c53d  668b8c2498030000       mov      cx, word ptr [esp + 0x398]
0040c545  6689c2                 mov      dx, ax
0040c548  31c0                   xor      eax, eax
0040c54a  668b9c2444030000       mov      bx, word ptr [esp + 0x344]
0040c552  668b84248c040000       mov      ax, word ptr [esp + 0x48c]
0040c55a  0fbfee                 movsx    ebp, si
0040c55d  e8b72f0000             call     0x40f519 ; SetClipping
0040c562  b901000000             mov      ecx, 1
0040c567  0fbfc7                 movsx    eax, di
0040c56a  bb791c0000             mov      ebx, 0x1c79
0040c56f  89442478               mov      dword ptr [esp + 0x78], eax
0040c573  89c2                   mov      edx, eax
0040c575  89e8                   mov      eax, ebp
0040c577  e8cbec0400             call     0x45b247 ; PasteBobCmp
0040c57c  31c0                   xor      eax, eax
0040c57e  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040c586  e82de00000             call     0x41a5b8 ; BatimentEstHabiter
0040c58b  84c0                   test     al, al
0040c58d  0f85af2d0000           jne      0x40f342
0040c593  b901000000             mov      ecx, 1
0040c598  bb791c0000             mov      ebx, 0x1c79
0040c59d  8b542478               mov      edx, dword ptr [esp + 0x78]
0040c5a1  e9b0cdffff             jmp      0x409356 ;
0040c5a6  31c0                   xor      eax, eax
0040c5a8  668b0424               mov      ax, word ptr [esp]
0040c5ac  8d1400                 lea      edx, [eax + eax]
0040c5af  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040c5b4  f644020180             test     byte ptr [edx + eax + 1], 0x80
0040c5b9  7422                   je       0x40c5dd
0040c5bb  31c0                   xor      eax, eax
0040c5bd  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040c5c3  668b0424               mov      ax, word ptr [esp]
0040c5c7  668b0442               mov      ax, word ptr [edx + eax*2]
0040c5cb  25e07f0000             and      eax, 0x7fe0
0040c5d0  89c3                   mov      ebx, eax
0040c5d2  81e3ffff0000           and      ebx, 0xffff
0040c5d8  c1fb05                 sar      ebx, 5
0040c5db  eb05                   jmp      0x40c5e2 ;
0040c5dd  bbffff0000             mov      ebx, 0xffff
0040c5e2  31d2                   xor      edx, edx
0040c5e4  6689da                 mov      dx, bx
0040c5e7  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040c5ee  81faffff0000           cmp      edx, 0xffff
0040c5f4  0f84972e0000           je       0x40f491
0040c5fa  89d5                   mov      ebp, edx
0040c5fc  8b742408               mov      esi, dword ptr [esp + 8]
0040c600  c1e504                 shl      ebp, 4
0040c603  8b7c2404               mov      edi, dword ptr [esp + 4]
0040c607  01d5                   add      ebp, edx
0040c609  89d0                   mov      eax, edx
0040c60b  c1e502                 shl      ebp, 2
0040c60e  e8d2e20000             call     0x41a8e5 ; BatimentGetEtat
0040c613  01d5                   add      ebp, edx
0040c615  898424f0010000         mov      dword ptr [esp + 0x1f0], eax
0040c61c  c1e502                 shl      ebp, 2
0040c61f  89c2                   mov      edx, eax
0040c621  81c5c8a04900           add      ebp, 0x49a0c8
0040c627  31c0                   xor      eax, eax
0040c629  81ee9d000000           sub      esi, 0x9d
0040c62f  8a4505                 mov      al, byte ptr [ebp + 5]
0040c632  83ef3e                 sub      edi, 0x3e
0040c635  83f805                 cmp      eax, 5
0040c638  740e                   je       0x40c648
0040c63a  83f803                 cmp      eax, 3
0040c63d  7409                   je       0x40c648
0040c63f  83f804                 cmp      eax, 4
0040c642  0f8563030000           jne      0x40c9ab
0040c648  31c0                   xor      eax, eax
0040c64a  8a4505                 mov      al, byte ptr [ebp + 5]
0040c64d  83f803                 cmp      eax, 3
0040c650  0f8511010000           jne      0x40c767
0040c656  31c0                   xor      eax, eax
0040c658  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040c660  e853df0000             call     0x41a5b8 ; BatimentEstHabiter
0040c665  84c0                   test     al, al
0040c667  0f85fa000000           jne      0x40c767
0040c66d  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
0040c673  31d2                   xor      edx, edx
0040c675  88ca                   mov      dl, cl
0040c677  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c67d  81e2ff000000           and      edx, 0xff
0040c683  bb03000000             mov      ebx, 3
0040c688  89d0                   mov      eax, edx
0040c68a  c1fa1f                 sar      edx, 0x1f
0040c68d  f7fb                   idiv     ebx
0040c68f  0fbfdf                 movsx    ebx, di
0040c692  fec1                   inc      cl
0040c694  8d0413                 lea      eax, [ebx + edx]
0040c697  31d2                   xor      edx, edx
0040c699  83c062                 add      eax, 0x62
0040c69c  88ca                   mov      dl, cl
0040c69e  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040c6a4  668984247c030000       mov      word ptr [esp + 0x37c], ax
0040c6ac  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c6b2  81e2ff000000           and      edx, 0xff
0040c6b8  bf03000000             mov      edi, 3
0040c6bd  89d0                   mov      eax, edx
0040c6bf  c1fa1f                 sar      edx, 0x1f
0040c6c2  f7ff                   idiv     edi
0040c6c4  fec1                   inc      cl
0040c6c6  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040c6cc  01da                   add      edx, ebx
0040c6ce  31c0                   xor      eax, eax
0040c6d0  8dbac8000000           lea      edi, [edx + 0xc8]
0040c6d6  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040c6dd  29c7                   sub      edi, eax
0040c6df  0fbfc7                 movsx    eax, di
0040c6e2  85c0                   test     eax, eax
0040c6e4  7d02                   jge      0x40c6e8
0040c6e6  31ff                   xor      edi, edi
0040c6e8  31c0                   xor      eax, eax
0040c6ea  66a126875000           mov      ax, word ptr [0x508726]
0040c6f0  8b94247a030000         mov      edx, dword ptr [esp + 0x37a]
0040c6f7  c1e005                 shl      eax, 5
0040c6fa  c1fa10                 sar      edx, 0x10
0040c6fd  48                     dec      eax
0040c6fe  39c2                   cmp      edx, eax
0040c700  7e12                   jle      0x40c714
0040c702  66a126875000           mov      ax, word ptr [0x508726]
0040c708  c1e005                 shl      eax, 5
0040c70b  48                     dec      eax
0040c70c  668984247c030000       mov      word ptr [esp + 0x37c], ax
0040c714  66a124875000           mov      ax, word ptr [0x508724]
0040c71a  31c9                   xor      ecx, ecx
0040c71c  31db                   xor      ebx, ebx
0040c71e  31d2                   xor      edx, edx
0040c720  668b8c247c030000       mov      cx, word ptr [esp + 0x37c]
0040c728  c1e005                 shl      eax, 5
0040c72b  6689fa                 mov      dx, di
0040c72e  6689c3                 mov      bx, ax
0040c731  31c0                   xor      eax, eax
0040c733  e8e12d0000             call     0x40f519 ; SetClipping
0040c738  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040c73e  31d2                   xor      edx, edx
0040c740  88da                   mov      dl, bl
0040c742  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040c748  81e2ff000000           and      edx, 0xff
0040c74e  b903000000             mov      ecx, 3
0040c753  89d0                   mov      eax, edx
0040c755  c1fa1f                 sar      edx, 0x1f
0040c758  f7f9                   idiv     ecx
0040c75a  fec3                   inc      bl
0040c75c  0fbff6                 movsx    esi, si
0040c75f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040c765  01d6                   add      esi, edx
0040c767  31db                   xor      ebx, ebx
0040c769  668b9c2410020000       mov      bx, word ptr [esp + 0x210]
0040c771  89d8                   mov      eax, ebx
0040c773  e840de0000             call     0x41a5b8 ; BatimentEstHabiter
0040c778  84c0                   test     al, al
0040c77a  0f84c2000000           je       0x40c842
0040c780  31c0                   xor      eax, eax
0040c782  8a4505                 mov      al, byte ptr [ebp + 5]
0040c785  83f804                 cmp      eax, 4
0040c788  7513                   jne      0x40c79d
0040c78a  8b542402               mov      edx, dword ptr [esp + 2]
0040c78e  8b442406               mov      eax, dword ptr [esp + 6]
0040c792  c1fa10                 sar      edx, 0x10
0040c795  c1f810                 sar      eax, 0x10
0040c798  e80566ffff             call     0x402da2 ; AffRentrerHangar
0040c79d  31c0                   xor      eax, eax
0040c79f  b901000000             mov      ecx, 1
0040c7a4  8a4504                 mov      al, byte ptr [ebp + 4]
0040c7a7  bb7b1c0000             mov      ebx, 0x1c7b
0040c7ac  50                     push     eax
0040c7ad  0fbfc6                 movsx    eax, si
0040c7b0  0fbfd7                 movsx    edx, di
0040c7b3  89842498000000         mov      dword ptr [esp + 0x98], eax
0040c7ba  e896fc0400             call     0x45c455 ; PastePlayerCmp
0040c7bf  30e4                   xor      ah, ah
0040c7c1  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c7c4  31db                   xor      ebx, ebx
0040c7c6  057c1c0000             add      eax, 0x1c7c
0040c7cb  6689c3                 mov      bx, ax
0040c7ce  89f8                   mov      eax, edi
0040c7d0  0537000000             add      eax, 0x37
0040c7d5  98                     cwde
0040c7d6  b901000000             mov      ecx, 1
0040c7db  8944247c               mov      dword ptr [esp + 0x7c], eax
0040c7df  89c2                   mov      edx, eax
0040c7e1  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040c7e8  e85aea0400             call     0x45b247 ; PasteBobCmp
0040c7ed  30e4                   xor      ah, ah
0040c7ef  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c7f2  31db                   xor      ebx, ebx
0040c7f4  05841c0000             add      eax, 0x1c84
0040c7f9  6689c3                 mov      bx, ax
0040c7fc  89f0                   mov      eax, esi
0040c7fe  b901000000             mov      ecx, 1
0040c803  0589000000             add      eax, 0x89
0040c808  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040c80c  98                     cwde
0040c80d  e835ea0400             call     0x45b247 ; PasteBobCmp
0040c812  30e4                   xor      ah, ah
0040c814  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c817  31db                   xor      ebx, ebx
0040c819  058c1c0000             add      eax, 0x1c8c
0040c81e  6689c3                 mov      bx, ax
0040c821  89f8                   mov      eax, edi
0040c823  0528000000             add      eax, 0x28
0040c828  0fbfd0                 movsx    edx, ax
0040c82b  89f0                   mov      eax, esi
0040c82d  0531000000             add      eax, 0x31
0040c832  b901000000             mov      ecx, 1
0040c837  98                     cwde
0040c838  e80aea0400             call     0x45b247 ; PasteBobCmp
0040c83d  e954010000             jmp      0x40c996 ;
0040c842  b901000000             mov      ecx, 1
0040c847  0fbfc7                 movsx    eax, di
0040c84a  bb7b1c0000             mov      ebx, 0x1c7b
0040c84f  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040c856  0fbfc6                 movsx    eax, si
0040c859  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040c860  89842498000000         mov      dword ptr [esp + 0x98], eax
0040c867  e8dbe90400             call     0x45b247 ; PasteBobCmp
0040c86c  30e4                   xor      ah, ah
0040c86e  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c871  31db                   xor      ebx, ebx
0040c873  057c1c0000             add      eax, 0x1c7c
0040c878  6689c3                 mov      bx, ax
0040c87b  89f8                   mov      eax, edi
0040c87d  0537000000             add      eax, 0x37
0040c882  98                     cwde
0040c883  b901000000             mov      ecx, 1
0040c888  89842494000000         mov      dword ptr [esp + 0x94], eax
0040c88f  89c2                   mov      edx, eax
0040c891  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040c898  e8aae90400             call     0x45b247 ; PasteBobCmp
0040c89d  30e4                   xor      ah, ah
0040c89f  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c8a2  31db                   xor      ebx, ebx
0040c8a4  05841c0000             add      eax, 0x1c84
0040c8a9  6689c3                 mov      bx, ax
0040c8ac  89f0                   mov      eax, esi
0040c8ae  0589000000             add      eax, 0x89
0040c8b3  b901000000             mov      ecx, 1
0040c8b8  98                     cwde
0040c8b9  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040c8c0  8944247c               mov      dword ptr [esp + 0x7c], eax
0040c8c4  e87ee90400             call     0x45b247 ; PasteBobCmp
0040c8c9  30e4                   xor      ah, ah
0040c8cb  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c8ce  31db                   xor      ebx, ebx
0040c8d0  058c1c0000             add      eax, 0x1c8c
0040c8d5  6689c3                 mov      bx, ax
0040c8d8  89f8                   mov      eax, edi
0040c8da  0528000000             add      eax, 0x28
0040c8df  98                     cwde
0040c8e0  89842480000000         mov      dword ptr [esp + 0x80], eax
0040c8e7  89f0                   mov      eax, esi
0040c8e9  0531000000             add      eax, 0x31
0040c8ee  b901000000             mov      ecx, 1
0040c8f3  98                     cwde
0040c8f4  8b942480000000         mov      edx, dword ptr [esp + 0x80]
0040c8fb  89842424010000         mov      dword ptr [esp + 0x124], eax
0040c902  e840e90400             call     0x45b247 ; PasteBobCmp
0040c907  b901000000             mov      ecx, 1
0040c90c  bb7b1c0000             mov      ebx, 0x1c7b
0040c911  8b94249c000000         mov      edx, dword ptr [esp + 0x9c]
0040c918  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040c91f  e88cf30400             call     0x45bcb0 ; PasteGrisCmp
0040c924  30e4                   xor      ah, ah
0040c926  b901000000             mov      ecx, 1
0040c92b  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c92e  31db                   xor      ebx, ebx
0040c930  057c1c0000             add      eax, 0x1c7c
0040c935  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040c93c  6689c3                 mov      bx, ax
0040c93f  8b842498000000         mov      eax, dword ptr [esp + 0x98]
0040c946  e865f30400             call     0x45bcb0 ; PasteGrisCmp
0040c94b  30e4                   xor      ah, ah
0040c94d  b901000000             mov      ecx, 1
0040c952  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c955  31db                   xor      ebx, ebx
0040c957  05841c0000             add      eax, 0x1c84
0040c95c  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040c963  6689c3                 mov      bx, ax
0040c966  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040c96a  e841f30400             call     0x45bcb0 ; PasteGrisCmp
0040c96f  30e4                   xor      ah, ah
0040c971  b901000000             mov      ecx, 1
0040c976  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040c979  31db                   xor      ebx, ebx
0040c97b  058c1c0000             add      eax, 0x1c8c
0040c980  8b942480000000         mov      edx, dword ptr [esp + 0x80]
0040c987  6689c3                 mov      bx, ax
0040c98a  8b842424010000         mov      eax, dword ptr [esp + 0x124]
0040c991  e81af30400             call     0x45bcb0 ; PasteGrisCmp
0040c996  31c0                   xor      eax, eax
0040c998  668b4506               mov      ax, word ptr [ebp + 6]
0040c99c  85c0                   test     eax, eax
0040c99e  0f8e9e290000           jle      0x40f342
0040c9a4  6a08                   push     8
0040c9a6  e9370c0000             jmp      0x40d5e2 ;
0040c9ab  31c0                   xor      eax, eax
0040c9ad  668b0d26875000         mov      cx, word ptr [0x508726]
0040c9b4  6689d0                 mov      ax, dx
0040c9b7  668b1524875000         mov      dx, word ptr [0x508724]
0040c9be  c1e105                 shl      ecx, 5
0040c9c1  c1e205                 shl      edx, 5
0040c9c4  49                     dec      ecx
0040c9c5  4a                     dec      edx
0040c9c6  83f864                 cmp      eax, 0x64
0040c9c9  0f8d80000000           jge      0x40ca4f
0040c9cf  89942430020000         mov      dword ptr [esp + 0x230], edx
0040c9d6  ba64000000             mov      edx, 0x64
0040c9db  29c2                   sub      edx, eax
0040c9dd  89d0                   mov      eax, edx
0040c9df  c1e202                 shl      edx, 2
0040c9e2  29c2                   sub      edx, eax
0040c9e4  c1e204                 shl      edx, 4
0040c9e7  01c2                   add      edx, eax
0040c9e9  01d2                   add      edx, edx
0040c9eb  bb64000000             mov      ebx, 0x64
0040c9f0  89d0                   mov      eax, edx
0040c9f2  c1fa1f                 sar      edx, 0x1f
0040c9f5  f7fb                   idiv     ebx
0040c9f7  0fbfd7                 movsx    edx, di
0040c9fa  01d0                   add      eax, edx
0040c9fc  0fbfd6                 movsx    edx, si
0040c9ff  89b42404020000         mov      dword ptr [esp + 0x204], esi
0040ca06  85d2                   test     edx, edx
0040ca08  7d09                   jge      0x40ca13
0040ca0a  31d2                   xor      edx, edx
0040ca0c  89942404020000         mov      dword ptr [esp + 0x204], edx
0040ca13  0fbfd0                 movsx    edx, ax
0040ca16  85d2                   test     edx, edx
0040ca18  7d02                   jge      0x40ca1c
0040ca1a  31c0                   xor      eax, eax
0040ca1c  81e1ffff0000           and      ecx, 0xffff
0040ca22  31d2                   xor      edx, edx
0040ca24  31db                   xor      ebx, ebx
0040ca26  6689c2                 mov      dx, ax
0040ca29  31c0                   xor      eax, eax
0040ca2b  668b9c2430020000       mov      bx, word ptr [esp + 0x230]
0040ca33  668b842404020000       mov      ax, word ptr [esp + 0x204]
0040ca3b  e8d92a0000             call     0x40f519 ; SetClipping
0040ca40  b901000000             mov      ecx, 1
0040ca45  bb7a1c0000             mov      ebx, 0x1c7a
0040ca4a  e9c3b9ffff             jmp      0x408412 ;
0040ca4f  899424fc030000         mov      dword ptr [esp + 0x3fc], edx
0040ca56  83e864                 sub      eax, 0x64
0040ca59  ba64000000             mov      edx, 0x64
0040ca5e  29c2                   sub      edx, eax
0040ca60  89d0                   mov      eax, edx
0040ca62  c1e202                 shl      edx, 2
0040ca65  29c2                   sub      edx, eax
0040ca67  c1e204                 shl      edx, 4
0040ca6a  01c2                   add      edx, eax
0040ca6c  01d2                   add      edx, edx
0040ca6e  bb64000000             mov      ebx, 0x64
0040ca73  89d0                   mov      eax, edx
0040ca75  c1fa1f                 sar      edx, 0x1f
0040ca78  f7fb                   idiv     ebx
0040ca7a  0fbfd7                 movsx    edx, di
0040ca7d  01d0                   add      eax, edx
0040ca7f  31d2                   xor      edx, edx
0040ca81  668b1526875000         mov      dx, word ptr [0x508726]
0040ca88  898c2498020000         mov      dword ptr [esp + 0x298], ecx
0040ca8f  c1e205                 shl      edx, 5
0040ca92  0fbfd8                 movsx    ebx, ax
0040ca95  4a                     dec      edx
0040ca96  6689b424a4020000       mov      word ptr [esp + 0x2a4], si
0040ca9e  39d3                   cmp      ebx, edx
0040caa0  7e02                   jle      0x40caa4
0040caa2  89c8                   mov      eax, ecx
0040caa4  31c9                   xor      ecx, ecx
0040caa6  31db                   xor      ebx, ebx
0040caa8  31d2                   xor      edx, edx
0040caaa  668b9c24fc030000       mov      bx, word ptr [esp + 0x3fc]
0040cab2  6689c1                 mov      cx, ax
0040cab5  31c0                   xor      eax, eax
0040cab7  e85d2a0000             call     0x40f519 ; SetClipping
0040cabc  0fbfc7                 movsx    eax, di
0040cabf  b901000000             mov      ecx, 1
0040cac4  89442454               mov      dword ptr [esp + 0x54], eax
0040cac8  bb7a1c0000             mov      ebx, 0x1c7a
0040cacd  8b542454               mov      edx, dword ptr [esp + 0x54]
0040cad1  0fbfc6                 movsx    eax, si
0040cad4  e86ee70400             call     0x45b247 ; PasteBobCmp
0040cad9  31c0                   xor      eax, eax
0040cadb  668b8424f0010000       mov      ax, word ptr [esp + 0x1f0]
0040cae3  ba64000000             mov      edx, 0x64
0040cae8  83e864                 sub      eax, 0x64
0040caeb  29c2                   sub      edx, eax
0040caed  89d0                   mov      eax, edx
0040caef  c1e202                 shl      edx, 2
0040caf2  29c2                   sub      edx, eax
0040caf4  c1e204                 shl      edx, 4
0040caf7  01c2                   add      edx, eax
0040caf9  01d2                   add      edx, edx
0040cafb  bb64000000             mov      ebx, 0x64
0040cb00  89d0                   mov      eax, edx
0040cb02  c1fa1f                 sar      edx, 0x1f
0040cb05  f7fb                   idiv     ebx
0040cb07  8b9424a2020000         mov      edx, dword ptr [esp + 0x2a2]
0040cb0e  8b4c2454               mov      ecx, dword ptr [esp + 0x54]
0040cb12  c1fa10                 sar      edx, 0x10
0040cb15  01c8                   add      eax, ecx
0040cb17  85d2                   test     edx, edx
0040cb19  7d0a                   jge      0x40cb25
0040cb1b  31c9                   xor      ecx, ecx
0040cb1d  66898c24a4020000       mov      word ptr [esp + 0x2a4], cx
0040cb25  0fbfd0                 movsx    edx, ax
0040cb28  85d2                   test     edx, edx
0040cb2a  7d02                   jge      0x40cb2e
0040cb2c  31c0                   xor      eax, eax
0040cb2e  31c9                   xor      ecx, ecx
0040cb30  31db                   xor      ebx, ebx
0040cb32  31d2                   xor      edx, edx
0040cb34  668b8c2498020000       mov      cx, word ptr [esp + 0x298]
0040cb3c  6689c2                 mov      dx, ax
0040cb3f  31c0                   xor      eax, eax
0040cb41  668b9c24fc030000       mov      bx, word ptr [esp + 0x3fc]
0040cb49  668b8424a4020000       mov      ax, word ptr [esp + 0x2a4]
0040cb51  0fbfee                 movsx    ebp, si
0040cb54  e8c0290000             call     0x40f519 ; SetClipping
0040cb59  b901000000             mov      ecx, 1
0040cb5e  0fbfc7                 movsx    eax, di
0040cb61  bb7b1c0000             mov      ebx, 0x1c7b
0040cb66  8984240c010000         mov      dword ptr [esp + 0x10c], eax
0040cb6d  89c2                   mov      edx, eax
0040cb6f  89e8                   mov      eax, ebp
0040cb71  e8d1e60400             call     0x45b247 ; PasteBobCmp
0040cb76  89f8                   mov      eax, edi
0040cb78  0537000000             add      eax, 0x37
0040cb7d  b901000000             mov      ecx, 1
0040cb82  98                     cwde
0040cb83  bb7c1c0000             mov      ebx, 0x1c7c
0040cb88  89442460               mov      dword ptr [esp + 0x60], eax
0040cb8c  89c2                   mov      edx, eax
0040cb8e  89e8                   mov      eax, ebp
0040cb90  e8b2e60400             call     0x45b247 ; PasteBobCmp
0040cb95  89f0                   mov      eax, esi
0040cb97  b901000000             mov      ecx, 1
0040cb9c  0589000000             add      eax, 0x89
0040cba1  bb841c0000             mov      ebx, 0x1c84
0040cba6  98                     cwde
0040cba7  8b542460               mov      edx, dword ptr [esp + 0x60]
0040cbab  898424b0000000         mov      dword ptr [esp + 0xb0], eax
0040cbb2  e890e60400             call     0x45b247 ; PasteBobCmp
0040cbb7  89f8                   mov      eax, edi
0040cbb9  0528000000             add      eax, 0x28
0040cbbe  98                     cwde
0040cbbf  898424ac010000         mov      dword ptr [esp + 0x1ac], eax
0040cbc6  89f0                   mov      eax, esi
0040cbc8  b901000000             mov      ecx, 1
0040cbcd  0531000000             add      eax, 0x31
0040cbd2  bb8c1c0000             mov      ebx, 0x1c8c
0040cbd7  98                     cwde
0040cbd8  8b9424ac010000         mov      edx, dword ptr [esp + 0x1ac]
0040cbdf  89442444               mov      dword ptr [esp + 0x44], eax
0040cbe3  e85fe60400             call     0x45b247 ; PasteBobCmp
0040cbe8  31c0                   xor      eax, eax
0040cbea  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040cbf2  e8c1d90000             call     0x41a5b8 ; BatimentEstHabiter
0040cbf7  84c0                   test     al, al
0040cbf9  0f8543270000           jne      0x40f342
0040cbff  b901000000             mov      ecx, 1
0040cc04  bb7b1c0000             mov      ebx, 0x1c7b
0040cc09  8b94240c010000         mov      edx, dword ptr [esp + 0x10c]
0040cc10  89e8                   mov      eax, ebp
0040cc12  e899f00400             call     0x45bcb0 ; PasteGrisCmp
0040cc17  b901000000             mov      ecx, 1
0040cc1c  bb7c1c0000             mov      ebx, 0x1c7c
0040cc21  8b542460               mov      edx, dword ptr [esp + 0x60]
0040cc25  89e8                   mov      eax, ebp
0040cc27  e884f00400             call     0x45bcb0 ; PasteGrisCmp
0040cc2c  b901000000             mov      ecx, 1
0040cc31  bb841c0000             mov      ebx, 0x1c84
0040cc36  8b542460               mov      edx, dword ptr [esp + 0x60]
0040cc3a  8b8424b0000000         mov      eax, dword ptr [esp + 0xb0]
0040cc41  e86af00400             call     0x45bcb0 ; PasteGrisCmp
0040cc46  b901000000             mov      ecx, 1
0040cc4b  bb8c1c0000             mov      ebx, 0x1c8c
0040cc50  8b9424ac010000         mov      edx, dword ptr [esp + 0x1ac]
0040cc57  8b442444               mov      eax, dword ptr [esp + 0x44]
0040cc5b  e90db9ffff             jmp      0x40856d ;
0040cc60  31c0                   xor      eax, eax
0040cc62  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040cc68  668b0424               mov      ax, word ptr [esp]
0040cc6c  f644420180             test     byte ptr [edx + eax*2 + 1], 0x80
0040cc71  741c                   je       0x40cc8f
0040cc73  31c0                   xor      eax, eax
0040cc75  668b0424               mov      ax, word ptr [esp]
0040cc79  668b0442               mov      ax, word ptr [edx + eax*2]
0040cc7d  25e07f0000             and      eax, 0x7fe0
0040cc82  89c3                   mov      ebx, eax
0040cc84  81e3ffff0000           and      ebx, 0xffff
0040cc8a  c1fb05                 sar      ebx, 5
0040cc8d  eb05                   jmp      0x40cc94 ;
0040cc8f  bbffff0000             mov      ebx, 0xffff
0040cc94  31c0                   xor      eax, eax
0040cc96  6689d8                 mov      ax, bx
0040cc99  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040cca0  3dffff0000             cmp      eax, 0xffff
0040cca5  0f84e6270000           je       0x40f491
0040ccab  89c5                   mov      ebp, eax
0040ccad  c1e504                 shl      ebp, 4
0040ccb0  01c5                   add      ebp, eax
0040ccb2  8b742408               mov      esi, dword ptr [esp + 8]
0040ccb6  c1e502                 shl      ebp, 2
0040ccb9  8b7c2404               mov      edi, dword ptr [esp + 4]
0040ccbd  01c5                   add      ebp, eax
0040ccbf  e821dc0000             call     0x41a8e5 ; BatimentGetEtat
0040ccc4  c1e502                 shl      ebp, 2
0040ccc7  89c2                   mov      edx, eax
0040ccc9  898424cc020000         mov      dword ptr [esp + 0x2cc], eax
0040ccd0  81c5c8a04900           add      ebp, 0x49a0c8
0040ccd6  31c0                   xor      eax, eax
0040ccd8  83ee3d                 sub      esi, 0x3d
0040ccdb  8a4505                 mov      al, byte ptr [ebp + 5]
0040ccde  83ef41                 sub      edi, 0x41
0040cce1  83f805                 cmp      eax, 5
0040cce4  740e                   je       0x40ccf4
0040cce6  83f803                 cmp      eax, 3
0040cce9  7409                   je       0x40ccf4
0040cceb  83f804                 cmp      eax, 4
0040ccee  0f8596020000           jne      0x40cf8a
0040ccf4  31c0                   xor      eax, eax
0040ccf6  8a4505                 mov      al, byte ptr [ebp + 5]
0040ccf9  83f803                 cmp      eax, 3
0040ccfc  0f8513010000           jne      0x40ce15
0040cd02  31c0                   xor      eax, eax
0040cd04  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040cd0c  e8a7d80000             call     0x41a5b8 ; BatimentEstHabiter
0040cd11  84c0                   test     al, al
0040cd13  0f85fc000000           jne      0x40ce15
0040cd19  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040cd1f  31d2                   xor      edx, edx
0040cd21  88da                   mov      dl, bl
0040cd23  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040cd29  81e2ff000000           and      edx, 0xff
0040cd2f  b903000000             mov      ecx, 3
0040cd34  89d0                   mov      eax, edx
0040cd36  c1fa1f                 sar      edx, 0x1f
0040cd39  f7f9                   idiv     ecx
0040cd3b  0fbfcf                 movsx    ecx, di
0040cd3e  01ca                   add      edx, ecx
0040cd40  83c274                 add      edx, 0x74
0040cd43  fec3                   inc      bl
0040cd45  6689942478030000       mov      word ptr [esp + 0x378], dx
0040cd4d  31d2                   xor      edx, edx
0040cd4f  88da                   mov      dl, bl
0040cd51  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040cd57  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040cd5d  81e2ff000000           and      edx, 0xff
0040cd63  bf03000000             mov      edi, 3
0040cd68  89d0                   mov      eax, edx
0040cd6a  c1fa1f                 sar      edx, 0x1f
0040cd6d  f7ff                   idiv     edi
0040cd6f  fec3                   inc      bl
0040cd71  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040cd77  01ca                   add      edx, ecx
0040cd79  31c0                   xor      eax, eax
0040cd7b  8dbac8000000           lea      edi, [edx + 0xc8]
0040cd81  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040cd88  29c7                   sub      edi, eax
0040cd8a  0fbfc7                 movsx    eax, di
0040cd8d  85c0                   test     eax, eax
0040cd8f  7d02                   jge      0x40cd93
0040cd91  31ff                   xor      edi, edi
0040cd93  31c0                   xor      eax, eax
0040cd95  66a126875000           mov      ax, word ptr [0x508726]
0040cd9b  8b942476030000         mov      edx, dword ptr [esp + 0x376]
0040cda2  c1e005                 shl      eax, 5
0040cda5  c1fa10                 sar      edx, 0x10
0040cda8  48                     dec      eax
0040cda9  39c2                   cmp      edx, eax
0040cdab  7e12                   jle      0x40cdbf
0040cdad  66a126875000           mov      ax, word ptr [0x508726]
0040cdb3  c1e005                 shl      eax, 5
0040cdb6  48                     dec      eax
0040cdb7  6689842478030000       mov      word ptr [esp + 0x378], ax
0040cdbf  66a124875000           mov      ax, word ptr [0x508724]
0040cdc5  31c9                   xor      ecx, ecx
0040cdc7  31db                   xor      ebx, ebx
0040cdc9  31d2                   xor      edx, edx
0040cdcb  668b8c2478030000       mov      cx, word ptr [esp + 0x378]
0040cdd3  c1e005                 shl      eax, 5
0040cdd6  6689fa                 mov      dx, di
0040cdd9  6689c3                 mov      bx, ax
0040cddc  31c0                   xor      eax, eax
0040cdde  e836270000             call     0x40f519 ; SetClipping
0040cde3  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040cde9  31d2                   xor      edx, edx
0040cdeb  88da                   mov      dl, bl
0040cded  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040cdf3  81e2ff000000           and      edx, 0xff
0040cdf9  b903000000             mov      ecx, 3
0040cdfe  89d0                   mov      eax, edx
0040ce00  c1fa1f                 sar      edx, 0x1f
0040ce03  f7f9                   idiv     ecx
0040ce05  0fbff6                 movsx    esi, si
0040ce08  fec3                   inc      bl
0040ce0a  83c74b                 add      edi, 0x4b
0040ce0d  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040ce13  01d6                   add      esi, edx
0040ce15  89f2                   mov      edx, esi
0040ce17  31c0                   xor      eax, eax
0040ce19  83c20a                 add      edx, 0xa
0040ce1c  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040ce24  6689942414040000       mov      word ptr [esp + 0x414], dx
0040ce2c  89fa                   mov      edx, edi
0040ce2e  89842470010000         mov      dword ptr [esp + 0x170], eax
0040ce35  83ea29                 sub      edx, 0x29
0040ce38  e87bd70000             call     0x41a5b8 ; BatimentEstHabiter
0040ce3d  6689942428040000       mov      word ptr [esp + 0x428], dx
0040ce45  84c0                   test     al, al
0040ce47  0f8487000000           je       0x40ced4
0040ce4d  b901000000             mov      ecx, 1
0040ce52  31c0                   xor      eax, eax
0040ce54  bb951c0000             mov      ebx, 0x1c95
0040ce59  8a4504                 mov      al, byte ptr [ebp + 4]
0040ce5c  0fbfd7                 movsx    edx, di
0040ce5f  50                     push     eax
0040ce60  0fbfc6                 movsx    eax, si
0040ce63  e8edf50400             call     0x45c455 ; PastePlayerCmp
0040ce68  31c0                   xor      eax, eax
0040ce6a  8a4508                 mov      al, byte ptr [ebp + 8]
0040ce6d  83f814                 cmp      eax, 0x14
0040ce70  7526                   jne      0x40ce98
0040ce72  8b942426040000         mov      edx, dword ptr [esp + 0x426]
0040ce79  8b842412040000         mov      eax, dword ptr [esp + 0x412]
0040ce80  31db                   xor      ebx, ebx
0040ce82  8b8c2470010000         mov      ecx, dword ptr [esp + 0x170]
0040ce89  668b1c24               mov      bx, word ptr [esp]
0040ce8d  c1fa10                 sar      edx, 0x10
0040ce90  c1f810                 sar      eax, 0x10
0040ce93  e85160ffff             call     0x402ee9 ; AffUpgradeMonastere
0040ce98  31c0                   xor      eax, eax
0040ce9a  8a4504                 mov      al, byte ptr [ebp + 4]
0040ce9d  8b1c24                 mov      ebx, dword ptr [esp]
0040cea0  50                     push     eax
0040cea1  66a1808f5000           mov      ax, word ptr [0x508f80]
0040cea7  01d8                   add      eax, ebx
0040cea9  30e4                   xor      ah, ah
0040ceab  2407                   and      al, 7
0040cead  31db                   xor      ebx, ebx
0040ceaf  05981c0000             add      eax, 0x1c98
0040ceb4  6689c3                 mov      bx, ax
0040ceb7  89f8                   mov      eax, edi
0040ceb9  0528000000             add      eax, 0x28
0040cebe  0fbfd0                 movsx    edx, ax
0040cec1  89f0                   mov      eax, esi
0040cec3  40                     inc      eax
0040cec4  b901000000             mov      ecx, 1
0040cec9  98                     cwde
0040ceca  e886f50400             call     0x45c455 ; PastePlayerCmp
0040cecf  e9a1000000             jmp      0x40cf75 ;
0040ced4  b901000000             mov      ecx, 1
0040ced9  bb951c0000             mov      ebx, 0x1c95
0040cede  0fbfd7                 movsx    edx, di
0040cee1  0fbfc6                 movsx    eax, si
0040cee4  e85ee30400             call     0x45b247 ; PasteBobCmp
0040cee9  31c0                   xor      eax, eax
0040ceeb  8a4508                 mov      al, byte ptr [ebp + 8]
0040ceee  83f814                 cmp      eax, 0x14
0040cef1  7526                   jne      0x40cf19
0040cef3  8b942426040000         mov      edx, dword ptr [esp + 0x426]
0040cefa  8b842412040000         mov      eax, dword ptr [esp + 0x412]
0040cf01  31db                   xor      ebx, ebx
0040cf03  8b8c2470010000         mov      ecx, dword ptr [esp + 0x170]
0040cf0a  668b1c24               mov      bx, word ptr [esp]
0040cf0e  c1fa10                 sar      edx, 0x10
0040cf11  c1f810                 sar      eax, 0x10
0040cf14  e8d05fffff             call     0x402ee9 ; AffUpgradeMonastere
0040cf19  89f8                   mov      eax, edi
0040cf1b  0528000000             add      eax, 0x28
0040cf20  98                     cwde
0040cf21  89842494000000         mov      dword ptr [esp + 0x94], eax
0040cf28  89f0                   mov      eax, esi
0040cf2a  b901000000             mov      ecx, 1
0040cf2f  40                     inc      eax
0040cf30  bb981c0000             mov      ebx, 0x1c98
0040cf35  98                     cwde
0040cf36  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040cf3d  8944247c               mov      dword ptr [esp + 0x7c], eax
0040cf41  e801e30400             call     0x45b247 ; PasteBobCmp
0040cf46  b901000000             mov      ecx, 1
0040cf4b  bb951c0000             mov      ebx, 0x1c95
0040cf50  0fbfd7                 movsx    edx, di
0040cf53  0fbfc6                 movsx    eax, si
0040cf56  e855ed0400             call     0x45bcb0 ; PasteGrisCmp
0040cf5b  b901000000             mov      ecx, 1
0040cf60  bb981c0000             mov      ebx, 0x1c98
0040cf65  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040cf6c  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040cf70  e83bed0400             call     0x45bcb0 ; PasteGrisCmp
0040cf75  31c0                   xor      eax, eax
0040cf77  668b4506               mov      ax, word ptr [ebp + 6]
0040cf7b  85c0                   test     eax, eax
0040cf7d  0f8ebf230000           jle      0x40f342
0040cf83  6a0f                   push     0xf
0040cf85  e958060000             jmp      0x40d5e2 ;
0040cf8a  31c0                   xor      eax, eax
0040cf8c  668b0d26875000         mov      cx, word ptr [0x508726]
0040cf93  6689d0                 mov      ax, dx
0040cf96  668b1524875000         mov      dx, word ptr [0x508724]
0040cf9d  c1e105                 shl      ecx, 5
0040cfa0  c1e205                 shl      edx, 5
0040cfa3  49                     dec      ecx
0040cfa4  4a                     dec      edx
0040cfa5  83f864                 cmp      eax, 0x64
0040cfa8  0f8d81000000           jge      0x40d02f
0040cfae  899424ec010000         mov      dword ptr [esp + 0x1ec], edx
0040cfb5  ba64000000             mov      edx, 0x64
0040cfba  29c2                   sub      edx, eax
0040cfbc  89d0                   mov      eax, edx
0040cfbe  c1e203                 shl      edx, 3
0040cfc1  29c2                   sub      edx, eax
0040cfc3  c1e202                 shl      edx, 2
0040cfc6  01c2                   add      edx, eax
0040cfc8  c1e202                 shl      edx, 2
0040cfcb  bb64000000             mov      ebx, 0x64
0040cfd0  89d0                   mov      eax, edx
0040cfd2  c1fa1f                 sar      edx, 0x1f
0040cfd5  f7fb                   idiv     ebx
0040cfd7  0fbfd7                 movsx    edx, di
0040cfda  01d0                   add      eax, edx
0040cfdc  0fbfd6                 movsx    edx, si
0040cfdf  89b42408020000         mov      dword ptr [esp + 0x208], esi
0040cfe6  85d2                   test     edx, edx
0040cfe8  7d09                   jge      0x40cff3
0040cfea  31d2                   xor      edx, edx
0040cfec  89942408020000         mov      dword ptr [esp + 0x208], edx
0040cff3  0fbfd0                 movsx    edx, ax
0040cff6  85d2                   test     edx, edx
0040cff8  7d02                   jge      0x40cffc
0040cffa  31c0                   xor      eax, eax
0040cffc  81e1ffff0000           and      ecx, 0xffff
0040d002  31d2                   xor      edx, edx
0040d004  31db                   xor      ebx, ebx
0040d006  6689c2                 mov      dx, ax
0040d009  31c0                   xor      eax, eax
0040d00b  668b9c24ec010000       mov      bx, word ptr [esp + 0x1ec]
0040d013  668b842408020000       mov      ax, word ptr [esp + 0x208]
0040d01b  e8f9240000             call     0x40f519 ; SetClipping
0040d020  b901000000             mov      ecx, 1
0040d025  bb941c0000             mov      ebx, 0x1c94
0040d02a  e9e3b3ffff             jmp      0x408412 ;
0040d02f  89942448030000         mov      dword ptr [esp + 0x348], edx
0040d036  83e864                 sub      eax, 0x64
0040d039  ba64000000             mov      edx, 0x64
0040d03e  29c2                   sub      edx, eax
0040d040  89d0                   mov      eax, edx
0040d042  c1e203                 shl      edx, 3
0040d045  29c2                   sub      edx, eax
0040d047  c1e202                 shl      edx, 2
0040d04a  01c2                   add      edx, eax
0040d04c  c1e202                 shl      edx, 2
0040d04f  bb64000000             mov      ebx, 0x64
0040d054  89d0                   mov      eax, edx
0040d056  c1fa1f                 sar      edx, 0x1f
0040d059  f7fb                   idiv     ebx
0040d05b  0fbfd7                 movsx    edx, di
0040d05e  01d0                   add      eax, edx
0040d060  31d2                   xor      edx, edx
0040d062  668b1526875000         mov      dx, word ptr [0x508726]
0040d069  898c24b8030000         mov      dword ptr [esp + 0x3b8], ecx
0040d070  c1e205                 shl      edx, 5
0040d073  0fbfd8                 movsx    ebx, ax
0040d076  4a                     dec      edx
0040d077  6689b424ac020000       mov      word ptr [esp + 0x2ac], si
0040d07f  39d3                   cmp      ebx, edx
0040d081  7e02                   jle      0x40d085
0040d083  89c8                   mov      eax, ecx
0040d085  31c9                   xor      ecx, ecx
0040d087  31db                   xor      ebx, ebx
0040d089  31d2                   xor      edx, edx
0040d08b  668b9c2448030000       mov      bx, word ptr [esp + 0x348]
0040d093  6689c1                 mov      cx, ax
0040d096  31c0                   xor      eax, eax
0040d098  e87c240000             call     0x40f519 ; SetClipping
0040d09d  0fbfc7                 movsx    eax, di
0040d0a0  b901000000             mov      ecx, 1
0040d0a5  8944247c               mov      dword ptr [esp + 0x7c], eax
0040d0a9  bb941c0000             mov      ebx, 0x1c94
0040d0ae  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040d0b2  0fbfc6                 movsx    eax, si
0040d0b5  e88de10400             call     0x45b247 ; PasteBobCmp
0040d0ba  31c0                   xor      eax, eax
0040d0bc  668b8424cc020000       mov      ax, word ptr [esp + 0x2cc]
0040d0c4  ba64000000             mov      edx, 0x64
0040d0c9  83e864                 sub      eax, 0x64
0040d0cc  29c2                   sub      edx, eax
0040d0ce  89d0                   mov      eax, edx
0040d0d0  c1e203                 shl      edx, 3
0040d0d3  29c2                   sub      edx, eax
0040d0d5  c1e202                 shl      edx, 2
0040d0d8  01c2                   add      edx, eax
0040d0da  c1e202                 shl      edx, 2
0040d0dd  bb64000000             mov      ebx, 0x64
0040d0e2  89d0                   mov      eax, edx
0040d0e4  c1fa1f                 sar      edx, 0x1f
0040d0e7  f7fb                   idiv     ebx
0040d0e9  8b9424aa020000         mov      edx, dword ptr [esp + 0x2aa]
0040d0f0  8b5c247c               mov      ebx, dword ptr [esp + 0x7c]
0040d0f4  c1fa10                 sar      edx, 0x10
0040d0f7  01d8                   add      eax, ebx
0040d0f9  85d2                   test     edx, edx
0040d0fb  7d0a                   jge      0x40d107
0040d0fd  31db                   xor      ebx, ebx
0040d0ff  66899c24ac020000       mov      word ptr [esp + 0x2ac], bx
0040d107  0fbfd0                 movsx    edx, ax
0040d10a  85d2                   test     edx, edx
0040d10c  7d02                   jge      0x40d110
0040d10e  31c0                   xor      eax, eax
0040d110  31c9                   xor      ecx, ecx
0040d112  31db                   xor      ebx, ebx
0040d114  31d2                   xor      edx, edx
0040d116  668b8c24b8030000       mov      cx, word ptr [esp + 0x3b8]
0040d11e  6689c2                 mov      dx, ax
0040d121  31c0                   xor      eax, eax
0040d123  668b9c2448030000       mov      bx, word ptr [esp + 0x348]
0040d12b  668b8424ac020000       mov      ax, word ptr [esp + 0x2ac]
0040d133  e8e1230000             call     0x40f519 ; SetClipping
0040d138  b901000000             mov      ecx, 1
0040d13d  0fbfc7                 movsx    eax, di
0040d140  bb951c0000             mov      ebx, 0x1c95
0040d145  89842474010000         mov      dword ptr [esp + 0x174], eax
0040d14c  0fbfc6                 movsx    eax, si
0040d14f  8b942474010000         mov      edx, dword ptr [esp + 0x174]
0040d156  898424a8010000         mov      dword ptr [esp + 0x1a8], eax
0040d15d  e8e5e00400             call     0x45b247 ; PasteBobCmp
0040d162  89f8                   mov      eax, edi
0040d164  0528000000             add      eax, 0x28
0040d169  0fbfe8                 movsx    ebp, ax
0040d16c  89f0                   mov      eax, esi
0040d16e  b901000000             mov      ecx, 1
0040d173  40                     inc      eax
0040d174  bb981c0000             mov      ebx, 0x1c98
0040d179  98                     cwde
0040d17a  89ea                   mov      edx, ebp
0040d17c  89842414010000         mov      dword ptr [esp + 0x114], eax
0040d183  e8bfe00400             call     0x45b247 ; PasteBobCmp
0040d188  31c0                   xor      eax, eax
0040d18a  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040d192  e821d40000             call     0x41a5b8 ; BatimentEstHabiter
0040d197  84c0                   test     al, al
0040d199  0f85a3210000           jne      0x40f342
0040d19f  b901000000             mov      ecx, 1
0040d1a4  bb951c0000             mov      ebx, 0x1c95
0040d1a9  8b942474010000         mov      edx, dword ptr [esp + 0x174]
0040d1b0  8b8424a8010000         mov      eax, dword ptr [esp + 0x1a8]
0040d1b7  e8f4ea0400             call     0x45bcb0 ; PasteGrisCmp
0040d1bc  b901000000             mov      ecx, 1
0040d1c1  bb981c0000             mov      ebx, 0x1c98
0040d1c6  8b842414010000         mov      eax, dword ptr [esp + 0x114]
0040d1cd  e999b3ffff             jmp      0x40856b ;
0040d1d2  31c0                   xor      eax, eax
0040d1d4  668b0424               mov      ax, word ptr [esp]
0040d1d8  8d1400                 lea      edx, [eax + eax]
0040d1db  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040d1e0  f644020180             test     byte ptr [edx + eax + 1], 0x80
0040d1e5  7422                   je       0x40d209
0040d1e7  31c0                   xor      eax, eax
0040d1e9  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0040d1ef  668b0424               mov      ax, word ptr [esp]
0040d1f3  668b0442               mov      ax, word ptr [edx + eax*2]
0040d1f7  25e07f0000             and      eax, 0x7fe0
0040d1fc  89c3                   mov      ebx, eax
0040d1fe  81e3ffff0000           and      ebx, 0xffff
0040d204  c1fb05                 sar      ebx, 5
0040d207  eb05                   jmp      0x40d20e ;
0040d209  bbffff0000             mov      ebx, 0xffff
0040d20e  31d2                   xor      edx, edx
0040d210  6689da                 mov      dx, bx
0040d213  899c2410020000         mov      dword ptr [esp + 0x210], ebx
0040d21a  81faffff0000           cmp      edx, 0xffff
0040d220  0f846b220000           je       0x40f491
0040d226  89d5                   mov      ebp, edx
0040d228  8b742408               mov      esi, dword ptr [esp + 8]
0040d22c  c1e504                 shl      ebp, 4
0040d22f  8b7c2404               mov      edi, dword ptr [esp + 4]
0040d233  01d5                   add      ebp, edx
0040d235  89d0                   mov      eax, edx
0040d237  c1e502                 shl      ebp, 2
0040d23a  e8a6d60000             call     0x41a8e5 ; BatimentGetEtat
0040d23f  01d5                   add      ebp, edx
0040d241  898424d0020000         mov      dword ptr [esp + 0x2d0], eax
0040d248  c1e502                 shl      ebp, 2
0040d24b  89c2                   mov      edx, eax
0040d24d  81c5c8a04900           add      ebp, 0x49a0c8
0040d253  31c0                   xor      eax, eax
0040d255  83ee34                 sub      esi, 0x34
0040d258  8a4505                 mov      al, byte ptr [ebp + 5]
0040d25b  83ef4c                 sub      edi, 0x4c
0040d25e  83f805                 cmp      eax, 5
0040d261  740e                   je       0x40d271
0040d263  83f803                 cmp      eax, 3
0040d266  7409                   je       0x40d271
0040d268  83f804                 cmp      eax, 4
0040d26b  0f8596030000           jne      0x40d607
0040d271  31c0                   xor      eax, eax
0040d273  8a4505                 mov      al, byte ptr [ebp + 5]
0040d276  83f803                 cmp      eax, 3
0040d279  0f8514010000           jne      0x40d393
0040d27f  31c0                   xor      eax, eax
0040d281  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040d289  e82ad30000             call     0x41a5b8 ; BatimentEstHabiter
0040d28e  84c0                   test     al, al
0040d290  0f85fd000000           jne      0x40d393
0040d296  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
0040d29c  31d2                   xor      edx, edx
0040d29e  88ca                   mov      dl, cl
0040d2a0  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d2a6  81e2ff000000           and      edx, 0xff
0040d2ac  bb03000000             mov      ebx, 3
0040d2b1  89d0                   mov      eax, edx
0040d2b3  c1fa1f                 sar      edx, 0x1f
0040d2b6  f7fb                   idiv     ebx
0040d2b8  0fbfdf                 movsx    ebx, di
0040d2bb  01da                   add      edx, ebx
0040d2bd  83c262                 add      edx, 0x62
0040d2c0  fec1                   inc      cl
0040d2c2  6689942480020000       mov      word ptr [esp + 0x280], dx
0040d2ca  31d2                   xor      edx, edx
0040d2cc  88ca                   mov      dl, cl
0040d2ce  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040d2d4  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d2da  81e2ff000000           and      edx, 0xff
0040d2e0  bf03000000             mov      edi, 3
0040d2e5  89d0                   mov      eax, edx
0040d2e7  c1fa1f                 sar      edx, 0x1f
0040d2ea  f7ff                   idiv     edi
0040d2ec  fec1                   inc      cl
0040d2ee  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040d2f4  01da                   add      edx, ebx
0040d2f6  31c0                   xor      eax, eax
0040d2f8  81c2c8000000           add      edx, 0xc8
0040d2fe  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040d305  29c2                   sub      edx, eax
0040d307  0fbfc2                 movsx    eax, dx
0040d30a  89d7                   mov      edi, edx
0040d30c  85c0                   test     eax, eax
0040d30e  7d02                   jge      0x40d312
0040d310  31d7                   xor      edi, edx
0040d312  31c0                   xor      eax, eax
0040d314  66a126875000           mov      ax, word ptr [0x508726]
0040d31a  89c2                   mov      edx, eax
0040d31c  8b84247e020000         mov      eax, dword ptr [esp + 0x27e]
0040d323  c1e205                 shl      edx, 5
0040d326  c1f810                 sar      eax, 0x10
0040d329  4a                     dec      edx
0040d32a  39d0                   cmp      eax, edx
0040d32c  7e12                   jle      0x40d340
0040d32e  66a126875000           mov      ax, word ptr [0x508726]
0040d334  c1e005                 shl      eax, 5
0040d337  48                     dec      eax
0040d338  6689842480020000       mov      word ptr [esp + 0x280], ax
0040d340  66a124875000           mov      ax, word ptr [0x508724]
0040d346  31c9                   xor      ecx, ecx
0040d348  31db                   xor      ebx, ebx
0040d34a  31d2                   xor      edx, edx
0040d34c  668b8c2480020000       mov      cx, word ptr [esp + 0x280]
0040d354  c1e005                 shl      eax, 5
0040d357  6689fa                 mov      dx, di
0040d35a  6689c3                 mov      bx, ax
0040d35d  31c0                   xor      eax, eax
0040d35f  e8b5210000             call     0x40f519 ; SetClipping
0040d364  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040d36a  31d2                   xor      edx, edx
0040d36c  88da                   mov      dl, bl
0040d36e  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d374  81e2ff000000           and      edx, 0xff
0040d37a  b903000000             mov      ecx, 3
0040d37f  89d0                   mov      eax, edx
0040d381  c1fa1f                 sar      edx, 0x1f
0040d384  f7f9                   idiv     ecx
0040d386  fec3                   inc      bl
0040d388  0fbff6                 movsx    esi, si
0040d38b  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040d391  01d6                   add      esi, edx
0040d393  89f2                   mov      edx, esi
0040d395  83c203                 add      edx, 3
0040d398  31c0                   xor      eax, eax
0040d39a  66899424a8020000       mov      word ptr [esp + 0x2a8], dx
0040d3a2  89fa                   mov      edx, edi
0040d3a4  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040d3ac  83c20d                 add      edx, 0xd
0040d3af  e804d20000             call     0x41a5b8 ; BatimentEstHabiter
0040d3b4  66899424e4030000       mov      word ptr [esp + 0x3e4], dx
0040d3bc  84c0                   test     al, al
0040d3be  0f842a010000           je       0x40d4ee
0040d3c4  b901000000             mov      ecx, 1
0040d3c9  31c0                   xor      eax, eax
0040d3cb  bba91c0000             mov      ebx, 0x1ca9
0040d3d0  8a4504                 mov      al, byte ptr [ebp + 4]
0040d3d3  0fbfd7                 movsx    edx, di
0040d3d6  50                     push     eax
0040d3d7  0fbfc6                 movsx    eax, si
0040d3da  e876f00400             call     0x45c455 ; PastePlayerCmp
0040d3df  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040d3e5  31d2                   xor      edx, edx
0040d3e7  88da                   mov      dl, bl
0040d3e9  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d3ef  81e2ff000000           and      edx, 0xff
0040d3f5  b914000000             mov      ecx, 0x14
0040d3fa  89d0                   mov      eax, edx
0040d3fc  c1fa1f                 sar      edx, 0x1f
0040d3ff  f7f9                   idiv     ecx
0040d401  fec3                   inc      bl
0040d403  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040d409  85d2                   test     edx, edx
0040d40b  752e                   jne      0x40d43b
0040d40d  8b1c24                 mov      ebx, dword ptr [esp]
0040d410  66a1808f5000           mov      ax, word ptr [0x508f80]
0040d416  01d8                   add      eax, ebx
0040d418  30e4                   xor      ah, ah
0040d41a  8b9424e2030000         mov      edx, dword ptr [esp + 0x3e2]
0040d421  2401                   and      al, 1
0040d423  31db                   xor      ebx, ebx
0040d425  05aa1c0000             add      eax, 0x1caa
0040d42a  b901000000             mov      ecx, 1
0040d42f  6689c3                 mov      bx, ax
0040d432  8b8424a6020000         mov      eax, dword ptr [esp + 0x2a6]
0040d439  eb18                   jmp      0x40d453 ;
0040d43b  8b9424e2030000         mov      edx, dword ptr [esp + 0x3e2]
0040d442  8b8424a6020000         mov      eax, dword ptr [esp + 0x2a6]
0040d449  b901000000             mov      ecx, 1
0040d44e  bbaa1c0000             mov      ebx, 0x1caa
0040d453  c1fa10                 sar      edx, 0x10
0040d456  c1f810                 sar      eax, 0x10
0040d459  e8e9dd0400             call     0x45b247 ; PasteBobCmp
0040d45e  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040d464  31d2                   xor      edx, edx
0040d466  88da                   mov      dl, bl
0040d468  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d46e  81e2ff000000           and      edx, 0xff
0040d474  b905000000             mov      ecx, 5
0040d479  89d0                   mov      eax, edx
0040d47b  c1fa1f                 sar      edx, 0x1f
0040d47e  f7f9                   idiv     ecx
0040d480  fec3                   inc      bl
0040d482  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040d488  89f8                   mov      eax, edi
0040d48a  89f1                   mov      ecx, esi
0040d48c  0536000000             add      eax, 0x36
0040d491  83c106                 add      ecx, 6
0040d494  66898424f8020000       mov      word ptr [esp + 0x2f8], ax
0040d49c  85d2                   test     edx, edx
0040d49e  7535                   jne      0x40d4d5
0040d4a0  8b1424                 mov      edx, dword ptr [esp]
0040d4a3  66a1808f5000           mov      ax, word ptr [0x508f80]
0040d4a9  01d0                   add      eax, edx
0040d4ab  30e4                   xor      ah, ah
0040d4ad  31db                   xor      ebx, ebx
0040d4af  2401                   and      al, 1
0040d4b1  8b9424f6020000         mov      edx, dword ptr [esp + 0x2f6]
0040d4b8  05ac1c0000             add      eax, 0x1cac
0040d4bd  c1fa10                 sar      edx, 0x10
0040d4c0  6689c3                 mov      bx, ax
0040d4c3  0fbfc1                 movsx    eax, cx
0040d4c6  b901000000             mov      ecx, 1
0040d4cb  e877dd0400             call     0x45b247 ; PasteBobCmp
0040d4d0  e9fd000000             jmp      0x40d5d2 ;
0040d4d5  8b9424f6020000         mov      edx, dword ptr [esp + 0x2f6]
0040d4dc  bbac1c0000             mov      ebx, 0x1cac
0040d4e1  0fbfc1                 movsx    eax, cx
0040d4e4  b901000000             mov      ecx, 1
0040d4e9  c1fa10                 sar      edx, 0x10
0040d4ec  ebdd                   jmp      0x40d4cb ;
0040d4ee  b901000000             mov      ecx, 1
0040d4f3  0fbfc7                 movsx    eax, di
0040d4f6  bba91c0000             mov      ebx, 0x1ca9
0040d4fb  8944247c               mov      dword ptr [esp + 0x7c], eax
0040d4ff  0fbfc6                 movsx    eax, si
0040d502  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040d506  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040d50d  e835dd0400             call     0x45b247 ; PasteBobCmp
0040d512  8b8424e2030000         mov      eax, dword ptr [esp + 0x3e2]
0040d519  c1f810                 sar      eax, 0x10
0040d51c  b901000000             mov      ecx, 1
0040d521  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040d528  8b8424a6020000         mov      eax, dword ptr [esp + 0x2a6]
0040d52f  bbaa1c0000             mov      ebx, 0x1caa
0040d534  c1f810                 sar      eax, 0x10
0040d537  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040d53e  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040d545  e8fddc0400             call     0x45b247 ; PasteBobCmp
0040d54a  89f8                   mov      eax, edi
0040d54c  0536000000             add      eax, 0x36
0040d551  98                     cwde
0040d552  89842498000000         mov      dword ptr [esp + 0x98], eax
0040d559  89f0                   mov      eax, esi
0040d55b  b901000000             mov      ecx, 1
0040d560  0506000000             add      eax, 6
0040d565  bbac1c0000             mov      ebx, 0x1cac
0040d56a  98                     cwde
0040d56b  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040d572  89842494000000         mov      dword ptr [esp + 0x94], eax
0040d579  e8c9dc0400             call     0x45b247 ; PasteBobCmp
0040d57e  b901000000             mov      ecx, 1
0040d583  bba91c0000             mov      ebx, 0x1ca9
0040d588  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040d58c  8b8424a4010000         mov      eax, dword ptr [esp + 0x1a4]
0040d593  e818e70400             call     0x45bcb0 ; PasteGrisCmp
0040d598  b901000000             mov      ecx, 1
0040d59d  bbaa1c0000             mov      ebx, 0x1caa
0040d5a2  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040d5a9  8b84249c000000         mov      eax, dword ptr [esp + 0x9c]
0040d5b0  e8fbe60400             call     0x45bcb0 ; PasteGrisCmp
0040d5b5  b901000000             mov      ecx, 1
0040d5ba  bbac1c0000             mov      ebx, 0x1cac
0040d5bf  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040d5c6  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040d5cd  e8dee60400             call     0x45bcb0 ; PasteGrisCmp
0040d5d2  31c0                   xor      eax, eax
0040d5d4  668b4506               mov      ax, word ptr [ebp + 6]
0040d5d8  85c0                   test     eax, eax
0040d5da  0f8e621d0000           jle      0x40f342
0040d5e0  6a07                   push     7
0040d5e2  31c9                   xor      ecx, ecx
0040d5e4  31db                   xor      ebx, ebx
0040d5e6  31d2                   xor      edx, edx
0040d5e8  31c0                   xor      eax, eax
0040d5ea  668b8c2414020000       mov      cx, word ptr [esp + 0x214]
0040d5f2  668b5c2404             mov      bx, word ptr [esp + 4]
0040d5f7  6689fa                 mov      dx, di
0040d5fa  6689f0                 mov      ax, si
0040d5fd  e83a5cffff             call     0x40323c ; AffFlamme
0040d602  e93b1d0000             jmp      0x40f342 ;
0040d607  31c0                   xor      eax, eax
0040d609  668b0d26875000         mov      cx, word ptr [0x508726]
0040d610  6689d0                 mov      ax, dx
0040d613  668b1524875000         mov      dx, word ptr [0x508724]
0040d61a  c1e105                 shl      ecx, 5
0040d61d  c1e205                 shl      edx, 5
0040d620  49                     dec      ecx
0040d621  4a                     dec      edx
0040d622  83f864                 cmp      eax, 0x64
0040d625  0f8d80000000           jge      0x40d6ab
0040d62b  89942484030000         mov      dword ptr [esp + 0x384], edx
0040d632  ba64000000             mov      edx, 0x64
0040d637  29c2                   sub      edx, eax
0040d639  89d0                   mov      eax, edx
0040d63b  c1e202                 shl      edx, 2
0040d63e  29c2                   sub      edx, eax
0040d640  c1e204                 shl      edx, 4
0040d643  01c2                   add      edx, eax
0040d645  01d2                   add      edx, edx
0040d647  bb64000000             mov      ebx, 0x64
0040d64c  89d0                   mov      eax, edx
0040d64e  c1fa1f                 sar      edx, 0x1f
0040d651  f7fb                   idiv     ebx
0040d653  0fbfd7                 movsx    edx, di
0040d656  01d0                   add      eax, edx
0040d658  0fbfd6                 movsx    edx, si
0040d65b  89b42458030000         mov      dword ptr [esp + 0x358], esi
0040d662  85d2                   test     edx, edx
0040d664  7d09                   jge      0x40d66f
0040d666  31d2                   xor      edx, edx
0040d668  89942458030000         mov      dword ptr [esp + 0x358], edx
0040d66f  0fbfd0                 movsx    edx, ax
0040d672  85d2                   test     edx, edx
0040d674  7d02                   jge      0x40d678
0040d676  31c0                   xor      eax, eax
0040d678  81e1ffff0000           and      ecx, 0xffff
0040d67e  31d2                   xor      edx, edx
0040d680  31db                   xor      ebx, ebx
0040d682  6689c2                 mov      dx, ax
0040d685  31c0                   xor      eax, eax
0040d687  668b9c2484030000       mov      bx, word ptr [esp + 0x384]
0040d68f  668b842458030000       mov      ax, word ptr [esp + 0x358]
0040d697  e87d1e0000             call     0x40f519 ; SetClipping
0040d69c  b901000000             mov      ecx, 1
0040d6a1  bba81c0000             mov      ebx, 0x1ca8
0040d6a6  e967adffff             jmp      0x408412 ;
0040d6ab  89942494030000         mov      dword ptr [esp + 0x394], edx
0040d6b2  83e864                 sub      eax, 0x64
0040d6b5  ba64000000             mov      edx, 0x64
0040d6ba  29c2                   sub      edx, eax
0040d6bc  89d0                   mov      eax, edx
0040d6be  c1e202                 shl      edx, 2
0040d6c1  29c2                   sub      edx, eax
0040d6c3  c1e204                 shl      edx, 4
0040d6c6  01c2                   add      edx, eax
0040d6c8  01d2                   add      edx, edx
0040d6ca  bb64000000             mov      ebx, 0x64
0040d6cf  89d0                   mov      eax, edx
0040d6d1  c1fa1f                 sar      edx, 0x1f
0040d6d4  f7fb                   idiv     ebx
0040d6d6  0fbfd7                 movsx    edx, di
0040d6d9  01d0                   add      eax, edx
0040d6db  31d2                   xor      edx, edx
0040d6dd  668b1526875000         mov      dx, word ptr [0x508726]
0040d6e4  898c24fc020000         mov      dword ptr [esp + 0x2fc], ecx
0040d6eb  c1e205                 shl      edx, 5
0040d6ee  0fbfd8                 movsx    ebx, ax
0040d6f1  4a                     dec      edx
0040d6f2  6689b42484020000       mov      word ptr [esp + 0x284], si
0040d6fa  39d3                   cmp      ebx, edx
0040d6fc  7e02                   jle      0x40d700
0040d6fe  89c8                   mov      eax, ecx
0040d700  31c9                   xor      ecx, ecx
0040d702  31db                   xor      ebx, ebx
0040d704  31d2                   xor      edx, edx
0040d706  668b9c2494030000       mov      bx, word ptr [esp + 0x394]
0040d70e  6689c1                 mov      cx, ax
0040d711  31c0                   xor      eax, eax
0040d713  e8011e0000             call     0x40f519 ; SetClipping
0040d718  0fbfc7                 movsx    eax, di
0040d71b  b901000000             mov      ecx, 1
0040d720  89842494000000         mov      dword ptr [esp + 0x94], eax
0040d727  bba81c0000             mov      ebx, 0x1ca8
0040d72c  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040d733  0fbfc6                 movsx    eax, si
0040d736  e80cdb0400             call     0x45b247 ; PasteBobCmp
0040d73b  31c0                   xor      eax, eax
0040d73d  668b8424d0020000       mov      ax, word ptr [esp + 0x2d0]
0040d745  ba64000000             mov      edx, 0x64
0040d74a  83e864                 sub      eax, 0x64
0040d74d  29c2                   sub      edx, eax
0040d74f  89d0                   mov      eax, edx
0040d751  c1e202                 shl      edx, 2
0040d754  29c2                   sub      edx, eax
0040d756  c1e204                 shl      edx, 4
0040d759  01c2                   add      edx, eax
0040d75b  01d2                   add      edx, edx
0040d75d  bb64000000             mov      ebx, 0x64
0040d762  89d0                   mov      eax, edx
0040d764  c1fa1f                 sar      edx, 0x1f
0040d767  f7fb                   idiv     ebx
0040d769  03842494000000         add      eax, dword ptr [esp + 0x94]
0040d770  8b942482020000         mov      edx, dword ptr [esp + 0x282]
0040d777  c1fa10                 sar      edx, 0x10
0040d77a  85d2                   test     edx, edx
0040d77c  7d0a                   jge      0x40d788
0040d77e  31c9                   xor      ecx, ecx
0040d780  66898c2484020000       mov      word ptr [esp + 0x284], cx
0040d788  0fbfd0                 movsx    edx, ax
0040d78b  85d2                   test     edx, edx
0040d78d  7d02                   jge      0x40d791
0040d78f  31c0                   xor      eax, eax
0040d791  31c9                   xor      ecx, ecx
0040d793  31db                   xor      ebx, ebx
0040d795  31d2                   xor      edx, edx
0040d797  668b8c24fc020000       mov      cx, word ptr [esp + 0x2fc]
0040d79f  6689c2                 mov      dx, ax
0040d7a2  31c0                   xor      eax, eax
0040d7a4  668b9c2494030000       mov      bx, word ptr [esp + 0x394]
0040d7ac  668b842484020000       mov      ax, word ptr [esp + 0x284]
0040d7b4  0fbfef                 movsx    ebp, di
0040d7b7  e85d1d0000             call     0x40f519 ; SetClipping
0040d7bc  b901000000             mov      ecx, 1
0040d7c1  bba91c0000             mov      ebx, 0x1ca9
0040d7c6  0fbfc6                 movsx    eax, si
0040d7c9  89ea                   mov      edx, ebp
0040d7cb  89442464               mov      dword ptr [esp + 0x64], eax
0040d7cf  e873da0400             call     0x45b247 ; PasteBobCmp
0040d7d4  89f8                   mov      eax, edi
0040d7d6  050d000000             add      eax, 0xd
0040d7db  98                     cwde
0040d7dc  89842418010000         mov      dword ptr [esp + 0x118], eax
0040d7e3  89f0                   mov      eax, esi
0040d7e5  b901000000             mov      ecx, 1
0040d7ea  0503000000             add      eax, 3
0040d7ef  bbaa1c0000             mov      ebx, 0x1caa
0040d7f4  98                     cwde
0040d7f5  8b942418010000         mov      edx, dword ptr [esp + 0x118]
0040d7fc  89442410               mov      dword ptr [esp + 0x10], eax
0040d800  e842da0400             call     0x45b247 ; PasteBobCmp
0040d805  89f8                   mov      eax, edi
0040d807  0536000000             add      eax, 0x36
0040d80c  98                     cwde
0040d80d  8984244c010000         mov      dword ptr [esp + 0x14c], eax
0040d814  89f0                   mov      eax, esi
0040d816  b901000000             mov      ecx, 1
0040d81b  0506000000             add      eax, 6
0040d820  bbac1c0000             mov      ebx, 0x1cac
0040d825  98                     cwde
0040d826  8b94244c010000         mov      edx, dword ptr [esp + 0x14c]
0040d82d  8984241c010000         mov      dword ptr [esp + 0x11c], eax
0040d834  e80eda0400             call     0x45b247 ; PasteBobCmp
0040d839  31c0                   xor      eax, eax
0040d83b  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040d843  e870cd0000             call     0x41a5b8 ; BatimentEstHabiter
0040d848  84c0                   test     al, al
0040d84a  0f85f21a0000           jne      0x40f342
0040d850  b901000000             mov      ecx, 1
0040d855  bba91c0000             mov      ebx, 0x1ca9
0040d85a  8b442464               mov      eax, dword ptr [esp + 0x64]
0040d85e  89ea                   mov      edx, ebp
0040d860  e84be40400             call     0x45bcb0 ; PasteGrisCmp
0040d865  b901000000             mov      ecx, 1
0040d86a  bbaa1c0000             mov      ebx, 0x1caa
0040d86f  8b942418010000         mov      edx, dword ptr [esp + 0x118]
0040d876  8b442410               mov      eax, dword ptr [esp + 0x10]
0040d87a  e831e40400             call     0x45bcb0 ; PasteGrisCmp
0040d87f  b901000000             mov      ecx, 1
0040d884  bbac1c0000             mov      ebx, 0x1cac
0040d889  8b94244c010000         mov      edx, dword ptr [esp + 0x14c]
0040d890  8b84241c010000         mov      eax, dword ptr [esp + 0x11c]
0040d897  e9d1acffff             jmp      0x40856d ;
0040d89c  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040d8a1  01c8                   add      eax, ecx
0040d8a3  f6400180               test     byte ptr [eax + 1], 0x80
0040d8a7  7415                   je       0x40d8be
0040d8a9  668b00                 mov      ax, word ptr [eax]
0040d8ac  25e07f0000             and      eax, 0x7fe0
0040d8b1  89c2                   mov      edx, eax
0040d8b3  81e2ffff0000           and      edx, 0xffff
0040d8b9  c1fa05                 sar      edx, 5
0040d8bc  eb05                   jmp      0x40d8c3 ;
0040d8be  baffff0000             mov      edx, 0xffff
0040d8c3  31c0                   xor      eax, eax
0040d8c5  6689d0                 mov      ax, dx
0040d8c8  89942410020000         mov      dword ptr [esp + 0x210], edx
0040d8cf  3dffff0000             cmp      eax, 0xffff
0040d8d4  0f84b71b0000           je       0x40f491
0040d8da  89c5                   mov      ebp, eax
0040d8dc  c1e504                 shl      ebp, 4
0040d8df  01c5                   add      ebp, eax
0040d8e1  8b742408               mov      esi, dword ptr [esp + 8]
0040d8e5  c1e502                 shl      ebp, 2
0040d8e8  8b7c2404               mov      edi, dword ptr [esp + 4]
0040d8ec  01c5                   add      ebp, eax
0040d8ee  e8f2cf0000             call     0x41a8e5 ; BatimentGetEtat
0040d8f3  c1e502                 shl      ebp, 2
0040d8f6  89c2                   mov      edx, eax
0040d8f8  898424b0020000         mov      dword ptr [esp + 0x2b0], eax
0040d8ff  81c5c8a04900           add      ebp, 0x49a0c8
0040d905  31c0                   xor      eax, eax
0040d907  83ee1c                 sub      esi, 0x1c
0040d90a  8a4505                 mov      al, byte ptr [ebp + 5]
0040d90d  83ef44                 sub      edi, 0x44
0040d910  83f805                 cmp      eax, 5
0040d913  740e                   je       0x40d923
0040d915  83f803                 cmp      eax, 3
0040d918  7409                   je       0x40d923
0040d91a  83f804                 cmp      eax, 4
0040d91d  0f8549020000           jne      0x40db6c
0040d923  31c0                   xor      eax, eax
0040d925  8a4505                 mov      al, byte ptr [ebp + 5]
0040d928  83f803                 cmp      eax, 3
0040d92b  0f8506010000           jne      0x40da37
0040d931  31c0                   xor      eax, eax
0040d933  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040d93b  e878cc0000             call     0x41a5b8 ; BatimentEstHabiter
0040d940  84c0                   test     al, al
0040d942  0f85ef000000           jne      0x40da37
0040d948  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040d94e  31d2                   xor      edx, edx
0040d950  88da                   mov      dl, bl
0040d952  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d958  81e2ff000000           and      edx, 0xff
0040d95e  b903000000             mov      ecx, 3
0040d963  89d0                   mov      eax, edx
0040d965  c1fa1f                 sar      edx, 0x1f
0040d968  f7f9                   idiv     ecx
0040d96a  0fbfff                 movsx    edi, di
0040d96d  01fa                   add      edx, edi
0040d96f  83c253                 add      edx, 0x53
0040d972  fec3                   inc      bl
0040d974  89d1                   mov      ecx, edx
0040d976  31d2                   xor      edx, edx
0040d978  88da                   mov      dl, bl
0040d97a  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040d980  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040d986  b803000000             mov      eax, 3
0040d98b  81e2ff000000           and      edx, 0xff
0040d991  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040d998  89d0                   mov      eax, edx
0040d99a  c1fa1f                 sar      edx, 0x1f
0040d99d  f7bc24a4010000         idiv     dword ptr [esp + 0x1a4]
0040d9a4  fec3                   inc      bl
0040d9a6  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040d9ac  01fa                   add      edx, edi
0040d9ae  31c0                   xor      eax, eax
0040d9b0  81c2c8000000           add      edx, 0xc8
0040d9b6  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040d9bd  29c2                   sub      edx, eax
0040d9bf  0fbfc2                 movsx    eax, dx
0040d9c2  89d7                   mov      edi, edx
0040d9c4  85c0                   test     eax, eax
0040d9c6  7d02                   jge      0x40d9ca
0040d9c8  31d7                   xor      edi, edx
0040d9ca  31c0                   xor      eax, eax
0040d9cc  66a126875000           mov      ax, word ptr [0x508726]
0040d9d2  c1e005                 shl      eax, 5
0040d9d5  0fbfd1                 movsx    edx, cx
0040d9d8  48                     dec      eax
0040d9d9  39c2                   cmp      edx, eax
0040d9db  7e0b                   jle      0x40d9e8
0040d9dd  668b0d26875000         mov      cx, word ptr [0x508726]
0040d9e4  c1e105                 shl      ecx, 5
0040d9e7  49                     dec      ecx
0040d9e8  66a124875000           mov      ax, word ptr [0x508724]
0040d9ee  81e1ffff0000           and      ecx, 0xffff
0040d9f4  31db                   xor      ebx, ebx
0040d9f6  31d2                   xor      edx, edx
0040d9f8  c1e005                 shl      eax, 5
0040d9fb  6689fa                 mov      dx, di
0040d9fe  6689c3                 mov      bx, ax
0040da01  31c0                   xor      eax, eax
0040da03  e8111b0000             call     0x40f519 ; SetClipping
0040da08  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040da0e  31d2                   xor      edx, edx
0040da10  88da                   mov      dl, bl
0040da12  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040da18  81e2ff000000           and      edx, 0xff
0040da1e  b903000000             mov      ecx, 3
0040da23  89d0                   mov      eax, edx
0040da25  c1fa1f                 sar      edx, 0x1f
0040da28  f7f9                   idiv     ecx
0040da2a  fec3                   inc      bl
0040da2c  0fbff6                 movsx    esi, si
0040da2f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040da35  01d6                   add      esi, edx
0040da37  89f2                   mov      edx, esi
0040da39  83c228                 add      edx, 0x28
0040da3c  31c0                   xor      eax, eax
0040da3e  6689942490030000       mov      word ptr [esp + 0x390], dx
0040da46  89fa                   mov      edx, edi
0040da48  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040da50  83c21a                 add      edx, 0x1a
0040da53  e860cb0000             call     0x41a5b8 ; BatimentEstHabiter
0040da58  6689942404040000       mov      word ptr [esp + 0x404], dx
0040da60  84c0                   test     al, al
0040da62  7457                   je       0x40dabb
0040da64  b901000000             mov      ecx, 1
0040da69  31c0                   xor      eax, eax
0040da6b  bbaf1c0000             mov      ebx, 0x1caf
0040da70  8a4504                 mov      al, byte ptr [ebp + 4]
0040da73  0fbfd7                 movsx    edx, di
0040da76  50                     push     eax
0040da77  0fbfc6                 movsx    eax, si
0040da7a  e8d6e90400             call     0x45c455 ; PastePlayerCmp
0040da7f  8b1c24                 mov      ebx, dword ptr [esp]
0040da82  66a1808f5000           mov      ax, word ptr [0x508f80]
0040da88  01d8                   add      eax, ebx
0040da8a  30e4                   xor      ah, ah
0040da8c  8b942402040000         mov      edx, dword ptr [esp + 0x402]
0040da93  2403                   and      al, 3
0040da95  31db                   xor      ebx, ebx
0040da97  05b01c0000             add      eax, 0x1cb0
0040da9c  b901000000             mov      ecx, 1
0040daa1  6689c3                 mov      bx, ax
0040daa4  8b84248e030000         mov      eax, dword ptr [esp + 0x38e]
0040daab  c1fa10                 sar      edx, 0x10
0040daae  c1f810                 sar      eax, 0x10
0040dab1  e891d70400             call     0x45b247 ; PasteBobCmp
0040dab6  e99c000000             jmp      0x40db57 ;
0040dabb  b901000000             mov      ecx, 1
0040dac0  0fbfc7                 movsx    eax, di
0040dac3  bbaf1c0000             mov      ebx, 0x1caf
0040dac8  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040dacf  0fbfc6                 movsx    eax, si
0040dad2  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040dad9  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040dae0  e862d70400             call     0x45b247 ; PasteBobCmp
0040dae5  8b842402040000         mov      eax, dword ptr [esp + 0x402]
0040daec  c1f810                 sar      eax, 0x10
0040daef  b901000000             mov      ecx, 1
0040daf4  89842498000000         mov      dword ptr [esp + 0x98], eax
0040dafb  8b84248e030000         mov      eax, dword ptr [esp + 0x38e]
0040db02  bbb01c0000             mov      ebx, 0x1cb0
0040db07  c1f810                 sar      eax, 0x10
0040db0a  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040db11  89842494000000         mov      dword ptr [esp + 0x94], eax
0040db18  e82ad70400             call     0x45b247 ; PasteBobCmp
0040db1d  b901000000             mov      ecx, 1
0040db22  bbaf1c0000             mov      ebx, 0x1caf
0040db27  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040db2e  8b84249c000000         mov      eax, dword ptr [esp + 0x9c]
0040db35  e876e10400             call     0x45bcb0 ; PasteGrisCmp
0040db3a  b901000000             mov      ecx, 1
0040db3f  bbb01c0000             mov      ebx, 0x1cb0
0040db44  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040db4b  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040db52  e859e10400             call     0x45bcb0 ; PasteGrisCmp
0040db57  31c0                   xor      eax, eax
0040db59  668b4506               mov      ax, word ptr [ebp + 6]
0040db5d  85c0                   test     eax, eax
0040db5f  0f8edd170000           jle      0x40f342
0040db65  6a12                   push     0x12
0040db67  e976faffff             jmp      0x40d5e2 ;
0040db6c  31c0                   xor      eax, eax
0040db6e  668b0d26875000         mov      cx, word ptr [0x508726]
0040db75  6689d0                 mov      ax, dx
0040db78  668b1524875000         mov      dx, word ptr [0x508724]
0040db7f  c1e105                 shl      ecx, 5
0040db82  c1e205                 shl      edx, 5
0040db85  49                     dec      ecx
0040db86  4a                     dec      edx
0040db87  83f864                 cmp      eax, 0x64
0040db8a  7d75                   jge      0x40dc01
0040db8c  8994249c020000         mov      dword ptr [esp + 0x29c], edx
0040db93  ba64000000             mov      edx, 0x64
0040db98  29c2                   sub      edx, eax
0040db9a  6bd253                 imul     edx, edx, 0x53
0040db9d  bb64000000             mov      ebx, 0x64
0040dba2  89d0                   mov      eax, edx
0040dba4  c1fa1f                 sar      edx, 0x1f
0040dba7  f7fb                   idiv     ebx
0040dba9  0fbfd7                 movsx    edx, di
0040dbac  01d0                   add      eax, edx
0040dbae  0fbfd6                 movsx    edx, si
0040dbb1  89b4246c040000         mov      dword ptr [esp + 0x46c], esi
0040dbb8  85d2                   test     edx, edx
0040dbba  7d09                   jge      0x40dbc5
0040dbbc  31d2                   xor      edx, edx
0040dbbe  8994246c040000         mov      dword ptr [esp + 0x46c], edx
0040dbc5  0fbfd0                 movsx    edx, ax
0040dbc8  85d2                   test     edx, edx
0040dbca  7d02                   jge      0x40dbce
0040dbcc  31c0                   xor      eax, eax
0040dbce  81e1ffff0000           and      ecx, 0xffff
0040dbd4  31d2                   xor      edx, edx
0040dbd6  31db                   xor      ebx, ebx
0040dbd8  6689c2                 mov      dx, ax
0040dbdb  31c0                   xor      eax, eax
0040dbdd  668b9c249c020000       mov      bx, word ptr [esp + 0x29c]
0040dbe5  668b84246c040000       mov      ax, word ptr [esp + 0x46c]
0040dbed  e827190000             call     0x40f519 ; SetClipping
0040dbf2  b901000000             mov      ecx, 1
0040dbf7  bbae1c0000             mov      ebx, 0x1cae
0040dbfc  e911a8ffff             jmp      0x408412 ;
0040dc01  89942490020000         mov      dword ptr [esp + 0x290], edx
0040dc08  83e864                 sub      eax, 0x64
0040dc0b  ba64000000             mov      edx, 0x64
0040dc10  29c2                   sub      edx, eax
0040dc12  6bd253                 imul     edx, edx, 0x53
0040dc15  bb64000000             mov      ebx, 0x64
0040dc1a  89d0                   mov      eax, edx
0040dc1c  c1fa1f                 sar      edx, 0x1f
0040dc1f  f7fb                   idiv     ebx
0040dc21  0fbfd7                 movsx    edx, di
0040dc24  01d0                   add      eax, edx
0040dc26  31d2                   xor      edx, edx
0040dc28  668b1526875000         mov      dx, word ptr [0x508726]
0040dc2f  898c2428020000         mov      dword ptr [esp + 0x228], ecx
0040dc36  c1e205                 shl      edx, 5
0040dc39  0fbfd8                 movsx    ebx, ax
0040dc3c  4a                     dec      edx
0040dc3d  6689b42400030000       mov      word ptr [esp + 0x300], si
0040dc45  39d3                   cmp      ebx, edx
0040dc47  7e02                   jle      0x40dc4b
0040dc49  89c8                   mov      eax, ecx
0040dc4b  31c9                   xor      ecx, ecx
0040dc4d  31db                   xor      ebx, ebx
0040dc4f  31d2                   xor      edx, edx
0040dc51  668b9c2490020000       mov      bx, word ptr [esp + 0x290]
0040dc59  6689c1                 mov      cx, ax
0040dc5c  31c0                   xor      eax, eax
0040dc5e  0fbfef                 movsx    ebp, di
0040dc61  e8b3180000             call     0x40f519 ; SetClipping
0040dc66  b901000000             mov      ecx, 1
0040dc6b  bbae1c0000             mov      ebx, 0x1cae
0040dc70  0fbfc6                 movsx    eax, si
0040dc73  89ea                   mov      edx, ebp
0040dc75  e8cdd50400             call     0x45b247 ; PasteBobCmp
0040dc7a  31c0                   xor      eax, eax
0040dc7c  668b8424b0020000       mov      ax, word ptr [esp + 0x2b0]
0040dc84  ba64000000             mov      edx, 0x64
0040dc89  83e864                 sub      eax, 0x64
0040dc8c  29c2                   sub      edx, eax
0040dc8e  6bd253                 imul     edx, edx, 0x53
0040dc91  bb64000000             mov      ebx, 0x64
0040dc96  89d0                   mov      eax, edx
0040dc98  c1fa1f                 sar      edx, 0x1f
0040dc9b  f7fb                   idiv     ebx
0040dc9d  8b9424fe020000         mov      edx, dword ptr [esp + 0x2fe]
0040dca4  c1fa10                 sar      edx, 0x10
0040dca7  01e8                   add      eax, ebp
0040dca9  85d2                   test     edx, edx
0040dcab  7d0a                   jge      0x40dcb7
0040dcad  31db                   xor      ebx, ebx
0040dcaf  66899c2400030000       mov      word ptr [esp + 0x300], bx
0040dcb7  0fbfd0                 movsx    edx, ax
0040dcba  85d2                   test     edx, edx
0040dcbc  7d02                   jge      0x40dcc0
0040dcbe  31c0                   xor      eax, eax
0040dcc0  31c9                   xor      ecx, ecx
0040dcc2  31db                   xor      ebx, ebx
0040dcc4  31d2                   xor      edx, edx
0040dcc6  668b8c2428020000       mov      cx, word ptr [esp + 0x228]
0040dcce  6689c2                 mov      dx, ax
0040dcd1  31c0                   xor      eax, eax
0040dcd3  668b9c2490020000       mov      bx, word ptr [esp + 0x290]
0040dcdb  668b842400030000       mov      ax, word ptr [esp + 0x300]
0040dce3  e831180000             call     0x40f519 ; SetClipping
0040dce8  b901000000             mov      ecx, 1
0040dced  0fbfc7                 movsx    eax, di
0040dcf0  bbaf1c0000             mov      ebx, 0x1caf
0040dcf5  8984243c010000         mov      dword ptr [esp + 0x13c], eax
0040dcfc  0fbfc6                 movsx    eax, si
0040dcff  8b94243c010000         mov      edx, dword ptr [esp + 0x13c]
0040dd06  89442428               mov      dword ptr [esp + 0x28], eax
0040dd0a  e838d50400             call     0x45b247 ; PasteBobCmp
0040dd0f  89f8                   mov      eax, edi
0040dd11  051a000000             add      eax, 0x1a
0040dd16  0fbfe8                 movsx    ebp, ax
0040dd19  89f0                   mov      eax, esi
0040dd1b  b901000000             mov      ecx, 1
0040dd20  0528000000             add      eax, 0x28
0040dd25  bbb01c0000             mov      ebx, 0x1cb0
0040dd2a  98                     cwde
0040dd2b  89ea                   mov      edx, ebp
0040dd2d  8984246c010000         mov      dword ptr [esp + 0x16c], eax
0040dd34  e80ed50400             call     0x45b247 ; PasteBobCmp
0040dd39  31c0                   xor      eax, eax
0040dd3b  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040dd43  e870c80000             call     0x41a5b8 ; BatimentEstHabiter
0040dd48  84c0                   test     al, al
0040dd4a  0f85f2150000           jne      0x40f342
0040dd50  b901000000             mov      ecx, 1
0040dd55  bbaf1c0000             mov      ebx, 0x1caf
0040dd5a  8b94243c010000         mov      edx, dword ptr [esp + 0x13c]
0040dd61  8b442428               mov      eax, dword ptr [esp + 0x28]
0040dd65  e846df0400             call     0x45bcb0 ; PasteGrisCmp
0040dd6a  b901000000             mov      ecx, 1
0040dd6f  bbb01c0000             mov      ebx, 0x1cb0
0040dd74  8b84246c010000         mov      eax, dword ptr [esp + 0x16c]
0040dd7b  e9eba7ffff             jmp      0x40856b ;
0040dd80  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040dd85  01c8                   add      eax, ecx
0040dd87  f6400180               test     byte ptr [eax + 1], 0x80
0040dd8b  7415                   je       0x40dda2
0040dd8d  668b00                 mov      ax, word ptr [eax]
0040dd90  25e07f0000             and      eax, 0x7fe0
0040dd95  89c2                   mov      edx, eax
0040dd97  81e2ffff0000           and      edx, 0xffff
0040dd9d  c1fa05                 sar      edx, 5
0040dda0  eb05                   jmp      0x40dda7 ;
0040dda2  baffff0000             mov      edx, 0xffff
0040dda7  89942410020000         mov      dword ptr [esp + 0x210], edx
0040ddae  31d2                   xor      edx, edx
0040ddb0  668b942410020000       mov      dx, word ptr [esp + 0x210]
0040ddb8  81faffff0000           cmp      edx, 0xffff
0040ddbe  0f84cd160000           je       0x40f491
0040ddc4  89d5                   mov      ebp, edx
0040ddc6  8b742408               mov      esi, dword ptr [esp + 8]
0040ddca  c1e504                 shl      ebp, 4
0040ddcd  8b7c2404               mov      edi, dword ptr [esp + 4]
0040ddd1  01d5                   add      ebp, edx
0040ddd3  89d0                   mov      eax, edx
0040ddd5  c1e502                 shl      ebp, 2
0040ddd8  e808cb0000             call     0x41a8e5 ; BatimentGetEtat
0040dddd  01d5                   add      ebp, edx
0040dddf  89842418020000         mov      dword ptr [esp + 0x218], eax
0040dde6  c1e502                 shl      ebp, 2
0040dde9  89c2                   mov      edx, eax
0040ddeb  81c5c8a04900           add      ebp, 0x49a0c8
0040ddf1  31c0                   xor      eax, eax
0040ddf3  83ee19                 sub      esi, 0x19
0040ddf6  8a4505                 mov      al, byte ptr [ebp + 5]
0040ddf9  83ef25                 sub      edi, 0x25
0040ddfc  83f805                 cmp      eax, 5
0040ddff  740e                   je       0x40de0f
0040de01  83f803                 cmp      eax, 3
0040de04  7409                   je       0x40de0f
0040de06  83f804                 cmp      eax, 4
0040de09  0f85f5010000           jne      0x40e004
0040de0f  31c0                   xor      eax, eax
0040de11  8a4505                 mov      al, byte ptr [ebp + 5]
0040de14  83f803                 cmp      eax, 3
0040de17  0f8500010000           jne      0x40df1d
0040de1d  31c0                   xor      eax, eax
0040de1f  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040de27  e88cc70000             call     0x41a5b8 ; BatimentEstHabiter
0040de2c  84c0                   test     al, al
0040de2e  0f85e9000000           jne      0x40df1d
0040de34  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040de3a  31d2                   xor      edx, edx
0040de3c  88da                   mov      dl, bl
0040de3e  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040de44  81e2ff000000           and      edx, 0xff
0040de4a  b903000000             mov      ecx, 3
0040de4f  89d0                   mov      eax, edx
0040de51  c1fa1f                 sar      edx, 0x1f
0040de54  f7f9                   idiv     ecx
0040de56  0fbfff                 movsx    edi, di
0040de59  01fa                   add      edx, edi
0040de5b  83c239                 add      edx, 0x39
0040de5e  fec3                   inc      bl
0040de60  89d1                   mov      ecx, edx
0040de62  31d2                   xor      edx, edx
0040de64  88da                   mov      dl, bl
0040de66  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040de6c  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040de72  b803000000             mov      eax, 3
0040de77  81e2ff000000           and      edx, 0xff
0040de7d  8944247c               mov      dword ptr [esp + 0x7c], eax
0040de81  89d0                   mov      eax, edx
0040de83  c1fa1f                 sar      edx, 0x1f
0040de86  f77c247c               idiv     dword ptr [esp + 0x7c]
0040de8a  fec3                   inc      bl
0040de8c  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040de92  01fa                   add      edx, edi
0040de94  31c0                   xor      eax, eax
0040de96  81c2c8000000           add      edx, 0xc8
0040de9c  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040dea3  29c2                   sub      edx, eax
0040dea5  0fbfc2                 movsx    eax, dx
0040dea8  89d7                   mov      edi, edx
0040deaa  85c0                   test     eax, eax
0040deac  7d02                   jge      0x40deb0
0040deae  31d7                   xor      edi, edx
0040deb0  31c0                   xor      eax, eax
0040deb2  66a126875000           mov      ax, word ptr [0x508726]
0040deb8  c1e005                 shl      eax, 5
0040debb  0fbfd1                 movsx    edx, cx
0040debe  48                     dec      eax
0040debf  39c2                   cmp      edx, eax
0040dec1  7e0b                   jle      0x40dece
0040dec3  668b0d26875000         mov      cx, word ptr [0x508726]
0040deca  c1e105                 shl      ecx, 5
0040decd  49                     dec      ecx
0040dece  66a124875000           mov      ax, word ptr [0x508724]
0040ded4  81e1ffff0000           and      ecx, 0xffff
0040deda  31db                   xor      ebx, ebx
0040dedc  31d2                   xor      edx, edx
0040dede  c1e005                 shl      eax, 5
0040dee1  6689fa                 mov      dx, di
0040dee4  6689c3                 mov      bx, ax
0040dee7  31c0                   xor      eax, eax
0040dee9  e82b160000             call     0x40f519 ; SetClipping
0040deee  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040def4  31d2                   xor      edx, edx
0040def6  88da                   mov      dl, bl
0040def8  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040defe  81e2ff000000           and      edx, 0xff
0040df04  b903000000             mov      ecx, 3
0040df09  89d0                   mov      eax, edx
0040df0b  c1fa1f                 sar      edx, 0x1f
0040df0e  f7f9                   idiv     ecx
0040df10  fec3                   inc      bl
0040df12  0fbff6                 movsx    esi, si
0040df15  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040df1b  01d6                   add      esi, edx
0040df1d  31c0                   xor      eax, eax
0040df1f  89f1                   mov      ecx, esi
0040df21  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040df29  89fa                   mov      edx, edi
0040df2b  e888c60000             call     0x41a5b8 ; BatimentEstHabiter
0040df30  83ea19                 sub      edx, 0x19
0040df33  83e906                 sub      ecx, 6
0040df36  66899424f0020000       mov      word ptr [esp + 0x2f0], dx
0040df3e  84c0                   test     al, al
0040df40  743d                   je       0x40df7f
0040df42  31c0                   xor      eax, eax
0040df44  8a4504                 mov      al, byte ptr [ebp + 4]
0040df47  50                     push     eax
0040df48  30e4                   xor      ah, ah
0040df4a  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040df50  89c2                   mov      edx, eax
0040df52  4a                     dec      edx
0040df53  c1e202                 shl      edx, 2
0040df56  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040df59  81c2d01c0000           add      edx, 0x1cd0
0040df5f  31db                   xor      ebx, ebx
0040df61  01d0                   add      eax, edx
0040df63  8b9424f2020000         mov      edx, dword ptr [esp + 0x2f2]
0040df6a  6689c3                 mov      bx, ax
0040df6d  c1fa10                 sar      edx, 0x10
0040df70  0fbfc1                 movsx    eax, cx
0040df73  b901000000             mov      ecx, 1
0040df78  e8d8e40400             call     0x45c455 ; PastePlayerCmp
0040df7d  eb70                   jmp      0x40dfef ;
0040df7f  30e4                   xor      ah, ah
0040df81  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040df87  48                     dec      eax
0040df88  c1e002                 shl      eax, 2
0040df8b  31db                   xor      ebx, ebx
0040df8d  05d01c0000             add      eax, 0x1cd0
0040df92  6689c3                 mov      bx, ax
0040df95  8b8424ee020000         mov      eax, dword ptr [esp + 0x2ee]
0040df9c  c1f810                 sar      eax, 0x10
0040df9f  89842498000000         mov      dword ptr [esp + 0x98], eax
0040dfa6  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040dfad  0fbfc1                 movsx    eax, cx
0040dfb0  b901000000             mov      ecx, 1
0040dfb5  89842494000000         mov      dword ptr [esp + 0x94], eax
0040dfbc  e886d20400             call     0x45b247 ; PasteBobCmp
0040dfc1  30e4                   xor      ah, ah
0040dfc3  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040dfc9  48                     dec      eax
0040dfca  b901000000             mov      ecx, 1
0040dfcf  c1e002                 shl      eax, 2
0040dfd2  31db                   xor      ebx, ebx
0040dfd4  05d01c0000             add      eax, 0x1cd0
0040dfd9  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040dfe0  6689c3                 mov      bx, ax
0040dfe3  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040dfea  e8c1dc0400             call     0x45bcb0 ; PasteGrisCmp
0040dfef  31c0                   xor      eax, eax
0040dff1  668b4506               mov      ax, word ptr [ebp + 6]
0040dff5  85c0                   test     eax, eax
0040dff7  0f8e45130000           jle      0x40f342
0040dffd  6a0a                   push     0xa
0040dfff  e9def5ffff             jmp      0x40d5e2 ;
0040e004  31c0                   xor      eax, eax
0040e006  668b0d26875000         mov      cx, word ptr [0x508726]
0040e00d  6689d0                 mov      ax, dx
0040e010  668b1524875000         mov      dx, word ptr [0x508724]
0040e017  c1e105                 shl      ecx, 5
0040e01a  c1e205                 shl      edx, 5
0040e01d  49                     dec      ecx
0040e01e  4a                     dec      edx
0040e01f  83f864                 cmp      eax, 0x64
0040e022  0f8d7e000000           jge      0x40e0a6
0040e028  8994242c030000         mov      dword ptr [esp + 0x32c], edx
0040e02f  ba64000000             mov      edx, 0x64
0040e034  29c2                   sub      edx, eax
0040e036  89d0                   mov      eax, edx
0040e038  c1e003                 shl      eax, 3
0040e03b  29d0                   sub      eax, edx
0040e03d  c1e003                 shl      eax, 3
0040e040  01c2                   add      edx, eax
0040e042  bb64000000             mov      ebx, 0x64
0040e047  89d0                   mov      eax, edx
0040e049  c1fa1f                 sar      edx, 0x1f
0040e04c  f7fb                   idiv     ebx
0040e04e  0fbfd7                 movsx    edx, di
0040e051  01d0                   add      eax, edx
0040e053  0fbfd6                 movsx    edx, si
0040e056  89b42460030000         mov      dword ptr [esp + 0x360], esi
0040e05d  85d2                   test     edx, edx
0040e05f  7d09                   jge      0x40e06a
0040e061  31d2                   xor      edx, edx
0040e063  89942460030000         mov      dword ptr [esp + 0x360], edx
0040e06a  0fbfd0                 movsx    edx, ax
0040e06d  85d2                   test     edx, edx
0040e06f  7d02                   jge      0x40e073
0040e071  31c0                   xor      eax, eax
0040e073  81e1ffff0000           and      ecx, 0xffff
0040e079  31d2                   xor      edx, edx
0040e07b  31db                   xor      ebx, ebx
0040e07d  6689c2                 mov      dx, ax
0040e080  31c0                   xor      eax, eax
0040e082  668b9c242c030000       mov      bx, word ptr [esp + 0x32c]
0040e08a  668b842460030000       mov      ax, word ptr [esp + 0x360]
0040e092  e882140000             call     0x40f519 ; SetClipping
0040e097  b901000000             mov      ecx, 1
0040e09c  bbb41c0000             mov      ebx, 0x1cb4
0040e0a1  e96ca3ffff             jmp      0x408412 ;
0040e0a6  899424ac030000         mov      dword ptr [esp + 0x3ac], edx
0040e0ad  83e864                 sub      eax, 0x64
0040e0b0  ba64000000             mov      edx, 0x64
0040e0b5  29c2                   sub      edx, eax
0040e0b7  89d0                   mov      eax, edx
0040e0b9  c1e203                 shl      edx, 3
0040e0bc  29c2                   sub      edx, eax
0040e0be  c1e203                 shl      edx, 3
0040e0c1  01c2                   add      edx, eax
0040e0c3  bb64000000             mov      ebx, 0x64
0040e0c8  89d0                   mov      eax, edx
0040e0ca  c1fa1f                 sar      edx, 0x1f
0040e0cd  f7fb                   idiv     ebx
0040e0cf  0fbfd7                 movsx    edx, di
0040e0d2  01d0                   add      eax, edx
0040e0d4  31d2                   xor      edx, edx
0040e0d6  668b1526875000         mov      dx, word ptr [0x508726]
0040e0dd  898c2438030000         mov      dword ptr [esp + 0x338], ecx
0040e0e4  c1e205                 shl      edx, 5
0040e0e7  0fbfd8                 movsx    ebx, ax
0040e0ea  4a                     dec      edx
0040e0eb  6689b42480030000       mov      word ptr [esp + 0x380], si
0040e0f3  39d3                   cmp      ebx, edx
0040e0f5  7e02                   jle      0x40e0f9
0040e0f7  89c8                   mov      eax, ecx
0040e0f9  31c9                   xor      ecx, ecx
0040e0fb  31db                   xor      ebx, ebx
0040e0fd  31d2                   xor      edx, edx
0040e0ff  668b9c24ac030000       mov      bx, word ptr [esp + 0x3ac]
0040e107  6689c1                 mov      cx, ax
0040e10a  31c0                   xor      eax, eax
0040e10c  0fbfef                 movsx    ebp, di
0040e10f  e805140000             call     0x40f519 ; SetClipping
0040e114  b901000000             mov      ecx, 1
0040e119  bbb41c0000             mov      ebx, 0x1cb4
0040e11e  0fbfc6                 movsx    eax, si
0040e121  89ea                   mov      edx, ebp
0040e123  e81fd10400             call     0x45b247 ; PasteBobCmp
0040e128  31c0                   xor      eax, eax
0040e12a  668b842418020000       mov      ax, word ptr [esp + 0x218]
0040e132  ba64000000             mov      edx, 0x64
0040e137  83e864                 sub      eax, 0x64
0040e13a  29c2                   sub      edx, eax
0040e13c  89d0                   mov      eax, edx
0040e13e  c1e003                 shl      eax, 3
0040e141  29d0                   sub      eax, edx
0040e143  c1e003                 shl      eax, 3
0040e146  01c2                   add      edx, eax
0040e148  bb64000000             mov      ebx, 0x64
0040e14d  89d0                   mov      eax, edx
0040e14f  c1fa1f                 sar      edx, 0x1f
0040e152  f7fb                   idiv     ebx
0040e154  8b94247e030000         mov      edx, dword ptr [esp + 0x37e]
0040e15b  c1fa10                 sar      edx, 0x10
0040e15e  01e8                   add      eax, ebp
0040e160  85d2                   test     edx, edx
0040e162  7d0a                   jge      0x40e16e
0040e164  31c9                   xor      ecx, ecx
0040e166  66898c2480030000       mov      word ptr [esp + 0x380], cx
0040e16e  0fbfd0                 movsx    edx, ax
0040e171  85d2                   test     edx, edx
0040e173  7d02                   jge      0x40e177
0040e175  31c0                   xor      eax, eax
0040e177  31c9                   xor      ecx, ecx
0040e179  31db                   xor      ebx, ebx
0040e17b  31d2                   xor      edx, edx
0040e17d  668b8c2438030000       mov      cx, word ptr [esp + 0x338]
0040e185  6689c2                 mov      dx, ax
0040e188  31c0                   xor      eax, eax
0040e18a  668b9c24ac030000       mov      bx, word ptr [esp + 0x3ac]
0040e192  668b842480030000       mov      ax, word ptr [esp + 0x380]
0040e19a  e87a130000             call     0x40f519 ; SetClipping
0040e19f  89f8                   mov      eax, edi
0040e1a1  83e819                 sub      eax, 0x19
0040e1a4  98                     cwde
0040e1a5  898424d0000000         mov      dword ptr [esp + 0xd0], eax
0040e1ac  89f0                   mov      eax, esi
0040e1ae  b901000000             mov      ecx, 1
0040e1b3  83e806                 sub      eax, 6
0040e1b6  bbd01c0000             mov      ebx, 0x1cd0
0040e1bb  0fbfe8                 movsx    ebp, ax
0040e1be  8b9424d0000000         mov      edx, dword ptr [esp + 0xd0]
0040e1c5  89e8                   mov      eax, ebp
0040e1c7  e87bd00400             call     0x45b247 ; PasteBobCmp
0040e1cc  31c0                   xor      eax, eax
0040e1ce  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040e1d6  e8ddc30000             call     0x41a5b8 ; BatimentEstHabiter
0040e1db  84c0                   test     al, al
0040e1dd  0f855f110000           jne      0x40f342
0040e1e3  b901000000             mov      ecx, 1
0040e1e8  bbd01c0000             mov      ebx, 0x1cd0
0040e1ed  8b9424d0000000         mov      edx, dword ptr [esp + 0xd0]
0040e1f4  e95db1ffff             jmp      0x409356 ;
0040e1f9  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040e1fe  01c8                   add      eax, ecx
0040e200  f6400180               test     byte ptr [eax + 1], 0x80
0040e204  7415                   je       0x40e21b
0040e206  668b00                 mov      ax, word ptr [eax]
0040e209  25e07f0000             and      eax, 0x7fe0
0040e20e  89c2                   mov      edx, eax
0040e210  81e2ffff0000           and      edx, 0xffff
0040e216  c1fa05                 sar      edx, 5
0040e219  eb05                   jmp      0x40e220 ;
0040e21b  baffff0000             mov      edx, 0xffff
0040e220  31c0                   xor      eax, eax
0040e222  6689d0                 mov      ax, dx
0040e225  89942410020000         mov      dword ptr [esp + 0x210], edx
0040e22c  3dffff0000             cmp      eax, 0xffff
0040e231  0f845a120000           je       0x40f491
0040e237  89c5                   mov      ebp, eax
0040e239  c1e504                 shl      ebp, 4
0040e23c  01c5                   add      ebp, eax
0040e23e  8b742408               mov      esi, dword ptr [esp + 8]
0040e242  c1e502                 shl      ebp, 2
0040e245  8b7c2404               mov      edi, dword ptr [esp + 4]
0040e249  01c5                   add      ebp, eax
0040e24b  e895c60000             call     0x41a8e5 ; BatimentGetEtat
0040e250  c1e502                 shl      ebp, 2
0040e253  89c2                   mov      edx, eax
0040e255  89842468030000         mov      dword ptr [esp + 0x368], eax
0040e25c  81c5c8a04900           add      ebp, 0x49a0c8
0040e262  31c0                   xor      eax, eax
0040e264  83ee30                 sub      esi, 0x30
0040e267  8a4505                 mov      al, byte ptr [ebp + 5]
0040e26a  83ef61                 sub      edi, 0x61
0040e26d  83f805                 cmp      eax, 5
0040e270  740e                   je       0x40e280
0040e272  83f803                 cmp      eax, 3
0040e275  7409                   je       0x40e280
0040e277  83f804                 cmp      eax, 4
0040e27a  0f85e5030000           jne      0x40e665
0040e280  31c0                   xor      eax, eax
0040e282  8a4505                 mov      al, byte ptr [ebp + 5]
0040e285  83f803                 cmp      eax, 3
0040e288  0f8509010000           jne      0x40e397
0040e28e  31c0                   xor      eax, eax
0040e290  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040e298  e81bc30000             call     0x41a5b8 ; BatimentEstHabiter
0040e29d  84c0                   test     al, al
0040e29f  0f85f2000000           jne      0x40e397
0040e2a5  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040e2ab  31d2                   xor      edx, edx
0040e2ad  88da                   mov      dl, bl
0040e2af  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040e2b5  81e2ff000000           and      edx, 0xff
0040e2bb  b903000000             mov      ecx, 3
0040e2c0  89d0                   mov      eax, edx
0040e2c2  c1fa1f                 sar      edx, 0x1f
0040e2c5  f7f9                   idiv     ecx
0040e2c7  0fbfff                 movsx    edi, di
0040e2ca  01fa                   add      edx, edi
0040e2cc  81c281000000           add      edx, 0x81
0040e2d2  fec3                   inc      bl
0040e2d4  89d1                   mov      ecx, edx
0040e2d6  31d2                   xor      edx, edx
0040e2d8  88da                   mov      dl, bl
0040e2da  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040e2e0  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040e2e6  b803000000             mov      eax, 3
0040e2eb  81e2ff000000           and      edx, 0xff
0040e2f1  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040e2f8  89d0                   mov      eax, edx
0040e2fa  c1fa1f                 sar      edx, 0x1f
0040e2fd  f7bc24a4010000         idiv     dword ptr [esp + 0x1a4]
0040e304  fec3                   inc      bl
0040e306  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040e30c  01fa                   add      edx, edi
0040e30e  31c0                   xor      eax, eax
0040e310  81c2c8000000           add      edx, 0xc8
0040e316  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040e31d  29c2                   sub      edx, eax
0040e31f  0fbfc2                 movsx    eax, dx
0040e322  89d7                   mov      edi, edx
0040e324  85c0                   test     eax, eax
0040e326  7d02                   jge      0x40e32a
0040e328  31d7                   xor      edi, edx
0040e32a  31c0                   xor      eax, eax
0040e32c  66a126875000           mov      ax, word ptr [0x508726]
0040e332  c1e005                 shl      eax, 5
0040e335  0fbfd1                 movsx    edx, cx
0040e338  48                     dec      eax
0040e339  39c2                   cmp      edx, eax
0040e33b  7e0b                   jle      0x40e348
0040e33d  668b0d26875000         mov      cx, word ptr [0x508726]
0040e344  c1e105                 shl      ecx, 5
0040e347  49                     dec      ecx
0040e348  66a124875000           mov      ax, word ptr [0x508724]
0040e34e  81e1ffff0000           and      ecx, 0xffff
0040e354  31db                   xor      ebx, ebx
0040e356  31d2                   xor      edx, edx
0040e358  c1e005                 shl      eax, 5
0040e35b  6689fa                 mov      dx, di
0040e35e  6689c3                 mov      bx, ax
0040e361  31c0                   xor      eax, eax
0040e363  e8b1110000             call     0x40f519 ; SetClipping
0040e368  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040e36e  31d2                   xor      edx, edx
0040e370  88da                   mov      dl, bl
0040e372  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040e378  81e2ff000000           and      edx, 0xff
0040e37e  b903000000             mov      ecx, 3
0040e383  89d0                   mov      eax, edx
0040e385  c1fa1f                 sar      edx, 0x1f
0040e388  f7f9                   idiv     ecx
0040e38a  fec3                   inc      bl
0040e38c  0fbff6                 movsx    esi, si
0040e38f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040e395  01d6                   add      esi, edx
0040e397  89f2                   mov      edx, esi
0040e399  83c20f                 add      edx, 0xf
0040e39c  31c0                   xor      eax, eax
0040e39e  6689942488040000       mov      word ptr [esp + 0x488], dx
0040e3a6  89fa                   mov      edx, edi
0040e3a8  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040e3b0  83c22d                 add      edx, 0x2d
0040e3b3  e800c20000             call     0x41a5b8 ; BatimentEstHabiter
0040e3b8  66899424bc020000       mov      word ptr [esp + 0x2bc], dx
0040e3c0  84c0                   test     al, al
0040e3c2  0f8423010000           je       0x40e4eb
0040e3c8  b901000000             mov      ecx, 1
0040e3cd  31c0                   xor      eax, eax
0040e3cf  bbb61c0000             mov      ebx, 0x1cb6
0040e3d4  8a4504                 mov      al, byte ptr [ebp + 4]
0040e3d7  0fbfd7                 movsx    edx, di
0040e3da  50                     push     eax
0040e3db  0fbfc6                 movsx    eax, si
0040e3de  e872e00400             call     0x45c455 ; PastePlayerCmp
0040e3e3  31c0                   xor      eax, eax
0040e3e5  668b457c               mov      ax, word ptr [ebp + 0x7c]
0040e3e9  3dfa000000             cmp      eax, 0xfa
0040e3ee  7e1a                   jle      0x40e40a
0040e3f0  8b9424ba020000         mov      edx, dword ptr [esp + 0x2ba]
0040e3f7  8b842486040000         mov      eax, dword ptr [esp + 0x486]
0040e3fe  b901000000             mov      ecx, 1
0040e403  bbb71c0000             mov      ebx, 0x1cb7
0040e408  eb18                   jmp      0x40e422 ;
0040e40a  8b9424ba020000         mov      edx, dword ptr [esp + 0x2ba]
0040e411  8b842486040000         mov      eax, dword ptr [esp + 0x486]
0040e418  b901000000             mov      ecx, 1
0040e41d  bbb81c0000             mov      ebx, 0x1cb8
0040e422  c1fa10                 sar      edx, 0x10
0040e425  c1f810                 sar      eax, 0x10
0040e428  e81ace0400             call     0x45b247 ; PasteBobCmp
0040e42d  89f3                   mov      ebx, esi
0040e42f  8b457e                 mov      eax, dword ptr [ebp + 0x7e]
0040e432  89fa                   mov      edx, edi
0040e434  c1f810                 sar      eax, 0x10
0040e437  83c34b                 add      ebx, 0x4b
0040e43a  83c231                 add      edx, 0x31
0040e43d  83f87d                 cmp      eax, 0x7d
0040e440  7e12                   jle      0x40e454
0040e442  b901000000             mov      ecx, 1
0040e447  0fbfd2                 movsx    edx, dx
0040e44a  0fbfc3                 movsx    eax, bx
0040e44d  bbb91c0000             mov      ebx, 0x1cb9
0040e452  eb10                   jmp      0x40e464 ;
0040e454  b901000000             mov      ecx, 1
0040e459  0fbfd2                 movsx    edx, dx
0040e45c  0fbfc3                 movsx    eax, bx
0040e45f  bbba1c0000             mov      ebx, 0x1cba
0040e464  e8decd0400             call     0x45b247 ; PasteBobCmp
0040e469  89f3                   mov      ebx, esi
0040e46b  8b8580000000           mov      eax, dword ptr [ebp + 0x80]
0040e471  89fa                   mov      edx, edi
0040e473  c1f810                 sar      eax, 0x10
0040e476  83c35e                 add      ebx, 0x5e
0040e479  83c245                 add      edx, 0x45
0040e47c  3db4000000             cmp      eax, 0xb4
0040e481  7e12                   jle      0x40e495
0040e483  b901000000             mov      ecx, 1
0040e488  0fbfd2                 movsx    edx, dx
0040e48b  0fbfc3                 movsx    eax, bx
0040e48e  bbbb1c0000             mov      ebx, 0x1cbb
0040e493  eb10                   jmp      0x40e4a5 ;
0040e495  b901000000             mov      ecx, 1
0040e49a  0fbfd2                 movsx    edx, dx
0040e49d  0fbfc3                 movsx    eax, bx
0040e4a0  bbbc1c0000             mov      ebx, 0x1cbc
0040e4a5  e89dcd0400             call     0x45b247 ; PasteBobCmp
0040e4aa  89f3                   mov      ebx, esi
0040e4ac  8b457c                 mov      eax, dword ptr [ebp + 0x7c]
0040e4af  89fa                   mov      edx, edi
0040e4b1  c1f810                 sar      eax, 0x10
0040e4b4  83c330                 add      ebx, 0x30
0040e4b7  83c261                 add      edx, 0x61
0040e4ba  83f850                 cmp      eax, 0x50
0040e4bd  7e1a                   jle      0x40e4d9
0040e4bf  b901000000             mov      ecx, 1
0040e4c4  0fbfd2                 movsx    edx, dx
0040e4c7  0fbfc3                 movsx    eax, bx
0040e4ca  bbbd1c0000             mov      ebx, 0x1cbd
0040e4cf  e873cd0400             call     0x45b247 ; PasteBobCmp
0040e4d4  e9f9f0ffff             jmp      0x40d5d2 ;
0040e4d9  b901000000             mov      ecx, 1
0040e4de  0fbfd2                 movsx    edx, dx
0040e4e1  0fbfc3                 movsx    eax, bx
0040e4e4  bbbe1c0000             mov      ebx, 0x1cbe
0040e4e9  ebe4                   jmp      0x40e4cf ;
0040e4eb  b901000000             mov      ecx, 1
0040e4f0  0fbfc7                 movsx    eax, di
0040e4f3  bbb61c0000             mov      ebx, 0x1cb6
0040e4f8  89842494000000         mov      dword ptr [esp + 0x94], eax
0040e4ff  0fbfc6                 movsx    eax, si
0040e502  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040e509  8944247c               mov      dword ptr [esp + 0x7c], eax
0040e50d  e835cd0400             call     0x45b247 ; PasteBobCmp
0040e512  8b8424ba020000         mov      eax, dword ptr [esp + 0x2ba]
0040e519  c1f810                 sar      eax, 0x10
0040e51c  b901000000             mov      ecx, 1
0040e521  89842498000000         mov      dword ptr [esp + 0x98], eax
0040e528  8b842486040000         mov      eax, dword ptr [esp + 0x486]
0040e52f  bbb71c0000             mov      ebx, 0x1cb7
0040e534  c1f810                 sar      eax, 0x10
0040e537  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040e53e  8984249c000000         mov      dword ptr [esp + 0x9c], eax
0040e545  e8fdcc0400             call     0x45b247 ; PasteBobCmp
0040e54a  89f8                   mov      eax, edi
0040e54c  0531000000             add      eax, 0x31
0040e551  98                     cwde
0040e552  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040e559  89f0                   mov      eax, esi
0040e55b  b901000000             mov      ecx, 1
0040e560  054b000000             add      eax, 0x4b
0040e565  bbb91c0000             mov      ebx, 0x1cb9
0040e56a  98                     cwde
0040e56b  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040e572  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040e579  e8c9cc0400             call     0x45b247 ; PasteBobCmp
0040e57e  89f8                   mov      eax, edi
0040e580  0545000000             add      eax, 0x45
0040e585  98                     cwde
0040e586  898424d4010000         mov      dword ptr [esp + 0x1d4], eax
0040e58d  89f0                   mov      eax, esi
0040e58f  b901000000             mov      ecx, 1
0040e594  055e000000             add      eax, 0x5e
0040e599  bbbb1c0000             mov      ebx, 0x1cbb
0040e59e  98                     cwde
0040e59f  8b9424d4010000         mov      edx, dword ptr [esp + 0x1d4]
0040e5a6  89442434               mov      dword ptr [esp + 0x34], eax
0040e5aa  e898cc0400             call     0x45b247 ; PasteBobCmp
0040e5af  89f8                   mov      eax, edi
0040e5b1  0561000000             add      eax, 0x61
0040e5b6  98                     cwde
0040e5b7  89442418               mov      dword ptr [esp + 0x18], eax
0040e5bb  89f0                   mov      eax, esi
0040e5bd  b901000000             mov      ecx, 1
0040e5c2  0530000000             add      eax, 0x30
0040e5c7  bbbd1c0000             mov      ebx, 0x1cbd
0040e5cc  98                     cwde
0040e5cd  8b542418               mov      edx, dword ptr [esp + 0x18]
0040e5d1  898424a0010000         mov      dword ptr [esp + 0x1a0], eax
0040e5d8  e86acc0400             call     0x45b247 ; PasteBobCmp
0040e5dd  b901000000             mov      ecx, 1
0040e5e2  bbb61c0000             mov      ebx, 0x1cb6
0040e5e7  8b942494000000         mov      edx, dword ptr [esp + 0x94]
0040e5ee  8b44247c               mov      eax, dword ptr [esp + 0x7c]
0040e5f2  e8b9d60400             call     0x45bcb0 ; PasteGrisCmp
0040e5f7  b901000000             mov      ecx, 1
0040e5fc  bbb71c0000             mov      ebx, 0x1cb7
0040e601  8b942498000000         mov      edx, dword ptr [esp + 0x98]
0040e608  8b84249c000000         mov      eax, dword ptr [esp + 0x9c]
0040e60f  e89cd60400             call     0x45bcb0 ; PasteGrisCmp
0040e614  b901000000             mov      ecx, 1
0040e619  bbb91c0000             mov      ebx, 0x1cb9
0040e61e  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040e625  8b8424b4000000         mov      eax, dword ptr [esp + 0xb4]
0040e62c  e87fd60400             call     0x45bcb0 ; PasteGrisCmp
0040e631  b901000000             mov      ecx, 1
0040e636  bbbb1c0000             mov      ebx, 0x1cbb
0040e63b  8b9424d4010000         mov      edx, dword ptr [esp + 0x1d4]
0040e642  8b442434               mov      eax, dword ptr [esp + 0x34]
0040e646  e865d60400             call     0x45bcb0 ; PasteGrisCmp
0040e64b  b901000000             mov      ecx, 1
0040e650  bbbd1c0000             mov      ebx, 0x1cbd
0040e655  8b542418               mov      edx, dword ptr [esp + 0x18]
0040e659  8b8424a0010000         mov      eax, dword ptr [esp + 0x1a0]
0040e660  e968efffff             jmp      0x40d5cd ;
0040e665  31c0                   xor      eax, eax
0040e667  668b0d26875000         mov      cx, word ptr [0x508726]
0040e66e  6689d0                 mov      ax, dx
0040e671  668b1524875000         mov      dx, word ptr [0x508724]
0040e678  c1e105                 shl      ecx, 5
0040e67b  c1e205                 shl      edx, 5
0040e67e  49                     dec      ecx
0040e67f  4a                     dec      edx
0040e680  83f864                 cmp      eax, 0x64
0040e683  0f8d79000000           jge      0x40e702
0040e689  89942434030000         mov      dword ptr [esp + 0x334], edx
0040e690  ba64000000             mov      edx, 0x64
0040e695  29c2                   sub      edx, eax
0040e697  89d0                   mov      eax, edx
0040e699  c1e007                 shl      eax, 7
0040e69c  01c2                   add      edx, eax
0040e69e  bb64000000             mov      ebx, 0x64
0040e6a3  89d0                   mov      eax, edx
0040e6a5  c1fa1f                 sar      edx, 0x1f
0040e6a8  f7fb                   idiv     ebx
0040e6aa  0fbfd7                 movsx    edx, di
0040e6ad  01d0                   add      eax, edx
0040e6af  0fbfd6                 movsx    edx, si
0040e6b2  89b424cc030000         mov      dword ptr [esp + 0x3cc], esi
0040e6b9  85d2                   test     edx, edx
0040e6bb  7d09                   jge      0x40e6c6
0040e6bd  31d2                   xor      edx, edx
0040e6bf  899424cc030000         mov      dword ptr [esp + 0x3cc], edx
0040e6c6  0fbfd0                 movsx    edx, ax
0040e6c9  85d2                   test     edx, edx
0040e6cb  7d02                   jge      0x40e6cf
0040e6cd  31c0                   xor      eax, eax
0040e6cf  81e1ffff0000           and      ecx, 0xffff
0040e6d5  31d2                   xor      edx, edx
0040e6d7  31db                   xor      ebx, ebx
0040e6d9  6689c2                 mov      dx, ax
0040e6dc  31c0                   xor      eax, eax
0040e6de  668b9c2434030000       mov      bx, word ptr [esp + 0x334]
0040e6e6  668b8424cc030000       mov      ax, word ptr [esp + 0x3cc]
0040e6ee  e8260e0000             call     0x40f519 ; SetClipping
0040e6f3  b901000000             mov      ecx, 1
0040e6f8  bbb51c0000             mov      ebx, 0x1cb5
0040e6fd  e9109dffff             jmp      0x408412 ;
0040e702  899424b4030000         mov      dword ptr [esp + 0x3b4], edx
0040e709  83e864                 sub      eax, 0x64
0040e70c  ba64000000             mov      edx, 0x64
0040e711  29c2                   sub      edx, eax
0040e713  89d0                   mov      eax, edx
0040e715  c1e007                 shl      eax, 7
0040e718  01c2                   add      edx, eax
0040e71a  bb64000000             mov      ebx, 0x64
0040e71f  89d0                   mov      eax, edx
0040e721  c1fa1f                 sar      edx, 0x1f
0040e724  f7fb                   idiv     ebx
0040e726  0fbfd7                 movsx    edx, di
0040e729  01d0                   add      eax, edx
0040e72b  31d2                   xor      edx, edx
0040e72d  668b1526875000         mov      dx, word ptr [0x508726]
0040e734  898c24ec020000         mov      dword ptr [esp + 0x2ec], ecx
0040e73b  c1e205                 shl      edx, 5
0040e73e  0fbfd8                 movsx    ebx, ax
0040e741  4a                     dec      edx
0040e742  6689b42408030000       mov      word ptr [esp + 0x308], si
0040e74a  39d3                   cmp      ebx, edx
0040e74c  7e02                   jle      0x40e750
0040e74e  89c8                   mov      eax, ecx
0040e750  31c9                   xor      ecx, ecx
0040e752  31db                   xor      ebx, ebx
0040e754  31d2                   xor      edx, edx
0040e756  668b9c24b4030000       mov      bx, word ptr [esp + 0x3b4]
0040e75e  6689c1                 mov      cx, ax
0040e761  31c0                   xor      eax, eax
0040e763  0fbfef                 movsx    ebp, di
0040e766  e8ae0d0000             call     0x40f519 ; SetClipping
0040e76b  b901000000             mov      ecx, 1
0040e770  bbb51c0000             mov      ebx, 0x1cb5
0040e775  0fbfc6                 movsx    eax, si
0040e778  89ea                   mov      edx, ebp
0040e77a  e8c8ca0400             call     0x45b247 ; PasteBobCmp
0040e77f  31c0                   xor      eax, eax
0040e781  668b842468030000       mov      ax, word ptr [esp + 0x368]
0040e789  ba64000000             mov      edx, 0x64
0040e78e  83e864                 sub      eax, 0x64
0040e791  29c2                   sub      edx, eax
0040e793  89d0                   mov      eax, edx
0040e795  c1e007                 shl      eax, 7
0040e798  01c2                   add      edx, eax
0040e79a  bb64000000             mov      ebx, 0x64
0040e79f  89d0                   mov      eax, edx
0040e7a1  c1fa1f                 sar      edx, 0x1f
0040e7a4  f7fb                   idiv     ebx
0040e7a6  8b942406030000         mov      edx, dword ptr [esp + 0x306]
0040e7ad  c1fa10                 sar      edx, 0x10
0040e7b0  01e8                   add      eax, ebp
0040e7b2  85d2                   test     edx, edx
0040e7b4  7d0a                   jge      0x40e7c0
0040e7b6  31db                   xor      ebx, ebx
0040e7b8  66899c2408030000       mov      word ptr [esp + 0x308], bx
0040e7c0  0fbfd0                 movsx    edx, ax
0040e7c3  85d2                   test     edx, edx
0040e7c5  7d02                   jge      0x40e7c9
0040e7c7  31c0                   xor      eax, eax
0040e7c9  31c9                   xor      ecx, ecx
0040e7cb  31db                   xor      ebx, ebx
0040e7cd  31d2                   xor      edx, edx
0040e7cf  668b8c24ec020000       mov      cx, word ptr [esp + 0x2ec]
0040e7d7  6689c2                 mov      dx, ax
0040e7da  31c0                   xor      eax, eax
0040e7dc  668b9c24b4030000       mov      bx, word ptr [esp + 0x3b4]
0040e7e4  668b842408030000       mov      ax, word ptr [esp + 0x308]
0040e7ec  0fbfee                 movsx    ebp, si
0040e7ef  e8250d0000             call     0x40f519 ; SetClipping
0040e7f4  b901000000             mov      ecx, 1
0040e7f9  0fbfc7                 movsx    eax, di
0040e7fc  bbb61c0000             mov      ebx, 0x1cb6
0040e801  89842454010000         mov      dword ptr [esp + 0x154], eax
0040e808  89c2                   mov      edx, eax
0040e80a  89e8                   mov      eax, ebp
0040e80c  e836ca0400             call     0x45b247 ; PasteBobCmp
0040e811  89f8                   mov      eax, edi
0040e813  052d000000             add      eax, 0x2d
0040e818  98                     cwde
0040e819  8944246c               mov      dword ptr [esp + 0x6c], eax
0040e81d  89f0                   mov      eax, esi
0040e81f  b901000000             mov      ecx, 1
0040e824  050f000000             add      eax, 0xf
0040e829  bbb71c0000             mov      ebx, 0x1cb7
0040e82e  98                     cwde
0040e82f  8b54246c               mov      edx, dword ptr [esp + 0x6c]
0040e833  89842434010000         mov      dword ptr [esp + 0x134], eax
0040e83a  e808ca0400             call     0x45b247 ; PasteBobCmp
0040e83f  89f8                   mov      eax, edi
0040e841  0531000000             add      eax, 0x31
0040e846  98                     cwde
0040e847  898424d0010000         mov      dword ptr [esp + 0x1d0], eax
0040e84e  89f0                   mov      eax, esi
0040e850  b901000000             mov      ecx, 1
0040e855  054b000000             add      eax, 0x4b
0040e85a  bbb91c0000             mov      ebx, 0x1cb9
0040e85f  98                     cwde
0040e860  8b9424d0010000         mov      edx, dword ptr [esp + 0x1d0]
0040e867  89842450010000         mov      dword ptr [esp + 0x150], eax
0040e86e  e8d4c90400             call     0x45b247 ; PasteBobCmp
0040e873  89f8                   mov      eax, edi
0040e875  0545000000             add      eax, 0x45
0040e87a  98                     cwde
0040e87b  8984248c010000         mov      dword ptr [esp + 0x18c], eax
0040e882  89f0                   mov      eax, esi
0040e884  b901000000             mov      ecx, 1
0040e889  055e000000             add      eax, 0x5e
0040e88e  bbbb1c0000             mov      ebx, 0x1cbb
0040e893  98                     cwde
0040e894  8b94248c010000         mov      edx, dword ptr [esp + 0x18c]
0040e89b  8944244c               mov      dword ptr [esp + 0x4c], eax
0040e89f  e8a3c90400             call     0x45b247 ; PasteBobCmp
0040e8a4  89f8                   mov      eax, edi
0040e8a6  0561000000             add      eax, 0x61
0040e8ab  98                     cwde
0040e8ac  898424b0010000         mov      dword ptr [esp + 0x1b0], eax
0040e8b3  89f0                   mov      eax, esi
0040e8b5  b901000000             mov      ecx, 1
0040e8ba  0530000000             add      eax, 0x30
0040e8bf  bbbd1c0000             mov      ebx, 0x1cbd
0040e8c4  98                     cwde
0040e8c5  8b9424b0010000         mov      edx, dword ptr [esp + 0x1b0]
0040e8cc  89842488010000         mov      dword ptr [esp + 0x188], eax
0040e8d3  e86fc90400             call     0x45b247 ; PasteBobCmp
0040e8d8  31c0                   xor      eax, eax
0040e8da  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040e8e2  e8d1bc0000             call     0x41a5b8 ; BatimentEstHabiter
0040e8e7  84c0                   test     al, al
0040e8e9  0f85530a0000           jne      0x40f342
0040e8ef  b901000000             mov      ecx, 1
0040e8f4  bbb61c0000             mov      ebx, 0x1cb6
0040e8f9  8b942454010000         mov      edx, dword ptr [esp + 0x154]
0040e900  89e8                   mov      eax, ebp
0040e902  e8a9d30400             call     0x45bcb0 ; PasteGrisCmp
0040e907  b901000000             mov      ecx, 1
0040e90c  bbb71c0000             mov      ebx, 0x1cb7
0040e911  8b54246c               mov      edx, dword ptr [esp + 0x6c]
0040e915  8b842434010000         mov      eax, dword ptr [esp + 0x134]
0040e91c  e88fd30400             call     0x45bcb0 ; PasteGrisCmp
0040e921  b901000000             mov      ecx, 1
0040e926  bbb91c0000             mov      ebx, 0x1cb9
0040e92b  8b9424d0010000         mov      edx, dword ptr [esp + 0x1d0]
0040e932  8b842450010000         mov      eax, dword ptr [esp + 0x150]
0040e939  e872d30400             call     0x45bcb0 ; PasteGrisCmp
0040e93e  b901000000             mov      ecx, 1
0040e943  bbbb1c0000             mov      ebx, 0x1cbb
0040e948  8b94248c010000         mov      edx, dword ptr [esp + 0x18c]
0040e94f  8b44244c               mov      eax, dword ptr [esp + 0x4c]
0040e953  e858d30400             call     0x45bcb0 ; PasteGrisCmp
0040e958  b901000000             mov      ecx, 1
0040e95d  bbbd1c0000             mov      ebx, 0x1cbd
0040e962  8b9424b0010000         mov      edx, dword ptr [esp + 0x1b0]
0040e969  8b842488010000         mov      eax, dword ptr [esp + 0x188]
0040e970  e9f89bffff             jmp      0x40856d ;
0040e975  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040e97a  01c8                   add      eax, ecx
0040e97c  f6400180               test     byte ptr [eax + 1], 0x80
0040e980  7415                   je       0x40e997
0040e982  668b00                 mov      ax, word ptr [eax]
0040e985  25e07f0000             and      eax, 0x7fe0
0040e98a  89c2                   mov      edx, eax
0040e98c  81e2ffff0000           and      edx, 0xffff
0040e992  c1fa05                 sar      edx, 5
0040e995  eb05                   jmp      0x40e99c ;
0040e997  baffff0000             mov      edx, 0xffff
0040e99c  89942410020000         mov      dword ptr [esp + 0x210], edx
0040e9a3  31d2                   xor      edx, edx
0040e9a5  668b942410020000       mov      dx, word ptr [esp + 0x210]
0040e9ad  81faffff0000           cmp      edx, 0xffff
0040e9b3  0f84d80a0000           je       0x40f491
0040e9b9  89d5                   mov      ebp, edx
0040e9bb  8b742408               mov      esi, dword ptr [esp + 8]
0040e9bf  c1e504                 shl      ebp, 4
0040e9c2  8b7c2404               mov      edi, dword ptr [esp + 4]
0040e9c6  01d5                   add      ebp, edx
0040e9c8  89d0                   mov      eax, edx
0040e9ca  c1e502                 shl      ebp, 2
0040e9cd  e813bf0000             call     0x41a8e5 ; BatimentGetEtat
0040e9d2  01d5                   add      ebp, edx
0040e9d4  898424d4020000         mov      dword ptr [esp + 0x2d4], eax
0040e9db  c1e502                 shl      ebp, 2
0040e9de  89c2                   mov      edx, eax
0040e9e0  81c5c8a04900           add      ebp, 0x49a0c8
0040e9e6  31c0                   xor      eax, eax
0040e9e8  83ee2c                 sub      esi, 0x2c
0040e9eb  8a4505                 mov      al, byte ptr [ebp + 5]
0040e9ee  83ef2d                 sub      edi, 0x2d
0040e9f1  83f805                 cmp      eax, 5
0040e9f4  740e                   je       0x40ea04
0040e9f6  83f803                 cmp      eax, 3
0040e9f9  7409                   je       0x40ea04
0040e9fb  83f804                 cmp      eax, 4
0040e9fe  0f851c020000           jne      0x40ec20
0040ea04  31c0                   xor      eax, eax
0040ea06  8a4505                 mov      al, byte ptr [ebp + 5]
0040ea09  83f803                 cmp      eax, 3
0040ea0c  0f8512010000           jne      0x40eb24
0040ea12  31c0                   xor      eax, eax
0040ea14  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040ea1c  e897bb0000             call     0x41a5b8 ; BatimentEstHabiter
0040ea21  84c0                   test     al, al
0040ea23  0f85fb000000           jne      0x40eb24
0040ea29  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040ea2f  31d2                   xor      edx, edx
0040ea31  88da                   mov      dl, bl
0040ea33  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040ea39  81e2ff000000           and      edx, 0xff
0040ea3f  b903000000             mov      ecx, 3
0040ea44  89d0                   mov      eax, edx
0040ea46  c1fa1f                 sar      edx, 0x1f
0040ea49  f7f9                   idiv     ecx
0040ea4b  0fbfcf                 movsx    ecx, di
0040ea4e  01ca                   add      edx, ecx
0040ea50  83c245                 add      edx, 0x45
0040ea53  fec3                   inc      bl
0040ea55  668994240c030000       mov      word ptr [esp + 0x30c], dx
0040ea5d  31d2                   xor      edx, edx
0040ea5f  88da                   mov      dl, bl
0040ea61  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040ea67  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040ea6d  81e2ff000000           and      edx, 0xff
0040ea73  bf03000000             mov      edi, 3
0040ea78  89d0                   mov      eax, edx
0040ea7a  c1fa1f                 sar      edx, 0x1f
0040ea7d  f7ff                   idiv     edi
0040ea7f  fec3                   inc      bl
0040ea81  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040ea87  01ca                   add      edx, ecx
0040ea89  31c0                   xor      eax, eax
0040ea8b  81c2c8000000           add      edx, 0xc8
0040ea91  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040ea98  29c2                   sub      edx, eax
0040ea9a  0fbfc2                 movsx    eax, dx
0040ea9d  89d7                   mov      edi, edx
0040ea9f  85c0                   test     eax, eax
0040eaa1  7d02                   jge      0x40eaa5
0040eaa3  31d7                   xor      edi, edx
0040eaa5  31c0                   xor      eax, eax
0040eaa7  66a126875000           mov      ax, word ptr [0x508726]
0040eaad  8b94240a030000         mov      edx, dword ptr [esp + 0x30a]
0040eab4  c1e005                 shl      eax, 5
0040eab7  c1fa10                 sar      edx, 0x10
0040eaba  48                     dec      eax
0040eabb  39c2                   cmp      edx, eax
0040eabd  7e12                   jle      0x40ead1
0040eabf  66a126875000           mov      ax, word ptr [0x508726]
0040eac5  c1e005                 shl      eax, 5
0040eac8  48                     dec      eax
0040eac9  668984240c030000       mov      word ptr [esp + 0x30c], ax
0040ead1  66a124875000           mov      ax, word ptr [0x508724]
0040ead7  31c9                   xor      ecx, ecx
0040ead9  31db                   xor      ebx, ebx
0040eadb  31d2                   xor      edx, edx
0040eadd  668b8c240c030000       mov      cx, word ptr [esp + 0x30c]
0040eae5  c1e005                 shl      eax, 5
0040eae8  6689fa                 mov      dx, di
0040eaeb  6689c3                 mov      bx, ax
0040eaee  31c0                   xor      eax, eax
0040eaf0  e8240a0000             call     0x40f519 ; SetClipping
0040eaf5  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040eafb  31d2                   xor      edx, edx
0040eafd  88da                   mov      dl, bl
0040eaff  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040eb05  81e2ff000000           and      edx, 0xff
0040eb0b  b903000000             mov      ecx, 3
0040eb10  89d0                   mov      eax, edx
0040eb12  c1fa1f                 sar      edx, 0x1f
0040eb15  f7f9                   idiv     ecx
0040eb17  fec3                   inc      bl
0040eb19  0fbff6                 movsx    esi, si
0040eb1c  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040eb22  01d6                   add      esi, edx
0040eb24  31c0                   xor      eax, eax
0040eb26  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040eb2e  e885ba0000             call     0x41a5b8 ; BatimentEstHabiter
0040eb33  84c0                   test     al, al
0040eb35  746d                   je       0x40eba4
0040eb37  31c0                   xor      eax, eax
0040eb39  8a4504                 mov      al, byte ptr [ebp + 4]
0040eb3c  50                     push     eax
0040eb3d  30e4                   xor      ah, ah
0040eb3f  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040eb45  89c2                   mov      edx, eax
0040eb47  4a                     dec      edx
0040eb48  01d2                   add      edx, edx
0040eb4a  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040eb4d  81c2501d0000           add      edx, 0x1d50
0040eb53  31db                   xor      ebx, ebx
0040eb55  01d0                   add      eax, edx
0040eb57  b901000000             mov      ecx, 1
0040eb5c  6689c3                 mov      bx, ax
0040eb5f  0fbfd7                 movsx    edx, di
0040eb62  0fbfc6                 movsx    eax, si
0040eb65  e8ebd80400             call     0x45c455 ; PastePlayerCmp
0040eb6a  31c0                   xor      eax, eax
0040eb6c  8a4576                 mov      al, byte ptr [ebp + 0x76]
0040eb6f  83f801                 cmp      eax, 1
0040eb72  0f8593000000           jne      0x40ec0b
0040eb78  30e4                   xor      ah, ah
0040eb7a  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040eb80  31db                   xor      ebx, ebx
0040eb82  05d41f0000             add      eax, 0x1fd4
0040eb87  6689c3                 mov      bx, ax
0040eb8a  89f8                   mov      eax, edi
0040eb8c  83e814                 sub      eax, 0x14
0040eb8f  0fbfd0                 movsx    edx, ax
0040eb92  89f0                   mov      eax, esi
0040eb94  83e80d                 sub      eax, 0xd
0040eb97  b901000000             mov      ecx, 1
0040eb9c  98                     cwde
0040eb9d  e8a5c60400             call     0x45b247 ; PasteBobCmp
0040eba2  eb67                   jmp      0x40ec0b ;
0040eba4  30e4                   xor      ah, ah
0040eba6  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040ebac  48                     dec      eax
0040ebad  01c0                   add      eax, eax
0040ebaf  31db                   xor      ebx, ebx
0040ebb1  05501d0000             add      eax, 0x1d50
0040ebb6  6689c3                 mov      bx, ax
0040ebb9  0fbfc7                 movsx    eax, di
0040ebbc  b901000000             mov      ecx, 1
0040ebc1  898424b4000000         mov      dword ptr [esp + 0xb4], eax
0040ebc8  0fbfc6                 movsx    eax, si
0040ebcb  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040ebd2  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040ebd9  e869c60400             call     0x45b247 ; PasteBobCmp
0040ebde  30e4                   xor      ah, ah
0040ebe0  8a858a000000           mov      al, byte ptr [ebp + 0x8a]
0040ebe6  48                     dec      eax
0040ebe7  b901000000             mov      ecx, 1
0040ebec  01c0                   add      eax, eax
0040ebee  31db                   xor      ebx, ebx
0040ebf0  05501d0000             add      eax, 0x1d50
0040ebf5  8b9424b4000000         mov      edx, dword ptr [esp + 0xb4]
0040ebfc  6689c3                 mov      bx, ax
0040ebff  8b8424a4010000         mov      eax, dword ptr [esp + 0x1a4]
0040ec06  e8a5d00400             call     0x45bcb0 ; PasteGrisCmp
0040ec0b  31c0                   xor      eax, eax
0040ec0d  668b4506               mov      ax, word ptr [ebp + 6]
0040ec11  85c0                   test     eax, eax
0040ec13  0f8e29070000           jle      0x40f342
0040ec19  6a0b                   push     0xb
0040ec1b  e9c2e9ffff             jmp      0x40d5e2 ;
0040ec20  31c0                   xor      eax, eax
0040ec22  668b0d26875000         mov      cx, word ptr [0x508726]
0040ec29  6689d0                 mov      ax, dx
0040ec2c  668b1524875000         mov      dx, word ptr [0x508724]
0040ec33  c1e105                 shl      ecx, 5
0040ec36  c1e205                 shl      edx, 5
0040ec39  49                     dec      ecx
0040ec3a  4a                     dec      edx
0040ec3b  83f864                 cmp      eax, 0x64
0040ec3e  0f8d7e000000           jge      0x40ecc2
0040ec44  899424f4020000         mov      dword ptr [esp + 0x2f4], edx
0040ec4b  ba64000000             mov      edx, 0x64
0040ec50  29c2                   sub      edx, eax
0040ec52  89d0                   mov      eax, edx
0040ec54  c1e004                 shl      eax, 4
0040ec57  01d0                   add      eax, edx
0040ec59  c1e002                 shl      eax, 2
0040ec5c  01c2                   add      edx, eax
0040ec5e  bb64000000             mov      ebx, 0x64
0040ec63  89d0                   mov      eax, edx
0040ec65  c1fa1f                 sar      edx, 0x1f
0040ec68  f7fb                   idiv     ebx
0040ec6a  0fbfd7                 movsx    edx, di
0040ec6d  01d0                   add      eax, edx
0040ec6f  0fbfd6                 movsx    edx, si
0040ec72  89b42464040000         mov      dword ptr [esp + 0x464], esi
0040ec79  85d2                   test     edx, edx
0040ec7b  7d09                   jge      0x40ec86
0040ec7d  31d2                   xor      edx, edx
0040ec7f  89942464040000         mov      dword ptr [esp + 0x464], edx
0040ec86  0fbfd0                 movsx    edx, ax
0040ec89  85d2                   test     edx, edx
0040ec8b  7d02                   jge      0x40ec8f
0040ec8d  31c0                   xor      eax, eax
0040ec8f  81e1ffff0000           and      ecx, 0xffff
0040ec95  31d2                   xor      edx, edx
0040ec97  31db                   xor      ebx, ebx
0040ec99  6689c2                 mov      dx, ax
0040ec9c  31c0                   xor      eax, eax
0040ec9e  668b9c24f4020000       mov      bx, word ptr [esp + 0x2f4]
0040eca6  668b842464040000       mov      ax, word ptr [esp + 0x464]
0040ecae  e866080000             call     0x40f519 ; SetClipping
0040ecb3  b901000000             mov      ecx, 1
0040ecb8  bbbf1c0000             mov      ebx, 0x1cbf
0040ecbd  e95097ffff             jmp      0x408412 ;
0040ecc2  89942424030000         mov      dword ptr [esp + 0x324], edx
0040ecc9  83e864                 sub      eax, 0x64
0040eccc  ba64000000             mov      edx, 0x64
0040ecd1  29c2                   sub      edx, eax
0040ecd3  89d0                   mov      eax, edx
0040ecd5  c1e004                 shl      eax, 4
0040ecd8  01d0                   add      eax, edx
0040ecda  c1e002                 shl      eax, 2
0040ecdd  01c2                   add      edx, eax
0040ecdf  bb64000000             mov      ebx, 0x64
0040ece4  89d0                   mov      eax, edx
0040ece6  c1fa1f                 sar      edx, 0x1f
0040ece9  f7fb                   idiv     ebx
0040eceb  0fbfd7                 movsx    edx, di
0040ecee  01d0                   add      eax, edx
0040ecf0  31d2                   xor      edx, edx
0040ecf2  668b1526875000         mov      dx, word ptr [0x508726]
0040ecf9  898c24e8020000         mov      dword ptr [esp + 0x2e8], ecx
0040ed00  c1e205                 shl      edx, 5
0040ed03  0fbfd8                 movsx    ebx, ax
0040ed06  4a                     dec      edx
0040ed07  6689b42470020000       mov      word ptr [esp + 0x270], si
0040ed0f  39d3                   cmp      ebx, edx
0040ed11  7e02                   jle      0x40ed15
0040ed13  89c8                   mov      eax, ecx
0040ed15  31c9                   xor      ecx, ecx
0040ed17  31db                   xor      ebx, ebx
0040ed19  31d2                   xor      edx, edx
0040ed1b  668b9c2424030000       mov      bx, word ptr [esp + 0x324]
0040ed23  6689c1                 mov      cx, ax
0040ed26  31c0                   xor      eax, eax
0040ed28  0fbfef                 movsx    ebp, di
0040ed2b  e8e9070000             call     0x40f519 ; SetClipping
0040ed30  b901000000             mov      ecx, 1
0040ed35  bbbf1c0000             mov      ebx, 0x1cbf
0040ed3a  0fbfc6                 movsx    eax, si
0040ed3d  89ea                   mov      edx, ebp
0040ed3f  e803c50400             call     0x45b247 ; PasteBobCmp
0040ed44  31c0                   xor      eax, eax
0040ed46  668b8424d4020000       mov      ax, word ptr [esp + 0x2d4]
0040ed4e  ba64000000             mov      edx, 0x64
0040ed53  83e864                 sub      eax, 0x64
0040ed56  29c2                   sub      edx, eax
0040ed58  89d0                   mov      eax, edx
0040ed5a  c1e004                 shl      eax, 4
0040ed5d  01d0                   add      eax, edx
0040ed5f  c1e002                 shl      eax, 2
0040ed62  01c2                   add      edx, eax
0040ed64  bb64000000             mov      ebx, 0x64
0040ed69  89d0                   mov      eax, edx
0040ed6b  c1fa1f                 sar      edx, 0x1f
0040ed6e  f7fb                   idiv     ebx
0040ed70  8b94246e020000         mov      edx, dword ptr [esp + 0x26e]
0040ed77  c1fa10                 sar      edx, 0x10
0040ed7a  01e8                   add      eax, ebp
0040ed7c  85d2                   test     edx, edx
0040ed7e  7d0a                   jge      0x40ed8a
0040ed80  31db                   xor      ebx, ebx
0040ed82  66899c2470020000       mov      word ptr [esp + 0x270], bx
0040ed8a  0fbfd0                 movsx    edx, ax
0040ed8d  85d2                   test     edx, edx
0040ed8f  7d02                   jge      0x40ed93
0040ed91  31c0                   xor      eax, eax
0040ed93  31c9                   xor      ecx, ecx
0040ed95  31db                   xor      ebx, ebx
0040ed97  31d2                   xor      edx, edx
0040ed99  668b8c24e8020000       mov      cx, word ptr [esp + 0x2e8]
0040eda1  6689c2                 mov      dx, ax
0040eda4  31c0                   xor      eax, eax
0040eda6  668b9c2424030000       mov      bx, word ptr [esp + 0x324]
0040edae  668b842470020000       mov      ax, word ptr [esp + 0x270]
0040edb6  0fbfef                 movsx    ebp, di
0040edb9  e85b070000             call     0x40f519 ; SetClipping
0040edbe  b901000000             mov      ecx, 1
0040edc3  bb501d0000             mov      ebx, 0x1d50
0040edc8  0fbfc6                 movsx    eax, si
0040edcb  89ea                   mov      edx, ebp
0040edcd  89842400010000         mov      dword ptr [esp + 0x100], eax
0040edd4  e86ec40400             call     0x45b247 ; PasteBobCmp
0040edd9  31c0                   xor      eax, eax
0040eddb  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040ede3  e8d0b70000             call     0x41a5b8 ; BatimentEstHabiter
0040ede8  84c0                   test     al, al
0040edea  0f8552050000           jne      0x40f342
0040edf0  b901000000             mov      ecx, 1
0040edf5  bb501d0000             mov      ebx, 0x1d50
0040edfa  8b842400010000         mov      eax, dword ptr [esp + 0x100]
0040ee01  e96597ffff             jmp      0x40856b ;
0040ee06  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0040ee0b  01c8                   add      eax, ecx
0040ee0d  f6400180               test     byte ptr [eax + 1], 0x80
0040ee11  7415                   je       0x40ee28
0040ee13  668b00                 mov      ax, word ptr [eax]
0040ee16  25e07f0000             and      eax, 0x7fe0
0040ee1b  89c2                   mov      edx, eax
0040ee1d  81e2ffff0000           and      edx, 0xffff
0040ee23  c1fa05                 sar      edx, 5
0040ee26  eb05                   jmp      0x40ee2d ;
0040ee28  baffff0000             mov      edx, 0xffff
0040ee2d  31c0                   xor      eax, eax
0040ee2f  6689d0                 mov      ax, dx
0040ee32  89942410020000         mov      dword ptr [esp + 0x210], edx
0040ee39  3dffff0000             cmp      eax, 0xffff
0040ee3e  0f844d060000           je       0x40f491
0040ee44  89c5                   mov      ebp, eax
0040ee46  c1e504                 shl      ebp, 4
0040ee49  01c5                   add      ebp, eax
0040ee4b  8b742408               mov      esi, dword ptr [esp + 8]
0040ee4f  c1e502                 shl      ebp, 2
0040ee52  8b7c2404               mov      edi, dword ptr [esp + 4]
0040ee56  01c5                   add      ebp, eax
0040ee58  e888ba0000             call     0x41a8e5 ; BatimentGetEtat
0040ee5d  c1e502                 shl      ebp, 2
0040ee60  89c2                   mov      edx, eax
0040ee62  89842414020000         mov      dword ptr [esp + 0x214], eax
0040ee69  81c5c8a04900           add      ebp, 0x49a0c8
0040ee6f  31c0                   xor      eax, eax
0040ee71  83ee2c                 sub      esi, 0x2c
0040ee74  8a4505                 mov      al, byte ptr [ebp + 5]
0040ee77  83ef2d                 sub      edi, 0x2d
0040ee7a  83f805                 cmp      eax, 5
0040ee7d  740e                   je       0x40ee8d
0040ee7f  83f803                 cmp      eax, 3
0040ee82  7409                   je       0x40ee8d
0040ee84  83f804                 cmp      eax, 4
0040ee87  0f85b1010000           jne      0x40f03e
0040ee8d  31c0                   xor      eax, eax
0040ee8f  8a4505                 mov      al, byte ptr [ebp + 5]
0040ee92  83f803                 cmp      eax, 3
0040ee95  0f850c010000           jne      0x40efa7
0040ee9b  31c0                   xor      eax, eax
0040ee9d  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040eea5  e80eb70000             call     0x41a5b8 ; BatimentEstHabiter
0040eeaa  84c0                   test     al, al
0040eeac  0f85f5000000           jne      0x40efa7
0040eeb2  8a0d181d4e00           mov      cl, byte ptr [0x4e1d18]
0040eeb8  31d2                   xor      edx, edx
0040eeba  88ca                   mov      dl, cl
0040eebc  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040eec2  81e2ff000000           and      edx, 0xff
0040eec8  bb03000000             mov      ebx, 3
0040eecd  89d0                   mov      eax, edx
0040eecf  c1fa1f                 sar      edx, 0x1f
0040eed2  f7fb                   idiv     ebx
0040eed4  0fbfdf                 movsx    ebx, di
0040eed7  fec1                   inc      cl
0040eed9  01da                   add      edx, ebx
0040eedb  880d181d4e00           mov      byte ptr [0x4e1d18], cl
0040eee1  83c25d                 add      edx, 0x5d
0040eee4  a0181d4e00             mov      al, byte ptr [0x4e1d18]
0040eee9  89d1                   mov      ecx, edx
0040eeeb  31d2                   xor      edx, edx
0040eeed  88c2                   mov      dl, al
0040eeef  88842498040000         mov      byte ptr [esp + 0x498], al
0040eef6  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040eefc  81e2ff000000           and      edx, 0xff
0040ef02  bf03000000             mov      edi, 3
0040ef07  89d0                   mov      eax, edx
0040ef09  c1fa1f                 sar      edx, 0x1f
0040ef0c  f7ff                   idiv     edi
0040ef0e  8a842498040000         mov      al, byte ptr [esp + 0x498]
0040ef15  fec0                   inc      al
0040ef17  01da                   add      edx, ebx
0040ef19  a2181d4e00             mov      byte ptr [0x4e1d18], al
0040ef1e  31c0                   xor      eax, eax
0040ef20  81c2c8000000           add      edx, 0xc8
0040ef26  668b8584000000         mov      ax, word ptr [ebp + 0x84]
0040ef2d  29c2                   sub      edx, eax
0040ef2f  0fbfc2                 movsx    eax, dx
0040ef32  89d7                   mov      edi, edx
0040ef34  85c0                   test     eax, eax
0040ef36  7d02                   jge      0x40ef3a
0040ef38  31d7                   xor      edi, edx
0040ef3a  31c0                   xor      eax, eax
0040ef3c  66a126875000           mov      ax, word ptr [0x508726]
0040ef42  c1e005                 shl      eax, 5
0040ef45  0fbfd1                 movsx    edx, cx
0040ef48  48                     dec      eax
0040ef49  39c2                   cmp      edx, eax
0040ef4b  7e0b                   jle      0x40ef58
0040ef4d  668b0d26875000         mov      cx, word ptr [0x508726]
0040ef54  c1e105                 shl      ecx, 5
0040ef57  49                     dec      ecx
0040ef58  66a124875000           mov      ax, word ptr [0x508724]
0040ef5e  81e1ffff0000           and      ecx, 0xffff
0040ef64  31db                   xor      ebx, ebx
0040ef66  31d2                   xor      edx, edx
0040ef68  c1e005                 shl      eax, 5
0040ef6b  6689fa                 mov      dx, di
0040ef6e  6689c3                 mov      bx, ax
0040ef71  31c0                   xor      eax, eax
0040ef73  e8a1050000             call     0x40f519 ; SetClipping
0040ef78  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0040ef7e  31d2                   xor      edx, edx
0040ef80  88da                   mov      dl, bl
0040ef82  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0040ef88  81e2ff000000           and      edx, 0xff
0040ef8e  b903000000             mov      ecx, 3
0040ef93  89d0                   mov      eax, edx
0040ef95  c1fa1f                 sar      edx, 0x1f
0040ef98  f7f9                   idiv     ecx
0040ef9a  fec3                   inc      bl
0040ef9c  0fbff6                 movsx    esi, si
0040ef9f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
0040efa5  01d6                   add      esi, edx
0040efa7  31c0                   xor      eax, eax
0040efa9  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040efb1  e802b60000             call     0x41a5b8 ; BatimentEstHabiter
0040efb6  84c0                   test     al, al
0040efb8  7431                   je       0x40efeb
0040efba  31c0                   xor      eax, eax
0040efbc  8a4504                 mov      al, byte ptr [ebp + 4]
0040efbf  8b1c24                 mov      ebx, dword ptr [esp]
0040efc2  50                     push     eax
0040efc3  66a1848f5000           mov      ax, word ptr [0x508f84]
0040efc9  01d8                   add      eax, ebx
0040efcb  30e4                   xor      ah, ah
0040efcd  b901000000             mov      ecx, 1
0040efd2  2407                   and      al, 7
0040efd4  31db                   xor      ebx, ebx
0040efd6  05901d0000             add      eax, 0x1d90
0040efdb  0fbfd7                 movsx    edx, di
0040efde  6689c3                 mov      bx, ax
0040efe1  0fbfc6                 movsx    eax, si
0040efe4  e86cd40400             call     0x45c455 ; PastePlayerCmp
0040efe9  eb3e                   jmp      0x40f029 ;
0040efeb  b901000000             mov      ecx, 1
0040eff0  0fbfc7                 movsx    eax, di
0040eff3  bb901d0000             mov      ebx, 0x1d90
0040eff8  8944247c               mov      dword ptr [esp + 0x7c], eax
0040effc  0fbfc6                 movsx    eax, si
0040efff  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040f003  89842494000000         mov      dword ptr [esp + 0x94], eax
0040f00a  e838c20400             call     0x45b247 ; PasteBobCmp
0040f00f  b901000000             mov      ecx, 1
0040f014  bb901d0000             mov      ebx, 0x1d90
0040f019  8b54247c               mov      edx, dword ptr [esp + 0x7c]
0040f01d  8b842494000000         mov      eax, dword ptr [esp + 0x94]
0040f024  e887cc0400             call     0x45bcb0 ; PasteGrisCmp
0040f029  31c0                   xor      eax, eax
0040f02b  668b4506               mov      ax, word ptr [ebp + 6]
0040f02f  85c0                   test     eax, eax
0040f031  0f8e0b030000           jle      0x40f342
0040f037  6a15                   push     0x15
0040f039  e9a4e5ffff             jmp      0x40d5e2 ;
0040f03e  31c0                   xor      eax, eax
0040f040  668b0d26875000         mov      cx, word ptr [0x508726]
0040f047  6689d0                 mov      ax, dx
0040f04a  668b1524875000         mov      dx, word ptr [0x508724]
0040f051  c1e105                 shl      ecx, 5
0040f054  c1e205                 shl      edx, 5
0040f057  49                     dec      ecx
0040f058  4a                     dec      edx
0040f059  83f864                 cmp      eax, 0x64
0040f05c  0f8d80000000           jge      0x40f0e2
0040f062  89942488030000         mov      dword ptr [esp + 0x388], edx
0040f069  ba64000000             mov      edx, 0x64
0040f06e  29c2                   sub      edx, eax
0040f070  89d5                   mov      ebp, edx
0040f072  c1e502                 shl      ebp, 2
0040f075  29d5                   sub      ebp, edx
0040f077  89ea                   mov      edx, ebp
0040f079  c1e205                 shl      edx, 5
0040f07c  29ea                   sub      edx, ebp
0040f07e  bb64000000             mov      ebx, 0x64
0040f083  89d0                   mov      eax, edx
0040f085  c1fa1f                 sar      edx, 0x1f
0040f088  f7fb                   idiv     ebx
0040f08a  0fbfd7                 movsx    edx, di
0040f08d  01d0                   add      eax, edx
0040f08f  0fbfd6                 movsx    edx, si
0040f092  89b42484040000         mov      dword ptr [esp + 0x484], esi
0040f099  85d2                   test     edx, edx
0040f09b  7d09                   jge      0x40f0a6
0040f09d  31d2                   xor      edx, edx
0040f09f  89942484040000         mov      dword ptr [esp + 0x484], edx
0040f0a6  0fbfd0                 movsx    edx, ax
0040f0a9  85d2                   test     edx, edx
0040f0ab  7d02                   jge      0x40f0af
0040f0ad  31c0                   xor      eax, eax
0040f0af  81e1ffff0000           and      ecx, 0xffff
0040f0b5  31d2                   xor      edx, edx
0040f0b7  31db                   xor      ebx, ebx
0040f0b9  6689c2                 mov      dx, ax
0040f0bc  31c0                   xor      eax, eax
0040f0be  668b9c2488030000       mov      bx, word ptr [esp + 0x388]
0040f0c6  668b842484040000       mov      ax, word ptr [esp + 0x484]
0040f0ce  e846040000             call     0x40f519 ; SetClipping
0040f0d3  b901000000             mov      ecx, 1
0040f0d8  bb6e1c0000             mov      ebx, 0x1c6e
0040f0dd  e93093ffff             jmp      0x408412 ;
0040f0e2  89942458040000         mov      dword ptr [esp + 0x458], edx
0040f0e9  83e864                 sub      eax, 0x64
0040f0ec  ba64000000             mov      edx, 0x64
0040f0f1  29c2                   sub      edx, eax
0040f0f3  89d5                   mov      ebp, edx
0040f0f5  c1e502                 shl      ebp, 2
0040f0f8  29d5                   sub      ebp, edx
0040f0fa  89ea                   mov      edx, ebp
0040f0fc  c1e205                 shl      edx, 5
0040f0ff  29ea                   sub      edx, ebp
0040f101  bb64000000             mov      ebx, 0x64
0040f106  89d0                   mov      eax, edx
0040f108  c1fa1f                 sar      edx, 0x1f
0040f10b  f7fb                   idiv     ebx
0040f10d  0fbfd7                 movsx    edx, di
0040f110  01d0                   add      eax, edx
0040f112  31d2                   xor      edx, edx
0040f114  668b1526875000         mov      dx, word ptr [0x508726]
0040f11b  898c24dc020000         mov      dword ptr [esp + 0x2dc], ecx
0040f122  c1e205                 shl      edx, 5
0040f125  0fbfd8                 movsx    ebx, ax
0040f128  4a                     dec      edx
0040f129  6689b42404030000       mov      word ptr [esp + 0x304], si
0040f131  39d3                   cmp      ebx, edx
0040f133  7e02                   jle      0x40f137
0040f135  89c8                   mov      eax, ecx
0040f137  31c9                   xor      ecx, ecx
0040f139  31db                   xor      ebx, ebx
0040f13b  31d2                   xor      edx, edx
0040f13d  668b9c2458040000       mov      bx, word ptr [esp + 0x458]
0040f145  6689c1                 mov      cx, ax
0040f148  31c0                   xor      eax, eax
0040f14a  e8ca030000             call     0x40f519 ; SetClipping
0040f14f  0fbfc7                 movsx    eax, di
0040f152  b901000000             mov      ecx, 1
0040f157  898424a4010000         mov      dword ptr [esp + 0x1a4], eax
0040f15e  bb6e1c0000             mov      ebx, 0x1c6e
0040f163  8b9424a4010000         mov      edx, dword ptr [esp + 0x1a4]
0040f16a  0fbfc6                 movsx    eax, si
0040f16d  e8d5c00400             call     0x45b247 ; PasteBobCmp
0040f172  31c0                   xor      eax, eax
0040f174  668b842414020000       mov      ax, word ptr [esp + 0x214]
0040f17c  ba64000000             mov      edx, 0x64
0040f181  83e864                 sub      eax, 0x64
0040f184  29c2                   sub      edx, eax
0040f186  89d5                   mov      ebp, edx
0040f188  c1e502                 shl      ebp, 2
0040f18b  29d5                   sub      ebp, edx
0040f18d  89ea                   mov      edx, ebp
0040f18f  c1e205                 shl      edx, 5
0040f192  29ea                   sub      edx, ebp
0040f194  bb64000000             mov      ebx, 0x64
0040f199  89d0                   mov      eax, edx
0040f19b  c1fa1f                 sar      edx, 0x1f
0040f19e  f7fb                   idiv     ebx
0040f1a0  038424a4010000         add      eax, dword ptr [esp + 0x1a4]
0040f1a7  8b942402030000         mov      edx, dword ptr [esp + 0x302]
0040f1ae  c1fa10                 sar      edx, 0x10
0040f1b1  85d2                   test     edx, edx
0040f1b3  7d0a                   jge      0x40f1bf
0040f1b5  31db                   xor      ebx, ebx
0040f1b7  66899c2404030000       mov      word ptr [esp + 0x304], bx
0040f1bf  0fbfd0                 movsx    edx, ax
0040f1c2  85d2                   test     edx, edx
0040f1c4  7d02                   jge      0x40f1c8
0040f1c6  31c0                   xor      eax, eax
0040f1c8  31c9                   xor      ecx, ecx
0040f1ca  31db                   xor      ebx, ebx
0040f1cc  31d2                   xor      edx, edx
0040f1ce  668b8c24dc020000       mov      cx, word ptr [esp + 0x2dc]
0040f1d6  6689c2                 mov      dx, ax
0040f1d9  31c0                   xor      eax, eax
0040f1db  668b9c2458040000       mov      bx, word ptr [esp + 0x458]
0040f1e3  668b842404030000       mov      ax, word ptr [esp + 0x304]
0040f1eb  0fbfef                 movsx    ebp, di
0040f1ee  e826030000             call     0x40f519 ; SetClipping
0040f1f3  b901000000             mov      ecx, 1
0040f1f8  bb901d0000             mov      ebx, 0x1d90
0040f1fd  0fbfc6                 movsx    eax, si
0040f200  89ea                   mov      edx, ebp
0040f202  898424d4000000         mov      dword ptr [esp + 0xd4], eax
0040f209  e839c00400             call     0x45b247 ; PasteBobCmp
0040f20e  31c0                   xor      eax, eax
0040f210  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040f218  e89bb30000             call     0x41a5b8 ; BatimentEstHabiter
0040f21d  84c0                   test     al, al
0040f21f  0f851d010000           jne      0x40f342
0040f225  b901000000             mov      ecx, 1
0040f22a  bb901d0000             mov      ebx, 0x1d90
0040f22f  8b8424d4000000         mov      eax, dword ptr [esp + 0xd4]
0040f236  e93093ffff             jmp      0x40856b ;
0040f23b  a1707d5000             mov      eax, dword ptr [0x507d70]
0040f240  01c9                   add      ecx, ecx
0040f242  668b0401               mov      ax, word ptr [ecx + eax]
0040f246  89c2                   mov      edx, eax
0040f248  663d9003               cmp      ax, 0x390
0040f24c  0f8286000000           jb       0x40f2d8
0040f252  0f86b1cbffff           jbe      0x40be09
0040f258  663df803               cmp      ax, 0x3f8
0040f25c  7240                   jb       0x40f29e
0040f25e  0f8638e6ffff           jbe      0x40d89c
0040f264  663d0e04               cmp      ax, 0x40e
0040f268  7225                   jb       0x40f28f
0040f26a  0f8696fbffff           jbe      0x40ee06
0040f270  663d2a04               cmp      ax, 0x42a
0040f274  0f82c8000000           jb       0x40f342
0040f27a  0f8679efffff           jbe      0x40e1f9
0040f280  663d3604               cmp      ax, 0x436
0040f284  0f84ebf6ffff           je       0x40e975
0040f28a  e9b3000000             jmp      0x40f342 ;
0040f28f  663d0604               cmp      ax, 0x406
0040f293  0f84e7eaffff           je       0x40dd80
0040f299  e9a4000000             jmp      0x40f342 ;
0040f29e  663db003               cmp      ax, 0x3b0
0040f2a2  7225                   jb       0x40f2c9
0040f2a4  0f86fcd2ffff           jbe      0x40c5a6
0040f2aa  663dce03               cmp      ax, 0x3ce
0040f2ae  0f828e000000           jb       0x40f342
0040f2b4  0f86a6d9ffff           jbe      0x40cc60
0040f2ba  663de103               cmp      ax, 0x3e1
0040f2be  0f840edfffff           je       0x40d1d2
0040f2c4  e979000000             jmp      0x40f342 ;
0040f2c9  663d9803               cmp      ax, 0x398
0040f2cd  0f84c9ceffff           je       0x40c19c
0040f2d3  e96a000000             jmp      0x40f342 ;
0040f2d8  663d2603               cmp      ax, 0x326
0040f2dc  7236                   jb       0x40f314
0040f2de  0f8693aaffff           jbe      0x409d77
0040f2e4  663d5e03               cmp      ax, 0x35e
0040f2e8  721e                   jb       0x40f308
0040f2ea  0f86bdb8ffff           jbe      0x40abad
0040f2f0  663d7a03               cmp      ax, 0x37a
0040f2f4  724c                   jb       0x40f342
0040f2f6  0f86f7c4ffff           jbe      0x40b7f3
0040f2fc  663d8803               cmp      ax, 0x388
0040f300  0f8497bfffff           je       0x40b29d
0040f306  eb3a                   jmp      0x40f342 ;
0040f308  663d4303               cmp      ax, 0x343
0040f30c  0f8464b0ffff           je       0x40a376
0040f312  eb2e                   jmp      0x40f342 ;
0040f314  663ded02               cmp      ax, 0x2ed
0040f318  721e                   jb       0x40f338
0040f31a  0f865792ffff           jbe      0x408577
0040f320  663dfb02               cmp      ax, 0x2fb
0040f324  721c                   jb       0x40f342
0040f326  0f86d09affff           jbe      0x408dfc
0040f32c  663d0d03               cmp      ax, 0x30d
0040f330  0f8427a0ffff           je       0x40935d
0040f336  eb0a                   jmp      0x40f342 ;
0040f338  663dcb02               cmp      ax, 0x2cb
0040f33c  0f84a68dffff           je       0x4080e8
0040f342  0fb72c24               movzx    ebp, word ptr [esp]
0040f346  8b542402               mov      edx, dword ptr [esp + 2]
0040f34a  8b442406               mov      eax, dword ptr [esp + 6]
0040f34e  31c9                   xor      ecx, ecx
0040f350  c1fa10                 sar      edx, 0x10
0040f353  c1f810                 sar      eax, 0x10
0040f356  89eb                   mov      ebx, ebp
0040f358  668b8c2410020000       mov      cx, word ptr [esp + 0x210]
0040f360  e8ff34ffff             call     0x402864 ; AffVehiculeAtelier
0040f365  e87e010000             call     0x40f4e8 ; RestaureClipping
0040f36a  81f9ffff0000           cmp      ecx, 0xffff
0040f370  0f84ce000000           je       0x40f444
0040f376  89c8                   mov      eax, ecx
0040f378  e83bb20000             call     0x41a5b8 ; BatimentEstHabiter
0040f37d  84c0                   test     al, al
0040f37f  0f84bf000000           je       0x40f444
0040f385  a1747d5000             mov      eax, dword ptr [0x507d74]
0040f38a  8a0428                 mov      al, byte ptr [eax + ebp]
0040f38d  3a05f85b4900           cmp      al, byte ptr [0x495bf8]
0040f393  0f84ab000000           je       0x40f444
0040f399  89cd                   mov      ebp, ecx
0040f39b  c1e504                 shl      ebp, 4
0040f39e  01cd                   add      ebp, ecx
0040f3a0  c1e502                 shl      ebp, 2
0040f3a3  8d0429                 lea      eax, [ecx + ebp]
0040f3a6  c1e002                 shl      eax, 2
0040f3a9  31d2                   xor      edx, edx
0040f3ab  8a90cda04900           mov      dl, byte ptr [eax + 0x49a0cd]
0040f3b1  83fa03                 cmp      edx, 3
0040f3b4  0f848a000000           je       0x40f444
0040f3ba  31d2                   xor      edx, edx
0040f3bc  8a90cca04900           mov      dl, byte ptr [eax + 0x49a0cc]
0040f3c2  663b0c55e05b4900       cmp      cx, word ptr [edx*2 + 0x495be0]
0040f3ca  751f                   jne      0x40f3eb
0040f3cc  8a3541805000           mov      dh, byte ptr [0x508041]
0040f3d2  3ab0cca04900           cmp      dh, byte ptr [eax + 0x49a0cc]
0040f3d8  7511                   jne      0x40f3eb
0040f3da  89c8                   mov      eax, ecx
0040f3dc  31db                   xor      ebx, ebx
0040f3de  31d2                   xor      edx, edx
0040f3e0  6689fb                 mov      bx, di
0040f3e3  6689f2                 mov      dx, si
0040f3e6  e8dd2effff             call     0x4022c8 ; BatimentPoseCadre
0040f3eb  31d2                   xor      edx, edx
0040f3ed  668b942410020000       mov      dx, word ptr [esp + 0x210]
0040f3f5  89d0                   mov      eax, edx
0040f3f7  e890ac0000             call     0x41a08c ; BatimentGetPlayer
0040f3fc  3a0541805000           cmp      al, byte ptr [0x508041]
0040f402  0f8589000000           jne      0x40f491
0040f408  663b15c46a4900         cmp      dx, word ptr [0x496ac4]
0040f40f  7421                   je       0x40f432
0040f411  89d5                   mov      ebp, edx
0040f413  c1e504                 shl      ebp, 4
0040f416  01d5                   add      ebp, edx
0040f418  c1e502                 shl      ebp, 2
0040f41b  89d0                   mov      eax, edx
0040f41d  01d5                   add      ebp, edx
0040f41f  31d0                   xor      eax, edx
0040f421  8a04adcca04900         mov      al, byte ptr [ebp*4 + 0x49a0cc]
0040f428  663b1445e05b4900       cmp      dx, word ptr [eax*2 + 0x495be0]
0040f430  755f                   jne      0x40f491
0040f432  0fbfdf                 movsx    ebx, di
0040f435  31c0                   xor      eax, eax
0040f437  0fbfd6                 movsx    edx, si
0040f43a  668b842410020000       mov      ax, word ptr [esp + 0x210]
0040f442  eb48                   jmp      0x40f48c ;
0040f444  0fb7ac2410020000       movzx    ebp, word ptr [esp + 0x210]
0040f44c  81fdffff0000           cmp      ebp, 0xffff
0040f452  743d                   je       0x40f491
0040f454  89e8                   mov      eax, ebp
0040f456  e899b00000             call     0x41a4f4 ; BatimentGetType
0040f45b  25ff000000             and      eax, 0xff
0040f460  83f811                 cmp      eax, 0x11
0040f463  752c                   jne      0x40f491
0040f465  89e8                   mov      eax, ebp
0040f467  e820ac0000             call     0x41a08c ; BatimentGetPlayer
0040f46c  3a0541805000           cmp      al, byte ptr [0x508041]
0040f472  751d                   jne      0x40f491
0040f474  8b942410020000         mov      edx, dword ptr [esp + 0x210]
0040f47b  663b15c46a4900         cmp      dx, word ptr [0x496ac4]
0040f482  750d                   jne      0x40f491
0040f484  0fbfdf                 movsx    ebx, di
0040f487  0fbfd6                 movsx    edx, si
0040f48a  89e8                   mov      eax, ebp
0040f48c  e85b2cffff             call     0x4020ec ; AffJaugeBatiment
0040f491  81c49c040000           add      esp, 0x49c
0040f497  5d                     pop      ebp
0040f498  5f                     pop      edi
0040f499  5e                     pop      esi
0040f49a  59                     pop      ecx
0040f49b  c3                     ret
