; AnimArretEngin [0x4478ee, 0x44792f)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004478ee  53                     push     ebx
004478ef  51                     push     ecx
004478f0  52                     push     edx
004478f1  31d2                   xor      edx, edx
004478f3  6689c2                 mov      dx, ax
004478f6  89d0                   mov      eax, edx
004478f8  c1e004                 shl      eax, 4
004478fb  01d0                   add      eax, edx
004478fd  c1e002                 shl      eax, 2
00447900  01d0                   add      eax, edx
00447902  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
00447908  c1e002                 shl      eax, 2
0044790b  01c3                   add      ebx, eax
0044790d  31d2                   xor      edx, edx
0044790f  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447915  31c9                   xor      ecx, ecx
00447917  42                     inc      edx
00447918  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
0044791e  89d0                   mov      eax, edx
00447920  c1fa1f                 sar      edx, 0x1f
00447923  f7f9                   idiv     ecx
00447925  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
0044792b  5a                     pop      edx
0044792c  59                     pop      ecx
0044792d  5b                     pop      ebx
0044792e  c3                     ret
