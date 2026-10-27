; TypeCaseBloqueTir; intervalo [0x0047653c, 0x0047656b)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047653c  52                       push     edx
0047653d  89c2                     mov      edx, eax
0047653f  81e2ffff0000             and      edx, 0xffff
00476545  a1707d5000               mov      eax, dword ptr [0x507d70]
0047654a  01d2                     add      edx, edx
0047654c  668b0402                 mov      ax, word ptr [edx + eax]
00476550  25ffff0000               and      eax, 0xffff
00476555  3ddd010000               cmp      eax, 0x1dd
0047655a  7c0b                     jl       0x476567
0047655c  3d60020000               cmp      eax, 0x260
00476561  7d04                     jge      0x476567
00476563  b001                     mov      al, 1
00476565  5a                       pop      edx
00476566  c3                       ret
00476567  30c0                     xor      al, al
00476569  5a                       pop      edx
0047656a  c3                       ret
