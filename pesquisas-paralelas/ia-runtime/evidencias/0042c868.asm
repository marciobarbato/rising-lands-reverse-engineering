; CalculGame (frame); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0042c868..0x0042d4f8 (end exclusive); labels are original SBL names
0042c868  53                       push ebx
0042c869  51                       push ecx
0042c86a  52                       push edx
0042c86b  56                       push esi
0042c86c  57                       push edi
0042c86d  55                       push ebp
0042c86e  81ec0c010000             sub esp, 0x10c
0042c874  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042c879  88842404010000           mov byte ptr [esp + 0x104], al
0042c880  31c0                     xor eax, eax
0042c882  66a1aa995000             mov ax, word ptr [0x5099aa]
0042c888  50                       push eax
0042c889  31c0                     xor eax, eax
0042c88b  66a1a8995000             mov ax, word ptr [0x5099a8]
0042c891  bad81d0000               mov edx, 0x1dd8
0042c896  50                       push eax
0042c897  66891510a04900           mov word ptr [0x49a010], dx
0042c89e  2eff15c8325200           call dword ptr cs:[0x5232c8] ; -> USER32.dll!SetCursorPos
0042c8a5  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042c8aa  3c18                     cmp al, 0x18
0042c8ac  0f87300c0000             ja 0x42d4e2
0042c8b2  25ff000000               and eax, 0xff
0042c8b7  2eff248504c84200         jmp dword ptr cs:[eax*4 + 0x42c804]
0042c8bf  be94955000               mov esi, 0x509594
0042c8c4  89e7                     mov edi, esp
0042c8c6  57                       push edi
0042c8c7  8a06                     mov al, byte ptr [esi]
0042c8c9  8807                     mov byte ptr [edi], al
0042c8cb  3c00                     cmp al, 0
0042c8cd  7410                     je 0x42c8df
0042c8cf  8a4601                   mov al, byte ptr [esi + 1]
0042c8d2  83c602                   add esi, 2
0042c8d5  884701                   mov byte ptr [edi + 1], al
0042c8d8  83c702                   add edi, 2
0042c8db  3c00                     cmp al, 0
0042c8dd  75e8                     jne 0x42c8c7
0042c8df  5f                       pop edi
0042c8e0  be44444900               mov esi, 0x494444
0042c8e5  89e7                     mov edi, esp
0042c8e7  ba58444900               mov edx, 0x494458
0042c8ec  57                       push edi
0042c8ed  2bc9                     sub ecx, ecx
0042c8ef  49                       dec ecx
0042c8f0  b000                     mov al, 0
0042c8f2  f2ae                     repne scasb al, byte ptr es:[edi]
0042c8f4  4f                       dec edi
0042c8f5  8a06                     mov al, byte ptr [esi]
0042c8f7  8807                     mov byte ptr [edi], al
0042c8f9  3c00                     cmp al, 0
0042c8fb  7410                     je 0x42c90d
0042c8fd  8a4601                   mov al, byte ptr [esi + 1]
0042c900  83c602                   add esi, 2
0042c903  884701                   mov byte ptr [edi + 1], al
0042c906  83c702                   add edi, 2
0042c909  3c00                     cmp al, 0
0042c90b  75e8                     jne 0x42c8f5
0042c90d  5f                       pop edi
0042c90e  89e0                     mov eax, esp
0042c910  e80bbb0200               call 0x458420 ; -> FileOpen
0042c915  84c0                     test al, al
0042c917  7422                     je 0x42c93b
0042c919  e82ebb0200               call 0x45844c ; -> FileClose
0042c91e  89e0                     mov eax, esp
0042c920  e807ff0400               call 0x47c82c ; -> PlayVideo
0042c925  31c0                     xor eax, eax
0042c927  ba02000000               mov edx, 2
0042c92c  a041805000               mov al, byte ptr [0x508041]
0042c931  e885b90300               call 0x4682bb ; -> MenuInit
0042c936  e9a70b0000               jmp 0x42d4e2
0042c93b  a1b0244e00               mov eax, dword ptr [0x4e24b0]
0042c940  e8ec240100               call 0x43ee31 ; -> DDSetPalette
0042c945  ebde                     jmp 0x42c925
0042c947  be94955000               mov esi, 0x509594
0042c94c  89e7                     mov edi, esp
0042c94e  57                       push edi
0042c94f  8a06                     mov al, byte ptr [esi]
0042c951  8807                     mov byte ptr [edi], al
0042c953  3c00                     cmp al, 0
0042c955  7410                     je 0x42c967
0042c957  8a4601                   mov al, byte ptr [esi + 1]
0042c95a  83c602                   add esi, 2
0042c95d  884701                   mov byte ptr [edi + 1], al
0042c960  83c702                   add edi, 2
0042c963  3c00                     cmp al, 0
0042c965  75e8                     jne 0x42c94f
0042c967  5f                       pop edi
0042c968  be5b444900               mov esi, 0x49445b
0042c96d  89e7                     mov edi, esp
0042c96f  ba6f444900               mov edx, 0x49446f
0042c974  e973ffffff               jmp 0x42c8ec
0042c979  6a1b                     push 0x1b
0042c97b  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042c982  98                       cwde
0042c983  85c0                     test eax, eax
0042c985  7c1a                     jl 0x42c9a1
0042c987  803dae99500000           cmp byte ptr [0x5099ae], 0
0042c98e  0f844e0b0000             je 0x42d4e2
0042c994  803daf99500000           cmp byte ptr [0x5099af], 0
0042c99b  0f84410b0000             je 0x42d4e2
0042c9a1  31c0                     xor eax, eax
0042c9a3  ba02000000               mov edx, 2
0042c9a8  a041805000               mov al, byte ptr [0x508041]
0042c9ad  e809b90300               call 0x4682bb ; -> MenuInit
0042c9b2  6a1b                     push 0x1b
0042c9b4  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042c9bb  98                       cwde
0042c9bc  85c0                     test eax, eax
0042c9be  7cf2                     jl 0x42c9b2
0042c9c0  e91d0b0000               jmp 0x42d4e2
0042c9c5  31c0                     xor eax, eax
0042c9c7  a041805000               mov al, byte ptr [0x508041]
0042c9cc  e813bc0200               call 0x4585e4 ; -> PartieGetResultat
0042c9d1  84c0                     test al, al
0042c9d3  7563                     jne 0x42ca38
0042c9d5  be94955000               mov esi, 0x509594
0042c9da  89e7                     mov edi, esp
0042c9dc  57                       push edi
0042c9dd  8a06                     mov al, byte ptr [esi]
0042c9df  8807                     mov byte ptr [edi], al
0042c9e1  3c00                     cmp al, 0
0042c9e3  7410                     je 0x42c9f5
0042c9e5  8a4601                   mov al, byte ptr [esi + 1]
0042c9e8  83c602                   add esi, 2
0042c9eb  884701                   mov byte ptr [edi + 1], al
0042c9ee  83c702                   add edi, 2
0042c9f1  3c00                     cmp al, 0
0042c9f3  75e8                     jne 0x42c9dd
0042c9f5  5f                       pop edi
0042c9f6  be72444900               mov esi, 0x494472
0042c9fb  89e7                     mov edi, esp
0042c9fd  ba86444900               mov edx, 0x494486
0042ca02  57                       push edi
0042ca03  2bc9                     sub ecx, ecx
0042ca05  49                       dec ecx
0042ca06  b000                     mov al, 0
0042ca08  f2ae                     repne scasb al, byte ptr es:[edi]
0042ca0a  4f                       dec edi
0042ca0b  8a06                     mov al, byte ptr [esi]
0042ca0d  8807                     mov byte ptr [edi], al
0042ca0f  3c00                     cmp al, 0
0042ca11  7410                     je 0x42ca23
0042ca13  8a4601                   mov al, byte ptr [esi + 1]
0042ca16  83c602                   add esi, 2
0042ca19  884701                   mov byte ptr [edi + 1], al
0042ca1c  83c702                   add edi, 2
0042ca1f  3c00                     cmp al, 0
0042ca21  75e8                     jne 0x42ca0b
0042ca23  5f                       pop edi
0042ca24  89e0                     mov eax, esp
0042ca26  e8f5b90200               call 0x458420 ; -> FileOpen
0042ca2b  84c0                     test al, al
0042ca2d  0f84f2feffff             je 0x42c925
0042ca33  e9e1feffff               jmp 0x42c919
0042ca38  6a0d                     push 0xd
0042ca3a  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042ca41  98                       cwde
0042ca42  85c0                     test eax, eax
0042ca44  7c1a                     jl 0x42ca60
0042ca46  803dae99500000           cmp byte ptr [0x5099ae], 0
0042ca4d  0f848f0a0000             je 0x42d4e2
0042ca53  803daf99500000           cmp byte ptr [0x5099af], 0
0042ca5a  0f84820a0000             je 0x42d4e2
0042ca60  6a0d                     push 0xd
0042ca62  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042ca69  98                       cwde
0042ca6a  85c0                     test eax, eax
0042ca6c  7cf2                     jl 0x42ca60
0042ca6e  e819f60300               call 0x46c08c ; -> MissionNext
0042ca73  25ff000000               and eax, 0xff
0042ca78  83f801                   cmp eax, 1
0042ca7b  7520                     jne 0x42ca9d
0042ca7d  e806300500               call 0x47fa88 ; -> IaRechercheAjuste
0042ca82  e8714a0100               call 0x4414f8 ; -> Engin_StoreExperimente
0042ca87  e8644a0400               call 0x4714f0 ; -> RechercheStore
0042ca8c  e854140400               call 0x46dee5 ; -> PlayerStore
0042ca91  31c0                     xor eax, eax
0042ca93  ba11000000               mov edx, 0x11
0042ca98  e98ffeffff               jmp 0x42c92c
0042ca9d  31c0                     xor eax, eax
0042ca9f  ba18000000               mov edx, 0x18
0042caa4  e983feffff               jmp 0x42c92c
0042caa9  803dae99500000           cmp byte ptr [0x5099ae], 0
0042cab0  0f8524010000             jne 0x42cbda
0042cab6  6a0d                     push 0xd
0042cab8  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042cabf  98                       cwde
0042cac0  85c0                     test eax, eax
0042cac2  0f8d1a0a0000             jge 0x42d4e2
0042cac8  30d2                     xor dl, dl
0042caca  8815782f4e00             mov byte ptr [0x4e2f78], dl
0042cad0  e90d0a0000               jmp 0x42d4e2
0042cad5  31c0                     xor eax, eax
0042cad7  31d2                     xor edx, edx
0042cad9  a041805000               mov al, byte ptr [0x508041]
0042cade  e854400400               call 0x470b37 ; -> RechercheSetBranche
0042cae3  ebd1                     jmp 0x42cab6
0042cae5  31c0                     xor eax, eax
0042cae7  ba02000000               mov edx, 2
0042caec  ebeb                     jmp 0x42cad9
0042caee  31c0                     xor eax, eax
0042caf0  ba01000000               mov edx, 1
0042caf5  ebe2                     jmp 0x42cad9
0042caf7  31c0                     xor eax, eax
0042caf9  ba03000000               mov edx, 3
0042cafe  ebd9                     jmp 0x42cad9
0042cb00  30e4                     xor ah, ah
0042cb02  8825782f4e00             mov byte ptr [0x4e2f78], ah
0042cb08  ebac                     jmp 0x42cab6
0042cb0a  bb0a000000               mov ebx, 0xa
0042cb0f  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cb14  31d2                     xor edx, edx
0042cb16  f7f3                     div ebx
0042cb18  85d2                     test edx, edx
0042cb1a  759a                     jne 0x42cab6
0042cb1c  b8ffffffff               mov eax, 0xffffffff
0042cb21  e8a4fc0400               call 0x47c7ca ; -> ObjectifTextScroll
0042cb26  eb8e                     jmp 0x42cab6
0042cb28  bb0a000000               mov ebx, 0xa
0042cb2d  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cb32  31d2                     xor edx, edx
0042cb34  f7f3                     div ebx
0042cb36  85d2                     test edx, edx
0042cb38  0f8578ffffff             jne 0x42cab6
0042cb3e  b801000000               mov eax, 1
0042cb43  ebdc                     jmp 0x42cb21
0042cb45  803daf99500000           cmp byte ptr [0x5099af], 0
0042cb4c  7528                     jne 0x42cb76
0042cb4e  e963ffffff               jmp 0x42cab6
0042cb53  b403                     mov ah, 3
0042cb55  e96c000000               jmp 0x42cbc6
0042cb5a  b410                     mov ah, 0x10
0042cb5c  e965000000               jmp 0x42cbc6
0042cb61  b402                     mov ah, 2
0042cb63  e95e000000               jmp 0x42cbc6
0042cb68  b405                     mov ah, 5
0042cb6a  e957000000               jmp 0x42cbc6
0042cb6f  b412                     mov ah, 0x12
0042cb71  e950000000               jmp 0x42cbc6
0042cb76  8a25782f4e00             mov ah, byte ptr [0x4e2f78]
0042cb7c  88e0                     mov al, ah
0042cb7e  80fc0c                   cmp ah, 0xc
0042cb81  7221                     jb 0x42cba4
0042cb83  76d5                     jbe 0x42cb5a
0042cb85  80fc10                   cmp ah, 0x10
0042cb88  7210                     jb 0x42cb9a
0042cb8a  76e3                     jbe 0x42cb6f
0042cb8c  80fc12                   cmp ah, 0x12
0042cb8f  72d0                     jb 0x42cb61
0042cb91  76c7                     jbe 0x42cb5a
0042cb93  80fc17                   cmp ah, 0x17
0042cb96  74c2                     je 0x42cb5a
0042cb98  eb2c                     jmp 0x42cbc6
0042cb9a  80fc0d                   cmp ah, 0xd
0042cb9d  76b4                     jbe 0x42cb53
0042cb9f  80fc0e                   cmp ah, 0xe
0042cba2  ebf2                     jmp 0x42cb96
0042cba4  80fc06                   cmp ah, 6
0042cba7  7211                     jb 0x42cbba
0042cba9  80fc07                   cmp ah, 7
0042cbac  76ba                     jbe 0x42cb68
0042cbae  80fc09                   cmp ah, 9
0042cbb1  76b5                     jbe 0x42cb68
0042cbb3  80fc0a                   cmp ah, 0xa
0042cbb6  74a9                     je 0x42cb61
0042cbb8  eb0c                     jmp 0x42cbc6
0042cbba  80fc03                   cmp ah, 3
0042cbbd  7207                     jb 0x42cbc6
0042cbbf  80fc04                   cmp ah, 4
0042cbc2  769d                     jbe 0x42cb61
0042cbc4  b404                     mov ah, 4
0042cbc6  0fbed4                   movsx edx, ah
0042cbc9  31c0                     xor eax, eax
0042cbcb  a041805000               mov al, byte ptr [0x508041]
0042cbd0  e8e6b60300               call 0x4682bb ; -> MenuInit
0042cbd5  e9dcfeffff               jmp 0x42cab6
0042cbda  e8cdd00400               call 0x479cac ; -> MouseZone
0042cbdf  66a3ac995000             mov word ptr [0x5099ac], ax
0042cbe5  48                       dec eax
0042cbe6  663d0700                 cmp ax, 7
0042cbea  0f87c6feffff             ja 0x42cab6
0042cbf0  25ffff0000               and eax, 0xffff
0042cbf5  2eff2485b4c74200         jmp dword ptr cs:[eax*4 + 0x42c7b4]
0042cbfd  803dae99500000           cmp byte ptr [0x5099ae], 0
0042cc04  0f85d1000000             jne 0x42ccdb
0042cc0a  6a0d                     push 0xd
0042cc0c  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042cc13  98                       cwde
0042cc14  85c0                     test eax, eax
0042cc16  0f8c00010000             jl 0x42cd1c
0042cc1c  e9c1080000               jmp 0x42d4e2
0042cc21  bb0a000000               mov ebx, 0xa
0042cc26  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cc2b  31d2                     xor edx, edx
0042cc2d  f7f3                     div ebx
0042cc2f  85d2                     test edx, edx
0042cc31  75d7                     jne 0x42cc0a
0042cc33  b8ffffffff               mov eax, 0xffffffff
0042cc38  e88dfb0400               call 0x47c7ca ; -> ObjectifTextScroll
0042cc3d  ebcb                     jmp 0x42cc0a
0042cc3f  bb0a000000               mov ebx, 0xa
0042cc44  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cc49  31d2                     xor edx, edx
0042cc4b  f7f3                     div ebx
0042cc4d  85d2                     test edx, edx
0042cc4f  75b9                     jne 0x42cc0a
0042cc51  b801000000               mov eax, 1
0042cc56  ebe0                     jmp 0x42cc38
0042cc58  803daf99500000           cmp byte ptr [0x5099af], 0
0042cc5f  7525                     jne 0x42cc86
0042cc61  eba7                     jmp 0x42cc0a
0042cc63  b003                     mov al, 3
0042cc65  e95d000000               jmp 0x42ccc7
0042cc6a  b010                     mov al, 0x10
0042cc6c  e956000000               jmp 0x42ccc7
0042cc71  b002                     mov al, 2
0042cc73  e94f000000               jmp 0x42ccc7
0042cc78  b005                     mov al, 5
0042cc7a  e948000000               jmp 0x42ccc7
0042cc7f  b012                     mov al, 0x12
0042cc81  e941000000               jmp 0x42ccc7
0042cc86  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cc8b  3c0c                     cmp al, 0xc
0042cc8d  721c                     jb 0x42ccab
0042cc8f  76d9                     jbe 0x42cc6a
0042cc91  3c10                     cmp al, 0x10
0042cc93  720e                     jb 0x42cca3
0042cc95  76e8                     jbe 0x42cc7f
0042cc97  3c12                     cmp al, 0x12
0042cc99  72d6                     jb 0x42cc71
0042cc9b  76cd                     jbe 0x42cc6a
0042cc9d  3c17                     cmp al, 0x17
0042cc9f  74c9                     je 0x42cc6a
0042cca1  eb24                     jmp 0x42ccc7
0042cca3  3c0d                     cmp al, 0xd
0042cca5  76bc                     jbe 0x42cc63
0042cca7  3c0e                     cmp al, 0xe
0042cca9  ebf4                     jmp 0x42cc9f
0042ccab  3c06                     cmp al, 6
0042ccad  720e                     jb 0x42ccbd
0042ccaf  3c07                     cmp al, 7
0042ccb1  76c5                     jbe 0x42cc78
0042ccb3  3c09                     cmp al, 9
0042ccb5  76c1                     jbe 0x42cc78
0042ccb7  3c0a                     cmp al, 0xa
0042ccb9  74b6                     je 0x42cc71
0042ccbb  eb0a                     jmp 0x42ccc7
0042ccbd  3c03                     cmp al, 3
0042ccbf  7206                     jb 0x42ccc7
0042ccc1  3c04                     cmp al, 4
0042ccc3  76ac                     jbe 0x42cc71
0042ccc5  b004                     mov al, 4
0042ccc7  0fbed0                   movsx edx, al
0042ccca  31c0                     xor eax, eax
0042cccc  a041805000               mov al, byte ptr [0x508041]
0042ccd1  e8e5b50300               call 0x4682bb ; -> MenuInit
0042ccd6  e92fffffff               jmp 0x42cc0a
0042ccdb  e8cccf0400               call 0x479cac ; -> MouseZone
0042cce0  66a3ac995000             mov word ptr [0x5099ac], ax
0042cce6  83e805                   sub eax, 5
0042cce9  663d0300                 cmp ax, 3
0042cced  0f8717ffffff             ja 0x42cc0a
0042ccf3  25ffff0000               and eax, 0xffff
0042ccf8  2eff2485d4c74200         jmp dword ptr cs:[eax*4 + 0x42c7d4]
0042cd00  b003                     mov al, 3
0042cd02  0fbed0                   movsx edx, al
0042cd05  31c0                     xor eax, eax
0042cd07  e920fcffff               jmp 0x42c92c
0042cd0c  b010                     mov al, 0x10
0042cd0e  ebf2                     jmp 0x42cd02
0042cd10  b002                     mov al, 2
0042cd12  ebee                     jmp 0x42cd02
0042cd14  b005                     mov al, 5
0042cd16  ebea                     jmp 0x42cd02
0042cd18  b012                     mov al, 0x12
0042cd1a  ebe6                     jmp 0x42cd02
0042cd1c  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cd21  3c0c                     cmp al, 0xc
0042cd23  721c                     jb 0x42cd41
0042cd25  76e5                     jbe 0x42cd0c
0042cd27  3c10                     cmp al, 0x10
0042cd29  720e                     jb 0x42cd39
0042cd2b  76eb                     jbe 0x42cd18
0042cd2d  3c12                     cmp al, 0x12
0042cd2f  72df                     jb 0x42cd10
0042cd31  76d9                     jbe 0x42cd0c
0042cd33  3c17                     cmp al, 0x17
0042cd35  74d5                     je 0x42cd0c
0042cd37  ebc9                     jmp 0x42cd02
0042cd39  3c0d                     cmp al, 0xd
0042cd3b  76c3                     jbe 0x42cd00
0042cd3d  3c0e                     cmp al, 0xe
0042cd3f  ebf4                     jmp 0x42cd35
0042cd41  3c06                     cmp al, 6
0042cd43  720e                     jb 0x42cd53
0042cd45  3c07                     cmp al, 7
0042cd47  76cb                     jbe 0x42cd14
0042cd49  3c09                     cmp al, 9
0042cd4b  76c7                     jbe 0x42cd14
0042cd4d  3c0a                     cmp al, 0xa
0042cd4f  74bf                     je 0x42cd10
0042cd51  ebaf                     jmp 0x42cd02
0042cd53  3c03                     cmp al, 3
0042cd55  72ab                     jb 0x42cd02
0042cd57  3c04                     cmp al, 4
0042cd59  76b5                     jbe 0x42cd10
0042cd5b  b004                     mov al, 4
0042cd5d  eba3                     jmp 0x42cd02
0042cd5f  6a20                     push 0x20
0042cd61  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042cd68  98                       cwde
0042cd69  85c0                     test eax, eax
0042cd6b  0f8d71070000             jge 0x42d4e2
0042cd71  31c0                     xor eax, eax
0042cd73  ba12000000               mov edx, 0x12
0042cd78  e9affbffff               jmp 0x42c92c
0042cd7d  bb28000000               mov ebx, 0x28
0042cd82  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cd87  31d2                     xor edx, edx
0042cd89  f7f3                     div ebx
0042cd8b  85d2                     test edx, edx
0042cd8d  7515                     jne 0x42cda4
0042cd8f  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042cd96  750c                     jne 0x42cda4
0042cd98  31c0                     xor eax, eax
0042cd9a  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cd9f  e874b20300               call 0x468018 ; -> UpdateListSession
0042cda4  bb28000000               mov ebx, 0x28
0042cda9  a17c8f5000               mov eax, dword ptr [0x508f7c]
0042cdae  31d2                     xor edx, edx
0042cdb0  f7f3                     div ebx
0042cdb2  85d2                     test edx, edx
0042cdb4  7515                     jne 0x42cdcb
0042cdb6  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042cdbd  740c                     je 0x42cdcb
0042cdbf  31c0                     xor eax, eax
0042cdc1  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cdc6  e84bb10300               call 0x467f16 ; -> UpdateListPlayer
0042cdcb  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042cdd2  0f84ca000000             je 0x42cea2
0042cdd8  833d0c3b4e0001           cmp dword ptr [0x4e3b0c], 1
0042cddf  0f85bd000000             jne 0x42cea2
0042cde5  8b1d74174e00             mov ebx, dword ptr [0x4e1774]
0042cdeb  85db                     test ebx, ebx
0042cded  740f                     je 0x42cdfe
0042cdef  89d8                     mov eax, ebx
0042cdf1  31c9                     xor ecx, ecx
0042cdf3  e8d3b00300               call 0x467ecb ; -> MemFree
0042cdf8  890d74174e00             mov dword ptr [0x4e1774], ecx
0042cdfe  8b3578174e00             mov esi, dword ptr [0x4e1778]
0042ce04  85f6                     test esi, esi
0042ce06  740f                     je 0x42ce17
0042ce08  89f0                     mov eax, esi
0042ce0a  31ff                     xor edi, edi
0042ce0c  e8bab00300               call 0x467ecb ; -> MemFree
0042ce11  893d78174e00             mov dword ptr [0x4e1778], edi
0042ce17  8b2d7c174e00             mov ebp, dword ptr [0x4e177c]
0042ce1d  85ed                     test ebp, ebp
0042ce1f  740e                     je 0x42ce2f
0042ce21  89e8                     mov eax, ebp
0042ce23  e8a3b00300               call 0x467ecb ; -> MemFree
0042ce28  31c0                     xor eax, eax
0042ce2a  a37c174e00               mov dword ptr [0x4e177c], eax
0042ce2f  30db                     xor bl, bl
0042ce31  eb09                     jmp 0x42ce3c
0042ce33  31d2                     xor edx, edx
0042ce35  e8b8090400               call 0x46d7f2 ; -> SetPlayerType
0042ce3a  fec3                     inc bl
0042ce3c  31c0                     xor eax, eax
0042ce3e  88d8                     mov al, bl
0042ce40  83f804                   cmp eax, 4
0042ce43  7cee                     jl 0x42ce33
0042ce45  30d8                     xor al, bl
0042ce47  88842408010000           mov byte ptr [esp + 0x108], al
0042ce4e  eb07                     jmp 0x42ce57
0042ce50  fe842408010000           inc byte ptr [esp + 0x108]
0042ce57  31db                     xor ebx, ebx
0042ce59  8b3da4394e00             mov edi, dword ptr [0x4e39a4]
0042ce5f  8a9c2408010000           mov bl, byte ptr [esp + 0x108]
0042ce66  39fb                     cmp ebx, edi
0042ce68  7d30                     jge 0x42ce9a
0042ce6a  89d8                     mov eax, ebx
0042ce6c  8b149dec3a4e00           mov edx, dword ptr [ebx*4 + 0x4e3aec]
0042ce73  e85e080400               call 0x46d6d6 ; -> SetPlayerMPID
0042ce78  ba01000000               mov edx, 1
0042ce7d  89d8                     mov eax, ebx
0042ce7f  e86e090400               call 0x46d7f2 ; -> SetPlayerType
0042ce84  e84c040400               call 0x46d2d5 ; -> mpGetMyID
0042ce89  3b049dec3a4e00           cmp eax, dword ptr [ebx*4 + 0x4e3aec]
0042ce90  75be                     jne 0x42ce50
0042ce92  881d41805000             mov byte ptr [0x508041], bl
0042ce98  ebb6                     jmp 0x42ce50
0042ce9a  30e4                     xor ah, ah
0042ce9c  8825782f4e00             mov byte ptr [0x4e2f78], ah
0042cea2  803dae99500000           cmp byte ptr [0x5099ae], 0
0042cea9  740d                     je 0x42ceb8
0042ceab  803daf99500000           cmp byte ptr [0x5099af], 0
0042ceb2  0f8508010000             jne 0x42cfc0
0042ceb8  803db099500000           cmp byte ptr [0x5099b0], 0
0042cebf  0f85fb000000             jne 0x42cfc0
0042cec5  e918060000               jmp 0x42d4e2
0042ceca  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042ced1  7564                     jne 0x42cf37
0042ced3  803d782f4e0006           cmp byte ptr [0x4e2f78], 6
0042ceda  753b                     jne 0x42cf17
0042cedc  e8f3c50300               call 0x4694d4 ; -> NetCreateSession
0042cee1  25ff000000               and eax, 0xff
0042cee6  83f801                   cmp eax, 1
0042cee9  7519                     jne 0x42cf04
0042ceeb  31c0                     xor eax, eax
0042ceed  b301                     mov bl, 1
0042ceef  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cef4  881d30074e00             mov byte ptr [0x4e0730], bl
0042cefa  e817b00300               call 0x467f16 ; -> UpdateListPlayer
0042ceff  e9de050000               jmp 0x42d4e2
0042cf04  31c0                     xor eax, eax
0042cf06  ba04000000               mov edx, 4
0042cf0b  8a842400010000           mov al, byte ptr [esp + 0x100]
0042cf12  e91afaffff               jmp 0x42c931
0042cf17  e87bc60300               call 0x469597 ; -> NetJoinSession
0042cf1c  25ff000000               and eax, 0xff
0042cf21  83f801                   cmp eax, 1
0042cf24  75de                     jne 0x42cf04
0042cf26  31c0                     xor eax, eax
0042cf28  b601                     mov dh, 1
0042cf2a  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042cf2f  883530074e00             mov byte ptr [0x4e0730], dh
0042cf35  ebc3                     jmp 0x42cefa
0042cf37  803d782f4e0006           cmp byte ptr [0x4e2f78], 6
0042cf3e  0f859e050000             jne 0x42d4e2
0042cf44  833da4394e0002           cmp dword ptr [0x4e39a4], 2
0042cf4b  0f8c91050000             jl 0x42d4e2
0042cf51  ba01000000               mov edx, 1
0042cf56  bb48000000               mov ebx, 0x48
0042cf5b  31c0                     xor eax, eax
0042cf5d  89150c3b4e00             mov dword ptr [0x4e3b0c], edx
0042cf63  bacc3a4e00               mov edx, 0x4e3acc
0042cf68  e878010400               call 0x46d0e5 ; -> mpSend
0042cf6d  e970050000               jmp 0x42d4e2
0042cf72  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042cf79  0f8563050000             jne 0x42d4e2
0042cf7f  b8ffffffff               mov eax, 0xffffffff
0042cf84  e849c60300               call 0x4695d2 ; -> ScrollListSession
0042cf89  e954050000               jmp 0x42d4e2
0042cf8e  803d30074e0000           cmp byte ptr [0x4e0730], 0
0042cf95  0f8547050000             jne 0x42d4e2
0042cf9b  b801000000               mov eax, 1
0042cfa0  ebe2                     jmp 0x42cf84
0042cfa2  31c0                     xor eax, eax
0042cfa4  ba02000000               mov edx, 2
0042cfa9  a041805000               mov al, byte ptr [0x508041]
0042cfae  30c9                     xor cl, cl
0042cfb0  e806b30300               call 0x4682bb ; -> MenuInit
0042cfb5  880d30074e00             mov byte ptr [0x4e0730], cl
0042cfbb  e922050000               jmp 0x42d4e2
0042cfc0  e8e7cc0400               call 0x479cac ; -> MouseZone
0042cfc5  66a3ac995000             mov word ptr [0x5099ac], ax
0042cfcb  48                       dec eax
0042cfcc  663d0700                 cmp ax, 7
0042cfd0  0f870c050000             ja 0x42d4e2
0042cfd6  25ffff0000               and eax, 0xffff
0042cfdb  2eff2485e4c74200         jmp dword ptr cs:[eax*4 + 0x42c7e4]
0042cfe3  6a0d                     push 0xd
0042cfe5  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042cfec  98                       cwde
0042cfed  85c0                     test eax, eax
0042cfef  7d31                     jge 0x42d022
0042cff1  e887c30300               call 0x46937d ; -> MenuGetItemSelect
0042cff6  31db                     xor ebx, ebx
0042cff8  31d2                     xor edx, edx
0042cffa  6689c3                   mov bx, ax
0042cffd  31c0                     xor eax, eax
0042cfff  8a15782f4e00             mov dl, byte ptr [0x4e2f78]
0042d005  a041805000               mov al, byte ptr [0x508041]
0042d00a  e8d5f3ffff               call 0x42c3e4 ; -> MenuNewSelect
0042d00f  6a0d                     push 0xd
0042d011  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d018  98                       cwde
0042d019  85c0                     test eax, eax
0042d01b  7cf2                     jl 0x42d00f
0042d01d  e9ea000000               jmp 0x42d10c
0042d022  6a26                     push 0x26
0042d024  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d02b  98                       cwde
0042d02c  85c0                     test eax, eax
0042d02e  7d1d                     jge 0x42d04d
0042d030  b8ffffffff               mov eax, 0xffffffff
0042d035  e8e6c20300               call 0x469320 ; -> MenuScroll
0042d03a  6a26                     push 0x26
0042d03c  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d043  98                       cwde
0042d044  85c0                     test eax, eax
0042d046  7cf2                     jl 0x42d03a
0042d048  e9bf000000               jmp 0x42d10c
0042d04d  6a28                     push 0x28
0042d04f  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d056  98                       cwde
0042d057  85c0                     test eax, eax
0042d059  7d1d                     jge 0x42d078
0042d05b  b801000000               mov eax, 1
0042d060  e8bbc20300               call 0x469320 ; -> MenuScroll
0042d065  6a28                     push 0x28
0042d067  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d06e  98                       cwde
0042d06f  85c0                     test eax, eax
0042d071  7cf2                     jl 0x42d065
0042d073  e994000000               jmp 0x42d10c
0042d078  6a1b                     push 0x1b
0042d07a  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d081  98                       cwde
0042d082  85c0                     test eax, eax
0042d084  7c28                     jl 0x42d0ae
0042d086  e981000000               jmp 0x42d10c
0042d08b  b003                     mov al, 3
0042d08d  e95d000000               jmp 0x42d0ef
0042d092  b010                     mov al, 0x10
0042d094  e956000000               jmp 0x42d0ef
0042d099  b002                     mov al, 2
0042d09b  e94f000000               jmp 0x42d0ef
0042d0a0  b005                     mov al, 5
0042d0a2  e948000000               jmp 0x42d0ef
0042d0a7  b012                     mov al, 0x12
0042d0a9  e941000000               jmp 0x42d0ef
0042d0ae  a0782f4e00               mov al, byte ptr [0x4e2f78]
0042d0b3  3c0c                     cmp al, 0xc
0042d0b5  721c                     jb 0x42d0d3
0042d0b7  76d9                     jbe 0x42d092
0042d0b9  3c10                     cmp al, 0x10
0042d0bb  720e                     jb 0x42d0cb
0042d0bd  76e8                     jbe 0x42d0a7
0042d0bf  3c12                     cmp al, 0x12
0042d0c1  72d6                     jb 0x42d099
0042d0c3  76cd                     jbe 0x42d092
0042d0c5  3c17                     cmp al, 0x17
0042d0c7  74c9                     je 0x42d092
0042d0c9  eb24                     jmp 0x42d0ef
0042d0cb  3c0d                     cmp al, 0xd
0042d0cd  76bc                     jbe 0x42d08b
0042d0cf  3c0e                     cmp al, 0xe
0042d0d1  ebf4                     jmp 0x42d0c7
0042d0d3  3c06                     cmp al, 6
0042d0d5  720e                     jb 0x42d0e5
0042d0d7  3c07                     cmp al, 7
0042d0d9  76c5                     jbe 0x42d0a0
0042d0db  3c09                     cmp al, 9
0042d0dd  76c1                     jbe 0x42d0a0
0042d0df  3c0a                     cmp al, 0xa
0042d0e1  74b6                     je 0x42d099
0042d0e3  eb0a                     jmp 0x42d0ef
0042d0e5  3c03                     cmp al, 3
0042d0e7  7206                     jb 0x42d0ef
0042d0e9  3c04                     cmp al, 4
0042d0eb  76ac                     jbe 0x42d099
0042d0ed  b004                     mov al, 4
0042d0ef  0fbed0                   movsx edx, al
0042d0f2  31c0                     xor eax, eax
0042d0f4  a041805000               mov al, byte ptr [0x508041]
0042d0f9  e8bdb10300               call 0x4682bb ; -> MenuInit
0042d0fe  6a1b                     push 0x1b
0042d100  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d107  98                       cwde
0042d108  85c0                     test eax, eax
0042d10a  7cf2                     jl 0x42d0fe
0042d10c  e89bcb0400               call 0x479cac ; -> MouseZone
0042d111  66a3ac995000             mov word ptr [0x5099ac], ax
0042d117  6685c0                   test ax, ax
0042d11a  7568                     jne 0x42d184
0042d11c  803dae99500000           cmp byte ptr [0x5099ae], 0
0042d123  7427                     je 0x42d14c
0042d125  803daf99500000           cmp byte ptr [0x5099af], 0
0042d12c  741e                     je 0x42d14c
0042d12e  e84ac20300               call 0x46937d ; -> MenuGetItemSelect
0042d133  31db                     xor ebx, ebx
0042d135  31d2                     xor edx, edx
0042d137  6689c3                   mov bx, ax
0042d13a  31c0                     xor eax, eax
0042d13c  8a15782f4e00             mov dl, byte ptr [0x4e2f78]
0042d142  a041805000               mov al, byte ptr [0x508041]
0042d147  e898f2ffff               call 0x42c3e4 ; -> MenuNewSelect
0042d14c  80bc240401000010         cmp byte ptr [esp + 0x104], 0x10
0042d154  0f8588030000             jne 0x42d4e2
0042d15a  a030074e00               mov al, byte ptr [0x4e0730]
0042d15f  84c0                     test al, al
0042d161  0f847b030000             je 0x42d4e2
0042d167  8a25782f4e00             mov ah, byte ptr [0x4e2f78]
0042d16d  80fc10                   cmp ah, 0x10
0042d170  0f8468010000             je 0x42d2de
0042d176  80fc12                   cmp ah, 0x12
0042d179  0f845f010000             je 0x42d2de
0042d17f  e95e030000               jmp 0x42d4e2
0042d184  a0ac995000               mov al, byte ptr [0x5099ac]
0042d189  fec8                     dec al
0042d18b  25ff000000               and eax, 0xff
0042d190  e8dfc10300               call 0x469374 ; -> MenuSetSelectItem
0042d195  eb85                     jmp 0x42d11c
0042d197  803dae99500000           cmp byte ptr [0x5099ae], 0
0042d19e  7409                     je 0x42d1a9
0042d1a0  803daf99500000           cmp byte ptr [0x5099af], 0
0042d1a7  7512                     jne 0x42d1bb
0042d1a9  6a1b                     push 0x1b
0042d1ab  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d1b2  98                       cwde
0042d1b3  85c0                     test eax, eax
0042d1b5  0f8d27030000             jge 0x42d4e2
0042d1bb  6a1b                     push 0x1b
0042d1bd  2eff1590325200           call dword ptr cs:[0x523290] ; -> USER32.dll!GetAsyncKeyState
0042d1c4  98                       cwde
0042d1c5  85c0                     test eax, eax
0042d1c7  7cf2                     jl 0x42d1bb
0042d1c9  c605782f4e0012           mov byte ptr [0x4e2f78], 0x12
0042d1d0  e8b3ae0200               call 0x458088 ; -> EvenementEnd
0042d1d5  e908030000               jmp 0x42d4e2
0042d1da  e805460400               call 0x4717e4 ; -> MouseInit
0042d1df  b201                     mov dl, 1
0042d1e1  30c0                     xor al, al
0042d1e3  30db                     xor bl, bl
0042d1e5  a2ae995000               mov byte ptr [0x5099ae], al
0042d1ea  a2af995000               mov byte ptr [0x5099af], al
0042d1ef  e84428feff               call 0x40fa38 ; -> InitCache
0042d1f4  e8d7d90200               call 0x45abd0 ; -> InitGouttes
0042d1f9  88152c6d4900             mov byte ptr [0x496d2c], dl
0042d1ff  881585724900             mov byte ptr [0x497285], dl
0042d205  881dd86f4900             mov byte ptr [0x496fd8], bl
0042d20b  31d2                     xor edx, edx
0042d20d  8a3d782f4e00             mov bh, byte ptr [0x4e2f78]
0042d213  89151c064e00             mov dword ptr [0x4e061c], edx
0042d219  84ff                     test bh, bh
0042d21b  751e                     jne 0x42d23b
0042d21d  a030074e00               mov al, byte ptr [0x4e0730]
0042d222  84c0                     test al, al
0042d224  7509                     jne 0x42d22f
0042d226  31c0                     xor eax, eax
0042d228  e8a2f00300               call 0x46c2cf ; -> MissionLoad
0042d22d  eb50                     jmp 0x42d27f
0042d22f  b8cc3a4e00               mov eax, 0x4e3acc
0042d234  e8aaf30300               call 0x46c5e3 ; -> MissionLoadName
0042d239  eb44                     jmp 0x42d27f
0042d23b  80ff0f                   cmp bh, 0xf
0042d23e  753f                     jne 0x42d27f
0042d240  6a01                     push 1
0042d242  2eff15d0325200           call dword ptr cs:[0x5232d0] ; -> USER32.dll!ShowCursor
0042d249  e87a360100               call 0x4408c8 ; -> OpenNewFile
0042d24e  84c0                     test al, al
0042d250  7524                     jne 0x42d276
0042d252  e8b1780400               call 0x474b08 ; -> RestoreAll
0042d257  31c0                     xor eax, eax
0042d259  ba02000000               mov edx, 2
0042d25e  a041805000               mov al, byte ptr [0x508041]
0042d263  e853b00300               call 0x4682bb ; -> MenuInit
0042d268  6a00                     push 0
0042d26a  2eff15d0325200           call dword ptr cs:[0x5232d0] ; -> USER32.dll!ShowCursor
0042d271  e974020000               jmp 0x42d4ea
0042d276  6a00                     push 0
0042d278  2eff15d0325200           call dword ptr cs:[0x5232d0] ; -> USER32.dll!ShowCursor
0042d27f  e884780400               call 0x474b08 ; -> RestoreAll
0042d284  66a126875000             mov ax, word ptr [0x508726]
0042d28a  c1e005                   shl eax, 5
0042d28d  31c9                     xor ecx, ecx
0042d28f  48                       dec eax
0042d290  6689c1                   mov cx, ax
0042d293  66a124875000             mov ax, word ptr [0x508724]
0042d299  c1e005                   shl eax, 5
0042d29c  31db                     xor ebx, ebx
0042d29e  48                       dec eax
0042d29f  31d2                     xor edx, edx
0042d2a1  6689c3                   mov bx, ax
0042d2a4  31c0                     xor eax, eax
0042d2a6  e86e22feff               call 0x40f519 ; -> SetClipping
0042d2ab  ba12000000               mov edx, 0x12
0042d2b0  b901000000               mov ecx, 1
0042d2b5  31c0                     xor eax, eax
0042d2b7  31db                     xor ebx, ebx
0042d2b9  a041805000               mov al, byte ptr [0x508041]
0042d2be  891d7c8f5000             mov dword ptr [0x508f7c], ebx
0042d2c4  891d808f5000             mov dword ptr [0x508f80], ebx
0042d2ca  891d848f5000             mov dword ptr [0x508f84], ebx
0042d2d0  e8e6af0300               call 0x4682bb ; -> MenuInit
0042d2d5  89c8                     mov eax, ecx
0042d2d7  31d2                     xor edx, edx
0042d2d9  e852450400               call 0x471830 ; -> InitGameZone
0042d2de  e845030400               call 0x46d628 ; -> PlayerAttaqueReset
0042d2e3  e8ceae0200               call 0x4581b6 ; -> EvenementEnCours
0042d2e8  84c0                     test al, al
0042d2ea  0f85fa010000             jne 0x42d4ea
0042d2f0  803d282f4e0000           cmp byte ptr [0x4e2f28], 0
0042d2f7  7534                     jne 0x42d32d
0042d2f9  8a1d181d4e00             mov bl, byte ptr [0x4e1d18]
0042d2ff  31d2                     xor edx, edx
0042d301  88da                     mov dl, bl
0042d303  8a92181c4e00             mov dl, byte ptr [edx + 0x4e1c18]
0042d309  81e2ff000000             and edx, 0xff
0042d30f  b902000000               mov ecx, 2
0042d314  89d0                     mov eax, edx
0042d316  c1fa1f                   sar edx, 0x1f
0042d319  f7f9                     idiv ecx
0042d31b  8d040a                   lea eax, [edx + ecx]
0042d31e  fec3                     inc bl
0042d320  31d2                     xor edx, edx
0042d322  881d181d4e00             mov byte ptr [0x4e1d18], bl
0042d328  e85fa70300               call 0x467a8c ; -> MCICD_Play
0042d32d  30c9                     xor cl, cl
0042d32f  eb59                     jmp 0x42d38a
0042d331  3a0d41805000             cmp cl, byte ptr [0x508041]
0042d337  7510                     jne 0x42d349
0042d339  89d8                     mov eax, ebx
0042d33b  e838bfffff               call 0x429278 ; -> InputGame
0042d340  89d8                     mov eax, ebx
0042d342  e858190300               call 0x45ec9f ; -> InputSend
0042d347  eb3f                     jmp 0x42d388
0042d349  89d8                     mov eax, ebx
0042d34b  e82c170300               call 0x45ea7c ; -> InputReceive
0042d350  eb36                     jmp 0x42d388
0042d352  31d2                     xor edx, edx
0042d354  e8c1ed0300               call 0x46c11a ; -> MissionGetNum
0042d359  88c2                     mov dl, al
0042d35b  89d8                     mov eax, ebx
0042d35d  e888280500               call 0x47fbea ; -> CalculNextReflect
0042d362  3a0d41805000             cmp cl, byte ptr [0x508041]
0042d368  751e                     jne 0x42d388
0042d36a  89d8                     mov eax, ebx
0042d36c  e807bfffff               call 0x429278 ; -> InputGame
0042d371  eb15                     jmp 0x42d388
0042d373  31db                     xor ebx, ebx
0042d375  88cb                     mov bl, cl
0042d377  89d8                     mov eax, ebx
0042d379  e899040400               call 0x46d817 ; -> PlayerGetType
0042d37e  3c01                     cmp al, 1
0042d380  7206                     jb 0x42d388
0042d382  76ad                     jbe 0x42d331
0042d384  3c02                     cmp al, 2
0042d386  74ca                     je 0x42d352
0042d388  fec1                     inc cl
0042d38a  31c0                     xor eax, eax
0042d38c  88c8                     mov al, cl
0042d38e  83f804                   cmp eax, 4
0042d391  7f0f                     jg 0x42d3a2
0042d393  8a1530074e00             mov dl, byte ptr [0x4e0730]
0042d399  84d2                     test dl, dl
0042d39b  74d6                     je 0x42d373
0042d39d  83f804                   cmp eax, 4
0042d3a0  75d1                     jne 0x42d373
0042d3a2  a041805000               mov al, byte ptr [0x508041]
0042d3a7  30db                     xor bl, bl
0042d3a9  a280244e00               mov byte ptr [0x4e2480], al
0042d3ae  eb07                     jmp 0x42d3b7
0042d3b0  e80b1a0300               call 0x45edc0 ; -> ProcessInputGame
0042d3b5  fec3                     inc bl
0042d3b7  31c0                     xor eax, eax
0042d3b9  88d8                     mov al, bl
0042d3bb  83f804                   cmp eax, 4
0042d3be  7cf0                     jl 0x42d3b0
0042d3c0  8a25782f4e00             mov ah, byte ptr [0x4e2f78]
0042d3c6  80fc12                   cmp ah, 0x12
0042d3c9  7416                     je 0x42d3e1
0042d3cb  80fc10                   cmp ah, 0x10
0042d3ce  0f850e010000             jne 0x42d4e2
0042d3d4  a030074e00               mov al, byte ptr [0x4e0730]
0042d3d9  84c0                     test al, al
0042d3db  0f8401010000             je 0x42d4e2
0042d3e1  e8e8c90300               call 0x469dce ; -> MessageBoxCalcul
0042d3e6  e82afc0200               call 0x45d015 ; -> GameNextFrame
0042d3eb  e854150300               call 0x45e944 ; -> CalculIconeAction
0042d3f0  e81a280400               call 0x46fc0f ; -> ProjectileCalcul
0042d3f5  e8bb990200               call 0x456db5 ; -> CalculEnginNextEtape
0042d3fa  e8c8adffff               call 0x4281c7 ; -> CalculBatimentNextEtape
0042d3ff  e8583e0400               call 0x47125c ; -> RechercheCalcul
0042d404  e832060400               call 0x46da3b ; -> PlayerInitAllianceCompteur
0042d409  e81a7f0400               call 0x475328 ; -> SetUpdateChamp
0042d40e  e8f3b30400               call 0x478806 ; -> UpdateChamp
0042d413  e800a30300               call 0x467718 ; -> CalculMatiere
0042d418  31c0                     xor eax, eax
0042d41a  a041805000               mov al, byte ptr [0x508041]
0042d41f  e8ad990300               call 0x466dd1 ; -> CalculCompteurMarche
0042d424  31c0                     xor eax, eax
0042d426  a041805000               mov al, byte ptr [0x508041]
0042d42b  31d2                     xor edx, edx
0042d42d  e8699a0300               call 0x466e9b ; -> CalculCompteurProposition
0042d432  31c0                     xor eax, eax
0042d434  668b1522875000           mov dx, word ptr [0x508722]
0042d43b  66a120875000             mov ax, word ptr [0x508720]
0042d441  e8baa20400               call 0x477700 ; -> NextAnimTerrain
0042d446  a030074e00               mov al, byte ptr [0x4e0730]
0042d44b  84c0                     test al, al
0042d44d  7407                     je 0x42d456
0042d44f  e8a6a00400               call 0x4774fa ; -> NextAnimVegetFullMap
0042d454  eb16                     jmp 0x42d46c
0042d456  31d2                     xor edx, edx
0042d458  31c0                     xor eax, eax
0042d45a  668b1522875000           mov dx, word ptr [0x508722]
0042d461  66a120875000             mov ax, word ptr [0x508720]
0042d467  e8809e0400               call 0x4772ec ; -> NextAnimVeget
0042d46c  e8b8010400               call 0x46d629 ; -> PlayerAttaqueCalculSympa
0042d471  a030074e00               mov al, byte ptr [0x4e0730]
0042d476  84c0                     test al, al
0042d478  7568                     jne 0x42d4e2
0042d47a  31c0                     xor eax, eax
0042d47c  a041805000               mov al, byte ptr [0x508041]
0042d481  e880b10200               call 0x458606 ; -> TestFinDeMission
0042d486  a2a0054e00               mov byte ptr [0x4e05a0], al
0042d48b  84c0                     test al, al
0042d48d  7453                     je 0x42d4e2
0042d48f  e886ec0300               call 0x46c11a ; -> MissionGetNum
0042d494  25ffff0000               and eax, 0xffff
0042d499  83f806                   cmp eax, 6
0042d49c  7518                     jne 0x42d4b6
0042d49e  833d1c064e0000           cmp dword ptr [0x4e061c], 0
0042d4a5  750f                     jne 0x42d4b6
0042d4a7  baf4010000               mov edx, 0x1f4
0042d4ac  b80a000000               mov eax, 0xa
0042d4b1  e895c40300               call 0x46994b ; -> MessageBoxSet
0042d4b6  8b0d1c064e00             mov ecx, dword ptr [0x4e061c]
0042d4bc  41                       inc ecx
0042d4bd  890d1c064e00             mov dword ptr [0x4e061c], ecx
0042d4c3  83f964                   cmp ecx, 0x64
0042d4c6  7c1a                     jl 0x42d4e2
0042d4c8  e8f8d50500               call 0x48aac5 ; -> PlaySnd_StopAllSound
0042d4cd  31c0                     xor eax, eax
0042d4cf  ba13000000               mov edx, 0x13
0042d4d4  e953f4ffff               jmp 0x42c92c
0042d4d9  6a00                     push 0
0042d4db  2eff15bc325200           call dword ptr cs:[0x5232bc] ; -> USER32.dll!PostQuitMessage
0042d4e2  30f6                     xor dh, dh
0042d4e4  8835b0995000             mov byte ptr [0x5099b0], dh
0042d4ea  81c40c010000             add esp, 0x10c
0042d4f0  e91feeffff               jmp 0x42c314
; 0x0042d4f5..0x0042d4f8 not reached by any static path (padding or data):
0042d4f5  .byte 000000

; shared Watcom tail reached from CalculGame; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0042c314..0x0042c31b (end exclusive); labels are original SBL names
0042c314  5d                       pop ebp
0042c315  5f                       pop edi
0042c316  5e                       pop esi
0042c317  5a                       pop edx
0042c318  59                       pop ecx
0042c319  5b                       pop ebx
0042c31a  c3                       ret
