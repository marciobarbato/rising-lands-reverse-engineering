; ResetBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041b9d6  52                       push edx
0041b9d7  31d2                     xor edx, edx
0041b9d9  6689c2                   mov dx, ax
0041b9dc  89d0                     mov eax, edx
0041b9de  c1e004                   shl eax, 4
0041b9e1  01d0                     add eax, edx
0041b9e3  c1e002                   shl eax, 2
0041b9e6  01d0                     add eax, edx
0041b9e8  c1e002                   shl eax, 2
0041b9eb  05c8a04900               add eax, 0x49a0c8
0041b9f0  66c74078ffff             mov word ptr [eax + 0x78], 0xffff
0041b9f6  c6407bff                 mov byte ptr [eax + 0x7b], 0xff
0041b9fa  66c7407c0000             mov word ptr [eax + 0x7c], 0
0041ba00  31d2                     xor edx, edx
0041ba02  66c7407e0000             mov word ptr [eax + 0x7e], 0
0041ba08  8a5008                   mov dl, byte ptr [eax + 8]
0041ba0b  66c78086000000ffff       mov word ptr [eax + 0x86], 0xffff
0041ba14  83fa14                   cmp edx, 0x14
0041ba17  7412                     je 0x41ba2b
0041ba19  66c780800000000000       mov word ptr [eax + 0x80], 0
0041ba22  66c780820000000000       mov word ptr [eax + 0x82], 0
0041ba2b  c6407400                 mov byte ptr [eax + 0x74], 0
0041ba2f  31d2                     xor edx, edx
0041ba31  8a5005                   mov dl, byte ptr [eax + 5]
0041ba34  c7808c00000000000000     mov dword ptr [eax + 0x8c], 0
0041ba3e  83fa03                   cmp edx, 3
0041ba41  7404                     je 0x41ba47
0041ba43  c6400505                 mov byte ptr [eax + 5], 5
0041ba47  5a                       pop edx
0041ba48  c3                       ret
