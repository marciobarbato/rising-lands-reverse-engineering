; LoadRessource: limite por próximo símbolo SBL, fim exclusivo 0x0046ab21.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0046aa96  53                       push     ebx
0046aa97  51                       push     ecx
0046aa98  52                       push     edx
0046aa99  83ec04                   sub      esp, 4
0046aa9c  30c9                     xor      cl, cl
0046aa9e  eb1e                     jmp      0x46aabe
0046aaa0  ba02000000               mov      edx, 2
0046aaa5  89e0                     mov      eax, esp
0046aaa7  e8b5d9feff               call     0x458461
0046aaac  31d2                     xor      edx, edx
0046aaae  b801000000               mov      eax, 1
0046aab3  668b1424                 mov      dx, word ptr [esp]
0046aab7  fec1                     inc      cl
0046aab9  e8deceffff               call     0x46799c
0046aabe  31db                     xor      ebx, ebx
0046aac0  88cb                     mov      bl, cl
0046aac2  83fb04                   cmp      ebx, 4
0046aac5  7cd9                     jl       0x46aaa0
0046aac7  30c9                     xor      cl, cl
0046aac9  eb1e                     jmp      0x46aae9
0046aacb  ba02000000               mov      edx, 2
0046aad0  89e0                     mov      eax, esp
0046aad2  e88ad9feff               call     0x458461
0046aad7  31d2                     xor      edx, edx
0046aad9  b802000000               mov      eax, 2
0046aade  668b1424                 mov      dx, word ptr [esp]
0046aae2  fec1                     inc      cl
0046aae4  e8b3ceffff               call     0x46799c
0046aae9  31db                     xor      ebx, ebx
0046aaeb  88cb                     mov      bl, cl
0046aaed  83fb04                   cmp      ebx, 4
0046aaf0  7cd9                     jl       0x46aacb
0046aaf2  30c9                     xor      cl, cl
0046aaf4  eb1b                     jmp      0x46ab11
0046aaf6  ba02000000               mov      edx, 2
0046aafb  89e0                     mov      eax, esp
0046aafd  e85fd9feff               call     0x458461
0046ab02  31d2                     xor      edx, edx
0046ab04  31c0                     xor      eax, eax
0046ab06  668b1424                 mov      dx, word ptr [esp]
0046ab0a  fec1                     inc      cl
0046ab0c  e88bceffff               call     0x46799c
0046ab11  31db                     xor      ebx, ebx
0046ab13  88cb                     mov      bl, cl
0046ab15  83fb04                   cmp      ebx, 4
0046ab18  7cdc                     jl       0x46aaf6
0046ab1a  83c404                   add      esp, 4
0046ab1d  5a                       pop      edx
0046ab1e  59                       pop      ecx
0046ab1f  5b                       pop      ebx
0046ab20  c3                       ret
