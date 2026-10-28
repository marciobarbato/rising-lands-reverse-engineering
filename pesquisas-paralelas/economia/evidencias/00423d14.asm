; ConstruitSort: limite por próximo símbolo SBL, fim exclusivo 0x00423e65.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423d14  53                       push     ebx
00423d15  51                       push     ecx
00423d16  52                       push     edx
00423d17  56                       push     esi
00423d18  57                       push     edi
00423d19  83ec20                   sub      esp, 0x20
00423d1c  89c2                     mov      edx, eax
00423d1e  31c9                     xor      ecx, ecx
00423d20  6689c1                   mov      cx, ax
00423d23  89c8                     mov      eax, ecx
00423d25  c1e004                   shl      eax, 4
00423d28  01c8                     add      eax, ecx
00423d2a  c1e002                   shl      eax, 2
00423d2d  01c8                     add      eax, ecx
00423d2f  b9c8a04900               mov      ecx, 0x49a0c8
00423d34  c1e002                   shl      eax, 2
00423d37  01c1                     add      ecx, eax
00423d39  31c0                     xor      eax, eax
00423d3b  8a417b                   mov      al, byte ptr [ecx + 0x7b]
00423d3e  e8270a0500               call     0x47476a
00423d43  83b98c00000000           cmp      dword ptr [ecx + 0x8c], 0
00423d4a  74c4                     je       0x423d10
00423d4c  80797400                 cmp      byte ptr [ecx + 0x74], 0
00423d50  74be                     je       0x423d10
00423d52  31c0                     xor      eax, eax
00423d54  8a417b                   mov      al, byte ptr [ecx + 0x7b]
00423d57  31f6                     xor      esi, esi
00423d59  e80c0a0500               call     0x47476a
00423d5e  6689c6                   mov      si, ax
00423d61  89f0                     mov      eax, esi
00423d63  c1e002                   shl      eax, 2
00423d66  29f0                     sub      eax, esi
00423d68  c1e003                   shl      eax, 3
00423d6b  01f0                     add      eax, esi
00423d6d  c1e002                   shl      eax, 2
00423d70  3b818c000000             cmp      eax, dword ptr [ecx + 0x8c]
00423d76  7741                     ja       0x423db9
00423d78  eb8c                     jmp      0x423d06
00423d7a  31c9                     xor      ecx, ecx
00423d7c  88c1                     mov      cl, al
00423d7e  89c8                     mov      eax, ecx
00423d80  c1e002                   shl      eax, 2
00423d83  29c8                     sub      eax, ecx
00423d85  c1e002                   shl      eax, 2
00423d88  01c8                     add      eax, ecx
00423d8a  8a15e85b4900             mov      dl, byte ptr [0x495be8]
00423d90  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423d97  28d0                     sub      al, dl
00423d99  e96d000000               jmp      0x423e0b
00423d9e  31c9                     xor      ecx, ecx
00423da0  88c1                     mov      cl, al
00423da2  89c8                     mov      eax, ecx
00423da4  c1e002                   shl      eax, 2
00423da7  29c8                     sub      eax, ecx
00423da9  c1e002                   shl      eax, 2
00423dac  01c8                     add      eax, ecx
00423dae  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423db5  fec8                     dec      al
00423db7  eb52                     jmp      0x423e0b
00423db9  bb09000000               mov      ebx, 9
00423dbe  8db18c000000             lea      esi, [ecx + 0x8c]
00423dc4  89d7                     mov      edi, edx
00423dc6  ba01000000               mov      edx, 1
00423dcb  8d410c                   lea      eax, [ecx + 0xc]
00423dce  e8e5330200               call     0x4471b8
00423dd3  25ffff0000               and      eax, 0xffff
00423dd8  89442418                 mov      dword ptr [esp + 0x18], eax
00423ddc  89ca                     mov      edx, ecx
00423dde  db442418                 fild     dword ptr [esp + 0x18]
00423de2  8a4108                   mov      al, byte ptr [ecx + 8]
00423de5  dd5c2410                 fstp     qword ptr [esp + 0x10]
00423de9  3c0e                     cmp      al, 0xe
00423deb  7206                     jb       0x423df3
00423ded  76af                     jbe      0x423d9e
00423def  3c13                     cmp      al, 0x13
00423df1  7487                     je       0x423d7a
00423df3  31c9                     xor      ecx, ecx
00423df5  8a4a08                   mov      cl, byte ptr [edx + 8]
00423df8  89c8                     mov      eax, ecx
00423dfa  c1e002                   shl      eax, 2
00423dfd  29c8                     sub      eax, ecx
00423dff  c1e002                   shl      eax, 2
00423e02  01c8                     add      eax, ecx
00423e04  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423e0b  31c9                     xor      ecx, ecx
00423e0d  30e4                     xor      ah, ah
00423e0f  6689f9                   mov      cx, di
00423e12  8944241c                 mov      dword ptr [esp + 0x1c], eax
00423e16  89c8                     mov      eax, ecx
00423e18  c1e004                   shl      eax, 4
00423e1b  01c8                     add      eax, ecx
00423e1d  c1e002                   shl      eax, 2
00423e20  01c8                     add      eax, ecx
00423e22  c1e002                   shl      eax, 2
00423e25  df44241c                 fild     word ptr [esp + 0x1c]
00423e29  05c8a04900               add      eax, 0x49a0c8
00423e2e  dd5c2408                 fstp     qword ptr [esp + 8]
00423e32  8a4008                   mov      al, byte ptr [eax + 8]
00423e35  25ff000000               and      eax, 0xff
00423e3a  83f80e                   cmp      eax, 0xe
00423e3d  7413                     je       0x423e52
00423e3f  dd442410                 fld      qword ptr [esp + 0x10]
00423e43  dc742408                 fdiv     qword ptr [esp + 8]
00423e47  dc0d0a444900             fmul     qword ptr [0x49440a]
00423e4d  e993feffff               jmp      0x423ce5
00423e52  dd442410                 fld      qword ptr [esp + 0x10]
00423e56  dc742408                 fdiv     qword ptr [esp + 8]
00423e5a  dc0d02444900             fmul     qword ptr [0x494402]
00423e60  e980feffff               jmp      0x423ce5
