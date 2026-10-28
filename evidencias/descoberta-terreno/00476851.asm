; DecouvreTerrain; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476851  51                       push ecx
00476852  56                       push esi
00476853  57                       push edi
00476854  83ec14                   sub esp, 0x14
00476857  89d7                     mov edi, edx
00476859  885c2410                 mov byte ptr [esp + 0x10], bl
0047685d  31db                     xor ebx, ebx
0047685f  6689c3                   mov bx, ax
00476862  b900010000               mov ecx, 0x100
00476867  89da                     mov edx, ebx
00476869  89d8                     mov eax, ebx
0047686b  c1fa1f                   sar edx, 0x1f
0047686e  f7f9                     idiv ecx
00476870  89542408                 mov dword ptr [esp + 8], edx
00476874  89da                     mov edx, ebx
00476876  89d8                     mov eax, ebx
00476878  c1fa1f                   sar edx, 0x1f
0047687b  f7f9                     idiv ecx
0047687d  47                       inc edi
0047687e  89c3                     mov ebx, eax
00476880  89f8                     mov eax, edi
00476882  0fafc7                   imul eax, edi
00476885  31d2                     xor edx, edx
00476887  6689fa                   mov dx, di
0047688a  83fa02                   cmp edx, 2
0047688d  7c01                     jl 0x476890
0047688f  40                       inc eax
00476890  8944240c                 mov dword ptr [esp + 0xc], eax
00476894  89fe                     mov esi, edi
00476896  f7de                     neg esi
00476898  01f3                     add ebx, esi
0047689a  eb05                     jmp 0x4768a1
0047689c  8b1c24                   mov ebx, dword ptr [esp]
0047689f  43                       inc ebx
004768a0  46                       inc esi
004768a1  66891c24                 mov word ptr [esp], bx
004768a5  31c0                     xor eax, eax
004768a7  0fbfd6                   movsx edx, si
004768aa  6689f8                   mov ax, di
004768ad  39c2                     cmp edx, eax
004768af  0f8f7e000000             jg 0x476933
004768b5  8b4424fe                 mov eax, dword ptr [esp - 2]
004768b9  c1f810                   sar eax, 0x10
004768bc  85c0                     test eax, eax
004768be  7cdc                     jl 0x47689c
004768c0  31d2                     xor edx, edx
004768c2  668b156a714900           mov dx, word ptr [0x49716a]
004768c9  39d0                     cmp eax, edx
004768cb  7dcf                     jge 0x47689c
004768cd  8b0424                   mov eax, dword ptr [esp]
004768d0  8b4c2408                 mov ecx, dword ptr [esp + 8]
004768d4  89fb                     mov ebx, edi
004768d6  c1e008                   shl eax, 8
004768d9  f7db                     neg ebx
004768db  89442404                 mov dword ptr [esp + 4], eax
004768df  01d9                     add ecx, ebx
004768e1  eb02                     jmp 0x4768e5
004768e3  41                       inc ecx
004768e4  43                       inc ebx
004768e5  31d2                     xor edx, edx
004768e7  0fbfc3                   movsx eax, bx
004768ea  6689fa                   mov dx, di
004768ed  39d0                     cmp eax, edx
004768ef  7fab                     jg 0x47689c
004768f1  0fbfc1                   movsx eax, cx
004768f4  85c0                     test eax, eax
004768f6  7ceb                     jl 0x4768e3
004768f8  31d2                     xor edx, edx
004768fa  668b1568714900           mov dx, word ptr [0x497168]
00476901  39d0                     cmp eax, edx
00476903  7dde                     jge 0x4768e3
00476905  31d2                     xor edx, edx
00476907  31c0                     xor eax, eax
00476909  6689da                   mov dx, bx
0047690c  6689f0                   mov ax, si
0047690f  e8382c0000               call 0x47954c
00476914  663b44240c               cmp ax, word ptr [esp + 0xc]
00476919  77c8                     ja 0x4768e3
0047691b  31d2                     xor edx, edx
0047691d  8b442404                 mov eax, dword ptr [esp + 4]
00476921  8a542410                 mov dl, byte ptr [esp + 0x10]
00476925  01c8                     add eax, ecx
00476927  25ffff0000               and eax, 0xffff
0047692c  e8d9fdffff               call 0x47670a
00476931  ebb0                     jmp 0x4768e3
00476933  83c414                   add esp, 0x14
00476936  5f                       pop edi
00476937  5e                       pop esi
00476938  59                       pop ecx
00476939  c3                       ret
