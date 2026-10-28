; PaletteAlloc [0x45f6e1, 0x45f760)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045f6e1  53                     push     ebx
0045f6e2  52                     push     edx
0045f6e3  b800030000             mov      eax, 0x300
0045f6e8  e8b9870000             call     0x467ea6 ; MemAlloc
0045f6ed  a3b0244e00             mov      dword ptr [0x4e24b0], eax
0045f6f2  b800010000             mov      eax, 0x100
0045f6f7  e8aa870000             call     0x467ea6 ; MemAlloc
0045f6fc  a3b4244e00             mov      dword ptr [0x4e24b4], eax
0045f701  b800010000             mov      eax, 0x100
0045f706  e89b870000             call     0x467ea6 ; MemAlloc
0045f70b  a3b8244e00             mov      dword ptr [0x4e24b8], eax
0045f710  b800010000             mov      eax, 0x100
0045f715  e88c870000             call     0x467ea6 ; MemAlloc
0045f71a  a3bc244e00             mov      dword ptr [0x4e24bc], eax
0045f71f  b800010000             mov      eax, 0x100
0045f724  e87d870000             call     0x467ea6 ; MemAlloc
0045f729  a3c0244e00             mov      dword ptr [0x4e24c0], eax
0045f72e  b800010000             mov      eax, 0x100
0045f733  31d2                   xor      edx, edx
0045f735  e86c870000             call     0x467ea6 ; MemAlloc
0045f73a  a3c4244e00             mov      dword ptr [0x4e24c4], eax
0045f73f  eb12                   jmp      0x45f753 ;
0045f741  b800010000             mov      eax, 0x100
0045f746  e85b870000             call     0x467ea6 ; MemAlloc
0045f74b  42                     inc      edx
0045f74c  89049dc8244e00         mov      dword ptr [ebx*4 + 0x4e24c8], eax
0045f753  31db                   xor      ebx, ebx
0045f755  6689d3                 mov      bx, dx
0045f758  83fb05                 cmp      ebx, 5
0045f75b  7ce4                   jl       0x45f741
0045f75d  5a                     pop      edx
0045f75e  5b                     pop      ebx
0045f75f  c3                     ret
