; PlaySnd_PostSound_dependency; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0048aa79  56                       push esi
0048aa7a  89c6                     mov esi, eax
0048aa7c  89d0                     mov eax, edx
0048aa7e  8b542408                 mov edx, dword ptr [esp + 8]
0048aa82  83fe42                   cmp esi, 0x42
0048aa85  7230                     jb 0x48aab7
0048aa87  761e                     jbe 0x48aaa7
0048aa89  83fe50                   cmp esi, 0x50
0048aa8c  7421                     je 0x48aaaf
0048aa8e  5e                       pop esi
0048aa8f  c20400                   ret 4
0048aa92  52                       push edx
0048aa93  bac81f5200               mov edx, 0x521fc8
0048aa98  81e1ff000000             and ecx, 0xff
0048aa9e  e875f7ffff               call 0x48a218
0048aaa3  5e                       pop esi
0048aaa4  c20400                   ret 4
0048aaa7  52                       push edx
0048aaa8  bae41f5200               mov edx, 0x521fe4
0048aaad  ebe9                     jmp 0x48aa98
0048aaaf  52                       push edx
0048aab0  ba00205200               mov edx, 0x522000
0048aab5  ebe1                     jmp 0x48aa98
0048aab7  83fe41                   cmp esi, 0x41
0048aaba  74d6                     je 0x48aa92
0048aabc  5e                       pop esi
0048aabd  c20400                   ret 4
