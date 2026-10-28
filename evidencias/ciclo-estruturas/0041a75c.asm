; BatimentResetAll; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a75c  53                       push ebx
0041a75d  51                       push ecx
0041a75e  52                       push edx
0041a75f  57                       push edi
0041a760  baffff0000               mov edx, 0xffff
0041a765  31c9                     xor ecx, ecx
0041a767  eb09                     jmp 0x41a772
0041a769  41                       inc ecx
0041a76a  66891445e05b4900         mov word ptr [eax*2 + 0x495be0], dx
0041a772  31c0                     xor eax, eax
0041a774  6689c8                   mov ax, cx
0041a777  83f804                   cmp eax, 4
0041a77a  7ced                     jl 0x41a769
0041a77c  31c9                     xor ecx, ecx
0041a77e  eb1c                     jmp 0x41a79c
0041a780  31db                     xor ebx, ebx
0041a782  6689cb                   mov bx, cx
0041a785  6bdb16                   imul ebx, ebx, 0x16
0041a788  40                       inc eax
0041a789  c6841a70a0490000         mov byte ptr [edx + ebx + 0x49a070], 0
0041a791  31d2                     xor edx, edx
0041a793  6689c2                   mov dx, ax
0041a796  83fa16                   cmp edx, 0x16
0041a799  7ce5                     jl 0x41a780
0041a79b  41                       inc ecx
0041a79c  31c0                     xor eax, eax
0041a79e  6689c8                   mov ax, cx
0041a7a1  83f804                   cmp eax, 4
0041a7a4  7d04                     jge 0x41a7aa
0041a7a6  31c8                     xor eax, ecx
0041a7a8  ebe7                     jmp 0x41a791
0041a7aa  31d2                     xor edx, edx
0041a7ac  bfc8000000               mov edi, 0xc8
0041a7b1  31db                     xor ebx, ebx
0041a7b3  e993000000               jmp 0x41a84b
0041a7b8  69c014010000             imul eax, eax, 0x114
0041a7be  8898cda04900             mov byte ptr [eax + 0x49a0cd], bl
0041a7c4  668998cea04900           mov word ptr [eax + 0x49a0ce], bx
0041a7cb  b1ff                     mov cl, 0xff
0041a7cd  668998d2a04900           mov word ptr [eax + 0x49a0d2], bx
0041a7d4  8888c8a04900             mov byte ptr [eax + 0x49a0c8], cl
0041a7da  88983ca14900             mov byte ptr [eax + 0x49a13c], bl
0041a7e0  88983da14900             mov byte ptr [eax + 0x49a13d], bl
0041a7e6  88983ea14900             mov byte ptr [eax + 0x49a13e], bl
0041a7ec  888843a14900             mov byte ptr [eax + 0x49a143], cl
0041a7f2  66899844a14900           mov word ptr [eax + 0x49a144], bx
0041a7f9  889858a14900             mov byte ptr [eax + 0x49a158], bl
0041a7ff  66899846a14900           mov word ptr [eax + 0x49a146], bx
0041a806  66899848a14900           mov word ptr [eax + 0x49a148], bx
0041a80d  6689984aa14900           mov word ptr [eax + 0x49a14a], bx
0041a814  6689b84ca14900           mov word ptr [eax + 0x49a14c], di
0041a81b  899854a14900             mov dword ptr [eax + 0x49a154], ebx
0041a821  b9ffff0000               mov ecx, 0xffff
0041a826  66898840a14900           mov word ptr [eax + 0x49a140], cx
0041a82d  6689884ea14900           mov word ptr [eax + 0x49a14e], cx
0041a834  b101                     mov cl, 1
0041a836  888852a14900             mov byte ptr [eax + 0x49a152], cl
0041a83c  888853a14900             mov byte ptr [eax + 0x49a153], cl
0041a842  b1ff                     mov cl, 0xff
0041a844  42                       inc edx
0041a845  8888cca04900             mov byte ptr [eax + 0x49a0cc], cl
0041a84b  31c0                     xor eax, eax
0041a84d  6689d0                   mov ax, dx
0041a850  3de8030000               cmp eax, 0x3e8
0041a855  0f8c5dffffff             jl 0x41a7b8
0041a85b  5f                       pop edi
0041a85c  5a                       pop edx
0041a85d  59                       pop ecx
0041a85e  5b                       pop ebx
0041a85f  c3                       ret
