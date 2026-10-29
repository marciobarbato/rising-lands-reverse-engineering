; BagReset; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044710b  53                       push ebx
0044710c  51                       push ecx
0044710d  52                       push edx
0044710e  89c1                     mov ecx, eax
00447110  66c7000000               mov word ptr [eax], 0
00447115  66c740660000             mov word ptr [eax + 0x66], 0
0044711b  66c740040000             mov word ptr [eax + 4], 0
00447121  66c740020000             mov word ptr [eax + 2], 0
00447127  31d2                     xor edx, edx
00447129  eb0f                     jmp 0x44713a
0044712b  89c3                     mov ebx, eax
0044712d  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
00447134  42                       inc edx
00447135  c644014200               mov byte ptr [ecx + eax + 0x42], 0
0044713a  31c0                     xor eax, eax
0044713c  6689d0                   mov ax, dx
0044713f  83f81e                   cmp eax, 0x1e
00447142  7ce7                     jl 0x44712b
00447144  5a                       pop edx
00447145  59                       pop ecx
00447146  5b                       pop ebx
00447147  c3                       ret
