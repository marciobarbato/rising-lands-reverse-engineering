00479c50  56                   push esi
00479c51  89c6                 mov esi, eax
00479c53  31c0                 xor eax, eax
00479c55  6689f0               mov ax, si
00479c58  c1e004               shl eax, 4
00479c5b  81e2ffff0000         and edx, 0xffff
00479c61  8990b4995000         mov dword ptr [eax + 0x5099b4], edx
00479c67  31d2                 xor edx, edx
00479c69  6689da               mov dx, bx
00479c6c  8990b8995000         mov dword ptr [eax + 0x5099b8], edx
00479c72  31d2                 xor edx, edx
00479c74  6689ca               mov dx, cx
00479c77  8990bc995000         mov dword ptr [eax + 0x5099bc], edx
00479c7d  31d2                 xor edx, edx
00479c7f  668b542408           mov dx, word ptr [esp + 8]
00479c84  8990c0995000         mov dword ptr [eax + 0x5099c0], edx
00479c8a  663b35b8a95000       cmp si, word ptr [0x50a9b8]
00479c91  7607                 jbe 0x479c9a
00479c93  668935b8a95000       mov word ptr [0x50a9b8], si
00479c9a  5e                   pop esi
00479c9b  c20400               ret 4
