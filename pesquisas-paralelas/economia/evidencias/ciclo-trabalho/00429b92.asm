; InputGame mode-9 depot packets 0x429b92..0x429da1; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00429b92  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429b98  3dffff0000               cmp eax, 0xffff
00429b9d  7453                     je 0x429bf2
00429b9f  31c0                     xor eax, eax
00429ba1  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429ba7  e81df6feff               call 0x4191c9
00429bac  84c0                     test al, al
00429bae  7429                     je 0x429bd9
00429bb0  31c0                     xor eax, eax
00429bb2  31d2                     xor edx, edx
00429bb4  8a45fc                   mov al, byte ptr [ebp - 4]
00429bb7  668b15c46a4900           mov dx, word ptr [0x496ac4]
00429bbe  e8e2860400               call 0x4722a5
00429bc3  84c0                     test al, al
00429bc5  7412                     je 0x429bd9
00429bc7  31c0                     xor eax, eax
00429bc9  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429bcf  e8b804ffff               call 0x41a08c
00429bd4  3a45fc                   cmp al, byte ptr [ebp - 4]
00429bd7  7419                     je 0x429bf2
00429bd9  bb0e1e0000               mov ebx, 0x1e0e
00429bde  31f6                     xor esi, esi
00429be0  66891d10a04900           mov word ptr [0x49a010], bx
00429be7  893514a04900             mov dword ptr [0x49a014], esi
00429bed  e9621c0000               jmp 0x42b854
00429bf2  bb03000000               mov ebx, 3
00429bf7  a1848f5000               mov eax, dword ptr [0x508f84]
00429bfc  31d2                     xor edx, edx
00429bfe  f7f3                     div ebx
00429c00  bf401e0000               mov edi, 0x1e40
00429c05  891514a04900             mov dword ptr [0x49a014], edx
00429c0b  8a15ae995000             mov dl, byte ptr [0x5099ae]
00429c11  66893d10a04900           mov word ptr [0x49a010], di
00429c18  84d2                     test dl, dl
00429c1a  0f84341c0000             je 0x42b854
00429c20  803daf99500000           cmp byte ptr [0x5099af], 0
00429c27  0f8557010000             jne 0x429d84
00429c2d  e9221c0000               jmp 0x42b854
00429c32  31c0                     xor eax, eax
00429c34  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429c3a  3dffff0000               cmp eax, 0xffff
00429c3f  7421                     je 0x429c62
00429c41  31d2                     xor edx, edx
00429c43  8a15b4054e00             mov dl, byte ptr [0x4e05b4]
00429c49  31db                     xor ebx, ebx
00429c4b  52                       push edx
00429c4c  b902000000               mov ecx, 2
00429c51  668b1db2054e00           mov bx, word ptr [0x4e05b2]
00429c58  50                       push eax
00429c59  31c0                     xor eax, eax
00429c5b  ba13000000               mov edx, 0x13
00429c60  eb23                     jmp 0x429c85
00429c62  31c0                     xor eax, eax
00429c64  a0b4054e00               mov al, byte ptr [0x4e05b4]
00429c69  b901000000               mov ecx, 1
00429c6e  50                       push eax
00429c6f  31c0                     xor eax, eax
00429c71  ba13000000               mov edx, 0x13
00429c76  6689f0                   mov ax, si
00429c79  31db                     xor ebx, ebx
00429c7b  50                       push eax
00429c7c  31c0                     xor eax, eax
00429c7e  668b1db2054e00           mov bx, word ptr [0x4e05b2]
00429c85  8a45fc                   mov al, byte ptr [ebp - 4]
00429c88  e847500300               call 0x45ecd4
00429c8d  ba031e0000               mov edx, 0x1e03
00429c92  31c0                     xor eax, eax
00429c94  66893504624900           mov word ptr [0x496204], si
00429c9b  66a3ae054e00             mov word ptr [0x4e05ae], ax
00429ca1  e901130000               jmp 0x42afa7
00429ca6  31c0                     xor eax, eax
00429ca8  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429cae  3dffff0000               cmp eax, 0xffff
00429cb3  7421                     je 0x429cd6
00429cb5  31d2                     xor edx, edx
00429cb7  8a15b4054e00             mov dl, byte ptr [0x4e05b4]
00429cbd  31db                     xor ebx, ebx
00429cbf  52                       push edx
00429cc0  b902000000               mov ecx, 2
00429cc5  668b1db2054e00           mov bx, word ptr [0x4e05b2]
00429ccc  50                       push eax
00429ccd  31c0                     xor eax, eax
00429ccf  ba06000000               mov edx, 6
00429cd4  ebaf                     jmp 0x429c85
00429cd6  31c0                     xor eax, eax
00429cd8  a0b4054e00               mov al, byte ptr [0x4e05b4]
00429cdd  b901000000               mov ecx, 1
00429ce2  50                       push eax
00429ce3  31c0                     xor eax, eax
00429ce5  ba06000000               mov edx, 6
00429cea  eb8a                     jmp 0x429c76
00429cec  31c0                     xor eax, eax
00429cee  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429cf4  3dffff0000               cmp eax, 0xffff
00429cf9  7424                     je 0x429d1f
00429cfb  31d2                     xor edx, edx
00429cfd  8a15b4054e00             mov dl, byte ptr [0x4e05b4]
00429d03  31db                     xor ebx, ebx
00429d05  52                       push edx
00429d06  b902000000               mov ecx, 2
00429d0b  668b1db2054e00           mov bx, word ptr [0x4e05b2]
00429d12  50                       push eax
00429d13  31c0                     xor eax, eax
00429d15  ba07000000               mov edx, 7
00429d1a  e966ffffff               jmp 0x429c85
00429d1f  31c0                     xor eax, eax
00429d21  a0b4054e00               mov al, byte ptr [0x4e05b4]
00429d26  b901000000               mov ecx, 1
00429d2b  50                       push eax
00429d2c  31c0                     xor eax, eax
00429d2e  ba07000000               mov edx, 7
00429d33  e93effffff               jmp 0x429c76
00429d38  31c0                     xor eax, eax
00429d3a  66a1c46a4900             mov ax, word ptr [0x496ac4]
00429d40  3dffff0000               cmp eax, 0xffff
00429d45  7424                     je 0x429d6b
00429d47  31d2                     xor edx, edx
00429d49  8a15b4054e00             mov dl, byte ptr [0x4e05b4]
00429d4f  31db                     xor ebx, ebx
00429d51  52                       push edx
00429d52  b902000000               mov ecx, 2
00429d57  668b1db2054e00           mov bx, word ptr [0x4e05b2]
00429d5e  50                       push eax
00429d5f  31c0                     xor eax, eax
00429d61  ba08000000               mov edx, 8
00429d66  e91affffff               jmp 0x429c85
00429d6b  31c0                     xor eax, eax
00429d6d  a0b4054e00               mov al, byte ptr [0x4e05b4]
00429d72  b901000000               mov ecx, 1
00429d77  50                       push eax
00429d78  31c0                     xor eax, eax
00429d7a  ba08000000               mov edx, 8
00429d7f  e9f2feffff               jmp 0x429c76
00429d84  66a1b0054e00             mov ax, word ptr [0x4e05b0]
00429d8a  663d0300                 cmp ax, 3
00429d8e  0f87f9feffff             ja 0x429c8d
00429d94  25ffff0000               and eax, 0xffff
00429d99  2eff24853c924200         jmp dword ptr cs:[eax*4 + 0x42923c]
