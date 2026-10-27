; AffEngin [0x41591f, 0x415a56)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041591f  51                     push     ecx
00415920  56                     push     esi
00415921  57                     push     edi
00415922  89c1                   mov      ecx, eax
00415924  89df                   mov      edi, ebx
00415926  31db                   xor      ebx, ebx
00415928  6689fb                 mov      bx, di
0041592b  89d8                   mov      eax, ebx
0041592d  c1e004                 shl      eax, 4
00415930  01d8                   add      eax, ebx
00415932  c1e002                 shl      eax, 2
00415935  01d8                   add      eax, ebx
00415937  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
0041593d  c1e002                 shl      eax, 2
00415940  01c6                   add      esi, eax
00415942  8a4602                 mov      al, byte ptr [esi + 2]
00415945  3c10                   cmp      al, 0x10
00415947  0f82b9000000           jb       0x415a06
0041594d  3c11                   cmp      al, 0x11
0041594f  761c                   jbe      0x41596d
00415951  3c15                   cmp      al, 0x15
00415953  0f8298000000           jb       0x4159f1
00415959  7612                   jbe      0x41596d
0041595b  3c17                   cmp      al, 0x17
0041595d  7231                   jb       0x415990
0041595f  760c                   jbe      0x41596d
00415961  3c18                   cmp      al, 0x18
00415963  7641                   jbe      0x4159a6
00415965  3c1e                   cmp      al, 0x1e
00415967  0f85e6000000           jne      0x415a53
0041596d  0fbfd2                 movsx    edx, dx
00415970  31db                   xor      ebx, ebx
00415972  0fbfc1                 movsx    eax, cx
00415975  6689fb                 mov      bx, di
00415978  e813caffff             call     0x412390 ; AffDeplaceEngin
0041597d  5f                     pop      edi
0041597e  5e                     pop      esi
0041597f  59                     pop      ecx
00415980  c3                     ret      
00415981  0fbfd2                 movsx    edx, dx
00415984  0fbfc1                 movsx    eax, cx
00415987  e8c0ddffff             call     0x41374c ; AffAttaqueEngin
0041598c  5f                     pop      edi
0041598d  5e                     pop      esi
0041598e  59                     pop      ecx
0041598f  c3                     ret      
00415990  8a868a000000           mov      al, byte ptr [esi + 0x8a]
00415996  84c0                   test     al, al
00415998  0f865d000000           jbe      0x4159fb
0041599e  3c01                   cmp      al, 1
004159a0  74df                   je       0x415981
004159a2  5f                     pop      edi
004159a3  5e                     pop      esi
004159a4  59                     pop      ecx
004159a5  c3                     ret      
004159a6  31db                   xor      ebx, ebx
004159a8  6689fb                 mov      bx, di
004159ab  89d8                   mov      eax, ebx
004159ad  e873c60200             call     0x442025 ; EnginGetType
004159b2  25ff000000             and      eax, 0xff
004159b7  83f810                 cmp      eax, 0x10
004159ba  743f                   je       0x4159fb
004159bc  8a868a000000           mov      al, byte ptr [esi + 0x8a]
004159c2  84c0                   test     al, al
004159c4  7635                   jbe      0x4159fb
004159c6  3c03                   cmp      al, 3
004159c8  76b7                   jbe      0x415981
004159ca  5f                     pop      edi
004159cb  5e                     pop      esi
004159cc  59                     pop      ecx
004159cd  c3                     ret      
004159ce  0fbfd2                 movsx    edx, dx
004159d1  31db                   xor      ebx, ebx
004159d3  0fbfc1                 movsx    eax, cx
004159d6  6689fb                 mov      bx, di
004159d9  e8b7eaffff             call     0x414495 ; AffConstruireBatiment
004159de  5f                     pop      edi
004159df  5e                     pop      esi
004159e0  59                     pop      ecx
004159e1  c3                     ret      
004159e2  0fbfd2                 movsx    edx, dx
004159e5  0fbfc1                 movsx    eax, cx
004159e8  e89df0ffff             call     0x414a8a ; AffWorkEngin
004159ed  5f                     pop      edi
004159ee  5e                     pop      esi
004159ef  59                     pop      ecx
004159f0  c3                     ret      
004159f1  3c13                   cmp      al, 0x13
004159f3  7206                   jb       0x4159fb
004159f5  0f8672ffffff           jbe      0x41596d
004159fb  0fbfd2                 movsx    edx, dx
004159fe  0fbfc1                 movsx    eax, cx
00415a01  e972ffffff             jmp      0x415978 ; 
00415a06  3c05                   cmp      al, 5
00415a08  7226                   jb       0x415a30
00415a0a  76d6                   jbe      0x4159e2
00415a0c  3c0b                   cmp      al, 0xb
00415a0e  7214                   jb       0x415a24
00415a10  76bc                   jbe      0x4159ce
00415a12  3c0d                   cmp      al, 0xd
00415a14  723d                   jb       0x415a53
00415a16  0f8651ffffff           jbe      0x41596d
00415a1c  3c0f                   cmp      al, 0xf
00415a1e  74ae                   je       0x4159ce
00415a20  5f                     pop      edi
00415a21  5e                     pop      esi
00415a22  59                     pop      ecx
00415a23  c3                     ret      
00415a24  3c09                   cmp      al, 9
00415a26  0f8641ffffff           jbe      0x41596d
00415a2c  5f                     pop      edi
00415a2d  5e                     pop      esi
00415a2e  59                     pop      ecx
00415a2f  c3                     ret      
00415a30  3c02                   cmp      al, 2
00415a32  7217                   jb       0x415a4b
00415a34  3c03                   cmp      al, 3
00415a36  0f8631ffffff           jbe      0x41596d
00415a3c  0fbfd2                 movsx    edx, dx
00415a3f  0fbfc1                 movsx    eax, cx
00415a42  e853fbffff             call     0x41559a ; AffDyingEngin
00415a47  5f                     pop      edi
00415a48  5e                     pop      esi
00415a49  59                     pop      ecx
00415a4a  c3                     ret      
00415a4b  3c01                   cmp      al, 1
00415a4d  0f8453ffffff           je       0x4159a6
00415a53  5f                     pop      edi
00415a54  5e                     pop      esi
00415a55  59                     pop      ecx
