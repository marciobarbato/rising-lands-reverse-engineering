; Random; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004704dc  53                       push ebx
004704dd  51                       push ecx
004704de  52                       push edx
004704df  bb1df30100               mov ebx, 0x1f31d
004704e4  a164714900               mov eax, dword ptr [0x497164]
004704e9  31d2                     xor edx, edx
004704eb  f7f3                     div ebx
004704ed  69d8140b0000             imul ebx, eax, 0xb14
004704f3  b91df30100               mov ecx, 0x1f31d
004704f8  31d2                     xor edx, edx
004704fa  a164714900               mov eax, dword ptr [0x497164]
004704ff  f7f1                     div ecx
00470501  69c2a7410000             imul eax, edx, 0x41a7
00470507  29d8                     sub eax, ebx
00470509  85c0                     test eax, eax
0047050b  7f05                     jg 0x470512
0047050d  05ffffff7f               add eax, 0x7fffffff
00470512  a364714900               mov dword ptr [0x497164], eax
00470517  a164714900               mov eax, dword ptr [0x497164]
0047051c  5a                       pop edx
0047051d  59                       pop ecx
0047051e  5b                       pop ebx
0047051f  c3                       ret
