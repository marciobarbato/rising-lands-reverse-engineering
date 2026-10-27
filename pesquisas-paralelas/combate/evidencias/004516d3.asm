; EnginRechargeArme; intervalo [0x004516d3, 0x0045173f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004516d3  53                       push     ebx
004516d4  51                       push     ecx
004516d5  52                       push     edx
004516d6  56                       push     esi
004516d7  31db                     xor      ebx, ebx
004516d9  6689c3                   mov      bx, ax
004516dc  89d8                     mov      eax, ebx
004516de  c1e004                   shl      eax, 4
004516e1  01d8                     add      eax, ebx
004516e3  c1e002                   shl      eax, 2
004516e6  01d8                     add      eax, ebx
004516e8  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
004516ee  c1e002                   shl      eax, 2
004516f1  01c1                     add      ecx, eax
004516f3  31db                     xor      ebx, ebx
004516f5  8a5901                   mov      bl, byte ptr [ecx + 1]
004516f8  89d8                     mov      eax, ebx
004516fa  c1e002                   shl      eax, 2
004516fd  29d8                     sub      eax, ebx
004516ff  c1e003                   shl      eax, 3
00451702  01d8                     add      eax, ebx
00451704  31f6                     xor      esi, esi
00451706  668b3445de654900         mov      si, word ptr [eax*2 + 0x4965de]
0045170e  31c0                     xor      eax, eax
00451710  ba03000000               mov      edx, 3
00451715  8a01                     mov      al, byte ptr [ecx]
00451717  e8a475fdff               call     0x428cc0
0045171c  25ffff0000               and      eax, 0xffff
00451721  29c6                     sub      esi, eax
00451723  31c0                     xor      eax, eax
00451725  668b8102010000           mov      ax, word ptr [ecx + 0x102]
0045172c  39f0                     cmp      eax, esi
0045172e  7d0a                     jge      0x45173a
00451730  89c2                     mov      edx, eax
00451732  42                       inc      edx
00451733  66899102010000           mov      word ptr [ecx + 0x102], dx
0045173a  5e                       pop      esi
0045173b  5a                       pop      edx
0045173c  59                       pop      ecx
0045173d  5b                       pop      ebx
0045173e  c3                       ret
