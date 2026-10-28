; ChercheIndiceEnginCible; [0x004465df, 0x00446693)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004465df  51                       push     ecx
004465e0  56                       push     esi
004465e1  57                       push     edi
004465e2  83ec04                   sub      esp, 4
004465e5  50                       push     eax
004465e6  52                       push     edx
004465e7  bfffff0000               mov      edi, 0xffff
004465ec  31c9                     xor      ecx, ecx
004465ee  84db                     test     bl, bl
004465f0  0f95442408               setne    byte ptr [esp + 8]
004465f5  eb01                     jmp      0x4465f8
004465f7  41                       inc      ecx
004465f8  31c0                     xor      eax, eax
004465fa  6689c8                   mov      ax, cx
004465fd  3d20030000               cmp      eax, 0x320
00446602  0f8d7a000000             jge      0x446682
00446608  663b0c24                 cmp      cx, word ptr [esp]
0044660c  74e9                     je       0x4465f7
0044660e  69c014010000             imul     eax, eax, 0x114
00446614  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0044661a  8a440202                 mov      al, byte ptr [edx + eax + 2]
0044661e  25ff000000               and      eax, 0xff
00446623  7409                     je       0x44662e
00446625  83f804                   cmp      eax, 4
00446628  7404                     je       0x44662e
0044662a  b001                     mov      al, 1
0044662c  eb02                     jmp      0x446630
0044662e  30c0                     xor      al, al
00446630  84c0                     test     al, al
00446632  74c3                     je       0x4465f7
00446634  31c0                     xor      eax, eax
00446636  6689c8                   mov      ax, cx
00446639  69f014010000             imul     esi, eax, 0x114
0044663f  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00446645  8a541e72                 mov      dl, byte ptr [esi + ebx + 0x72]
00446649  84d2                     test     dl, dl
0044664b  74aa                     je       0x4465f7
0044664d  31d2                     xor      edx, edx
0044664f  8a542408                 mov      dl, byte ptr [esp + 8]
00446653  31db                     xor      ebx, ebx
00446655  42                       inc      edx
00446656  88d3                     mov      bl, dl
00446658  31d2                     xor      edx, edx
0044665a  668b542404               mov      dx, word ptr [esp + 4]
0044665f  e80abeffff               call     0x44246e
00446664  84c0                     test     al, al
00446666  748f                     je       0x4465f7
00446668  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0044666d  8a9406ab000000           mov      dl, byte ptr [esi + eax + 0xab]
00446674  89cf                     mov      edi, ecx
00446676  84d2                     test     dl, dl
00446678  0f8479ffffff             je       0x4465f7
0044667e  89c8                     mov      eax, ecx
00446680  eb0a                     jmp      0x44668c
00446682  31c0                     xor      eax, eax
00446684  6689f8                   mov      ax, di
00446687  3dffff0000               cmp      eax, 0xffff
0044668c  83c40c                   add      esp, 0xc
0044668f  5f                       pop      edi
00446690  5e                       pop      esi
00446691  59                       pop      ecx
00446692  c3                       ret
