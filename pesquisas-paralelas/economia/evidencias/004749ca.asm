; SortilegeResetRealisable: limite por próximo símbolo SBL, fim exclusivo 0x004749f2.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004749ca  53                       push     ebx
004749cb  51                       push     ecx
004749cc  52                       push     edx
004749cd  88c1                     mov      cl, al
004749cf  31c0                     xor      eax, eax
004749d1  eb11                     jmp      0x4749e4
004749d3  31db                     xor      ebx, ebx
004749d5  88cb                     mov      bl, cl
004749d7  8d1c9b                   lea      ebx, [ebx + ebx*4]
004749da  30ed                     xor      ch, ch
004749dc  40                       inc      eax
004749dd  88ac1a308f5000           mov      byte ptr [edx + ebx + 0x508f30], ch
004749e4  31d2                     xor      edx, edx
004749e6  6689c2                   mov      dx, ax
004749e9  83fa05                   cmp      edx, 5
004749ec  7ce5                     jl       0x4749d3
004749ee  5a                       pop      edx
004749ef  59                       pop      ecx
004749f0  5b                       pop      ebx
004749f1  c3                       ret
