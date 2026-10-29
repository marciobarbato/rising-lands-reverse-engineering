; BagInit; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00447148  53                       push ebx
00447149  51                       push ecx
0044714a  56                       push esi
0044714b  83ec04                   sub esp, 4
0044714e  89c6                     mov esi, eax
00447150  891424                   mov dword ptr [esp], edx
00447153  66c7000000               mov word ptr [eax], 0
00447158  66c740660000             mov word ptr [eax + 0x66], 0
0044715e  66c740040000             mov word ptr [eax + 4], 0
00447164  89c1                     mov ecx, eax
00447166  66c740020000             mov word ptr [eax + 2], 0
0044716c  31d2                     xor edx, edx
0044716e  eb0f                     jmp 0x44717f
00447170  89c3                     mov ebx, eax
00447172  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
00447179  42                       inc edx
0044717a  c644014200               mov byte ptr [ecx + eax + 0x42], 0
0044717f  31c0                     xor eax, eax
00447181  6689d0                   mov ax, dx
00447184  83f81e                   cmp eax, 0x1e
00447187  7ce7                     jl 0x447170
00447189  8b0424                   mov eax, dword ptr [esp]
0044718c  66894602                 mov word ptr [esi + 2], ax
00447190  83c404                   add esp, 4
00447193  5e                       pop esi
00447194  59                       pop ecx
00447195  5b                       pop ebx
00447196  c3                       ret
