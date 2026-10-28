; HandlSnd_Insert_dependency; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048a218  56                       push esi
0048a219  57                       push edi
0048a21a  55                       push ebp
0048a21b  83ec08                   sub esp, 8
0048a21e  89c5                     mov ebp, eax
0048a220  891424                   mov dword ptr [esp], edx
0048a223  89de                     mov esi, ebx
0048a225  8b13                     mov edx, dword ptr [ebx]
0048a227  83faff                   cmp edx, -1
0048a22a  0f8494010000             je 0x48a3c4
0048a230  837c241800               cmp dword ptr [esp + 0x18], 0
0048a235  0f857e000000             jne 0x48a2b9
0048a23b  8b1b                     mov ebx, dword ptr [ebx]
0048a23d  89d8                     mov eax, ebx
0048a23f  c1e002                   shl eax, 2
0048a242  29d8                     sub eax, ebx
0048a244  c1e002                   shl eax, 2
0048a247  29d8                     sub eax, ebx
0048a249  c1e002                   shl eax, 2
0048a24c  8b9894135200             mov ebx, dword ptr [eax + 0x521394]
0048a252  668b5b04                 mov bx, word ptr [ebx + 4]
0048a256  81e3ffff0000             and ebx, 0xffff
0048a25c  81fb00010000             cmp ebx, 0x100
0048a262  7455                     je 0x48a2b9
0048a264  057c135200               add eax, 0x52137c
0048a269  31db                     xor ebx, ebx
0048a26b  8a5808                   mov bl, byte ptr [eax + 8]
0048a26e  89c6                     mov esi, eax
0048a270  83fb01                   cmp ebx, 1
0048a273  7505                     jne 0x48a27a
0048a275  e8bbfbffff               call 0x489e35
0048a27a  8b4628                   mov eax, dword ptr [esi + 0x28]
0048a27d  8338ff                   cmp dword ptr [eax], -1
0048a280  742d                     je 0x48a2af
0048a282  31db                     xor ebx, ebx
0048a284  8a5e08                   mov bl, byte ptr [esi + 8]
0048a287  85db                     test ebx, ebx
0048a289  7424                     je 0x48a2af
0048a28b  83fb02                   cmp ebx, 2
0048a28e  750e                     jne 0x48a29e
0048a290  ba01000000               mov edx, 1
0048a295  89f0                     mov eax, esi
0048a297  e87f0c0000               call 0x48af1b
0048a29c  eb11                     jmp 0x48a2af
0048a29e  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a2a4  c6460800                 mov byte ptr [esi + 8], 0
0048a2a8  c7462000000000           mov dword ptr [esi + 0x20], 0
0048a2af  b801000000               mov eax, 1
0048a2b4  e976010000               jmp 0x48a42f
0048a2b9  8b1e                     mov ebx, dword ptr [esi]
0048a2bb  89d8                     mov eax, ebx
0048a2bd  c1e002                   shl eax, 2
0048a2c0  29d8                     sub eax, ebx
0048a2c2  c1e002                   shl eax, 2
0048a2c5  29d8                     sub eax, ebx
0048a2c7  c1e002                   shl eax, 2
0048a2ca  3ba87c135200             cmp ebp, dword ptr [eax + 0x52137c]
0048a2d0  7518                     jne 0x48a2ea
0048a2d2  8b1c24                   mov ebx, dword ptr [esp]
0048a2d5  3b9880135200             cmp ebx, dword ptr [eax + 0x521380]
0048a2db  750d                     jne 0x48a2ea
0048a2dd  8b542418                 mov edx, dword ptr [esp + 0x18]
0048a2e1  89f0                     mov eax, esi
0048a2e3  e862feffff               call 0x48a14a
0048a2e8  ebc5                     jmp 0x48a2af
0048a2ea  8b1e                     mov ebx, dword ptr [esi]
0048a2ec  89d8                     mov eax, ebx
0048a2ee  c1e002                   shl eax, 2
0048a2f1  29d8                     sub eax, ebx
0048a2f3  c1e002                   shl eax, 2
0048a2f6  29d8                     sub eax, ebx
0048a2f8  c1e002                   shl eax, 2
0048a2fb  31db                     xor ebx, ebx
0048a2fd  8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048a303  83fb01                   cmp ebx, 1
0048a306  7566                     jne 0x48a36e
0048a308  057c135200               add eax, 0x52137c
0048a30d  0fb67808                 movzx edi, byte ptr [eax + 8]
0048a311  89c3                     mov ebx, eax
0048a313  83ff01                   cmp edi, 1
0048a316  7505                     jne 0x48a31d
0048a318  e818fbffff               call 0x489e35
0048a31d  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a320  8338ff                   cmp dword ptr [eax], -1
0048a323  742c                     je 0x48a351
0048a325  0fb67b08                 movzx edi, byte ptr [ebx + 8]
0048a329  85ff                     test edi, edi
0048a32b  7424                     je 0x48a351
0048a32d  83ff02                   cmp edi, 2
0048a330  750e                     jne 0x48a340
0048a332  ba01000000               mov edx, 1
0048a337  89d8                     mov eax, ebx
0048a339  e8dd0b0000               call 0x48af1b
0048a33e  eb11                     jmp 0x48a351
0048a340  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a346  c6430800                 mov byte ptr [ebx + 8], 0
0048a34a  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a351  e8a20b0000               call 0x48aef8
0048a356  8906                     mov dword ptr [esi], eax
0048a358  83f8ff                   cmp eax, -1
0048a35b  7507                     jne 0x48a364
0048a35d  31c0                     xor eax, eax
0048a35f  e9cb000000               jmp 0x48a42f
0048a364  c705841f520001000000     mov dword ptr [0x521f84], 1
0048a36e  8b442418                 mov eax, dword ptr [esp + 0x18]
0048a372  8b1e                     mov ebx, dword ptr [esi]
0048a374  50                       push eax
0048a375  89d8                     mov eax, ebx
0048a377  c1e002                   shl eax, 2
0048a37a  29d8                     sub eax, ebx
0048a37c  c1e002                   shl eax, 2
0048a37f  29d8                     sub eax, ebx
0048a381  89ea                     mov edx, ebp
0048a383  c1e002                   shl eax, 2
0048a386  8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a38a  057c135200               add eax, 0x52137c
0048a38f  e860fdffff               call 0x48a0f4
0048a394  8b1e                     mov ebx, dword ptr [esi]
0048a396  89d8                     mov eax, ebx
0048a398  c1e002                   shl eax, 2
0048a39b  29d8                     sub eax, ebx
0048a39d  c1e002                   shl eax, 2
0048a3a0  29d8                     sub eax, ebx
0048a3a2  893485a4135200           mov dword ptr [eax*4 + 0x5213a4], esi
0048a3a9  8b1e                     mov ebx, dword ptr [esi]
0048a3ab  89d8                     mov eax, ebx
0048a3ad  c1e002                   shl eax, 2
0048a3b0  29d8                     sub eax, ebx
0048a3b2  c1e002                   shl eax, 2
0048a3b5  29d8                     sub eax, ebx
0048a3b7  c604858413520002         mov byte ptr [eax*4 + 0x521384], 2
0048a3bf  e9ebfeffff               jmp 0x48a2af
0048a3c4  e82f0b0000               call 0x48aef8
0048a3c9  89442404                 mov dword ptr [esp + 4], eax
0048a3cd  39d0                     cmp eax, edx
0048a3cf  7504                     jne 0x48a3d5
0048a3d1  31d0                     xor eax, edx
0048a3d3  eb5a                     jmp 0x48a42f
0048a3d5  8b7c2418                 mov edi, dword ptr [esp + 0x18]
0048a3d9  57                       push edi
0048a3da  89c7                     mov edi, eax
0048a3dc  c1e702                   shl edi, 2
0048a3df  29c7                     sub edi, eax
0048a3e1  c1e702                   shl edi, 2
0048a3e4  8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a3e8  29c7                     sub edi, eax
0048a3ea  b87c135200               mov eax, 0x52137c
0048a3ef  c1e702                   shl edi, 2
0048a3f2  89ea                     mov edx, ebp
0048a3f4  01f8                     add eax, edi
0048a3f6  e8f9fcffff               call 0x48a0f4
0048a3fb  85c0                     test eax, eax
0048a3fd  750a                     jne 0x48a409
0048a3ff  e8cc0b0000               call 0x48afd0
0048a404  e954ffffff               jmp 0x48a35d
0048a409  8b442404                 mov eax, dword ptr [esp + 4]
0048a40d  8906                     mov dword ptr [esi], eax
0048a40f  b402                     mov ah, 2
0048a411  89b7a4135200             mov dword ptr [edi + 0x5213a4], esi
0048a417  31ed                     xor ebp, ebp
0048a419  88a784135200             mov byte ptr [edi + 0x521384], ah
0048a41f  b801000000               mov eax, 1
0048a424  89af90135200             mov dword ptr [edi + 0x521390], ebp
0048a42a  a3841f5200               mov dword ptr [0x521f84], eax
0048a42f  83c408                   add esp, 8
0048a432  5d                       pop ebp
0048a433  5f                       pop edi
0048a434  5e                       pop esi
0048a435  c20400                   ret 4
