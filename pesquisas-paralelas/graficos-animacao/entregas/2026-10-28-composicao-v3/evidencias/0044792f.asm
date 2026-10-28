; AnimDyingEngin [0x44792f, 0x447977)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0044792f  53                     push     ebx
00447930  51                     push     ecx
00447931  52                     push     edx
00447932  31d2                   xor      edx, edx
00447934  6689c2                 mov      dx, ax
00447937  89d0                   mov      eax, edx
00447939  c1e004                 shl      eax, 4
0044793c  01d0                   add      eax, edx
0044793e  c1e002                 shl      eax, 2
00447941  01d0                   add      eax, edx
00447943  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
00447949  c1e002                 shl      eax, 2
0044794c  01c3                   add      ebx, eax
0044794e  31c9                   xor      ecx, ecx
00447950  31d2                   xor      edx, edx
00447952  8a8bdb000000           mov      cl, byte ptr [ebx + 0xdb]
00447958  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
0044795e  8d41ff                 lea      eax, [ecx - 1]
00447961  39c2                   cmp      edx, eax
00447963  740e                   je       0x447973
00447965  42                     inc      edx
00447966  89d0                   mov      eax, edx
00447968  c1fa1f                 sar      edx, 0x1f
0044796b  f7f9                   idiv     ecx
0044796d  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00447973  5a                     pop      edx
00447974  59                     pop      ecx
00447975  5b                     pop      ebx
00447976  c3                     ret
