; ResetEnginCollision; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00442eac  53                       push ebx
00442ead  51                       push ecx
00442eae  56                       push esi
00442eaf  57                       push edi
00442eb0  55                       push ebp
00442eb1  83ec04                   sub esp, 4
00442eb4  89c1                     mov ecx, eax
00442eb6  89d6                     mov esi, edx
00442eb8  31ff                     xor edi, edi
00442eba  6689c7                   mov di, ax
00442ebd  89f8                     mov eax, edi
00442ebf  c1e004                   shl eax, 4
00442ec2  01f8                     add eax, edi
00442ec4  c1e002                   shl eax, 2
00442ec7  01f8                     add eax, edi
00442ec9  8b2da0194e00             mov ebp, dword ptr [0x4e19a0]
00442ecf  c1e002                   shl eax, 2
00442ed2  01c5                     add ebp, eax
00442ed4  8a4501                   mov al, byte ptr [ebp + 1]
00442ed7  3c19                     cmp al, 0x19
00442ed9  0f8740feffff             ja 0x442d1f
00442edf  25ff000000               and eax, 0xff
00442ee4  2eff2485442e4400         jmp dword ptr cs:[eax*4 + 0x442e44]
00442eec  ba01000000               mov edx, 1
00442ef1  81e6ffff0000             and esi, 0xffff
00442ef7  81c5fa000000             add ebp, 0xfa
00442efd  89f0                     mov eax, esi
00442eff  31db                     xor ebx, ebx
00442f01  e838330300               call 0x47623e
00442f06  6a00                     push 0
00442f08  31d2                     xor edx, edx
00442f0a  89f0                     mov eax, esi
00442f0c  6689ca                   mov dx, cx
00442f0f  89e9                     mov ecx, ebp
00442f11  e822b2ffff               call 0x43e138
00442f16  e904feffff               jmp 0x442d1f
00442f1b  31c0                     xor eax, eax
00442f1d  6689d0                   mov ax, dx
00442f20  ba02000000               mov edx, 2
00442f25  e814330300               call 0x47623e
00442f2a  e9f0fdffff               jmp 0x442d1f
00442f2f  ba01000000               mov edx, 1
00442f34  31c0                     xor eax, eax
00442f36  31ff                     xor edi, edi
00442f38  31db                     xor ebx, ebx
00442f3a  6689f0                   mov ax, si
00442f3d  6689cf                   mov di, cx
00442f40  890424                   mov dword ptr [esp], eax
00442f43  e8f6320300               call 0x47623e
00442f48  6a00                     push 0
00442f4a  8d85fa000000             lea eax, [ebp + 0xfa]
00442f50  89fa                     mov edx, edi
00442f52  89c1                     mov ecx, eax
00442f54  8b442404                 mov eax, dword ptr [esp + 4]
00442f58  e8dbb1ffff               call 0x43e138
00442f5d  89f0                     mov eax, esi
00442f5f  48                       dec eax
00442f60  ba01000000               mov edx, 1
00442f65  25ffff0000               and eax, 0xffff
00442f6a  8d8dfc000000             lea ecx, [ebp + 0xfc]
00442f70  31db                     xor ebx, ebx
00442f72  890424                   mov dword ptr [esp], eax
00442f75  e8c4320300               call 0x47623e
00442f7a  6a01                     push 1
00442f7c  8b442404                 mov eax, dword ptr [esp + 4]
00442f80  89fa                     mov edx, edi
00442f82  e8b1b1ffff               call 0x43e138
00442f87  89f0                     mov eax, esi
00442f89  81e801010000             sub eax, 0x101
00442f8f  ba01000000               mov edx, 1
00442f94  25ffff0000               and eax, 0xffff
00442f99  8d8dfe000000             lea ecx, [ebp + 0xfe]
00442f9f  31db                     xor ebx, ebx
00442fa1  890424                   mov dword ptr [esp], eax
00442fa4  e895320300               call 0x47623e
00442fa9  6a02                     push 2
00442fab  8b442404                 mov eax, dword ptr [esp + 4]
00442faf  89fa                     mov edx, edi
00442fb1  81ee00010000             sub esi, 0x100
00442fb7  e87cb1ffff               call 0x43e138
00442fbc  ba01000000               mov edx, 1
00442fc1  81e6ffff0000             and esi, 0xffff
00442fc7  8d8d00010000             lea ecx, [ebp + 0x100]
00442fcd  89f0                     mov eax, esi
00442fcf  31db                     xor ebx, ebx
00442fd1  e868320300               call 0x47623e
00442fd6  6a03                     push 3
00442fd8  89fa                     mov edx, edi
00442fda  89f0                     mov eax, esi
00442fdc  e930ffffff               jmp 0x442f11
00442fe1  31c0                     xor eax, eax
00442fe3  6689d0                   mov ax, dx
00442fe6  ba02000000               mov edx, 2
00442feb  e84e320300               call 0x47623e
00442ff0  89f0                     mov eax, esi
00442ff2  48                       dec eax
00442ff3  ba02000000               mov edx, 2
00442ff8  25ffff0000               and eax, 0xffff
00442ffd  e83c320300               call 0x47623e
00443002  89f0                     mov eax, esi
00443004  81e801010000             sub eax, 0x101
0044300a  ba02000000               mov edx, 2
0044300f  25ffff0000               and eax, 0xffff
00443014  e825320300               call 0x47623e
00443019  81ee00010000             sub esi, 0x100
0044301f  31c0                     xor eax, eax
00443021  ba02000000               mov edx, 2
00443026  6689f0                   mov ax, si
00443029  e9f7feffff               jmp 0x442f25
