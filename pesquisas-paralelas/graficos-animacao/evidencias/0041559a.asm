; AffDyingEngin [0x41559a, 0x41591f)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041559a  51                     push     ecx
0041559b  56                     push     esi
0041559c  57                     push     edi
0041559d  55                     push     ebp
0041559e  83ec48                 sub      esp, 0x48
004155a1  89c1                   mov      ecx, eax
004155a3  895c242c               mov      dword ptr [esp + 0x2c], ebx
004155a7  31ff                   xor      edi, edi
004155a9  6689df                 mov      di, bx
004155ac  89f8                   mov      eax, edi
004155ae  c1e004                 shl      eax, 4
004155b1  01f8                   add      eax, edi
004155b3  c1e002                 shl      eax, 2
004155b6  01f8                   add      eax, edi
004155b8  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
004155be  c1e002                 shl      eax, 2
004155c1  01c6                   add      esi, eax
004155c3  660fbe8686000000       movsx    ax, byte ptr [esi + 0x86]
004155cb  01c1                   add      ecx, eax
004155cd  660fbe8687000000       movsx    ax, byte ptr [esi + 0x87]
004155d5  01c2                   add      edx, eax
004155d7  8d5c2414               lea      ebx, [esp + 0x14]
004155db  89542428               mov      dword ptr [esp + 0x28], edx
004155df  31d2                   xor      edx, edx
004155e1  31c0                   xor      eax, eax
004155e3  89542410               mov      dword ptr [esp + 0x10], edx
004155e7  89542414               mov      dword ptr [esp + 0x14], edx
004155eb  8d542410               lea      edx, [esp + 0x10]
004155ef  8a4601                 mov      al, byte ptr [esi + 1]
004155f2  e8d5b9ffff             call     0x410fcc ; AffCorpsEnginDecalage
004155f7  89f8                   mov      eax, edi
004155f9  894c243c               mov      dword ptr [esp + 0x3c], ecx
004155fd  e823ca0200             call     0x442025 ; EnginGetType
00415602  25ff000000             and      eax, 0xff
00415607  e88afeffff             call     0x415496 ; EnginGetSpriteMort
0041560c  89442434               mov      dword ptr [esp + 0x34], eax
00415610  8a4601                 mov      al, byte ptr [esi + 1]
00415613  3c05                   cmp      al, 5
00415615  0f82f5020000           jb       0x415910
0041561b  3c0a                   cmp      al, 0xa
0041561d  7618                   jbe      0x415637
0041561f  3c13                   cmp      al, 0x13
00415621  0f82e2020000           jb       0x415909
00415627  3c16                   cmp      al, 0x16
00415629  760c                   jbe      0x415637
0041562b  3c18                   cmp      al, 0x18
0041562d  7608                   jbe      0x415637
0041562f  3c19                   cmp      al, 0x19
00415631  0f85e0020000           jne      0x415917
00415637  31c0                   xor      eax, eax
00415639  668b86c2000000         mov      ax, word ptr [esi + 0xc2]
00415640  3d3b010000             cmp      eax, 0x13b
00415645  7f5a                   jg       0x4156a1
00415647  31d2                   xor      edx, edx
00415649  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041564f  42                     inc      edx
00415650  89d0                   mov      eax, edx
00415652  c1fa1f                 sar      edx, 0x1f
00415655  2bc2                   sub      eax, edx
00415657  d1f8                   sar      eax, 1
00415659  31d2                   xor      edx, edx
0041565b  48                     dec      eax
0041565c  8a96db000000           mov      dl, byte ptr [esi + 0xdb]
00415662  0fafd0                 imul     edx, eax
00415665  31c0                   xor      eax, eax
00415667  668b442434             mov      ax, word ptr [esp + 0x34]
0041566c  01d0                   add      eax, edx
0041566e  31d2                   xor      edx, edx
00415670  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00415676  31db                   xor      ebx, ebx
00415678  01d0                   add      eax, edx
0041567a  8b7c2414               mov      edi, dword ptr [esp + 0x14]
0041567e  6689c3                 mov      bx, ax
00415681  8b442428               mov      eax, dword ptr [esp + 0x28]
00415685  01f8                   add      eax, edi
00415687  8b7c2410               mov      edi, dword ptr [esp + 0x10]
0041568b  0fbfd0                 movsx    edx, ax
0041568e  8b44243c               mov      eax, dword ptr [esp + 0x3c]
00415692  31c9                   xor      ecx, ecx
00415694  01f8                   add      eax, edi
00415696  668b4c242c             mov      cx, word ptr [esp + 0x2c]
0041569b  98                     cwde
0041569c  e8a6baffff             call     0x411147 ; AffCorpsEngin
004156a1  31c0                   xor      eax, eax
004156a3  668b86c2000000         mov      ax, word ptr [esi + 0xc2]
004156aa  3d2c010000             cmp      eax, 0x12c
004156af  0f8c20010000           jl       0x4157d5
004156b5  3d3b010000             cmp      eax, 0x13b
004156ba  0f8d15010000           jge      0x4157d5
004156c0  31c0                   xor      eax, eax
004156c2  89442420               mov      dword ptr [esp + 0x20], eax
004156c6  eb1a                   jmp      0x4156e2 ;
004156c8  81e3ffff0000           and      ebx, 0xffff
004156ce  0fbfd1                 movsx    edx, cx
004156d1  0fbfc7                 movsx    eax, di
004156d4  b901000000             mov      ecx, 1
004156d9  e8b8600400             call     0x45b796 ; PasteOmbreCmp
004156de  ff442420               inc      dword ptr [esp + 0x20]
004156e2  31d2                   xor      edx, edx
004156e4  668b96c2000000         mov      dx, word ptr [esi + 0xc2]
004156eb  81ea2c010000           sub      edx, 0x12c
004156f1  bb05000000             mov      ebx, 5
004156f6  89d0                   mov      eax, edx
004156f8  c1fa1f                 sar      edx, 0x1f
004156fb  f7fb                   idiv     ebx
004156fd  31d2                   xor      edx, edx
004156ff  668b542420             mov      dx, word ptr [esp + 0x20]
00415704  39c2                   cmp      edx, eax
00415706  0f8dc9000000           jge      0x4157d5
0041570c  31d2                   xor      edx, edx
0041570e  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415714  42                     inc      edx
00415715  89d0                   mov      eax, edx
00415717  c1fa1f                 sar      edx, 0x1f
0041571a  2bc2                   sub      eax, edx
0041571c  d1f8                   sar      eax, 1
0041571e  31d2                   xor      edx, edx
00415720  48                     dec      eax
00415721  8a96db000000           mov      dl, byte ptr [esi + 0xdb]
00415727  0fafd0                 imul     edx, eax
0041572a  8b4c2428               mov      ecx, dword ptr [esp + 0x28]
0041572e  8b7c243c               mov      edi, dword ptr [esp + 0x3c]
00415732  31c0                   xor      eax, eax
00415734  31db                   xor      ebx, ebx
00415736  668b442434             mov      ax, word ptr [esp + 0x34]
0041573b  8a9ea4000000           mov      bl, byte ptr [esi + 0xa4]
00415741  01d0                   add      eax, edx
00415743  8b542414               mov      edx, dword ptr [esp + 0x14]
00415747  01c3                   add      ebx, eax
00415749  8b442410               mov      eax, dword ptr [esp + 0x10]
0041574d  01d1                   add      ecx, edx
0041574f  895c240c               mov      dword ptr [esp + 0xc], ebx
00415753  66894c2418             mov      word ptr [esp + 0x18], cx
00415758  01c7                   add      edi, eax
0041575a  31c0                   xor      eax, eax
0041575c  31d2                   xor      edx, edx
0041575e  668b44242c             mov      ax, word ptr [esp + 0x2c]
00415763  66897c2438             mov      word ptr [esp + 0x38], di
00415768  e8d8c80200             call     0x442045 ; EnginGetPlayer
0041576d  88c2                   mov      dl, al
0041576f  88442444               mov      byte ptr [esp + 0x44], al
00415773  85d2                   test     edx, edx
00415775  7411                   je       0x415788
00415777  81fac8000000           cmp      edx, 0xc8
0041577d  7409                   je       0x415788
0041577f  83fa04                 cmp      edx, 4
00415782  0f8540ffffff           jne      0x4156c8
00415788  8b6c2416               mov      ebp, dword ptr [esp + 0x16]
0041578c  8b442436               mov      eax, dword ptr [esp + 0x36]
00415790  31ff                   xor      edi, edi
00415792  b901000000             mov      ecx, 1
00415797  668b7c240c             mov      di, word ptr [esp + 0xc]
0041579c  c1fd10                 sar      ebp, 0x10
0041579f  c1f810                 sar      eax, 0x10
004157a2  89fb                   mov      ebx, edi
004157a4  89ea                   mov      edx, ebp
004157a6  890424                 mov      dword ptr [esp], eax
004157a9  e8e85f0400             call     0x45b796 ; PasteOmbreCmp
004157ae  31c0                   xor      eax, eax
004157b0  8a442444               mov      al, byte ptr [esp + 0x44]
004157b4  3dc8000000             cmp      eax, 0xc8
004157b9  0f851fffffff           jne      0x4156de
004157bf  b901000000             mov      ecx, 1
004157c4  8b0424                 mov      eax, dword ptr [esp]
004157c7  89fb                   mov      ebx, edi
004157c9  89ea                   mov      edx, ebp
004157cb  e8e0640400             call     0x45bcb0 ; PasteGrisCmp
004157d0  e909ffffff             jmp      0x4156de ;
004157d5  31c0                   xor      eax, eax
004157d7  668b86c2000000         mov      ax, word ptr [esi + 0xc2]
004157de  3d3b010000             cmp      eax, 0x13b
004157e3  0f8c2e010000           jl       0x415917
004157e9  31db                   xor      ebx, ebx
004157eb  895c241c               mov      dword ptr [esp + 0x1c], ebx
004157ef  eb1a                   jmp      0x41580b ;
004157f1  81e3ffff0000           and      ebx, 0xffff
004157f7  0fbfd7                 movsx    edx, di
004157fa  0fbfc1                 movsx    eax, cx
004157fd  b901000000             mov      ecx, 1
00415802  e88f5f0400             call     0x45b796 ; PasteOmbreCmp
00415807  ff44241c               inc      dword ptr [esp + 0x1c]
0041580b  31d2                   xor      edx, edx
0041580d  668b96c2000000         mov      dx, word ptr [esi + 0xc2]
00415814  81ea3b010000           sub      edx, 0x13b
0041581a  bb05000000             mov      ebx, 5
0041581f  89d0                   mov      eax, edx
00415821  c1fa1f                 sar      edx, 0x1f
00415824  f7fb                   idiv     ebx
00415826  ba03000000             mov      edx, 3
0041582b  29c2                   sub      edx, eax
0041582d  89d0                   mov      eax, edx
0041582f  31d2                   xor      edx, edx
00415831  668b54241c             mov      dx, word ptr [esp + 0x1c]
00415836  39c2                   cmp      edx, eax
00415838  0f8dd9000000           jge      0x415917
0041583e  31d2                   xor      edx, edx
00415840  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415846  42                     inc      edx
00415847  89d0                   mov      eax, edx
00415849  c1fa1f                 sar      edx, 0x1f
0041584c  2bc2                   sub      eax, edx
0041584e  d1f8                   sar      eax, 1
00415850  31d2                   xor      edx, edx
00415852  48                     dec      eax
00415853  8a96db000000           mov      dl, byte ptr [esi + 0xdb]
00415859  0fafd0                 imul     edx, eax
0041585c  8b7c2428               mov      edi, dword ptr [esp + 0x28]
00415860  31db                   xor      ebx, ebx
00415862  8b4c2414               mov      ecx, dword ptr [esp + 0x14]
00415866  8a9ea4000000           mov      bl, byte ptr [esi + 0xa4]
0041586c  31c0                   xor      eax, eax
0041586e  01cf                   add      edi, ecx
00415870  668b442434             mov      ax, word ptr [esp + 0x34]
00415875  8b4c243c               mov      ecx, dword ptr [esp + 0x3c]
00415879  01d0                   add      eax, edx
0041587b  66897c2408             mov      word ptr [esp + 8], di
00415880  01c3                   add      ebx, eax
00415882  8b442410               mov      eax, dword ptr [esp + 0x10]
00415886  31d2                   xor      edx, edx
00415888  01c1                   add      ecx, eax
0041588a  31c0                   xor      eax, eax
0041588c  895c2424               mov      dword ptr [esp + 0x24], ebx
00415890  668b44242c             mov      ax, word ptr [esp + 0x2c]
00415895  66894c2430             mov      word ptr [esp + 0x30], cx
0041589a  e8a6c70200             call     0x442045 ; EnginGetPlayer
0041589f  88c2                   mov      dl, al
004158a1  88442440               mov      byte ptr [esp + 0x40], al
004158a5  85d2                   test     edx, edx
004158a7  7411                   je       0x4158ba
004158a9  81fac8000000           cmp      edx, 0xc8
004158af  7409                   je       0x4158ba
004158b1  83fa04                 cmp      edx, 4
004158b4  0f8537ffffff           jne      0x4157f1
004158ba  8b6c2406               mov      ebp, dword ptr [esp + 6]
004158be  8b44242e               mov      eax, dword ptr [esp + 0x2e]
004158c2  31ff                   xor      edi, edi
004158c4  b901000000             mov      ecx, 1
004158c9  668b7c2424             mov      di, word ptr [esp + 0x24]
004158ce  c1fd10                 sar      ebp, 0x10
004158d1  c1f810                 sar      eax, 0x10
004158d4  89fb                   mov      ebx, edi
004158d6  89ea                   mov      edx, ebp
004158d8  89442404               mov      dword ptr [esp + 4], eax
004158dc  e8b55e0400             call     0x45b796 ; PasteOmbreCmp
004158e1  31c0                   xor      eax, eax
004158e3  8a442440               mov      al, byte ptr [esp + 0x40]
004158e7  3dc8000000             cmp      eax, 0xc8
004158ec  0f8515ffffff           jne      0x415807
004158f2  b901000000             mov      ecx, 1
004158f7  8b442404               mov      eax, dword ptr [esp + 4]
004158fb  89fb                   mov      ebx, edi
004158fd  89ea                   mov      edx, ebp
004158ff  e8ac630400             call     0x45bcb0 ; PasteGrisCmp
00415904  e9fefeffff             jmp      0x415807 ;
00415909  3c12                   cmp      al, 0x12
0041590b  e921fdffff             jmp      0x415631 ;
00415910  3c02                   cmp      al, 2
00415912  e920fdffff             jmp      0x415637 ;
00415917  83c448                 add      esp, 0x48
0041591a  5d                     pop      ebp
0041591b  5f                     pop      edi
0041591c  5e                     pop      esi
0041591d  59                     pop      ecx
0041591e  c3                     ret
