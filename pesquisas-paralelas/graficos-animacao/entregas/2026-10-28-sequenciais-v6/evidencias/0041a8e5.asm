; BatimentGetEtat [0x41a8e5, 0x41a940)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041a8e5  53                     push     ebx
0041a8e6  52                     push     edx
0041a8e7  31d2                   xor      edx, edx
0041a8e9  6689c2                 mov      dx, ax
0041a8ec  89d0                   mov      eax, edx
0041a8ee  c1e004                 shl      eax, 4
0041a8f1  01d0                   add      eax, edx
0041a8f3  c1e002                 shl      eax, 2
0041a8f6  01d0                   add      eax, edx
0041a8f8  bac8a04900             mov      edx, 0x49a0c8
0041a8fd  c1e002                 shl      eax, 2
0041a900  01c2                   add      edx, eax
0041a902  31db                   xor      ebx, ebx
0041a904  8a5a08                 mov      bl, byte ptr [edx + 8]
0041a907  89d8                   mov      eax, ebx
0041a909  c1e002                 shl      eax, 2
0041a90c  29d8                   sub      eax, ebx
0041a90e  c1e002                 shl      eax, 2
0041a911  01d8                   add      eax, ebx
0041a913  31db                   xor      ebx, ebx
0041a915  668b520a               mov      dx, word ptr [edx + 0xa]
0041a919  668b1c85905d4900       mov      bx, word ptr [eax*4 + 0x495d90]
0041a921  81e2ffff0000           and      edx, 0xffff
0041a927  89d0                   mov      eax, edx
0041a929  c1e002                 shl      eax, 2
0041a92c  29d0                   sub      eax, edx
0041a92e  c1e003                 shl      eax, 3
0041a931  01c2                   add      edx, eax
0041a933  c1e203                 shl      edx, 3
0041a936  89d0                   mov      eax, edx
0041a938  c1fa1f                 sar      edx, 0x1f
0041a93b  f7fb                   idiv     ebx
0041a93d  5a                     pop      edx
0041a93e  5b                     pop      ebx
0041a93f  c3                     ret
