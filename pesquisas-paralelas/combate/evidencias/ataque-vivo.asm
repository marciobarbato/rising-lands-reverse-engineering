; Stage 18 attack branch and declared fragments; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; EnginNextEtape_ramo_ataque [0x45673b,0x4568ad)
0045673b  31c0                     xor      eax, eax
0045673d  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
00456744  3dffff0000               cmp      eax, 0xffff
00456749  7427                     je       0x456772
0045674b  e8bb3ffcff               call     0x41a70b
00456750  84c0                     test     al, al
00456752  751e                     jne      0x456772
00456754  31c0                     xor      eax, eax
00456756  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045675d  e82a39fcff               call     0x41a08c
00456762  25ff000000               and      eax, 0xff
00456767  3dc8000000               cmp      eax, 0xc8
0045676c  0f852c010000             jne      0x45689e
00456772  31c9                     xor      ecx, ecx
00456774  6689f9                   mov      cx, di
00456777  89c8                     mov      eax, ecx
00456779  c1e004                   shl      eax, 4
0045677c  01c8                     add      eax, ecx
0045677e  c1e002                   shl      eax, 2
00456781  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00456787  01c8                     add      eax, ecx
00456789  8a0482                   mov      al, byte ptr [edx + eax*4]
0045678c  25ff000000               and      eax, 0xff
00456791  e881700100               call     0x46d817
00456796  25ff000000               and      eax, 0xff
0045679b  83f802                   cmp      eax, 2
0045679e  7513                     jne      0x4567b3
004567a0  ba4a000000               mov      edx, 0x4a
004567a5  89c8                     mov      eax, ecx
004567a7  31db                     xor      ebx, ebx
004567a9  e81ac20200               call     0x4829c8
004567ae  e91ae5ffff               jmp      0x454ccd
004567b3  31d2                     xor      edx, edx
004567b5  89c8                     mov      eax, ecx
004567b7  668b567e                 mov      dx, word ptr [esi + 0x7e]
004567bb  e813f0feff               call     0x4457d3
004567c0  66c786b8000000ffff       mov      word ptr [esi + 0xb8], 0xffff
004567c9  e9ffe4ffff               jmp      0x454ccd
004567ce  31c0                     xor      eax, eax
004567d0  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
004567d7  3dffff0000               cmp      eax, 0xffff
004567dc  0f846d000000             je       0x45684f
004567e2  31d2                     xor      edx, edx
004567e4  6689c2                   mov      dx, ax
004567e7  89d0                     mov      eax, edx
004567e9  c1e004                   shl      eax, 4
004567ec  01d0                     add      eax, edx
004567ee  c1e002                   shl      eax, 2
004567f1  01d0                     add      eax, edx
004567f3  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004567f9  c1e002                   shl      eax, 2
004567fc  01c2                     add      edx, eax
004567fe  31c0                     xor      eax, eax
00456800  8a4202                   mov      al, byte ptr [edx + 2]
00456803  85c0                     test     eax, eax
00456805  7409                     je       0x456810
00456807  83f804                   cmp      eax, 4
0045680a  7404                     je       0x456810
0045680c  b001                     mov      al, 1
0045680e  eb02                     jmp      0x456812
00456810  30c0                     xor      al, al
00456812  84c0                     test     al, al
00456814  7439                     je       0x45684f
00456816  668b86b8000000           mov      ax, word ptr [esi + 0xb8]
0045681d  31d2                     xor      edx, edx
0045681f  6689c2                   mov      dx, ax
00456822  89d0                     mov      eax, edx
00456824  c1e004                   shl      eax, 4
00456827  01d0                     add      eax, edx
00456829  c1e002                   shl      eax, 2
0045682c  01c2                     add      edx, eax
0045682e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00456833  c1e202                   shl      edx, 2
00456836  01d0                     add      eax, edx
00456838  8a10                     mov      dl, byte ptr [eax]
0045683a  81e2ff000000             and      edx, 0xff
00456840  81fac8000000             cmp      edx, 0xc8
00456846  7407                     je       0x45684f
00456848  8a4072                   mov      al, byte ptr [eax + 0x72]
0045684b  84c0                     test     al, al
0045684d  754f                     jne      0x45689e
0045684f  31c9                     xor      ecx, ecx
00456851  6689f9                   mov      cx, di
00456854  89c8                     mov      eax, ecx
00456856  c1e004                   shl      eax, 4
00456859  01c8                     add      eax, ecx
0045685b  c1e002                   shl      eax, 2
0045685e  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00456864  01c8                     add      eax, ecx
00456866  8a0482                   mov      al, byte ptr [edx + eax*4]
00456869  25ff000000               and      eax, 0xff
0045686e  e8a46f0100               call     0x46d817
00456873  25ff000000               and      eax, 0xff
00456878  83f802                   cmp      eax, 2
0045687b  0f841fffffff             je       0x4567a0
00456881  e92dffffff               jmp      0x4567b3
00456886  8a86b7000000             mov      al, byte ptr [esi + 0xb7]
0045688c  3c01                     cmp      al, 1
0045688e  720e                     jb       0x45689e
00456890  0f8638ffffff             jbe      0x4567ce
00456896  3c03                     cmp      al, 3
00456898  0f849dfeffff             je       0x45673b
0045689e  31c0                     xor      eax, eax
004568a0  6689f8                   mov      ax, di
004568a3  e86cb0ffff               call     0x451914
004568a8  e920e4ffff               jmp      0x454ccd
; EnginNextEtape_saida [0x454ccd,0x454cd5)
00454ccd  83c464                   add      esp, 0x64
00454cd0  e9c8a5ffff               jmp      0x44f29d
; EnginNextEtape_prelude_recarga [0x45442c,0x454591)
0045442c  53                       push     ebx
0045442d  51                       push     ecx
0045442e  52                       push     edx
0045442f  56                       push     esi
00454430  57                       push     edi
00454431  55                       push     ebp
00454432  83ec64                   sub      esp, 0x64
00454435  89c7                     mov      edi, eax
00454437  31db                     xor      ebx, ebx
00454439  6689c3                   mov      bx, ax
0045443c  89d8                     mov      eax, ebx
0045443e  c1e004                   shl      eax, 4
00454441  01d8                     add      eax, ebx
00454443  c1e002                   shl      eax, 2
00454446  01d8                     add      eax, ebx
00454448  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
0045444e  c1e002                   shl      eax, 2
00454451  01c6                     add      esi, eax
00454453  31c0                     xor      eax, eax
00454455  8a4602                   mov      al, byte ptr [esi + 2]
00454458  85c0                     test     eax, eax
0045445a  0f95c0                   setne    al
0045445d  84c0                     test     al, al
0045445f  7437                     je       0x454498
00454461  8a06                     mov      al, byte ptr [esi]
00454463  88442458                 mov      byte ptr [esp + 0x58], al
00454467  8a4601                   mov      al, byte ptr [esi + 1]
0045446a  8b9604010000             mov      edx, dword ptr [esi + 0x104]
00454470  88442460                 mov      byte ptr [esp + 0x60], al
00454474  83faff                   cmp      edx, -1
00454477  7418                     je       0x454491
00454479  89d8                     mov      eax, ebx
0045447b  e8ddc7feff               call     0x440c5d
00454480  8d9e04010000             lea      ebx, [esi + 0x104]
00454486  89c2                     mov      edx, eax
00454488  89d8                     mov      eax, ebx
0045448a  e840660300               call     0x48aacf
0045448f  eb07                     jmp      0x454498
00454491  c686f900000000           mov      byte ptr [esi + 0xf9], 0
00454498  31d2                     xor      edx, edx
0045449a  6689fa                   mov      dx, di
0045449d  89d0                     mov      eax, edx
0045449f  c1e004                   shl      eax, 4
004544a2  01d0                     add      eax, edx
004544a4  c1e002                   shl      eax, 2
004544a7  01d0                     add      eax, edx
004544a9  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004544af  8a448202                 mov      al, byte ptr [edx + eax*4 + 2]
004544b3  25ff000000               and      eax, 0xff
004544b8  7409                     je       0x4544c3
004544ba  83f804                   cmp      eax, 4
004544bd  7404                     je       0x4544c3
004544bf  b001                     mov      al, 1
004544c1  eb02                     jmp      0x4544c5
004544c3  30c0                     xor      al, al
004544c5  84c0                     test     al, al
004544c7  0f844f270000             je       0x456c1c
004544cd  31c0                     xor      eax, eax
004544cf  8a4601                   mov      al, byte ptr [esi + 1]
004544d2  83f810                   cmp      eax, 0x10
004544d5  7559                     jne      0x454530
004544d7  31d2                     xor      edx, edx
004544d9  6689fa                   mov      dx, di
004544dc  89d0                     mov      eax, edx
004544de  c1e004                   shl      eax, 4
004544e1  01d0                     add      eax, edx
004544e3  c1e002                   shl      eax, 2
004544e6  01d0                     add      eax, edx
004544e8  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
004544ee  c1e002                   shl      eax, 2
004544f1  01c3                     add      ebx, eax
004544f3  8aa3a9000000             mov      ah, byte ptr [ebx + 0xa9]
004544f9  fec4                     inc      ah
004544fb  8a93a7000000             mov      dl, byte ptr [ebx + 0xa7]
00454501  88a3a9000000             mov      byte ptr [ebx + 0xa9], ah
00454507  38d4                     cmp      ah, dl
00454509  7525                     jne      0x454530
0045450b  31d2                     xor      edx, edx
0045450d  8a93a4000000             mov      dl, byte ptr [ebx + 0xa4]
00454513  31c9                     xor      ecx, ecx
00454515  42                       inc      edx
00454516  8a8ba5000000             mov      cl, byte ptr [ebx + 0xa5]
0045451c  89d0                     mov      eax, edx
0045451e  c1fa1f                   sar      edx, 0x1f
00454521  f7f9                     idiv     ecx
00454523  c683a900000000           mov      byte ptr [ebx + 0xa9], 0
0045452a  8893a4000000             mov      byte ptr [ebx + 0xa4], dl
00454530  31d2                     xor      edx, edx
00454532  6689fa                   mov      dx, di
00454535  89d0                     mov      eax, edx
00454537  c1e004                   shl      eax, 4
0045453a  01d0                     add      eax, edx
0045453c  c1e002                   shl      eax, 2
0045453f  01d0                     add      eax, edx
00454541  8b0da0194e00             mov      ecx, dword ptr [0x4e19a0]
00454547  c1e002                   shl      eax, 2
0045454a  01c1                     add      ecx, eax
0045454c  31db                     xor      ebx, ebx
0045454e  8a5901                   mov      bl, byte ptr [ecx + 1]
00454551  89d8                     mov      eax, ebx
00454553  c1e002                   shl      eax, 2
00454556  29d8                     sub      eax, ebx
00454558  c1e003                   shl      eax, 3
0045455b  01d8                     add      eax, ebx
0045455d  0fb72c45de654900         movzx    ebp, word ptr [eax*2 + 0x4965de]
00454565  31c0                     xor      eax, eax
00454567  ba03000000               mov      edx, 3
0045456c  8a01                     mov      al, byte ptr [ecx]
0045456e  e84d47fdff               call     0x428cc0
00454573  25ffff0000               and      eax, 0xffff
00454578  29c5                     sub      ebp, eax
0045457a  31c0                     xor      eax, eax
0045457c  668b8102010000           mov      ax, word ptr [ecx + 0x102]
00454583  39e8                     cmp      eax, ebp
00454585  7d0a                     jge      0x454591
00454587  89c2                     mov      edx, eax
00454589  42                       inc      edx
0045458a  66899102010000           mov      word ptr [ecx + 0x102], dx
; SetAttaqueEngin [0x445a36,0x445af1)
00445a36  51                       push     ecx
00445a37  56                       push     esi
00445a38  89c6                     mov      esi, eax
00445a3a  88d1                     mov      cl, dl
00445a3c  31c0                     xor      eax, eax
00445a3e  6689f0                   mov      ax, si
00445a41  89c2                     mov      edx, eax
00445a43  c1e204                   shl      edx, 4
00445a46  01c2                     add      edx, eax
00445a48  c1e202                   shl      edx, 2
00445a4b  01c2                     add      edx, eax
00445a4d  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00445a52  c1e202                   shl      edx, 2
00445a55  01c2                     add      edx, eax
00445a57  31c0                     xor      eax, eax
00445a59  8a4202                   mov      al, byte ptr [edx + 2]
00445a5c  83f801                   cmp      eax, 1
00445a5f  7515                     jne      0x445a76
00445a61  3a8ab7000000             cmp      cl, byte ptr [edx + 0xb7]
00445a67  750d                     jne      0x445a76
00445a69  663b9ab8000000           cmp      bx, word ptr [edx + 0xb8]
00445a70  0f8478000000             je       0x445aee
00445a76  31c0                     xor      eax, eax
00445a78  6689f0                   mov      ax, si
00445a7b  e8fcdaffff               call     0x44357c
00445a80  31c0                     xor      eax, eax
00445a82  8a4201                   mov      al, byte ptr [edx + 1]
00445a85  83f807                   cmp      eax, 7
00445a88  0f8460000000             je       0x445aee
00445a8e  83f806                   cmp      eax, 6
00445a91  0f8457000000             je       0x445aee
00445a97  83f805                   cmp      eax, 5
00445a9a  7452                     je       0x445aee
00445a9c  83f80d                   cmp      eax, 0xd
00445a9f  744d                     je       0x445aee
00445aa1  83f809                   cmp      eax, 9
00445aa4  7448                     je       0x445aee
00445aa6  83f80a                   cmp      eax, 0xa
00445aa9  752f                     jne      0x445ada
00445aab  5e                       pop      esi
00445aac  59                       pop      ecx
00445aad  c3                       ret      
00445aae  6639de                   cmp      si, bx
00445ab1  743b                     je       0x445aee
00445ab3  c6828a00000000           mov      byte ptr [edx + 0x8a], 0
00445aba  884a02                   mov      byte ptr [edx + 2], cl
00445abd  888ab7000000             mov      byte ptr [edx + 0xb7], cl
00445ac3  66899ab8000000           mov      word ptr [edx + 0xb8], bx
00445aca  5e                       pop      esi
00445acb  59                       pop      ecx
00445acc  c3                       ret      
00445acd  c6420201                 mov      byte ptr [edx + 2], 1
00445ad1  c6828a00000000           mov      byte ptr [edx + 0x8a], 0
00445ad8  ebe3                     jmp      0x445abd
00445ada  80f903                   cmp      cl, 3
00445add  720a                     jb       0x445ae9
00445adf  76ec                     jbe      0x445acd
00445ae1  80f905                   cmp      cl, 5
00445ae4  74e7                     je       0x445acd
00445ae6  5e                       pop      esi
00445ae7  59                       pop      ecx
00445ae8  c3                       ret      
00445ae9  80f901                   cmp      cl, 1
00445aec  74c0                     je       0x445aae
00445aee  5e                       pop      esi
00445aef  59                       pop      ecx
00445af0  c3                       ret      
; PlayerGetType [0x46d817,0x46d838)
0046d817  52                       push     edx
0046d818  31d2                     xor      edx, edx
0046d81a  88c2                     mov      dl, al
0046d81c  83fa04                   cmp      edx, 4
0046d81f  7d13                     jge      0x46d834
0046d821  89d0                     mov      eax, edx
0046d823  c1e002                   shl      eax, 2
0046d826  01d0                     add      eax, edx
0046d828  8b15a8805000             mov      edx, dword ptr [0x5080a8]
0046d82e  8a448201                 mov      al, byte ptr [edx + eax*4 + 1]
0046d832  5a                       pop      edx
0046d833  c3                       ret      
0046d834  b002                     mov      al, 2
0046d836  5a                       pop      edx
0046d837  c3                       ret      
; PlayerEstAllie [0x46d838,0x46d877)
0046d838  51                       push     ecx
0046d839  38d0                     cmp      al, dl
0046d83b  7436                     je       0x46d873
0046d83d  25ff000000               and      eax, 0xff
0046d842  83f804                   cmp      eax, 4
0046d845  7f09                     jg       0x46d850
0046d847  31c9                     xor      ecx, ecx
0046d849  88d1                     mov      cl, dl
0046d84b  83f904                   cmp      ecx, 4
0046d84e  7e04                     jle      0x46d854
0046d850  30c0                     xor      al, al
0046d852  59                       pop      ecx
0046d853  c3                       ret      
0046d854  b201                     mov      dl, 1
0046d856  d2e2                     shl      dl, cl
0046d858  89c1                     mov      ecx, eax
0046d85a  c1e002                   shl      eax, 2
0046d85d  01c8                     add      eax, ecx
0046d85f  8b0da8805000             mov      ecx, dword ptr [0x5080a8]
0046d865  8b4c8103                 mov      ecx, dword ptr [ecx + eax*4 + 3]
0046d869  c1f918                   sar      ecx, 0x18
0046d86c  0fbec2                   movsx    eax, dl
0046d86f  85c1                     test     ecx, eax
0046d871  74dd                     je       0x46d850
0046d873  b001                     mov      al, 1
0046d875  59                       pop      ecx
0046d876  c3                       ret      
; PlayerAAttaqueSet [0x46d600,0x46d629)
0046d600  53                       push     ebx
0046d601  25ff000000               and      eax, 0xff
0046d606  83f804                   cmp      eax, 4
0046d609  7d1c                     jge      0x46d627
0046d60b  31db                     xor      ebx, ebx
0046d60d  88d3                     mov      bl, dl
0046d60f  83fb04                   cmp      ebx, 4
0046d612  7d13                     jge      0x46d627
0046d614  89c2                     mov      edx, eax
0046d616  c1e002                   shl      eax, 2
0046d619  01c2                     add      edx, eax
0046d61b  c1e202                   shl      edx, 2
0046d61e  89d8                     mov      eax, ebx
0046d620  ff848244805000           inc      dword ptr [edx + eax*4 + 0x508044]
0046d627  5b                       pop      ebx
0046d628  c3                       ret      
; BatimentEnDestruction [0x41a70b,0x41a735)
0041a70b  52                       push     edx
0041a70c  31d2                     xor      edx, edx
0041a70e  6689c2                   mov      dx, ax
0041a711  89d0                     mov      eax, edx
0041a713  c1e004                   shl      eax, 4
0041a716  01d0                     add      eax, edx
0041a718  c1e002                   shl      eax, 2
0041a71b  01d0                     add      eax, edx
0041a71d  c1e002                   shl      eax, 2
0041a720  05c8a04900               add      eax, 0x49a0c8
0041a725  8a4005                   mov      al, byte ptr [eax + 5]
0041a728  25ff000000               and      eax, 0xff
0041a72d  83f803                   cmp      eax, 3
0041a730  0f94c0                   sete     al
0041a733  5a                       pop      edx
0041a734  c3                       ret      
; BatimentGetPlayer [0x41a08c,0x41a0ab)
0041a08c  52                       push     edx
0041a08d  31d2                     xor      edx, edx
0041a08f  6689c2                   mov      dx, ax
0041a092  89d0                     mov      eax, edx
0041a094  c1e004                   shl      eax, 4
0041a097  01d0                     add      eax, edx
0041a099  c1e002                   shl      eax, 2
0041a09c  01d0                     add      eax, edx
0041a09e  c1e002                   shl      eax, 2
0041a0a1  05c8a04900               add      eax, 0x49a0c8
0041a0a6  8a4004                   mov      al, byte ptr [eax + 4]
0041a0a9  5a                       pop      edx
0041a0aa  c3                       ret      
