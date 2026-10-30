; BonusReset; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x428ef0
00428e71  53                       push     ebx
00428e72  51                       push     ecx
00428e73  52                       push     edx
00428e74  30f6                     xor      dh, dh
00428e76  31c9                     xor      ecx, ecx
00428e78  eb63                     jmp      0x428edd
00428e7a  6bc012                   imul     eax, eax, 0x12
00428e7d  31db                     xor      ebx, ebx
00428e7f  88f3                     mov      bl, dh
00428e81  69dbd4010000             imul     ebx, ebx, 0x1d4
00428e87  66898c03a0fb4d00         mov      word ptr [ebx + eax + 0x4dfba0], cx
00428e8f  888c03a2fb4d00           mov      byte ptr [ebx + eax + 0x4dfba2], cl
00428e96  66898c03a4fb4d00         mov      word ptr [ebx + eax + 0x4dfba4], cx
00428e9e  888c03acfb4d00           mov      byte ptr [ebx + eax + 0x4dfbac], cl
00428ea5  888c03a6fb4d00           mov      byte ptr [ebx + eax + 0x4dfba6], cl
00428eac  888c03abfb4d00           mov      byte ptr [ebx + eax + 0x4dfbab], cl
00428eb3  66898c03a8fb4d00         mov      word ptr [ebx + eax + 0x4dfba8], cx
00428ebb  888c03aafb4d00           mov      byte ptr [ebx + eax + 0x4dfbaa], cl
00428ec2  888c03adfb4d00           mov      byte ptr [ebx + eax + 0x4dfbad], cl
00428ec9  fec2                     inc      dl
00428ecb  888c03aefb4d00           mov      byte ptr [ebx + eax + 0x4dfbae], cl
00428ed2  31c0                     xor      eax, eax
00428ed4  88d0                     mov      al, dl
00428ed6  83f81a                   cmp      eax, 0x1a
00428ed9  7c9f                     jl       0x428e7a
00428edb  fec6                     inc      dh
00428edd  31c0                     xor      eax, eax
00428edf  88f0                     mov      al, dh
00428ee1  83f804                   cmp      eax, 4
00428ee4  0f8d2cf8ffff             jge      0x428716
00428eea  88ca                     mov      dl, cl
00428eec  ebe4                     jmp      0x428ed2
00428eee  0000                     add      byte ptr [eax], al
