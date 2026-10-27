; SetBank [0x418590, 0x418599)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00418590  8b4004                 mov      eax, dword ptr [eax + 4]
00418593  a36c8f5000             mov      dword ptr [0x508f6c], eax
00418598  c3                     ret      
