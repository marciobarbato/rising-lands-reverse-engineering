; call site 0x45efe2..0x45f041 (ProcessInputGame tag 6); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045efe2  31c0                     xor eax, eax
0045efe4  8a0424                   mov al, byte ptr [esp]
0045efe7  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045efee  31d2                     xor edx, edx
0045eff0  668b5002                 mov dx, word ptr [eax + 2]
0045eff4  31c0                     xor eax, eax
0045eff6  8a0424                   mov al, byte ptr [esp]
0045eff9  e826430100               call 0x473324
0045effe  31c0                     xor eax, eax
0045f000  8a0424                   mov al, byte ptr [esp]
0045f003  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f00a  31c9                     xor ecx, ecx
0045f00c  8a4808                   mov cl, byte ptr [eax + 8]
0045f00f  31c0                     xor eax, eax
0045f011  8a0424                   mov al, byte ptr [esp]
0045f014  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f01b  31db                     xor ebx, ebx
0045f01d  668b5806                 mov bx, word ptr [eax + 6]
0045f021  31c0                     xor eax, eax
0045f023  8a0424                   mov al, byte ptr [esp]
0045f026  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f02d  31d2                     xor edx, edx
0045f02f  8a5004                   mov dl, byte ptr [eax + 4]
0045f032  31c0                     xor eax, eax
0045f034  8a0424                   mov al, byte ptr [esp]
0045f037  e8f0400100               call 0x47312c
0045f03c  e99d020000               jmp 0x45f2de
