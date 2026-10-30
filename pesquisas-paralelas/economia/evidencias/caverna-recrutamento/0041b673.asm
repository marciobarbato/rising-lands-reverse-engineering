; BatimentSelection; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041b673  53                       push ebx
0041b674  51                       push ecx
0041b675  52                       push edx
0041b676  56                       push esi
0041b677  89c6                     mov esi, eax
0041b679  31d2                     xor edx, edx
0041b67b  6689c2                   mov dx, ax
0041b67e  89d0                     mov eax, edx
0041b680  c1e004                   shl eax, 4
0041b683  01d0                     add eax, edx
0041b685  c1e002                   shl eax, 2
0041b688  01d0                     add eax, edx
0041b68a  b9c8a04900               mov ecx, 0x49a0c8
0041b68f  c1e002                   shl eax, 2
0041b692  01c1                     add ecx, eax
0041b694  8a4108                   mov al, byte ptr [ecx + 8]
0041b697  25ff000000               and eax, 0xff
0041b69c  83f80c                   cmp eax, 0xc
0041b69f  7512                     jne 0x41b6b3
0041b6a1  31c0                     xor eax, eax
0041b6a3  8a4104                   mov al, byte ptr [ecx + 4]
0041b6a6  66893445e05b4900         mov word ptr [eax*2 + 0x495be0], si
0041b6ae  5e                       pop esi
0041b6af  5a                       pop edx
0041b6b0  59                       pop ecx
0041b6b1  5b                       pop ebx
0041b6b2  c3                       ret
0041b6b3  31c0                     xor eax, eax
0041b6b5  8a4105                   mov al, byte ptr [ecx + 5]
0041b6b8  85c0                     test eax, eax
0041b6ba  0f95c0                   setne al
0041b6bd  84c0                     test al, al
0041b6bf  0f84c5000000             je 0x41b78a
0041b6c5  31d2                     xor edx, edx
0041b6c7  6689f2                   mov dx, si
0041b6ca  89d0                     mov eax, edx
0041b6cc  c1e004                   shl eax, 4
0041b6cf  01d0                     add eax, edx
0041b6d1  c1e002                   shl eax, 2
0041b6d4  01d0                     add eax, edx
0041b6d6  bac8a04900               mov edx, 0x49a0c8
0041b6db  c1e002                   shl eax, 2
0041b6de  01c2                     add edx, eax
0041b6e0  31db                     xor ebx, ebx
0041b6e2  8a4208                   mov al, byte ptr [edx + 8]
0041b6e5  88c3                     mov bl, al
0041b6e7  8d420c                   lea eax, [edx + 0xc]
0041b6ea  83fb15                   cmp ebx, 0x15
0041b6ed  750d                     jne 0x41b6fc
0041b6ef  e856bb0200               call 0x44724a
0041b6f4  84c0                     test al, al
0041b6f6  7429                     je 0x41b721
0041b6f8  b001                     mov al, 1
0041b6fa  eb27                     jmp 0x41b723
0041b6fc  83fb02                   cmp ebx, 2
0041b6ff  7509                     jne 0x41b70a
0041b701  e844bb0200               call 0x44724a
0041b706  84c0                     test al, al
0041b708  75ee                     jne 0x41b6f8
0041b70a  8d420c                   lea eax, [edx + 0xc]
0041b70d  bb09000000               mov ebx, 9
0041b712  ba01000000               mov edx, 1
0041b717  e89cba0200               call 0x4471b8
0041b71c  6685c0                   test ax, ax
0041b71f  ebd5                     jmp 0x41b6f6
0041b721  30c0                     xor al, al
0041b723  84c0                     test al, al
0041b725  7463                     je 0x41b78a
0041b727  31c0                     xor eax, eax
0041b729  31db                     xor ebx, ebx
0041b72b  8a4104                   mov al, byte ptr [ecx + 4]
0041b72e  6689f3                   mov bx, si
0041b731  66893445e05b4900         mov word ptr [eax*2 + 0x495be0], si
0041b739  89d8                     mov eax, ebx
0041b73b  c1e004                   shl eax, 4
0041b73e  01d8                     add eax, ebx
0041b740  c1e002                   shl eax, 2
0041b743  01d8                     add eax, ebx
0041b745  b9c8a04900               mov ecx, 0x49a0c8
0041b74a  c1e002                   shl eax, 2
0041b74d  01c1                     add ecx, eax
0041b74f  8a4104                   mov al, byte ptr [ecx + 4]
0041b752  3a0541805000             cmp al, byte ptr [0x508041]
0041b758  7530                     jne 0x41b78a
0041b75a  89d8                     mov eax, ebx
0041b75c  e84ae9ffff               call 0x41a0ab
0041b761  83b900010000ff           cmp dword ptr [ecx + 0x100], -1
0041b768  7520                     jne 0x41b78a
0041b76a  50                       push eax
0041b76b  31c0                     xor eax, eax
0041b76d  8a4108                   mov al, byte ptr [ecx + 8]
0041b770  c1e010                   shl eax, 0x10
0041b773  8d9900010000             lea ebx, [ecx + 0x100]
0041b779  80cc08                   or ah, 8
0041b77c  31c9                     xor ecx, ecx
0041b77e  89c2                     mov edx, eax
0041b780  b842000000               mov eax, 0x42
0041b785  e8eff20600               call 0x48aa79
0041b78a  5e                       pop esi
0041b78b  5a                       pop edx
0041b78c  59                       pop ecx
0041b78d  5b                       pop ebx
0041b78e  c3                       ret
