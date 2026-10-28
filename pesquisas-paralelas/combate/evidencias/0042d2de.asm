; CalculGameEventoEComandos; intervalo [0x0042d2de, 0x0042d3c0)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042d2de  e845030400               call     0x46d628
0042d2e3  e8ceae0200               call     0x4581b6
0042d2e8  84c0                     test     al, al
0042d2ea  0f85fa010000             jne      0x42d4ea
0042d2f0  803d282f4e0000           cmp      byte ptr [0x4e2f28], 0
0042d2f7  7534                     jne      0x42d32d
0042d2f9  8a1d181d4e00             mov      bl, byte ptr [0x4e1d18]
0042d2ff  31d2                     xor      edx, edx
0042d301  88da                     mov      dl, bl
0042d303  8a92181c4e00             mov      dl, byte ptr [edx + 0x4e1c18]
0042d309  81e2ff000000             and      edx, 0xff
0042d30f  b902000000               mov      ecx, 2
0042d314  89d0                     mov      eax, edx
0042d316  c1fa1f                   sar      edx, 0x1f
0042d319  f7f9                     idiv     ecx
0042d31b  8d040a                   lea      eax, [edx + ecx]
0042d31e  fec3                     inc      bl
0042d320  31d2                     xor      edx, edx
0042d322  881d181d4e00             mov      byte ptr [0x4e1d18], bl
0042d328  e85fa70300               call     0x467a8c
0042d32d  30c9                     xor      cl, cl
0042d32f  eb59                     jmp      0x42d38a
0042d331  3a0d41805000             cmp      cl, byte ptr [0x508041]
0042d337  7510                     jne      0x42d349
0042d339  89d8                     mov      eax, ebx
0042d33b  e838bfffff               call     0x429278
0042d340  89d8                     mov      eax, ebx
0042d342  e858190300               call     0x45ec9f
0042d347  eb3f                     jmp      0x42d388
0042d349  89d8                     mov      eax, ebx
0042d34b  e82c170300               call     0x45ea7c
0042d350  eb36                     jmp      0x42d388
0042d352  31d2                     xor      edx, edx
0042d354  e8c1ed0300               call     0x46c11a
0042d359  88c2                     mov      dl, al
0042d35b  89d8                     mov      eax, ebx
0042d35d  e888280500               call     0x47fbea
0042d362  3a0d41805000             cmp      cl, byte ptr [0x508041]
0042d368  751e                     jne      0x42d388
0042d36a  89d8                     mov      eax, ebx
0042d36c  e807bfffff               call     0x429278
0042d371  eb15                     jmp      0x42d388
0042d373  31db                     xor      ebx, ebx
0042d375  88cb                     mov      bl, cl
0042d377  89d8                     mov      eax, ebx
0042d379  e899040400               call     0x46d817
0042d37e  3c01                     cmp      al, 1
0042d380  7206                     jb       0x42d388
0042d382  76ad                     jbe      0x42d331
0042d384  3c02                     cmp      al, 2
0042d386  74ca                     je       0x42d352
0042d388  fec1                     inc      cl
0042d38a  31c0                     xor      eax, eax
0042d38c  88c8                     mov      al, cl
0042d38e  83f804                   cmp      eax, 4
0042d391  7f0f                     jg       0x42d3a2
0042d393  8a1530074e00             mov      dl, byte ptr [0x4e0730]
0042d399  84d2                     test     dl, dl
0042d39b  74d6                     je       0x42d373
0042d39d  83f804                   cmp      eax, 4
0042d3a0  75d1                     jne      0x42d373
0042d3a2  a041805000               mov      al, byte ptr [0x508041]
0042d3a7  30db                     xor      bl, bl
0042d3a9  a280244e00               mov      byte ptr [0x4e2480], al
0042d3ae  eb07                     jmp      0x42d3b7
0042d3b0  e80b1a0300               call     0x45edc0
0042d3b5  fec3                     inc      bl
0042d3b7  31c0                     xor      eax, eax
0042d3b9  88d8                     mov      al, bl
0042d3bb  83f804                   cmp      eax, 4
0042d3be  7cf0                     jl       0x42d3b0
