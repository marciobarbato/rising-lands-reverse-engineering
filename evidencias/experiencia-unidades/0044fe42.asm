; EnginSetExperimente; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044fe42  53                       push ebx
0044fe43  51                       push ecx
0044fe44  52                       push edx
0044fe45  56                       push esi
0044fe46  57                       push edi
0044fe47  31c9                     xor ecx, ecx
0044fe49  6689c1                   mov cx, ax
0044fe4c  89cf                     mov edi, ecx
0044fe4e  c1e704                   shl edi, 4
0044fe51  01cf                     add edi, ecx
0044fe53  c1e702                   shl edi, 2
0044fe56  01cf                     add edi, ecx
0044fe58  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044fe5e  c1e702                   shl edi, 2
0044fe61  01fb                     add ebx, edi
0044fe63  0fb633                   movzx esi, byte ptr [ebx]
0044fe66  89f0                     mov eax, esi
0044fe68  c1e002                   shl eax, 2
0044fe6b  01f0                     add eax, esi
0044fe6d  01c0                     add eax, eax
0044fe6f  80b8c5194e0000           cmp byte ptr [eax + 0x4e19c5], 0
0044fe76  0f84dc0effff             je 0x440d58
0044fe7c  8a90c4194e00             mov dl, byte ptr [eax + 0x4e19c4]
0044fe82  3a5301                   cmp dl, byte ptr [ebx + 1]
0044fe85  0f85cd0effff             jne 0x440d58
0044fe8b  8a80c5194e00             mov al, byte ptr [eax + 0x4e19c5]
0044fe91  8883af000000             mov byte ptr [ebx + 0xaf], al
0044fe97  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044fe9c  8a8407af000000           mov al, byte ptr [edi + eax + 0xaf]
0044fea3  31d2                     xor edx, edx
0044fea5  c0e805                   shr al, 5
0044fea8  88c2                     mov dl, al
0044feaa  89c8                     mov eax, ecx
0044feac  e82ffbffff               call 0x44f9e0
0044feb1  31d2                     xor edx, edx
0044feb3  eb2e                     jmp 0x44fee3
0044feb5  0fb633                   movzx esi, byte ptr [ebx]
0044feb8  6bce0a                   imul ecx, esi, 0xa
0044febb  8d3400                   lea esi, [eax + eax]
0044febe  8d0431                   lea eax, [ecx + esi]
0044fec1  8a88c7194e00             mov cl, byte ptr [eax + 0x4e19c7]
0044fec7  8888c5194e00             mov byte ptr [eax + 0x4e19c5], cl
0044fecd  31c0                     xor eax, eax
0044fecf  8a03                     mov al, byte ptr [ebx]
0044fed1  6bc00a                   imul eax, eax, 0xa
0044fed4  8a8c06c6194e00           mov cl, byte ptr [esi + eax + 0x4e19c6]
0044fedb  42                       inc edx
0044fedc  888c06c4194e00           mov byte ptr [esi + eax + 0x4e19c4], cl
0044fee3  31c0                     xor eax, eax
0044fee5  6689d0                   mov ax, dx
0044fee8  83f804                   cmp eax, 4
0044feeb  7cc8                     jl 0x44feb5
0044feed  31c9                     xor ecx, ecx
0044feef  8a0b                     mov cl, byte ptr [ebx]
0044fef1  89c8                     mov eax, ecx
0044fef3  c1e002                   shl eax, 2
0044fef6  01c8                     add eax, ecx
0044fef8  30c9                     xor cl, cl
0044fefa  880c45cd194e00           mov byte ptr [eax*2 + 0x4e19cd], cl
0044ff01  8a1b                     mov bl, byte ptr [ebx]
0044ff03  81e3ff000000             and ebx, 0xff
0044ff09  89d8                     mov eax, ebx
0044ff0b  c1e002                   shl eax, 2
0044ff0e  01d8                     add eax, ebx
0044ff10  c60445cc194e00ff         mov byte ptr [eax*2 + 0x4e19cc], 0xff
0044ff18  e93b0effff               jmp 0x440d58
