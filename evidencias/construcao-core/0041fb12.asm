; BatimentConstructible; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041fb12  51                       push ecx
0041fb13  56                       push esi
0041fb14  57                       push edi
0041fb15  55                       push ebp
0041fb16  83ec0c                   sub esp, 0xc
0041fb19  53                       push ebx
0041fb1a  31db                     xor ebx, ebx
0041fb1c  88c3                     mov bl, al
0041fb1e  89d8                     mov eax, ebx
0041fb20  c1e002                   shl eax, 2
0041fb23  29d8                     sub eax, ebx
0041fb25  c1e002                   shl eax, 2
0041fb28  8d0c03                   lea ecx, [ebx + eax]
0041fb2b  c1e102                   shl ecx, 2
0041fb2e  668b818c5d4900           mov ax, word ptr [ecx + 0x495d8c]
0041fb35  89442408                 mov dword ptr [esp + 8], eax
0041fb39  668b818e5d4900           mov ax, word ptr [ecx + 0x495d8e]
0041fb40  8944240c                 mov dword ptr [esp + 0xc], eax
0041fb44  8b442408                 mov eax, dword ptr [esp + 8]
0041fb48  89d6                     mov esi, edx
0041fb4a  48                       dec eax
0041fb4b  29c6                     sub esi, eax
0041fb4d  8b44240c                 mov eax, dword ptr [esp + 0xc]
0041fb51  48                       dec eax
0041fb52  c1e008                   shl eax, 8
0041fb55  29c6                     sub esi, eax
0041fb57  83fb0c                   cmp ebx, 0xc
0041fb5a  0f857b000000             jne 0x41fbdb
0041fb60  31c0                     xor eax, eax
0041fb62  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041fb68  6689d0                   mov ax, dx
0041fb6b  8a1403                   mov dl, byte ptr [ebx + eax]
0041fb6e  3a15f85b4900             cmp dl, byte ptr [0x495bf8]
0041fb74  0f85bf000000             jne 0x41fc39
0041fb7a  8d1c00                   lea ebx, [eax + eax]
0041fb7d  a1380f4e00               mov eax, dword ptr [0x4e0f38]
0041fb82  01d8                     add eax, ebx
0041fb84  f6400180                 test byte ptr [eax + 1], 0x80
0041fb88  7412                     je 0x41fb9c
0041fb8a  668b00                   mov ax, word ptr [eax]
0041fb8d  25e07f0000               and eax, 0x7fe0
0041fb92  25ffff0000               and eax, 0xffff
0041fb97  c1f805                   sar eax, 5
0041fb9a  eb05                     jmp 0x41fba1
0041fb9c  b8ffff0000               mov eax, 0xffff
0041fba1  31c9                     xor ecx, ecx
0041fba3  6689c1                   mov cx, ax
0041fba6  81f9ffff0000             cmp ecx, 0xffff
0041fbac  0f8487000000             je 0x41fc39
0041fbb2  89cb                     mov ebx, ecx
0041fbb4  c1e304                   shl ebx, 4
0041fbb7  01cb                     add ebx, ecx
0041fbb9  c1e302                   shl ebx, 2
0041fbbc  31c0                     xor eax, eax
0041fbbe  01cb                     add ebx, ecx
0041fbc0  668b0424                 mov ax, word ptr [esp]
0041fbc4  c1e302                   shl ebx, 2
0041fbc7  e879240200               call 0x442045
0041fbcc  3a83cca04900             cmp al, byte ptr [ebx + 0x49a0cc]
0041fbd2  7565                     jne 0x41fc39
0041fbd4  b001                     mov al, 1
0041fbd6  e9d3a8ffff               jmp 0x41a4ae
0041fbdb  31d2                     xor edx, edx
0041fbdd  89542404                 mov dword ptr [esp + 4], edx
0041fbe1  bd01000000               mov ebp, 1
0041fbe6  eb0d                     jmp 0x41fbf5
0041fbe8  b800010000               mov eax, 0x100
0041fbed  29c8                     sub eax, ecx
0041fbef  01c6                     add esi, eax
0041fbf1  ff442404                 inc dword ptr [esp + 4]
0041fbf5  8b442404                 mov eax, dword ptr [esp + 4]
0041fbf9  663b44240c               cmp ax, word ptr [esp + 0xc]
0041fbfe  73d4                     jae 0x41fbd4
0041fc00  31ff                     xor edi, edi
0041fc02  eb02                     jmp 0x41fc06
0041fc04  46                       inc esi
0041fc05  47                       inc edi
0041fc06  8b4c2408                 mov ecx, dword ptr [esp + 8]
0041fc0a  6639cf                   cmp di, cx
0041fc0d  73d9                     jae 0x41fbe8
0041fc0f  31c9                     xor ecx, ecx
0041fc11  6689f1                   mov cx, si
0041fc14  89ea                     mov edx, ebp
0041fc16  89c8                     mov eax, ecx
0041fc18  e8b7650500               call 0x4761d4
0041fc1d  84c0                     test al, al
0041fc1f  74e3                     je 0x41fc04
0041fc21  89eb                     mov ebx, ebp
0041fc23  31c0                     xor eax, eax
0041fc25  89ca                     mov edx, ecx
0041fc27  668b0424                 mov ax, word ptr [esp]
0041fc2b  e83e280200               call 0x44246e
0041fc30  84c0                     test al, al
0041fc32  75d0                     jne 0x41fc04
0041fc34  e975a8ffff               jmp 0x41a4ae
0041fc39  30c0                     xor al, al
0041fc3b  e96ea8ffff               jmp 0x41a4ae
