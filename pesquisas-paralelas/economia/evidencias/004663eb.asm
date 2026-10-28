; VideMatiere: limite por próximo símbolo SBL, fim exclusivo 0x00466533.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004663eb  53                       push     ebx
004663ec  51                       push     ecx
004663ed  56                       push     esi
004663ee  57                       push     edi
004663ef  83ec10                   sub      esp, 0x10
004663f2  88442404                 mov      byte ptr [esp + 4], al
004663f6  8854240c                 mov      byte ptr [esp + 0xc], dl
004663fa  30e4                     xor      ah, ah
004663fc  88642408                 mov      byte ptr [esp + 8], ah
00466400  eb53                     jmp      0x466455
00466402  31db                     xor      ebx, ebx
00466404  8a5c2404                 mov      bl, byte ptr [esp + 4]
00466408  6bdb06                   imul     ebx, ebx, 6
0046640b  31c0                     xor      eax, eax
0046640d  31d2                     xor      edx, edx
0046640f  8a44240c                 mov      al, byte ptr [esp + 0xc]
00466413  8a542408                 mov      dl, byte ptr [esp + 8]
00466417  c1e002                   shl      eax, 2
0046641a  01d0                     add      eax, edx
0046641c  01d2                     add      edx, edx
0046641e  01d3                     add      ebx, edx
00466420  668b0cc5aa2e4e00         mov      cx, word ptr [eax*8 + 0x4e2eaa]
00466428  668b93fc2c4e00           mov      dx, word ptr [ebx + 0x4e2cfc]
0046642f  668b34c5a82e4e00         mov      si, word ptr [eax*8 + 0x4e2ea8]
00466437  01d1                     add      ecx, edx
00466439  01d6                     add      esi, edx
0046643b  8a742408                 mov      dh, byte ptr [esp + 8]
0046643f  66890cc5aa2e4e00         mov      word ptr [eax*8 + 0x4e2eaa], cx
00466447  fec6                     inc      dh
00466449  668934c5a82e4e00         mov      word ptr [eax*8 + 0x4e2ea8], si
00466451  88742408                 mov      byte ptr [esp + 8], dh
00466455  31c9                     xor      ecx, ecx
00466457  8a4c2408                 mov      cl, byte ptr [esp + 8]
0046645b  83f903                   cmp      ecx, 3
0046645e  7d34                     jge      0x466494
00466460  31db                     xor      ebx, ebx
00466462  8a5c2404                 mov      bl, byte ptr [esp + 4]
00466466  89d8                     mov      eax, ebx
00466468  e8aa730000               call     0x46d817
0046646d  25ff000000               and      eax, 0xff
00466472  83f801                   cmp      eax, 1
00466475  758b                     jne      0x466402
00466477  6bd306                   imul     edx, ebx, 6
0046647a  89c8                     mov      eax, ecx
0046647c  668b9442fc2c4e00         mov      dx, word ptr [edx + eax*2 + 0x4e2cfc]
00466484  81e2ffff0000             and      edx, 0xffff
0046648a  e82ed1fbff               call     0x4235bd
0046648f  e96effffff               jmp      0x466402
00466494  30d2                     xor      dl, dl
00466496  881424                   mov      byte ptr [esp], dl
00466499  eb4c                     jmp      0x4664e7
0046649b  31d2                     xor      edx, edx
0046649d  8a542404                 mov      dl, byte ptr [esp + 4]
004664a1  89d0                     mov      eax, edx
004664a3  6bd206                   imul     edx, edx, 6
004664a6  31db                     xor      ebx, ebx
004664a8  8a1c24                   mov      bl, byte ptr [esp]
004664ab  c1e002                   shl      eax, 2
004664ae  01d8                     add      eax, ebx
004664b0  01db                     add      ebx, ebx
004664b2  01d3                     add      ebx, edx
004664b4  668b93142d4e00           mov      dx, word ptr [ebx + 0x4e2d14]
004664bb  668b1cc5a82e4e00         mov      bx, word ptr [eax*8 + 0x4e2ea8]
004664c3  01d3                     add      ebx, edx
004664c5  668b3cc5aa2e4e00         mov      di, word ptr [eax*8 + 0x4e2eaa]
004664cd  66891cc5a82e4e00         mov      word ptr [eax*8 + 0x4e2ea8], bx
004664d5  8a1c24                   mov      bl, byte ptr [esp]
004664d8  01d7                     add      edi, edx
004664da  fec3                     inc      bl
004664dc  66893cc5aa2e4e00         mov      word ptr [eax*8 + 0x4e2eaa], di
004664e4  881c24                   mov      byte ptr [esp], bl
004664e7  31c9                     xor      ecx, ecx
004664e9  8a0c24                   mov      cl, byte ptr [esp]
004664ec  83f903                   cmp      ecx, 3
004664ef  7d3a                     jge      0x46652b
004664f1  31db                     xor      ebx, ebx
004664f3  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
004664f7  89d8                     mov      eax, ebx
004664f9  e819730000               call     0x46d817
004664fe  25ff000000               and      eax, 0xff
00466503  83f801                   cmp      eax, 1
00466506  7593                     jne      0x46649b
00466508  31d2                     xor      edx, edx
0046650a  8a542404                 mov      dl, byte ptr [esp + 4]
0046650e  6bd206                   imul     edx, edx, 6
00466511  8d0409                   lea      eax, [ecx + ecx]
00466514  01d0                     add      eax, edx
00466516  31d2                     xor      edx, edx
00466518  668b90142d4e00           mov      dx, word ptr [eax + 0x4e2d14]
0046651f  89c8                     mov      eax, ecx
00466521  e897d0fbff               call     0x4235bd
00466526  e970ffffff               jmp      0x46649b
0046652b  83c410                   add      esp, 0x10
0046652e  5f                       pop      edi
0046652f  5e                       pop      esi
00466530  59                       pop      ecx
00466531  5b                       pop      ebx
00466532  c3                       ret
