; TerrainEstObstacleNaturel; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004752b8  53                       push ebx
004752b9  52                       push edx
004752ba  31d2                     xor edx, edx
004752bc  8b1d707d5000             mov ebx, dword ptr [0x507d70]
004752c2  6689c2                   mov dx, ax
004752c5  668b1453                 mov dx, word ptr [ebx + edx*2]
004752c9  81e2ffff0000             and edx, 0xffff
004752cf  81fabe020000             cmp edx, 0x2be
004752d5  7d11                     jge 0x4752e8
004752d7  8b1db07d5000             mov ebx, dword ptr [0x507db0]
004752dd  803c1a00                 cmp byte ptr [edx + ebx], 0
004752e1  7405                     je 0x4752e8
004752e3  b001                     mov al, 1
004752e5  5a                       pop edx
004752e6  5b                       pop ebx
004752e7  c3                       ret
004752e8  31d2                     xor edx, edx
004752ea  6689c2                   mov dx, ax
004752ed  a1747d5000               mov eax, dword ptr [0x507d74]
004752f2  8a0402                   mov al, byte ptr [edx + eax]
004752f5  3c01                     cmp al, 1
004752f7  7204                     jb 0x4752fd
004752f9  3c0b                     cmp al, 0xb
004752fb  76e6                     jbe 0x4752e3
004752fd  30c0                     xor al, al
004752ff  5a                       pop edx
00475300  5b                       pop ebx
00475301  c3                       ret
