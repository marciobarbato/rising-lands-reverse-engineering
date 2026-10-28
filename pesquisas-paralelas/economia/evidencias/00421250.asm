; ApprentissageSortTerminer: limite por próximo símbolo SBL, fim exclusivo 0x004212f5.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00421250  53                       push     ebx
00421251  52                       push     edx
00421252  25ffff0000               and      eax, 0xffff
00421257  89c3                     mov      ebx, eax
00421259  c1e304                   shl      ebx, 4
0042125c  01c3                     add      ebx, eax
0042125e  c1e302                   shl      ebx, 2
00421261  01c3                     add      ebx, eax
00421263  c1e302                   shl      ebx, 2
00421266  81c3c8a04900             add      ebx, 0x49a0c8
0042126c  31d2                     xor      edx, edx
0042126e  31c0                     xor      eax, eax
00421270  8a537b                   mov      dl, byte ptr [ebx + 0x7b]
00421273  8a4304                   mov      al, byte ptr [ebx + 4]
00421276  e8f9360500               call     0x474974
0042127b  31c0                     xor      eax, eax
0042127d  8a4304                   mov      al, byte ptr [ebx + 4]
00421280  31d2                     xor      edx, edx
00421282  e8b1370500               call     0x474a38
00421287  8a4308                   mov      al, byte ptr [ebx + 8]
0042128a  88c2                     mov      dl, al
0042128c  8a4304                   mov      al, byte ptr [ebx + 4]
0042128f  25ff000000               and      eax, 0xff
00421294  e8d3b4ffff               call     0x41c76c
00421299  66c74378ffff             mov      word ptr [ebx + 0x78], 0xffff
0042129f  c6437bff                 mov      byte ptr [ebx + 0x7b], 0xff
004212a3  66c7437c0000             mov      word ptr [ebx + 0x7c], 0
004212a9  66c7437e0000             mov      word ptr [ebx + 0x7e], 0
004212af  31d2                     xor      edx, edx
004212b1  89d8                     mov      eax, ebx
004212b3  8a5308                   mov      dl, byte ptr [ebx + 8]
004212b6  66c78386000000ffff       mov      word ptr [ebx + 0x86], 0xffff
004212bf  83fa14                   cmp      edx, 0x14
004212c2  7412                     je       0x4212d6
004212c4  66c783800000000000       mov      word ptr [ebx + 0x80], 0
004212cd  66c783820000000000       mov      word ptr [ebx + 0x82], 0
004212d6  c6407400                 mov      byte ptr [eax + 0x74], 0
004212da  31d2                     xor      edx, edx
004212dc  8a5005                   mov      dl, byte ptr [eax + 5]
004212df  c7808c00000000000000     mov      dword ptr [eax + 0x8c], 0
004212e9  83fa03                   cmp      edx, 3
004212ec  7404                     je       0x4212f2
004212ee  c6400505                 mov      byte ptr [eax + 5], 5
004212f2  5a                       pop      edx
004212f3  5b                       pop      ebx
004212f4  c3                       ret
