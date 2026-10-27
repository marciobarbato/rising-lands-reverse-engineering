; ProjectileInit; intervalo [0x0046e44c, 0x0046e4ca)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046e44c  56                       push     esi
0046e44d  57                       push     edi
0046e44e  83ec04                   sub      esp, 4
0046e451  880424                   mov      byte ptr [esp], al
0046e454  89d7                     mov      edi, edx
0046e456  89de                     mov      esi, ebx
0046e458  31c0                     xor      eax, eax
0046e45a  31d2                     xor      edx, edx
0046e45c  6689c2                   mov      dx, ax
0046e45f  83fa64                   cmp      edx, 0x64
0046e462  7d14                     jge      0x46e478
0046e464  6bda38                   imul     ebx, edx, 0x38
0046e467  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046e46d  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046e471  84d2                     test     dl, dl
0046e473  7403                     je       0x46e478
0046e475  40                       inc      eax
0046e476  ebe2                     jmp      0x46e45a
0046e478  25ffff0000               and      eax, 0xffff
0046e47d  83f864                   cmp      eax, 0x64
0046e480  7440                     je       0x46e4c2
0046e482  31d2                     xor      edx, edx
0046e484  8a542420                 mov      dl, byte ptr [esp + 0x20]
0046e488  52                       push     edx
0046e489  8b54241e                 mov      edx, dword ptr [esp + 0x1e]
0046e48d  c1fa10                   sar      edx, 0x10
0046e490  52                       push     edx
0046e491  8b54241e                 mov      edx, dword ptr [esp + 0x1e]
0046e495  c1fa10                   sar      edx, 0x10
0046e498  52                       push     edx
0046e499  31d2                     xor      edx, edx
0046e49b  8a542420                 mov      dl, byte ptr [esp + 0x20]
0046e49f  52                       push     edx
0046e4a0  31d2                     xor      edx, edx
0046e4a2  668b542420               mov      dx, word ptr [esp + 0x20]
0046e4a7  52                       push     edx
0046e4a8  31d2                     xor      edx, edx
0046e4aa  31db                     xor      ebx, ebx
0046e4ac  88ca                     mov      dl, cl
0046e4ae  6689fb                   mov      bx, di
0046e4b1  52                       push     edx
0046e4b2  31c9                     xor      ecx, ecx
0046e4b4  31d2                     xor      edx, edx
0046e4b6  6689f1                   mov      cx, si
0046e4b9  8a542418                 mov      dl, byte ptr [esp + 0x18]
0046e4bd  e846fdffff               call     0x46e208
0046e4c2  83c404                   add      esp, 4
0046e4c5  5f                       pop      edi
0046e4c6  5e                       pop      esi
0046e4c7  c21400                   ret      0x14
