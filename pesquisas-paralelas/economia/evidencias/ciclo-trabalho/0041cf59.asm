; BatimentConstruction; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041cf59  53                       push ebx
0041cf5a  51                       push ecx
0041cf5b  52                       push edx
0041cf5c  56                       push esi
0041cf5d  57                       push edi
0041cf5e  89c7                     mov edi, eax
0041cf60  31db                     xor ebx, ebx
0041cf62  6689c3                   mov bx, ax
0041cf65  89d8                     mov eax, ebx
0041cf67  c1e004                   shl eax, 4
0041cf6a  01d8                     add eax, ebx
0041cf6c  c1e002                   shl eax, 2
0041cf6f  01d8                     add eax, ebx
0041cf71  bec8a04900               mov esi, 0x49a0c8
0041cf76  c1e002                   shl eax, 2
0041cf79  01c6                     add esi, eax
0041cf7b  668b560a                 mov dx, word ptr [esi + 0xa]
0041cf7f  83c202                   add edx, 2
0041cf82  8a4604                   mov al, byte ptr [esi + 4]
0041cf85  6689560a                 mov word ptr [esi + 0xa], dx
0041cf89  3a0541805000             cmp al, byte ptr [0x508041]
0041cf8f  7530                     jne 0x41cfc1
0041cf91  89d8                     mov eax, ebx
0041cf93  e813d1ffff               call 0x41a0ab
0041cf98  83be00010000ff           cmp dword ptr [esi + 0x100], -1
0041cf9f  7520                     jne 0x41cfc1
0041cfa1  50                       push eax
0041cfa2  31c0                     xor eax, eax
0041cfa4  8a4608                   mov al, byte ptr [esi + 8]
0041cfa7  c1e010                   shl eax, 0x10
0041cfaa  8d9e00010000             lea ebx, [esi + 0x100]
0041cfb0  80cc25                   or ah, 0x25
0041cfb3  31c9                     xor ecx, ecx
0041cfb5  89c2                     mov edx, eax
0041cfb7  b842000000               mov eax, 0x42
0041cfbc  e8b8da0600               call 0x48aa79
0041cfc1  31d2                     xor edx, edx
0041cfc3  8a5608                   mov dl, byte ptr [esi + 8]
0041cfc6  89d0                     mov eax, edx
0041cfc8  c1e002                   shl eax, 2
0041cfcb  29d0                     sub eax, edx
0041cfcd  c1e002                   shl eax, 2
0041cfd0  01d0                     add eax, edx
0041cfd2  c1e002                   shl eax, 2
0041cfd5  668b560a                 mov dx, word ptr [esi + 0xa]
0041cfd9  668b98905d4900           mov bx, word ptr [eax + 0x495d90]
0041cfe0  6639da                   cmp dx, bx
0041cfe3  0f82350b0000             jb 0x41db1e
0041cfe9  c6460505                 mov byte ptr [esi + 5], 5
0041cfed  31c0                     xor eax, eax
0041cfef  8a4608                   mov al, byte ptr [esi + 8]
0041cff2  66895e0a                 mov word ptr [esi + 0xa], bx
0041cff6  83f811                   cmp eax, 0x11
0041cff9  750c                     jne 0x41d007
0041cffb  31c0                     xor eax, eax
0041cffd  6689f8                   mov ax, di
0041d000  e86bfcffff               call 0x41cc70
0041d005  eb10                     jmp 0x41d017
0041d007  83f809                   cmp eax, 9
0041d00a  750b                     jne 0x41d017
0041d00c  31c0                     xor eax, eax
0041d00e  668b4602                 mov ax, word ptr [esi + 2]
0041d012  e83af2ffff               call 0x41c251
0041d017  31c0                     xor eax, eax
0041d019  ba01000000               mov edx, 1
0041d01e  6689f8                   mov ax, di
0041d021  e871ceffff               call 0x419e97
0041d026  e9f30a0000               jmp 0x41db1e
