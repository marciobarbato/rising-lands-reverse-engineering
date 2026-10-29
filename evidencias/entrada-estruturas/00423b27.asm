; GetCaseCentrale; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00423b27  53                       push ebx
00423b28  51                       push ecx
00423b29  52                       push edx
00423b2a  57                       push edi
00423b2b  83ec08                   sub esp, 8
00423b2e  31d2                     xor edx, edx
00423b30  6689c2                   mov dx, ax
00423b33  89d0                     mov eax, edx
00423b35  c1e004                   shl eax, 4
00423b38  01d0                     add eax, edx
00423b3a  c1e002                   shl eax, 2
00423b3d  01d0                     add eax, edx
00423b3f  bbc8a04900               mov ebx, 0x49a0c8
00423b44  c1e002                   shl eax, 2
00423b47  01c3                     add ebx, eax
00423b49  31d2                     xor edx, edx
00423b4b  8a4308                   mov al, byte ptr [ebx + 8]
00423b4e  88c2                     mov dl, al
00423b50  89d0                     mov eax, edx
00423b52  c1e002                   shl eax, 2
00423b55  29d0                     sub eax, edx
00423b57  c1e002                   shl eax, 2
00423b5a  01c2                     add edx, eax
00423b5c  c1e202                   shl edx, 2
00423b5f  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
00423b66  890424                   mov dword ptr [esp], eax
00423b69  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
00423b70  8b1424                   mov edx, dword ptr [esp]
00423b73  89442404                 mov dword ptr [esp + 4], eax
00423b77  89c1                     mov ecx, eax
00423b79  66d1ea                   shr dx, 1
00423b7c  66d1e9                   shr cx, 1
00423b7f  891424                   mov dword ptr [esp], edx
00423b82  89c8                     mov eax, ecx
00423b84  894c2404                 mov dword ptr [esp + 4], ecx
00423b88  c1e008                   shl eax, 8
00423b8b  668b7b02                 mov di, word ptr [ebx + 2]
00423b8f  01d0                     add eax, edx
00423b91  01f8                     add eax, edi
00423b93  83c408                   add esp, 8
00423b96  5f                       pop edi
00423b97  5a                       pop edx
00423b98  59                       pop ecx
00423b99  5b                       pop ebx
00423b9a  c3                       ret
