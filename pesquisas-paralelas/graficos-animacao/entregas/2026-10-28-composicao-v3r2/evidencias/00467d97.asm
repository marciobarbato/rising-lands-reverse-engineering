; GetBit [0x467d97, 0x467da6)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00467d97  51                     push     ecx
00467d98  25ff000000             and      eax, 0xff
00467d9d  88d1                   mov      cl, dl
00467d9f  d3f8                   sar      eax, cl
00467da1  83e001                 and      eax, 1
00467da4  59                     pop      ecx
00467da5  c3                     ret
