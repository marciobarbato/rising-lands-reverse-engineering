; Intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Static evidence only; ranges end exclusively.

; WinMain 00460170..00460277
00460170  53                       push     ebx
00460171  83ec1c                   sub      esp, 0x1c
00460174  6815494900               push     0x494915
00460179  30e4                     xor      ah, ah
0046017b  6822494900               push     0x494922
00460180  8825ec284e00             mov      byte ptr [0x4e28ec], ah
00460186  2eff158c325200           call     dword ptr cs:[0x52328c] ; FindWindowA
0046018d  85c0                     test     eax, eax
0046018f  7407                     je       0x460198
00460191  31c0                     xor      eax, eax
00460193  e9da000000               jmp      0x460272
00460198  8b542428                 mov      edx, dword ptr [esp + 0x28]
0046019c  8b442424                 mov      eax, dword ptr [esp + 0x24]
004601a0  e8c7feffff               call     0x46006c
004601a5  e8c2cd0100               call     0x47cf6c
004601aa  a1e8274e00               mov      eax, dword ptr [0x4e27e8]
004601af  31db                     xor      ebx, ebx
004601b1  e8d27ffbff               call     0x418188
004601b6  e8e4a60200               call     0x48a89f
004601bb  e836790000               call     0x467af6
004601c0  3a1d59a04900             cmp      bl, byte ptr [0x49a059]
004601c6  755f                     jne      0x460227
004601c8  53                       push     ebx
004601c9  53                       push     ebx
004601ca  53                       push     ebx
004601cb  53                       push     ebx
004601cc  8d442410                 lea      eax, [esp + 0x10]
004601d0  50                       push     eax
004601d1  2eff15b8325200           call     dword ptr cs:[0x5232b8] ; PeekMessageA
004601d8  85c0                     test     eax, eax
004601da  7429                     je       0x460205
004601dc  53                       push     ebx
004601dd  53                       push     ebx
004601de  53                       push     ebx
004601df  8d44240c                 lea      eax, [esp + 0xc]
004601e3  50                       push     eax
004601e4  2eff1598325200           call     dword ptr cs:[0x523298] ; GetMessageA
004601eb  85c0                     test     eax, eax
004601ed  7438                     je       0x460227
004601ef  89e0                     mov      eax, esp
004601f1  50                       push     eax
004601f2  2eff15d8325200           call     dword ptr cs:[0x5232d8] ; TranslateMessage
004601f9  89e0                     mov      eax, esp
004601fb  50                       push     eax
004601fc  2eff1584325200           call     dword ptr cs:[0x523284] ; DispatchMessageA
00460203  eb16                     jmp      0x46021b
00460205  3a1d58a04900             cmp      bl, byte ptr [0x49a058]
0046020b  7407                     je       0x460214
0046020d  e8fc4d0100               call     0x47500e
00460212  eb07                     jmp      0x46021b
00460214  2eff15e4325200           call     dword ptr cs:[0x5232e4] ; WaitMessage
0046021b  e8aaa80200               call     0x48aaca
00460220  e8cb790000               call     0x467bf0
00460225  eb99                     jmp      0x4601c0
00460227  e859790000               call     0x467b85
0046022c  e8d3a70200               call     0x48aa04
00460231  a1e8274e00               mov      eax, dword ptr [0x4e27e8]
00460236  e8617ffbff               call     0x41819c
0046023b  8b15e4274e00             mov      edx, dword ptr [0x4e27e4]
00460241  52                       push     edx
00460242  68d8484900               push     0x4948d8
00460247  2eff15dc325200           call     dword ptr cs:[0x5232dc] ; UnregisterClassA
0046024e  31c0                     xor      eax, eax
00460250  a0ec284e00               mov      al, byte ptr [0x4e28ec]
00460255  85c0                     test     eax, eax
00460257  7415                     je       0x46026e
00460259  6a00                     push     0
0046025b  68ec274e00               push     0x4e27ec
00460260  682f494900               push     0x49492f
00460265  6a00                     push     0
00460267  2eff15b0325200           call     dword ptr cs:[0x5232b0] ; MessageBoxA
0046026e  8b442408                 mov      eax, dword ptr [esp + 8]
00460272  83c41c                   add      esp, 0x1c
00460275  5b                       pop      ebx
00460276  c2                       .byte    0xc2

; game_iteration 0047500e..0047509d
0047500e  53                       push     ebx
0047500f  51                       push     ecx
00475010  52                       push     edx
00475011  83ec08                   sub      esp, 8
00475014  ff057c8f5000             inc      dword ptr [0x508f7c]
0047501a  f6057c8f500001           test     byte ptr [0x508f7c], 1
00475021  7506                     jne      0x475029
00475023  ff05808f5000             inc      dword ptr [0x508f80]
00475029  bb03000000               mov      ebx, 3
0047502e  a17c8f5000               mov      eax, dword ptr [0x508f7c]
00475033  31d2                     xor      edx, edx
00475035  f7f3                     div      ebx
00475037  85d2                     test     edx, edx
00475039  7506                     jne      0x475041
0047503b  ff05848f5000             inc      dword ptr [0x508f84]
00475041  89e2                     mov      edx, esp
00475043  52                       push     edx
00475044  2eff1594325200           call     dword ptr cs:[0x523294] ; GetCursorPos
0047504b  8b0424                   mov      eax, dword ptr [esp]
0047504e  66a3a8995000             mov      word ptr [0x5099a8], ax
00475054  8b442404                 mov      eax, dword ptr [esp + 4]
00475058  66a3aa995000             mov      word ptr [0x5099aa], ax
0047505e  e80578fbff               call     0x42c868
00475063  e83026faff               call     0x417698
00475068  803daf99500000           cmp      byte ptr [0x5099af], 0
0047506f  740e                     je       0x47507f
00475071  30f6                     xor      dh, dh
00475073  8835af995000             mov      byte ptr [0x5099af], dh
00475079  8835ae995000             mov      byte ptr [0x5099ae], dh
0047507f  803db299500000           cmp      byte ptr [0x5099b2], 0
00475086  740e                     je       0x475096
00475088  30c9                     xor      cl, cl
0047508a  880db1995000             mov      byte ptr [0x5099b1], cl
00475090  880db2995000             mov      byte ptr [0x5099b2], cl
00475096  83c408                   add      esp, 8
00475099  5a                       pop      edx
0047509a  59                       pop      ecx
0047509b  5b                       pop      ebx
0047509c  c3                       ret      

; CalculFrame 0043f710..0043f7af
0043f710  53                       push     ebx
0043f711  51                       push     ecx
0043f712  52                       push     edx
0043f713  66ff05ae174e00           inc      word ptr [0x4e17ae]
0043f71a  2eff15b8315200           call     dword ptr cs:[0x5231b8] ; GetTickCount
0043f721  8b1db0174e00             mov      ebx, dword ptr [0x4e17b0]
0043f727  89c2                     mov      edx, eax
0043f729  29da                     sub      edx, ebx
0043f72b  a3b4174e00               mov      dword ptr [0x4e17b4], eax
0043f730  81fae8030000             cmp      edx, 0x3e8
0043f736  725d                     jb       0x43f795
0043f738  a3b0174e00               mov      dword ptr [0x4e17b0], eax
0043f73d  31c0                     xor      eax, eax
0043f73f  66a1ae174e00             mov      ax, word ptr [0x4e17ae]
0043f745  83f863                   cmp      eax, 0x63
0043f748  7e09                     jle      0x43f753
0043f74a  66c705ae174e006300       mov      word ptr [0x4e17ae], 0x63
0043f753  31db                     xor      ebx, ebx
0043f755  668b1dae174e00           mov      bx, word ptr [0x4e17ae]
0043f75c  b90a000000               mov      ecx, 0xa
0043f761  89da                     mov      edx, ebx
0043f763  89d8                     mov      eax, ebx
0043f765  c1fa1f                   sar      edx, 0x1f
0043f768  f7f9                     idiv     ecx
0043f76a  83c030                   add      eax, 0x30
0043f76d  89da                     mov      edx, ebx
0043f76f  a294634900               mov      byte ptr [0x496394], al
0043f774  c1fa1f                   sar      edx, 0x1f
0043f777  89d8                     mov      eax, ebx
0043f779  f7f9                     idiv     ecx
0043f77b  83c230                   add      edx, 0x30
0043f77e  30e4                     xor      ah, ah
0043f780  31c9                     xor      ecx, ecx
0043f782  881595634900             mov      byte ptr [0x496395], dl
0043f788  882596634900             mov      byte ptr [0x496396], ah
0043f78e  66890dae174e00           mov      word ptr [0x4e17ae], cx
0043f795  bb0a000000               mov      ebx, 0xa
0043f79a  31c0                     xor      eax, eax
0043f79c  bab4634900               mov      edx, 0x4963b4
0043f7a1  a05ba04900               mov      al, byte ptr [0x49a05b]
0043f7a6  e8e0cb0400               call     0x48c38b
0043f7ab  5a                       pop      edx
0043f7ac  59                       pop      ecx
0043f7ad  5b                       pop      ebx
0043f7ae  c3                       ret      

; draw_divisor 004178f7..0041793c
004178f7  e8147e0200               call     0x43f710
004178fc  e8b5080400               call     0x4581b6
00417901  84c0                     test     al, al
00417903  7404                     je       0x417909
00417905  c645fc01                 mov      byte ptr [ebp - 4], 1
00417909  803da2054e0000           cmp      byte ptr [0x4e05a2], 0
00417910  7519                     jne      0x41792b
00417912  a17c8f5000               mov      eax, dword ptr [0x508f7c]
00417917  31db                     xor      ebx, ebx
00417919  31d2                     xor      edx, edx
0041791b  8a1d84724900             mov      bl, byte ptr [0x497284]
00417921  f7f3                     div      ebx
00417923  85d2                     test     edx, edx
00417925  0f8504060000             jne      0x417f2f
0041792b  803d928f500000           cmp      byte ptr [0x508f92], 0
00417932  0f8491000000             je       0x4179c9
00417938  31c0                     xor      eax, eax
0041793a  66                       .byte    0x66
0041793b  a1                       .byte    0xa1

; DDFlipPage 0043f14f..0043f31c
0043f14f  53                       push     ebx
0043f150  51                       push     ecx
0043f151  52                       push     edx
0043f152  56                       push     esi
0043f153  57                       push     edi
0043f154  55                       push     ebp
0043f155  83ec14                   sub      esp, 0x14
0043f158  88442410                 mov      byte ptr [esp + 0x10], al
0043f15c  31db                     xor      ebx, ebx
0043f15e  8a1d44fb4d00             mov      bl, byte ptr [0x4dfb44]
0043f164  30c0                     xor      al, al
0043f166  85db                     test     ebx, ebx
0043f168  743c                     je       0x43f1a6
0043f16a  8a0d181d4e00             mov      cl, byte ptr [0x4e1d18]
0043f170  31d2                     xor      edx, edx
0043f172  88ca                     mov      dl, cl
0043f174  8a92181c4e00             mov      dl, byte ptr [edx + 0x4e1c18]
0043f17a  81e2ff000000             and      edx, 0xff
0043f180  89d0                     mov      eax, edx
0043f182  c1fa1f                   sar      edx, 0x1f
0043f185  f7fb                     idiv     ebx
0043f187  88d0                     mov      al, dl
0043f189  fec1                     inc      cl
0043f18b  8a257c8f5000             mov      ah, byte ptr [0x508f7c]
0043f191  880d181d4e00             mov      byte ptr [0x4e1d18], cl
0043f197  f6c401                   test     ah, 1
0043f19a  750a                     jne      0x43f1a6
0043f19c  88da                     mov      dl, bl
0043f19e  feca                     dec      dl
0043f1a0  881544fb4d00             mov      byte ptr [0x4dfb44], dl
0043f1a6  31d2                     xor      edx, edx
0043f1a8  668b1518a04900           mov      dx, word ptr [0x49a018]
0043f1af  81fa20030000             cmp      edx, 0x320
0043f1b5  753d                     jne      0x43f1f4
0043f1b7  8b158d8f5000             mov      edx, dword ptr [0x508f8d]
0043f1bd  c1fa18                   sar      edx, 0x18
0043f1c0  c1e205                   shl      edx, 5
0043f1c3  891424                   mov      dword ptr [esp], edx
0043f1c6  25ff000000               and      eax, 0xff
0043f1cb  01c2                     add      edx, eax
0043f1cd  31c0                     xor      eax, eax
0043f1cf  66a126875000             mov      ax, word ptr [0x508726]
0043f1d5  8b1c24                   mov      ebx, dword ptr [esp]
0043f1d8  c1e005                   shl      eax, 5
0043f1db  29d8                     sub      eax, ebx
0043f1dd  8944240c                 mov      dword ptr [esp + 0xc], eax
0043f1e1  31c0                     xor      eax, eax
0043f1e3  66a124875000             mov      ax, word ptr [0x508724]
0043f1e9  c1e005                   shl      eax, 5
0043f1ec  29d8                     sub      eax, ebx
0043f1ee  89542404                 mov      dword ptr [esp + 4], edx
0043f1f2  eb28                     jmp      0x43f21c
0043f1f4  31d2                     xor      edx, edx
0043f1f6  891424                   mov      dword ptr [esp], edx
0043f1f9  25ff000000               and      eax, 0xff
0043f1fe  89442404                 mov      dword ptr [esp + 4], eax
0043f202  31c0                     xor      eax, eax
0043f204  66a126875000             mov      ax, word ptr [0x508726]
0043f20a  c1e005                   shl      eax, 5
0043f20d  8944240c                 mov      dword ptr [esp + 0xc], eax
0043f211  31c0                     xor      eax, eax
0043f213  66a124875000             mov      ax, word ptr [0x508724]
0043f219  c1e005                   shl      eax, 5
0043f21c  89442408                 mov      dword ptr [esp + 8], eax
0043f220  6a10                     push     0x10
0043f222  8d5c2404                 lea      ebx, [esp + 4]
0043f226  53                       push     ebx
0043f227  8b1d8d8f5000             mov      ebx, dword ptr [0x508f8d]
0043f22d  8b3590174e00             mov      esi, dword ptr [0x4e1790]
0043f233  c1fb18                   sar      ebx, 0x18
0043f236  56                       push     esi
0043f237  c1e305                   shl      ebx, 5
0043f23a  53                       push     ebx
0043f23b  a18c174e00               mov      eax, dword ptr [0x4e178c]
0043f240  53                       push     ebx
0043f241  8b10                     mov      edx, dword ptr [eax]
0043f243  50                       push     eax
0043f244  ff521c                   call     dword ptr [edx + 0x1c]
0043f247  89c2                     mov      edx, eax
0043f249  85c0                     test     eax, eax
0043f24b  7420                     je       0x43f26d
0043f24d  3dc2017688               cmp      eax, 0x887601c2
0043f252  7511                     jne      0x43f265
0043f254  a18c174e00               mov      eax, dword ptr [0x4e178c]
0043f259  50                       push     eax
0043f25a  8b10                     mov      edx, dword ptr [eax]
0043f25c  ff526c                   call     dword ptr [edx + 0x6c]
0043f25f  89c2                     mov      edx, eax
0043f261  85c0                     test     eax, eax
0043f263  7508                     jne      0x43f26d
0043f265  81fa1c027688             cmp      edx, 0x8876021c
0043f26b  74b3                     je       0x43f220
0043f26d  807c241000               cmp      byte ptr [esp + 0x10], 0
0043f272  0f849a000000             je       0x43f312
0043f278  31c0                     xor      eax, eax
0043f27a  66a118a04900             mov      ax, word ptr [0x49a018]
0043f280  3d20030000               cmp      eax, 0x320
0043f285  751d                     jne      0x43f2a4
0043f287  b920020000               mov      ecx, 0x220
0043f28c  bf58020000               mov      edi, 0x258
0043f291  31db                     xor      ebx, ebx
0043f293  89442408                 mov      dword ptr [esp + 8], eax
0043f297  891c24                   mov      dword ptr [esp], ebx
0043f29a  894c2404                 mov      dword ptr [esp + 4], ecx
0043f29e  897c240c                 mov      dword ptr [esp + 0xc], edi
0043f2a2  eb20                     jmp      0x43f2c4
0043f2a4  bd20020000               mov      ebp, 0x220
0043f2a9  b880020000               mov      eax, 0x280
0043f2ae  31ff                     xor      edi, edi
0043f2b0  ba58020000               mov      edx, 0x258
0043f2b5  893c24                   mov      dword ptr [esp], edi
0043f2b8  896c2404                 mov      dword ptr [esp + 4], ebp
0043f2bc  89442408                 mov      dword ptr [esp + 8], eax
0043f2c0  8954240c                 mov      dword ptr [esp + 0xc], edx
0043f2c4  6a10                     push     0x10
0043f2c6  8d5c2404                 lea      ebx, [esp + 4]
0043f2ca  53                       push     ebx
0043f2cb  31db                     xor      ebx, ebx
0043f2cd  8b2d90174e00             mov      ebp, dword ptr [0x4e1790]
0043f2d3  668b1d26875000           mov      bx, word ptr [0x508726]
0043f2da  55                       push     ebp
0043f2db  c1e305                   shl      ebx, 5
0043f2de  53                       push     ebx
0043f2df  a18c174e00               mov      eax, dword ptr [0x4e178c]
0043f2e4  6a00                     push     0
0043f2e6  8b10                     mov      edx, dword ptr [eax]
0043f2e8  50                       push     eax
0043f2e9  ff521c                   call     dword ptr [edx + 0x1c]
0043f2ec  89c2                     mov      edx, eax
0043f2ee  85c0                     test     eax, eax
0043f2f0  7420                     je       0x43f312
0043f2f2  3dc2017688               cmp      eax, 0x887601c2
0043f2f7  7511                     jne      0x43f30a
0043f2f9  a18c174e00               mov      eax, dword ptr [0x4e178c]
0043f2fe  50                       push     eax
0043f2ff  8b10                     mov      edx, dword ptr [eax]
0043f301  ff526c                   call     dword ptr [edx + 0x6c]
0043f304  89c2                     mov      edx, eax
0043f306  85c0                     test     eax, eax
0043f308  7508                     jne      0x43f312
0043f30a  81fa1c027688             cmp      edx, 0x8876021c
0043f310  74b2                     je       0x43f2c4
0043f312  83c414                   add      esp, 0x14
0043f315  5d                       pop      ebp
0043f316  5f                       pop      edi
0043f317  5e                       pop      esi
0043f318  5a                       pop      edx
0043f319  59                       pop      ecx
0043f31a  5b                       pop      ebx
0043f31b  c3                       ret      

; GameNextFrame 0045d015..0045d01c
0045d015  ff05406d4900             inc      dword ptr [0x496d40]
0045d01b  c3                       ret      

; OpenFli_timer 0045a692..0045a6b1
0045a692  c78688000000ffffffff     mov      dword ptr [esi + 0x88], 0xffffffff
0045a69c  89868c000000             mov      dword ptr [esi + 0x8c], eax
0045a6a2  e87d930300               call     0x493a24 ; timeGetTime
0045a6a7  6a08                     push     8
0045a6a9  6a00                     push     0
0045a6ab  898690000000             mov      dword ptr [esi + 0x90], eax

; ReadFli_timer 0045aac6..0045aaeb
0045aac6  8b0424                   mov      eax, dword ptr [esp]
0045aac9  ff8088000000             inc      dword ptr [eax + 0x88]
0045aacf  e8508f0300               call     0x493a24 ; timeGetTime
0045aad4  8b1424                   mov      edx, dword ptr [esp]
0045aad7  898290000000             mov      dword ptr [edx + 0x90], eax
0045aadd  8b442410                 mov      eax, dword ptr [esp + 0x10]
0045aae1  83c414                   add      esp, 0x14
0045aae4  5d                       pop      ebp
0045aae5  5f                       pop      edi
0045aae6  5e                       pop      esi
0045aae7  5a                       pop      edx
0045aae8  59                       pop      ecx
0045aae9  5b                       pop      ebx
0045aaea  c3                       ret      

; GetNextNbFrameEllapsedFli 0045abb1..0045abce
0045abb1  53                       push     ebx
0045abb2  51                       push     ecx
0045abb3  52                       push     edx
0045abb4  89c3                     mov      ebx, eax
0045abb6  e8698e0300               call     0x493a24 ; timeGetTime
0045abbb  8b9390000000             mov      edx, dword ptr [ebx + 0x90]
0045abc1  8b4b10                   mov      ecx, dword ptr [ebx + 0x10]
0045abc4  29d0                     sub      eax, edx
0045abc6  31d2                     xor      edx, edx
0045abc8  f7f1                     div      ecx
0045abca  5a                       pop      edx
0045abcb  59                       pop      ecx
0045abcc  5b                       pop      ebx
0045abcd  c3                       ret      

; network_input_timer 0045ea7c..0045eabf
0045ea7c  53                       push     ebx
0045ea7d  51                       push     ecx
0045ea7e  52                       push     edx
0045ea7f  56                       push     esi
0045ea80  57                       push     edi
0045ea81  55                       push     ebp
0045ea82  83ec10                   sub      esp, 0x10
0045ea85  88442408                 mov      byte ptr [esp + 8], al
0045ea89  e822d9fcff               call     0x42c3b0
0045ea8e  84c0                     test     al, al
0045ea90  0f84ff010000             je       0x45ec95
0045ea96  e8894f0300               call     0x493a24 ; timeGetTime
0045ea9b  bd10000000               mov      ebp, 0x10
0045eaa0  30e4                     xor      ah, ah
0045eaa2  89e3                     mov      ebx, esp
0045eaa4  8864240c                 mov      byte ptr [esp + 0xc], ah
0045eaa8  a17c244e00               mov      eax, dword ptr [0x4e247c]
0045eaad  8d542404                 lea      edx, [esp + 4]
0045eab1  89442404                 mov      dword ptr [esp + 4], eax
0045eab5  a168244e00               mov      eax, dword ptr [0x4e2468]
0045eaba  e8cde30000               call     0x46ce8c

; MCICD_deadline 00467a34..00467a4d
00467a34  8d442428                 lea      eax, [esp + 0x28]
00467a38  e8095a0200               call     0x48d446
00467a3d  89c3                     mov      ebx, eax
00467a3f  e8e0bf0200               call     0x493a24 ; timeGetTime
00467a44  01d8                     add      eax, ebx
00467a46  83c450                   add      esp, 0x50
00467a49  5a                       pop      edx
00467a4a  59                       pop      ecx
00467a4b  5b                       pop      ebx
00467a4c  c3                       ret      

; MCICD_Manage_timer 00467bf0..00467c33
00467bf0  53                       push     ebx
00467bf1  51                       push     ecx
00467bf2  52                       push     edx
00467bf3  83ec50                   sub      esp, 0x50
00467bf6  803d292f4e0000           cmp      byte ptr [0x4e2f29], 0
00467bfd  0f8443feffff             je       0x467a46
00467c03  803d282f4e0000           cmp      byte ptr [0x4e2f28], 0
00467c0a  0f8436feffff             je       0x467a46
00467c10  e80fbe0200               call     0x493a24 ; timeGetTime
00467c15  3b05302f4e00             cmp      eax, dword ptr [0x4e2f30]
00467c1b  0f8225feffff             jb       0x467a46
00467c21  803d292f4e0000           cmp      byte ptr [0x4e2f29], 0
00467c28  7426                     je       0x467c50
00467c2a  803d282f4e0000           cmp      byte ptr [0x4e2f28], 0
00467c31  741d                     je       0x467c50

; iaRandom_seed 00489775..004897a4
00489775  7d12                     jge      0x489789
00489777  89c2                     mov      edx, eax
00489779  f7da                     neg      edx
0048977b  bbffffff7f               mov      ebx, 0x7fffffff
00489780  89d0                     mov      eax, edx
00489782  c1fa1f                   sar      edx, 0x1f
00489785  f7fb                     idiv     ebx
00489787  eb0e                     jmp      0x489797
00489789  e896a20000               call     0x493a24 ; timeGetTime
0048978e  bbffffff7f               mov      ebx, 0x7fffffff
00489793  31d2                     xor      edx, edx
00489795  f7f3                     div      ebx
00489797  8915b48d4900             mov      dword ptr [0x498db4], edx
0048979d  31c0                     xor      eax, eax
0048979f  5e                       pop      esi
004897a0  5a                       pop      edx
004897a1  59                       pop      ecx
004897a2  5b                       pop      ebx
004897a3  c3                       ret      

; CRT_semaphore 00490d41..00490d9e
00490d41  53                       push     ebx
00490d42  51                       push     ecx
00490d43  52                       push     edx
00490d44  56                       push     esi
00490d45  55                       push     ebp
00490d46  89c3                     mov      ebx, eax
00490d48  e81d2c0000               call     0x49396a
00490d4d  8b5308                   mov      edx, dword ptr [ebx + 8]
00490d50  89c6                     mov      esi, eax
00490d52  39d0                     cmp      eax, edx
00490d54  743f                     je       0x490d95
00490d56  8b4b04                   mov      ecx, dword ptr [ebx + 4]
00490d59  85c9                     test     ecx, ecx
00490d5b  752b                     jne      0x490d88
00490d5d  b874225200               mov      eax, 0x522274
00490d62  e8daffffff               call     0x490d41
00490d67  837b0400                 cmp      dword ptr [ebx + 4], 0
00490d6b  7511                     jne      0x490d7e
00490d6d  51                       push     ecx
00490d6e  51                       push     ecx
00490d6f  51                       push     ecx
00490d70  e8ef2b0000               call     0x493964
00490d75  c7430401000000           mov      dword ptr [ebx + 4], 1
00490d7c  8903                     mov      dword ptr [ebx], eax
00490d7e  b874225200               mov      eax, 0x522274
00490d83  e81b000000               call     0x490da3
00490d88  6aff                     push     -1
00490d8a  8b2b                     mov      ebp, dword ptr [ebx]
00490d8c  55                       push     ebp
00490d8d  e8cc2b0000               call     0x49395e ; WaitForSingleObject
00490d92  897308                   mov      dword ptr [ebx + 8], esi
00490d95  ff430c                   inc      dword ptr [ebx + 0xc]
00490d98  5d                       pop      ebp
00490d99  5e                       pop      esi
00490d9a  5a                       pop      edx
00490d9b  59                       pop      ecx
00490d9c  5b                       pop      ebx
00490d9d  c3                       ret      

; CRT_thread_join 004936a7..004936c9
004936a7  6aff                     push     -1
004936a9  8b5c2434                 mov      ebx, dword ptr [esp + 0x34]
004936ad  53                       push     ebx
004936ae  e8ab020000               call     0x49395e ; WaitForSingleObject
004936b3  8b742430                 mov      esi, dword ptr [esp + 0x30]
004936b7  56                       push     esi
004936b8  e8ef020000               call     0x4939ac
004936bd  8b44243c                 mov      eax, dword ptr [esp + 0x3c]
004936c1  83c440                   add      esp, 0x40
004936c4  5d                       pop      ebp
004936c5  07                       pop      es
004936c6  5f                       pop      edi
004936c7  5e                       pop      esi
004936c8  c3                       ret      
