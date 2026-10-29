; BatimentTailleGet; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041a996  51                       push ecx
0041a997  89c1                     mov ecx, eax
0041a999  81e3ff000000             and ebx, 0xff
0041a99f  89d8                     mov eax, ebx
0041a9a1  c1e002                   shl eax, 2
0041a9a4  29d8                     sub eax, ebx
0041a9a6  c1e002                   shl eax, 2
0041a9a9  01d8                     add eax, ebx
0041a9ab  668b1c858c5d4900         mov bx, word ptr [eax*4 + 0x495d8c]
0041a9b3  668919                   mov word ptr [ecx], bx
0041a9b6  668b04858e5d4900         mov ax, word ptr [eax*4 + 0x495d8e]
0041a9be  668902                   mov word ptr [edx], ax
0041a9c1  59                       pop ecx
0041a9c2  c3                       ret
