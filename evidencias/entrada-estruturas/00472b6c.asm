; EnginSelectPeutEntrer; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00472b6c  51                       push ecx
00472b6d  56                       push esi
00472b6e  83ec18                   sub esp, 0x18
00472b71  880424                   mov byte ptr [esp], al
00472b74  88d5                     mov ch, dl
00472b76  89de                     mov esi, ebx
00472b78  88c1                     mov cl, al
00472b7a  31db                     xor ebx, ebx
00472b7c  eb01                     jmp 0x472b7f
00472b7e  43                       inc ebx
00472b7f  31d2                     xor edx, edx
00472b81  88ca                     mov dl, cl
00472b83  c1e209                   shl edx, 9
00472b86  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472b8d  732c                     jae 0x472bbb
00472b8f  31c0                     xor eax, eax
00472b91  6689d8                   mov ax, bx
00472b94  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472b9c  31d2                     xor edx, edx
00472b9e  6689c2                   mov dx, ax
00472ba1  89d0                     mov eax, edx
00472ba3  e80512fdff               call 0x443dad
00472ba8  84c0                     test al, al
00472baa  74d2                     je 0x472b7e
00472bac  89d0                     mov eax, edx
00472bae  e84bd4fdff               call 0x44fffe
00472bb3  84c0                     test al, al
00472bb5  74c7                     je 0x472b7e
00472bb7  b001                     mov al, 1
00472bb9  eb02                     jmp 0x472bbd
00472bbb  30c0                     xor al, al
00472bbd  84c0                     test al, al
00472bbf  0f84cd040000             je 0x473092
00472bc5  e9dc040000               jmp 0x4730a6
00472bca  31d2                     xor edx, edx
00472bcc  6689f2                   mov dx, si
00472bcf  89d0                     mov eax, edx
00472bd1  e81e79faff               call 0x41a4f4
00472bd6  88442408                 mov byte ptr [esp + 8], al
00472bda  89d0                     mov eax, edx
00472bdc  e8ab74faff               call 0x41a08c
00472be1  88442404                 mov byte ptr [esp + 4], al
00472be5  3a0424                   cmp al, byte ptr [esp]
00472be8  740c                     je 0x472bf6
00472bea  25ff000000               and eax, 0xff
00472bef  3dc8000000               cmp eax, 0xc8
00472bf4  7560                     jne 0x472c56
00472bf6  8a2c24                   mov ch, byte ptr [esp]
00472bf9  31d2                     xor edx, edx
00472bfb  30c9                     xor cl, cl
00472bfd  eb03                     jmp 0x472c02
00472bff  b101                     mov cl, 1
00472c01  42                       inc edx
00472c02  31db                     xor ebx, ebx
00472c04  88eb                     mov bl, ch
00472c06  c1e309                   shl ebx, 9
00472c09  663b9328875000           cmp dx, word ptr [ebx + 0x508728]
00472c10  7331                     jae 0x472c43
00472c12  31c0                     xor eax, eax
00472c14  6689d0                   mov ax, dx
00472c17  668b84432a875000         mov ax, word ptr [ebx + eax*2 + 0x50872a]
00472c1f  31db                     xor ebx, ebx
00472c21  6689c3                   mov bx, ax
00472c24  89d8                     mov eax, ebx
00472c26  e88211fdff               call 0x443dad
00472c2b  84c0                     test al, al
00472c2d  74d2                     je 0x472c01
00472c2f  69db14010000             imul ebx, ebx, 0x114
00472c35  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00472c3a  807c030109               cmp byte ptr [ebx + eax + 1], 9
00472c3f  74be                     je 0x472bff
00472c41  30c9                     xor cl, cl
00472c43  84c9                     test cl, cl
00472c45  740f                     je 0x472c56
00472c47  31c0                     xor eax, eax
00472c49  8a442408                 mov al, byte ptr [esp + 8]
00472c4d  83f809                   cmp eax, 9
00472c50  0f85c8020000             jne 0x472f1e
00472c56  8a442404                 mov al, byte ptr [esp + 4]
00472c5a  8a2c24                   mov ch, byte ptr [esp]
00472c5d  38e8                     cmp al, ch
00472c5f  0f85c0020000             jne 0x472f25
00472c65  31c0                     xor eax, eax
00472c67  8a442408                 mov al, byte ptr [esp + 8]
00472c6b  83f815                   cmp eax, 0x15
00472c6e  7555                     jne 0x472cc5
00472c70  88e9                     mov cl, ch
00472c72  31db                     xor ebx, ebx
00472c74  eb01                     jmp 0x472c77
00472c76  43                       inc ebx
00472c77  31d2                     xor edx, edx
00472c79  88ca                     mov dl, cl
00472c7b  c1e209                   shl edx, 9
00472c7e  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472c85  7334                     jae 0x472cbb
00472c87  31c0                     xor eax, eax
00472c89  6689d8                   mov ax, bx
00472c8c  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472c94  31d2                     xor edx, edx
00472c96  6689c2                   mov dx, ax
00472c99  89d0                     mov eax, edx
00472c9b  e80d11fdff               call 0x443dad
00472ca0  84c0                     test al, al
00472ca2  74d2                     je 0x472c76
00472ca4  89d0                     mov eax, edx
00472ca6  e87af3fcff               call 0x442025
00472cab  25ff000000               and eax, 0xff
00472cb0  e8fbf6fcff               call 0x4423b0
00472cb5  84c0                     test al, al
00472cb7  75bd                     jne 0x472c76
00472cb9  eb02                     jmp 0x472cbd
00472cbb  b001                     mov al, 1
00472cbd  84c0                     test al, al
00472cbf  0f8559020000             jne 0x472f1e
00472cc5  8a2c24                   mov ch, byte ptr [esp]
00472cc8  31db                     xor ebx, ebx
00472cca  30c9                     xor cl, cl
00472ccc  eb03                     jmp 0x472cd1
00472cce  b101                     mov cl, 1
00472cd0  43                       inc ebx
00472cd1  31d2                     xor edx, edx
00472cd3  88ea                     mov dl, ch
00472cd5  c1e209                   shl edx, 9
00472cd8  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472cdf  7334                     jae 0x472d15
00472ce1  31c0                     xor eax, eax
00472ce3  6689d8                   mov ax, bx
00472ce6  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472cee  31d2                     xor edx, edx
00472cf0  6689c2                   mov dx, ax
00472cf3  89d0                     mov eax, edx
00472cf5  e8b310fdff               call 0x443dad
00472cfa  84c0                     test al, al
00472cfc  74d2                     je 0x472cd0
00472cfe  89d0                     mov eax, edx
00472d00  e820f3fcff               call 0x442025
00472d05  25ff000000               and eax, 0xff
00472d0a  e838f6fcff               call 0x442347
00472d0f  84c0                     test al, al
00472d11  75bb                     jne 0x472cce
00472d13  30c9                     xor cl, cl
00472d15  84c9                     test cl, cl
00472d17  0f8472000000             je 0x472d8f
00472d1d  31c0                     xor eax, eax
00472d1f  8a442408                 mov al, byte ptr [esp + 8]
00472d23  83f802                   cmp eax, 2
00472d26  0f84f2010000             je 0x472f1e
00472d2c  83f813                   cmp eax, 0x13
00472d2f  755e                     jne 0x472d8f
00472d31  8a0424                   mov al, byte ptr [esp]
00472d34  31c9                     xor ecx, ecx
00472d36  31db                     xor ebx, ebx
00472d38  88442414                 mov byte ptr [esp + 0x14], al
00472d3c  eb01                     jmp 0x472d3f
00472d3e  43                       inc ebx
00472d3f  31d2                     xor edx, edx
00472d41  8a542414                 mov dl, byte ptr [esp + 0x14]
00472d45  c1e209                   shl edx, 9
00472d48  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472d4f  732b                     jae 0x472d7c
00472d51  31c0                     xor eax, eax
00472d53  6689d8                   mov ax, bx
00472d56  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472d5e  31d2                     xor edx, edx
00472d60  6689c2                   mov dx, ax
00472d63  89d0                     mov eax, edx
00472d65  e84310fdff               call 0x443dad
00472d6a  84c0                     test al, al
00472d6c  74d0                     je 0x472d3e
00472d6e  89d0                     mov eax, edx
00472d70  e831f3fcff               call 0x4420a6
00472d75  84c0                     test al, al
00472d77  74c5                     je 0x472d3e
00472d79  41                       inc ecx
00472d7a  ebc2                     jmp 0x472d3e
00472d7c  31c0                     xor eax, eax
00472d7e  6689c8                   mov ax, cx
00472d81  83f801                   cmp eax, 1
00472d84  0f9dc0                   setge al
00472d87  84c0                     test al, al
00472d89  0f858f010000             jne 0x472f1e
00472d8f  31c0                     xor eax, eax
00472d91  8a442408                 mov al, byte ptr [esp + 8]
00472d95  83f80e                   cmp eax, 0xe
00472d98  0f8514010000             jne 0x472eb2
00472d9e  8a2c24                   mov ch, byte ptr [esp]
00472da1  31db                     xor ebx, ebx
00472da3  30c9                     xor cl, cl
00472da5  eb03                     jmp 0x472daa
00472da7  b101                     mov cl, 1
00472da9  43                       inc ebx
00472daa  31d2                     xor edx, edx
00472dac  88ea                     mov dl, ch
00472dae  c1e209                   shl edx, 9
00472db1  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472db8  7334                     jae 0x472dee
00472dba  31c0                     xor eax, eax
00472dbc  6689d8                   mov ax, bx
00472dbf  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472dc7  31d2                     xor edx, edx
00472dc9  6689c2                   mov dx, ax
00472dcc  89d0                     mov eax, edx
00472dce  e8da0ffdff               call 0x443dad
00472dd3  84c0                     test al, al
00472dd5  74d2                     je 0x472da9
00472dd7  89d0                     mov eax, edx
00472dd9  e847f2fcff               call 0x442025
00472dde  25ff000000               and eax, 0xff
00472de3  e84cf6fcff               call 0x442434
00472de8  84c0                     test al, al
00472dea  75bb                     jne 0x472da7
00472dec  30c9                     xor cl, cl
00472dee  84c9                     test cl, cl
00472df0  0f84bc000000             je 0x472eb2
00472df6  8a0424                   mov al, byte ptr [esp]
00472df9  31c9                     xor ecx, ecx
00472dfb  31db                     xor ebx, ebx
00472dfd  8844240c                 mov byte ptr [esp + 0xc], al
00472e01  eb01                     jmp 0x472e04
00472e03  43                       inc ebx
00472e04  31d2                     xor edx, edx
00472e06  8a54240c                 mov dl, byte ptr [esp + 0xc]
00472e0a  c1e209                   shl edx, 9
00472e0d  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472e14  732b                     jae 0x472e41
00472e16  31c0                     xor eax, eax
00472e18  6689d8                   mov ax, bx
00472e1b  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472e23  31d2                     xor edx, edx
00472e25  6689c2                   mov dx, ax
00472e28  89d0                     mov eax, edx
00472e2a  e87e0ffdff               call 0x443dad
00472e2f  84c0                     test al, al
00472e31  74d0                     je 0x472e03
00472e33  89d0                     mov eax, edx
00472e35  e86cf2fcff               call 0x4420a6
00472e3a  84c0                     test al, al
00472e3c  74c5                     je 0x472e03
00472e3e  41                       inc ecx
00472e3f  ebc2                     jmp 0x472e03
00472e41  31c0                     xor eax, eax
00472e43  6689c8                   mov ax, cx
00472e46  83f801                   cmp eax, 1
00472e49  0f9dc0                   setge al
00472e4c  84c0                     test al, al
00472e4e  0f85ca000000             jne 0x472f1e
00472e54  8a0424                   mov al, byte ptr [esp]
00472e57  31c9                     xor ecx, ecx
00472e59  31db                     xor ebx, ebx
00472e5b  88442410                 mov byte ptr [esp + 0x10], al
00472e5f  eb01                     jmp 0x472e62
00472e61  43                       inc ebx
00472e62  31d2                     xor edx, edx
00472e64  8a542410                 mov dl, byte ptr [esp + 0x10]
00472e68  c1e209                   shl edx, 9
00472e6b  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472e72  732b                     jae 0x472e9f
00472e74  31c0                     xor eax, eax
00472e76  6689d8                   mov ax, bx
00472e79  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472e81  31d2                     xor edx, edx
00472e83  6689c2                   mov dx, ax
00472e86  89d0                     mov eax, edx
00472e88  e8200ffdff               call 0x443dad
00472e8d  84c0                     test al, al
00472e8f  74d0                     je 0x472e61
00472e91  89d0                     mov eax, edx
00472e93  e88355fdff               call 0x44841b
00472e98  84c0                     test al, al
00472e9a  75c5                     jne 0x472e61
00472e9c  41                       inc ecx
00472e9d  ebc2                     jmp 0x472e61
00472e9f  31c0                     xor eax, eax
00472ea1  6689c8                   mov ax, cx
00472ea4  83f801                   cmp eax, 1
00472ea7  0f9dc0                   setge al
00472eaa  84c0                     test al, al
00472eac  0f856c000000             jne 0x472f1e
00472eb2  31c0                     xor eax, eax
00472eb4  8a442408                 mov al, byte ptr [esp + 8]
00472eb8  83f812                   cmp eax, 0x12
00472ebb  7552                     jne 0x472f0f
00472ebd  8a2c24                   mov ch, byte ptr [esp]
00472ec0  31d2                     xor edx, edx
00472ec2  30c9                     xor cl, cl
00472ec4  eb03                     jmp 0x472ec9
00472ec6  b101                     mov cl, 1
00472ec8  42                       inc edx
00472ec9  31db                     xor ebx, ebx
00472ecb  88eb                     mov bl, ch
00472ecd  c1e309                   shl ebx, 9
00472ed0  663b9328875000           cmp dx, word ptr [ebx + 0x508728]
00472ed7  7332                     jae 0x472f0b
00472ed9  31c0                     xor eax, eax
00472edb  6689d0                   mov ax, dx
00472ede  668b84432a875000         mov ax, word ptr [ebx + eax*2 + 0x50872a]
00472ee6  31db                     xor ebx, ebx
00472ee8  6689c3                   mov bx, ax
00472eeb  89d8                     mov eax, ebx
00472eed  e8bb0efdff               call 0x443dad
00472ef2  84c0                     test al, al
00472ef4  74d2                     je 0x472ec8
00472ef6  69c314010000             imul eax, ebx, 0x114
00472efc  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00472f02  807c030110               cmp byte ptr [ebx + eax + 1], 0x10
00472f07  74bd                     je 0x472ec6
00472f09  30c9                     xor cl, cl
00472f0b  84c9                     test cl, cl
00472f0d  750f                     jne 0x472f1e
00472f0f  31c0                     xor eax, eax
00472f11  8a442408                 mov al, byte ptr [esp + 8]
00472f15  83f808                   cmp eax, 8
00472f18  0f8588010000             jne 0x4730a6
00472f1e  b001                     mov al, 1
00472f20  e983010000               jmp 0x4730a8
00472f25  31c0                     xor eax, eax
00472f27  8a442408                 mov al, byte ptr [esp + 8]
00472f2b  83f810                   cmp eax, 0x10
00472f2e  0f8572010000             jne 0x4730a6
00472f34  30c9                     xor cl, cl
00472f36  31db                     xor ebx, ebx
00472f38  eb03                     jmp 0x472f3d
00472f3a  b101                     mov cl, 1
00472f3c  43                       inc ebx
00472f3d  31d2                     xor edx, edx
00472f3f  88ea                     mov dl, ch
00472f41  c1e209                   shl edx, 9
00472f44  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472f4b  7332                     jae 0x472f7f
00472f4d  31c0                     xor eax, eax
00472f4f  6689d8                   mov ax, bx
00472f52  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472f5a  31d2                     xor edx, edx
00472f5c  6689c2                   mov dx, ax
00472f5f  89d0                     mov eax, edx
00472f61  e8470efdff               call 0x443dad
00472f66  84c0                     test al, al
00472f68  74d2                     je 0x472f3c
00472f6a  69c214010000             imul eax, edx, 0x114
00472f70  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00472f76  807c02010a               cmp byte ptr [edx + eax + 1], 0xa
00472f7b  74bd                     je 0x472f3a
00472f7d  30c9                     xor cl, cl
00472f7f  84c9                     test cl, cl
00472f81  0f841f010000             je 0x4730a6
00472f87  eb95                     jmp 0x472f1e
00472f89  31d2                     xor edx, edx
00472f8b  6689f2                   mov dx, si
00472f8e  89d0                     mov eax, edx
00472f90  e890f0fcff               call 0x442025
00472f95  25ff000000               and eax, 0xff
00472f9a  83f810                   cmp eax, 0x10
00472f9d  0f8403010000             je 0x4730a6
00472fa3  89d0                     mov eax, edx
00472fa5  e87bf0fcff               call 0x442025
00472faa  25ff000000               and eax, 0xff
00472faf  e880f4fcff               call 0x442434
00472fb4  84c0                     test al, al
00472fb6  0f84ea000000             je 0x4730a6
00472fbc  8a2c24                   mov ch, byte ptr [esp]
00472fbf  31db                     xor ebx, ebx
00472fc1  30c9                     xor cl, cl
00472fc3  eb03                     jmp 0x472fc8
00472fc5  b101                     mov cl, 1
00472fc7  43                       inc ebx
00472fc8  31d2                     xor edx, edx
00472fca  88ea                     mov dl, ch
00472fcc  c1e209                   shl edx, 9
00472fcf  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00472fd6  7334                     jae 0x47300c
00472fd8  31c0                     xor eax, eax
00472fda  6689d8                   mov ax, bx
00472fdd  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00472fe5  31d2                     xor edx, edx
00472fe7  6689c2                   mov dx, ax
00472fea  89d0                     mov eax, edx
00472fec  e8bc0dfdff               call 0x443dad
00472ff1  84c0                     test al, al
00472ff3  74d2                     je 0x472fc7
00472ff5  89d0                     mov eax, edx
00472ff7  e829f0fcff               call 0x442025
00472ffc  25ff000000               and eax, 0xff
00473001  e841f3fcff               call 0x442347
00473006  84c0                     test al, al
00473008  75bb                     jne 0x472fc5
0047300a  30c9                     xor cl, cl
0047300c  84c9                     test cl, cl
0047300e  0f8492000000             je 0x4730a6
00473014  31d2                     xor edx, edx
00473016  6689f2                   mov dx, si
00473019  89d0                     mov eax, edx
0047301b  e805f0fcff               call 0x442025
00473020  25ff000000               and eax, 0xff
00473025  83f811                   cmp eax, 0x11
00473028  0f85f0feffff             jne 0x472f1e
0047302e  89d0                     mov eax, edx
00473030  e8f0effcff               call 0x442025
00473035  25ff000000               and eax, 0xff
0047303a  83f811                   cmp eax, 0x11
0047303d  7567                     jne 0x4730a6
0047303f  8a0c24                   mov cl, byte ptr [esp]
00473042  31db                     xor ebx, ebx
00473044  eb01                     jmp 0x473047
00473046  43                       inc ebx
00473047  31d2                     xor edx, edx
00473049  88ca                     mov dl, cl
0047304b  c1e209                   shl edx, 9
0047304e  663b9a28875000           cmp bx, word ptr [edx + 0x508728]
00473055  7332                     jae 0x473089
00473057  31c0                     xor eax, eax
00473059  6689d8                   mov ax, bx
0047305c  668b84422a875000         mov ax, word ptr [edx + eax*2 + 0x50872a]
00473064  31d2                     xor edx, edx
00473066  6689c2                   mov dx, ax
00473069  89d0                     mov eax, edx
0047306b  e83d0dfdff               call 0x443dad
00473070  84c0                     test al, al
00473072  74d2                     je 0x473046
00473074  89d0                     mov eax, edx
00473076  e8aaeffcff               call 0x442025
0047307b  25ff000000               and eax, 0xff
00473080  83f808                   cmp eax, 8
00473083  75c1                     jne 0x473046
00473085  b001                     mov al, 1
00473087  eb02                     jmp 0x47308b
00473089  30c0                     xor al, al
0047308b  84c0                     test al, al
0047308d  e986feffff               jmp 0x472f18
00473092  80fd01                   cmp ch, 1
00473095  720f                     jb 0x4730a6
00473097  0f86ecfeffff             jbe 0x472f89
0047309d  80fd03                   cmp ch, 3
004730a0  0f8424fbffff             je 0x472bca
004730a6  30c0                     xor al, al
004730a8  83c418                   add esp, 0x18
004730ab  5e                       pop esi
004730ac  59                       pop ecx
004730ad  c3                       ret
