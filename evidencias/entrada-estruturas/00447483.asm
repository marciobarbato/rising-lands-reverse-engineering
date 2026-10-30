; BagPrend; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00447483  51                       push ecx
00447484  56                       push esi
00447485  88d1                     mov cl, dl
00447487  89de                     mov esi, ebx
00447489  66ff4066                 inc word ptr [eax + 0x66]
0044748d  31db                     xor ebx, ebx
0044748f  668b10                   mov dx, word ptr [eax]
00447492  6689d3                   mov bx, dx
00447495  89da                     mov edx, ebx
00447497  884c0342                 mov byte ptr [ebx + eax + 0x42], cl
0044749b  6689745006               mov word ptr [eax + edx*2 + 6], si
004474a0  66ff00                   inc word ptr [eax]
004474a3  5e                       pop esi
004474a4  59                       pop ecx
004474a5  c3                       ret
