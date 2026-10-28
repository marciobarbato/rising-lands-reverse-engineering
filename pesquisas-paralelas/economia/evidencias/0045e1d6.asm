; IconeFillContenu_teste_de_custos_de_aprendizagem: limite por trecho de contexto; não é função independente nem execução até RET, fim exclusivo 0x0045e210.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0045e1d6  8d4c245c                 lea      ecx, [esp + 0x5c]
0045e1da  8d5c2438                 lea      ebx, [esp + 0x38]
0045e1de  8d542404                 lea      edx, [esp + 4]
0045e1e2  89f8                     mov      eax, edi
0045e1e4  e815650100               call     0x4746fe
0045e1e9  31c0                     xor      eax, eax
0045e1eb  31d2                     xor      edx, edx
0045e1ed  31c9                     xor      ecx, ecx
0045e1ef  a041805000               mov      al, byte ptr [0x508041]
0045e1f4  31db                     xor      ebx, ebx
0045e1f6  50                       push     eax
0045e1f7  31c0                     xor      eax, eax
0045e1f9  668b54243c               mov      dx, word ptr [esp + 0x3c]
0045e1fe  668b442408               mov      ax, word ptr [esp + 8]
0045e203  e8dd940000               call     0x4676e5
0045e208  84c0                     test     al, al
0045e20a  0f8475000000             je       0x45e285
