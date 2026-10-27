; AnimDeplaceEngin [0x448088, 0x44812b)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00448088  53                     push     ebx
00448089  51                     push     ecx
0044808a  52                     push     edx
0044808b  31d2                   xor      edx, edx
0044808d  6689c2                 mov      dx, ax
00448090  89d3                   mov      ebx, edx
00448092  c1e304                 shl      ebx, 4
00448095  01d3                   add      ebx, edx
00448097  c1e302                 shl      ebx, 2
0044809a  8d041a                 lea      eax, [edx + ebx]
0044809d  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
004480a3  c1e002                 shl      eax, 2
004480a6  01c3                   add      ebx, eax
004480a8  8a4301                 mov      al, byte ptr [ebx + 1]
004480ab  3c0b                   cmp      al, 0xb
004480ad  0f8274000000           jb       0x448127
004480b3  7616                   jbe      0x4480cb
004480b5  3c12                   cmp      al, 0x12
004480b7  725e                   jb       0x448117
004480b9  7610                   jbe      0x4480cb
004480bb  3c17                   cmp      al, 0x17
004480bd  720c                   jb       0x4480cb
004480bf  3c18                   cmp      al, 0x18
004480c1  7608                   jbe      0x4480cb
004480c3  3c19                   cmp      al, 0x19
004480c5  7404                   je       0x4480cb
004480c7  5a                     pop      edx
004480c8  59                     pop      ecx
004480c9  5b                     pop      ebx
004480ca  c3                     ret      
004480cb  8aa3a9000000           mov      ah, byte ptr [ebx + 0xa9]
004480d1  fec4                   inc      ah
004480d3  8a93a7000000           mov      dl, byte ptr [ebx + 0xa7]
004480d9  88a3a9000000           mov      byte ptr [ebx + 0xa9], ah
004480df  38d4                   cmp      ah, dl
004480e1  75a1                   jne      0x448084
004480e3  31d2                   xor      edx, edx
004480e5  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
004480eb  31c9                   xor      ecx, ecx
004480ed  42                     inc      edx
004480ee  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
004480f4  89d0                   mov      eax, edx
004480f6  c1fa1f                 sar      edx, 0x1f
004480f9  f7f9                   idiv     ecx
004480fb  c683a900000000         mov      byte ptr [ebx + 0xa9], 0
00448102  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00448108  5a                     pop      edx
00448109  59                     pop      ecx
0044810a  5b                     pop      ebx
0044810b  c3                     ret      
0044810c  89d0                   mov      eax, edx
0044810e  e81cfaffff             call     0x447b2f ; AnimBallonStatic
00448113  5a                     pop      edx
00448114  59                     pop      ecx
00448115  5b                     pop      ebx
00448116  c3                     ret      
00448117  3c0e                   cmp      al, 0xe
00448119  72b0                   jb       0x4480cb
0044811b  3c0f                   cmp      al, 0xf
0044811d  76ac                   jbe      0x4480cb
0044811f  3c11                   cmp      al, 0x11
00448121  74e9                   je       0x44810c
00448123  5a                     pop      edx
00448124  59                     pop      ecx
00448125  5b                     pop      ebx
00448126  c3                     ret      
00448127  3c03                   cmp      al, 3
00448129  eba0                   jmp      0x4480cb ; 
