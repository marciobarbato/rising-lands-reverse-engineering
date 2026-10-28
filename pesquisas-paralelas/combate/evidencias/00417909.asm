; AffGameFiltroDesenho; intervalo [0x00417909, 0x0041792b)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00417909  803da2054e0000           cmp      byte ptr [0x4e05a2], 0
00417910  7519                     jne      0x41792b
00417912  a17c8f5000               mov      eax, dword ptr [0x508f7c]
00417917  31db                     xor      ebx, ebx
00417919  31d2                     xor      edx, edx
0041791b  8a1d84724900             mov      bl, byte ptr [0x497284]
00417921  f7f3                     div      ebx
00417923  85d2                     test     edx, edx
00417925  0f8504060000             jne      0x417f2f
