; Engin_ResetExperience (provenance); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441470  53                       push ebx
00441471  51                       push ecx
00441472  52                       push edx
00441473  31c9                     xor ecx, ecx
00441475  eb24                     jmp 0x44149b
00441477  31db                     xor ebx, ebx
00441479  6689cb                   mov bx, cx
0044147c  6bdb0a                   imul ebx, ebx, 0xa
0044147f  c68443ed194e0000         mov byte ptr [ebx + eax*2 + 0x4e19ed], 0
00441487  42                       inc edx
00441488  c68443ec194e00ff         mov byte ptr [ebx + eax*2 + 0x4e19ec], 0xff
00441490  31c0                     xor eax, eax
00441492  6689d0                   mov ax, dx
00441495  83f805                   cmp eax, 5
00441498  7cdd                     jl 0x441477
0044149a  41                       inc ecx
0044149b  31c0                     xor eax, eax
0044149d  6689c8                   mov ax, cx
004414a0  83f804                   cmp eax, 4
004414a3  0f8db1f8ffff             jge 0x440d5a
004414a9  31d2                     xor edx, edx
004414ab  ebe3                     jmp 0x441490
