; PlaceLibre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041f552  53                       push ebx
0041f553  51                       push ecx
0041f554  56                       push esi
0041f555  57                       push edi
0041f556  83ec0c                   sub esp, 0xc
0041f559  50                       push eax
0041f55a  52                       push edx
0041f55b  31c0                     xor eax, eax
0041f55d  668b442404               mov ax, word ptr [esp + 4]
0041f562  89c2                     mov edx, eax
0041f564  c1e204                   shl edx, 4
0041f567  01c2                     add edx, eax
0041f569  c1e202                   shl edx, 2
0041f56c  01c2                     add edx, eax
0041f56e  b9c8a04900               mov ecx, 0x49a0c8
0041f573  c1e202                   shl edx, 2
0041f576  01d1                     add ecx, edx
0041f578  8a4108                   mov al, byte ptr [ecx + 8]
0041f57b  31d2                     xor edx, edx
0041f57d  88c2                     mov dl, al
0041f57f  8d410c                   lea eax, [ecx + 0xc]
0041f582  83fa08                   cmp edx, 8
0041f585  7530                     jne 0x41f5b7
0041f587  31d2                     xor edx, edx
0041f589  e8797b0200               call 0x447107
0041f58e  8a15e95b4900             mov dl, byte ptr [0x495be9]
0041f594  89c3                     mov ebx, eax
0041f596  89d0                     mov eax, edx
0041f598  c1fa1f                   sar edx, 0x1f
0041f59b  2bc2                     sub eax, edx
0041f59d  d1f8                     sar eax, 1
0041f59f  31d2                     xor edx, edx
0041f5a1  40                       inc eax
0041f5a2  6689da                   mov dx, bx
0041f5a5  39c2                     cmp edx, eax
0041f5a7  0f9cc0                   setl al
0041f5aa  84c0                     test al, al
0041f5ac  0f8593010000             jne 0x41f745
0041f5b2  e9ae010000               jmp 0x41f765
0041f5b7  83fa13                   cmp edx, 0x13
0041f5ba  0f8597010000             jne 0x41f757
0041f5c0  31d2                     xor edx, edx
0041f5c2  668b1424                 mov dx, word ptr [esp]
0041f5c6  89d0                     mov eax, edx
0041f5c8  e8bd7b0300               call 0x45718a
0041f5cd  89c3                     mov ebx, eax
0041f5cf  89d0                     mov eax, edx
0041f5d1  e8321b0200               call 0x441108
0041f5d6  6639c3                   cmp bx, ax
0041f5d9  7515                     jne 0x41f5f0
0041f5db  89d0                     mov eax, edx
0041f5dd  e8432a0200               call 0x442025
0041f5e2  25ff000000               and eax, 0xff
0041f5e7  83f809                   cmp eax, 9
0041f5ea  0f8575010000             jne 0x41f765
0041f5f0  83c10c                   add ecx, 0xc
0041f5f3  ba01000000               mov edx, 1
0041f5f8  89c8                     mov eax, ecx
0041f5fa  e8d37a0200               call 0x4470d2
0041f5ff  84c0                     test al, al
0041f601  0f845e010000             je 0x41f765
0041f607  89c8                     mov eax, ecx
0041f609  e8f97a0200               call 0x447107
0041f60e  31ff                     xor edi, edi
0041f610  31f6                     xor esi, esi
0041f612  897c2410                 mov dword ptr [esp + 0x10], edi
0041f616  89442408                 mov dword ptr [esp + 8], eax
0041f61a  eb09                     jmp 0x41f625
0041f61c  8b7c240c                 mov edi, dword ptr [esp + 0xc]
0041f620  eb02                     jmp 0x41f624
0041f622  89c7                     mov edi, eax
0041f624  46                       inc esi
0041f625  663b742408               cmp si, word ptr [esp + 8]
0041f62a  7357                     jae 0x41f683
0041f62c  31db                     xor ebx, ebx
0041f62e  6689f3                   mov bx, si
0041f631  89c8                     mov eax, ecx
0041f633  89da                     mov edx, ebx
0041f635  e8997c0200               call 0x4472d3
0041f63a  31d2                     xor edx, edx
0041f63c  88c2                     mov dl, al
0041f63e  83fa01                   cmp edx, 1
0041f641  75e1                     jne 0x41f624
0041f643  89da                     mov edx, ebx
0041f645  89c8                     mov eax, ecx
0041f647  e8927c0200               call 0x4472de
0041f64c  31d2                     xor edx, edx
0041f64e  6689c2                   mov dx, ax
0041f651  89d0                     mov eax, edx
0041f653  31db                     xor ebx, ebx
0041f655  e8cb290200               call 0x442025
0041f65a  88c3                     mov bl, al
0041f65c  89f8                     mov eax, edi
0041f65e  40                       inc eax
0041f65f  8944240c                 mov dword ptr [esp + 0xc], eax
0041f663  83fb09                   cmp ebx, 9
0041f666  75ba                     jne 0x41f622
0041f668  89d0                     mov eax, edx
0041f66a  e81b7b0300               call 0x45718a
0041f66f  89c3                     mov ebx, eax
0041f671  89d0                     mov eax, edx
0041f673  e8901a0200               call 0x441108
0041f678  6639c3                   cmp bx, ax
0041f67b  759f                     jne 0x41f61c
0041f67d  ff442410                 inc dword ptr [esp + 0x10]
0041f681  eba1                     jmp 0x41f624
0041f683  31d2                     xor edx, edx
0041f685  668b1424                 mov dx, word ptr [esp]
0041f689  89d0                     mov eax, edx
0041f68b  e895290200               call 0x442025
0041f690  25ff000000               and eax, 0xff
0041f695  83f809                   cmp eax, 9
0041f698  0f85ab000000             jne 0x41f749
0041f69e  89d0                     mov eax, edx
0041f6a0  e8e57a0300               call 0x45718a
0041f6a5  89c3                     mov ebx, eax
0041f6a7  89d0                     mov eax, edx
0041f6a9  e85a1a0200               call 0x441108
0041f6ae  6639c3                   cmp bx, ax
0041f6b1  7441                     je 0x41f6f4
0041f6b3  e991000000               jmp 0x41f749
0041f6b8  25ff000000               and eax, 0xff
0041f6bd  89c2                     mov edx, eax
0041f6bf  c1e202                   shl edx, 2
0041f6c2  29c2                     sub edx, eax
0041f6c4  c1e202                   shl edx, 2
0041f6c7  01c2                     add edx, eax
0041f6c9  8a04959e5d4900           mov al, byte ptr [edx*4 + 0x495d9e]
0041f6d0  2a05e85b4900             sub al, byte ptr [0x495be8]
0041f6d6  eb5d                     jmp 0x41f735
0041f6d8  25ff000000               and eax, 0xff
0041f6dd  89c2                     mov edx, eax
0041f6df  c1e202                   shl edx, 2
0041f6e2  29c2                     sub edx, eax
0041f6e4  c1e202                   shl edx, 2
0041f6e7  01c2                     add edx, eax
0041f6e9  8a04959e5d4900           mov al, byte ptr [edx*4 + 0x495d9e]
0041f6f0  fec8                     dec al
0041f6f2  eb41                     jmp 0x41f735
0041f6f4  31c0                     xor eax, eax
0041f6f6  668b442404               mov ax, word ptr [esp + 4]
0041f6fb  89c2                     mov edx, eax
0041f6fd  c1e204                   shl edx, 4
0041f700  01c2                     add edx, eax
0041f702  c1e202                   shl edx, 2
0041f705  01c2                     add edx, eax
0041f707  c1e202                   shl edx, 2
0041f70a  81c2c8a04900             add edx, 0x49a0c8
0041f710  8a4208                   mov al, byte ptr [edx + 8]
0041f713  3c0e                     cmp al, 0xe
0041f715  7206                     jb 0x41f71d
0041f717  76bf                     jbe 0x41f6d8
0041f719  3c13                     cmp al, 0x13
0041f71b  749b                     je 0x41f6b8
0041f71d  31c0                     xor eax, eax
0041f71f  8a4208                   mov al, byte ptr [edx + 8]
0041f722  89c2                     mov edx, eax
0041f724  c1e202                   shl edx, 2
0041f727  29c2                     sub edx, eax
0041f729  c1e202                   shl edx, 2
0041f72c  01c2                     add edx, eax
0041f72e  8a04959e5d4900           mov al, byte ptr [edx*4 + 0x495d9e]
0041f735  31d2                     xor edx, edx
0041f737  25ff000000               and eax, 0xff
0041f73c  668b542410               mov dx, word ptr [esp + 0x10]
0041f741  39c2                     cmp edx, eax
0041f743  7d20                     jge 0x41f765
0041f745  b201                     mov dl, 1
0041f747  eb1e                     jmp 0x41f767
0041f749  31c0                     xor eax, eax
0041f74b  31d2                     xor edx, edx
0041f74d  a0e85b4900               mov al, byte ptr [0x495be8]
0041f752  6689fa                   mov dx, di
0041f755  ebea                     jmp 0x41f741
0041f757  ba01000000               mov edx, 1
0041f75c  e871790200               call 0x4470d2
0041f761  84c0                     test al, al
0041f763  75e0                     jne 0x41f745
0041f765  30d2                     xor dl, dl
0041f767  88d0                     mov al, dl
0041f769  e9e6a8ffff               jmp 0x41a054
