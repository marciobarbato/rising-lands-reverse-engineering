; LoadPalette [0x4798e9, 0x4799c4)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004798e9  53                     push     ebx
004798ea  51                     push     ecx
004798eb  83ec08                 sub      esp, 8
004798ee  89d3                   mov      ebx, edx
004798f0  ba2f4e4900             mov      edx, 0x494e2f
004798f5  e826ebfdff             call     0x458420 ; FileOpen
004798fa  25ff000000             and      eax, 0xff
004798ff  7507                   jne      0x479908
00479901  30c0                   xor      al, al
00479903  e9b6000000             jmp      0x4799be ;
00479908  ba01000000             mov      edx, 1
0047990d  8d442404               lea      eax, [esp + 4]
00479911  e84bebfdff             call     0x458461 ; FileRead
00479916  31c0                   xor      eax, eax
00479918  8a442404               mov      al, byte ptr [esp + 4]
0047991c  83f850                 cmp      eax, 0x50
0047991f  75e0                   jne      0x479901
00479921  ba01000000             mov      edx, 1
00479926  8d442404               lea      eax, [esp + 4]
0047992a  e832ebfdff             call     0x458461 ; FileRead
0047992f  31c0                   xor      eax, eax
00479931  8a442404               mov      al, byte ptr [esp + 4]
00479935  83f869                 cmp      eax, 0x69
00479938  75c7                   jne      0x479901
0047993a  ba01000000             mov      edx, 1
0047993f  8d442404               lea      eax, [esp + 4]
00479943  e819ebfdff             call     0x458461 ; FileRead
00479948  31c0                   xor      eax, eax
0047994a  8a442404               mov      al, byte ptr [esp + 4]
0047994e  83f865                 cmp      eax, 0x65
00479951  75ae                   jne      0x479901
00479953  ba01000000             mov      edx, 1
00479958  b804000000             mov      eax, 4
0047995d  e829ebfdff             call     0x45848b ; FileSeek
00479962  ba02000000             mov      edx, 2
00479967  89e0                   mov      eax, esp
00479969  e8f3eafdff             call     0x458461 ; FileRead
0047996e  31d2                   xor      edx, edx
00479970  668b1424               mov      dx, word ptr [esp]
00479974  89d0                   mov      eax, edx
00479976  c1e002                 shl      eax, 2
00479979  29d0                   sub      eax, edx
0047997b  89c2                   mov      edx, eax
0047997d  89d8                   mov      eax, ebx
0047997f  e8ddeafdff             call     0x458461 ; FileRead
00479984  e8c3eafdff             call     0x45844c ; FileClose
00479989  31d2                   xor      edx, edx
0047998b  eb1d                   jmp      0x4799aa ;
0047998d  31c0                   xor      eax, eax
0047998f  6689d0                 mov      ax, dx
00479992  8d0440                 lea      eax, [eax + eax*2]
00479995  c0240302               shl      byte ptr [ebx + eax], 2
00479999  c064030102             shl      byte ptr [ebx + eax + 1], 2
0047999e  8a4c0302               mov      cl, byte ptr [ebx + eax + 2]
004799a2  c0e102                 shl      cl, 2
004799a5  42                     inc      edx
004799a6  884c0302               mov      byte ptr [ebx + eax + 2], cl
004799aa  663b1424               cmp      dx, word ptr [esp]
004799ae  72dd                   jb       0x47998d
004799b0  c6430200               mov      byte ptr [ebx + 2], 0
004799b4  8a4302                 mov      al, byte ptr [ebx + 2]
004799b7  884301                 mov      byte ptr [ebx + 1], al
004799ba  8803                   mov      byte ptr [ebx], al
004799bc  b001                   mov      al, 1
004799be  83c408                 add      esp, 8
004799c1  59                     pop      ecx
004799c2  5b                     pop      ebx
004799c3  c3                     ret
