; BatimentEstHabiter [0x41a5b8, 0x41a61c)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041a5b8  53                     push     ebx
0041a5b9  52                     push     edx
0041a5ba  31d2                   xor      edx, edx
0041a5bc  6689c2                 mov      dx, ax
0041a5bf  89d0                   mov      eax, edx
0041a5c1  c1e004                 shl      eax, 4
0041a5c4  01d0                   add      eax, edx
0041a5c6  c1e002                 shl      eax, 2
0041a5c9  01d0                   add      eax, edx
0041a5cb  bac8a04900             mov      edx, 0x49a0c8
0041a5d0  c1e002                 shl      eax, 2
0041a5d3  01c2                   add      edx, eax
0041a5d5  31db                   xor      ebx, ebx
0041a5d7  8a4208                 mov      al, byte ptr [edx + 8]
0041a5da  88c3                   mov      bl, al
0041a5dc  8d420c                 lea      eax, [edx + 0xc]
0041a5df  83fb15                 cmp      ebx, 0x15
0041a5e2  750e                   jne      0x41a5f2
0041a5e4  e861cc0200             call     0x44724a ; BagContientTroupe
0041a5e9  84c0                   test     al, al
0041a5eb  742a                   je       0x41a617
0041a5ed  b001                   mov      al, 1
0041a5ef  5a                     pop      edx
0041a5f0  5b                     pop      ebx
0041a5f1  c3                     ret
0041a5f2  83fb02                 cmp      ebx, 2
0041a5f5  7509                   jne      0x41a600
0041a5f7  e84ecc0200             call     0x44724a ; BagContientTroupe
0041a5fc  84c0                   test     al, al
0041a5fe  75ed                   jne      0x41a5ed
0041a600  8d420c                 lea      eax, [edx + 0xc]
0041a603  bb09000000             mov      ebx, 9
0041a608  ba01000000             mov      edx, 1
0041a60d  e8a6cb0200             call     0x4471b8 ; BagContient
0041a612  6685c0                 test     ax, ax
0041a615  ebd4                   jmp      0x41a5eb ;
0041a617  30c0                   xor      al, al
0041a619  5a                     pop      edx
0041a61a  5b                     pop      ebx
0041a61b  c3                     ret
