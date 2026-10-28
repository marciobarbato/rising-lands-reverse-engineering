; MemPlayerCopy [0x45f850, 0x45f871)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f850  56                     push     esi
0045f851  57                     push     edi
0045f852  0fb6f9                 movzx    edi, cl
0045f855  8b3cbdc8244e00         mov      edi, dword ptr [edi*4 + 0x4e24c8]
0045f85c  4b                     dec      ebx
0045f85d  83fbff                 cmp      ebx, -1
0045f860  740c                   je       0x45f86e
0045f862  0fb632                 movzx    esi, byte ptr [edx]
0045f865  8a0c37                 mov      cl, byte ptr [edi + esi]
0045f868  42                     inc      edx
0045f869  8808                   mov      byte ptr [eax], cl
0045f86b  40                     inc      eax
0045f86c  ebee                   jmp      0x45f85c ;
0045f86e  5f                     pop      edi
0045f86f  5e                     pop      esi
0045f870  c3                     ret
