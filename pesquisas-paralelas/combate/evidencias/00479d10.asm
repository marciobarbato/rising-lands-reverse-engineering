; LoadEngin; intervalo [0x00479d10, 0x00479d7f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00479d10  53                       push     ebx
00479d11  52                       push     edx
00479d12  83ec08                   sub      esp, 8
00479d15  ba3c4e4900               mov      edx, 0x494e3c
00479d1a  e801e7fdff               call     0x458420
00479d1f  25ff000000               and      eax, 0xff
00479d24  83f801                   cmp      eax, 1
00479d27  7545                     jne      0x479d6e
00479d29  ba02000000               mov      edx, 2
00479d2e  8d442404                 lea      eax, [esp + 4]
00479d32  e82ae7fdff               call     0x458461
00479d37  31db                     xor      ebx, ebx
00479d39  eb2a                     jmp      0x479d65
00479d3b  ba02000000               mov      edx, 2
00479d40  89e0                     mov      eax, esp
00479d42  e81ae7fdff               call     0x458461
00479d47  31c0                     xor      eax, eax
00479d49  668b0424                 mov      ax, word ptr [esp]
00479d4d  69d014010000             imul     edx, eax, 0x114
00479d53  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00479d58  01d0                     add      eax, edx
00479d5a  ba14010000               mov      edx, 0x114
00479d5f  43                       inc      ebx
00479d60  e8fce6fdff               call     0x458461
00479d65  663b5c2404               cmp      bx, word ptr [esp + 4]
00479d6a  7306                     jae      0x479d72
00479d6c  ebcd                     jmp      0x479d3b
00479d6e  30c0                     xor      al, al
00479d70  eb07                     jmp      0x479d79
00479d72  e8d5e6fdff               call     0x45844c
00479d77  b001                     mov      al, 1
00479d79  83c408                   add      esp, 8
00479d7c  5a                       pop      edx
00479d7d  5b                       pop      ebx
00479d7e  c3                       ret
