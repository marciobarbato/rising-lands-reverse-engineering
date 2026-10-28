; table_bag_entries; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441679  89c3                     mov ebx, eax
0044167b  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
00441682  42                       inc edx
00441683  c644014200               mov byte ptr [ecx + eax + 0x42], 0
00441688  31c0                     xor eax, eax
0044168a  6689d0                   mov ax, dx
0044168d  83f81e                   cmp eax, 0x1e
00441690  7ce7                     jl 0x441679
