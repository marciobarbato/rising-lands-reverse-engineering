; AffContenanceEngin [0x410a2c, 0x410b40)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00410a2c  51                     push     ecx
00410a2d  56                     push     esi
00410a2e  57                     push     edi
00410a2f  55                     push     ebp
00410a30  83ec0c                 sub      esp, 0xc
00410a33  50                     push     eax
00410a34  89d6                   mov      esi, edx
00410a36  895c2404               mov      dword ptr [esp + 4], ebx
00410a3a  31c0                   xor      eax, eax
00410a3c  6689d8                 mov      ax, bx
00410a3f  e8626a0300             call     0x4474a6 ; EnginGetBag
00410a44  89c5                   mov      ebp, eax
00410a46  668b4002               mov      ax, word ptr [eax + 2]
00410a4a  25ffff0000             and      eax, 0xffff
00410a4f  83f801                 cmp      eax, 1
00410a52  0f84e0000000           je       0x410b38
00410a58  31d2                   xor      edx, edx
00410a5a  89542408               mov      dword ptr [esp + 8], edx
00410a5e  e97d000000             jmp      0x410ae0 ;
00410a63  83f802                 cmp      eax, 2
00410a66  7559                   jne      0x410ac1
00410a68  bb01000000             mov      ebx, 1
00410a6d  89c2                   mov      edx, eax
00410a6f  89e8                   mov      eax, ebp
00410a71  e842670300             call     0x4471b8 ; BagContient
00410a76  bb02000000             mov      ebx, 2
00410a7b  89c7                   mov      edi, eax
00410a7d  89da                   mov      edx, ebx
00410a7f  89e8                   mov      eax, ebp
00410a81  e832670300             call     0x4471b8 ; BagContient
00410a86  01c7                   add      edi, eax
00410a88  897c240c               mov      dword ptr [esp + 0xc], edi
00410a8c  31ff                   xor      edi, edi
00410a8e  eb1d                   jmp      0x410aad ;
00410a90  8b4424fe               mov      eax, dword ptr [esp - 2]
00410a94  b901000000             mov      ecx, 1
00410a99  bb3d2a0000             mov      ebx, 0x2a3d
00410a9e  0fbfd6                 movsx    edx, si
00410aa1  c1f810                 sar      eax, 0x10
00410aa4  47                     inc      edi
00410aa5  e89da70400             call     0x45b247 ; PasteBobCmp
00410aaa  83c608                 add      esi, 8
00410aad  663b7c240c             cmp      di, word ptr [esp + 0xc]
00410ab2  72dc                   jb       0x410a90
00410ab4  8b442408               mov      eax, dword ptr [esp + 8]
00410ab8  4f                     dec      edi
00410ab9  01f8                   add      eax, edi
00410abb  89442408               mov      dword ptr [esp + 8], eax
00410abf  eb1b                   jmp      0x410adc ;
00410ac1  8b4424fe               mov      eax, dword ptr [esp - 2]
00410ac5  b901000000             mov      ecx, 1
00410aca  bb3b2a0000             mov      ebx, 0x2a3b
00410acf  0fbfd6                 movsx    edx, si
00410ad2  c1f810                 sar      eax, 0x10
00410ad5  e86da70400             call     0x45b247 ; PasteBobCmp
00410ada  89fe                   mov      esi, edi
00410adc  ff442408               inc      dword ptr [esp + 8]
00410ae0  8b442408               mov      eax, dword ptr [esp + 8]
00410ae4  663b4502               cmp      ax, word ptr [ebp + 2]
00410ae8  734e                   jae      0x410b38
00410aea  31d2                   xor      edx, edx
00410aec  6689c2                 mov      dx, ax
00410aef  89e8                   mov      eax, ebp
00410af1  e8dd670300             call     0x4472d3 ; BagGetCode
00410af6  89f7                   mov      edi, esi
00410af8  25ff000000             and      eax, 0xff
00410afd  83c708                 add      edi, 8
00410b00  83f801                 cmp      eax, 1
00410b03  0f855affffff           jne      0x410a63
00410b09  31c0                   xor      eax, eax
00410b0b  668b442404             mov      ax, word ptr [esp + 4]
00410b10  e830150300             call     0x442045 ; EnginGetPlayer
00410b15  b901000000             mov      ecx, 1
00410b1a  25ff000000             and      eax, 0xff
00410b1f  bb3c2a0000             mov      ebx, 0x2a3c
00410b24  50                     push     eax
00410b25  8b442402               mov      eax, dword ptr [esp + 2]
00410b29  0fbfd6                 movsx    edx, si
00410b2c  c1f810                 sar      eax, 0x10
00410b2f  89fe                   mov      esi, edi
00410b31  e81fb90400             call     0x45c455 ; PastePlayerCmp
00410b36  eba4                   jmp      0x410adc ;
00410b38  83c410                 add      esp, 0x10
00410b3b  5d                     pop      ebp
00410b3c  5f                     pop      edi
00410b3d  5e                     pop      esi
00410b3e  59                     pop      ecx
00410b3f  c3                     ret
