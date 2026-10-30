; EnginGetEtat; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00440e11  52                       push edx
00440e12  31d2                     xor edx, edx
00440e14  6689c2                   mov dx, ax
00440e17  89d0                     mov eax, edx
00440e19  c1e004                   shl eax, 4
00440e1c  01d0                     add eax, edx
00440e1e  c1e002                   shl eax, 2
00440e21  01c2                     add edx, eax
00440e23  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00440e28  c1e202                   shl edx, 2
00440e2b  8a440202                 mov al, byte ptr [edx + eax + 2]
00440e2f  5a                       pop edx
00440e30  c3                       ret
