; TestFinDeMission_NOT_IMPLEMENTED; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00458606  53                       push ebx
00458607  51                       push ecx
00458608  52                       push edx
00458609  56                       push esi
0045860a  57                       push edi
0045860b  55                       push ebp
0045860c  83ec14                   sub esp, 0x14
0045860f  8844240c                 mov byte ptr [esp + 0xc], al
00458613  b401                     mov ah, 1
00458615  31f6                     xor esi, esi
00458617  88642410                 mov byte ptr [esp + 0x10], ah
0045861b  e9cd000000               jmp 0x4586ed
00458620  85ff                     test edi, edi
00458622  0f85c4000000             jne 0x4586ec
00458628  80bf881d4e0000           cmp byte ptr [edi + 0x4e1d88], 0
0045862f  7408                     je 0x458639
00458631  30e4                     xor ah, ah
00458633  88a7881d4e00             mov byte ptr [edi + 0x4e1d88], ah
00458639  30d2                     xor dl, dl
0045863b  88542410                 mov byte ptr [esp + 0x10], dl
0045863f  e9a8000000               jmp 0x4586ec
00458644  31d2                     xor edx, edx
00458646  8a54240c                 mov dl, byte ptr [esp + 0xc]
0045864a  668b80221d4e00           mov ax, word ptr [eax + 0x4e1d22]
00458651  52                       push edx
00458652  25ffff0000               and eax, 0xffff
00458657  31c9                     xor ecx, ecx
00458659  31db                     xor ebx, ebx
0045865b  31d2                     xor edx, edx
0045865d  e883f00000               call 0x4676e5
00458662  84c0                     test al, al
00458664  7525                     jne 0x45868b
00458666  88442410                 mov byte ptr [esp + 0x10], al
0045866a  31c0                     xor eax, eax
0045866c  6689f0                   mov ax, si
0045866f  80b8881d4e0000           cmp byte ptr [eax + 0x4e1d88], 0
00458676  0f8470000000             je 0x4586ec
0045867c  31c0                     xor eax, eax
0045867e  6689f0                   mov ax, si
00458681  30ff                     xor bh, bh
00458683  88b8881d4e00             mov byte ptr [eax + 0x4e1d88], bh
00458689  eb61                     jmp 0x4586ec
0045868b  31c0                     xor eax, eax
0045868d  6689f0                   mov ax, si
00458690  80b8881d4e0000           cmp byte ptr [eax + 0x4e1d88], 0
00458697  7553                     jne 0x4586ec
00458699  31c0                     xor eax, eax
0045869b  6689f0                   mov ax, si
0045869e  c680881d4e0001           mov byte ptr [eax + 0x4e1d88], 1
004586a5  eb45                     jmp 0x4586ec
004586a7  31d2                     xor edx, edx
004586a9  8a54240c                 mov dl, byte ptr [esp + 0xc]
004586ad  31c9                     xor ecx, ecx
004586af  52                       push edx
004586b0  31d2                     xor edx, edx
004586b2  31db                     xor ebx, ebx
004586b4  668b90221d4e00           mov dx, word ptr [eax + 0x4e1d22]
004586bb  31c0                     xor eax, eax
004586bd  e823f00000               call 0x4676e5
004586c2  84c0                     test al, al
004586c4  7516                     jne 0x4586dc
004586c6  8aaf881d4e00             mov ch, byte ptr [edi + 0x4e1d88]
004586cc  88442410                 mov byte ptr [esp + 0x10], al
004586d0  84ed                     test ch, ch
004586d2  7418                     je 0x4586ec
004586d4  8887881d4e00             mov byte ptr [edi + 0x4e1d88], al
004586da  eb10                     jmp 0x4586ec
004586dc  80bf881d4e0000           cmp byte ptr [edi + 0x4e1d88], 0
004586e3  7507                     jne 0x4586ec
004586e5  c687881d4e0001           mov byte ptr [edi + 0x4e1d88], 1
004586ec  46                       inc esi
004586ed  31ff                     xor edi, edi
004586ef  6689f7                   mov di, si
004586f2  83ff0a                   cmp edi, 0xa
004586f5  0f8c53020000             jl 0x45894e
004586fb  e81a3a0100               call 0x46c11a
00458700  25ffff0000               and eax, 0xffff
00458705  83f806                   cmp eax, 6
00458708  751b                     jne 0x458725
0045870a  31c0                     xor eax, eax
0045870c  31d2                     xor edx, edx
0045870e  e8013a0200               call 0x47c114
00458713  8a54240c                 mov dl, byte ptr [esp + 0xc]
00458717  25ffff0000               and eax, 0xffff
0045871c  e819e20100               call 0x47693a
00458721  88442410                 mov byte ptr [esp + 0x10], al
00458725  807c241000               cmp byte ptr [esp + 0x10], 0
0045872a  7407                     je 0x458733
0045872c  c605841d4e0001           mov byte ptr [0x4e1d84], 1
00458733  31c0                     xor eax, eax
00458735  66a13a1a4e00             mov ax, word ptr [0x4e1a3a]
0045873b  85c0                     test eax, eax
0045873d  750d                     jne 0x45874c
0045873f  c644241001               mov byte ptr [esp + 0x10], 1
00458744  30ff                     xor bh, bh
00458746  883d841d4e00             mov byte ptr [0x4e1d84], bh
0045874c  807c241000               cmp byte ptr [esp + 0x10], 0
00458751  0f8481030000             je 0x458ad8
00458757  803d841d4e0000           cmp byte ptr [0x4e1d84], 0
0045875e  0f8474030000             je 0x458ad8
00458764  e8b1390100               call 0x46c11a
00458769  25ffff0000               and eax, 0xffff
0045876e  83f808                   cmp eax, 8
00458771  7413                     je 0x458786
00458773  e8a2390100               call 0x46c11a
00458778  25ffff0000               and eax, 0xffff
0045877d  83f80d                   cmp eax, 0xd
00458780  0f8552030000             jne 0x458ad8
00458786  31c0                     xor eax, eax
00458788  e945020000               jmp 0x4589d2
0045878d  31d2                     xor edx, edx
0045878f  668b90221d4e00           mov dx, word ptr [eax + 0x4e1d22]
00458796  31c0                     xor eax, eax
00458798  8a44240c                 mov al, byte ptr [esp + 0xc]
0045879c  e8b37d0100               call 0x470554
004587a1  25ff000000               and eax, 0xff
004587a6  39d0                     cmp eax, edx
004587a8  0f8d2effffff             jge 0x4586dc
004587ae  30c9                     xor cl, cl
004587b0  884c2410                 mov byte ptr [esp + 0x10], cl
004587b4  80bf881d4e0000           cmp byte ptr [edi + 0x4e1d88], 0
004587bb  0f842bffffff             je 0x4586ec
004587c1  888f881d4e00             mov byte ptr [edi + 0x4e1d88], cl
004587c7  e920ffffff               jmp 0x4586ec
004587cc  31f7                     xor edi, esi
004587ce  eb1b                     jmp 0x4587eb
004587d0  31d2                     xor edx, edx
004587d2  6689f2                   mov dx, si
004587d5  8aaa881d4e00             mov ch, byte ptr [edx + 0x4e1d88]
004587db  89742408                 mov dword ptr [esp + 8], esi
004587df  84ed                     test ch, ch
004587e1  7507                     jne 0x4587ea
004587e3  c682881d4e0001           mov byte ptr [edx + 0x4e1d88], 1
004587ea  47                       inc edi
004587eb  31db                     xor ebx, ebx
004587ed  6689fb                   mov bx, di
004587f0  81fbe8030000             cmp ebx, 0x3e8
004587f6  0f8dc6000000             jge 0x4588c2
004587fc  89d8                     mov eax, ebx
004587fe  e8321ffcff               call 0x41a735
00458803  84c0                     test al, al
00458805  74e3                     je 0x4587ea
00458807  89d8                     mov eax, ebx
00458809  8a4c240c                 mov cl, byte ptr [esp + 0xc]
0045880d  e87a18fcff               call 0x41a08c
00458812  38c8                     cmp al, cl
00458814  75d4                     jne 0x4587ea
00458816  31c9                     xor ecx, ecx
00458818  6689f1                   mov cx, si
0045881b  6bd10a                   imul edx, ecx, 0xa
0045881e  31c0                     xor eax, eax
00458820  668b82221d4e00           mov ax, word ptr [edx + 0x4e1d22]
00458827  890424                   mov dword ptr [esp], eax
0045882a  89d8                     mov eax, ebx
0045882c  e8c31cfcff               call 0x41a4f4
00458831  8b2c24                   mov ebp, dword ptr [esp]
00458834  25ff000000               and eax, 0xff
00458839  39e8                     cmp eax, ebp
0045883b  75ad                     jne 0x4587ea
0045883d  89d8                     mov eax, ebx
0045883f  e89e26fcff               call 0x41aee2
00458844  25ffff0000               and eax, 0xffff
00458849  31db                     xor ebx, ebx
0045884b  e816370200               call 0x47bf66
00458850  668b9a241d4e00           mov bx, word ptr [edx + 0x4e1d24]
00458857  81fbff000000             cmp ebx, 0xff
0045885d  0f846dffffff             je 0x4587d0
00458863  6639d8                   cmp ax, bx
00458866  0f8464ffffff             je 0x4587d0
0045886c  31db                     xor ebx, ebx
0045886e  668b9a261d4e00           mov bx, word ptr [edx + 0x4e1d26]
00458875  81fbff000000             cmp ebx, 0xff
0045887b  0f844fffffff             je 0x4587d0
00458881  6639d8                   cmp ax, bx
00458884  0f8446ffffff             je 0x4587d0
0045888a  31db                     xor ebx, ebx
0045888c  668b9a281d4e00           mov bx, word ptr [edx + 0x4e1d28]
00458893  81fbff000000             cmp ebx, 0xff
00458899  0f8431ffffff             je 0x4587d0
0045889f  6639d8                   cmp ax, bx
004588a2  0f8428ffffff             je 0x4587d0
004588a8  80b9881d4e0000           cmp byte ptr [ecx + 0x4e1d88], 0
004588af  0f8435ffffff             je 0x4587ea
004588b5  30d2                     xor dl, dl
004588b7  8891881d4e00             mov byte ptr [ecx + 0x4e1d88], dl
004588bd  e928ffffff               jmp 0x4587ea
004588c2  31c0                     xor eax, eax
004588c4  6689f0                   mov ax, si
004588c7  8ab0881d4e00             mov dh, byte ptr [eax + 0x4e1d88]
004588cd  84f6                     test dh, dh
004588cf  0f8517feffff             jne 0x4586ec
004588d5  88742410                 mov byte ptr [esp + 0x10], dh
004588d9  e90efeffff               jmp 0x4586ec
004588de  b601                     mov dh, 1
004588e0  31c9                     xor ecx, ecx
004588e2  88b7881d4e00             mov byte ptr [edi + 0x4e1d88], dh
004588e8  eb01                     jmp 0x4588eb
004588ea  41                       inc ecx
004588eb  31db                     xor ebx, ebx
004588ed  6689cb                   mov bx, cx
004588f0  83fb04                   cmp ebx, 4
004588f3  7d3f                     jge 0x458934
004588f5  31c0                     xor eax, eax
004588f7  8a44240c                 mov al, byte ptr [esp + 0xc]
004588fb  39c3                     cmp ebx, eax
004588fd  74eb                     je 0x4588ea
004588ff  31d2                     xor edx, edx
00458901  88ca                     mov dl, cl
00458903  e8304f0100               call 0x46d838
00458908  84c0                     test al, al
0045890a  75de                     jne 0x4588ea
0045890c  668b045d28194e00         mov ax, word ptr [ebx*2 + 0x4e1928]
00458914  25ffff0000               and eax, 0xffff
00458919  750a                     jne 0x458925
0045891b  833c9da8fa4d0000         cmp dword ptr [ebx*4 + 0x4dfaa8], 0
00458923  74c5                     je 0x4588ea
00458925  31c0                     xor eax, eax
00458927  6689f0                   mov ax, si
0045892a  30d2                     xor dl, dl
0045892c  8890881d4e00             mov byte ptr [eax + 0x4e1d88], dl
00458932  ebb6                     jmp 0x4588ea
00458934  31c0                     xor eax, eax
00458936  6689f0                   mov ax, si
00458939  8a4c2410                 mov cl, byte ptr [esp + 0x10]
0045893d  8a80881d4e00             mov al, byte ptr [eax + 0x4e1d88]
00458943  20c1                     and cl, al
00458945  884c2410                 mov byte ptr [esp + 0x10], cl
00458949  e99efdffff               jmp 0x4586ec
0045894e  6bc70a                   imul eax, edi, 0xa
00458951  8a90201d4e00             mov dl, byte ptr [eax + 0x4e1d20]
00458957  80fa03                   cmp dl, 3
0045895a  7223                     jb 0x45897f
0045895c  0f862bfeffff             jbe 0x45878d
00458962  80fa05                   cmp dl, 5
00458965  0f8261feffff             jb 0x4587cc
0045896b  0f866dffffff             jbe 0x4588de
00458971  80faff                   cmp dl, 0xff
00458974  0f84a6fcffff             je 0x458620
0045897a  e96dfdffff               jmp 0x4586ec
0045897f  80fa01                   cmp dl, 1
00458982  723a                     jb 0x4589be
00458984  0f861dfdffff             jbe 0x4586a7
0045898a  31d2                     xor edx, edx
0045898c  31db                     xor ebx, ebx
0045898e  31c9                     xor ecx, ecx
00458990  8a54240c                 mov dl, byte ptr [esp + 0xc]
00458994  668b98221d4e00           mov bx, word ptr [eax + 0x4e1d22]
0045899b  52                       push edx
0045899c  31c0                     xor eax, eax
0045899e  31d2                     xor edx, edx
004589a0  e840ed0000               call 0x4676e5
004589a5  84c0                     test al, al
004589a7  0f852ffdffff             jne 0x4586dc
004589ad  8a97881d4e00             mov dl, byte ptr [edi + 0x4e1d88]
004589b3  88442410                 mov byte ptr [esp + 0x10], al
004589b7  84d2                     test dl, dl
004589b9  e914fdffff               jmp 0x4586d2
004589be  84d2                     test dl, dl
004589c0  0f847efcffff             je 0x458644
004589c6  e921fdffff               jmp 0x4586ec
004589cb  30d2                     xor dl, dl
004589cd  40                       inc eax
004589ce  88540c04                 mov byte ptr [esp + ecx + 4], dl
004589d2  31c9                     xor ecx, ecx
004589d4  6689c1                   mov cx, ax
004589d7  83f904                   cmp ecx, 4
004589da  7cef                     jl 0x4589cb
004589dc  8b742408                 mov esi, dword ptr [esp + 8]
004589e0  31c1                     xor ecx, eax
004589e2  eb01                     jmp 0x4589e5
004589e4  41                       inc ecx
004589e5  31db                     xor ebx, ebx
004589e7  6689cb                   mov bx, cx
004589ea  81fbe8030000             cmp ebx, 0x3e8
004589f0  0f8dbc000000             jge 0x458ab2
004589f6  89d8                     mov eax, ebx
004589f8  e8381dfcff               call 0x41a735
004589fd  84c0                     test al, al
004589ff  74e3                     je 0x4589e4
00458a01  89d8                     mov eax, ebx
00458a03  e88416fcff               call 0x41a08c
00458a08  3a44240c                 cmp al, byte ptr [esp + 0xc]
00458a0c  74d6                     je 0x4589e4
00458a0e  89d8                     mov eax, ebx
00458a10  e87716fcff               call 0x41a08c
00458a15  25ff000000               and eax, 0xff
00458a1a  3dc8000000               cmp eax, 0xc8
00458a1f  74c3                     je 0x4589e4
00458a21  31d2                     xor edx, edx
00458a23  6689f2                   mov dx, si
00458a26  6bd20a                   imul edx, edx, 0xa
00458a29  31ff                     xor edi, edi
00458a2b  89d8                     mov eax, ebx
00458a2d  668bba221d4e00           mov di, word ptr [edx + 0x4e1d22]
00458a34  e8bb1afcff               call 0x41a4f4
00458a39  25ff000000               and eax, 0xff
00458a3e  39f8                     cmp eax, edi
00458a40  75a2                     jne 0x4589e4
00458a42  89d8                     mov eax, ebx
00458a44  e89924fcff               call 0x41aee2
00458a49  25ffff0000               and eax, 0xffff
00458a4e  31db                     xor ebx, ebx
00458a50  e811350200               call 0x47bf66
00458a55  668b9a241d4e00           mov bx, word ptr [edx + 0x4e1d24]
00458a5c  81fbff000000             cmp ebx, 0xff
00458a62  7435                     je 0x458a99
00458a64  6639d8                   cmp ax, bx
00458a67  7430                     je 0x458a99
00458a69  31db                     xor ebx, ebx
00458a6b  668b9a261d4e00           mov bx, word ptr [edx + 0x4e1d26]
00458a72  81fbff000000             cmp ebx, 0xff
00458a78  741f                     je 0x458a99
00458a7a  6639d8                   cmp ax, bx
00458a7d  741a                     je 0x458a99
00458a7f  31db                     xor ebx, ebx
00458a81  668b9a281d4e00           mov bx, word ptr [edx + 0x4e1d28]
00458a88  81fbff000000             cmp ebx, 0xff
00458a8e  7409                     je 0x458a99
00458a90  6639d8                   cmp ax, bx
00458a93  0f854bffffff             jne 0x4589e4
00458a99  31c0                     xor eax, eax
00458a9b  6689c8                   mov ax, cx
00458a9e  e8e915fcff               call 0x41a08c
00458aa3  25ff000000               and eax, 0xff
00458aa8  c644040401               mov byte ptr [esp + eax + 4], 1
00458aad  e932ffffff               jmp 0x4589e4
00458ab2  30f6                     xor dh, dh
00458ab4  8835851d4e00             mov byte ptr [0x4e1d85], dh
00458aba  30d2                     xor dl, dl
00458abc  eb01                     jmp 0x458abf
00458abe  42                       inc edx
00458abf  31c0                     xor eax, eax
00458ac1  6689d0                   mov ax, dx
00458ac4  83f804                   cmp eax, 4
00458ac7  7d0f                     jge 0x458ad8
00458ac9  807c040400               cmp byte ptr [esp + eax + 4], 0
00458ace  74ee                     je 0x458abe
00458ad0  fe05851d4e00             inc byte ptr [0x4e1d85]
00458ad6  ebe6                     jmp 0x458abe
00458ad8  8a442410                 mov al, byte ptr [esp + 0x10]
00458adc  83c414                   add esp, 0x14
00458adf  5d                       pop ebp
00458ae0  5f                       pop edi
00458ae1  5e                       pop esi
00458ae2  5a                       pop edx
00458ae3  59                       pop ecx
00458ae4  5b                       pop ebx
00458ae5  c3                       ret
