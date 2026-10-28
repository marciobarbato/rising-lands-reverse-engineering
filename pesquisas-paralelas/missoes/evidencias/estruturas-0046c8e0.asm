; MissionLoadName_inline_structures; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c8e0  ba02000000               mov edx, 2
0046c8e5  8d842408010000           lea eax, [esp + 0x108]
0046c8ec  e870bbfeff               call 0x458461
0046c8f1  ba02000000               mov edx, 2
0046c8f6  8d842414010000           lea eax, [esp + 0x114]
0046c8fd  31db                     xor ebx, ebx
0046c8ff  eb31                     jmp 0x46c932
0046c901  ba02000000               mov edx, 2
0046c906  8d842410010000           lea eax, [esp + 0x110]
0046c90d  e84fbbfeff               call 0x458461
0046c912  31c0                     xor eax, eax
0046c914  668b842410010000         mov ax, word ptr [esp + 0x110]
0046c91c  69c014010000             imul eax, eax, 0x114
0046c922  31d2                     xor edx, edx
0046c924  668b942414010000         mov dx, word ptr [esp + 0x114]
0046c92c  05c8a04900               add eax, 0x49a0c8
0046c931  43                       inc ebx
0046c932  e82abbfeff               call 0x458461
0046c937  663b9c2408010000         cmp bx, word ptr [esp + 0x108]
0046c93f  72c0                     jb 0x46c901
