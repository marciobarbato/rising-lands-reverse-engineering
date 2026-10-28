; SetCyclage [0x45f5ac, 0x45f5de)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f5ac  51                     push     ecx
0045f5ad  88c1                   mov      cl, al
0045f5af  88d5                   mov      ch, dl
0045f5b1  31d2                   xor      edx, edx
0045f5b3  8a15e1244e00           mov      dl, byte ptr [0x4e24e1]
0045f5b9  89d0                   mov      eax, edx
0045f5bb  c1e002                 shl      eax, 2
0045f5be  29d0                   sub      eax, edx
0045f5c0  8888e4244e00           mov      byte ptr [eax + 0x4e24e4], cl
0045f5c6  88a8e5244e00           mov      byte ptr [eax + 0x4e24e5], ch
0045f5cc  8898e6244e00           mov      byte ptr [eax + 0x4e24e6], bl
0045f5d2  88d4                   mov      ah, dl
0045f5d4  fec4                   inc      ah
0045f5d6  8825e1244e00           mov      byte ptr [0x4e24e1], ah
0045f5dc  59                     pop      ecx
0045f5dd  c3                     ret
