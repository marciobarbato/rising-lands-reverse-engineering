; BagRetire: limite por próximo símbolo SBL, fim exclusivo 0x004473cf.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004472ea  51                       push     ecx
004472eb  56                       push     esi
004472ec  57                       push     edi
004472ed  55                       push     ebp
004472ee  83ec0c                   sub      esp, 0xc
004472f1  88542408                 mov      byte ptr [esp + 8], dl
004472f5  895c2404                 mov      dword ptr [esp + 4], ebx
004472f9  beffff0000               mov      esi, 0xffff
004472fe  30c9                     xor      cl, cl
00447300  31db                     xor      ebx, ebx
00447302  eb3c                     jmp      0x447340
00447304  668b7a06                 mov      di, word ptr [edx + 6]
00447308  81e7ffff0000             and      edi, 0xffff
0044730e  69ff14010000             imul     edi, edi, 0x114
00447314  8b2da0194e00             mov      ebp, dword ptr [0x4e19a0]
0044731a  01ef                     add      edi, ebp
0044731c  8a6f01                   mov      ch, byte ptr [edi + 1]
0044731f  31ff                     xor      edi, edi
00447321  0fb6ed                   movzx    ebp, ch
00447324  668b7c2404               mov      di, word ptr [esp + 4]
00447329  39fd                     cmp      ebp, edi
0044732b  7512                     jne      0x44733f
0044732d  668b7066                 mov      si, word ptr [eax + 0x66]
00447331  4e                       dec      esi
00447332  b101                     mov      cl, 1
00447334  66897066                 mov      word ptr [eax + 0x66], si
00447338  891c24                   mov      dword ptr [esp], ebx
0044733b  668b7206                 mov      si, word ptr [edx + 6]
0044733f  43                       inc      ebx
00447340  663b18                   cmp      bx, word ptr [eax]
00447343  7342                     jae      0x447387
00447345  31d2                     xor      edx, edx
00447347  6689f2                   mov      dx, si
0044734a  81faffff0000             cmp      edx, 0xffff
00447350  7535                     jne      0x447387
00447352  31d2                     xor      edx, edx
00447354  6689da                   mov      dx, bx
00447357  8a6c0242                 mov      ch, byte ptr [edx + eax + 0x42]
0044735b  3a6c2408                 cmp      ch, byte ptr [esp + 8]
0044735f  7402                     je       0x447363
00447361  ebdc                     jmp      0x44733f
00447363  01d2                     add      edx, edx
00447365  01c2                     add      edx, eax
00447367  80fd01                   cmp      ch, 1
0044736a  7498                     je       0x447304
0044736c  668b7a06                 mov      di, word ptr [edx + 6]
00447370  663b7c2404               cmp      di, word ptr [esp + 4]
00447375  75c8                     jne      0x44733f
00447377  668b4866                 mov      cx, word ptr [eax + 0x66]
0044737b  49                       dec      ecx
0044737c  891c24                   mov      dword ptr [esp], ebx
0044737f  66894866                 mov      word ptr [eax + 0x66], cx
00447383  b101                     mov      cl, 1
00447385  ebb4                     jmp      0x44733b
00447387  84c9                     test     cl, cl
00447389  743a                     je       0x4473c5
0044738b  8b3c24                   mov      edi, dword ptr [esp]
0044738e  eb0f                     jmp      0x44739f
00447390  8a4a43                   mov      cl, byte ptr [edx + 0x43]
00447393  884a42                   mov      byte ptr [edx + 0x42], cl
00447396  668b5308                 mov      dx, word ptr [ebx + 8]
0044739a  47                       inc      edi
0044739b  66895306                 mov      word ptr [ebx + 6], dx
0044739f  31d2                     xor      edx, edx
004473a1  31c9                     xor      ecx, ecx
004473a3  668b10                   mov      dx, word ptr [eax]
004473a6  6689f9                   mov      cx, di
004473a9  8d6aff                   lea      ebp, [edx - 1]
004473ac  8d1408                   lea      edx, [eax + ecx]
004473af  8d1c09                   lea      ebx, [ecx + ecx]
004473b2  01c3                     add      ebx, eax
004473b4  39e9                     cmp      ecx, ebp
004473b6  7cd8                     jl       0x447390
004473b8  c6424200                 mov      byte ptr [edx + 0x42], 0
004473bc  66c743060000             mov      word ptr [ebx + 6], 0
004473c2  66ff08                   dec      word ptr [eax]
004473c5  89f0                     mov      eax, esi
004473c7  83c40c                   add      esp, 0xc
004473ca  5d                       pop      ebp
004473cb  5f                       pop      edi
004473cc  5e                       pop      esi
004473cd  59                       pop      ecx
004473ce  c3                       ret
