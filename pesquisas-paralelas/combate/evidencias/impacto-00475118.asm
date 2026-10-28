; MAJSympathie; [0x00475118,0x00475267)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00475118  51                       push     ecx
00475119  56                       push     esi
0047511a  57                       push     edi
0047511b  55                       push     ebp
0047511c  83ec10                   sub      esp, 0x10
0047511f  89c1                     mov      ecx, eax
00475121  39d0                     cmp      eax, edx
00475123  0f8436010000             je       0x47525f
00475129  83f804                   cmp      eax, 4
0047512c  0f832d010000             jae      0x47525f
00475132  83fa04                   cmp      edx, 4
00475135  0f8324010000             jae      0x47525f
0047513b  c1e004                   shl      eax, 4
0047513e  80b890a9510000           cmp      byte ptr [eax + 0x51a990], 0
00475145  0f8514010000             jne      0x47525f
0047514b  89d0                     mov      eax, edx
0047514d  c1e004                   shl      eax, 4
00475150  80b890a9510000           cmp      byte ptr [eax + 0x51a990], 0
00475157  0f8502010000             jne      0x47525f
0047515d  89d8                     mov      eax, ebx
0047515f  c1e004                   shl      eax, 4
00475162  8b9890724900             mov      ebx, dword ptr [eax + 0x497290]
00475168  43                       inc      ebx
00475169  8bb094724900             mov      esi, dword ptr [eax + 0x497294]
0047516f  899890724900             mov      dword ptr [eax + 0x497290], ebx
00475175  39f3                     cmp      ebx, esi
00475177  0f82e2000000             jb       0x47525f
0047517d  31db                     xor      ebx, ebx
0047517f  31ff                     xor      edi, edi
00475181  8a988c724900             mov      bl, byte ptr [eax + 0x49728c]
00475187  89b890724900             mov      dword ptr [eax + 0x497290], edi
0047518d  83fb01                   cmp      ebx, 1
00475190  0f8576000000             jne      0x47520c
00475196  89c7                     mov      edi, eax
00475198  31f6                     xor      esi, esi
0047519a  bd32000000               mov      ebp, 0x32
0047519f  eb0a                     jmp      0x4751ab
004751a1  46                       inc      esi
004751a2  83fe04                   cmp      esi, 4
004751a5  0f8db4000000             jge      0x47525f
004751ab  31c9                     xor      ecx, ecx
004751ad  eb24                     jmp      0x4751d3
004751af  83fbce                   cmp      ebx, -0x32
004751b2  7d05                     jge      0x4751b9
004751b4  bbceffffff               mov      ebx, 0xffffffce
004751b9  0fbfdb                   movsx    ebx, bx
004751bc  31d2                     xor      edx, edx
004751be  31c0                     xor      eax, eax
004751c0  8a542408                 mov      dl, byte ptr [esp + 8]
004751c4  8a44240c                 mov      al, byte ptr [esp + 0xc]
004751c8  e8c38affff               call     0x46dc90
004751cd  41                       inc      ecx
004751ce  83f904                   cmp      ecx, 4
004751d1  7dce                     jge      0x4751a1
004751d3  39ce                     cmp      esi, ecx
004751d5  74f6                     je       0x4751cd
004751d7  8974240c                 mov      dword ptr [esp + 0xc], esi
004751db  894c2408                 mov      dword ptr [esp + 8], ecx
004751df  8b9f88724900             mov      ebx, dword ptr [edi + 0x497288]
004751e5  83fe04                   cmp      esi, 4
004751e8  73e3                     jae      0x4751cd
004751ea  83f904                   cmp      ecx, 4
004751ed  73de                     jae      0x4751cd
004751ef  31d2                     xor      edx, edx
004751f1  31c0                     xor      eax, eax
004751f3  8a542408                 mov      dl, byte ptr [esp + 8]
004751f7  8a44240c                 mov      al, byte ptr [esp + 0xc]
004751fb  e86c8affff               call     0x46dc6c
00475200  98                       cwde
00475201  01c3                     add      ebx, eax
00475203  83fb32                   cmp      ebx, 0x32
00475206  7ea7                     jle      0x4751af
00475208  89eb                     mov      ebx, ebp
0047520a  ebad                     jmp      0x4751b9
0047520c  894c2404                 mov      dword ptr [esp + 4], ecx
00475210  891424                   mov      dword ptr [esp], edx
00475213  8b9888724900             mov      ebx, dword ptr [eax + 0x497288]
00475219  83f904                   cmp      ecx, 4
0047521c  7341                     jae      0x47525f
0047521e  83fa04                   cmp      edx, 4
00475221  733c                     jae      0x47525f
00475223  31d2                     xor      edx, edx
00475225  31c0                     xor      eax, eax
00475227  8a1424                   mov      dl, byte ptr [esp]
0047522a  8a442404                 mov      al, byte ptr [esp + 4]
0047522e  e8398affff               call     0x46dc6c
00475233  98                       cwde
00475234  01c3                     add      ebx, eax
00475236  83fb32                   cmp      ebx, 0x32
00475239  7e07                     jle      0x475242
0047523b  bb32000000               mov      ebx, 0x32
00475240  eb0a                     jmp      0x47524c
00475242  83fbce                   cmp      ebx, -0x32
00475245  7d05                     jge      0x47524c
00475247  bbceffffff               mov      ebx, 0xffffffce
0047524c  0fbfdb                   movsx    ebx, bx
0047524f  31d2                     xor      edx, edx
00475251  31c0                     xor      eax, eax
00475253  8a1424                   mov      dl, byte ptr [esp]
00475256  8a442404                 mov      al, byte ptr [esp + 4]
0047525a  e8318affff               call     0x46dc90
0047525f  83c410                   add      esp, 0x10
00475262  5d                       pop      ebp
00475263  5f                       pop      edi
00475264  5e                       pop      esi
00475265  59                       pop      ecx
00475266  c3                       ret
