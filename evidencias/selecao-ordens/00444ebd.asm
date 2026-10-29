; SetRecolteEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444ebd  53                       push ebx
00444ebe  51                       push ecx
00444ebf  56                       push esi
00444ec0  57                       push edi
00444ec1  89c3                     mov ebx, eax
00444ec3  89d6                     mov esi, edx
00444ec5  31c9                     xor ecx, ecx
00444ec7  6689c1                   mov cx, ax
00444eca  89cf                     mov edi, ecx
00444ecc  c1e704                   shl edi, 4
00444ecf  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444ed5  01cf                     add edi, ecx
00444ed7  89c8                     mov eax, ecx
00444ed9  c1e702                   shl edi, 2
00444edc  e89be6ffff               call 0x44357c
00444ee1  01cf                     add edi, ecx
00444ee3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444ee8  c1e702                   shl edi, 2
00444eeb  01f8                     add eax, edi
00444eed  6689707e                 mov word ptr [eax + 0x7e], si
00444ef1  668b0d04634900           mov cx, word ptr [0x496304]
00444ef8  01fa                     add edx, edi
00444efa  6639cb                   cmp bx, cx
00444efd  7524                     jne 0x444f23
00444eff  30cb                     xor bl, cl
00444f01  881d360f4e00             mov byte ptr [0x4e0f36], bl
00444f07  30ef                     xor bh, ch
00444f09  bfffff0000               mov edi, 0xffff
00444f0e  883d370f4e00             mov byte ptr [0x4e0f37], bh
00444f14  31db                     xor ebx, ebx
00444f16  66893d04634900           mov word ptr [0x496304], di
00444f1d  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00444f23  c6808800000000           mov byte ptr [eax + 0x88], 0
00444f2a  c6828900000000           mov byte ptr [edx + 0x89], 0
00444f31  c6420205                 mov byte ptr [edx + 2], 5
00444f35  c6828200000000           mov byte ptr [edx + 0x82], 0
00444f3c  6689b2b2000000           mov word ptr [edx + 0xb2], si
00444f43  5f                       pop edi
00444f44  5e                       pop esi
00444f45  59                       pop ecx
00444f46  5b                       pop ebx
00444f47  c3                       ret
