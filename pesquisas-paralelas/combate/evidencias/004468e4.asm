; ContactUnite; intervalo [0x004468e4, 0x00446b0c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004468e4  53                       push     ebx
004468e5  51                       push     ecx
004468e6  56                       push     esi
004468e7  57                       push     edi
004468e8  83ec18                   sub      esp, 0x18
004468eb  89d7                     mov      edi, edx
004468ed  31d2                     xor      edx, edx
004468ef  6689c2                   mov      dx, ax
004468f2  89d0                     mov      eax, edx
004468f4  c1e004                   shl      eax, 4
004468f7  01d0                     add      eax, edx
004468f9  c1e002                   shl      eax, 2
004468fc  01d0                     add      eax, edx
004468fe  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00446904  c1e002                   shl      eax, 2
00446907  01d0                     add      eax, edx
00446909  8b9083000000             mov      edx, dword ptr [eax + 0x83]
0044690f  c1fa18                   sar      edx, 0x18
00446912  85d2                     test     edx, edx
00446914  0f8580010000             jne      0x446a9a
0044691a  8b9084000000             mov      edx, dword ptr [eax + 0x84]
00446920  c1fa18                   sar      edx, 0x18
00446923  85d2                     test     edx, edx
00446925  741d                     je       0x446944
00446927  e96e010000               jmp      0x446a9a
0044692c  66c7020100               mov      word ptr [edx], 1
00446931  66c7060100               mov      word ptr [esi], 1
00446936  eb2a                     jmp      0x446962
00446938  66c7020200               mov      word ptr [edx], 2
0044693d  66c7060200               mov      word ptr [esi], 2
00446942  eb1e                     jmp      0x446962
00446944  8d54240c                 lea      edx, [esp + 0xc]
00446948  668b4808                 mov      cx, word ptr [eax + 8]
0044694c  8a4001                   mov      al, byte ptr [eax + 1]
0044694f  89e6                     mov      esi, esp
00446951  3c19                     cmp      al, 0x19
00446953  770d                     ja       0x446962
00446955  25ff000000               and      eax, 0xff
0044695a  2eff24857c684400         jmp      dword ptr cs:[eax*4 + 0x44687c]
00446962  8b0424                   mov      eax, dword ptr [esp]
00446965  48                       dec      eax
00446966  8b54240c                 mov      edx, dword ptr [esp + 0xc]
0044696a  c1e008                   shl      eax, 8
0044696d  01d0                     add      eax, edx
0044696f  48                       dec      eax
00446970  31db                     xor      ebx, ebx
00446972  29c1                     sub      ecx, eax
00446974  6689cb                   mov      bx, cx
00446977  be00010000               mov      esi, 0x100
0044697c  89da                     mov      edx, ebx
0044697e  89d8                     mov      eax, ebx
00446980  c1fa1f                   sar      edx, 0x1f
00446983  f7fe                     idiv     esi
00446985  89d6                     mov      esi, edx
00446987  89da                     mov      edx, ebx
00446989  89d8                     mov      eax, ebx
0044698b  c1fa1f                   sar      edx, 0x1f
0044698e  c1e208                   shl      edx, 8
00446991  1bc2                     sbb      eax, edx
00446993  c1f808                   sar      eax, 8
00446996  89c2                     mov      edx, eax
00446998  31c0                     xor      eax, eax
0044699a  6689f0                   mov      ax, si
0044699d  85c0                     test     eax, eax
0044699f  7403                     je       0x4469a4
004469a1  49                       dec      ecx
004469a2  eb04                     jmp      0x4469a8
004469a4  ff4c240c                 dec      dword ptr [esp + 0xc]
004469a8  31c0                     xor      eax, eax
004469aa  6689d0                   mov      ax, dx
004469ad  85c0                     test     eax, eax
004469af  7408                     je       0x4469b9
004469b1  81e900010000             sub      ecx, 0x100
004469b7  eb03                     jmp      0x4469bc
004469b9  ff0c24                   dec      dword ptr [esp]
004469bc  31db                     xor      ebx, ebx
004469be  6689cb                   mov      bx, cx
004469c1  be00010000               mov      esi, 0x100
004469c6  89da                     mov      edx, ebx
004469c8  89d8                     mov      eax, ebx
004469ca  c1fa1f                   sar      edx, 0x1f
004469cd  f7fe                     idiv     esi
004469cf  89542404                 mov      dword ptr [esp + 4], edx
004469d3  89da                     mov      edx, ebx
004469d5  89d8                     mov      eax, ebx
004469d7  c1fa1f                   sar      edx, 0x1f
004469da  f7fe                     idiv     esi
004469dc  31d2                     xor      edx, edx
004469de  6689fa                   mov      dx, di
004469e1  89442410                 mov      dword ptr [esp + 0x10], eax
004469e5  89d0                     mov      eax, edx
004469e7  c1e004                   shl      eax, 4
004469ea  01d0                     add      eax, edx
004469ec  c1e002                   shl      eax, 2
004469ef  01d0                     add      eax, edx
004469f1  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004469f7  8a8482ab000000           mov      al, byte ptr [edx + eax*4 + 0xab]
004469fe  25ff000000               and      eax, 0xff
00446a03  0f95c0                   setne    al
00446a06  fec0                     inc      al
00446a08  88442414                 mov      byte ptr [esp + 0x14], al
00446a0c  31c0                     xor      eax, eax
00446a0e  89442408                 mov      dword ptr [esp + 8], eax
00446a12  eb19                     jmp      0x446a2d
00446a14  b800010000               mov      eax, 0x100
00446a19  8b54240c                 mov      edx, dword ptr [esp + 0xc]
00446a1d  8b5c2408                 mov      ebx, dword ptr [esp + 8]
00446a21  29d0                     sub      eax, edx
00446a23  43                       inc      ebx
00446a24  83e802                   sub      eax, 2
00446a27  895c2408                 mov      dword ptr [esp + 8], ebx
00446a2b  01c1                     add      ecx, eax
00446a2d  31d2                     xor      edx, edx
00446a2f  31c0                     xor      eax, eax
00446a31  668b1424                 mov      dx, word ptr [esp]
00446a35  668b442408               mov      ax, word ptr [esp + 8]
00446a3a  83c202                   add      edx, 2
00446a3d  39d0                     cmp      eax, edx
00446a3f  7d59                     jge      0x446a9a
00446a41  31d2                     xor      edx, edx
00446a43  668b542410               mov      dx, word ptr [esp + 0x10]
00446a48  01d0                     add      eax, edx
00446a4a  3d00010000               cmp      eax, 0x100
00446a4f  7dc3                     jge      0x446a14
00446a51  31f6                     xor      esi, esi
00446a53  eb02                     jmp      0x446a57
00446a55  41                       inc      ecx
00446a56  46                       inc      esi
00446a57  31d2                     xor      edx, edx
00446a59  31c0                     xor      eax, eax
00446a5b  668b54240c               mov      dx, word ptr [esp + 0xc]
00446a60  6689f0                   mov      ax, si
00446a63  83c202                   add      edx, 2
00446a66  39d0                     cmp      eax, edx
00446a68  7daa                     jge      0x446a14
00446a6a  31d2                     xor      edx, edx
00446a6c  668b542404               mov      dx, word ptr [esp + 4]
00446a71  01d0                     add      eax, edx
00446a73  3d00010000               cmp      eax, 0x100
00446a78  7ddb                     jge      0x446a55
00446a7a  31db                     xor      ebx, ebx
00446a7c  31d2                     xor      edx, edx
00446a7e  31c0                     xor      eax, eax
00446a80  8a5c2414                 mov      bl, byte ptr [esp + 0x14]
00446a84  6689ca                   mov      dx, cx
00446a87  6689f8                   mov      ax, di
00446a8a  e8dfb9ffff               call     0x44246e
00446a8f  84c0                     test     al, al
00446a91  74c2                     je       0x446a55
00446a93  b001                     mov      al, 1
00446a95  e9cec9ffff               jmp      0x443468
00446a9a  30c0                     xor      al, al
00446a9c  e9c7c9ffff               jmp      0x443468
00446aa1  8d4000                   lea      eax, [eax]
00446aa4  546b4400                 dd       0x00446b54 ; tabela de saltos
00446aa8  546b4400                 dd       0x00446b54 ; tabela de saltos
00446aac  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ab0  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ab4  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ab8  546b4400                 dd       0x00446b54 ; tabela de saltos
00446abc  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ac0  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ac4  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ac8  546b4400                 dd       0x00446b54 ; tabela de saltos
00446acc  546b4400                 dd       0x00446b54 ; tabela de saltos
00446ad0  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ad4  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ad8  606b4400                 dd       0x00446b60 ; tabela de saltos
00446adc  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ae0  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ae4  606b4400                 dd       0x00446b60 ; tabela de saltos
00446ae8  546b4400                 dd       0x00446b54 ; tabela de saltos
00446aec  546b4400                 dd       0x00446b54 ; tabela de saltos
00446af0  546b4400                 dd       0x00446b54 ; tabela de saltos
00446af4  546b4400                 dd       0x00446b54 ; tabela de saltos
00446af8  546b4400                 dd       0x00446b54 ; tabela de saltos
00446afc  546b4400                 dd       0x00446b54 ; tabela de saltos
00446b00  546b4400                 dd       0x00446b54 ; tabela de saltos
00446b04  546b4400                 dd       0x00446b54 ; tabela de saltos
00446b08  606b4400                 dd       0x00446b60 ; tabela de saltos
