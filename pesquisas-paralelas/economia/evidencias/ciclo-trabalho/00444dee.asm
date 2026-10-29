; SetDechargeCaveEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444dee  53                       push ebx
00444def  51                       push ecx
00444df0  56                       push esi
00444df1  89c1                     mov ecx, eax
00444df3  89d3                     mov ebx, edx
00444df5  31d2                     xor edx, edx
00444df7  6689c2                   mov dx, ax
00444dfa  89d6                     mov esi, edx
00444dfc  c1e604                   shl esi, 4
00444dff  01d6                     add esi, edx
00444e01  c1e602                   shl esi, 2
00444e04  01d6                     add esi, edx
00444e06  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444e0c  c1e602                   shl esi, 2
00444e0f  31c0                     xor eax, eax
00444e11  c644320214               mov byte ptr [edx + esi + 2], 0x14
00444e16  6689d8                   mov ax, bx
00444e19  c684328900000000         mov byte ptr [edx + esi + 0x89], 0
00444e21  e8bc60fdff               call 0x41aee2
00444e26  66898432b2000000         mov word ptr [edx + esi + 0xb2], ax
00444e2e  66899c32c0000000         mov word ptr [edx + esi + 0xc0], bx
00444e36  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444e3b  01f0                     add eax, esi
00444e3d  668b9432b2000000         mov dx, word ptr [edx + esi + 0xb2]
00444e45  6689507e                 mov word ptr [eax + 0x7e], dx
00444e49  663b0d04634900           cmp cx, word ptr [0x496304]
00444e50  7522                     jne 0x444e74
00444e52  30d2                     xor dl, dl
00444e54  bbffff0000               mov ebx, 0xffff
00444e59  8815360f4e00             mov byte ptr [0x4e0f36], dl
00444e5f  8815370f4e00             mov byte ptr [0x4e0f37], dl
00444e65  31d2                     xor edx, edx
00444e67  66891d04634900           mov word ptr [0x496304], bx
00444e6e  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00444e74  c6808800000000           mov byte ptr [eax + 0x88], 0
00444e7b  5e                       pop esi
00444e7c  59                       pop ecx
00444e7d  5b                       pop ebx
00444e7e  c3                       ret
