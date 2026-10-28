; PlayerGetType; [0x0046d817, 0x0046d838)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046d817  52                       push     edx
0046d818  31d2                     xor      edx, edx
0046d81a  88c2                     mov      dl, al
0046d81c  83fa04                   cmp      edx, 4
0046d81f  7d13                     jge      0x46d834
0046d821  89d0                     mov      eax, edx
0046d823  c1e002                   shl      eax, 2
0046d826  01d0                     add      eax, edx
0046d828  8b15a8805000             mov      edx, dword ptr [0x5080a8]
0046d82e  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
0046d832  5a                       pop      edx
0046d833  c3                       ret
0046d834  b002                     mov      al, 2
0046d836  5a                       pop      edx
0046d837  c3                       ret
