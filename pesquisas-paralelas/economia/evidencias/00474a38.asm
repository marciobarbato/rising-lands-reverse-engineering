; SortilegeSetTechnologie: limite por próximo símbolo SBL, fim exclusivo 0x00474a95.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00474a38  53                       push     ebx
00474a39  51                       push     ecx
00474a3a  52                       push     edx
00474a3b  56                       push     esi
00474a3c  83ec04                   sub      esp, 4
00474a3f  880424                   mov      byte ptr [esp], al
00474a42  31c0                     xor      eax, eax
00474a44  ba04000000               mov      edx, 4
00474a49  8a0424                   mov      al, byte ptr [esp]
00474a4c  31c9                     xor      ecx, ecx
00474a4e  e8742afdff               call     0x4474c7
00474a53  ba05000000               mov      edx, 5
00474a58  89c6                     mov      esi, eax
00474a5a  e8e926fdff               call     0x447148
00474a5f  eb01                     jmp      0x474a62
00474a61  41                       inc      ecx
00474a62  31db                     xor      ebx, ebx
00474a64  6689cb                   mov      bx, cx
00474a67  83fb05                   cmp      ebx, 5
00474a6a  7d21                     jge      0x474a8d
00474a6c  31c0                     xor      eax, eax
00474a6e  8a0424                   mov      al, byte ptr [esp]
00474a71  8d0480                   lea      eax, [eax + eax*4]
00474a74  8a8403308f5000           mov      al, byte ptr [ebx + eax + 0x508f30]
00474a7b  84c0                     test     al, al
00474a7d  74e2                     je       0x474a61
00474a7f  ba04000000               mov      edx, 4
00474a84  89f0                     mov      eax, esi
00474a86  e8f829fdff               call     0x447483
00474a8b  ebd4                     jmp      0x474a61
00474a8d  83c404                   add      esp, 4
00474a90  5e                       pop      esi
00474a91  5a                       pop      edx
00474a92  59                       pop      ecx
00474a93  5b                       pop      ebx
00474a94  c3                       ret
