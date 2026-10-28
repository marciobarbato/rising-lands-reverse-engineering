; CalculTroupe: limite por próximo símbolo SBL, fim exclusivo 0x00426418.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004259e6  53                       push     ebx
004259e7  51                       push     ecx
004259e8  52                       push     edx
004259e9  56                       push     esi
004259ea  57                       push     edi
004259eb  55                       push     ebp
004259ec  81ec9c000000             sub      esp, 0x9c
004259f2  89c1                     mov      ecx, eax
004259f4  31db                     xor      ebx, ebx
004259f6  6689c3                   mov      bx, ax
004259f9  89d8                     mov      eax, ebx
004259fb  c1e004                   shl      eax, 4
004259fe  01d8                     add      eax, ebx
00425a00  c1e002                   shl      eax, 2
00425a03  01d8                     add      eax, ebx
00425a05  bac8a04900               mov      edx, 0x49a0c8
00425a0a  c1e002                   shl      eax, 2
00425a0d  01c2                     add      edx, eax
00425a0f  8a4208                   mov      al, byte ptr [edx + 8]
00425a12  3c0d                     cmp      al, 0xd
00425a14  0f82cb090000             jb       0x4263e5
00425a1a  8dba8c000000             lea      edi, [edx + 0x8c]
00425a20  0f8638010000             jbe      0x425b5e
00425a26  3c10                     cmp      al, 0x10
00425a28  0f82ea080000             jb       0x426318
00425a2e  761b                     jbe      0x425a4b
00425a30  3c12                     cmp      al, 0x12
00425a32  0f82d5090000             jb       0x42640d
00425a38  0f866c060000             jbe      0x4260aa
00425a3e  3c14                     cmp      al, 0x14
00425a40  0f84da080000             je       0x426320
00425a46  e9c2090000               jmp      0x42640d
00425a4b  31db                     xor      ebx, ebx
00425a4d  6689cb                   mov      bx, cx
00425a50  89d8                     mov      eax, ebx
00425a52  c1e004                   shl      eax, 4
00425a55  01d8                     add      eax, ebx
00425a57  c1e002                   shl      eax, 2
00425a5a  01d8                     add      eax, ebx
00425a5c  bac8a04900               mov      edx, 0x49a0c8
00425a61  c1e002                   shl      eax, 2
00425a64  01c2                     add      edx, eax
00425a66  83ba8c00000000           cmp      dword ptr [edx + 0x8c], 0
00425a6d  0f84e7000000             je       0x425b5a
00425a73  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425a77  0f84dd000000             je       0x425b5a
00425a7d  31c0                     xor      eax, eax
00425a7f  8a427b                   mov      al, byte ptr [edx + 0x7b]
00425a82  31f6                     xor      esi, esi
00425a84  e82eb60100               call     0x4410b7
00425a89  6689c6                   mov      si, ax
00425a8c  89f0                     mov      eax, esi
00425a8e  c1e002                   shl      eax, 2
00425a91  29f0                     sub      eax, esi
00425a93  c1e003                   shl      eax, 3
00425a96  01f0                     add      eax, esi
00425a98  c1e002                   shl      eax, 2
00425a9b  3b828c000000             cmp      eax, dword ptr [edx + 0x8c]
00425aa1  0f8695000000             jbe      0x425b3c
00425aa7  89d8                     mov      eax, ebx
00425aa9  81c28c000000             add      edx, 0x8c
00425aaf  e8104affff               call     0x41a4c4
00425ab4  25ffff0000               and      eax, 0xffff
00425ab9  89842490000000           mov      dword ptr [esp + 0x90], eax
00425ac0  db842490000000           fild     dword ptr [esp + 0x90]
00425ac7  89d8                     mov      eax, ebx
00425ac9  dd5c2428                 fstp     qword ptr [esp + 0x28]
00425acd  e81b99ffff               call     0x41f3ed
00425ad2  30e4                     xor      ah, ah
00425ad4  89842498000000           mov      dword ptr [esp + 0x98], eax
00425adb  df842498000000           fild     word ptr [esp + 0x98]
00425ae2  89d8                     mov      eax, ebx
00425ae4  dd5c2410                 fstp     qword ptr [esp + 0x10]
00425ae8  e8074affff               call     0x41a4f4
00425aed  25ff000000               and      eax, 0xff
00425af2  83f80e                   cmp      eax, 0xe
00425af5  7410                     je       0x425b07
00425af7  dd442428                 fld      qword ptr [esp + 0x28]
00425afb  dc742410                 fdiv     qword ptr [esp + 0x10]
00425aff  dc0d3a444900             fmul     qword ptr [0x49443a]
00425b05  eb0e                     jmp      0x425b15
00425b07  dd442428                 fld      qword ptr [esp + 0x28]
00425b0b  dc742410                 fdiv     qword ptr [esp + 0x10]
00425b0f  dc0d32444900             fmul     qword ptr [0x494432]
00425b15  dd1c24                   fstp     qword ptr [esp]
00425b18  dd0424                   fld      qword ptr [esp]
00425b1b  e81e690600               call     0x48c43e
00425b20  db9c2490000000           fistp    dword ptr [esp + 0x90]
00425b27  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00425b2e  25ffff0000               and      eax, 0xffff
00425b33  8b3a                     mov      edi, dword ptr [edx]
00425b35  83c064                   add      eax, 0x64
00425b38  01c7                     add      edi, eax
00425b3a  893a                     mov      dword ptr [edx], edi
00425b3c  b001                     mov      al, 1
00425b3e  84c0                     test     al, al
00425b40  0f84c7080000             je       0x42640d
00425b46  31c0                     xor      eax, eax
00425b48  ba04000000               mov      edx, 4
00425b4d  6689c8                   mov      ax, cx
00425b50  e8f7b2ffff               call     0x420e4c
00425b55  e9b3080000               jmp      0x42640d
00425b5a  30c0                     xor      al, al
00425b5c  ebe0                     jmp      0x425b3e
00425b5e  83ba8c00000000           cmp      dword ptr [edx + 0x8c], 0
00425b65  0f84cd000000             je       0x425c38
00425b6b  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425b6f  0f84c3000000             je       0x425c38
00425b75  31c0                     xor      eax, eax
00425b77  8a427b                   mov      al, byte ptr [edx + 0x7b]
00425b7a  31f6                     xor      esi, esi
00425b7c  e836b50100               call     0x4410b7
00425b81  6689c6                   mov      si, ax
00425b84  89f0                     mov      eax, esi
00425b86  c1e002                   shl      eax, 2
00425b89  29f0                     sub      eax, esi
00425b8b  c1e003                   shl      eax, 3
00425b8e  01f0                     add      eax, esi
00425b90  8baa8c000000             mov      ebp, dword ptr [edx + 0x8c]
00425b96  c1e002                   shl      eax, 2
00425b99  39e8                     cmp      eax, ebp
00425b9b  0f8693000000             jbe      0x425c34
00425ba1  89d8                     mov      eax, ebx
00425ba3  89fa                     mov      edx, edi
00425ba5  e81a49ffff               call     0x41a4c4
00425baa  25ffff0000               and      eax, 0xffff
00425baf  89842490000000           mov      dword ptr [esp + 0x90], eax
00425bb6  db842490000000           fild     dword ptr [esp + 0x90]
00425bbd  89d8                     mov      eax, ebx
00425bbf  dd5c2478                 fstp     qword ptr [esp + 0x78]
00425bc3  e82598ffff               call     0x41f3ed
00425bc8  30e4                     xor      ah, ah
00425bca  89842498000000           mov      dword ptr [esp + 0x98], eax
00425bd1  df842498000000           fild     word ptr [esp + 0x98]
00425bd8  89d8                     mov      eax, ebx
00425bda  dd5c2438                 fstp     qword ptr [esp + 0x38]
00425bde  e81149ffff               call     0x41a4f4
00425be3  25ff000000               and      eax, 0xff
00425be8  83f80e                   cmp      eax, 0xe
00425beb  7410                     je       0x425bfd
00425bed  dd442478                 fld      qword ptr [esp + 0x78]
00425bf1  dc742438                 fdiv     qword ptr [esp + 0x38]
00425bf5  dc0d3a444900             fmul     qword ptr [0x49443a]
00425bfb  eb0e                     jmp      0x425c0b
00425bfd  dd442478                 fld      qword ptr [esp + 0x78]
00425c01  dc742438                 fdiv     qword ptr [esp + 0x38]
00425c05  dc0d32444900             fmul     qword ptr [0x494432]
00425c0b  dd5c2420                 fstp     qword ptr [esp + 0x20]
00425c0f  dd442420                 fld      qword ptr [esp + 0x20]
00425c13  e826680600               call     0x48c43e
00425c18  db9c2490000000           fistp    dword ptr [esp + 0x90]
00425c1f  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00425c26  25ffff0000               and      eax, 0xffff
00425c2b  8b1a                     mov      ebx, dword ptr [edx]
00425c2d  83c064                   add      eax, 0x64
00425c30  01c3                     add      ebx, eax
00425c32  891a                     mov      dword ptr [edx], ebx
00425c34  b001                     mov      al, 1
00425c36  eb02                     jmp      0x425c3a
00425c38  30c0                     xor      al, al
00425c3a  84c0                     test     al, al
00425c3c  0f84cb070000             je       0x42640d
00425c42  31c0                     xor      eax, eax
00425c44  ba0e000000               mov      edx, 0xe
00425c49  e9fffeffff               jmp      0x425b4d
00425c4e  dd442460                 fld      qword ptr [esp + 0x60]
00425c52  dc742448                 fdiv     qword ptr [esp + 0x48]
00425c56  dc0d32444900             fmul     qword ptr [0x494432]
00425c5c  dd9c2488000000           fstp     qword ptr [esp + 0x88]
00425c63  dd842488000000           fld      qword ptr [esp + 0x88]
00425c6a  e8cf670600               call     0x48c43e
00425c6f  db9c2490000000           fistp    dword ptr [esp + 0x90]
00425c76  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00425c7d  25ffff0000               and      eax, 0xffff
00425c82  8b1a                     mov      ebx, dword ptr [edx]
00425c84  83c064                   add      eax, 0x64
00425c87  01c3                     add      ebx, eax
00425c89  891a                     mov      dword ptr [edx], ebx
00425c8b  e9acfeffff               jmp      0x425b3c
00425c90  31db                     xor      ebx, ebx
00425c92  6689cb                   mov      bx, cx
00425c95  89d8                     mov      eax, ebx
00425c97  c1e004                   shl      eax, 4
00425c9a  01d8                     add      eax, ebx
00425c9c  c1e002                   shl      eax, 2
00425c9f  01d8                     add      eax, ebx
00425ca1  bbc8a04900               mov      ebx, 0x49a0c8
00425ca6  c1e002                   shl      eax, 2
00425ca9  01c3                     add      ebx, eax
00425cab  8bab8c000000             mov      ebp, dword ptr [ebx + 0x8c]
00425cb1  89cf                     mov      edi, ecx
00425cb3  85ed                     test     ebp, ebp
00425cb5  0f84f1000000             je       0x425dac
00425cbb  807b7400                 cmp      byte ptr [ebx + 0x74], 0
00425cbf  0f84e7000000             je       0x425dac
00425cc5  31c0                     xor      eax, eax
00425cc7  8a437b                   mov      al, byte ptr [ebx + 0x7b]
00425cca  31f6                     xor      esi, esi
00425ccc  e8e6b30100               call     0x4410b7
00425cd1  6689c6                   mov      si, ax
00425cd4  89f0                     mov      eax, esi
00425cd6  c1e002                   shl      eax, 2
00425cd9  29f0                     sub      eax, esi
00425cdb  c1e003                   shl      eax, 3
00425cde  01f0                     add      eax, esi
00425ce0  c1e002                   shl      eax, 2
00425ce3  3b838c000000             cmp      eax, dword ptr [ebx + 0x8c]
00425ce9  0f877c000000             ja       0x425d6b
00425cef  e9b4000000               jmp      0x425da8
00425cf4  31c0                     xor      eax, eax
00425cf6  6689c8                   mov      ax, cx
00425cf9  e8c647ffff               call     0x41a4c4
00425cfe  25ffff0000               and      eax, 0xffff
00425d03  89842490000000           mov      dword ptr [esp + 0x90], eax
00425d0a  31c0                     xor      eax, eax
00425d0c  db842490000000           fild     dword ptr [esp + 0x90]
00425d13  6689c8                   mov      ax, cx
00425d16  dd5c2430                 fstp     qword ptr [esp + 0x30]
00425d1a  e8ce96ffff               call     0x41f3ed
00425d1f  30e4                     xor      ah, ah
00425d21  89842498000000           mov      dword ptr [esp + 0x98], eax
00425d28  31c0                     xor      eax, eax
00425d2a  df842498000000           fild     word ptr [esp + 0x98]
00425d31  6689c8                   mov      ax, cx
00425d34  dd5c2458                 fstp     qword ptr [esp + 0x58]
00425d38  e8b747ffff               call     0x41a4f4
00425d3d  25ff000000               and      eax, 0xff
00425d42  83f80e                   cmp      eax, 0xe
00425d45  7414                     je       0x425d5b
00425d47  dd442430                 fld      qword ptr [esp + 0x30]
00425d4b  dc742458                 fdiv     qword ptr [esp + 0x58]
00425d4f  dc0d3a444900             fmul     qword ptr [0x49443a]
00425d55  dd5c2450                 fstp     qword ptr [esp + 0x50]
00425d59  eb28                     jmp      0x425d83
00425d5b  dd442430                 fld      qword ptr [esp + 0x30]
00425d5f  dc742458                 fdiv     qword ptr [esp + 0x58]
00425d63  dc0d32444900             fmul     qword ptr [0x494432]
00425d69  ebea                     jmp      0x425d55
00425d6b  b003                     mov      al, 3
00425d6d  81c38c000000             add      ebx, 0x8c
00425d73  89ce                     mov      esi, ecx
00425d75  3c01                     cmp      al, 1
00425d77  720a                     jb       0x425d83
00425d79  7608                     jbe      0x425d83
00425d7b  38c0                     cmp      al, al
00425d7d  0f8471ffffff             je       0x425cf4
00425d83  dd442450                 fld      qword ptr [esp + 0x50]
00425d87  e8b2660600               call     0x48c43e
00425d8c  db9c2490000000           fistp    dword ptr [esp + 0x90]
00425d93  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00425d9a  25ffff0000               and      eax, 0xffff
00425d9f  8b3b                     mov      edi, dword ptr [ebx]
00425da1  83c064                   add      eax, 0x64
00425da4  01c7                     add      edi, eax
00425da6  893b                     mov      dword ptr [ebx], edi
00425da8  b001                     mov      al, 1
00425daa  eb02                     jmp      0x425dae
00425dac  30c0                     xor      al, al
00425dae  84c0                     test     al, al
00425db0  7452                     je       0x425e04
00425db2  31ff                     xor      edi, edi
00425db4  6689cf                   mov      di, cx
00425db7  89f8                     mov      eax, edi
00425db9  c1e004                   shl      eax, 4
00425dbc  01f8                     add      eax, edi
00425dbe  c1e002                   shl      eax, 2
00425dc1  01f8                     add      eax, edi
00425dc3  bbc8a04900               mov      ebx, 0x49a0c8
00425dc8  c1e002                   shl      eax, 2
00425dcb  01c3                     add      ebx, eax
00425dcd  31c0                     xor      eax, eax
00425dcf  8a437b                   mov      al, byte ptr [ebx + 0x7b]
00425dd2  31f6                     xor      esi, esi
00425dd4  e8deb20100               call     0x4410b7
00425dd9  6689c6                   mov      si, ax
00425ddc  89f0                     mov      eax, esi
00425dde  c1e002                   shl      eax, 2
00425de1  29f0                     sub      eax, esi
00425de3  c1e003                   shl      eax, 3
00425de6  01f0                     add      eax, esi
00425de8  8bab8c000000             mov      ebp, dword ptr [ebx + 0x8c]
00425dee  c1e002                   shl      eax, 2
00425df1  39e8                     cmp      eax, ebp
00425df3  770f                     ja       0x425e04
00425df5  89f8                     mov      eax, edi
00425df7  e89ca8ffff               call     0x420698
00425dfc  c6437501                 mov      byte ptr [ebx + 0x75], 1
00425e00  c6437401                 mov      byte ptr [ebx + 0x74], 1
00425e04  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425e08  0f84ff050000             je       0x42640d
00425e0e  31d2                     xor      edx, edx
00425e10  6689ca                   mov      dx, cx
00425e13  89d0                     mov      eax, edx
00425e15  c1e004                   shl      eax, 4
00425e18  01d0                     add      eax, edx
00425e1a  c1e002                   shl      eax, 2
00425e1d  01d0                     add      eax, edx
00425e1f  c1e002                   shl      eax, 2
00425e22  05c8a04900               add      eax, 0x49a0c8
00425e27  31d2                     xor      edx, edx
00425e29  8a5076                   mov      dl, byte ptr [eax + 0x76]
00425e2c  83fa07                   cmp      edx, 7
00425e2f  750a                     jne      0x425e3b
00425e31  80787500                 cmp      byte ptr [eax + 0x75], 0
00425e35  7404                     je       0x425e3b
00425e37  b001                     mov      al, 1
00425e39  eb02                     jmp      0x425e3d
00425e3b  30c0                     xor      al, al
00425e3d  84c0                     test     al, al
00425e3f  0f84c8050000             je       0x42640d
00425e45  31c0                     xor      eax, eax
00425e47  6689c8                   mov      ax, cx
00425e4a  e8b1caffff               call     0x422900
00425e4f  e9b9050000               jmp      0x42640d
00425e54  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425e58  0f84af050000             je       0x42640d
00425e5e  89d8                     mov      eax, ebx
00425e60  e8f7baffff               call     0x42195c
00425e65  e9a3050000               jmp      0x42640d
00425e6a  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425e6e  0f8499050000             je       0x42640d
00425e74  8b427c                   mov      eax, dword ptr [edx + 0x7c]
00425e77  c1f810                   sar      eax, 0x10
00425e7a  3d80000000               cmp      eax, 0x80
00425e7f  7d0c                     jge      0x425e8d
00425e81  89d8                     mov      eax, ebx
00425e83  e8ffb4ffff               call     0x421387
00425e88  e980050000               jmp      0x42640d
00425e8d  89d8                     mov      eax, ebx
00425e8f  e867b7ffff               call     0x4215fb
00425e94  e974050000               jmp      0x42640d
00425e99  807a7400                 cmp      byte ptr [edx + 0x74], 0
00425e9d  0f846a050000             je       0x42640d
00425ea3  89cf                     mov      edi, ecx
00425ea5  31db                     xor      ebx, ebx
00425ea7  6689fb                   mov      bx, di
00425eaa  89d8                     mov      eax, ebx
00425eac  c1e004                   shl      eax, 4
00425eaf  01d8                     add      eax, ebx
00425eb1  c1e002                   shl      eax, 2
00425eb4  01d8                     add      eax, ebx
00425eb6  bbc8a04900               mov      ebx, 0x49a0c8
00425ebb  c1e002                   shl      eax, 2
00425ebe  01c3                     add      ebx, eax
00425ec0  31c0                     xor      eax, eax
00425ec2  8a437b                   mov      al, byte ptr [ebx + 0x7b]
00425ec5  e8a0e80400               call     0x47476a
00425eca  83bb8c00000000           cmp      dword ptr [ebx + 0x8c], 0
00425ed1  0f84f3000000             je       0x425fca
00425ed7  807b7400                 cmp      byte ptr [ebx + 0x74], 0
00425edb  0f84e9000000             je       0x425fca
00425ee1  31c0                     xor      eax, eax
00425ee3  8a437b                   mov      al, byte ptr [ebx + 0x7b]
00425ee6  31f6                     xor      esi, esi
00425ee8  e87de80400               call     0x47476a
00425eed  6689c6                   mov      si, ax
00425ef0  89f0                     mov      eax, esi
00425ef2  c1e002                   shl      eax, 2
00425ef5  29f0                     sub      eax, esi
00425ef7  c1e003                   shl      eax, 3
00425efa  01f0                     add      eax, esi
00425efc  8bab8c000000             mov      ebp, dword ptr [ebx + 0x8c]
00425f02  c1e002                   shl      eax, 2
00425f05  39e8                     cmp      eax, ebp
00425f07  0f877c000000             ja       0x425f89
00425f0d  e9b4000000               jmp      0x425fc6
00425f12  31c0                     xor      eax, eax
00425f14  6689f8                   mov      ax, di
00425f17  e8a845ffff               call     0x41a4c4
00425f1c  25ffff0000               and      eax, 0xffff
00425f21  89842490000000           mov      dword ptr [esp + 0x90], eax
00425f28  31c0                     xor      eax, eax
00425f2a  db842490000000           fild     dword ptr [esp + 0x90]
00425f31  6689f8                   mov      ax, di
00425f34  dd5c2440                 fstp     qword ptr [esp + 0x40]
00425f38  e8b094ffff               call     0x41f3ed
00425f3d  30e4                     xor      ah, ah
00425f3f  89842498000000           mov      dword ptr [esp + 0x98], eax
00425f46  31c0                     xor      eax, eax
00425f48  df842498000000           fild     word ptr [esp + 0x98]
00425f4f  6689c8                   mov      ax, cx
00425f52  dd5c2408                 fstp     qword ptr [esp + 8]
00425f56  e89945ffff               call     0x41a4f4
00425f5b  25ff000000               and      eax, 0xff
00425f60  83f80e                   cmp      eax, 0xe
00425f63  7414                     je       0x425f79
00425f65  dd442440                 fld      qword ptr [esp + 0x40]
00425f69  dc742408                 fdiv     qword ptr [esp + 8]
00425f6d  dc0d3a444900             fmul     qword ptr [0x49443a]
00425f73  dd5c2418                 fstp     qword ptr [esp + 0x18]
00425f77  eb28                     jmp      0x425fa1
00425f79  dd442440                 fld      qword ptr [esp + 0x40]
00425f7d  dc742408                 fdiv     qword ptr [esp + 8]
00425f81  dc0d32444900             fmul     qword ptr [0x494432]
00425f87  ebea                     jmp      0x425f73
00425f89  b003                     mov      al, 3
00425f8b  81c38c000000             add      ebx, 0x8c
00425f91  89fe                     mov      esi, edi
00425f93  3c01                     cmp      al, 1
00425f95  720a                     jb       0x425fa1
00425f97  7608                     jbe      0x425fa1
00425f99  38c0                     cmp      al, al
00425f9b  0f8471ffffff             je       0x425f12
00425fa1  dd442418                 fld      qword ptr [esp + 0x18]
00425fa5  e894640600               call     0x48c43e
00425faa  db9c2490000000           fistp    dword ptr [esp + 0x90]
00425fb1  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00425fb8  25ffff0000               and      eax, 0xffff
00425fbd  8b33                     mov      esi, dword ptr [ebx]
00425fbf  83c064                   add      eax, 0x64
00425fc2  01c6                     add      esi, eax
00425fc4  8933                     mov      dword ptr [ebx], esi
00425fc6  b001                     mov      al, 1
00425fc8  eb02                     jmp      0x425fcc
00425fca  30c0                     xor      al, al
00425fcc  84c0                     test     al, al
00425fce  0f8439040000             je       0x42640d
00425fd4  31c0                     xor      eax, eax
00425fd6  8a427b                   mov      al, byte ptr [edx + 0x7b]
00425fd9  31db                     xor      ebx, ebx
00425fdb  e88ae70400               call     0x47476a
00425fe0  6689c3                   mov      bx, ax
00425fe3  89d8                     mov      eax, ebx
00425fe5  c1e002                   shl      eax, 2
00425fe8  29d8                     sub      eax, ebx
00425fea  c1e003                   shl      eax, 3
00425fed  01d8                     add      eax, ebx
00425fef  8bba8c000000             mov      edi, dword ptr [edx + 0x8c]
00425ff5  c1e002                   shl      eax, 2
00425ff8  39f8                     cmp      eax, edi
00425ffa  0f870d040000             ja       0x42640d
00426000  31d2                     xor      edx, edx
00426002  6689ca                   mov      dx, cx
00426005  89d0                     mov      eax, edx
00426007  c1e004                   shl      eax, 4
0042600a  01d0                     add      eax, edx
0042600c  c1e002                   shl      eax, 2
0042600f  01d0                     add      eax, edx
00426011  bbc8a04900               mov      ebx, 0x49a0c8
00426016  c1e002                   shl      eax, 2
00426019  01c3                     add      ebx, eax
0042601b  31d2                     xor      edx, edx
0042601d  31c0                     xor      eax, eax
0042601f  8a537b                   mov      dl, byte ptr [ebx + 0x7b]
00426022  8a4304                   mov      al, byte ptr [ebx + 4]
00426025  e84ae90400               call     0x474974
0042602a  31c0                     xor      eax, eax
0042602c  8a4304                   mov      al, byte ptr [ebx + 4]
0042602f  31d2                     xor      edx, edx
00426031  e802ea0400               call     0x474a38
00426036  8a4308                   mov      al, byte ptr [ebx + 8]
00426039  88c2                     mov      dl, al
0042603b  8a4304                   mov      al, byte ptr [ebx + 4]
0042603e  25ff000000               and      eax, 0xff
00426043  e82467ffff               call     0x41c76c
00426048  66c74378ffff             mov      word ptr [ebx + 0x78], 0xffff
0042604e  c6437bff                 mov      byte ptr [ebx + 0x7b], 0xff
00426052  66c7437c0000             mov      word ptr [ebx + 0x7c], 0
00426058  66c7437e0000             mov      word ptr [ebx + 0x7e], 0
0042605e  31d2                     xor      edx, edx
00426060  89d8                     mov      eax, ebx
00426062  8a5308                   mov      dl, byte ptr [ebx + 8]
00426065  66c78386000000ffff       mov      word ptr [ebx + 0x86], 0xffff
0042606e  83fa14                   cmp      edx, 0x14
00426071  7412                     je       0x426085
00426073  66c783800000000000       mov      word ptr [ebx + 0x80], 0
0042607c  66c783820000000000       mov      word ptr [ebx + 0x82], 0
00426085  c6407400                 mov      byte ptr [eax + 0x74], 0
00426089  31d2                     xor      edx, edx
0042608b  8a5005                   mov      dl, byte ptr [eax + 5]
0042608e  c7808c00000000000000     mov      dword ptr [eax + 0x8c], 0
00426098  83fa03                   cmp      edx, 3
0042609b  0f846c030000             je       0x42640d
004260a1  c6400505                 mov      byte ptr [eax + 5], 5
004260a5  e963030000               jmp      0x42640d
004260aa  8a6274                   mov      ah, byte ptr [edx + 0x74]
004260ad  84e4                     test     ah, ah
004260af  0f8458030000             je       0x42640d
004260b5  83ba8c00000000           cmp      dword ptr [edx + 0x8c], 0
004260bc  0f84d4000000             je       0x426196
004260c2  84e4                     test     ah, ah
004260c4  0f84cc000000             je       0x426196
004260ca  31c0                     xor      eax, eax
004260cc  8a427b                   mov      al, byte ptr [edx + 0x7b]
004260cf  31f6                     xor      esi, esi
004260d1  e8e1af0100               call     0x4410b7
004260d6  6689c6                   mov      si, ax
004260d9  89f0                     mov      eax, esi
004260db  c1e002                   shl      eax, 2
004260de  29f0                     sub      eax, esi
004260e0  c1e003                   shl      eax, 3
004260e3  01f0                     add      eax, esi
004260e5  8baa8c000000             mov      ebp, dword ptr [edx + 0x8c]
004260eb  c1e002                   shl      eax, 2
004260ee  39e8                     cmp      eax, ebp
004260f0  0f869c000000             jbe      0x426192
004260f6  89d8                     mov      eax, ebx
004260f8  89fe                     mov      esi, edi
004260fa  e8c543ffff               call     0x41a4c4
004260ff  25ffff0000               and      eax, 0xffff
00426104  89842490000000           mov      dword ptr [esp + 0x90], eax
0042610b  db842490000000           fild     dword ptr [esp + 0x90]
00426112  89d8                     mov      eax, ebx
00426114  dd5c2470                 fstp     qword ptr [esp + 0x70]
00426118  e8d092ffff               call     0x41f3ed
0042611d  30e4                     xor      ah, ah
0042611f  89842498000000           mov      dword ptr [esp + 0x98], eax
00426126  df842498000000           fild     word ptr [esp + 0x98]
0042612d  89d8                     mov      eax, ebx
0042612f  dd9c2480000000           fstp     qword ptr [esp + 0x80]
00426136  e8b943ffff               call     0x41a4f4
0042613b  25ff000000               and      eax, 0xff
00426140  83f80e                   cmp      eax, 0xe
00426143  7413                     je       0x426158
00426145  dd442470                 fld      qword ptr [esp + 0x70]
00426149  dcb42480000000           fdiv     qword ptr [esp + 0x80]
00426150  dc0d3a444900             fmul     qword ptr [0x49443a]
00426156  eb11                     jmp      0x426169
00426158  dd442470                 fld      qword ptr [esp + 0x70]
0042615c  dcb42480000000           fdiv     qword ptr [esp + 0x80]
00426163  dc0d32444900             fmul     qword ptr [0x494432]
00426169  dd5c2468                 fstp     qword ptr [esp + 0x68]
0042616d  dd442468                 fld      qword ptr [esp + 0x68]
00426171  e8c8620600               call     0x48c43e
00426176  db9c2490000000           fistp    dword ptr [esp + 0x90]
0042617d  8b842490000000           mov      eax, dword ptr [esp + 0x90]
00426184  25ffff0000               and      eax, 0xffff
00426189  8b1e                     mov      ebx, dword ptr [esi]
0042618b  83c064                   add      eax, 0x64
0042618e  01c3                     add      ebx, eax
00426190  891e                     mov      dword ptr [esi], ebx
00426192  b001                     mov      al, 1
00426194  eb02                     jmp      0x426198
00426196  30c0                     xor      al, al
00426198  84c0                     test     al, al
0042619a  0f846d020000             je       0x42640d
004261a0  31c0                     xor      eax, eax
004261a2  8a427b                   mov      al, byte ptr [edx + 0x7b]
004261a5  31db                     xor      ebx, ebx
004261a7  e80baf0100               call     0x4410b7
004261ac  6689c3                   mov      bx, ax
004261af  89d8                     mov      eax, ebx
004261b1  c1e002                   shl      eax, 2
004261b4  29d8                     sub      eax, ebx
004261b6  c1e003                   shl      eax, 3
004261b9  01d8                     add      eax, ebx
004261bb  8bb28c000000             mov      esi, dword ptr [edx + 0x8c]
004261c1  c1e002                   shl      eax, 2
004261c4  39f0                     cmp      eax, esi
004261c6  0f8741020000             ja       0x42640d
004261cc  b80a000000               mov      eax, 0xa
004261d1  e806a30400               call     0x4704dc
004261d6  31db                     xor      ebx, ebx
004261d8  31d2                     xor      edx, edx
004261da  668b1d68714900           mov      bx, word ptr [0x497168]
004261e1  f7f3                     div      ebx
004261e3  31f6                     xor      esi, esi
004261e5  6689ce                   mov      si, cx
004261e8  89f7                     mov      edi, esi
004261ea  c1e704                   shl      edi, 4
004261ed  01f7                     add      edi, esi
004261ef  c1e702                   shl      edi, 2
004261f2  01f7                     add      edi, esi
004261f4  898c2494000000           mov      dword ptr [esp + 0x94], ecx
004261fb  c1e702                   shl      edi, 2
004261fe  31c9                     xor      ecx, ecx
00426200  8a8fcca04900             mov      cl, byte ptr [edi + 0x49a0cc]
00426206  31c0                     xor      eax, eax
00426208  bb10000000               mov      ebx, 0x10
0042620d  6689d0                   mov      ax, dx
00426210  ba01000000               mov      edx, 1
00426215  e8521c0300               call     0x457e6c
0042621a  31db                     xor      ebx, ebx
0042621c  6689c3                   mov      bx, ax
0042621f  89d8                     mov      eax, ebx
00426221  89f2                     mov      edx, esi
00426223  e87e0d0300               call     0x456fa6
00426228  89d8                     mov      eax, ebx
0042622a  e8e1f80100               call     0x445b10
0042622f  b8c8a04900               mov      eax, 0x49a0c8
00426234  01f8                     add      eax, edi
00426236  66c74078ffff             mov      word ptr [eax + 0x78], 0xffff
0042623c  c6407bff                 mov      byte ptr [eax + 0x7b], 0xff
00426240  66c7407c0000             mov      word ptr [eax + 0x7c], 0
00426246  31d2                     xor      edx, edx
00426248  66c7407e0000             mov      word ptr [eax + 0x7e], 0
0042624e  8a5008                   mov      dl, byte ptr [eax + 8]
00426251  66c78086000000ffff       mov      word ptr [eax + 0x86], 0xffff
0042625a  83fa14                   cmp      edx, 0x14
0042625d  7412                     je       0x426271
0042625f  66c780800000000000       mov      word ptr [eax + 0x80], 0
00426268  66c780820000000000       mov      word ptr [eax + 0x82], 0
00426271  c6407400                 mov      byte ptr [eax + 0x74], 0
00426275  31d2                     xor      edx, edx
00426277  8a5005                   mov      dl, byte ptr [eax + 5]
0042627a  c7808c00000000000000     mov      dword ptr [eax + 0x8c], 0
00426284  83fa03                   cmp      edx, 3
00426287  7404                     je       0x42628d
00426289  c6400505                 mov      byte ptr [eax + 5], 5
0042628d  31d2                     xor      edx, edx
0042628f  668b942494000000         mov      dx, word ptr [esp + 0x94]
00426297  89d0                     mov      eax, edx
00426299  c1e004                   shl      eax, 4
0042629c  01d0                     add      eax, edx
0042629e  c1e002                   shl      eax, 2
004262a1  01d0                     add      eax, edx
004262a3  bbc8a04900               mov      ebx, 0x49a0c8
004262a8  c1e002                   shl      eax, 2
004262ab  01c3                     add      ebx, eax
004262ad  8a4304                   mov      al, byte ptr [ebx + 4]
004262b0  25ff000000               and      eax, 0xff
004262b5  31c9                     xor      ecx, ecx
004262b7  ba10000000               mov      edx, 0x10
004262bc  8a884cfb4d00             mov      cl, byte ptr [eax + 0x4dfb4c]
004262c2  e8cb0a0300               call     0x456d92
004262c7  25ffff0000               and      eax, 0xffff
004262cc  40                       inc      eax
004262cd  39c1                     cmp      ecx, eax
004262cf  0f8f38010000             jg       0x42640d
004262d5  8a4304                   mov      al, byte ptr [ebx + 4]
004262d8  31d2                     xor      edx, edx
004262da  88c2                     mov      dl, al
004262dc  89d0                     mov      eax, edx
004262de  c1e003                   shl      eax, 3
004262e1  01d0                     add      eax, edx
004262e3  c1e004                   shl      eax, 4
004262e6  29d0                     sub      eax, edx
004262e8  c1e004                   shl      eax, 4
004262eb  05e8d64d00               add      eax, 0x4dd6e8
004262f0  8d8850070000             lea      ecx, [eax + 0x750]
004262f6  ba01000000               mov      edx, 1
004262fb  89c8                     mov      eax, ecx
004262fd  bb10000000               mov      ebx, 0x10
00426302  e8410e0200               call     0x447148
00426307  ba06000000               mov      edx, 6
0042630c  89c8                     mov      eax, ecx
0042630e  e8d70f0200               call     0x4472ea
00426313  e9f5000000               jmp      0x42640d
00426318  3c0e                     cmp      al, 0xe
0042631a  0f8634fbffff             jbe      0x425e54
00426320  31db                     xor      ebx, ebx
00426322  6689cb                   mov      bx, cx
00426325  89d8                     mov      eax, ebx
00426327  c1e004                   shl      eax, 4
0042632a  01d8                     add      eax, ebx
0042632c  c1e002                   shl      eax, 2
0042632f  01d8                     add      eax, ebx
00426331  bac8a04900               mov      edx, 0x49a0c8
00426336  c1e002                   shl      eax, 2
00426339  01c2                     add      edx, eax
0042633b  83ba8c00000000           cmp      dword ptr [edx + 0x8c], 0
00426342  0f8412f8ffff             je       0x425b5a
00426348  807a7400                 cmp      byte ptr [edx + 0x74], 0
0042634c  0f8408f8ffff             je       0x425b5a
00426352  31c0                     xor      eax, eax
00426354  8a427b                   mov      al, byte ptr [edx + 0x7b]
00426357  31f6                     xor      esi, esi
00426359  e859ad0100               call     0x4410b7
0042635e  6689c6                   mov      si, ax
00426361  89f0                     mov      eax, esi
00426363  c1e002                   shl      eax, 2
00426366  29f0                     sub      eax, esi
00426368  c1e003                   shl      eax, 3
0042636b  01f0                     add      eax, esi
0042636d  8baa8c000000             mov      ebp, dword ptr [edx + 0x8c]
00426373  c1e002                   shl      eax, 2
00426376  39e8                     cmp      eax, ebp
00426378  0f86bef7ffff             jbe      0x425b3c
0042637e  89d8                     mov      eax, ebx
00426380  81c28c000000             add      edx, 0x8c
00426386  e83941ffff               call     0x41a4c4
0042638b  25ffff0000               and      eax, 0xffff
00426390  89842490000000           mov      dword ptr [esp + 0x90], eax
00426397  db842490000000           fild     dword ptr [esp + 0x90]
0042639e  89d8                     mov      eax, ebx
004263a0  dd5c2460                 fstp     qword ptr [esp + 0x60]
004263a4  e84490ffff               call     0x41f3ed
004263a9  30e4                     xor      ah, ah
004263ab  89842498000000           mov      dword ptr [esp + 0x98], eax
004263b2  df842498000000           fild     word ptr [esp + 0x98]
004263b9  89d8                     mov      eax, ebx
004263bb  dd5c2448                 fstp     qword ptr [esp + 0x48]
004263bf  e83041ffff               call     0x41a4f4
004263c4  25ff000000               and      eax, 0xff
004263c9  83f80e                   cmp      eax, 0xe
004263cc  0f847cf8ffff             je       0x425c4e
004263d2  dd442460                 fld      qword ptr [esp + 0x60]
004263d6  dc742448                 fdiv     qword ptr [esp + 0x48]
004263da  dc0d3a444900             fmul     qword ptr [0x49443a]
004263e0  e977f8ffff               jmp      0x425c5c
004263e5  3c05                     cmp      al, 5
004263e7  7218                     jb       0x426401
004263e9  0f86a1f8ffff             jbe      0x425c90
004263ef  3c06                     cmp      al, 6
004263f1  0f86a2faffff             jbe      0x425e99
004263f7  3c08                     cmp      al, 8
004263f9  0f846bfaffff             je       0x425e6a
004263ff  eb0c                     jmp      0x42640d
00426401  3c01                     cmp      al, 1
00426403  7208                     jb       0x42640d
00426405  3c02                     cmp      al, 2
00426407  0f863ef6ffff             jbe      0x425a4b
0042640d  81c49c000000             add      esp, 0x9c
00426413  e90577ffff               jmp      0x41db1d
