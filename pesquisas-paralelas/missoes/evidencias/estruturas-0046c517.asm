; MissionLoad_inline_structures; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046c517  ba02000000               mov edx, 2
0046c51c  8d84241c010000           lea eax, [esp + 0x11c]
0046c523  e839bffeff               call 0x458461
0046c528  ba02000000               mov edx, 2
0046c52d  8d842414010000           lea eax, [esp + 0x114]
0046c534  31db                     xor ebx, ebx
0046c536  eb31                     jmp 0x46c569
0046c538  ba02000000               mov edx, 2
0046c53d  8d842420010000           lea eax, [esp + 0x120]
0046c544  e818bffeff               call 0x458461
0046c549  31c0                     xor eax, eax
0046c54b  668b842420010000         mov ax, word ptr [esp + 0x120]
0046c553  69c014010000             imul eax, eax, 0x114
0046c559  31d2                     xor edx, edx
0046c55b  668b942414010000         mov dx, word ptr [esp + 0x114]
0046c563  05c8a04900               add eax, 0x49a0c8
0046c568  43                       inc ebx
0046c569  e8f3befeff               call 0x458461
0046c56e  663b9c241c010000         cmp bx, word ptr [esp + 0x11c]
0046c576  72c0                     jb 0x46c538
