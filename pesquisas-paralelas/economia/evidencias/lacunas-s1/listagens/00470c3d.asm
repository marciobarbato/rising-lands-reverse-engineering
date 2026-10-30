; InventionGetCout; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x470c70
00470c3d  53                       push     ebx
00470c3e  51                       push     ecx
00470c3f  89c3                     mov      ebx, eax
00470c41  81e2ffff0000             and      edx, 0xffff
00470c47  89d0                     mov      eax, edx
00470c49  c1e002                   shl      eax, 2
00470c4c  29d0                     sub      eax, edx
00470c4e  c1e003                   shl      eax, 3
00470c51  89c2                     mov      edx, eax
00470c53  89c1                     mov      ecx, eax
00470c55  31c2                     xor      edx, eax
00470c57  c1e104                   shl      ecx, 4
00470c5a  6689da                   mov      dx, bx
00470c5d  29c1                     sub      ecx, eax
00470c5f  89d0                     mov      eax, edx
00470c61  c1e002                   shl      eax, 2
00470c64  29d0                     sub      eax, edx
00470c66  8b84817c815000           mov      eax, dword ptr [ecx + eax*4 + 0x50817c]
00470c6d  59                       pop      ecx
00470c6e  5b                       pop      ebx
00470c6f  c3                       ret      
