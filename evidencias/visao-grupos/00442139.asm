; EnginGetCentreGroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00442139  56                       push esi
0044213a  57                       push edi
0044213b  55                       push ebp
0044213c  83ec1c                   sub esp, 0x1c
0044213f  88442414                 mov byte ptr [esp + 0x14], al
00442143  891424                   mov dword ptr [esp], edx
00442146  89df                     mov edi, ebx
00442148  884c2418                 mov byte ptr [esp + 0x18], cl
0044214c  baffff0000               mov edx, 0xffff
00442151  31db                     xor ebx, ebx
00442153  89542410                 mov dword ptr [esp + 0x10], edx
00442157  89d6                     mov esi, edx
00442159  895c2404                 mov dword ptr [esp + 4], ebx
0044215d  895c240c                 mov dword ptr [esp + 0xc], ebx
00442161  eb01                     jmp 0x442164
00442163  43                       inc ebx
00442164  31c0                     xor eax, eax
00442166  6689d8                   mov ax, bx
00442169  3d20030000               cmp eax, 0x320
0044216e  0f8d9e000000             jge 0x442212
00442174  69d014010000             imul edx, eax, 0x114
0044217a  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044217f  01d0                     add eax, edx
00442181  31d2                     xor edx, edx
00442183  8a5002                   mov dl, byte ptr [eax + 2]
00442186  85d2                     test edx, edx
00442188  7409                     je 0x442193
0044218a  83fa04                   cmp edx, 4
0044218d  7404                     je 0x442193
0044218f  b201                     mov dl, 1
00442191  eb02                     jmp 0x442195
00442193  30d2                     xor dl, dl
00442195  84d2                     test dl, dl
00442197  74ca                     je 0x442163
00442199  8a90bc000000             mov dl, byte ptr [eax + 0xbc]
0044219f  3a542418                 cmp dl, byte ptr [esp + 0x18]
004421a3  75be                     jne 0x442163
004421a5  31d2                     xor edx, edx
004421a7  6689da                   mov dx, bx
004421aa  69d214010000             imul edx, edx, 0x114
004421b0  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
004421b6  8a1411                   mov dl, byte ptr [ecx + edx]
004421b9  3a542414                 cmp dl, byte ptr [esp + 0x14]
004421bd  75a4                     jne 0x442163
004421bf  31c9                     xor ecx, ecx
004421c1  668b4808                 mov cx, word ptr [eax + 8]
004421c5  bd00010000               mov ebp, 0x100
004421ca  89ca                     mov edx, ecx
004421cc  89c8                     mov eax, ecx
004421ce  c1fa1f                   sar edx, 0x1f
004421d1  f7fd                     idiv ebp
004421d3  89542408                 mov dword ptr [esp + 8], edx
004421d7  89ca                     mov edx, ecx
004421d9  89c8                     mov eax, ecx
004421db  c1fa1f                   sar edx, 0x1f
004421de  f7fd                     idiv ebp
004421e0  8b542408                 mov edx, dword ptr [esp + 8]
004421e4  6639d6                   cmp si, dx
004421e7  7602                     jbe 0x4421eb
004421e9  89d6                     mov esi, edx
004421eb  663b442410               cmp ax, word ptr [esp + 0x10]
004421f0  7304                     jae 0x4421f6
004421f2  89442410                 mov dword ptr [esp + 0x10], eax
004421f6  8b54240c                 mov edx, dword ptr [esp + 0xc]
004421fa  8b4c2408                 mov ecx, dword ptr [esp + 8]
004421fe  6639ca                   cmp dx, cx
00442201  7304                     jae 0x442207
00442203  894c240c                 mov dword ptr [esp + 0xc], ecx
00442207  663b442404               cmp ax, word ptr [esp + 4]
0044220c  7604                     jbe 0x442212
0044220e  89442404                 mov dword ptr [esp + 4], eax
00442212  31c0                     xor eax, eax
00442214  6689d8                   mov ax, bx
00442217  3d20030000               cmp eax, 0x320
0044221c  752c                     jne 0x44224a
0044221e  668b07                   mov ax, word ptr [edi]
00442221  8b3424                   mov esi, dword ptr [esp]
00442224  89442410                 mov dword ptr [esp + 0x10], eax
00442228  668b36                   mov si, word ptr [esi]
0044222b  66a124875000             mov ax, word ptr [0x508724]
00442231  01f0                     add eax, esi
00442233  48                       dec eax
00442234  668b1d26875000           mov bx, word ptr [0x508726]
0044223b  8944240c                 mov dword ptr [esp + 0xc], eax
0044223f  8b442410                 mov eax, dword ptr [esp + 0x10]
00442243  01d8                     add eax, ebx
00442245  48                       dec eax
00442246  89442404                 mov dword ptr [esp + 4], eax
0044224a  31d2                     xor edx, edx
0044224c  31c9                     xor ecx, ecx
0044224e  668b54240c               mov dx, word ptr [esp + 0xc]
00442253  6689f1                   mov cx, si
00442256  29ca                     sub edx, ecx
00442258  89d0                     mov eax, edx
0044225a  c1fa1f                   sar edx, 0x1f
0044225d  2bc2                     sub eax, edx
0044225f  d1f8                     sar eax, 1
00442261  8b1424                   mov edx, dword ptr [esp]
00442264  01c8                     add eax, ecx
00442266  31c9                     xor ecx, ecx
00442268  668902                   mov word ptr [edx], ax
0044226b  31d2                     xor edx, edx
0044226d  668b4c2410               mov cx, word ptr [esp + 0x10]
00442272  668b542404               mov dx, word ptr [esp + 4]
00442277  29ca                     sub edx, ecx
00442279  89d0                     mov eax, edx
0044227b  c1fa1f                   sar edx, 0x1f
0044227e  2bc2                     sub eax, edx
00442280  d1f8                     sar eax, 1
00442282  01c8                     add eax, ecx
00442284  668907                   mov word ptr [edi], ax
00442287  83c41c                   add esp, 0x1c
0044228a  5d                       pop ebp
0044228b  5f                       pop edi
0044228c  5e                       pop esi
0044228d  c3                       ret
