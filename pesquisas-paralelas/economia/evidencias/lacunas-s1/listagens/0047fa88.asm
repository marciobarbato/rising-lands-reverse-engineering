; IaRechercheAjuste; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x47fb15
0047fa88  53                       push     ebx
0047fa89  51                       push     ecx
0047fa8a  52                       push     edx
0047fa8b  56                       push     esi
0047fa8c  57                       push     edi
0047fa8d  55                       push     ebp
0047fa8e  83ec04                   sub      esp, 4
0047fa91  31c0                     xor      eax, eax
0047fa93  ba01000000               mov      edx, 1
0047fa98  e8b70affff               call     0x470554
0047fa9d  0fb6e8                   movzx    ebp, al
0047faa0  891424                   mov      dword ptr [esp], edx
0047faa3  eb10                     jmp      0x47fab5
0047faa5  8b1c24                   mov      ebx, dword ptr [esp]
0047faa8  43                       inc      ebx
0047faa9  891c24                   mov      dword ptr [esp], ebx
0047faac  83fb04                   cmp      ebx, 4
0047faaf  0f8d4efcffff             jge      0x47f703
0047fab5  31d2                     xor      edx, edx
0047fab7  8a1424                   mov      dl, byte ptr [esp]
0047faba  89d0                     mov      eax, edx
0047fabc  31db                     xor      ebx, ebx
0047fabe  e854ddfeff               call     0x46d817
0047fac3  88c3                     mov      bl, al
0047fac5  83fb02                   cmp      ebx, 2
0047fac8  75db                     jne      0x47faa5
0047faca  31db                     xor      ebx, ebx
0047facc  e849c6feff               call     0x46c11a
0047fad1  6689c3                   mov      bx, ax
0047fad4  83fb03                   cmp      ebx, 3
0047fad7  7ccc                     jl       0x47faa5
0047fad9  89d0                     mov      eax, edx
0047fadb  e8d11cffff               call     0x4717b1
0047fae0  31c9                     xor      ecx, ecx
0047fae2  89c7                     mov      edi, eax
0047fae4  eb01                     jmp      0x47fae7
0047fae6  41                       inc      ecx
0047fae7  39e9                     cmp      ecx, ebp
0047fae9  7dba                     jge      0x47faa5
0047faeb  31db                     xor      ebx, ebx
0047faed  31d2                     xor      edx, edx
0047faef  8a1c24                   mov      bl, byte ptr [esp]
0047faf2  6689fa                   mov      dx, di
0047faf5  89d8                     mov      eax, ebx
0047faf7  0fb6b264844900           movzx    esi, byte ptr [edx + 0x498464]
0047fafe  e8bf1cffff               call     0x4717c2
0047fb03  31d2                     xor      edx, edx
0047fb05  6689c2                   mov      dx, ax
0047fb08  39f2                     cmp      edx, esi
0047fb0a  7dda                     jge      0x47fae6
0047fb0c  89d8                     mov      eax, ebx
0047fb0e  e88a19ffff               call     0x47149d
0047fb13  ebd1                     jmp      0x47fae6
