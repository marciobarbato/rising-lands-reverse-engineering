; AnimAttaqueTermineEngin [0x447977, 0x4479c4)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447977  52                     push     edx
00447978  31d2                   xor      edx, edx
0044797a  6689c2                 mov      dx, ax
0044797d  89d0                   mov      eax, edx
0044797f  c1e004                 shl      eax, 4
00447982  01d0                   add      eax, edx
00447984  c1e002                 shl      eax, 2
00447987  01c2                   add      edx, eax
00447989  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
0044798e  c1e202                 shl      edx, 2
00447991  01d0                   add      eax, edx
00447993  8a5001                 mov      dl, byte ptr [eax + 1]
00447996  80fa02                 cmp      dl, 2
00447999  7404                   je       0x44799f
0044799b  30c0                   xor      al, al
0044799d  5a                     pop      edx
0044799e  c3                     ret
0044799f  8a80a4000000           mov      al, byte ptr [eax + 0xa4]
004479a5  25ff000000             and      eax, 0xff
004479aa  83f801                 cmp      eax, 1
004479ad  75ec                   jne      0x44799b
004479af  b001                   mov      al, 1
004479b1  5a                     pop      edx
004479b2  c3                     ret
004479b3  90                     nop
004479b4  1b7a44                 sbb      edi, dword ptr [edx + 0x44]
004479b7  00607a                 add      byte ptr [eax + 0x7a], ah
004479ba  44                     inc      esp
004479bb  00cb                   add      bl, cl
004479bd  7a44                   jp       0x447a03
004479bf  00cb                   add      bl, cl
004479c1  7a44                   jp       0x447a07
