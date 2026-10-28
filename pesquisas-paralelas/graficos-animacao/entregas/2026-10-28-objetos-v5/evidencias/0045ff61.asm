; CalculTabPlayer [0x45ff61, 0x46003b)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045ff61  53                     push     ebx
0045ff62  51                     push     ecx
0045ff63  52                     push     edx
0045ff64  56                     push     esi
0045ff65  57                     push     edi
0045ff66  83ec20                 sub      esp, 0x20
0045ff69  b908000000             mov      ecx, 8
0045ff6e  89e7                   mov      edi, esp
0045ff70  be4c6d4900             mov      esi, 0x496d4c
0045ff75  f3a5                   rep movsd dword ptr es:[edi], dword ptr [esi]
0045ff77  31c9                   xor      ecx, ecx
0045ff79  eb1e                   jmp      0x45ff99 ;
0045ff7b  31d2                   xor      edx, edx
0045ff7d  6689ca                 mov      dx, cx
0045ff80  8b1495c8244e00         mov      edx, dword ptr [edx*4 + 0x4e24c8]
0045ff87  88041a                 mov      byte ptr [edx + ebx], al
0045ff8a  40                     inc      eax
0045ff8b  31db                   xor      ebx, ebx
0045ff8d  6689c3                 mov      bx, ax
0045ff90  81fb00010000           cmp      ebx, 0x100
0045ff96  7ce3                   jl       0x45ff7b
0045ff98  41                     inc      ecx
0045ff99  31d2                   xor      edx, edx
0045ff9b  6689ca                 mov      dx, cx
0045ff9e  83fa04                 cmp      edx, 4
0045ffa1  7d04                   jge      0x45ffa7
0045ffa3  31c0                   xor      eax, eax
0045ffa5  ebe4                   jmp      0x45ff8b ;
0045ffa7  31c0                   xor      eax, eax
0045ffa9  eb0a                   jmp      0x45ffb5 ;
0045ffab  8b1dd8244e00           mov      ebx, dword ptr [0x4e24d8]
0045ffb1  88041a                 mov      byte ptr [edx + ebx], al
0045ffb4  40                     inc      eax
0045ffb5  31d2                   xor      edx, edx
0045ffb7  6689c2                 mov      dx, ax
0045ffba  81fa00010000           cmp      edx, 0x100
0045ffc0  7ce9                   jl       0x45ffab
0045ffc2  31c0                   xor      eax, eax
0045ffc4  eb41                   jmp      0x460007 ;
0045ffc6  8b1dcc244e00           mov      ebx, dword ptr [0x4e24cc]
0045ffcc  8a0c14                 mov      cl, byte ptr [esp + edx]
0045ffcf  888c1aa0000000         mov      byte ptr [edx + ebx + 0xa0], cl
0045ffd6  8b1dd0244e00           mov      ebx, dword ptr [0x4e24d0]
0045ffdc  8a4c1408               mov      cl, byte ptr [esp + edx + 8]
0045ffe0  888c1aa0000000         mov      byte ptr [edx + ebx + 0xa0], cl
0045ffe7  8b1dd4244e00           mov      ebx, dword ptr [0x4e24d4]
0045ffed  8a4c1410               mov      cl, byte ptr [esp + edx + 0x10]
0045fff1  888c1aa0000000         mov      byte ptr [edx + ebx + 0xa0], cl
0045fff8  8b1dd8244e00           mov      ebx, dword ptr [0x4e24d8]
0045fffe  40                     inc      eax
0045ffff  c6841aa00000002f       mov      byte ptr [edx + ebx + 0xa0], 0x2f
00460007  31d2                   xor      edx, edx
00460009  6689c2                 mov      dx, ax
0046000c  83fa08                 cmp      edx, 8
0046000f  7cb5                   jl       0x45ffc6
00460011  31c0                   xor      eax, eax
00460013  eb14                   jmp      0x460029 ;
00460015  8b1c95c8244e00         mov      ebx, dword ptr [edx*4 + 0x4e24c8]
0046001c  8a9ba0000000           mov      bl, byte ptr [ebx + 0xa0]
00460022  40                     inc      eax
00460023  889adc244e00           mov      byte ptr [edx + 0x4e24dc], bl
00460029  31d2                   xor      edx, edx
0046002b  6689c2                 mov      dx, ax
0046002e  83fa04                 cmp      edx, 4
00460031  7ee2                   jle      0x460015
00460033  83c420                 add      esp, 0x20
00460036  e99efdffff             jmp      0x45fdd9 ;
