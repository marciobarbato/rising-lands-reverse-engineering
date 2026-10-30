; BatimentGetVolume; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a0ab  53                       push ebx
0041a0ac  51                       push ecx
0041a0ad  52                       push edx
0041a0ae  56                       push esi
0041a0af  57                       push edi
0041a0b0  31d2                     xor edx, edx
0041a0b2  6689c2                   mov dx, ax
0041a0b5  89d0                     mov eax, edx
0041a0b7  c1e004                   shl eax, 4
0041a0ba  01d0                     add eax, edx
0041a0bc  c1e002                   shl eax, 2
0041a0bf  bbc8a04900               mov ebx, 0x49a0c8
0041a0c4  01d0                     add eax, edx
0041a0c6  668b5c8302               mov bx, word ptr [ebx + eax*4 + 2]
0041a0cb  81e3ffff0000             and ebx, 0xffff
0041a0d1  b900010000               mov ecx, 0x100
0041a0d6  89da                     mov edx, ebx
0041a0d8  89d8                     mov eax, ebx
0041a0da  c1fa1f                   sar edx, 0x1f
0041a0dd  f7f9                     idiv ecx
0041a0df  89d7                     mov edi, edx
0041a0e1  89da                     mov edx, ebx
0041a0e3  89d8                     mov eax, ebx
0041a0e5  c1fa1f                   sar edx, 0x1f
0041a0e8  f7f9                     idiv ecx
0041a0ea  31d2                     xor edx, edx
0041a0ec  668b1524875000           mov dx, word ptr [0x508724]
0041a0f3  89c3                     mov ebx, eax
0041a0f5  89d0                     mov eax, edx
0041a0f7  c1fa1f                   sar edx, 0x1f
0041a0fa  2bc2                     sub eax, edx
0041a0fc  d1f8                     sar eax, 1
0041a0fe  31d2                     xor edx, edx
0041a100  668b1520875000           mov dx, word ptr [0x508720]
0041a107  01d0                     add eax, edx
0041a109  31d2                     xor edx, edx
0041a10b  668b1526875000           mov dx, word ptr [0x508726]
0041a112  89c6                     mov esi, eax
0041a114  89d0                     mov eax, edx
0041a116  c1fa1f                   sar edx, 0x1f
0041a119  2bc2                     sub eax, edx
0041a11b  d1f8                     sar eax, 1
0041a11d  31d2                     xor edx, edx
0041a11f  31c9                     xor ecx, ecx
0041a121  668b1522875000           mov dx, word ptr [0x508722]
0041a128  6689d9                   mov cx, bx
0041a12b  01d0                     add eax, edx
0041a12d  31d2                     xor edx, edx
0041a12f  31db                     xor ebx, ebx
0041a131  6689c2                   mov dx, ax
0041a134  31c0                     xor eax, eax
0041a136  6689fb                   mov bx, di
0041a139  6689f0                   mov ax, si
0041a13c  e814f40500               call 0x479555
0041a141  89c3                     mov ebx, eax
0041a143  89c2                     mov edx, eax
0041a145  31c0                     xor eax, eax
0041a147  81fb91000000             cmp ebx, 0x91
0041a14d  7f0a                     jg 0x41a159
0041a14f  b800010000               mov eax, 0x100
0041a154  e9c5390000               jmp 0x41db1e
0041a159  7e12                     jle 0x41a16d
0041a15b  81fb2c010000             cmp ebx, 0x12c
0041a161  7f0a                     jg 0x41a16d
0041a163  b8b4000000               mov eax, 0xb4
0041a168  e9b1390000               jmp 0x41db1e
0041a16d  81fa2c010000             cmp edx, 0x12c
0041a173  0f8ea5390000             jle 0x41db1e
0041a179  81fa58020000             cmp edx, 0x258
0041a17f  0f8d99390000             jge 0x41db1e
0041a185  b864000000               mov eax, 0x64
0041a18a  e98f390000               jmp 0x41db1e
0041a18f  90                       nop
0041a190  4a                       dec edx
0041a191  a24100eba1               mov byte ptr [0xa1eb0041], al
0041a196  41                       inc ecx
0041a197  0029                     add byte ptr [ecx], ch
0041a199  a2410045a2               mov byte ptr [0xa2450041], al
0041a19e  41                       inc ecx
0041a19f  004ea2                   add byte ptr [esi - 0x5e], cl
0041a1a2  41                       inc ecx
0041a1a3  0030                     add byte ptr [eax], dh
0041a1a5  a241003ca2               mov byte ptr [0xa23c0041], al
0041a1aa  41                       inc ecx
; 1 trailing bytes are not code (alignment/data): 00
