; ProjectileGetLibre; intervalo [0x0046e422, 0x0046e44c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e422  53                       push     ebx
0046e423  52                       push     edx
0046e424  31c0                     xor      eax, eax
0046e426  31d2                     xor      edx, edx
0046e428  6689c2                   mov      dx, ax
0046e42b  83fa64                   cmp      edx, 0x64
0046e42e  0f8df5fbffff             jge      0x46e029
0046e434  6bda38                   imul     ebx, edx, 0x38
0046e437  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046e43d  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046e441  84d2                     test     dl, dl
0046e443  0f84e0fbffff             je       0x46e029
0046e449  40                       inc      eax
0046e44a  ebda                     jmp      0x46e426
