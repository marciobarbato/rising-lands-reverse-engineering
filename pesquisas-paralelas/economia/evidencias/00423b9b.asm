; ConstruitPerso: limite por próximo símbolo SBL, fim exclusivo 0x00423d14.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423b9b  53                       push     ebx
00423b9c  51                       push     ecx
00423b9d  52                       push     edx
00423b9e  56                       push     esi
00423b9f  57                       push     edi
00423ba0  83ec20                   sub      esp, 0x20
00423ba3  89c2                     mov      edx, eax
00423ba5  31c9                     xor      ecx, ecx
00423ba7  6689c1                   mov      cx, ax
00423baa  89c8                     mov      eax, ecx
00423bac  c1e004                   shl      eax, 4
00423baf  01c8                     add      eax, ecx
00423bb1  c1e002                   shl      eax, 2
00423bb4  01c8                     add      eax, ecx
00423bb6  b9c8a04900               mov      ecx, 0x49a0c8
00423bbb  c1e002                   shl      eax, 2
00423bbe  01c1                     add      ecx, eax
00423bc0  83b98c00000000           cmp      dword ptr [ecx + 0x8c], 0
00423bc7  0f8443010000             je       0x423d10
00423bcd  80797400                 cmp      byte ptr [ecx + 0x74], 0
00423bd1  0f8439010000             je       0x423d10
00423bd7  31c0                     xor      eax, eax
00423bd9  8a417b                   mov      al, byte ptr [ecx + 0x7b]
00423bdc  31f6                     xor      esi, esi
00423bde  e8d4d40100               call     0x4410b7
00423be3  6689c6                   mov      si, ax
00423be6  89f0                     mov      eax, esi
00423be8  c1e002                   shl      eax, 2
00423beb  29f0                     sub      eax, esi
00423bed  c1e003                   shl      eax, 3
00423bf0  01f0                     add      eax, esi
00423bf2  c1e002                   shl      eax, 2
00423bf5  3b818c000000             cmp      eax, dword ptr [ecx + 0x8c]
00423bfb  7744                     ja       0x423c41
00423bfd  e904010000               jmp      0x423d06
00423c02  31c9                     xor      ecx, ecx
00423c04  88c1                     mov      cl, al
00423c06  89c8                     mov      eax, ecx
00423c08  c1e002                   shl      eax, 2
00423c0b  29c8                     sub      eax, ecx
00423c0d  c1e002                   shl      eax, 2
00423c10  01c8                     add      eax, ecx
00423c12  8a15e85b4900             mov      dl, byte ptr [0x495be8]
00423c18  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423c1f  28d0                     sub      al, dl
00423c21  e96d000000               jmp      0x423c93
00423c26  31c9                     xor      ecx, ecx
00423c28  88c1                     mov      cl, al
00423c2a  89c8                     mov      eax, ecx
00423c2c  c1e002                   shl      eax, 2
00423c2f  29c8                     sub      eax, ecx
00423c31  c1e002                   shl      eax, 2
00423c34  01c8                     add      eax, ecx
00423c36  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423c3d  fec8                     dec      al
00423c3f  eb52                     jmp      0x423c93
00423c41  bb09000000               mov      ebx, 9
00423c46  8db18c000000             lea      esi, [ecx + 0x8c]
00423c4c  89d7                     mov      edi, edx
00423c4e  ba01000000               mov      edx, 1
00423c53  8d410c                   lea      eax, [ecx + 0xc]
00423c56  e85d350200               call     0x4471b8
00423c5b  25ffff0000               and      eax, 0xffff
00423c60  89442418                 mov      dword ptr [esp + 0x18], eax
00423c64  89ca                     mov      edx, ecx
00423c66  db442418                 fild     dword ptr [esp + 0x18]
00423c6a  8a4108                   mov      al, byte ptr [ecx + 8]
00423c6d  dd5c2410                 fstp     qword ptr [esp + 0x10]
00423c71  3c0e                     cmp      al, 0xe
00423c73  7206                     jb       0x423c7b
00423c75  76af                     jbe      0x423c26
00423c77  3c13                     cmp      al, 0x13
00423c79  7487                     je       0x423c02
00423c7b  31c9                     xor      ecx, ecx
00423c7d  8a4a08                   mov      cl, byte ptr [edx + 8]
00423c80  89c8                     mov      eax, ecx
00423c82  c1e002                   shl      eax, 2
00423c85  29c8                     sub      eax, ecx
00423c87  c1e002                   shl      eax, 2
00423c8a  01c8                     add      eax, ecx
00423c8c  8a04859e5d4900           mov      al, byte ptr [eax*4 + 0x495d9e]
00423c93  31c9                     xor      ecx, ecx
00423c95  30e4                     xor      ah, ah
00423c97  6689f9                   mov      cx, di
00423c9a  8944241c                 mov      dword ptr [esp + 0x1c], eax
00423c9e  89c8                     mov      eax, ecx
00423ca0  c1e004                   shl      eax, 4
00423ca3  01c8                     add      eax, ecx
00423ca5  c1e002                   shl      eax, 2
00423ca8  01c8                     add      eax, ecx
00423caa  c1e002                   shl      eax, 2
00423cad  df44241c                 fild     word ptr [esp + 0x1c]
00423cb1  05c8a04900               add      eax, 0x49a0c8
00423cb6  dd5c2408                 fstp     qword ptr [esp + 8]
00423cba  8a4008                   mov      al, byte ptr [eax + 8]
00423cbd  25ff000000               and      eax, 0xff
00423cc2  83f80e                   cmp      eax, 0xe
00423cc5  7410                     je       0x423cd7
00423cc7  dd442410                 fld      qword ptr [esp + 0x10]
00423ccb  dc742408                 fdiv     qword ptr [esp + 8]
00423ccf  dc0def434900             fmul     qword ptr [0x4943ef]
00423cd5  eb0e                     jmp      0x423ce5
00423cd7  dd442410                 fld      qword ptr [esp + 0x10]
00423cdb  dc742408                 fdiv     qword ptr [esp + 8]
00423cdf  dc0de7434900             fmul     qword ptr [0x4943e7]
00423ce5  dd1c24                   fstp     qword ptr [esp]
00423ce8  dd0424                   fld      qword ptr [esp]
00423ceb  e84e870600               call     0x48c43e
00423cf0  db5c2418                 fistp    dword ptr [esp + 0x18]
00423cf4  8b442418                 mov      eax, dword ptr [esp + 0x18]
00423cf8  25ffff0000               and      eax, 0xffff
00423cfd  8b3e                     mov      edi, dword ptr [esi]
00423cff  83c064                   add      eax, 0x64
00423d02  01c7                     add      edi, eax
00423d04  893e                     mov      dword ptr [esi], edi
00423d06  b001                     mov      al, 1
00423d08  83c420                   add      esp, 0x20
00423d0b  e90e9effff               jmp      0x41db1e
00423d10  30c0                     xor      al, al
00423d12  ebf4                     jmp      0x423d08
