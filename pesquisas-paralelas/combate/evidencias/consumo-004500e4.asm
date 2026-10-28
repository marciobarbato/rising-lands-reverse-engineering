; ChercheTypeEnginProximite; [0x004500e4, 0x00450286)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004500e4  56                       push     esi
004500e5  57                       push     edi
004500e6  55                       push     ebp
004500e7  83ec28                   sub      esp, 0x28
004500ea  88542424                 mov      byte ptr [esp + 0x24], dl
004500ee  81e3ffff0000             and      ebx, 0xffff
004500f4  be00010000               mov      esi, 0x100
004500f9  89da                     mov      edx, ebx
004500fb  89d8                     mov      eax, ebx
004500fd  c1fa1f                   sar      edx, 0x1f
00450100  f7fe                     idiv     esi
00450102  89542408                 mov      dword ptr [esp + 8], edx
00450106  89da                     mov      edx, ebx
00450108  89d8                     mov      eax, ebx
0045010a  c1fa1f                   sar      edx, 0x1f
0045010d  f7fe                     idiv     esi
0045010f  8944241c                 mov      dword ptr [esp + 0x1c], eax
00450113  89442404                 mov      dword ptr [esp + 4], eax
00450117  89c8                     mov      eax, ecx
00450119  01c8                     add      eax, ecx
0045011b  40                       inc      eax
0045011c  8b542408                 mov      edx, dword ptr [esp + 8]
00450120  8944240c                 mov      dword ptr [esp + 0xc], eax
00450124  89442420                 mov      dword ptr [esp + 0x20], eax
00450128  6639d1                   cmp      cx, dx
0045012b  730a                     jae      0x450137
0045012d  89d0                     mov      eax, edx
0045012f  29c8                     sub      eax, ecx
00450131  89442410                 mov      dword ptr [esp + 0x10], eax
00450135  eb14                     jmp      0x45014b
00450137  89c8                     mov      eax, ecx
00450139  8b74240c                 mov      esi, dword ptr [esp + 0xc]
0045013d  29d0                     sub      eax, edx
0045013f  31ff                     xor      edi, edi
00450141  29c6                     sub      esi, eax
00450143  897c2410                 mov      dword ptr [esp + 0x10], edi
00450147  8974240c                 mov      dword ptr [esp + 0xc], esi
0045014b  8b442404                 mov      eax, dword ptr [esp + 4]
0045014f  6639c1                   cmp      cx, ax
00450152  730a                     jae      0x45015e
00450154  89c7                     mov      edi, eax
00450156  29cf                     sub      edi, ecx
00450158  897c2404                 mov      dword ptr [esp + 4], edi
0045015c  eb18                     jmp      0x450176
0045015e  8b542404                 mov      edx, dword ptr [esp + 4]
00450162  89c8                     mov      eax, ecx
00450164  8b5c2420                 mov      ebx, dword ptr [esp + 0x20]
00450168  29d0                     sub      eax, edx
0045016a  31f6                     xor      esi, esi
0045016c  29c3                     sub      ebx, eax
0045016e  89742404                 mov      dword ptr [esp + 4], esi
00450172  895c2420                 mov      dword ptr [esp + 0x20], ebx
00450176  0fafc9                   imul     ecx, ecx
00450179  8b7c2404                 mov      edi, dword ptr [esp + 4]
0045017d  8b442410                 mov      eax, dword ptr [esp + 0x10]
00450181  c1e708                   shl      edi, 8
00450184  01c7                     add      edi, eax
00450186  8b442404                 mov      eax, dword ptr [esp + 4]
0045018a  8b54240c                 mov      edx, dword ptr [esp + 0xc]
0045018e  6689442414               mov      word ptr [esp + 0x14], ax
00450193  b800010000               mov      eax, 0x100
00450198  29d0                     sub      eax, edx
0045019a  894c2418                 mov      dword ptr [esp + 0x18], ecx
0045019e  890424                   mov      dword ptr [esp], eax
004501a1  bdffff0000               mov      ebp, 0xffff
004501a6  eb0f                     jmp      0x4501b7
004501a8  8b742414                 mov      esi, dword ptr [esp + 0x14]
004501ac  8b0c24                   mov      ecx, dword ptr [esp]
004501af  46                       inc      esi
004501b0  01cf                     add      edi, ecx
004501b2  6689742414               mov      word ptr [esp + 0x14], si
004501b7  31d2                     xor      edx, edx
004501b9  31c0                     xor      eax, eax
004501bb  668b542404               mov      dx, word ptr [esp + 4]
004501c0  668b442420               mov      ax, word ptr [esp + 0x20]
004501c5  01c2                     add      edx, eax
004501c7  8b442412                 mov      eax, dword ptr [esp + 0x12]
004501cb  c1f810                   sar      eax, 0x10
004501ce  39d0                     cmp      eax, edx
004501d0  0f8de829ffff             jge      0x442bbe
004501d6  3d00010000               cmp      eax, 0x100
004501db  7dcb                     jge      0x4501a8
004501dd  8b742410                 mov      esi, dword ptr [esp + 0x10]
004501e1  eb02                     jmp      0x4501e5
004501e3  47                       inc      edi
004501e4  46                       inc      esi
004501e5  31d2                     xor      edx, edx
004501e7  31c0                     xor      eax, eax
004501e9  668b542410               mov      dx, word ptr [esp + 0x10]
004501ee  668b44240c               mov      ax, word ptr [esp + 0xc]
004501f3  01c2                     add      edx, eax
004501f5  0fbfc6                   movsx    eax, si
004501f8  39d0                     cmp      eax, edx
004501fa  7dac                     jge      0x4501a8
004501fc  3d00010000               cmp      eax, 0x100
00450201  7de0                     jge      0x4501e3
00450203  31c0                     xor      eax, eax
00450205  6689f8                   mov      ax, di
00450208  8b15380f4e00             mov      edx, dword ptr [0x4e0f38]
0045020e  01c0                     add      eax, eax
00450210  01d0                     add      eax, edx
00450212  668b10                   mov      dx, word ptr [eax]
00450215  30d2                     xor      dl, dl
00450217  80e6c0                   and      dh, 0xc0
0045021a  6681fa0040               cmp      dx, 0x4000
0045021f  7512                     jne      0x450233
00450221  668b00                   mov      ax, word ptr [eax]
00450224  31db                     xor      ebx, ebx
00450226  25f83f0000               and      eax, 0x3ff8
0045022b  6689c3                   mov      bx, ax
0045022e  c1fb03                   sar      ebx, 3
00450231  eb02                     jmp      0x450235
00450233  89eb                     mov      ebx, ebp
00450235  31c0                     xor      eax, eax
00450237  6689d8                   mov      ax, bx
0045023a  3dffff0000               cmp      eax, 0xffff
0045023f  74a2                     je       0x4501e3
00450241  69d014010000             imul     edx, eax, 0x114
00450247  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0045024c  8a0402                   mov      al, byte ptr [edx + eax]
0045024f  3a442424                 cmp      al, byte ptr [esp + 0x24]
00450253  758e                     jne      0x4501e3
00450255  31c9                     xor      ecx, ecx
00450257  31db                     xor      ebx, ebx
00450259  31d2                     xor      edx, edx
0045025b  31c0                     xor      eax, eax
0045025d  668b4c2414               mov      cx, word ptr [esp + 0x14]
00450262  668b54241c               mov      dx, word ptr [esp + 0x1c]
00450267  668b442408               mov      ax, word ptr [esp + 8]
0045026c  6689f3                   mov      bx, si
0045026f  e8e1920200               call     0x479555
00450274  663b442418               cmp      ax, word ptr [esp + 0x18]
00450279  0f8764ffffff             ja       0x4501e3
0045027f  b001                     mov      al, 1
00450281  e99524ffff               jmp      0x44271b
