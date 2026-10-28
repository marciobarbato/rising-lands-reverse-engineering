; FileReadSeek; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00458461  53                       push ebx
00458462  51                       push ecx
00458463  bb01000000               mov ebx, 1
00458468  8b0d1c1d4e00             mov ecx, dword ptr [0x4e1d1c]
0045846e  e808450300               call 0x48c97b
00458473  59                       pop ecx
00458474  5b                       pop ebx
00458475  c3                       ret
00458476  53                       push ebx
00458477  51                       push ecx
00458478  bb01000000               mov ebx, 1
0045847d  8b0d1c1d4e00             mov ecx, dword ptr [0x4e1d1c]
00458483  e8f2460300               call 0x48cb7a
00458488  59                       pop ecx
00458489  5b                       pop ebx
0045848a  c3                       ret
0045848b  53                       push ebx
0045848c  51                       push ecx
0045848d  31db                     xor ebx, ebx
0045848f  8b0d1c1d4e00             mov ecx, dword ptr [0x4e1d1c]
00458495  88d3                     mov bl, dl
00458497  89c2                     mov edx, eax
00458499  89c8                     mov eax, ecx
0045849b  e802490300               call 0x48cda2
004584a0  59                       pop ecx
004584a1  5b                       pop ebx
004584a2  c3                       ret
