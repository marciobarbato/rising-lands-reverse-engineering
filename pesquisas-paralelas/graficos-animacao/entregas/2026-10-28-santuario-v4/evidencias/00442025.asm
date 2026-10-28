; EnginGetType [0x442025, 0x442045)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00442025  52                     push     edx
00442026  31d2                   xor      edx, edx
00442028  6689c2                 mov      dx, ax
0044202b  89d0                   mov      eax, edx
0044202d  c1e004                 shl      eax, 4
00442030  01d0                   add      eax, edx
00442032  c1e002                 shl      eax, 2
00442035  01c2                   add      edx, eax
00442037  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
0044203c  c1e202                 shl      edx, 2
0044203f  8a440201               mov      al, byte ptr [edx + eax + 1]
00442043  5a                     pop      edx
00442044  c3                     ret
