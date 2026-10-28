; CalculBatimentNextEtape (structure-dispatch); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004281c7..0x004283e2 (end exclusive); labels are original SBL names
004281c7  53                       push ebx
004281c8  51                       push ecx
004281c9  52                       push edx
004281ca  56                       push esi
004281cb  57                       push edi
004281cc  55                       push ebp
004281cd  83ec08                   sub esp, 8
004281d0  e85e9c0300               call 0x461e33 ; -> ResetTableauHangar
004281d5  a17c8f5000               mov eax, dword ptr [0x508f7c]
004281da  31db                     xor ebx, ebx
004281dc  31d2                     xor edx, edx
004281de  668b1d025c4900           mov bx, word ptr [0x495c02]
004281e5  f7f3                     div ebx
004281e7  85d2                     test edx, edx
004281e9  7508                     jne 0x4281f3
004281eb  30e4                     xor ah, ah
004281ed  88259bfb4d00             mov byte ptr [0x4dfb9b], ah
004281f3  31c0                     xor eax, eax
004281f5  eb0a                     jmp 0x428201
004281f7  31d2                     xor edx, edx
004281f9  40                       inc eax
004281fa  89149da8fa4d00           mov dword ptr [ebx*4 + 0x4dfaa8], edx
00428201  31db                     xor ebx, ebx
00428203  6689c3                   mov bx, ax
00428206  83fb04                   cmp ebx, 4
00428209  7cec                     jl 0x4281f7
0042820b  31d2                     xor edx, edx
0042820d  89542404                 mov dword ptr [esp + 4], edx
00428211  bd01000000               mov ebp, 1
00428216  eb04                     jmp 0x42821c
00428218  ff442404                 inc dword ptr [esp + 4]
0042821c  31c0                     xor eax, eax
0042821e  668b442404               mov ax, word ptr [esp + 4]
00428223  3de8030000               cmp eax, 0x3e8
00428228  0f8da7010000             jge 0x4283d5
0042822e  69c014010000             imul eax, eax, 0x114
00428234  05c8a04900               add eax, 0x49a0c8
00428239  8a4005                   mov al, byte ptr [eax + 5]
0042823c  25ff000000               and eax, 0xff
00428241  0f95c0                   setne al
00428244  84c0                     test al, al
00428246  74d0                     je 0x428218
00428248  31c0                     xor eax, eax
0042824a  668b442404               mov ax, word ptr [esp + 4]
0042824f  69c014010000             imul eax, eax, 0x114
00428255  05c8a04900               add eax, 0x49a0c8
0042825a  8a5804                   mov bl, byte ptr [eax + 4]
0042825d  8a4008                   mov al, byte ptr [eax + 8]
00428260  81e3ff000000             and ebx, 0xff
00428266  83fb04                   cmp ebx, 4
00428269  7d25                     jge 0x428290
0042826b  25ff000000               and eax, 0xff
00428270  83f809                   cmp eax, 9
00428273  741b                     je 0x428290
00428275  83f80c                   cmp eax, 0xc
00428278  7416                     je 0x428290
0042827a  83f811                   cmp eax, 0x11
0042827d  7411                     je 0x428290
0042827f  89d8                     mov eax, ebx
00428281  8b1c9da8fa4d00           mov ebx, dword ptr [ebx*4 + 0x4dfaa8]
00428288  43                       inc ebx
00428289  891c85a8fa4d00           mov dword ptr [eax*4 + 0x4dfaa8], ebx
00428290  31c0                     xor eax, eax
00428292  668b442404               mov ax, word ptr [esp + 4]
00428297  69c014010000             imul eax, eax, 0x114
0042829d  05c8a04900               add eax, 0x49a0c8
004282a2  8a4005                   mov al, byte ptr [eax + 5]
004282a5  25ff000000               and eax, 0xff
004282aa  83f803                   cmp eax, 3
004282ad  0f94c0                   sete al
004282b0  84c0                     test al, al
004282b2  7411                     je 0x4282c5
004282b4  31c0                     xor eax, eax
004282b6  668b442404               mov ax, word ptr [esp + 4]
004282bb  e83d6dffff               call 0x41effd ; -> DemonteBatiment
004282c0  e953ffffff               jmp 0x428218
004282c5  31db                     xor ebx, ebx
004282c7  668b5c2404               mov bx, word ptr [esp + 4]
004282cc  b803000000               mov eax, 3
004282d1  89da                     mov edx, ebx
004282d3  e825790500               call 0x47fbfd ; -> IATestUtilite
004282d8  89d8                     mov eax, ebx
004282da  e8f5e5ffff               call 0x4268d4 ; -> BatimentNextEtape
004282df  89d8                     mov eax, ebx
004282e1  e8fc2bffff               call 0x41aee2 ; -> BatimentGetCase
004282e6  31db                     xor ebx, ebx
004282e8  89c7                     mov edi, eax
004282ea  66891c24                 mov word ptr [esp], bx
004282ee  eb04                     jmp 0x4282f4
004282f0  66ff0424                 inc word ptr [esp]
004282f4  31c0                     xor eax, eax
004282f6  668b0424                 mov ax, word ptr [esp]
004282fa  83f804                   cmp eax, 4
004282fd  7d4d                     jge 0x42834c
004282ff  31f6                     xor esi, esi
00428301  668b742404               mov si, word ptr [esp + 4]
00428306  69de14010000             imul ebx, esi, 0x114
0042830c  81c3c8a04900             add ebx, 0x49a0c8
00428312  8a5b04                   mov bl, byte ptr [ebx + 4]
00428315  81e3ff000000             and ebx, 0xff
0042831b  39c3                     cmp ebx, eax
0042831d  74d1                     je 0x4282f0
0042831f  31c9                     xor ecx, ecx
00428321  31c0                     xor eax, eax
00428323  8a0c24                   mov cl, byte ptr [esp]
00428326  6689f8                   mov ax, di
00428329  89ca                     mov edx, ecx
0042832b  e8a6e30400               call 0x4766d6 ; -> CaseEstDecouverte
00428330  84c0                     test al, al
00428332  75bc                     jne 0x4282f0
00428334  89ca                     mov edx, ecx
00428336  89f0                     mov eax, esi
00428338  e81219ffff               call 0x419c4f ; -> BatimentEstDecouvert
0042833d  84c0                     test al, al
0042833f  74af                     je 0x4282f0
00428341  89ca                     mov edx, ecx
00428343  89f0                     mov eax, esi
00428345  e80a1affff               call 0x419d54 ; -> BatimentDecouvre
0042834a  eba4                     jmp 0x4282f0
0042834c  31c9                     xor ecx, ecx
0042834e  66890c24                 mov word ptr [esp], cx
00428352  eb20                     jmp 0x428374
00428354  80b9d8a1490000           cmp byte ptr [ecx + 0x49a1d8], 0
0042835b  7413                     je 0x428370
0042835d  89fa                     mov edx, edi
0042835f  89f0                     mov eax, esi
00428361  31db                     xor ebx, ebx
00428363  e8cb0effff               call 0x419233 ; -> BatimentIllumine
00428368  30f6                     xor dh, dh
0042836a  88b1d8a14900             mov byte ptr [ecx + 0x49a1d8], dh
00428370  66ff0424                 inc word ptr [esp]
00428374  31c9                     xor ecx, ecx
00428376  668b0c24                 mov cx, word ptr [esp]
0042837a  83f904                   cmp ecx, 4
0042837d  0f8d95feffff             jge 0x428218
00428383  31f6                     xor esi, esi
00428385  668b742404               mov si, word ptr [esp + 4]
0042838a  69de14010000             imul ebx, esi, 0x114
00428390  bfc8a04900               mov edi, 0x49a0c8
00428395  8a441f04                 mov al, byte ptr [edi + ebx + 4]
00428399  25ff000000               and eax, 0xff
0042839e  39c8                     cmp eax, ecx
004283a0  74ce                     je 0x428370
004283a2  0fb63c24                 movzx edi, byte ptr [esp]
004283a6  89f0                     mov eax, esi
004283a8  89fa                     mov edx, edi
004283aa  01d9                     add ecx, ebx
004283ac  e84816ffff               call 0x4199f9 ; -> BatimentContourEstIllumine
004283b1  84c0                     test al, al
004283b3  749f                     je 0x428354
004283b5  80b9d8a1490000           cmp byte ptr [ecx + 0x49a1d8], 0
004283bc  75b2                     jne 0x428370
004283be  bb01000000               mov ebx, 1
004283c3  89fa                     mov edx, edi
004283c5  89f0                     mov eax, esi
004283c7  e8670effff               call 0x419233 ; -> BatimentIllumine
004283cc  c681d8a1490001           mov byte ptr [ecx + 0x49a1d8], 1
004283d3  eb9b                     jmp 0x428370
004283d5  30c9                     xor cl, cl
004283d7  880d50fb4d00             mov byte ptr [0x4dfb50], cl
004283dd  e93857ffff               jmp 0x41db1a

; shared Watcom tail reached from CalculBatimentNextEtape; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0041db1a..0x0041db24 (end exclusive); labels are original SBL names
0041db1a  83c408                   add esp, 8
0041db1d  5d                       pop ebp
0041db1e  5f                       pop edi
0041db1f  5e                       pop esi
0041db20  5a                       pop edx
0041db21  59                       pop ecx
0041db22  5b                       pop ebx
0041db23  c3                       ret
