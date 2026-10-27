; EnginAPorteeMinimale; intervalo [0x00446eed, 0x00446fbf)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00446eed  51                       push     ecx
00446eee  56                       push     esi
00446eef  57                       push     edi
00446ef0  55                       push     ebp
00446ef1  83ec04                   sub      esp, 4
00446ef4  89df                     mov      edi, ebx
00446ef6  31db                     xor      ebx, ebx
00446ef8  6689c3                   mov      bx, ax
00446efb  89d8                     mov      eax, ebx
00446efd  c1e004                   shl      eax, 4
00446f00  01d8                     add      eax, ebx
00446f02  c1e002                   shl      eax, 2
00446f05  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
00446f0b  01d8                     add      eax, ebx
00446f0d  668b448608               mov      ax, word ptr [esi + eax*4 + 8]
00446f12  890424                   mov      dword ptr [esp], eax
00446f15  31c0                     xor      eax, eax
00446f17  88d0                     mov      al, dl
00446f19  83f801                   cmp      eax, 1
00446f1c  0f8593000000             jne      0x446fb5
00446f22  31db                     xor      ebx, ebx
00446f24  6689fb                   mov      bx, di
00446f27  89d8                     mov      eax, ebx
00446f29  c1e004                   shl      eax, 4
00446f2c  01d8                     add      eax, ebx
00446f2e  c1e002                   shl      eax, 2
00446f31  01d8                     add      eax, ebx
00446f33  c1e002                   shl      eax, 2
00446f36  01f0                     add      eax, esi
00446f38  8a5001                   mov      dl, byte ptr [eax + 1]
00446f3b  81e2ff000000             and      edx, 0xff
00446f41  83fa10                   cmp      edx, 0x10
00446f44  756f                     jne      0x446fb5
00446f46  668b407c                 mov      ax, word ptr [eax + 0x7c]
00446f4a  31db                     xor      ebx, ebx
00446f4c  6689c3                   mov      bx, ax
00446f4f  89da                     mov      edx, ebx
00446f51  89d8                     mov      eax, ebx
00446f53  c1fa1f                   sar      edx, 0x1f
00446f56  c1e208                   shl      edx, 8
00446f59  1bc2                     sbb      eax, edx
00446f5b  c1f808                   sar      eax, 8
00446f5e  31c9                     xor      ecx, ecx
00446f60  be00010000               mov      esi, 0x100
00446f65  6689c1                   mov      cx, ax
00446f68  89da                     mov      edx, ebx
00446f6a  89d8                     mov      eax, ebx
00446f6c  c1fa1f                   sar      edx, 0x1f
00446f6f  f7fe                     idiv     esi
00446f71  31db                     xor      ebx, ebx
00446f73  31f6                     xor      esi, esi
00446f75  668b1c24                 mov      bx, word ptr [esp]
00446f79  6689d6                   mov      si, dx
00446f7c  89da                     mov      edx, ebx
00446f7e  89d8                     mov      eax, ebx
00446f80  c1fa1f                   sar      edx, 0x1f
00446f83  c1e208                   shl      edx, 8
00446f86  1bc2                     sbb      eax, edx
00446f88  c1f808                   sar      eax, 8
00446f8b  31ff                     xor      edi, edi
00446f8d  bd00010000               mov      ebp, 0x100
00446f92  6689c7                   mov      di, ax
00446f95  89da                     mov      edx, ebx
00446f97  89d8                     mov      eax, ebx
00446f99  c1fa1f                   sar      edx, 0x1f
00446f9c  f7fd                     idiv     ebp
00446f9e  31c0                     xor      eax, eax
00446fa0  89f3                     mov      ebx, esi
00446fa2  6689d0                   mov      ax, dx
00446fa5  89fa                     mov      edx, edi
00446fa7  e8a9250300               call     0x479555
00446fac  83f804                   cmp      eax, 4
00446faf  7704                     ja       0x446fb5
00446fb1  30c0                     xor      al, al
00446fb3  eb02                     jmp      0x446fb7
00446fb5  b001                     mov      al, 1
00446fb7  83c404                   add      esp, 4
00446fba  5d                       pop      ebp
00446fbb  5f                       pop      edi
00446fbc  5e                       pop      esi
00446fbd  59                       pop      ecx
00446fbe  c3                       ret
