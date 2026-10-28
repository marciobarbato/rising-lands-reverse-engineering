; memset; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048c3b0  50                       push eax
0048c3b1  51                       push ecx
0048c3b2  88d6                     mov dh, dl
0048c3b4  c1e208                   shl edx, 8
0048c3b7  88f2                     mov dl, dh
0048c3b9  c1e208                   shl edx, 8
0048c3bc  88f2                     mov dl, dh
0048c3be  89d9                     mov ecx, ebx
0048c3c0  e8cb140000               call 0x48d890
0048c3c5  59                       pop ecx
0048c3c6  58                       pop eax
0048c3c7  c3                       ret
