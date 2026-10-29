; EnginResetType; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004571d4  53                       push ebx
004571d5  51                       push ecx
004571d6  52                       push edx
004571d7  56                       push esi
004571d8  55                       push ebp
004571d9  83ec04                   sub esp, 4
004571dc  50                       push eax
004571dd  31db                     xor ebx, ebx
004571df  6689c3                   mov bx, ax
004571e2  89d8                     mov eax, ebx
004571e4  c1e004                   shl eax, 4
004571e7  01d8                     add eax, ebx
004571e9  c1e002                   shl eax, 2
004571ec  01d8                     add eax, ebx
004571ee  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
004571f4  c1e002                   shl eax, 2
004571f7  01c1                     add ecx, eax
004571f9  c6410109                 mov byte ptr [ecx + 1], 9
004571fd  c6819300000001           mov byte ptr [ecx + 0x93], 1
00457204  c6819800000002           mov byte ptr [ecx + 0x98], 2
0045720b  c681a700000002           mov byte ptr [ecx + 0xa7], 2
00457212  c681a800000004           mov byte ptr [ecx + 0xa8], 4
00457219  c681a500000008           mov byte ptr [ecx + 0xa5], 8
00457220  c6819d000000ff           mov byte ptr [ecx + 0x9d], 0xff
00457227  c681ac00000003           mov byte ptr [ecx + 0xac], 3
0045722e  c681ad00000003           mov byte ptr [ecx + 0xad], 3
00457235  8d410a                   lea eax, [ecx + 0xa]
00457238  c6819900000000           mov byte ptr [ecx + 0x99], 0
0045723f  31d2                     xor edx, edx
00457241  c681bb00000005           mov byte ptr [ecx + 0xbb], 5
00457248  668910                   mov word ptr [eax], dx
0045724b  89542404                 mov dword ptr [esp + 4], edx
0045724f  66895066                 mov word ptr [eax + 0x66], dx
00457253  89c5                     mov ebp, eax
00457255  66895004                 mov word ptr [eax + 4], dx
00457259  89c6                     mov esi, eax
0045725b  66895002                 mov word ptr [eax + 2], dx
0045725f  eb0f                     jmp 0x457270
00457261  89c3                     mov ebx, eax
00457263  66c7445e060000           mov word ptr [esi + ebx*2 + 6], 0
0045726a  42                       inc edx
0045726b  c644064200               mov byte ptr [esi + eax + 0x42], 0
00457270  31c0                     xor eax, eax
00457272  6689d0                   mov ax, dx
00457275  83f81e                   cmp eax, 0x1e
00457278  7ce7                     jl 0x457261
0045727a  31db                     xor ebx, ebx
0045727c  8b442404                 mov eax, dword ptr [esp + 4]
00457280  668b1c24                 mov bx, word ptr [esp]
00457284  66894502                 mov word ptr [ebp + 2], ax
00457288  89d8                     mov eax, ebx
0045728a  c1e004                   shl eax, 4
0045728d  01d8                     add eax, ebx
0045728f  c1e002                   shl eax, 2
00457292  01d8                     add eax, ebx
00457294  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0045729a  8a448301                 mov al, byte ptr [ebx + eax*4 + 1]
0045729e  31db                     xor ebx, ebx
004572a0  88c3                     mov bl, al
004572a2  89d8                     mov eax, ebx
004572a4  c1e002                   shl eax, 2
004572a7  29d8                     sub eax, ebx
004572a9  c1e003                   shl eax, 3
004572ac  01d8                     add eax, ebx
004572ae  668b0445b6654900         mov ax, word ptr [eax*2 + 0x4965b6]
004572b6  663b819a000000           cmp ax, word ptr [ecx + 0x9a]
004572bd  7307                     jae 0x4572c6
004572bf  6689819a000000           mov word ptr [ecx + 0x9a], ax
004572c6  83c408                   add esp, 8
004572c9  e9b7a5feff               jmp 0x441885
