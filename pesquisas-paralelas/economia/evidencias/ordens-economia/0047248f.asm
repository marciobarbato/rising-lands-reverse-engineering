; EnginTravailSelectionne; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047248f  53                       push ebx
00472490  51                       push ecx
00472491  83ec04                   sub esp, 4
00472494  880424                   mov byte ptr [esp], al
00472497  30f6                     xor dh, dh
00472499  31db                     xor ebx, ebx
0047249b  eb37                     jmp 0x4724d4
0047249d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004724a2  8a4c0101                 mov cl, byte ptr [ecx + eax + 1]
004724a6  81e1ff000000             and ecx, 0xff
004724ac  83f90d                   cmp ecx, 0xd
004724af  7420                     je 0x4724d1
004724b1  83f905                   cmp ecx, 5
004724b4  741b                     je 0x4724d1
004724b6  30c0                     xor al, al
004724b8  e992feffff               jmp 0x47234f
004724bd  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004724c2  8a4c0101                 mov cl, byte ptr [ecx + eax + 1]
004724c6  81e1ff000000             and ecx, 0xff
004724cc  83f907                   cmp ecx, 7
004724cf  75e5                     jne 0x4724b6
004724d1  b601                     mov dh, 1
004724d3  43                       inc ebx
004724d4  31c9                     xor ecx, ecx
004724d6  8a0c24                   mov cl, byte ptr [esp]
004724d9  c1e109                   shl ecx, 9
004724dc  663b9928875000           cmp bx, word ptr [ecx + 0x508728]
004724e3  7351                     jae 0x472536
004724e5  31c0                     xor eax, eax
004724e7  6689d8                   mov ax, bx
004724ea  668b84412a875000         mov ax, word ptr [ecx + eax*2 + 0x50872a]
004724f2  31c9                     xor ecx, ecx
004724f4  6689c1                   mov cx, ax
004724f7  89c8                     mov eax, ecx
004724f9  e8af18fdff               call 0x443dad
004724fe  84c0                     test al, al
00472500  7516                     jne 0x472518
00472502  ebcf                     jmp 0x4724d3
00472504  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00472509  8a4c0101                 mov cl, byte ptr [ecx + eax + 1]
0047250d  81e1ff000000             and ecx, 0xff
00472513  83f906                   cmp ecx, 6
00472516  ebb7                     jmp 0x4724cf
00472518  69c914010000             imul ecx, ecx, 0x114
0047251e  80fa01                   cmp dl, 1
00472521  720d                     jb 0x472530
00472523  0f8674ffffff             jbe 0x47249d
00472529  80fa02                   cmp dl, 2
0047252c  748f                     je 0x4724bd
0047252e  eba3                     jmp 0x4724d3
00472530  84d2                     test dl, dl
00472532  74d0                     je 0x472504
00472534  eb9d                     jmp 0x4724d3
00472536  88f0                     mov al, dh
00472538  e912feffff               jmp 0x47234f
