; PlaceEngin_vision_sums; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
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
