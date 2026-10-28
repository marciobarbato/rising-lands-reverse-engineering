; BatimentGetType [0x41a4f4, 0x41a513)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041a4f4  52                     push     edx
0041a4f5  31d2                   xor      edx, edx
0041a4f7  6689c2                 mov      dx, ax
0041a4fa  89d0                   mov      eax, edx
0041a4fc  c1e004                 shl      eax, 4
0041a4ff  01d0                   add      eax, edx
0041a501  c1e002                 shl      eax, 2
0041a504  01d0                   add      eax, edx
0041a506  c1e002                 shl      eax, 2
0041a509  05c8a04900             add      eax, 0x49a0c8
0041a50e  8a4008                 mov      al, byte ptr [eax + 8]
0041a511  5a                     pop      edx
0041a512  c3                     ret
