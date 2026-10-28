; MemOmbreCopy [0x45f7ba, 0x45f7d8)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f7ba  53                     push     ebx
0045f7bb  51                     push     ecx
0045f7bc  4a                     dec      edx
0045f7bd  83faff                 cmp      edx, -1
0045f7c0  0f8418ffffff           je       0x45f6de
0045f7c6  31db                   xor      ebx, ebx
0045f7c8  8b0db4244e00           mov      ecx, dword ptr [0x4e24b4]
0045f7ce  8a18                   mov      bl, byte ptr [eax]
0045f7d0  8a1c19                 mov      bl, byte ptr [ecx + ebx]
0045f7d3  8818                   mov      byte ptr [eax], bl
0045f7d5  40                     inc      eax
0045f7d6  ebe4                   jmp      0x45f7bc ;
