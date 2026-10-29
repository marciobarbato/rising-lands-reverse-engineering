; EnginOccupeCase; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044246e  51                       push ecx
0044246f  56                       push esi
00442470  57                       push edi
00442471  88df                     mov bh, bl
00442473  31c9                     xor ecx, ecx
00442475  6689c1                   mov cx, ax
00442478  89c8                     mov eax, ecx
0044247a  c1e004                   shl eax, 4
0044247d  01c8                     add eax, ecx
0044247f  c1e002                   shl eax, 2
00442482  01c1                     add ecx, eax
00442484  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00442489  c1e102                   shl ecx, 2
0044248c  01c8                     add eax, ecx
0044248e  b301                     mov bl, 1
00442490  668b4808                 mov cx, word ptr [eax + 8]
00442494  0fb6b8ab000000           movzx edi, byte ptr [eax + 0xab]
0044249b  668b707c                 mov si, word ptr [eax + 0x7c]
0044249f  85ff                     test edi, edi
004424a1  7408                     je 0x4424ab
004424a3  0fb6ff                   movzx edi, bh
004424a6  83ff01                   cmp edi, 1
004424a9  7413                     je 0x4424be
004424ab  0fb6b8ab000000           movzx edi, byte ptr [eax + 0xab]
004424b2  85ff                     test edi, edi
004424b4  750e                     jne 0x4424c4
004424b6  0fb6ff                   movzx edi, bh
004424b9  83ff02                   cmp edi, 2
004424bc  7506                     jne 0x4424c4
004424be  30c0                     xor al, al
004424c0  5f                       pop edi
004424c1  5e                       pop esi
004424c2  59                       pop ecx
004424c3  c3                       ret
004424c4  0fb67802                 movzx edi, byte ptr [eax + 2]
004424c8  83ff0e                   cmp edi, 0xe
004424cb  0f8502000000             jne 0x4424d3
004424d1  ebeb                     jmp 0x4424be
004424d3  8a4001                   mov al, byte ptr [eax + 1]
004424d6  3c0e                     cmp al, 0xe
004424d8  7238                     jb 0x442512
004424da  7646                     jbe 0x442522
004424dc  3c12                     cmp al, 0x12
004424de  7217                     jb 0x4424f7
004424e0  761b                     jbe 0x4424fd
004424e2  3c14                     cmp al, 0x14
004424e4  7217                     jb 0x4424fd
004424e6  3c16                     cmp al, 0x16
004424e8  7613                     jbe 0x4424fd
004424ea  3c18                     cmp al, 0x18
004424ec  760f                     jbe 0x4424fd
004424ee  3c19                     cmp al, 0x19
004424f0  7430                     je 0x442522
004424f2  e97c000000               jmp 0x442573
004424f7  3c10                     cmp al, 0x10
004424f9  7227                     jb 0x442522
004424fb  7625                     jbe 0x442522
004424fd  6639d1                   cmp cx, dx
00442500  7409                     je 0x44250b
00442502  6639d6                   cmp si, dx
00442505  0f8566000000             jne 0x442571
0044250b  b301                     mov bl, 1
0044250d  e961000000               jmp 0x442573
00442512  3c06                     cmp al, 6
00442514  0f825f000000             jb 0x442579
0044251a  3c08                     cmp al, 8
0044251c  76df                     jbe 0x4424fd
0044251e  3c0b                     cmp al, 0xb
00442520  72db                     jb 0x4424fd
00442522  6639d1                   cmp cx, dx
00442525  74e4                     je 0x44250b
00442527  31db                     xor ebx, ebx
00442529  31c0                     xor eax, eax
0044252b  6689cb                   mov bx, cx
0044252e  6689d0                   mov ax, dx
00442531  8d4bff                   lea ecx, [ebx - 1]
00442534  39c1                     cmp ecx, eax
00442536  74d3                     je 0x44250b
00442538  8d8bfffeffff             lea ecx, [ebx - 0x101]
0044253e  39c1                     cmp ecx, eax
00442540  74c9                     je 0x44250b
00442542  81eb00010000             sub ebx, 0x100
00442548  39c3                     cmp ebx, eax
0044254a  74bf                     je 0x44250b
0044254c  6639d6                   cmp si, dx
0044254f  74ba                     je 0x44250b
00442551  31d2                     xor edx, edx
00442553  6689f2                   mov dx, si
00442556  8d5aff                   lea ebx, [edx - 1]
00442559  39c3                     cmp ebx, eax
0044255b  74ae                     je 0x44250b
0044255d  8d9afffeffff             lea ebx, [edx - 0x101]
00442563  39c3                     cmp ebx, eax
00442565  74a4                     je 0x44250b
00442567  81ea00010000             sub edx, 0x100
0044256d  39c2                     cmp edx, eax
0044256f  749a                     je 0x44250b
00442571  30db                     xor bl, bl
00442573  88d8                     mov al, bl
00442575  5f                       pop edi
00442576  5e                       pop esi
00442577  59                       pop ecx
00442578  c3                       ret
00442579  3c03                     cmp al, 3
0044257b  0f837affffff             jae 0x4424fb
00442581  e977ffffff               jmp 0x4424fd
