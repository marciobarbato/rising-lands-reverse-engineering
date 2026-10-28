; ValideHerse; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041ac8b  53                       push ebx
0041ac8c  51                       push ecx
0041ac8d  52                       push edx
0041ac8e  56                       push esi
0041ac8f  89c1                     mov ecx, eax
0041ac91  31db                     xor ebx, ebx
0041ac93  6689c3                   mov bx, ax
0041ac96  be00010000               mov esi, 0x100
0041ac9b  89da                     mov edx, ebx
0041ac9d  89d8                     mov eax, ebx
0041ac9f  c1fa1f                   sar edx, 0x1f
0041aca2  f7fe                     idiv esi
0041aca4  89d6                     mov esi, edx
0041aca6  89da                     mov edx, ebx
0041aca8  89d8                     mov eax, ebx
0041acaa  c1fa1f                   sar edx, 0x1f
0041acad  c1e208                   shl edx, 8
0041acb0  1bc2                     sbb eax, edx
0041acb2  c1f808                   sar eax, 8
0041acb5  31d2                     xor edx, edx
0041acb7  6689f2                   mov dx, si
0041acba  85d2                     test edx, edx
0041acbc  7e4f                     jle 0x41ad0d
0041acbe  8b15747d5000             mov edx, dword ptr [0x507d74]
0041acc4  01d3                     add ebx, edx
0041acc6  8a53ff                   mov dl, byte ptr [ebx - 1]
0041acc9  3a15f85b4900             cmp dl, byte ptr [0x495bf8]
0041accf  7408                     je 0x41acd9
0041acd1  3a15f95b4900             cmp dl, byte ptr [0x495bf9]
0041acd7  7534                     jne 0x41ad0d
0041acd9  31d2                     xor edx, edx
0041acdb  6689f2                   mov dx, si
0041acde  81fa00010000             cmp edx, 0x100
0041ace4  7d27                     jge 0x41ad0d
0041ace6  31d2                     xor edx, edx
0041ace8  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041acee  6689ca                   mov dx, cx
0041acf1  01d3                     add ebx, edx
0041acf3  8a5301                   mov dl, byte ptr [ebx + 1]
0041acf6  3a15f85b4900             cmp dl, byte ptr [0x495bf8]
0041acfc  7408                     je 0x41ad06
0041acfe  3a15f95b4900             cmp dl, byte ptr [0x495bf9]
0041ad04  7507                     jne 0x41ad0d
0041ad06  30c0                     xor al, al
0041ad08  5e                       pop esi
0041ad09  5a                       pop edx
0041ad0a  59                       pop ecx
0041ad0b  5b                       pop ebx
0041ad0c  c3                       ret
0041ad0d  31d2                     xor edx, edx
0041ad0f  6689c2                   mov dx, ax
0041ad12  85d2                     test edx, edx
0041ad14  7e5b                     jle 0x41ad71
0041ad16  31db                     xor ebx, ebx
0041ad18  8b15747d5000             mov edx, dword ptr [0x507d74]
0041ad1e  6689cb                   mov bx, cx
0041ad21  01d3                     add ebx, edx
0041ad23  8a9300ffffff             mov dl, byte ptr [ebx - 0x100]
0041ad29  3a15f85b4900             cmp dl, byte ptr [0x495bf8]
0041ad2f  7408                     je 0x41ad39
0041ad31  3a15f95b4900             cmp dl, byte ptr [0x495bf9]
0041ad37  7538                     jne 0x41ad71
0041ad39  25ffff0000               and eax, 0xffff
0041ad3e  3d00010000               cmp eax, 0x100
0041ad43  7d2c                     jge 0x41ad71
0041ad45  31c0                     xor eax, eax
0041ad47  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041ad4d  6689c8                   mov ax, cx
0041ad50  01c3                     add ebx, eax
0041ad52  8a0df85b4900             mov cl, byte ptr [0x495bf8]
0041ad58  8a8300010000             mov al, byte ptr [ebx + 0x100]
0041ad5e  38c8                     cmp al, cl
0041ad60  7408                     je 0x41ad6a
0041ad62  3a05f95b4900             cmp al, byte ptr [0x495bf9]
0041ad68  7507                     jne 0x41ad71
0041ad6a  b001                     mov al, 1
0041ad6c  5e                       pop esi
0041ad6d  5a                       pop edx
0041ad6e  59                       pop ecx
0041ad6f  5b                       pop ebx
0041ad70  c3                       ret
0041ad71  b0ff                     mov al, 0xff
0041ad73  5e                       pop esi
0041ad74  5a                       pop edx
0041ad75  59                       pop ecx
0041ad76  5b                       pop ebx
0041ad77  c3                       ret
