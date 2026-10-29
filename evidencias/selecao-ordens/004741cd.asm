; EnginAddSelection; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004741cd  53                       push ebx
004741ce  51                       push ecx
004741cf  56                       push esi
004741d0  57                       push edi
004741d1  89c3                     mov ebx, eax
004741d3  88d1                     mov cl, dl
004741d5  31d2                     xor edx, edx
004741d7  6689c2                   mov dx, ax
004741da  89d0                     mov eax, edx
004741dc  e8ccfbfcff               call 0x443dad
004741e1  84c0                     test al, al
004741e3  0f84ee000000             je 0x4742d7
004741e9  89d0                     mov eax, edx
004741eb  c1e004                   shl eax, 4
004741ee  01d0                     add eax, edx
004741f0  c1e002                   shl eax, 2
004741f3  01c2                     add edx, eax
004741f5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004741fa  c1e202                   shl edx, 2
004741fd  01d0                     add eax, edx
004741ff  31d2                     xor edx, edx
00474201  8a5002                   mov dl, byte ptr [eax + 2]
00474204  89de                     mov esi, ebx
00474206  83fa0e                   cmp edx, 0xe
00474209  742c                     je 0x474237
0047420b  0fb67801                 movzx edi, byte ptr [eax + 1]
0047420f  83ff10                   cmp edi, 0x10
00474212  7515                     jne 0x474229
00474214  83fa0d                   cmp edx, 0xd
00474217  7510                     jne 0x474229
00474219  8a80ab000000             mov al, byte ptr [eax + 0xab]
0047421f  25ff000000               and eax, 0xff
00474224  83f832                   cmp eax, 0x32
00474227  750e                     jne 0x474237
00474229  31c0                     xor eax, eax
0047422b  6689f0                   mov ax, si
0047422e  e88c23fdff               call 0x4465bf
00474233  84c0                     test al, al
00474235  7504                     jne 0x47423b
00474237  30c0                     xor al, al
00474239  eb02                     jmp 0x47423d
0047423b  b001                     mov al, 1
0047423d  84c0                     test al, al
0047423f  0f8492000000             je 0x4742d7
00474245  31d2                     xor edx, edx
00474247  6689da                   mov dx, bx
0047424a  89d0                     mov eax, edx
0047424c  e8f4ddfcff               call 0x442045
00474251  38c8                     cmp al, cl
00474253  0f857e000000             jne 0x4742d7
00474259  89d0                     mov eax, edx
0047425b  c1e004                   shl eax, 4
0047425e  01d0                     add eax, edx
00474260  c1e002                   shl eax, 2
00474263  01d0                     add eax, edx
00474265  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0047426b  c1e002                   shl eax, 2
0047426e  01c2                     add edx, eax
00474270  80babd00000000           cmp byte ptr [edx + 0xbd], 0
00474277  755e                     jne 0x4742d7
00474279  31c0                     xor eax, eax
0047427b  88c8                     mov al, cl
0047427d  c1e009                   shl eax, 9
00474280  31c9                     xor ecx, ecx
00474282  668b8828875000           mov cx, word ptr [eax + 0x508728]
00474289  81f9ff000000             cmp ecx, 0xff
0047428f  7d21                     jge 0x4742b2
00474291  41                       inc ecx
00474292  66898828875000           mov word ptr [eax + 0x508728], cx
00474299  81e1ffff0000             and ecx, 0xffff
0047429f  66899c4828875000         mov word ptr [eax + ecx*2 + 0x508728], bx
004742a7  b001                     mov al, 1
004742a9  c682bd00000001           mov byte ptr [edx + 0xbd], 1
004742b0  eb02                     jmp 0x4742b4
004742b2  30c0                     xor al, al
004742b4  84c0                     test al, al
004742b6  741f                     je 0x4742d7
004742b8  31d2                     xor edx, edx
004742ba  6689da                   mov dx, bx
004742bd  89d0                     mov eax, edx
004742bf  c1e004                   shl eax, 4
004742c2  01d0                     add eax, edx
004742c4  c1e002                   shl eax, 2
004742c7  01d0                     add eax, edx
004742c9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004742cf  c68482bd00000001         mov byte ptr [edx + eax*4 + 0xbd], 1
004742d7  5f                       pop edi
004742d8  5e                       pop esi
004742d9  59                       pop ecx
004742da  5b                       pop ebx
004742db  c3                       ret
