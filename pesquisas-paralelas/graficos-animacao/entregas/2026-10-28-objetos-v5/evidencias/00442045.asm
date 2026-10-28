; EnginGetPlayer [0x442045, 0x442064)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00442045  52                     push     edx
00442046  31d2                   xor      edx, edx
00442048  6689c2                 mov      dx, ax
0044204b  89d0                   mov      eax, edx
0044204d  c1e004                 shl      eax, 4
00442050  01d0                   add      eax, edx
00442052  c1e002                 shl      eax, 2
00442055  01c2                   add      edx, eax
00442057  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
0044205c  c1e202                 shl      edx, 2
0044205f  8a0402                 mov      al, byte ptr [edx + eax]
00442062  5a                     pop      edx
00442063  c3                     ret
