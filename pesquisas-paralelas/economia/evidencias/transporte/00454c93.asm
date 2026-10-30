; EnginNextEtape saved-state checks; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00454c93  31c0                     xor eax, eax
00454c95  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454c9c  3dffff0000               cmp eax, 0xffff
00454ca1  0f84ad080000             je 0x455554
00454ca7  31c0                     xor eax, eax
00454ca9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454cb0  e8565afcff               call 0x41a70b
00454cb5  84c0                     test al, al
00454cb7  0f8497080000             je 0x455554
00454cbd  31c0                     xor eax, eax
00454cbf  31d2                     xor edx, edx
00454cc1  6689f8                   mov ax, di
00454cc4  668b567e                 mov dx, word ptr [esi + 0x7e]
00454cc8  e8060bffff               call 0x4457d3
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
00454d8a  e87c59fcff               call 0x41a70b
00454d8f  84c0                     test al, al
00454d91  0f84bd070000             je 0x455554
00454d97  31c0                     xor eax, eax
00454d99  31d2                     xor edx, edx
00454d9b  6689f8                   mov ax, di
00454d9e  668b567e                 mov dx, word ptr [esi + 0x7e]
00454da2  e82c0affff               call 0x4457d3
00454da7  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
00454db0  e918ffffff               jmp 0x454ccd
00454db5  31c0                     xor eax, eax
00454db7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454dbe  e84859fcff               call 0x41a70b
00454dc3  84c0                     test al, al
00454dc5  7516                     jne 0x454ddd
00454dc7  31c0                     xor eax, eax
00454dc9  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00454dd0  e8b752fcff               call 0x41a08c
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
00454e0f  e8a0defeff               call 0x442cb4
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
00454e64  e8e8190200               call 0x476851
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
00454e8c  e8221e0200               call 0x476cb3
00454e91  ba04000000               mov edx, 4
00454e96  31db                     xor ebx, ebx
00454e98  31c0                     xor eax, eax
00454e9a  668b5c2424               mov bx, word ptr [esp + 0x24]
00454e9f  8a01                     mov al, byte ptr [ecx]
00454ea1  e8e2540100               call 0x46a388
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
00454ed9  e82d58fcff               call 0x41a70b
00454ede  84c0                     test al, al
00454ee0  7516                     jne 0x454ef8
00454ee2  31c0                     xor eax, eax
00454ee4  668b8680000000           mov ax, word ptr [esi + 0x80]
00454eeb  e89c51fcff               call 0x41a08c
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
00454f26  e889ddfeff               call 0x442cb4
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
00454f73  e8d9180200               call 0x476851
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
00454f95  e8191d0200               call 0x476cb3
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
00454fc7  e83f57fcff               call 0x41a70b
00454fcc  84c0                     test al, al
00454fce  7516                     jne 0x454fe6
00454fd0  31c0                     xor eax, eax
00454fd2  668b8680000000           mov ax, word ptr [esi + 0x80]
00454fd9  e8ae50fcff               call 0x41a08c
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
00455018  e897dcfeff               call 0x442cb4
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
0045506d  e8df170200               call 0x476851
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
0045508f  e81f1c0200               call 0x476cb3
00455094  ba04000000               mov edx, 4
00455099  31db                     xor ebx, ebx
0045509b  31c0                     xor eax, eax
0045509d  668b5c2440               mov bx, word ptr [esp + 0x40]
004550a2  8a01                     mov al, byte ptr [ecx]
004550a4  e8df520100               call 0x46a388
004550a9  31c0                     xor eax, eax
004550ab  31d2                     xor edx, edx
004550ad  6689f8                   mov ax, di
004550b0  668b567e                 mov dx, word ptr [esi + 0x7e]
004550b4  e81a07ffff               call 0x4457d3
004550b9  c6868200000000           mov byte ptr [esi + 0x82], 0
004550c0  66c78680000000ffff       mov word ptr [esi + 0x80], 0xffff
004550c9  e9fffbffff               jmp 0x454ccd
004550ce  31c0                     xor eax, eax
004550d0  8a8682000000             mov al, byte ptr [esi + 0x82]
004550d6  83f802                   cmp eax, 2
004550d9  0f8575040000             jne 0x455554
004550df  31c0                     xor eax, eax
004550e1  668b8680000000           mov ax, word ptr [esi + 0x80]
004550e8  e81e56fcff               call 0x41a70b
004550ed  84c0                     test al, al
004550ef  7516                     jne 0x455107
004550f1  31c0                     xor eax, eax
004550f3  668b8680000000           mov ax, word ptr [esi + 0x80]
004550fa  e88d4ffcff               call 0x41a08c
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
00455139  e8a0030200               call 0x4754de
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
00455166  e849dbfeff               call 0x442cb4
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
004551bc  e890160200               call 0x476851
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
004551de  e8d01a0200               call 0x476cb3
004551e3  ba04000000               mov edx, 4
004551e8  31db                     xor ebx, ebx
004551ea  31c0                     xor eax, eax
004551ec  668b5c2430               mov bx, word ptr [esp + 0x30]
004551f1  e9acfeffff               jmp 0x4550a2
004551f6  31c0                     xor eax, eax
004551f8  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004551ff  e80755fcff               call 0x41a70b
00455204  84c0                     test al, al
00455206  0f858bfbffff             jne 0x454d97
0045520c  31c0                     xor eax, eax
0045520e  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455215  e8724efcff               call 0x41a08c
0045521a  25ff000000               and eax, 0xff
0045521f  3dc8000000               cmp eax, 0xc8
00455224  0f846dfbffff             je 0x454d97
0045522a  31c0                     xor eax, eax
0045522c  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455233  e8544efcff               call 0x41a08c
00455238  3a06                     cmp al, byte ptr [esi]
0045523a  0f8514030000             jne 0x455554
00455240  e952fbffff               jmp 0x454d97
00455245  31c0                     xor eax, eax
00455247  668b86b8000000           mov ax, word ptr [esi + 0xb8]
0045524e  3dffff0000               cmp eax, 0xffff
00455253  7427                     je 0x45527c
00455255  e8b154fcff               call 0x41a70b
0045525a  84c0                     test al, al
0045525c  751e                     jne 0x45527c
0045525e  31c0                     xor eax, eax
00455260  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455267  e8204efcff               call 0x41a08c
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
0045529b  e877850100               call 0x46d817
004552a0  25ff000000               and eax, 0xff
004552a5  83f802                   cmp eax, 2
004552a8  7513                     jne 0x4552bd
004552aa  ba4a000000               mov edx, 0x4a
004552af  89c8                     mov eax, ecx
004552b1  31db                     xor ebx, ebx
004552b3  e810d70200               call 0x4829c8
004552b8  e997020000               jmp 0x455554
004552bd  31d2                     xor edx, edx
004552bf  89c8                     mov eax, ecx
004552c1  668b567e                 mov dx, word ptr [esi + 0x7e]
004552c5  e80905ffff               call 0x4457d3
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
0045537b  e897840100               call 0x46d817
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
004553cd  e83953fcff               call 0x41a70b
004553d2  84c0                     test al, al
004553d4  0f85bdf9ffff             jne 0x454d97
004553da  31c0                     xor eax, eax
004553dc  8a4601                   mov al, byte ptr [esi + 1]
004553df  83f80a                   cmp eax, 0xa
004553e2  0f8424feffff             je 0x45520c
004553e8  31c0                     xor eax, eax
004553ea  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004553f1  e8964cfcff               call 0x41a08c
004553f6  3a06                     cmp al, byte ptr [esi]
004553f8  0f8456010000             je 0x455554
004553fe  31c0                     xor eax, eax
00455400  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455407  e8804cfcff               call 0x41a08c
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
