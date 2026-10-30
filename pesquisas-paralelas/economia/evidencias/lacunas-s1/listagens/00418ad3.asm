; SetBatimentRecrutable; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x418af4
00418ad3  53                       push     ebx
00418ad4  88d3                     mov      bl, dl
00418ad6  31d2                     xor      edx, edx
00418ad8  88c2                     mov      dl, al
00418ada  89d0                     mov      eax, edx
00418adc  c1e002                   shl      eax, 2
00418adf  29d0                     sub      eax, edx
00418ae1  c1e002                   shl      eax, 2
00418ae4  29d0                     sub      eax, edx
00418ae6  31d2                     xor      edx, edx
00418ae8  88da                     mov      dl, bl
00418aea  c68442d4fa4d0001         mov      byte ptr [edx + eax*2 + 0x4dfad4], 1
00418af2  5b                       pop      ebx
00418af3  c3                       ret      
