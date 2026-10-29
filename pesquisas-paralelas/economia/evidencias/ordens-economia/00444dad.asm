; SetDepotEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444dad  83ec04                   sub esp, 4
00444db0  881424                   mov byte ptr [esp], dl
00444db3  31d2                     xor edx, edx
00444db5  6689c2                   mov dx, ax
00444db8  89d0                     mov eax, edx
00444dba  c1e004                   shl eax, 4
00444dbd  01d0                     add eax, edx
00444dbf  c1e002                   shl eax, 2
00444dc2  01d0                     add eax, edx
00444dc4  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444dca  c1e002                   shl eax, 2
00444dcd  01c2                     add edx, eax
00444dcf  8a0424                   mov al, byte ptr [esp]
00444dd2  888282000000             mov byte ptr [edx + 0x82], al
00444dd8  30e4                     xor ah, ah
00444dda  66899a80000000           mov word ptr [edx + 0x80], bx
00444de1  88c8                     mov al, cl
00444de3  66898284000000           mov word ptr [edx + 0x84], ax
00444dea  83c404                   add esp, 4
00444ded  c3                       ret
