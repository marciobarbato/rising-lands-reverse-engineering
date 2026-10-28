; BagVide [0x4470b9, 0x4470c5)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004470b9  668b00                 mov      ax, word ptr [eax]
004470bc  25ffff0000             and      eax, 0xffff
004470c1  0f94c0                 sete     al
004470c4  c3                     ret
