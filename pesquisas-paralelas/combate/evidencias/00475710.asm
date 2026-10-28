; CreerExplosion; intervalo [0x00475710, 0x00475736)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00475710  53                       push     ebx
00475711  51                       push     ecx
00475712  88d3                     mov      bl, dl
00475714  31d2                     xor      edx, edx
00475716  6689c2                   mov      dx, ax
00475719  a1747d5000               mov      eax, dword ptr [0x507d74]
0047571e  01d0                     add      eax, edx
00475720  31c9                     xor      ecx, ecx
00475722  8a08                     mov      cl, byte ptr [eax]
00475724  85c9                     test     ecx, ecx
00475726  750b                     jne      0x475733
00475728  8818                     mov      byte ptr [eax], bl
0047572a  a1ac7d5000               mov      eax, dword ptr [0x507dac]
0047572f  c6040200                 mov      byte ptr [edx + eax], 0
00475733  59                       pop      ecx
00475734  5b                       pop      ebx
00475735  c3                       ret
