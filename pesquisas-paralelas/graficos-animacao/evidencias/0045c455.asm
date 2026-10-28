; PastePlayerCmp [0x45c455, 0x45c72a)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045c455  56                     push     esi
0045c456  57                     push     edi
0045c457  55                     push     ebp
0045c458  83ec1c                 sub      esp, 0x1c
0045c45b  50                     push     eax
0045c45c  52                     push     edx
0045c45d  8b356c8f5000           mov      esi, dword ptr [0x508f6c]
0045c463  81e3ffff0000           and      ebx, 0xffff
0045c469  8b5c9efc               mov      ebx, dword ptr [esi + ebx*4 - 4]
0045c46d  895c2408               mov      dword ptr [esp + 8], ebx
0045c471  84c9                   test     cl, cl
0045c473  742a                   je       0x45c49f
0045c475  668b1522a04900         mov      dx, word ptr [0x49a022]
0045c47c  89542410               mov      dword ptr [esp + 0x10], edx
0045c480  668b1520a04900         mov      dx, word ptr [0x49a020]
0045c487  89542418               mov      dword ptr [esp + 0x18], edx
0045c48b  668b151ea04900         mov      dx, word ptr [0x49a01e]
0045c492  8954240c               mov      dword ptr [esp + 0xc], edx
0045c496  668b151ca04900         mov      dx, word ptr [0x49a01c]
0045c49d  eb20                   jmp      0x45c4bf ;
0045c49f  668b1518a04900         mov      dx, word ptr [0x49a018]
0045c4a6  4a                     dec      edx
0045c4a7  89542410               mov      dword ptr [esp + 0x10], edx
0045c4ab  31d2                   xor      edx, edx
0045c4ad  89542418               mov      dword ptr [esp + 0x18], edx
0045c4b1  668b151aa04900         mov      dx, word ptr [0x49a01a]
0045c4b8  4a                     dec      edx
0045c4b9  8954240c               mov      dword ptr [esp + 0xc], edx
0045c4bd  31d2                   xor      edx, edx
0045c4bf  31c9                   xor      ecx, ecx
0045c4c1  8b5c2402               mov      ebx, dword ptr [esp + 2]
0045c4c5  668b4c2410             mov      cx, word ptr [esp + 0x10]
0045c4ca  c1fb10                 sar      ebx, 0x10
0045c4cd  39cb                   cmp      ebx, ecx
0045c4cf  0f8f4d020000           jg       0x45c722
0045c4d5  31c9                   xor      ecx, ecx
0045c4d7  8b7424fe               mov      esi, dword ptr [esp - 2]
0045c4db  668b4c240c             mov      cx, word ptr [esp + 0xc]
0045c4e0  c1fe10                 sar      esi, 0x10
0045c4e3  39ce                   cmp      esi, ecx
0045c4e5  0f8f37020000           jg       0x45c722
0045c4eb  31c9                   xor      ecx, ecx
0045c4ed  668b4c2418             mov      cx, word ptr [esp + 0x18]
0045c4f2  39cb                   cmp      ebx, ecx
0045c4f4  7d13                   jge      0x45c509
0045c4f6  8b7c2408               mov      edi, dword ptr [esp + 8]
0045c4fa  31f6                   xor      esi, esi
0045c4fc  668b37                 mov      si, word ptr [edi]
0045c4ff  01f3                   add      ebx, esi
0045c501  39cb                   cmp      ebx, ecx
0045c503  0f8c19020000           jl       0x45c722
0045c509  8b4c24fe               mov      ecx, dword ptr [esp - 2]
0045c50d  31db                   xor      ebx, ebx
0045c50f  c1f910                 sar      ecx, 0x10
0045c512  6689d3                 mov      bx, dx
0045c515  39d9                   cmp      ecx, ebx
0045c517  7d14                   jge      0x45c52d
0045c519  8b7c2408               mov      edi, dword ptr [esp + 8]
0045c51d  31f6                   xor      esi, esi
0045c51f  668b7702               mov      si, word ptr [edi + 2]
0045c523  01f1                   add      ecx, esi
0045c525  39d9                   cmp      ecx, ebx
0045c527  0f8cf5010000           jl       0x45c722
0045c52d  8b5c24fe               mov      ebx, dword ptr [esp - 2]
0045c531  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045c537  c1fb10                 sar      ebx, 0x10
0045c53a  0fafcb                 imul     ecx, ebx
0045c53d  8b5c2402               mov      ebx, dword ptr [esp + 2]
0045c541  c1fb10                 sar      ebx, 0x10
0045c544  8b3d708f5000           mov      edi, dword ptr [0x508f70]
0045c54a  01cb                   add      ebx, ecx
0045c54c  8b742408               mov      esi, dword ptr [esp + 8]
0045c550  01df                   add      edi, ebx
0045c552  31db                   xor      ebx, ebx
0045c554  8b7608                 mov      esi, dword ptr [esi + 8]
0045c557  895c2414               mov      dword ptr [esp + 0x14], ebx
0045c55b  31c9                   xor      ecx, ecx
0045c55d  8b5c24fe               mov      ebx, dword ptr [esp - 2]
0045c561  668b4c2414             mov      cx, word ptr [esp + 0x14]
0045c566  c1fb10                 sar      ebx, 0x10
0045c569  01cb                   add      ebx, ecx
0045c56b  31c9                   xor      ecx, ecx
0045c56d  6689d1                 mov      cx, dx
0045c570  39cb                   cmp      ebx, ecx
0045c572  0f8d7f000000           jge      0x45c5f7
0045c578  31c9                   xor      ecx, ecx
0045c57a  668b4c240c             mov      cx, word ptr [esp + 0xc]
0045c57f  39cb                   cmp      ebx, ecx
0045c581  0f8f70000000           jg       0x45c5f7
0045c587  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045c58b  8b5c2414               mov      ebx, dword ptr [esp + 0x14]
0045c58f  663b5902               cmp      bx, word ptr [ecx + 2]
0045c593  7362                   jae      0x45c5f7
0045c595  31db                   xor      ebx, ebx
0045c597  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045c59b  668b01                 mov      ax, word ptr [ecx]
0045c59e  6639c3                 cmp      bx, ax
0045c5a1  731e                   jae      0x45c5c1
0045c5a3  8a06                   mov      al, byte ptr [esi]
0045c5a5  0fbec8                 movsx    ecx, al
0045c5a8  46                     inc      esi
0045c5a9  85c9                   test     ecx, ecx
0045c5ab  7d07                   jge      0x45c5b4
0045c5ad  f6d8                   neg      al
0045c5af  0fbec8                 movsx    ecx, al
0045c5b2  01ce                   add      esi, ecx
0045c5b4  660fbec8               movsx    cx, al
0045c5b8  01cb                   add      ebx, ecx
0045c5ba  0fbec8                 movsx    ecx, al
0045c5bd  01cf                   add      edi, ecx
0045c5bf  ebd6                   jmp      0x45c597 ;
0045c5c1  8b4c2414               mov      ecx, dword ptr [esp + 0x14]
0045c5c5  31db                   xor      ebx, ebx
0045c5c7  41                     inc      ecx
0045c5c8  6689c3                 mov      bx, ax
0045c5cb  894c2414               mov      dword ptr [esp + 0x14], ecx
0045c5cf  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045c5d5  29d9                   sub      ecx, ebx
0045c5d7  01cf                   add      edi, ecx
0045c5d9  eb80                   jmp      0x45c55b ;
0045c5db  8b4c2408               mov      ecx, dword ptr [esp + 8]
0045c5df  31db                   xor      ebx, ebx
0045c5e1  8b442414               mov      eax, dword ptr [esp + 0x14]
0045c5e5  668b19                 mov      bx, word ptr [ecx]
0045c5e8  8b0da0174e00           mov      ecx, dword ptr [0x4e17a0]
0045c5ee  40                     inc      eax
0045c5ef  29d9                   sub      ecx, ebx
0045c5f1  89442414               mov      dword ptr [esp + 0x14], eax
0045c5f5  01cf                   add      edi, ecx
0045c5f7  8b5c2408               mov      ebx, dword ptr [esp + 8]
0045c5fb  8b542414               mov      edx, dword ptr [esp + 0x14]
0045c5ff  663b5302               cmp      dx, word ptr [ebx + 2]
0045c603  0f8319010000           jae      0x45c722
0045c609  31db                   xor      ebx, ebx
0045c60b  8b4c24fe               mov      ecx, dword ptr [esp - 2]
0045c60f  6689d3                 mov      bx, dx
0045c612  c1f910                 sar      ecx, 0x10
0045c615  01cb                   add      ebx, ecx
0045c617  31c9                   xor      ecx, ecx
0045c619  668b4c240c             mov      cx, word ptr [esp + 0xc]
0045c61e  39cb                   cmp      ebx, ecx
0045c620  0f8ffc000000           jg       0x45c722
0045c626  31d2                   xor      edx, edx
0045c628  8954241c               mov      dword ptr [esp + 0x1c], edx
0045c62c  8b5c2408               mov      ebx, dword ptr [esp + 8]
0045c630  8b54241c               mov      edx, dword ptr [esp + 0x1c]
0045c634  663b13                 cmp      dx, word ptr [ebx]
0045c637  73a2                   jae      0x45c5db
0045c639  8a06                   mov      al, byte ptr [esi]
0045c63b  88442420               mov      byte ptr [esp + 0x20], al
0045c63f  8b5c241d               mov      ebx, dword ptr [esp + 0x1d]
0045c643  c1fb18                 sar      ebx, 0x18
0045c646  46                     inc      esi
0045c647  85db                   test     ebx, ebx
0045c649  0f8dc6000000           jge      0x45c715
0045c64f  31c9                   xor      ecx, ecx
0045c651  8b5c2402               mov      ebx, dword ptr [esp + 2]
0045c655  6689d1                 mov      cx, dx
0045c658  c1fb10                 sar      ebx, 0x10
0045c65b  88c4                   mov      ah, al
0045c65d  01cb                   add      ebx, ecx
0045c65f  31c9                   xor      ecx, ecx
0045c661  f6dc                   neg      ah
0045c663  668b4c2418             mov      cx, word ptr [esp + 0x18]
0045c668  88642420               mov      byte ptr [esp + 0x20], ah
0045c66c  39cb                   cmp      ebx, ecx
0045c66e  7c44                   jl       0x45c6b4
0045c670  8b6c241d               mov      ebp, dword ptr [esp + 0x1d]
0045c674  c1fd18                 sar      ebp, 0x18
0045c677  8d0c2b                 lea      ecx, [ebx + ebp]
0045c67a  31db                   xor      ebx, ebx
0045c67c  668b5c2410             mov      bx, word ptr [esp + 0x10]
0045c681  39d9                   cmp      ecx, ebx
0045c683  7f2f                   jg       0x45c6b4
0045c685  8b5c241d               mov      ebx, dword ptr [esp + 0x1d]
0045c689  89f2                   mov      edx, esi
0045c68b  31c9                   xor      ecx, ecx
0045c68d  89f8                   mov      eax, edi
0045c68f  8a4c2434               mov      cl, byte ptr [esp + 0x34]
0045c693  c1fb18                 sar      ebx, 0x18
0045c696  e8b5310000             call     0x45f850 ; MemPlayerCopy
0045c69b  660fbe5c2420           movsx    bx, byte ptr [esp + 0x20]
0045c6a1  8b4c241c               mov      ecx, dword ptr [esp + 0x1c]
0045c6a5  01ee                   add      esi, ebp
0045c6a7  01d9                   add      ecx, ebx
0045c6a9  01ef                   add      edi, ebp
0045c6ab  894c241c               mov      dword ptr [esp + 0x1c], ecx
0045c6af  e978ffffff             jmp      0x45c62c ;
0045c6b4  0fb66c2434             movzx    ebp, byte ptr [esp + 0x34]
0045c6b9  30c0                   xor      al, al
0045c6bb  eb0d                   jmp      0x45c6ca ;
0045c6bd  8b54241c               mov      edx, dword ptr [esp + 0x1c]
0045c6c1  47                     inc      edi
0045c6c2  46                     inc      esi
0045c6c3  42                     inc      edx
0045c6c4  fec0                   inc      al
0045c6c6  8954241c               mov      dword ptr [esp + 0x1c], edx
0045c6ca  31c9                   xor      ecx, ecx
0045c6cc  8b5c241d               mov      ebx, dword ptr [esp + 0x1d]
0045c6d0  88c1                   mov      cl, al
0045c6d2  c1fb18                 sar      ebx, 0x18
0045c6d5  39d9                   cmp      ecx, ebx
0045c6d7  0f8d4fffffff           jge      0x45c62c
0045c6dd  31db                   xor      ebx, ebx
0045c6df  8b4c2402               mov      ecx, dword ptr [esp + 2]
0045c6e3  668b5c241c             mov      bx, word ptr [esp + 0x1c]
0045c6e8  c1f910                 sar      ecx, 0x10
0045c6eb  01cb                   add      ebx, ecx
0045c6ed  31c9                   xor      ecx, ecx
0045c6ef  668b4c2418             mov      cx, word ptr [esp + 0x18]
0045c6f4  39cb                   cmp      ebx, ecx
0045c6f6  7cc5                   jl       0x45c6bd
0045c6f8  31c9                   xor      ecx, ecx
0045c6fa  668b4c2410             mov      cx, word ptr [esp + 0x10]
0045c6ff  39cb                   cmp      ebx, ecx
0045c701  7fba                   jg       0x45c6bd
0045c703  31c9                   xor      ecx, ecx
0045c705  8b1cadc8244e00         mov      ebx, dword ptr [ebp*4 + 0x4e24c8]
0045c70c  8a0e                   mov      cl, byte ptr [esi]
0045c70e  8a1c19                 mov      bl, byte ptr [ecx + ebx]
0045c711  881f                   mov      byte ptr [edi], bl
0045c713  eba8                   jmp      0x45c6bd ;
0045c715  660fbec8               movsx    cx, al
0045c719  01ca                   add      edx, ecx
0045c71b  01df                   add      edi, ebx
0045c71d  e906ffffff             jmp      0x45c628 ;
0045c722  83c424                 add      esp, 0x24
0045c725  e961060000             jmp      0x45cd8b ;
