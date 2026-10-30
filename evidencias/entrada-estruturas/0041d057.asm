; BatimentGetCaseEntrer; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041d057  53                       push ebx
0041d058  89d3                     mov ebx, edx
0041d05a  31d2                     xor edx, edx
0041d05c  6689c2                   mov dx, ax
0041d05f  89d0                     mov eax, edx
0041d061  c1e004                   shl eax, 4
0041d064  01d0                     add eax, edx
0041d066  c1e002                   shl eax, 2
0041d069  01d0                     add eax, edx
0041d06b  bac8a04900               mov edx, 0x49a0c8
0041d070  c1e002                   shl eax, 2
0041d073  01c2                     add edx, eax
0041d075  8a4208                   mov al, byte ptr [edx + 8]
0041d078  3c08                     cmp al, 8
0041d07a  7253                     jb 0x41d0cf
0041d07c  760f                     jbe 0x41d08d
0041d07e  3c0e                     cmp al, 0xe
0041d080  754d                     jne 0x41d0cf
0041d082  668b4202                 mov ax, word ptr [edx + 2]
0041d086  0502040000               add eax, 0x402
0041d08b  5b                       pop ebx
0041d08c  c3                       ret
0041d08d  81e3ffff0000             and ebx, 0xffff
0041d093  89d8                     mov eax, ebx
0041d095  e88b4f0200               call 0x442025
0041d09a  25ff000000               and eax, 0xff
0041d09f  83f803                   cmp eax, 3
0041d0a2  750b                     jne 0x41d0af
0041d0a4  668b4202                 mov ax, word ptr [edx + 2]
0041d0a8  0503040000               add eax, 0x403
0041d0ad  5b                       pop ebx
0041d0ae  c3                       ret
0041d0af  89d8                     mov eax, ebx
0041d0b1  e86f4f0200               call 0x442025
0041d0b6  25ff000000               and eax, 0xff
0041d0bb  e874530200               call 0x442434
0041d0c0  84c0                     test al, al
0041d0c2  75e0                     jne 0x41d0a4
0041d0c4  668b4202                 mov ax, word ptr [edx + 2]
0041d0c8  0503030000               add eax, 0x303
0041d0cd  5b                       pop ebx
0041d0ce  c3                       ret
0041d0cf  31c0                     xor eax, eax
0041d0d1  5b                       pop ebx
0041d0d2  c3                       ret
