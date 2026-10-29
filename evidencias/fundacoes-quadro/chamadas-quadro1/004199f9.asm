004199f9  53                   push ebx
004199fa  51                   push ecx
004199fb  56                   push esi
004199fc  57                   push edi
004199fd  83ec1c               sub esp, 0x1c
00419a00  88542418             mov byte ptr [esp + 0x18], dl
00419a04  31d2                 xor edx, edx
00419a06  6689c2               mov dx, ax
00419a09  89d0                 mov eax, edx
00419a0b  c1e004               shl eax, 4
00419a0e  01d0                 add eax, edx
00419a10  c1e002               shl eax, 2
00419a13  01d0                 add eax, edx
00419a15  bec8a04900           mov esi, 0x49a0c8
00419a1a  c1e002               shl eax, 2
00419a1d  01c6                 add esi, eax
00419a1f  31d2                 xor edx, edx
00419a21  8a4608               mov al, byte ptr [esi + 8]
00419a24  88c2                 mov dl, al
00419a26  89d0                 mov eax, edx
00419a28  c1e002               shl eax, 2
00419a2b  29d0                 sub eax, edx
00419a2d  c1e002               shl eax, 2
00419a30  01c2                 add edx, eax
00419a32  c1e202               shl edx, 2
00419a35  668b828c5d4900       mov ax, word ptr [edx + 0x495d8c]
00419a3c  31c9                 xor ecx, ecx
00419a3e  89442408             mov dword ptr [esp + 8], eax
00419a42  668b828e5d4900       mov ax, word ptr [edx + 0x495d8e]
00419a49  8b542408             mov edx, dword ptr [esp + 8]
00419a4d  89442404             mov dword ptr [esp + 4], eax
00419a51  89c3                 mov ebx, eax
00419a53  42                   inc edx
00419a54  43                   inc ebx
00419a55  89542408             mov dword ptr [esp + 8], edx
00419a59  895c2404             mov dword ptr [esp + 4], ebx
00419a5d  668b4e02             mov cx, word ptr [esi + 2]
00419a61  bb00010000           mov ebx, 0x100
00419a66  89ca                 mov edx, ecx
00419a68  89c8                 mov eax, ecx
00419a6a  c1fa1f               sar edx, 0x1f
00419a6d  f7fb                 idiv ebx
00419a6f  89542410             mov dword ptr [esp + 0x10], edx
00419a73  89ca                 mov edx, ecx
00419a75  89c8                 mov eax, ecx
00419a77  c1fa1f               sar edx, 0x1f
00419a7a  f7fb                 idiv ebx
00419a7c  b900ff0000           mov ecx, 0xff00
00419a81  bfffffffff           mov edi, 0xffffffff
00419a86  66894c240c           mov word ptr [esp + 0xc], cx
00419a8b  89442414             mov dword ptr [esp + 0x14], eax
00419a8f  eb0b                 jmp 0x419a9c
00419a91  8a64240d             mov ah, byte ptr [esp + 0xd]
00419a95  fec4                 inc ah
00419a97  47                   inc edi
00419a98  8864240d             mov byte ptr [esp + 0xd], ah
00419a9c  31d2                 xor edx, edx
00419a9e  0fbfc7               movsx eax, di
00419aa1  668b542404           mov dx, word ptr [esp + 4]
00419aa6  39d0                 cmp eax, edx
00419aa8  0f8d87000000         jge 0x419b35
00419aae  31d2                 xor edx, edx
00419ab0  668b542414           mov dx, word ptr [esp + 0x14]
00419ab5  01d0                 add eax, edx
00419ab7  85c0                 test eax, eax
00419ab9  7cd6                 jl 0x419a91
00419abb  3d00010000           cmp eax, 0x100
00419ac0  7dcf                 jge 0x419a91
00419ac2  8b44240c             mov eax, dword ptr [esp + 0xc]
00419ac6  bbffffffff           mov ebx, 0xffffffff
00419acb  890424               mov dword ptr [esp], eax
00419ace  eb01                 jmp 0x419ad1
00419ad0  43                   inc ebx
00419ad1  31d2                 xor edx, edx
00419ad3  0fbfc3               movsx eax, bx
00419ad6  668b542408           mov dx, word ptr [esp + 8]
00419adb  39d0                 cmp eax, edx
00419add  7db2                 jge 0x419a91
00419adf  31c9                 xor ecx, ecx
00419ae1  668b4c2410           mov cx, word ptr [esp + 0x10]
00419ae6  01c1                 add ecx, eax
00419ae8  85c9                 test ecx, ecx
00419aea  7ce4                 jl 0x419ad0
00419aec  81f900010000         cmp ecx, 0x100
00419af2  7ddc                 jge 0x419ad0
00419af4  83f8ff               cmp eax, -1
00419af7  7419                 je 0x419b12
00419af9  4a                   dec edx
00419afa  39d0                 cmp eax, edx
00419afc  7414                 je 0x419b12
00419afe  0fbfc7               movsx eax, di
00419b01  83f8ff               cmp eax, -1
00419b04  740c                 je 0x419b12
00419b06  31d2                 xor edx, edx
00419b08  668b542404           mov dx, word ptr [esp + 4]
00419b0d  4a                   dec edx
00419b0e  39d0                 cmp eax, edx
00419b10  75be                 jne 0x419ad0
00419b12  8b0c24               mov ecx, dword ptr [esp]
00419b15  668b4602             mov ax, word ptr [esi + 2]
00419b19  31d2                 xor edx, edx
00419b1b  01d8                 add eax, ebx
00419b1d  8a542418             mov dl, byte ptr [esp + 0x18]
00419b21  01c8                 add eax, ecx
00419b23  25ffff0000           and eax, 0xffff
00419b28  e80dce0500           call 0x47693a
00419b2d  84c0                 test al, al
00419b2f  749f                 je 0x419ad0
00419b31  b001                 mov al, 1
00419b33  eb02                 jmp 0x419b37
00419b35  30c0                 xor al, al
00419b37  83c41c               add esp, 0x1c
00419b3a  5f                   pop edi
00419b3b  5e                   pop esi
00419b3c  59                   pop ecx
00419b3d  5b                   pop ebx
00419b3e  c3                   ret 
