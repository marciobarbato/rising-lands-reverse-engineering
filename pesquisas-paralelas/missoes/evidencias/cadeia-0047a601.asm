; InitEntrerMonstre; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
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
