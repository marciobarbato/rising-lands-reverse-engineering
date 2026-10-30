; TechnologieReset; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x46b57f
0046b517  53                       push     ebx
0046b518  51                       push     ecx
0046b519  52                       push     edx
0046b51a  31c9                     xor      ecx, ecx
0046b51c  eb1c                     jmp      0x46b53a
0046b51e  31db                     xor      ebx, ebx
0046b520  6689cb                   mov      bx, cx
0046b523  6bdb1a                   imul     ebx, ebx, 0x1a
0046b526  40                       inc      eax
0046b527  c6841a34194e0000         mov      byte ptr [edx + ebx + 0x4e1934], 0
0046b52f  31d2                     xor      edx, edx
0046b531  6689c2                   mov      dx, ax
0046b534  83fa1a                   cmp      edx, 0x1a
0046b537  7ce5                     jl       0x46b51e
0046b539  41                       inc      ecx
0046b53a  31d2                     xor      edx, edx
0046b53c  6689ca                   mov      dx, cx
0046b53f  83fa04                   cmp      edx, 4
0046b542  7d04                     jge      0x46b548
0046b544  31c0                     xor      eax, eax
0046b546  ebe7                     jmp      0x46b52f
0046b548  30c9                     xor      cl, cl
0046b54a  eb1d                     jmp      0x46b569
0046b54c  31db                     xor      ebx, ebx
0046b54e  88cb                     mov      bl, cl
0046b550  6bdb16                   imul     ebx, ebx, 0x16
0046b553  30ed                     xor      ch, ch
0046b555  40                       inc      eax
0046b556  88ac1ad4fa4d00           mov      byte ptr [edx + ebx + 0x4dfad4], ch
0046b55d  31d2                     xor      edx, edx
0046b55f  6689c2                   mov      dx, ax
0046b562  83fa16                   cmp      edx, 0x16
0046b565  7ce5                     jl       0x46b54c
0046b567  fec1                     inc      cl
0046b569  31d2                     xor      edx, edx
0046b56b  88ca                     mov      dl, cl
0046b56d  83fa04                   cmp      edx, 4
0046b570  7d04                     jge      0x46b576
0046b572  31c0                     xor      eax, eax
0046b574  ebe7                     jmp      0x46b55d
0046b576  e877940000               call     0x4749f2
0046b57b  5a                       pop      edx
0046b57c  59                       pop      ecx
0046b57d  5b                       pop      ebx
0046b57e  c3                       ret      
