; BatimentInitCave: Counts type 3 (CAVE) into warehouse word 0x4dfb2c; exclusive end 0x004191c9.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419112  53                       push     ebx
00419113  51                       push     ecx
00419114  52                       push     edx
00419115  56                       push     esi
00419116  57                       push     edi
00419117  bfc8a04900               mov      edi, 0x49a0c8
0041911c  30ff                     xor      bh, bh
0041911e  eb27                     jmp      0x419147
00419120  31c9                     xor      ecx, ecx
00419122  88f9                     mov      cl, bh
00419124  6bc116                   imul     eax, ecx, 0x16
00419127  6bd106                   imul     edx, ecx, 6
0041912a  660fb6b073a04900         movzx    si, byte ptr [eax + 0x49a073]
00419132  8a8082a04900             mov      al, byte ptr [eax + 0x49a082]
00419138  fec7                     inc      bh
0041913a  88814cfb4d00             mov      byte ptr [ecx + 0x4dfb4c], al
00419140  6689b22cfb4d00           mov      word ptr [edx + 0x4dfb2c], si
00419147  31c0                     xor      eax, eax
00419149  88f8                     mov      al, bh
0041914b  83f804                   cmp      eax, 4
0041914e  0f8dca490000             jge      0x41db1e
00419154  88fb                     mov      bl, bh
00419156  31d2                     xor      edx, edx
00419158  eb10                     jmp      0x41916a
0041915a  31c9                     xor      ecx, ecx
0041915c  88d9                     mov      cl, bl
0041915e  6bc916                   imul     ecx, ecx, 0x16
00419161  42                       inc      edx
00419162  c6840170a0490000         mov      byte ptr [ecx + eax + 0x49a070], 0
0041916a  31c0                     xor      eax, eax
0041916c  6689d0                   mov      ax, dx
0041916f  83f816                   cmp      eax, 0x16
00419172  7ce6                     jl       0x41915a
00419174  31d2                     xor      edx, edx
00419176  eb01                     jmp      0x419179
00419178  42                       inc      edx
00419179  31c0                     xor      eax, eax
0041917b  6689d0                   mov      ax, dx
0041917e  3de8030000               cmp      eax, 0x3e8
00419183  7d9b                     jge      0x419120
00419185  69c014010000             imul     eax, eax, 0x114
0041918b  8a440705                 mov      al, byte ptr [edi + eax + 5]
0041918f  25ff000000               and      eax, 0xff
00419194  0f95c0                   setne    al
00419197  84c0                     test     al, al
00419199  74dd                     je       0x419178
0041919b  31c0                     xor      eax, eax
0041919d  6689d0                   mov      ax, dx
004191a0  69c014010000             imul     eax, eax, 0x114
004191a6  01f8                     add      eax, edi
004191a8  8a4804                   mov      cl, byte ptr [eax + 4]
004191ab  38d9                     cmp      cl, bl
004191ad  75c9                     jne      0x419178
004191af  31c9                     xor      ecx, ecx
004191b1  88d9                     mov      cl, bl
004191b3  6bc916                   imul     ecx, ecx, 0x16
004191b6  8a4008                   mov      al, byte ptr [eax + 8]
004191b9  8d8970a04900             lea      ecx, [ecx + 0x49a070]
004191bf  25ff000000               and      eax, 0xff
004191c4  fe0401                   inc      byte ptr [ecx + eax]
004191c7  ebaf                     jmp      0x419178
