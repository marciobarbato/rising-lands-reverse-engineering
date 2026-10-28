; iaGroupNew (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00483bd8..0x00483ce7 (end exclusive); labels are original SBL names
00483bd8  53                       push ebx
00483bd9  51                       push ecx
00483bda  56                       push esi
00483bdb  57                       push edi
00483bdc  55                       push ebp
00483bdd  83ec04                   sub esp, 4
00483be0  89c6                     mov esi, eax
00483be2  891424                   mov dword ptr [esp], edx
00483be5  8b1560b65100             mov edx, dword ptr [0x51b660]
00483beb  89d0                     mov eax, edx
00483bed  b9ffffffff               mov ecx, 0xffffffff
00483bf2  c1e005                   shl eax, 5
00483bf5  eb04                     jmp 0x483bfb
00483bf7  83c020                   add eax, 0x20
00483bfa  42                       inc edx
00483bfb  3d800c0000               cmp eax, 0xc80
00483c00  0f8da5000000             jge 0x483cab
00483c06  31db                     xor ebx, ebx
00483c08  8a98f8a95100             mov bl, byte ptr [eax + 0x51a9f8]
00483c0e  85db                     test ebx, ebx
00483c10  75e5                     jne 0x483bf7
00483c12  bbffffffff               mov ebx, 0xffffffff
00483c17  8998e0a95100             mov dword ptr [eax + 0x51a9e0], ebx
00483c1d  31c9                     xor ecx, ecx
00483c1f  8998e4a95100             mov dword ptr [eax + 0x51a9e4], ebx
00483c25  bfff7f0000               mov edi, 0x7fff
00483c2a  668988f2a95100           mov word ptr [eax + 0x51a9f2], cx
00483c31  bdffffffff               mov ebp, 0xffffffff
00483c36  6689b8f4a95100           mov word ptr [eax + 0x51a9f4], di
00483c3d  89a8e8a95100             mov dword ptr [eax + 0x51a9e8], ebp
00483c43  89a8eca95100             mov dword ptr [eax + 0x51a9ec], ebp
00483c49  66c780f0a95100ffff       mov word ptr [eax + 0x51a9f0], 0xffff
00483c52  c680f8a9510001           mov byte ptr [eax + 0x51a9f8], 1
00483c59  8a1c24                   mov bl, byte ptr [esp]
00483c5c  8898f9a95100             mov byte ptr [eax + 0x51a9f9], bl
00483c62  c680faa95100ff           mov byte ptr [eax + 0x51a9fa], 0xff
00483c69  bbffff0000               mov ebx, 0xffff
00483c6e  31ff                     xor edi, edi
00483c70  668998f6a95100           mov word ptr [eax + 0x51a9f6], bx
00483c77  8b1c24                   mov ebx, dword ptr [esp]
00483c7a  89b8fca95100             mov dword ptr [eax + 0x51a9fc], edi
00483c80  8a1c9dc48e4900           mov bl, byte ptr [ebx*4 + 0x498ec4]
00483c87  8b0d60b65100             mov ecx, dword ptr [0x51b660]
00483c8d  8898fba95100             mov byte ptr [eax + 0x51a9fb], bl
00483c93  83f963                   cmp ecx, 0x63
00483c96  7d0b                     jge 0x483ca3
00483c98  8d6901                   lea ebp, [ecx + 1]
00483c9b  892d60b65100             mov dword ptr [0x51b660], ebp
00483ca1  eb06                     jmp 0x483ca9
00483ca3  893d60b65100             mov dword ptr [0x51b660], edi
00483ca9  89d1                     mov ecx, edx
00483cab  83f9ff                   cmp ecx, -1
00483cae  7507                     jne 0x483cb7
00483cb0  89c8                     mov eax, ecx
00483cb2  e97afdffff               jmp 0x483a31
00483cb7  89f2                     mov edx, esi
00483cb9  c1e202                   shl edx, 2
00483cbc  8b0424                   mov eax, dword ptr [esp]
00483cbf  29f2                     sub edx, esi
00483cc1  c1e002                   shl eax, 2
00483cc4  c1e205                   shl edx, 5
00483cc7  01d0                     add eax, edx
00483cc9  89ca                     mov edx, ecx
00483ccb  8b9864b65100             mov ebx, dword ptr [eax + 0x51b664]
00483cd1  c1e205                   shl edx, 5
00483cd4  898864b65100             mov dword ptr [eax + 0x51b664], ecx
00483cda  89c8                     mov eax, ecx
00483cdc  899ae0a95100             mov dword ptr [edx + 0x51a9e0], ebx
00483ce2  e94afdffff               jmp 0x483a31

; shared Watcom tail reached from iaGroupNew; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00483a31..0x00483a3a (end exclusive); labels are original SBL names
00483a31  83c404                   add esp, 4
00483a34  5d                       pop ebp
00483a35  5f                       pop edi
00483a36  5e                       pop esi
00483a37  59                       pop ecx
00483a38  5b                       pop ebx
00483a39  c3                       ret
