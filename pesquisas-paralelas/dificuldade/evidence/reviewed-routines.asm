; Static disassembly only; no original execution.
; Original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb

; InitEntrerMonstre 0x47a601..0x47a81d sha256 2e6140e96408377d3ea63f3a4d88338d6dc8e183629f275c87c3fd08c21a852f
0047a601  53                       push ebx
0047a602  51                       push ecx
0047a603  52                       push edx
0047a604  56                       push esi
0047a605  57                       push edi
0047a606  55                       push ebp
0047a607  81ec1c010000             sub esp, 0x11c
0047a60d  31db                     xor ebx, ebx
0047a60f  83c30c                   add ebx, 0xc
0047a612  baffff0000               mov edx, 0xffff
0047a617  668993c4a95000           mov word ptr [ebx + 0x50a9c4], dx
0047a61e  31f6                     xor esi, esi
0047a620  668993c6a95000           mov word ptr [ebx + 0x50a9c6], dx
0047a627  6689b3c8a95000           mov word ptr [ebx + 0x50a9c8], si
0047a62e  31d2                     xor edx, edx
0047a630  31c0                     xor eax, eax
0047a632  8993cca95000             mov dword ptr [ebx + 0x50a9cc], edx
0047a638  e89f5effff               call 0x4704dc
0047a63d  240f                     and al, 0xf
0047a63f  8883caa95000             mov byte ptr [ebx + 0x50a9ca], al
0047a645  81fbb0040000             cmp ebx, 0x4b0
0047a64b  75c2                     jne 0x47a60f
0047a64d  684c4e4900               push 0x494e4c
0047a652  52                       push edx
0047a653  685a4e4900               push 0x494e5a
0047a658  30e4                     xor ah, ah
0047a65a  68644e4900               push 0x494e64
0047a65f  8825bca95000             mov byte ptr [0x50a9bc], ah
0047a665  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047a66c  85c0                     test eax, eax
0047a66e  7407                     je 0x47a677
0047a670  c605bca9500001           mov byte ptr [0x50a9bc], 1
0047a677  686c4e4900               push 0x494e6c
0047a67c  6a05                     push 5
0047a67e  687a4e4900               push 0x494e7a
0047a683  688a4e4900               push 0x494e8a
0047a688  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047a68f  68924e4900               push 0x494e92
0047a694  6a02                     push 2
0047a696  68a04e4900               push 0x494ea0
0047a69b  68ac4e4900               push 0x494eac
0047a6a0  a3c0a95000               mov dword ptr [0x50a9c0], eax
0047a6a5  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047a6ac  68b44e4900               push 0x494eb4
0047a6b1  6a02                     push 2
0047a6b3  68c24e4900               push 0x494ec2
0047a6b8  68d14e4900               push 0x494ed1
0047a6bd  bba0010000               mov ebx, 0x1a0
0047a6c2  a3c4a95000               mov dword ptr [0x50a9c4], eax
0047a6c7  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047a6ce  a3c8a95000               mov dword ptr [0x50a9c8], eax
0047a6d3  31d2                     xor edx, edx
0047a6d5  b884af5000               mov eax, 0x50af84
0047a6da  e8d11c0100               call 0x48c3b0
0047a6df  bb10000000               mov ebx, 0x10
0047a6e4  b824b15000               mov eax, 0x50b124
0047a6e9  31d2                     xor edx, edx
0047a6eb  e8c01c0100               call 0x48c3b0
0047a6f0  31db                     xor ebx, ebx
0047a6f2  899c2410010000           mov dword ptr [esp + 0x110], ebx
0047a6f9  eb1b                     jmp 0x47a716
0047a6fb  8bb42410010000           mov esi, dword ptr [esp + 0x110]
0047a702  83c61a                   add esi, 0x1a
0047a705  43                       inc ebx
0047a706  89b42410010000           mov dword ptr [esp + 0x110], esi
0047a70d  83fb10                   cmp ebx, 0x10
0047a710  0f8dfa000000             jge 0x47a810
0047a716  53                       push ebx
0047a717  68d94e4900               push 0x494ed9
0047a71c  8d842408010000           lea eax, [esp + 0x108]
0047a723  50                       push eax
0047a724  e892280100               call 0x48cfbb
0047a729  83c40c                   add esp, 0xc
0047a72c  68e44e4900               push 0x494ee4
0047a731  6800010000               push 0x100
0047a736  8d442408                 lea eax, [esp + 8]
0047a73a  50                       push eax
0047a73b  68f24e4900               push 0x494ef2
0047a740  8d842410010000           lea eax, [esp + 0x110]
0047a747  50                       push eax
0047a748  68f34e4900               push 0x494ef3
0047a74d  2eff15b0315200           call dword ptr cs:[0x5231b0]
0047a754  89842418010000           mov dword ptr [esp + 0x118], eax
0047a75b  85c0                     test eax, eax
0047a75d  749c                     je 0x47a6fb
0047a75f  89e5                     mov ebp, esp
0047a761  b101                     mov cl, 1
0047a763  8b842410010000           mov eax, dword ptr [esp + 0x110]
0047a76a  b22c                     mov dl, 0x2c
0047a76c  89842414010000           mov dword ptr [esp + 0x114], eax
0047a773  89ee                     mov esi, ebp
0047a775  8a06                     mov al, byte ptr [esi]
0047a777  3ac2                     cmp al, dl
0047a779  7412                     je 0x47a78d
0047a77b  3c00                     cmp al, 0
0047a77d  740c                     je 0x47a78b
0047a77f  46                       inc esi
0047a780  8a06                     mov al, byte ptr [esi]
0047a782  3ac2                     cmp al, dl
0047a784  7407                     je 0x47a78d
0047a786  46                       inc esi
0047a787  3c00                     cmp al, 0
0047a789  75ea                     jne 0x47a775
0047a78b  2bf6                     sub esi, esi
0047a78d  89f7                     mov edi, esi
0047a78f  85f6                     test esi, esi
0047a791  7512                     jne 0x47a7a5
0047a793  89e7                     mov edi, esp
0047a795  29c9                     sub ecx, ecx
0047a797  49                       dec ecx
0047a798  31c0                     xor eax, eax
0047a79a  f2ae                     repne scasb al, byte ptr es:[edi]
0047a79c  f7d1                     not ecx
0047a79e  49                       dec ecx
0047a79f  89e7                     mov edi, esp
0047a7a1  01cf                     add edi, ecx
0047a7a3  30c9                     xor cl, cl
0047a7a5  8d842418010000           lea eax, [esp + 0x118]
0047a7ac  50                       push eax
0047a7ad  68fb4e4900               push 0x494efb
0047a7b2  55                       push ebp
0047a7b3  e8641c0100               call 0x48c41c
0047a7b8  83c40c                   add esp, 0xc
0047a7bb  83f801                   cmp eax, 1
0047a7be  7540                     jne 0x47a800
0047a7c0  8bb42418010000           mov esi, dword ptr [esp + 0x118]
0047a7c7  31c0                     xor eax, eax
0047a7c9  8a8600844900             mov al, byte ptr [esi + 0x498400]
0047a7cf  89842418010000           mov dword ptr [esp + 0x118], eax
0047a7d6  8b842414010000           mov eax, dword ptr [esp + 0x114]
0047a7dd  03842418010000           add eax, dword ptr [esp + 0x118]
0047a7e4  8aab24b15000             mov ch, byte ptr [ebx + 0x50b124]
0047a7ea  8ab084af5000             mov dh, byte ptr [eax + 0x50af84]
0047a7f0  fec5                     inc ch
0047a7f2  fec6                     inc dh
0047a7f4  88ab24b15000             mov byte ptr [ebx + 0x50b124], ch
0047a7fa  88b084af5000             mov byte ptr [eax + 0x50af84], dh
0047a800  8d6f01                   lea ebp, [edi + 1]
0047a803  84c9                     test cl, cl
0047a805  0f8568ffffff             jne 0x47a773
0047a80b  e9ebfeffff               jmp 0x47a6fb
0047a810  81c41c010000             add esp, 0x11c
0047a816  5d                       pop ebp
0047a817  5f                       pop edi
0047a818  5e                       pop esi
0047a819  5a                       pop edx
0047a81a  59                       pop ecx
0047a81b  5b                       pop ebx
0047a81c  c3                       ret

; ReadConfigMonstre 0x47aba9..0x47ac30 sha256 3996046f71630fbb178e635f3babab477c3bc46960451eb59e0faf2e5bbe7491
0047aba9  51                       push ecx
0047abaa  52                       push edx
0047abab  684c4e4900               push 0x494e4c
0047abb0  6a00                     push 0
0047abb2  685a4e4900               push 0x494e5a
0047abb7  30e4                     xor ah, ah
0047abb9  68644e4900               push 0x494e64
0047abbe  8825bca95000             mov byte ptr [0x50a9bc], ah
0047abc4  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047abcb  85c0                     test eax, eax
0047abcd  7407                     je 0x47abd6
0047abcf  c605bca9500001           mov byte ptr [0x50a9bc], 1
0047abd6  686c4e4900               push 0x494e6c
0047abdb  6a05                     push 5
0047abdd  687a4e4900               push 0x494e7a
0047abe2  688a4e4900               push 0x494e8a
0047abe7  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047abee  68924e4900               push 0x494e92
0047abf3  6a02                     push 2
0047abf5  68a04e4900               push 0x494ea0
0047abfa  68ac4e4900               push 0x494eac
0047abff  a3c0a95000               mov dword ptr [0x50a9c0], eax
0047ac04  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047ac0b  68b44e4900               push 0x494eb4
0047ac10  6a02                     push 2
0047ac12  68c24e4900               push 0x494ec2
0047ac17  68d14e4900               push 0x494ed1
0047ac1c  a3c4a95000               mov dword ptr [0x50a9c4], eax
0047ac21  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047ac28  a3c8a95000               mov dword ptr [0x50a9c8], eax
0047ac2d  5a                       pop edx
0047ac2e  59                       pop ecx
0047ac2f  c3                       ret

; LoadEntrerMonstre 0x47ac30..0x47ad6a sha256 e623b7fa891620a4bfd65509458ec7a2ac0cf1d16eac5bb0af8123ccb1ca7fec
0047ac30  53                       push ebx
0047ac31  51                       push ecx
0047ac32  52                       push edx
0047ac33  56                       push esi
0047ac34  57                       push edi
0047ac35  55                       push ebp
0047ac36  83ec0c                   sub esp, 0xc
0047ac39  31d2                     xor edx, edx
0047ac3b  89542404                 mov dword ptr [esp + 4], edx
0047ac3f  e8bdf9ffff               call 0x47a601
0047ac44  ba02000000               mov edx, 2
0047ac49  b8cea95000               mov eax, 0x50a9ce
0047ac4e  e80ed8fdff               call 0x458461
0047ac53  ba02000000               mov edx, 2
0047ac58  8d442404                 lea eax, [esp + 4]
0047ac5c  bdd0a95000               mov ebp, 0x50a9d0
0047ac61  e8fbd7fdff               call 0x458461
0047ac66  31d2                     xor edx, edx
0047ac68  31f6                     xor esi, esi
0047ac6a  891424                   mov dword ptr [esp], edx
0047ac6d  eb13                     jmp 0x47ac82
0047ac6f  8b3c24                   mov edi, dword ptr [esp]
0047ac72  83c60c                   add esi, 0xc
0047ac75  83c50c                   add ebp, 0xc
0047ac78  47                       inc edi
0047ac79  8886caa95000             mov byte ptr [esi + 0x50a9ca], al
0047ac7f  893c24                   mov dword ptr [esp], edi
0047ac82  31ff                     xor edi, edi
0047ac84  8b1c24                   mov ebx, dword ptr [esp]
0047ac87  668b3dcea95000           mov di, word ptr [0x50a9ce]
0047ac8e  39df                     cmp edi, ebx
0047ac90  7e5a                     jle 0x47acec
0047ac92  31d2                     xor edx, edx
0047ac94  89e8                     mov eax, ebp
0047ac96  668b542404               mov dx, word ptr [esp + 4]
0047ac9b  e8c1d7fdff               call 0x458461
0047aca0  668b9ed4a95000           mov bx, word ptr [esi + 0x50a9d4]
0047aca7  6bc31e                   imul eax, ebx, 0x1e
0047acaa  668986d4a95000           mov word ptr [esi + 0x50a9d4], ax
0047acb1  31c9                     xor ecx, ecx
0047acb3  668bbed2a95000           mov di, word ptr [esi + 0x50a9d2]
0047acba  8a86d6a95000             mov al, byte ptr [esi + 0x50a9d6]
0047acc0  898ed8a95000             mov dword ptr [esi + 0x50a9d8], ecx
0047acc6  b410                     mov ah, 0x10
0047acc8  fec0                     inc al
0047acca  240f                     and al, 0xf
0047accc  ba01000000               mov edx, 1
0047acd1  88c1                     mov cl, al
0047acd3  d3e2                     shl edx, cl
0047acd5  31db                     xor ebx, ebx
0047acd7  81e2ffff0000             and edx, 0xffff
0047acdd  6689fb                   mov bx, di
0047ace0  85da                     test edx, ebx
0047ace2  758b                     jne 0x47ac6f
0047ace4  fecc                     dec ah
0047ace6  75e0                     jne 0x47acc8
0047ace8  b0ff                     mov al, 0xff
0047acea  eb83                     jmp 0x47ac6f
0047acec  4f                       dec edi
0047aced  89f9                     mov ecx, edi
0047acef  c1e102                   shl ecx, 2
0047acf2  29f9                     sub ecx, edi
0047acf4  c1e102                   shl ecx, 2
0047acf7  eb04                     jmp 0x47acfd
0047acf9  83e90c                   sub ecx, 0xc
0047acfc  4f                       dec edi
0047acfd  85ff                     test edi, edi
0047acff  7c61                     jl 0x47ad62
0047ad01  31c0                     xor eax, eax
0047ad03  668b81d0a95000           mov ax, word ptr [ecx + 0x50a9d0]
0047ad0a  3dffff0000               cmp eax, 0xffff
0047ad0f  7509                     jne 0x47ad1a
0047ad11  66ff0dcea95000           dec word ptr [0x50a9ce]
0047ad18  ebdf                     jmp 0x47acf9
0047ad1a  30e4                     xor ah, ah
0047ad1c  8d57ff                   lea edx, [edi - 1]
0047ad1f  88642408                 mov byte ptr [esp + 8], ah
0047ad23  6bc20c                   imul eax, edx, 0xc
0047ad26  eb04                     jmp 0x47ad2c
0047ad28  83e80c                   sub eax, 0xc
0047ad2b  4a                       dec edx
0047ad2c  85c0                     test eax, eax
0047ad2e  7c2b                     jl 0x47ad5b
0047ad30  31db                     xor ebx, ebx
0047ad32  668b98d0a95000           mov bx, word ptr [eax + 0x50a9d0]
0047ad39  81fbffff0000             cmp ebx, 0xffff
0047ad3f  75e7                     jne 0x47ad28
0047ad41  c644240801               mov byte ptr [esp + 8], 1
0047ad46  668b91d0a95000           mov dx, word ptr [ecx + 0x50a9d0]
0047ad4d  668990d0a95000           mov word ptr [eax + 0x50a9d0], dx
0047ad54  66ff0dcea95000           dec word ptr [0x50a9ce]
0047ad5b  807c240800               cmp byte ptr [esp + 8], 0
0047ad60  7597                     jne 0x47acf9
0047ad62  83c40c                   add esp, 0xc
0047ad65  e9acfaffff               jmp 0x47a816

; AvanceMonstre_and_wait_response_prefix 0x47b283..0x47b6f1 sha256 f0fe987dd7b4352431f4a16a4d32dab62b19122978d5610307dd08155ee3f90e
0047b283  53                       push ebx
0047b284  51                       push ecx
0047b285  52                       push edx
0047b286  56                       push esi
0047b287  57                       push edi
0047b288  55                       push ebp
0047b289  89e5                     mov ebp, esp
0047b28b  83ec44                   sub esp, 0x44
0047b28e  31c0                     xor eax, eax
0047b290  a0cca95000               mov al, byte ptr [0x50a9cc]
0047b295  85c0                     test eax, eax
0047b297  752b                     jne 0x47b2c4
0047b299  b401                     mov ah, 1
0047b29b  31d2                     xor edx, edx
0047b29d  8825cca95000             mov byte ptr [0x50a9cc], ah
0047b2a3  31c0                     xor eax, eax
0047b2a5  eb10                     jmp 0x47b2b7
0047b2a7  83c00c                   add eax, 0xc
0047b2aa  8b1d7c8f5000             mov ebx, dword ptr [0x508f7c]
0047b2b0  42                       inc edx
0047b2b1  8998cca95000             mov dword ptr [eax + 0x50a9cc], ebx
0047b2b7  31db                     xor ebx, ebx
0047b2b9  668b1dcea95000           mov bx, word ptr [0x50a9ce]
0047b2c0  39da                     cmp edx, ebx
0047b2c2  7ce3                     jl 0x47b2a7
0047b2c4  e8510effff               call 0x46c11a
0047b2c9  25ffff0000               and eax, 0xffff
0047b2ce  83f817                   cmp eax, 0x17
0047b2d1  7546                     jne 0x47b319
0047b2d3  8a1534b15000             mov dl, byte ptr [0x50b134]
0047b2d9  84d2                     test dl, dl
0047b2db  0f84f3030000             je 0x47b6d4
0047b2e1  6a00                     push 0
0047b2e3  6a00                     push 0
0047b2e5  b804000000               mov eax, 4
0047b2ea  31db                     xor ebx, ebx
0047b2ec  6a00                     push 0
0047b2ee  31c9                     xor ecx, ecx
0047b2f0  88d3                     mov bl, dl
0047b2f2  6a00                     push 0
0047b2f4  ba12000000               mov edx, 0x12
0047b2f9  8b1c9d34b15000           mov ebx, dword ptr [ebx*4 + 0x50b134]
0047b300  e81b260000               call 0x47d920
0047b305  83f8ff                   cmp eax, -1
0047b308  0f84c6030000             je 0x47b6d4
0047b30e  fe0d34b15000             dec byte ptr [0x50b134]
0047b314  e9bb030000               jmp 0x47b6d4
0047b319  a17c8f5000               mov eax, dword ptr [0x508f7c]
0047b31e  8945e4                   mov dword ptr [ebp - 0x1c], eax
0047b321  31c0                     xor eax, eax
0047b323  66a1cea95000             mov ax, word ptr [0x50a9ce]
0047b329  bed0a95000               mov esi, 0x50a9d0
0047b32e  8945ec                   mov dword ptr [ebp - 0x14], eax
0047b331  85c0                     test eax, eax
0047b333  7462                     je 0x47b397
0047b335  31c0                     xor eax, eax
0047b337  668b4604                 mov ax, word ptr [esi + 4]
0047b33b  85c0                     test eax, eax
0047b33d  744c                     je 0x47b38b
0047b33f  8b55e4                   mov edx, dword ptr [ebp - 0x1c]
0047b342  2b5608                   sub edx, dword ptr [esi + 8]
0047b345  39c2                     cmp edx, eax
0047b347  7c42                     jl 0x47b38b
0047b349  8a4606                   mov al, byte ptr [esi + 6]
0047b34c  668b7e02                 mov di, word ptr [esi + 2]
0047b350  b410                     mov ah, 0x10
0047b352  fec0                     inc al
0047b354  240f                     and al, 0xf
0047b356  ba01000000               mov edx, 1
0047b35b  88c1                     mov cl, al
0047b35d  31db                     xor ebx, ebx
0047b35f  d3e2                     shl edx, cl
0047b361  6689d3                   mov bx, dx
0047b364  31d2                     xor edx, edx
0047b366  6689fa                   mov dx, di
0047b369  85d3                     test ebx, edx
0047b36b  7506                     jne 0x47b373
0047b36d  fecc                     dec ah
0047b36f  75e1                     jne 0x47b352
0047b371  b0ff                     mov al, 0xff
0047b373  884606                   mov byte ptr [esi + 6], al
0047b376  8b45e4                   mov eax, dword ptr [ebp - 0x1c]
0047b379  31d2                     xor edx, edx
0047b37b  894608                   mov dword ptr [esi + 8], eax
0047b37e  31c0                     xor eax, eax
0047b380  8a5606                   mov dl, byte ptr [esi + 6]
0047b383  668b06                   mov ax, word ptr [esi]
0047b386  e892f4ffff               call 0x47a81d
0047b38b  8b4dec                   mov ecx, dword ptr [ebp - 0x14]
0047b38e  83c60c                   add esi, 0xc
0047b391  49                       dec ecx
0047b392  894dec                   mov dword ptr [ebp - 0x14], ecx
0047b395  759e                     jne 0x47b335
0047b397  bfc2010000               mov edi, 0x1c2
0047b39c  31f6                     xor esi, esi
0047b39e  eb01                     jmp 0x47b3a1
0047b3a0  46                       inc esi
0047b3a1  3b3580ae5000             cmp esi, dword ptr [0x50ae80]
0047b3a7  0f8d92000000             jge 0x47b43f
0047b3ad  89f2                     mov edx, esi
0047b3af  c1e204                   shl edx, 4
0047b3b2  31c0                     xor eax, eax
0047b3b4  668b8292ae5000           mov ax, word ptr [edx + 0x50ae92]
0047b3bb  83f831                   cmp eax, 0x31
0047b3be  75e0                     jne 0x47b3a0
0047b3c0  8b9a8cae5000             mov ebx, dword ptr [edx + 0x50ae8c]
0047b3c6  4b                       dec ebx
0047b3c7  899a8cae5000             mov dword ptr [edx + 0x50ae8c], ebx
0047b3cd  85db                     test ebx, ebx
0047b3cf  7fcf                     jg 0x47b3a0
0047b3d1  8b8288ae5000             mov eax, dword ptr [edx + 0x50ae88]
0047b3d7  31db                     xor ebx, ebx
0047b3d9  89ba8cae5000             mov dword ptr [edx + 0x50ae8c], edi
0047b3df  e80c840000               call 0x4837f0
0047b3e4  6689c3                   mov bx, ax
0047b3e7  81fbffff0000             cmp ebx, 0xffff
0047b3ed  7524                     jne 0x47b413
0047b3ef  31c0                     xor eax, eax
0047b3f1  8945bc                   mov dword ptr [ebp - 0x44], eax
0047b3f4  8b8288ae5000             mov eax, dword ptr [edx + 0x50ae88]
0047b3fa  8945c0                   mov dword ptr [ebp - 0x40], eax
0047b3fd  8d45bc                   lea eax, [ebp - 0x44]
0047b400  e8d6020000               call 0x47b6db
0047b405  8b55c0                   mov edx, dword ptr [ebp - 0x40]
0047b408  b804000000               mov eax, 4
0047b40d  4e                       dec esi
0047b40e  e8d4880000               call 0x483ce7
0047b413  89f1                     mov ecx, esi
0047b415  c1e104                   shl ecx, 4
0047b418  81fbffff0000             cmp ebx, 0xffff
0047b41e  7480                     je 0x47b3a0
0047b420  31c0                     xor eax, eax
0047b422  31d2                     xor edx, edx
0047b424  6689d8                   mov ax, bx
0047b427  668b9190ae5000           mov dx, word ptr [ecx + 0x50ae90]
0047b42e  e8a0a3fcff               call 0x4457d3
0047b433  31db                     xor ebx, ebx
0047b435  e8eb830000               call 0x483825
0047b43a  6689c3                   mov bx, ax
0047b43d  ebd9                     jmp 0x47b418
0047b43f  803d34b1500000           cmp byte ptr [0x50b134], 0
0047b446  0f8488020000             je 0x47b6d4
0047b44c  31c0                     xor eax, eax
0047b44e  e88950ffff               call 0x4704dc
0047b453  83e003                   and eax, 3
0047b456  40                       inc eax
0047b457  8945fc                   mov dword ptr [ebp - 4], eax
0047b45a  83f804                   cmp eax, 4
0047b45d  7c05                     jl 0x47b464
0047b45f  31db                     xor ebx, ebx
0047b461  895dfc                   mov dword ptr [ebp - 4], ebx
0047b464  803dbca9500000           cmp byte ptr [0x50a9bc], 0
0047b46b  7414                     je 0x47b481
0047b46d  31c0                     xor eax, eax
0047b46f  8a45fc                   mov al, byte ptr [ebp - 4]
0047b472  e8a023ffff               call 0x46d817
0047b477  25ff000000               and eax, 0xff
0047b47c  83f802                   cmp eax, 2
0047b47f  74cb                     je 0x47b44c
0047b481  0fb63534b15000           movzx esi, byte ptr [0x50b134]
0047b488  8b34b534b15000           mov esi, dword ptr [esi*4 + 0x50b134]
0047b48f  89f0                     mov eax, esi
0047b491  31db                     xor ebx, ebx
0047b493  e858830000               call 0x4837f0
0047b498  6689c3                   mov bx, ax
0047b49b  81fbffff0000             cmp ebx, 0xffff
0047b4a1  7511                     jne 0x47b4b4
0047b4a3  b804000000               mov eax, 4
0047b4a8  89f2                     mov edx, esi
0047b4aa  e838880000               call 0x483ce7
0047b4af  e95afeffff               jmp 0x47b30e
0047b4b4  81e3ffff0000             and ebx, 0xffff
0047b4ba  89d8                     mov eax, ebx
0047b4bc  b964000000               mov ecx, 0x64
0047b4c1  e8785cfcff               call 0x44113e
0047b4c6  89c7                     mov edi, eax
0047b4c8  31c0                     xor eax, eax
0047b4ca  31d2                     xor edx, edx
0047b4cc  e80b50ffff               call 0x4704dc
0047b4d1  f7f1                     div ecx
0047b4d3  89d8                     mov eax, ebx
0047b4d5  8955e0                   mov dword ptr [ebp - 0x20], edx
0047b4d8  e8486bfcff               call 0x442025
0047b4dd  25ff000000               and eax, 0xff
0047b4e2  83f818                   cmp eax, 0x18
0047b4e5  7549                     jne 0x47b530
0047b4e7  31c9                     xor ecx, ecx
0047b4e9  894df0                   mov dword ptr [ebp - 0x10], ecx
0047b4ec  eb03                     jmp 0x47b4f1
0047b4ee  ff45f0                   inc dword ptr [ebp - 0x10]
0047b4f1  837df014                 cmp dword ptr [ebp - 0x10], 0x14
0047b4f5  7d39                     jge 0x47b530
0047b4f7  31db                     xor ebx, ebx
0047b4f9  e849dc0000               call 0x489147
0047b4fe  6689c3                   mov bx, ax
0047b501  81fbffff0000             cmp ebx, 0xffff
0047b507  7427                     je 0x47b530
0047b509  31c9                     xor ecx, ecx
0047b50b  6689f9                   mov cx, di
0047b50e  89da                     mov edx, ebx
0047b510  89c8                     mov eax, ecx
0047b512  e8e11ffbff               call 0x42d4f8
0047b517  84c0                     test al, al
0047b519  74d3                     je 0x47b4ee
0047b51b  b831000000               mov eax, 0x31
0047b520  89f2                     mov edx, esi
0047b522  e873f4ffff               call 0x47a99a
0047b527  84c0                     test al, al
0047b529  74c3                     je 0x47b4ee
0047b52b  e9defdffff               jmp 0x47b30e
0047b530  8b45e0                   mov eax, dword ptr [ebp - 0x20]
0047b533  8b1dc0a95000             mov ebx, dword ptr [0x50a9c0]
0047b539  39d8                     cmp eax, ebx
0047b53b  7d12                     jge 0x47b54f
0047b53d  31d2                     xor edx, edx
0047b53f  8a1541805000             mov dl, byte ptr [0x508041]
0047b545  31c0                     xor eax, eax
0047b547  8955fc                   mov dword ptr [ebp - 4], edx
0047b54a  e933000000               jmp 0x47b582
0047b54f  8b0dc4a95000             mov ecx, dword ptr [0x50a9c4]
0047b555  8b55e0                   mov edx, dword ptr [ebp - 0x20]
0047b558  8d040b                   lea eax, [ebx + ecx]
0047b55b  39d0                     cmp eax, edx
0047b55d  7e0a                     jle 0x47b569
0047b55f  b801000000               mov eax, 1
0047b564  e919000000               jmp 0x47b582
0047b569  0305c8a95000             add eax, dword ptr [0x50a9c8]
0047b56f  39d0                     cmp eax, edx
0047b571  7e0a                     jle 0x47b57d
0047b573  b802000000               mov eax, 2
0047b578  e905000000               jmp 0x47b582
0047b57d  b803000000               mov eax, 3
0047b582  83f801                   cmp eax, 1
0047b585  0f86af000000             jbe 0x47b63a
0047b58b  83f802                   cmp eax, 2
0047b58e  0f85f7000000             jne 0x47b68b
0047b594  31c0                     xor eax, eax
0047b596  8945f8                   mov dword ptr [ebp - 8], eax
0047b599  eb03                     jmp 0x47b59e
0047b59b  ff45f8                   inc dword ptr [ebp - 8]
0047b59e  837df814                 cmp dword ptr [ebp - 8], 0x14
0047b5a2  0f8d92000000             jge 0x47b63a
0047b5a8  31db                     xor ebx, ebx
0047b5aa  eb01                     jmp 0x47b5ad
0047b5ac  43                       inc ebx
0047b5ad  31c0                     xor eax, eax
0047b5af  66a1cea95000             mov ax, word ptr [0x50a9ce]
0047b5b5  39c3                     cmp ebx, eax
0047b5b7  7d40                     jge 0x47b5f9
0047b5b9  8b0dd4235200             mov ecx, dword ptr [0x5223d4]
0047b5bf  41                       inc ecx
0047b5c0  890dd4235200             mov dword ptr [0x5223d4], ecx
0047b5c6  39c8                     cmp eax, ecx
0047b5c8  7f08                     jg 0x47b5d2
0047b5ca  31c9                     xor ecx, ecx
0047b5cc  890dd4235200             mov dword ptr [0x5223d4], ecx
0047b5d2  6b05d42352000c           imul eax, dword ptr [0x5223d4], 0xc
0047b5d9  31d2                     xor edx, edx
0047b5db  668b90d4a95000           mov dx, word ptr [eax + 0x50a9d4]
0047b5e2  85d2                     test edx, edx
0047b5e4  75c6                     jne 0x47b5ac
0047b5e6  668b90d0a95000           mov dx, word ptr [eax + 0x50a9d0]
0047b5ed  81faffff0000             cmp edx, 0xffff
0047b5f3  74b7                     je 0x47b5ac
0047b5f5  89d0                     mov eax, edx
0047b5f7  eb05                     jmp 0x47b5fe
0047b5f9  b8ffff0000               mov eax, 0xffff
0047b5fe  31db                     xor ebx, ebx
0047b600  6689c3                   mov bx, ax
0047b603  81fbffff0000             cmp ebx, 0xffff
0047b609  742f                     je 0x47b63a
0047b60b  31c9                     xor ecx, ecx
0047b60d  6689f9                   mov cx, di
0047b610  89da                     mov edx, ebx
0047b612  89c8                     mov eax, ecx
0047b614  e8df1efbff               call 0x42d4f8
0047b619  84c0                     test al, al
0047b61b  0f847affffff             je 0x47b59b
0047b621  b82e000000               mov eax, 0x2e
0047b626  89f2                     mov edx, esi
0047b628  e86df3ffff               call 0x47a99a
0047b62d  84c0                     test al, al
0047b62f  0f8466ffffff             je 0x47b59b
0047b635  e9d4fcffff               jmp 0x47b30e
0047b63a  31c9                     xor ecx, ecx
0047b63c  894de8                   mov dword ptr [ebp - 0x18], ecx
0047b63f  eb03                     jmp 0x47b644
0047b641  ff45e8                   inc dword ptr [ebp - 0x18]
0047b644  837de814                 cmp dword ptr [ebp - 0x18], 0x14
0047b648  7d41                     jge 0x47b68b
0047b64a  ba03000000               mov edx, 3
0047b64f  8b45fc                   mov eax, dword ptr [ebp - 4]
0047b652  31db                     xor ebx, ebx
0047b654  e8a7dc0000               call 0x489300
0047b659  6689c3                   mov bx, ax
0047b65c  81fbffff0000             cmp ebx, 0xffff
0047b662  7427                     je 0x47b68b
0047b664  31c9                     xor ecx, ecx
0047b666  6689f9                   mov cx, di
0047b669  89da                     mov edx, ebx
0047b66b  89c8                     mov eax, ecx
0047b66d  e8861efbff               call 0x42d4f8
0047b672  84c0                     test al, al
0047b674  74cb                     je 0x47b641
0047b676  b830000000               mov eax, 0x30
0047b67b  89f2                     mov edx, esi
0047b67d  e818f3ffff               call 0x47a99a
0047b682  84c0                     test al, al
0047b684  74bb                     je 0x47b641
0047b686  e983fcffff               jmp 0x47b30e
0047b68b  31db                     xor ebx, ebx
0047b68d  895df4                   mov dword ptr [ebp - 0xc], ebx
0047b690  eb03                     jmp 0x47b695
0047b692  ff45f4                   inc dword ptr [ebp - 0xc]
0047b695  837df414                 cmp dword ptr [ebp - 0xc], 0x14
0047b699  7d39                     jge 0x47b6d4
0047b69b  31db                     xor ebx, ebx
0047b69d  e8a5da0000               call 0x489147
0047b6a2  6689c3                   mov bx, ax
0047b6a5  81fbffff0000             cmp ebx, 0xffff
0047b6ab  7427                     je 0x47b6d4
0047b6ad  31c9                     xor ecx, ecx
0047b6af  6689f9                   mov cx, di
0047b6b2  89da                     mov edx, ebx
0047b6b4  89c8                     mov eax, ecx
0047b6b6  e83d1efbff               call 0x42d4f8
0047b6bb  84c0                     test al, al
0047b6bd  74d3                     je 0x47b692
0047b6bf  b82f000000               mov eax, 0x2f
0047b6c4  89f2                     mov edx, esi
0047b6c6  e8cff2ffff               call 0x47a99a
0047b6cb  84c0                     test al, al
0047b6cd  74c3                     je 0x47b692
0047b6cf  e93afcffff               jmp 0x47b30e
0047b6d4  89ec                     mov esp, ebp
0047b6d6  e93bf1ffff               jmp 0x47a816
0047b6db  53                       push ebx
0047b6dc  51                       push ecx
0047b6dd  52                       push edx
0047b6de  56                       push esi
0047b6df  57                       push edi
0047b6e0  8b30                     mov esi, dword ptr [eax]
0047b6e2  8b4804                   mov ecx, dword ptr [eax + 4]
0047b6e5  85f6                     test esi, esi
0047b6e7  7605                     jbe 0x47b6ee
0047b6e9  83fe01                   cmp esi, 1
0047b6ec  740f                     je 0x47b6fd
0047b6ee  8b                       .byte 0x8b
0047b6ef  1d                       .byte 0x1d
0047b6f0  80                       .byte 0x80

; ChargeMonstre 0x47b796..0x47b8e8 sha256 f017986d566cbfcbeb7e2c3b7bcc3ddd81d9a8ca037d43984e6ffdaf58cd9c42
0047b796  53                       push ebx
0047b797  51                       push ecx
0047b798  52                       push edx
0047b799  83ec04                   sub esp, 4
0047b79c  684c4e4900               push 0x494e4c
0047b7a1  6a00                     push 0
0047b7a3  685a4e4900               push 0x494e5a
0047b7a8  30e4                     xor ah, ah
0047b7aa  68644e4900               push 0x494e64
0047b7af  8825bca95000             mov byte ptr [0x50a9bc], ah
0047b7b5  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047b7bc  85c0                     test eax, eax
0047b7be  7407                     je 0x47b7c7
0047b7c0  c605bca9500001           mov byte ptr [0x50a9bc], 1
0047b7c7  686c4e4900               push 0x494e6c
0047b7cc  6a05                     push 5
0047b7ce  687a4e4900               push 0x494e7a
0047b7d3  688a4e4900               push 0x494e8a
0047b7d8  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047b7df  68924e4900               push 0x494e92
0047b7e4  6a02                     push 2
0047b7e6  68a04e4900               push 0x494ea0
0047b7eb  68ac4e4900               push 0x494eac
0047b7f0  a3c0a95000               mov dword ptr [0x50a9c0], eax
0047b7f5  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047b7fc  68b44e4900               push 0x494eb4
0047b801  6a02                     push 2
0047b803  68c24e4900               push 0x494ec2
0047b808  68d14e4900               push 0x494ed1
0047b80d  a3c4a95000               mov dword ptr [0x50a9c4], eax
0047b812  2eff15ac315200           call dword ptr cs:[0x5231ac]
0047b819  ba04000000               mov edx, 4
0047b81e  a3c8a95000               mov dword ptr [0x50a9c8], eax
0047b823  89e0                     mov eax, esp
0047b825  e837ccfdff               call 0x458461
0047b82a  ba01000000               mov edx, 1
0047b82f  b8cca95000               mov eax, 0x50a9cc
0047b834  e828ccfdff               call 0x458461
0047b839  ba04000000               mov edx, 4
0047b83e  b880ae5000               mov eax, 0x50ae80
0047b843  e819ccfdff               call 0x458461
0047b848  ba04000000               mov edx, 4
0047b84d  b878b15000               mov eax, 0x50b178
0047b852  e80accfdff               call 0x458461
0047b857  ba02000000               mov edx, 2
0047b85c  b8cea95000               mov eax, 0x50a9ce
0047b861  e8fbcbfdff               call 0x458461
0047b866  ba01000000               mov edx, 1
0047b86b  b834b15000               mov eax, 0x50b134
0047b870  e8eccbfdff               call 0x458461
0047b875  ba40000000               mov edx, 0x40
0047b87a  b884ae5000               mov eax, 0x50ae84
0047b87f  e8ddcbfdff               call 0x458461
0047b884  bab0040000               mov edx, 0x4b0
0047b889  b8d0a95000               mov eax, 0x50a9d0
0047b88e  e8cecbfdff               call 0x458461
0047b893  ba40000000               mov edx, 0x40
0047b898  b838b15000               mov eax, 0x50b138
0047b89d  e8bfcbfdff               call 0x458461
0047b8a2  baa0010000               mov edx, 0x1a0
0047b8a7  b884af5000               mov eax, 0x50af84
0047b8ac  e8b0cbfdff               call 0x458461
0047b8b1  8b1424                   mov edx, dword ptr [esp]
0047b8b4  8b0d7c8f5000             mov ecx, dword ptr [0x508f7c]
0047b8ba  31c0                     xor eax, eax
0047b8bc  29d1                     sub ecx, edx
0047b8be  31d2                     xor edx, edx
0047b8c0  eb12                     jmp 0x47b8d4
0047b8c2  8b98d8a95000             mov ebx, dword ptr [eax + 0x50a9d8]
0047b8c8  83c00c                   add eax, 0xc
0047b8cb  01cb                     add ebx, ecx
0047b8cd  42                       inc edx
0047b8ce  8998cca95000             mov dword ptr [eax + 0x50a9cc], ebx
0047b8d4  31db                     xor ebx, ebx
0047b8d6  668b1dcea95000           mov bx, word ptr [0x50a9ce]
0047b8dd  39da                     cmp edx, ebx
0047b8df  7ce1                     jl 0x47b8c2
0047b8e1  83c404                   add esp, 4
0047b8e4  5a                       pop edx
0047b8e5  59                       pop ecx
0047b8e6  5b                       pop ebx
0047b8e7  c3                       ret

; LoadCalculMissionDivers 0x47c30f..0x47c359 sha256 4c9bb1b6009448b4c5a6ee205112b86033d33a7254b504f2759e67484e3d8111
0047c30f  53                       push ebx
0047c310  52                       push edx
0047c311  83ec04                   sub esp, 4
0047c314  30db                     xor bl, bl
0047c316  eb32                     jmp 0x47c34a
0047c318  ba01000000               mov edx, 1
0047c31d  89e0                     mov eax, esp
0047c31f  e83dc1fdff               call 0x458461
0047c324  ba01000000               mov edx, 1
0047c329  89e0                     mov eax, esp
0047c32b  e831c1fdff               call 0x458461
0047c330  ba01000000               mov edx, 1
0047c335  89e0                     mov eax, esp
0047c337  e825c1fdff               call 0x458461
0047c33c  ba01000000               mov edx, 1
0047c341  89e0                     mov eax, esp
0047c343  fec3                     inc bl
0047c345  e817c1fdff               call 0x458461
0047c34a  31c0                     xor eax, eax
0047c34c  88d8                     mov al, bl
0047c34e  83f804                   cmp eax, 4
0047c351  7cc5                     jl 0x47c318
0047c353  83c404                   add esp, 4
0047c356  5a                       pop edx
0047c357  5b                       pop ebx
0047c358  c3                       ret

; iaConfigGetValue 0x47fc54..0x47fc57 sha256 93b5600a402a472f2004a7f9f6e9816519fe2bab72db90614cb375bb822d6324
0047fc54  89d8                     mov eax, ebx
0047fc56  c3                       ret

; iaSetMode 0x47f8b7..0x47f8e7 sha256 735703a3d1b1c2624ca3594c0d4ede07b389561150cb216add2bdf1917d8137e
0047f8b7  53                       push ebx
0047f8b8  51                       push ecx
0047f8b9  89c3                     mov ebx, eax
0047f8bb  89c1                     mov ecx, eax
0047f8bd  c1e104                   shl ecx, 4
0047f8c0  81c18ca95100             add ecx, 0x51a98c
0047f8c6  8811                     mov byte ptr [ecx], dl
0047f8c8  0fbeca                   movsx ecx, dl
0047f8cb  89ca                     mov edx, ecx
0047f8cd  e8d54d0000               call 0x4846a7
0047f8d2  89ca                     mov edx, ecx
0047f8d4  89d8                     mov eax, ebx
0047f8d6  e8bf5d0000               call 0x48569a
0047f8db  89ca                     mov edx, ecx
0047f8dd  89d8                     mov eax, ebx
0047f8df  e8c3730000               call 0x486ca7
0047f8e4  59                       pop ecx
0047f8e5  5b                       pop ebx
0047f8e6  c3                       ret
