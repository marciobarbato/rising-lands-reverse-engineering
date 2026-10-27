; TypeEnginGetSortieProjectile; intervalo [0x004511a5, 0x004513c7)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004511a5  56                       push     esi
004511a6  66c7030000               mov      word ptr [ebx], 0
004511ab  66c7010000               mov      word ptr [ecx], 0
004511b0  3c12                     cmp      al, 0x12
004511b2  0f82e1010000             jb       0x451399
004511b8  0f868a000000             jbe      0x451248
004511be  3c16                     cmp      al, 0x16
004511c0  0f82cd010000             jb       0x451393
004511c6  0f865d010000             jbe      0x451329
004511cc  3c17                     cmp      al, 0x17
004511ce  0f86a9000000             jbe      0x45127d
004511d4  3c18                     cmp      al, 0x18
004511d6  0f84d6000000             je       0x4512b2
004511dc  5e                       pop      esi
004511dd  c3                       ret
004511de  81e2ff000000             and      edx, 0xff
004511e4  4a                       dec      edx
004511e5  89d0                     mov      eax, edx
004511e7  c1fa1f                   sar      edx, 0x1f
004511ea  2bc2                     sub      eax, edx
004511ec  d1f8                     sar      eax, 1
004511ee  88c2                     mov      dl, al
004511f0  81e2ff000000             and      edx, 0xff
004511f6  668b33                   mov      si, word ptr [ebx]
004511f9  668b0495106b4900         mov      ax, word ptr [edx*4 + 0x496b10]
00451201  01c6                     add      esi, eax
00451203  668933                   mov      word ptr [ebx], si
00451206  668b0495126b4900         mov      ax, word ptr [edx*4 + 0x496b12]
0045120e  660101                   add      word ptr [ecx], ax
00451211  5e                       pop      esi
00451212  c3                       ret
00451213  81e2ff000000             and      edx, 0xff
00451219  4a                       dec      edx
0045121a  89d0                     mov      eax, edx
0045121c  c1fa1f                   sar      edx, 0x1f
0045121f  2bc2                     sub      eax, edx
00451221  d1f8                     sar      eax, 1
00451223  88c2                     mov      dl, al
00451225  81e2ff000000             and      edx, 0xff
0045122b  668b33                   mov      si, word ptr [ebx]
0045122e  668b0495f06a4900         mov      ax, word ptr [edx*4 + 0x496af0]
00451236  01c6                     add      esi, eax
00451238  668933                   mov      word ptr [ebx], si
0045123b  668b0495f26a4900         mov      ax, word ptr [edx*4 + 0x496af2]
00451243  660101                   add      word ptr [ecx], ax
00451246  5e                       pop      esi
00451247  c3                       ret
00451248  81e2ff000000             and      edx, 0xff
0045124e  4a                       dec      edx
0045124f  89d0                     mov      eax, edx
00451251  c1fa1f                   sar      edx, 0x1f
00451254  2bc2                     sub      eax, edx
00451256  d1f8                     sar      eax, 1
00451258  88c2                     mov      dl, al
0045125a  81e2ff000000             and      edx, 0xff
00451260  668b33                   mov      si, word ptr [ebx]
00451263  668b0495306b4900         mov      ax, word ptr [edx*4 + 0x496b30]
0045126b  01c6                     add      esi, eax
0045126d  668933                   mov      word ptr [ebx], si
00451270  668b0495326b4900         mov      ax, word ptr [edx*4 + 0x496b32]
00451278  660101                   add      word ptr [ecx], ax
0045127b  5e                       pop      esi
0045127c  c3                       ret
0045127d  81e2ff000000             and      edx, 0xff
00451283  4a                       dec      edx
00451284  89d0                     mov      eax, edx
00451286  c1fa1f                   sar      edx, 0x1f
00451289  2bc2                     sub      eax, edx
0045128b  d1f8                     sar      eax, 1
0045128d  88c2                     mov      dl, al
0045128f  81e2ff000000             and      edx, 0xff
00451295  668b33                   mov      si, word ptr [ebx]
00451298  668b0495506b4900         mov      ax, word ptr [edx*4 + 0x496b50]
004512a0  01c6                     add      esi, eax
004512a2  668933                   mov      word ptr [ebx], si
004512a5  668b0495526b4900         mov      ax, word ptr [edx*4 + 0x496b52]
004512ad  660101                   add      word ptr [ecx], ax
004512b0  5e                       pop      esi
004512b1  c3                       ret
004512b2  81e2ff000000             and      edx, 0xff
004512b8  4a                       dec      edx
004512b9  89d0                     mov      eax, edx
004512bb  c1fa1f                   sar      edx, 0x1f
004512be  2bc2                     sub      eax, edx
004512c0  d1f8                     sar      eax, 1
004512c2  88c2                     mov      dl, al
004512c4  81e2ff000000             and      edx, 0xff
004512ca  668b33                   mov      si, word ptr [ebx]
004512cd  668b0495706b4900         mov      ax, word ptr [edx*4 + 0x496b70]
004512d5  01c6                     add      esi, eax
004512d7  668933                   mov      word ptr [ebx], si
004512da  668b0495726b4900         mov      ax, word ptr [edx*4 + 0x496b72]
004512e2  660101                   add      word ptr [ecx], ax
004512e5  5e                       pop      esi
004512e6  c3                       ret
004512e7  31d2                     xor      edx, edx
004512e9  88e2                     mov      dl, ah
004512eb  668b33                   mov      si, word ptr [ebx]
004512ee  668b0495d06b4900         mov      ax, word ptr [edx*4 + 0x496bd0]
004512f6  01c6                     add      esi, eax
004512f8  668933                   mov      word ptr [ebx], si
004512fb  668b0495d26b4900         mov      ax, word ptr [edx*4 + 0x496bd2]
00451303  660101                   add      word ptr [ecx], ax
00451306  5e                       pop      esi
00451307  c3                       ret
00451308  31d2                     xor      edx, edx
0045130a  88e2                     mov      dl, ah
0045130c  668b33                   mov      si, word ptr [ebx]
0045130f  668b0495506c4900         mov      ax, word ptr [edx*4 + 0x496c50]
00451317  01c6                     add      esi, eax
00451319  668933                   mov      word ptr [ebx], si
0045131c  668b0495526c4900         mov      ax, word ptr [edx*4 + 0x496c52]
00451324  660101                   add      word ptr [ecx], ax
00451327  5e                       pop      esi
00451328  c3                       ret
00451329  81e2ff000000             and      edx, 0xff
0045132f  4a                       dec      edx
00451330  89d0                     mov      eax, edx
00451332  c1fa1f                   sar      edx, 0x1f
00451335  2bc2                     sub      eax, edx
00451337  d1f8                     sar      eax, 1
00451339  88c2                     mov      dl, al
0045133b  81e2ff000000             and      edx, 0xff
00451341  668b33                   mov      si, word ptr [ebx]
00451344  668b0495b06b4900         mov      ax, word ptr [edx*4 + 0x496bb0]
0045134c  01c6                     add      esi, eax
0045134e  668933                   mov      word ptr [ebx], si
00451351  668b0495b26b4900         mov      ax, word ptr [edx*4 + 0x496bb2]
00451359  660101                   add      word ptr [ecx], ax
0045135c  5e                       pop      esi
0045135d  c3                       ret
0045135e  81e2ff000000             and      edx, 0xff
00451364  4a                       dec      edx
00451365  89d0                     mov      eax, edx
00451367  c1fa1f                   sar      edx, 0x1f
0045136a  2bc2                     sub      eax, edx
0045136c  d1f8                     sar      eax, 1
0045136e  88c2                     mov      dl, al
00451370  81e2ff000000             and      edx, 0xff
00451376  668b33                   mov      si, word ptr [ebx]
00451379  668b0495906b4900         mov      ax, word ptr [edx*4 + 0x496b90]
00451381  01c6                     add      esi, eax
00451383  668933                   mov      word ptr [ebx], si
00451386  668b0495926b4900         mov      ax, word ptr [edx*4 + 0x496b92]
0045138e  660101                   add      word ptr [ecx], ax
00451391  5e                       pop      esi
00451392  c3                       ret
00451393  3c15                     cmp      al, 0x15
00451395  74c7                     je       0x45135e
00451397  5e                       pop      esi
00451398  c3                       ret
00451399  3c08                     cmp      al, 8
0045139b  7220                     jb       0x4513bd
0045139d  0f863bfeffff             jbe      0x4511de
004513a3  3c0c                     cmp      al, 0xc
004513a5  721e                     jb       0x4513c5
004513a7  88d4                     mov      ah, dl
004513a9  fecc                     dec      ah
004513ab  3c0c                     cmp      al, 0xc
004513ad  0f8655ffffff             jbe      0x451308
004513b3  3c0f                     cmp      al, 0xf
004513b5  0f842cffffff             je       0x4512e7
004513bb  5e                       pop      esi
004513bc  c3                       ret
004513bd  3c02                     cmp      al, 2
004513bf  0f844efeffff             je       0x451213
004513c5  5e                       pop      esi
004513c6  c3                       ret
