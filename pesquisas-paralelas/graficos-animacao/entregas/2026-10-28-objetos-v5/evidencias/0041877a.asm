; LoadSTRATBank [0x41877a, 0x4189c2)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041877a  53                     push     ebx
0041877b  51                     push     ecx
0041877c  52                     push     edx
0041877d  56                     push     esi
0041877e  57                     push     edi
0041877f  55                     push     ebp
00418780  81ec30010000           sub      esp, 0x130
00418786  b906000000             mov      ecx, 6
0041878b  8dbc2400010000         lea      edi, [esp + 0x100]
00418792  bec85b4900             mov      esi, 0x495bc8
00418797  31d2                   xor      edx, edx
00418799  b808000000             mov      eax, 8
0041879e  89942428010000         mov      dword ptr [esp + 0x128], edx
004187a5  f3a5                   rep movsd dword ptr es:[edi], dword ptr [esi]
004187a7  e8faf60400             call     0x467ea6 ; MemAlloc
004187ac  89942424010000         mov      dword ptr [esp + 0x124], edx
004187b3  89c5                   mov      ebp, eax
004187b5  668910                 mov      word ptr [eax], dx
004187b8  eb3b                   jmp      0x4187f5 ;
004187ba  8d842418010000         lea      eax, [esp + 0x118]
004187c1  01db                   add      ebx, ebx
004187c3  ba02000000             mov      edx, 2
004187c8  01d8                   add      eax, ebx
004187ca  8bbc2424010000         mov      edi, dword ptr [esp + 0x124]
004187d1  e88bfc0300             call     0x458461 ; FileRead
004187d6  668b841c18010000       mov      ax, word ptr [esp + ebx + 0x118]
004187de  668b7500               mov      si, word ptr [ebp]
004187e2  47                     inc      edi
004187e3  01c6                   add      esi, eax
004187e5  89bc2424010000         mov      dword ptr [esp + 0x124], edi
004187ec  66897500               mov      word ptr [ebp], si
004187f0  e857fc0300             call     0x45844c ; FileClose
004187f5  31db                   xor      ebx, ebx
004187f7  668b9c2424010000       mov      bx, word ptr [esp + 0x124]
004187ff  83fb06                 cmp      ebx, 6
00418802  7d68                   jge      0x41886c
00418804  be94945000             mov      esi, 0x509494
00418809  89e7                   mov      edi, esp
0041880b  57                     push     edi
0041880c  8a06                   mov      al, byte ptr [esi]
0041880e  8807                   mov      byte ptr [edi], al
00418810  3c00                   cmp      al, 0
00418812  7410                   je       0x418824
00418814  8a4601                 mov      al, byte ptr [esi + 1]
00418817  83c602                 add      esi, 2
0041881a  884701                 mov      byte ptr [edi + 1], al
0041881d  83c702                 add      edi, 2
00418820  3c00                   cmp      al, 0
00418822  75e8                   jne      0x41880c
00418824  5f                     pop      edi
00418825  89e7                   mov      edi, esp
00418827  8bb49c00010000         mov      esi, dword ptr [esp + ebx*4 + 0x100]
0041882e  bad6414900             mov      edx, 0x4941d6
00418833  57                     push     edi
00418834  2bc9                   sub      ecx, ecx
00418836  49                     dec      ecx
00418837  b000                   mov      al, 0
00418839  f2ae                   repne scasb al, byte ptr es:[edi]
0041883b  4f                     dec      edi
0041883c  8a06                   mov      al, byte ptr [esi]
0041883e  8807                   mov      byte ptr [edi], al
00418840  3c00                   cmp      al, 0
00418842  7410                   je       0x418854
00418844  8a4601                 mov      al, byte ptr [esi + 1]
00418847  83c602                 add      esi, 2
0041884a  884701                 mov      byte ptr [edi + 1], al
0041884d  83c702                 add      edi, 2
00418850  3c00                   cmp      al, 0
00418852  75e8                   jne      0x41883c
00418854  5f                     pop      edi
00418855  89e0                   mov      eax, esp
00418857  e8c4fb0300             call     0x458420 ; FileOpen
0041885c  25ff000000             and      eax, 0xff
00418861  0f8553ffffff           jne      0x4187ba
00418867  e949010000             jmp      0x4189b5 ;
0041886c  31c0                   xor      eax, eax
0041886e  668b4500               mov      ax, word ptr [ebp]
00418872  31c9                   xor      ecx, ecx
00418874  c1e002                 shl      eax, 2
00418877  898c242c010000         mov      dword ptr [esp + 0x12c], ecx
0041887e  e823f60400             call     0x467ea6 ; MemAlloc
00418883  894504                 mov      dword ptr [ebp + 4], eax
00418886  e9a4000000             jmp      0x41892f ;
0041888b  89c3                   mov      ebx, eax
0041888d  43                     inc      ebx
0041888e  41                     inc      ecx
0041888f  899c2428010000         mov      dword ptr [esp + 0x128], ebx
00418896  31c0                   xor      eax, eax
00418898  668b84242c010000       mov      ax, word ptr [esp + 0x12c]
004188a0  663b8c4418010000       cmp      cx, word ptr [esp + eax*2 + 0x118]
004188a8  7371                   jae      0x41891b
004188aa  b80c000000             mov      eax, 0xc
004188af  e8f2f50400             call     0x467ea6 ; MemAlloc
004188b4  89c3                   mov      ebx, eax
004188b6  85c0                   test     eax, eax
004188b8  743f                   je       0x4188f9
004188ba  ba02000000             mov      edx, 2
004188bf  e89dfb0300             call     0x458461 ; FileRead
004188c4  ba02000000             mov      edx, 2
004188c9  8d4302                 lea      eax, [ebx + 2]
004188cc  e890fb0300             call     0x458461 ; FileRead
004188d1  ba04000000             mov      edx, 4
004188d6  8d4304                 lea      eax, [ebx + 4]
004188d9  e883fb0300             call     0x458461 ; FileRead
004188de  8b4304                 mov      eax, dword ptr [ebx + 4]
004188e1  e8c0f50400             call     0x467ea6 ; MemAlloc
004188e6  894308                 mov      dword ptr [ebx + 8], eax
004188e9  85c0                   test     eax, eax
004188eb  7504                   jne      0x4188f1
004188ed  31db                   xor      ebx, ebx
004188ef  eb08                   jmp      0x4188f9 ;
004188f1  8b5304                 mov      edx, dword ptr [ebx + 4]
004188f4  e868fb0300             call     0x458461 ; FileRead
004188f9  31c0                   xor      eax, eax
004188fb  8b5504                 mov      edx, dword ptr [ebp + 4]
004188fe  668b842428010000       mov      ax, word ptr [esp + 0x128]
00418906  891c82                 mov      dword ptr [edx + eax*4], ebx
00418909  8b5504                 mov      edx, dword ptr [ebp + 4]
0041890c  833c8200               cmp      dword ptr [edx + eax*4], 0
00418910  0f8575ffffff           jne      0x41888b
00418916  e831fb0300             call     0x45844c ; FileClose
0041891b  8b8c242c010000         mov      ecx, dword ptr [esp + 0x12c]
00418922  41                     inc      ecx
00418923  e824fb0300             call     0x45844c ; FileClose
00418928  898c242c010000         mov      dword ptr [esp + 0x12c], ecx
0041892f  31db                   xor      ebx, ebx
00418931  668b9c242c010000       mov      bx, word ptr [esp + 0x12c]
00418939  83fb06                 cmp      ebx, 6
0041893c  7d75                   jge      0x4189b3
0041893e  be94945000             mov      esi, 0x509494
00418943  89e7                   mov      edi, esp
00418945  57                     push     edi
00418946  8a06                   mov      al, byte ptr [esi]
00418948  8807                   mov      byte ptr [edi], al
0041894a  3c00                   cmp      al, 0
0041894c  7410                   je       0x41895e
0041894e  8a4601                 mov      al, byte ptr [esi + 1]
00418951  83c602                 add      esi, 2
00418954  884701                 mov      byte ptr [edi + 1], al
00418957  83c702                 add      edi, 2
0041895a  3c00                   cmp      al, 0
0041895c  75e8                   jne      0x418946
0041895e  5f                     pop      edi
0041895f  89e7                   mov      edi, esp
00418961  8bb49c00010000         mov      esi, dword ptr [esp + ebx*4 + 0x100]
00418968  bad9414900             mov      edx, 0x4941d9
0041896d  57                     push     edi
0041896e  2bc9                   sub      ecx, ecx
00418970  49                     dec      ecx
00418971  b000                   mov      al, 0
00418973  f2ae                   repne scasb al, byte ptr es:[edi]
00418975  4f                     dec      edi
00418976  8a06                   mov      al, byte ptr [esi]
00418978  8807                   mov      byte ptr [edi], al
0041897a  3c00                   cmp      al, 0
0041897c  7410                   je       0x41898e
0041897e  8a4601                 mov      al, byte ptr [esi + 1]
00418981  83c602                 add      esi, 2
00418984  884701                 mov      byte ptr [edi + 1], al
00418987  83c702                 add      edi, 2
0041898a  3c00                   cmp      al, 0
0041898c  75e8                   jne      0x418976
0041898e  5f                     pop      edi
0041898f  89e0                   mov      eax, esp
00418991  e88afa0300             call     0x458420 ; FileOpen
00418996  8d942418010000         lea      edx, [esp + 0x118]
0041899d  8d041b                 lea      eax, [ebx + ebx]
004189a0  01d0                   add      eax, edx
004189a2  ba02000000             mov      edx, 2
004189a7  31c9                   xor      ecx, ecx
004189a9  e8b3fa0300             call     0x458461 ; FileRead
004189ae  e9e3feffff             jmp      0x418896 ;
004189b3  89e8                   mov      eax, ebp
004189b5  81c430010000           add      esp, 0x130
004189bb  5d                     pop      ebp
004189bc  5f                     pop      edi
004189bd  5e                     pop      esi
004189be  5a                     pop      edx
004189bf  59                     pop      ecx
004189c0  5b                     pop      ebx
004189c1  c3                     ret
