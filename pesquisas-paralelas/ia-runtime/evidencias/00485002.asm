; iagRessReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00485002..0x00485180 (end exclusive); labels are original SBL names
00485002  53                       push ebx
00485003  51                       push ecx
00485004  52                       push edx
00485005  56                       push esi
00485006  57                       push edi
00485007  55                       push ebp
00485008  83ec14                   sub esp, 0x14
0048500b  31d2                     xor edx, edx
0048500d  b83cba5100               mov eax, 0x51ba3c
00485012  89542410                 mov dword ptr [esp + 0x10], edx
00485016  83c028                   add eax, 0x28
00485019  8954240c                 mov dword ptr [esp + 0xc], edx
0048501d  89442408                 mov dword ptr [esp + 8], eax
00485021  eb46                     jmp 0x485069
00485023  ba03000000               mov edx, 3
00485028  8b442410                 mov eax, dword ptr [esp + 0x10]
0048502c  e8a7ebffff               call 0x483bd8 ; -> iaGroupNew
00485031  83f8ff                   cmp eax, -1
00485034  0f8435010000             je 0x48516f
0048503a  c6859d00000000           mov byte ptr [ebp + 0x9d], 0
00485041  c6859c00000000           mov byte ptr [ebp + 0x9c], 0
00485048  8b6c240c                 mov ebp, dword ptr [esp + 0xc]
0048504c  8b442408                 mov eax, dword ptr [esp + 8]
00485050  8b542410                 mov edx, dword ptr [esp + 0x10]
00485054  83c514                   add ebp, 0x14
00485057  05a8000000               add eax, 0xa8
0048505c  42                       inc edx
0048505d  896c240c                 mov dword ptr [esp + 0xc], ebp
00485061  89442408                 mov dword ptr [esp + 8], eax
00485065  89542410                 mov dword ptr [esp + 0x10], edx
00485069  8b4c2410                 mov ecx, dword ptr [esp + 0x10]
0048506d  83f904                   cmp ecx, 4
00485070  0f8d00010000             jge 0x485176
00485076  8b74240c                 mov esi, dword ptr [esp + 0xc]
0048507a  a1a8805000               mov eax, dword ptr [0x5080a8]
0048507f  01f0                     add eax, esi
00485081  8a4001                   mov al, byte ptr [eax + 1]
00485084  25ff000000               and eax, 0xff
00485089  83f802                   cmp eax, 2
0048508c  75ba                     jne 0x485048
0048508e  69f1a8000000             imul esi, ecx, 0xa8
00485094  bd3cba5100               mov ebp, 0x51ba3c
00485099  89c8                     mov eax, ecx
0048509b  01f5                     add ebp, esi
0048509d  8d4c2406                 lea ecx, [esp + 6]
004850a1  25ff000000               and eax, 0xff
004850a6  8d5c2404                 lea ebx, [esp + 4]
004850aa  50                       push eax
004850ab  8d542406                 lea edx, [esp + 6]
004850af  8d442404                 lea eax, [esp + 4]
004850b3  e8b825feff               call 0x467670 ; -> GetRessource
004850b8  31c0                     xor eax, eax
004850ba  668b0424                 mov ax, word ptr [esp]
004850be  89863cba5100             mov dword ptr [esi + 0x51ba3c], eax
004850c4  31c0                     xor eax, eax
004850c6  668b442402               mov ax, word ptr [esp + 2]
004850cb  898640ba5100             mov dword ptr [esi + 0x51ba40], eax
004850d1  31c0                     xor eax, eax
004850d3  668b442404               mov ax, word ptr [esp + 4]
004850d8  898644ba5100             mov dword ptr [esi + 0x51ba44], eax
004850de  89ee                     mov esi, ebp
004850e0  8d7d10                   lea edi, [ebp + 0x10]
004850e3  a5                       movsd dword ptr es:[edi], dword ptr [esi]
004850e4  a5                       movsd dword ptr es:[edi], dword ptr [esi]
004850e5  a5                       movsd dword ptr es:[edi], dword ptr [esi]
004850e6  a5                       movsd dword ptr es:[edi], dword ptr [esi]
004850e7  c7452000000000           mov dword ptr [ebp + 0x20], 0
004850ee  c7452400000000           mov dword ptr [ebp + 0x24], 0
004850f5  8b542408                 mov edx, dword ptr [esp + 8]
004850f9  c7452800000000           mov dword ptr [ebp + 0x28], 0
00485100  89e8                     mov eax, ebp
00485102  c74544ffffffff           mov dword ptr [ebp + 0x44], 0xffffffff
00485109  83c008                   add eax, 8
0048510c  c74050ffffffff           mov dword ptr [eax + 0x50], 0xffffffff
00485113  c7404cffffffff           mov dword ptr [eax + 0x4c], 0xffffffff
0048511a  39d0                     cmp eax, edx
0048511c  75eb                     jne 0x485109
0048511e  c7858400000000000000     mov dword ptr [ebp + 0x84], 0
00485128  c7858800000000000000     mov dword ptr [ebp + 0x88], 0
00485132  c78580000000ffffffff     mov dword ptr [ebp + 0x80], 0xffffffff
0048513c  89e8                     mov eax, ebp
0048513e  c7457cffffffff           mov dword ptr [ebp + 0x7c], 0xffffffff
00485145  8d5510                   lea edx, [ebp + 0x10]
00485148  83c002                   add eax, 2
0048514b  66c7808a000000ffff       mov word ptr [eax + 0x8a], 0xffff
00485154  39d0                     cmp eax, edx
00485156  75f0                     jne 0x485148
00485158  ba07000000               mov edx, 7
0048515d  8b442410                 mov eax, dword ptr [esp + 0x10]
00485161  e872eaffff               call 0x483bd8 ; -> iaGroupNew
00485166  83f8ff                   cmp eax, -1
00485169  0f85b4feffff             jne 0x485023
0048516f  b80f001a1a               mov eax, 0x1a1a000f
00485174  eb02                     jmp 0x485178
00485176  31c0                     xor eax, eax
00485178  83c414                   add esp, 0x14
0048517b  e913050000               jmp 0x485693

; shared Watcom tail reached from iagRessReset; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00485693..0x0048569a (end exclusive); labels are original SBL names
00485693  5d                       pop ebp
00485694  5f                       pop edi
00485695  5e                       pop esi
00485696  5a                       pop edx
00485697  59                       pop ecx
00485698  5b                       pop ebx
00485699  c3                       ret
