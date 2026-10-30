; BatimentGetCapacite; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041f3ed  52                       push edx
0041f3ee  31d2                     xor edx, edx
0041f3f0  6689c2                   mov dx, ax
0041f3f3  89d0                     mov eax, edx
0041f3f5  c1e004                   shl eax, 4
0041f3f8  01d0                     add eax, edx
0041f3fa  c1e002                   shl eax, 2
0041f3fd  01d0                     add eax, edx
0041f3ff  bac8a04900               mov edx, 0x49a0c8
0041f404  c1e002                   shl eax, 2
0041f407  01c2                     add edx, eax
0041f409  8a4208                   mov al, byte ptr [edx + 8]
0041f40c  3c0e                     cmp al, 0xe
0041f40e  7240                     jb 0x41f450
0041f410  7623                     jbe 0x41f435
0041f412  3c13                     cmp al, 0x13
0041f414  753a                     jne 0x41f450
0041f416  31d2                     xor edx, edx
0041f418  88c2                     mov dl, al
0041f41a  89d0                     mov eax, edx
0041f41c  c1e002                   shl eax, 2
0041f41f  29d0                     sub eax, edx
0041f421  c1e002                   shl eax, 2
0041f424  01d0                     add eax, edx
0041f426  8a04859e5d4900           mov al, byte ptr [eax*4 + 0x495d9e]
0041f42d  2a05e85b4900             sub al, byte ptr [0x495be8]
0041f433  5a                       pop edx
0041f434  c3                       ret
0041f435  31d2                     xor edx, edx
0041f437  88c2                     mov dl, al
0041f439  89d0                     mov eax, edx
0041f43b  c1e002                   shl eax, 2
0041f43e  29d0                     sub eax, edx
0041f440  c1e002                   shl eax, 2
0041f443  01d0                     add eax, edx
0041f445  8a04859e5d4900           mov al, byte ptr [eax*4 + 0x495d9e]
0041f44c  fec8                     dec al
0041f44e  5a                       pop edx
0041f44f  c3                       ret
0041f450  8a5208                   mov dl, byte ptr [edx + 8]
0041f453  81e2ff000000             and edx, 0xff
0041f459  89d0                     mov eax, edx
0041f45b  c1e002                   shl eax, 2
0041f45e  29d0                     sub eax, edx
0041f460  c1e002                   shl eax, 2
0041f463  01d0                     add eax, edx
0041f465  8a04859e5d4900           mov al, byte ptr [eax*4 + 0x495d9e]
0041f46c  5a                       pop edx
0041f46d  c3                       ret
