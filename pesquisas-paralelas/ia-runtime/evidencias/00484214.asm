; iagVilleInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00484214..0x0048427f (end exclusive); labels are original SBL names
00484214  53                       push ebx
00484215  52                       push edx
00484216  bbd0070000               mov ebx, 0x7d0
0048421b  bac84f4900               mov edx, 0x494fc8
00484220  b8d34f4900               mov eax, 0x494fd3
00484225  e82abaffff               call 0x47fc54 ; -> iaConfigGetValue
0048422a  bbc4090000               mov ebx, 0x9c4
0048422f  bad94f4900               mov edx, 0x494fd9
00484234  a3108c4900               mov dword ptr [0x498c10], eax
00484239  b8e64f4900               mov eax, 0x494fe6
0048423e  e811baffff               call 0x47fc54 ; -> iaConfigGetValue
00484243  bbe8030000               mov ebx, 0x3e8
00484248  baec4f4900               mov edx, 0x494fec
0048424d  a3148c4900               mov dword ptr [0x498c14], eax
00484252  b8f84f4900               mov eax, 0x494ff8
00484257  e8f8b9ffff               call 0x47fc54 ; -> iaConfigGetValue
0048425c  bbe8030000               mov ebx, 0x3e8
00484261  bafe4f4900               mov edx, 0x494ffe
00484266  a3188c4900               mov dword ptr [0x498c18], eax
0048426b  b80a504900               mov eax, 0x49500a
00484270  e8dfb9ffff               call 0x47fc54 ; -> iaConfigGetValue
00484275  a31c8c4900               mov dword ptr [0x498c1c], eax
0048427a  31c0                     xor eax, eax
0048427c  5a                       pop edx
0048427d  5b                       pop ebx
0048427e  c3                       ret
