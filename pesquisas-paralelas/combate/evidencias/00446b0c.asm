; ContactCellule; intervalo [0x00446b0c, 0x00446c94)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00446b0c  53                       push     ebx
00446b0d  51                       push     ecx
00446b0e  56                       push     esi
00446b0f  57                       push     edi
00446b10  83ec14                   sub      esp, 0x14
00446b13  89d6                     mov      esi, edx
00446b15  31c9                     xor      ecx, ecx
00446b17  6689c1                   mov      cx, ax
00446b1a  89c8                     mov      eax, ecx
00446b1c  c1e004                   shl      eax, 4
00446b1f  01c8                     add      eax, ecx
00446b21  c1e002                   shl      eax, 2
00446b24  01c8                     add      eax, ecx
00446b26  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00446b2c  c1e002                   shl      eax, 2
00446b2f  01c2                     add      edx, eax
00446b31  8b8283000000             mov      eax, dword ptr [edx + 0x83]
00446b37  c1f818                   sar      eax, 0x18
00446b3a  85c0                     test     eax, eax
00446b3c  0f8548010000             jne      0x446c8a
00446b42  8b8284000000             mov      eax, dword ptr [edx + 0x84]
00446b48  c1f818                   sar      eax, 0x18
00446b4b  85c0                     test     eax, eax
00446b4d  741d                     je       0x446b6c
00446b4f  e936010000               jmp      0x446c8a
00446b54  66c7010100               mov      word ptr [ecx], 1
00446b59  66c7070100               mov      word ptr [edi], 1
00446b5e  eb29                     jmp      0x446b89
00446b60  66c7010200               mov      word ptr [ecx], 2
00446b65  66c7070200               mov      word ptr [edi], 2
00446b6a  eb1d                     jmp      0x446b89
00446b6c  8d4c2404                 lea      ecx, [esp + 4]
00446b70  89e7                     mov      edi, esp
00446b72  8a4201                   mov      al, byte ptr [edx + 1]
00446b75  668b5a08                 mov      bx, word ptr [edx + 8]
00446b79  3c19                     cmp      al, 0x19
00446b7b  770c                     ja       0x446b89
00446b7d  31d2                     xor      edx, edx
00446b7f  88c2                     mov      dl, al
00446b81  2eff2495a46a4400         jmp      dword ptr cs:[edx*4 + 0x446aa4]
00446b89  8b0424                   mov      eax, dword ptr [esp]
00446b8c  48                       dec      eax
00446b8d  8b542404                 mov      edx, dword ptr [esp + 4]
00446b91  c1e008                   shl      eax, 8
00446b94  01d0                     add      eax, edx
00446b96  48                       dec      eax
00446b97  31c9                     xor      ecx, ecx
00446b99  29c3                     sub      ebx, eax
00446b9b  6689d9                   mov      cx, bx
00446b9e  bf00010000               mov      edi, 0x100
00446ba3  89ca                     mov      edx, ecx
00446ba5  89c8                     mov      eax, ecx
00446ba7  c1fa1f                   sar      edx, 0x1f
00446baa  f7ff                     idiv     edi
00446bac  89d7                     mov      edi, edx
00446bae  89ca                     mov      edx, ecx
00446bb0  89c8                     mov      eax, ecx
00446bb2  c1fa1f                   sar      edx, 0x1f
00446bb5  c1e208                   shl      edx, 8
00446bb8  1bc2                     sbb      eax, edx
00446bba  c1f808                   sar      eax, 8
00446bbd  89c2                     mov      edx, eax
00446bbf  31c0                     xor      eax, eax
00446bc1  6689f8                   mov      ax, di
00446bc4  85c0                     test     eax, eax
00446bc6  7403                     je       0x446bcb
00446bc8  4b                       dec      ebx
00446bc9  eb04                     jmp      0x446bcf
00446bcb  ff4c2404                 dec      dword ptr [esp + 4]
00446bcf  31c0                     xor      eax, eax
00446bd1  6689d0                   mov      ax, dx
00446bd4  85c0                     test     eax, eax
00446bd6  7408                     je       0x446be0
00446bd8  81eb00010000             sub      ebx, 0x100
00446bde  eb03                     jmp      0x446be3
00446be0  ff0c24                   dec      dword ptr [esp]
00446be3  31c9                     xor      ecx, ecx
00446be5  6689d9                   mov      cx, bx
00446be8  bf00010000               mov      edi, 0x100
00446bed  89ca                     mov      edx, ecx
00446bef  89c8                     mov      eax, ecx
00446bf1  c1fa1f                   sar      edx, 0x1f
00446bf4  f7ff                     idiv     edi
00446bf6  89d7                     mov      edi, edx
00446bf8  89ca                     mov      edx, ecx
00446bfa  89c8                     mov      eax, ecx
00446bfc  c1fa1f                   sar      edx, 0x1f
00446bff  c1e208                   shl      edx, 8
00446c02  1bc2                     sbb      eax, edx
00446c04  c1f808                   sar      eax, 8
00446c07  8944240c                 mov      dword ptr [esp + 0xc], eax
00446c0b  31c0                     xor      eax, eax
00446c0d  8b542404                 mov      edx, dword ptr [esp + 4]
00446c11  89442410                 mov      dword ptr [esp + 0x10], eax
00446c15  b800010000               mov      eax, 0x100
00446c1a  29d0                     sub      eax, edx
00446c1c  83e802                   sub      eax, 2
00446c1f  89442408                 mov      dword ptr [esp + 8], eax
00446c23  eb0f                     jmp      0x446c34
00446c25  8b442410                 mov      eax, dword ptr [esp + 0x10]
00446c29  8b4c2408                 mov      ecx, dword ptr [esp + 8]
00446c2d  40                       inc      eax
00446c2e  01cb                     add      ebx, ecx
00446c30  89442410                 mov      dword ptr [esp + 0x10], eax
00446c34  31c9                     xor      ecx, ecx
00446c36  31d2                     xor      edx, edx
00446c38  668b0c24                 mov      cx, word ptr [esp]
00446c3c  668b542410               mov      dx, word ptr [esp + 0x10]
00446c41  83c102                   add      ecx, 2
00446c44  39ca                     cmp      edx, ecx
00446c46  7d42                     jge      0x446c8a
00446c48  31c9                     xor      ecx, ecx
00446c4a  668b4c240c               mov      cx, word ptr [esp + 0xc]
00446c4f  01ca                     add      edx, ecx
00446c51  81fa00010000             cmp      edx, 0x100
00446c57  7dcc                     jge      0x446c25
00446c59  31c0                     xor      eax, eax
00446c5b  eb02                     jmp      0x446c5f
00446c5d  43                       inc      ebx
00446c5e  40                       inc      eax
00446c5f  31c9                     xor      ecx, ecx
00446c61  31d2                     xor      edx, edx
00446c63  668b4c2404               mov      cx, word ptr [esp + 4]
00446c68  6689c2                   mov      dx, ax
00446c6b  83c102                   add      ecx, 2
00446c6e  39ca                     cmp      edx, ecx
00446c70  7db3                     jge      0x446c25
00446c72  31c9                     xor      ecx, ecx
00446c74  6689f9                   mov      cx, di
00446c77  01ca                     add      edx, ecx
00446c79  81fa00010000             cmp      edx, 0x100
00446c7f  7ddc                     jge      0x446c5d
00446c81  6639f3                   cmp      bx, si
00446c84  75d7                     jne      0x446c5d
00446c86  b001                     mov      al, 1
00446c88  eb02                     jmp      0x446c8c
00446c8a  30c0                     xor      al, al
00446c8c  83c414                   add      esp, 0x14
00446c8f  5f                       pop      edi
00446c90  5e                       pop      esi
00446c91  59                       pop      ecx
00446c92  5b                       pop      ebx
00446c93  c3                       ret
