; SetEnginConstruitBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004454ce  51                       push ecx
004454cf  56                       push esi
004454d0  57                       push edi
004454d1  55                       push ebp
004454d2  83ec10                   sub esp, 0x10
004454d5  89c7                     mov edi, eax
004454d7  8854240c                 mov byte ptr [esp + 0xc], dl
004454db  89de                     mov esi, ebx
004454dd  31db                     xor ebx, ebx
004454df  6689c3                   mov bx, ax
004454e2  89dd                     mov ebp, ebx
004454e4  c1e504                   shl ebp, 4
004454e7  01dd                     add ebp, ebx
004454e9  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
004454ef  c1e502                   shl ebp, 2
004454f2  8d442404                 lea eax, [esp + 4]
004454f6  01dd                     add ebp, ebx
004454f8  31db                     xor ebx, ebx
004454fa  c1e502                   shl ebp, 2
004454fd  88d3                     mov bl, dl
004454ff  8d542408                 lea edx, [esp + 8]
00445503  01e9                     add ecx, ebp
00445505  e88c54fdff               call 0x41a996
0044550a  31c0                     xor eax, eax
0044550c  8a4102                   mov al, byte ptr [ecx + 2]
0044550f  83f80b                   cmp eax, 0xb
00445512  7542                     jne 0x445556
00445514  31c0                     xor eax, eax
00445516  8a81be000000             mov al, byte ptr [ecx + 0xbe]
0044551c  83f809                   cmp eax, 9
0044551f  7535                     jne 0x445556
00445521  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445526  01e8                     add eax, ebp
00445528  31d2                     xor edx, edx
0044552a  668b90d8000000           mov dx, word ptr [eax + 0xd8]
00445531  83fa0a                   cmp edx, 0xa
00445534  0f8d0a010000             jge 0x445644
0044553a  89d3                     mov ebx, edx
0044553c  31d2                     xor edx, edx
0044553e  6689da                   mov dx, bx
00445541  43                       inc ebx
00445542  668998d8000000           mov word ptr [eax + 0xd8], bx
00445549  6689b450c4000000         mov word ptr [eax + edx*2 + 0xc4], si
00445551  e9ee000000               jmp 0x445644
00445556  31c0                     xor eax, eax
00445558  6689f8                   mov ax, di
0044555b  0fb66c240c               movzx ebp, byte ptr [esp + 0xc]
00445560  e817e0ffff               call 0x44357c
00445565  83fd09                   cmp ebp, 9
00445568  7449                     je 0x4455b3
0044556a  83fd0c                   cmp ebp, 0xc
0044556d  7444                     je 0x4455b3
0044556f  31db                     xor ebx, ebx
00445571  668b5c2408               mov bx, word ptr [esp + 8]
00445576  89da                     mov edx, ebx
00445578  89d8                     mov eax, ebx
0044557a  c1fa1f                   sar edx, 0x1f
0044557d  2bc2                     sub eax, edx
0044557f  d1f8                     sar eax, 1
00445581  29c3                     sub ebx, eax
00445583  c1e308                   shl ebx, 8
00445586  891c24                   mov dword ptr [esp], ebx
00445589  31db                     xor ebx, ebx
0044558b  668b5c2404               mov bx, word ptr [esp + 4]
00445590  89da                     mov edx, ebx
00445592  89d8                     mov eax, ebx
00445594  c1fa1f                   sar edx, 0x1f
00445597  2bc2                     sub eax, edx
00445599  d1f8                     sar eax, 1
0044559b  29c3                     sub ebx, eax
0044559d  8b0424                   mov eax, dword ptr [esp]
004455a0  4b                       dec ebx
004455a1  2d00010000               sub eax, 0x100
004455a6  01d8                     add eax, ebx
004455a8  01c6                     add esi, eax
004455aa  89e8                     mov eax, ebp
004455ac  e8f358fdff               call 0x41aea4
004455b1  29c6                     sub esi, eax
004455b3  31db                     xor ebx, ebx
004455b5  6689fb                   mov bx, di
004455b8  89da                     mov edx, ebx
004455ba  c1e204                   shl edx, 4
004455bd  01da                     add edx, ebx
004455bf  c1e202                   shl edx, 2
004455c2  01da                     add edx, ebx
004455c4  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004455c9  c1e202                   shl edx, 2
004455cc  01d0                     add eax, edx
004455ce  6689707e                 mov word ptr [eax + 0x7e], si
004455d2  663b3d04634900           cmp di, word ptr [0x496304]
004455d9  7522                     jne 0x4455fd
004455db  30d2                     xor dl, dl
004455dd  bbffff0000               mov ebx, 0xffff
004455e2  8815360f4e00             mov byte ptr [0x4e0f36], dl
004455e8  8815370f4e00             mov byte ptr [0x4e0f37], dl
004455ee  31d2                     xor edx, edx
004455f0  66891d04634900           mov word ptr [0x496304], bx
004455f7  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
004455fd  c6808800000000           mov byte ptr [eax + 0x88], 0
00445604  c6818800000000           mov byte ptr [ecx + 0x88], 0
0044560b  c6818900000000           mov byte ptr [ecx + 0x89], 0
00445612  8a44240c                 mov al, byte ptr [esp + 0xc]
00445616  66c781c0000000ffff       mov word ptr [ecx + 0xc0], 0xffff
0044561f  8881be000000             mov byte ptr [ecx + 0xbe], al
00445625  31c0                     xor eax, eax
00445627  c641020b                 mov byte ptr [ecx + 2], 0xb
0044562b  8a44240c                 mov al, byte ptr [esp + 0xc]
0044562f  6689b1b2000000           mov word ptr [ecx + 0xb2], si
00445636  83f809                   cmp eax, 9
00445639  7509                     jne 0x445644
0044563b  66c781d80000000000       mov word ptr [ecx + 0xd8], 0
00445644  83c410                   add esp, 0x10
00445647  5d                       pop ebp
00445648  5f                       pop edi
00445649  5e                       pop esi
0044564a  59                       pop ecx
0044564b  c3                       ret
