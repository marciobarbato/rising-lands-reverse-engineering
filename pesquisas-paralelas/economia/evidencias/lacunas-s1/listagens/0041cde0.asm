; BatimentInitTechnologie; intact EXE 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb; exclusive end 0x41cec4
0041cde0  53                       push     ebx
0041cde1  51                       push     ecx
0041cde2  52                       push     edx
0041cde3  56                       push     esi
0041cde4  57                       push     edi
0041cde5  83ec10                   sub      esp, 0x10
0041cde8  31ff                     xor      edi, edi
0041cdea  eb01                     jmp      0x41cded
0041cdec  47                       inc      edi
0041cded  31c0                     xor      eax, eax
0041cdef  6689f8                   mov      ax, di
0041cdf2  3de8030000               cmp      eax, 0x3e8
0041cdf7  0f8d45e7ffff             jge      0x41b542
0041cdfd  69c014010000             imul     eax, eax, 0x114
0041ce03  bac8a04900               mov      edx, 0x49a0c8
0041ce08  01c2                     add      edx, eax
0041ce0a  31c0                     xor      eax, eax
0041ce0c  8a4205                   mov      al, byte ptr [edx + 5]
0041ce0f  85c0                     test     eax, eax
0041ce11  0f95c0                   setne    al
0041ce14  84c0                     test     al, al
0041ce16  74d4                     je       0x41cdec
0041ce18  31d2                     xor      edx, edx
0041ce1a  6689fa                   mov      dx, di
0041ce1d  69d214010000             imul     edx, edx, 0x114
0041ce23  81c2c8a04900             add      edx, 0x49a0c8
0041ce29  8a4208                   mov      al, byte ptr [edx + 8]
0041ce2c  25ff000000               and      eax, 0xff
0041ce31  83f803                   cmp      eax, 3
0041ce34  7564                     jne      0x41ce9a
0041ce36  8a4204                   mov      al, byte ptr [edx + 4]
0041ce39  31d2                     xor      edx, edx
0041ce3b  88c2                     mov      dl, al
0041ce3d  83fa04                   cmp      edx, 4
0041ce40  7d58                     jge      0x41ce9a
0041ce42  6bf206                   imul     esi, edx, 6
0041ce45  31c0                     xor      eax, eax
0041ce47  668b862cfb4d00           mov      ax, word ptr [esi + 0x4dfb2c]
0041ce4e  85c0                     test     eax, eax
0041ce50  7e48                     jle      0x41ce9a
0041ce52  8d4c240c                 lea      ecx, [esp + 0xc]
0041ce56  89e3                     mov      ebx, esp
0041ce58  52                       push     edx
0041ce59  8d44240c                 lea      eax, [esp + 0xc]
0041ce5d  8d542408                 lea      edx, [esp + 8]
0041ce61  e837a80400               call     0x46769d
0041ce66  8b442408                 mov      eax, dword ptr [esp + 8]
0041ce6a  8b542404                 mov      edx, dword ptr [esp + 4]
0041ce6e  668b9e2cfb4d00           mov      bx, word ptr [esi + 0x4dfb2c]
0041ce75  01d0                     add      eax, edx
0041ce77  31d2                     xor      edx, edx
0041ce79  66f7f3                   div      bx
0041ce7c  31d2                     xor      edx, edx
0041ce7e  6689c2                   mov      dx, ax
0041ce81  6bd207                   imul     edx, edx, 7
0041ce84  31db                     xor      ebx, ebx
0041ce86  668b9e2efb4d00           mov      bx, word ptr [esi + 0x4dfb2e]
0041ce8d  89d0                     mov      eax, edx
0041ce8f  c1fa1f                   sar      edx, 0x1f
0041ce92  f7fb                     idiv     ebx
0041ce94  888630fb4d00             mov      byte ptr [esi + 0x4dfb30], al
0041ce9a  31f6                     xor      esi, esi
0041ce9c  6689fe                   mov      si, di
0041ce9f  69f614010000             imul     esi, esi, 0x114
0041cea5  81c6c8a04900             add      esi, 0x49a0c8
0041ceab  31d2                     xor      edx, edx
0041cead  8a4608                   mov      al, byte ptr [esi + 8]
0041ceb0  88c2                     mov      dl, al
0041ceb2  8a4604                   mov      al, byte ptr [esi + 4]
0041ceb5  25ff000000               and      eax, 0xff
0041ceba  e8adf8ffff               call     0x41c76c
0041cebf  e928ffffff               jmp      0x41cdec
