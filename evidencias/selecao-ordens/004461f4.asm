; EnginInZone; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004461f4  56                       push esi
004461f5  57                       push edi
004461f6  55                       push ebp
004461f7  83ec14                   sub esp, 0x14
004461fa  89c6                     mov esi, eax
004461fc  89d7                     mov edi, edx
004461fe  895c240c                 mov dword ptr [esp + 0xc], ebx
00446202  894c2408                 mov dword ptr [esp + 8], ecx
00446206  31db                     xor ebx, ebx
00446208  6689c3                   mov bx, ax
0044620b  89d8                     mov eax, ebx
0044620d  c1e004                   shl eax, 4
00446210  01d8                     add eax, ebx
00446212  c1e002                   shl eax, 2
00446215  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044621b  01d8                     add eax, ebx
0044621d  8a448201                 mov al, byte ptr [edx + eax*4 + 1]
00446221  30c9                     xor cl, cl
00446223  3c19                     cmp al, 0x19
00446225  0f877a000000             ja 0x4462a5
0044622b  25ff000000               and eax, 0xff
00446230  2eff24858c614400         jmp dword ptr cs:[eax*4 + 0x44618c]
00446238  31db                     xor ebx, ebx
0044623a  6689f3                   mov bx, si
0044623d  89d8                     mov eax, ebx
0044623f  c1e004                   shl eax, 4
00446242  01d8                     add eax, ebx
00446244  c1e002                   shl eax, 2
00446247  01d8                     add eax, ebx
00446249  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044624f  668b5c8308               mov bx, word ptr [ebx + eax*4 + 8]
00446254  81e3ffff0000             and ebx, 0xffff
0044625a  be00010000               mov esi, 0x100
0044625f  89da                     mov edx, ebx
00446261  89d8                     mov eax, ebx
00446263  c1fa1f                   sar edx, 0x1f
00446266  f7fe                     idiv esi
00446268  89d6                     mov esi, edx
0044626a  89da                     mov edx, ebx
0044626c  89d8                     mov eax, ebx
0044626e  c1fa1f                   sar edx, 0x1f
00446271  c1e208                   shl edx, 8
00446274  1bc2                     sbb eax, edx
00446276  c1f808                   sar eax, 8
00446279  6639fe                   cmp si, di
0044627c  0f8223000000             jb 0x4462a5
00446282  663b742408               cmp si, word ptr [esp + 8]
00446287  0f8718000000             ja 0x4462a5
0044628d  663b44240c               cmp ax, word ptr [esp + 0xc]
00446292  0f820d000000             jb 0x4462a5
00446298  663b442424               cmp ax, word ptr [esp + 0x24]
0044629d  0f8702000000             ja 0x4462a5
004462a3  b101                     mov cl, 1
004462a5  88c8                     mov al, cl
004462a7  83c414                   add esp, 0x14
004462aa  5d                       pop ebp
004462ab  5f                       pop edi
004462ac  5e                       pop esi
004462ad  c20400                   ret 4
004462b0  31db                     xor ebx, ebx
004462b2  6689f3                   mov bx, si
004462b5  89d8                     mov eax, ebx
004462b7  c1e004                   shl eax, 4
004462ba  01d8                     add eax, ebx
004462bc  c1e002                   shl eax, 2
004462bf  01d8                     add eax, ebx
004462c1  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
004462c7  668b5c8308               mov bx, word ptr [ebx + eax*4 + 8]
004462cc  81e3ffff0000             and ebx, 0xffff
004462d2  bd00010000               mov ebp, 0x100
004462d7  89da                     mov edx, ebx
004462d9  89d8                     mov eax, ebx
004462db  c1fa1f                   sar edx, 0x1f
004462de  f7fd                     idiv ebp
004462e0  891424                   mov dword ptr [esp], edx
004462e3  89da                     mov edx, ebx
004462e5  89d8                     mov eax, ebx
004462e7  c1fa1f                   sar edx, 0x1f
004462ea  f7fd                     idiv ebp
004462ec  8b1424                   mov edx, dword ptr [esp]
004462ef  6639d7                   cmp di, dx
004462f2  7717                     ja 0x44630b
004462f4  663b542408               cmp dx, word ptr [esp + 8]
004462f9  7710                     ja 0x44630b
004462fb  663b44240c               cmp ax, word ptr [esp + 0xc]
00446300  7209                     jb 0x44630b
00446302  663b442424               cmp ax, word ptr [esp + 0x24]
00446307  7702                     ja 0x44630b
00446309  b101                     mov cl, 1
0044630b  31db                     xor ebx, ebx
0044630d  6689f3                   mov bx, si
00446310  89d8                     mov eax, ebx
00446312  c1e004                   shl eax, 4
00446315  01d8                     add eax, ebx
00446317  c1e002                   shl eax, 2
0044631a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00446320  01d8                     add eax, ebx
00446322  31db                     xor ebx, ebx
00446324  668b5c8208               mov bx, word ptr [edx + eax*4 + 8]
00446329  4b                       dec ebx
0044632a  bd00010000               mov ebp, 0x100
0044632f  89da                     mov edx, ebx
00446331  89d8                     mov eax, ebx
00446333  c1fa1f                   sar edx, 0x1f
00446336  f7fd                     idiv ebp
00446338  89542410                 mov dword ptr [esp + 0x10], edx
0044633c  89da                     mov edx, ebx
0044633e  89d8                     mov eax, ebx
00446340  c1fa1f                   sar edx, 0x1f
00446343  f7fd                     idiv ebp
00446345  8b542410                 mov edx, dword ptr [esp + 0x10]
00446349  6639d7                   cmp di, dx
0044634c  7717                     ja 0x446365
0044634e  663b542408               cmp dx, word ptr [esp + 8]
00446353  7710                     ja 0x446365
00446355  663b44240c               cmp ax, word ptr [esp + 0xc]
0044635a  7209                     jb 0x446365
0044635c  663b442424               cmp ax, word ptr [esp + 0x24]
00446361  7702                     ja 0x446365
00446363  b101                     mov cl, 1
00446365  31db                     xor ebx, ebx
00446367  6689f3                   mov bx, si
0044636a  89d8                     mov eax, ebx
0044636c  c1e004                   shl eax, 4
0044636f  01d8                     add eax, ebx
00446371  c1e002                   shl eax, 2
00446374  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044637a  01d8                     add eax, ebx
0044637c  31db                     xor ebx, ebx
0044637e  668b5c8208               mov bx, word ptr [edx + eax*4 + 8]
00446383  81eb01010000             sub ebx, 0x101
00446389  bd00010000               mov ebp, 0x100
0044638e  89da                     mov edx, ebx
00446390  89d8                     mov eax, ebx
00446392  c1fa1f                   sar edx, 0x1f
00446395  f7fd                     idiv ebp
00446397  89542404                 mov dword ptr [esp + 4], edx
0044639b  89da                     mov edx, ebx
0044639d  89d8                     mov eax, ebx
0044639f  c1fa1f                   sar edx, 0x1f
004463a2  f7fd                     idiv ebp
004463a4  8b542404                 mov edx, dword ptr [esp + 4]
004463a8  6639d7                   cmp di, dx
004463ab  7717                     ja 0x4463c4
004463ad  663b542408               cmp dx, word ptr [esp + 8]
004463b2  7710                     ja 0x4463c4
004463b4  663b44240c               cmp ax, word ptr [esp + 0xc]
004463b9  7209                     jb 0x4463c4
004463bb  663b442424               cmp ax, word ptr [esp + 0x24]
004463c0  7702                     ja 0x4463c4
004463c2  b101                     mov cl, 1
004463c4  31db                     xor ebx, ebx
004463c6  6689f3                   mov bx, si
004463c9  89da                     mov edx, ebx
004463cb  c1e204                   shl edx, 4
004463ce  01da                     add edx, ebx
004463d0  c1e202                   shl edx, 2
004463d3  01da                     add edx, ebx
004463d5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004463da  c1e202                   shl edx, 2
004463dd  31db                     xor ebx, ebx
004463df  668b5c0208               mov bx, word ptr [edx + eax + 8]
004463e4  81eb00010000             sub ebx, 0x100
004463ea  e96bfeffff               jmp 0x44625a
