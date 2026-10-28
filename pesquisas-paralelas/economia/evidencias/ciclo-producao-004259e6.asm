; CalculTroupe entry and selected production branches; exclusive end 0x00425c4e.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Only building types 1/2/13/16 are in the implemented caller domain.
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
