; SortieTroupe: Empty-Bag cleanup: GetCase, EteintTerrain, deselect, owner 200, ModifyMap, reset, messages; exclusive end 0x004211f2.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004210f7  c744240814000000         mov      dword ptr [esp + 8], 0x14
004210ff  31c0                     xor      eax, eax
00421101  31d2                     xor      edx, edx
00421103  668b0424                 mov      ax, word ptr [esp]
00421107  668b542408               mov      dx, word ptr [esp + 8]
0042110c  e8d19dffff               call     0x41aee2
00421111  25ffff0000               and      eax, 0xffff
00421116  e8675d0500               call     0x476e82
0042111b  31c0                     xor      eax, eax
0042111d  8a4704                   mov      al, byte ptr [edi + 4]
00421120  8b1c24                   mov      ebx, dword ptr [esp]
00421123  663b1c45e05b4900         cmp      bx, word ptr [eax*2 + 0x495be0]
0042112b  7512                     jne      0x42113f
0042112d  8a4704                   mov      al, byte ptr [edi + 4]
00421130  25ff000000               and      eax, 0xff
00421135  66c70445e05b4900ffff     mov      word ptr [eax*2 + 0x495be0], 0xffff
0042113f  31c0                     xor      eax, eax
00421141  ba01000000               mov      edx, 1
00421146  668b0424                 mov      ax, word ptr [esp]
0042114a  c64704c8                 mov      byte ptr [edi + 4], 0xc8
0042114e  e8448dffff               call     0x419e97
00421153  31c0                     xor      eax, eax
00421155  668b0424                 mov      ax, word ptr [esp]
00421159  89c2                     mov      edx, eax
0042115b  c1e204                   shl      edx, 4
0042115e  01c2                     add      edx, eax
00421160  c1e202                   shl      edx, 2
00421163  01c2                     add      edx, eax
00421165  c1e202                   shl      edx, 2
00421168  81c2c8a04900             add      edx, 0x49a0c8
0042116e  66c74278ffff             mov      word ptr [edx + 0x78], 0xffff
00421174  c6427bff                 mov      byte ptr [edx + 0x7b], 0xff
00421178  66c7427c0000             mov      word ptr [edx + 0x7c], 0
0042117e  31c0                     xor      eax, eax
00421180  66c7427e0000             mov      word ptr [edx + 0x7e], 0
00421186  8a4208                   mov      al, byte ptr [edx + 8]
00421189  66c78286000000ffff       mov      word ptr [edx + 0x86], 0xffff
00421192  83f814                   cmp      eax, 0x14
00421195  7412                     je       0x4211a9
00421197  66c782800000000000       mov      word ptr [edx + 0x80], 0
004211a0  66c782820000000000       mov      word ptr [edx + 0x82], 0
004211a9  c6427400                 mov      byte ptr [edx + 0x74], 0
004211ad  31c0                     xor      eax, eax
004211af  8a4205                   mov      al, byte ptr [edx + 5]
004211b2  c7828c00000000000000     mov      dword ptr [edx + 0x8c], 0
004211bc  83f803                   cmp      eax, 3
004211bf  7404                     je       0x4211c5
004211c1  c6420505                 mov      byte ptr [edx + 5], 5
004211c5  ba46000000               mov      edx, 0x46
004211ca  31c0                     xor      eax, eax
004211cc  31db                     xor      ebx, ebx
004211ce  668b442404               mov      ax, word ptr [esp + 4]
004211d3  e8f0170600               call     0x4829c8
004211d8  ba03000000               mov      edx, 3
004211dd  31c0                     xor      eax, eax
004211df  31db                     xor      ebx, ebx
004211e1  668b0424                 mov      ax, word ptr [esp]
004211e5  e81e360600               call     0x484808
004211ea  83c410                   add      esp, 0x10
004211ed  e9a8270000               jmp      0x42399a
