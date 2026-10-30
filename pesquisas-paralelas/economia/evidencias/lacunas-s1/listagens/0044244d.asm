; SetTroupeRecrutable; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x44246e
0044244d  53                       push     ebx
0044244e  88d3                     mov      bl, dl
00442450  31d2                     xor      edx, edx
00442452  88c2                     mov      dl, al
00442454  89d0                     mov      eax, edx
00442456  c1e002                   shl      eax, 2
00442459  29d0                     sub      eax, edx
0044245b  c1e002                   shl      eax, 2
0044245e  01d0                     add      eax, edx
00442460  31d2                     xor      edx, edx
00442462  88da                     mov      dl, bl
00442464  c6844234194e0001         mov      byte ptr [edx + eax*2 + 0x4e1934], 1
0044246c  5b                       pop      ebx
0044246d  c3                       ret      
