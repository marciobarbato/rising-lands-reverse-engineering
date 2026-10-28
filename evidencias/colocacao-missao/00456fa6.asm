; PlaceEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00456fa6  53                       push ebx
00456fa7  51                       push ecx
00456fa8  52                       push edx
00456fa9  56                       push esi
00456faa  57                       push edi
00456fab  25ffff0000               and eax, 0xffff
00456fb0  89c1                     mov ecx, eax
00456fb2  c1e104                   shl ecx, 4
00456fb5  01c1                     add ecx, eax
00456fb7  c1e102                   shl ecx, 2
00456fba  8d1c08                   lea ebx, [eax + ecx]
00456fbd  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00456fc3  c1e302                   shl ebx, 2
00456fc6  668b541908               mov dx, word ptr [ecx + ebx + 8]
00456fcb  81e2ffff0000             and edx, 0xffff
00456fd1  e8debcfeff               call 0x442cb4
00456fd6  c644197201               mov byte ptr [ecx + ebx + 0x72], 1
00456fdb  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00456fe1  01d9                     add ecx, ebx
00456fe3  31db                     xor ebx, ebx
00456fe5  8a19                     mov bl, byte ptr [ecx]
00456fe7  668b7908                 mov di, word ptr [ecx + 8]
00456feb  81fbc8000000             cmp ebx, 0xc8
00456ff1  744d                     je 0x457040
00456ff3  83fb04                   cmp ebx, 4
00456ff6  7448                     je 0x457040
00456ff8  30e4                     xor ah, ah
00456ffa  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00457000  89c2                     mov edx, eax
00457002  83c202                   add edx, 2
00457005  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0045700b  31f6                     xor esi, esi
0045700d  01d0                     add eax, edx
0045700f  31d2                     xor edx, edx
00457011  6689fe                   mov si, di
00457014  6689c2                   mov dx, ax
00457017  89f0                     mov eax, esi
00457019  e833f80100               call 0x476851
0045701e  31db                     xor ebx, ebx
00457020  30f6                     xor dh, dh
00457022  30e4                     xor ah, ah
00457024  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
0045702a  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00457030  01d0                     add eax, edx
00457032  31d2                     xor edx, edx
00457034  8a19                     mov bl, byte ptr [ecx]
00457036  6689c2                   mov dx, ax
00457039  89f0                     mov eax, esi
0045703b  e873fc0100               call 0x476cb3
00457040  ba04000000               mov edx, 4
00457045  31db                     xor ebx, ebx
00457047  31c0                     xor eax, eax
00457049  6689fb                   mov bx, di
0045704c  8a01                     mov al, byte ptr [ecx]
0045704e  e835330100               call 0x46a388
00457053  e9009dfeff               jmp 0x440d58
