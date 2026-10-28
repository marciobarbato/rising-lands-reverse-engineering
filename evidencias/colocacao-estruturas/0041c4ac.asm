; PlaceBatiment; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041c4ac  53                       push ebx
0041c4ad  51                       push ecx
0041c4ae  52                       push edx
0041c4af  56                       push esi
0041c4b0  57                       push edi
0041c4b1  89c1                     mov ecx, eax
0041c4b3  31f6                     xor esi, esi
0041c4b5  6689c6                   mov si, ax
0041c4b8  89f3                     mov ebx, esi
0041c4ba  c1e304                   shl ebx, 4
0041c4bd  01f3                     add ebx, esi
0041c4bf  c1e302                   shl ebx, 2
0041c4c2  01f3                     add ebx, esi
0041c4c4  c1e302                   shl ebx, 2
0041c4c7  81c3c8a04900             add ebx, 0x49a0c8
0041c4cd  8a4308                   mov al, byte ptr [ebx + 8]
0041c4d0  668b7302                 mov si, word ptr [ebx + 2]
0041c4d4  3c15                     cmp al, 0x15
0041c4d6  0f879d000000             ja 0x41c579
0041c4dc  0fb6f8                   movzx edi, al
0041c4df  2eff24bd54c44100         jmp dword ptr cs:[edi*4 + 0x41c454]
0041c4e7  badc020000               mov edx, 0x2dc
0041c4ec  e988000000               jmp 0x41c579
0041c4f1  babe020000               mov edx, 0x2be
0041c4f6  e97e000000               jmp 0x41c579
0041c4fb  bafa020000               mov edx, 0x2fa
0041c500  e974000000               jmp 0x41c579
0041c505  ba06030000               mov edx, 0x306
0041c50a  e96a000000               jmp 0x41c579
0041c50f  ba1f030000               mov edx, 0x31f
0041c514  e960000000               jmp 0x41c579
0041c519  ba33030000               mov edx, 0x333
0041c51e  eb59                     jmp 0x41c579
0041c520  ba57030000               mov edx, 0x357
0041c525  eb52                     jmp 0x41c579
0041c527  ba83030000               mov edx, 0x383
0041c52c  eb4b                     jmp 0x41c579
0041c52e  ba09040000               mov edx, 0x409
0041c533  eb44                     jmp 0x41c579
0041c535  ba6f030000               mov edx, 0x36f
0041c53a  eb3d                     jmp 0x41c579
0041c53c  baef030000               mov edx, 0x3ef
0041c541  eb36                     jmp 0x41c579
0041c543  ba8f030000               mov edx, 0x38f
0041c548  eb2f                     jmp 0x41c579
0041c54a  ba93030000               mov edx, 0x393
0041c54f  eb28                     jmp 0x41c579
0041c551  ba9f030000               mov edx, 0x39f
0041c556  eb21                     jmp 0x41c579
0041c558  bac3030000               mov edx, 0x3c3
0041c55d  eb1a                     jmp 0x41c579
0041c55f  bad7030000               mov edx, 0x3d7
0041c564  eb13                     jmp 0x41c579
0041c566  ba33040000               mov edx, 0x433
0041c56b  eb0c                     jmp 0x41c579
0041c56d  ba03040000               mov edx, 0x403
0041c572  eb05                     jmp 0x41c579
0041c574  ba15040000               mov edx, 0x415
0041c579  0fb67b08                 movzx edi, byte ptr [ebx + 8]
0041c57d  83ff09                   cmp edi, 9
0041c580  741f                     je 0x41c5a1
0041c582  83ff0c                   cmp edi, 0xc
0041c585  741a                     je 0x41c5a1
0041c587  31db                     xor ebx, ebx
0041c589  6689cb                   mov bx, cx
0041c58c  31c0                     xor eax, eax
0041c58e  81e2ffff0000             and edx, 0xffff
0041c594  6689f0                   mov ax, si
0041c597  e8adf4ffff               call 0x41ba49
0041c59c  e97d150000               jmp 0x41db1e
0041c5a1  31c0                     xor eax, eax
0041c5a3  8a4308                   mov al, byte ptr [ebx + 8]
0041c5a6  8dbbcc000000             lea edi, [ebx + 0xcc]
0041c5ac  83f809                   cmp eax, 9
0041c5af  7536                     jne 0x41c5e7
0041c5b1  81e6ffff0000             and esi, 0xffff
0041c5b7  89f0                     mov eax, esi
0041c5b9  e8ccfbffff               call 0x41c18a
0041c5be  30e4                     xor ah, ah
0041c5c0  6689437c                 mov word ptr [ebx + 0x7c], ax
0041c5c4  8b1d747d5000             mov ebx, dword ptr [0x507d74]
0041c5ca  a0f85b4900               mov al, byte ptr [0x495bf8]
0041c5cf  ba01000000               mov edx, 1
0041c5d4  88041e                   mov byte ptr [esi + ebx], al
0041c5d7  89f0                     mov eax, esi
0041c5d9  bb03000000               mov ebx, 3
0041c5de  e84b9c0500               call 0x47622e
0041c5e3  6a00                     push 0
0041c5e5  eb58                     jmp 0x41c63f
0041c5e7  83f80c                   cmp eax, 0xc
0041c5ea  0f852e150000             jne 0x41db1e
0041c5f0  81e6ffff0000             and esi, 0xffff
0041c5f6  89f0                     mov eax, esi
0041c5f8  30f6                     xor dh, dh
0041c5fa  e88ce6ffff               call 0x41ac8b
0041c5ff  88c2                     mov dl, al
0041c601  25ff000000               and eax, 0xff
0041c606  3dff000000               cmp eax, 0xff
0041c60b  0f840d150000             je 0x41db1e
0041c611  6689537c                 mov word ptr [ebx + 0x7c], dx
0041c615  a1747d5000               mov eax, dword ptr [0x507d74]
0041c61a  8a15f95b4900             mov dl, byte ptr [0x495bf9]
0041c620  881406                   mov byte ptr [esi + eax], dl
0041c623  ba01000000               mov edx, 1
0041c628  89f0                     mov eax, esi
0041c62a  66c783860000000000       mov word ptr [ebx + 0x86], 0
0041c633  e8f69b0500               call 0x47622e
0041c638  6a00                     push 0
0041c63a  bb03000000               mov ebx, 3
0041c63f  31d2                     xor edx, edx
0041c641  89f0                     mov eax, esi
0041c643  6689ca                   mov dx, cx
0041c646  89f9                     mov ecx, edi
0041c648  e8eb1a0200               call 0x43e138
0041c64d  e9cc140000               jmp 0x41db1e
