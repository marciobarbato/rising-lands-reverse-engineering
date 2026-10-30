; InventionSetEffet; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x47125c
00470f98  56                       push     esi
00470f99  57                       push     edi
00470f9a  83ec04                   sub      esp, 4
00470f9d  880424                   mov      byte ptr [esp], al
00470fa0  89d6                     mov      esi, edx
00470fa2  89df                     mov      edi, ebx
00470fa4  31c0                     xor      eax, eax
00470fa6  6689d8                   mov      ax, bx
00470fa9  89c3                     mov      ebx, eax
00470fab  c1e302                   shl      ebx, 2
00470fae  29c3                     sub      ebx, eax
00470fb0  c1e303                   shl      ebx, 3
00470fb3  89d8                     mov      eax, ebx
00470fb5  89da                     mov      edx, ebx
00470fb7  31d8                     xor      eax, ebx
00470fb9  c1e204                   shl      edx, 4
00470fbc  6689f0                   mov      ax, si
00470fbf  29da                     sub      edx, ebx
00470fc1  89c3                     mov      ebx, eax
00470fc3  c1e302                   shl      ebx, 2
00470fc6  29c3                     sub      ebx, eax
00470fc8  c1e302                   shl      ebx, 2
00470fcb  8d041a                   lea      eax, [edx + ebx]
00470fce  31d2                     xor      edx, edx
00470fd0  8a9082815000             mov      dl, byte ptr [eax + 0x508182]
00470fd6  81faff000000             cmp      edx, 0xff
00470fdc  7413                     je       0x470ff1
00470fde  8a8080815000             mov      al, byte ptr [eax + 0x508180]
00470fe4  25ff000000               and      eax, 0xff
00470fe9  83f864                   cmp      eax, 0x64
00470fec  0f95c0                   setne    al
00470fef  eb02                     jmp      0x470ff3
00470ff1  30c0                     xor      al, al
00470ff3  84c0                     test     al, al
00470ff5  0f8530000000             jne      0x47102b
00470ffb  31c0                     xor      eax, eax
00470ffd  88c8                     mov      al, cl
00470fff  83f801                   cmp      eax, 1
00471002  0f8523000000             jne      0x47102b
00471008  8a0424                   mov      al, byte ptr [esp]
0047100b  3a0541805000             cmp      al, byte ptr [0x508041]
00471011  0f8514000000             jne      0x47102b
00471017  6bc764                   imul     eax, edi, 0x64
0047101a  31d2                     xor      edx, edx
0047101c  01f0                     add      eax, esi
0047101e  6689c2                   mov      dx, ax
00471021  b80a000000               mov      eax, 0xa
00471026  e82089ffff               call     0x46994b
0047102b  31c0                     xor      eax, eax
0047102d  6689f8                   mov      ax, di
00471030  89c3                     mov      ebx, eax
00471032  c1e302                   shl      ebx, 2
00471035  29c3                     sub      ebx, eax
00471037  c1e303                   shl      ebx, 3
0047103a  89d8                     mov      eax, ebx
0047103c  89da                     mov      edx, ebx
0047103e  31d8                     xor      eax, ebx
00471040  c1e204                   shl      edx, 4
00471043  6689f0                   mov      ax, si
00471046  29da                     sub      edx, ebx
00471048  89c3                     mov      ebx, eax
0047104a  c1e302                   shl      ebx, 2
0047104d  29c3                     sub      ebx, eax
0047104f  c1e302                   shl      ebx, 2
00471052  01d3                     add      ebx, edx
00471054  8a8382815000             mov      al, byte ptr [ebx + 0x508182]
0047105a  3c01                     cmp      al, 1
0047105c  0f82f0010000             jb       0x471252
00471062  7670                     jbe      0x4710d4
00471064  3c02                     cmp      al, 2
00471066  742c                     je       0x471094
00471068  e9e9010000               jmp      0x471256
0047106d  31c9                     xor      ecx, ecx
0047106f  8a8b85815000             mov      cl, byte ptr [ebx + 0x508185]
00471075  8a9b84815000             mov      bl, byte ptr [ebx + 0x508184]
0047107b  31d2                     xor      edx, edx
0047107d  88c2                     mov      dl, al
0047107f  31c0                     xor      eax, eax
00471081  81e3ff000000             and      ebx, 0xff
00471087  8a0424                   mov      al, byte ptr [esp]
0047108a  e88b76fbff               call     0x42871a
0047108f  e9c2010000               jmp      0x471256
00471094  8a8383815000             mov      al, byte ptr [ebx + 0x508183]
0047109a  3c01                     cmp      al, 1
0047109c  0f82b4010000             jb       0x471256
004710a2  76c9                     jbe      0x47106d
004710a4  3c06                     cmp      al, 6
004710a6  74c5                     je       0x47106d
004710a8  e9a9010000               jmp      0x471256
004710ad  31c9                     xor      ecx, ecx
004710af  8a8b85815000             mov      cl, byte ptr [ebx + 0x508185]
004710b5  8a9b84815000             mov      bl, byte ptr [ebx + 0x508184]
004710bb  31d2                     xor      edx, edx
004710bd  88c2                     mov      dl, al
004710bf  31c0                     xor      eax, eax
004710c1  81e3ff000000             and      ebx, 0xff
004710c7  8a0424                   mov      al, byte ptr [esp]
004710ca  e8a977fbff               call     0x428878
004710cf  e982010000               jmp      0x471256
004710d4  8a8383815000             mov      al, byte ptr [ebx + 0x508183]
004710da  3c0c                     cmp      al, 0xc
004710dc  0f8774010000             ja       0x471256
004710e2  31d2                     xor      edx, edx
004710e4  88c2                     mov      dl, al
004710e6  2eff2495640f4700         jmp      dword ptr cs:[edx*4 + 0x470f64]
004710ee  31c0                     xor      eax, eax
004710f0  ba10000000               mov      edx, 0x10
004710f5  88c8                     mov      al, cl
004710f7  e85113fdff               call     0x44244d
004710fc  31c0                     xor      eax, eax
004710fe  ba11000000               mov      edx, 0x11
00471103  88c8                     mov      al, cl
00471105  e84313fdff               call     0x44244d
0047110a  e8d1bcfaff               call     0x41cde0
0047110f  e942010000               jmp      0x471256
00471114  31c0                     xor      eax, eax
00471116  ba03000000               mov      edx, 3
0047111b  ebe6                     jmp      0x471103
0047111d  31c0                     xor      eax, eax
0047111f  ba0a000000               mov      edx, 0xa
00471124  ebdd                     jmp      0x471103
00471126  31c9                     xor      ecx, ecx
00471128  31d2                     xor      edx, edx
0047112a  8a0c24                   mov      cl, byte ptr [esp]
0047112d  8a9384815000             mov      dl, byte ptr [ebx + 0x508184]
00471133  89c8                     mov      eax, ecx
00471135  e89979faff               call     0x418ad3
0047113a  89c8                     mov      eax, ecx
0047113c  e8a000fdff               call     0x4411e1
00471141  8a8384815000             mov      al, byte ptr [ebx + 0x508184]
00471147  88c4                     mov      ah, al
00471149  3c10                     cmp      al, 0x10
0047114b  7215                     jb       0x471162
0047114d  76ce                     jbe      0x47111d
0047114f  3c12                     cmp      al, 0x12
00471151  0f82ff000000             jb       0x471256
00471157  7695                     jbe      0x4710ee
00471159  3c14                     cmp      al, 0x14
0047115b  74ad                     je       0x47110a
0047115d  e9f4000000               jmp      0x471256
00471162  3c0d                     cmp      al, 0xd
00471164  74ae                     je       0x471114
00471166  e9eb000000               jmp      0x471256
0047116b  31db                     xor      ebx, ebx
0047116d  8a1c24                   mov      bl, byte ptr [esp]
00471170  ba05000000               mov      edx, 5
00471175  89d8                     mov      eax, ebx
00471177  e85779faff               call     0x418ad3
0047117c  89d8                     mov      eax, ebx
0047117e  e85e00fdff               call     0x4411e1
00471183  e9ce000000               jmp      0x471256
00471188  31c0                     xor      eax, eax
0047118a  6689f8                   mov      ax, di
0047118d  89c3                     mov      ebx, eax
0047118f  c1e302                   shl      ebx, 2
00471192  29c3                     sub      ebx, eax
00471194  c1e303                   shl      ebx, 3
00471197  89d8                     mov      eax, ebx
00471199  89da                     mov      edx, ebx
0047119b  31d8                     xor      eax, ebx
0047119d  c1e204                   shl      edx, 4
004711a0  6689f0                   mov      ax, si
004711a3  29da                     sub      edx, ebx
004711a5  89c3                     mov      ebx, eax
004711a7  c1e302                   shl      ebx, 2
004711aa  29c3                     sub      ebx, eax
004711ac  8a949a84815000           mov      dl, byte ptr [edx + ebx*4 + 0x508184]
004711b3  31c0                     xor      eax, eax
004711b5  81e2ff000000             and      edx, 0xff
004711bb  8a0424                   mov      al, byte ptr [esp]
004711be  e88a12fdff               call     0x44244d
004711c3  e818bcfaff               call     0x41cde0
004711c8  31c0                     xor      eax, eax
004711ca  6689f8                   mov      ax, di
004711cd  89c3                     mov      ebx, eax
004711cf  c1e302                   shl      ebx, 2
004711d2  29c3                     sub      ebx, eax
004711d4  c1e303                   shl      ebx, 3
004711d7  89d8                     mov      eax, ebx
004711d9  89da                     mov      edx, ebx
004711db  31d8                     xor      eax, ebx
004711dd  c1e204                   shl      edx, 4
004711e0  6689f0                   mov      ax, si
004711e3  29da                     sub      edx, ebx
004711e5  89c3                     mov      ebx, eax
004711e7  c1e302                   shl      ebx, 2
004711ea  29c3                     sub      ebx, eax
004711ec  8aa49a84815000           mov      ah, byte ptr [edx + ebx*4 + 0x508184]
004711f3  88e0                     mov      al, ah
004711f5  80fc0d                   cmp      ah, 0xd
004711f8  7211                     jb       0x47120b
004711fa  0f866bffffff             jbe      0x47116b
00471200  80fc0f                   cmp      ah, 0xf
00471203  0f8462ffffff             je       0x47116b
00471209  eb4b                     jmp      0x471256
0047120b  80fc0b                   cmp      ah, 0xb
0047120e  ebf3                     jmp      0x471203
00471210  31d2                     xor      edx, edx
00471212  8a9384815000             mov      dl, byte ptr [ebx + 0x508184]
00471218  31db                     xor      ebx, ebx
0047121a  8a1c24                   mov      bl, byte ptr [esp]
0047121d  89d8                     mov      eax, ebx
0047121f  e889370000               call     0x4749ad
00471224  ba06000000               mov      edx, 6
00471229  89d8                     mov      eax, ebx
0047122b  e83cb5faff               call     0x41c76c
00471230  eb24                     jmp      0x471256
00471232  8a8383815000             mov      al, byte ptr [ebx + 0x508183]
00471238  3c03                     cmp      al, 3
0047123a  720c                     jb       0x471248
0047123c  0f86e4feffff             jbe      0x471126
00471242  3c04                     cmp      al, 4
00471244  74ca                     je       0x471210
00471246  eb0e                     jmp      0x471256
00471248  3c01                     cmp      al, 1
0047124a  0f8438ffffff             je       0x471188
00471250  eb04                     jmp      0x471256
00471252  84c0                     test     al, al
00471254  74dc                     je       0x471232
00471256  83c404                   add      esp, 4
00471259  5f                       pop      edi
0047125a  5e                       pop      esi
0047125b  c3                       ret      
