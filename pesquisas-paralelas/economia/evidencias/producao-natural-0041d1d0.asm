; RechercheDecalageSortie: CalculPosition, then radius-1 ring with TerrainEnCollision(cell, 1); exclusive end 0x0041d2fc.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041d1d0  53                       push     ebx
0041d1d1  51                       push     ecx
0041d1d2  52                       push     edx
0041d1d3  56                       push     esi
0041d1d4  57                       push     edi
0041d1d5  55                       push     ebp
0041d1d6  83ec10                   sub      esp, 0x10
0041d1d9  89c2                     mov      edx, eax
0041d1db  31c9                     xor      ecx, ecx
0041d1dd  6689c1                   mov      cx, ax
0041d1e0  89c8                     mov      eax, ecx
0041d1e2  c1e004                   shl      eax, 4
0041d1e5  01c8                     add      eax, ecx
0041d1e7  c1e002                   shl      eax, 2
0041d1ea  01c8                     add      eax, ecx
0041d1ec  c1e002                   shl      eax, 2
0041d1ef  05c8a04900               add      eax, 0x49a0c8
0041d1f4  8a4008                   mov      al, byte ptr [eax + 8]
0041d1f7  3c15                     cmp      al, 0x15
0041d1f9  7742                     ja       0x41d23d
0041d1fb  25ff000000               and      eax, 0xff
0041d200  2eff248578d14100         jmp      dword ptr cs:[eax*4 + 0x41d178]
0041d208  b301                     mov      bl, 1
0041d20a  b900010000               mov      ecx, 0x100
0041d20f  31c0                     xor      eax, eax
0041d211  885c240c                 mov      byte ptr [esp + 0xc], bl
0041d215  6689d0                   mov      ax, dx
0041d218  31db                     xor      ebx, ebx
0041d21a  e879340000               call     0x420698
0041d21f  6689c3                   mov      bx, ax
0041d222  890424                   mov      dword ptr [esp], eax
0041d225  89da                     mov      edx, ebx
0041d227  89d8                     mov      eax, ebx
0041d229  c1fa1f                   sar      edx, 0x1f
0041d22c  f7f9                     idiv     ecx
0041d22e  89d7                     mov      edi, edx
0041d230  89da                     mov      edx, ebx
0041d232  89d8                     mov      eax, ebx
0041d234  c1fa1f                   sar      edx, 0x1f
0041d237  f7f9                     idiv     ecx
0041d239  89442404                 mov      dword ptr [esp + 4], eax
0041d23d  660fb674240c             movzx    si, byte ptr [esp + 0xc]
0041d243  f7de                     neg      esi
0041d245  89f0                     mov      eax, esi
0041d247  c1e008                   shl      eax, 8
0041d24a  6689442408               mov      word ptr [esp + 8], ax
0041d24f  bd01000000               mov      ebp, 1
0041d254  eb20                     jmp      0x41d276
0041d256  c644240c01               mov      byte ptr [esp + 0xc], 1
0041d25b  89c8                     mov      eax, ecx
0041d25d  31db                     xor      ebx, ebx
0041d25f  e834340000               call     0x420698
0041d264  b900010000               mov      ecx, 0x100
0041d269  ebb4                     jmp      0x41d21f
0041d26b  8a7c2409                 mov      bh, byte ptr [esp + 9]
0041d26f  fec7                     inc      bh
0041d271  46                       inc      esi
0041d272  887c2409                 mov      byte ptr [esp + 9], bh
0041d276  31d2                     xor      edx, edx
0041d278  0fbfc6                   movsx    eax, si
0041d27b  8a54240c                 mov      dl, byte ptr [esp + 0xc]
0041d27f  39d0                     cmp      eax, edx
0041d281  0f8f6a000000             jg       0x41d2f1
0041d287  31d2                     xor      edx, edx
0041d289  668b542404               mov      dx, word ptr [esp + 4]
0041d28e  01d0                     add      eax, edx
0041d290  85c0                     test     eax, eax
0041d292  7cd7                     jl       0x41d26b
0041d294  3d00010000               cmp      eax, 0x100
0041d299  7dd0                     jge      0x41d26b
0041d29b  31db                     xor      ebx, ebx
0041d29d  8a5c240c                 mov      bl, byte ptr [esp + 0xc]
0041d2a1  8b0c24                   mov      ecx, dword ptr [esp]
0041d2a4  f7db                     neg      ebx
0041d2a6  8b542408                 mov      edx, dword ptr [esp + 8]
0041d2aa  01d9                     add      ecx, ebx
0041d2ac  01d1                     add      ecx, edx
0041d2ae  eb02                     jmp      0x41d2b2
0041d2b0  41                       inc      ecx
0041d2b1  43                       inc      ebx
0041d2b2  31d2                     xor      edx, edx
0041d2b4  0fbfc3                   movsx    eax, bx
0041d2b7  8a54240c                 mov      dl, byte ptr [esp + 0xc]
0041d2bb  39d0                     cmp      eax, edx
0041d2bd  7fac                     jg       0x41d26b
0041d2bf  31d2                     xor      edx, edx
0041d2c1  6689fa                   mov      dx, di
0041d2c4  01c2                     add      edx, eax
0041d2c6  85d2                     test     edx, edx
0041d2c8  7ce6                     jl       0x41d2b0
0041d2ca  81fa00010000             cmp      edx, 0x100
0041d2d0  7dde                     jge      0x41d2b0
0041d2d2  85c0                     test     eax, eax
0041d2d4  7507                     jne      0x41d2dd
0041d2d6  0fbfc6                   movsx    eax, si
0041d2d9  85c0                     test     eax, eax
0041d2db  74d3                     je       0x41d2b0
0041d2dd  31c0                     xor      eax, eax
0041d2df  89ea                     mov      edx, ebp
0041d2e1  6689c8                   mov      ax, cx
0041d2e4  e8eb8e0500               call     0x4761d4
0041d2e9  84c0                     test     al, al
0041d2eb  75c3                     jne      0x41d2b0
0041d2ed  89c8                     mov      eax, ecx
0041d2ef  eb03                     jmp      0x41d2f4
0041d2f1  8b0424                   mov      eax, dword ptr [esp]
0041d2f4  83c410                   add      esp, 0x10
0041d2f7  e921080000               jmp      0x41db1d
