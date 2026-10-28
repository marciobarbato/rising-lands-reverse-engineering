; SetDyingEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00444938  53                       push ebx
00444939  51                       push ecx
0044493a  52                       push edx
0044493b  56                       push esi
0044493c  57                       push edi
0044493d  55                       push ebp
0044493e  89c7                     mov edi, eax
00444940  31d2                     xor edx, edx
00444942  6689c2                   mov dx, ax
00444945  89d0                     mov eax, edx
00444947  c1e004                   shl eax, 4
0044494a  01d0                     add eax, edx
0044494c  c1e002                   shl eax, 2
0044494f  01d0                     add eax, edx
00444951  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
00444957  c1e002                   shl eax, 2
0044495a  01c6                     add esi, eax
0044495c  31c0                     xor eax, eax
0044495e  8a4602                   mov al, byte ptr [esi + 2]
00444961  85c0                     test eax, eax
00444963  7409                     je 0x44496e
00444965  83f804                   cmp eax, 4
00444968  7404                     je 0x44496e
0044496a  b001                     mov al, 1
0044496c  eb02                     jmp 0x444970
0044496e  30c0                     xor al, al
00444970  84c0                     test al, al
00444972  0f84cf020000             je 0x444c47
00444978  31c9                     xor ecx, ecx
0044497a  6689f9                   mov cx, di
0044497d  89cd                     mov ebp, ecx
0044497f  c1e504                   shl ebp, 4
00444982  01cd                     add ebp, ecx
00444984  c1e502                   shl ebp, 2
00444987  01cd                     add ebp, ecx
00444989  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044498e  c1e502                   shl ebp, 2
00444991  8a8428dc000000           mov al, byte ptr [eax + ebp + 0xdc]
00444998  ba02000000               mov edx, 2
0044499d  25ff000000               and eax, 0xff
004449a2  e8f0330200               call 0x467d97
004449a7  84c0                     test al, al
004449a9  0f8598020000             jne 0x444c47
004449af  ba44000000               mov edx, 0x44
004449b4  89c8                     mov eax, ecx
004449b6  31db                     xor ebx, ebx
004449b8  e80be00300               call 0x4829c8
004449bd  8d8604010000             lea eax, [esi + 0x104]
004449c3  e8f8600400               call 0x48aac0
004449c8  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
004449ce  31d2                     xor edx, edx
004449d0  01eb                     add ebx, ebp
004449d2  31c0                     xor eax, eax
004449d4  8a1541805000             mov dl, byte ptr [0x508041]
004449da  668b4308                 mov ax, word ptr [ebx + 8]
004449de  e80d1d0300               call 0x4766f0
004449e3  84c0                     test al, al
004449e5  7439                     je 0x444a20
004449e7  89c8                     mov eax, ecx
004449e9  e86fc2ffff               call 0x440c5d
004449ee  8b9304010000             mov edx, dword ptr [ebx + 0x104]
004449f4  c683f900000000           mov byte ptr [ebx + 0xf9], 0
004449fb  83faff                   cmp edx, -1
004449fe  7520                     jne 0x444a20
00444a00  50                       push eax
00444a01  31d2                     xor edx, edx
00444a03  31c9                     xor ecx, ecx
00444a05  8a5301                   mov dl, byte ptr [ebx + 1]
00444a08  8d8304010000             lea eax, [ebx + 0x104]
00444a0e  c1e210                   shl edx, 0x10
00444a11  89c3                     mov ebx, eax
00444a13  b850000000               mov eax, 0x50
00444a18  80ce05                   or dh, 5
00444a1b  e859600400               call 0x48aa79
00444a20  31d2                     xor edx, edx
00444a22  6689fa                   mov dx, di
00444a25  89d0                     mov eax, edx
00444a27  c1e004                   shl eax, 4
00444a2a  01d0                     add eax, edx
00444a2c  c1e002                   shl eax, 2
00444a2f  01d0                     add eax, edx
00444a31  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444a37  b104                     mov cl, 4
00444a39  89fb                     mov ebx, edi
00444a3b  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00444a3f  25ff000000               and eax, 0xff
00444a44  7409                     je 0x444a4f
00444a46  83f804                   cmp eax, 4
00444a49  7404                     je 0x444a4f
00444a4b  b001                     mov al, 1
00444a4d  eb02                     jmp 0x444a51
00444a4f  30c0                     xor al, al
00444a51  84c0                     test al, al
00444a53  7448                     je 0x444a9d
00444a55  31d2                     xor edx, edx
00444a57  6689da                   mov dx, bx
00444a5a  89d0                     mov eax, edx
00444a5c  c1e004                   shl eax, 4
00444a5f  01d0                     add eax, edx
00444a61  c1e002                   shl eax, 2
00444a64  01c2                     add edx, eax
00444a66  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444a6b  c1e202                   shl edx, 2
00444a6e  884c0202                 mov byte ptr [edx + eax + 2], cl
00444a72  663b1d04634900           cmp bx, word ptr [0x496304]
00444a79  7522                     jne 0x444a9d
00444a7b  30e4                     xor ah, ah
00444a7d  31db                     xor ebx, ebx
00444a7f  8825360f4e00             mov byte ptr [0x4e0f36], ah
00444a85  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00444a8b  bbffff0000               mov ebx, 0xffff
00444a90  8825370f4e00             mov byte ptr [0x4e0f37], ah
00444a96  66891d04634900           mov word ptr [0x496304], bx
00444a9d  31d2                     xor edx, edx
00444a9f  6689fa                   mov dx, di
00444aa2  89d0                     mov eax, edx
00444aa4  c1e004                   shl eax, 4
00444aa7  01d0                     add eax, edx
00444aa9  c1e002                   shl eax, 2
00444aac  01d0                     add eax, edx
00444aae  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444ab4  c1e002                   shl eax, 2
00444ab7  01d0                     add eax, edx
00444ab9  89f9                     mov ecx, edi
00444abb  8d580a                   lea ebx, [eax + 0xa]
00444abe  668b03                   mov ax, word ptr [ebx]
00444ac1  25ffff0000               and eax, 0xffff
00444ac6  740e                     je 0x444ad6
00444ac8  31c0                     xor eax, eax
00444aca  31d2                     xor edx, edx
00444acc  6689c8                   mov ax, cx
00444acf  e828f3ffff               call 0x443dfc
00444ad4  ebe8                     jmp 0x444abe
00444ad6  31d2                     xor edx, edx
00444ad8  6689fa                   mov dx, di
00444adb  89d0                     mov eax, edx
00444add  c1e004                   shl eax, 4
00444ae0  01d0                     add eax, edx
00444ae2  c1e002                   shl eax, 2
00444ae5  01d0                     add eax, edx
00444ae7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00444aed  b104                     mov cl, 4
00444aef  89fb                     mov ebx, edi
00444af1  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00444af5  25ff000000               and eax, 0xff
00444afa  7409                     je 0x444b05
00444afc  83f804                   cmp eax, 4
00444aff  7404                     je 0x444b05
00444b01  b001                     mov al, 1
00444b03  eb02                     jmp 0x444b07
00444b05  30c0                     xor al, al
00444b07  84c0                     test al, al
00444b09  744d                     je 0x444b58
00444b0b  31d2                     xor edx, edx
00444b0d  6689da                   mov dx, bx
00444b10  89d0                     mov eax, edx
00444b12  c1e004                   shl eax, 4
00444b15  01d0                     add eax, edx
00444b17  c1e002                   shl eax, 2
00444b1a  01c2                     add edx, eax
00444b1c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444b21  c1e202                   shl edx, 2
00444b24  884c0202                 mov byte ptr [edx + eax + 2], cl
00444b28  668b1504634900           mov dx, word ptr [0x496304]
00444b2f  6639d3                   cmp bx, dx
00444b32  7524                     jne 0x444b58
00444b34  30f7                     xor bh, dh
00444b36  30c9                     xor cl, cl
00444b38  31ed                     xor ebp, ebp
00444b3a  883d360f4e00             mov byte ptr [0x4e0f36], bh
00444b40  880d370f4e00             mov byte ptr [0x4e0f37], cl
00444b46  bbffff0000               mov ebx, 0xffff
00444b4b  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
00444b51  66891d04634900           mov word ptr [0x496304], bx
00444b58  31db                     xor ebx, ebx
00444b5a  c686a400000000           mov byte ptr [esi + 0xa4], 0
00444b61  6689fb                   mov bx, di
00444b64  66c786c20000000000       mov word ptr [esi + 0xc2], 0
00444b6d  89d8                     mov eax, ebx
00444b6f  31d2                     xor edx, edx
00444b71  e8d2da0200               call 0x472648
00444b76  89d8                     mov eax, ebx
00444b78  668b5608                 mov dx, word ptr [esi + 8]
00444b7c  e82be3ffff               call 0x442eac
00444b81  668b4608                 mov ax, word ptr [esi + 8]
00444b85  668b4e7c                 mov cx, word ptr [esi + 0x7c]
00444b89  6639c8                   cmp ax, cx
00444b8c  740c                     je 0x444b9a
00444b8e  31d2                     xor edx, edx
00444b90  89d8                     mov eax, ebx
00444b92  6689ca                   mov dx, cx
00444b95  e812e3ffff               call 0x442eac
00444b9a  31d2                     xor edx, edx
00444b9c  6689fa                   mov dx, di
00444b9f  89d0                     mov eax, edx
00444ba1  c1e004                   shl eax, 4
00444ba4  01d0                     add eax, edx
00444ba6  c1e002                   shl eax, 2
00444ba9  01c2                     add edx, eax
00444bab  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444bb0  c1e202                   shl edx, 2
00444bb3  8a440201                 mov al, byte ptr [edx + eax + 1]
00444bb7  2c0b                     sub al, 0xb
00444bb9  3c06                     cmp al, 6
00444bbb  7711                     ja 0x444bce
00444bbd  25ff000000               and eax, 0xff
00444bc2  2eff24851c494400         jmp dword ptr cs:[eax*4 + 0x44491c]
00444bca  b001                     mov al, 1
00444bcc  eb02                     jmp 0x444bd0
00444bce  30c0                     xor al, al
00444bd0  84c0                     test al, al
00444bd2  0f84c5a60000             je 0x44f29d
00444bd8  31c0                     xor eax, eax
00444bda  8a4601                   mov al, byte ptr [esi + 1]
00444bdd  83f810                   cmp eax, 0x10
00444be0  743d                     je 0x444c1f
00444be2  b841000000               mov eax, 0x41
00444be7  e8f0b80200               call 0x4704dc
00444bec  a801                     test al, 1
00444bee  751e                     jne 0x444c0e
00444bf0  6a00                     push 0
00444bf2  6ae0                     push -0x20
00444bf4  6ae0                     push -0x20
00444bf6  31d2                     xor edx, edx
00444bf8  6a00                     push 0
00444bfa  b812000000               mov eax, 0x12
00444bff  668b5608                 mov dx, word ptr [esi + 8]
00444c03  6a00                     push 0
00444c05  31c9                     xor ecx, ecx
00444c07  89d3                     mov ebx, edx
00444c09  e995010000               jmp 0x444da3
00444c0e  6a00                     push 0
00444c10  6ae0                     push -0x20
00444c12  6ae0                     push -0x20
00444c14  31d2                     xor edx, edx
00444c16  6a00                     push 0
00444c18  b813000000               mov eax, 0x13
00444c1d  ebe0                     jmp 0x444bff
00444c1f  31c0                     xor eax, eax
00444c21  8a86ab000000             mov al, byte ptr [esi + 0xab]
00444c27  f7d8                     neg eax
00444c29  6a00                     push 0
00444c2b  98                       cwde
00444c2c  50                       push eax
00444c2d  6a00                     push 0
00444c2f  31d2                     xor edx, edx
00444c31  6a00                     push 0
00444c33  31c9                     xor ecx, ecx
00444c35  668b5608                 mov dx, word ptr [esi + 8]
00444c39  6a00                     push 0
00444c3b  89d3                     mov ebx, edx
00444c3d  b822000000               mov eax, 0x22
00444c42  e95c010000               jmp 0x444da3
00444c47  31db                     xor ebx, ebx
00444c49  6689fb                   mov bx, di
00444c4c  89d9                     mov ecx, ebx
00444c4e  c1e104                   shl ecx, 4
00444c51  01d9                     add ecx, ebx
00444c53  c1e102                   shl ecx, 2
00444c56  01d9                     add ecx, ebx
00444c58  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444c5d  c1e102                   shl ecx, 2
00444c60  8a8401dc000000           mov al, byte ptr [ecx + eax + 0xdc]
00444c67  ba02000000               mov edx, 2
00444c6c  25ff000000               and eax, 0xff
00444c71  e821310200               call 0x467d97
00444c76  84c0                     test al, al
00444c78  0f841fa60000             je 0x44f29d
00444c7e  8d8604010000             lea eax, [esi + 0x104]
00444c84  e8375e0400               call 0x48aac0
00444c89  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444c8e  8a4c0172                 mov cl, byte ptr [ecx + eax + 0x72]
00444c92  89d8                     mov eax, ebx
00444c94  31d2                     xor edx, edx
00444c96  e8add90200               call 0x472648
00444c9b  89d8                     mov eax, ebx
00444c9d  668b5608                 mov dx, word ptr [esi + 8]
00444ca1  e806e2ffff               call 0x442eac
00444ca6  668b4608                 mov ax, word ptr [esi + 8]
00444caa  663b467c                 cmp ax, word ptr [esi + 0x7c]
00444cae  740d                     je 0x444cbd
00444cb0  31d2                     xor edx, edx
00444cb2  89d8                     mov eax, ebx
00444cb4  668b567c                 mov dx, word ptr [esi + 0x7c]
00444cb8  e8efe1ffff               call 0x442eac
00444cbd  31d2                     xor edx, edx
00444cbf  6689fa                   mov dx, di
00444cc2  89d0                     mov eax, edx
00444cc4  c1e004                   shl eax, 4
00444cc7  01d0                     add eax, edx
00444cc9  c1e002                   shl eax, 2
00444ccc  89fb                     mov ebx, edi
00444cce  01c2                     add edx, eax
00444cd0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444cd5  c1e202                   shl edx, 2
00444cd8  30ed                     xor ch, ch
00444cda  8a440202                 mov al, byte ptr [edx + eax + 2]
00444cde  25ff000000               and eax, 0xff
00444ce3  7409                     je 0x444cee
00444ce5  83f804                   cmp eax, 4
00444ce8  7404                     je 0x444cee
00444cea  b001                     mov al, 1
00444cec  eb02                     jmp 0x444cf0
00444cee  30c0                     xor al, al
00444cf0  84c0                     test al, al
00444cf2  7447                     je 0x444d3b
00444cf4  31d2                     xor edx, edx
00444cf6  6689da                   mov dx, bx
00444cf9  89d0                     mov eax, edx
00444cfb  c1e004                   shl eax, 4
00444cfe  01d0                     add eax, edx
00444d00  c1e002                   shl eax, 2
00444d03  01c2                     add edx, eax
00444d05  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00444d0a  c1e202                   shl edx, 2
00444d0d  886c0202                 mov byte ptr [edx + eax + 2], ch
00444d11  663b1d04634900           cmp bx, word ptr [0x496304]
00444d18  7521                     jne 0x444d3b
00444d1a  b8ffff0000               mov eax, 0xffff
00444d1f  30f6                     xor dh, dh
00444d21  31ff                     xor edi, edi
00444d23  8835360f4e00             mov byte ptr [0x4e0f36], dh
00444d29  8835370f4e00             mov byte ptr [0x4e0f37], dh
00444d2f  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
00444d35  66a304634900             mov word ptr [0x496304], ax
00444d3b  84c9                     test cl, cl
00444d3d  0f845aa50000             je 0x44f29d
00444d43  ba05000000               mov edx, 5
00444d48  31db                     xor ebx, ebx
00444d4a  31c0                     xor eax, eax
00444d4c  668b5e08                 mov bx, word ptr [esi + 8]
00444d50  8a06                     mov al, byte ptr [esi]
00444d52  e831560200               call 0x46a388
00444d57  31db                     xor ebx, ebx
00444d59  8a1e                     mov bl, byte ptr [esi]
00444d5b  81fbc8000000             cmp ebx, 0xc8
00444d61  7427                     je 0x444d8a
00444d63  83fb04                   cmp ebx, 4
00444d66  7422                     je 0x444d8a
00444d68  30f6                     xor dh, dh
00444d6a  30e4                     xor ah, ah
00444d6c  8a96bb000000             mov dl, byte ptr [esi + 0xbb]
00444d72  8a86f5000000             mov al, byte ptr [esi + 0xf5]
00444d78  01d0                     add eax, edx
00444d7a  31d2                     xor edx, edx
00444d7c  6689c2                   mov dx, ax
00444d7f  31c0                     xor eax, eax
00444d81  668b4608                 mov ax, word ptr [esi + 8]
00444d85  e8f8200300               call 0x476e82
00444d8a  6a00                     push 0
00444d8c  6a00                     push 0
00444d8e  6a00                     push 0
00444d90  31d2                     xor edx, edx
00444d92  6a00                     push 0
00444d94  b81f000000               mov eax, 0x1f
00444d99  668b5608                 mov dx, word ptr [esi + 8]
00444d9d  6a00                     push 0
00444d9f  31c9                     xor ecx, ecx
00444da1  89d3                     mov ebx, edx
00444da3  e8a4960200               call 0x46e44c
00444da8  e9f0a40000               jmp 0x44f29d
