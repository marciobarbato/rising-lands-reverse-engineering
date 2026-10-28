; SetSortEngin_vision_sums; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
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
