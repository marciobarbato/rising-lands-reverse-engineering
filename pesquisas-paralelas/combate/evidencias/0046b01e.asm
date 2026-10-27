; LoadEnginGame; intervalo [0x0046b01e, 0x0046b119)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046b01e  53                       push     ebx
0046b01f  51                       push     ecx
0046b020  52                       push     edx
0046b021  83ec0c                   sub      esp, 0xc
0046b024  e82c750000               call     0x472555
0046b029  b332                     mov      bl, 0x32
0046b02b  31d2                     xor      edx, edx
0046b02d  eb07                     jmp      0x46b036
0046b02f  42                       inc      edx
0046b030  8898bc194e00             mov      byte ptr [eax + 0x4e19bc], bl
0046b036  31c0                     xor      eax, eax
0046b038  6689d0                   mov      ax, dx
0046b03b  83f804                   cmp      eax, 4
0046b03e  7cef                     jl       0x46b02f
0046b040  ba02000000               mov      edx, 2
0046b045  8d442404                 lea      eax, [esp + 4]
0046b049  e813d4feff               call     0x458461
0046b04e  ba02000000               mov      edx, 2
0046b053  8d442408                 lea      eax, [esp + 8]
0046b057  31db                     xor      ebx, ebx
0046b059  e803d4feff               call     0x458461
0046b05e  e980000000               jmp      0x46b0e3
0046b063  ba02000000               mov      edx, 2
0046b068  89e0                     mov      eax, esp
0046b06a  e8f2d3feff               call     0x458461
0046b06f  31c0                     xor      eax, eax
0046b071  668b0424                 mov      ax, word ptr [esp]
0046b075  69c014010000             imul     eax, eax, 0x114
0046b07b  31d2                     xor      edx, edx
0046b07d  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
0046b083  668b542408               mov      dx, word ptr [esp + 8]
0046b088  01c8                     add      eax, ecx
0046b08a  e8d2d3feff               call     0x458461
0046b08f  31c0                     xor      eax, eax
0046b091  668b0424                 mov      ax, word ptr [esp]
0046b095  69d014010000             imul     edx, eax, 0x114
0046b09b  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0046b0a0  c68402bd00000000         mov      byte ptr [edx + eax + 0xbd], 0
0046b0a8  31c0                     xor      eax, eax
0046b0aa  668b0424                 mov      ax, word ptr [esp]
0046b0ae  69c014010000             imul     eax, eax, 0x114
0046b0b4  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0046b0ba  c784021001000000000000   mov      dword ptr [edx + eax + 0x110], 0
0046b0c5  31c0                     xor      eax, eax
0046b0c7  668b0424                 mov      ax, word ptr [esp]
0046b0cb  69c014010000             imul     eax, eax, 0x114
0046b0d1  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0046b0d7  43                       inc      ebx
0046b0d8  c7840204010000ffffffff   mov      dword ptr [edx + eax + 0x104], 0xffffffff
0046b0e3  663b5c2404               cmp      bx, word ptr [esp + 4]
0046b0e8  0f8275ffffff             jb       0x46b063
0046b0ee  31db                     xor      ebx, ebx
0046b0f0  eb14                     jmp      0x46b106
0046b0f2  8b1524194e00             mov      edx, dword ptr [0x4e1924]
0046b0f8  8b0482                   mov      eax, dword ptr [edx + eax*4]
0046b0fb  ba00020000               mov      edx, 0x200
0046b100  43                       inc      ebx
0046b101  e85bd3feff               call     0x458461
0046b106  31c0                     xor      eax, eax
0046b108  6689d8                   mov      ax, bx
0046b10b  3d20030000               cmp      eax, 0x320
0046b110  7ce0                     jl       0x46b0f2
0046b112  83c40c                   add      esp, 0xc
0046b115  5a                       pop      edx
0046b116  59                       pop      ecx
0046b117  5b                       pop      ebx
0046b118  c3                       ret
