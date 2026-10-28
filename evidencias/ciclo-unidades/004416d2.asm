; unit_bag_entries; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004416d2  89c3                     mov ebx, eax
004416d4  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
004416db  42                       inc edx
004416dc  c644014200               mov byte ptr [ecx + eax + 0x42], 0
004416e1  31c0                     xor eax, eax
004416e3  6689d0                   mov ax, dx
004416e6  83f81e                   cmp eax, 0x1e
004416e9  7ce7                     jl 0x4416d2
