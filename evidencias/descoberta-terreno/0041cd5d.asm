; BatimentHabitable_vision_radii; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041cd5d  8a4608                   mov al, byte ptr [esi + 8]
0041cd60  3c15                     cmp al, 0x15
0041cd62  7735                     ja 0x41cd99
0041cd64  25ff000000               and eax, 0xff
0041cd69  2eff248518cc4100         jmp dword ptr cs:[eax*4 + 0x41cc18]
0041cd71  bf14000000               mov edi, 0x14
0041cd76  eb21                     jmp 0x41cd99
0041cd78  bf0a000000               mov edi, 0xa
0041cd7d  eb1a                     jmp 0x41cd99
0041cd7f  bf08000000               mov edi, 8
0041cd84  eb13                     jmp 0x41cd99
0041cd86  bf04000000               mov edi, 4
0041cd8b  eb0c                     jmp 0x41cd99
0041cd8d  bf05000000               mov edi, 5
0041cd92  eb05                     jmp 0x41cd99
0041cd94  bf07000000               mov edi, 7
0041cd99  31c0                     xor eax, eax
0041cd9b  89fa                     mov edx, edi
0041cd9d  668b0424                 mov ax, word ptr [esp]
0041cda1  31db                     xor ebx, ebx
0041cda3  e83ae1ffff               call 0x41aee2
0041cda8  83c203                   add edx, 3
0041cdab  8a5e04                   mov bl, byte ptr [esi + 4]
0041cdae  0fb7e8                   movzx ebp, ax
0041cdb1  81e2ffff0000             and edx, 0xffff
0041cdb7  89e8                     mov eax, ebp
0041cdb9  e8939a0500               call 0x476851
0041cdbe  89e8                     mov eax, ebp
0041cdc0  31d2                     xor edx, edx
0041cdc2  31db                     xor ebx, ebx
0041cdc4  6689fa                   mov dx, di
0041cdc7  8a5e04                   mov bl, byte ptr [esi + 4]
0041cdca  e8e49e0500               call 0x476cb3
