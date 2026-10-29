; SetMineEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444f48  53                       push ebx
00444f49  51                       push ecx
00444f4a  56                       push esi
00444f4b  57                       push edi
00444f4c  89c3                     mov ebx, eax
00444f4e  89d1                     mov ecx, edx
00444f50  31f6                     xor esi, esi
00444f52  6689c6                   mov si, ax
00444f55  89f7                     mov edi, esi
00444f57  c1e704                   shl edi, 4
00444f5a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444f60  01f7                     add edi, esi
00444f62  89f0                     mov eax, esi
00444f64  c1e702                   shl edi, 2
00444f67  e810e6ffff               call 0x44357c
00444f6c  01f7                     add edi, esi
00444f6e  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444f73  c1e702                   shl edi, 2
00444f76  89ce                     mov esi, ecx
00444f78  01f8                     add eax, edi
00444f7a  81c600010000             add esi, 0x100
00444f80  6689707e                 mov word ptr [eax + 0x7e], si
00444f84  668b3504634900           mov si, word ptr [0x496304]
00444f8b  01fa                     add edx, edi
00444f8d  6639f3                   cmp bx, si
00444f90  7522                     jne 0x444fb4
00444f92  30db                     xor bl, bl
00444f94  bfffff0000               mov edi, 0xffff
00444f99  881d360f4e00             mov byte ptr [0x4e0f36], bl
00444f9f  881d370f4e00             mov byte ptr [0x4e0f37], bl
00444fa5  31db                     xor ebx, ebx
00444fa7  66893d04634900           mov word ptr [0x496304], di
00444fae  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00444fb4  c6808800000000           mov byte ptr [eax + 0x88], 0
00444fbb  c6828900000000           mov byte ptr [edx + 0x89], 0
00444fc2  c6420205                 mov byte ptr [edx + 2], 5
00444fc6  fec5                     inc ch
00444fc8  c6828200000000           mov byte ptr [edx + 0x82], 0
00444fcf  66898ab2000000           mov word ptr [edx + 0xb2], cx
00444fd6  5f                       pop edi
00444fd7  5e                       pop esi
00444fd8  59                       pop ecx
00444fd9  5b                       pop ebx
00444fda  c3                       ret
