; ResetCheminTerrainModify; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041b78f  53                       push ebx
0041b790  51                       push ecx
0041b791  52                       push edx
0041b792  56                       push esi
0041b793  57                       push edi
0041b794  55                       push ebp
0041b795  83ec20                   sub esp, 0x20
0041b798  50                       push eax
0041b799  31d2                     xor edx, edx
0041b79b  6689c2                   mov dx, ax
0041b79e  89d0                     mov eax, edx
0041b7a0  c1e004                   shl eax, 4
0041b7a3  01d0                     add eax, edx
0041b7a5  c1e002                   shl eax, 2
0041b7a8  01d0                     add eax, edx
0041b7aa  bdc8a04900               mov ebp, 0x49a0c8
0041b7af  c1e002                   shl eax, 2
0041b7b2  01c5                     add ebp, eax
0041b7b4  31d2                     xor edx, edx
0041b7b6  8a5508                   mov dl, byte ptr [ebp + 8]
0041b7b9  89d0                     mov eax, edx
0041b7bb  c1e002                   shl eax, 2
0041b7be  29d0                     sub eax, edx
0041b7c0  c1e002                   shl eax, 2
0041b7c3  01d0                     add eax, edx
0041b7c5  668b7d02                 mov di, word ptr [ebp + 2]
0041b7c9  668b14858c5d4900         mov dx, word ptr [eax*4 + 0x495d8c]
0041b7d1  668b04858e5d4900         mov ax, word ptr [eax*4 + 0x495d8e]
0041b7d9  89542410                 mov dword ptr [esp + 0x10], edx
0041b7dd  89442418                 mov dword ptr [esp + 0x18], eax
0041b7e1  30e4                     xor ah, ah
0041b7e3  8b5c2410                 mov ebx, dword ptr [esp + 0x10]
0041b7e7  88642420                 mov byte ptr [esp + 0x20], ah
0041b7eb  b800010000               mov eax, 0x100
0041b7f0  31d2                     xor edx, edx
0041b7f2  29d8                     sub eax, ebx
0041b7f4  89542414                 mov dword ptr [esp + 0x14], edx
0041b7f8  8944241c                 mov dword ptr [esp + 0x1c], eax
0041b7fc  8d85cc000000             lea eax, [ebp + 0xcc]
0041b802  895c2408                 mov dword ptr [esp + 8], ebx
0041b806  89442404                 mov dword ptr [esp + 4], eax
0041b80a  eb0f                     jmp 0x41b81b
0041b80c  8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0041b810  8b54241c                 mov edx, dword ptr [esp + 0x1c]
0041b814  43                       inc ebx
0041b815  01d7                     add edi, edx
0041b817  895c2414                 mov dword ptr [esp + 0x14], ebx
0041b81b  8b442414                 mov eax, dword ptr [esp + 0x14]
0041b81f  663b442418               cmp ax, word ptr [esp + 0x18]
0041b824  735a                     jae 0x41b880
0041b826  0faf442410               imul eax, dword ptr [esp + 0x10]
0041b82b  8b542408                 mov edx, dword ptr [esp + 8]
0041b82f  01c2                     add edx, eax
0041b831  89c6                     mov esi, eax
0041b833  8954240c                 mov dword ptr [esp + 0xc], edx
0041b837  eb02                     jmp 0x41b83b
0041b839  47                       inc edi
0041b83a  46                       inc esi
0041b83b  663b74240c               cmp si, word ptr [esp + 0xc]
0041b840  73ca                     jae 0x41b80c
0041b842  31d2                     xor edx, edx
0041b844  31c0                     xor eax, eax
0041b846  6689f2                   mov dx, si
0041b849  8a4508                   mov al, byte ptr [ebp + 8]
0041b84c  e80bf3ffff               call 0x41ab5c
0041b851  84c0                     test al, al
0041b853  74e4                     je 0x41b839
0041b855  31c0                     xor eax, eax
0041b857  8b4c2404                 mov ecx, dword ptr [esp + 4]
0041b85b  8a442420                 mov al, byte ptr [esp + 0x20]
0041b85f  bb01000000               mov ebx, 1
0041b864  50                       push eax
0041b865  01c0                     add eax, eax
0041b867  31d2                     xor edx, edx
0041b869  01c1                     add ecx, eax
0041b86b  31c0                     xor eax, eax
0041b86d  668b542404               mov dx, word ptr [esp + 4]
0041b872  6689f8                   mov ax, di
0041b875  e8be280200               call 0x43e138
0041b87a  fe442420                 inc byte ptr [esp + 0x20]
0041b87e  ebb9                     jmp 0x41b839
0041b880  83c424                   add esp, 0x24
0041b883  e995220000               jmp 0x41db1d
