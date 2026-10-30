; RestaureSelectionGroupe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00472769  53                       push ebx
0047276a  51                       push ecx
0047276b  56                       push esi
0047276c  57                       push edi
0047276d  83ec08                   sub esp, 8
00472770  88442404                 mov byte ptr [esp + 4], al
00472774  881424                   mov byte ptr [esp], dl
00472777  31ff                     xor edi, edi
00472779  31c9                     xor ecx, ecx
0047277b  eb01                     jmp 0x47277e
0047277d  41                       inc ecx
0047277e  31db                     xor ebx, ebx
00472780  6689cb                   mov bx, cx
00472783  81fb20030000             cmp ebx, 0x320
00472789  0f8d74010000             jge 0x472903
0047278f  89d8                     mov eax, ebx
00472791  e81716fdff               call 0x443dad
00472796  84c0                     test al, al
00472798  74e3                     je 0x47277d
0047279a  89d8                     mov eax, ebx
0047279c  e8a4f8fcff               call 0x442045
004727a1  3a442404                 cmp al, byte ptr [esp + 4]
004727a5  75d6                     jne 0x47277d
004727a7  69c314010000             imul eax, ebx, 0x114
004727ad  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004727b3  01d0                     add eax, edx
004727b5  80b8bd00000000           cmp byte ptr [eax + 0xbd], 0
004727bc  7419                     je 0x4727d7
004727be  c680bd00000000           mov byte ptr [eax + 0xbd], 0
004727c5  89d8                     mov eax, ebx
004727c7  31d2                     xor edx, edx
004727c9  e877f8fcff               call 0x442045
004727ce  88c2                     mov dl, al
004727d0  89d8                     mov eax, ebx
004727d2  e89ffdffff               call 0x472576
004727d7  31c0                     xor eax, eax
004727d9  6689c8                   mov ax, cx
004727dc  69d014010000             imul edx, eax, 0x114
004727e2  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
004727e8  8a9c32bc000000           mov bl, byte ptr [edx + esi + 0xbc]
004727ef  3a1c24                   cmp bl, byte ptr [esp]
004727f2  7589                     jne 0x47277d
004727f4  e818e6fcff               call 0x440e11
004727f9  25ff000000               and eax, 0xff
004727fe  83f80e                   cmp eax, 0xe
00472801  0f8476ffffff             je 0x47277d
00472807  31db                     xor ebx, ebx
00472809  8a5c2404                 mov bl, byte ptr [esp + 4]
0047280d  c1e309                   shl ebx, 9
00472810  31c0                     xor eax, eax
00472812  668b8328875000           mov ax, word ptr [ebx + 0x508728]
00472819  3dff000000               cmp eax, 0xff
0047281e  7d26                     jge 0x472846
00472820  89c6                     mov esi, eax
00472822  46                       inc esi
00472823  89f0                     mov eax, esi
00472825  6689b328875000           mov word ptr [ebx + 0x508728], si
0047282c  25ffff0000               and eax, 0xffff
00472831  66898c4328875000         mov word ptr [ebx + eax*2 + 0x508728], cx
00472839  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0047283e  c68402bd00000001         mov byte ptr [edx + eax + 0xbd], 1
00472846  83ff01                   cmp edi, 1
00472849  0f8d2effffff             jge 0x47277d
0047284f  31db                     xor ebx, ebx
00472851  6689cb                   mov bx, cx
00472854  89d8                     mov eax, ebx
00472856  e8caf7fcff               call 0x442025
0047285b  25ff000000               and eax, 0xff
00472860  83f80a                   cmp eax, 0xa
00472863  0f8414ffffff             je 0x47277d
00472869  8a442404                 mov al, byte ptr [esp + 4]
0047286d  3a0541805000             cmp al, byte ptr [0x508041]
00472873  0f8504ffffff             jne 0x47277d
00472879  89d8                     mov eax, ebx
0047287b  e8a5f7fcff               call 0x442025
00472880  25ff000000               and eax, 0xff
00472885  e8bae3fcff               call 0x440c44
0047288a  84c0                     test al, al
0047288c  0f85ebfeffff             jne 0x47277d
00472892  89d8                     mov eax, ebx
00472894  47                       inc edi
00472895  e88bf7fcff               call 0x442025
0047289a  25ff000000               and eax, 0xff
0047289f  83f807                   cmp eax, 7
004728a2  7551                     jne 0x4728f5
004728a4  89d8                     mov eax, ebx
004728a6  e866e5fcff               call 0x440e11
004728ab  25ff000000               and eax, 0xff
004728b0  83f80b                   cmp eax, 0xb
004728b3  7411                     je 0x4728c6
004728b5  89d8                     mov eax, ebx
004728b7  e855e5fcff               call 0x440e11
004728bc  25ff000000               and eax, 0xff
004728c1  83f80f                   cmp eax, 0xf
004728c4  752f                     jne 0x4728f5
004728c6  31f6                     xor esi, esi
004728c8  6689ce                   mov si, cx
004728cb  69d614010000             imul edx, esi, 0x114
004728d1  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004728d6  01d0                     add eax, edx
004728d8  31db                     xor ebx, ebx
004728da  0504010000               add eax, 0x104
004728df  ba16000000               mov edx, 0x16
004728e4  e8d7810100               call 0x48aac0
004728e9  89f0                     mov eax, esi
004728eb  e86ee4fcff               call 0x440d5e
004728f0  e988feffff               jmp 0x47277d
004728f5  ba08000000               mov edx, 8
004728fa  31c0                     xor eax, eax
004728fc  31db                     xor ebx, ebx
004728fe  6689c8                   mov ax, cx
00472901  ebe8                     jmp 0x4728eb
00472903  83c408                   add esp, 8
00472906  5f                       pop edi
00472907  5e                       pop esi
00472908  59                       pop ecx
00472909  5b                       pop ebx
0047290a  c3                       ret
