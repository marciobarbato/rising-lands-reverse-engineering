; EnginEstCharge; intervalo [0x0045173f, 0x004517a2)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045173f  53                       push     ebx
00451740  51                       push     ecx
00451741  52                       push     edx
00451742  56                       push     esi
00451743  31c9                     xor      ecx, ecx
00451745  6689c1                   mov      cx, ax
00451748  89c8                     mov      eax, ecx
0045174a  c1e004                   shl      eax, 4
0045174d  01c8                     add      eax, ecx
0045174f  c1e002                   shl      eax, 2
00451752  01c8                     add      eax, ecx
00451754  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
0045175a  c1e002                   shl      eax, 2
0045175d  01c1                     add      ecx, eax
0045175f  31db                     xor      ebx, ebx
00451761  8a5901                   mov      bl, byte ptr [ecx + 1]
00451764  89d8                     mov      eax, ebx
00451766  c1e002                   shl      eax, 2
00451769  29d8                     sub      eax, ebx
0045176b  c1e003                   shl      eax, 3
0045176e  01d8                     add      eax, ebx
00451770  31f6                     xor      esi, esi
00451772  668b3445de654900         mov      si, word ptr [eax*2 + 0x4965de]
0045177a  31c0                     xor      eax, eax
0045177c  ba03000000               mov      edx, 3
00451781  8a01                     mov      al, byte ptr [ecx]
00451783  e83875fdff               call     0x428cc0
00451788  31d2                     xor      edx, edx
0045178a  25ffff0000               and      eax, 0xffff
0045178f  668b9102010000           mov      dx, word ptr [ecx + 0x102]
00451796  29c6                     sub      esi, eax
00451798  39f2                     cmp      edx, esi
0045179a  0f9dc0                   setge    al
0045179d  5e                       pop      esi
0045179e  5a                       pop      edx
0045179f  59                       pop      ecx
004517a0  5b                       pop      ebx
004517a1  c3                       ret
