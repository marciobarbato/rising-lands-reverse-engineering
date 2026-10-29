; BatimentConstruit; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041c652  53                       push ebx
0041c653  52                       push edx
0041c654  31d2                     xor edx, edx
0041c656  6689c2                   mov dx, ax
0041c659  89d0                     mov eax, edx
0041c65b  c1e004                   shl eax, 4
0041c65e  01d0                     add eax, edx
0041c660  c1e002                   shl eax, 2
0041c663  01d0                     add eax, edx
0041c665  bac8a04900               mov edx, 0x49a0c8
0041c66a  c1e002                   shl eax, 2
0041c66d  01c2                     add edx, eax
0041c66f  31db                     xor ebx, ebx
0041c671  8a5a08                   mov bl, byte ptr [edx + 8]
0041c674  89d8                     mov eax, ebx
0041c676  c1e002                   shl eax, 2
0041c679  29d8                     sub eax, ebx
0041c67b  c1e002                   shl eax, 2
0041c67e  01d8                     add eax, ebx
0041c680  668b520a                 mov dx, word ptr [edx + 0xa]
0041c684  663b1485905d4900         cmp dx, word ptr [eax*4 + 0x495d90]
0041c68c  0f94c0                   sete al
0041c68f  5a                       pop edx
0041c690  5b                       pop ebx
0041c691  c3                       ret
