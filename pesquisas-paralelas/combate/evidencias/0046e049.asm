; ProjectileLineaire; intervalo [0x0046e049, 0x0046e17f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e049  53                       push     ebx
0046e04a  51                       push     ecx
0046e04b  52                       push     edx
0046e04c  56                       push     esi
0046e04d  57                       push     edi
0046e04e  83ec18                   sub      esp, 0x18
0046e051  89c3                     mov      ebx, eax
0046e053  be00010000               mov      esi, 0x100
0046e058  668b400c                 mov      ax, word ptr [eax + 0xc]
0046e05c  31c9                     xor      ecx, ecx
0046e05e  6689442414               mov      word ptr [esp + 0x14], ax
0046e063  668b4b16                 mov      cx, word ptr [ebx + 0x16]
0046e067  668b430e                 mov      ax, word ptr [ebx + 0xe]
0046e06b  89ca                     mov      edx, ecx
0046e06d  6689442408               mov      word ptr [esp + 8], ax
0046e072  c1fa1f                   sar      edx, 0x1f
0046e075  89c8                     mov      eax, ecx
0046e077  f7fe                     idiv     esi
0046e079  c1e205                   shl      edx, 5
0046e07c  83c210                   add      edx, 0x10
0046e07f  89d6                     mov      esi, edx
0046e081  89ca                     mov      edx, ecx
0046e083  89c8                     mov      eax, ecx
0046e085  c1fa1f                   sar      edx, 0x1f
0046e088  c1e208                   shl      edx, 8
0046e08b  1bc2                     sbb      eax, edx
0046e08d  c1f808                   sar      eax, 8
0046e090  89f1                     mov      ecx, esi
0046e092  8b742408                 mov      esi, dword ptr [esp + 8]
0046e096  c1e005                   shl      eax, 5
0046e099  8b542414                 mov      edx, dword ptr [esp + 0x14]
0046e09d  83c010                   add      eax, 0x10
0046e0a0  29d1                     sub      ecx, edx
0046e0a2  89c2                     mov      edx, eax
0046e0a4  0fbfc1                   movsx    eax, cx
0046e0a7  29f2                     sub      edx, esi
0046e0a9  85c0                     test     eax, eax
0046e0ab  7d0f                     jge      0x46e0bc
0046e0ad  b8ffffffff               mov      eax, 0xffffffff
0046e0b2  f7d9                     neg      ecx
0046e0b4  8944240c                 mov      dword ptr [esp + 0xc], eax
0046e0b8  89c7                     mov      edi, eax
0046e0ba  eb09                     jmp      0x46e0c5
0046e0bc  bf01000000               mov      edi, 1
0046e0c1  897c240c                 mov      dword ptr [esp + 0xc], edi
0046e0c5  0fbfc2                   movsx    eax, dx
0046e0c8  85c0                     test     eax, eax
0046e0ca  7d0f                     jge      0x46e0db
0046e0cc  b800e0ffff               mov      eax, 0xffffe000
0046e0d1  f7da                     neg      edx
0046e0d3  89442410                 mov      dword ptr [esp + 0x10], eax
0046e0d7  89c6                     mov      esi, eax
0046e0d9  eb09                     jmp      0x46e0e4
0046e0db  be00200000               mov      esi, 0x2000
0046e0e0  89742410                 mov      dword ptr [esp + 0x10], esi
0046e0e4  6639d1                   cmp      cx, dx
0046e0e7  7e06                     jle      0x46e0ef
0046e0e9  89c8                     mov      eax, ecx
0046e0eb  31f6                     xor      esi, esi
0046e0ed  eb06                     jmp      0x46e0f5
0046e0ef  89d0                     mov      eax, edx
0046e0f1  31ff                     xor      edi, edi
0046e0f3  89ca                     mov      edx, ecx
0046e0f5  8b4c240c                 mov      ecx, dword ptr [esp + 0xc]
0046e0f9  01fe                     add      esi, edi
0046e0fb  034c2410                 add      ecx, dword ptr [esp + 0x10]
0046e0ff  01d2                     add      edx, edx
0046e101  894c2404                 mov      dword ptr [esp + 4], ecx
0046e105  89d1                     mov      ecx, edx
0046e107  66894334                 mov      word ptr [ebx + 0x34], ax
0046e10b  29c1                     sub      ecx, eax
0046e10d  89d7                     mov      edi, edx
0046e10f  890c24                   mov      dword ptr [esp], ecx
0046e112  89c1                     mov      ecx, eax
0046e114  6689732c                 mov      word ptr [ebx + 0x2c], si
0046e118  01c1                     add      ecx, eax
0046e11a  66895332                 mov      word ptr [ebx + 0x32], dx
0046e11e  29cf                     sub      edi, ecx
0046e120  8b4c2404                 mov      ecx, dword ptr [esp + 4]
0046e124  66894b2a                 mov      word ptr [ebx + 0x2a], cx
0046e128  8b4c2406                 mov      ecx, dword ptr [esp + 6]
0046e12c  8b742412                 mov      esi, dword ptr [esp + 0x12]
0046e130  c1f910                   sar      ecx, 0x10
0046e133  c1fe10                   sar      esi, 0x10
0046e136  c1e10d                   shl      ecx, 0xd
0046e139  66897b30                 mov      word ptr [ebx + 0x30], di
0046e13d  01f1                     add      ecx, esi
0046e13f  8a5323                   mov      dl, byte ptr [ebx + 0x23]
0046e142  894b08                   mov      dword ptr [ebx + 8], ecx
0046e145  8b0c24                   mov      ecx, dword ptr [esp]
0046e148  66894b2e                 mov      word ptr [ebx + 0x2e], cx
0046e14c  84d2                     test     dl, dl
0046e14e  7427                     je       0x46e177
0046e150  6685c0                   test     ax, ax
0046e153  7415                     je       0x46e16a
0046e155  0fbfc8                   movsx    ecx, ax
0046e158  b800320000               mov      eax, 0x3200
0046e15d  89c2                     mov      edx, eax
0046e15f  c1fa1f                   sar      edx, 0x1f
0046e162  f7f9                     idiv     ecx
0046e164  66894328                 mov      word ptr [ebx + 0x28], ax
0046e168  eb06                     jmp      0x46e170
0046e16a  66c743280032             mov      word ptr [ebx + 0x28], 0x3200
0046e170  c7432400000000           mov      dword ptr [ebx + 0x24], 0
0046e177  83c418                   add      esp, 0x18
0046e17a  e98a1a0000               jmp      0x46fc09
