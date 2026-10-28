; EnginNextEtape (unit-dispatch); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0045442c..0x00456c34 (end exclusive); labels are original SBL names
0045442c  53                       push ebx
0045442d  51                       push ecx
0045442e  52                       push edx
0045442f  56                       push esi
00454430  57                       push edi
00454431  55                       push ebp
00454432  83ec64                   sub esp, 0x64
00454435  89c7                     mov edi, eax
00454437  31db                     xor ebx, ebx
00454439  6689c3                   mov bx, ax
0045443c  89d8                     mov eax, ebx
0045443e  c1e004                   shl eax, 4
00454441  01d8                     add eax, ebx
00454443  c1e002                   shl eax, 2
00454446  01d8                     add eax, ebx
00454448  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0045444e  c1e002                   shl eax, 2
00454451  01c6                     add esi, eax
00454453  31c0                     xor eax, eax
00454455  8a4602                   mov al, byte ptr [esi + 2]
00454458  85c0                     test eax, eax
0045445a  0f95c0                   setne al
0045445d  84c0                     test al, al
0045445f  7437                     je 0x454498
00454461  8a06                     mov al, byte ptr [esi]
00454463  88442458                 mov byte ptr [esp + 0x58], al
00454467  8a4601                   mov al, byte ptr [esi + 1]
0045446a  8b9604010000             mov edx, dword ptr [esi + 0x104]
00454470  88442460                 mov byte ptr [esp + 0x60], al
00454474  83faff                   cmp edx, -1
00454477  7418                     je 0x454491
00454479  89d8                     mov eax, ebx
0045447b  e8ddc7feff               call 0x440c5d ; -> EnginGetVolume
00454480  8d9e04010000             lea ebx, [esi + 0x104]
00454486  89c2                     mov edx, eax
00454488  89d8                     mov eax, ebx
0045448a  e840660300               call 0x48aacf ; -> PlaySnd_PostVolume
0045448f  eb07                     jmp 0x454498
00454491  c686f900000000           mov byte ptr [esi + 0xf9], 0
00454498  31d2                     xor edx, edx
0045449a  6689fa                   mov dx, di
0045449d  89d0                     mov eax, edx
0045449f  c1e004                   shl eax, 4
004544a2  01d0                     add eax, edx
004544a4  c1e002                   shl eax, 2
004544a7  01d0                     add eax, edx
004544a9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004544af  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
004544b3  25ff000000               and eax, 0xff
004544b8  7409                     je 0x4544c3
004544ba  83f804                   cmp eax, 4
004544bd  7404                     je 0x4544c3
004544bf  b001                     mov al, 1
004544c1  eb02                     jmp 0x4544c5
004544c3  30c0                     xor al, al
004544c5  84c0                     test al, al
004544c7  0f844f270000             je 0x456c1c
004544cd  31c0                     xor eax, eax
004544cf  8a4601                   mov al, byte ptr [esi + 1]
004544d2  83f810                   cmp eax, 0x10
004544d5  7559                     jne 0x454530
004544d7  31d2                     xor edx, edx
004544d9  6689fa                   mov dx, di
004544dc  89d0                     mov eax, edx
004544de  c1e004                   shl eax, 4
004544e1  01d0                     add eax, edx
004544e3  c1e002                   shl eax, 2
004544e6  01d0                     add eax, edx
004544e8  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
004544ee  c1e002                   shl eax, 2
004544f1  01c3                     add ebx, eax
004544f3  8aa3a9000000             mov ah, byte ptr [ebx + 0xa9]
004544f9  fec4                     inc ah
004544fb  8a93a7000000             mov dl, byte ptr [ebx + 0xa7]
00454501  88a3a9000000             mov byte ptr [ebx + 0xa9], ah
00454507  38d4                     cmp ah, dl
00454509  7525                     jne 0x454530
0045450b  31d2                     xor edx, edx
0045450d  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
00454513  31c9                     xor ecx, ecx
00454515  42                       inc edx
00454516  8a8ba5000000             mov cl, byte ptr [ebx + 0xa5]
0045451c  89d0                     mov eax, edx
0045451e  c1fa1f                   sar edx, 0x1f
00454521  f7f9                     idiv ecx
00454523  c683a900000000           mov byte ptr [ebx + 0xa9], 0
0045452a  8893a4000000             mov byte ptr [ebx + 0xa4], dl
00454530  31d2                     xor edx, edx
00454532  6689fa                   mov dx, di
00454535  89d0                     mov eax, edx
00454537  c1e004                   shl eax, 4
0045453a  01d0                     add eax, edx
0045453c  c1e002                   shl eax, 2
0045453f  01d0                     add eax, edx
00454541  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00454547  c1e002                   shl eax, 2
0045454a  01c1                     add ecx, eax
0045454c  31db                     xor ebx, ebx
0045454e  8a5901                   mov bl, byte ptr [ecx + 1]
00454551  89d8                     mov eax, ebx
00454553  c1e002                   shl eax, 2
00454556  29d8                     sub eax, ebx
00454558  c1e003                   shl eax, 3
0045455b  01d8                     add eax, ebx
0045455d  0fb72c45de654900         movzx ebp, word ptr [eax*2 + 0x4965de]
00454565  31c0                     xor eax, eax
00454567  ba03000000               mov edx, 3
0045456c  8a01                     mov al, byte ptr [ecx]
0045456e  e84d47fdff               call 0x428cc0 ; -> BonusGetValEngin
00454573  25ffff0000               and eax, 0xffff
00454578  29c5                     sub ebp, eax
0045457a  31c0                     xor eax, eax
0045457c  668b8102010000           mov ax, word ptr [ecx + 0x102]
00454583  39e8                     cmp eax, ebp
00454585  7d0a                     jge 0x454591
00454587  89c2                     mov edx, eax
00454589  42                       inc edx
0045458a  66899102010000           mov word ptr [ecx + 0x102], dx
00454591  8a742460                 mov dh, byte ptr [esp + 0x60]
00454595  80fe10                   cmp dh, 0x10
00454598  7205                     jb 0x45459f
0045459a  80fe11                   cmp dh, 0x11
0045459d  7608                     jbe 0x4545a7
0045459f  30c0                     xor al, al
004545a1  84c0                     test al, al
004545a3  754e                     jne 0x4545f3
004545a5  eb08                     jmp 0x4545af
004545a7  b001                     mov al, 1
004545a9  ebf6                     jmp 0x4545a1
004545ab  b001                     mov al, 1
004545ad  eb19                     jmp 0x4545c8
004545af  8a442460                 mov al, byte ptr [esp + 0x60]
004545b3  2c0b                     sub al, 0xb
004545b5  3c05                     cmp al, 5
004545b7  770d                     ja 0x4545c6
004545b9  25ff000000               and eax, 0xff
004545be  2eff24852c434500         jmp dword ptr cs:[eax*4 + 0x45432c]
004545c6  30c0                     xor al, al
004545c8  84c0                     test al, al
004545ca  7427                     je 0x4545f3
004545cc  83be04010000ff           cmp dword ptr [esi + 0x104], -1
004545d3  741e                     je 0x4545f3
004545d5  668b467e                 mov ax, word ptr [esi + 0x7e]
004545d9  663b4608                 cmp ax, word ptr [esi + 8]
004545dd  7514                     jne 0x4545f3
004545df  80bef900000000           cmp byte ptr [esi + 0xf9], 0
004545e6  740b                     je 0x4545f3
004545e8  8d8604010000             lea eax, [esi + 0x104]
004545ee  e8cd640300               call 0x48aac0 ; -> PlaySnd_StopSound
004545f3  31c0                     xor eax, eax
004545f5  8a442460                 mov al, byte ptr [esp + 0x60]
004545f9  83f810                   cmp eax, 0x10
004545fc  0f8585000000             jne 0x454687
00454602  83be04010000ff           cmp dword ptr [esi + 0x104], -1
00454609  0f8578000000             jne 0x454687
0045460f  31c9                     xor ecx, ecx
00454611  6689f9                   mov cx, di
00454614  89c8                     mov eax, ecx
00454616  c1e004                   shl eax, 4
00454619  01c8                     add eax, ecx
0045461b  c1e002                   shl eax, 2
0045461e  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00454624  01c8                     add eax, ecx
00454626  89ca                     mov edx, ecx
00454628  c1e002                   shl eax, 2
0045462b  31ca                     xor edx, ecx
0045462d  01c3                     add ebx, eax
0045462f  31c0                     xor eax, eax
00454631  8a1541805000             mov dl, byte ptr [0x508041]
00454637  668b4308                 mov ax, word ptr [ebx + 8]
0045463b  e8b0200200               call 0x4766f0 ; -> TerrainEstDecouvert
00454640  84c0                     test al, al
00454642  743c                     je 0x454680
00454644  89c8                     mov eax, ecx
00454646  e812c6feff               call 0x440c5d ; -> EnginGetVolume
0045464b  8bab04010000             mov ebp, dword ptr [ebx + 0x104]
00454651  c683f900000001           mov byte ptr [ebx + 0xf9], 1
00454658  83fdff                   cmp ebp, -1
0045465b  7523                     jne 0x454680
0045465d  b901000000               mov ecx, 1
00454662  31d2                     xor edx, edx
00454664  50                       push eax
00454665  8a5301                   mov dl, byte ptr [ebx + 1]
00454668  8d8304010000             lea eax, [ebx + 0x104]
0045466e  c1e210                   shl edx, 0x10
00454671  89c3                     mov ebx, eax
00454673  b850000000               mov eax, 0x50
00454678  80ce08                   or dh, 8
0045467b  e8f9630300               call 0x48aa79 ; -> PlaySnd_PostSound
00454680  c686f900000001           mov byte ptr [esi + 0xf9], 1
00454687  31c0                     xor eax, eax
00454689  8a4602                   mov al, byte ptr [esi + 2]
0045468c  83f80e                   cmp eax, 0xe
0045468f  0f844b010000             je 0x4547e0
00454695  31c0                     xor eax, eax
00454697  8b157c8f5000             mov edx, dword ptr [0x508f7c]
0045469d  6689f8                   mov ax, di
004546a0  01d0                     add eax, edx
004546a2  a81f                     test al, 0x1f
004546a4  0f8536010000             jne 0x4547e0
004546aa  31c0                     xor eax, eax
004546ac  8a442458                 mov al, byte ptr [esp + 0x58]
004546b0  3dc8000000               cmp eax, 0xc8
004546b5  7505                     jne 0x4546bc
004546b7  e924010000               jmp 0x4547e0
004546bc  31d2                     xor edx, edx
004546be  6689fa                   mov dx, di
004546c1  89d0                     mov eax, edx
004546c3  c1e004                   shl eax, 4
004546c6  01d0                     add eax, edx
004546c8  c1e002                   shl eax, 2
004546cb  01c2                     add edx, eax
004546cd  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004546d2  c1e202                   shl edx, 2
004546d5  8a440201                 mov al, byte ptr [edx + eax + 1]
004546d9  3c0f                     cmp al, 0xf
004546db  7220                     jb 0x4546fd
004546dd  761a                     jbe 0x4546f9
004546df  3c14                     cmp al, 0x14
004546e1  720e                     jb 0x4546f1
004546e3  3c16                     cmp al, 0x16
004546e5  7612                     jbe 0x4546f9
004546e7  3c18                     cmp al, 0x18
004546e9  760e                     jbe 0x4546f9
004546eb  3c19                     cmp al, 0x19
004546ed  740a                     je 0x4546f9
004546ef  eb20                     jmp 0x454711
004546f1  3c10                     cmp al, 0x10
004546f3  7604                     jbe 0x4546f9
004546f5  3c12                     cmp al, 0x12
004546f7  7218                     jb 0x454711
004546f9  b001                     mov al, 1
004546fb  eb16                     jmp 0x454713
004546fd  3c03                     cmp al, 3
004546ff  72f8                     jb 0x4546f9
00454701  76f6                     jbe 0x4546f9
00454703  3c08                     cmp al, 8
00454705  720a                     jb 0x454711
00454707  76f0                     jbe 0x4546f9
00454709  3c0b                     cmp al, 0xb
0045470b  7204                     jb 0x454711
0045470d  3c0c                     cmp al, 0xc
0045470f  76e8                     jbe 0x4546f9
00454711  30c0                     xor al, al
00454713  84c0                     test al, al
00454715  0f84c5000000             je 0x4547e0
0045471b  31c0                     xor eax, eax
0045471d  8a442458                 mov al, byte ptr [esp + 0x58]
00454721  e8f1900100               call 0x46d817 ; -> PlayerGetType
00454726  88442450                 mov byte ptr [esp + 0x50], al
0045472a  31c0                     xor eax, eax
0045472c  8a4602                   mov al, byte ptr [esi + 2]
0045472f  83f801                   cmp eax, 1
00454732  0f84a8000000             je 0x4547e0
00454738  83f813                   cmp eax, 0x13
0045473b  7509                     jne 0x454746
0045473d  e99e000000               jmp 0x4547e0
00454742  b001                     mov al, 1
00454744  eb12                     jmp 0x454758
00454746  8a4c2460                 mov cl, byte ptr [esp + 0x60]
0045474a  80f90e                   cmp cl, 0xe
0045474d  7207                     jb 0x454756
0045474f  76f1                     jbe 0x454742
00454751  80f910                   cmp cl, 0x10
00454754  74ec                     je 0x454742
00454756  30c0                     xor al, al
00454758  84c0                     test al, al
0045475a  7422                     je 0x45477e
0045475c  31d2                     xor edx, edx
0045475e  6689fa                   mov dx, di
00454761  89d0                     mov eax, edx
00454763  c1e004                   shl eax, 4
00454766  01d0                     add eax, edx
00454768  c1e002                   shl eax, 2
0045476b  01d0                     add eax, edx
0045476d  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454773  8a8482da000000           mov al, byte ptr [edx + eax*4 + 0xda]
0045477a  84c0                     test al, al
0045477c  7516                     jne 0x454794
0045477e  8a642460                 mov ah, byte ptr [esp + 0x60]
00454782  80fc0e                   cmp ah, 0xe
00454785  7207                     jb 0x45478e
00454787  763d                     jbe 0x4547c6
00454789  80fc10                   cmp ah, 0x10
0045478c  7438                     je 0x4547c6
0045478e  30c0                     xor al, al
00454790  84c0                     test al, al
00454792  754c                     jne 0x4547e0
00454794  31c9                     xor ecx, ecx
00454796  6689f9                   mov cx, di
00454799  89c8                     mov eax, ecx
0045479b  31db                     xor ebx, ebx
0045479d  e8d2f7ffff               call 0x453f74 ; -> EnginTrouveCible
004547a2  6689c3                   mov bx, ax
004547a5  81fbffff0000             cmp ebx, 0xffff
004547ab  7433                     je 0x4547e0
004547ad  31c0                     xor eax, eax
004547af  8a442450                 mov al, byte ptr [esp + 0x50]
004547b3  83f802                   cmp eax, 2
004547b6  7512                     jne 0x4547ca
004547b8  ba49000000               mov edx, 0x49
004547bd  89c8                     mov eax, ecx
004547bf  e804e20200               call 0x4829c8 ; -> iagUnitSendMessage
004547c4  eb1a                     jmp 0x4547e0
004547c6  b001                     mov al, 1
004547c8  ebc6                     jmp 0x454790
004547ca  31c0                     xor eax, eax
004547cc  8a4602                   mov al, byte ptr [esi + 2]
004547cf  83f807                   cmp eax, 7
004547d2  750c                     jne 0x4547e0
004547d4  ba01000000               mov edx, 1
004547d9  89c8                     mov eax, ecx
004547db  e85612ffff               call 0x445a36 ; -> SetAttaqueEngin
004547e0  31db                     xor ebx, ebx
004547e2  6689fb                   mov bx, di
004547e5  89d8                     mov eax, ebx
004547e7  c1e004                   shl eax, 4
004547ea  01d8                     add eax, ebx
004547ec  c1e002                   shl eax, 2
004547ef  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004547f5  01d8                     add eax, ebx
004547f7  8a8482dc000000           mov al, byte ptr [edx + eax*4 + 0xdc]
004547fe  ba02000000               mov edx, 2
00454803  25ff000000               and eax, 0xff
00454808  e88a350100               call 0x467d97 ; -> GetBit
0045480d  84c0                     test al, al
0045480f  7444                     je 0x454855
00454811  b802000000               mov eax, 2
00454816  e834ff0100               call 0x47474f ; -> SortilegeGetTempsFin
0045481b  31c9                     xor ecx, ecx
0045481d  31d2                     xor edx, edx
0045481f  6689c1                   mov cx, ax
00454822  a17c8f5000               mov eax, dword ptr [0x508f7c]
00454827  f7f1                     div ecx
00454829  85d2                     test edx, edx
0045482b  7528                     jne 0x454855
0045482d  668b8e9a000000           mov cx, word ptr [esi + 0x9a]
00454834  31c0                     xor eax, eax
00454836  49                       dec ecx
00454837  6689c8                   mov ax, cx
0045483a  66898e9a000000           mov word ptr [esi + 0x9a], cx
00454841  85c0                     test eax, eax
00454843  7510                     jne 0x454855
00454845  89d8                     mov eax, ebx
00454847  e8ec00ffff               call 0x444938 ; -> SetDyingEngin
0045484c  e97c040000               jmp 0x454ccd
00454851  b001                     mov al, 1
00454853  eb16                     jmp 0x45486b
00454855  8a4601                   mov al, byte ptr [esi + 1]
00454858  3c19                     cmp al, 0x19
0045485a  770d                     ja 0x454869
0045485c  25ff000000               and eax, 0xff
00454861  2eff248544434500         jmp dword ptr cs:[eax*4 + 0x454344]
00454869  30c0                     xor al, al
0045486b  84c0                     test al, al
0045486d  0f8421010000             je 0x454994
00454873  31db                     xor ebx, ebx
00454875  6689fb                   mov bx, di
00454878  89d9                     mov ecx, ebx
0045487a  c1e104                   shl ecx, 4
0045487d  01d9                     add ecx, ebx
0045487f  c1e102                   shl ecx, 2
00454882  01d9                     add ecx, ebx
00454884  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454889  c1e102                   shl ecx, 2
0045488c  8a8401dc000000           mov al, byte ptr [ecx + eax + 0xdc]
00454893  ba02000000               mov edx, 2
00454898  25ff000000               and eax, 0xff
0045489d  e8f5340100               call 0x467d97 ; -> GetBit
004548a2  84c0                     test al, al
004548a4  0f85ea000000             jne 0x454994
004548aa  89d8                     mov eax, ebx
004548ac  e817e4ffff               call 0x452cc8 ; -> CalculFatigue
004548b1  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004548b6  01c1                     add ecx, eax
004548b8  31c0                     xor eax, eax
004548ba  8a4102                   mov al, byte ptr [ecx + 2]
004548bd  85c0                     test eax, eax
004548bf  7409                     je 0x4548ca
004548c1  83f804                   cmp eax, 4
004548c4  7404                     je 0x4548ca
004548c6  b001                     mov al, 1
004548c8  eb02                     jmp 0x4548cc
004548ca  30c0                     xor al, al
004548cc  84c0                     test al, al
004548ce  0f84f9030000             je 0x454ccd
004548d4  31c0                     xor eax, eax
004548d6  668b4604                 mov ax, word ptr [esi + 4]
004548da  83f804                   cmp eax, 4
004548dd  0f84b1000000             je 0x454994
004548e3  31d2                     xor edx, edx
004548e5  6689fa                   mov dx, di
004548e8  89d0                     mov eax, edx
004548ea  c1e004                   shl eax, 4
004548ed  01d0                     add eax, edx
004548ef  c1e002                   shl eax, 2
004548f2  01d0                     add eax, edx
004548f4  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004548fa  c1e002                   shl eax, 2
004548fd  01c2                     add edx, eax
004548ff  31c0                     xor eax, eax
00454901  8a4202                   mov al, byte ptr [edx + 2]
00454904  85c0                     test eax, eax
00454906  7409                     je 0x454911
00454908  83f804                   cmp eax, 4
0045490b  7404                     je 0x454911
0045490d  b001                     mov al, 1
0045490f  eb02                     jmp 0x454913
00454911  30c0                     xor al, al
00454913  84c0                     test al, al
00454915  0f8479000000             je 0x454994
0045491b  31c9                     xor ecx, ecx
0045491d  6689f9                   mov cx, di
00454920  89c8                     mov eax, ecx
00454922  c1e004                   shl eax, 4
00454925  01c8                     add eax, ecx
00454927  c1e002                   shl eax, 2
0045492a  01c8                     add eax, ecx
0045492c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454932  c1e002                   shl eax, 2
00454935  01d0                     add eax, edx
00454937  8a5072                   mov dl, byte ptr [eax + 0x72]
0045493a  84d2                     test dl, dl
0045493c  7456                     je 0x454994
0045493e  31d2                     xor edx, edx
00454940  668b5004                 mov dx, word ptr [eax + 4]
00454944  85d2                     test edx, edx
00454946  0f94c2                   sete dl
00454949  84d2                     test dl, dl
0045494b  7447                     je 0x454994
0045494d  8b9683000000             mov edx, dword ptr [esi + 0x83]
00454953  c1fa18                   sar edx, 0x18
00454956  85d2                     test edx, edx
00454958  753a                     jne 0x454994
0045495a  8b9684000000             mov edx, dword ptr [esi + 0x84]
00454960  c1fa18                   sar edx, 0x18
00454963  85d2                     test edx, edx
00454965  752d                     jne 0x454994
00454967  8a00                     mov al, byte ptr [eax]
00454969  25ff000000               and eax, 0xff
0045496e  e8a48e0100               call 0x46d817 ; -> PlayerGetType
00454973  25ff000000               and eax, 0xff
00454978  83f802                   cmp eax, 2
0045497b  7510                     jne 0x45498d
0045497d  ba4b000000               mov edx, 0x4b
00454982  89c8                     mov eax, ecx
00454984  31db                     xor ebx, ebx
00454986  e83de00200               call 0x4829c8 ; -> iagUnitSendMessage
0045498b  eb07                     jmp 0x454994
0045498d  89c8                     mov eax, ecx
0045498f  e8f0f1ffff               call 0x453b84 ; -> EnginSetFatigue
00454994  31d2                     xor edx, edx
00454996  6689fa                   mov dx, di
00454999  89d0                     mov eax, edx
0045499b  c1e004                   shl eax, 4
0045499e  01d0                     add eax, edx
004549a0  c1e002                   shl eax, 2
004549a3  01d0                     add eax, edx
004549a5  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004549ab  c1e002                   shl eax, 2
004549ae  01d0                     add eax, edx
004549b0  8a5001                   mov dl, byte ptr [eax + 1]
004549b3  81e2ff000000             and edx, 0xff
004549b9  83fa11                   cmp edx, 0x11
004549bc  0f857a010000             jne 0x454b3c
004549c2  8a10                     mov dl, byte ptr [eax]
004549c4  897c2428                 mov dword ptr [esp + 0x28], edi
004549c8  8854244c                 mov byte ptr [esp + 0x4c], dl
004549cc  81e2ff000000             and edx, 0xff
004549d2  668b14d5141a4e00         mov dx, word ptr [edx*8 + 0x4e1a14]
004549da  81e2ffff0000             and edx, 0xffff
004549e0  0f8556010000             jne 0x454b3c
004549e6  b11e                     mov cl, 0x1e
004549e8  89fb                     mov ebx, edi
004549ea  8a4002                   mov al, byte ptr [eax + 2]
004549ed  25ff000000               and eax, 0xff
004549f2  7409                     je 0x4549fd
004549f4  83f804                   cmp eax, 4
004549f7  7404                     je 0x4549fd
004549f9  b001                     mov al, 1
004549fb  eb02                     jmp 0x4549ff
004549fd  30c0                     xor al, al
004549ff  84c0                     test al, al
00454a01  744c                     je 0x454a4f
00454a03  31d2                     xor edx, edx
00454a05  6689da                   mov dx, bx
00454a08  89d0                     mov eax, edx
00454a0a  c1e004                   shl eax, 4
00454a0d  01d0                     add eax, edx
00454a0f  c1e002                   shl eax, 2
00454a12  01c2                     add edx, eax
00454a14  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454a19  c1e202                   shl edx, 2
00454a1c  884c0202                 mov byte ptr [edx + eax + 2], cl
00454a20  66a104634900             mov ax, word ptr [0x496304]
00454a26  6639c3                   cmp bx, ax
00454a29  7524                     jne 0x454a4f
00454a2b  30c3                     xor bl, al
00454a2d  881d360f4e00             mov byte ptr [0x4e0f36], bl
00454a33  30e7                     xor bh, ah
00454a35  baffff0000               mov edx, 0xffff
00454a3a  883d370f4e00             mov byte ptr [0x4e0f37], bh
00454a40  31db                     xor ebx, ebx
00454a42  66891504634900           mov word ptr [0x496304], dx
00454a49  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00454a4f  31db                     xor ebx, ebx
00454a51  31c9                     xor ecx, ecx
00454a53  8a5c244c                 mov bl, byte ptr [esp + 0x4c]
00454a57  668b4c2428               mov cx, word ptr [esp + 0x28]
00454a5c  31d2                     xor edx, edx
00454a5e  89c8                     mov eax, ecx
00454a60  668b14dd1a1a4e00         mov dx, word ptr [ebx*8 + 0x4e1a1a]
00454a68  e8660dffff               call 0x4457d3 ; -> SetDeplaceEngin
00454a6d  89c8                     mov eax, ecx
00454a6f  c1e004                   shl eax, 4
00454a72  01c8                     add eax, ecx
00454a74  c1e002                   shl eax, 2
00454a77  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454a7d  01c8                     add eax, ecx
00454a7f  668b44827c               mov ax, word ptr [edx + eax*4 + 0x7c]
00454a84  663b04dd1a1a4e00         cmp ax, word ptr [ebx*8 + 0x4e1a1a]
00454a8c  741a                     je 0x454aa8
00454a8e  31d2                     xor edx, edx
00454a90  6689c2                   mov dx, ax
00454a93  89d0                     mov eax, edx
00454a95  c1fa1f                   sar edx, 0x1f
00454a98  c1e208                   shl edx, 8
00454a9b  1bc2                     sbb eax, edx
00454a9d  c1f808                   sar eax, 8
00454aa0  85c0                     test eax, eax
00454aa2  0f8594000000             jne 0x454b3c
00454aa8  31d2                     xor edx, edx
00454aaa  668b542428               mov dx, word ptr [esp + 0x28]
00454aaf  89d0                     mov eax, edx
00454ab1  e8a2250000               call 0x457058 ; -> RetireEngin
00454ab6  89d0                     mov eax, edx
00454ab8  c1e004                   shl eax, 4
00454abb  01d0                     add eax, edx
00454abd  c1e002                   shl eax, 2
00454ac0  89d3                     mov ebx, edx
00454ac2  01d0                     add eax, edx
00454ac4  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454aca  30c9                     xor cl, cl
00454acc  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00454ad0  25ff000000               and eax, 0xff
00454ad5  7409                     je 0x454ae0
00454ad7  83f804                   cmp eax, 4
00454ada  7404                     je 0x454ae0
00454adc  b001                     mov al, 1
00454ade  eb02                     jmp 0x454ae2
00454ae0  30c0                     xor al, al
00454ae2  84c0                     test al, al
00454ae4  7446                     je 0x454b2c
00454ae6  31d2                     xor edx, edx
00454ae8  6689da                   mov dx, bx
00454aeb  89d0                     mov eax, edx
00454aed  c1e004                   shl eax, 4
00454af0  01d0                     add eax, edx
00454af2  c1e002                   shl eax, 2
00454af5  01d0                     add eax, edx
00454af7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454afd  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
00454b01  663b1d04634900           cmp bx, word ptr [0x496304]
00454b08  7522                     jne 0x454b2c
00454b0a  30c9                     xor cl, cl
00454b0c  baffff0000               mov edx, 0xffff
00454b11  880d360f4e00             mov byte ptr [0x4e0f36], cl
00454b17  880d370f4e00             mov byte ptr [0x4e0f37], cl
00454b1d  31c9                     xor ecx, ecx
00454b1f  66891504634900           mov word ptr [0x496304], dx
00454b26  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
00454b2c  31c0                     xor eax, eax
00454b2e  8a44244c                 mov al, byte ptr [esp + 0x4c]
00454b32  66c704c5181a4e00ffff     mov word ptr [eax*8 + 0x4e1a18], 0xffff
00454b3c  31db                     xor ebx, ebx
00454b3e  6689fb                   mov bx, di
00454b41  89d8                     mov eax, ebx
00454b43  c1e004                   shl eax, 4
00454b46  01d8                     add eax, ebx
00454b48  c1e002                   shl eax, 2
00454b4b  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454b51  01d8                     add eax, ebx
00454b53  8a448272                 mov al, byte ptr [edx + eax*4 + 0x72]
00454b57  84c0                     test al, al
00454b59  7417                     je 0x454b72
00454b5b  31c0                     xor eax, eax
00454b5d  8a4602                   mov al, byte ptr [esi + 2]
00454b60  83f804                   cmp eax, 4
00454b63  740d                     je 0x454b72
00454b65  31d2                     xor edx, edx
00454b67  89d8                     mov eax, ebx
00454b69  668b5608                 mov dx, word ptr [esi + 8]
00454b6d  e842e1feff               call 0x442cb4 ; -> SetEnginCollision
00454b72  31d2                     xor edx, edx
00454b74  6689fa                   mov dx, di
00454b77  89d3                     mov ebx, edx
00454b79  c1e304                   shl ebx, 4
00454b7c  01d3                     add ebx, edx
00454b7e  c1e302                   shl ebx, 2
00454b81  01d3                     add ebx, edx
00454b83  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454b88  c1e302                   shl ebx, 2
00454b8b  8a8403dc000000           mov al, byte ptr [ebx + eax + 0xdc]
00454b92  ba01000000               mov edx, 1
00454b97  25ff000000               and eax, 0xff
00454b9c  e8f6310100               call 0x467d97 ; -> GetBit
00454ba1  84c0                     test al, al
00454ba3  744a                     je 0x454bef
00454ba5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454baa  01d8                     add eax, ebx
00454bac  8bb0e4000000             mov esi, dword ptr [eax + 0xe4]
00454bb2  83c004                   add eax, 4
00454bb5  4e                       dec esi
00454bb6  89b0e0000000             mov dword ptr [eax + 0xe0], esi
00454bbc  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454bc1  01c3                     add ebx, eax
00454bc3  8d4304                   lea eax, [ebx + 4]
00454bc6  668b80e0000000           mov ax, word ptr [eax + 0xe0]
00454bcd  25ffff0000               and eax, 0xffff
00454bd2  0f85f5000000             jne 0x454ccd
00454bd8  8d83dc000000             lea eax, [ebx + 0xdc]
00454bde  ba01000000               mov edx, 1
00454be3  31db                     xor ebx, ebx
00454be5  e887310100               call 0x467d71 ; -> SetBit
00454bea  e9de000000               jmp 0x454ccd
00454bef  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454bf4  8a8403dc000000           mov al, byte ptr [ebx + eax + 0xdc]
00454bfb  ba03000000               mov edx, 3
00454c00  25ff000000               and eax, 0xff
00454c05  e88d310100               call 0x467d97 ; -> GetBit
00454c0a  84c0                     test al, al
00454c0c  7441                     je 0x454c4f
00454c0e  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454c13  01d8                     add eax, ebx
00454c15  8ba8ec000000             mov ebp, dword ptr [eax + 0xec]
00454c1b  83c00c                   add eax, 0xc
00454c1e  4d                       dec ebp
00454c1f  89a8e0000000             mov dword ptr [eax + 0xe0], ebp
00454c25  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454c2a  01c3                     add ebx, eax
00454c2c  8d430c                   lea eax, [ebx + 0xc]
00454c2f  668b80e0000000           mov ax, word ptr [eax + 0xe0]
00454c36  25ffff0000               and eax, 0xffff
00454c3b  7512                     jne 0x454c4f
00454c3d  8d83dc000000             lea eax, [ebx + 0xdc]
00454c43  ba03000000               mov edx, 3
00454c48  31db                     xor ebx, ebx
00454c4a  e822310100               call 0x467d71 ; -> SetBit
00454c4f  31d2                     xor edx, edx
00454c51  6689fa                   mov dx, di
00454c54  89d0                     mov eax, edx
00454c56  c1e004                   shl eax, 4
00454c59  01d0                     add eax, edx
00454c5b  c1e002                   shl eax, 2
00454c5e  01c2                     add edx, eax
00454c60  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454c65  c1e202                   shl edx, 2
00454c68  8a440201                 mov al, byte ptr [edx + eax + 1]
00454c6c  3c0c                     cmp al, 0xc
00454c6e  7206                     jb 0x454c76
00454c70  761d                     jbe 0x454c8f
00454c72  3c0f                     cmp al, 0xf
00454c74  7419                     je 0x454c8f
00454c76  30c0                     xor al, al
00454c78  84c0                     test al, al
00454c7a  0f849c1f0000             je 0x456c1c
00454c80  31c0                     xor eax, eax
00454c82  6689f8                   mov ax, di
00454c85  e81d38ffff               call 0x4484a7 ; -> RotateTourEngin
00454c8a  e98d1f0000               jmp 0x456c1c
00454c8f  b001                     mov al, 1
00454c91  ebe5                     jmp 0x454c78
00454c93  31c0                     xor eax, eax
00454c95  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454c9c  3dffff0000               cmp eax, 0xffff
00454ca1  0f84ad080000             je 0x455554
00454ca7  31c0                     xor eax, eax
00454ca9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454cb0  e8565afcff               call 0x41a70b ; -> BatimentEnDestruction
00454cb5  84c0                     test al, al
00454cb7  0f8497080000             je 0x455554
00454cbd  31c0                     xor eax, eax
00454cbf  31d2                     xor edx, edx
00454cc1  6689f8                   mov ax, di
00454cc4  668b567e                 mov dx, word ptr [esi + 0x7e]
00454cc8  e8060bffff               call 0x4457d3 ; -> SetDeplaceEngin
00454ccd  83c464                   add esp, 0x64
00454cd0  e9c8a5ffff               jmp 0x44f29d
00454cd5  31d2                     xor edx, edx
00454cd7  6689fa                   mov dx, di
00454cda  89d0                     mov eax, edx
00454cdc  c1e004                   shl eax, 4
00454cdf  01d0                     add eax, edx
00454ce1  c1e002                   shl eax, 2
00454ce4  01d0                     add eax, edx
00454ce6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00454cec  8a448201                 mov al, byte ptr [edx + eax*4 + 1]
00454cf0  25ff000000               and eax, 0xff
00454cf5  83f806                   cmp eax, 6
00454cf8  755c                     jne 0x454d56
00454cfa  668b9ec0000000           mov bx, word ptr [esi + 0xc0]
00454d01  31d2                     xor edx, edx
00454d03  6689da                   mov dx, bx
00454d06  89d0                     mov eax, edx
00454d08  c1e004                   shl eax, 4
00454d0b  01d0                     add eax, edx
00454d0d  c1e002                   shl eax, 2
00454d10  01c2                     add edx, eax
00454d12  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454d17  c1e202                   shl edx, 2
00454d1a  8a440202                 mov al, byte ptr [edx + eax + 2]
00454d1e  25ff000000               and eax, 0xff
00454d23  742b                     je 0x454d50
00454d25  31d2                     xor edx, edx
00454d27  6689da                   mov dx, bx
00454d2a  89d0                     mov eax, edx
00454d2c  c1e004                   shl eax, 4
00454d2f  01d0                     add eax, edx
00454d31  c1e002                   shl eax, 2
00454d34  01c2                     add edx, eax
00454d36  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454d3b  c1e202                   shl edx, 2
00454d3e  8a440202                 mov al, byte ptr [edx + eax + 2]
00454d42  25ff000000               and eax, 0xff
00454d47  83f804                   cmp eax, 4
00454d4a  7404                     je 0x454d50
00454d4c  b001                     mov al, 1
00454d4e  eb02                     jmp 0x454d52
00454d50  30c0                     xor al, al
00454d52  84c0                     test al, al
00454d54  7441                     je 0x454d97
00454d56  31d2                     xor edx, edx
00454d58  6689fa                   mov dx, di
00454d5b  89d0                     mov eax, edx
00454d5d  c1e004                   shl eax, 4
00454d60  01d0                     add eax, edx
00454d62  c1e002                   shl eax, 2
00454d65  01c2                     add edx, eax
00454d67  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00454d6c  c1e202                   shl edx, 2
00454d6f  8a440201                 mov al, byte ptr [edx + eax + 1]
00454d73  25ff000000               and eax, 0xff
00454d78  83f807                   cmp eax, 7
00454d7b  0f85d3070000             jne 0x455554
00454d81  31c0                     xor eax, eax
00454d83  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454d8a  e87c59fcff               call 0x41a70b ; -> BatimentEnDestruction
00454d8f  84c0                     test al, al
00454d91  0f84bd070000             je 0x455554
00454d97  31c0                     xor eax, eax
00454d99  31d2                     xor edx, edx
00454d9b  6689f8                   mov ax, di
00454d9e  668b567e                 mov dx, word ptr [esi + 0x7e]
00454da2  e82c0affff               call 0x4457d3 ; -> SetDeplaceEngin
00454da7  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
00454db0  e918ffffff               jmp 0x454ccd
00454db5  31c0                     xor eax, eax
00454db7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454dbe  e84859fcff               call 0x41a70b ; -> BatimentEnDestruction
00454dc3  84c0                     test al, al
00454dc5  7516                     jne 0x454ddd
00454dc7  31c0                     xor eax, eax
00454dc9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454dd0  e8b752fcff               call 0x41a08c ; -> BatimentGetPlayer
00454dd5  3a06                     cmp al, byte ptr [esi]
00454dd7  0f84e2000000             je 0x454ebf
00454ddd  31c9                     xor ecx, ecx
00454ddf  6689f9                   mov cx, di
00454de2  89cd                     mov ebp, ecx
00454de4  c1e504                   shl ebp, 4
00454de7  01cd                     add ebp, ecx
00454de9  c1e502                   shl ebp, 2
00454dec  01cd                     add ebp, ecx
00454dee  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00454df4  c1e502                   shl ebp, 2
00454df7  01eb                     add ebx, ebp
00454df9  8a4372                   mov al, byte ptr [ebx + 0x72]
00454dfc  84c0                     test al, al
00454dfe  0f85a2000000             jne 0x454ea6
00454e04  668b4308                 mov ax, word ptr [ebx + 8]
00454e08  31d2                     xor edx, edx
00454e0a  6689c2                   mov dx, ax
00454e0d  89c8                     mov eax, ecx
00454e0f  e8a0defeff               call 0x442cb4 ; -> SetEnginCollision
00454e14  c6437201                 mov byte ptr [ebx + 0x72], 1
00454e18  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00454e1e  01e9                     add ecx, ebp
00454e20  31db                     xor ebx, ebx
00454e22  668b4108                 mov ax, word ptr [ecx + 8]
00454e26  8a19                     mov bl, byte ptr [ecx]
00454e28  89442424                 mov dword ptr [esp + 0x24], eax
00454e2c  81fbc8000000             cmp ebx, 0xc8
00454e32  745d                     je 0x454e91
00454e34  83fb04                   cmp ebx, 4
00454e37  7458                     je 0x454e91
00454e39  30e4                     xor ah, ah
00454e3b  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00454e41  0502000000               add eax, 2
00454e46  89442448                 mov dword ptr [esp + 0x48], eax
00454e4a  30e4                     xor ah, ah
00454e4c  8b542448                 mov edx, dword ptr [esp + 0x48]
00454e50  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00454e56  01d0                     add eax, edx
00454e58  31d2                     xor edx, edx
00454e5a  0fb76c2424               movzx ebp, word ptr [esp + 0x24]
00454e5f  6689c2                   mov dx, ax
00454e62  89e8                     mov eax, ebp
00454e64  e8e8190200               call 0x476851 ; -> DecouvreTerrain
00454e69  30e4                     xor ah, ah
00454e6b  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00454e71  89442448                 mov dword ptr [esp + 0x48], eax
00454e75  8b542448                 mov edx, dword ptr [esp + 0x48]
00454e79  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00454e7f  31db                     xor ebx, ebx
00454e81  01d0                     add eax, edx
00454e83  31d2                     xor edx, edx
00454e85  8a19                     mov bl, byte ptr [ecx]
00454e87  6689c2                   mov dx, ax
00454e8a  89e8                     mov eax, ebp
00454e8c  e8221e0200               call 0x476cb3 ; -> IllumineTerrain
00454e91  ba04000000               mov edx, 4
00454e96  31db                     xor ebx, ebx
00454e98  31c0                     xor eax, eax
00454e9a  668b5c2424               mov bx, word ptr [esp + 0x24]
00454e9f  8a01                     mov al, byte ptr [ecx]
00454ea1  e8e2540100               call 0x46a388 ; -> SetMiniMap
00454ea6  31c0                     xor eax, eax
00454ea8  31d2                     xor edx, edx
00454eaa  6689f8                   mov ax, di
00454ead  668b567e                 mov dx, word ptr [esi + 0x7e]
00454eb1  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
00454eba  e9f5010000               jmp 0x4550b4
00454ebf  31c0                     xor eax, eax
00454ec1  8a8682000000             mov al, byte ptr [esi + 0x82]
00454ec7  83f802                   cmp eax, 2
00454eca  0f8584060000             jne 0x455554
00454ed0  31c0                     xor eax, eax
00454ed2  668b8680000000           mov ax, word ptr [esi + 0x80]
00454ed9  e82d58fcff               call 0x41a70b ; -> BatimentEnDestruction
00454ede  84c0                     test al, al
00454ee0  7516                     jne 0x454ef8
00454ee2  31c0                     xor eax, eax
00454ee4  668b8680000000           mov ax, word ptr [esi + 0x80]
00454eeb  e89c51fcff               call 0x41a08c ; -> BatimentGetPlayer
00454ef0  3a06                     cmp al, byte ptr [esi]
00454ef2  0f845c060000             je 0x455554
00454ef8  31c9                     xor ecx, ecx
00454efa  6689f9                   mov cx, di
00454efd  89cd                     mov ebp, ecx
00454eff  c1e504                   shl ebp, 4
00454f02  01cd                     add ebp, ecx
00454f04  c1e502                   shl ebp, 2
00454f07  01cd                     add ebp, ecx
00454f09  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00454f0f  c1e502                   shl ebp, 2
00454f12  01eb                     add ebx, ebp
00454f14  8a4372                   mov al, byte ptr [ebx + 0x72]
00454f17  84c0                     test al, al
00454f19  758b                     jne 0x454ea6
00454f1b  668b4308                 mov ax, word ptr [ebx + 8]
00454f1f  31d2                     xor edx, edx
00454f21  6689c2                   mov dx, ax
00454f24  89c8                     mov eax, ecx
00454f26  e889ddfeff               call 0x442cb4 ; -> SetEnginCollision
00454f2b  c6437201                 mov byte ptr [ebx + 0x72], 1
00454f2f  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00454f35  01e9                     add ecx, ebp
00454f37  31db                     xor ebx, ebx
00454f39  668b4108                 mov ax, word ptr [ecx + 8]
00454f3d  8a19                     mov bl, byte ptr [ecx]
00454f3f  89442444                 mov dword ptr [esp + 0x44], eax
00454f43  81fbc8000000             cmp ebx, 0xc8
00454f49  744f                     je 0x454f9a
00454f4b  83fb04                   cmp ebx, 4
00454f4e  744a                     je 0x454f9a
00454f50  30e4                     xor ah, ah
00454f52  30f6                     xor dh, dh
00454f54  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00454f5a  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
00454f60  0502000000               add eax, 2
00454f65  01d0                     add eax, edx
00454f67  31d2                     xor edx, edx
00454f69  0fb76c2444               movzx ebp, word ptr [esp + 0x44]
00454f6e  6689c2                   mov dx, ax
00454f71  89e8                     mov eax, ebp
00454f73  e8d9180200               call 0x476851 ; -> DecouvreTerrain
00454f78  31db                     xor ebx, ebx
00454f7a  30f6                     xor dh, dh
00454f7c  30e4                     xor ah, ah
00454f7e  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
00454f84  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00454f8a  01d0                     add eax, edx
00454f8c  31d2                     xor edx, edx
00454f8e  8a19                     mov bl, byte ptr [ecx]
00454f90  6689c2                   mov dx, ax
00454f93  89e8                     mov eax, ebp
00454f95  e8191d0200               call 0x476cb3 ; -> IllumineTerrain
00454f9a  ba04000000               mov edx, 4
00454f9f  31db                     xor ebx, ebx
00454fa1  31c0                     xor eax, eax
00454fa3  668b5c2444               mov bx, word ptr [esp + 0x44]
00454fa8  e9f2feffff               jmp 0x454e9f
00454fad  31c0                     xor eax, eax
00454faf  8a8682000000             mov al, byte ptr [esi + 0x82]
00454fb5  83f802                   cmp eax, 2
00454fb8  0f8596050000             jne 0x455554
00454fbe  31c0                     xor eax, eax
00454fc0  668b8680000000           mov ax, word ptr [esi + 0x80]
00454fc7  e83f57fcff               call 0x41a70b ; -> BatimentEnDestruction
00454fcc  84c0                     test al, al
00454fce  7516                     jne 0x454fe6
00454fd0  31c0                     xor eax, eax
00454fd2  668b8680000000           mov ax, word ptr [esi + 0x80]
00454fd9  e8ae50fcff               call 0x41a08c ; -> BatimentGetPlayer
00454fde  3a06                     cmp al, byte ptr [esi]
00454fe0  0f846e050000             je 0x455554
00454fe6  31c9                     xor ecx, ecx
00454fe8  6689f9                   mov cx, di
00454feb  89cd                     mov ebp, ecx
00454fed  c1e504                   shl ebp, 4
00454ff0  01cd                     add ebp, ecx
00454ff2  c1e502                   shl ebp, 2
00454ff5  01cd                     add ebp, ecx
00454ff7  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00454ffd  c1e502                   shl ebp, 2
00455000  01eb                     add ebx, ebp
00455002  8a4372                   mov al, byte ptr [ebx + 0x72]
00455005  84c0                     test al, al
00455007  0f859c000000             jne 0x4550a9
0045500d  668b4308                 mov ax, word ptr [ebx + 8]
00455011  31d2                     xor edx, edx
00455013  6689c2                   mov dx, ax
00455016  89c8                     mov eax, ecx
00455018  e897dcfeff               call 0x442cb4 ; -> SetEnginCollision
0045501d  c6437201                 mov byte ptr [ebx + 0x72], 1
00455021  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00455027  01e9                     add ecx, ebp
00455029  31db                     xor ebx, ebx
0045502b  668b4108                 mov ax, word ptr [ecx + 8]
0045502f  8a19                     mov bl, byte ptr [ecx]
00455031  89442440                 mov dword ptr [esp + 0x40], eax
00455035  81fbc8000000             cmp ebx, 0xc8
0045503b  7457                     je 0x455094
0045503d  83fb04                   cmp ebx, 4
00455040  7452                     je 0x455094
00455042  30e4                     xor ah, ah
00455044  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0045504a  0502000000               add eax, 2
0045504f  89442448                 mov dword ptr [esp + 0x48], eax
00455053  30e4                     xor ah, ah
00455055  8b542448                 mov edx, dword ptr [esp + 0x48]
00455059  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0045505f  01d0                     add eax, edx
00455061  31d2                     xor edx, edx
00455063  0fb76c2440               movzx ebp, word ptr [esp + 0x40]
00455068  6689c2                   mov dx, ax
0045506b  89e8                     mov eax, ebp
0045506d  e8df170200               call 0x476851 ; -> DecouvreTerrain
00455072  31db                     xor ebx, ebx
00455074  30f6                     xor dh, dh
00455076  30e4                     xor ah, ah
00455078  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
0045507e  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455084  01d0                     add eax, edx
00455086  31d2                     xor edx, edx
00455088  8a19                     mov bl, byte ptr [ecx]
0045508a  6689c2                   mov dx, ax
0045508d  89e8                     mov eax, ebp
0045508f  e81f1c0200               call 0x476cb3 ; -> IllumineTerrain
00455094  ba04000000               mov edx, 4
00455099  31db                     xor ebx, ebx
0045509b  31c0                     xor eax, eax
0045509d  668b5c2440               mov bx, word ptr [esp + 0x40]
004550a2  8a01                     mov al, byte ptr [ecx]
004550a4  e8df520100               call 0x46a388 ; -> SetMiniMap
004550a9  31c0                     xor eax, eax
004550ab  31d2                     xor edx, edx
004550ad  6689f8                   mov ax, di
004550b0  668b567e                 mov dx, word ptr [esi + 0x7e]
004550b4  e81a07ffff               call 0x4457d3 ; -> SetDeplaceEngin
004550b9  c6868200000000           mov byte ptr [esi + 0x82], 0
004550c0  66c78680000000ffff       mov word ptr [esi + 0x80], 0xffff
004550c9  e9fffbffff               jmp 0x454ccd
004550ce  31c0                     xor eax, eax
004550d0  8a8682000000             mov al, byte ptr [esi + 0x82]
004550d6  83f802                   cmp eax, 2
004550d9  0f8575040000             jne 0x455554
004550df  31c0                     xor eax, eax
004550e1  668b8680000000           mov ax, word ptr [esi + 0x80]
004550e8  e81e56fcff               call 0x41a70b ; -> BatimentEnDestruction
004550ed  84c0                     test al, al
004550ef  7516                     jne 0x455107
004550f1  31c0                     xor eax, eax
004550f3  668b8680000000           mov ax, word ptr [esi + 0x80]
004550fa  e88d4ffcff               call 0x41a08c ; -> BatimentGetPlayer
004550ff  3a06                     cmp al, byte ptr [esi]
00455101  0f844d040000             je 0x455554
00455107  31d2                     xor edx, edx
00455109  6689fa                   mov dx, di
0045510c  89d0                     mov eax, edx
0045510e  c1e004                   shl eax, 4
00455111  01d0                     add eax, edx
00455113  c1e002                   shl eax, 2
00455116  01d0                     add eax, edx
00455118  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045511e  8a448272                 mov al, byte ptr [edx + eax*4 + 0x72]
00455122  84c0                     test al, al
00455124  7583                     jne 0x4550a9
00455126  31c0                     xor eax, eax
00455128  8a4601                   mov al, byte ptr [esi + 1]
0045512b  83f807                   cmp eax, 7
0045512e  750e                     jne 0x45513e
00455130  31c0                     xor eax, eax
00455132  668b86b2000000           mov ax, word ptr [esi + 0xb2]
00455139  e8a0030200               call 0x4754de ; -> MineEndWork
0045513e  31c9                     xor ecx, ecx
00455140  6689f9                   mov cx, di
00455143  89cd                     mov ebp, ecx
00455145  c1e504                   shl ebp, 4
00455148  01cd                     add ebp, ecx
0045514a  c1e502                   shl ebp, 2
0045514d  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455153  01cd                     add ebp, ecx
00455155  89ca                     mov edx, ecx
00455157  c1e502                   shl ebp, 2
0045515a  31ca                     xor edx, ecx
0045515c  668b442b08               mov ax, word ptr [ebx + ebp + 8]
00455161  6689c2                   mov dx, ax
00455164  89c8                     mov eax, ecx
00455166  e849dbfeff               call 0x442cb4 ; -> SetEnginCollision
0045516b  c6442b7201               mov byte ptr [ebx + ebp + 0x72], 1
00455170  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00455176  01e9                     add ecx, ebp
00455178  31db                     xor ebx, ebx
0045517a  668b4108                 mov ax, word ptr [ecx + 8]
0045517e  8a19                     mov bl, byte ptr [ecx]
00455180  89442430                 mov dword ptr [esp + 0x30], eax
00455184  81fbc8000000             cmp ebx, 0xc8
0045518a  7457                     je 0x4551e3
0045518c  83fb04                   cmp ebx, 4
0045518f  7452                     je 0x4551e3
00455191  30e4                     xor ah, ah
00455193  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455199  0502000000               add eax, 2
0045519e  89442448                 mov dword ptr [esp + 0x48], eax
004551a2  30e4                     xor ah, ah
004551a4  8b542448                 mov edx, dword ptr [esp + 0x48]
004551a8  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
004551ae  01d0                     add eax, edx
004551b0  31d2                     xor edx, edx
004551b2  0fb76c2430               movzx ebp, word ptr [esp + 0x30]
004551b7  6689c2                   mov dx, ax
004551ba  89e8                     mov eax, ebp
004551bc  e890160200               call 0x476851 ; -> DecouvreTerrain
004551c1  31db                     xor ebx, ebx
004551c3  30f6                     xor dh, dh
004551c5  30e4                     xor ah, ah
004551c7  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
004551cd  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
004551d3  01d0                     add eax, edx
004551d5  31d2                     xor edx, edx
004551d7  8a19                     mov bl, byte ptr [ecx]
004551d9  6689c2                   mov dx, ax
004551dc  89e8                     mov eax, ebp
004551de  e8d01a0200               call 0x476cb3 ; -> IllumineTerrain
004551e3  ba04000000               mov edx, 4
004551e8  31db                     xor ebx, ebx
004551ea  31c0                     xor eax, eax
004551ec  668b5c2430               mov bx, word ptr [esp + 0x30]
004551f1  e9acfeffff               jmp 0x4550a2
004551f6  31c0                     xor eax, eax
004551f8  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004551ff  e80755fcff               call 0x41a70b ; -> BatimentEnDestruction
00455204  84c0                     test al, al
00455206  0f858bfbffff             jne 0x454d97
0045520c  31c0                     xor eax, eax
0045520e  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455215  e8724efcff               call 0x41a08c ; -> BatimentGetPlayer
0045521a  25ff000000               and eax, 0xff
0045521f  3dc8000000               cmp eax, 0xc8
00455224  0f846dfbffff             je 0x454d97
0045522a  31c0                     xor eax, eax
0045522c  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455233  e8544efcff               call 0x41a08c ; -> BatimentGetPlayer
00455238  3a06                     cmp al, byte ptr [esi]
0045523a  0f8514030000             jne 0x455554
00455240  e952fbffff               jmp 0x454d97
00455245  31c0                     xor eax, eax
00455247  668b86b8000000           mov ax, word ptr [esi + 0xb8]
0045524e  3dffff0000               cmp eax, 0xffff
00455253  7427                     je 0x45527c
00455255  e8b154fcff               call 0x41a70b ; -> BatimentEnDestruction
0045525a  84c0                     test al, al
0045525c  751e                     jne 0x45527c
0045525e  31c0                     xor eax, eax
00455260  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455267  e8204efcff               call 0x41a08c ; -> BatimentGetPlayer
0045526c  25ff000000               and eax, 0xff
00455271  3dc8000000               cmp eax, 0xc8
00455276  0f85d8020000             jne 0x455554
0045527c  31c9                     xor ecx, ecx
0045527e  6689f9                   mov cx, di
00455281  89c8                     mov eax, ecx
00455283  c1e004                   shl eax, 4
00455286  01c8                     add eax, ecx
00455288  c1e002                   shl eax, 2
0045528b  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455291  01c8                     add eax, ecx
00455293  8a0482                   mov al, byte ptr [edx + eax*4]
00455296  25ff000000               and eax, 0xff
0045529b  e877850100               call 0x46d817 ; -> PlayerGetType
004552a0  25ff000000               and eax, 0xff
004552a5  83f802                   cmp eax, 2
004552a8  7513                     jne 0x4552bd
004552aa  ba4a000000               mov edx, 0x4a
004552af  89c8                     mov eax, ecx
004552b1  31db                     xor ebx, ebx
004552b3  e810d70200               call 0x4829c8 ; -> iagUnitSendMessage
004552b8  e997020000               jmp 0x455554
004552bd  31d2                     xor edx, edx
004552bf  89c8                     mov eax, ecx
004552c1  668b567e                 mov dx, word ptr [esi + 0x7e]
004552c5  e80905ffff               call 0x4457d3 ; -> SetDeplaceEngin
004552ca  66c786b8000000ffff       mov word ptr [esi + 0xb8], 0xffff
004552d3  e97c020000               jmp 0x455554
004552d8  31c0                     xor eax, eax
004552da  668b86b8000000           mov ax, word ptr [esi + 0xb8]
004552e1  3dffff0000               cmp eax, 0xffff
004552e6  0f8470000000             je 0x45535c
004552ec  31d2                     xor edx, edx
004552ee  6689c2                   mov dx, ax
004552f1  89d0                     mov eax, edx
004552f3  c1e004                   shl eax, 4
004552f6  01d0                     add eax, edx
004552f8  c1e002                   shl eax, 2
004552fb  01d0                     add eax, edx
004552fd  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455303  c1e002                   shl eax, 2
00455306  01c2                     add edx, eax
00455308  31c0                     xor eax, eax
0045530a  8a4202                   mov al, byte ptr [edx + 2]
0045530d  85c0                     test eax, eax
0045530f  7409                     je 0x45531a
00455311  83f804                   cmp eax, 4
00455314  7404                     je 0x45531a
00455316  b001                     mov al, 1
00455318  eb02                     jmp 0x45531c
0045531a  30c0                     xor al, al
0045531c  84c0                     test al, al
0045531e  743c                     je 0x45535c
00455320  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455327  31d2                     xor edx, edx
00455329  6689c2                   mov dx, ax
0045532c  89d0                     mov eax, edx
0045532e  c1e004                   shl eax, 4
00455331  01d0                     add eax, edx
00455333  c1e002                   shl eax, 2
00455336  01d0                     add eax, edx
00455338  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045533e  c1e002                   shl eax, 2
00455341  01c2                     add edx, eax
00455343  8a02                     mov al, byte ptr [edx]
00455345  25ff000000               and eax, 0xff
0045534a  3dc8000000               cmp eax, 0xc8
0045534f  740b                     je 0x45535c
00455351  8a4272                   mov al, byte ptr [edx + 0x72]
00455354  84c0                     test al, al
00455356  0f85f8010000             jne 0x455554
0045535c  31c9                     xor ecx, ecx
0045535e  6689f9                   mov cx, di
00455361  89c8                     mov eax, ecx
00455363  c1e004                   shl eax, 4
00455366  01c8                     add eax, ecx
00455368  c1e002                   shl eax, 2
0045536b  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455371  01c8                     add eax, ecx
00455373  8a0482                   mov al, byte ptr [edx + eax*4]
00455376  25ff000000               and eax, 0xff
0045537b  e897840100               call 0x46d817 ; -> PlayerGetType
00455380  25ff000000               and eax, 0xff
00455385  83f802                   cmp eax, 2
00455388  0f841cffffff             je 0x4552aa
0045538e  e92affffff               jmp 0x4552bd
00455393  8a86b7000000             mov al, byte ptr [esi + 0xb7]
00455399  3c01                     cmp al, 1
0045539b  0f82b3010000             jb 0x455554
004553a1  0f8631ffffff             jbe 0x4552d8
004553a7  3c03                     cmp al, 3
004553a9  0f8496feffff             je 0x455245
004553af  e9a0010000               jmp 0x455554
004553b4  31c0                     xor eax, eax
004553b6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004553bd  3dffff0000               cmp eax, 0xffff
004553c2  7465                     je 0x455429
004553c4  31c0                     xor eax, eax
004553c6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004553cd  e83953fcff               call 0x41a70b ; -> BatimentEnDestruction
004553d2  84c0                     test al, al
004553d4  0f85bdf9ffff             jne 0x454d97
004553da  31c0                     xor eax, eax
004553dc  8a4601                   mov al, byte ptr [esi + 1]
004553df  83f80a                   cmp eax, 0xa
004553e2  0f8424feffff             je 0x45520c
004553e8  31c0                     xor eax, eax
004553ea  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004553f1  e8964cfcff               call 0x41a08c ; -> BatimentGetPlayer
004553f6  3a06                     cmp al, byte ptr [esi]
004553f8  0f8456010000             je 0x455554
004553fe  31c0                     xor eax, eax
00455400  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455407  e8804cfcff               call 0x41a08c ; -> BatimentGetPlayer
0045540c  25ff000000               and eax, 0xff
00455411  3dc8000000               cmp eax, 0xc8
00455416  0f857bf9ffff             jne 0x454d97
0045541c  31c0                     xor eax, eax
0045541e  8a4601                   mov al, byte ptr [esi + 1]
00455421  83f809                   cmp eax, 9
00455424  e968f9ffff               jmp 0x454d91
00455429  31c0                     xor eax, eax
0045542b  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455432  3dffff0000               cmp eax, 0xffff
00455437  0f8417010000             je 0x455554
0045543d  31d2                     xor edx, edx
0045543f  6689c2                   mov dx, ax
00455442  89c3                     mov ebx, eax
00455444  89d0                     mov eax, edx
00455446  c1e004                   shl eax, 4
00455449  01d0                     add eax, edx
0045544b  c1e002                   shl eax, 2
0045544e  01c2                     add edx, eax
00455450  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00455455  c1e202                   shl edx, 2
00455458  8a440202                 mov al, byte ptr [edx + eax + 2]
0045545c  25ff000000               and eax, 0xff
00455461  7429                     je 0x45548c
00455463  31d2                     xor edx, edx
00455465  6689da                   mov dx, bx
00455468  89d0                     mov eax, edx
0045546a  c1e004                   shl eax, 4
0045546d  01d0                     add eax, edx
0045546f  c1e002                   shl eax, 2
00455472  01d0                     add eax, edx
00455474  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045547a  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
0045547e  25ff000000               and eax, 0xff
00455483  83f804                   cmp eax, 4
00455486  7404                     je 0x45548c
00455488  b001                     mov al, 1
0045548a  eb02                     jmp 0x45548e
0045548c  30c0                     xor al, al
0045548e  84c0                     test al, al
00455490  750c                     jne 0x45549e
00455492  31c0                     xor eax, eax
00455494  31d2                     xor edx, edx
00455496  6689f8                   mov ax, di
00455499  e919130000               jmp 0x4567b7
0045549e  668b86b8000000           mov ax, word ptr [esi + 0xb8]
004554a5  31d2                     xor edx, edx
004554a7  6689c2                   mov dx, ax
004554aa  89d0                     mov eax, edx
004554ac  c1e004                   shl eax, 4
004554af  01d0                     add eax, edx
004554b1  c1e002                   shl eax, 2
004554b4  01d0                     add eax, edx
004554b6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004554bc  8a1e                     mov bl, byte ptr [esi]
004554be  8a0482                   mov al, byte ptr [edx + eax*4]
004554c1  38d8                     cmp al, bl
004554c3  0f848b000000             je 0x455554
004554c9  25ff000000               and eax, 0xff
004554ce  3dc8000000               cmp eax, 0xc8
004554d3  0f847b000000             je 0x455554
004554d9  ebb7                     jmp 0x455492
004554db  668b96a0000000           mov dx, word ptr [esi + 0xa0]
004554e2  89d0                     mov eax, edx
004554e4  6683fa0f                 cmp dx, 0xf
004554e8  723c                     jb 0x455526
004554ea  0f86e5f7ffff             jbe 0x454cd5
004554f0  6683fa15                 cmp dx, 0x15
004554f4  7218                     jb 0x45550e
004554f6  0f8697f7ffff             jbe 0x454c93
004554fc  6683fa17                 cmp dx, 0x17
00455500  7252                     jb 0x455554
00455502  0f86eefcffff             jbe 0x4551f6
00455508  6683fa18                 cmp dx, 0x18
0045550c  eb40                     jmp 0x45554e
0045550e  6683fa12                 cmp dx, 0x12
00455512  7240                     jb 0x455554
00455514  0f8693faffff             jbe 0x454fad
0045551a  6683fa14                 cmp dx, 0x14
0045551e  0f8491f8ffff             je 0x454db5
00455524  eb2e                     jmp 0x455554
00455526  6683fa05                 cmp dx, 5
0045552a  721e                     jb 0x45554a
0045552c  0f869cfbffff             jbe 0x4550ce
00455532  6683fa0b                 cmp dx, 0xb
00455536  721c                     jb 0x455554
00455538  0f8655f7ffff             jbe 0x454c93
0045553e  6683fa0d                 cmp dx, 0xd
00455542  0f846cfeffff             je 0x4553b4
00455548  eb0a                     jmp 0x455554
0045554a  6683fa01                 cmp dx, 1
0045554e  0f843ffeffff             je 0x455393
00455554  31c0                     xor eax, eax
00455556  668b86c2000000           mov ax, word ptr [esi + 0xc2]
0045555d  3dffff0000               cmp eax, 0xffff
00455562  750a                     jne 0x45556e
00455564  668b4608                 mov ax, word ptr [esi + 8]
00455568  663b467e                 cmp ax, word ptr [esi + 0x7e]
0045556c  7539                     jne 0x4555a7
0045556e  31c0                     xor eax, eax
00455570  668b86c2000000           mov ax, word ptr [esi + 0xc2]
00455577  3dffff0000               cmp eax, 0xffff
0045557c  740f                     je 0x45558d
0045557e  31d2                     xor edx, edx
00455580  668b5608                 mov dx, word ptr [esi + 8]
00455584  e896e2fcff               call 0x42381f ; -> BatimentAdjacent
00455589  84c0                     test al, al
0045558b  741a                     je 0x4555a7
0045558d  8b8683000000             mov eax, dword ptr [esi + 0x83]
00455593  c1f818                   sar eax, 0x18
00455596  85c0                     test eax, eax
00455598  750d                     jne 0x4555a7
0045559a  8b8684000000             mov eax, dword ptr [esi + 0x84]
004555a0  c1f818                   sar eax, 0x18
004555a3  85c0                     test eax, eax
004555a5  740f                     je 0x4555b6
004555a7  31c0                     xor eax, eax
004555a9  6689f8                   mov ax, di
004555ac  e85b3dffff               call 0x44930c ; -> DeplaceEngin
004555b1  e917f7ffff               jmp 0x454ccd
004555b6  668b86c2000000           mov ax, word ptr [esi + 0xc2]
004555bd  3dffff0000               cmp eax, 0xffff
004555c2  0f85ac000000             jne 0x455674
004555c8  31c0                     xor eax, eax
004555ca  668b467e                 mov ax, word ptr [esi + 0x7e]
004555ce  e8650a0200               call 0x476038 ; -> TerrainGetSacType
004555d3  25ff000000               and eax, 0xff
004555d8  83f801                   cmp eax, 1
004555db  0f8593000000             jne 0x455674
004555e1  31c0                     xor eax, eax
004555e3  668b467e                 mov ax, word ptr [esi + 0x7e]
004555e7  31c9                     xor ecx, ecx
004555e9  e874100200               call 0x476662 ; -> TerrainRetireMatiere
004555ee  668b4676                 mov ax, word ptr [esi + 0x76]
004555f2  6689f9                   mov cx, di
004555f5  66894604                 mov word ptr [esi + 4], ax
004555f9  89c8                     mov eax, ecx
004555fb  c1e004                   shl eax, 4
004555fe  01c8                     add eax, ecx
00455600  89ca                     mov edx, ecx
00455602  c1e002                   shl eax, 2
00455605  66c746740000             mov word ptr [esi + 0x74], 0
0045560b  01c8                     add eax, ecx
0045560d  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455613  c1e002                   shl eax, 2
00455616  31ca                     xor edx, ecx
00455618  01c3                     add ebx, eax
0045561a  31c0                     xor eax, eax
0045561c  8a1541805000             mov dl, byte ptr [0x508041]
00455622  668b4308                 mov ax, word ptr [ebx + 8]
00455626  e8c5100200               call 0x4766f0 ; -> TerrainEstDecouvert
0045562b  84c0                     test al, al
0045562d  7436                     je 0x455665
0045562f  89c8                     mov eax, ecx
00455631  e827b6feff               call 0x440c5d ; -> EnginGetVolume
00455636  8bab04010000             mov ebp, dword ptr [ebx + 0x104]
0045563c  c683f900000000           mov byte ptr [ebx + 0xf9], 0
00455643  83fdff                   cmp ebp, -1
00455646  751d                     jne 0x455665
00455648  50                       push eax
00455649  31d2                     xor edx, edx
0045564b  31c9                     xor ecx, ecx
0045564d  8a5301                   mov dl, byte ptr [ebx + 1]
00455650  8d8304010000             lea eax, [ebx + 0x104]
00455656  c1e210                   shl edx, 0x10
00455659  89c3                     mov ebx, eax
0045565b  b850000000               mov eax, 0x50
00455660  e814540300               call 0x48aa79 ; -> PlaySnd_PostSound
00455665  31c0                     xor eax, eax
00455667  6689f8                   mov ax, di
0045566a  e8f0daffff               call 0x45315f ; -> EnginRestaureEtat
0045566f  e959f6ffff               jmp 0x454ccd
00455674  31c0                     xor eax, eax
00455676  668b86c2000000           mov ax, word ptr [esi + 0xc2]
0045567d  3dffff0000               cmp eax, 0xffff
00455682  0f84b5000000             je 0x45573d
00455688  e8674efcff               call 0x41a4f4 ; -> BatimentGetType
0045568d  25ff000000               and eax, 0xff
00455692  83f803                   cmp eax, 3
00455695  0f85a2000000             jne 0x45573d
0045569b  31c0                     xor eax, eax
0045569d  668b86c2000000           mov ax, word ptr [esi + 0xc2]
004556a4  e8e349fcff               call 0x41a08c ; -> BatimentGetPlayer
004556a9  3a06                     cmp al, byte ptr [esi]
004556ab  0f858c000000             jne 0x45573d
004556b1  31c0                     xor eax, eax
004556b3  31c9                     xor ecx, ecx
004556b5  8a06                     mov al, byte ptr [esi]
004556b7  31db                     xor ebx, ebx
004556b9  50                       push eax
004556ba  31d2                     xor edx, edx
004556bc  b801000000               mov eax, 1
004556c1  e81f200100               call 0x4676e5 ; -> TestRessource
004556c6  84c0                     test al, al
004556c8  7473                     je 0x45573d
004556ca  ba01000000               mov edx, 1
004556cf  31db                     xor ebx, ebx
004556d1  89d0                     mov eax, edx
004556d3  8a1e                     mov bl, byte ptr [esi]
004556d5  31c9                     xor ecx, ecx
004556d7  e8e1defcff               call 0x4235bd ; -> BatimentEnleveMatiere
004556dc  668b4676                 mov ax, word ptr [esi + 0x76]
004556e0  6689f9                   mov cx, di
004556e3  66894604                 mov word ptr [esi + 4], ax
004556e7  89c8                     mov eax, ecx
004556e9  c1e004                   shl eax, 4
004556ec  01c8                     add eax, ecx
004556ee  89ca                     mov edx, ecx
004556f0  c1e002                   shl eax, 2
004556f3  66c746740000             mov word ptr [esi + 0x74], 0
004556f9  01c8                     add eax, ecx
004556fb  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455701  c1e002                   shl eax, 2
00455704  31ca                     xor edx, ecx
00455706  01c3                     add ebx, eax
00455708  31c0                     xor eax, eax
0045570a  8a1541805000             mov dl, byte ptr [0x508041]
00455710  668b4308                 mov ax, word ptr [ebx + 8]
00455714  e8d70f0200               call 0x4766f0 ; -> TerrainEstDecouvert
00455719  84c0                     test al, al
0045571b  0f8444ffffff             je 0x455665
00455721  89c8                     mov eax, ecx
00455723  e835b5feff               call 0x440c5d ; -> EnginGetVolume
00455728  8bb304010000             mov esi, dword ptr [ebx + 0x104]
0045572e  c683f900000000           mov byte ptr [ebx + 0xf9], 0
00455735  83feff                   cmp esi, -1
00455738  e909ffffff               jmp 0x455646
0045573d  b943000000               mov ecx, 0x43
00455742  0fb7ef                   movzx ebp, di
00455745  31d2                     xor edx, edx
00455747  31c0                     xor eax, eax
00455749  55                       push ebp
0045574a  89cb                     mov ebx, ecx
0045574c  8a96bb000000             mov dl, byte ptr [esi + 0xbb]
00455752  668b467c                 mov ax, word ptr [esi + 0x7c]
00455756  e819240200               call 0x477b74 ; -> ChercheVegetLibre
0045575b  31c9                     xor ecx, ecx
0045575d  89c3                     mov ebx, eax
0045575f  6689c1                   mov cx, ax
00455762  89e8                     mov eax, ebp
00455764  c1e004                   shl eax, 4
00455767  01e8                     add eax, ebp
00455769  c1e002                   shl eax, 2
0045576c  01e8                     add eax, ebp
0045576e  c1e002                   shl eax, 2
00455771  81f9ffff0000             cmp ecx, 0xffff
00455777  0f84ba000000             je 0x455837
0045577d  c6460213                 mov byte ptr [esi + 2], 0x13
00455781  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455787  01d0                     add eax, edx
00455789  6689587e                 mov word ptr [eax + 0x7e], bx
0045578d  663b3d04634900           cmp di, word ptr [0x496304]
00455794  7522                     jne 0x4557b8
00455796  beffff0000               mov esi, 0xffff
0045579b  30db                     xor bl, bl
0045579d  31d2                     xor edx, edx
0045579f  881d360f4e00             mov byte ptr [0x4e0f36], bl
004557a5  881d370f4e00             mov byte ptr [0x4e0f37], bl
004557ab  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
004557b1  66893504634900           mov word ptr [0x496304], si
004557b8  31c9                     xor ecx, ecx
004557ba  6689f9                   mov cx, di
004557bd  c6808800000000           mov byte ptr [eax + 0x88], 0
004557c4  89c8                     mov eax, ecx
004557c6  c1e004                   shl eax, 4
004557c9  01c8                     add eax, ecx
004557cb  c1e002                   shl eax, 2
004557ce  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
004557d4  01c8                     add eax, ecx
004557d6  89ca                     mov edx, ecx
004557d8  c1e002                   shl eax, 2
004557db  31ca                     xor edx, ecx
004557dd  01c3                     add ebx, eax
004557df  31c0                     xor eax, eax
004557e1  8a1541805000             mov dl, byte ptr [0x508041]
004557e7  668b4308                 mov ax, word ptr [ebx + 8]
004557eb  e8000f0200               call 0x4766f0 ; -> TerrainEstDecouvert
004557f0  84c0                     test al, al
004557f2  0f84d5f4ffff             je 0x454ccd
004557f8  89c8                     mov eax, ecx
004557fa  e85eb4feff               call 0x440c5d ; -> EnginGetVolume
004557ff  8b8b04010000             mov ecx, dword ptr [ebx + 0x104]
00455805  c683f900000000           mov byte ptr [ebx + 0xf9], 0
0045580c  83f9ff                   cmp ecx, -1
0045580f  0f85b8f4ffff             jne 0x454ccd
00455815  50                       push eax
00455816  31d2                     xor edx, edx
00455818  31c9                     xor ecx, ecx
0045581a  8a5301                   mov dl, byte ptr [ebx + 1]
0045581d  8d8304010000             lea eax, [ebx + 0x104]
00455823  c1e210                   shl edx, 0x10
00455826  89c3                     mov ebx, eax
00455828  b850000000               mov eax, 0x50
0045582d  e847520300               call 0x48aa79 ; -> PlaySnd_PostSound
00455832  e996f4ffff               jmp 0x454ccd
00455837  8a16                     mov dl, byte ptr [esi]
00455839  3a1541805000             cmp dl, byte ptr [0x508041]
0045583f  0f8520feffff             jne 0x455665
00455845  31d2                     xor edx, edx
00455847  668b5674                 mov dx, word ptr [esi + 0x74]
0045584b  83fa01                   cmp edx, 1
0045584e  0f8511feffff             jne 0x455665
00455854  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0045585a  31d2                     xor edx, edx
0045585c  01c3                     add ebx, eax
0045585e  31c0                     xor eax, eax
00455860  8a1541805000             mov dl, byte ptr [0x508041]
00455866  668b4308                 mov ax, word ptr [ebx + 8]
0045586a  e8810e0200               call 0x4766f0 ; -> TerrainEstDecouvert
0045586f  84c0                     test al, al
00455871  0f84eefdffff             je 0x455665
00455877  89e8                     mov eax, ebp
00455879  e8dfb3feff               call 0x440c5d ; -> EnginGetVolume
0045587e  8bab04010000             mov ebp, dword ptr [ebx + 0x104]
00455884  c683f900000000           mov byte ptr [ebx + 0xf9], 0
0045588b  83fdff                   cmp ebp, -1
0045588e  0f85d1fdffff             jne 0x455665
00455894  50                       push eax
00455895  31d2                     xor edx, edx
00455897  31c9                     xor ecx, ecx
00455899  8a5301                   mov dl, byte ptr [ebx + 1]
0045589c  8d8304010000             lea eax, [ebx + 0x104]
004558a2  c1e210                   shl edx, 0x10
004558a5  89c3                     mov ebx, eax
004558a7  b850000000               mov eax, 0x50
004558ac  80ce0c                   or dh, 0xc
004558af  e9acfdffff               jmp 0x455660
004558b4  31c0                     xor eax, eax
004558b6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004558bd  3dffff0000               cmp eax, 0xffff
004558c2  0f8405f4ffff             je 0x454ccd
004558c8  e83e4efcff               call 0x41a70b ; -> BatimentEnDestruction
004558cd  84c0                     test al, al
004558cf  0f85e8f3ffff             jne 0x454cbd
004558d5  31c0                     xor eax, eax
004558d7  6689f8                   mov ax, di
004558da  e8513cffff               call 0x449530 ; -> CalculGareBatiment
004558df  e9e9f3ffff               jmp 0x454ccd
004558e4  31c0                     xor eax, eax
004558e6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004558ed  3dffff0000               cmp eax, 0xffff
004558f2  0f84ba000000             je 0x4559b2
004558f8  31c0                     xor eax, eax
004558fa  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455901  e8054efcff               call 0x41a70b ; -> BatimentEnDestruction
00455906  84c0                     test al, al
00455908  0f8589f4ffff             jne 0x454d97
0045590e  31c0                     xor eax, eax
00455910  8a4601                   mov al, byte ptr [esi + 1]
00455913  83f80a                   cmp eax, 0xa
00455916  754d                     jne 0x455965
00455918  31c0                     xor eax, eax
0045591a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455921  e86647fcff               call 0x41a08c ; -> BatimentGetPlayer
00455926  25ff000000               and eax, 0xff
0045592b  3dc8000000               cmp eax, 0xc8
00455930  0f8461f4ffff             je 0x454d97
00455936  31c0                     xor eax, eax
00455938  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045593f  e84847fcff               call 0x41a08c ; -> BatimentGetPlayer
00455944  3a06                     cmp al, byte ptr [esi]
00455946  755b                     jne 0x4559a3
00455948  31c0                     xor eax, eax
0045594a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455951  e89e4bfcff               call 0x41a4f4 ; -> BatimentGetType
00455956  25ff000000               and eax, 0xff
0045595b  83f810                   cmp eax, 0x10
0045595e  7543                     jne 0x4559a3
00455960  e932f4ffff               jmp 0x454d97
00455965  31c0                     xor eax, eax
00455967  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045596e  e81947fcff               call 0x41a08c ; -> BatimentGetPlayer
00455973  3a06                     cmp al, byte ptr [esi]
00455975  742c                     je 0x4559a3
00455977  31c0                     xor eax, eax
00455979  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455980  e80747fcff               call 0x41a08c ; -> BatimentGetPlayer
00455985  25ff000000               and eax, 0xff
0045598a  3dc8000000               cmp eax, 0xc8
0045598f  0f8502f4ffff             jne 0x454d97
00455995  31c0                     xor eax, eax
00455997  8a4601                   mov al, byte ptr [esi + 1]
0045599a  83f809                   cmp eax, 9
0045599d  0f85f4f3ffff             jne 0x454d97
004559a3  31c0                     xor eax, eax
004559a5  6689f8                   mov ax, di
004559a8  e8693dffff               call 0x449716 ; -> CalculEntreBatiment
004559ad  e91bf3ffff               jmp 0x454ccd
004559b2  31c0                     xor eax, eax
004559b4  668b86b8000000           mov ax, word ptr [esi + 0xb8]
004559bb  3dffff0000               cmp eax, 0xffff
004559c0  0f8407f3ffff             je 0x454ccd
004559c6  31d2                     xor edx, edx
004559c8  6689c2                   mov dx, ax
004559cb  89c3                     mov ebx, eax
004559cd  89d0                     mov eax, edx
004559cf  c1e004                   shl eax, 4
004559d2  01d0                     add eax, edx
004559d4  c1e002                   shl eax, 2
004559d7  01d0                     add eax, edx
004559d9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004559df  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
004559e3  25ff000000               and eax, 0xff
004559e8  7429                     je 0x455a13
004559ea  31d2                     xor edx, edx
004559ec  6689da                   mov dx, bx
004559ef  89d0                     mov eax, edx
004559f1  c1e004                   shl eax, 4
004559f4  01d0                     add eax, edx
004559f6  c1e002                   shl eax, 2
004559f9  01d0                     add eax, edx
004559fb  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455a01  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00455a05  25ff000000               and eax, 0xff
00455a0a  83f804                   cmp eax, 4
00455a0d  7404                     je 0x455a13
00455a0f  b001                     mov al, 1
00455a11  eb02                     jmp 0x455a15
00455a13  30c0                     xor al, al
00455a15  84c0                     test al, al
00455a17  0f8475faffff             je 0x455492
00455a1d  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455a24  31d2                     xor edx, edx
00455a26  6689c2                   mov dx, ax
00455a29  89d0                     mov eax, edx
00455a2b  c1e004                   shl eax, 4
00455a2e  01d0                     add eax, edx
00455a30  c1e002                   shl eax, 2
00455a33  01d0                     add eax, edx
00455a35  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455a3b  8a0482                   mov al, byte ptr [edx + eax*4]
00455a3e  3a06                     cmp al, byte ptr [esi]
00455a40  7410                     je 0x455a52
00455a42  25ff000000               and eax, 0xff
00455a47  3dc8000000               cmp eax, 0xc8
00455a4c  0f8540faffff             jne 0x455492
00455a52  31c0                     xor eax, eax
00455a54  6689f8                   mov ax, di
00455a57  e89148ffff               call 0x44a2ed ; -> CalculEntreEngin
00455a5c  e96cf2ffff               jmp 0x454ccd
00455a61  8a8690000000             mov al, byte ptr [esi + 0x90]
00455a67  3a8691000000             cmp al, byte ptr [esi + 0x91]
00455a6d  740f                     je 0x455a7e
00455a6f  31c0                     xor eax, eax
00455a71  6689f8                   mov ax, di
00455a74  e8202bffff               call 0x448599 ; -> RotateEngin
00455a79  e94ff2ffff               jmp 0x454ccd
00455a7e  31d2                     xor edx, edx
00455a80  6689fa                   mov dx, di
00455a83  89d0                     mov eax, edx
00455a85  c1e004                   shl eax, 4
00455a88  01d0                     add eax, edx
00455a8a  c1e002                   shl eax, 2
00455a8d  b107                     mov cl, 7
00455a8f  01c2                     add edx, eax
00455a91  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00455a96  c1e202                   shl edx, 2
00455a99  89fb                     mov ebx, edi
00455a9b  8a440202                 mov al, byte ptr [edx + eax + 2]
00455a9f  25ff000000               and eax, 0xff
00455aa4  742b                     je 0x455ad1
00455aa6  31d2                     xor edx, edx
00455aa8  6689fa                   mov dx, di
00455aab  89d0                     mov eax, edx
00455aad  c1e004                   shl eax, 4
00455ab0  01d0                     add eax, edx
00455ab2  c1e002                   shl eax, 2
00455ab5  01c2                     add edx, eax
00455ab7  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00455abc  c1e202                   shl edx, 2
00455abf  8a440202                 mov al, byte ptr [edx + eax + 2]
00455ac3  25ff000000               and eax, 0xff
00455ac8  83f804                   cmp eax, 4
00455acb  7404                     je 0x455ad1
00455acd  b001                     mov al, 1
00455acf  eb02                     jmp 0x455ad3
00455ad1  30c0                     xor al, al
00455ad3  84c0                     test al, al
00455ad5  0f84f2f1ffff             je 0x454ccd
00455adb  31d2                     xor edx, edx
00455add  6689fa                   mov dx, di
00455ae0  89d0                     mov eax, edx
00455ae2  c1e004                   shl eax, 4
00455ae5  01d0                     add eax, edx
00455ae7  c1e002                   shl eax, 2
00455aea  01d0                     add eax, edx
00455aec  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455af2  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
00455af6  663b3d04634900           cmp di, word ptr [0x496304]
00455afd  0f85caf1ffff             jne 0x454ccd
00455b03  30c0                     xor al, al
00455b05  31db                     xor ebx, ebx
00455b07  a2360f4e00               mov byte ptr [0x4e0f36], al
00455b0c  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00455b12  bbffff0000               mov ebx, 0xffff
00455b17  a2370f4e00               mov byte ptr [0x4e0f37], al
00455b1c  66891d04634900           mov word ptr [0x496304], bx
00455b23  e9a5f1ffff               jmp 0x454ccd
00455b28  31c0                     xor eax, eax
00455b2a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455b31  e8d54bfcff               call 0x41a70b ; -> BatimentEnDestruction
00455b36  84c0                     test al, al
00455b38  7516                     jne 0x455b50
00455b3a  31c0                     xor eax, eax
00455b3c  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455b43  e84445fcff               call 0x41a08c ; -> BatimentGetPlayer
00455b48  3a06                     cmp al, byte ptr [esi]
00455b4a  0f84c7000000             je 0x455c17
00455b50  31c9                     xor ecx, ecx
00455b52  6689f9                   mov cx, di
00455b55  89cd                     mov ebp, ecx
00455b57  c1e504                   shl ebp, 4
00455b5a  01cd                     add ebp, ecx
00455b5c  c1e502                   shl ebp, 2
00455b5f  01cd                     add ebp, ecx
00455b61  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455b67  c1e502                   shl ebp, 2
00455b6a  01eb                     add ebx, ebp
00455b6c  8a4372                   mov al, byte ptr [ebx + 0x72]
00455b6f  84c0                     test al, al
00455b71  0f852ff3ffff             jne 0x454ea6
00455b77  668b4308                 mov ax, word ptr [ebx + 8]
00455b7b  31d2                     xor edx, edx
00455b7d  6689c2                   mov dx, ax
00455b80  89c8                     mov eax, ecx
00455b82  e82dd1feff               call 0x442cb4 ; -> SetEnginCollision
00455b87  c6437201                 mov byte ptr [ebx + 0x72], 1
00455b8b  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00455b91  01e9                     add ecx, ebp
00455b93  31db                     xor ebx, ebx
00455b95  668b4108                 mov ax, word ptr [ecx + 8]
00455b99  8a19                     mov bl, byte ptr [ecx]
00455b9b  8944243c                 mov dword ptr [esp + 0x3c], eax
00455b9f  81fbc8000000             cmp ebx, 0xc8
00455ba5  745d                     je 0x455c04
00455ba7  83fb04                   cmp ebx, 4
00455baa  7458                     je 0x455c04
00455bac  30e4                     xor ah, ah
00455bae  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455bb4  0502000000               add eax, 2
00455bb9  89442448                 mov dword ptr [esp + 0x48], eax
00455bbd  30e4                     xor ah, ah
00455bbf  8b542448                 mov edx, dword ptr [esp + 0x48]
00455bc3  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455bc9  01d0                     add eax, edx
00455bcb  31d2                     xor edx, edx
00455bcd  0fb76c243c               movzx ebp, word ptr [esp + 0x3c]
00455bd2  6689c2                   mov dx, ax
00455bd5  89e8                     mov eax, ebp
00455bd7  e8750c0200               call 0x476851 ; -> DecouvreTerrain
00455bdc  30e4                     xor ah, ah
00455bde  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455be4  89442448                 mov dword ptr [esp + 0x48], eax
00455be8  8b542448                 mov edx, dword ptr [esp + 0x48]
00455bec  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455bf2  31db                     xor ebx, ebx
00455bf4  01d0                     add eax, edx
00455bf6  31d2                     xor edx, edx
00455bf8  8a19                     mov bl, byte ptr [ecx]
00455bfa  6689c2                   mov dx, ax
00455bfd  89e8                     mov eax, ebp
00455bff  e8af100200               call 0x476cb3 ; -> IllumineTerrain
00455c04  ba04000000               mov edx, 4
00455c09  31db                     xor ebx, ebx
00455c0b  31c0                     xor eax, eax
00455c0d  668b5c243c               mov bx, word ptr [esp + 0x3c]
00455c12  e988f2ffff               jmp 0x454e9f
00455c17  31c0                     xor eax, eax
00455c19  8a8682000000             mov al, byte ptr [esi + 0x82]
00455c1f  83f802                   cmp eax, 2
00455c22  0f85ef000000             jne 0x455d17
00455c28  31c0                     xor eax, eax
00455c2a  668b8680000000           mov ax, word ptr [esi + 0x80]
00455c31  e8d54afcff               call 0x41a70b ; -> BatimentEnDestruction
00455c36  84c0                     test al, al
00455c38  7516                     jne 0x455c50
00455c3a  31c0                     xor eax, eax
00455c3c  668b8680000000           mov ax, word ptr [esi + 0x80]
00455c43  e84444fcff               call 0x41a08c ; -> BatimentGetPlayer
00455c48  3a06                     cmp al, byte ptr [esi]
00455c4a  0f84c7000000             je 0x455d17
00455c50  31c9                     xor ecx, ecx
00455c52  6689f9                   mov cx, di
00455c55  89cd                     mov ebp, ecx
00455c57  c1e504                   shl ebp, 4
00455c5a  01cd                     add ebp, ecx
00455c5c  c1e502                   shl ebp, 2
00455c5f  01cd                     add ebp, ecx
00455c61  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455c67  c1e502                   shl ebp, 2
00455c6a  01eb                     add ebx, ebp
00455c6c  8a4372                   mov al, byte ptr [ebx + 0x72]
00455c6f  84c0                     test al, al
00455c71  0f852ff2ffff             jne 0x454ea6
00455c77  668b4308                 mov ax, word ptr [ebx + 8]
00455c7b  31d2                     xor edx, edx
00455c7d  6689c2                   mov dx, ax
00455c80  89c8                     mov eax, ecx
00455c82  e82dd0feff               call 0x442cb4 ; -> SetEnginCollision
00455c87  c6437201                 mov byte ptr [ebx + 0x72], 1
00455c8b  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
00455c91  01e9                     add ecx, ebp
00455c93  31db                     xor ebx, ebx
00455c95  668b4108                 mov ax, word ptr [ecx + 8]
00455c99  8a19                     mov bl, byte ptr [ecx]
00455c9b  89442410                 mov dword ptr [esp + 0x10], eax
00455c9f  81fbc8000000             cmp ebx, 0xc8
00455ca5  745d                     je 0x455d04
00455ca7  83fb04                   cmp ebx, 4
00455caa  7458                     je 0x455d04
00455cac  30e4                     xor ah, ah
00455cae  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455cb4  0502000000               add eax, 2
00455cb9  89442448                 mov dword ptr [esp + 0x48], eax
00455cbd  30e4                     xor ah, ah
00455cbf  8b542448                 mov edx, dword ptr [esp + 0x48]
00455cc3  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455cc9  01d0                     add eax, edx
00455ccb  31d2                     xor edx, edx
00455ccd  0fb76c2410               movzx ebp, word ptr [esp + 0x10]
00455cd2  6689c2                   mov dx, ax
00455cd5  89e8                     mov eax, ebp
00455cd7  e8750b0200               call 0x476851 ; -> DecouvreTerrain
00455cdc  30e4                     xor ah, ah
00455cde  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455ce4  89442448                 mov dword ptr [esp + 0x48], eax
00455ce8  8b542448                 mov edx, dword ptr [esp + 0x48]
00455cec  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455cf2  31db                     xor ebx, ebx
00455cf4  01d0                     add eax, edx
00455cf6  31d2                     xor edx, edx
00455cf8  8a19                     mov bl, byte ptr [ecx]
00455cfa  6689c2                   mov dx, ax
00455cfd  89e8                     mov eax, ebp
00455cff  e8af0f0200               call 0x476cb3 ; -> IllumineTerrain
00455d04  ba04000000               mov edx, 4
00455d09  31db                     xor ebx, ebx
00455d0b  31c0                     xor eax, eax
00455d0d  668b5c2410               mov bx, word ptr [esp + 0x10]
00455d12  e988f1ffff               jmp 0x454e9f
00455d17  31c0                     xor eax, eax
00455d19  6689f8                   mov ax, di
00455d1c  e83b86ffff               call 0x44e35c ; -> CalculDechargeCaveEngin
00455d21  e9a7efffff               jmp 0x454ccd
00455d26  31c0                     xor eax, eax
00455d28  8a8682000000             mov al, byte ptr [esi + 0x82]
00455d2e  83f802                   cmp eax, 2
00455d31  0f85ec000000             jne 0x455e23
00455d37  31c0                     xor eax, eax
00455d39  668b8680000000           mov ax, word ptr [esi + 0x80]
00455d40  e8c649fcff               call 0x41a70b ; -> BatimentEnDestruction
00455d45  84c0                     test al, al
00455d47  7516                     jne 0x455d5f
00455d49  31c0                     xor eax, eax
00455d4b  668b8680000000           mov ax, word ptr [esi + 0x80]
00455d52  e83543fcff               call 0x41a08c ; -> BatimentGetPlayer
00455d57  3a06                     cmp al, byte ptr [esi]
00455d59  0f84c4000000             je 0x455e23
00455d5f  0fb7ef                   movzx ebp, di
00455d62  89e9                     mov ecx, ebp
00455d64  c1e104                   shl ecx, 4
00455d67  01e9                     add ecx, ebp
00455d69  c1e102                   shl ecx, 2
00455d6c  01e9                     add ecx, ebp
00455d6e  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00455d74  c1e102                   shl ecx, 2
00455d77  01cb                     add ebx, ecx
00455d79  8a4372                   mov al, byte ptr [ebx + 0x72]
00455d7c  84c0                     test al, al
00455d7e  0f8525f3ffff             jne 0x4550a9
00455d84  668b4308                 mov ax, word ptr [ebx + 8]
00455d88  31d2                     xor edx, edx
00455d8a  6689c2                   mov dx, ax
00455d8d  89e8                     mov eax, ebp
00455d8f  e820cffeff               call 0x442cb4 ; -> SetEnginCollision
00455d94  c6437201                 mov byte ptr [ebx + 0x72], 1
00455d98  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00455d9d  01c1                     add ecx, eax
00455d9f  31db                     xor ebx, ebx
00455da1  668b4108                 mov ax, word ptr [ecx + 8]
00455da5  8a19                     mov bl, byte ptr [ecx]
00455da7  89442438                 mov dword ptr [esp + 0x38], eax
00455dab  81fbc8000000             cmp ebx, 0xc8
00455db1  745d                     je 0x455e10
00455db3  83fb04                   cmp ebx, 4
00455db6  7458                     je 0x455e10
00455db8  30e4                     xor ah, ah
00455dba  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455dc0  0502000000               add eax, 2
00455dc5  89442448                 mov dword ptr [esp + 0x48], eax
00455dc9  30e4                     xor ah, ah
00455dcb  8b542448                 mov edx, dword ptr [esp + 0x48]
00455dcf  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455dd5  01d0                     add eax, edx
00455dd7  31d2                     xor edx, edx
00455dd9  0fb76c2438               movzx ebp, word ptr [esp + 0x38]
00455dde  6689c2                   mov dx, ax
00455de1  89e8                     mov eax, ebp
00455de3  e8690a0200               call 0x476851 ; -> DecouvreTerrain
00455de8  30e4                     xor ah, ah
00455dea  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00455df0  89442448                 mov dword ptr [esp + 0x48], eax
00455df4  8b542448                 mov edx, dword ptr [esp + 0x48]
00455df8  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
00455dfe  31db                     xor ebx, ebx
00455e00  01d0                     add eax, edx
00455e02  31d2                     xor edx, edx
00455e04  8a19                     mov bl, byte ptr [ecx]
00455e06  6689c2                   mov dx, ax
00455e09  89e8                     mov eax, ebp
00455e0b  e8a30e0200               call 0x476cb3 ; -> IllumineTerrain
00455e10  ba04000000               mov edx, 4
00455e15  31db                     xor ebx, ebx
00455e17  31c0                     xor eax, eax
00455e19  668b5c2438               mov bx, word ptr [esp + 0x38]
00455e1e  e97ff2ffff               jmp 0x4550a2
00455e23  31c0                     xor eax, eax
00455e25  6689f8                   mov ax, di
00455e28  e8a794ffff               call 0x44f2d4 ; -> CalculTransporteEngin
00455e2d  e99beeffff               jmp 0x454ccd
00455e32  668b4608                 mov ax, word ptr [esi + 8]
00455e36  663b467e                 cmp ax, word ptr [esi + 0x7e]
00455e3a  0f8567f7ffff             jne 0x4555a7
00455e40  31c0                     xor eax, eax
00455e42  8a4602                   mov al, byte ptr [esi + 2]
00455e45  83f810                   cmp eax, 0x10
00455e48  0f8558010000             jne 0x455fa6
00455e4e  31c0                     xor eax, eax
00455e50  668b4608                 mov ax, word ptr [esi + 8]
00455e54  e8df010200               call 0x476038 ; -> TerrainGetSacType
00455e59  88c6                     mov dh, al
00455e5b  88c2                     mov dl, al
00455e5d  31c0                     xor eax, eax
00455e5f  668b4608                 mov ax, word ptr [esi + 8]
00455e63  e849080200               call 0x4766b1 ; -> TerrainEstSac
00455e68  84c0                     test al, al
00455e6a  0f84ab000000             je 0x455f1b
00455e70  8d460a                   lea eax, [esi + 0xa]
00455e73  31db                     xor ebx, ebx
00455e75  668b5866                 mov bx, word ptr [eax + 0x66]
00455e79  43                       inc ebx
00455e7a  668b4002                 mov ax, word ptr [eax + 2]
00455e7e  25ffff0000               and eax, 0xffff
00455e83  39c3                     cmp ebx, eax
00455e85  0f9ec0                   setle al
00455e88  84c0                     test al, al
00455e8a  0f848b000000             je 0x455f1b
00455e90  31c0                     xor eax, eax
00455e92  8a4601                   mov al, byte ptr [esi + 1]
00455e95  83f807                   cmp eax, 7
00455e98  7509                     jne 0x455ea3
00455e9a  31c0                     xor eax, eax
00455e9c  88f0                     mov al, dh
00455e9e  83f802                   cmp eax, 2
00455ea1  7425                     je 0x455ec8
00455ea3  31c0                     xor eax, eax
00455ea5  8a4601                   mov al, byte ptr [esi + 1]
00455ea8  83f805                   cmp eax, 5
00455eab  7509                     jne 0x455eb6
00455ead  31c0                     xor eax, eax
00455eaf  88d0                     mov al, dl
00455eb1  83f801                   cmp eax, 1
00455eb4  7412                     je 0x455ec8
00455eb6  31c0                     xor eax, eax
00455eb8  8a4601                   mov al, byte ptr [esi + 1]
00455ebb  83f806                   cmp eax, 6
00455ebe  755b                     jne 0x455f1b
00455ec0  31c0                     xor eax, eax
00455ec2  88d0                     mov al, dl
00455ec4  85c0                     test eax, eax
00455ec6  7553                     jne 0x455f1b
00455ec8  31c0                     xor eax, eax
00455eca  30ed                     xor ch, ch
00455ecc  668b4608                 mov ax, word ptr [esi + 8]
00455ed0  31d2                     xor edx, edx
00455ed2  e88b070200               call 0x476662 ; -> TerrainRetireMatiere
00455ed7  6689fa                   mov dx, di
00455eda  88c1                     mov cl, al
00455edc  89d0                     mov eax, edx
00455ede  c1e004                   shl eax, 4
00455ee1  01d0                     add eax, edx
00455ee3  c1e002                   shl eax, 2
00455ee6  01d0                     add eax, edx
00455ee8  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455eee  c1e002                   shl eax, 2
00455ef1  01d0                     add eax, edx
00455ef3  668b5070                 mov dx, word ptr [eax + 0x70]
00455ef7  83c00a                   add eax, 0xa
00455efa  42                       inc edx
00455efb  66895066                 mov word ptr [eax + 0x66], dx
00455eff  31db                     xor ebx, ebx
00455f01  668b10                   mov dx, word ptr [eax]
00455f04  6689d3                   mov bx, dx
00455f07  89da                     mov edx, ebx
00455f09  c644034202               mov byte ptr [ebx + eax + 0x42], 2
00455f0e  66894c5006               mov word ptr [eax + edx*2 + 6], cx
00455f13  66ff00                   inc word ptr [eax]
00455f16  e9b2edffff               jmp 0x454ccd
00455f1b  31d2                     xor edx, edx
00455f1d  6689fa                   mov dx, di
00455f20  89d0                     mov eax, edx
00455f22  c1e004                   shl eax, 4
00455f25  01d0                     add eax, edx
00455f27  c1e002                   shl eax, 2
00455f2a  01d0                     add eax, edx
00455f2c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455f32  c1e002                   shl eax, 2
00455f35  01c2                     add edx, eax
00455f37  31c0                     xor eax, eax
00455f39  b107                     mov cl, 7
00455f3b  8a4202                   mov al, byte ptr [edx + 2]
00455f3e  89fb                     mov ebx, edi
00455f40  85c0                     test eax, eax
00455f42  7409                     je 0x455f4d
00455f44  83f804                   cmp eax, 4
00455f47  7404                     je 0x455f4d
00455f49  b001                     mov al, 1
00455f4b  eb02                     jmp 0x455f4f
00455f4d  30c0                     xor al, al
00455f4f  84c0                     test al, al
00455f51  7445                     je 0x455f98
00455f53  31d2                     xor edx, edx
00455f55  6689da                   mov dx, bx
00455f58  89d0                     mov eax, edx
00455f5a  c1e004                   shl eax, 4
00455f5d  01d0                     add eax, edx
00455f5f  c1e002                   shl eax, 2
00455f62  01d0                     add eax, edx
00455f64  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455f6a  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
00455f6e  663b1d04634900           cmp bx, word ptr [0x496304]
00455f75  7521                     jne 0x455f98
00455f77  bfffff0000               mov edi, 0xffff
00455f7c  30ed                     xor ch, ch
00455f7e  31c0                     xor eax, eax
00455f80  882d360f4e00             mov byte ptr [0x4e0f36], ch
00455f86  882d370f4e00             mov byte ptr [0x4e0f37], ch
00455f8c  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
00455f91  66893d04634900           mov word ptr [0x496304], di
00455f98  66c786b2000000ffff       mov word ptr [esi + 0xb2], 0xffff
00455fa1  e927edffff               jmp 0x454ccd
00455fa6  83f811                   cmp eax, 0x11
00455fa9  0f851eedffff             jne 0x454ccd
00455faf  31db                     xor ebx, ebx
00455fb1  31c9                     xor ecx, ecx
00455fb3  31d2                     xor edx, edx
00455fb5  6689f9                   mov cx, di
00455fb8  668b9e84000000           mov bx, word ptr [esi + 0x84]
00455fbf  8a9682000000             mov dl, byte ptr [esi + 0x82]
00455fc5  89c8                     mov eax, ecx
00455fc7  e80cd9feff               call 0x4438d8 ; -> EnginRetireType
00455fcc  31d2                     xor edx, edx
00455fce  89c8                     mov eax, ecx
00455fd0  668b567c                 mov dx, word ptr [esi + 0x7c]
00455fd4  e8faf7feff               call 0x4457d3 ; -> SetDeplaceEngin
00455fd9  c6868200000000           mov byte ptr [esi + 0x82], 0
00455fe0  ebb6                     jmp 0x455f98
00455fe2  31c0                     xor eax, eax
00455fe4  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455feb  e81b47fcff               call 0x41a70b ; -> BatimentEnDestruction
00455ff0  84c0                     test al, al
00455ff2  0f859fedffff             jne 0x454d97
00455ff8  31c0                     xor eax, eax
00455ffa  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00456001  e88640fcff               call 0x41a08c ; -> BatimentGetPlayer
00456006  25ff000000               and eax, 0xff
0045600b  3dc8000000               cmp eax, 0xc8
00456010  0f8481edffff             je 0x454d97
00456016  31c0                     xor eax, eax
00456018  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045601f  e86840fcff               call 0x41a08c ; -> BatimentGetPlayer
00456024  3a06                     cmp al, byte ptr [esi]
00456026  0f846bedffff             je 0x454d97
0045602c  31d2                     xor edx, edx
0045602e  31c0                     xor eax, eax
00456030  668b5608                 mov dx, word ptr [esi + 8]
00456034  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045603b  e8dfd7fcff               call 0x42381f ; -> BatimentAdjacent
00456040  84c0                     test al, al
00456042  7571                     jne 0x4560b5
00456044  668b467e                 mov ax, word ptr [esi + 0x7e]
00456048  663b4608                 cmp ax, word ptr [esi + 8]
0045604c  0f8555f5ffff             jne 0x4555a7
00456052  31c0                     xor eax, eax
00456054  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045605b  31d2                     xor edx, edx
0045605d  e8804efcff               call 0x41aee2 ; -> BatimentGetCase
00456062  6689fa                   mov dx, di
00456065  89c3                     mov ebx, eax
00456067  89d0                     mov eax, edx
00456069  c1e004                   shl eax, 4
0045606c  01d0                     add eax, edx
0045606e  c1e002                   shl eax, 2
00456071  01c2                     add edx, eax
00456073  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456078  c1e202                   shl edx, 2
0045607b  01d0                     add eax, edx
0045607d  6689587e                 mov word ptr [eax + 0x7e], bx
00456081  663b3d04634900           cmp di, word ptr [0x496304]
00456088  751f                     jne 0x4560a9
0045608a  30d2                     xor dl, dl
0045608c  8815360f4e00             mov byte ptr [0x4e0f36], dl
00456092  8815370f4e00             mov byte ptr [0x4e0f37], dl
00456098  31d2                     xor edx, edx
0045609a  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
004560a0  66c70504634900ffff       mov word ptr [0x496304], 0xffff
004560a9  c6808800000000           mov byte ptr [eax + 0x88], 0
004560b0  e9f2f4ffff               jmp 0x4555a7
004560b5  31c0                     xor eax, eax
004560b7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004560be  31d2                     xor edx, edx
004560c0  e8c73ffcff               call 0x41a08c ; -> BatimentGetPlayer
004560c5  6689fa                   mov dx, di
004560c8  88c1                     mov cl, al
004560ca  89d0                     mov eax, edx
004560cc  c1e004                   shl eax, 4
004560cf  01d0                     add eax, edx
004560d1  c1e002                   shl eax, 2
004560d4  01d0                     add eax, edx
004560d6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004560dc  31db                     xor ebx, ebx
004560de  8a0482                   mov al, byte ptr [edx + eax*4]
004560e1  ba64000000               mov edx, 0x64
004560e6  8844245c                 mov byte ptr [esp + 0x5c], al
004560ea  88442454                 mov byte ptr [esp + 0x54], al
004560ee  0fb6e8                   movzx ebp, al
004560f1  8954240c                 mov dword ptr [esp + 0xc], edx
004560f5  8a9dbc194e00             mov bl, byte ptr [ebp + 0x4e19bc]
004560fb  31c0                     xor eax, eax
004560fd  31d2                     xor edx, edx
004560ff  e8d8a30100               call 0x4704dc ; -> Random
00456104  f774240c                 div dword ptr [esp + 0xc]
00456108  39da                     cmp edx, ebx
0045610a  0f86c6000000             jbe 0x4561d6
00456110  31c0                     xor eax, eax
00456112  8a85bc194e00             mov al, byte ptr [ebp + 0x4e19bc]
00456118  83f805                   cmp eax, 5
0045611b  7c0d                     jl 0x45612a
0045611d  88c4                     mov ah, al
0045611f  80ec05                   sub ah, 5
00456122  88a5bc194e00             mov byte ptr [ebp + 0x4e19bc], ah
00456128  eb08                     jmp 0x456132
0045612a  30c0                     xor al, al
0045612c  8885bc194e00             mov byte ptr [ebp + 0x4e19bc], al
00456132  31d2                     xor edx, edx
00456134  6689fa                   mov dx, di
00456137  89d0                     mov eax, edx
00456139  e81a0f0000               call 0x457058 ; -> RetireEngin
0045613e  89d0                     mov eax, edx
00456140  c1e004                   shl eax, 4
00456143  01d0                     add eax, edx
00456145  c1e002                   shl eax, 2
00456148  01d0                     add eax, edx
0045614a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456150  30db                     xor bl, bl
00456152  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00456156  25ff000000               and eax, 0xff
0045615b  7409                     je 0x456166
0045615d  83f804                   cmp eax, 4
00456160  7404                     je 0x456166
00456162  b001                     mov al, 1
00456164  eb02                     jmp 0x456168
00456166  30c0                     xor al, al
00456168  84c0                     test al, al
0045616a  7446                     je 0x4561b2
0045616c  31d2                     xor edx, edx
0045616e  6689fa                   mov dx, di
00456171  89d0                     mov eax, edx
00456173  c1e004                   shl eax, 4
00456176  01d0                     add eax, edx
00456178  c1e002                   shl eax, 2
0045617b  01d0                     add eax, edx
0045617d  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456183  885c8202                 mov byte ptr [edx + eax*4 + 2], bl
00456187  663b3d04634900           cmp di, word ptr [0x496304]
0045618e  7522                     jne 0x4561b2
00456190  b9ffff0000               mov ecx, 0xffff
00456195  30d2                     xor dl, dl
00456197  31f6                     xor esi, esi
00456199  8815360f4e00             mov byte ptr [0x4e0f36], dl
0045619f  8815370f4e00             mov byte ptr [0x4e0f37], dl
004561a5  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
004561ab  66890d04634900           mov word ptr [0x496304], cx
004561b2  8a442454                 mov al, byte ptr [esp + 0x54]
004561b6  3a0541805000             cmp al, byte ptr [0x508041]
004561bc  0f850bebffff             jne 0x454ccd
004561c2  baf6010000               mov edx, 0x1f6
004561c7  b80a000000               mov eax, 0xa
004561cc  e87a370100               call 0x46994b ; -> MessageBoxSet
004561d1  e9f7eaffff               jmp 0x454ccd
004561d6  31c0                     xor eax, eax
004561d8  bb0a000000               mov ebx, 0xa
004561dd  668b86c4000000           mov ax, word ptr [esi + 0xc4]
004561e4  895c242c                 mov dword ptr [esp + 0x2c], ebx
004561e8  83f803                   cmp eax, 3
004561eb  0f84cb000000             je 0x4562bc
004561f1  bb03000000               mov ebx, 3
004561f6  31d2                     xor edx, edx
004561f8  31c0                     xor eax, eax
004561fa  8a54245c                 mov dl, byte ptr [esp + 0x5c]
004561fe  88c8                     mov al, cl
00456200  e813ef0100               call 0x475118 ; -> MAJSympathie
00456205  89e3                     mov ebx, esp
00456207  31c0                     xor eax, eax
00456209  8d542404                 lea edx, [esp + 4]
0045620d  88c8                     mov al, cl
0045620f  8d4c2418                 lea ecx, [esp + 0x18]
00456213  50                       push eax
00456214  89442410                 mov dword ptr [esp + 0x10], eax
00456218  8d442406                 lea eax, [esp + 6]
0045621c  e87c140100               call 0x46769d ; -> GetRessourceStock
00456221  ba03000000               mov edx, 3
00456226  89e8                     mov eax, ebp
00456228  e8f5af0000               call 0x461222 ; -> RechercheTypeBatiment
0045622d  89442448                 mov dword ptr [esp + 0x48], eax
00456231  8a9ec4000000             mov bl, byte ptr [esi + 0xc4]
00456237  81e3ff000000             and ebx, 0xff
0045623d  b903000000               mov ecx, 3
00456242  89da                     mov edx, ebx
00456244  89d8                     mov eax, ebx
00456246  c1fa1f                   sar edx, 0x1f
00456249  f7f9                     idiv ecx
0045624b  0fb6f2                   movzx esi, dl
0045624e  31d2                     xor edx, edx
00456250  668b1474                 mov dx, word ptr [esp + esi*2]
00456254  89d0                     mov eax, edx
00456256  c1fa1f                   sar edx, 0x1f
00456259  2bc2                     sub eax, edx
0045625b  d1f8                     sar eax, 1
0045625d  31d2                     xor edx, edx
0045625f  8b5c240c                 mov ebx, dword ptr [esp + 0xc]
00456263  6689c2                   mov dx, ax
00456266  89f0                     mov eax, esi
00456268  e850d3fcff               call 0x4235bd ; -> BatimentEnleveMatiere
0045626d  31d2                     xor edx, edx
0045626f  668b1474                 mov dx, word ptr [esp + esi*2]
00456273  89d0                     mov eax, edx
00456275  c1fa1f                   sar edx, 0x1f
00456278  2bc2                     sub eax, edx
0045627a  d1f8                     sar eax, 1
0045627c  31db                     xor ebx, ebx
0045627e  668b5c2448               mov bx, word ptr [esp + 0x48]
00456283  89d9                     mov ecx, ebx
00456285  31d2                     xor edx, edx
00456287  89eb                     mov ebx, ebp
00456289  6689c2                   mov dx, ax
0045628c  89f0                     mov eax, esi
0045628e  e87cd1fcff               call 0x42340f ; -> BatimentAjouteMatiere
00456293  8a44245c                 mov al, byte ptr [esp + 0x5c]
00456297  31f6                     xor esi, esi
00456299  8a3d41805000             mov bh, byte ptr [0x508041]
0045629f  8974242c                 mov dword ptr [esp + 0x2c], esi
004562a3  38f8                     cmp al, bh
004562a5  0f8579000000             jne 0x456324
004562ab  baf5010000               mov edx, 0x1f5
004562b0  b80a000000               mov eax, 0xa
004562b5  e891360100               call 0x46994b ; -> MessageBoxSet
004562ba  eb68                     jmp 0x456324
004562bc  bb04000000               mov ebx, 4
004562c1  31d2                     xor edx, edx
004562c3  31c0                     xor eax, eax
004562c5  8a54245c                 mov dl, byte ptr [esp + 0x5c]
004562c9  88c8                     mov al, cl
004562cb  e848ee0100               call 0x475118 ; -> MAJSympathie
004562d0  31db                     xor ebx, ebx
004562d2  88cb                     mov bl, cl
004562d4  89d8                     mov eax, ebx
004562d6  31c9                     xor ecx, ecx
004562d8  e8d4b40100               call 0x4717b1 ; -> RechercheGetBranche
004562dd  88c1                     mov cl, al
004562df  89ca                     mov edx, ecx
004562e1  89e8                     mov eax, ebp
004562e3  e8dab40100               call 0x4717c2 ; -> RechercheGetNiveau
004562e8  89c6                     mov esi, eax
004562ea  89ca                     mov edx, ecx
004562ec  89d8                     mov eax, ebx
004562ee  e8cfb40100               call 0x4717c2 ; -> RechercheGetNiveau
004562f3  6639c6                   cmp si, ax
004562f6  732c                     jae 0x456324
004562f8  8a44245c                 mov al, byte ptr [esp + 0x5c]
004562fc  3a0541805000             cmp al, byte ptr [0x508041]
00456302  750f                     jne 0x456313
00456304  baf5010000               mov edx, 0x1f5
00456309  b80a000000               mov eax, 0xa
0045630e  e838360100               call 0x46994b ; -> MessageBoxSet
00456313  31c0                     xor eax, eax
00456315  8a442454                 mov al, byte ptr [esp + 0x54]
00456319  31c9                     xor ecx, ecx
0045631b  e87db10100               call 0x47149d ; -> RechercheEndTechnologie
00456320  894c242c                 mov dword ptr [esp + 0x2c], ecx
00456324  31c0                     xor eax, eax
00456326  668b44242c               mov ax, word ptr [esp + 0x2c]
0045632b  83f80a                   cmp eax, 0xa
0045632e  741d                     je 0x45634d
00456330  31db                     xor ebx, ebx
00456332  8a5c2454                 mov bl, byte ptr [esp + 0x54]
00456336  31d2                     xor edx, edx
00456338  8a93bc194e00             mov dl, byte ptr [ebx + 0x4e19bc]
0045633e  89d0                     mov eax, edx
00456340  c1fa1f                   sar edx, 0x1f
00456343  2bc2                     sub eax, edx
00456345  d1f8                     sar eax, 1
00456347  8883bc194e00             mov byte ptr [ebx + 0x4e19bc], al
0045634d  31d2                     xor edx, edx
0045634f  6689fa                   mov dx, di
00456352  89d0                     mov eax, edx
00456354  e8ff0c0000               call 0x457058 ; -> RetireEngin
00456359  89d0                     mov eax, edx
0045635b  c1e004                   shl eax, 4
0045635e  01d0                     add eax, edx
00456360  c1e002                   shl eax, 2
00456363  01d0                     add eax, edx
00456365  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045636b  30db                     xor bl, bl
0045636d  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00456371  25ff000000               and eax, 0xff
00456376  7409                     je 0x456381
00456378  83f804                   cmp eax, 4
0045637b  7404                     je 0x456381
0045637d  b001                     mov al, 1
0045637f  eb02                     jmp 0x456383
00456381  30c0                     xor al, al
00456383  84c0                     test al, al
00456385  0f8442e9ffff             je 0x454ccd
0045638b  31d2                     xor edx, edx
0045638d  6689fa                   mov dx, di
00456390  89d0                     mov eax, edx
00456392  c1e004                   shl eax, 4
00456395  01d0                     add eax, edx
00456397  c1e002                   shl eax, 2
0045639a  01d0                     add eax, edx
0045639c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004563a2  885c8202                 mov byte ptr [edx + eax*4 + 2], bl
004563a6  663b3d04634900           cmp di, word ptr [0x496304]
004563ad  0f851ae9ffff             jne 0x454ccd
004563b3  30c9                     xor cl, cl
004563b5  baffff0000               mov edx, 0xffff
004563ba  880d360f4e00             mov byte ptr [0x4e0f36], cl
004563c0  880d370f4e00             mov byte ptr [0x4e0f37], cl
004563c6  31c9                     xor ecx, ecx
004563c8  66891504634900           mov word ptr [0x496304], dx
004563cf  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
004563d5  e9f3e8ffff               jmp 0x454ccd
004563da  668b467e                 mov ax, word ptr [esi + 0x7e]
004563de  663b4608                 cmp ax, word ptr [esi + 8]
004563e2  0f85bff1ffff             jne 0x4555a7
004563e8  8a8691000000             mov al, byte ptr [esi + 0x91]
004563ee  3a8690000000             cmp al, byte ptr [esi + 0x90]
004563f4  0f8575f6ffff             jne 0x455a6f
004563fa  31c0                     xor eax, eax
004563fc  6689f8                   mov ax, di
004563ff  e8901dffff               call 0x448194 ; -> EnginEnArret
00456404  84c0                     test al, al
00456406  753f                     jne 0x456447
00456408  31d2                     xor edx, edx
0045640a  6689fa                   mov dx, di
0045640d  89d0                     mov eax, edx
0045640f  c1e004                   shl eax, 4
00456412  01d0                     add eax, edx
00456414  c1e002                   shl eax, 2
00456417  01d0                     add eax, edx
00456419  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0045641f  c1e002                   shl eax, 2
00456422  01c3                     add ebx, eax
00456424  31d2                     xor edx, edx
00456426  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
0045642c  31c9                     xor ecx, ecx
0045642e  42                       inc edx
0045642f  8a8ba5000000             mov cl, byte ptr [ebx + 0xa5]
00456435  89d0                     mov eax, edx
00456437  c1fa1f                   sar edx, 0x1f
0045643a  f7f9                     idiv ecx
0045643c  8893a4000000             mov byte ptr [ebx + 0xa4], dl
00456442  e986e8ffff               jmp 0x454ccd
00456447  31d2                     xor edx, edx
00456449  6689fa                   mov dx, di
0045644c  89d0                     mov eax, edx
0045644e  c1e004                   shl eax, 4
00456451  01d0                     add eax, edx
00456453  c1e002                   shl eax, 2
00456456  01d0                     add eax, edx
00456458  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045645e  b107                     mov cl, 7
00456460  89fb                     mov ebx, edi
00456462  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00456466  25ff000000               and eax, 0xff
0045646b  7429                     je 0x456496
0045646d  31d2                     xor edx, edx
0045646f  6689fa                   mov dx, di
00456472  89d0                     mov eax, edx
00456474  c1e004                   shl eax, 4
00456477  01d0                     add eax, edx
00456479  c1e002                   shl eax, 2
0045647c  01d0                     add eax, edx
0045647e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456484  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00456488  25ff000000               and eax, 0xff
0045648d  83f804                   cmp eax, 4
00456490  7404                     je 0x456496
00456492  b001                     mov al, 1
00456494  eb02                     jmp 0x456498
00456496  30c0                     xor al, al
00456498  84c0                     test al, al
0045649a  0f842de8ffff             je 0x454ccd
004564a0  31d2                     xor edx, edx
004564a2  6689fa                   mov dx, di
004564a5  89d0                     mov eax, edx
004564a7  c1e004                   shl eax, 4
004564aa  01d0                     add eax, edx
004564ac  c1e002                   shl eax, 2
004564af  01d0                     add eax, edx
004564b1  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004564b7  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
004564bb  663b3d04634900           cmp di, word ptr [0x496304]
004564c2  0f8505e8ffff             jne 0x454ccd
004564c8  bfffff0000               mov edi, 0xffff
004564cd  30f6                     xor dh, dh
004564cf  31c9                     xor ecx, ecx
004564d1  8835360f4e00             mov byte ptr [0x4e0f36], dh
004564d7  8835370f4e00             mov byte ptr [0x4e0f37], dh
004564dd  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
004564e3  66893d04634900           mov word ptr [0x496304], di
004564ea  e9dee7ffff               jmp 0x454ccd
004564ef  31c0                     xor eax, eax
004564f1  8a8689000000             mov al, byte ptr [esi + 0x89]
004564f7  85c0                     test eax, eax
004564f9  7416                     je 0x456511
004564fb  31c0                     xor eax, eax
004564fd  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00456504  e80242fcff               call 0x41a70b ; -> BatimentEnDestruction
00456509  84c0                     test al, al
0045650b  0f85ace7ffff             jne 0x454cbd
00456511  31c0                     xor eax, eax
00456513  6689f8                   mov ax, di
00456516  e84546ffff               call 0x44ab60 ; -> CalculConstruireBatiment
0045651b  e9ade7ffff               jmp 0x454ccd
00456520  31c0                     xor eax, eax
00456522  6689f8                   mov ax, di
00456525  e8dc41ffff               call 0x44a706 ; -> CalculPiege
0045652a  e99ee7ffff               jmp 0x454ccd
0045652f  31d2                     xor edx, edx
00456531  6689fa                   mov dx, di
00456534  89d0                     mov eax, edx
00456536  c1e004                   shl eax, 4
00456539  01d0                     add eax, edx
0045653b  c1e002                   shl eax, 2
0045653e  01c2                     add edx, eax
00456540  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456545  c1e202                   shl edx, 2
00456548  8a440201                 mov al, byte ptr [edx + eax + 1]
0045654c  25ff000000               and eax, 0xff
00456551  83f806                   cmp eax, 6
00456554  755e                     jne 0x4565b4
00456556  668b9ec0000000           mov bx, word ptr [esi + 0xc0]
0045655d  31d2                     xor edx, edx
0045655f  6689da                   mov dx, bx
00456562  89d0                     mov eax, edx
00456564  c1e004                   shl eax, 4
00456567  01d0                     add eax, edx
00456569  c1e002                   shl eax, 2
0045656c  01d0                     add eax, edx
0045656e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456574  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00456578  25ff000000               and eax, 0xff
0045657d  742b                     je 0x4565aa
0045657f  31d2                     xor edx, edx
00456581  6689da                   mov dx, bx
00456584  89d0                     mov eax, edx
00456586  c1e004                   shl eax, 4
00456589  01d0                     add eax, edx
0045658b  c1e002                   shl eax, 2
0045658e  01c2                     add edx, eax
00456590  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456595  c1e202                   shl edx, 2
00456598  8a440202                 mov al, byte ptr [edx + eax + 2]
0045659c  25ff000000               and eax, 0xff
004565a1  83f804                   cmp eax, 4
004565a4  7404                     je 0x4565aa
004565a6  b001                     mov al, 1
004565a8  eb02                     jmp 0x4565ac
004565aa  30c0                     xor al, al
004565ac  84c0                     test al, al
004565ae  0f84e3e7ffff             je 0x454d97
004565b4  31d2                     xor edx, edx
004565b6  6689fa                   mov dx, di
004565b9  89d0                     mov eax, edx
004565bb  c1e004                   shl eax, 4
004565be  01d0                     add eax, edx
004565c0  c1e002                   shl eax, 2
004565c3  01c2                     add edx, eax
004565c5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004565ca  c1e202                   shl edx, 2
004565cd  8a440201                 mov al, byte ptr [edx + eax + 1]
004565d1  25ff000000               and eax, 0xff
004565d6  83f807                   cmp eax, 7
004565d9  7516                     jne 0x4565f1
004565db  31c0                     xor eax, eax
004565dd  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004565e4  e82241fcff               call 0x41a70b ; -> BatimentEnDestruction
004565e9  84c0                     test al, al
004565eb  0f85a6e7ffff             jne 0x454d97
004565f1  31c0                     xor eax, eax
004565f3  6689f8                   mov ax, di
004565f6  e8fa4fffff               call 0x44b5f5 ; -> CalculReparer
004565fb  e9cde6ffff               jmp 0x454ccd
00456600  31c0                     xor eax, eax
00456602  8a8682000000             mov al, byte ptr [esi + 0x82]
00456608  83f802                   cmp eax, 2
0045660b  0f851b010000             jne 0x45672c
00456611  31c0                     xor eax, eax
00456613  668b8680000000           mov ax, word ptr [esi + 0x80]
0045661a  e8ec40fcff               call 0x41a70b ; -> BatimentEnDestruction
0045661f  84c0                     test al, al
00456621  7516                     jne 0x456639
00456623  31c0                     xor eax, eax
00456625  668b8680000000           mov ax, word ptr [esi + 0x80]
0045662c  e85b3afcff               call 0x41a08c ; -> BatimentGetPlayer
00456631  3a06                     cmp al, byte ptr [esi]
00456633  0f84f3000000             je 0x45672c
00456639  31d2                     xor edx, edx
0045663b  6689fa                   mov dx, di
0045663e  89d0                     mov eax, edx
00456640  c1e004                   shl eax, 4
00456643  01d0                     add eax, edx
00456645  c1e002                   shl eax, 2
00456648  01d0                     add eax, edx
0045664a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456650  8a448272                 mov al, byte ptr [edx + eax*4 + 0x72]
00456654  84c0                     test al, al
00456656  0f854deaffff             jne 0x4550a9
0045665c  31c0                     xor eax, eax
0045665e  8a4601                   mov al, byte ptr [esi + 1]
00456661  83f807                   cmp eax, 7
00456664  750e                     jne 0x456674
00456666  31c0                     xor eax, eax
00456668  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0045666f  e86aee0100               call 0x4754de ; -> MineEndWork
00456674  31c9                     xor ecx, ecx
00456676  6689f9                   mov cx, di
00456679  89cd                     mov ebp, ecx
0045667b  c1e504                   shl ebp, 4
0045667e  01cd                     add ebp, ecx
00456680  c1e502                   shl ebp, 2
00456683  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00456689  01cd                     add ebp, ecx
0045668b  89ca                     mov edx, ecx
0045668d  c1e502                   shl ebp, 2
00456690  31ca                     xor edx, ecx
00456692  668b442b08               mov ax, word ptr [ebx + ebp + 8]
00456697  6689c2                   mov dx, ax
0045669a  89c8                     mov eax, ecx
0045669c  e813c6feff               call 0x442cb4 ; -> SetEnginCollision
004566a1  c6442b7201               mov byte ptr [ebx + ebp + 0x72], 1
004566a6  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
004566ac  01e9                     add ecx, ebp
004566ae  31db                     xor ebx, ebx
004566b0  668b4108                 mov ax, word ptr [ecx + 8]
004566b4  8a19                     mov bl, byte ptr [ecx]
004566b6  89442434                 mov dword ptr [esp + 0x34], eax
004566ba  81fbc8000000             cmp ebx, 0xc8
004566c0  7457                     je 0x456719
004566c2  83fb04                   cmp ebx, 4
004566c5  7452                     je 0x456719
004566c7  30e4                     xor ah, ah
004566c9  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
004566cf  0502000000               add eax, 2
004566d4  89442448                 mov dword ptr [esp + 0x48], eax
004566d8  30e4                     xor ah, ah
004566da  8b542448                 mov edx, dword ptr [esp + 0x48]
004566de  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
004566e4  01d0                     add eax, edx
004566e6  31d2                     xor edx, edx
004566e8  0fb76c2434               movzx ebp, word ptr [esp + 0x34]
004566ed  6689c2                   mov dx, ax
004566f0  89e8                     mov eax, ebp
004566f2  e85a010200               call 0x476851 ; -> DecouvreTerrain
004566f7  31db                     xor ebx, ebx
004566f9  30f6                     xor dh, dh
004566fb  30e4                     xor ah, ah
004566fd  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
00456703  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
00456709  01d0                     add eax, edx
0045670b  31d2                     xor edx, edx
0045670d  8a19                     mov bl, byte ptr [ecx]
0045670f  6689c2                   mov dx, ax
00456712  89e8                     mov eax, ebp
00456714  e89a050200               call 0x476cb3 ; -> IllumineTerrain
00456719  ba04000000               mov edx, 4
0045671e  31db                     xor ebx, ebx
00456720  31c0                     xor eax, eax
00456722  668b5c2434               mov bx, word ptr [esp + 0x34]
00456727  e976e9ffff               jmp 0x4550a2
0045672c  31c0                     xor eax, eax
0045672e  6689f8                   mov ax, di
00456731  e83e55ffff               call 0x44bc74 ; -> CalculWorkEngin
00456736  e992e5ffff               jmp 0x454ccd
0045673b  31c0                     xor eax, eax
0045673d  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00456744  3dffff0000               cmp eax, 0xffff
00456749  7427                     je 0x456772
0045674b  e8bb3ffcff               call 0x41a70b ; -> BatimentEnDestruction
00456750  84c0                     test al, al
00456752  751e                     jne 0x456772
00456754  31c0                     xor eax, eax
00456756  668b86b8000000           mov ax, word ptr [esi + 0xb8]
0045675d  e82a39fcff               call 0x41a08c ; -> BatimentGetPlayer
00456762  25ff000000               and eax, 0xff
00456767  3dc8000000               cmp eax, 0xc8
0045676c  0f852c010000             jne 0x45689e
00456772  31c9                     xor ecx, ecx
00456774  6689f9                   mov cx, di
00456777  89c8                     mov eax, ecx
00456779  c1e004                   shl eax, 4
0045677c  01c8                     add eax, ecx
0045677e  c1e002                   shl eax, 2
00456781  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456787  01c8                     add eax, ecx
00456789  8a0482                   mov al, byte ptr [edx + eax*4]
0045678c  25ff000000               and eax, 0xff
00456791  e881700100               call 0x46d817 ; -> PlayerGetType
00456796  25ff000000               and eax, 0xff
0045679b  83f802                   cmp eax, 2
0045679e  7513                     jne 0x4567b3
004567a0  ba4a000000               mov edx, 0x4a
004567a5  89c8                     mov eax, ecx
004567a7  31db                     xor ebx, ebx
004567a9  e81ac20200               call 0x4829c8 ; -> iagUnitSendMessage
004567ae  e91ae5ffff               jmp 0x454ccd
004567b3  31d2                     xor edx, edx
004567b5  89c8                     mov eax, ecx
004567b7  668b567e                 mov dx, word ptr [esi + 0x7e]
004567bb  e813f0feff               call 0x4457d3 ; -> SetDeplaceEngin
004567c0  66c786b8000000ffff       mov word ptr [esi + 0xb8], 0xffff
004567c9  e9ffe4ffff               jmp 0x454ccd
004567ce  31c0                     xor eax, eax
004567d0  668b86b8000000           mov ax, word ptr [esi + 0xb8]
004567d7  3dffff0000               cmp eax, 0xffff
004567dc  0f846d000000             je 0x45684f
004567e2  31d2                     xor edx, edx
004567e4  6689c2                   mov dx, ax
004567e7  89d0                     mov eax, edx
004567e9  c1e004                   shl eax, 4
004567ec  01d0                     add eax, edx
004567ee  c1e002                   shl eax, 2
004567f1  01d0                     add eax, edx
004567f3  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004567f9  c1e002                   shl eax, 2
004567fc  01c2                     add edx, eax
004567fe  31c0                     xor eax, eax
00456800  8a4202                   mov al, byte ptr [edx + 2]
00456803  85c0                     test eax, eax
00456805  7409                     je 0x456810
00456807  83f804                   cmp eax, 4
0045680a  7404                     je 0x456810
0045680c  b001                     mov al, 1
0045680e  eb02                     jmp 0x456812
00456810  30c0                     xor al, al
00456812  84c0                     test al, al
00456814  7439                     je 0x45684f
00456816  668b86b8000000           mov ax, word ptr [esi + 0xb8]
0045681d  31d2                     xor edx, edx
0045681f  6689c2                   mov dx, ax
00456822  89d0                     mov eax, edx
00456824  c1e004                   shl eax, 4
00456827  01d0                     add eax, edx
00456829  c1e002                   shl eax, 2
0045682c  01c2                     add edx, eax
0045682e  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456833  c1e202                   shl edx, 2
00456836  01d0                     add eax, edx
00456838  8a10                     mov dl, byte ptr [eax]
0045683a  81e2ff000000             and edx, 0xff
00456840  81fac8000000             cmp edx, 0xc8
00456846  7407                     je 0x45684f
00456848  8a4072                   mov al, byte ptr [eax + 0x72]
0045684b  84c0                     test al, al
0045684d  754f                     jne 0x45689e
0045684f  31c9                     xor ecx, ecx
00456851  6689f9                   mov cx, di
00456854  89c8                     mov eax, ecx
00456856  c1e004                   shl eax, 4
00456859  01c8                     add eax, ecx
0045685b  c1e002                   shl eax, 2
0045685e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456864  01c8                     add eax, ecx
00456866  8a0482                   mov al, byte ptr [edx + eax*4]
00456869  25ff000000               and eax, 0xff
0045686e  e8a46f0100               call 0x46d817 ; -> PlayerGetType
00456873  25ff000000               and eax, 0xff
00456878  83f802                   cmp eax, 2
0045687b  0f841fffffff             je 0x4567a0
00456881  e92dffffff               jmp 0x4567b3
00456886  8a86b7000000             mov al, byte ptr [esi + 0xb7]
0045688c  3c01                     cmp al, 1
0045688e  720e                     jb 0x45689e
00456890  0f8638ffffff             jbe 0x4567ce
00456896  3c03                     cmp al, 3
00456898  0f849dfeffff             je 0x45673b
0045689e  31c0                     xor eax, eax
004568a0  6689f8                   mov ax, di
004568a3  e86cb0ffff               call 0x451914 ; -> CalculAttaqueEngin
004568a8  e920e4ffff               jmp 0x454ccd
004568ad  31d2                     xor edx, edx
004568af  6689fa                   mov dx, di
004568b2  89d0                     mov eax, edx
004568b4  c1e004                   shl eax, 4
004568b7  01d0                     add eax, edx
004568b9  c1e002                   shl eax, 2
004568bc  b107                     mov cl, 7
004568be  01c2                     add edx, eax
004568c0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004568c5  c1e202                   shl edx, 2
004568c8  89fb                     mov ebx, edi
004568ca  8a440202                 mov al, byte ptr [edx + eax + 2]
004568ce  25ff000000               and eax, 0xff
004568d3  7429                     je 0x4568fe
004568d5  31d2                     xor edx, edx
004568d7  6689fa                   mov dx, di
004568da  89d0                     mov eax, edx
004568dc  c1e004                   shl eax, 4
004568df  01d0                     add eax, edx
004568e1  c1e002                   shl eax, 2
004568e4  01d0                     add eax, edx
004568e6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004568ec  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
004568f0  25ff000000               and eax, 0xff
004568f5  83f804                   cmp eax, 4
004568f8  7404                     je 0x4568fe
004568fa  b001                     mov al, 1
004568fc  eb02                     jmp 0x456900
004568fe  30c0                     xor al, al
00456900  84c0                     test al, al
00456902  0f84c5e3ffff             je 0x454ccd
00456908  31d2                     xor edx, edx
0045690a  6689fa                   mov dx, di
0045690d  89d0                     mov eax, edx
0045690f  c1e004                   shl eax, 4
00456912  01d0                     add eax, edx
00456914  c1e002                   shl eax, 2
00456917  01d0                     add eax, edx
00456919  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0045691f  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
00456923  663b3d04634900           cmp di, word ptr [0x496304]
0045692a  0f859de3ffff             jne 0x454ccd
00456930  beffff0000               mov esi, 0xffff
00456935  30db                     xor bl, bl
00456937  31d2                     xor edx, edx
00456939  881d360f4e00             mov byte ptr [0x4e0f36], bl
0045693f  881d370f4e00             mov byte ptr [0x4e0f37], bl
00456945  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0045694b  66893504634900           mov word ptr [0x496304], si
00456952  e976e3ffff               jmp 0x454ccd
00456957  31c0                     xor eax, eax
00456959  6689f8                   mov ax, di
0045695c  e8ce11ffff               call 0x447b2f ; -> AnimBallonStatic
00456961  e967e3ffff               jmp 0x454ccd
00456966  31d2                     xor edx, edx
00456968  6689fa                   mov dx, di
0045696b  89d0                     mov eax, edx
0045696d  c1e004                   shl eax, 4
00456970  01d0                     add eax, edx
00456972  c1e002                   shl eax, 2
00456975  01d0                     add eax, edx
00456977  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0045697d  c1e002                   shl eax, 2
00456980  01c3                     add ebx, eax
00456982  8a4301                   mov al, byte ptr [ebx + 1]
00456985  3c08                     cmp al, 8
00456987  7226                     jb 0x4569af
00456989  7626                     jbe 0x4569b1
0045698b  3c12                     cmp al, 0x12
0045698d  7213                     jb 0x4569a2
0045698f  7620                     jbe 0x4569b1
00456991  3c17                     cmp al, 0x17
00456993  721c                     jb 0x4569b1
00456995  3c18                     cmp al, 0x18
00456997  7618                     jbe 0x4569b1
00456999  3c19                     cmp al, 0x19
0045699b  7414                     je 0x4569b1
0045699d  e92be3ffff               jmp 0x454ccd
004569a2  3c0a                     cmp al, 0xa
004569a4  760b                     jbe 0x4569b1
004569a6  3c11                     cmp al, 0x11
004569a8  74ad                     je 0x456957
004569aa  e91ee3ffff               jmp 0x454ccd
004569af  3c04                     cmp al, 4
004569b1  b824000000               mov eax, 0x24
004569b6  b9c8000000               mov ecx, 0xc8
004569bb  31d2                     xor edx, edx
004569bd  e81a9b0100               call 0x4704dc ; -> Random
004569c2  f7f1                     div ecx
004569c4  85d2                     test edx, edx
004569c6  0f8501e3ffff             jne 0x454ccd
004569cc  8a9391000000             mov dl, byte ptr [ebx + 0x91]
004569d2  b910000000               mov ecx, 0x10
004569d7  89d0                     mov eax, edx
004569d9  c1fa1f                   sar edx, 0x1f
004569dc  f7f9                     idiv ecx
004569de  42                       inc edx
004569df  889390000000             mov byte ptr [ebx + 0x90], dl
004569e5  889391000000             mov byte ptr [ebx + 0x91], dl
004569eb  e9dde2ffff               jmp 0x454ccd
004569f0  b001                     mov al, 1
004569f2  84c0                     test al, al
004569f4  0f8535010000             jne 0x456b2f
004569fa  31c0                     xor eax, eax
004569fc  8a86a4000000             mov al, byte ptr [esi + 0xa4]
00456a02  85c0                     test eax, eax
00456a04  7532                     jne 0x456a38
00456a06  31db                     xor ebx, ebx
00456a08  6689fb                   mov bx, di
00456a0b  89d8                     mov eax, ebx
00456a0d  31d2                     xor edx, edx
00456a0f  e834bc0100               call 0x472648 ; -> DeselectionEngin
00456a14  89d8                     mov eax, ebx
00456a16  668b5608                 mov dx, word ptr [esi + 8]
00456a1a  e88dc4feff               call 0x442eac ; -> ResetEnginCollision
00456a1f  668b4608                 mov ax, word ptr [esi + 8]
00456a23  668b4e7c                 mov cx, word ptr [esi + 0x7c]
00456a27  6639c8                   cmp ax, cx
00456a2a  740c                     je 0x456a38
00456a2c  31d2                     xor edx, edx
00456a2e  89d8                     mov eax, ebx
00456a30  6689ca                   mov dx, cx
00456a33  e874c4feff               call 0x442eac ; -> ResetEnginCollision
00456a38  31d2                     xor edx, edx
00456a3a  6689fa                   mov dx, di
00456a3d  89d0                     mov eax, edx
00456a3f  c1e004                   shl eax, 4
00456a42  01d0                     add eax, edx
00456a44  c1e002                   shl eax, 2
00456a47  01d0                     add eax, edx
00456a49  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00456a4f  c1e002                   shl eax, 2
00456a52  01c3                     add ebx, eax
00456a54  31c9                     xor ecx, ecx
00456a56  31d2                     xor edx, edx
00456a58  8a8bdb000000             mov cl, byte ptr [ebx + 0xdb]
00456a5e  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
00456a64  8d41ff                   lea eax, [ecx - 1]
00456a67  39c2                     cmp edx, eax
00456a69  740e                     je 0x456a79
00456a6b  42                       inc edx
00456a6c  89d0                     mov eax, edx
00456a6e  c1fa1f                   sar edx, 0x1f
00456a71  f7f9                     idiv ecx
00456a73  8893a4000000             mov byte ptr [ebx + 0xa4], dl
00456a79  66ff86c2000000           inc word ptr [esi + 0xc2]
00456a80  31c0                     xor eax, eax
00456a82  668b86c2000000           mov ax, word ptr [esi + 0xc2]
00456a89  3d4a010000               cmp eax, 0x14a
00456a8e  0f8c39e2ffff             jl 0x454ccd
00456a94  31db                     xor ebx, ebx
00456a96  6689fb                   mov bx, di
00456a99  89d8                     mov eax, ebx
00456a9b  c1e004                   shl eax, 4
00456a9e  01d8                     add eax, ebx
00456aa0  c1e002                   shl eax, 2
00456aa3  8d1403                   lea edx, [ebx + eax]
00456aa6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456aab  c1e202                   shl edx, 2
00456aae  8d0c10                   lea ecx, [eax + edx]
00456ab1  89d8                     mov eax, ebx
00456ab3  e890bb0100               call 0x472648 ; -> DeselectionEngin
00456ab8  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456abd  01d0                     add eax, edx
00456abf  897c2414                 mov dword ptr [esp + 0x14], edi
00456ac3  8d580a                   lea ebx, [eax + 0xa]
00456ac6  668b03                   mov ax, word ptr [ebx]
00456ac9  25ffff0000               and eax, 0xffff
00456ace  7443                     je 0x456b13
00456ad0  31c0                     xor eax, eax
00456ad2  31d2                     xor edx, edx
00456ad4  6689f8                   mov ax, di
00456ad7  e820d3feff               call 0x443dfc ; -> EnginRetire
00456adc  ebe8                     jmp 0x456ac6
00456ade  30c0                     xor al, al
00456ae0  e90dffffff               jmp 0x4569f2
00456ae5  31d2                     xor edx, edx
00456ae7  6689fa                   mov dx, di
00456aea  89d0                     mov eax, edx
00456aec  c1e004                   shl eax, 4
00456aef  01d0                     add eax, edx
00456af1  c1e002                   shl eax, 2
00456af4  01d0                     add eax, edx
00456af6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00456afc  8a448201                 mov al, byte ptr [edx + eax*4 + 1]
00456b00  2c0b                     sub al, 0xb
00456b02  3c06                     cmp al, 6
00456b04  77d8                     ja 0x456ade
00456b06  25ff000000               and eax, 0xff
00456b0b  2eff2485ac434500         jmp dword ptr cs:[eax*4 + 0x4543ac]
00456b13  668b442414               mov ax, word ptr [esp + 0x14]
00456b18  e83b050000               call 0x457058 ; -> RetireEngin
00456b1d  66c7819a0000000000       mov word ptr [ecx + 0x9a], 0
00456b26  c6460200                 mov byte ptr [esi + 2], 0
00456b2a  e99ee1ffff               jmp 0x454ccd
00456b2f  31d2                     xor edx, edx
00456b31  6689fa                   mov dx, di
00456b34  89d3                     mov ebx, edx
00456b36  c1e304                   shl ebx, 4
00456b39  01d3                     add ebx, edx
00456b3b  c1e302                   shl ebx, 2
00456b3e  01d3                     add ebx, edx
00456b40  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456b45  c1e302                   shl ebx, 2
00456b48  8a8403dc000000           mov al, byte ptr [ebx + eax + 0xdc]
00456b4f  ba02000000               mov edx, 2
00456b54  25ff000000               and eax, 0xff
00456b59  e839120100               call 0x467d97 ; -> GetBit
00456b5e  84c0                     test al, al
00456b60  7555                     jne 0x456bb7
00456b62  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456b67  31d2                     xor edx, edx
00456b69  8a440301                 mov al, byte ptr [ebx + eax + 1]
00456b6d  88c2                     mov dl, al
00456b6f  89d0                     mov eax, edx
00456b71  c1e002                   shl eax, 2
00456b74  29d0                     sub eax, edx
00456b76  c1e003                   shl eax, 3
00456b79  01c2                     add edx, eax
00456b7b  01d2                     add edx, edx
00456b7d  668b82b0654900           mov ax, word ptr [edx + 0x4965b0]
00456b84  8944241c                 mov dword ptr [esp + 0x1c], eax
00456b88  668b82b4654900           mov ax, word ptr [edx + 0x4965b4]
00456b8f  8944241c                 mov dword ptr [esp + 0x1c], eax
00456b93  668b82b2654900           mov ax, word ptr [edx + 0x4965b2]
00456b9a  31db                     xor ebx, ebx
00456b9c  89442420                 mov dword ptr [esp + 0x20], eax
00456ba0  eb0e                     jmp 0x456bb0
00456ba2  31c0                     xor eax, eax
00456ba4  31d2                     xor edx, edx
00456ba6  668b4608                 mov ax, word ptr [esi + 8]
00456baa  43                       inc ebx
00456bab  e8adf40100               call 0x47605d ; -> CreerSac
00456bb0  663b5c2420               cmp bx, word ptr [esp + 0x20]
00456bb5  72eb                     jb 0x456ba2
00456bb7  31d2                     xor edx, edx
00456bb9  6689fa                   mov dx, di
00456bbc  89d0                     mov eax, edx
00456bbe  c1e004                   shl eax, 4
00456bc1  01d0                     add eax, edx
00456bc3  c1e002                   shl eax, 2
00456bc6  8d1c02                   lea ebx, [edx + eax]
00456bc9  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456bce  c1e302                   shl ebx, 2
00456bd1  01d8                     add eax, ebx
00456bd3  89442408                 mov dword ptr [esp + 8], eax
00456bd7  89d0                     mov eax, edx
00456bd9  e86aba0100               call 0x472648 ; -> DeselectionEngin
00456bde  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00456be3  01c3                     add ebx, eax
00456be5  89f9                     mov ecx, edi
00456be7  83c30a                   add ebx, 0xa
00456bea  668b03                   mov ax, word ptr [ebx]
00456bed  25ffff0000               and eax, 0xffff
00456bf2  740e                     je 0x456c02
00456bf4  31c0                     xor eax, eax
00456bf6  31d2                     xor edx, edx
00456bf8  6689f8                   mov ax, di
00456bfb  e8fcd1feff               call 0x443dfc ; -> EnginRetire
00456c00  ebe8                     jmp 0x456bea
00456c02  6689c8                   mov ax, cx
00456c05  e84e040000               call 0x457058 ; -> RetireEngin
00456c0a  8b442408                 mov eax, dword ptr [esp + 8]
00456c0e  66c7809a0000000000       mov word ptr [eax + 0x9a], 0
00456c17  e90affffff               jmp 0x456b26
00456c1c  8a4602                   mov al, byte ptr [esi + 2]
00456c1f  3c18                     cmp al, 0x18
00456c21  0f87a6e0ffff             ja 0x454ccd
00456c27  25ff000000               and eax, 0xff
00456c2c  2eff2485c8434500         jmp dword ptr cs:[eax*4 + 0x4543c8]

; shared Watcom tail reached from EnginNextEtape; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00440d58..0x00440d5e (end exclusive); labels are original SBL names
00440d58  5f                       pop edi
00440d59  5e                       pop esi
00440d5a  5a                       pop edx
00440d5b  59                       pop ecx
00440d5c  5b                       pop ebx
00440d5d  c3                       ret

; shared Watcom tail reached from EnginNextEtape; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0044f29d..0x0044f2a3 (end exclusive); labels are original SBL names
0044f29d  5d                       pop ebp
0044f29e  e9b51affff               jmp 0x440d58
