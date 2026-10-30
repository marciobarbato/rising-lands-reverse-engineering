; SauveSelectionGroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004726f7  53                       push ebx
004726f8  51                       push ecx
004726f9  88c5                     mov ch, al
004726fb  88d1                     mov cl, dl
004726fd  31db                     xor ebx, ebx
004726ff  eb01                     jmp 0x472702
00472701  43                       inc ebx
00472702  31d2                     xor edx, edx
00472704  6689da                   mov dx, bx
00472707  81fa20030000             cmp edx, 0x320
0047270d  0f8dd8feffff             jge 0x4725eb
00472713  89d0                     mov eax, edx
00472715  e89316fdff               call 0x443dad
0047271a  84c0                     test al, al
0047271c  74e3                     je 0x472701
0047271e  89d0                     mov eax, edx
00472720  e820f9fcff               call 0x442045
00472725  38e8                     cmp al, ch
00472727  75d8                     jne 0x472701
00472729  69c214010000             imul eax, edx, 0x114
0047272f  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00472735  01c2                     add edx, eax
00472737  3a8abc000000             cmp cl, byte ptr [edx + 0xbc]
0047273d  7507                     jne 0x472746
0047273f  c682bc00000000           mov byte ptr [edx + 0xbc], 0
00472746  31d2                     xor edx, edx
00472748  6689da                   mov dx, bx
0047274b  69d214010000             imul edx, edx, 0x114
00472751  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00472756  01c2                     add edx, eax
00472758  80babd00000000           cmp byte ptr [edx + 0xbd], 0
0047275f  74a0                     je 0x472701
00472761  888abc000000             mov byte ptr [edx + 0xbc], cl
00472767  eb98                     jmp 0x472701
