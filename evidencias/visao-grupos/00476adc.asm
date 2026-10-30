; EteintCase; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476adc  53                       push ebx
00476add  51                       push ecx
00476ade  56                       push esi
00476adf  57                       push edi
00476ae0  83ec04                   sub esp, 4
00476ae3  89c1                     mov ecx, eax
00476ae5  881424                   mov byte ptr [esp], dl
00476ae8  31db                     xor ebx, ebx
00476aea  6689c3                   mov bx, ax
00476aed  be00010000               mov esi, 0x100
00476af2  89da                     mov edx, ebx
00476af4  89d8                     mov eax, ebx
00476af6  c1fa1f                   sar edx, 0x1f
00476af9  f7fe                     idiv esi
00476afb  89d6                     mov esi, edx
00476afd  89da                     mov edx, ebx
00476aff  89d8                     mov eax, ebx
00476b01  c1fa1f                   sar edx, 0x1f
00476b04  c1e208                   shl edx, 8
00476b07  1bc2                     sbb eax, edx
00476b09  c1f808                   sar eax, 8
00476b0c  89c7                     mov edi, eax
00476b0e  31c0                     xor eax, eax
00476b10  8a0424                   mov al, byte ptr [esp]
00476b13  c1e002                   shl eax, 2
00476b16  8b90987d5000             mov edx, dword ptr [eax + 0x507d98]
00476b1c  8a141a                   mov dl, byte ptr [edx + ebx]
00476b1f  81e2ff000000             and edx, 0xff
00476b25  83fa01                   cmp edx, 1
00476b28  0f85f9000000             jne 0x476c27
00476b2e  31d2                     xor edx, edx
00476b30  6689f2                   mov dx, si
00476b33  85d2                     test edx, edx
00476b35  740d                     je 0x476b44
00476b37  8b80887d5000             mov eax, dword ptr [eax + 0x507d88]
00476b3d  804c03ff02               or byte ptr [ebx + eax - 1], 2
00476b42  eb0a                     jmp 0x476b4e
00476b44  8b80887d5000             mov eax, dword ptr [eax + 0x507d88]
00476b4a  800c0308                 or byte ptr [ebx + eax], 8
00476b4e  31c0                     xor eax, eax
00476b50  6689f8                   mov ax, di
00476b53  85c0                     test eax, eax
00476b55  741b                     je 0x476b72
00476b57  31c0                     xor eax, eax
00476b59  31d2                     xor edx, edx
00476b5b  8a0424                   mov al, byte ptr [esp]
00476b5e  6689ca                   mov dx, cx
00476b61  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476b68  808c0200ffffff01         or byte ptr [edx + eax - 0x100], 1
00476b70  eb13                     jmp 0x476b85
00476b72  31d2                     xor edx, edx
00476b74  8a0424                   mov al, byte ptr [esp]
00476b77  6689ca                   mov dx, cx
00476b7a  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476b81  800c0204                 or byte ptr [edx + eax], 4
00476b85  31c0                     xor eax, eax
00476b87  31d2                     xor edx, edx
00476b89  66a168714900             mov ax, word ptr [0x497168]
00476b8f  6689f2                   mov dx, si
00476b92  48                       dec eax
00476b93  39c2                     cmp edx, eax
00476b95  7418                     je 0x476baf
00476b97  31c0                     xor eax, eax
00476b99  31d2                     xor edx, edx
00476b9b  8a0424                   mov al, byte ptr [esp]
00476b9e  6689ca                   mov dx, cx
00476ba1  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476ba8  804c020108               or byte ptr [edx + eax + 1], 8
00476bad  eb15                     jmp 0x476bc4
00476baf  31c0                     xor eax, eax
00476bb1  31d2                     xor edx, edx
00476bb3  8a0424                   mov al, byte ptr [esp]
00476bb6  6689ca                   mov dx, cx
00476bb9  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476bc0  800c0202                 or byte ptr [edx + eax], 2
00476bc4  31d2                     xor edx, edx
00476bc6  31c0                     xor eax, eax
00476bc8  668b156a714900           mov dx, word ptr [0x49716a]
00476bcf  6689f8                   mov ax, di
00476bd2  4a                       dec edx
00476bd3  39d0                     cmp eax, edx
00476bd5  741b                     je 0x476bf2
00476bd7  31c0                     xor eax, eax
00476bd9  31d2                     xor edx, edx
00476bdb  8a0424                   mov al, byte ptr [esp]
00476bde  6689ca                   mov dx, cx
00476be1  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476be8  808c020001000004         or byte ptr [edx + eax + 0x100], 4
00476bf0  eb15                     jmp 0x476c07
00476bf2  31d0                     xor eax, edx
00476bf4  31d2                     xor edx, edx
00476bf6  8a0424                   mov al, byte ptr [esp]
00476bf9  6689ca                   mov dx, cx
00476bfc  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476c03  800c0201                 or byte ptr [edx + eax], 1
00476c07  31db                     xor ebx, ebx
00476c09  0fb63424                 movzx esi, byte ptr [esp]
00476c0d  6689cb                   mov bx, cx
00476c10  8b04b5887d5000           mov eax, dword ptr [esi*4 + 0x507d88]
00476c17  800c0310                 or byte ptr [ebx + eax], 0x10
00476c1b  ba03000000               mov edx, 3
00476c20  89f0                     mov eax, esi
00476c22  e86137ffff               call 0x46a388
00476c27  31db                     xor ebx, ebx
00476c29  8a1c24                   mov bl, byte ptr [esp]
00476c2c  81fbc8000000             cmp ebx, 0xc8
00476c32  0f849cfeffff             je 0x476ad4
00476c38  31d2                     xor edx, edx
00476c3a  8b049d987d5000           mov eax, dword ptr [ebx*4 + 0x507d98]
00476c41  6689ca                   mov dx, cx
00476c44  01d0                     add eax, edx
00476c46  8a30                     mov dh, byte ptr [eax]
00476c48  84f6                     test dh, dh
00476c4a  0f8484feffff             je 0x476ad4
00476c50  83fb04                   cmp ebx, 4
00476c53  0f847bfeffff             je 0x476ad4
00476c59  88f3                     mov bl, dh
00476c5b  fecb                     dec bl
00476c5d  8818                     mov byte ptr [eax], bl
00476c5f  e970feffff               jmp 0x476ad4
