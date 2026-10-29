; DeSelectionGroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047268b  53                       push ebx
0047268c  51                       push ecx
0047268d  52                       push edx
0047268e  83ec04                   sub esp, 4
00472691  880424                   mov byte ptr [esp], al
00472694  31c9                     xor ecx, ecx
00472696  eb01                     jmp 0x472699
00472698  41                       inc ecx
00472699  31db                     xor ebx, ebx
0047269b  6689cb                   mov bx, cx
0047269e  81fb20030000             cmp ebx, 0x320
004726a4  0f8da7fbffff             jge 0x472251
004726aa  89d8                     mov eax, ebx
004726ac  e8fc16fdff               call 0x443dad
004726b1  84c0                     test al, al
004726b3  74e3                     je 0x472698
004726b5  69c314010000             imul eax, ebx, 0x114
004726bb  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004726c1  01d0                     add eax, edx
004726c3  80b8bd00000000           cmp byte ptr [eax + 0xbd], 0
004726ca  74cc                     je 0x472698
004726cc  8a10                     mov dl, byte ptr [eax]
004726ce  3a1424                   cmp dl, byte ptr [esp]
004726d1  75c5                     jne 0x472698
004726d3  80b8bd00000000           cmp byte ptr [eax + 0xbd], 0
004726da  74bc                     je 0x472698
004726dc  c680bd00000000           mov byte ptr [eax + 0xbd], 0
004726e3  89d8                     mov eax, ebx
004726e5  31d2                     xor edx, edx
004726e7  e859f9fcff               call 0x442045
004726ec  88c2                     mov dl, al
004726ee  89d8                     mov eax, ebx
004726f0  e881feffff               call 0x472576
004726f5  eba1                     jmp 0x472698
