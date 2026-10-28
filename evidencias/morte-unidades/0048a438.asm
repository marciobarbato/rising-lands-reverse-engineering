; HandleSnd_StopHandle_inactive; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048a438  53                       push ebx
0048a439  52                       push edx
0048a43a  8b10                     mov edx, dword ptr [eax]
0048a43c  83faff                   cmp edx, -1
0048a43f  7505                     jne 0x48a446
0048a441  31c0                     xor eax, eax
0048a443  5a                       pop edx
0048a444  5b                       pop ebx
0048a445  c3                       ret
