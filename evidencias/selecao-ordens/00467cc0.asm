; SwapWORD; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00467cc0  53                       push ebx
00467cc1  51                       push ecx
00467cc2  668b1a                   mov bx, word ptr [edx]
00467cc5  668b08                   mov cx, word ptr [eax]
00467cc8  668918                   mov word ptr [eax], bx
00467ccb  66890a                   mov word ptr [edx], cx
00467cce  59                       pop ecx
00467ccf  5b                       pop ebx
00467cd0  c3                       ret
