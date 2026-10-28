; BatimentNextEtape (structure-dispatch); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004268d4..0x004281c7 (end exclusive); labels are original SBL names
004268d4  53                       push ebx
004268d5  51                       push ecx
004268d6  52                       push edx
004268d7  56                       push esi
004268d8  57                       push edi
004268d9  55                       push ebp
004268da  89e5                     mov ebp, esp
004268dc  83ec34                   sub esp, 0x34
004268df  89c7                     mov edi, eax
004268e1  31d2                     xor edx, edx
004268e3  6689c2                   mov dx, ax
004268e6  89d0                     mov eax, edx
004268e8  c1e004                   shl eax, 4
004268eb  01d0                     add eax, edx
004268ed  c1e002                   shl eax, 2
004268f0  01d0                     add eax, edx
004268f2  bec8a04900               mov esi, 0x49a0c8
004268f7  c1e002                   shl eax, 2
004268fa  01c6                     add esi, eax
004268fc  8a4608                   mov al, byte ptr [esi + 8]
004268ff  88c4                     mov ah, al
00426901  fecc                     dec ah
00426903  80fc14                   cmp ah, 0x14
00426906  0f87b4180000             ja 0x4281c0
0042690c  31db                     xor ebx, ebx
0042690e  88e3                     mov bl, ah
00426910  2eff249d80684200         jmp dword ptr cs:[ebx*4 + 0x426880]
00426918  31d2                     xor edx, edx
0042691a  6689fa                   mov dx, di
0042691d  89d0                     mov eax, edx
0042691f  c1e004                   shl eax, 4
00426922  01d0                     add eax, edx
00426924  c1e002                   shl eax, 2
00426927  01d0                     add eax, edx
00426929  bac8a04900               mov edx, 0x49a0c8
0042692e  c1e002                   shl eax, 2
00426931  01c2                     add edx, eax
00426933  31db                     xor ebx, ebx
00426935  8a4208                   mov al, byte ptr [edx + 8]
00426938  88c3                     mov bl, al
0042693a  8d420c                   lea eax, [edx + 0xc]
0042693d  83fb15                   cmp ebx, 0x15
00426940  750d                     jne 0x42694f
00426942  e803090200               call 0x44724a ; -> BagContientTroupe
00426947  84c0                     test al, al
00426949  7429                     je 0x426974
0042694b  b001                     mov al, 1
0042694d  eb27                     jmp 0x426976
0042694f  83fb02                   cmp ebx, 2
00426952  7509                     jne 0x42695d
00426954  e8f1080200               call 0x44724a ; -> BagContientTroupe
00426959  84c0                     test al, al
0042695b  75ee                     jne 0x42694b
0042695d  8d420c                   lea eax, [edx + 0xc]
00426960  bb09000000               mov ebx, 9
00426965  ba01000000               mov edx, 1
0042696a  e849080200               call 0x4471b8 ; -> BagContient
0042696f  6685c0                   test ax, ax
00426972  ebd5                     jmp 0x426949
00426974  30c0                     xor al, al
00426976  84c0                     test al, al
00426978  0f8442180000             je 0x4281c0
0042697e  31c0                     xor eax, eax
00426980  6689f8                   mov ax, di
00426983  e85ef0ffff               call 0x4259e6 ; -> CalculTroupe
00426988  e933180000               jmp 0x4281c0
0042698d  31d2                     xor edx, edx
0042698f  6689fa                   mov dx, di
00426992  89d0                     mov eax, edx
00426994  c1e004                   shl eax, 4
00426997  01d0                     add eax, edx
00426999  c1e002                   shl eax, 2
0042699c  01d0                     add eax, edx
0042699e  bac8a04900               mov edx, 0x49a0c8
004269a3  c1e002                   shl eax, 2
004269a6  01c2                     add edx, eax
004269a8  31db                     xor ebx, ebx
004269aa  8a4208                   mov al, byte ptr [edx + 8]
004269ad  88c3                     mov bl, al
004269af  8d420c                   lea eax, [edx + 0xc]
004269b2  83fb15                   cmp ebx, 0x15
004269b5  750d                     jne 0x4269c4
004269b7  e88e080200               call 0x44724a ; -> BagContientTroupe
004269bc  84c0                     test al, al
004269be  7429                     je 0x4269e9
004269c0  b001                     mov al, 1
004269c2  eb27                     jmp 0x4269eb
004269c4  83fb02                   cmp ebx, 2
004269c7  7509                     jne 0x4269d2
004269c9  e87c080200               call 0x44724a ; -> BagContientTroupe
004269ce  84c0                     test al, al
004269d0  75ee                     jne 0x4269c0
004269d2  8d420c                   lea eax, [edx + 0xc]
004269d5  bb09000000               mov ebx, 9
004269da  ba01000000               mov edx, 1
004269df  e8d4070200               call 0x4471b8 ; -> BagContient
004269e4  6685c0                   test ax, ax
004269e7  ebd5                     jmp 0x4269be
004269e9  30c0                     xor al, al
004269eb  84c0                     test al, al
004269ed  740a                     je 0x4269f9
004269ef  31c0                     xor eax, eax
004269f1  6689f8                   mov ax, di
004269f4  e8edefffff               call 0x4259e6 ; -> CalculTroupe
004269f9  31c0                     xor eax, eax
004269fb  6689f8                   mov ax, di
004269fe  e837a3ffff               call 0x420d3a ; -> AnimPorteBatiment
00426a03  e9b8170000               jmp 0x4281c0
00426a08  31d2                     xor edx, edx
00426a0a  6689fa                   mov dx, di
00426a0d  89d0                     mov eax, edx
00426a0f  c1e004                   shl eax, 4
00426a12  01d0                     add eax, edx
00426a14  c1e002                   shl eax, 2
00426a17  bbc8a04900               mov ebx, 0x49a0c8
00426a1c  01d0                     add eax, edx
00426a1e  31d2                     xor edx, edx
00426a20  c1e002                   shl eax, 2
00426a23  6689fa                   mov dx, di
00426a26  01c3                     add ebx, eax
00426a28  89d0                     mov eax, edx
00426a2a  c1e004                   shl eax, 4
00426a2d  01d0                     add eax, edx
00426a2f  c1e002                   shl eax, 2
00426a32  01d0                     add eax, edx
00426a34  c1e002                   shl eax, 2
00426a37  8945cc                   mov dword ptr [ebp - 0x34], eax
00426a3a  b8c8a04900               mov eax, 0x49a0c8
00426a3f  0345cc                   add eax, dword ptr [ebp - 0x34]
00426a42  89f9                     mov ecx, edi
00426a44  8a4008                   mov al, byte ptr [eax + 8]
00426a47  25ff000000               and eax, 0xff
00426a4c  83f815                   cmp eax, 0x15
00426a4f  7510                     jne 0x426a61
00426a51  8d430c                   lea eax, [ebx + 0xc]
00426a54  e8f1070200               call 0x44724a ; -> BagContientTroupe
00426a59  84c0                     test al, al
00426a5b  744b                     je 0x426aa8
00426a5d  b001                     mov al, 1
00426a5f  eb49                     jmp 0x426aaa
00426a61  31d2                     xor edx, edx
00426a63  6689fa                   mov dx, di
00426a66  89d0                     mov eax, edx
00426a68  c1e004                   shl eax, 4
00426a6b  01d0                     add eax, edx
00426a6d  c1e002                   shl eax, 2
00426a70  01d0                     add eax, edx
00426a72  bac8a04900               mov edx, 0x49a0c8
00426a77  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426a7b  25ff000000               and eax, 0xff
00426a80  83f802                   cmp eax, 2
00426a83  750c                     jne 0x426a91
00426a85  8d430c                   lea eax, [ebx + 0xc]
00426a88  e8bd070200               call 0x44724a ; -> BagContientTroupe
00426a8d  84c0                     test al, al
00426a8f  75cc                     jne 0x426a5d
00426a91  8d430c                   lea eax, [ebx + 0xc]
00426a94  ba01000000               mov edx, 1
00426a99  bb09000000               mov ebx, 9
00426a9e  e815070200               call 0x4471b8 ; -> BagContient
00426aa3  6685c0                   test ax, ax
00426aa6  ebb3                     jmp 0x426a5b
00426aa8  30c0                     xor al, al
00426aaa  84c0                     test al, al
00426aac  0f840e170000             je 0x4281c0
00426ab2  31d2                     xor edx, edx
00426ab4  6689fa                   mov dx, di
00426ab7  89d0                     mov eax, edx
00426ab9  e828efffff               call 0x4259e6 ; -> CalculTroupe
00426abe  89d0                     mov eax, edx
00426ac0  e875a2ffff               call 0x420d3a ; -> AnimPorteBatiment
00426ac5  807e7400                 cmp byte ptr [esi + 0x74], 0
00426ac9  7507                     jne 0x426ad2
00426acb  89d0                     mov eax, edx
00426acd  e812e3ffff               call 0x424de4 ; -> ControleArrivageHangar
00426ad2  31db                     xor ebx, ebx
00426ad4  6689fb                   mov bx, di
00426ad7  89d8                     mov eax, ebx
00426ad9  c1e004                   shl eax, 4
00426adc  01d8                     add eax, ebx
00426ade  c1e002                   shl eax, 2
00426ae1  01d8                     add eax, ebx
00426ae3  c1e002                   shl eax, 2
00426ae6  05c8a04900               add eax, 0x49a0c8
00426aeb  89da                     mov edx, ebx
00426aed  8a4004                   mov al, byte ptr [eax + 4]
00426af0  25ff000000               and eax, 0xff
00426af5  e874b30300               call 0x461e6e ; -> SetTableauHangar
00426afa  e9c1160000               jmp 0x4281c0
00426aff  31d2                     xor edx, edx
00426b01  6689fa                   mov dx, di
00426b04  89d0                     mov eax, edx
00426b06  c1e004                   shl eax, 4
00426b09  01d0                     add eax, edx
00426b0b  c1e002                   shl eax, 2
00426b0e  b9c8a04900               mov ecx, 0x49a0c8
00426b13  01d0                     add eax, edx
00426b15  31d2                     xor edx, edx
00426b17  c1e002                   shl eax, 2
00426b1a  6689fa                   mov dx, di
00426b1d  01c1                     add ecx, eax
00426b1f  89d0                     mov eax, edx
00426b21  c1e004                   shl eax, 4
00426b24  01d0                     add eax, edx
00426b26  c1e002                   shl eax, 2
00426b29  01d0                     add eax, edx
00426b2b  bac8a04900               mov edx, 0x49a0c8
00426b30  89fb                     mov ebx, edi
00426b32  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426b36  25ff000000               and eax, 0xff
00426b3b  83f815                   cmp eax, 0x15
00426b3e  7510                     jne 0x426b50
00426b40  8d410c                   lea eax, [ecx + 0xc]
00426b43  e802070200               call 0x44724a ; -> BagContientTroupe
00426b48  84c0                     test al, al
00426b4a  744b                     je 0x426b97
00426b4c  b001                     mov al, 1
00426b4e  eb49                     jmp 0x426b99
00426b50  31d2                     xor edx, edx
00426b52  6689fa                   mov dx, di
00426b55  89d0                     mov eax, edx
00426b57  c1e004                   shl eax, 4
00426b5a  01d0                     add eax, edx
00426b5c  c1e002                   shl eax, 2
00426b5f  01d0                     add eax, edx
00426b61  bac8a04900               mov edx, 0x49a0c8
00426b66  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426b6a  25ff000000               and eax, 0xff
00426b6f  83f802                   cmp eax, 2
00426b72  750c                     jne 0x426b80
00426b74  8d410c                   lea eax, [ecx + 0xc]
00426b77  e8ce060200               call 0x44724a ; -> BagContientTroupe
00426b7c  84c0                     test al, al
00426b7e  75cc                     jne 0x426b4c
00426b80  bb09000000               mov ebx, 9
00426b85  ba01000000               mov edx, 1
00426b8a  8d410c                   lea eax, [ecx + 0xc]
00426b8d  e826060200               call 0x4471b8 ; -> BagContient
00426b92  6685c0                   test ax, ax
00426b95  ebb3                     jmp 0x426b4a
00426b97  30c0                     xor al, al
00426b99  84c0                     test al, al
00426b9b  0f841f160000             je 0x4281c0
00426ba1  31d2                     xor edx, edx
00426ba3  6689fa                   mov dx, di
00426ba6  89d0                     mov eax, edx
00426ba8  c1e004                   shl eax, 4
00426bab  01d0                     add eax, edx
00426bad  c1e002                   shl eax, 2
00426bb0  01d0                     add eax, edx
00426bb2  bec8a04900               mov esi, 0x49a0c8
00426bb7  c1e002                   shl eax, 2
00426bba  01c6                     add esi, eax
00426bbc  31c0                     xor eax, eax
00426bbe  8a4608                   mov al, byte ptr [esi + 8]
00426bc1  83f803                   cmp eax, 3
00426bc4  0f85f6150000             jne 0x4281c0
00426bca  f605808f500001           test byte ptr [0x508f80], 1
00426bd1  0f85e9150000             jne 0x4281c0
00426bd7  807e7500                 cmp byte ptr [esi + 0x75], 0
00426bdb  741a                     je 0x426bf7
00426bdd  31c0                     xor eax, eax
00426bdf  8a4676                   mov al, byte ptr [esi + 0x76]
00426be2  83f80f                   cmp eax, 0xf
00426be5  0f8dd5150000             jge 0x4281c0
00426beb  88c2                     mov dl, al
00426bed  fec2                     inc dl
00426bef  885676                   mov byte ptr [esi + 0x76], dl
00426bf2  e9c9150000               jmp 0x4281c0
00426bf7  31c0                     xor eax, eax
00426bf9  8a4676                   mov al, byte ptr [esi + 0x76]
00426bfc  85c0                     test eax, eax
00426bfe  0f84bc150000             je 0x4281c0
00426c04  88c4                     mov ah, al
00426c06  fecc                     dec ah
00426c08  886676                   mov byte ptr [esi + 0x76], ah
00426c0b  e9b0150000               jmp 0x4281c0
00426c10  31db                     xor ebx, ebx
00426c12  6689fb                   mov bx, di
00426c15  89d8                     mov eax, ebx
00426c17  c1e004                   shl eax, 4
00426c1a  01d8                     add eax, ebx
00426c1c  c1e002                   shl eax, 2
00426c1f  01d8                     add eax, ebx
00426c21  bbc8a04900               mov ebx, 0x49a0c8
00426c26  c1e002                   shl eax, 2
00426c29  01c3                     add ebx, eax
00426c2b  89f8                     mov eax, edi
00426c2d  25ffff0000               and eax, 0xffff
00426c32  8945cc                   mov dword ptr [ebp - 0x34], eax
00426c35  8b4dcc                   mov ecx, dword ptr [ebp - 0x34]
00426c38  c1e004                   shl eax, 4
00426c3b  01c8                     add eax, ecx
00426c3d  c1e002                   shl eax, 2
00426c40  01c8                     add eax, ecx
00426c42  c1e002                   shl eax, 2
00426c45  8945cc                   mov dword ptr [ebp - 0x34], eax
00426c48  b8c8a04900               mov eax, 0x49a0c8
00426c4d  0345cc                   add eax, dword ptr [ebp - 0x34]
00426c50  8a4008                   mov al, byte ptr [eax + 8]
00426c53  25ff000000               and eax, 0xff
00426c58  83f815                   cmp eax, 0x15
00426c5b  7510                     jne 0x426c6d
00426c5d  8d430c                   lea eax, [ebx + 0xc]
00426c60  e8e5050200               call 0x44724a ; -> BagContientTroupe
00426c65  84c0                     test al, al
00426c67  744c                     je 0x426cb5
00426c69  b001                     mov al, 1
00426c6b  eb4a                     jmp 0x426cb7
00426c6d  81e2ffff0000             and edx, 0xffff
00426c73  89d0                     mov eax, edx
00426c75  c1e004                   shl eax, 4
00426c78  01d0                     add eax, edx
00426c7a  c1e002                   shl eax, 2
00426c7d  01d0                     add eax, edx
00426c7f  bac8a04900               mov edx, 0x49a0c8
00426c84  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426c88  25ff000000               and eax, 0xff
00426c8d  83f802                   cmp eax, 2
00426c90  750c                     jne 0x426c9e
00426c92  8d430c                   lea eax, [ebx + 0xc]
00426c95  e8b0050200               call 0x44724a ; -> BagContientTroupe
00426c9a  84c0                     test al, al
00426c9c  75cb                     jne 0x426c69
00426c9e  8d430c                   lea eax, [ebx + 0xc]
00426ca1  ba01000000               mov edx, 1
00426ca6  bb09000000               mov ebx, 9
00426cab  e808050200               call 0x4471b8 ; -> BagContient
00426cb0  6685c0                   test ax, ax
00426cb3  ebb2                     jmp 0x426c67
00426cb5  30c0                     xor al, al
00426cb7  84c0                     test al, al
00426cb9  0f8401150000             je 0x4281c0
00426cbf  bb09000000               mov ebx, 9
00426cc4  31c0                     xor eax, eax
00426cc6  ba02000000               mov edx, 2
00426ccb  8a4604                   mov al, byte ptr [esi + 4]
00426cce  e8ed1f0000               call 0x428cc0 ; -> BonusGetValEngin
00426cd3  ba05000000               mov edx, 5
00426cd8  25ffff0000               and eax, 0xffff
00426cdd  29c2                     sub edx, eax
00426cdf  89d0                     mov eax, edx
00426ce1  31d2                     xor edx, edx
00426ce3  668b5678                 mov dx, word ptr [esi + 0x78]
00426ce7  39c2                     cmp edx, eax
00426ce9  0f8cd1140000             jl 0x4281c0
00426cef  e818110300               call 0x457e0c ; -> EnginNewPossible
00426cf4  84c0                     test al, al
00426cf6  0f84c4140000             je 0x4281c0
00426cfc  ba01000000               mov edx, 1
00426d01  8d460c                   lea eax, [esi + 0xc]
00426d04  e8c9030200               call 0x4470d2 ; -> BagAccepte
00426d09  84c0                     test al, al
00426d0b  0f84af140000             je 0x4281c0
00426d11  bb09000000               mov ebx, 9
00426d16  ba01000000               mov edx, 1
00426d1b  66c746780000             mov word ptr [esi + 0x78], 0
00426d21  31c9                     xor ecx, ecx
00426d23  31c0                     xor eax, eax
00426d25  8a4e04                   mov cl, byte ptr [esi + 4]
00426d28  668b4602                 mov ax, word ptr [esi + 2]
00426d2c  31f6                     xor esi, esi
00426d2e  e839110300               call 0x457e6c ; -> CreerEngin
00426d33  6689c6                   mov si, ax
00426d36  31c0                     xor eax, eax
00426d38  89f2                     mov edx, esi
00426d3a  6689f8                   mov ax, di
00426d3d  e82c8affff               call 0x41f76e ; -> BatimentLogeEngin
00426d42  ba0e000000               mov edx, 0xe
00426d47  89f0                     mov eax, esi
00426d49  31db                     xor ebx, ebx
00426d4b  e80fa40100               call 0x44115f ; -> EnginSetEtat
00426d50  ba43000000               mov edx, 0x43
00426d55  89f0                     mov eax, esi
00426d57  e86cbc0500               call 0x4829c8 ; -> iagUnitSendMessage
00426d5c  e95f140000               jmp 0x4281c0
00426d61  31db                     xor ebx, ebx
00426d63  6689fb                   mov bx, di
00426d66  89d8                     mov eax, ebx
00426d68  c1e004                   shl eax, 4
00426d6b  01d8                     add eax, ebx
00426d6d  c1e002                   shl eax, 2
00426d70  b9c8a04900               mov ecx, 0x49a0c8
00426d75  01d8                     add eax, ebx
00426d77  31db                     xor ebx, ebx
00426d79  c1e002                   shl eax, 2
00426d7c  6689fb                   mov bx, di
00426d7f  01c1                     add ecx, eax
00426d81  89d8                     mov eax, ebx
00426d83  c1e004                   shl eax, 4
00426d86  01d8                     add eax, ebx
00426d88  c1e002                   shl eax, 2
00426d8b  01d8                     add eax, ebx
00426d8d  bbc8a04900               mov ebx, 0x49a0c8
00426d92  8a448308                 mov al, byte ptr [ebx + eax*4 + 8]
00426d96  25ff000000               and eax, 0xff
00426d9b  83f815                   cmp eax, 0x15
00426d9e  7510                     jne 0x426db0
00426da0  8d410c                   lea eax, [ecx + 0xc]
00426da3  e8a2040200               call 0x44724a ; -> BagContientTroupe
00426da8  84c0                     test al, al
00426daa  7449                     je 0x426df5
00426dac  b001                     mov al, 1
00426dae  eb47                     jmp 0x426df7
00426db0  81e2ffff0000             and edx, 0xffff
00426db6  89d0                     mov eax, edx
00426db8  c1e004                   shl eax, 4
00426dbb  01d0                     add eax, edx
00426dbd  c1e002                   shl eax, 2
00426dc0  01d0                     add eax, edx
00426dc2  89da                     mov edx, ebx
00426dc4  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426dc8  25ff000000               and eax, 0xff
00426dcd  83f802                   cmp eax, 2
00426dd0  750c                     jne 0x426dde
00426dd2  8d410c                   lea eax, [ecx + 0xc]
00426dd5  e870040200               call 0x44724a ; -> BagContientTroupe
00426dda  84c0                     test al, al
00426ddc  75ce                     jne 0x426dac
00426dde  bb09000000               mov ebx, 9
00426de3  ba01000000               mov edx, 1
00426de8  8d410c                   lea eax, [ecx + 0xc]
00426deb  e8c8030200               call 0x4471b8 ; -> BagContient
00426df0  6685c0                   test ax, ax
00426df3  ebb5                     jmp 0x426daa
00426df5  30c0                     xor al, al
00426df7  84c0                     test al, al
00426df9  0f84c1130000             je 0x4281c0
00426dff  31d2                     xor edx, edx
00426e01  6689fa                   mov dx, di
00426e04  89d0                     mov eax, edx
00426e06  c1e004                   shl eax, 4
00426e09  01d0                     add eax, edx
00426e0b  c1e002                   shl eax, 2
00426e0e  01d0                     add eax, edx
00426e10  bec8a04900               mov esi, 0x49a0c8
00426e15  c1e002                   shl eax, 2
00426e18  bb09000000               mov ebx, 9
00426e1d  01c6                     add esi, eax
00426e1f  ba01000000               mov edx, 1
00426e24  8d460c                   lea eax, [esi + 0xc]
00426e27  e88c030200               call 0x4471b8 ; -> BagContient
00426e2c  31d2                     xor edx, edx
00426e2e  6689c2                   mov dx, ax
00426e31  8a4604                   mov al, byte ptr [esi + 4]
00426e34  25ff000000               and eax, 0xff
00426e39  e8b99d0400               call 0x470bf7 ; -> RechercheAddScientifique
00426e3e  e97d130000               jmp 0x4281c0
00426e43  31d2                     xor edx, edx
00426e45  6689fa                   mov dx, di
00426e48  89d0                     mov eax, edx
00426e4a  c1e004                   shl eax, 4
00426e4d  01d0                     add eax, edx
00426e4f  c1e002                   shl eax, 2
00426e52  bbc8a04900               mov ebx, 0x49a0c8
00426e57  01d0                     add eax, edx
00426e59  31d2                     xor edx, edx
00426e5b  c1e002                   shl eax, 2
00426e5e  6689fa                   mov dx, di
00426e61  01c3                     add ebx, eax
00426e63  89d0                     mov eax, edx
00426e65  c1e004                   shl eax, 4
00426e68  01d0                     add eax, edx
00426e6a  c1e002                   shl eax, 2
00426e6d  01d0                     add eax, edx
00426e6f  bac8a04900               mov edx, 0x49a0c8
00426e74  c1e002                   shl eax, 2
00426e77  01d0                     add eax, edx
00426e79  89f9                     mov ecx, edi
00426e7b  8a4008                   mov al, byte ptr [eax + 8]
00426e7e  25ff000000               and eax, 0xff
00426e83  83f815                   cmp eax, 0x15
00426e86  7510                     jne 0x426e98
00426e88  8d430c                   lea eax, [ebx + 0xc]
00426e8b  e8ba030200               call 0x44724a ; -> BagContientTroupe
00426e90  84c0                     test al, al
00426e92  744b                     je 0x426edf
00426e94  b001                     mov al, 1
00426e96  eb49                     jmp 0x426ee1
00426e98  31d2                     xor edx, edx
00426e9a  6689fa                   mov dx, di
00426e9d  89d0                     mov eax, edx
00426e9f  c1e004                   shl eax, 4
00426ea2  01d0                     add eax, edx
00426ea4  c1e002                   shl eax, 2
00426ea7  01d0                     add eax, edx
00426ea9  bac8a04900               mov edx, 0x49a0c8
00426eae  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426eb2  25ff000000               and eax, 0xff
00426eb7  83f802                   cmp eax, 2
00426eba  750c                     jne 0x426ec8
00426ebc  8d430c                   lea eax, [ebx + 0xc]
00426ebf  e886030200               call 0x44724a ; -> BagContientTroupe
00426ec4  84c0                     test al, al
00426ec6  75cc                     jne 0x426e94
00426ec8  8d430c                   lea eax, [ebx + 0xc]
00426ecb  ba01000000               mov edx, 1
00426ed0  bb09000000               mov ebx, 9
00426ed5  e8de020200               call 0x4471b8 ; -> BagContient
00426eda  6685c0                   test ax, ax
00426edd  ebb3                     jmp 0x426e92
00426edf  30c0                     xor al, al
00426ee1  84c0                     test al, al
00426ee3  0f8449060000             je 0x427532
00426ee9  31d2                     xor edx, edx
00426eeb  6689fa                   mov dx, di
00426eee  89d0                     mov eax, edx
00426ef0  e82fd7ffff               call 0x424624 ; -> CibleTourelleValide
00426ef5  84c0                     test al, al
00426ef7  0f8595000000             jne 0x426f92
00426efd  884676                   mov byte ptr [esi + 0x76], al
00426f00  884674                   mov byte ptr [esi + 0x74], al
00426f03  89d0                     mov eax, edx
00426f05  c1e004                   shl eax, 4
00426f08  01d0                     add eax, edx
00426f0a  c1e002                   shl eax, 2
00426f0d  bbc8a04900               mov ebx, 0x49a0c8
00426f12  01d0                     add eax, edx
00426f14  66c746780000             mov word ptr [esi + 0x78], 0
00426f1a  c1e002                   shl eax, 2
00426f1d  66c78686000000ffff       mov word ptr [esi + 0x86], 0xffff
00426f26  01c3                     add ebx, eax
00426f28  31c0                     xor eax, eax
00426f2a  8b0d7c8f5000             mov ecx, dword ptr [0x508f7c]
00426f30  6689f8                   mov ax, di
00426f33  01c8                     add eax, ecx
00426f35  a81f                     test al, 0x1f
00426f37  7407                     je 0x426f40
00426f39  b8ffff0000               mov eax, 0xffff
00426f3e  eb4b                     jmp 0x426f8b
00426f40  89d0                     mov eax, edx
00426f42  e872d0ffff               call 0x423fb9 ; -> TourelleTrouveEngin
00426f47  8945ec                   mov dword ptr [ebp - 0x14], eax
00426f4a  25ffff0000               and eax, 0xffff
00426f4f  3dffff0000               cmp eax, 0xffff
00426f54  740f                     je 0x426f65
00426f56  66c783880000000000       mov word ptr [ebx + 0x88], 0
00426f5f  c6437b01                 mov byte ptr [ebx + 0x7b], 1
00426f63  eb23                     jmp 0x426f88
00426f65  89d0                     mov eax, edx
00426f67  e8b7d1ffff               call 0x424123 ; -> TourelleTrouveBatiment
00426f6c  8945ec                   mov dword ptr [ebp - 0x14], eax
00426f6f  25ffff0000               and eax, 0xffff
00426f74  3dffff0000               cmp eax, 0xffff
00426f79  740d                     je 0x426f88
00426f7b  66c783880000000000       mov word ptr [ebx + 0x88], 0
00426f84  c6437b03                 mov byte ptr [ebx + 0x7b], 3
00426f88  8b45ec                   mov eax, dword ptr [ebp - 0x14]
00426f8b  66898686000000           mov word ptr [esi + 0x86], ax
00426f92  31c0                     xor eax, eax
00426f94  668b8686000000           mov ax, word ptr [esi + 0x86]
00426f9b  3dffff0000               cmp eax, 0xffff
00426fa0  0f849f040000             je 0x427445
00426fa6  31c0                     xor eax, eax
00426fa8  8a467b                   mov al, byte ptr [esi + 0x7b]
00426fab  c6467401                 mov byte ptr [esi + 0x74], 1
00426faf  83f801                   cmp eax, 1
00426fb2  0f858d000000             jne 0x427045
00426fb8  31c0                     xor eax, eax
00426fba  6a20                     push 0x20
00426fbc  668b8686000000           mov ax, word ptr [esi + 0x86]
00426fc3  31d2                     xor edx, edx
00426fc5  e8269e0100               call 0x440df0 ; -> EnginGetStart
00426fca  6689c2                   mov dx, ax
00426fcd  89d0                     mov eax, edx
00426fcf  c1fa1f                   sar edx, 0x1f
00426fd2  c1e208                   shl edx, 8
00426fd5  1bc2                     sbb eax, edx
00426fd7  c1f808                   sar eax, 8
00426fda  31c9                     xor ecx, ecx
00426fdc  6689c1                   mov cx, ax
00426fdf  31c0                     xor eax, eax
00426fe1  668b8686000000           mov ax, word ptr [esi + 0x86]
00426fe8  31d2                     xor edx, edx
00426fea  e8019e0100               call 0x440df0 ; -> EnginGetStart
00426fef  6689c2                   mov dx, ax
00426ff2  bb00010000               mov ebx, 0x100
00426ff7  89d0                     mov eax, edx
00426ff9  c1fa1f                   sar edx, 0x1f
00426ffc  f7fb                     idiv ebx
00426ffe  31db                     xor ebx, ebx
00427000  31c0                     xor eax, eax
00427002  668b5e02                 mov bx, word ptr [esi + 2]
00427006  6689d0                   mov ax, dx
00427009  81eb00010000             sub ebx, 0x100
0042700f  8945d4                   mov dword ptr [ebp - 0x2c], eax
00427012  89da                     mov edx, ebx
00427014  89d8                     mov eax, ebx
00427016  c1fa1f                   sar edx, 0x1f
00427019  c1e208                   shl edx, 8
0042701c  1bc2                     sbb eax, edx
0042701e  c1f808                   sar eax, 8
00427021  25ffff0000               and eax, 0xffff
00427026  89da                     mov edx, ebx
00427028  8945cc                   mov dword ptr [ebp - 0x34], eax
0042702b  b800010000               mov eax, 0x100
00427030  c1fa1f                   sar edx, 0x1f
00427033  8945d0                   mov dword ptr [ebp - 0x30], eax
00427036  89d8                     mov eax, ebx
00427038  f77dd0                   idiv dword ptr [ebp - 0x30]
0042703b  31c0                     xor eax, eax
0042703d  8b5dd4                   mov ebx, dword ptr [ebp - 0x2c]
00427040  e94f010000               jmp 0x427194
00427045  83f803                   cmp eax, 3
00427048  0f8557010000             jne 0x4271a5
0042704e  668b8686000000           mov ax, word ptr [esi + 0x86]
00427055  31d2                     xor edx, edx
00427057  6689c2                   mov dx, ax
0042705a  89d0                     mov eax, edx
0042705c  c1e004                   shl eax, 4
0042705f  01d0                     add eax, edx
00427061  c1e002                   shl eax, 2
00427064  01d0                     add eax, edx
00427066  bac8a04900               mov edx, 0x49a0c8
0042706b  c1e002                   shl eax, 2
0042706e  01c2                     add edx, eax
00427070  31db                     xor ebx, ebx
00427072  8a4208                   mov al, byte ptr [edx + 8]
00427075  88c3                     mov bl, al
00427077  89d8                     mov eax, ebx
00427079  c1e002                   shl eax, 2
0042707c  29d8                     sub eax, ebx
0042707e  c1e002                   shl eax, 2
00427081  01c3                     add ebx, eax
00427083  c1e302                   shl ebx, 2
00427086  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
0042708d  8945f0                   mov dword ptr [ebp - 0x10], eax
00427090  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
00427097  8945fc                   mov dword ptr [ebp - 4], eax
0042709a  8b45f0                   mov eax, dword ptr [ebp - 0x10]
0042709d  8b5dfc                   mov ebx, dword ptr [ebp - 4]
004270a0  66d1e8                   shr ax, 1
004270a3  66d1eb                   shr bx, 1
004270a6  8945f0                   mov dword ptr [ebp - 0x10], eax
004270a9  895dfc                   mov dword ptr [ebp - 4], ebx
004270ac  89d8                     mov eax, ebx
004270ae  8b4df0                   mov ecx, dword ptr [ebp - 0x10]
004270b1  c1e008                   shl eax, 8
004270b4  668b5a02                 mov bx, word ptr [edx + 2]
004270b8  01c8                     add eax, ecx
004270ba  31d2                     xor edx, edx
004270bc  01d8                     add eax, ebx
004270be  6689c2                   mov dx, ax
004270c1  89d0                     mov eax, edx
004270c3  c1fa1f                   sar edx, 0x1f
004270c6  c1e208                   shl edx, 8
004270c9  1bc2                     sbb eax, edx
004270cb  c1f808                   sar eax, 8
004270ce  31c9                     xor ecx, ecx
004270d0  6689c1                   mov cx, ax
004270d3  31d2                     xor edx, edx
004270d5  668b8686000000           mov ax, word ptr [esi + 0x86]
004270dc  6689c2                   mov dx, ax
004270df  89d0                     mov eax, edx
004270e1  c1e004                   shl eax, 4
004270e4  01d0                     add eax, edx
004270e6  c1e002                   shl eax, 2
004270e9  01d0                     add eax, edx
004270eb  bac8a04900               mov edx, 0x49a0c8
004270f0  c1e002                   shl eax, 2
004270f3  01c2                     add edx, eax
004270f5  31db                     xor ebx, ebx
004270f7  8a4208                   mov al, byte ptr [edx + 8]
004270fa  88c3                     mov bl, al
004270fc  89d8                     mov eax, ebx
004270fe  c1e002                   shl eax, 2
00427101  29d8                     sub eax, ebx
00427103  c1e002                   shl eax, 2
00427106  01c3                     add ebx, eax
00427108  c1e302                   shl ebx, 2
0042710b  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
00427112  8945e8                   mov dword ptr [ebp - 0x18], eax
00427115  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
0042711c  8945dc                   mov dword ptr [ebp - 0x24], eax
0042711f  8b45e8                   mov eax, dword ptr [ebp - 0x18]
00427122  8b5ddc                   mov ebx, dword ptr [ebp - 0x24]
00427125  66d1e8                   shr ax, 1
00427128  66d1eb                   shr bx, 1
0042712b  8945e8                   mov dword ptr [ebp - 0x18], eax
0042712e  895ddc                   mov dword ptr [ebp - 0x24], ebx
00427131  89d8                     mov eax, ebx
00427133  8b5de8                   mov ebx, dword ptr [ebp - 0x18]
00427136  c1e008                   shl eax, 8
00427139  01d8                     add eax, ebx
0042713b  66034202                 add ax, word ptr [edx + 2]
0042713f  31d2                     xor edx, edx
00427141  6689c2                   mov dx, ax
00427144  bb00010000               mov ebx, 0x100
00427149  89d0                     mov eax, edx
0042714b  c1fa1f                   sar edx, 0x1f
0042714e  f7fb                     idiv ebx
00427150  31db                     xor ebx, ebx
00427152  31c0                     xor eax, eax
00427154  668b5e02                 mov bx, word ptr [esi + 2]
00427158  6689d0                   mov ax, dx
0042715b  81eb00010000             sub ebx, 0x100
00427161  8945d0                   mov dword ptr [ebp - 0x30], eax
00427164  89da                     mov edx, ebx
00427166  89d8                     mov eax, ebx
00427168  c1fa1f                   sar edx, 0x1f
0042716b  c1e208                   shl edx, 8
0042716e  1bc2                     sbb eax, edx
00427170  c1f808                   sar eax, 8
00427173  6a20                     push 0x20
00427175  25ffff0000               and eax, 0xffff
0042717a  89da                     mov edx, ebx
0042717c  8945cc                   mov dword ptr [ebp - 0x34], eax
0042717f  b800010000               mov eax, 0x100
00427184  c1fa1f                   sar edx, 0x1f
00427187  8945d4                   mov dword ptr [ebp - 0x2c], eax
0042718a  89d8                     mov eax, ebx
0042718c  f77dd4                   idiv dword ptr [ebp - 0x2c]
0042718f  31c0                     xor eax, eax
00427191  8b5dd0                   mov ebx, dword ptr [ebp - 0x30]
00427194  6689d0                   mov ax, dx
00427197  8b55cc                   mov edx, dword ptr [ebp - 0x34]
0042719a  e82c250500               call 0x4796cb ; -> AngleCalcul
0042719f  88868b000000             mov byte ptr [esi + 0x8b], al
004271a5  a17c8f5000               mov eax, dword ptr [0x508f7c]
004271aa  31db                     xor ebx, ebx
004271ac  31d2                     xor edx, edx
004271ae  668b1dfc5b4900           mov bx, word ptr [0x495bfc]
004271b5  f7f3                     div ebx
004271b7  85d2                     test edx, edx
004271b9  0f85dd010000             jne 0x42739c
004271bf  8a868b000000             mov al, byte ptr [esi + 0x8b]
004271c5  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004271cb  0f85cb010000             jne 0x42739c
004271d1  31c0                     xor eax, eax
004271d3  8a467b                   mov al, byte ptr [esi + 0x7b]
004271d6  66c746786400             mov word ptr [esi + 0x78], 0x64
004271dc  83f801                   cmp eax, 1
004271df  0f85e1000000             jne 0x4272c6
004271e5  807e7400                 cmp byte ptr [esi + 0x74], 0
004271e9  0f84b9000000             je 0x4272a8
004271ef  8a868b000000             mov al, byte ptr [esi + 0x8b]
004271f5  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004271fb  0f85a7000000             jne 0x4272a8
00427201  c6467601                 mov byte ptr [esi + 0x76], 1
00427205  81e7ffff0000             and edi, 0xffff
0042720b  31c0                     xor eax, eax
0042720d  57                       push edi
0042720e  668b8686000000           mov ax, word ptr [esi + 0x86]
00427215  50                       push eax
00427216  31c9                     xor ecx, ecx
00427218  31db                     xor ebx, ebx
0042721a  e81f9f0100               call 0x44113e ; -> EnginGetCase
0042721f  6689c1                   mov cx, ax
00427222  31c0                     xor eax, eax
00427224  668b5e02                 mov bx, word ptr [esi + 2]
00427228  8a868a000000             mov al, byte ptr [esi + 0x8a]
0042722e  8a5608                   mov dl, byte ptr [esi + 8]
00427231  e8cadeffff               call 0x425100 ; -> RechercheDecalageProjectile
00427236  31c0                     xor eax, eax
00427238  668b8686000000           mov ax, word ptr [esi + 0x86]
0042723f  31d2                     xor edx, edx
00427241  e8ffad0100               call 0x442045 ; -> EnginGetPlayer
00427246  88c2                     mov dl, al
00427248  89f8                     mov eax, edi
0042724a  e8052bffff               call 0x419d54 ; -> BatimentDecouvre
0042724f  89f8                     mov eax, edi
00427251  c1e004                   shl eax, 4
00427254  01f8                     add eax, edi
00427256  c1e002                   shl eax, 2
00427259  01f8                     add eax, edi
0042725b  bbc8a04900               mov ebx, 0x49a0c8
00427260  c1e002                   shl eax, 2
00427263  01c3                     add ebx, eax
00427265  8a4304                   mov al, byte ptr [ebx + 4]
00427268  3a0541805000             cmp al, byte ptr [0x508041]
0042726e  0f8534000000             jne 0x4272a8
00427274  89f8                     mov eax, edi
00427276  e8302effff               call 0x41a0ab ; -> BatimentGetVolume
0042727b  83bb00010000ff           cmp dword ptr [ebx + 0x100], -1
00427282  0f8520000000             jne 0x4272a8
00427288  50                       push eax
00427289  31d2                     xor edx, edx
0042728b  31c9                     xor ecx, ecx
0042728d  8a5308                   mov dl, byte ptr [ebx + 8]
00427290  8d8300010000             lea eax, [ebx + 0x100]
00427296  c1e210                   shl edx, 0x10
00427299  89c3                     mov ebx, eax
0042729b  b842000000               mov eax, 0x42
004272a0  80ce23                   or dh, 0x23
004272a3  e8d1370600               call 0x48aa79 ; -> PlaySnd_PostSound
004272a8  8a467b                   mov al, byte ptr [esi + 0x7b]
004272ab  3c01                     cmp al, 1
004272ad  0f82f4010000             jb 0x4274a7
004272b3  0f8631010000             jbe 0x4273ea
004272b9  3c03                     cmp al, 3
004272bb  0f8457010000             je 0x427418
004272c1  e9e1010000               jmp 0x4274a7
004272c6  83f803                   cmp eax, 3
004272c9  75dd                     jne 0x4272a8
004272cb  807e7400                 cmp byte ptr [esi + 0x74], 0
004272cf  74d7                     je 0x4272a8
004272d1  8a868b000000             mov al, byte ptr [esi + 0x8b]
004272d7  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004272dd  75c9                     jne 0x4272a8
004272df  c6467601                 mov byte ptr [esi + 0x76], 1
004272e3  81e7ffff0000             and edi, 0xffff
004272e9  31c0                     xor eax, eax
004272eb  57                       push edi
004272ec  668b8686000000           mov ax, word ptr [esi + 0x86]
004272f3  31c9                     xor ecx, ecx
004272f5  50                       push eax
004272f6  31db                     xor ebx, ebx
004272f8  31d2                     xor edx, edx
004272fa  e8e33bffff               call 0x41aee2 ; -> BatimentGetCase
004272ff  6689c1                   mov cx, ax
00427302  31c0                     xor eax, eax
00427304  668b5e02                 mov bx, word ptr [esi + 2]
00427308  8a868a000000             mov al, byte ptr [esi + 0x8a]
0042730e  8a5608                   mov dl, byte ptr [esi + 8]
00427311  e8eaddffff               call 0x425100 ; -> RechercheDecalageProjectile
00427316  668b8686000000           mov ax, word ptr [esi + 0x86]
0042731d  31d2                     xor edx, edx
0042731f  6689c2                   mov dx, ax
00427322  89d0                     mov eax, edx
00427324  c1e004                   shl eax, 4
00427327  01d0                     add eax, edx
00427329  c1e002                   shl eax, 2
0042732c  01d0                     add eax, edx
0042732e  c1e002                   shl eax, 2
00427331  05c8a04900               add eax, 0x49a0c8
00427336  31d2                     xor edx, edx
00427338  8a4004                   mov al, byte ptr [eax + 4]
0042733b  88c2                     mov dl, al
0042733d  89f8                     mov eax, edi
0042733f  e8102affff               call 0x419d54 ; -> BatimentDecouvre
00427344  89f8                     mov eax, edi
00427346  c1e004                   shl eax, 4
00427349  01f8                     add eax, edi
0042734b  c1e002                   shl eax, 2
0042734e  01f8                     add eax, edi
00427350  bac8a04900               mov edx, 0x49a0c8
00427355  c1e002                   shl eax, 2
00427358  01c2                     add edx, eax
0042735a  8a3d41805000             mov bh, byte ptr [0x508041]
00427360  3a7a04                   cmp bh, byte ptr [edx + 4]
00427363  0f853fffffff             jne 0x4272a8
00427369  89f8                     mov eax, edi
0042736b  e83b2dffff               call 0x41a0ab ; -> BatimentGetVolume
00427370  83ba00010000ff           cmp dword ptr [edx + 0x100], -1
00427377  0f852bffffff             jne 0x4272a8
0042737d  8d9a00010000             lea ebx, [edx + 0x100]
00427383  50                       push eax
00427384  8a5208                   mov dl, byte ptr [edx + 8]
00427387  81e2ff000000             and edx, 0xff
0042738d  b842000000               mov eax, 0x42
00427392  c1e210                   shl edx, 0x10
00427395  31c9                     xor ecx, ecx
00427397  e904ffffff               jmp 0x4272a0
0042739c  31c0                     xor eax, eax
0042739e  668b4678                 mov ax, word ptr [esi + 0x78]
004273a2  85c0                     test eax, eax
004273a4  740e                     je 0x4273b4
004273a6  3dffff0000               cmp eax, 0xffff
004273ab  7407                     je 0x4273b4
004273ad  89c1                     mov ecx, eax
004273af  49                       dec ecx
004273b0  66894e78                 mov word ptr [esi + 0x78], cx
004273b4  31c0                     xor eax, eax
004273b6  8a4676                   mov al, byte ptr [esi + 0x76]
004273b9  83f801                   cmp eax, 1
004273bc  740e                     je 0x4273cc
004273be  83f802                   cmp eax, 2
004273c1  7409                     je 0x4273cc
004273c3  83f803                   cmp eax, 3
004273c6  0f85dcfeffff             jne 0x4272a8
004273cc  bb05000000               mov ebx, 5
004273d1  a17c8f5000               mov eax, dword ptr [0x508f7c]
004273d6  31d2                     xor edx, edx
004273d8  f7f3                     div ebx
004273da  85d2                     test edx, edx
004273dc  0f85c6feffff             jne 0x4272a8
004273e2  fe4676                   inc byte ptr [esi + 0x76]
004273e5  e9befeffff               jmp 0x4272a8
004273ea  31c0                     xor eax, eax
004273ec  668b8686000000           mov ax, word ptr [esi + 0x86]
004273f3  e8b5c90100               call 0x443dad ; -> EnginEstVivant
004273f8  84c0                     test al, al
004273fa  0f85a7000000             jne 0x4274a7
00427400  66c78686000000ffff       mov word ptr [esi + 0x86], 0xffff
00427409  c6467bff                 mov byte ptr [esi + 0x7b], 0xff
0042740d  884676                   mov byte ptr [esi + 0x76], al
00427410  884674                   mov byte ptr [esi + 0x74], al
00427413  e98f000000               jmp 0x4274a7
00427418  668b8686000000           mov ax, word ptr [esi + 0x86]
0042741f  31d2                     xor edx, edx
00427421  6689c2                   mov dx, ax
00427424  89d0                     mov eax, edx
00427426  c1e004                   shl eax, 4
00427429  01d0                     add eax, edx
0042742b  c1e002                   shl eax, 2
0042742e  01d0                     add eax, edx
00427430  c1e002                   shl eax, 2
00427433  05c8a04900               add eax, 0x49a0c8
00427438  8a4005                   mov al, byte ptr [eax + 5]
0042743b  25ff000000               and eax, 0xff
00427440  0f95c0                   setne al
00427443  ebb3                     jmp 0x4273f8
00427445  31c0                     xor eax, eax
00427447  8a4676                   mov al, byte ptr [esi + 0x76]
0042744a  83f801                   cmp eax, 1
0042744d  740a                     je 0x427459
0042744f  83f802                   cmp eax, 2
00427452  7405                     je 0x427459
00427454  83f803                   cmp eax, 3
00427457  7515                     jne 0x42746e
00427459  bb05000000               mov ebx, 5
0042745e  a17c8f5000               mov eax, dword ptr [0x508f7c]
00427463  31d2                     xor edx, edx
00427465  f7f3                     div ebx
00427467  85d2                     test edx, edx
00427469  7503                     jne 0x42746e
0042746b  fe4676                   inc byte ptr [esi + 0x76]
0042746e  b80b000000               mov eax, 0xb
00427473  bb64000000               mov ebx, 0x64
00427478  31d2                     xor edx, edx
0042747a  e85d900400               call 0x4704dc ; -> Random
0042747f  f7f3                     div ebx
00427481  85d2                     test edx, edx
00427483  7522                     jne 0x4274a7
00427485  8a868b000000             mov al, byte ptr [esi + 0x8b]
0042748b  3a868a000000             cmp al, byte ptr [esi + 0x8a]
00427491  7514                     jne 0x4274a7
00427493  b80c000000               mov eax, 0xc
00427498  e83f900400               call 0x4704dc ; -> Random
0042749d  241f                     and al, 0x1f
0042749f  fec0                     inc al
004274a1  88868b000000             mov byte ptr [esi + 0x8b], al
004274a7  8a868b000000             mov al, byte ptr [esi + 0x8b]
004274ad  8a968a000000             mov dl, byte ptr [esi + 0x8a]
004274b3  38d0                     cmp al, dl
004274b5  0f8477000000             je 0x427532
004274bb  f6057c8f500001           test byte ptr [0x508f7c], 1
004274c2  0f856a000000             jne 0x427532
004274c8  38d0                     cmp al, dl
004274ca  7613                     jbe 0x4274df
004274cc  31d2                     xor edx, edx
004274ce  88c2                     mov dl, al
004274d0  31c0                     xor eax, eax
004274d2  8a868a000000             mov al, byte ptr [esi + 0x8a]
004274d8  29c2                     sub edx, eax
004274da  83fa10                   cmp edx, 0x10
004274dd  7c1f                     jl 0x4274fe
004274df  8a868a000000             mov al, byte ptr [esi + 0x8a]
004274e5  8abe8b000000             mov bh, byte ptr [esi + 0x8b]
004274eb  38f8                     cmp al, bh
004274ed  7626                     jbe 0x427515
004274ef  31d2                     xor edx, edx
004274f1  88c2                     mov dl, al
004274f3  31c0                     xor eax, eax
004274f5  88f8                     mov al, bh
004274f7  29c2                     sub edx, eax
004274f9  83fa10                   cmp edx, 0x10
004274fc  7e17                     jle 0x427515
004274fe  31d2                     xor edx, edx
00427500  8a968a000000             mov dl, byte ptr [esi + 0x8a]
00427506  bb20000000               mov ebx, 0x20
0042750b  89d0                     mov eax, edx
0042750d  c1fa1f                   sar edx, 0x1f
00427510  f7fb                     idiv ebx
00427512  42                       inc edx
00427513  eb17                     jmp 0x42752c
00427515  31c0                     xor eax, eax
00427517  8a868a000000             mov al, byte ptr [esi + 0x8a]
0042751d  83f801                   cmp eax, 1
00427520  7405                     je 0x427527
00427522  8d50ff                   lea edx, [eax - 1]
00427525  eb05                     jmp 0x42752c
00427527  ba20000000               mov edx, 0x20
0042752c  88968a000000             mov byte ptr [esi + 0x8a], dl
00427532  31c0                     xor eax, eax
00427534  8a4676                   mov al, byte ptr [esi + 0x76]
00427537  83f804                   cmp eax, 4
0042753a  0f85800c0000             jne 0x4281c0
00427540  c6467600                 mov byte ptr [esi + 0x76], 0
00427544  e9770c0000               jmp 0x4281c0
00427549  31d2                     xor edx, edx
0042754b  6689fa                   mov dx, di
0042754e  89d0                     mov eax, edx
00427550  c1e004                   shl eax, 4
00427553  01d0                     add eax, edx
00427555  c1e002                   shl eax, 2
00427558  01d0                     add eax, edx
0042755a  bbc8a04900               mov ebx, 0x49a0c8
0042755f  c1e002                   shl eax, 2
00427562  89f9                     mov ecx, edi
00427564  01c3                     add ebx, eax
00427566  89f8                     mov eax, edi
00427568  25ffff0000               and eax, 0xffff
0042756d  89c2                     mov edx, eax
0042756f  c1e004                   shl eax, 4
00427572  01d0                     add eax, edx
00427574  c1e002                   shl eax, 2
00427577  01d0                     add eax, edx
00427579  bac8a04900               mov edx, 0x49a0c8
0042757e  c1e002                   shl eax, 2
00427581  01d0                     add eax, edx
00427583  8a4008                   mov al, byte ptr [eax + 8]
00427586  25ff000000               and eax, 0xff
0042758b  83f815                   cmp eax, 0x15
0042758e  7510                     jne 0x4275a0
00427590  8d430c                   lea eax, [ebx + 0xc]
00427593  e8b2fc0100               call 0x44724a ; -> BagContientTroupe
00427598  84c0                     test al, al
0042759a  744b                     je 0x4275e7
0042759c  b001                     mov al, 1
0042759e  eb49                     jmp 0x4275e9
004275a0  31d2                     xor edx, edx
004275a2  6689fa                   mov dx, di
004275a5  89d0                     mov eax, edx
004275a7  c1e004                   shl eax, 4
004275aa  01d0                     add eax, edx
004275ac  c1e002                   shl eax, 2
004275af  01d0                     add eax, edx
004275b1  bac8a04900               mov edx, 0x49a0c8
004275b6  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
004275ba  25ff000000               and eax, 0xff
004275bf  83f802                   cmp eax, 2
004275c2  750c                     jne 0x4275d0
004275c4  8d430c                   lea eax, [ebx + 0xc]
004275c7  e87efc0100               call 0x44724a ; -> BagContientTroupe
004275cc  84c0                     test al, al
004275ce  75cc                     jne 0x42759c
004275d0  8d430c                   lea eax, [ebx + 0xc]
004275d3  ba01000000               mov edx, 1
004275d8  bb09000000               mov ebx, 9
004275dd  e8d6fb0100               call 0x4471b8 ; -> BagContient
004275e2  6685c0                   test ax, ax
004275e5  ebb3                     jmp 0x42759a
004275e7  30c0                     xor al, al
004275e9  84c0                     test al, al
004275eb  0f84cf0b0000             je 0x4281c0
004275f1  31d2                     xor edx, edx
004275f3  6689fa                   mov dx, di
004275f6  89d0                     mov eax, edx
004275f8  e827d0ffff               call 0x424624 ; -> CibleTourelleValide
004275fd  84c0                     test al, al
004275ff  0f8595000000             jne 0x42769a
00427605  884676                   mov byte ptr [esi + 0x76], al
00427608  884674                   mov byte ptr [esi + 0x74], al
0042760b  89d0                     mov eax, edx
0042760d  c1e004                   shl eax, 4
00427610  01d0                     add eax, edx
00427612  c1e002                   shl eax, 2
00427615  bbc8a04900               mov ebx, 0x49a0c8
0042761a  01d0                     add eax, edx
0042761c  66c746780000             mov word ptr [esi + 0x78], 0
00427622  c1e002                   shl eax, 2
00427625  66c78686000000ffff       mov word ptr [esi + 0x86], 0xffff
0042762e  01c3                     add ebx, eax
00427630  31c0                     xor eax, eax
00427632  8b0d7c8f5000             mov ecx, dword ptr [0x508f7c]
00427638  6689f8                   mov ax, di
0042763b  01c8                     add eax, ecx
0042763d  a81f                     test al, 0x1f
0042763f  7407                     je 0x427648
00427641  b8ffff0000               mov eax, 0xffff
00427646  eb4b                     jmp 0x427693
00427648  89d0                     mov eax, edx
0042764a  e86ac9ffff               call 0x423fb9 ; -> TourelleTrouveEngin
0042764f  8945d8                   mov dword ptr [ebp - 0x28], eax
00427652  25ffff0000               and eax, 0xffff
00427657  3dffff0000               cmp eax, 0xffff
0042765c  740f                     je 0x42766d
0042765e  66c783880000000000       mov word ptr [ebx + 0x88], 0
00427667  c6437b01                 mov byte ptr [ebx + 0x7b], 1
0042766b  eb23                     jmp 0x427690
0042766d  89d0                     mov eax, edx
0042766f  e8afcaffff               call 0x424123 ; -> TourelleTrouveBatiment
00427674  8945d8                   mov dword ptr [ebp - 0x28], eax
00427677  25ffff0000               and eax, 0xffff
0042767c  3dffff0000               cmp eax, 0xffff
00427681  740d                     je 0x427690
00427683  66c783880000000000       mov word ptr [ebx + 0x88], 0
0042768c  c6437b03                 mov byte ptr [ebx + 0x7b], 3
00427690  8b45d8                   mov eax, dword ptr [ebp - 0x28]
00427693  66898686000000           mov word ptr [esi + 0x86], ax
0042769a  31c0                     xor eax, eax
0042769c  668b8686000000           mov ax, word ptr [esi + 0x86]
004276a3  3dffff0000               cmp eax, 0xffff
004276a8  0f8435040000             je 0x427ae3
004276ae  31c0                     xor eax, eax
004276b0  8a467b                   mov al, byte ptr [esi + 0x7b]
004276b3  c6467401                 mov byte ptr [esi + 0x74], 1
004276b7  83f801                   cmp eax, 1
004276ba  0f858d000000             jne 0x42774d
004276c0  31c0                     xor eax, eax
004276c2  6a20                     push 0x20
004276c4  668b8686000000           mov ax, word ptr [esi + 0x86]
004276cb  31d2                     xor edx, edx
004276cd  e81e970100               call 0x440df0 ; -> EnginGetStart
004276d2  6689c2                   mov dx, ax
004276d5  89d0                     mov eax, edx
004276d7  c1fa1f                   sar edx, 0x1f
004276da  c1e208                   shl edx, 8
004276dd  1bc2                     sbb eax, edx
004276df  c1f808                   sar eax, 8
004276e2  31c9                     xor ecx, ecx
004276e4  6689c1                   mov cx, ax
004276e7  31c0                     xor eax, eax
004276e9  668b8686000000           mov ax, word ptr [esi + 0x86]
004276f0  31d2                     xor edx, edx
004276f2  e8f9960100               call 0x440df0 ; -> EnginGetStart
004276f7  6689c2                   mov dx, ax
004276fa  bb00010000               mov ebx, 0x100
004276ff  89d0                     mov eax, edx
00427701  c1fa1f                   sar edx, 0x1f
00427704  f7fb                     idiv ebx
00427706  31c0                     xor eax, eax
00427708  31db                     xor ebx, ebx
0042770a  6689d0                   mov ax, dx
0042770d  668b5e02                 mov bx, word ptr [esi + 2]
00427711  8945d0                   mov dword ptr [ebp - 0x30], eax
00427714  89da                     mov edx, ebx
00427716  89d8                     mov eax, ebx
00427718  c1fa1f                   sar edx, 0x1f
0042771b  c1e208                   shl edx, 8
0042771e  1bc2                     sbb eax, edx
00427720  c1f808                   sar eax, 8
00427723  25ffff0000               and eax, 0xffff
00427728  89da                     mov edx, ebx
0042772a  8945cc                   mov dword ptr [ebp - 0x34], eax
0042772d  b800010000               mov eax, 0x100
00427732  c1fa1f                   sar edx, 0x1f
00427735  8945d4                   mov dword ptr [ebp - 0x2c], eax
00427738  89d8                     mov eax, ebx
0042773a  f77dd4                   idiv dword ptr [ebp - 0x2c]
0042773d  31c0                     xor eax, eax
0042773f  8b5dd0                   mov ebx, dword ptr [ebp - 0x30]
00427742  6689d0                   mov ax, dx
00427745  8b55cc                   mov edx, dword ptr [ebp - 0x34]
00427748  e946010000               jmp 0x427893
0042774d  83f803                   cmp eax, 3
00427750  0f8548010000             jne 0x42789e
00427756  668b8686000000           mov ax, word ptr [esi + 0x86]
0042775d  31d2                     xor edx, edx
0042775f  6689c2                   mov dx, ax
00427762  89d0                     mov eax, edx
00427764  c1e004                   shl eax, 4
00427767  01d0                     add eax, edx
00427769  c1e002                   shl eax, 2
0042776c  01d0                     add eax, edx
0042776e  bac8a04900               mov edx, 0x49a0c8
00427773  c1e002                   shl eax, 2
00427776  01c2                     add edx, eax
00427778  31db                     xor ebx, ebx
0042777a  8a4208                   mov al, byte ptr [edx + 8]
0042777d  88c3                     mov bl, al
0042777f  89d8                     mov eax, ebx
00427781  c1e002                   shl eax, 2
00427784  29d8                     sub eax, ebx
00427786  c1e002                   shl eax, 2
00427789  01c3                     add ebx, eax
0042778b  c1e302                   shl ebx, 2
0042778e  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
00427795  8945e0                   mov dword ptr [ebp - 0x20], eax
00427798  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
0042779f  8b4de0                   mov ecx, dword ptr [ebp - 0x20]
004277a2  8945f8                   mov dword ptr [ebp - 8], eax
004277a5  66d1e8                   shr ax, 1
004277a8  66d1e9                   shr cx, 1
004277ab  8945f8                   mov dword ptr [ebp - 8], eax
004277ae  c1e008                   shl eax, 8
004277b1  894de0                   mov dword ptr [ebp - 0x20], ecx
004277b4  01c8                     add eax, ecx
004277b6  66034202                 add ax, word ptr [edx + 2]
004277ba  31d2                     xor edx, edx
004277bc  6689c2                   mov dx, ax
004277bf  89d0                     mov eax, edx
004277c1  c1fa1f                   sar edx, 0x1f
004277c4  c1e208                   shl edx, 8
004277c7  1bc2                     sbb eax, edx
004277c9  c1f808                   sar eax, 8
004277cc  31c9                     xor ecx, ecx
004277ce  6689c1                   mov cx, ax
004277d1  31d2                     xor edx, edx
004277d3  668b8686000000           mov ax, word ptr [esi + 0x86]
004277da  6689c2                   mov dx, ax
004277dd  89d0                     mov eax, edx
004277df  c1e004                   shl eax, 4
004277e2  01d0                     add eax, edx
004277e4  c1e002                   shl eax, 2
004277e7  01d0                     add eax, edx
004277e9  bac8a04900               mov edx, 0x49a0c8
004277ee  c1e002                   shl eax, 2
004277f1  01c2                     add edx, eax
004277f3  6a20                     push 0x20
004277f5  8a4208                   mov al, byte ptr [edx + 8]
004277f8  25ff000000               and eax, 0xff
004277fd  89c3                     mov ebx, eax
004277ff  c1e002                   shl eax, 2
00427802  29d8                     sub eax, ebx
00427804  c1e002                   shl eax, 2
00427807  01c3                     add ebx, eax
00427809  c1e302                   shl ebx, 2
0042780c  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
00427813  8945e4                   mov dword ptr [ebp - 0x1c], eax
00427816  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
0042781d  8945f4                   mov dword ptr [ebp - 0xc], eax
00427820  8b45e4                   mov eax, dword ptr [ebp - 0x1c]
00427823  8b5df4                   mov ebx, dword ptr [ebp - 0xc]
00427826  66d1e8                   shr ax, 1
00427829  66d1eb                   shr bx, 1
0042782c  8945e4                   mov dword ptr [ebp - 0x1c], eax
0042782f  895df4                   mov dword ptr [ebp - 0xc], ebx
00427832  89d8                     mov eax, ebx
00427834  8b5de4                   mov ebx, dword ptr [ebp - 0x1c]
00427837  c1e008                   shl eax, 8
0042783a  01d8                     add eax, ebx
0042783c  66034202                 add ax, word ptr [edx + 2]
00427840  31d2                     xor edx, edx
00427842  6689c2                   mov dx, ax
00427845  bb00010000               mov ebx, 0x100
0042784a  89d0                     mov eax, edx
0042784c  c1fa1f                   sar edx, 0x1f
0042784f  f7fb                     idiv ebx
00427851  31c0                     xor eax, eax
00427853  31db                     xor ebx, ebx
00427855  6689d0                   mov ax, dx
00427858  668b5e02                 mov bx, word ptr [esi + 2]
0042785c  8945d0                   mov dword ptr [ebp - 0x30], eax
0042785f  89da                     mov edx, ebx
00427861  89d8                     mov eax, ebx
00427863  c1fa1f                   sar edx, 0x1f
00427866  c1e208                   shl edx, 8
00427869  1bc2                     sbb eax, edx
0042786b  c1f808                   sar eax, 8
0042786e  25ffff0000               and eax, 0xffff
00427873  89da                     mov edx, ebx
00427875  8945d4                   mov dword ptr [ebp - 0x2c], eax
00427878  b800010000               mov eax, 0x100
0042787d  c1fa1f                   sar edx, 0x1f
00427880  8945cc                   mov dword ptr [ebp - 0x34], eax
00427883  89d8                     mov eax, ebx
00427885  f77dcc                   idiv dword ptr [ebp - 0x34]
00427888  31c0                     xor eax, eax
0042788a  8b5dd0                   mov ebx, dword ptr [ebp - 0x30]
0042788d  6689d0                   mov ax, dx
00427890  8b55d4                   mov edx, dword ptr [ebp - 0x2c]
00427893  e8331e0500               call 0x4796cb ; -> AngleCalcul
00427898  88868b000000             mov byte ptr [esi + 0x8b], al
0042789e  a17c8f5000               mov eax, dword ptr [0x508f7c]
004278a3  31db                     xor ebx, ebx
004278a5  31d2                     xor edx, edx
004278a7  668b1dfa5b4900           mov bx, word ptr [0x495bfa]
004278ae  f7f3                     div ebx
004278b0  85d2                     test edx, edx
004278b2  0f85ab010000             jne 0x427a63
004278b8  8a868b000000             mov al, byte ptr [esi + 0x8b]
004278be  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004278c4  0f8599010000             jne 0x427a63
004278ca  31c0                     xor eax, eax
004278cc  8a467b                   mov al, byte ptr [esi + 0x7b]
004278cf  66c746786400             mov word ptr [esi + 0x78], 0x64
004278d5  83f801                   cmp eax, 1
004278d8  0f85e3000000             jne 0x4279c1
004278de  807e7400                 cmp byte ptr [esi + 0x74], 0
004278e2  0f84bb000000             je 0x4279a3
004278e8  8a868b000000             mov al, byte ptr [esi + 0x8b]
004278ee  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004278f4  0f85a9000000             jne 0x4279a3
004278fa  c6467601                 mov byte ptr [esi + 0x76], 1
004278fe  81e7ffff0000             and edi, 0xffff
00427904  31c0                     xor eax, eax
00427906  57                       push edi
00427907  668b8686000000           mov ax, word ptr [esi + 0x86]
0042790e  31c9                     xor ecx, ecx
00427910  50                       push eax
00427911  31db                     xor ebx, ebx
00427913  31d2                     xor edx, edx
00427915  e824980100               call 0x44113e ; -> EnginGetCase
0042791a  6689c1                   mov cx, ax
0042791d  31c0                     xor eax, eax
0042791f  668b5e02                 mov bx, word ptr [esi + 2]
00427923  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427929  8a5608                   mov dl, byte ptr [esi + 8]
0042792c  e8cfd7ffff               call 0x425100 ; -> RechercheDecalageProjectile
00427931  31c0                     xor eax, eax
00427933  668b8686000000           mov ax, word ptr [esi + 0x86]
0042793a  31d2                     xor edx, edx
0042793c  e804a70100               call 0x442045 ; -> EnginGetPlayer
00427941  88c2                     mov dl, al
00427943  89f8                     mov eax, edi
00427945  e80a24ffff               call 0x419d54 ; -> BatimentDecouvre
0042794a  89f8                     mov eax, edi
0042794c  c1e004                   shl eax, 4
0042794f  01f8                     add eax, edi
00427951  c1e002                   shl eax, 2
00427954  01f8                     add eax, edi
00427956  bac8a04900               mov edx, 0x49a0c8
0042795b  c1e002                   shl eax, 2
0042795e  01c2                     add edx, eax
00427960  8a4204                   mov al, byte ptr [edx + 4]
00427963  3a0541805000             cmp al, byte ptr [0x508041]
00427969  0f8534000000             jne 0x4279a3
0042796f  89f8                     mov eax, edi
00427971  e83527ffff               call 0x41a0ab ; -> BatimentGetVolume
00427976  83ba00010000ff           cmp dword ptr [edx + 0x100], -1
0042797d  0f8520000000             jne 0x4279a3
00427983  50                       push eax
00427984  31c0                     xor eax, eax
00427986  8a4208                   mov al, byte ptr [edx + 8]
00427989  c1e010                   shl eax, 0x10
0042798c  8d9a00010000             lea ebx, [edx + 0x100]
00427992  80cc23                   or ah, 0x23
00427995  31c9                     xor ecx, ecx
00427997  89c2                     mov edx, eax
00427999  b842000000               mov eax, 0x42
0042799e  e8d6300600               call 0x48aa79 ; -> PlaySnd_PostSound
004279a3  8a467b                   mov al, byte ptr [esi + 0x7b]
004279a6  3c01                     cmp al, 1
004279a8  0f826e010000             jb 0x427b1c
004279ae  0f86da000000             jbe 0x427a8e
004279b4  3c03                     cmp al, 3
004279b6  0f84fa000000             je 0x427ab6
004279bc  e95b010000               jmp 0x427b1c
004279c1  83f803                   cmp eax, 3
004279c4  75dd                     jne 0x4279a3
004279c6  807e7400                 cmp byte ptr [esi + 0x74], 0
004279ca  74d7                     je 0x4279a3
004279cc  8a868b000000             mov al, byte ptr [esi + 0x8b]
004279d2  3a868a000000             cmp al, byte ptr [esi + 0x8a]
004279d8  75c9                     jne 0x4279a3
004279da  c6467601                 mov byte ptr [esi + 0x76], 1
004279de  81e7ffff0000             and edi, 0xffff
004279e4  31c0                     xor eax, eax
004279e6  57                       push edi
004279e7  668b8686000000           mov ax, word ptr [esi + 0x86]
004279ee  31c9                     xor ecx, ecx
004279f0  50                       push eax
004279f1  31db                     xor ebx, ebx
004279f3  31d2                     xor edx, edx
004279f5  e8e834ffff               call 0x41aee2 ; -> BatimentGetCase
004279fa  6689c1                   mov cx, ax
004279fd  31c0                     xor eax, eax
004279ff  668b5e02                 mov bx, word ptr [esi + 2]
00427a03  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427a09  8a5608                   mov dl, byte ptr [esi + 8]
00427a0c  e8efd6ffff               call 0x425100 ; -> RechercheDecalageProjectile
00427a11  668b8686000000           mov ax, word ptr [esi + 0x86]
00427a18  31d2                     xor edx, edx
00427a1a  6689c2                   mov dx, ax
00427a1d  89d0                     mov eax, edx
00427a1f  c1e004                   shl eax, 4
00427a22  01d0                     add eax, edx
00427a24  c1e002                   shl eax, 2
00427a27  01d0                     add eax, edx
00427a29  c1e002                   shl eax, 2
00427a2c  05c8a04900               add eax, 0x49a0c8
00427a31  31d2                     xor edx, edx
00427a33  8a4004                   mov al, byte ptr [eax + 4]
00427a36  88c2                     mov dl, al
00427a38  89f8                     mov eax, edi
00427a3a  e81523ffff               call 0x419d54 ; -> BatimentDecouvre
00427a3f  89f8                     mov eax, edi
00427a41  c1e004                   shl eax, 4
00427a44  01f8                     add eax, edi
00427a46  c1e002                   shl eax, 2
00427a49  01f8                     add eax, edi
00427a4b  bac8a04900               mov edx, 0x49a0c8
00427a50  c1e002                   shl eax, 2
00427a53  01c2                     add edx, eax
00427a55  8a3d41805000             mov bh, byte ptr [0x508041]
00427a5b  3a7a04                   cmp bh, byte ptr [edx + 4]
00427a5e  e906ffffff               jmp 0x427969
00427a63  31c0                     xor eax, eax
00427a65  668b4678                 mov ax, word ptr [esi + 0x78]
00427a69  85c0                     test eax, eax
00427a6b  0f8e32ffffff             jle 0x4279a3
00427a71  3dffff0000               cmp eax, 0xffff
00427a76  0f8427ffffff             je 0x4279a3
00427a7c  668b4e78                 mov cx, word ptr [esi + 0x78]
00427a80  c6467600                 mov byte ptr [esi + 0x76], 0
00427a84  49                       dec ecx
00427a85  66894e78                 mov word ptr [esi + 0x78], cx
00427a89  e915ffffff               jmp 0x4279a3
00427a8e  31c0                     xor eax, eax
00427a90  668b8686000000           mov ax, word ptr [esi + 0x86]
00427a97  e811c30100               call 0x443dad ; -> EnginEstVivant
00427a9c  84c0                     test al, al
00427a9e  0f8578000000             jne 0x427b1c
00427aa4  66c78686000000ffff       mov word ptr [esi + 0x86], 0xffff
00427aad  c6467bff                 mov byte ptr [esi + 0x7b], 0xff
00427ab1  884674                   mov byte ptr [esi + 0x74], al
00427ab4  eb66                     jmp 0x427b1c
00427ab6  668b8686000000           mov ax, word ptr [esi + 0x86]
00427abd  31d2                     xor edx, edx
00427abf  6689c2                   mov dx, ax
00427ac2  89d0                     mov eax, edx
00427ac4  c1e004                   shl eax, 4
00427ac7  01d0                     add eax, edx
00427ac9  c1e002                   shl eax, 2
00427acc  01d0                     add eax, edx
00427ace  c1e002                   shl eax, 2
00427ad1  05c8a04900               add eax, 0x49a0c8
00427ad6  8a4005                   mov al, byte ptr [eax + 5]
00427ad9  25ff000000               and eax, 0xff
00427ade  0f95c0                   setne al
00427ae1  ebb9                     jmp 0x427a9c
00427ae3  b80d000000               mov eax, 0xd
00427ae8  bb64000000               mov ebx, 0x64
00427aed  31d2                     xor edx, edx
00427aef  e8e8890400               call 0x4704dc ; -> Random
00427af4  f7f3                     div ebx
00427af6  85d2                     test edx, edx
00427af8  7522                     jne 0x427b1c
00427afa  8a868b000000             mov al, byte ptr [esi + 0x8b]
00427b00  3a868a000000             cmp al, byte ptr [esi + 0x8a]
00427b06  7514                     jne 0x427b1c
00427b08  b80e000000               mov eax, 0xe
00427b0d  e8ca890400               call 0x4704dc ; -> Random
00427b12  241f                     and al, 0x1f
00427b14  fec0                     inc al
00427b16  88868b000000             mov byte ptr [esi + 0x8b], al
00427b1c  8a868b000000             mov al, byte ptr [esi + 0x8b]
00427b22  8a968a000000             mov dl, byte ptr [esi + 0x8a]
00427b28  38d0                     cmp al, dl
00427b2a  0f8490060000             je 0x4281c0
00427b30  f6057c8f500001           test byte ptr [0x508f7c], 1
00427b37  0f8583060000             jne 0x4281c0
00427b3d  38d0                     cmp al, dl
00427b3f  7613                     jbe 0x427b54
00427b41  31d2                     xor edx, edx
00427b43  88c2                     mov dl, al
00427b45  31c0                     xor eax, eax
00427b47  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427b4d  29c2                     sub edx, eax
00427b4f  83fa10                   cmp edx, 0x10
00427b52  7c23                     jl 0x427b77
00427b54  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427b5a  8abe8b000000             mov bh, byte ptr [esi + 0x8b]
00427b60  38f8                     cmp al, bh
00427b62  7633                     jbe 0x427b97
00427b64  31d2                     xor edx, edx
00427b66  31c0                     xor eax, eax
00427b68  88fa                     mov dl, bh
00427b6a  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427b70  29d0                     sub eax, edx
00427b72  83f810                   cmp eax, 0x10
00427b75  7e20                     jle 0x427b97
00427b77  31d2                     xor edx, edx
00427b79  8a968a000000             mov dl, byte ptr [esi + 0x8a]
00427b7f  bb20000000               mov ebx, 0x20
00427b84  89d0                     mov eax, edx
00427b86  c1fa1f                   sar edx, 0x1f
00427b89  f7fb                     idiv ebx
00427b8b  42                       inc edx
00427b8c  88968a000000             mov byte ptr [esi + 0x8a], dl
00427b92  e929060000               jmp 0x4281c0
00427b97  31c0                     xor eax, eax
00427b99  8a868a000000             mov al, byte ptr [esi + 0x8a]
00427b9f  83f801                   cmp eax, 1
00427ba2  7403                     je 0x427ba7
00427ba4  48                       dec eax
00427ba5  eb05                     jmp 0x427bac
00427ba7  b820000000               mov eax, 0x20
00427bac  88868a000000             mov byte ptr [esi + 0x8a], al
00427bb2  e909060000               jmp 0x4281c0
00427bb7  803daf99500000           cmp byte ptr [0x5099af], 0
00427bbe  0f84e3000000             je 0x427ca7
00427bc4  803d50fb4d0000           cmp byte ptr [0x4dfb50], 0
00427bcb  0f85d6000000             jne 0x427ca7
00427bd1  31c0                     xor eax, eax
00427bd3  b101                     mov cl, 1
00427bd5  a041805000               mov al, byte ptr [0x508041]
00427bda  880d50fb4d00             mov byte ptr [0x4dfb50], cl
00427be0  e8b4ebffff               call 0x426799 ; -> HerseSousCurseur
00427be5  89c3                     mov ebx, eax
00427be7  31c0                     xor eax, eax
00427be9  6689d8                   mov ax, bx
00427bec  3dffff0000               cmp eax, 0xffff
00427bf1  0f84b0000000             je 0x427ca7
00427bf7  31d2                     xor edx, edx
00427bf9  6689da                   mov dx, bx
00427bfc  89d0                     mov eax, edx
00427bfe  c1e004                   shl eax, 4
00427c01  01d0                     add eax, edx
00427c03  c1e002                   shl eax, 2
00427c06  01d0                     add eax, edx
00427c08  668b0c85caa04900         mov cx, word ptr [eax*4 + 0x49a0ca]
00427c10  89d8                     mov eax, ebx
00427c12  31db                     xor ebx, ebx
00427c14  6689c3                   mov bx, ax
00427c17  89d8                     mov eax, ebx
00427c19  c1e004                   shl eax, 4
00427c1c  01d8                     add eax, ebx
00427c1e  c1e002                   shl eax, 2
00427c21  01d8                     add eax, ebx
00427c23  c1e002                   shl eax, 2
00427c26  8945cc                   mov dword ptr [ebp - 0x34], eax
00427c29  b8c8a04900               mov eax, 0x49a0c8
00427c2e  0345cc                   add eax, dword ptr [ebp - 0x34]
00427c31  31db                     xor ebx, ebx
00427c33  8a5876                   mov bl, byte ptr [eax + 0x76]
00427c36  85db                     test ebx, ebx
00427c38  741a                     je 0x427c54
00427c3a  31db                     xor ebx, ebx
00427c3c  8a5876                   mov bl, byte ptr [eax + 0x76]
00427c3f  83fb0f                   cmp ebx, 0xf
00427c42  7410                     je 0x427c54
00427c44  88d8                     mov al, bl
00427c46  25ff000000               and eax, 0xff
00427c4b  83f81f                   cmp eax, 0x1f
00427c4e  7404                     je 0x427c54
00427c50  b001                     mov al, 1
00427c52  eb02                     jmp 0x427c56
00427c54  30c0                     xor al, al
00427c56  84c0                     test al, al
00427c58  754d                     jne 0x427ca7
00427c5a  31db                     xor ebx, ebx
00427c5c  6689d3                   mov bx, dx
00427c5f  89d8                     mov eax, ebx
00427c61  c1e004                   shl eax, 4
00427c64  01d8                     add eax, ebx
00427c66  c1e002                   shl eax, 2
00427c69  01d8                     add eax, ebx
00427c6b  c1e002                   shl eax, 2
00427c6e  05c8a04900               add eax, 0x49a0c8
00427c73  8a4076                   mov al, byte ptr [eax + 0x76]
00427c76  25ff000000               and eax, 0xff
00427c7b  83f80f                   cmp eax, 0xf
00427c7e  0f94c0                   sete al
00427c81  84c0                     test al, al
00427c83  7412                     je 0x427c97
00427c85  31c0                     xor eax, eax
00427c87  81e2ffff0000             and edx, 0xffff
00427c8d  6689c8                   mov ax, cx
00427c90  e83519ffff               call 0x4195ca ; -> RemonteTouteHerse
00427c95  eb10                     jmp 0x427ca7
00427c97  31c0                     xor eax, eax
00427c99  81e2ffff0000             and edx, 0xffff
00427c9f  6689c8                   mov ax, cx
00427ca2  e82d17ffff               call 0x4193d4 ; -> BaisseTouteHerse
00427ca7  31d2                     xor edx, edx
00427ca9  6689fa                   mov dx, di
00427cac  89d0                     mov eax, edx
00427cae  c1e004                   shl eax, 4
00427cb1  01d0                     add eax, edx
00427cb3  c1e002                   shl eax, 2
00427cb6  01d0                     add eax, edx
00427cb8  c1e002                   shl eax, 2
00427cbb  05c8a04900               add eax, 0x49a0c8
00427cc0  8a4076                   mov al, byte ptr [eax + 0x76]
00427cc3  25ff000000               and eax, 0xff
00427cc8  740e                     je 0x427cd8
00427cca  83f80f                   cmp eax, 0xf
00427ccd  7409                     je 0x427cd8
00427ccf  83f81f                   cmp eax, 0x1f
00427cd2  7404                     je 0x427cd8
00427cd4  b001                     mov al, 1
00427cd6  eb02                     jmp 0x427cda
00427cd8  30c0                     xor al, al
00427cda  84c0                     test al, al
00427cdc  0f84de040000             je 0x4281c0
00427ce2  8a6e76                   mov ch, byte ptr [esi + 0x76]
00427ce5  31c0                     xor eax, eax
00427ce7  fec5                     inc ch
00427ce9  88e8                     mov al, ch
00427ceb  886e76                   mov byte ptr [esi + 0x76], ch
00427cee  83f81f                   cmp eax, 0x1f
00427cf1  7c04                     jl 0x427cf7
00427cf3  c6467600                 mov byte ptr [esi + 0x76], 0
00427cf7  31c0                     xor eax, eax
00427cf9  8a4676                   mov al, byte ptr [esi + 0x76]
00427cfc  83f80f                   cmp eax, 0xf
00427cff  7532                     jne 0x427d33
00427d01  ba01000000               mov edx, 1
00427d06  31c0                     xor eax, eax
00427d08  bb01000000               mov ebx, 1
00427d0d  668b4602                 mov ax, word ptr [esi + 2]
00427d11  8d8ecc000000             lea ecx, [esi + 0xcc]
00427d17  e822e50400               call 0x47623e ; -> ResetCollision
00427d1c  6a00                     push 0
00427d1e  31d2                     xor edx, edx
00427d20  31c0                     xor eax, eax
00427d22  6689fa                   mov dx, di
00427d25  668b4602                 mov ax, word ptr [esi + 2]
00427d29  e80a640100               call 0x43e138 ; -> Chemin_ModifieZone
00427d2e  e98d040000               jmp 0x4281c0
00427d33  83f81f                   cmp eax, 0x1f
00427d36  7d08                     jge 0x427d40
00427d38  85c0                     test eax, eax
00427d3a  0f8580040000             jne 0x4281c0
00427d40  ba01000000               mov edx, 1
00427d45  31c0                     xor eax, eax
00427d47  bb03000000               mov ebx, 3
00427d4c  668b4602                 mov ax, word ptr [esi + 2]
00427d50  8d8ecc000000             lea ecx, [esi + 0xcc]
00427d56  e8d3e40400               call 0x47622e ; -> SetCollision
00427d5b  ebbf                     jmp 0x427d1c
00427d5d  31d2                     xor edx, edx
00427d5f  89f3                     mov ebx, esi
00427d61  88c2                     mov dl, al
00427d63  8d460c                   lea eax, [esi + 0xc]
00427d66  83fa15                   cmp edx, 0x15
00427d69  7514                     jne 0x427d7f
00427d6b  e8daf40100               call 0x44724a ; -> BagContientTroupe
00427d70  84c0                     test al, al
00427d72  0f84fcebffff             je 0x426974
00427d78  b001                     mov al, 1
00427d7a  e9f7ebffff               jmp 0x426976
00427d7f  83fa02                   cmp edx, 2
00427d82  7509                     jne 0x427d8d
00427d84  e8c1f40100               call 0x44724a ; -> BagContientTroupe
00427d89  84c0                     test al, al
00427d8b  75eb                     jne 0x427d78
00427d8d  8d430c                   lea eax, [ebx + 0xc]
00427d90  ba01000000               mov edx, 1
00427d95  bb09000000               mov ebx, 9
00427d9a  e819f40100               call 0x4471b8 ; -> BagContient
00427d9f  6685c0                   test ax, ax
00427da2  ebce                     jmp 0x427d72
00427da4  31d2                     xor edx, edx
00427da6  89f3                     mov ebx, esi
00427da8  88c2                     mov dl, al
00427daa  8d460c                   lea eax, [esi + 0xc]
00427dad  83fa15                   cmp edx, 0x15
00427db0  750d                     jne 0x427dbf
00427db2  e893f40100               call 0x44724a ; -> BagContientTroupe
00427db7  84c0                     test al, al
00427db9  7429                     je 0x427de4
00427dbb  b001                     mov al, 1
00427dbd  eb27                     jmp 0x427de6
00427dbf  83fa02                   cmp edx, 2
00427dc2  7509                     jne 0x427dcd
00427dc4  e881f40100               call 0x44724a ; -> BagContientTroupe
00427dc9  84c0                     test al, al
00427dcb  75ee                     jne 0x427dbb
00427dcd  8d430c                   lea eax, [ebx + 0xc]
00427dd0  ba01000000               mov edx, 1
00427dd5  bb09000000               mov ebx, 9
00427dda  e8d9f30100               call 0x4471b8 ; -> BagContient
00427ddf  6685c0                   test ax, ax
00427de2  ebd5                     jmp 0x427db9
00427de4  30c0                     xor al, al
00427de6  84c0                     test al, al
00427de8  0f84d2030000             je 0x4281c0
00427dee  807e7500                 cmp byte ptr [esi + 0x75], 0
00427df2  741d                     je 0x427e11
00427df4  31c0                     xor eax, eax
00427df6  8a8604010000             mov al, byte ptr [esi + 0x104]
00427dfc  85c0                     test eax, eax
00427dfe  7511                     jne 0x427e11
00427e00  c7860801000001000000     mov dword ptr [esi + 0x108], 1
00427e0a  c6860401000001           mov byte ptr [esi + 0x104], 1
00427e11  31d2                     xor edx, edx
00427e13  6689fa                   mov dx, di
00427e16  89d0                     mov eax, edx
00427e18  e8fbe5ffff               call 0x426418 ; -> InitNova
00427e1d  89d0                     mov eax, edx
00427e1f  e8c2dbffff               call 0x4259e6 ; -> CalculTroupe
00427e24  8b467e                   mov eax, dword ptr [esi + 0x7e]
00427e27  c1f810                   sar eax, 0x10
00427e2a  85c0                     test eax, eax
00427e2c  7e0c                     jle 0x427e3a
00427e2e  66ff8e80000000           dec word ptr [esi + 0x80]
00427e35  e986030000               jmp 0x4281c0
00427e3a  31d2                     xor edx, edx
00427e3c  8a5608                   mov dl, byte ptr [esi + 8]
00427e3f  89d0                     mov eax, edx
00427e41  c1e002                   shl eax, 2
00427e44  29d0                     sub eax, edx
00427e46  c1e002                   shl eax, 2
00427e49  01d0                     add eax, edx
00427e4b  668b0485905d4900         mov ax, word ptr [eax*4 + 0x495d90]
00427e53  8b9680000000             mov edx, dword ptr [esi + 0x80]
00427e59  25ffff0000               and eax, 0xffff
00427e5e  c1fa10                   sar edx, 0x10
00427e61  39c2                     cmp edx, eax
00427e63  7d1f                     jge 0x427e84
00427e65  668b9682000000           mov dx, word ptr [esi + 0x82]
00427e6c  66c786800000001400       mov word ptr [esi + 0x80], 0x14
00427e75  83c214                   add edx, 0x14
00427e78  66899682000000           mov word ptr [esi + 0x82], dx
00427e7f  e93c030000               jmp 0x4281c0
00427e84  8a4604                   mov al, byte ptr [esi + 4]
00427e87  31d2                     xor edx, edx
00427e89  88c2                     mov dl, al
00427e8b  89d0                     mov eax, edx
00427e8d  c1e003                   shl eax, 3
00427e90  01d0                     add eax, edx
00427e92  c1e004                   shl eax, 4
00427e95  29d0                     sub eax, edx
00427e97  c1e004                   shl eax, 4
00427e9a  05e8d64d00               add eax, 0x4dd6e8
00427e9f  8db820080000             lea edi, [eax + 0x820]
00427ea5  ba02000000               mov edx, 2
00427eaa  89f8                     mov eax, edi
00427eac  bb04000000               mov ebx, 4
00427eb1  e892f20100               call 0x447148 ; -> BagInit
00427eb6  ba06000000               mov edx, 6
00427ebb  89f8                     mov eax, edi
00427ebd  e8c1f50100               call 0x447483 ; -> BagPrend
00427ec2  bb04000000               mov ebx, 4
00427ec7  89f8                     mov eax, edi
00427ec9  89da                     mov edx, ebx
00427ecb  e8b3f50100               call 0x447483 ; -> BagPrend
00427ed0  c6467501                 mov byte ptr [esi + 0x75], 1
00427ed4  e9e7020000               jmp 0x4281c0
00427ed9  89d0                     mov eax, edx
00427edb  e8fecaffff               call 0x4249de ; -> CristalCherchePretre
00427ee0  66898686000000           mov word ptr [esi + 0x86], ax
00427ee7  e9d4020000               jmp 0x4281c0
00427eec  31d2                     xor edx, edx
00427eee  89f3                     mov ebx, esi
00427ef0  88c2                     mov dl, al
00427ef2  8d460c                   lea eax, [esi + 0xc]
00427ef5  83fa15                   cmp edx, 0x15
00427ef8  750d                     jne 0x427f07
00427efa  e84bf30100               call 0x44724a ; -> BagContientTroupe
00427eff  84c0                     test al, al
00427f01  7429                     je 0x427f2c
00427f03  b001                     mov al, 1
00427f05  eb27                     jmp 0x427f2e
00427f07  83fa02                   cmp edx, 2
00427f0a  7509                     jne 0x427f15
00427f0c  e839f30100               call 0x44724a ; -> BagContientTroupe
00427f11  84c0                     test al, al
00427f13  75ee                     jne 0x427f03
00427f15  8d430c                   lea eax, [ebx + 0xc]
00427f18  ba01000000               mov edx, 1
00427f1d  bb09000000               mov ebx, 9
00427f22  e891f20100               call 0x4471b8 ; -> BagContient
00427f27  6685c0                   test ax, ax
00427f2a  ebd5                     jmp 0x427f01
00427f2c  30c0                     xor al, al
00427f2e  84c0                     test al, al
00427f30  0f848a020000             je 0x4281c0
00427f36  807e7400                 cmp byte ptr [esi + 0x74], 0
00427f3a  741c                     je 0x427f58
00427f3c  807e7a00                 cmp byte ptr [esi + 0x7a], 0
00427f40  740c                     je 0x427f4e
00427f42  31c0                     xor eax, eax
00427f44  6689f8                   mov ax, di
00427f47  e8109affff               call 0x42195c ; -> CalculReparation
00427f4c  eb0a                     jmp 0x427f58
00427f4e  31c0                     xor eax, eax
00427f50  6689f8                   mov ax, di
00427f53  e88edaffff               call 0x4259e6 ; -> CalculTroupe
00427f58  31c0                     xor eax, eax
00427f5a  8a4604                   mov al, byte ptr [esi + 4]
00427f5d  31db                     xor ebx, ebx
00427f5f  ba10000000               mov edx, 0x10
00427f64  8a984cfb4d00             mov bl, byte ptr [eax + 0x4dfb4c]
00427f6a  e823ee0200               call 0x456d92 ; -> TypeEnginGetNb
00427f6f  25ffff0000               and eax, 0xffff
00427f74  39c3                     cmp ebx, eax
00427f76  7e5d                     jle 0x427fd5
00427f78  8a4604                   mov al, byte ptr [esi + 4]
00427f7b  31d2                     xor edx, edx
00427f7d  88c2                     mov dl, al
00427f7f  89d0                     mov eax, edx
00427f81  c1e003                   shl eax, 3
00427f84  01d0                     add eax, edx
00427f86  c1e004                   shl eax, 4
00427f89  29d0                     sub eax, edx
00427f8b  c1e004                   shl eax, 4
00427f8e  05e8d64d00               add eax, 0x4dd6e8
00427f93  bb10000000               mov ebx, 0x10
00427f98  8db050070000             lea esi, [eax + 0x750]
00427f9e  ba06000000               mov edx, 6
00427fa3  89f0                     mov eax, esi
00427fa5  e80ef20100               call 0x4471b8 ; -> BagContient
00427faa  6685c0                   test ax, ax
00427fad  0f850d020000             jne 0x4281c0
00427fb3  ba01000000               mov edx, 1
00427fb8  89f0                     mov eax, esi
00427fba  bb10000000               mov ebx, 0x10
00427fbf  e884f10100               call 0x447148 ; -> BagInit
00427fc4  ba06000000               mov edx, 6
00427fc9  89f0                     mov eax, esi
00427fcb  e8b3f40100               call 0x447483 ; -> BagPrend
00427fd0  e9eb010000               jmp 0x4281c0
00427fd5  31c0                     xor eax, eax
00427fd7  8a4604                   mov al, byte ptr [esi + 4]
00427fda  31db                     xor ebx, ebx
00427fdc  ba10000000               mov edx, 0x10
00427fe1  8a984cfb4d00             mov bl, byte ptr [eax + 0x4dfb4c]
00427fe7  e8a6ed0200               call 0x456d92 ; -> TypeEnginGetNb
00427fec  25ffff0000               and eax, 0xffff
00427ff1  39c3                     cmp ebx, eax
00427ff3  0f8fc7010000             jg 0x4281c0
00427ff9  8a4604                   mov al, byte ptr [esi + 4]
00427ffc  31d2                     xor edx, edx
00427ffe  88c2                     mov dl, al
00428000  89d0                     mov eax, edx
00428002  c1e003                   shl eax, 3
00428005  01d0                     add eax, edx
00428007  c1e004                   shl eax, 4
0042800a  29d0                     sub eax, edx
0042800c  c1e004                   shl eax, 4
0042800f  05e8d64d00               add eax, 0x4dd6e8
00428014  8db050070000             lea esi, [eax + 0x750]
0042801a  ba01000000               mov edx, 1
0042801f  89f0                     mov eax, esi
00428021  bb10000000               mov ebx, 0x10
00428026  e81df10100               call 0x447148 ; -> BagInit
0042802b  ba06000000               mov edx, 6
00428030  89f0                     mov eax, esi
00428032  e8b3f20100               call 0x4472ea ; -> BagRetire
00428037  e984010000               jmp 0x4281c0
0042803c  31d2                     xor edx, edx
0042803e  89f3                     mov ebx, esi
00428040  88c2                     mov dl, al
00428042  8d460c                   lea eax, [esi + 0xc]
00428045  83fa15                   cmp edx, 0x15
00428048  750d                     jne 0x428057
0042804a  e8fbf10100               call 0x44724a ; -> BagContientTroupe
0042804f  84c0                     test al, al
00428051  7429                     je 0x42807c
00428053  b001                     mov al, 1
00428055  eb27                     jmp 0x42807e
00428057  83fa02                   cmp edx, 2
0042805a  7509                     jne 0x428065
0042805c  e8e9f10100               call 0x44724a ; -> BagContientTroupe
00428061  84c0                     test al, al
00428063  75ee                     jne 0x428053
00428065  8d430c                   lea eax, [ebx + 0xc]
00428068  ba01000000               mov edx, 1
0042806d  bb09000000               mov ebx, 9
00428072  e841f10100               call 0x4471b8 ; -> BagContient
00428077  6685c0                   test ax, ax
0042807a  ebd5                     jmp 0x428051
0042807c  30c0                     xor al, al
0042807e  84c0                     test al, al
00428080  0f843a010000             je 0x4281c0
00428086  31c0                     xor eax, eax
00428088  6689f8                   mov ax, di
0042808b  e89ecbffff               call 0x424c2e ; -> BatimentSoignePerso
00428090  e92b010000               jmp 0x4281c0
00428095  31d2                     xor edx, edx
00428097  6689fa                   mov dx, di
0042809a  89d0                     mov eax, edx
0042809c  c1e004                   shl eax, 4
0042809f  01d0                     add eax, edx
004280a1  c1e002                   shl eax, 2
004280a4  01d0                     add eax, edx
004280a6  b9c8a04900               mov ecx, 0x49a0c8
004280ab  c1e002                   shl eax, 2
004280ae  89fb                     mov ebx, edi
004280b0  01c1                     add ecx, eax
004280b2  89f8                     mov eax, edi
004280b4  25ffff0000               and eax, 0xffff
004280b9  89c2                     mov edx, eax
004280bb  c1e004                   shl eax, 4
004280be  01d0                     add eax, edx
004280c0  c1e002                   shl eax, 2
004280c3  01d0                     add eax, edx
004280c5  bac8a04900               mov edx, 0x49a0c8
004280ca  c1e002                   shl eax, 2
004280cd  01d0                     add eax, edx
004280cf  8a4008                   mov al, byte ptr [eax + 8]
004280d2  25ff000000               and eax, 0xff
004280d7  83f815                   cmp eax, 0x15
004280da  7510                     jne 0x4280ec
004280dc  8d410c                   lea eax, [ecx + 0xc]
004280df  e866f10100               call 0x44724a ; -> BagContientTroupe
004280e4  84c0                     test al, al
004280e6  744e                     je 0x428136
004280e8  b001                     mov al, 1
004280ea  eb4c                     jmp 0x428138
004280ec  31d2                     xor edx, edx
004280ee  6689fa                   mov dx, di
004280f1  89d0                     mov eax, edx
004280f3  c1e004                   shl eax, 4
004280f6  01d0                     add eax, edx
004280f8  c1e002                   shl eax, 2
004280fb  01c2                     add edx, eax
004280fd  b8c8a04900               mov eax, 0x49a0c8
00428102  c1e202                   shl edx, 2
00428105  8a440208                 mov al, byte ptr [edx + eax + 8]
00428109  25ff000000               and eax, 0xff
0042810e  83f802                   cmp eax, 2
00428111  750c                     jne 0x42811f
00428113  8d410c                   lea eax, [ecx + 0xc]
00428116  e82ff10100               call 0x44724a ; -> BagContientTroupe
0042811b  84c0                     test al, al
0042811d  75c9                     jne 0x4280e8
0042811f  bb09000000               mov ebx, 9
00428124  ba01000000               mov edx, 1
00428129  8d410c                   lea eax, [ecx + 0xc]
0042812c  e887f00100               call 0x4471b8 ; -> BagContient
00428131  6685c0                   test ax, ax
00428134  ebb0                     jmp 0x4280e6
00428136  30c0                     xor al, al
00428138  84c0                     test al, al
0042813a  0f8480000000             je 0x4281c0
00428140  31c0                     xor eax, eax
00428142  6689f8                   mov ax, di
00428145  e89cd8ffff               call 0x4259e6 ; -> CalculTroupe
0042814a  31c0                     xor eax, eax
0042814c  668b467c                 mov ax, word ptr [esi + 0x7c]
00428150  3df4010000               cmp eax, 0x1f4
00428155  7508                     jne 0x42815f
00428157  66c7467c0000             mov word ptr [esi + 0x7c], 0
0042815d  eb07                     jmp 0x428166
0042815f  89c7                     mov edi, eax
00428161  47                       inc edi
00428162  66897e7c                 mov word ptr [esi + 0x7c], di
00428166  8b467e                   mov eax, dword ptr [esi + 0x7e]
00428169  c1f810                   sar eax, 0x10
0042816c  3dfa000000               cmp eax, 0xfa
00428171  750b                     jne 0x42817e
00428173  66c786800000000000       mov word ptr [esi + 0x80], 0
0042817c  eb07                     jmp 0x428185
0042817e  66ff8680000000           inc word ptr [esi + 0x80]
00428185  8b8680000000             mov eax, dword ptr [esi + 0x80]
0042818b  c1f810                   sar eax, 0x10
0042818e  3d68010000               cmp eax, 0x168
00428193  750b                     jne 0x4281a0
00428195  66c786820000000000       mov word ptr [esi + 0x82], 0
0042819e  eb07                     jmp 0x4281a7
004281a0  66ff8682000000           inc word ptr [esi + 0x82]
004281a7  8b467c                   mov eax, dword ptr [esi + 0x7c]
004281aa  c1f810                   sar eax, 0x10
004281ad  3da0000000               cmp eax, 0xa0
004281b2  7508                     jne 0x4281bc
004281b4  66c7467e0000             mov word ptr [esi + 0x7e], 0
004281ba  eb04                     jmp 0x4281c0
004281bc  66ff467e                 inc word ptr [esi + 0x7e]
004281c0  89ec                     mov esp, ebp
004281c2  e95659ffff               jmp 0x41db1d

; shared Watcom tail reached from BatimentNextEtape; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0041db1d..0x0041db24 (end exclusive); labels are original SBL names
0041db1d  5d                       pop ebp
0041db1e  5f                       pop edi
0041db1f  5e                       pop esi
0041db20  5a                       pop edx
0041db21  59                       pop ecx
0041db22  5b                       pop ebx
0041db23  c3                       ret
