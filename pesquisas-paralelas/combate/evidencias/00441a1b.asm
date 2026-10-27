; EnginAlloc; intervalo [0x00441a1b, 0x00441ade)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441a1b  53                       push     ebx
00441a1c  51                       push     ecx
00441a1d  52                       push     edx
00441a1e  b8805e0300               mov      eax, 0x35e80
00441a23  e87e640200               call     0x467ea6
00441a28  a3a0194e00               mov      dword ptr [0x4e19a0], eax
00441a2d  b86c000000               mov      eax, 0x6c
00441a32  e86f640200               call     0x467ea6
00441a37  a39c194e00               mov      dword ptr [0x4e199c], eax
00441a3c  b8800c0000               mov      eax, 0xc80
00441a41  31d2                     xor      edx, edx
00441a43  e85e640200               call     0x467ea6
00441a48  a324194e00               mov      dword ptr [0x4e1924], eax
00441a4d  eb18                     jmp      0x441a67
00441a4f  b800020000               mov      eax, 0x200
00441a54  e84d640200               call     0x467ea6
00441a59  89c1                     mov      ecx, eax
00441a5b  89d8                     mov      eax, ebx
00441a5d  8b1d24194e00             mov      ebx, dword ptr [0x4e1924]
00441a63  42                       inc      edx
00441a64  890c83                   mov      dword ptr [ebx + eax*4], ecx
00441a67  31db                     xor      ebx, ebx
00441a69  6689d3                   mov      bx, dx
00441a6c  81fb20030000             cmp      ebx, 0x320
00441a72  7cdb                     jl       0x441a4f
00441a74  31d2                     xor      edx, edx
00441a76  eb19                     jmp      0x441a91
00441a78  b81b000000               mov      eax, 0x1b
00441a7d  e824640200               call     0x467ea6
00441a82  89d9                     mov      ecx, ebx
00441a84  8b1d9c194e00             mov      ebx, dword ptr [0x4e199c]
00441a8a  c1e102                   shl      ecx, 2
00441a8d  42                       inc      edx
00441a8e  890419                   mov      dword ptr [ecx + ebx], eax
00441a91  31db                     xor      ebx, ebx
00441a93  6689d3                   mov      bx, dx
00441a96  83fb1b                   cmp      ebx, 0x1b
00441a99  7cdd                     jl       0x441a78
00441a9b  b810000000               mov      eax, 0x10
00441aa0  e801640200               call     0x467ea6
00441aa5  31d2                     xor      edx, edx
00441aa7  a3b8194e00               mov      dword ptr [0x4e19b8], eax
00441aac  eb18                     jmp      0x441ac6
00441aae  b8900a0000               mov      eax, 0xa90
00441ab3  e8ee630200               call     0x467ea6
00441ab8  89c3                     mov      ebx, eax
00441aba  89c8                     mov      eax, ecx
00441abc  8b0db8194e00             mov      ecx, dword ptr [0x4e19b8]
00441ac2  42                       inc      edx
00441ac3  891c81                   mov      dword ptr [ecx + eax*4], ebx
00441ac6  31c9                     xor      ecx, ecx
00441ac8  6689d1                   mov      cx, dx
00441acb  83f904                   cmp      ecx, 4
00441ace  7cde                     jl       0x441aae
00441ad0  e8b6fdffff               call     0x44188b
00441ad5  e87ffbffff               call     0x441659
00441ada  5a                       pop      edx
00441adb  59                       pop      ecx
00441adc  5b                       pop      ebx
00441add  c3                       ret
