; PlayerRetrieve: Copies +6 and +0x0c..+0x13 of four 20-byte players from [0x5080ac] to [0x5080a8]; exclusive end 0x0046dfa0.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046df41  53                       push     ebx
0046df42  51                       push     ecx
0046df43  52                       push     edx
0046df44  56                       push     esi
0046df45  31c0                     xor      eax, eax
0046df47  8b1dac805000             mov      ebx, dword ptr [0x5080ac]
0046df4d  83c014                   add      eax, 0x14
0046df50  8b15a8805000             mov      edx, dword ptr [0x5080a8]
0046df56  8a5c03f2                 mov      bl, byte ptr [ebx + eax - 0xe]
0046df5a  885c02f2                 mov      byte ptr [edx + eax - 0xe], bl
0046df5e  83f850                   cmp      eax, 0x50
0046df61  75e4                     jne      0x46df47
0046df63  31f6                     xor      esi, esi
0046df65  eb0c                     jmp      0x46df73
0046df67  83c614                   add      esi, 0x14
0046df6a  83fe50                   cmp      esi, 0x50
0046df6d  0f8463fbffff             je       0x46dad6
0046df73  89f1                     mov      ecx, esi
0046df75  31c0                     xor      eax, eax
0046df77  8b15ac805000             mov      edx, dword ptr [0x5080ac]
0046df7d  01ca                     add      edx, ecx
0046df7f  8d1c02                   lea      ebx, [edx + eax]
0046df82  8b15a8805000             mov      edx, dword ptr [0x5080a8]
0046df88  83c002                   add      eax, 2
0046df8b  01ca                     add      edx, ecx
0046df8d  668b5b0c                 mov      bx, word ptr [ebx + 0xc]
0046df91  66895c020a               mov      word ptr [edx + eax + 0xa], bx
0046df96  83f808                   cmp      eax, 8
0046df99  74cc                     je       0x46df67
0046df9b  ebda                     jmp      0x46df77
0046df9d  0000                     add      byte ptr [eax], al
