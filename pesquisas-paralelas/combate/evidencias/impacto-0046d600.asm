; PlayerAAttaqueSet; [0x0046d600,0x0046d629)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046d600  53                       push     ebx
0046d601  25ff000000               and      eax, 0xff
0046d606  83f804                   cmp      eax, 4
0046d609  7d1c                     jge      0x46d627
0046d60b  31db                     xor      ebx, ebx
0046d60d  88d3                     mov      bl, dl
0046d60f  83fb04                   cmp      ebx, 4
0046d612  7d13                     jge      0x46d627
0046d614  89c2                     mov      edx, eax
0046d616  c1e002                   shl      eax, 2
0046d619  01c2                     add      edx, eax
0046d61b  c1e202                   shl      edx, 2
0046d61e  89d8                     mov      eax, ebx
0046d620  ff848244805000           inc      dword ptr [edx + eax*4 + 0x508044]
0046d627  5b                       pop      ebx
0046d628  c3                       ret
