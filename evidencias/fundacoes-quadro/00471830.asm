00471830  56                   push esi
00471831  57                   push edi
00471832  83ec18               sub esp, 0x18
00471835  48                   dec eax
00471836  663d0300             cmp ax, 3
0047183a  0f8709010000         ja 0x471949
00471840  25ffff0000           and eax, 0xffff
00471845  2eff248520184700     jmp dword ptr cs:[eax*4 + 0x471820]
0047184d  6823020000           push 0x223
00471852  b9e0010000           mov ecx, 0x1e0
00471857  bbe6010000           mov ebx, 0x1e6
0047185c  ba92010000           mov edx, 0x192
00471861  b801000000           mov eax, 1
00471866  e8e5830000           call 0x479c50
0047186b  682b020000           push 0x22b
00471870  b943020000           mov ecx, 0x243
00471875  bbd9010000           mov ebx, 0x1d9
0047187a  bafa010000           mov edx, 0x1fa
0047187f  b802000000           mov eax, 2
00471884  e8c7830000           call 0x479c50
00471889  6834020000           push 0x234
0047188e  b9b3020000           mov ecx, 0x2b3
00471893  bbd7010000           mov ebx, 0x1d7
00471898  ba6c020000           mov edx, 0x26c
0047189d  b803000000           mov eax, 3
004718a2  e8a9830000           call 0x479c50
004718a7  6821020000           push 0x221
004718ac  b908030000           mov ecx, 0x308
004718b1  bbd4010000           mov ebx, 0x1d4
004718b6  bad7020000           mov edx, 0x2d7
004718bb  b804000000           mov eax, 4
004718c0  e88b830000           call 0x479c50
004718c5  6878010000           push 0x178
004718ca  b94f010000           mov ecx, 0x14f
004718cf  bb5b010000           mov ebx, 0x15b
004718d4  ba21010000           mov edx, 0x121
004718d9  b805000000           mov eax, 5
004718de  e86d830000           call 0x479c50
004718e3  68f5000000           push 0xf5
004718e8  b921010000           mov ecx, 0x121
004718ed  bbdf000000           mov ebx, 0xdf
004718f2  ba0e010000           mov edx, 0x10e
004718f7  b806000000           mov eax, 6
004718fc  e84f830000           call 0x479c50
00471901  68f5000000           push 0xf5
00471906  b941010000           mov ecx, 0x141
0047190b  bbdf000000           mov ebx, 0xdf
00471910  ba2b010000           mov edx, 0x12b
00471915  b807000000           mov eax, 7
0047191a  e831830000           call 0x479c50
0047191f  6a57                 push 0x57
00471921  b97e000000           mov ecx, 0x7e
00471926  bb2d000000           mov ebx, 0x2d
0047192b  ba42000000           mov edx, 0x42
00471930  b808000000           mov eax, 8
00471935  e816830000           call 0x479c50
0047193a  ba08000000           mov edx, 8
0047193f  b801000000           mov eax, 1
00471944  e855830000           call 0x479c9e
00471949  83c418               add esp, 0x18
0047194c  5f                   pop edi
0047194d  5e                   pop esi
0047194e  c3                   ret 
0047194f  c744240c1e010000     mov dword ptr [esp + 0xc], 0x11e
00471957  e8117affff           call 0x46936d
0047195c  89c6                 mov esi, eax
0047195e  30e4                 xor ah, ah
00471960  88642414             mov byte ptr [esp + 0x14], ah
00471964  eb47                 jmp 0x4719ad
00471966  8b44240c             mov eax, dword ptr [esp + 0xc]
0047196a  0514000000           add eax, 0x14
0047196f  25ffff0000           and eax, 0xffff
00471974  31c9                 xor ecx, ecx
00471976  31db                 xor ebx, ebx
00471978  50                   push eax
00471979  30e4                 xor ah, ah
0047197b  668b5c2410           mov bx, word ptr [esp + 0x10]
00471980  8a442418             mov al, byte ptr [esp + 0x18]
00471984  668b0d18a04900       mov cx, word ptr [0x49a018]
0047198b  40                   inc eax
0047198c  25ffff0000           and eax, 0xffff
00471991  31d2                 xor edx, edx
00471993  e8b8820000           call 0x479c50
00471998  8b7c240c             mov edi, dword ptr [esp + 0xc]
0047199c  8a7c2414             mov bh, byte ptr [esp + 0x14]
004719a0  83c719               add edi, 0x19
004719a3  fec7                 inc bh
004719a5  897c240c             mov dword ptr [esp + 0xc], edi
004719a9  887c2414             mov byte ptr [esp + 0x14], bh
004719ad  31c0                 xor eax, eax
004719af  31d2                 xor edx, edx
004719b1  8a442414             mov al, byte ptr [esp + 0x14]
004719b5  6689f2               mov dx, si
004719b8  39d0                 cmp eax, edx
004719ba  7caa                 jl 0x471966
004719bc  eb81                 jmp 0x47193f
004719be  6823020000           push 0x223
004719c3  b9e0010000           mov ecx, 0x1e0
004719c8  bbe6010000           mov ebx, 0x1e6
004719cd  ba92010000           mov edx, 0x192
004719d2  b801000000           mov eax, 1
004719d7  e874820000           call 0x479c50
004719dc  682b020000           push 0x22b
004719e1  b943020000           mov ecx, 0x243
004719e6  bbd9010000           mov ebx, 0x1d9
004719eb  bafa010000           mov edx, 0x1fa
004719f0  b802000000           mov eax, 2
004719f5  e856820000           call 0x479c50
004719fa  6834020000           push 0x234
004719ff  b9b3020000           mov ecx, 0x2b3
00471a04  bbd7010000           mov ebx, 0x1d7
00471a09  ba6c020000           mov edx, 0x26c
00471a0e  b803000000           mov eax, 3
00471a13  e838820000           call 0x479c50
00471a18  e8fda6ffff           call 0x46c11a
00471a1d  25ffff0000           and eax, 0xffff
00471a22  83f807               cmp eax, 7
00471a25  7c1b                 jl 0x471a42
00471a27  6821020000           push 0x221
00471a2c  b908030000           mov ecx, 0x308
00471a31  bbd4010000           mov ebx, 0x1d4
00471a36  bad7020000           mov edx, 0x2d7
00471a3b  b804000000           mov eax, 4
00471a40  eb0d                 jmp 0x471a4f
00471a42  6a01                 push 1
00471a44  b804000000           mov eax, 4
00471a49  31c9                 xor ecx, ecx
00471a4b  31db                 xor ebx, ebx
00471a4d  31d2                 xor edx, edx
00471a4f  e8fc810000           call 0x479c50
00471a54  681c020000           push 0x21c
00471a59  b94e010000           mov ecx, 0x14e
00471a5e  bb00020000           mov ebx, 0x200
00471a63  ba22010000           mov edx, 0x122
00471a68  b805000000           mov eax, 5
00471a6d  e8de810000           call 0x479c50
00471a72  68b6000000           push 0xb6
00471a77  b921010000           mov ecx, 0x121
00471a7c  bba2000000           mov ebx, 0xa2
00471a81  ba0e010000           mov edx, 0x10e
00471a86  b806000000           mov eax, 6
00471a8b  e8c0810000           call 0x479c50
00471a90  68b6000000           push 0xb6
00471a95  b941010000           mov ecx, 0x141
00471a9a  bba2000000           mov ebx, 0xa2
00471a9f  e96cfeffff           jmp 0x471910
00471aa4  6a01                 push 1
00471aa6  b901000000           mov ecx, 1
00471aab  31db                 xor ebx, ebx
00471aad  31d2                 xor edx, edx
00471aaf  89c8                 mov eax, ecx
00471ab1  e89a810000           call 0x479c50
00471ab6  6a01                 push 1
00471ab8  ba02000000           mov edx, 2
00471abd  66a118a04900         mov ax, word ptr [0x49a018]
00471ac3  31c9                 xor ecx, ecx
00471ac5  83e803               sub eax, 3
00471ac8  31db                 xor ebx, ebx
00471aca  6689c1               mov cx, ax
00471acd  89d0                 mov eax, edx
00471acf  e87c810000           call 0x479c50
00471ad4  66a118a04900         mov ax, word ptr [0x49a018]
00471ada  31c9                 xor ecx, ecx
00471adc  48                   dec eax
00471add  6a01                 push 1
00471adf  6689c1               mov cx, ax
00471ae2  66a118a04900         mov ax, word ptr [0x49a018]
00471ae8  31d2                 xor edx, edx
00471aea  83e802               sub eax, 2
00471aed  31db                 xor ebx, ebx
00471aef  6689c2               mov dx, ax
00471af2  b803000000           mov eax, 3
00471af7  e854810000           call 0x479c50
00471afc  66a11aa04900         mov ax, word ptr [0x49a01a]
00471b02  83e803               sub eax, 3
00471b05  25ffff0000           and eax, 0xffff
00471b0a  50                   push eax
00471b0b  66a118a04900         mov ax, word ptr [0x49a018]
00471b11  31c9                 xor ecx, ecx
00471b13  48                   dec eax
00471b14  6689c1               mov cx, ax
00471b17  66a118a04900         mov ax, word ptr [0x49a018]
00471b1d  31d2                 xor edx, edx
00471b1f  83e802               sub eax, 2
00471b22  bb02000000           mov ebx, 2
00471b27  6689c2               mov dx, ax
00471b2a  b804000000           mov eax, 4
00471b2f  e81c810000           call 0x479c50
00471b34  66a11aa04900         mov ax, word ptr [0x49a01a]
00471b3a  48                   dec eax
00471b3b  25ffff0000           and eax, 0xffff
00471b40  50                   push eax
00471b41  66a118a04900         mov ax, word ptr [0x49a018]
00471b47  31c9                 xor ecx, ecx
00471b49  48                   dec eax
00471b4a  6689c1               mov cx, ax
00471b4d  66a11aa04900         mov ax, word ptr [0x49a01a]
00471b53  31db                 xor ebx, ebx
00471b55  83e802               sub eax, 2
00471b58  6689c3               mov bx, ax
00471b5b  66a118a04900         mov ax, word ptr [0x49a018]
00471b61  31d2                 xor edx, edx
00471b63  83e802               sub eax, 2
00471b66  6689c2               mov dx, ax
00471b69  b805000000           mov eax, 5
00471b6e  e8dd800000           call 0x479c50
00471b73  66a11aa04900         mov ax, word ptr [0x49a01a]
00471b79  48                   dec eax
00471b7a  25ffff0000           and eax, 0xffff
00471b7f  50                   push eax
00471b80  66a118a04900         mov ax, word ptr [0x49a018]
00471b86  31c9                 xor ecx, ecx
00471b88  83e803               sub eax, 3
00471b8b  6689c1               mov cx, ax
00471b8e  66a11aa04900         mov ax, word ptr [0x49a01a]
00471b94  31db                 xor ebx, ebx
00471b96  83e802               sub eax, 2
00471b99  ba02000000           mov edx, 2
00471b9e  6689c3               mov bx, ax
00471ba1  b806000000           mov eax, 6
00471ba6  e8a5800000           call 0x479c50
00471bab  66a11aa04900         mov ax, word ptr [0x49a01a]
00471bb1  48                   dec eax
00471bb2  25ffff0000           and eax, 0xffff
00471bb7  b901000000           mov ecx, 1
00471bbc  50                   push eax
00471bbd  66a11aa04900         mov ax, word ptr [0x49a01a]
00471bc3  31db                 xor ebx, ebx
00471bc5  83e802               sub eax, 2
00471bc8  31d2                 xor edx, edx
00471bca  6689c3               mov bx, ax
00471bcd  b807000000           mov eax, 7
00471bd2  e879800000           call 0x479c50
00471bd7  66a11aa04900         mov ax, word ptr [0x49a01a]
00471bdd  83e803               sub eax, 3
00471be0  b902000000           mov ecx, 2
00471be5  25ffff0000           and eax, 0xffff
00471bea  31d2                 xor edx, edx
00471bec  50                   push eax
00471bed  89cb                 mov ebx, ecx
00471bef  b808000000           mov eax, 8
00471bf4  e857800000           call 0x479c50
00471bf9  6a00                 push 0
00471bfb  b809000000           mov eax, 9
00471c00  31c9                 xor ecx, ecx
00471c02  31db                 xor ebx, ebx
00471c04  31d2                 xor edx, edx
00471c06  e845800000           call 0x479c50
00471c0b  31c0                 xor eax, eax
00471c0d  66a118a04900         mov ax, word ptr [0x49a018]
00471c13  3d80020000           cmp eax, 0x280
00471c18  0f8556010000         jne 0x471d74
00471c1e  803d8572490000       cmp byte ptr [0x497285], 0
00471c25  7449                 je 0x471c70
00471c27  8d54240c             lea edx, [esp + 0xc]
00471c2b  8d442408             lea eax, [esp + 8]
00471c2f  e8c485ffff           call 0x46a1f8
00471c34  89e2                 mov edx, esp
00471c36  8d442404             lea eax, [esp + 4]
00471c3a  e8cf85ffff           call 0x46a20e
00471c3f  8b44240c             mov eax, dword ptr [esp + 0xc]
00471c43  030424               add eax, dword ptr [esp]
00471c46  8b5c2404             mov ebx, dword ptr [esp + 4]
00471c4a  25ffff0000           and eax, 0xffff
00471c4f  31c9                 xor ecx, ecx
00471c51  31d2                 xor edx, edx
00471c53  50                   push eax
00471c54  8b44240c             mov eax, dword ptr [esp + 0xc]
00471c58  668b54240c           mov dx, word ptr [esp + 0xc]
00471c5d  01d8                 add eax, ebx
00471c5f  31db                 xor ebx, ebx
00471c61  6689c1               mov cx, ax
00471c64  668b5c2410           mov bx, word ptr [esp + 0x10]
00471c69  b80a000000           mov eax, 0xa
00471c6e  eb10                 jmp 0x471c80
00471c70  6a01                 push 1
00471c72  b901000000           mov ecx, 1
00471c77  b80a000000           mov eax, 0xa
00471c7c  31db                 xor ebx, ebx
00471c7e  31d2                 xor edx, edx
00471c80  e8cb7f0000           call 0x479c50
00471c85  31c0                 xor eax, eax
00471c87  a041805000           mov al, byte ptr [0x508041]
00471c8c  e8873bffff           call 0x465818
00471c91  25ff000000           and eax, 0xff
00471c96  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471c9c  25ff000000           and eax, 0xff
00471ca1  83f801               cmp eax, 1
00471ca4  7421                 je 0x471cc7
00471ca6  31c0                 xor eax, eax
00471ca8  a041805000           mov al, byte ptr [0x508041]
00471cad  e8663bffff           call 0x465818
00471cb2  25ff000000           and eax, 0xff
00471cb7  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471cbd  25ff000000           and eax, 0xff
00471cc2  83f802               cmp eax, 2
00471cc5  752b                 jne 0x471cf2
00471cc7  66a126875000         mov ax, word ptr [0x508726]
00471ccd  c1e005               shl eax, 5
00471cd0  48                   dec eax
00471cd1  25ffff0000           and eax, 0xffff
00471cd6  50                   push eax
00471cd7  66a126875000         mov ax, word ptr [0x508726]
00471cdd  b94c000000           mov ecx, 0x4c
00471ce2  48                   dec eax
00471ce3  31db                 xor ebx, ebx
00471ce5  c1e005               shl eax, 5
00471ce8  ba2d000000           mov edx, 0x2d
00471ced  6689c3               mov bx, ax
00471cf0  eb63                 jmp 0x471d55
00471cf2  31c0                 xor eax, eax
00471cf4  a041805000           mov al, byte ptr [0x508041]
00471cf9  e81a3bffff           call 0x465818
00471cfe  25ff000000           and eax, 0xff
00471d03  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471d09  25ff000000           and eax, 0xff
00471d0e  83f803               cmp eax, 3
00471d11  754c                 jne 0x471d5f
00471d13  8d54240c             lea edx, [esp + 0xc]
00471d17  8d442408             lea eax, [esp + 8]
00471d1b  e8bc03ffff           call 0x4620dc
00471d20  89e2                 mov edx, esp
00471d22  8d442404             lea eax, [esp + 4]
00471d26  e8c703ffff           call 0x4620f2
00471d2b  8b44240c             mov eax, dword ptr [esp + 0xc]
00471d2f  030424               add eax, dword ptr [esp]
00471d32  8b742404             mov esi, dword ptr [esp + 4]
00471d36  25ffff0000           and eax, 0xffff
00471d3b  31c9                 xor ecx, ecx
00471d3d  31db                 xor ebx, ebx
00471d3f  31d2                 xor edx, edx
00471d41  50                   push eax
00471d42  8b44240c             mov eax, dword ptr [esp + 0xc]
00471d46  668b5c2410           mov bx, word ptr [esp + 0x10]
00471d4b  01f0                 add eax, esi
00471d4d  668b54240c           mov dx, word ptr [esp + 0xc]
00471d52  6689c1               mov cx, ax
00471d55  b81a000000           mov eax, 0x1a
00471d5a  e978010000           jmp 0x471ed7
00471d5f  6a01                 push 1
00471d61  b901000000           mov ecx, 1
00471d66  b81a000000           mov eax, 0x1a
00471d6b  31db                 xor ebx, ebx
00471d6d  31d2                 xor edx, edx
00471d6f  e963010000           jmp 0x471ed7
00471d74  803d8572490000       cmp byte ptr [0x497285], 0
00471d7b  7449                 je 0x471dc6
00471d7d  8d54240c             lea edx, [esp + 0xc]
00471d81  8d442408             lea eax, [esp + 8]
00471d85  e86e84ffff           call 0x46a1f8
00471d8a  89e2                 mov edx, esp
00471d8c  8d442404             lea eax, [esp + 4]
00471d90  e87984ffff           call 0x46a20e
00471d95  8b44240c             mov eax, dword ptr [esp + 0xc]
00471d99  030424               add eax, dword ptr [esp]
00471d9c  8b4c2404             mov ecx, dword ptr [esp + 4]
00471da0  25ffff0000           and eax, 0xffff
00471da5  31db                 xor ebx, ebx
00471da7  31d2                 xor edx, edx
00471da9  50                   push eax
00471daa  8b44240c             mov eax, dword ptr [esp + 0xc]
00471dae  668b5c2410           mov bx, word ptr [esp + 0x10]
00471db3  01c8                 add eax, ecx
00471db5  31c9                 xor ecx, ecx
00471db7  668b54240c           mov dx, word ptr [esp + 0xc]
00471dbc  6689c1               mov cx, ax
00471dbf  b80a000000           mov eax, 0xa
00471dc4  eb10                 jmp 0x471dd6
00471dc6  6a01                 push 1
00471dc8  b901000000           mov ecx, 1
00471dcd  b80a000000           mov eax, 0xa
00471dd2  31db                 xor ebx, ebx
00471dd4  31d2                 xor edx, edx
00471dd6  e8757e0000           call 0x479c50
00471ddb  31c0                 xor eax, eax
00471ddd  a041805000           mov al, byte ptr [0x508041]
00471de2  e8313affff           call 0x465818
00471de7  25ff000000           and eax, 0xff
00471dec  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471df2  25ff000000           and eax, 0xff
00471df7  83f801               cmp eax, 1
00471dfa  7421                 je 0x471e1d
00471dfc  31c0                 xor eax, eax
00471dfe  a041805000           mov al, byte ptr [0x508041]
00471e03  e8103affff           call 0x465818
00471e08  25ff000000           and eax, 0xff
00471e0d  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471e13  25ff000000           and eax, 0xff
00471e18  83f802               cmp eax, 2
00471e1b  754a                 jne 0x471e67
00471e1d  668b1526875000       mov dx, word ptr [0x508726]
00471e24  660fbe05908f5000     movsx ax, byte ptr [0x508f90]
00471e2c  c1e205               shl edx, 5
00471e2f  c1e005               shl eax, 5
00471e32  4a                   dec edx
00471e33  29c2                 sub edx, eax
00471e35  81e2ffff0000         and edx, 0xffff
00471e3b  52                   push edx
00471e3c  89c2                 mov edx, eax
00471e3e  31c9                 xor ecx, ecx
00471e40  83c24c               add edx, 0x4c
00471e43  6689d1               mov cx, dx
00471e46  668b1526875000       mov dx, word ptr [0x508726]
00471e4d  4a                   dec edx
00471e4e  c1e205               shl edx, 5
00471e51  31db                 xor ebx, ebx
00471e53  29c2                 sub edx, eax
00471e55  6689d3               mov bx, dx
00471e58  052d000000           add eax, 0x2d
00471e5d  31d2                 xor edx, edx
00471e5f  6689c2               mov dx, ax
00471e62  e9eefeffff           jmp 0x471d55
00471e67  31c0                 xor eax, eax
00471e69  a041805000           mov al, byte ptr [0x508041]
00471e6e  e8a539ffff           call 0x465818
00471e73  25ff000000           and eax, 0xff
00471e78  8a807c2e4e00         mov al, byte ptr [eax + 0x4e2e7c]
00471e7e  25ff000000           and eax, 0xff
00471e83  83f803               cmp eax, 3
00471e86  753f                 jne 0x471ec7
00471e88  8d54240c             lea edx, [esp + 0xc]
00471e8c  8d442408             lea eax, [esp + 8]
00471e90  e84702ffff           call 0x4620dc
00471e95  89e2                 mov edx, esp
00471e97  8d442404             lea eax, [esp + 4]
00471e9b  e85202ffff           call 0x4620f2
00471ea0  8b44240c             mov eax, dword ptr [esp + 0xc]
00471ea4  030424               add eax, dword ptr [esp]
00471ea7  8b7c2404             mov edi, dword ptr [esp + 4]
00471eab  25ffff0000           and eax, 0xffff
00471eb0  31c9                 xor ecx, ecx
00471eb2  31db                 xor ebx, ebx
00471eb4  31d2                 xor edx, edx
00471eb6  50                   push eax
00471eb7  8b44240c             mov eax, dword ptr [esp + 0xc]
00471ebb  668b5c2410           mov bx, word ptr [esp + 0x10]
00471ec0  01f8                 add eax, edi
00471ec2  e986feffff           jmp 0x471d4d
00471ec7  6a01                 push 1
00471ec9  b901000000           mov ecx, 1
00471ece  b81a000000           mov eax, 0x1a
00471ed3  31db                 xor ebx, ebx
00471ed5  31d2                 xor edx, edx
00471ed7  e8747d0000           call 0x479c50
00471edc  e8527dffff           call 0x469c33
00471ee1  84c0                 test al, al
00471ee3  744b                 je 0x471f30
00471ee5  660fbe05908f5000     movsx ax, byte ptr [0x508f90]
00471eed  668b1526875000       mov dx, word ptr [0x508726]
00471ef4  29c2                 sub edx, eax
00471ef6  c1e205               shl edx, 5
00471ef9  81e2ffff0000         and edx, 0xffff
00471eff  52                   push edx
00471f00  89c2                 mov edx, eax
00471f02  c1e205               shl edx, 5
00471f05  89d3                 mov ebx, edx
00471f07  31c9                 xor ecx, ecx
00471f09  83c32d               add ebx, 0x2d
00471f0c  6689d9               mov cx, bx
00471f0f  668b1d26875000       mov bx, word ptr [0x508726]
00471f16  4b                   dec ebx
00471f17  29c3                 sub ebx, eax
00471f19  89d8                 mov eax, ebx
00471f1b  c1e005               shl eax, 5
00471f1e  31db                 xor ebx, ebx
00471f20  6689c3               mov bx, ax
00471f23  b81b000000           mov eax, 0x1b
00471f28  81e2ffff0000         and edx, 0xffff
00471f2e  eb10                 jmp 0x471f40
00471f30  6a01                 push 1
00471f32  b901000000           mov ecx, 1
00471f37  b81b000000           mov eax, 0x1b
00471f3c  31db                 xor ebx, ebx
00471f3e  31d2                 xor edx, edx
00471f40  e80b7d0000           call 0x479c50
00471f45  30db                 xor bl, bl
00471f47  885c2410             mov byte ptr [esp + 0x10], bl
00471f4b  eb04                 jmp 0x471f51
00471f4d  fe442410             inc byte ptr [esp + 0x10]
00471f51  31c0                 xor eax, eax
00471f53  8a442410             mov al, byte ptr [esp + 0x10]
00471f57  83f804               cmp eax, 4
00471f5a  0f8db1000000         jge 0x472011
00471f60  8a0d41805000         mov cl, byte ptr [0x508041]
00471f66  38c8                 cmp al, cl
00471f68  0f8486000000         je 0x471ff4
00471f6e  31db                 xor ebx, ebx
00471f70  88cb                 mov bl, cl
00471f72  89c2                 mov edx, eax
00471f74  89d8                 mov eax, ebx
00471f76  e8a3baffff           call 0x46da1e
00471f7b  84c0                 test al, al
00471f7d  7475                 je 0x471ff4
00471f7f  668b1526875000       mov dx, word ptr [0x508726]
00471f86  660fbe05908f5000     movsx ax, byte ptr [0x508f90]
00471f8e  c1e205               shl edx, 5
00471f91  c1e005               shl eax, 5
00471f94  4a                   dec edx
00471f95  29c2                 sub edx, eax
00471f97  30ff                 xor bh, bh
00471f99  8a5c2410             mov bl, byte ptr [esp + 0x10]
00471f9d  6bcb14               imul ecx, ebx, 0x14
00471fa0  81e2ffff0000         and edx, 0xffff
00471fa6  52                   push edx
00471fa7  668b1524875000       mov dx, word ptr [0x508724]
00471fae  4a                   dec edx
00471faf  c1e205               shl edx, 5
00471fb2  83ea50               sub edx, 0x50
00471fb5  01ca                 add edx, ecx
00471fb7  29c2                 sub edx, eax
00471fb9  89d1                 mov ecx, edx
00471fbb  83c113               add ecx, 0x13
00471fbe  668b3526875000       mov si, word ptr [0x508726]
00471fc5  4e                   dec esi
00471fc6  c1e605               shl esi, 5
00471fc9  29c6                 sub esi, eax
00471fcb  81e1ffff0000         and ecx, 0xffff
00471fd1  89f0                 mov eax, esi
00471fd3  25ffff0000           and eax, 0xffff
00471fd8  83c31c               add ebx, 0x1c
00471fdb  31f6                 xor esi, esi
00471fdd  81e2ffff0000         and edx, 0xffff
00471fe3  6689de               mov si, bx
00471fe6  89c3                 mov ebx, eax
00471fe8  89f0                 mov eax, esi
00471fea  e8617c0000           call 0x479c50
00471fef  e959ffffff           jmp 0x471f4d
00471ff4  30e4                 xor ah, ah
00471ff6  8a442410             mov al, byte ptr [esp + 0x10]
00471ffa  6a01                 push 1
00471ffc  051c000000           add eax, 0x1c
00472001  b901000000           mov ecx, 1
00472006  25ffff0000           and eax, 0xffff
0047200b  31db                 xor ebx, ebx
0047200d  31d2                 xor edx, edx
0047200f  ebd9                 jmp 0x471fea
00472011  31c0                 xor eax, eax
00472013  31c9                 xor ecx, ecx
00472015  66a11aa04900         mov ax, word ptr [0x49a01a]
0047201b  31db                 xor ebx, ebx
0047201d  50                   push eax
0047201e  66a126875000         mov ax, word ptr [0x508726]
00472024  31d2                 xor edx, edx
00472026  c1e005               shl eax, 5
00472029  668b0d18a04900       mov cx, word ptr [0x49a018]
00472030  6689c3               mov bx, ax
00472033  b80b000000           mov eax, 0xb
00472038  e8137c0000           call 0x479c50
0047203d  ba1f000000           mov edx, 0x1f
00472042  e9f8f8ffff           jmp 0x47193f
