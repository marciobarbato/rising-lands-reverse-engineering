; Intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Exported by pesquisas-paralelas/audio/extrair_som.py; symbols from INSTALHD/RISING.SBL
; HndSound_LoadDataInfo (identity)
0048a0f4  56                       push esi
0048a0f5  57                       push edi
0048a0f6  89c6                     mov esi, eax
0048a0f8  89d7                     mov edi, edx
0048a0fa  89da                     mov edx, ebx
0048a0fc  89f8                     mov eax, edi
0048a0fe  e88d120000               call 0x48b390
0048a103  894618                   mov dword ptr [esi + 0x18], eax
0048a106  85c0                     test eax, eax
0048a108  743b                     je 0x48a145
0048a10a  893e                     mov dword ptr [esi], edi
0048a10c  89da                     mov edx, ebx
0048a10e  8b4618                   mov eax, dword ptr [esi + 0x18]
0048a111  895e04                   mov dword ptr [esi + 4], ebx
0048a114  e89a120000               call 0x48b3b3
0048a119  89461c                   mov dword ptr [esi + 0x1c], eax
0048a11c  8b4618                   mov eax, dword ptr [esi + 0x18]
0048a11f  894e0c                   mov dword ptr [esi + 0xc], ecx
0048a122  668b4004                 mov ax, word ptr [eax + 4]
0048a126  25ffff0000               and eax, 0xffff
0048a12b  3d00010000               cmp eax, 0x100
0048a130  7404                     je 0x48a136
0048a132  8b44240c                 mov eax, dword ptr [esp + 0xc]
0048a136  894610                   mov dword ptr [esi + 0x10], eax
0048a139  b801000000               mov eax, 1
0048a13e  c7461400000000           mov dword ptr [esi + 0x14], 0
0048a145  5f                       pop edi
0048a146  5e                       pop esi
0048a147  c20400                   ret 4
; PlaySnd_CreateSoundPath (identity)
0048a834  52                       push edx
0048a835  bae8030000               mov edx, 0x3e8
0048a83a  31c0                     xor eax, eax
0048a83c  e8401c0000               call 0x48c481
0048a841  89c2                     mov edx, eax
0048a843  803800                   cmp byte ptr [eax], 0
0048a846  7403                     je 0x48a84b
0048a848  40                       inc eax
0048a849  ebf8                     jmp 0x48a843
0048a84b  8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a84f  750d                     jne 0x48a85e
0048a851  687c534900               push 0x49537c
0048a856  52                       push edx
0048a857  6882534900               push 0x495382
0048a85c  eb0b                     jmp 0x48a869
0048a85e  6887534900               push 0x495387
0048a863  52                       push edx
0048a864  688d534900               push 0x49538d
0048a869  681c205200               push 0x52201c
0048a86e  e848270000               call 0x48cfbb
0048a873  83c410                   add esp, 0x10
0048a876  89d0                     mov eax, edx
0048a878  e8772f0000               call 0x48d7f4
0048a87d  5a                       pop edx
0048a87e  c3                       ret
; SoundFile (identity)
0048a87f  50                       push eax
0048a880  681c205200               push 0x52201c
0048a885  6893534900               push 0x495393
0048a88a  52                       push edx
0048a88b  e82b270000               call 0x48cfbb
0048a890  83c410                   add esp, 0x10
0048a893  c3                       ret
; PlaySnd_MakeID (identity)
0048a894  c1e010                   shl eax, 0x10
0048a897  c1e208                   shl edx, 8
0048a89a  09d0                     or eax, edx
0048a89c  09d8                     or eax, ebx
0048a89e  c3                       ret
; PlaySnd_InitSoundLib (identity)
0048a89f  51                       push ecx
0048a8a0  52                       push edx
0048a8a1  56                       push esi
0048a8a2  81ec00010000             sub esp, 0x100
0048a8a8  803dc41f520000           cmp byte ptr [0x521fc4], 0
0048a8af  7407                     je 0x48a8b8
0048a8b1  30c0                     xor al, al
0048a8b3  e942010000               jmp 0x48a9fa
0048a8b8  a1e8274e00               mov eax, dword ptr [0x4e27e8]
0048a8bd  e835150000               call 0x48bdf7
0048a8c2  85c0                     test eax, eax
0048a8c4  74eb                     je 0x48a8b1
0048a8c6  e8a1180000               call 0x48c16c
0048a8cb  85c0                     test eax, eax
0048a8cd  74e2                     je 0x48a8b1
0048a8cf  bae8030000               mov edx, 0x3e8
0048a8d4  31c0                     xor eax, eax
0048a8d6  e8a61b0000               call 0x48c481
0048a8db  89c2                     mov edx, eax
0048a8dd  803800                   cmp byte ptr [eax], 0
0048a8e0  7403                     je 0x48a8e5
0048a8e2  40                       inc eax
0048a8e3  ebf8                     jmp 0x48a8dd
0048a8e5  8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a8e9  750d                     jne 0x48a8f8
0048a8eb  687c534900               push 0x49537c
0048a8f0  52                       push edx
0048a8f1  6882534900               push 0x495382
0048a8f6  eb0b                     jmp 0x48a903
0048a8f8  6887534900               push 0x495387
0048a8fd  52                       push edx
0048a8fe  688d534900               push 0x49538d
0048a903  681c205200               push 0x52201c
0048a908  e8ae260000               call 0x48cfbb
0048a90d  83c410                   add esp, 0x10
0048a910  89d0                     mov eax, edx
0048a912  e8dd2e0000               call 0x48d7f4
0048a917  6899534900               push 0x495399
0048a91c  681c205200               push 0x52201c
0048a921  31d2                     xor edx, edx
0048a923  6893534900               push 0x495393
0048a928  8d44240c                 lea eax, [esp + 0xc]
0048a92c  8915c81f5200             mov dword ptr [0x521fc8], edx
0048a932  50                       push eax
0048a933  8915e41f5200             mov dword ptr [0x521fe4], edx
0048a939  891500205200             mov dword ptr [0x522000], edx
0048a93f  e877260000               call 0x48cfbb
0048a944  83c410                   add esp, 0x10
0048a947  bac81f5200               mov edx, 0x521fc8
0048a94c  89e0                     mov eax, esp
0048a94e  e8530c0000               call 0x48b5a6
0048a953  85c0                     test eax, eax
0048a955  0f8456ffffff             je 0x48a8b1
0048a95b  689b534900               push 0x49539b
0048a960  681c205200               push 0x52201c
0048a965  6893534900               push 0x495393
0048a96a  8d44240c                 lea eax, [esp + 0xc]
0048a96e  50                       push eax
0048a96f  e847260000               call 0x48cfbb
0048a974  83c410                   add esp, 0x10
0048a977  bae41f5200               mov edx, 0x521fe4
0048a97c  89e0                     mov eax, esp
0048a97e  e8230c0000               call 0x48b5a6
0048a983  85c0                     test eax, eax
0048a985  0f8426ffffff             je 0x48a8b1
0048a98b  689d534900               push 0x49539d
0048a990  681c205200               push 0x52201c
0048a995  6893534900               push 0x495393
0048a99a  8d44240c                 lea eax, [esp + 0xc]
0048a99e  50                       push eax
0048a99f  e817260000               call 0x48cfbb
0048a9a4  83c410                   add esp, 0x10
0048a9a7  ba00205200               mov edx, 0x522000
0048a9ac  89e0                     mov eax, esp
0048a9ae  e8f30b0000               call 0x48b5a6
0048a9b3  85c0                     test eax, eax
0048a9b5  0f84f6feffff             je 0x48a8b1
0048a9bb  e879f5ffff               call 0x489f39
0048a9c0  85c0                     test eax, eax
0048a9c2  0f84e9feffff             je 0x48a8b1
0048a9c8  31c0                     xor eax, eax
0048a9ca  83c02c                   add eax, 0x2c
0048a9cd  30c9                     xor cl, cl
0048a9cf  31f6                     xor esi, esi
0048a9d1  888858135200             mov byte ptr [eax + 0x521358], cl
0048a9d7  89b070135200             mov dword ptr [eax + 0x521370], esi
0048a9dd  89b078135200             mov dword ptr [eax + 0x521378], esi
0048a9e3  89b064135200             mov dword ptr [eax + 0x521364], esi
0048a9e9  3d080c0000               cmp eax, 0xc08
0048a9ee  75da                     jne 0x48a9ca
0048a9f0  b501                     mov ch, 1
0048a9f2  882dc41f5200             mov byte ptr [0x521fc4], ch
0048a9f8  88e8                     mov al, ch
0048a9fa  81c400010000             add esp, 0x100
0048aa00  5e                       pop esi
0048aa01  5a                       pop edx
0048aa02  59                       pop ecx
0048aa03  c3                       ret
; PlaySnd_PostSound (identity)
0048aa79  56                       push esi
0048aa7a  89c6                     mov esi, eax
0048aa7c  89d0                     mov eax, edx
0048aa7e  8b542408                 mov edx, dword ptr [esp + 8]
0048aa82  83fe42                   cmp esi, 0x42
0048aa85  7230                     jb 0x48aab7
0048aa87  761e                     jbe 0x48aaa7
0048aa89  83fe50                   cmp esi, 0x50
0048aa8c  7421                     je 0x48aaaf
0048aa8e  5e                       pop esi
0048aa8f  c20400                   ret 4
0048aa92  52                       push edx
0048aa93  bac81f5200               mov edx, 0x521fc8
0048aa98  81e1ff000000             and ecx, 0xff
0048aa9e  e875f7ffff               call 0x48a218
0048aaa3  5e                       pop esi
0048aaa4  c20400                   ret 4
0048aaa7  52                       push edx
0048aaa8  bae41f5200               mov edx, 0x521fe4
0048aaad  ebe9                     jmp 0x48aa98
0048aaaf  52                       push edx
0048aab0  ba00205200               mov edx, 0x522000
0048aab5  ebe1                     jmp 0x48aa98
0048aab7  83fe41                   cmp esi, 0x41
0048aaba  74d6                     je 0x48aa92
0048aabc  5e                       pop esi
0048aabd  c20400                   ret 4
; PSB_CreateMySurfaceWithSound (buffer)
0048aad4  53                       push ebx
0048aad5  51                       push ecx
0048aad6  56                       push esi
0048aad7  57                       push edi
0048aad8  55                       push ebp
0048aad9  89c6                     mov esi, eax
0048aadb  89d7                     mov edi, edx
0048aadd  8b5210                   mov edx, dword ptr [edx + 0x10]
0048aae0  31ed                     xor ebp, ebp
0048aae2  85d2                     test edx, edx
0048aae4  0f850a000000             jne 0x48aaf4
0048aaea  8b4708                   mov eax, dword ptr [edi + 8]
0048aaed  31db                     xor ebx, ebx
0048aaef  e86a150000               call 0x48c05e
0048aaf4  8a460c                   mov al, byte ptr [esi + 0xc]
0048aaf7  84c0                     test al, al
0048aaf9  760c                     jbe 0x48ab07
0048aafb  3c04                     cmp al, 4
0048aafd  745a                     je 0x48ab59
0048aaff  89e8                     mov eax, ebp
0048ab01  5d                       pop ebp
0048ab02  5f                       pop edi
0048ab03  5e                       pop esi
0048ab04  59                       pop ecx
0048ab05  5b                       pop ebx
0048ab06  c3                       ret
0048ab07  8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab0a  31db                     xor ebx, ebx
0048ab0c  31d2                     xor edx, edx
0048ab0e  31c0                     xor eax, eax
0048ab10  8a5e09                   mov bl, byte ptr [esi + 9]
0048ab13  668b560a                 mov dx, word ptr [esi + 0xa]
0048ab17  8a4608                   mov al, byte ptr [esi + 8]
0048ab1a  e8920c0000               call 0x48b7b1
0048ab1f  89c1                     mov ecx, eax
0048ab21  89c5                     mov ebp, eax
0048ab23  85c0                     test eax, eax
0048ab25  74da                     je 0x48ab01
0048ab27  837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab2b  7513                     jne 0x48ab40
0048ab2d  8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab30  8b1e                     mov ebx, dword ptr [esi]
0048ab32  89c8                     mov eax, ecx
0048ab34  01da                     add edx, ebx
0048ab36  8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab39  e86a160000               call 0x48c1a8
0048ab3e  ebbf                     jmp 0x48aaff
0048ab40  8b16                     mov edx, dword ptr [esi]
0048ab42  8b4708                   mov eax, dword ptr [edi + 8]
0048ab45  e8ed150000               call 0x48c137
0048ab4a  89c8                     mov eax, ecx
0048ab4c  8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab4f  8b5708                   mov edx, dword ptr [edi + 8]
0048ab52  e819150000               call 0x48c070
0048ab57  eba6                     jmp 0x48aaff
0048ab59  8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab5c  31db                     xor ebx, ebx
0048ab5e  31d2                     xor edx, edx
0048ab60  31c0                     xor eax, eax
0048ab62  c1e102                   shl ecx, 2
0048ab65  8a5e09                   mov bl, byte ptr [esi + 9]
0048ab68  668b560a                 mov dx, word ptr [esi + 0xa]
0048ab6c  8a4608                   mov al, byte ptr [esi + 8]
0048ab6f  e83d0c0000               call 0x48b7b1
0048ab74  89c5                     mov ebp, eax
0048ab76  85c0                     test eax, eax
0048ab78  7487                     je 0x48ab01
0048ab7a  837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab7e  7507                     jne 0x48ab87
0048ab80  8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab83  0316                     add edx, dword ptr [esi]
0048ab85  eb17                     jmp 0x48ab9e
0048ab87  8b16                     mov edx, dword ptr [esi]
0048ab89  8b4708                   mov eax, dword ptr [edi + 8]
0048ab8c  e8a6150000               call 0x48c137
0048ab91  8b5604                   mov edx, dword ptr [esi + 4]
0048ab94  8b4708                   mov eax, dword ptr [edi + 8]
0048ab97  e8a5150000               call 0x48c141
0048ab9c  89c2                     mov edx, eax
0048ab9e  31c0                     xor eax, eax
0048aba0  8b5e04                   mov ebx, dword ptr [esi + 4]
0048aba3  8a4608                   mov al, byte ptr [esi + 8]
0048aba6  31c9                     xor ecx, ecx
0048aba8  50                       push eax
0048aba9  668b4e0e                 mov cx, word ptr [esi + 0xe]
0048abad  89e8                     mov eax, ebp
0048abaf  e808150000               call 0x48c0bc
0048abb4  e946ffffff               jmp 0x48aaff
; UseBank_FindIdInBanque (bank)
0048b390  53                       push ebx
0048b391  51                       push ecx
0048b392  89c1                     mov ecx, eax
0048b394  89d3                     mov ebx, edx
0048b396  8b420c                   mov eax, dword ptr [edx + 0xc]
0048b399  31d2                     xor edx, edx
0048b39b  eb04                     jmp 0x48b3a1
0048b39d  83c00c                   add eax, 0xc
0048b3a0  42                       inc edx
0048b3a1  663b5304                 cmp dx, word ptr [ebx + 4]
0048b3a5  7307                     jae 0x48b3ae
0048b3a7  3b08                     cmp ecx, dword ptr [eax]
0048b3a9  75f2                     jne 0x48b39d
0048b3ab  59                       pop ecx
0048b3ac  5b                       pop ebx
0048b3ad  c3                       ret
0048b3ae  31c0                     xor eax, eax
0048b3b0  59                       pop ecx
0048b3b1  5b                       pop ebx
0048b3b2  c3                       ret
; UseBank_GetDataHeader (bank)
0048b3b3  53                       push ebx
0048b3b4  51                       push ecx
0048b3b5  56                       push esi
0048b3b6  ff05bc215200             inc dword ptr [0x5221bc]
0048b3bc  31db                     xor ebx, ebx
0048b3be  668b5806                 mov bx, word ptr [eax + 6]
0048b3c2  4b                       dec ebx
0048b3c3  85db                     test ebx, ebx
0048b3c5  7e17                     jle 0x48b3de
0048b3c7  8b35bc215200             mov esi, dword ptr [0x5221bc]
0048b3cd  8b4808                   mov ecx, dword ptr [eax + 8]
0048b3d0  89d8                     mov eax, ebx
0048b3d2  8b520c                   mov edx, dword ptr [edx + 0xc]
0048b3d5  21f0                     and eax, esi
0048b3d7  01ca                     add edx, ecx
0048b3d9  c1e004                   shl eax, 4
0048b3dc  eb06                     jmp 0x48b3e4
0048b3de  8b520c                   mov edx, dword ptr [edx + 0xc]
0048b3e1  8b4008                   mov eax, dword ptr [eax + 8]
0048b3e4  01d0                     add eax, edx
0048b3e6  5e                       pop esi
0048b3e7  59                       pop ecx
0048b3e8  5b                       pop ebx
0048b3e9  c3                       ret
; BanqSon_OpenDataFile (bank)
0048b3ec  51                       push ecx
0048b3ed  52                       push edx
0048b3ee  56                       push esi
0048b3ef  57                       push edi
0048b3f0  bfc0215200               mov edi, 0x5221c0
0048b3f5  89c6                     mov esi, eax
0048b3f7  57                       push edi
0048b3f8  8a06                     mov al, byte ptr [esi]
0048b3fa  8807                     mov byte ptr [edi], al
0048b3fc  3c00                     cmp al, 0
0048b3fe  7410                     je 0x48b410
0048b400  8a4601                   mov al, byte ptr [esi + 1]
0048b403  83c602                   add esi, 2
0048b406  884701                   mov byte ptr [edi + 1], al
0048b409  83c702                   add edi, 2
0048b40c  3c00                     cmp al, 0
0048b40e  75e8                     jne 0x48b3f8
0048b410  5f                       pop edi
0048b411  bea0534900               mov esi, 0x4953a0
0048b416  31d2                     xor edx, edx
0048b418  57                       push edi
0048b419  2bc9                     sub ecx, ecx
0048b41b  49                       dec ecx
0048b41c  b000                     mov al, 0
0048b41e  f2ae                     repne scasb al, byte ptr es:[edi]
0048b420  4f                       dec edi
0048b421  8a06                     mov al, byte ptr [esi]
0048b423  8807                     mov byte ptr [edi], al
0048b425  3c00                     cmp al, 0
0048b427  7410                     je 0x48b439
0048b429  8a4601                   mov al, byte ptr [esi + 1]
0048b42c  83c602                   add esi, 2
0048b42f  884701                   mov byte ptr [edi + 1], al
0048b432  83c702                   add edi, 2
0048b435  3c00                     cmp al, 0
0048b437  75e8                     jne 0x48b421
0048b439  5f                       pop edi
0048b43a  89f8                     mov eax, edi
0048b43c  e8d60b0000               call 0x48c017
0048b441  5f                       pop edi
0048b442  5e                       pop esi
0048b443  5a                       pop edx
0048b444  59                       pop ecx
0048b445  c3                       ret
; BanqSon_CloseDataFile (bank)
0048b446  8b4008                   mov eax, dword ptr [eax + 8]
0048b449  e9d80b0000               jmp 0x48c026
; BanqSon_ControleValiditeHeader (bank)
0048b44e  51                       push ecx
0048b44f  56                       push esi
0048b450  83ec10                   sub esp, 0x10
0048b453  89d6                     mov esi, edx
0048b455  89d9                     mov ecx, ebx
0048b457  bb10000000               mov ebx, 0x10
0048b45c  89e2                     mov edx, esp
0048b45e  e8db0b0000               call 0x48c03e
0048b463  813c2441424344           cmp dword ptr [esp], 0x44434241
0048b46a  740a                     je 0x48b476
0048b46c  c70600000000             mov dword ptr [esi], 0
0048b472  31c0                     xor eax, eax
0048b474  eb1a                     jmp 0x48b490
0048b476  8b442404                 mov eax, dword ptr [esp + 4]
0048b47a  8906                     mov dword ptr [esi], eax
0048b47c  8b44240c                 mov eax, dword ptr [esp + 0xc]
0048b480  66894104                 mov word ptr [ecx + 4], ax
0048b484  8b442408                 mov eax, dword ptr [esp + 8]
0048b488  894118                   mov dword ptr [ecx + 0x18], eax
0048b48b  b801000000               mov eax, 1
0048b490  83c410                   add esp, 0x10
0048b493  5e                       pop esi
0048b494  59                       pop ecx
0048b495  c3                       ret
; BanqSon_LoadHeader (bank)
0048b496  53                       push ebx
0048b497  51                       push ecx
0048b498  56                       push esi
0048b499  57                       push edi
0048b49a  55                       push ebp
0048b49b  83ec18                   sub esp, 0x18
0048b49e  89d5                     mov ebp, edx
0048b4a0  bfc0215200               mov edi, 0x5221c0
0048b4a5  89c6                     mov esi, eax
0048b4a7  57                       push edi
0048b4a8  8a06                     mov al, byte ptr [esi]
0048b4aa  8807                     mov byte ptr [edi], al
0048b4ac  3c00                     cmp al, 0
0048b4ae  7410                     je 0x48b4c0
0048b4b0  8a4601                   mov al, byte ptr [esi + 1]
0048b4b3  83c602                   add esi, 2
0048b4b6  884701                   mov byte ptr [edi + 1], al
0048b4b9  83c702                   add edi, 2
0048b4bc  3c00                     cmp al, 0
0048b4be  75e8                     jne 0x48b4a8
0048b4c0  5f                       pop edi
0048b4c1  bea5534900               mov esi, 0x4953a5
0048b4c6  31d2                     xor edx, edx
0048b4c8  57                       push edi
0048b4c9  2bc9                     sub ecx, ecx
0048b4cb  49                       dec ecx
0048b4cc  b000                     mov al, 0
0048b4ce  f2ae                     repne scasb al, byte ptr es:[edi]
0048b4d0  4f                       dec edi
0048b4d1  8a06                     mov al, byte ptr [esi]
0048b4d3  8807                     mov byte ptr [edi], al
0048b4d5  3c00                     cmp al, 0
0048b4d7  7410                     je 0x48b4e9
0048b4d9  8a4601                   mov al, byte ptr [esi + 1]
0048b4dc  83c602                   add esi, 2
0048b4df  884701                   mov byte ptr [edi + 1], al
0048b4e2  83c702                   add edi, 2
0048b4e5  3c00                     cmp al, 0
0048b4e7  75e8                     jne 0x48b4d1
0048b4e9  5f                       pop edi
0048b4ea  89f8                     mov eax, edi
0048b4ec  e8260b0000               call 0x48c017
0048b4f1  89c1                     mov ecx, eax
0048b4f3  83f8ff                   cmp eax, -1
0048b4f6  7446                     je 0x48b53e
0048b4f8  bb10000000               mov ebx, 0x10
0048b4fd  89e2                     mov edx, esp
0048b4ff  e83a0b0000               call 0x48c03e
0048b504  813c2441424344           cmp dword ptr [esp], 0x44434241
0048b50b  740a                     je 0x48b517
0048b50d  31db                     xor ebx, ebx
0048b50f  31c0                     xor eax, eax
0048b511  895c2414                 mov dword ptr [esp + 0x14], ebx
0048b515  eb1c                     jmp 0x48b533
0048b517  8b442404                 mov eax, dword ptr [esp + 4]
0048b51b  89442414                 mov dword ptr [esp + 0x14], eax
0048b51f  8b44240c                 mov eax, dword ptr [esp + 0xc]
0048b523  66894504                 mov word ptr [ebp + 4], ax
0048b527  8b442408                 mov eax, dword ptr [esp + 8]
0048b52b  894518                   mov dword ptr [ebp + 0x18], eax
0048b52e  b801000000               mov eax, 1
0048b533  85c0                     test eax, eax
0048b535  750b                     jne 0x48b542
0048b537  89c8                     mov eax, ecx
0048b539  e8e80a0000               call 0x48c026
0048b53e  31c0                     xor eax, eax
0048b540  eb4b                     jmp 0x48b58d
0048b542  baaa534900               mov edx, 0x4953aa
0048b547  8b442414                 mov eax, dword ptr [esp + 0x14]
0048b54b  e8b40c0000               call 0x48c204
0048b550  89442410                 mov dword ptr [esp + 0x10], eax
0048b554  85c0                     test eax, eax
0048b556  74df                     je 0x48b537
0048b558  8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0048b55c  89c2                     mov edx, eax
0048b55e  89c8                     mov eax, ecx
0048b560  e8d90a0000               call 0x48c03e
0048b565  3b442414                 cmp eax, dword ptr [esp + 0x14]
0048b569  7417                     je 0x48b582
0048b56b  89c8                     mov eax, ecx
0048b56d  bad6534900               mov edx, 0x4953d6
0048b572  e8af0a0000               call 0x48c026
0048b577  8d442410                 lea eax, [esp + 0x10]
0048b57b  e8ff0c0000               call 0x48c27f
0048b580  ebbc                     jmp 0x48b53e
0048b582  89c8                     mov eax, ecx
0048b584  e89d0a0000               call 0x48c026
0048b589  8b442410                 mov eax, dword ptr [esp + 0x10]
0048b58d  83c418                   add esp, 0x18
0048b590  5d                       pop ebp
0048b591  5f                       pop edi
0048b592  5e                       pop esi
0048b593  59                       pop ecx
0048b594  5b                       pop ebx
0048b595  c3                       ret
; BanqSon_FreeHeader (bank)
0048b596  52                       push edx
0048b597  ba05544900               mov edx, 0x495405
0048b59c  83c00c                   add eax, 0xc
0048b59f  e8db0c0000               call 0x48c27f
0048b5a4  5a                       pop edx
0048b5a5  c3                       ret
; BanqSon_Open (bank)
0048b5a6  53                       push ebx
0048b5a7  51                       push ecx
0048b5a8  56                       push esi
0048b5a9  57                       push edi
0048b5aa  89c6                     mov esi, eax
0048b5ac  89d3                     mov ebx, edx
0048b5ae  833a01                   cmp dword ptr [edx], 1
0048b5b1  7507                     jne 0x48b5ba
0048b5b3  31c0                     xor eax, eax
0048b5b5  5f                       pop edi
0048b5b6  5e                       pop esi
0048b5b7  59                       pop ecx
0048b5b8  5b                       pop ebx
0048b5b9  c3                       ret
0048b5ba  89da                     mov edx, ebx
0048b5bc  e8d5feffff               call 0x48b496
0048b5c1  89430c                   mov dword ptr [ebx + 0xc], eax
0048b5c4  85c0                     test eax, eax
0048b5c6  0f847f000000             je 0x48b64b
0048b5cc  bfc0215200               mov edi, 0x5221c0
0048b5d1  57                       push edi
0048b5d2  8a06                     mov al, byte ptr [esi]
0048b5d4  8807                     mov byte ptr [edi], al
0048b5d6  3c00                     cmp al, 0
0048b5d8  7410                     je 0x48b5ea
0048b5da  8a4601                   mov al, byte ptr [esi + 1]
0048b5dd  83c602                   add esi, 2
0048b5e0  884701                   mov byte ptr [edi + 1], al
0048b5e3  83c702                   add edi, 2
0048b5e6  3c00                     cmp al, 0
0048b5e8  75e8                     jne 0x48b5d2
0048b5ea  5f                       pop edi
0048b5eb  bea0534900               mov esi, 0x4953a0
0048b5f0  31d2                     xor edx, edx
0048b5f2  57                       push edi
0048b5f3  2bc9                     sub ecx, ecx
0048b5f5  49                       dec ecx
0048b5f6  b000                     mov al, 0
0048b5f8  f2ae                     repne scasb al, byte ptr es:[edi]
0048b5fa  4f                       dec edi
0048b5fb  8a06                     mov al, byte ptr [esi]
0048b5fd  8807                     mov byte ptr [edi], al
0048b5ff  3c00                     cmp al, 0
0048b601  7410                     je 0x48b613
0048b603  8a4601                   mov al, byte ptr [esi + 1]
0048b606  83c602                   add esi, 2
0048b609  884701                   mov byte ptr [edi + 1], al
0048b60c  83c702                   add edi, 2
0048b60f  3c00                     cmp al, 0
0048b611  75e8                     jne 0x48b5fb
0048b613  5f                       pop edi
0048b614  89f8                     mov eax, edi
0048b616  e8fc090000               call 0x48c017
0048b61b  894308                   mov dword ptr [ebx + 8], eax
0048b61e  83f8ff                   cmp eax, -1
0048b621  750f                     jne 0x48b632
0048b623  ba05544900               mov edx, 0x495405
0048b628  8d430c                   lea eax, [ebx + 0xc]
0048b62b  e84f0c0000               call 0x48c27f
0048b630  eb81                     jmp 0x48b5b3
0048b632  c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b639  c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b640  b801000000               mov eax, 1
0048b645  c70301000000             mov dword ptr [ebx], 1
0048b64b  5f                       pop edi
0048b64c  5e                       pop esi
0048b64d  59                       pop ecx
0048b64e  5b                       pop ebx
0048b64f  c3                       ret
; BanqSon_FreeDataInMemory (bank)
0048b650  53                       push ebx
0048b651  52                       push edx
0048b652  89c3                     mov ebx, eax
0048b654  833800                   cmp dword ptr [eax], 0
0048b657  7505                     jne 0x48b65e
0048b659  31c0                     xor eax, eax
0048b65b  5a                       pop edx
0048b65c  5b                       pop ebx
0048b65d  c3                       ret
0048b65e  83781000                 cmp dword ptr [eax + 0x10], 0
0048b662  74f5                     je 0x48b659
0048b664  ba18544900               mov edx, 0x495418
0048b669  83c014                   add eax, 0x14
0048b66c  e80e0c0000               call 0x48c27f
0048b671  c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b678  b801000000               mov eax, 1
0048b67d  c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b684  5a                       pop edx
0048b685  5b                       pop ebx
0048b686  c3                       ret
; BanqSon_Close (bank)
0048b687  53                       push ebx
0048b688  51                       push ecx
0048b689  52                       push edx
0048b68a  89c3                     mov ebx, eax
0048b68c  8b10                     mov edx, dword ptr [eax]
0048b68e  85d2                     test edx, edx
0048b690  7506                     jne 0x48b698
0048b692  31c0                     xor eax, eax
0048b694  5a                       pop edx
0048b695  59                       pop ecx
0048b696  5b                       pop ebx
0048b697  c3                       ret
0048b698  8b4810                   mov ecx, dword ptr [eax + 0x10]
0048b69b  83f901                   cmp ecx, 1
0048b69e  7523                     jne 0x48b6c3
0048b6a0  85d2                     test edx, edx
0048b6a2  741f                     je 0x48b6c3
0048b6a4  85c9                     test ecx, ecx
0048b6a6  741b                     je 0x48b6c3
0048b6a8  ba18544900               mov edx, 0x495418
0048b6ad  83c014                   add eax, 0x14
0048b6b0  e8ca0b0000               call 0x48c27f
0048b6b5  c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b6bc  c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b6c3  ba05544900               mov edx, 0x495405
0048b6c8  8d430c                   lea eax, [ebx + 0xc]
0048b6cb  e8af0b0000               call 0x48c27f
0048b6d0  8b4308                   mov eax, dword ptr [ebx + 8]
0048b6d3  e84e090000               call 0x48c026
0048b6d8  b801000000               mov eax, 1
0048b6dd  c70300000000             mov dword ptr [ebx], 0
0048b6e3  5a                       pop edx
0048b6e4  59                       pop ecx
0048b6e5  5b                       pop ebx
0048b6e6  c3                       ret
; BanqSon_LoadAllData (bank)
0048b6e7  53                       push ebx
0048b6e8  51                       push ecx
0048b6e9  52                       push edx
0048b6ea  56                       push esi
0048b6eb  83ec04                   sub esp, 4
0048b6ee  89c1                     mov ecx, eax
0048b6f0  ba52544900               mov edx, 0x495452
0048b6f5  8b4018                   mov eax, dword ptr [eax + 0x18]
0048b6f8  e8070b0000               call 0x48c204
0048b6fd  890424                   mov dword ptr [esp], eax
0048b700  85c0                     test eax, eax
0048b702  7427                     je 0x48b72b
0048b704  89c2                     mov edx, eax
0048b706  8b7108                   mov esi, dword ptr [ecx + 8]
0048b709  8b5918                   mov ebx, dword ptr [ecx + 0x18]
0048b70c  89f0                     mov eax, esi
0048b70e  e82b090000               call 0x48c03e
0048b713  3b4118                   cmp eax, dword ptr [ecx + 0x18]
0048b716  7410                     je 0x48b728
0048b718  ba85544900               mov edx, 0x495485
0048b71d  89e0                     mov eax, esp
0048b71f  e85b0b0000               call 0x48c27f
0048b724  31c0                     xor eax, eax
0048b726  eb03                     jmp 0x48b72b
0048b728  8b0424                   mov eax, dword ptr [esp]
0048b72b  83c404                   add esp, 4
0048b72e  5e                       pop esi
0048b72f  5a                       pop edx
0048b730  59                       pop ecx
0048b731  5b                       pop ebx
0048b732  c3                       ret
; BanqSon_LoadDataInMemory (bank)
0048b733  53                       push ebx
0048b734  51                       push ecx
0048b735  52                       push edx
0048b736  56                       push esi
0048b737  83ec04                   sub esp, 4
0048b73a  89c1                     mov ecx, eax
0048b73c  833800                   cmp dword ptr [eax], 0
0048b73f  7504                     jne 0x48b745
0048b741  31c0                     xor eax, eax
0048b743  ebe6                     jmp 0x48b72b
0048b745  ba52544900               mov edx, 0x495452
0048b74a  8b4018                   mov eax, dword ptr [eax + 0x18]
0048b74d  e8b20a0000               call 0x48c204
0048b752  890424                   mov dword ptr [esp], eax
0048b755  85c0                     test eax, eax
0048b757  7427                     je 0x48b780
0048b759  89c2                     mov edx, eax
0048b75b  8b7108                   mov esi, dword ptr [ecx + 8]
0048b75e  8b5918                   mov ebx, dword ptr [ecx + 0x18]
0048b761  89f0                     mov eax, esi
0048b763  e8d6080000               call 0x48c03e
0048b768  3b4118                   cmp eax, dword ptr [ecx + 0x18]
0048b76b  7410                     je 0x48b77d
0048b76d  ba85544900               mov edx, 0x495485
0048b772  89e0                     mov eax, esp
0048b774  e8060b0000               call 0x48c27f
0048b779  31c0                     xor eax, eax
0048b77b  eb03                     jmp 0x48b780
0048b77d  8b0424                   mov eax, dword ptr [esp]
0048b780  894114                   mov dword ptr [ecx + 0x14], eax
0048b783  b801000000               mov eax, 1
0048b788  c7411001000000           mov dword ptr [ecx + 0x10], 1
0048b78f  eb9a                     jmp 0x48b72b
; DSB_CreateEmptySoundBuffer (buffer)
0048b7b1  56                       push esi
0048b7b2  57                       push edi
0048b7b3  55                       push ebp
0048b7b4  83ec28                   sub esp, 0x28
0048b7b7  833d2822520000           cmp dword ptr [0x522228], 0
0048b7be  747a                     je 0x48b83a
0048b7c0  6689442416               mov word ptr [esp + 0x16], ax
0048b7c5  0fafc3                   imul eax, ebx
0048b7c8  c1f803                   sar eax, 3
0048b7cb  6689442420               mov word ptr [esp + 0x20], ax
0048b7d0  31c0                     xor eax, eax
0048b7d2  668b442420               mov ax, word ptr [esp + 0x20]
0048b7d7  89542418                 mov dword ptr [esp + 0x18], edx
0048b7db  0fafd0                   imul edx, eax
0048b7de  be01000000               mov esi, 1
0048b7e3  bf14000000               mov edi, 0x14
0048b7e8  bde0000000               mov ebp, 0xe0
0048b7ed  66895c2422               mov word ptr [esp + 0x22], bx
0048b7f2  bb14000000               mov ebx, 0x14
0048b7f7  89e0                     mov eax, esp
0048b7f9  8954241c                 mov dword ptr [esp + 0x1c], edx
0048b7fd  31d2                     xor edx, edx
0048b7ff  6689742414               mov word ptr [esp + 0x14], si
0048b804  e8a70b0000               call 0x48c3b0
0048b809  8d442414                 lea eax, [esp + 0x14]
0048b80d  6a00                     push 0
0048b80f  8d5c2428                 lea ebx, [esp + 0x28]
0048b813  897c2404                 mov dword ptr [esp + 4], edi
0048b817  896c2408                 mov dword ptr [esp + 8], ebp
0048b81b  89442414                 mov dword ptr [esp + 0x14], eax
0048b81f  53                       push ebx
0048b820  8d5c2408                 lea ebx, [esp + 8]
0048b824  a128225200               mov eax, dword ptr [0x522228]
0048b829  894c2410                 mov dword ptr [esp + 0x10], ecx
0048b82d  53                       push ebx
0048b82e  8b10                     mov edx, dword ptr [eax]
0048b830  50                       push eax
0048b831  ff520c                   call dword ptr [edx + 0xc]
0048b834  8b442424                 mov eax, dword ptr [esp + 0x24]
0048b838  eb02                     jmp 0x48b83c
0048b83a  31c0                     xor eax, eax
0048b83c  83c428                   add esp, 0x28
0048b83f  5d                       pop ebp
0048b840  5f                       pop edi
0048b841  5e                       pop esi
0048b842  c3                       ret
; imaadpcmNextStepIndex (decode)
0048b844  53                       push ebx
0048b845  89c3                     mov ebx, eax
0048b847  89d0                     mov eax, edx
0048b849  89da                     mov edx, ebx
0048b84b  8b14556a8f4900           mov edx, dword ptr [edx*2 + 0x498f6a]
0048b852  c1fa10                   sar edx, 0x10
0048b855  01d0                     add eax, edx
0048b857  85c0                     test eax, eax
0048b859  7d04                     jge 0x48b85f
0048b85b  31c0                     xor eax, eax
0048b85d  5b                       pop ebx
0048b85e  c3                       ret
0048b85f  83f858                   cmp eax, 0x58
0048b862  7e05                     jle 0x48b869
0048b864  b858000000               mov eax, 0x58
0048b869  5b                       pop ebx
0048b86a  c3                       ret
; imaadpcmSampleDecode (decode)
0048b86b  51                       push ecx
0048b86c  56                       push esi
0048b86d  89c1                     mov ecx, eax
0048b86f  89d8                     mov eax, ebx
0048b871  c1f803                   sar eax, 3
0048b874  f6c104                   test cl, 4
0048b877  7402                     je 0x48b87b
0048b879  01d8                     add eax, ebx
0048b87b  f6c102                   test cl, 2
0048b87e  7406                     je 0x48b886
0048b880  89de                     mov esi, ebx
0048b882  d1fe                     sar esi, 1
0048b884  01f0                     add eax, esi
0048b886  f6c101                   test cl, 1
0048b889  7405                     je 0x48b890
0048b88b  c1fb02                   sar ebx, 2
0048b88e  01d8                     add eax, ebx
0048b890  f6c108                   test cl, 8
0048b893  7402                     je 0x48b897
0048b895  f7d8                     neg eax
0048b897  01d0                     add eax, edx
0048b899  0fbfd0                   movsx edx, ax
0048b89c  39c2                     cmp edx, eax
0048b89e  7414                     je 0x48b8b4
0048b8a0  3d0080ffff               cmp eax, 0xffff8000
0048b8a5  7d08                     jge 0x48b8af
0048b8a7  b80080ffff               mov eax, 0xffff8000
0048b8ac  5e                       pop esi
0048b8ad  59                       pop ecx
0048b8ae  c3                       ret
0048b8af  b8ff7f0000               mov eax, 0x7fff
0048b8b4  5e                       pop esi
0048b8b5  59                       pop ecx
0048b8b6  c3                       ret
; imaadpcmValidStepIndex (decode)
0048b8b7  85c0                     test eax, eax
0048b8b9  7c0b                     jl 0x48b8c6
0048b8bb  83f858                   cmp eax, 0x58
0048b8be  7f06                     jg 0x48b8c6
0048b8c0  b801000000               mov eax, 1
0048b8c5  c3                       ret
0048b8c6  31c0                     xor eax, eax
0048b8c8  c3                       ret
; imaadpcmDecode4Bit_M16 (decode)
0048b8c9  56                       push esi
0048b8ca  57                       push edi
0048b8cb  55                       push ebp
0048b8cc  83ec2c                   sub esp, 0x2c
0048b8cf  89c6                     mov esi, eax
0048b8d1  8954240c                 mov dword ptr [esp + 0xc], edx
0048b8d5  894c2408                 mov dword ptr [esp + 8], ecx
0048b8d9  895c2404                 mov dword ptr [esp + 4], ebx
0048b8dd  8b54240c                 mov edx, dword ptr [esp + 0xc]
0048b8e1  83fa04                   cmp edx, 4
0048b8e4  0f829b010000             jb 0x48ba85
0048b8ea  8b7c2408                 mov edi, dword ptr [esp + 8]
0048b8ee  39fa                     cmp edx, edi
0048b8f0  7304                     jae 0x48b8f6
0048b8f2  89d0                     mov eax, edx
0048b8f4  eb02                     jmp 0x48b8f8
0048b8f6  89f8                     mov eax, edi
0048b8f8  8b6c240c                 mov ebp, dword ptr [esp + 0xc]
0048b8fc  29c5                     sub ebp, eax
0048b8fe  83e804                   sub eax, 4
0048b901  89442420                 mov dword ptr [esp + 0x20], eax
0048b905  8b06                     mov eax, dword ptr [esi]
0048b907  0fbfd0                   movsx edx, ax
0048b90a  c1e810                   shr eax, 0x10
0048b90d  896c240c                 mov dword ptr [esp + 0xc], ebp
0048b911  25ffff0000               and eax, 0xffff
0048b916  25ff000000               and eax, 0xff
0048b91b  83c604                   add esi, 4
0048b91e  89442424                 mov dword ptr [esp + 0x24], eax
0048b922  85c0                     test eax, eax
0048b924  7c0c                     jl 0x48b932
0048b926  83f858                   cmp eax, 0x58
0048b929  7f07                     jg 0x48b932
0048b92b  b801000000               mov eax, 1
0048b930  eb02                     jmp 0x48b934
0048b932  31c0                     xor eax, eax
0048b934  85c0                     test eax, eax
0048b936  0f8451010000             je 0x48ba8d
0048b93c  668913                   mov word ptr [ebx], dx
0048b93f  83c302                   add ebx, 2
0048b942  8b7c2420                 mov edi, dword ptr [esp + 0x20]
0048b946  4f                       dec edi
0048b947  897c2420                 mov dword ptr [esp + 0x20], edi
0048b94b  83ffff                   cmp edi, -1
0048b94e  748d                     je 0x48b8dd
0048b950  8b6c2424                 mov ebp, dword ptr [esp + 0x24]
0048b954  8a06                     mov al, byte ptr [esi]
0048b956  89542410                 mov dword ptr [esp + 0x10], edx
0048b95a  88442428                 mov byte ptr [esp + 0x28], al
0048b95e  46                       inc esi
0048b95f  8b2c6d8a8f4900           mov ebp, dword ptr [ebp*2 + 0x498f8a]
0048b966  240f                     and al, 0xf
0048b968  c1fd10                   sar ebp, 0x10
0048b96b  0fb6f8                   movzx edi, al
0048b96e  896c2418                 mov dword ptr [esp + 0x18], ebp
0048b972  89e8                     mov eax, ebp
0048b974  89f9                     mov ecx, edi
0048b976  c1f803                   sar eax, 3
0048b979  66f7c70400               test di, 4
0048b97e  7402                     je 0x48b982
0048b980  01e8                     add eax, ebp
0048b982  f6c102                   test cl, 2
0048b985  7408                     je 0x48b98f
0048b987  8b542418                 mov edx, dword ptr [esp + 0x18]
0048b98b  d1fa                     sar edx, 1
0048b98d  01d0                     add eax, edx
0048b98f  f6c101                   test cl, 1
0048b992  7409                     je 0x48b99d
0048b994  8b542418                 mov edx, dword ptr [esp + 0x18]
0048b998  c1fa02                   sar edx, 2
0048b99b  01d0                     add eax, edx
0048b99d  f6c108                   test cl, 8
0048b9a0  7402                     je 0x48b9a4
0048b9a2  f7d8                     neg eax
0048b9a4  03442410                 add eax, dword ptr [esp + 0x10]
0048b9a8  0fbfd0                   movsx edx, ax
0048b9ab  39c2                     cmp edx, eax
0048b9ad  7413                     je 0x48b9c2
0048b9af  3d0080ffff               cmp eax, 0xffff8000
0048b9b4  7d07                     jge 0x48b9bd
0048b9b6  b80080ffff               mov eax, 0xffff8000
0048b9bb  eb05                     jmp 0x48b9c2
0048b9bd  b8ff7f0000               mov eax, 0x7fff
0048b9c2  89c2                     mov edx, eax
0048b9c4  8b047d6a8f4900           mov eax, dword ptr [edi*2 + 0x498f6a]
0048b9cb  8b4c2424                 mov ecx, dword ptr [esp + 0x24]
0048b9cf  c1f810                   sar eax, 0x10
0048b9d2  01c8                     add eax, ecx
0048b9d4  85c0                     test eax, eax
0048b9d6  7d04                     jge 0x48b9dc
0048b9d8  31c0                     xor eax, eax
0048b9da  eb0a                     jmp 0x48b9e6
0048b9dc  83f858                   cmp eax, 0x58
0048b9df  7e05                     jle 0x48b9e6
0048b9e1  b858000000               mov eax, 0x58
0048b9e6  0fb67c2428               movzx edi, byte ptr [esp + 0x28]
0048b9eb  890424                   mov dword ptr [esp], eax
0048b9ee  89542414                 mov dword ptr [esp + 0x14], edx
0048b9f2  668913                   mov word ptr [ebx], dx
0048b9f5  c1ff04                   sar edi, 4
0048b9f8  8b2c458a8f4900           mov ebp, dword ptr [eax*2 + 0x498f8a]
0048b9ff  83c302                   add ebx, 2
0048ba02  c1fd10                   sar ebp, 0x10
0048ba05  89f9                     mov ecx, edi
0048ba07  89e8                     mov eax, ebp
0048ba09  896c241c                 mov dword ptr [esp + 0x1c], ebp
0048ba0d  c1f803                   sar eax, 3
0048ba10  66f7c70400               test di, 4
0048ba15  7402                     je 0x48ba19
0048ba17  01e8                     add eax, ebp
0048ba19  f6c102                   test cl, 2
0048ba1c  7408                     je 0x48ba26
0048ba1e  8b54241c                 mov edx, dword ptr [esp + 0x1c]
0048ba22  d1fa                     sar edx, 1
0048ba24  01d0                     add eax, edx
0048ba26  f6c101                   test cl, 1
0048ba29  7409                     je 0x48ba34
0048ba2b  8b54241c                 mov edx, dword ptr [esp + 0x1c]
0048ba2f  c1fa02                   sar edx, 2
0048ba32  01d0                     add eax, edx
0048ba34  f6c108                   test cl, 8
0048ba37  7402                     je 0x48ba3b
0048ba39  f7d8                     neg eax
0048ba3b  03442414                 add eax, dword ptr [esp + 0x14]
0048ba3f  0fbfd0                   movsx edx, ax
0048ba42  39c2                     cmp edx, eax
0048ba44  7413                     je 0x48ba59
0048ba46  3d0080ffff               cmp eax, 0xffff8000
0048ba4b  7d07                     jge 0x48ba54
0048ba4d  b80080ffff               mov eax, 0xffff8000
0048ba52  eb05                     jmp 0x48ba59
0048ba54  b8ff7f0000               mov eax, 0x7fff
0048ba59  89c2                     mov edx, eax
0048ba5b  8b047d6a8f4900           mov eax, dword ptr [edi*2 + 0x498f6a]
0048ba62  8b0c24                   mov ecx, dword ptr [esp]
0048ba65  c1f810                   sar eax, 0x10
0048ba68  01c8                     add eax, ecx
0048ba6a  85c0                     test eax, eax
0048ba6c  7d04                     jge 0x48ba72
0048ba6e  31c0                     xor eax, eax
0048ba70  eb0a                     jmp 0x48ba7c
0048ba72  83f858                   cmp eax, 0x58
0048ba75  7e05                     jle 0x48ba7c
0048ba77  b858000000               mov eax, 0x58
0048ba7c  89442424                 mov dword ptr [esp + 0x24], eax
0048ba80  e9b7feffff               jmp 0x48b93c
0048ba85  8b4c2404                 mov ecx, dword ptr [esp + 4]
0048ba89  89d8                     mov eax, ebx
0048ba8b  29c8                     sub eax, ecx
0048ba8d  83c42c                   add esp, 0x2c
0048ba90  5d                       pop ebp
0048ba91  5f                       pop edi
0048ba92  5e                       pop esi
0048ba93  c20c00                   ret 0xc
; imaadpcmDecode4Bit_S16 (decode)
0048ba96  56                       push esi
0048ba97  57                       push edi
0048ba98  55                       push ebp
0048ba99  83ec3c                   sub esp, 0x3c
0048ba9c  89c5                     mov ebp, eax
0048ba9e  89542410                 mov dword ptr [esp + 0x10], edx
0048baa2  894c240c                 mov dword ptr [esp + 0xc], ecx
0048baa6  8d41f8                   lea eax, [ecx - 8]
0048baa9  895c2404                 mov dword ptr [esp + 4], ebx
0048baad  89442408                 mov dword ptr [esp + 8], eax
0048bab1  8b542410                 mov edx, dword ptr [esp + 0x10]
0048bab5  85d2                     test edx, edx
0048bab7  0f8445020000             je 0x48bd02
0048babd  8b44240c                 mov eax, dword ptr [esp + 0xc]
0048bac1  89d6                     mov esi, edx
0048bac3  29c6                     sub esi, eax
0048bac5  8b442408                 mov eax, dword ptr [esp + 8]
0048bac9  89442414                 mov dword ptr [esp + 0x14], eax
0048bacd  8b4500                   mov eax, dword ptr [ebp]
0048bad0  89742410                 mov dword ptr [esp + 0x10], esi
0048bad4  0fbfd0                   movsx edx, ax
0048bad7  c1e810                   shr eax, 0x10
0048bada  89542428                 mov dword ptr [esp + 0x28], edx
0048bade  25ffff0000               and eax, 0xffff
0048bae3  25ff000000               and eax, 0xff
0048bae8  83c504                   add ebp, 4
0048baeb  8944242c                 mov dword ptr [esp + 0x2c], eax
0048baef  85c0                     test eax, eax
0048baf1  7c0c                     jl 0x48baff
0048baf3  83f858                   cmp eax, 0x58
0048baf6  7f07                     jg 0x48baff
0048baf8  b801000000               mov eax, 1
0048bafd  eb02                     jmp 0x48bb01
0048baff  31c0                     xor eax, eax
0048bb01  85c0                     test eax, eax
0048bb03  0f8401020000             je 0x48bd0a
0048bb09  8b4500                   mov eax, dword ptr [ebp]
0048bb0c  0fbfd0                   movsx edx, ax
0048bb0f  c1e810                   shr eax, 0x10
0048bb12  89542424                 mov dword ptr [esp + 0x24], edx
0048bb16  25ffff0000               and eax, 0xffff
0048bb1b  25ff000000               and eax, 0xff
0048bb20  83c504                   add ebp, 4
0048bb23  89442430                 mov dword ptr [esp + 0x30], eax
0048bb27  85c0                     test eax, eax
0048bb29  7c0c                     jl 0x48bb37
0048bb2b  83f858                   cmp eax, 0x58
0048bb2e  7f07                     jg 0x48bb37
0048bb30  b801000000               mov eax, 1
0048bb35  eb02                     jmp 0x48bb39
0048bb37  31c0                     xor eax, eax
0048bb39  85c0                     test eax, eax
0048bb3b  0f84c9010000             je 0x48bd0a
0048bb41  31c0                     xor eax, eax
0048bb43  668b442424               mov ax, word ptr [esp + 0x24]
0048bb48  89c2                     mov edx, eax
0048bb4a  31c0                     xor eax, eax
0048bb4c  c1e210                   shl edx, 0x10
0048bb4f  668b442428               mov ax, word ptr [esp + 0x28]
0048bb54  09d0                     or eax, edx
0048bb56  8903                     mov dword ptr [ebx], eax
0048bb58  83c304                   add ebx, 4
0048bb5b  8b742414                 mov esi, dword ptr [esp + 0x14]
0048bb5f  85f6                     test esi, esi
0048bb61  0f844affffff             je 0x48bab1
0048bb67  8d7ef8                   lea edi, [esi - 8]
0048bb6a  8b4500                   mov eax, dword ptr [ebp]
0048bb6d  83c504                   add ebp, 4
0048bb70  89442434                 mov dword ptr [esp + 0x34], eax
0048bb74  897c2414                 mov dword ptr [esp + 0x14], edi
0048bb78  8b4500                   mov eax, dword ptr [ebp]
0048bb7b  bf08000000               mov edi, 8
0048bb80  89442438                 mov dword ptr [esp + 0x38], eax
0048bb84  83c504                   add ebp, 4
0048bb87  e901010000               jmp 0x48bc8d
0048bb8c  b8ff7f0000               mov eax, 0x7fff
0048bb91  89442428                 mov dword ptr [esp + 0x28], eax
0048bb95  8b04756a8f4900           mov eax, dword ptr [esi*2 + 0x498f6a]
0048bb9c  8b74242c                 mov esi, dword ptr [esp + 0x2c]
0048bba0  c1f810                   sar eax, 0x10
0048bba3  01f0                     add eax, esi
0048bba5  85c0                     test eax, eax
0048bba7  7d04                     jge 0x48bbad
0048bba9  31c0                     xor eax, eax
0048bbab  eb0a                     jmp 0x48bbb7
0048bbad  83f858                   cmp eax, 0x58
0048bbb0  7e05                     jle 0x48bbb7
0048bbb2  b858000000               mov eax, 0x58
0048bbb7  8b742438                 mov esi, dword ptr [esp + 0x38]
0048bbbb  8b4c2430                 mov ecx, dword ptr [esp + 0x30]
0048bbbf  8944242c                 mov dword ptr [esp + 0x2c], eax
0048bbc3  8b442424                 mov eax, dword ptr [esp + 0x24]
0048bbc7  8b0c4d8a8f4900           mov ecx, dword ptr [ecx*2 + 0x498f8a]
0048bbce  83e60f                   and esi, 0xf
0048bbd1  c1f910                   sar ecx, 0x10
0048bbd4  89f2                     mov edx, esi
0048bbd6  89442418                 mov dword ptr [esp + 0x18], eax
0048bbda  89c8                     mov eax, ecx
0048bbdc  894c241c                 mov dword ptr [esp + 0x1c], ecx
0048bbe0  c1f803                   sar eax, 3
0048bbe3  66f7c60400               test si, 4
0048bbe8  7402                     je 0x48bbec
0048bbea  01c8                     add eax, ecx
0048bbec  f6c202                   test dl, 2
0048bbef  7408                     je 0x48bbf9
0048bbf1  8b4c241c                 mov ecx, dword ptr [esp + 0x1c]
0048bbf5  d1f9                     sar ecx, 1
0048bbf7  01c8                     add eax, ecx
0048bbf9  f6c201                   test dl, 1
0048bbfc  7409                     je 0x48bc07
0048bbfe  8b4c241c                 mov ecx, dword ptr [esp + 0x1c]
0048bc02  c1f902                   sar ecx, 2
0048bc05  01c8                     add eax, ecx
0048bc07  f6c208                   test dl, 8
0048bc0a  7402                     je 0x48bc0e
0048bc0c  f7d8                     neg eax
0048bc0e  03442418                 add eax, dword ptr [esp + 0x18]
0048bc12  0fbfd0                   movsx edx, ax
0048bc15  39c2                     cmp edx, eax
0048bc17  7413                     je 0x48bc2c
0048bc19  3d0080ffff               cmp eax, 0xffff8000
0048bc1e  7d07                     jge 0x48bc27
0048bc20  b80080ffff               mov eax, 0xffff8000
0048bc25  eb05                     jmp 0x48bc2c
0048bc27  b8ff7f0000               mov eax, 0x7fff
0048bc2c  89442424                 mov dword ptr [esp + 0x24], eax
0048bc30  8b04756a8f4900           mov eax, dword ptr [esi*2 + 0x498f6a]
0048bc37  8b4c2430                 mov ecx, dword ptr [esp + 0x30]
0048bc3b  c1f810                   sar eax, 0x10
0048bc3e  01c8                     add eax, ecx
0048bc40  85c0                     test eax, eax
0048bc42  7d04                     jge 0x48bc48
0048bc44  31c0                     xor eax, eax
0048bc46  eb0a                     jmp 0x48bc52
0048bc48  83f858                   cmp eax, 0x58
0048bc4b  7e05                     jle 0x48bc52
0048bc4d  b858000000               mov eax, 0x58
0048bc52  89442430                 mov dword ptr [esp + 0x30], eax
0048bc56  31c0                     xor eax, eax
0048bc58  31d2                     xor edx, edx
0048bc5a  668b442424               mov ax, word ptr [esp + 0x24]
0048bc5f  668b542428               mov dx, word ptr [esp + 0x28]
0048bc64  c1e010                   shl eax, 0x10
0048bc67  4f                       dec edi
0048bc68  09c2                     or edx, eax
0048bc6a  8b442434                 mov eax, dword ptr [esp + 0x34]
0048bc6e  8913                     mov dword ptr [ebx], edx
0048bc70  8b542438                 mov edx, dword ptr [esp + 0x38]
0048bc74  c1e804                   shr eax, 4
0048bc77  83c304                   add ebx, 4
0048bc7a  c1ea04                   shr edx, 4
0048bc7d  89442434                 mov dword ptr [esp + 0x34], eax
0048bc81  89542438                 mov dword ptr [esp + 0x38], edx
0048bc85  85ff                     test edi, edi
0048bc87  0f8ecefeffff             jle 0x48bb5b
0048bc8d  8b742434                 mov esi, dword ptr [esp + 0x34]
0048bc91  8b54242c                 mov edx, dword ptr [esp + 0x2c]
0048bc95  8b442428                 mov eax, dword ptr [esp + 0x28]
0048bc99  83e60f                   and esi, 0xf
0048bc9c  8b14558a8f4900           mov edx, dword ptr [edx*2 + 0x498f8a]
0048bca3  890424                   mov dword ptr [esp], eax
0048bca6  c1fa10                   sar edx, 0x10
0048bca9  89f1                     mov ecx, esi
0048bcab  89d0                     mov eax, edx
0048bcad  89542420                 mov dword ptr [esp + 0x20], edx
0048bcb1  c1f803                   sar eax, 3
0048bcb4  66f7c60400               test si, 4
0048bcb9  7402                     je 0x48bcbd
0048bcbb  01d0                     add eax, edx
0048bcbd  f6c102                   test cl, 2
0048bcc0  7408                     je 0x48bcca
0048bcc2  8b542420                 mov edx, dword ptr [esp + 0x20]
0048bcc6  d1fa                     sar edx, 1
0048bcc8  01d0                     add eax, edx
0048bcca  f6c101                   test cl, 1
0048bccd  7409                     je 0x48bcd8
0048bccf  8b542420                 mov edx, dword ptr [esp + 0x20]
0048bcd3  c1fa02                   sar edx, 2
0048bcd6  01d0                     add eax, edx
0048bcd8  f6c108                   test cl, 8
0048bcdb  7402                     je 0x48bcdf
0048bcdd  f7d8                     neg eax
0048bcdf  030424                   add eax, dword ptr [esp]
0048bce2  0fbfd0                   movsx edx, ax
0048bce5  39c2                     cmp edx, eax
0048bce7  0f84a4feffff             je 0x48bb91
0048bced  3d0080ffff               cmp eax, 0xffff8000
0048bcf2  0f8d94feffff             jge 0x48bb8c
0048bcf8  b80080ffff               mov eax, 0xffff8000
0048bcfd  e98ffeffff               jmp 0x48bb91
0048bd02  8b4c2404                 mov ecx, dword ptr [esp + 4]
0048bd06  89d8                     mov eax, ebx
0048bd08  29c8                     sub eax, ecx
0048bd0a  83c43c                   add esp, 0x3c
0048bd0d  e97efdffff               jmp 0x48ba90
; CreatM (wrapper)
0048c008  51                       push ecx
0048c009  52                       push edx
0048c00a  50                       push eax
0048c00b  2eff15f4315200           call dword ptr cs:[0x5231f4]
0048c012  83f8ff                   cmp eax, -1
0048c015  59                       pop ecx
0048c016  c3                       ret
; OpenM (wrapper)
0048c017  51                       push ecx
0048c018  52                       push edx
0048c019  50                       push eax
0048c01a  2eff15fc315200           call dword ptr cs:[0x5231fc]
0048c021  83f8ff                   cmp eax, -1
0048c024  59                       pop ecx
0048c025  c3                       ret
; CloseM (wrapper)
0048c026  51                       push ecx
0048c027  52                       push edx
0048c028  50                       push eax
0048c029  2eff15f0315200           call dword ptr cs:[0x5231f0]
0048c030  83f8ff                   cmp eax, -1
0048c033  0f95c0                   setne al
0048c036  25ff000000               and eax, 0xff
0048c03b  5a                       pop edx
0048c03c  59                       pop ecx
0048c03d  c3                       ret
; ReadM (wrapper)
0048c03e  51                       push ecx
0048c03f  53                       push ebx
0048c040  52                       push edx
0048c041  50                       push eax
0048c042  2eff15e8315200           call dword ptr cs:[0x5231e8]
0048c049  83f8ff                   cmp eax, -1
0048c04c  59                       pop ecx
0048c04d  c3                       ret
; WriteM (wrapper)
0048c04e  51                       push ecx
0048c04f  53                       push ebx
0048c050  52                       push edx
0048c051  50                       push eax
0048c052  2eff15ec315200           call dword ptr cs:[0x5231ec]
0048c059  83f8ff                   cmp eax, -1
0048c05c  59                       pop ecx
0048c05d  c3                       ret
; SeekM (wrapper)
0048c05e  51                       push ecx
0048c05f  53                       push ebx
0048c060  52                       push edx
0048c061  50                       push eax
0048c062  2eff15f8315200           call dword ptr cs:[0x5231f8]
0048c069  83f8ff                   cmp eax, -1
0048c06c  59                       pop ecx
0048c06d  c3                       ret
; LoadSoundBuffer_LoadDataFromFileInSoundBuffer (decode)
0048c070  51                       push ecx
0048c071  56                       push esi
0048c072  57                       push edi
0048c073  83ec08                   sub esp, 8
0048c076  89c6                     mov esi, eax
0048c078  89d7                     mov edi, edx
0048c07a  85c0                     test eax, eax
0048c07c  7437                     je 0x48c0b5
0048c07e  6a00                     push 0
0048c080  6a00                     push 0
0048c082  6a00                     push 0
0048c084  8d542410                 lea edx, [esp + 0x10]
0048c088  52                       push edx
0048c089  8d542410                 lea edx, [esp + 0x10]
0048c08d  52                       push edx
0048c08e  53                       push ebx
0048c08f  6a00                     push 0
0048c091  8b00                     mov eax, dword ptr [eax]
0048c093  56                       push esi
0048c094  ff502c                   call dword ptr [eax + 0x2c]
0048c097  8b1424                   mov edx, dword ptr [esp]
0048c09a  89f8                     mov eax, edi
0048c09c  e89dffffff               call 0x48c03e
0048c0a1  6a00                     push 0
0048c0a3  6a00                     push 0
0048c0a5  8b54240c                 mov edx, dword ptr [esp + 0xc]
0048c0a9  52                       push edx
0048c0aa  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c0ae  53                       push ebx
0048c0af  8b06                     mov eax, dword ptr [esi]
0048c0b1  56                       push esi
0048c0b2  ff504c                   call dword ptr [eax + 0x4c]
0048c0b5  83c408                   add esp, 8
0048c0b8  5f                       pop edi
0048c0b9  5e                       pop esi
0048c0ba  59                       pop ecx
0048c0bb  c3                       ret
; LoadSoundBuffer_DecompactInSoundBuffer (decode)
0048c0bc  56                       push esi
0048c0bd  57                       push edi
0048c0be  55                       push ebp
0048c0bf  83ec08                   sub esp, 8
0048c0c2  89c6                     mov esi, eax
0048c0c4  89d5                     mov ebp, edx
0048c0c6  89df                     mov edi, ebx
0048c0c8  89cb                     mov ebx, ecx
0048c0ca  85c0                     test eax, eax
0048c0cc  7460                     je 0x48c12e
0048c0ce  6a00                     push 0
0048c0d0  6a00                     push 0
0048c0d2  6a00                     push 0
0048c0d4  8d542410                 lea edx, [esp + 0x10]
0048c0d8  52                       push edx
0048c0d9  8d542410                 lea edx, [esp + 0x10]
0048c0dd  52                       push edx
0048c0de  57                       push edi
0048c0df  6a00                     push 0
0048c0e1  8b00                     mov eax, dword ptr [eax]
0048c0e3  56                       push esi
0048c0e4  ff502c                   call dword ptr [eax + 0x2c]
0048c0e7  837c241801               cmp dword ptr [esp + 0x18], 1
0048c0ec  7517                     jne 0x48c105
0048c0ee  6a00                     push 0
0048c0f0  6a00                     push 0
0048c0f2  89d9                     mov ecx, ebx
0048c0f4  89fa                     mov edx, edi
0048c0f6  6a00                     push 0
0048c0f8  89e8                     mov eax, ebp
0048c0fa  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c0fe  e8c6f7ffff               call 0x48b8c9
0048c103  eb15                     jmp 0x48c11a
0048c105  6a00                     push 0
0048c107  6a00                     push 0
0048c109  89d9                     mov ecx, ebx
0048c10b  89fa                     mov edx, edi
0048c10d  6a00                     push 0
0048c10f  89e8                     mov eax, ebp
0048c111  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c115  e87cf9ffff               call 0x48ba96
0048c11a  6a00                     push 0
0048c11c  6a00                     push 0
0048c11e  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c122  53                       push ebx
0048c123  8b4c240c                 mov ecx, dword ptr [esp + 0xc]
0048c127  51                       push ecx
0048c128  8b06                     mov eax, dword ptr [esi]
0048c12a  56                       push esi
0048c12b  ff504c                   call dword ptr [eax + 0x4c]
0048c12e  83c408                   add esp, 8
0048c131  5d                       pop ebp
0048c132  5f                       pop edi
0048c133  5e                       pop esi
0048c134  c20400                   ret 4
; LoadSoundBuffer_PlaceOnSample (decode)
0048c137  53                       push ebx
0048c138  31db                     xor ebx, ebx
0048c13a  e81fffffff               call 0x48c05e
0048c13f  5b                       pop ebx
0048c140  c3                       ret
; LoadSoundBuffer_LoadCompactedData (decode)
0048c141  53                       push ebx
0048c142  51                       push ecx
0048c143  89d1                     mov ecx, edx
0048c145  8b152c225200             mov edx, dword ptr [0x52222c]
0048c14b  85d2                     test edx, edx
0048c14d  7505                     jne 0x48c154
0048c14f  89d0                     mov eax, edx
0048c151  59                       pop ecx
0048c152  5b                       pop ebx
0048c153  c3                       ret
0048c154  89cb                     mov ebx, ecx
0048c156  e8e3feffff               call 0x48c03e
0048c15b  39c1                     cmp ecx, eax
0048c15d  7405                     je 0x48c164
0048c15f  31c0                     xor eax, eax
0048c161  59                       pop ecx
0048c162  5b                       pop ebx
0048c163  c3                       ret
0048c164  a12c225200               mov eax, dword ptr [0x52222c]
0048c169  59                       pop ecx
0048c16a  5b                       pop ebx
0048c16b  c3                       ret
; LoadSoundBuffer_InitCompressedBuffer (decode)
0048c16c  52                       push edx
0048c16d  bab0544900               mov edx, 0x4954b0
0048c172  b800710200               mov eax, 0x27100
0048c177  e888000000               call 0x48c204
0048c17c  a32c225200               mov dword ptr [0x52222c], eax
0048c181  85c0                     test eax, eax
0048c183  0f95c0                   setne al
0048c186  25ff000000               and eax, 0xff
0048c18b  5a                       pop edx
0048c18c  c3                       ret
; LoadSoundBuffer_FreeCompressedBuffer (decode)
0048c18d  52                       push edx
0048c18e  833d2c22520000           cmp dword ptr [0x52222c], 0
0048c195  740f                     je 0x48c1a6
0048c197  bae8544900               mov edx, 0x4954e8
0048c19c  b82c225200               mov eax, 0x52222c
0048c1a1  e8d9000000               call 0x48c27f
0048c1a6  5a                       pop edx
0048c1a7  c3                       ret
; LoadSoundBuffer_LoadDataFromMemoryInSoundBuffer (decode)
0048c1a8  51                       push ecx
0048c1a9  56                       push esi
0048c1aa  57                       push edi
0048c1ab  55                       push ebp
0048c1ac  83ec08                   sub esp, 8
0048c1af  89c5                     mov ebp, eax
0048c1b1  89d6                     mov esi, edx
0048c1b3  85c0                     test eax, eax
0048c1b5  7443                     je 0x48c1fa
0048c1b7  6a00                     push 0
0048c1b9  6a00                     push 0
0048c1bb  6a00                     push 0
0048c1bd  8d542410                 lea edx, [esp + 0x10]
0048c1c1  52                       push edx
0048c1c2  8d542410                 lea edx, [esp + 0x10]
0048c1c6  52                       push edx
0048c1c7  53                       push ebx
0048c1c8  6a00                     push 0
0048c1ca  8b00                     mov eax, dword ptr [eax]
0048c1cc  55                       push ebp
0048c1cd  ff502c                   call dword ptr [eax + 0x2c]
0048c1d0  8b3c24                   mov edi, dword ptr [esp]
0048c1d3  89d9                     mov ecx, ebx
0048c1d5  57                       push edi
0048c1d6  89c8                     mov eax, ecx
0048c1d8  c1e902                   shr ecx, 2
0048c1db  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048c1dd  8ac8                     mov cl, al
0048c1df  80e103                   and cl, 3
0048c1e2  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048c1e4  5f                       pop edi
0048c1e5  6a00                     push 0
0048c1e7  6a00                     push 0
0048c1e9  8b54240c                 mov edx, dword ptr [esp + 0xc]
0048c1ed  52                       push edx
0048c1ee  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c1f2  53                       push ebx
0048c1f3  8b4500                   mov eax, dword ptr [ebp]
0048c1f6  55                       push ebp
0048c1f7  ff504c                   call dword ptr [eax + 0x4c]
0048c1fa  83c408                   add esp, 8
0048c1fd  5d                       pop ebp
0048c1fe  5f                       pop edi
0048c1ff  5e                       pop esi
0048c200  59                       pop ecx
0048c201  c3                       ret
; OurAlloc (wrapper)
0048c204  53                       push ebx
0048c205  51                       push ecx
0048c206  56                       push esi
0048c207  89d6                     mov esi, edx
0048c209  50                       push eax
0048c20a  6a00                     push 0
0048c20c  2eff15c0315200           call dword ptr cs:[0x5231c0]
0048c213  89c3                     mov ebx, eax
0048c215  85c0                     test eax, eax
0048c217  7515                     jne 0x48c22e
0048c219  50                       push eax
0048c21a  6830554900               push 0x495530
0048c21f  56                       push esi
0048c220  8b15e8274e00             mov edx, dword ptr [0x4e27e8]
0048c226  52                       push edx
0048c227  2eff15b0325200           call dword ptr cs:[0x5232b0]
0048c22e  8b0d30225200             mov ecx, dword ptr [0x522230]
0048c234  41                       inc ecx
0048c235  89d8                     mov eax, ebx
0048c237  890d30225200             mov dword ptr [0x522230], ecx
0048c23d  5e                       pop esi
0048c23e  59                       pop ecx
0048c23f  5b                       pop ebx
0048c240  c3                       ret
; OurCalloc (wrapper)
0048c241  51                       push ecx
0048c242  56                       push esi
0048c243  89de                     mov esi, ebx
0048c245  0fafc2                   imul eax, edx
0048c248  50                       push eax
0048c249  6a40                     push 0x40
0048c24b  2eff15c0315200           call dword ptr cs:[0x5231c0]
0048c252  89c3                     mov ebx, eax
0048c254  85c0                     test eax, eax
0048c256  7515                     jne 0x48c26d
0048c258  50                       push eax
0048c259  6831554900               push 0x495531
0048c25e  56                       push esi
0048c25f  8b15e8274e00             mov edx, dword ptr [0x4e27e8]
0048c265  52                       push edx
0048c266  2eff15b0325200           call dword ptr cs:[0x5232b0]
0048c26d  8b0d30225200             mov ecx, dword ptr [0x522230]
0048c273  41                       inc ecx
0048c274  89d8                     mov eax, ebx
0048c276  890d30225200             mov dword ptr [0x522230], ecx
0048c27c  5e                       pop esi
0048c27d  59                       pop ecx
0048c27e  c3                       ret
; OurFree (wrapper)
0048c27f  53                       push ebx
0048c280  51                       push ecx
0048c281  56                       push esi
0048c282  55                       push ebp
0048c283  89c3                     mov ebx, eax
0048c285  89d6                     mov esi, edx
0048c287  8b10                     mov edx, dword ptr [eax]
0048c289  85d2                     test edx, edx
0048c28b  7517                     jne 0x48c2a4
0048c28d  52                       push edx
0048c28e  6832554900               push 0x495532
0048c293  56                       push esi
0048c294  8b2de8274e00             mov ebp, dword ptr [0x4e27e8]
0048c29a  55                       push ebp
0048c29b  2eff15b0325200           call dword ptr cs:[0x5232b0]
0048c2a2  eb28                     jmp 0x48c2cc
0048c2a4  52                       push edx
0048c2a5  2eff15c8315200           call dword ptr cs:[0x5231c8]
0048c2ac  85c0                     test eax, eax
0048c2ae  7416                     je 0x48c2c6
0048c2b0  6a00                     push 0
0048c2b2  683d554900               push 0x49553d
0048c2b7  56                       push esi
0048c2b8  8b35e8274e00             mov esi, dword ptr [0x4e27e8]
0048c2be  56                       push esi
0048c2bf  2eff15b0325200           call dword ptr cs:[0x5232b0]
0048c2c6  ff0d30225200             dec dword ptr [0x522230]
0048c2cc  c70300000000             mov dword ptr [ebx], 0
0048c2d2  5d                       pop ebp
0048c2d3  5e                       pop esi
0048c2d4  59                       pop ecx
0048c2d5  5b                       pop ebx
0048c2d6  c3                       ret
; memset (crt)
0048c3b0  50                       push eax
0048c3b1  51                       push ecx
0048c3b2  88d6                     mov dh, dl
0048c3b4  c1e208                   shl edx, 8
0048c3b7  88f2                     mov dl, dh
0048c3b9  c1e208                   shl edx, 8
0048c3bc  88f2                     mov dl, dh
0048c3be  89d9                     mov ecx, ebx
0048c3c0  e8cb140000               call 0x48d890
0048c3c5  59                       pop ecx
0048c3c6  58                       pop eax
0048c3c7  c3                       ret
0048c3c8  53                       push ebx
0048c3c9  52                       push edx
0048c3ca  8b5808                   mov ebx, dword ptr [eax + 8]
0048c3cd  31d2                     xor edx, edx
0048c3cf  8a13                     mov dl, byte ptr [ebx]
0048c3d1  85d2                     test edx, edx
0048c3d3  7409                     je 0x48c3de
0048c3d5  43                       inc ebx
0048c3d6  895808                   mov dword ptr [eax + 8], ebx
0048c3d9  89d0                     mov eax, edx
0048c3db  5a                       pop edx
0048c3dc  5b                       pop ebx
0048c3dd  c3                       ret
0048c3de  8a5810                   mov bl, byte ptr [eax + 0x10]
0048c3e1  80cb02                   or bl, 2
0048c3e4  baffffffff               mov edx, 0xffffffff
0048c3e9  885810                   mov byte ptr [eax + 0x10], bl
0048c3ec  89d0                     mov eax, edx
0048c3ee  5a                       pop edx
0048c3ef  5b                       pop ebx
0048c3f0  c3                       ret
0048c3f1  ff4a08                   dec dword ptr [edx + 8]
0048c3f4  c3                       ret
; sprintf_character_sink (crt)
0048cfa8  53                       push ebx
0048cfa9  51                       push ecx
0048cfaa  88d3                     mov bl, dl
0048cfac  8b10                     mov edx, dword ptr [eax]
0048cfae  8d4a01                   lea ecx, [edx + 1]
0048cfb1  8908                     mov dword ptr [eax], ecx
0048cfb3  881a                     mov byte ptr [edx], bl
0048cfb5  ff4010                   inc dword ptr [eax + 0x10]
0048cfb8  59                       pop ecx
0048cfb9  5b                       pop ebx
0048cfba  c3                       ret
; sprintf (crt)
0048cfbb  53                       push ebx
0048cfbc  51                       push ecx
0048cfbd  52                       push edx
0048cfbe  83ec04                   sub esp, 4
0048cfc1  8d44241c                 lea eax, [esp + 0x1c]
0048cfc5  b9a8cf4800               mov ecx, 0x48cfa8
0048cfca  89e3                     mov ebx, esp
0048cfcc  8b542418                 mov edx, dword ptr [esp + 0x18]
0048cfd0  890424                   mov dword ptr [esp], eax
0048cfd3  8b442414                 mov eax, dword ptr [esp + 0x14]
0048cfd7  e80c200000               call 0x48efe8
0048cfdc  8b542414                 mov edx, dword ptr [esp + 0x14]
0048cfe0  c6040200                 mov byte ptr [edx + eax], 0
0048cfe4  83c404                   add esp, 4
0048cfe7  5a                       pop edx
0048cfe8  59                       pop ecx
0048cfe9  5b                       pop ebx
0048cfea  c3                       ret
; __STOSB (crt)
0048d890  09c9                     or ecx, ecx
0048d892  742c                     je 0x48d8c0
0048d894  3810                     cmp byte ptr [eax], dl
0048d896  a803                     test al, 3
0048d898  7409                     je 0x48d8a3
0048d89a  8810                     mov byte ptr [eax], dl
0048d89c  40                       inc eax
0048d89d  c1ca08                   ror edx, 8
0048d8a0  49                       dec ecx
0048d8a1  75f3                     jne 0x48d896
0048d8a3  51                       push ecx
0048d8a4  c1e902                   shr ecx, 2
0048d8a7  e81b000000               call 0x48d8c7
0048d8ac  59                       pop ecx
0048d8ad  83e103                   and ecx, 3
0048d8b0  740e                     je 0x48d8c0
0048d8b2  8810                     mov byte ptr [eax], dl
0048d8b4  49                       dec ecx
0048d8b5  7409                     je 0x48d8c0
0048d8b7  887001                   mov byte ptr [eax + 1], dh
0048d8ba  49                       dec ecx
0048d8bb  7403                     je 0x48d8c0
0048d8bd  885002                   mov byte ptr [eax + 2], dl
0048d8c0  c3                       ret
0048d8c1  90                       nop
0048d8c2  90                       nop
0048d8c3  90                       nop
0048d8c4  90                       nop
0048d8c5  90                       nop
0048d8c6  90                       nop
; __STOSD (crt)
0048d8c7  09c9                     or ecx, ecx
0048d8c9  7467                     je 0x48d932
0048d8cb  a81f                     test al, 0x1f
0048d8cd  7408                     je 0x48d8d7
0048d8cf  8910                     mov dword ptr [eax], edx
0048d8d1  8d4004                   lea eax, [eax + 4]
0048d8d4  49                       dec ecx
0048d8d5  75f4                     jne 0x48d8cb
0048d8d7  51                       push ecx
0048d8d8  c1e902                   shr ecx, 2
0048d8db  743a                     je 0x48d917
0048d8dd  49                       dec ecx
0048d8de  7429                     je 0x48d909
0048d8e0  8910                     mov dword ptr [eax], edx
0048d8e2  895004                   mov dword ptr [eax + 4], edx
0048d8e5  49                       dec ecx
0048d8e6  895008                   mov dword ptr [eax + 8], edx
0048d8e9  89500c                   mov dword ptr [eax + 0xc], edx
0048d8ec  7418                     je 0x48d906
0048d8ee  385020                   cmp byte ptr [eax + 0x20], dl
0048d8f1  895010                   mov dword ptr [eax + 0x10], edx
0048d8f4  895014                   mov dword ptr [eax + 0x14], edx
0048d8f7  49                       dec ecx
0048d8f8  895018                   mov dword ptr [eax + 0x18], edx
0048d8fb  89501c                   mov dword ptr [eax + 0x1c], edx
0048d8fe  8d4020                   lea eax, [eax + 0x20]
0048d901  75dd                     jne 0x48d8e0
0048d903  8d40f0                   lea eax, [eax - 0x10]
0048d906  8d4010                   lea eax, [eax + 0x10]
0048d909  8910                     mov dword ptr [eax], edx
0048d90b  895004                   mov dword ptr [eax + 4], edx
0048d90e  895008                   mov dword ptr [eax + 8], edx
0048d911  89500c                   mov dword ptr [eax + 0xc], edx
0048d914  8d4010                   lea eax, [eax + 0x10]
0048d917  59                       pop ecx
0048d918  83e103                   and ecx, 3
0048d91b  7415                     je 0x48d932
0048d91d  8910                     mov dword ptr [eax], edx
0048d91f  8d4004                   lea eax, [eax + 4]
0048d922  49                       dec ecx
0048d923  740d                     je 0x48d932
0048d925  8910                     mov dword ptr [eax], edx
0048d927  8d4004                   lea eax, [eax + 4]
0048d92a  49                       dec ecx
0048d92b  7405                     je 0x48d932
0048d92d  8910                     mov dword ptr [eax], edx
0048d92f  8d4004                   lea eax, [eax + 4]
0048d932  c3                       ret
0048d933  52                       push edx
0048d934  89c2                     mov edx, eax
0048d936  ff12                     call dword ptr [edx]
0048d938  5a                       pop edx
0048d939  c3                       ret
0048d93a  53                       push ebx
0048d93b  89d3                     mov ebx, edx
0048d93d  ff5304                   call dword ptr [ebx + 4]
0048d940  5b                       pop ebx
0048d941  c3                       ret
; __prtf 0x0048efe8..0x0048fb01: Watcom CRT, hash only
