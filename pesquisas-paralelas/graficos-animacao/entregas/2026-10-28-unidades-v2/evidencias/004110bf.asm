; AffOmbreEngin [0x4110bf, 0x411147)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004110bf  56                     push     esi
004110c0  57                     push     edi
004110c1  55                     push     ebp
004110c2  83ec04                 sub      esp, 4
004110c5  50                     push     eax
004110c6  31c0                   xor      eax, eax
004110c8  6689c8                 mov      ax, cx
004110cb  e8750f0300             call     0x442045 ; EnginGetPlayer
004110d0  0fb6f0                 movzx    esi, al
004110d3  88442404               mov      byte ptr [esp + 4], al
004110d7  85f6                   test     esi, esi
004110d9  740d                   je       0x4110e8
004110db  81fec8000000           cmp      esi, 0xc8
004110e1  7405                   je       0x4110e8
004110e3  83fe04                 cmp      esi, 4
004110e6  753e                   jne      0x411126
004110e8  8b6c24fe               mov      ebp, dword ptr [esp - 2]
004110ec  b901000000             mov      ecx, 1
004110f1  31ff                   xor      edi, edi
004110f3  0fbff2                 movsx    esi, dx
004110f6  6689df                 mov      di, bx
004110f9  c1fd10                 sar      ebp, 0x10
004110fc  89f2                   mov      edx, esi
004110fe  89fb                   mov      ebx, edi
00411100  89e8                   mov      eax, ebp
00411102  e88fa60400             call     0x45b796 ; PasteOmbreCmp
00411107  31c0                   xor      eax, eax
00411109  8a442404               mov      al, byte ptr [esp + 4]
0041110d  3dc8000000             cmp      eax, 0xc8
00411112  752c                   jne      0x411140
00411114  b901000000             mov      ecx, 1
00411119  89fb                   mov      ebx, edi
0041111b  89f2                   mov      edx, esi
0041111d  89e8                   mov      eax, ebp
0041111f  e88cab0400             call     0x45bcb0 ; PasteGrisCmp
00411124  eb1a                   jmp      0x411140 ;
00411126  8b4424fe               mov      eax, dword ptr [esp - 2]
0041112a  b901000000             mov      ecx, 1
0041112f  81e3ffff0000           and      ebx, 0xffff
00411135  0fbfd2                 movsx    edx, dx
00411138  c1f810                 sar      eax, 0x10
0041113b  e856a60400             call     0x45b796 ; PasteOmbreCmp
00411140  83c408                 add      esp, 8
00411143  5d                     pop      ebp
00411144  5f                     pop      edi
00411145  5e                     pop      esi
00411146  c3                     ret
