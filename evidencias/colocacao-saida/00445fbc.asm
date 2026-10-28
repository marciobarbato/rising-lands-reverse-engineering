; SetSortEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00445fbc  53                       push ebx
00445fbd  51                       push ecx
00445fbe  56                       push esi
00445fbf  57                       push edi
00445fc0  83ec08                   sub esp, 8
00445fc3  89c3                     mov ebx, eax
00445fc5  31c9                     xor ecx, ecx
00445fc7  6689c1                   mov cx, ax
00445fca  89c8                     mov eax, ecx
00445fcc  c1e004                   shl eax, 4
00445fcf  01c8                     add eax, ecx
00445fd1  c1e002                   shl eax, 2
00445fd4  01c1                     add ecx, eax
00445fd6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445fdb  c1e102                   shl ecx, 2
00445fde  01c8                     add eax, ecx
00445fe0  6689507e                 mov word ptr [eax + 0x7e], dx
00445fe4  6689507c                 mov word ptr [eax + 0x7c], dx
00445fe8  66895008                 mov word ptr [eax + 8], dx
00445fec  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
00445ff2  01f1                     add ecx, esi
00445ff4  6689517e                 mov word ptr [ecx + 0x7e], dx
00445ff8  663b1d04634900           cmp bx, word ptr [0x496304]
00445fff  7522                     jne 0x446023
00446001  30d2                     xor dl, dl
00446003  beffff0000               mov esi, 0xffff
00446008  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044600e  8815370f4e00             mov byte ptr [0x4e0f37], dl
00446014  31d2                     xor edx, edx
00446016  66893504634900           mov word ptr [0x496304], si
0044601d  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00446023  31f6                     xor esi, esi
00446025  6689de                   mov si, bx
00446028  89f2                     mov edx, esi
0044602a  c1e204                   shl edx, 4
0044602d  c6818800000000           mov byte ptr [ecx + 0x88], 0
00446034  01f2                     add edx, esi
00446036  b107                     mov cl, 7
00446038  c1e202                   shl edx, 2
0044603b  884c2404                 mov byte ptr [esp + 4], cl
0044603f  01f2                     add edx, esi
00446041  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00446047  c1e202                   shl edx, 2
0044604a  89df                     mov edi, ebx
0044604c  8a4c1102                 mov cl, byte ptr [ecx + edx + 2]
00446050  81e1ff000000             and ecx, 0xff
00446056  7409                     je 0x446061
00446058  83f904                   cmp ecx, 4
0044605b  7404                     je 0x446061
0044605d  b201                     mov dl, 1
0044605f  eb02                     jmp 0x446063
00446061  30d2                     xor dl, dl
00446063  84d2                     test dl, dl
00446065  744b                     je 0x4460b2
00446067  31f6                     xor esi, esi
00446069  6689fe                   mov si, di
0044606c  89f1                     mov ecx, esi
0044606e  c1e104                   shl ecx, 4
00446071  01f1                     add ecx, esi
00446073  c1e102                   shl ecx, 2
00446076  01f1                     add ecx, esi
00446078  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044607e  c1e102                   shl ecx, 2
00446081  01ca                     add edx, ecx
00446083  8a4c2404                 mov cl, byte ptr [esp + 4]
00446087  884a02                   mov byte ptr [edx + 2], cl
0044608a  663b3d04634900           cmp di, word ptr [0x496304]
00446091  751f                     jne 0x4460b2
00446093  30ed                     xor ch, ch
00446095  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044609b  882d370f4e00             mov byte ptr [0x4e0f37], ch
004460a1  31c9                     xor ecx, ecx
004460a3  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
004460a9  66c70504634900ffff       mov word ptr [0x496304], 0xffff
004460b2  66c780c0000000ffff       mov word ptr [eax + 0xc0], 0xffff
004460bb  66c780b8000000ffff       mov word ptr [eax + 0xb8], 0xffff
004460c4  c6808700000000           mov byte ptr [eax + 0x87], 0
004460cb  31f6                     xor esi, esi
004460cd  8a9087000000             mov dl, byte ptr [eax + 0x87]
004460d3  6689de                   mov si, bx
004460d6  889086000000             mov byte ptr [eax + 0x86], dl
004460dc  89f0                     mov eax, esi
004460de  c1e004                   shl eax, 4
004460e1  01f0                     add eax, esi
004460e3  c1e002                   shl eax, 2
004460e6  8d1c06                   lea ebx, [esi + eax]
004460e9  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
004460ef  c1e302                   shl ebx, 2
004460f2  31d2                     xor edx, edx
004460f4  668b441908               mov ax, word ptr [ecx + ebx + 8]
004460f9  6689c2                   mov dx, ax
004460fc  89f0                     mov eax, esi
004460fe  e8b1cbffff               call 0x442cb4
00446103  c644197201               mov byte ptr [ecx + ebx + 0x72], 1
00446108  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
0044610e  01d9                     add ecx, ebx
00446110  31db                     xor ebx, ebx
00446112  8a19                     mov bl, byte ptr [ecx]
00446114  668b7908                 mov di, word ptr [ecx + 8]
00446118  81fbc8000000             cmp ebx, 0xc8
0044611e  7451                     je 0x446171
00446120  83fb04                   cmp ebx, 4
00446123  744c                     je 0x446171
00446125  30e4                     xor ah, ah
00446127  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0044612d  89c2                     mov edx, eax
0044612f  83c202                   add edx, 2
00446132  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00446138  31f6                     xor esi, esi
0044613a  01d0                     add eax, edx
0044613c  31d2                     xor edx, edx
0044613e  6689fe                   mov si, di
00446141  6689c2                   mov dx, ax
00446144  89f0                     mov eax, esi
00446146  e806070300               call 0x476851
0044614b  30e4                     xor ah, ah
0044614d  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00446153  890424                   mov dword ptr [esp], eax
00446156  8b1424                   mov edx, dword ptr [esp]
00446159  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0044615f  31db                     xor ebx, ebx
00446161  01d0                     add eax, edx
00446163  31d2                     xor edx, edx
00446165  8a19                     mov bl, byte ptr [ecx]
00446167  6689c2                   mov dx, ax
0044616a  89f0                     mov eax, esi
0044616c  e8420b0300               call 0x476cb3
00446171  ba04000000               mov edx, 4
00446176  31db                     xor ebx, ebx
00446178  31c0                     xor eax, eax
0044617a  6689fb                   mov bx, di
0044617d  8a01                     mov al, byte ptr [ecx]
0044617f  e804420200               call 0x46a388
00446184  e972d0ffff               jmp 0x4431fb
