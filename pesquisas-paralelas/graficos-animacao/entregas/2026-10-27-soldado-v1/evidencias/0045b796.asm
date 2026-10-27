; PasteOmbreCmp [0x45b796, 0x45ba23)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045b796  56                     push     esi
0045b797  57                     push     edi
0045b798  55                     push     ebp
0045b799  83ec1c                 sub      esp, 0x1c
0045b79c  50                     push     eax
0045b79d  52                     push     edx
0045b79e  31c0                   xor      eax, eax
0045b7a0  8b2d6c8f5000           mov      ebp, dword ptr [0x508f6c]
0045b7a6  6689d8                 mov      ax, bx
0045b7a9  8b6c85fc               mov      ebp, dword ptr [ebp + eax*4 - 4]
0045b7ad  84c9                   test     cl, cl
0045b7af  742a                   je       0x45b7db
0045b7b1  66a122a04900           mov      ax, word ptr [0x49a022]
0045b7b7  8944240c               mov      dword ptr [esp + 0xc], eax
0045b7bb  66a120a04900           mov      ax, word ptr [0x49a020]
0045b7c1  8944241c               mov      dword ptr [esp + 0x1c], eax
0045b7c5  66a11ea04900           mov      ax, word ptr [0x49a01e]
0045b7cb  89442414               mov      dword ptr [esp + 0x14], eax
0045b7cf  66a11ca04900           mov      ax, word ptr [0x49a01c]
0045b7d5  89442418               mov      dword ptr [esp + 0x18], eax
0045b7d9  eb20                   jmp      0x45b7fb ; 
0045b7db  66a118a04900           mov      ax, word ptr [0x49a018]
0045b7e1  48                     dec      eax
0045b7e2  31d2                   xor      edx, edx
0045b7e4  8944240c               mov      dword ptr [esp + 0xc], eax
0045b7e8  66a11aa04900           mov      ax, word ptr [0x49a01a]
0045b7ee  8954241c               mov      dword ptr [esp + 0x1c], edx
0045b7f2  48                     dec      eax
0045b7f3  89542418               mov      dword ptr [esp + 0x18], edx
0045b7f7  89442414               mov      dword ptr [esp + 0x14], eax
0045b7fb  31d2                   xor      edx, edx
0045b7fd  8b442402               mov      eax, dword ptr [esp + 2]
0045b801  668b54240c             mov      dx, word ptr [esp + 0xc]
0045b806  c1f810                 sar      eax, 0x10
0045b809  39d0                   cmp      eax, edx
0045b80b  0f8fe5fcffff           jg       0x45b4f6
0045b811  31d2                   xor      edx, edx
0045b813  8b5c24fe               mov      ebx, dword ptr [esp - 2]
0045b817  668b542414             mov      dx, word ptr [esp + 0x14]
0045b81c  c1fb10                 sar      ebx, 0x10
0045b81f  39d3                   cmp      ebx, edx
0045b821  0f8fcffcffff           jg       0x45b4f6
0045b827  31d2                   xor      edx, edx
0045b829  668b54241c             mov      dx, word ptr [esp + 0x1c]
0045b82e  39d0                   cmp      eax, edx
0045b830  7d10                   jge      0x45b842
0045b832  31db                   xor      ebx, ebx
0045b834  668b5d00               mov      bx, word ptr [ebp]
0045b838  01d8                   add      eax, ebx
0045b83a  39d0                   cmp      eax, edx
0045b83c  0f8cb4fcffff           jl       0x45b4f6
0045b842  31d2                   xor      edx, edx
0045b844  8b4424fe               mov      eax, dword ptr [esp - 2]
0045b848  668b542418             mov      dx, word ptr [esp + 0x18]
0045b84d  c1f810                 sar      eax, 0x10
0045b850  39d0                   cmp      eax, edx
0045b852  7d10                   jge      0x45b864
0045b854  31db                   xor      ebx, ebx
0045b856  668b5d02               mov      bx, word ptr [ebp + 2]
0045b85a  01d8                   add      eax, ebx
0045b85c  39d0                   cmp      eax, edx
0045b85e  0f8c92fcffff           jl       0x45b4f6
0045b864  8b4424fe               mov      eax, dword ptr [esp - 2]
0045b868  8b15a0174e00           mov      edx, dword ptr [0x4e17a0]
0045b86e  c1f810                 sar      eax, 0x10
0045b871  0fafd0                 imul     edx, eax
0045b874  8b1d708f5000           mov      ebx, dword ptr [0x508f70]
0045b87a  8b442402               mov      eax, dword ptr [esp + 2]
0045b87e  8b7508                 mov      esi, dword ptr [ebp + 8]
0045b881  c1f810                 sar      eax, 0x10
0045b884  31c9                   xor      ecx, ecx
0045b886  01d0                   add      eax, edx
0045b888  894c2410               mov      dword ptr [esp + 0x10], ecx
0045b88c  01c3                   add      ebx, eax
0045b88e  31c0                   xor      eax, eax
0045b890  8b5424fe               mov      edx, dword ptr [esp - 2]
0045b894  668b442410             mov      ax, word ptr [esp + 0x10]
0045b899  c1fa10                 sar      edx, 0x10
0045b89c  01d0                   add      eax, edx
0045b89e  31d2                   xor      edx, edx
0045b8a0  668b542418             mov      dx, word ptr [esp + 0x18]
0045b8a5  39d0                   cmp      eax, edx
0045b8a7  0f8d6e000000           jge      0x45b91b
0045b8ad  31d2                   xor      edx, edx
0045b8af  668b542414             mov      dx, word ptr [esp + 0x14]
0045b8b4  39d0                   cmp      eax, edx
0045b8b6  7f63                   jg       0x45b91b
0045b8b8  8b442410               mov      eax, dword ptr [esp + 0x10]
0045b8bc  663b4502               cmp      ax, word ptr [ebp + 2]
0045b8c0  7359                   jae      0x45b91b
0045b8c2  31d2                   xor      edx, edx
0045b8c4  663b5500               cmp      dx, word ptr [ebp]
0045b8c8  731e                   jae      0x45b8e8
0045b8ca  8a06                   mov      al, byte ptr [esi]
0045b8cc  0fbef8                 movsx    edi, al
0045b8cf  46                     inc      esi
0045b8d0  85ff                   test     edi, edi
0045b8d2  7d07                   jge      0x45b8db
0045b8d4  f6d8                   neg      al
0045b8d6  0fbef8                 movsx    edi, al
0045b8d9  01fe                   add      esi, edi
0045b8db  660fbec8               movsx    cx, al
0045b8df  0fbec0                 movsx    eax, al
0045b8e2  01ca                   add      edx, ecx
0045b8e4  01c3                   add      ebx, eax
0045b8e6  ebdc                   jmp      0x45b8c4 ; 
0045b8e8  8b542410               mov      edx, dword ptr [esp + 0x10]
0045b8ec  31c0                   xor      eax, eax
0045b8ee  42                     inc      edx
0045b8ef  668b4500               mov      ax, word ptr [ebp]
0045b8f3  89542410               mov      dword ptr [esp + 0x10], edx
0045b8f7  8b15a0174e00           mov      edx, dword ptr [0x4e17a0]
0045b8fd  29c2                   sub      edx, eax
0045b8ff  01d3                   add      ebx, edx
0045b901  eb8b                   jmp      0x45b88e ; 
0045b903  31c0                   xor      eax, eax
0045b905  8b15a0174e00           mov      edx, dword ptr [0x4e17a0]
0045b90b  6689f8                 mov      ax, di
0045b90e  29c2                   sub      edx, eax
0045b910  8b442410               mov      eax, dword ptr [esp + 0x10]
0045b914  40                     inc      eax
0045b915  01d3                   add      ebx, edx
0045b917  89442410               mov      dword ptr [esp + 0x10], eax
0045b91b  8b442410               mov      eax, dword ptr [esp + 0x10]
0045b91f  663b4502               cmp      ax, word ptr [ebp + 2]
0045b923  0f83cdfbffff           jae      0x45b4f6
0045b929  31d2                   xor      edx, edx
0045b92b  6689c2                 mov      dx, ax
0045b92e  8b4424fe               mov      eax, dword ptr [esp - 2]
0045b932  c1f810                 sar      eax, 0x10
0045b935  01c2                   add      edx, eax
0045b937  31c0                   xor      eax, eax
0045b939  668b442414             mov      ax, word ptr [esp + 0x14]
0045b93e  39c2                   cmp      edx, eax
0045b940  0f8fb0fbffff           jg       0x45b4f6
0045b946  31c9                   xor      ecx, ecx
0045b948  668b7d00               mov      di, word ptr [ebp]
0045b94c  6639f9                 cmp      cx, di
0045b94f  73b2                   jae      0x45b903
0045b951  8a06                   mov      al, byte ptr [esi]
0045b953  88442420               mov      byte ptr [esp + 0x20], al
0045b957  8b44241d               mov      eax, dword ptr [esp + 0x1d]
0045b95b  c1f818                 sar      eax, 0x18
0045b95e  46                     inc      esi
0045b95f  85c0                   test     eax, eax
0045b961  0f8dad000000           jge      0x45ba14
0045b967  8a642420               mov      ah, byte ptr [esp + 0x20]
0045b96b  f6dc                   neg      ah
0045b96d  8b542402               mov      edx, dword ptr [esp + 2]
0045b971  88642420               mov      byte ptr [esp + 0x20], ah
0045b975  31c0                   xor      eax, eax
0045b977  c1fa10                 sar      edx, 0x10
0045b97a  6689c8                 mov      ax, cx
0045b97d  01d0                   add      eax, edx
0045b97f  31d2                   xor      edx, edx
0045b981  668b54241c             mov      dx, word ptr [esp + 0x1c]
0045b986  39d0                   cmp      eax, edx
0045b988  7c38                   jl       0x45b9c2
0045b98a  8b7c241d               mov      edi, dword ptr [esp + 0x1d]
0045b98e  c1ff18                 sar      edi, 0x18
0045b991  01f8                   add      eax, edi
0045b993  89442408               mov      dword ptr [esp + 8], eax
0045b997  31c0                   xor      eax, eax
0045b999  8b542408               mov      edx, dword ptr [esp + 8]
0045b99d  668b44240c             mov      ax, word ptr [esp + 0xc]
0045b9a2  39d0                   cmp      eax, edx
0045b9a4  7c1c                   jl       0x45b9c2
0045b9a6  8b54241d               mov      edx, dword ptr [esp + 0x1d]
0045b9aa  89d8                   mov      eax, ebx
0045b9ac  c1fa18                 sar      edx, 0x18
0045b9af  01fe                   add      esi, edi
0045b9b1  e8043e0000             call     0x45f7ba ; MemOmbreCopy
0045b9b6  660fbe442420           movsx    ax, byte ptr [esp + 0x20]
0045b9bc  01fb                   add      ebx, edi
0045b9be  01c1                   add      ecx, eax
0045b9c0  eb86                   jmp      0x45b948 ; 
0045b9c2  30c0                   xor      al, al
0045b9c4  eb05                   jmp      0x45b9cb ; 
0045b9c6  41                     inc      ecx
0045b9c7  43                     inc      ebx
0045b9c8  46                     inc      esi
0045b9c9  fec0                   inc      al
0045b9cb  8b7c241d               mov      edi, dword ptr [esp + 0x1d]
0045b9cf  31d2                   xor      edx, edx
0045b9d1  c1ff18                 sar      edi, 0x18
0045b9d4  88c2                   mov      dl, al
0045b9d6  39fa                   cmp      edx, edi
0045b9d8  0f8d6affffff           jge      0x45b948
0045b9de  8b7c2402               mov      edi, dword ptr [esp + 2]
0045b9e2  31d2                   xor      edx, edx
0045b9e4  c1ff10                 sar      edi, 0x10
0045b9e7  6689ca                 mov      dx, cx
0045b9ea  01fa                   add      edx, edi
0045b9ec  31ff                   xor      edi, edi
0045b9ee  668b7c241c             mov      di, word ptr [esp + 0x1c]
0045b9f3  39fa                   cmp      edx, edi
0045b9f5  7ccf                   jl       0x45b9c6
0045b9f7  31ff                   xor      edi, edi
0045b9f9  668b7c240c             mov      di, word ptr [esp + 0xc]
0045b9fe  39fa                   cmp      edx, edi
0045ba00  7fc4                   jg       0x45b9c6
0045ba02  31d2                   xor      edx, edx
0045ba04  8b3db4244e00           mov      edi, dword ptr [0x4e24b4]
0045ba0a  8a13                   mov      dl, byte ptr [ebx]
0045ba0c  01d7                   add      edi, edx
0045ba0e  8a27                   mov      ah, byte ptr [edi]
0045ba10  8823                   mov      byte ptr [ebx], ah
0045ba12  ebb2                   jmp      0x45b9c6 ; 
0045ba14  660fbe542420           movsx    dx, byte ptr [esp + 0x20]
0045ba1a  01c3                   add      ebx, eax
0045ba1c  01d1                   add      ecx, edx
0045ba1e  e925ffffff             jmp      0x45b948 ; 
