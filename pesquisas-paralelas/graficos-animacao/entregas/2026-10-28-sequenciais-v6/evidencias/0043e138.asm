; Chemin_ModifieZone [0x43e138, 0x43e2a3)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0043e138  56                     push     esi
0043e139  57                     push     edi
0043e13a  89c6                   mov      esi, eax
0043e13c  89d0                   mov      eax, edx
0043e13e  80fb03                 cmp      bl, 3
0043e141  0f8755010000           ja       0x43e29c
0043e147  31d2                   xor      edx, edx
0043e149  88da                   mov      dl, bl
0043e14b  2eff249528e14300       jmp      dword ptr cs:[edx*4 + 0x43e128]
0043e153  30f6                   xor      dh, dh
0043e155  89c3                   mov      ebx, eax
0043e157  8a54240c               mov      dl, byte ptr [esp + 0xc]
0043e15b  c1e303                 shl      ebx, 3
0043e15e  01da                   add      edx, ebx
0043e160  31db                   xor      ebx, ebx
0043e162  6689c3                 mov      bx, ax
0043e165  89d8                   mov      eax, ebx
0043e167  c1e004                 shl      eax, 4
0043e16a  01d8                   add      eax, ebx
0043e16c  c1e002                 shl      eax, 2
0043e16f  01d8                   add      eax, ebx
0043e171  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
0043e177  80c640                 add      dh, 0x40
0043e17a  8a448301               mov      al, byte ptr [ebx + eax*4 + 1]
0043e17e  25ff000000             and      eax, 0xff
0043e183  80b8c862490001         cmp      byte ptr [eax + 0x4962c8], 1
0043e18a  7403                   je       0x43e18f
0043e18c  80ca04                 or       dl, 4
0043e18f  31c0                   xor      eax, eax
0043e191  6689f0                 mov      ax, si
0043e194  8b1d380f4e00           mov      ebx, dword ptr [0x4e0f38]
0043e19a  01c0                   add      eax, eax
0043e19c  01d8                   add      eax, ebx
0043e19e  663b10                 cmp      dx, word ptr [eax]
0043e1a1  0f85f5000000           jne      0x43e29c
0043e1a7  668b11                 mov      dx, word ptr [ecx]
0043e1aa  668910                 mov      word ptr [eax], dx
0043e1ad  b001                   mov      al, 1
0043e1af  5f                     pop      edi
0043e1b0  5e                     pop      esi
0043e1b1  c20400                 ret      4
0043e1b4  89c2                   mov      edx, eax
0043e1b6  30e4                   xor      ah, ah
0043e1b8  c1e205                 shl      edx, 5
0043e1bb  8a44240c               mov      al, byte ptr [esp + 0xc]
0043e1bf  8b1d380f4e00           mov      ebx, dword ptr [0x4e0f38]
0043e1c5  01d0                   add      eax, edx
0043e1c7  31d2                   xor      edx, edx
0043e1c9  80c480                 add      ah, 0x80
0043e1cc  6689f2                 mov      dx, si
0043e1cf  89c7                   mov      edi, eax
0043e1d1  8d0412                 lea      eax, [edx + edx]
0043e1d4  01d8                   add      eax, ebx
0043e1d6  663b38                 cmp      di, word ptr [eax]
0043e1d9  0f85bd000000           jne      0x43e29c
0043e1df  668b19                 mov      bx, word ptr [ecx]
0043e1e2  668918                 mov      word ptr [eax], bx
0043e1e5  89d0                   mov      eax, edx
0043e1e7  e8cb060000             call     0x43e8b7 ; MurRetire
0043e1ec  ebbf                   jmp      0x43e1ad ;
0043e1ee  30f6                   xor      dh, dh
0043e1f0  89c3                   mov      ebx, eax
0043e1f2  8a54240c               mov      dl, byte ptr [esp + 0xc]
0043e1f6  c1e303                 shl      ebx, 3
0043e1f9  01d3                   add      ebx, edx
0043e1fb  31d2                   xor      edx, edx
0043e1fd  6689c2                 mov      dx, ax
0043e200  89d0                   mov      eax, edx
0043e202  c1e004                 shl      eax, 4
0043e205  01d0                   add      eax, edx
0043e207  c1e002                 shl      eax, 2
0043e20a  01d0                   add      eax, edx
0043e20c  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
0043e212  80c740                 add      bh, 0x40
0043e215  8a448201               mov      al, byte ptr [edx + eax*4 + 1]
0043e219  25ff000000             and      eax, 0xff
0043e21e  80b8c862490001         cmp      byte ptr [eax + 0x4962c8], 1
0043e225  7403                   je       0x43e22a
0043e227  80cb04                 or       bl, 4
0043e22a  31d2                   xor      edx, edx
0043e22c  6689f2                 mov      dx, si
0043e22f  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0043e234  01d2                   add      edx, edx
0043e236  01d0                   add      eax, edx
0043e238  31f6                   xor      esi, esi
0043e23a  668b30                 mov      si, word ptr [eax]
0043e23d  81fe00400000           cmp      esi, 0x4000
0043e243  7d57                   jge      0x43e29c
0043e245  668931                 mov      word ptr [ecx], si
0043e248  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0043e24d  66891c02               mov      word ptr [edx + eax], bx
0043e251  e957ffffff             jmp      0x43e1ad ;
0043e256  89c2                   mov      edx, eax
0043e258  30e4                   xor      ah, ah
0043e25a  c1e205                 shl      edx, 5
0043e25d  8a44240c               mov      al, byte ptr [esp + 0xc]
0043e261  01d0                   add      eax, edx
0043e263  80c480                 add      ah, 0x80
0043e266  31d2                   xor      edx, edx
0043e268  89c7                   mov      edi, eax
0043e26a  6689f2                 mov      dx, si
0043e26d  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0043e272  8d1c12                 lea      ebx, [edx + edx]
0043e275  01d8                   add      eax, ebx
0043e277  31f6                   xor      esi, esi
0043e279  668b30                 mov      si, word ptr [eax]
0043e27c  81fe00400000           cmp      esi, 0x4000
0043e282  7d18                   jge      0x43e29c
0043e284  668931                 mov      word ptr [ecx], si
0043e287  a1380f4e00             mov      eax, dword ptr [0x4e0f38]
0043e28c  66893c03               mov      word ptr [ebx + eax], di
0043e290  89d0                   mov      eax, edx
0043e292  e87f030000             call     0x43e616 ; MurAjoute
0043e297  e911ffffff             jmp      0x43e1ad ;
0043e29c  30c0                   xor      al, al
0043e29e  5f                     pop      edi
0043e29f  5e                     pop      esi
0043e2a0  c20400                 ret      4
