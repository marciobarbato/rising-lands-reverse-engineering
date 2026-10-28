; EnginApporteMatiere; exclusive end0x456d92.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00456d35  51                       push     ecx
00456d36  88d1                     mov      cl, dl
00456d38  31d2                     xor      edx, edx
00456d3a  6689c2                   mov      dx, ax
00456d3d  89d0                     mov      eax, edx
00456d3f  c1e004                   shl      eax, 4
00456d42  01d0                     add      eax, edx
00456d44  c1e002                   shl      eax, 2
00456d47  01c2                     add      edx, eax
00456d49  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00456d4e  c1e202                   shl      edx, 2
00456d51  01d0                     add      eax, edx
00456d53  31d2                     xor      edx, edx
00456d55  8a5002                   mov      dl, byte ptr [eax + 2]
00456d58  83fa05                   cmp      edx, 5
00456d5b  740a                     je       0x456d67
00456d5d  83fa12                   cmp      edx, 0x12
00456d60  7405                     je       0x456d67
00456d62  83fa11                   cmp      edx, 0x11
00456d65  7527                     jne      0x456d8e
00456d67  31d2                     xor      edx, edx
00456d69  668b9084000000           mov      dx, word ptr [eax + 0x84]
00456d70  81e1ff000000             and      ecx, 0xff
00456d76  39ca                     cmp      edx, ecx
00456d78  7514                     jne      0x456d8e
00456d7a  31ca                     xor      edx, ecx
00456d7c  88da                     mov      dl, bl
00456d7e  85d2                     test     edx, edx
00456d80  7408                     je       0x456d8a
00456d82  3a9882000000             cmp      bl, byte ptr [eax + 0x82]
00456d88  7504                     jne      0x456d8e
00456d8a  b001                     mov      al, 1
00456d8c  59                       pop      ecx
00456d8d  c3                       ret
00456d8e  30c0                     xor      al, al
00456d90  59                       pop      ecx
00456d91  c3                       ret
