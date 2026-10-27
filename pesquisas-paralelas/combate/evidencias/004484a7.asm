; GiroTorre; intervalo [0x004484a7, 0x00448599)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004484a7  53                       push     ebx
004484a8  51                       push     ecx
004484a9  52                       push     edx
004484aa  31d2                     xor      edx, edx
004484ac  6689c2                   mov      dx, ax
004484af  89d3                     mov      ebx, edx
004484b1  c1e304                   shl      ebx, 4
004484b4  01d3                     add      ebx, edx
004484b6  c1e302                   shl      ebx, 2
004484b9  01d3                     add      ebx, edx
004484bb  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004484c1  c1e302                   shl      ebx, 2
004484c4  01d3                     add      ebx, edx
004484c6  8a5301                   mov      dl, byte ptr [ebx + 1]
004484c9  80fa0c                   cmp      dl, 0xc
004484cc  720f                     jb       0x4484dd
004484ce  0f8698000000             jbe      0x44856c
004484d4  80fa0f                   cmp      dl, 0xf
004484d7  0f848f000000             je       0x44856c
004484dd  30d2                     xor      dl, dl
004484df  84d2                     test     dl, dl
004484e1  0f84ae000000             je       0x448595
004484e7  8a83da000000             mov      al, byte ptr [ebx + 0xda]
004484ed  3a8394000000             cmp      al, byte ptr [ebx + 0x94]
004484f3  0f849c000000             je       0x448595
004484f9  8a9396000000             mov      dl, byte ptr [ebx + 0x96]
004484ff  fec2                     inc      dl
00448501  889396000000             mov      byte ptr [ebx + 0x96], dl
00448507  3a9393000000             cmp      dl, byte ptr [ebx + 0x93]
0044850d  0f8582000000             jne      0x448595
00448513  8a83da000000             mov      al, byte ptr [ebx + 0xda]
00448519  3a8394000000             cmp      al, byte ptr [ebx + 0x94]
0044851f  7613                     jbe      0x448534
00448521  31c9                     xor      ecx, ecx
00448523  31d2                     xor      edx, edx
00448525  88c1                     mov      cl, al
00448527  8a9394000000             mov      dl, byte ptr [ebx + 0x94]
0044852d  29d1                     sub      ecx, edx
0044852f  83f910                   cmp      ecx, 0x10
00448532  7c21                     jl       0x448555
00448534  8a8394000000             mov      al, byte ptr [ebx + 0x94]
0044853a  3a83da000000             cmp      al, byte ptr [ebx + 0xda]
00448540  7631                     jbe      0x448573
00448542  31c9                     xor      ecx, ecx
00448544  31d2                     xor      edx, edx
00448546  88c1                     mov      cl, al
00448548  8a93da000000             mov      dl, byte ptr [ebx + 0xda]
0044854e  29d1                     sub      ecx, edx
00448550  83f910                   cmp      ecx, 0x10
00448553  7e1e                     jle      0x448573
00448555  31d2                     xor      edx, edx
00448557  8a9394000000             mov      dl, byte ptr [ebx + 0x94]
0044855d  b920000000               mov      ecx, 0x20
00448562  89d0                     mov      eax, edx
00448564  c1fa1f                   sar      edx, 0x1f
00448567  f7f9                     idiv     ecx
00448569  42                       inc      edx
0044856a  eb1c                     jmp      0x448588
0044856c  b201                     mov      dl, 1
0044856e  e96cffffff               jmp      0x4484df
00448573  31d2                     xor      edx, edx
00448575  8a9394000000             mov      dl, byte ptr [ebx + 0x94]
0044857b  83fa01                   cmp      edx, 1
0044857e  7403                     je       0x448583
00448580  4a                       dec      edx
00448581  eb05                     jmp      0x448588
00448583  ba20000000               mov      edx, 0x20
00448588  889394000000             mov      byte ptr [ebx + 0x94], dl
0044858e  c6839600000000           mov      byte ptr [ebx + 0x96], 0
00448595  5a                       pop      edx
00448596  59                       pop      ecx
00448597  5b                       pop      ebx
00448598  c3                       ret
