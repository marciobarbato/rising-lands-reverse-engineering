; BatimentHabitable: Complete body; exclusive end 0x0041cde0.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041cc70  53                       push     ebx
0041cc71  51                       push     ecx
0041cc72  52                       push     edx
0041cc73  56                       push     esi
0041cc74  57                       push     edi
0041cc75  55                       push     ebp
0041cc76  83ec10                   sub      esp, 0x10
0041cc79  50                       push     eax
0041cc7a  31c0                     xor      eax, eax
0041cc7c  668b0424                 mov      ax, word ptr [esp]
0041cc80  89c6                     mov      esi, eax
0041cc82  c1e604                   shl      esi, 4
0041cc85  01c6                     add      esi, eax
0041cc87  c1e602                   shl      esi, 2
0041cc8a  01c6                     add      esi, eax
0041cc8c  c1e602                   shl      esi, 2
0041cc8f  81c6c8a04900             add      esi, 0x49a0c8
0041cc95  31d2                     xor      edx, edx
0041cc97  8a4608                   mov      al, byte ptr [esi + 8]
0041cc9a  88c2                     mov      dl, al
0041cc9c  8a4604                   mov      al, byte ptr [esi + 4]
0041cc9f  25ff000000               and      eax, 0xff
0041cca4  e8c3faffff               call     0x41c76c
0041cca9  31c0                     xor      eax, eax
0041ccab  8a4608                   mov      al, byte ptr [esi + 8]
0041ccae  83f811                   cmp      eax, 0x11
0041ccb1  0f8418010000             je       0x41cdcf
0041ccb7  83f809                   cmp      eax, 9
0041ccba  0f840f010000             je       0x41cdcf
0041ccc0  83f80c                   cmp      eax, 0xc
0041ccc3  0f8406010000             je       0x41cdcf
0041ccc9  83f804                   cmp      eax, 4
0041cccc  750b                     jne      0x41ccd9
0041ccce  66c746780000             mov      word ptr [esi + 0x78], 0
0041ccd4  e984000000               jmp      0x41cd5d
0041ccd9  83f803                   cmp      eax, 3
0041ccdc  0f857b000000             jne      0x41cd5d
0041cce2  8a4604                   mov      al, byte ptr [esi + 4]
0041cce5  25ff000000               and      eax, 0xff
0041ccea  83f804                   cmp      eax, 4
0041cced  0f8d6a000000             jge      0x41cd5d
0041ccf3  89c5                     mov      ebp, eax
0041ccf5  c1e502                   shl      ebp, 2
0041ccf8  29c5                     sub      ebp, eax
0041ccfa  89c2                     mov      edx, eax
0041ccfc  01ed                     add      ebp, ebp
0041ccfe  31c2                     xor      edx, eax
0041cd00  668b952cfb4d00           mov      dx, word ptr [ebp + 0x4dfb2c]
0041cd07  85d2                     test     edx, edx
0041cd09  0f8e4e000000             jle      0x41cd5d
0041cd0f  8d4c2404                 lea      ecx, [esp + 4]
0041cd13  8d5c2408                 lea      ebx, [esp + 8]
0041cd17  50                       push     eax
0041cd18  8d542410                 lea      edx, [esp + 0x10]
0041cd1c  8d442414                 lea      eax, [esp + 0x14]
0041cd20  e878a90400               call     0x46769d
0041cd25  8b442410                 mov      eax, dword ptr [esp + 0x10]
0041cd29  8b54240c                 mov      edx, dword ptr [esp + 0xc]
0041cd2d  668b9d2cfb4d00           mov      bx, word ptr [ebp + 0x4dfb2c]
0041cd34  01d0                     add      eax, edx
0041cd36  31d2                     xor      edx, edx
0041cd38  66f7f3                   div      bx
0041cd3b  31d2                     xor      edx, edx
0041cd3d  6689c2                   mov      dx, ax
0041cd40  89d0                     mov      eax, edx
0041cd42  c1e003                   shl      eax, 3
0041cd45  29d0                     sub      eax, edx
0041cd47  31db                     xor      ebx, ebx
0041cd49  89c2                     mov      edx, eax
0041cd4b  668b9d2efb4d00           mov      bx, word ptr [ebp + 0x4dfb2e]
0041cd52  c1fa1f                   sar      edx, 0x1f
0041cd55  f7fb                     idiv     ebx
0041cd57  888530fb4d00             mov      byte ptr [ebp + 0x4dfb30], al
0041cd5d  8a4608                   mov      al, byte ptr [esi + 8]
0041cd60  3c15                     cmp      al, 0x15
0041cd62  7735                     ja       0x41cd99
0041cd64  25ff000000               and      eax, 0xff
0041cd69  2eff248518cc4100         jmp      dword ptr cs:[eax*4 + 0x41cc18]
0041cd71  bf14000000               mov      edi, 0x14
0041cd76  eb21                     jmp      0x41cd99
0041cd78  bf0a000000               mov      edi, 0xa
0041cd7d  eb1a                     jmp      0x41cd99
0041cd7f  bf08000000               mov      edi, 8
0041cd84  eb13                     jmp      0x41cd99
0041cd86  bf04000000               mov      edi, 4
0041cd8b  eb0c                     jmp      0x41cd99
0041cd8d  bf05000000               mov      edi, 5
0041cd92  eb05                     jmp      0x41cd99
0041cd94  bf07000000               mov      edi, 7
0041cd99  31c0                     xor      eax, eax
0041cd9b  89fa                     mov      edx, edi
0041cd9d  668b0424                 mov      ax, word ptr [esp]
0041cda1  31db                     xor      ebx, ebx
0041cda3  e83ae1ffff               call     0x41aee2
0041cda8  83c203                   add      edx, 3
0041cdab  8a5e04                   mov      bl, byte ptr [esi + 4]
0041cdae  0fb7e8                   movzx    ebp, ax
0041cdb1  81e2ffff0000             and      edx, 0xffff
0041cdb7  89e8                     mov      eax, ebp
0041cdb9  e8939a0500               call     0x476851
0041cdbe  89e8                     mov      eax, ebp
0041cdc0  31d2                     xor      edx, edx
0041cdc2  31db                     xor      ebx, ebx
0041cdc4  6689fa                   mov      dx, di
0041cdc7  8a5e04                   mov      bl, byte ptr [esi + 4]
0041cdca  e8e49e0500               call     0x476cb3
0041cdcf  66c78684000000c800       mov      word ptr [esi + 0x84], 0xc8
0041cdd8  83c414                   add      esp, 0x14
0041cddb  e93d0d0000               jmp      0x41db1d
