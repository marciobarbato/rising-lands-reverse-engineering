; SetMurAllentour; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041c251  53                       push ebx
0041c252  51                       push ecx
0041c253  52                       push edx
0041c254  89c2                     mov edx, eax
0041c256  31c0                     xor eax, eax
0041c258  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c25e  6689d0                   mov ax, dx
0041c261  8a4403ff                 mov al, byte ptr [ebx + eax - 1]
0041c265  3a05f85b4900             cmp al, byte ptr [0x495bf8]
0041c26b  7562                     jne 0x41c2cf
0041c26d  89d0                     mov eax, edx
0041c26f  48                       dec eax
0041c270  25ffff0000               and eax, 0xffff
0041c275  8b1d380f4e00             mov ebx, dword ptr [0x4e0f38]
0041c27b  01c0                     add eax, eax
0041c27d  01d8                     add eax, ebx
0041c27f  f6400180                 test byte ptr [eax + 1], 0x80
0041c283  7412                     je 0x41c297
0041c285  668b00                   mov ax, word ptr [eax]
0041c288  31db                     xor ebx, ebx
0041c28a  25e07f0000               and eax, 0x7fe0
0041c28f  6689c3                   mov bx, ax
0041c292  c1fb05                   sar ebx, 5
0041c295  eb05                     jmp 0x41c29c
0041c297  bbffff0000               mov ebx, 0xffff
0041c29c  81e3ffff0000             and ebx, 0xffff
0041c2a2  81fbffff0000             cmp ebx, 0xffff
0041c2a8  7425                     je 0x41c2cf
0041c2aa  89d0                     mov eax, edx
0041c2ac  48                       dec eax
0041c2ad  25ffff0000               and eax, 0xffff
0041c2b2  30ed                     xor ch, ch
0041c2b4  e8d1feffff               call 0x41c18a
0041c2b9  88c1                     mov cl, al
0041c2bb  89d8                     mov eax, ebx
0041c2bd  c1e004                   shl eax, 4
0041c2c0  01d8                     add eax, ebx
0041c2c2  c1e002                   shl eax, 2
0041c2c5  01d8                     add eax, ebx
0041c2c7  66890c8544a14900         mov word ptr [eax*4 + 0x49a144], cx
0041c2cf  31c0                     xor eax, eax
0041c2d1  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c2d7  6689d0                   mov ax, dx
0041c2da  8a440301                 mov al, byte ptr [ebx + eax + 1]
0041c2de  3a05f85b4900             cmp al, byte ptr [0x495bf8]
0041c2e4  7564                     jne 0x41c34a
0041c2e6  89d0                     mov eax, edx
0041c2e8  40                       inc eax
0041c2e9  89c3                     mov ebx, eax
0041c2eb  81e3ffff0000             and ebx, 0xffff
0041c2f1  a1380f4e00               mov eax, dword ptr [0x4e0f38]
0041c2f6  01db                     add ebx, ebx
0041c2f8  01d8                     add eax, ebx
0041c2fa  f6400180                 test byte ptr [eax + 1], 0x80
0041c2fe  7412                     je 0x41c312
0041c300  668b00                   mov ax, word ptr [eax]
0041c303  31db                     xor ebx, ebx
0041c305  25e07f0000               and eax, 0x7fe0
0041c30a  6689c3                   mov bx, ax
0041c30d  c1fb05                   sar ebx, 5
0041c310  eb05                     jmp 0x41c317
0041c312  bbffff0000               mov ebx, 0xffff
0041c317  81e3ffff0000             and ebx, 0xffff
0041c31d  81fbffff0000             cmp ebx, 0xffff
0041c323  7425                     je 0x41c34a
0041c325  89d0                     mov eax, edx
0041c327  40                       inc eax
0041c328  25ffff0000               and eax, 0xffff
0041c32d  30ed                     xor ch, ch
0041c32f  e856feffff               call 0x41c18a
0041c334  88c1                     mov cl, al
0041c336  89d8                     mov eax, ebx
0041c338  c1e004                   shl eax, 4
0041c33b  01d8                     add eax, ebx
0041c33d  c1e002                   shl eax, 2
0041c340  01d8                     add eax, ebx
0041c342  66890c8544a14900         mov word ptr [eax*4 + 0x49a144], cx
0041c34a  31c0                     xor eax, eax
0041c34c  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c352  6689d0                   mov ax, dx
0041c355  8a2df85b4900             mov ch, byte ptr [0x495bf8]
0041c35b  3aac0300ffffff           cmp ch, byte ptr [ebx + eax - 0x100]
0041c362  756d                     jne 0x41c3d1
0041c364  89d0                     mov eax, edx
0041c366  81e800010000             sub eax, 0x100
0041c36c  89c3                     mov ebx, eax
0041c36e  81e3ffff0000             and ebx, 0xffff
0041c374  a1380f4e00               mov eax, dword ptr [0x4e0f38]
0041c379  01db                     add ebx, ebx
0041c37b  01d8                     add eax, ebx
0041c37d  f6400180                 test byte ptr [eax + 1], 0x80
0041c381  7412                     je 0x41c395
0041c383  668b00                   mov ax, word ptr [eax]
0041c386  25e07f0000               and eax, 0x7fe0
0041c38b  25ffff0000               and eax, 0xffff
0041c390  c1f805                   sar eax, 5
0041c393  eb05                     jmp 0x41c39a
0041c395  b8ffff0000               mov eax, 0xffff
0041c39a  31db                     xor ebx, ebx
0041c39c  6689c3                   mov bx, ax
0041c39f  81fbffff0000             cmp ebx, 0xffff
0041c3a5  742a                     je 0x41c3d1
0041c3a7  89d0                     mov eax, edx
0041c3a9  81e800010000             sub eax, 0x100
0041c3af  25ffff0000               and eax, 0xffff
0041c3b4  30ed                     xor ch, ch
0041c3b6  e8cffdffff               call 0x41c18a
0041c3bb  88c1                     mov cl, al
0041c3bd  89d8                     mov eax, ebx
0041c3bf  c1e004                   shl eax, 4
0041c3c2  01d8                     add eax, ebx
0041c3c4  c1e002                   shl eax, 2
0041c3c7  01d8                     add eax, ebx
0041c3c9  66890c8544a14900         mov word ptr [eax*4 + 0x49a144], cx
0041c3d1  31c0                     xor eax, eax
0041c3d3  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c3d9  6689d0                   mov ax, dx
0041c3dc  8a840300010000           mov al, byte ptr [ebx + eax + 0x100]
0041c3e3  3a05f85b4900             cmp al, byte ptr [0x495bf8]
0041c3e9  7562                     jne 0x41c44d
0041c3eb  89d0                     mov eax, edx
0041c3ed  fec4                     inc ah
0041c3ef  25ffff0000               and eax, 0xffff
0041c3f4  8b1d380f4e00             mov ebx, dword ptr [0x4e0f38]
0041c3fa  01c0                     add eax, eax
0041c3fc  01d8                     add eax, ebx
0041c3fe  f6400180                 test byte ptr [eax + 1], 0x80
0041c402  7412                     je 0x41c416
0041c404  668b00                   mov ax, word ptr [eax]
0041c407  31db                     xor ebx, ebx
0041c409  25e07f0000               and eax, 0x7fe0
0041c40e  6689c3                   mov bx, ax
0041c411  c1fb05                   sar ebx, 5
0041c414  eb05                     jmp 0x41c41b
0041c416  bbffff0000               mov ebx, 0xffff
0041c41b  81e3ffff0000             and ebx, 0xffff
0041c421  81fbffff0000             cmp ebx, 0xffff
0041c427  7424                     je 0x41c44d
0041c429  fec6                     inc dh
0041c42b  31c0                     xor eax, eax
0041c42d  6689d0                   mov ax, dx
0041c430  30f6                     xor dh, dh
0041c432  e853fdffff               call 0x41c18a
0041c437  88c2                     mov dl, al
0041c439  89d8                     mov eax, ebx
0041c43b  c1e004                   shl eax, 4
0041c43e  01d8                     add eax, ebx
0041c440  c1e002                   shl eax, 2
0041c443  01d8                     add eax, ebx
0041c445  6689148544a14900         mov word ptr [eax*4 + 0x49a144], dx
0041c44d  5a                       pop edx
0041c44e  59                       pop ecx
0041c44f  5b                       pop ebx
0041c450  c3                       ret
