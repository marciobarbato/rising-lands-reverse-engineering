; SortilegeResetTechnologie: limite por próximo símbolo SBL, fim exclusivo 0x00474a38.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004749f2  53                       push     ebx
004749f3  52                       push     edx
004749f4  31d2                     xor      edx, edx
004749f6  eb33                     jmp      0x474a2b
004749f8  30db                     xor      bl, bl
004749fa  42                       inc      edx
004749fb  8898308f5000             mov      byte ptr [eax + 0x508f30], bl
00474a01  8898448f5000             mov      byte ptr [eax + 0x508f44], bl
00474a07  8898358f5000             mov      byte ptr [eax + 0x508f35], bl
00474a0d  8898498f5000             mov      byte ptr [eax + 0x508f49], bl
00474a13  88983a8f5000             mov      byte ptr [eax + 0x508f3a], bl
00474a19  88984e8f5000             mov      byte ptr [eax + 0x508f4e], bl
00474a1f  88983f8f5000             mov      byte ptr [eax + 0x508f3f], bl
00474a25  8898538f5000             mov      byte ptr [eax + 0x508f53], bl
00474a2b  31c0                     xor      eax, eax
00474a2d  6689d0                   mov      ax, dx
00474a30  83f805                   cmp      eax, 5
00474a33  7cc3                     jl       0x4749f8
00474a35  5a                       pop      edx
00474a36  5b                       pop      ebx
00474a37  c3                       ret
