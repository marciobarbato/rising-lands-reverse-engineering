; ObjectiveCursorQueries_NOT_IMPLEMENTED; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047c39a  53                       push ebx
0047c39b  51                       push ecx
0047c39c  52                       push edx
0047c39d  88c2                     mov dl, al
0047c39f  31c0                     xor eax, eax
0047c3a1  88d0                     mov al, dl
0047c3a3  31c9                     xor ecx, ecx
0047c3a5  8a981c235100             mov bl, byte ptr [eax + 0x51231c]
0047c3ab  88d9                     mov cl, bl
0047c3ad  83f963                   cmp ecx, 0x63
0047c3b0  7d0a                     jge 0x47c3bc
0047c3b2  88de                     mov dh, bl
0047c3b4  fec6                     inc dh
0047c3b6  88b01c235100             mov byte ptr [eax + 0x51231c], dh
0047c3bc  81e2ff000000             and edx, 0xff
0047c3c2  89d0                     mov eax, edx
0047c3c4  c1e002                   shl eax, 2
0047c3c7  29d0                     sub eax, edx
0047c3c9  c1e003                   shl eax, 3
0047c3cc  01c2                     add edx, eax
0047c3ce  31c0                     xor eax, eax
0047c3d0  c1e203                   shl edx, 3
0047c3d3  88d8                     mov al, bl
0047c3d5  668b8442fc1f5100         mov ax, word ptr [edx + eax*2 + 0x511ffc]
0047c3dd  5a                       pop edx
0047c3de  59                       pop ecx
0047c3df  5b                       pop ebx
0047c3e0  c3                       ret
0047c3e1  53                       push ebx
0047c3e2  88d3                     mov bl, dl
0047c3e4  31d2                     xor edx, edx
0047c3e6  88c2                     mov dl, al
0047c3e8  89d0                     mov eax, edx
0047c3ea  c1e002                   shl eax, 2
0047c3ed  29d0                     sub eax, edx
0047c3ef  c1e003                   shl eax, 3
0047c3f2  01d0                     add eax, edx
0047c3f4  31d2                     xor edx, edx
0047c3f6  88da                     mov dl, bl
0047c3f8  01d2                     add edx, edx
0047c3fa  668b84c2fc1f5100         mov ax, word ptr [edx + eax*8 + 0x511ffc]
0047c402  5b                       pop ebx
0047c403  c3                       ret
