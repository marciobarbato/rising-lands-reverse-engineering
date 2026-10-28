; AnimHelipede [0x447acf, 0x447b2f)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00447acf  53                     push     ebx
00447ad0  51                     push     ecx
00447ad1  52                     push     edx
00447ad2  31d2                   xor      edx, edx
00447ad4  6689c2                 mov      dx, ax
00447ad7  89d3                   mov      ebx, edx
00447ad9  c1e304                 shl      ebx, 4
00447adc  01d3                   add      ebx, edx
00447ade  c1e302                 shl      ebx, 2
00447ae1  01d3                   add      ebx, edx
00447ae3  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00447ae9  c1e302                 shl      ebx, 2
00447aec  01d3                   add      ebx, edx
00447aee  8aa3a9000000           mov      ah, byte ptr [ebx + 0xa9]
00447af4  fec4                   inc      ah
00447af6  8a93a7000000           mov      dl, byte ptr [ebx + 0xa7]
00447afc  88a3a9000000           mov      byte ptr [ebx + 0xa9], ah
00447b02  38d4                   cmp      ah, dl
00447b04  7525                   jne      0x447b2b
00447b06  31d2                   xor      edx, edx
00447b08  8a93a4000000           mov      dl, byte ptr [ebx + 0xa4]
00447b0e  31c9                   xor      ecx, ecx
00447b10  42                     inc      edx
00447b11  8a8ba5000000           mov      cl, byte ptr [ebx + 0xa5]
00447b17  89d0                   mov      eax, edx
00447b19  c1fa1f                 sar      edx, 0x1f
00447b1c  f7f9                   idiv     ecx
00447b1e  c683a900000000         mov      byte ptr [ebx + 0xa9], 0
00447b25  8893a4000000           mov      byte ptr [ebx + 0xa4], dl
00447b2b  5a                     pop      edx
00447b2c  59                     pop      ecx
00447b2d  5b                     pop      ebx
00447b2e  c3                     ret
