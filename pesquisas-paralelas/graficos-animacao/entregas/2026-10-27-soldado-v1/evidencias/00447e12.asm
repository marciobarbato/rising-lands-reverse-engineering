; AnimConstruireBatiment [0x447e12, 0x447f58)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447e12  53                     push     ebx
00447e13  51                     push     ecx
00447e14  52                     push     edx
00447e15  31d2                   xor      edx, edx
00447e17  6689c2                 mov      dx, ax
00447e1a  89d3                   mov      ebx, edx
00447e1c  c1e304                 shl      ebx, 4
00447e1f  01d3                   add      ebx, edx
00447e21  c1e302                 shl      ebx, 2
00447e24  01d3                   add      ebx, edx
00447e26  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00447e2c  c1e302                 shl      ebx, 2
00447e2f  01d3                   add      ebx, edx
00447e31  8a5301                 mov      dl, byte ptr [ebx + 1]
00447e34  80fa07                 cmp      dl, 7
00447e37  0f82eb000000           jb       0x447f28
00447e3d  7652                   jbe      0x447e91
00447e3f  80fa0e                 cmp      dl, 0xe
00447e42  0f84cd000000           je       0x447f15
00447e48  5a                     pop      edx
00447e49  59                     pop      ecx
00447e4a  5b                     pop      ebx
00447e4b  c3                     ret      
00447e4c  8ab3a9000000           mov      dh, byte ptr [ebx + 0xa9]
00447e52  00d6                   add      dh, dl
00447e54  8a8ba7000000           mov      cl, byte ptr [ebx + 0xa7]
00447e5a  88b3a9000000           mov      byte ptr [ebx + 0xa9], dh
00447e60  38ce                   cmp      dh, cl
00447e62  0f85c5000000           jne      0x447f2d
00447e68  31d2                   xor      edx, edx
00447e6a  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447e70  31c9                   xor      ecx, ecx
00447e72  42                     inc      edx
00447e73  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
00447e79  89d0                   mov      eax, edx
00447e7b  c1fa1f                 sar      edx, 0x1f
00447e7e  f7f9                   idiv     ecx
00447e80  c683a900000000         mov      byte ptr [ebx + 0xa9], 0
00447e87  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00447e8d  5a                     pop      edx
00447e8e  59                     pop      ecx
00447e8f  5b                     pop      ebx
00447e90  c3                     ret      
00447e91  8a9389000000           mov      dl, byte ptr [ebx + 0x89]
00447e97  84d2                   test     dl, dl
00447e99  0f868e000000           jbe      0x447f2d
00447e9f  80fa01                 cmp      dl, 1
00447ea2  74a8                   je       0x447e4c
00447ea4  5a                     pop      edx
00447ea5  59                     pop      ecx
00447ea6  5b                     pop      ebx
00447ea7  c3                     ret      
00447ea8  8aaba9000000           mov      ch, byte ptr [ebx + 0xa9]
00447eae  00d5                   add      ch, dl
00447eb0  8aa3a7000000           mov      ah, byte ptr [ebx + 0xa7]
00447eb6  88aba9000000           mov      byte ptr [ebx + 0xa9], ch
00447ebc  38e5                   cmp      ch, ah
00447ebe  0f8569000000           jne      0x447f2d
00447ec4  31d2                   xor      edx, edx
00447ec6  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447ecc  42                     inc      edx
00447ecd  b904000000             mov      ecx, 4
00447ed2  eba5                   jmp      0x447e79 ; 
00447ed4  8a9389000000           mov      dl, byte ptr [ebx + 0x89]
00447eda  84d2                   test     dl, dl
00447edc  764f                   jbe      0x447f2d
00447ede  80fa01                 cmp      dl, 1
00447ee1  74c5                   je       0x447ea8
00447ee3  5a                     pop      edx
00447ee4  59                     pop      ecx
00447ee5  5b                     pop      ebx
00447ee6  c3                     ret      
00447ee7  8aa3a9000000           mov      ah, byte ptr [ebx + 0xa9]
00447eed  00d4                   add      ah, dl
00447eef  8a93a8000000           mov      dl, byte ptr [ebx + 0xa8]
00447ef5  88a3a9000000           mov      byte ptr [ebx + 0xa9], ah
00447efb  38d4                   cmp      ah, dl
00447efd  752e                   jne      0x447f2d
00447eff  31d2                   xor      edx, edx
00447f01  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447f07  31c9                   xor      ecx, ecx
00447f09  42                     inc      edx
00447f0a  8a8ba6000000           mov      cl, byte ptr [ebx + 0xa6]
00447f10  e964ffffff             jmp      0x447e79 ; 
00447f15  8a9389000000           mov      dl, byte ptr [ebx + 0x89]
00447f1b  84d2                   test     dl, dl
00447f1d  760e                   jbe      0x447f2d
00447f1f  80fa01                 cmp      dl, 1
00447f22  74c3                   je       0x447ee7
00447f24  5a                     pop      edx
00447f25  59                     pop      ecx
00447f26  5b                     pop      ebx
00447f27  c3                     ret      
00447f28  80fa06                 cmp      dl, 6
00447f2b  74a7                   je       0x447ed4
00447f2d  5a                     pop      edx
00447f2e  59                     pop      ecx
00447f2f  5b                     pop      ebx
00447f30  c3                     ret      
00447f31  8d4000                 lea      eax, [eax]
00447f34  84804400987f           test     byte ptr [eax + 0x7f980044], al
00447f3a  44                     inc      esp
00447f3b  00848044008480         add      byte ptr [eax + eax*4 - 0x7f7bffbc], al
00447f42  44                     inc      esp
00447f43  00da                   add      dl, bl
00447f45  7f44                   jg       0x447f8b
00447f47  00848044000c80         add      byte ptr [eax + eax*4 - 0x7ff3ffbc], al
00447f4e  44                     inc      esp
00447f4f  00848044008480         add      byte ptr [eax + eax*4 - 0x7f7bffbc], al
00447f56  44                     inc      esp
