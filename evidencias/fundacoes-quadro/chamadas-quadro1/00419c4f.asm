00419c4f  53                   push ebx
00419c50  51                   push ecx
00419c51  56                   push esi
00419c52  57                   push edi
00419c53  83ec18               sub esp, 0x18
00419c56  88542414             mov byte ptr [esp + 0x14], dl
00419c5a  31d2                 xor edx, edx
00419c5c  6689c2               mov dx, ax
00419c5f  89d0                 mov eax, edx
00419c61  c1e004               shl eax, 4
00419c64  01d0                 add eax, edx
00419c66  c1e002               shl eax, 2
00419c69  01d0                 add eax, edx
00419c6b  b9c8a04900           mov ecx, 0x49a0c8
00419c70  c1e002               shl eax, 2
00419c73  01c1                 add ecx, eax
00419c75  31d2                 xor edx, edx
00419c77  8a4108               mov al, byte ptr [ecx + 8]
00419c7a  88c2                 mov dl, al
00419c7c  89d0                 mov eax, edx
00419c7e  c1e002               shl eax, 2
00419c81  29d0                 sub eax, edx
00419c83  c1e002               shl eax, 2
00419c86  01c2                 add edx, eax
00419c88  c1e202               shl edx, 2
00419c8b  668b828c5d4900       mov ax, word ptr [edx + 0x495d8c]
00419c92  890424               mov dword ptr [esp], eax
00419c95  668b828e5d4900       mov ax, word ptr [edx + 0x495d8e]
00419c9c  31db                 xor ebx, ebx
00419c9e  89442410             mov dword ptr [esp + 0x10], eax
00419ca2  668b5902             mov bx, word ptr [ecx + 2]
00419ca6  be00010000           mov esi, 0x100
00419cab  89da                 mov edx, ebx
00419cad  89d8                 mov eax, ebx
00419caf  c1fa1f               sar edx, 0x1f
00419cb2  f7fe                 idiv esi
00419cb4  89d7                 mov edi, edx
00419cb6  89da                 mov edx, ebx
00419cb8  89d8                 mov eax, ebx
00419cba  c1fa1f               sar edx, 0x1f
00419cbd  f7fe                 idiv esi
00419cbf  31d2                 xor edx, edx
00419cc1  89442404             mov dword ptr [esp + 4], eax
00419cc5  8954240c             mov dword ptr [esp + 0xc], edx
00419cc9  6689542408           mov word ptr [esp + 8], dx
00419cce  eb13                 jmp 0x419ce3
00419cd0  8a642409             mov ah, byte ptr [esp + 9]
00419cd4  8b54240c             mov edx, dword ptr [esp + 0xc]
00419cd8  fec4                 inc ah
00419cda  42                   inc edx
00419cdb  88642409             mov byte ptr [esp + 9], ah
00419cdf  8954240c             mov dword ptr [esp + 0xc], edx
00419ce3  8b44240c             mov eax, dword ptr [esp + 0xc]
00419ce7  663b442410           cmp ax, word ptr [esp + 0x10]
00419cec  0f8359ffffff         jae 0x419c4b
00419cf2  31c0                 xor eax, eax
00419cf4  31d2                 xor edx, edx
00419cf6  668b442404           mov ax, word ptr [esp + 4]
00419cfb  668b54240c           mov dx, word ptr [esp + 0xc]
00419d00  01d0                 add eax, edx
00419d02  85c0                 test eax, eax
00419d04  7cca                 jl 0x419cd0
00419d06  3d00010000           cmp eax, 0x100
00419d0b  7dc3                 jge 0x419cd0
00419d0d  8b742408             mov esi, dword ptr [esp + 8]
00419d11  31db                 xor ebx, ebx
00419d13  eb01                 jmp 0x419d16
00419d15  43                   inc ebx
00419d16  663b1c24             cmp bx, word ptr [esp]
00419d1a  73b4                 jae 0x419cd0
00419d1c  31d2                 xor edx, edx
00419d1e  31c0                 xor eax, eax
00419d20  6689fa               mov dx, di
00419d23  6689d8               mov ax, bx
00419d26  01d0                 add eax, edx
00419d28  85c0                 test eax, eax
00419d2a  7ce9                 jl 0x419d15
00419d2c  3d00010000           cmp eax, 0x100
00419d31  7de2                 jge 0x419d15
00419d33  668b4102             mov ax, word ptr [ecx + 2]
00419d37  31d2                 xor edx, edx
00419d39  01d8                 add eax, ebx
00419d3b  8a542414             mov dl, byte ptr [esp + 0x14]
00419d3f  01f0                 add eax, esi
00419d41  25ffff0000           and eax, 0xffff
00419d46  e88bc90500           call 0x4766d6
00419d4b  84c0                 test al, al
00419d4d  74c6                 je 0x419d15
00419d4f  e9ebfeffff           jmp 0x419c3f
