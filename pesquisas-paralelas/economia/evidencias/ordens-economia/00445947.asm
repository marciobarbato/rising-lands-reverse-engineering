; SetRamasseEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00445947  53                       push ebx
00445948  51                       push ecx
00445949  56                       push esi
0044594a  57                       push edi
0044594b  89c3                     mov ebx, eax
0044594d  89d6                     mov esi, edx
0044594f  31c9                     xor ecx, ecx
00445951  6689c1                   mov cx, ax
00445954  89cf                     mov edi, ecx
00445956  c1e704                   shl edi, 4
00445959  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044595f  01cf                     add edi, ecx
00445961  89c8                     mov eax, ecx
00445963  c1e702                   shl edi, 2
00445966  e811dcffff               call 0x44357c
0044596b  01cf                     add edi, ecx
0044596d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445972  c1e702                   shl edi, 2
00445975  01f8                     add eax, edi
00445977  6689707e                 mov word ptr [eax + 0x7e], si
0044597b  668b0d04634900           mov cx, word ptr [0x496304]
00445982  01fa                     add edx, edi
00445984  6639cb                   cmp bx, cx
00445987  7524                     jne 0x4459ad
00445989  30cb                     xor bl, cl
0044598b  881d360f4e00             mov byte ptr [0x4e0f36], bl
00445991  30ef                     xor bh, ch
00445993  bfffff0000               mov edi, 0xffff
00445998  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044599e  31db                     xor ebx, ebx
004459a0  66893d04634900           mov word ptr [0x496304], di
004459a7  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
004459ad  c6808800000000           mov byte ptr [eax + 0x88], 0
004459b4  c6420210                 mov byte ptr [edx + 2], 0x10
004459b8  c6828900000000           mov byte ptr [edx + 0x89], 0
004459bf  e978f5ffff               jmp 0x444f3c
