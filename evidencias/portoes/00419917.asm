; ChercheEtatHerse; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419917  53                       push ebx
00419918  51                       push ecx
00419919  89c1                     mov ecx, eax
0041991b  31db                     xor ebx, ebx
0041991d  6689d3                   mov bx, dx
00419920  89d8                     mov eax, ebx
00419922  c1e004                   shl eax, 4
00419925  01d8                     add eax, ebx
00419927  c1e002                   shl eax, 2
0041992a  01d8                     add eax, ebx
0041992c  c1e002                   shl eax, 2
0041992f  05c8a04900               add eax, 0x49a0c8
00419934  8a4076                   mov al, byte ptr [eax + 0x76]
00419937  25ff000000               and eax, 0xff
0041993c  740e                     je 0x41994c
0041993e  83f80f                   cmp eax, 0xf
00419941  7409                     je 0x41994c
00419943  83f81f                   cmp eax, 0x1f
00419946  7404                     je 0x41994c
00419948  b001                     mov al, 1
0041994a  eb02                     jmp 0x41994e
0041994c  30c0                     xor al, al
0041994e  84c0                     test al, al
00419950  754e                     jne 0x4199a0
00419952  31db                     xor ebx, ebx
00419954  6689d3                   mov bx, dx
00419957  89d8                     mov eax, ebx
00419959  c1e004                   shl eax, 4
0041995c  01d8                     add eax, ebx
0041995e  c1e002                   shl eax, 2
00419961  01d8                     add eax, ebx
00419963  c1e002                   shl eax, 2
00419966  05c8a04900               add eax, 0x49a0c8
0041996b  8a4076                   mov al, byte ptr [eax + 0x76]
0041996e  25ff000000               and eax, 0xff
00419973  83f80f                   cmp eax, 0xf
00419976  0f94c0                   sete al
00419979  84c0                     test al, al
0041997b  7413                     je 0x419990
0041997d  31c0                     xor eax, eax
0041997f  81e2ffff0000             and edx, 0xffff
00419985  6689c8                   mov ax, cx
00419988  e83dfcffff               call 0x4195ca
0041998d  59                       pop ecx
0041998e  5b                       pop ebx
0041998f  c3                       ret
00419990  31c0                     xor eax, eax
00419992  81e2ffff0000             and edx, 0xffff
00419998  6689c8                   mov ax, cx
0041999b  e834faffff               call 0x4193d4
004199a0  59                       pop ecx
004199a1  5b                       pop ebx
004199a2  c3                       ret
