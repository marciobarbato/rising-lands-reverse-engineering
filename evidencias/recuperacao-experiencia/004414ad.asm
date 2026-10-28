; Engin_LoadExperimente (provenance); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004414ad  53                       push ebx
004414ae  52                       push edx
004414af  89c3                     mov ebx, eax
004414b1  ba28000000               mov edx, 0x28
004414b6  b8c4194e00               mov eax, 0x4e19c4
004414bb  e8a16f0100               call 0x458461
004414c0  83fb04                   cmp ebx, 4
004414c3  7c0f                     jl 0x4414d4
004414c5  ba28000000               mov edx, 0x28
004414ca  b8ec194e00               mov eax, 0x4e19ec
004414cf  e88d6f0100               call 0x458461
004414d4  5a                       pop edx
004414d5  5b                       pop ebx
004414d6  c3                       ret
