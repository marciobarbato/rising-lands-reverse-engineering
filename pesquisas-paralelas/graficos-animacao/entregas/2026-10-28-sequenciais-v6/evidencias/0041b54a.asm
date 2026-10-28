; ChercheIndiceBatiment [0x41b54a, 0x41b579)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041b54a  52                     push     edx
0041b54b  25ffff0000             and      eax, 0xffff
0041b550  8b15380f4e00           mov      edx, dword ptr [0x4e0f38]
0041b556  01c0                   add      eax, eax
0041b558  01d0                   add      eax, edx
0041b55a  f6400180               test     byte ptr [eax + 1], 0x80
0041b55e  7412                   je       0x41b572
0041b560  668b00                 mov      ax, word ptr [eax]
0041b563  25e07f0000             and      eax, 0x7fe0
0041b568  25ffff0000             and      eax, 0xffff
0041b56d  c1f805                 sar      eax, 5
0041b570  5a                     pop      edx
0041b571  c3                     ret
0041b572  b8ffff0000             mov      eax, 0xffff
0041b577  5a                     pop      edx
0041b578  c3                     ret
