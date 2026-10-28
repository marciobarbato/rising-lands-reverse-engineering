; ProjectileCalculLineaire; intervalo [0x0046e4ca, 0x0046e52c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e4ca  53                       push     ebx
0046e4cb  51                       push     ecx
0046e4cc  52                       push     edx
0046e4cd  56                       push     esi
0046e4ce  6683783400               cmp      word ptr [eax + 0x34], 0
0046e4d3  7452                     je       0x46e527
0046e4d5  8b502c                   mov      edx, dword ptr [eax + 0x2c]
0046e4d8  c1fa10                   sar      edx, 0x10
0046e4db  85d2                     test     edx, edx
0046e4dd  7c14                     jl       0x46e4f3
0046e4df  8b5028                   mov      edx, dword ptr [eax + 0x28]
0046e4e2  8b4808                   mov      ecx, dword ptr [eax + 8]
0046e4e5  c1fa10                   sar      edx, 0x10
0046e4e8  01d1                     add      ecx, edx
0046e4ea  894808                   mov      dword ptr [eax + 8], ecx
0046e4ed  668b5030                 mov      dx, word ptr [eax + 0x30]
0046e4f1  eb12                     jmp      0x46e505
0046e4f3  8b502a                   mov      edx, dword ptr [eax + 0x2a]
0046e4f6  8b5808                   mov      ebx, dword ptr [eax + 8]
0046e4f9  c1fa10                   sar      edx, 0x10
0046e4fc  01d3                     add      ebx, edx
0046e4fe  895808                   mov      dword ptr [eax + 8], ebx
0046e501  668b5032                 mov      dx, word ptr [eax + 0x32]
0046e505  6601502e                 add      word ptr [eax + 0x2e], dx
0046e509  668b5008                 mov      dx, word ptr [eax + 8]
0046e50d  80e61f                   and      dh, 0x1f
0046e510  668b7034                 mov      si, word ptr [eax + 0x34]
0046e514  6689500c                 mov      word ptr [eax + 0xc], dx
0046e518  4e                       dec      esi
0046e519  8b5008                   mov      edx, dword ptr [eax + 8]
0046e51c  66897034                 mov      word ptr [eax + 0x34], si
0046e520  c1ea0d                   shr      edx, 0xd
0046e523  6689500e                 mov      word ptr [eax + 0xe], dx
0046e527  5e                       pop      esi
0046e528  5a                       pop      edx
0046e529  59                       pop      ecx
0046e52a  5b                       pop      ebx
0046e52b  c3                       ret
