; Resource-removal pointer context; exclusive end0x4766f0.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Context evidence; this composition does not invoke every resource-removal branch.
00476662  53                       push     ebx
00476663  51                       push     ecx
00476664  52                       push     edx
00476665  56                       push     esi
00476666  89c3                     mov      ebx, eax
00476668  31c9                     xor      ecx, ecx
0047666a  6689c1                   mov      cx, ax
0047666d  a1ac7d5000               mov      eax, dword ptr [0x507dac]
00476672  01c8                     add      eax, ecx
00476674  0fb630                   movzx    esi, byte ptr [eax]
00476677  30d2                     xor      dl, dl
00476679  85f6                     test     esi, esi
0047667b  740d                     je       0x47668a
0047667d  fe08                     dec      byte ptr [eax]
0047667f  a1747d5000               mov      eax, dword ptr [0x507d74]
00476684  8a1401                   mov      dl, byte ptr [ecx + eax]
00476687  80ea42                   sub      dl, 0x42
0047668a  31c0                     xor      eax, eax
0047668c  8b0dac7d5000             mov      ecx, dword ptr [0x507dac]
00476692  6689d8                   mov      ax, bx
00476695  8a0c01                   mov      cl, byte ptr [ecx + eax]
00476698  81e1ff000000             and      ecx, 0xff
0047669e  750a                     jne      0x4766aa
004766a0  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
004766a6  c6040100                 mov      byte ptr [ecx + eax], 0
004766aa  88d0                     mov      al, dl
004766ac  5e                       pop      esi
004766ad  5a                       pop      edx
004766ae  59                       pop      ecx
004766af  5b                       pop      ebx
004766b0  c3                       ret
004766b1  52                       push     edx
004766b2  31d2                     xor      edx, edx
004766b4  6689c2                   mov      dx, ax
004766b7  a1747d5000               mov      eax, dword ptr [0x507d74]
004766bc  8a0402                   mov      al, byte ptr [edx + eax]
004766bf  25ff000000               and      eax, 0xff
004766c4  83f842                   cmp      eax, 0x42
004766c7  7c09                     jl       0x4766d2
004766c9  83f844                   cmp      eax, 0x44
004766cc  7f04                     jg       0x4766d2
004766ce  b001                     mov      al, 1
004766d0  5a                       pop      edx
004766d1  c3                       ret
004766d2  30c0                     xor      al, al
004766d4  5a                       pop      edx
004766d5  c3                       ret
004766d6  81e2ff000000             and      edx, 0xff
004766dc  25ffff0000               and      eax, 0xffff
004766e1  8b1495787d5000           mov      edx, dword ptr [edx*4 + 0x507d78]
004766e8  f6040210                 test     byte ptr [edx + eax], 0x10
004766ec  0f94c0                   sete     al
004766ef  c3                       ret
