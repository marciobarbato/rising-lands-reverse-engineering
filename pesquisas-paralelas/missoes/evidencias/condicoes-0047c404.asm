; LoadObjectif; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047c404  53                       push ebx
0047c405  51                       push ecx
0047c406  52                       push edx
0047c407  56                       push esi
0047c408  57                       push edi
0047c409  55                       push ebp
0047c40a  81ec24030000             sub esp, 0x324
0047c410  baffff0000               mov edx, 0xffff
0047c415  30db                     xor bl, bl
0047c417  eb1e                     jmp 0x47c437
0047c419  0fb6f3                   movzx esi, bl
0047c41c  69f6c8000000             imul esi, esi, 0xc8
0047c422  40                       inc eax
0047c423  6689944efc1f5100         mov word ptr [esi + ecx*2 + 0x511ffc], dx
0047c42b  31c9                     xor ecx, ecx
0047c42d  6689c1                   mov cx, ax
0047c430  83f964                   cmp ecx, 0x64
0047c433  7ce4                     jl 0x47c419
0047c435  fec3                     inc bl
0047c437  31c0                     xor eax, eax
0047c439  88d8                     mov al, bl
0047c43b  83f804                   cmp eax, 4
0047c43e  7d04                     jge 0x47c444
0047c440  31c0                     xor eax, eax
0047c442  ebe7                     jmp 0x47c42b
0047c444  30e4                     xor ah, ah
0047c446  88a42420030000           mov byte ptr [esp + 0x320], ah
0047c44d  bd02000000               mov ebp, 2
0047c452  bf01000000               mov edi, 1
0047c457  eb3f                     jmp 0x47c498
0047c459  0fb6b42420030000         movzx esi, byte ptr [esp + 0x320]
0047c461  69f6c8000000             imul esi, esi, 0xc8
0047c467  b8fc1f5100               mov eax, 0x511ffc
0047c46c  01c9                     add ecx, ecx
0047c46e  01f0                     add eax, esi
0047c470  89ea                     mov edx, ebp
0047c472  01c8                     add eax, ecx
0047c474  e8e8bffdff               call 0x458461
0047c479  89e0                     mov eax, esp
0047c47b  01f0                     add eax, esi
0047c47d  89fa                     mov edx, edi
0047c47f  01c8                     add eax, ecx
0047c481  43                       inc ebx
0047c482  e8dabffdff               call 0x458461
0047c487  31c9                     xor ecx, ecx
0047c489  6689d9                   mov cx, bx
0047c48c  83f964                   cmp ecx, 0x64
0047c48f  7cc8                     jl 0x47c459
0047c491  fe842420030000           inc byte ptr [esp + 0x320]
0047c498  31c0                     xor eax, eax
0047c49a  8a842420030000           mov al, byte ptr [esp + 0x320]
0047c4a1  83f804                   cmp eax, 4
0047c4a4  7d04                     jge 0x47c4aa
0047c4a6  31db                     xor ebx, ebx
0047c4a8  ebdd                     jmp 0x47c487
0047c4aa  81c424030000             add esp, 0x324
0047c4b0  5d                       pop ebp
0047c4b1  5f                       pop edi
0047c4b2  5e                       pop esi
0047c4b3  5a                       pop edx
0047c4b4  59                       pop ecx
0047c4b5  5b                       pop ebx
0047c4b6  c3                       ret
