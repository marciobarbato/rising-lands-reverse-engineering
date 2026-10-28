; SortilegeInitTechnologie: limite por próximo símbolo SBL, fim exclusivo 0x00474b08.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00474a95  53                       push     ebx
00474a96  51                       push     ecx
00474a97  52                       push     edx
00474a98  56                       push     esi
00474a99  57                       push     edi
00474a9a  55                       push     ebp
00474a9b  83ec08                   sub      esp, 8
00474a9e  bd05000000               mov      ebp, 5
00474aa3  30e4                     xor      ah, ah
00474aa5  bf04000000               mov      edi, 4
00474aaa  882424                   mov      byte ptr [esp], ah
00474aad  eb03                     jmp      0x474ab2
00474aaf  fe0424                   inc      byte ptr [esp]
00474ab2  31c0                     xor      eax, eax
00474ab4  8a0424                   mov      al, byte ptr [esp]
00474ab7  83f804                   cmp      eax, 4
00474aba  7d42                     jge      0x474afe
00474abc  89fa                     mov      edx, edi
00474abe  88442404                 mov      byte ptr [esp + 4], al
00474ac2  e8002afdff               call     0x4474c7
00474ac7  31c9                     xor      ecx, ecx
00474ac9  89ea                     mov      edx, ebp
00474acb  89c6                     mov      esi, eax
00474acd  e87626fdff               call     0x447148
00474ad2  eb01                     jmp      0x474ad5
00474ad4  41                       inc      ecx
00474ad5  31db                     xor      ebx, ebx
00474ad7  6689cb                   mov      bx, cx
00474ada  83fb05                   cmp      ebx, 5
00474add  7dd0                     jge      0x474aaf
00474adf  31c0                     xor      eax, eax
00474ae1  8a442404                 mov      al, byte ptr [esp + 4]
00474ae5  8d0480                   lea      eax, [eax + eax*4]
00474ae8  8a8403308f5000           mov      al, byte ptr [ebx + eax + 0x508f30]
00474aef  84c0                     test     al, al
00474af1  74e1                     je       0x474ad4
00474af3  89fa                     mov      edx, edi
00474af5  89f0                     mov      eax, esi
00474af7  e88729fdff               call     0x447483
00474afc  ebd6                     jmp      0x474ad4
00474afe  83c408                   add      esp, 8
00474b01  5d                       pop      ebp
00474b02  5f                       pop      edi
00474b03  5e                       pop      esi
00474b04  5a                       pop      edx
00474b05  59                       pop      ecx
00474b06  5b                       pop      ebx
00474b07  c3                       ret
