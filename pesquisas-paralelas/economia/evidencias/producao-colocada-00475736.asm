; Terrain paired raw-byte pointer consumers; exclusive end0x475763.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Context evidence; this composition does not invoke every resource-removal branch.
00475736  52                       push     edx
00475737  31d2                     xor      edx, edx
00475739  6689c2                   mov      dx, ax
0047573c  a1747d5000               mov      eax, dword ptr [0x507d74]
00475741  8a0402                   mov      al, byte ptr [edx + eax]
00475744  25ff000000               and      eax, 0xff
00475749  83f842                   cmp      eax, 0x42
0047574c  7c11                     jl       0x47575f
0047574e  83f844                   cmp      eax, 0x44
00475751  7f0c                     jg       0x47575f
00475753  a1ac7d5000               mov      eax, dword ptr [0x507dac]
00475758  8a0402                   mov      al, byte ptr [edx + eax]
0047575b  30e4                     xor      ah, ah
0047575d  5a                       pop      edx
0047575e  c3                       ret
0047575f  31c0                     xor      eax, eax
00475761  5a                       pop      edx
00475762  c3                       ret
