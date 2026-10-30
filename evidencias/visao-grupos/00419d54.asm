; BatimentDecouvre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419d54  53                       push ebx
00419d55  51                       push ecx
00419d56  56                       push esi
00419d57  57                       push edi
00419d58  83ec18                   sub esp, 0x18
00419d5b  88542414                 mov byte ptr [esp + 0x14], dl
00419d5f  31d2                     xor edx, edx
00419d61  6689c2                   mov dx, ax
00419d64  89d0                     mov eax, edx
00419d66  c1e004                   shl eax, 4
00419d69  01d0                     add eax, edx
00419d6b  c1e002                   shl eax, 2
00419d6e  01d0                     add eax, edx
00419d70  b9c8a04900               mov ecx, 0x49a0c8
00419d75  c1e002                   shl eax, 2
00419d78  01c1                     add ecx, eax
00419d7a  31c0                     xor eax, eax
00419d7c  8a442414                 mov al, byte ptr [esp + 0x14]
00419d80  3dc8000000               cmp eax, 0xc8
00419d85  0f84b8feffff             je 0x419c43
00419d8b  8a4108                   mov al, byte ptr [ecx + 8]
00419d8e  31d2                     xor edx, edx
00419d90  88c2                     mov dl, al
00419d92  89d0                     mov eax, edx
00419d94  c1e002                   shl eax, 2
00419d97  29d0                     sub eax, edx
00419d99  c1e002                   shl eax, 2
00419d9c  01c2                     add edx, eax
00419d9e  c1e202                   shl edx, 2
00419da1  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
00419da8  8944240c                 mov dword ptr [esp + 0xc], eax
00419dac  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
00419db3  31db                     xor ebx, ebx
00419db5  890424                   mov dword ptr [esp], eax
00419db8  668b5902                 mov bx, word ptr [ecx + 2]
00419dbc  be00010000               mov esi, 0x100
00419dc1  89da                     mov edx, ebx
00419dc3  89d8                     mov eax, ebx
00419dc5  c1fa1f                   sar edx, 0x1f
00419dc8  f7fe                     idiv esi
00419dca  89d7                     mov edi, edx
00419dcc  89da                     mov edx, ebx
00419dce  89d8                     mov eax, ebx
00419dd0  c1fa1f                   sar edx, 0x1f
00419dd3  f7fe                     idiv esi
00419dd5  6689442408               mov word ptr [esp + 8], ax
00419dda  31c0                     xor eax, eax
00419ddc  668b44240c               mov ax, word ptr [esp + 0xc]
00419de1  39f0                     cmp eax, esi
00419de3  7d07                     jge 0x419dec
00419de5  89c2                     mov edx, eax
00419de7  42                       inc edx
00419de8  8954240c                 mov dword ptr [esp + 0xc], edx
00419dec  31c0                     xor eax, eax
00419dee  668b0424                 mov ax, word ptr [esp]
00419df2  3d00010000               cmp eax, 0x100
00419df7  7d06                     jge 0x419dff
00419df9  89c3                     mov ebx, eax
00419dfb  43                       inc ebx
00419dfc  891c24                   mov dword ptr [esp], ebx
00419dff  beffffffff               mov esi, 0xffffffff
00419e04  b800ff0000               mov eax, 0xff00
00419e09  6689742410               mov word ptr [esp + 0x10], si
00419e0e  6689442404               mov word ptr [esp + 4], ax
00419e13  eb14                     jmp 0x419e29
00419e15  8a642405                 mov ah, byte ptr [esp + 5]
00419e19  8b542410                 mov edx, dword ptr [esp + 0x10]
00419e1d  fec4                     inc ah
00419e1f  42                       inc edx
00419e20  88642405                 mov byte ptr [esp + 5], ah
00419e24  6689542410               mov word ptr [esp + 0x10], dx
00419e29  31d2                     xor edx, edx
00419e2b  8b44240e                 mov eax, dword ptr [esp + 0xe]
00419e2f  668b1424                 mov dx, word ptr [esp]
00419e33  c1f810                   sar eax, 0x10
00419e36  39d0                     cmp eax, edx
00419e38  0f8d05feffff             jge 0x419c43
00419e3e  8b542406                 mov edx, dword ptr [esp + 6]
00419e42  c1fa10                   sar edx, 0x10
00419e45  01d0                     add eax, edx
00419e47  85c0                     test eax, eax
00419e49  7cca                     jl 0x419e15
00419e4b  3d00010000               cmp eax, 0x100
00419e50  7dc3                     jge 0x419e15
00419e52  bbffffffff               mov ebx, 0xffffffff
00419e57  8b742404                 mov esi, dword ptr [esp + 4]
00419e5b  eb01                     jmp 0x419e5e
00419e5d  43                       inc ebx
00419e5e  31c0                     xor eax, eax
00419e60  0fbfd3                   movsx edx, bx
00419e63  668b44240c               mov ax, word ptr [esp + 0xc]
00419e68  39c2                     cmp edx, eax
00419e6a  7da9                     jge 0x419e15
00419e6c  0fbfc7                   movsx eax, di
00419e6f  01c2                     add edx, eax
00419e71  85d2                     test edx, edx
00419e73  7ce8                     jl 0x419e5d
00419e75  81fa00010000             cmp edx, 0x100
00419e7b  7de0                     jge 0x419e5d
00419e7d  668b4102                 mov ax, word ptr [ecx + 2]
00419e81  31d2                     xor edx, edx
00419e83  01d8                     add eax, ebx
00419e85  8a542414                 mov dl, byte ptr [esp + 0x14]
00419e89  01f0                     add eax, esi
00419e8b  25ffff0000               and eax, 0xffff
00419e90  e875c80500               call 0x47670a
00419e95  ebc6                     jmp 0x419e5d
