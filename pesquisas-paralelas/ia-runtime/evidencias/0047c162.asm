; IAResetAttaque (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047c162..0x0047c1ba (end exclusive); labels are original SBL names
0047c162  53                       push ebx
0047c163  51                       push ecx
0047c164  52                       push edx
0047c165  31d2                     xor edx, edx
0047c167  b1ff                     mov cl, 0xff
0047c169  89159cd95000             mov dword ptr [0x50d99c], edx
0047c16f  31d2                     xor edx, edx
0047c171  eb39                     jmp 0x47c1ac
0047c173  6bc00a                   imul eax, eax, 0xa
0047c176  c680b4d55000c8           mov byte ptr [eax + 0x50d5b4], 0xc8
0047c17d  8888b8d55000             mov byte ptr [eax + 0x50d5b8], cl
0047c183  8888b9d55000             mov byte ptr [eax + 0x50d5b9], cl
0047c189  c680b5d55000ff           mov byte ptr [eax + 0x50d5b5], 0xff
0047c190  bbffff0000               mov ebx, 0xffff
0047c195  668998b6d55000           mov word ptr [eax + 0x50d5b6], bx
0047c19c  668998bad55000           mov word ptr [eax + 0x50d5ba], bx
0047c1a3  30db                     xor bl, bl
0047c1a5  42                       inc edx
0047c1a6  8898bcd55000             mov byte ptr [eax + 0x50d5bc], bl
0047c1ac  31c0                     xor eax, eax
0047c1ae  6689d0                   mov ax, dx
0047c1b1  83f864                   cmp eax, 0x64
0047c1b4  7cbd                     jl 0x47c173
0047c1b6  5a                       pop edx
0047c1b7  59                       pop ecx
0047c1b8  5b                       pop ebx
0047c1b9  c3                       ret
