; MatiereEstDemander_ordem_pecas_comida_pedra: limite por trecho de contexto; não é função independente nem execução até RET, fim exclusivo 0x00464c1a.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00464bee  52                       push     edx
00464bef  668bb0fe2c4e00           mov      si, word ptr [eax + 0x4e2cfe]
00464bf6  668b88002d4e00           mov      cx, word ptr [eax + 0x4e2d00]
00464bfd  31db                     xor      ebx, ebx
00464bff  668b80fc2c4e00           mov      ax, word ptr [eax + 0x4e2cfc]
00464c06  31d2                     xor      edx, edx
00464c08  6689c3                   mov      bx, ax
00464c0b  6689ca                   mov      dx, cx
00464c0e  31c0                     xor      eax, eax
00464c10  31c9                     xor      ecx, ecx
00464c12  6689f0                   mov      ax, si
00464c15  e8cb2a0000               call     0x4676e5
