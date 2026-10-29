; Stage 19 static inventory only; intact EXE SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; InfligeDegat_building_branch [0x450874,0x450a9d)
00450874  56                       push     esi
00450875  57                       push     edi
00450876  55                       push     ebp
00450877  83ec24                   sub      esp, 0x24
0045087a  50                       push     eax
0045087b  88542418                 mov      byte ptr [esp + 0x18], dl
0045087f  89de                     mov      esi, ebx
00450881  884c240c                 mov      byte ptr [esp + 0xc], cl
00450885  807c243800               cmp      byte ptr [esp + 0x38], 0
0045088a  750f                     jne      0x45089b
0045088c  31c0                     xor      eax, eax
0045088e  668b0424                 mov      ax, word ptr [esp]
00450892  e8b3acfcff               call     0x41b54a
00450897  89c7                     mov      edi, eax
00450899  eb05                     jmp      0x4508a0
0045089b  bfffff0000               mov      edi, 0xffff
004508a0  0fb7ef                   movzx    ebp, di
004508a3  81fdffff0000             cmp      ebp, 0xffff
004508a9  0f84ee010000             je       0x450a9d
004508af  31c0                     xor      eax, eax
004508b1  8a442418                 mov      al, byte ptr [esp + 0x18]
004508b5  b902000000               mov      ecx, 2
004508ba  83f801                   cmp      eax, 1
004508bd  7566                     jne      0x450925
004508bf  31c0                     xor      eax, eax
004508c1  6689f0                   mov      ax, si
004508c4  89442404                 mov      dword ptr [esp + 4], eax
004508c8  89c2                     mov      edx, eax
004508ca  c1e004                   shl      eax, 4
004508cd  01d0                     add      eax, edx
004508cf  c1e002                   shl      eax, 2
004508d2  01d0                     add      eax, edx
004508d4  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
004508da  c1e002                   shl      eax, 2
004508dd  01c6                     add      esi, eax
004508df  31db                     xor      ebx, ebx
004508e1  8a4601                   mov      al, byte ptr [esi + 1]
004508e4  88c3                     mov      bl, al
004508e6  8b159c194e00             mov      edx, dword ptr [0x4e199c]
004508ec  89d8                     mov      eax, ebx
004508ee  8b0482                   mov      eax, dword ptr [edx + eax*4]
004508f1  83c01a                   add      eax, 0x1a
004508f4  30ed                     xor      ch, ch
004508f6  8a00                     mov      al, byte ptr [eax]
004508f8  88c1                     mov      cl, al
004508fa  31c0                     xor      eax, eax
004508fc  ba05000000               mov      edx, 5
00450901  8a06                     mov      al, byte ptr [esi]
00450903  e8b883fdff               call     0x428cc0
00450908  8b5c2404                 mov      ebx, dword ptr [esp + 4]
0045090c  01c1                     add      ecx, eax
0045090e  8a06                     mov      al, byte ptr [esi]
00450910  ba04000000               mov      edx, 4
00450915  88442414                 mov      byte ptr [esp + 0x14], al
00450919  89e8                     mov      eax, ebp
0045091b  e8e83e0300               call     0x484808
00450920  e98d000000               jmp      0x4509b2
00450925  83f803                   cmp      eax, 3
00450928  7536                     jne      0x450960
0045092a  89e8                     mov      eax, ebp
0045092c  31db                     xor      ebx, ebx
0045092e  e8c19bfcff               call     0x41a4f4
00450933  88c3                     mov      bl, al
00450935  81e6ffff0000             and      esi, 0xffff
0045093b  89f0                     mov      eax, esi
0045093d  e8b29bfcff               call     0x41a4f4
00450942  ba03000000               mov      edx, 3
00450947  25ff000000               and      eax, 0xff
0045094c  e83982fcff               call     0x418b8a
00450951  89c1                     mov      ecx, eax
00450953  89f0                     mov      eax, esi
00450955  e83297fcff               call     0x41a08c
0045095a  88442414                 mov      byte ptr [esp + 0x14], al
0045095e  eb52                     jmp      0x4509b2
00450960  83f804                   cmp      eax, 4
00450963  754d                     jne      0x4509b2
00450965  31d2                     xor      edx, edx
00450967  6689f2                   mov      dx, si
0045096a  89d0                     mov      eax, edx
0045096c  c1e004                   shl      eax, 4
0045096f  01d0                     add      eax, edx
00450971  c1e002                   shl      eax, 2
00450974  01d0                     add      eax, edx
00450976  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0045097c  8a0482                   mov      al, byte ptr [edx + eax*4]
0045097f  88442414                 mov      byte ptr [esp + 0x14], al
00450983  31c0                     xor      eax, eax
00450985  8a44240c                 mov      al, byte ptr [esp + 0xc]
00450989  83f81d                   cmp      eax, 0x1d
0045098c  750b                     jne      0x450999
0045098e  31d2                     xor      edx, edx
00450990  668b156c714900           mov      dx, word ptr [0x49716c]
00450997  eb0e                     jmp      0x4509a7
00450999  83f81e                   cmp      eax, 0x1e
0045099c  7514                     jne      0x4509b2
0045099e  31d2                     xor      edx, edx
004509a0  668b156e714900           mov      dx, word ptr [0x49716e]
004509a7  89d0                     mov      eax, edx
004509a9  c1fa1f                   sar      edx, 0x1f
004509ac  2bc2                     sub      eax, edx
004509ae  d1f8                     sar      eax, 1
004509b0  89c1                     mov      ecx, eax
004509b2  31db                     xor      ebx, ebx
004509b4  31d2                     xor      edx, edx
004509b6  31c0                     xor      eax, eax
004509b8  8a5c2414                 mov      bl, byte ptr [esp + 0x14]
004509bc  6689ca                   mov      dx, cx
004509bf  6689f8                   mov      ax, di
004509c2  e8fa98fcff               call     0x41a2c1
004509c7  b821000000               mov      eax, 0x21
004509cc  e80bfb0100               call     0x4704dc
004509d1  a801                     test     al, 1
004509d3  7511                     jne      0x4509e6
004509d5  6a00                     push     0
004509d7  6a00                     push     0
004509d9  6a00                     push     0
004509db  31d2                     xor      edx, edx
004509dd  6a00                     push     0
004509df  b80f000000               mov      eax, 0xf
004509e4  eb0f                     jmp      0x4509f5
004509e6  6a00                     push     0
004509e8  6a00                     push     0
004509ea  6a00                     push     0
004509ec  31d2                     xor      edx, edx
004509ee  6a00                     push     0
004509f0  b810000000               mov      eax, 0x10
004509f5  668b542410               mov      dx, word ptr [esp + 0x10]
004509fa  6a00                     push     0
004509fc  31c9                     xor      ecx, ecx
004509fe  89d3                     mov      ebx, edx
00450a00  e847da0100               call     0x46e44c
00450a05  31c9                     xor      ecx, ecx
00450a07  6689f9                   mov      cx, di
00450a0a  0fb6742414               movzx    esi, byte ptr [esp + 0x14]
00450a0f  89c8                     mov      eax, ecx
00450a11  31d2                     xor      edx, edx
00450a13  e87496fcff               call     0x41a08c
00450a18  88c2                     mov      dl, al
00450a1a  89f0                     mov      eax, esi
00450a1c  e817ce0100               call     0x46d838
00450a21  84c0                     test     al, al
00450a23  745a                     je       0x450a7f
00450a25  89c8                     mov      eax, ecx
00450a27  0fb66c2414               movzx    ebp, byte ptr [esp + 0x14]
00450a2c  e85b96fcff               call     0x41a08c
00450a31  bb0a000000               mov      ebx, 0xa
00450a36  25ff000000               and      eax, 0xff
00450a3b  89ea                     mov      edx, ebp
00450a3d  e8d6460200               call     0x475118
00450a42  89c8                     mov      eax, ecx
00450a44  e84396fcff               call     0x41a08c
00450a49  bb06000000               mov      ebx, 6
00450a4e  25ff000000               and      eax, 0xff
00450a53  89ea                     mov      edx, ebp
00450a55  e8be460200               call     0x475118
00450a5a  89c8                     mov      eax, ecx
00450a5c  31d2                     xor      edx, edx
00450a5e  e82996fcff               call     0x41a08c
00450a63  88c2                     mov      dl, al
00450a65  89f0                     mov      eax, esi
00450a67  e85fce0100               call     0x46d8cb
00450a6c  89c8                     mov      eax, ecx
00450a6e  e81996fcff               call     0x41a08c
00450a73  25ff000000               and      eax, 0xff
00450a78  89f2                     mov      edx, esi
00450a7a  e84cce0100               call     0x46d8cb
00450a7f  31c0                     xor      eax, eax
00450a81  6689f8                   mov      ax, di
00450a84  31d2                     xor      edx, edx
00450a86  e80196fcff               call     0x41a08c
00450a8b  88c2                     mov      dl, al
00450a8d  31c0                     xor      eax, eax
00450a8f  8a442414                 mov      al, byte ptr [esp + 0x14]
00450a93  e868cb0100               call     0x46d600
00450a98  e938060000               jmp      0x4510d5
; InfligeDegat_return [0x4510d5,0x4510dd)
004510d5  83c428                   add      esp, 0x28
004510d8  e9cd51ffff               jmp      0x4462aa
; BatimentInfligeDegat [0x41a2c1,0x41a4b6)
0041a2c1  51                       push     ecx
0041a2c2  56                       push     esi
0041a2c3  57                       push     edi
0041a2c4  55                       push     ebp
0041a2c5  83ec10                   sub      esp, 0x10
0041a2c8  89c7                     mov      edi, eax
0041a2ca  89542408                 mov      dword ptr [esp + 8], edx
0041a2ce  885c240c                 mov      byte ptr [esp + 0xc], bl
0041a2d2  31d2                     xor      edx, edx
0041a2d4  6689c2                   mov      dx, ax
0041a2d7  89d0                     mov      eax, edx
0041a2d9  c1e004                   shl      eax, 4
0041a2dc  01d0                     add      eax, edx
0041a2de  c1e002                   shl      eax, 2
0041a2e1  01d0                     add      eax, edx
0041a2e3  bec8a04900               mov      esi, 0x49a0c8
0041a2e8  c1e002                   shl      eax, 2
0041a2eb  01c6                     add      esi, eax
0041a2ed  8b442408                 mov      eax, dword ptr [esp + 8]
0041a2f1  668b5e06                 mov      bx, word ptr [esi + 6]
0041a2f5  01c3                     add      ebx, eax
0041a2f7  8a4604                   mov      al, byte ptr [esi + 4]
0041a2fa  66895e06                 mov      word ptr [esi + 6], bx
0041a2fe  3a0541805000             cmp      al, byte ptr [0x508041]
0041a304  7530                     jne      0x41a336
0041a306  89d0                     mov      eax, edx
0041a308  e89efdffff               call     0x41a0ab
0041a30d  83be00010000ff           cmp      dword ptr [esi + 0x100], -1
0041a314  7520                     jne      0x41a336
0041a316  50                       push     eax
0041a317  31c0                     xor      eax, eax
0041a319  8a4608                   mov      al, byte ptr [esi + 8]
0041a31c  c1e010                   shl      eax, 0x10
0041a31f  8d9e00010000             lea      ebx, [esi + 0x100]
0041a325  80cc01                   or       ah, 1
0041a328  31c9                     xor      ecx, ecx
0041a32a  89c2                     mov      edx, eax
0041a32c  b842000000               mov      eax, 0x42
0041a331  e843070700               call     0x48aa79
0041a336  31d2                     xor      edx, edx
0041a338  6689fa                   mov      dx, di
0041a33b  89d0                     mov      eax, edx
0041a33d  c1e004                   shl      eax, 4
0041a340  01d0                     add      eax, edx
0041a342  c1e002                   shl      eax, 2
0041a345  01d0                     add      eax, edx
0041a347  c1e002                   shl      eax, 2
0041a34a  05c8a04900               add      eax, 0x49a0c8
0041a34f  8a1541805000             mov      dl, byte ptr [0x508041]
0041a355  3a5004                   cmp      dl, byte ptr [eax + 4]
0041a358  7521                     jne      0x41a37b
0041a35a  803d9bfb4d0000           cmp      byte ptr [0x4dfb9b], 0
0041a361  7518                     jne      0x41a37b
0041a363  ba03000000               mov      edx, 3
0041a368  b801000000               mov      eax, 1
0041a36d  31db                     xor      ebx, ebx
0041a36f  e838feffff               call     0x41a1ac
0041a374  c6059bfb4d0001           mov      byte ptr [0x4dfb9b], 1
0041a37b  31c0                     xor      eax, eax
0041a37d  6689f8                   mov      ax, di
0041a380  890424                   mov      dword ptr [esp], eax
0041a383  89c2                     mov      edx, eax
0041a385  c1e004                   shl      eax, 4
0041a388  01d0                     add      eax, edx
0041a38a  c1e002                   shl      eax, 2
0041a38d  01d0                     add      eax, edx
0041a38f  b9c8a04900               mov      ecx, 0x49a0c8
0041a394  c1e002                   shl      eax, 2
0041a397  01c1                     add      ecx, eax
0041a399  31d2                     xor      edx, edx
0041a39b  8a5108                   mov      dl, byte ptr [ecx + 8]
0041a39e  89d0                     mov      eax, edx
0041a3a0  c1e002                   shl      eax, 2
0041a3a3  29d0                     sub      eax, edx
0041a3a5  c1e002                   shl      eax, 2
0041a3a8  01d0                     add      eax, edx
0041a3aa  31d2                     xor      edx, edx
0041a3ac  31db                     xor      ebx, ebx
0041a3ae  668b5106                 mov      dx, word ptr [ecx + 6]
0041a3b2  668b1c85905d4900         mov      bx, word ptr [eax*4 + 0x495d90]
0041a3ba  89d0                     mov      eax, edx
0041a3bc  c1e002                   shl      eax, 2
0041a3bf  29d0                     sub      eax, edx
0041a3c1  c1e003                   shl      eax, 3
0041a3c4  01c2                     add      edx, eax
0041a3c6  c1e203                   shl      edx, 3
0041a3c9  89d0                     mov      eax, edx
0041a3cb  c1fa1f                   sar      edx, 0x1f
0041a3ce  f7fb                     idiv     ebx
0041a3d0  31d2                     xor      edx, edx
0041a3d2  668b510a                 mov      dx, word ptr [ecx + 0xa]
0041a3d6  89442404                 mov      dword ptr [esp + 4], eax
0041a3da  89d0                     mov      eax, edx
0041a3dc  c1e002                   shl      eax, 2
0041a3df  29d0                     sub      eax, edx
0041a3e1  c1e003                   shl      eax, 3
0041a3e4  01c2                     add      edx, eax
0041a3e6  c1e203                   shl      edx, 3
0041a3e9  89d0                     mov      eax, edx
0041a3eb  c1fa1f                   sar      edx, 0x1f
0041a3ee  f7fb                     idiv     ebx
0041a3f0  663b442404               cmp      ax, word ptr [esp + 4]
0041a3f5  0f83b3000000             jae      0x41a4ae
0041a3fb  8a4604                   mov      al, byte ptr [esi + 4]
0041a3fe  8a7904                   mov      bh, byte ptr [ecx + 4]
0041a401  89cd                     mov      ebp, ecx
0041a403  38f8                     cmp      al, bh
0041a405  7543                     jne      0x41a44a
0041a407  ba02000000               mov      edx, 2
0041a40c  8b0424                   mov      eax, dword ptr [esp]
0041a40f  31db                     xor      ebx, ebx
0041a411  e8f2a30600               call     0x484808
0041a416  c6819000000001           mov      byte ptr [ecx + 0x90], 1
0041a41d  31c0                     xor      eax, eax
0041a41f  8a4108                   mov      al, byte ptr [ecx + 8]
0041a422  c6410503                 mov      byte ptr [ecx + 5], 3
0041a426  83f809                   cmp      eax, 9
0041a429  740c                     je       0x41a437
0041a42b  83f80c                   cmp      eax, 0xc
0041a42e  7407                     je       0x41a437
0041a430  c60544fb4d0014           mov      byte ptr [0x4dfb44], 0x14
0041a437  31c0                     xor      eax, eax
0041a439  8a4508                   mov      al, byte ptr [ebp + 8]
0041a43c  83f814                   cmp      eax, 0x14
0041a43f  7509                     jne      0x41a44a
0041a441  66c785840000001301       mov      word ptr [ebp + 0x84], 0x113
0041a44a  bb08000000               mov      ebx, 8
0041a44f  31c0                     xor      eax, eax
0041a451  31d2                     xor      edx, edx
0041a453  8a44240c                 mov      al, byte ptr [esp + 0xc]
0041a457  8a5604                   mov      dl, byte ptr [esi + 4]
0041a45a  e8b9ac0500               call     0x475118
0041a45f  31d2                     xor      edx, edx
0041a461  6689fa                   mov      dx, di
0041a464  89d0                     mov      eax, edx
0041a466  c1e004                   shl      eax, 4
0041a469  01d0                     add      eax, edx
0041a46b  c1e002                   shl      eax, 2
0041a46e  01d0                     add      eax, edx
0041a470  bac8a04900               mov      edx, 0x49a0c8
0041a475  c1e002                   shl      eax, 2
0041a478  8a2d41805000             mov      ch, byte ptr [0x508041]
0041a47e  3a6c0204                 cmp      ch, byte ptr [edx + eax + 4]
0041a482  741c                     je       0x41a4a0
0041a484  31d2                     xor      edx, edx
0041a486  88ea                     mov      dl, ch
0041a488  80bc02d8a1490000         cmp      byte ptr [edx + eax + 0x49a1d8], 0
0041a490  741c                     je       0x41a4ae
0041a492  ba04000000               mov      edx, 4
0041a497  b801000000               mov      eax, 1
0041a49c  31db                     xor      ebx, ebx
0041a49e  eb09                     jmp      0x41a4a9
0041a4a0  ba01000000               mov      edx, 1
0041a4a5  31db                     xor      ebx, ebx
0041a4a7  89d0                     mov      eax, edx
0041a4a9  e8fefcffff               call     0x41a1ac
0041a4ae  83c410                   add      esp, 0x10
0041a4b1  5d                       pop      ebp
0041a4b2  5f                       pop      edi
0041a4b3  5e                       pop      esi
0041a4b4  59                       pop      ecx
0041a4b5  c3                       ret      
; TypeBatimentGetDegat_shared_bodies [0x418b42,0x418b97)
00418b42  31c0                     xor      eax, eax
00418b44  88d8                     mov      al, bl
00418b46  8a8064fb4d00             mov      al, byte ptr [eax + 0x4dfb64]
00418b4c  30e4                     xor      ah, ah
00418b4e  c3                       ret      
00418b4f  30e4                     xor      ah, ah
00418b51  a07efb4d00               mov      al, byte ptr [0x4dfb7e]
00418b56  c3                       ret      
00418b57  80fa01                   cmp      dl, 1
00418b5a  7238                     jb       0x418b94
00418b5c  76e4                     jbe      0x418b42
00418b5e  80fa03                   cmp      dl, 3
00418b61  74ec                     je       0x418b4f
00418b63  31c0                     xor      eax, eax
00418b65  c3                       ret      
00418b66  31c0                     xor      eax, eax
00418b68  88d8                     mov      al, bl
00418b6a  8a8080fb4d00             mov      al, byte ptr [eax + 0x4dfb80]
00418b70  30e4                     xor      ah, ah
00418b72  c3                       ret      
00418b73  30e4                     xor      ah, ah
00418b75  a09afb4d00               mov      al, byte ptr [0x4dfb9a]
00418b7a  c3                       ret      
00418b7b  80fa01                   cmp      dl, 1
00418b7e  7214                     jb       0x418b94
00418b80  76e4                     jbe      0x418b66
00418b82  80fa03                   cmp      dl, 3
00418b85  74ec                     je       0x418b73
00418b87  31c0                     xor      eax, eax
00418b89  c3                       ret      
00418b8a  3c0a                     cmp      al, 0xa
00418b8c  7206                     jb       0x418b94
00418b8e  76eb                     jbe      0x418b7b
00418b90  3c0b                     cmp      al, 0xb
00418b92  74c3                     je       0x418b57
00418b94  31c0                     xor      eax, eax
00418b96  c3                       ret      
; BatimentGetVolume [0x41a0ab,0x41a18f)
0041a0ab  53                       push     ebx
0041a0ac  51                       push     ecx
0041a0ad  52                       push     edx
0041a0ae  56                       push     esi
0041a0af  57                       push     edi
0041a0b0  31d2                     xor      edx, edx
0041a0b2  6689c2                   mov      dx, ax
0041a0b5  89d0                     mov      eax, edx
0041a0b7  c1e004                   shl      eax, 4
0041a0ba  01d0                     add      eax, edx
0041a0bc  c1e002                   shl      eax, 2
0041a0bf  bbc8a04900               mov      ebx, 0x49a0c8
0041a0c4  01d0                     add      eax, edx
0041a0c6  668b5c8302               mov      bx, word ptr [ebx + eax*4 + 2]
0041a0cb  81e3ffff0000             and      ebx, 0xffff
0041a0d1  b900010000               mov      ecx, 0x100
0041a0d6  89da                     mov      edx, ebx
0041a0d8  89d8                     mov      eax, ebx
0041a0da  c1fa1f                   sar      edx, 0x1f
0041a0dd  f7f9                     idiv     ecx
0041a0df  89d7                     mov      edi, edx
0041a0e1  89da                     mov      edx, ebx
0041a0e3  89d8                     mov      eax, ebx
0041a0e5  c1fa1f                   sar      edx, 0x1f
0041a0e8  f7f9                     idiv     ecx
0041a0ea  31d2                     xor      edx, edx
0041a0ec  668b1524875000           mov      dx, word ptr [0x508724]
0041a0f3  89c3                     mov      ebx, eax
0041a0f5  89d0                     mov      eax, edx
0041a0f7  c1fa1f                   sar      edx, 0x1f
0041a0fa  2bc2                     sub      eax, edx
0041a0fc  d1f8                     sar      eax, 1
0041a0fe  31d2                     xor      edx, edx
0041a100  668b1520875000           mov      dx, word ptr [0x508720]
0041a107  01d0                     add      eax, edx
0041a109  31d2                     xor      edx, edx
0041a10b  668b1526875000           mov      dx, word ptr [0x508726]
0041a112  89c6                     mov      esi, eax
0041a114  89d0                     mov      eax, edx
0041a116  c1fa1f                   sar      edx, 0x1f
0041a119  2bc2                     sub      eax, edx
0041a11b  d1f8                     sar      eax, 1
0041a11d  31d2                     xor      edx, edx
0041a11f  31c9                     xor      ecx, ecx
0041a121  668b1522875000           mov      dx, word ptr [0x508722]
0041a128  6689d9                   mov      cx, bx
0041a12b  01d0                     add      eax, edx
0041a12d  31d2                     xor      edx, edx
0041a12f  31db                     xor      ebx, ebx
0041a131  6689c2                   mov      dx, ax
0041a134  31c0                     xor      eax, eax
0041a136  6689fb                   mov      bx, di
0041a139  6689f0                   mov      ax, si
0041a13c  e814f40500               call     0x479555
0041a141  89c3                     mov      ebx, eax
0041a143  89c2                     mov      edx, eax
0041a145  31c0                     xor      eax, eax
0041a147  81fb91000000             cmp      ebx, 0x91
0041a14d  7f0a                     jg       0x41a159
0041a14f  b800010000               mov      eax, 0x100
0041a154  e9c5390000               jmp      0x41db1e
0041a159  7e12                     jle      0x41a16d
0041a15b  81fb2c010000             cmp      ebx, 0x12c
0041a161  7f0a                     jg       0x41a16d
0041a163  b8b4000000               mov      eax, 0xb4
0041a168  e9b1390000               jmp      0x41db1e
0041a16d  81fa2c010000             cmp      edx, 0x12c
0041a173  0f8ea5390000             jle      0x41db1e
0041a179  81fa58020000             cmp      edx, 0x258
0041a17f  0f8d99390000             jge      0x41db1e
0041a185  b864000000               mov      eax, 0x64
0041a18a  e98f390000               jmp      0x41db1e
; Batiment_shared_return [0x41db1e,0x41db24)
0041db1e  5f                       pop      edi
0041db1f  5e                       pop      esi
0041db20  5a                       pop      edx
0041db21  59                       pop      ecx
0041db22  5b                       pop      ebx
0041db23  c3                       ret      
; VoixOffAsk [0x41a1ac,0x41a255)
0041a1ac  51                       push     ecx
0041a1ad  56                       push     esi
0041a1ae  88d9                     mov      cl, bl
0041a1b0  31db                     xor      ebx, ebx
0041a1b2  6689c3                   mov      bx, ax
0041a1b5  89d8                     mov      eax, ebx
0041a1b7  c1e004                   shl      eax, 4
0041a1ba  01d8                     add      eax, ebx
0041a1bc  c1e002                   shl      eax, 2
0041a1bf  01d8                     add      eax, ebx
0041a1c1  bec8a04900               mov      esi, 0x49a0c8
0041a1c6  c1e002                   shl      eax, 2
0041a1c9  01c6                     add      esi, eax
0041a1cb  8d8600010000             lea      eax, [esi + 0x100]
0041a1d1  31db                     xor      ebx, ebx
0041a1d3  e8e8080700               call     0x48aac0
0041a1d8  6683fa06                 cmp      dx, 6
0041a1dc  7717                     ja       0x41a1f5
0041a1de  31c0                     xor      eax, eax
0041a1e0  6689d0                   mov      ax, dx
0041a1e3  2eff248590a14100         jmp      dword ptr cs:[eax*4 + 0x41a190]
0041a1eb  bb01000000               mov      ebx, 1
0041a1f0  ba03000000               mov      edx, 3
0041a1f5  6800010000               push     0x100
0041a1fa  81e1ff000000             and      ecx, 0xff
0041a200  8d8600010000             lea      eax, [esi + 0x100]
0041a206  81e3ffff0000             and      ebx, 0xffff
0041a20c  c1e310                   shl      ebx, 0x10
0041a20f  81e2ffff0000             and      edx, 0xffff
0041a215  c1e208                   shl      edx, 8
0041a218  09da                     or       edx, ebx
0041a21a  89c3                     mov      ebx, eax
0041a21c  b841000000               mov      eax, 0x41
0041a221  e853080700               call     0x48aa79
0041a226  5e                       pop      esi
0041a227  59                       pop      ecx
0041a228  c3                       ret      
0041a229  bb02000000               mov      ebx, 2
0041a22e  eb1a                     jmp      0x41a24a
0041a230  bb02000000               mov      ebx, 2
0041a235  ba01000000               mov      edx, 1
0041a23a  ebb9                     jmp      0x41a1f5
0041a23c  bb02000000               mov      ebx, 2
0041a241  89da                     mov      edx, ebx
0041a243  ebb0                     jmp      0x41a1f5
0041a245  bb01000000               mov      ebx, 1
0041a24a  31d2                     xor      edx, edx
0041a24c  eba7                     jmp      0x41a1f5
0041a24e  bb01000000               mov      ebx, 1
0041a253  ebec                     jmp      0x41a241
; CibleTourelleValide [0x424624,0x42484b)
00424624  53                       push     ebx
00424625  51                       push     ecx
00424626  52                       push     edx
00424627  56                       push     esi
00424628  57                       push     edi
00424629  55                       push     ebp
0042462a  83ec04                   sub      esp, 4
0042462d  31d2                     xor      edx, edx
0042462f  6689c2                   mov      dx, ax
00424632  89d0                     mov      eax, edx
00424634  c1e004                   shl      eax, 4
00424637  01d0                     add      eax, edx
00424639  c1e002                   shl      eax, 2
0042463c  01d0                     add      eax, edx
0042463e  bbc8a04900               mov      ebx, 0x49a0c8
00424643  c1e002                   shl      eax, 2
00424646  01c3                     add      ebx, eax
00424648  31c0                     xor      eax, eax
0042464a  668b8386000000           mov      ax, word ptr [ebx + 0x86]
00424651  3dffff0000               cmp      eax, 0xffff
00424656  7541                     jne      0x424699
00424658  e9e4010000               jmp      0x424841
0042465d  b914000000               mov      ecx, 0x14
00424662  e9c5010000               jmp      0x42482c
00424667  b90a000000               mov      ecx, 0xa
0042466c  e9bb010000               jmp      0x42482c
00424671  b908000000               mov      ecx, 8
00424676  e9b1010000               jmp      0x42482c
0042467b  b904000000               mov      ecx, 4
00424680  e9a7010000               jmp      0x42482c
00424685  b905000000               mov      ecx, 5
0042468a  e99d010000               jmp      0x42482c
0042468f  b907000000               mov      ecx, 7
00424694  e993010000               jmp      0x42482c
00424699  31f6                     xor      esi, esi
0042469b  668b7302                 mov      si, word ptr [ebx + 2]
0042469f  bd00010000               mov      ebp, 0x100
004246a4  89f2                     mov      edx, esi
004246a6  89f0                     mov      eax, esi
004246a8  c1fa1f                   sar      edx, 0x1f
004246ab  f7fd                     idiv     ebp
004246ad  89d7                     mov      edi, edx
004246af  89f2                     mov      edx, esi
004246b1  89f0                     mov      eax, esi
004246b3  c1fa1f                   sar      edx, 0x1f
004246b6  f7fd                     idiv     ebp
004246b8  89c6                     mov      esi, eax
004246ba  8a4308                   mov      al, byte ptr [ebx + 8]
004246bd  3c15                     cmp      al, 0x15
004246bf  0f8767010000             ja       0x42482c
004246c5  25ff000000               and      eax, 0xff
004246ca  2eff2485cc454200         jmp      dword ptr cs:[eax*4 + 0x4245cc]
004246d2  31c0                     xor      eax, eax
004246d4  668b8386000000           mov      ax, word ptr [ebx + 0x86]
004246db  e8cdf60100               call     0x443dad
004246e0  84c0                     test     al, al
004246e2  0f8459010000             je       0x424841
004246e8  31c0                     xor      eax, eax
004246ea  668b8386000000           mov      ax, word ptr [ebx + 0x86]
004246f1  e84fd90100               call     0x442045
004246f6  25ff000000               and      eax, 0xff
004246fb  3dc8000000               cmp      eax, 0xc8
00424700  0f843b010000             je       0x424841
00424706  31c0                     xor      eax, eax
00424708  668b8386000000           mov      ax, word ptr [ebx + 0x86]
0042470f  e8fdc60100               call     0x440e11
00424714  25ff000000               and      eax, 0xff
00424719  83f80e                   cmp      eax, 0xe
0042471c  0f841f010000             je       0x424841
00424722  31c0                     xor      eax, eax
00424724  668b8386000000           mov      ax, word ptr [ebx + 0x86]
0042472b  31d2                     xor      edx, edx
0042472d  e80cca0100               call     0x44113e
00424732  6689c2                   mov      dx, ax
00424735  bd00010000               mov      ebp, 0x100
0042473a  89d0                     mov      eax, edx
0042473c  c1fa1f                   sar      edx, 0x1f
0042473f  f7fd                     idiv     ebp
00424741  31c0                     xor      eax, eax
00424743  891424                   mov      dword ptr [esp], edx
00424746  668b8386000000           mov      ax, word ptr [ebx + 0x86]
0042474d  31d2                     xor      edx, edx
0042474f  e8eac90100               call     0x44113e
00424754  6689c2                   mov      dx, ax
00424757  89d0                     mov      eax, edx
00424759  c1fa1f                   sar      edx, 0x1f
0042475c  f7fd                     idiv     ebp
0042475e  89c2                     mov      edx, eax
00424760  31c0                     xor      eax, eax
00424762  6689c8                   mov      ax, cx
00424765  89c5                     mov      ebp, eax
00424767  0fafe8                   imul     ebp, eax
0042476a  31db                     xor      ebx, ebx
0042476c  31c9                     xor      ecx, ecx
0042476e  668b1c24                 mov      bx, word ptr [esp]
00424772  6689d1                   mov      cx, dx
00424775  31d2                     xor      edx, edx
00424777  31c0                     xor      eax, eax
00424779  6689f2                   mov      dx, si
0042477c  6689f8                   mov      ax, di
0042477f  e8d14d0500               call     0x479555
00424784  39e8                     cmp      eax, ebp
00424786  0f87b5000000             ja       0x424841
0042478c  b001                     mov      al, 1
0042478e  e9b0000000               jmp      0x424843
00424793  668b8386000000           mov      ax, word ptr [ebx + 0x86]
0042479a  31d2                     xor      edx, edx
0042479c  6689c2                   mov      dx, ax
0042479f  89d0                     mov      eax, edx
004247a1  c1e004                   shl      eax, 4
004247a4  01d0                     add      eax, edx
004247a6  c1e002                   shl      eax, 2
004247a9  01d0                     add      eax, edx
004247ab  c1e002                   shl      eax, 2
004247ae  05c8a04900               add      eax, 0x49a0c8
004247b3  8a4005                   mov      al, byte ptr [eax + 5]
004247b6  25ff000000               and      eax, 0xff
004247bb  0f95c0                   setne    al
004247be  84c0                     test     al, al
004247c0  0f847b000000             je       0x424841
004247c6  31c0                     xor      eax, eax
004247c8  8a4304                   mov      al, byte ptr [ebx + 4]
004247cb  3dc8000000               cmp      eax, 0xc8
004247d0  746f                     je       0x424841
004247d2  31c0                     xor      eax, eax
004247d4  6689d0                   mov      ax, dx
004247d7  31d2                     xor      edx, edx
004247d9  e80467ffff               call     0x41aee2
004247de  6689c2                   mov      dx, ax
004247e1  b900010000               mov      ecx, 0x100
004247e6  89d0                     mov      eax, edx
004247e8  c1fa1f                   sar      edx, 0x1f
004247eb  f7f9                     idiv     ecx
004247ed  31c0                     xor      eax, eax
004247ef  891424                   mov      dword ptr [esp], edx
004247f2  668b8386000000           mov      ax, word ptr [ebx + 0x86]
004247f9  31d2                     xor      edx, edx
004247fb  e8e266ffff               call     0x41aee2
00424800  6689c2                   mov      dx, ax
00424803  89d0                     mov      eax, edx
00424805  c1fa1f                   sar      edx, 0x1f
00424808  f7f9                     idiv     ecx
0042480a  31db                     xor      ebx, ebx
0042480c  668b1c24                 mov      bx, word ptr [esp]
00424810  31c9                     xor      ecx, ecx
00424812  31d2                     xor      edx, edx
00424814  6689c1                   mov      cx, ax
00424817  31c0                     xor      eax, eax
00424819  6689f2                   mov      dx, si
0042481c  6689f8                   mov      ax, di
0042481f  e8314d0500               call     0x479555
00424824  83f864                   cmp      eax, 0x64
00424827  e95affffff               jmp      0x424786
0042482c  8a437b                   mov      al, byte ptr [ebx + 0x7b]
0042482f  3c01                     cmp      al, 1
00424831  720e                     jb       0x424841
00424833  0f8699feffff             jbe      0x4246d2
00424839  3c03                     cmp      al, 3
0042483b  0f8452ffffff             je       0x424793
00424841  30c0                     xor      al, al
00424843  83c404                   add      esp, 4
00424846  e9d292ffff               jmp      0x41db1d
; RechercheDecalageProjectile [0x425100,0x425516)
00425100  56                       push     esi
00425101  57                       push     edi
00425102  88d4                     mov      ah, dl
00425104  31d2                     xor      edx, edx
00425106  88e2                     mov      dl, ah
00425108  83fa0b                   cmp      edx, 0xb
0042510b  0f84d4010000             je       0x4252e5
00425111  83fa0a                   cmp      edx, 0xa
00425114  0f84b1030000             je       0x4254cb
0042511a  5f                       pop      edi
0042511b  5e                       pop      esi
0042511c  c20800                   ret      8
0042511f  bff5ffffff               mov      edi, 0xfffffff5
00425124  be03000000               mov      esi, 3
00425129  6a00                     push     0
0042512b  0fbfc6                   movsx    eax, si
0042512e  50                       push     eax
0042512f  0fbfc7                   movsx    eax, di
00425132  50                       push     eax
00425133  31c0                     xor      eax, eax
00425135  6a00                     push     0
00425137  668b442420               mov      ax, word ptr [esp + 0x20]
0042513c  31d2                     xor      edx, edx
0042513e  50                       push     eax
0042513f  31c0                     xor      eax, eax
00425141  6689da                   mov      dx, bx
00425144  6689c8                   mov      ax, cx
00425147  b903000000               mov      ecx, 3
0042514c  89c3                     mov      ebx, eax
0042514e  b814000000               mov      eax, 0x14
00425153  e9b4030000               jmp      0x42550c
00425158  bff6ffffff               mov      edi, 0xfffffff6
0042515d  befeffffff               mov      esi, 0xfffffffe
00425162  ebc5                     jmp      0x425129
00425164  bff7ffffff               mov      edi, 0xfffffff7
00425169  bef9ffffff               mov      esi, 0xfffffff9
0042516e  ebb9                     jmp      0x425129
00425170  bff9ffffff               mov      edi, 0xfffffff9
00425175  bef5ffffff               mov      esi, 0xfffffff5
0042517a  ebad                     jmp      0x425129
0042517c  bffeffffff               mov      edi, 0xfffffffe
00425181  beefffffff               mov      esi, 0xffffffef
00425186  eba1                     jmp      0x425129
00425188  bf02000000               mov      edi, 2
0042518d  beecffffff               mov      esi, 0xffffffec
00425192  eb95                     jmp      0x425129
00425194  bf09000000               mov      edi, 9
00425199  bee9ffffff               mov      esi, 0xffffffe9
0042519e  eb89                     jmp      0x425129
004251a0  bf11000000               mov      edi, 0x11
004251a5  bee6ffffff               mov      esi, 0xffffffe6
004251aa  e97affffff               jmp      0x425129
004251af  bf18000000               mov      edi, 0x18
004251b4  ebef                     jmp      0x4251a5
004251b6  bf20000000               mov      edi, 0x20
004251bb  bee7ffffff               mov      esi, 0xffffffe7
004251c0  e964ffffff               jmp      0x425129
004251c5  bf26000000               mov      edi, 0x26
004251ca  ebcd                     jmp      0x425199
004251cc  bf2d000000               mov      edi, 0x2d
004251d1  beebffffff               mov      esi, 0xffffffeb
004251d6  e94effffff               jmp      0x425129
004251db  bf32000000               mov      edi, 0x32
004251e0  bef0ffffff               mov      esi, 0xfffffff0
004251e5  e93fffffff               jmp      0x425129
004251ea  bf35000000               mov      edi, 0x35
004251ef  bef3ffffff               mov      esi, 0xfffffff3
004251f4  e930ffffff               jmp      0x425129
004251f9  bf3a000000               mov      edi, 0x3a
004251fe  e966ffffff               jmp      0x425169
00425203  bf3a000000               mov      edi, 0x3a
00425208  e950ffffff               jmp      0x42515d
0042520d  bf3b000000               mov      edi, 0x3b
00425212  be04000000               mov      esi, 4
00425217  e90dffffff               jmp      0x425129
0042521c  bf3b000000               mov      edi, 0x3b
00425221  be07000000               mov      esi, 7
00425226  e9fefeffff               jmp      0x425129
0042522b  bf3a000000               mov      edi, 0x3a
00425230  be0c000000               mov      esi, 0xc
00425235  e9effeffff               jmp      0x425129
0042523a  bf36000000               mov      edi, 0x36
0042523f  be10000000               mov      esi, 0x10
00425244  e9e0feffff               jmp      0x425129
00425249  bf31000000               mov      edi, 0x31
0042524e  be16000000               mov      esi, 0x16
00425253  e9d1feffff               jmp      0x425129
00425258  bf2c000000               mov      edi, 0x2c
0042525d  be1a000000               mov      esi, 0x1a
00425262  e9c2feffff               jmp      0x425129
00425267  bf26000000               mov      edi, 0x26
0042526c  be1b000000               mov      esi, 0x1b
00425271  e9b3feffff               jmp      0x425129
00425276  bf1f000000               mov      edi, 0x1f
0042527b  ebef                     jmp      0x42526c
0042527d  bf19000000               mov      edi, 0x19
00425282  be1c000000               mov      esi, 0x1c
00425287  e99dfeffff               jmp      0x425129
0042528c  bf12000000               mov      edi, 0x12
00425291  ebef                     jmp      0x425282
00425293  bf0a000000               mov      edi, 0xa
00425298  be19000000               mov      esi, 0x19
0042529d  e987feffff               jmp      0x425129
004252a2  bf05000000               mov      edi, 5
004252a7  be17000000               mov      esi, 0x17
004252ac  e978feffff               jmp      0x425129
004252b1  be13000000               mov      esi, 0x13
004252b6  31ff                     xor      edi, edi
004252b8  e96cfeffff               jmp      0x425129
004252bd  bffbffffff               mov      edi, 0xfffffffb
004252c2  e978ffffff               jmp      0x42523f
004252c7  bff8ffffff               mov      edi, 0xfffffff8
004252cc  be0b000000               mov      esi, 0xb
004252d1  e953feffff               jmp      0x425129
004252d6  bff6ffffff               mov      edi, 0xfffffff6
004252db  be08000000               mov      esi, 8
004252e0  e944feffff               jmp      0x425129
004252e5  fec8                     dec      al
004252e7  3c1f                     cmp      al, 0x1f
004252e9  0f873afeffff             ja       0x425129
004252ef  25ff000000               and      eax, 0xff
004252f4  2eff248500504200         jmp      dword ptr cs:[eax*4 + 0x425000]
004252fc  bff7ffffff               mov      edi, 0xfffffff7
00425301  bef1ffffff               mov      esi, 0xfffffff1
00425306  31c0                     xor      eax, eax
00425308  668b44240c               mov      ax, word ptr [esp + 0xc]
0042530d  e813cd0100               call     0x442025
00425312  25ff000000               and      eax, 0xff
00425317  e8b3cf0100               call     0x4422cf
0042531c  84c0                     test     al, al
0042531e  0f84be010000             je       0x4254e2
00425324  6a01                     push     1
00425326  0fbfc6                   movsx    eax, si
00425329  50                       push     eax
0042532a  0fbfc7                   movsx    eax, di
0042532d  50                       push     eax
0042532e  31c0                     xor      eax, eax
00425330  6a00                     push     0
00425332  668b442420               mov      ax, word ptr [esp + 0x20]
00425337  31d2                     xor      edx, edx
00425339  50                       push     eax
0042533a  31c0                     xor      eax, eax
0042533c  6689da                   mov      dx, bx
0042533f  6689c8                   mov      ax, cx
00425342  b903000000               mov      ecx, 3
00425347  89c3                     mov      ebx, eax
00425349  b815000000               mov      eax, 0x15
0042534e  e9b9010000               jmp      0x42550c
00425353  bff7ffffff               mov      edi, 0xfffffff7
00425358  bee8ffffff               mov      esi, 0xffffffe8
0042535d  eba7                     jmp      0x425306
0042535f  bff9ffffff               mov      edi, 0xfffffff9
00425364  bee3ffffff               mov      esi, 0xffffffe3
00425369  eb9b                     jmp      0x425306
0042536b  bffdffffff               mov      edi, 0xfffffffd
00425370  beddffffff               mov      esi, 0xffffffdd
00425375  eb8f                     jmp      0x425306
00425377  bf01000000               mov      edi, 1
0042537c  bedbffffff               mov      esi, 0xffffffdb
00425381  eb83                     jmp      0x425306
00425383  bf07000000               mov      edi, 7
00425388  bed7ffffff               mov      esi, 0xffffffd7
0042538d  e974ffffff               jmp      0x425306
00425392  bf0d000000               mov      edi, 0xd
00425397  bed5ffffff               mov      esi, 0xffffffd5
0042539c  e965ffffff               jmp      0x425306
004253a1  bf11000000               mov      edi, 0x11
004253a6  ebef                     jmp      0x425397
004253a8  bf17000000               mov      edi, 0x17
004253ad  ebe8                     jmp      0x425397
004253af  bf1e000000               mov      edi, 0x1e
004253b4  ebe1                     jmp      0x425397
004253b6  bf24000000               mov      edi, 0x24
004253bb  bed6ffffff               mov      esi, 0xffffffd6
004253c0  e941ffffff               jmp      0x425306
004253c5  bf2b000000               mov      edi, 0x2b
004253ca  bed8ffffff               mov      esi, 0xffffffd8
004253cf  e932ffffff               jmp      0x425306
004253d4  bf2e000000               mov      edi, 0x2e
004253d9  eba1                     jmp      0x42537c
004253db  bf34000000               mov      edi, 0x34
004253e0  bedfffffff               mov      esi, 0xffffffdf
004253e5  e91cffffff               jmp      0x425306
004253ea  bf36000000               mov      edi, 0x36
004253ef  e970ffffff               jmp      0x425364
004253f4  bf38000000               mov      edi, 0x38
004253f9  e95affffff               jmp      0x425358
004253fe  bf38000000               mov      edi, 0x38
00425403  beedffffff               mov      esi, 0xffffffed
00425408  e9f9feffff               jmp      0x425306
0042540d  bf38000000               mov      edi, 0x38
00425412  bef4ffffff               mov      esi, 0xfffffff4
00425417  e9eafeffff               jmp      0x425306
0042541c  bf37000000               mov      edi, 0x37
00425421  bef8ffffff               mov      esi, 0xfffffff8
00425426  e9dbfeffff               jmp      0x425306
0042542b  bf33000000               mov      edi, 0x33
00425430  befcffffff               mov      esi, 0xfffffffc
00425435  e9ccfeffff               jmp      0x425306
0042543a  bf2f000000               mov      edi, 0x2f
0042543f  31f6                     xor      esi, esi
00425441  e9c0feffff               jmp      0x425306
00425446  bf29000000               mov      edi, 0x29
0042544b  be03000000               mov      esi, 3
00425450  e9b1feffff               jmp      0x425306
00425455  bf23000000               mov      edi, 0x23
0042545a  be05000000               mov      esi, 5
0042545f  e9a2feffff               jmp      0x425306
00425464  bf1e000000               mov      edi, 0x1e
00425469  be06000000               mov      esi, 6
0042546e  e993feffff               jmp      0x425306
00425473  bf19000000               mov      edi, 0x19
00425478  ebef                     jmp      0x425469
0042547a  bf12000000               mov      edi, 0x12
0042547f  ebe8                     jmp      0x425469
00425481  bf0d000000               mov      edi, 0xd
00425486  ebd2                     jmp      0x42545a
00425488  bf07000000               mov      edi, 7
0042548d  be02000000               mov      esi, 2
00425492  e96ffeffff               jmp      0x425306
00425497  bf02000000               mov      edi, 2
0042549c  eba1                     jmp      0x42543f
0042549e  bffeffffff               mov      edi, 0xfffffffe
004254a3  befdffffff               mov      esi, 0xfffffffd
004254a8  e959feffff               jmp      0x425306
004254ad  bffbffffff               mov      edi, 0xfffffffb
004254b2  bef9ffffff               mov      esi, 0xfffffff9
004254b7  e94afeffff               jmp      0x425306
004254bc  bff7ffffff               mov      edi, 0xfffffff7
004254c1  bef3ffffff               mov      esi, 0xfffffff3
004254c6  e93bfeffff               jmp      0x425306
004254cb  fec8                     dec      al
004254cd  3c1f                     cmp      al, 0x1f
004254cf  0f8731feffff             ja       0x425306
004254d5  25ff000000               and      eax, 0xff
004254da  2eff248580504200         jmp      dword ptr cs:[eax*4 + 0x425080]
004254e2  6a00                     push     0
004254e4  0fbfc6                   movsx    eax, si
004254e7  50                       push     eax
004254e8  0fbfc7                   movsx    eax, di
004254eb  50                       push     eax
004254ec  31c0                     xor      eax, eax
004254ee  6a00                     push     0
004254f0  668b442420               mov      ax, word ptr [esp + 0x20]
004254f5  31d2                     xor      edx, edx
004254f7  50                       push     eax
004254f8  31c0                     xor      eax, eax
004254fa  6689da                   mov      dx, bx
004254fd  6689c8                   mov      ax, cx
00425500  b903000000               mov      ecx, 3
00425505  89c3                     mov      ebx, eax
00425507  b815000000               mov      eax, 0x15
0042550c  e83b8f0400               call     0x46e44c
00425511  5f                       pop      edi
00425512  5e                       pop      esi
00425513  c20800                   ret      8
; BatimentNextEtape_type10 [0x426e43,0x427549)
00426e43  31d2                     xor      edx, edx
00426e45  6689fa                   mov      dx, di
00426e48  89d0                     mov      eax, edx
00426e4a  c1e004                   shl      eax, 4
00426e4d  01d0                     add      eax, edx
00426e4f  c1e002                   shl      eax, 2
00426e52  bbc8a04900               mov      ebx, 0x49a0c8
00426e57  01d0                     add      eax, edx
00426e59  31d2                     xor      edx, edx
00426e5b  c1e002                   shl      eax, 2
00426e5e  6689fa                   mov      dx, di
00426e61  01c3                     add      ebx, eax
00426e63  89d0                     mov      eax, edx
00426e65  c1e004                   shl      eax, 4
00426e68  01d0                     add      eax, edx
00426e6a  c1e002                   shl      eax, 2
00426e6d  01d0                     add      eax, edx
00426e6f  bac8a04900               mov      edx, 0x49a0c8
00426e74  c1e002                   shl      eax, 2
00426e77  01d0                     add      eax, edx
00426e79  89f9                     mov      ecx, edi
00426e7b  8a4008                   mov      al, byte ptr [eax + 8]
00426e7e  25ff000000               and      eax, 0xff
00426e83  83f815                   cmp      eax, 0x15
00426e86  7510                     jne      0x426e98
00426e88  8d430c                   lea      eax, [ebx + 0xc]
00426e8b  e8ba030200               call     0x44724a
00426e90  84c0                     test     al, al
00426e92  744b                     je       0x426edf
00426e94  b001                     mov      al, 1
00426e96  eb49                     jmp      0x426ee1
00426e98  31d2                     xor      edx, edx
00426e9a  6689fa                   mov      dx, di
00426e9d  89d0                     mov      eax, edx
00426e9f  c1e004                   shl      eax, 4
00426ea2  01d0                     add      eax, edx
00426ea4  c1e002                   shl      eax, 2
00426ea7  01d0                     add      eax, edx
00426ea9  bac8a04900               mov      edx, 0x49a0c8
00426eae  8a448208                 mov      al, byte ptr [edx + eax*4 + 8]
00426eb2  25ff000000               and      eax, 0xff
00426eb7  83f802                   cmp      eax, 2
00426eba  750c                     jne      0x426ec8
00426ebc  8d430c                   lea      eax, [ebx + 0xc]
00426ebf  e886030200               call     0x44724a
00426ec4  84c0                     test     al, al
00426ec6  75cc                     jne      0x426e94
00426ec8  8d430c                   lea      eax, [ebx + 0xc]
00426ecb  ba01000000               mov      edx, 1
00426ed0  bb09000000               mov      ebx, 9
00426ed5  e8de020200               call     0x4471b8
00426eda  6685c0                   test     ax, ax
00426edd  ebb3                     jmp      0x426e92
00426edf  30c0                     xor      al, al
00426ee1  84c0                     test     al, al
00426ee3  0f8449060000             je       0x427532
00426ee9  31d2                     xor      edx, edx
00426eeb  6689fa                   mov      dx, di
00426eee  89d0                     mov      eax, edx
00426ef0  e82fd7ffff               call     0x424624
00426ef5  84c0                     test     al, al
00426ef7  0f8595000000             jne      0x426f92
00426efd  884676                   mov      byte ptr [esi + 0x76], al
00426f00  884674                   mov      byte ptr [esi + 0x74], al
00426f03  89d0                     mov      eax, edx
00426f05  c1e004                   shl      eax, 4
00426f08  01d0                     add      eax, edx
00426f0a  c1e002                   shl      eax, 2
00426f0d  bbc8a04900               mov      ebx, 0x49a0c8
00426f12  01d0                     add      eax, edx
00426f14  66c746780000             mov      word ptr [esi + 0x78], 0
00426f1a  c1e002                   shl      eax, 2
00426f1d  66c78686000000ffff       mov      word ptr [esi + 0x86], 0xffff
00426f26  01c3                     add      ebx, eax
00426f28  31c0                     xor      eax, eax
00426f2a  8b0d7c8f5000             mov      ecx, dword ptr [0x508f7c]
00426f30  6689f8                   mov      ax, di
00426f33  01c8                     add      eax, ecx
00426f35  a81f                     test     al, 0x1f
00426f37  7407                     je       0x426f40
00426f39  b8ffff0000               mov      eax, 0xffff
00426f3e  eb4b                     jmp      0x426f8b
00426f40  89d0                     mov      eax, edx
00426f42  e872d0ffff               call     0x423fb9
00426f47  8945ec                   mov      dword ptr [ebp - 0x14], eax
00426f4a  25ffff0000               and      eax, 0xffff
00426f4f  3dffff0000               cmp      eax, 0xffff
00426f54  740f                     je       0x426f65
00426f56  66c783880000000000       mov      word ptr [ebx + 0x88], 0
00426f5f  c6437b01                 mov      byte ptr [ebx + 0x7b], 1
00426f63  eb23                     jmp      0x426f88
00426f65  89d0                     mov      eax, edx
00426f67  e8b7d1ffff               call     0x424123
00426f6c  8945ec                   mov      dword ptr [ebp - 0x14], eax
00426f6f  25ffff0000               and      eax, 0xffff
00426f74  3dffff0000               cmp      eax, 0xffff
00426f79  740d                     je       0x426f88
00426f7b  66c783880000000000       mov      word ptr [ebx + 0x88], 0
00426f84  c6437b03                 mov      byte ptr [ebx + 0x7b], 3
00426f88  8b45ec                   mov      eax, dword ptr [ebp - 0x14]
00426f8b  66898686000000           mov      word ptr [esi + 0x86], ax
00426f92  31c0                     xor      eax, eax
00426f94  668b8686000000           mov      ax, word ptr [esi + 0x86]
00426f9b  3dffff0000               cmp      eax, 0xffff
00426fa0  0f849f040000             je       0x427445
00426fa6  31c0                     xor      eax, eax
00426fa8  8a467b                   mov      al, byte ptr [esi + 0x7b]
00426fab  c6467401                 mov      byte ptr [esi + 0x74], 1
00426faf  83f801                   cmp      eax, 1
00426fb2  0f858d000000             jne      0x427045
00426fb8  31c0                     xor      eax, eax
00426fba  6a20                     push     0x20
00426fbc  668b8686000000           mov      ax, word ptr [esi + 0x86]
00426fc3  31d2                     xor      edx, edx
00426fc5  e8269e0100               call     0x440df0
00426fca  6689c2                   mov      dx, ax
00426fcd  89d0                     mov      eax, edx
00426fcf  c1fa1f                   sar      edx, 0x1f
00426fd2  c1e208                   shl      edx, 8
00426fd5  1bc2                     sbb      eax, edx
00426fd7  c1f808                   sar      eax, 8
00426fda  31c9                     xor      ecx, ecx
00426fdc  6689c1                   mov      cx, ax
00426fdf  31c0                     xor      eax, eax
00426fe1  668b8686000000           mov      ax, word ptr [esi + 0x86]
00426fe8  31d2                     xor      edx, edx
00426fea  e8019e0100               call     0x440df0
00426fef  6689c2                   mov      dx, ax
00426ff2  bb00010000               mov      ebx, 0x100
00426ff7  89d0                     mov      eax, edx
00426ff9  c1fa1f                   sar      edx, 0x1f
00426ffc  f7fb                     idiv     ebx
00426ffe  31db                     xor      ebx, ebx
00427000  31c0                     xor      eax, eax
00427002  668b5e02                 mov      bx, word ptr [esi + 2]
00427006  6689d0                   mov      ax, dx
00427009  81eb00010000             sub      ebx, 0x100
0042700f  8945d4                   mov      dword ptr [ebp - 0x2c], eax
00427012  89da                     mov      edx, ebx
00427014  89d8                     mov      eax, ebx
00427016  c1fa1f                   sar      edx, 0x1f
00427019  c1e208                   shl      edx, 8
0042701c  1bc2                     sbb      eax, edx
0042701e  c1f808                   sar      eax, 8
00427021  25ffff0000               and      eax, 0xffff
00427026  89da                     mov      edx, ebx
00427028  8945cc                   mov      dword ptr [ebp - 0x34], eax
0042702b  b800010000               mov      eax, 0x100
00427030  c1fa1f                   sar      edx, 0x1f
00427033  8945d0                   mov      dword ptr [ebp - 0x30], eax
00427036  89d8                     mov      eax, ebx
00427038  f77dd0                   idiv     dword ptr [ebp - 0x30]
0042703b  31c0                     xor      eax, eax
0042703d  8b5dd4                   mov      ebx, dword ptr [ebp - 0x2c]
00427040  e94f010000               jmp      0x427194
00427045  83f803                   cmp      eax, 3
00427048  0f8557010000             jne      0x4271a5
0042704e  668b8686000000           mov      ax, word ptr [esi + 0x86]
00427055  31d2                     xor      edx, edx
00427057  6689c2                   mov      dx, ax
0042705a  89d0                     mov      eax, edx
0042705c  c1e004                   shl      eax, 4
0042705f  01d0                     add      eax, edx
00427061  c1e002                   shl      eax, 2
00427064  01d0                     add      eax, edx
00427066  bac8a04900               mov      edx, 0x49a0c8
0042706b  c1e002                   shl      eax, 2
0042706e  01c2                     add      edx, eax
00427070  31db                     xor      ebx, ebx
00427072  8a4208                   mov      al, byte ptr [edx + 8]
00427075  88c3                     mov      bl, al
00427077  89d8                     mov      eax, ebx
00427079  c1e002                   shl      eax, 2
0042707c  29d8                     sub      eax, ebx
0042707e  c1e002                   shl      eax, 2
00427081  01c3                     add      ebx, eax
00427083  c1e302                   shl      ebx, 2
00427086  668b838c5d4900           mov      ax, word ptr [ebx + 0x495d8c]
0042708d  8945f0                   mov      dword ptr [ebp - 0x10], eax
00427090  668b838e5d4900           mov      ax, word ptr [ebx + 0x495d8e]
00427097  8945fc                   mov      dword ptr [ebp - 4], eax
0042709a  8b45f0                   mov      eax, dword ptr [ebp - 0x10]
0042709d  8b5dfc                   mov      ebx, dword ptr [ebp - 4]
004270a0  66d1e8                   shr      ax, 1
004270a3  66d1eb                   shr      bx, 1
004270a6  8945f0                   mov      dword ptr [ebp - 0x10], eax
004270a9  895dfc                   mov      dword ptr [ebp - 4], ebx
004270ac  89d8                     mov      eax, ebx
004270ae  8b4df0                   mov      ecx, dword ptr [ebp - 0x10]
004270b1  c1e008                   shl      eax, 8
004270b4  668b5a02                 mov      bx, word ptr [edx + 2]
004270b8  01c8                     add      eax, ecx
004270ba  31d2                     xor      edx, edx
004270bc  01d8                     add      eax, ebx
004270be  6689c2                   mov      dx, ax
004270c1  89d0                     mov      eax, edx
004270c3  c1fa1f                   sar      edx, 0x1f
004270c6  c1e208                   shl      edx, 8
004270c9  1bc2                     sbb      eax, edx
004270cb  c1f808                   sar      eax, 8
004270ce  31c9                     xor      ecx, ecx
004270d0  6689c1                   mov      cx, ax
004270d3  31d2                     xor      edx, edx
004270d5  668b8686000000           mov      ax, word ptr [esi + 0x86]
004270dc  6689c2                   mov      dx, ax
004270df  89d0                     mov      eax, edx
004270e1  c1e004                   shl      eax, 4
004270e4  01d0                     add      eax, edx
004270e6  c1e002                   shl      eax, 2
004270e9  01d0                     add      eax, edx
004270eb  bac8a04900               mov      edx, 0x49a0c8
004270f0  c1e002                   shl      eax, 2
004270f3  01c2                     add      edx, eax
004270f5  31db                     xor      ebx, ebx
004270f7  8a4208                   mov      al, byte ptr [edx + 8]
004270fa  88c3                     mov      bl, al
004270fc  89d8                     mov      eax, ebx
004270fe  c1e002                   shl      eax, 2
00427101  29d8                     sub      eax, ebx
00427103  c1e002                   shl      eax, 2
00427106  01c3                     add      ebx, eax
00427108  c1e302                   shl      ebx, 2
0042710b  668b838c5d4900           mov      ax, word ptr [ebx + 0x495d8c]
00427112  8945e8                   mov      dword ptr [ebp - 0x18], eax
00427115  668b838e5d4900           mov      ax, word ptr [ebx + 0x495d8e]
0042711c  8945dc                   mov      dword ptr [ebp - 0x24], eax
0042711f  8b45e8                   mov      eax, dword ptr [ebp - 0x18]
00427122  8b5ddc                   mov      ebx, dword ptr [ebp - 0x24]
00427125  66d1e8                   shr      ax, 1
00427128  66d1eb                   shr      bx, 1
0042712b  8945e8                   mov      dword ptr [ebp - 0x18], eax
0042712e  895ddc                   mov      dword ptr [ebp - 0x24], ebx
00427131  89d8                     mov      eax, ebx
00427133  8b5de8                   mov      ebx, dword ptr [ebp - 0x18]
00427136  c1e008                   shl      eax, 8
00427139  01d8                     add      eax, ebx
0042713b  66034202                 add      ax, word ptr [edx + 2]
0042713f  31d2                     xor      edx, edx
00427141  6689c2                   mov      dx, ax
00427144  bb00010000               mov      ebx, 0x100
00427149  89d0                     mov      eax, edx
0042714b  c1fa1f                   sar      edx, 0x1f
0042714e  f7fb                     idiv     ebx
00427150  31db                     xor      ebx, ebx
00427152  31c0                     xor      eax, eax
00427154  668b5e02                 mov      bx, word ptr [esi + 2]
00427158  6689d0                   mov      ax, dx
0042715b  81eb00010000             sub      ebx, 0x100
00427161  8945d0                   mov      dword ptr [ebp - 0x30], eax
00427164  89da                     mov      edx, ebx
00427166  89d8                     mov      eax, ebx
00427168  c1fa1f                   sar      edx, 0x1f
0042716b  c1e208                   shl      edx, 8
0042716e  1bc2                     sbb      eax, edx
00427170  c1f808                   sar      eax, 8
00427173  6a20                     push     0x20
00427175  25ffff0000               and      eax, 0xffff
0042717a  89da                     mov      edx, ebx
0042717c  8945cc                   mov      dword ptr [ebp - 0x34], eax
0042717f  b800010000               mov      eax, 0x100
00427184  c1fa1f                   sar      edx, 0x1f
00427187  8945d4                   mov      dword ptr [ebp - 0x2c], eax
0042718a  89d8                     mov      eax, ebx
0042718c  f77dd4                   idiv     dword ptr [ebp - 0x2c]
0042718f  31c0                     xor      eax, eax
00427191  8b5dd0                   mov      ebx, dword ptr [ebp - 0x30]
00427194  6689d0                   mov      ax, dx
00427197  8b55cc                   mov      edx, dword ptr [ebp - 0x34]
0042719a  e82c250500               call     0x4796cb
0042719f  88868b000000             mov      byte ptr [esi + 0x8b], al
004271a5  a17c8f5000               mov      eax, dword ptr [0x508f7c]
004271aa  31db                     xor      ebx, ebx
004271ac  31d2                     xor      edx, edx
004271ae  668b1dfc5b4900           mov      bx, word ptr [0x495bfc]
004271b5  f7f3                     div      ebx
004271b7  85d2                     test     edx, edx
004271b9  0f85dd010000             jne      0x42739c
004271bf  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004271c5  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004271cb  0f85cb010000             jne      0x42739c
004271d1  31c0                     xor      eax, eax
004271d3  8a467b                   mov      al, byte ptr [esi + 0x7b]
004271d6  66c746786400             mov      word ptr [esi + 0x78], 0x64
004271dc  83f801                   cmp      eax, 1
004271df  0f85e1000000             jne      0x4272c6
004271e5  807e7400                 cmp      byte ptr [esi + 0x74], 0
004271e9  0f84b9000000             je       0x4272a8
004271ef  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004271f5  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004271fb  0f85a7000000             jne      0x4272a8
00427201  c6467601                 mov      byte ptr [esi + 0x76], 1
00427205  81e7ffff0000             and      edi, 0xffff
0042720b  31c0                     xor      eax, eax
0042720d  57                       push     edi
0042720e  668b8686000000           mov      ax, word ptr [esi + 0x86]
00427215  50                       push     eax
00427216  31c9                     xor      ecx, ecx
00427218  31db                     xor      ebx, ebx
0042721a  e81f9f0100               call     0x44113e
0042721f  6689c1                   mov      cx, ax
00427222  31c0                     xor      eax, eax
00427224  668b5e02                 mov      bx, word ptr [esi + 2]
00427228  8a868a000000             mov      al, byte ptr [esi + 0x8a]
0042722e  8a5608                   mov      dl, byte ptr [esi + 8]
00427231  e8cadeffff               call     0x425100
00427236  31c0                     xor      eax, eax
00427238  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042723f  31d2                     xor      edx, edx
00427241  e8ffad0100               call     0x442045
00427246  88c2                     mov      dl, al
00427248  89f8                     mov      eax, edi
0042724a  e8052bffff               call     0x419d54
0042724f  89f8                     mov      eax, edi
00427251  c1e004                   shl      eax, 4
00427254  01f8                     add      eax, edi
00427256  c1e002                   shl      eax, 2
00427259  01f8                     add      eax, edi
0042725b  bbc8a04900               mov      ebx, 0x49a0c8
00427260  c1e002                   shl      eax, 2
00427263  01c3                     add      ebx, eax
00427265  8a4304                   mov      al, byte ptr [ebx + 4]
00427268  3a0541805000             cmp      al, byte ptr [0x508041]
0042726e  0f8534000000             jne      0x4272a8
00427274  89f8                     mov      eax, edi
00427276  e8302effff               call     0x41a0ab
0042727b  83bb00010000ff           cmp      dword ptr [ebx + 0x100], -1
00427282  0f8520000000             jne      0x4272a8
00427288  50                       push     eax
00427289  31d2                     xor      edx, edx
0042728b  31c9                     xor      ecx, ecx
0042728d  8a5308                   mov      dl, byte ptr [ebx + 8]
00427290  8d8300010000             lea      eax, [ebx + 0x100]
00427296  c1e210                   shl      edx, 0x10
00427299  89c3                     mov      ebx, eax
0042729b  b842000000               mov      eax, 0x42
004272a0  80ce23                   or       dh, 0x23
004272a3  e8d1370600               call     0x48aa79
004272a8  8a467b                   mov      al, byte ptr [esi + 0x7b]
004272ab  3c01                     cmp      al, 1
004272ad  0f82f4010000             jb       0x4274a7
004272b3  0f8631010000             jbe      0x4273ea
004272b9  3c03                     cmp      al, 3
004272bb  0f8457010000             je       0x427418
004272c1  e9e1010000               jmp      0x4274a7
004272c6  83f803                   cmp      eax, 3
004272c9  75dd                     jne      0x4272a8
004272cb  807e7400                 cmp      byte ptr [esi + 0x74], 0
004272cf  74d7                     je       0x4272a8
004272d1  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004272d7  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004272dd  75c9                     jne      0x4272a8
004272df  c6467601                 mov      byte ptr [esi + 0x76], 1
004272e3  81e7ffff0000             and      edi, 0xffff
004272e9  31c0                     xor      eax, eax
004272eb  57                       push     edi
004272ec  668b8686000000           mov      ax, word ptr [esi + 0x86]
004272f3  31c9                     xor      ecx, ecx
004272f5  50                       push     eax
004272f6  31db                     xor      ebx, ebx
004272f8  31d2                     xor      edx, edx
004272fa  e8e33bffff               call     0x41aee2
004272ff  6689c1                   mov      cx, ax
00427302  31c0                     xor      eax, eax
00427304  668b5e02                 mov      bx, word ptr [esi + 2]
00427308  8a868a000000             mov      al, byte ptr [esi + 0x8a]
0042730e  8a5608                   mov      dl, byte ptr [esi + 8]
00427311  e8eaddffff               call     0x425100
00427316  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042731d  31d2                     xor      edx, edx
0042731f  6689c2                   mov      dx, ax
00427322  89d0                     mov      eax, edx
00427324  c1e004                   shl      eax, 4
00427327  01d0                     add      eax, edx
00427329  c1e002                   shl      eax, 2
0042732c  01d0                     add      eax, edx
0042732e  c1e002                   shl      eax, 2
00427331  05c8a04900               add      eax, 0x49a0c8
00427336  31d2                     xor      edx, edx
00427338  8a4004                   mov      al, byte ptr [eax + 4]
0042733b  88c2                     mov      dl, al
0042733d  89f8                     mov      eax, edi
0042733f  e8102affff               call     0x419d54
00427344  89f8                     mov      eax, edi
00427346  c1e004                   shl      eax, 4
00427349  01f8                     add      eax, edi
0042734b  c1e002                   shl      eax, 2
0042734e  01f8                     add      eax, edi
00427350  bac8a04900               mov      edx, 0x49a0c8
00427355  c1e002                   shl      eax, 2
00427358  01c2                     add      edx, eax
0042735a  8a3d41805000             mov      bh, byte ptr [0x508041]
00427360  3a7a04                   cmp      bh, byte ptr [edx + 4]
00427363  0f853fffffff             jne      0x4272a8
00427369  89f8                     mov      eax, edi
0042736b  e83b2dffff               call     0x41a0ab
00427370  83ba00010000ff           cmp      dword ptr [edx + 0x100], -1
00427377  0f852bffffff             jne      0x4272a8
0042737d  8d9a00010000             lea      ebx, [edx + 0x100]
00427383  50                       push     eax
00427384  8a5208                   mov      dl, byte ptr [edx + 8]
00427387  81e2ff000000             and      edx, 0xff
0042738d  b842000000               mov      eax, 0x42
00427392  c1e210                   shl      edx, 0x10
00427395  31c9                     xor      ecx, ecx
00427397  e904ffffff               jmp      0x4272a0
0042739c  31c0                     xor      eax, eax
0042739e  668b4678                 mov      ax, word ptr [esi + 0x78]
004273a2  85c0                     test     eax, eax
004273a4  740e                     je       0x4273b4
004273a6  3dffff0000               cmp      eax, 0xffff
004273ab  7407                     je       0x4273b4
004273ad  89c1                     mov      ecx, eax
004273af  49                       dec      ecx
004273b0  66894e78                 mov      word ptr [esi + 0x78], cx
004273b4  31c0                     xor      eax, eax
004273b6  8a4676                   mov      al, byte ptr [esi + 0x76]
004273b9  83f801                   cmp      eax, 1
004273bc  740e                     je       0x4273cc
004273be  83f802                   cmp      eax, 2
004273c1  7409                     je       0x4273cc
004273c3  83f803                   cmp      eax, 3
004273c6  0f85dcfeffff             jne      0x4272a8
004273cc  bb05000000               mov      ebx, 5
004273d1  a17c8f5000               mov      eax, dword ptr [0x508f7c]
004273d6  31d2                     xor      edx, edx
004273d8  f7f3                     div      ebx
004273da  85d2                     test     edx, edx
004273dc  0f85c6feffff             jne      0x4272a8
004273e2  fe4676                   inc      byte ptr [esi + 0x76]
004273e5  e9befeffff               jmp      0x4272a8
004273ea  31c0                     xor      eax, eax
004273ec  668b8686000000           mov      ax, word ptr [esi + 0x86]
004273f3  e8b5c90100               call     0x443dad
004273f8  84c0                     test     al, al
004273fa  0f85a7000000             jne      0x4274a7
00427400  66c78686000000ffff       mov      word ptr [esi + 0x86], 0xffff
00427409  c6467bff                 mov      byte ptr [esi + 0x7b], 0xff
0042740d  884676                   mov      byte ptr [esi + 0x76], al
00427410  884674                   mov      byte ptr [esi + 0x74], al
00427413  e98f000000               jmp      0x4274a7
00427418  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042741f  31d2                     xor      edx, edx
00427421  6689c2                   mov      dx, ax
00427424  89d0                     mov      eax, edx
00427426  c1e004                   shl      eax, 4
00427429  01d0                     add      eax, edx
0042742b  c1e002                   shl      eax, 2
0042742e  01d0                     add      eax, edx
00427430  c1e002                   shl      eax, 2
00427433  05c8a04900               add      eax, 0x49a0c8
00427438  8a4005                   mov      al, byte ptr [eax + 5]
0042743b  25ff000000               and      eax, 0xff
00427440  0f95c0                   setne    al
00427443  ebb3                     jmp      0x4273f8
00427445  31c0                     xor      eax, eax
00427447  8a4676                   mov      al, byte ptr [esi + 0x76]
0042744a  83f801                   cmp      eax, 1
0042744d  740a                     je       0x427459
0042744f  83f802                   cmp      eax, 2
00427452  7405                     je       0x427459
00427454  83f803                   cmp      eax, 3
00427457  7515                     jne      0x42746e
00427459  bb05000000               mov      ebx, 5
0042745e  a17c8f5000               mov      eax, dword ptr [0x508f7c]
00427463  31d2                     xor      edx, edx
00427465  f7f3                     div      ebx
00427467  85d2                     test     edx, edx
00427469  7503                     jne      0x42746e
0042746b  fe4676                   inc      byte ptr [esi + 0x76]
0042746e  b80b000000               mov      eax, 0xb
00427473  bb64000000               mov      ebx, 0x64
00427478  31d2                     xor      edx, edx
0042747a  e85d900400               call     0x4704dc
0042747f  f7f3                     div      ebx
00427481  85d2                     test     edx, edx
00427483  7522                     jne      0x4274a7
00427485  8a868b000000             mov      al, byte ptr [esi + 0x8b]
0042748b  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
00427491  7514                     jne      0x4274a7
00427493  b80c000000               mov      eax, 0xc
00427498  e83f900400               call     0x4704dc
0042749d  241f                     and      al, 0x1f
0042749f  fec0                     inc      al
004274a1  88868b000000             mov      byte ptr [esi + 0x8b], al
004274a7  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004274ad  8a968a000000             mov      dl, byte ptr [esi + 0x8a]
004274b3  38d0                     cmp      al, dl
004274b5  0f8477000000             je       0x427532
004274bb  f6057c8f500001           test     byte ptr [0x508f7c], 1
004274c2  0f856a000000             jne      0x427532
004274c8  38d0                     cmp      al, dl
004274ca  7613                     jbe      0x4274df
004274cc  31d2                     xor      edx, edx
004274ce  88c2                     mov      dl, al
004274d0  31c0                     xor      eax, eax
004274d2  8a868a000000             mov      al, byte ptr [esi + 0x8a]
004274d8  29c2                     sub      edx, eax
004274da  83fa10                   cmp      edx, 0x10
004274dd  7c1f                     jl       0x4274fe
004274df  8a868a000000             mov      al, byte ptr [esi + 0x8a]
004274e5  8abe8b000000             mov      bh, byte ptr [esi + 0x8b]
004274eb  38f8                     cmp      al, bh
004274ed  7626                     jbe      0x427515
004274ef  31d2                     xor      edx, edx
004274f1  88c2                     mov      dl, al
004274f3  31c0                     xor      eax, eax
004274f5  88f8                     mov      al, bh
004274f7  29c2                     sub      edx, eax
004274f9  83fa10                   cmp      edx, 0x10
004274fc  7e17                     jle      0x427515
004274fe  31d2                     xor      edx, edx
00427500  8a968a000000             mov      dl, byte ptr [esi + 0x8a]
00427506  bb20000000               mov      ebx, 0x20
0042750b  89d0                     mov      eax, edx
0042750d  c1fa1f                   sar      edx, 0x1f
00427510  f7fb                     idiv     ebx
00427512  42                       inc      edx
00427513  eb17                     jmp      0x42752c
00427515  31c0                     xor      eax, eax
00427517  8a868a000000             mov      al, byte ptr [esi + 0x8a]
0042751d  83f801                   cmp      eax, 1
00427520  7405                     je       0x427527
00427522  8d50ff                   lea      edx, [eax - 1]
00427525  eb05                     jmp      0x42752c
00427527  ba20000000               mov      edx, 0x20
0042752c  88968a000000             mov      byte ptr [esi + 0x8a], dl
00427532  31c0                     xor      eax, eax
00427534  8a4676                   mov      al, byte ptr [esi + 0x76]
00427537  83f804                   cmp      eax, 4
0042753a  0f85800c0000             jne      0x4281c0
00427540  c6467600                 mov      byte ptr [esi + 0x76], 0
00427544  e9770c0000               jmp      0x4281c0
; BatimentNextEtape_type11 [0x427549,0x427bb7)
00427549  31d2                     xor      edx, edx
0042754b  6689fa                   mov      dx, di
0042754e  89d0                     mov      eax, edx
00427550  c1e004                   shl      eax, 4
00427553  01d0                     add      eax, edx
00427555  c1e002                   shl      eax, 2
00427558  01d0                     add      eax, edx
0042755a  bbc8a04900               mov      ebx, 0x49a0c8
0042755f  c1e002                   shl      eax, 2
00427562  89f9                     mov      ecx, edi
00427564  01c3                     add      ebx, eax
00427566  89f8                     mov      eax, edi
00427568  25ffff0000               and      eax, 0xffff
0042756d  89c2                     mov      edx, eax
0042756f  c1e004                   shl      eax, 4
00427572  01d0                     add      eax, edx
00427574  c1e002                   shl      eax, 2
00427577  01d0                     add      eax, edx
00427579  bac8a04900               mov      edx, 0x49a0c8
0042757e  c1e002                   shl      eax, 2
00427581  01d0                     add      eax, edx
00427583  8a4008                   mov      al, byte ptr [eax + 8]
00427586  25ff000000               and      eax, 0xff
0042758b  83f815                   cmp      eax, 0x15
0042758e  7510                     jne      0x4275a0
00427590  8d430c                   lea      eax, [ebx + 0xc]
00427593  e8b2fc0100               call     0x44724a
00427598  84c0                     test     al, al
0042759a  744b                     je       0x4275e7
0042759c  b001                     mov      al, 1
0042759e  eb49                     jmp      0x4275e9
004275a0  31d2                     xor      edx, edx
004275a2  6689fa                   mov      dx, di
004275a5  89d0                     mov      eax, edx
004275a7  c1e004                   shl      eax, 4
004275aa  01d0                     add      eax, edx
004275ac  c1e002                   shl      eax, 2
004275af  01d0                     add      eax, edx
004275b1  bac8a04900               mov      edx, 0x49a0c8
004275b6  8a448208                 mov      al, byte ptr [edx + eax*4 + 8]
004275ba  25ff000000               and      eax, 0xff
004275bf  83f802                   cmp      eax, 2
004275c2  750c                     jne      0x4275d0
004275c4  8d430c                   lea      eax, [ebx + 0xc]
004275c7  e87efc0100               call     0x44724a
004275cc  84c0                     test     al, al
004275ce  75cc                     jne      0x42759c
004275d0  8d430c                   lea      eax, [ebx + 0xc]
004275d3  ba01000000               mov      edx, 1
004275d8  bb09000000               mov      ebx, 9
004275dd  e8d6fb0100               call     0x4471b8
004275e2  6685c0                   test     ax, ax
004275e5  ebb3                     jmp      0x42759a
004275e7  30c0                     xor      al, al
004275e9  84c0                     test     al, al
004275eb  0f84cf0b0000             je       0x4281c0
004275f1  31d2                     xor      edx, edx
004275f3  6689fa                   mov      dx, di
004275f6  89d0                     mov      eax, edx
004275f8  e827d0ffff               call     0x424624
004275fd  84c0                     test     al, al
004275ff  0f8595000000             jne      0x42769a
00427605  884676                   mov      byte ptr [esi + 0x76], al
00427608  884674                   mov      byte ptr [esi + 0x74], al
0042760b  89d0                     mov      eax, edx
0042760d  c1e004                   shl      eax, 4
00427610  01d0                     add      eax, edx
00427612  c1e002                   shl      eax, 2
00427615  bbc8a04900               mov      ebx, 0x49a0c8
0042761a  01d0                     add      eax, edx
0042761c  66c746780000             mov      word ptr [esi + 0x78], 0
00427622  c1e002                   shl      eax, 2
00427625  66c78686000000ffff       mov      word ptr [esi + 0x86], 0xffff
0042762e  01c3                     add      ebx, eax
00427630  31c0                     xor      eax, eax
00427632  8b0d7c8f5000             mov      ecx, dword ptr [0x508f7c]
00427638  6689f8                   mov      ax, di
0042763b  01c8                     add      eax, ecx
0042763d  a81f                     test     al, 0x1f
0042763f  7407                     je       0x427648
00427641  b8ffff0000               mov      eax, 0xffff
00427646  eb4b                     jmp      0x427693
00427648  89d0                     mov      eax, edx
0042764a  e86ac9ffff               call     0x423fb9
0042764f  8945d8                   mov      dword ptr [ebp - 0x28], eax
00427652  25ffff0000               and      eax, 0xffff
00427657  3dffff0000               cmp      eax, 0xffff
0042765c  740f                     je       0x42766d
0042765e  66c783880000000000       mov      word ptr [ebx + 0x88], 0
00427667  c6437b01                 mov      byte ptr [ebx + 0x7b], 1
0042766b  eb23                     jmp      0x427690
0042766d  89d0                     mov      eax, edx
0042766f  e8afcaffff               call     0x424123
00427674  8945d8                   mov      dword ptr [ebp - 0x28], eax
00427677  25ffff0000               and      eax, 0xffff
0042767c  3dffff0000               cmp      eax, 0xffff
00427681  740d                     je       0x427690
00427683  66c783880000000000       mov      word ptr [ebx + 0x88], 0
0042768c  c6437b03                 mov      byte ptr [ebx + 0x7b], 3
00427690  8b45d8                   mov      eax, dword ptr [ebp - 0x28]
00427693  66898686000000           mov      word ptr [esi + 0x86], ax
0042769a  31c0                     xor      eax, eax
0042769c  668b8686000000           mov      ax, word ptr [esi + 0x86]
004276a3  3dffff0000               cmp      eax, 0xffff
004276a8  0f8435040000             je       0x427ae3
004276ae  31c0                     xor      eax, eax
004276b0  8a467b                   mov      al, byte ptr [esi + 0x7b]
004276b3  c6467401                 mov      byte ptr [esi + 0x74], 1
004276b7  83f801                   cmp      eax, 1
004276ba  0f858d000000             jne      0x42774d
004276c0  31c0                     xor      eax, eax
004276c2  6a20                     push     0x20
004276c4  668b8686000000           mov      ax, word ptr [esi + 0x86]
004276cb  31d2                     xor      edx, edx
004276cd  e81e970100               call     0x440df0
004276d2  6689c2                   mov      dx, ax
004276d5  89d0                     mov      eax, edx
004276d7  c1fa1f                   sar      edx, 0x1f
004276da  c1e208                   shl      edx, 8
004276dd  1bc2                     sbb      eax, edx
004276df  c1f808                   sar      eax, 8
004276e2  31c9                     xor      ecx, ecx
004276e4  6689c1                   mov      cx, ax
004276e7  31c0                     xor      eax, eax
004276e9  668b8686000000           mov      ax, word ptr [esi + 0x86]
004276f0  31d2                     xor      edx, edx
004276f2  e8f9960100               call     0x440df0
004276f7  6689c2                   mov      dx, ax
004276fa  bb00010000               mov      ebx, 0x100
004276ff  89d0                     mov      eax, edx
00427701  c1fa1f                   sar      edx, 0x1f
00427704  f7fb                     idiv     ebx
00427706  31c0                     xor      eax, eax
00427708  31db                     xor      ebx, ebx
0042770a  6689d0                   mov      ax, dx
0042770d  668b5e02                 mov      bx, word ptr [esi + 2]
00427711  8945d0                   mov      dword ptr [ebp - 0x30], eax
00427714  89da                     mov      edx, ebx
00427716  89d8                     mov      eax, ebx
00427718  c1fa1f                   sar      edx, 0x1f
0042771b  c1e208                   shl      edx, 8
0042771e  1bc2                     sbb      eax, edx
00427720  c1f808                   sar      eax, 8
00427723  25ffff0000               and      eax, 0xffff
00427728  89da                     mov      edx, ebx
0042772a  8945cc                   mov      dword ptr [ebp - 0x34], eax
0042772d  b800010000               mov      eax, 0x100
00427732  c1fa1f                   sar      edx, 0x1f
00427735  8945d4                   mov      dword ptr [ebp - 0x2c], eax
00427738  89d8                     mov      eax, ebx
0042773a  f77dd4                   idiv     dword ptr [ebp - 0x2c]
0042773d  31c0                     xor      eax, eax
0042773f  8b5dd0                   mov      ebx, dword ptr [ebp - 0x30]
00427742  6689d0                   mov      ax, dx
00427745  8b55cc                   mov      edx, dword ptr [ebp - 0x34]
00427748  e946010000               jmp      0x427893
0042774d  83f803                   cmp      eax, 3
00427750  0f8548010000             jne      0x42789e
00427756  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042775d  31d2                     xor      edx, edx
0042775f  6689c2                   mov      dx, ax
00427762  89d0                     mov      eax, edx
00427764  c1e004                   shl      eax, 4
00427767  01d0                     add      eax, edx
00427769  c1e002                   shl      eax, 2
0042776c  01d0                     add      eax, edx
0042776e  bac8a04900               mov      edx, 0x49a0c8
00427773  c1e002                   shl      eax, 2
00427776  01c2                     add      edx, eax
00427778  31db                     xor      ebx, ebx
0042777a  8a4208                   mov      al, byte ptr [edx + 8]
0042777d  88c3                     mov      bl, al
0042777f  89d8                     mov      eax, ebx
00427781  c1e002                   shl      eax, 2
00427784  29d8                     sub      eax, ebx
00427786  c1e002                   shl      eax, 2
00427789  01c3                     add      ebx, eax
0042778b  c1e302                   shl      ebx, 2
0042778e  668b838c5d4900           mov      ax, word ptr [ebx + 0x495d8c]
00427795  8945e0                   mov      dword ptr [ebp - 0x20], eax
00427798  668b838e5d4900           mov      ax, word ptr [ebx + 0x495d8e]
0042779f  8b4de0                   mov      ecx, dword ptr [ebp - 0x20]
004277a2  8945f8                   mov      dword ptr [ebp - 8], eax
004277a5  66d1e8                   shr      ax, 1
004277a8  66d1e9                   shr      cx, 1
004277ab  8945f8                   mov      dword ptr [ebp - 8], eax
004277ae  c1e008                   shl      eax, 8
004277b1  894de0                   mov      dword ptr [ebp - 0x20], ecx
004277b4  01c8                     add      eax, ecx
004277b6  66034202                 add      ax, word ptr [edx + 2]
004277ba  31d2                     xor      edx, edx
004277bc  6689c2                   mov      dx, ax
004277bf  89d0                     mov      eax, edx
004277c1  c1fa1f                   sar      edx, 0x1f
004277c4  c1e208                   shl      edx, 8
004277c7  1bc2                     sbb      eax, edx
004277c9  c1f808                   sar      eax, 8
004277cc  31c9                     xor      ecx, ecx
004277ce  6689c1                   mov      cx, ax
004277d1  31d2                     xor      edx, edx
004277d3  668b8686000000           mov      ax, word ptr [esi + 0x86]
004277da  6689c2                   mov      dx, ax
004277dd  89d0                     mov      eax, edx
004277df  c1e004                   shl      eax, 4
004277e2  01d0                     add      eax, edx
004277e4  c1e002                   shl      eax, 2
004277e7  01d0                     add      eax, edx
004277e9  bac8a04900               mov      edx, 0x49a0c8
004277ee  c1e002                   shl      eax, 2
004277f1  01c2                     add      edx, eax
004277f3  6a20                     push     0x20
004277f5  8a4208                   mov      al, byte ptr [edx + 8]
004277f8  25ff000000               and      eax, 0xff
004277fd  89c3                     mov      ebx, eax
004277ff  c1e002                   shl      eax, 2
00427802  29d8                     sub      eax, ebx
00427804  c1e002                   shl      eax, 2
00427807  01c3                     add      ebx, eax
00427809  c1e302                   shl      ebx, 2
0042780c  668b838c5d4900           mov      ax, word ptr [ebx + 0x495d8c]
00427813  8945e4                   mov      dword ptr [ebp - 0x1c], eax
00427816  668b838e5d4900           mov      ax, word ptr [ebx + 0x495d8e]
0042781d  8945f4                   mov      dword ptr [ebp - 0xc], eax
00427820  8b45e4                   mov      eax, dword ptr [ebp - 0x1c]
00427823  8b5df4                   mov      ebx, dword ptr [ebp - 0xc]
00427826  66d1e8                   shr      ax, 1
00427829  66d1eb                   shr      bx, 1
0042782c  8945e4                   mov      dword ptr [ebp - 0x1c], eax
0042782f  895df4                   mov      dword ptr [ebp - 0xc], ebx
00427832  89d8                     mov      eax, ebx
00427834  8b5de4                   mov      ebx, dword ptr [ebp - 0x1c]
00427837  c1e008                   shl      eax, 8
0042783a  01d8                     add      eax, ebx
0042783c  66034202                 add      ax, word ptr [edx + 2]
00427840  31d2                     xor      edx, edx
00427842  6689c2                   mov      dx, ax
00427845  bb00010000               mov      ebx, 0x100
0042784a  89d0                     mov      eax, edx
0042784c  c1fa1f                   sar      edx, 0x1f
0042784f  f7fb                     idiv     ebx
00427851  31c0                     xor      eax, eax
00427853  31db                     xor      ebx, ebx
00427855  6689d0                   mov      ax, dx
00427858  668b5e02                 mov      bx, word ptr [esi + 2]
0042785c  8945d0                   mov      dword ptr [ebp - 0x30], eax
0042785f  89da                     mov      edx, ebx
00427861  89d8                     mov      eax, ebx
00427863  c1fa1f                   sar      edx, 0x1f
00427866  c1e208                   shl      edx, 8
00427869  1bc2                     sbb      eax, edx
0042786b  c1f808                   sar      eax, 8
0042786e  25ffff0000               and      eax, 0xffff
00427873  89da                     mov      edx, ebx
00427875  8945d4                   mov      dword ptr [ebp - 0x2c], eax
00427878  b800010000               mov      eax, 0x100
0042787d  c1fa1f                   sar      edx, 0x1f
00427880  8945cc                   mov      dword ptr [ebp - 0x34], eax
00427883  89d8                     mov      eax, ebx
00427885  f77dcc                   idiv     dword ptr [ebp - 0x34]
00427888  31c0                     xor      eax, eax
0042788a  8b5dd0                   mov      ebx, dword ptr [ebp - 0x30]
0042788d  6689d0                   mov      ax, dx
00427890  8b55d4                   mov      edx, dword ptr [ebp - 0x2c]
00427893  e8331e0500               call     0x4796cb
00427898  88868b000000             mov      byte ptr [esi + 0x8b], al
0042789e  a17c8f5000               mov      eax, dword ptr [0x508f7c]
004278a3  31db                     xor      ebx, ebx
004278a5  31d2                     xor      edx, edx
004278a7  668b1dfa5b4900           mov      bx, word ptr [0x495bfa]
004278ae  f7f3                     div      ebx
004278b0  85d2                     test     edx, edx
004278b2  0f85ab010000             jne      0x427a63
004278b8  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004278be  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004278c4  0f8599010000             jne      0x427a63
004278ca  31c0                     xor      eax, eax
004278cc  8a467b                   mov      al, byte ptr [esi + 0x7b]
004278cf  66c746786400             mov      word ptr [esi + 0x78], 0x64
004278d5  83f801                   cmp      eax, 1
004278d8  0f85e3000000             jne      0x4279c1
004278de  807e7400                 cmp      byte ptr [esi + 0x74], 0
004278e2  0f84bb000000             je       0x4279a3
004278e8  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004278ee  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004278f4  0f85a9000000             jne      0x4279a3
004278fa  c6467601                 mov      byte ptr [esi + 0x76], 1
004278fe  81e7ffff0000             and      edi, 0xffff
00427904  31c0                     xor      eax, eax
00427906  57                       push     edi
00427907  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042790e  31c9                     xor      ecx, ecx
00427910  50                       push     eax
00427911  31db                     xor      ebx, ebx
00427913  31d2                     xor      edx, edx
00427915  e824980100               call     0x44113e
0042791a  6689c1                   mov      cx, ax
0042791d  31c0                     xor      eax, eax
0042791f  668b5e02                 mov      bx, word ptr [esi + 2]
00427923  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427929  8a5608                   mov      dl, byte ptr [esi + 8]
0042792c  e8cfd7ffff               call     0x425100
00427931  31c0                     xor      eax, eax
00427933  668b8686000000           mov      ax, word ptr [esi + 0x86]
0042793a  31d2                     xor      edx, edx
0042793c  e804a70100               call     0x442045
00427941  88c2                     mov      dl, al
00427943  89f8                     mov      eax, edi
00427945  e80a24ffff               call     0x419d54
0042794a  89f8                     mov      eax, edi
0042794c  c1e004                   shl      eax, 4
0042794f  01f8                     add      eax, edi
00427951  c1e002                   shl      eax, 2
00427954  01f8                     add      eax, edi
00427956  bac8a04900               mov      edx, 0x49a0c8
0042795b  c1e002                   shl      eax, 2
0042795e  01c2                     add      edx, eax
00427960  8a4204                   mov      al, byte ptr [edx + 4]
00427963  3a0541805000             cmp      al, byte ptr [0x508041]
00427969  0f8534000000             jne      0x4279a3
0042796f  89f8                     mov      eax, edi
00427971  e83527ffff               call     0x41a0ab
00427976  83ba00010000ff           cmp      dword ptr [edx + 0x100], -1
0042797d  0f8520000000             jne      0x4279a3
00427983  50                       push     eax
00427984  31c0                     xor      eax, eax
00427986  8a4208                   mov      al, byte ptr [edx + 8]
00427989  c1e010                   shl      eax, 0x10
0042798c  8d9a00010000             lea      ebx, [edx + 0x100]
00427992  80cc23                   or       ah, 0x23
00427995  31c9                     xor      ecx, ecx
00427997  89c2                     mov      edx, eax
00427999  b842000000               mov      eax, 0x42
0042799e  e8d6300600               call     0x48aa79
004279a3  8a467b                   mov      al, byte ptr [esi + 0x7b]
004279a6  3c01                     cmp      al, 1
004279a8  0f826e010000             jb       0x427b1c
004279ae  0f86da000000             jbe      0x427a8e
004279b4  3c03                     cmp      al, 3
004279b6  0f84fa000000             je       0x427ab6
004279bc  e95b010000               jmp      0x427b1c
004279c1  83f803                   cmp      eax, 3
004279c4  75dd                     jne      0x4279a3
004279c6  807e7400                 cmp      byte ptr [esi + 0x74], 0
004279ca  74d7                     je       0x4279a3
004279cc  8a868b000000             mov      al, byte ptr [esi + 0x8b]
004279d2  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
004279d8  75c9                     jne      0x4279a3
004279da  c6467601                 mov      byte ptr [esi + 0x76], 1
004279de  81e7ffff0000             and      edi, 0xffff
004279e4  31c0                     xor      eax, eax
004279e6  57                       push     edi
004279e7  668b8686000000           mov      ax, word ptr [esi + 0x86]
004279ee  31c9                     xor      ecx, ecx
004279f0  50                       push     eax
004279f1  31db                     xor      ebx, ebx
004279f3  31d2                     xor      edx, edx
004279f5  e8e834ffff               call     0x41aee2
004279fa  6689c1                   mov      cx, ax
004279fd  31c0                     xor      eax, eax
004279ff  668b5e02                 mov      bx, word ptr [esi + 2]
00427a03  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427a09  8a5608                   mov      dl, byte ptr [esi + 8]
00427a0c  e8efd6ffff               call     0x425100
00427a11  668b8686000000           mov      ax, word ptr [esi + 0x86]
00427a18  31d2                     xor      edx, edx
00427a1a  6689c2                   mov      dx, ax
00427a1d  89d0                     mov      eax, edx
00427a1f  c1e004                   shl      eax, 4
00427a22  01d0                     add      eax, edx
00427a24  c1e002                   shl      eax, 2
00427a27  01d0                     add      eax, edx
00427a29  c1e002                   shl      eax, 2
00427a2c  05c8a04900               add      eax, 0x49a0c8
00427a31  31d2                     xor      edx, edx
00427a33  8a4004                   mov      al, byte ptr [eax + 4]
00427a36  88c2                     mov      dl, al
00427a38  89f8                     mov      eax, edi
00427a3a  e81523ffff               call     0x419d54
00427a3f  89f8                     mov      eax, edi
00427a41  c1e004                   shl      eax, 4
00427a44  01f8                     add      eax, edi
00427a46  c1e002                   shl      eax, 2
00427a49  01f8                     add      eax, edi
00427a4b  bac8a04900               mov      edx, 0x49a0c8
00427a50  c1e002                   shl      eax, 2
00427a53  01c2                     add      edx, eax
00427a55  8a3d41805000             mov      bh, byte ptr [0x508041]
00427a5b  3a7a04                   cmp      bh, byte ptr [edx + 4]
00427a5e  e906ffffff               jmp      0x427969
00427a63  31c0                     xor      eax, eax
00427a65  668b4678                 mov      ax, word ptr [esi + 0x78]
00427a69  85c0                     test     eax, eax
00427a6b  0f8e32ffffff             jle      0x4279a3
00427a71  3dffff0000               cmp      eax, 0xffff
00427a76  0f8427ffffff             je       0x4279a3
00427a7c  668b4e78                 mov      cx, word ptr [esi + 0x78]
00427a80  c6467600                 mov      byte ptr [esi + 0x76], 0
00427a84  49                       dec      ecx
00427a85  66894e78                 mov      word ptr [esi + 0x78], cx
00427a89  e915ffffff               jmp      0x4279a3
00427a8e  31c0                     xor      eax, eax
00427a90  668b8686000000           mov      ax, word ptr [esi + 0x86]
00427a97  e811c30100               call     0x443dad
00427a9c  84c0                     test     al, al
00427a9e  0f8578000000             jne      0x427b1c
00427aa4  66c78686000000ffff       mov      word ptr [esi + 0x86], 0xffff
00427aad  c6467bff                 mov      byte ptr [esi + 0x7b], 0xff
00427ab1  884674                   mov      byte ptr [esi + 0x74], al
00427ab4  eb66                     jmp      0x427b1c
00427ab6  668b8686000000           mov      ax, word ptr [esi + 0x86]
00427abd  31d2                     xor      edx, edx
00427abf  6689c2                   mov      dx, ax
00427ac2  89d0                     mov      eax, edx
00427ac4  c1e004                   shl      eax, 4
00427ac7  01d0                     add      eax, edx
00427ac9  c1e002                   shl      eax, 2
00427acc  01d0                     add      eax, edx
00427ace  c1e002                   shl      eax, 2
00427ad1  05c8a04900               add      eax, 0x49a0c8
00427ad6  8a4005                   mov      al, byte ptr [eax + 5]
00427ad9  25ff000000               and      eax, 0xff
00427ade  0f95c0                   setne    al
00427ae1  ebb9                     jmp      0x427a9c
00427ae3  b80d000000               mov      eax, 0xd
00427ae8  bb64000000               mov      ebx, 0x64
00427aed  31d2                     xor      edx, edx
00427aef  e8e8890400               call     0x4704dc
00427af4  f7f3                     div      ebx
00427af6  85d2                     test     edx, edx
00427af8  7522                     jne      0x427b1c
00427afa  8a868b000000             mov      al, byte ptr [esi + 0x8b]
00427b00  3a868a000000             cmp      al, byte ptr [esi + 0x8a]
00427b06  7514                     jne      0x427b1c
00427b08  b80e000000               mov      eax, 0xe
00427b0d  e8ca890400               call     0x4704dc
00427b12  241f                     and      al, 0x1f
00427b14  fec0                     inc      al
00427b16  88868b000000             mov      byte ptr [esi + 0x8b], al
00427b1c  8a868b000000             mov      al, byte ptr [esi + 0x8b]
00427b22  8a968a000000             mov      dl, byte ptr [esi + 0x8a]
00427b28  38d0                     cmp      al, dl
00427b2a  0f8490060000             je       0x4281c0
00427b30  f6057c8f500001           test     byte ptr [0x508f7c], 1
00427b37  0f8583060000             jne      0x4281c0
00427b3d  38d0                     cmp      al, dl
00427b3f  7613                     jbe      0x427b54
00427b41  31d2                     xor      edx, edx
00427b43  88c2                     mov      dl, al
00427b45  31c0                     xor      eax, eax
00427b47  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427b4d  29c2                     sub      edx, eax
00427b4f  83fa10                   cmp      edx, 0x10
00427b52  7c23                     jl       0x427b77
00427b54  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427b5a  8abe8b000000             mov      bh, byte ptr [esi + 0x8b]
00427b60  38f8                     cmp      al, bh
00427b62  7633                     jbe      0x427b97
00427b64  31d2                     xor      edx, edx
00427b66  31c0                     xor      eax, eax
00427b68  88fa                     mov      dl, bh
00427b6a  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427b70  29d0                     sub      eax, edx
00427b72  83f810                   cmp      eax, 0x10
00427b75  7e20                     jle      0x427b97
00427b77  31d2                     xor      edx, edx
00427b79  8a968a000000             mov      dl, byte ptr [esi + 0x8a]
00427b7f  bb20000000               mov      ebx, 0x20
00427b84  89d0                     mov      eax, edx
00427b86  c1fa1f                   sar      edx, 0x1f
00427b89  f7fb                     idiv     ebx
00427b8b  42                       inc      edx
00427b8c  88968a000000             mov      byte ptr [esi + 0x8a], dl
00427b92  e929060000               jmp      0x4281c0
00427b97  31c0                     xor      eax, eax
00427b99  8a868a000000             mov      al, byte ptr [esi + 0x8a]
00427b9f  83f801                   cmp      eax, 1
00427ba2  7403                     je       0x427ba7
00427ba4  48                       dec      eax
00427ba5  eb05                     jmp      0x427bac
00427ba7  b820000000               mov      eax, 0x20
00427bac  88868a000000             mov      byte ptr [esi + 0x8a], al
00427bb2  e909060000               jmp      0x4281c0
