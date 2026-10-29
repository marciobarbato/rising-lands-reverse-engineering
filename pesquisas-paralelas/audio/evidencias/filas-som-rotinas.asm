; Intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Static request/queue inventory; no execution or reconstructed behavior claim.
; HandlSnd_GetAverageVolume
00489dac  53                       push ebx
00489dad  52                       push edx
00489dae  8b501c                   mov edx, dword ptr [eax + 0x1c]
00489db1  8a520d                   mov dl, byte ptr [edx + 0xd]
00489db4  81e2ff000000             and edx, 0xff
00489dba  7505                     jne 0x489dc1
00489dbc  ba00010000               mov edx, 0x100
00489dc1  8b5818                   mov ebx, dword ptr [eax + 0x18]
00489dc4  668b5b04                 mov bx, word ptr [ebx + 4]
00489dc8  81e3ffff0000             and ebx, 0xffff
00489dce  81fb00010000             cmp ebx, 0x100
00489dd4  7503                     jne 0x489dd9
00489dd6  895810                   mov dword ptr [eax + 0x10], ebx
00489dd9  8b4010                   mov eax, dword ptr [eax + 0x10]
00489ddc  0fafc2                   imul eax, edx
00489ddf  0faf05588f4900           imul eax, dword ptr [0x498f58]
00489de6  c1f814                   sar eax, 0x14
00489de9  8b0485148f4900           mov eax, dword ptr [eax*4 + 0x498f14]
00489df0  5a                       pop edx
00489df1  5b                       pop ebx
00489df2  c3                       ret
; DeleteHandle
00489df3  53                       push ebx
00489df4  52                       push edx
00489df5  8b5028                   mov edx, dword ptr [eax + 0x28]
00489df8  833aff                   cmp dword ptr [edx], -1
00489dfb  7505                     jne 0x489e02
00489dfd  31c0                     xor eax, eax
00489dff  5a                       pop edx
00489e00  5b                       pop ebx
00489e01  c3                       ret
00489e02  31db                     xor ebx, ebx
00489e04  8a5808                   mov bl, byte ptr [eax + 8]
00489e07  85db                     test ebx, ebx
00489e09  74f2                     je 0x489dfd
00489e0b  83fb02                   cmp ebx, 2
00489e0e  750c                     jne 0x489e1c
00489e10  ba01000000               mov edx, 1
00489e15  e801110000               call 0x48af1b
00489e1a  eb11                     jmp 0x489e2d
00489e1c  c702ffffffff             mov dword ptr [edx], 0xffffffff
00489e22  c6400800                 mov byte ptr [eax + 8], 0
00489e26  c7402000000000           mov dword ptr [eax + 0x20], 0
00489e2d  b801000000               mov eax, 1
00489e32  5a                       pop edx
00489e33  5b                       pop ebx
00489e34  c3                       ret
; DestroyOnlySound
00489e35  53                       push ebx
00489e36  51                       push ecx
00489e37  52                       push edx
00489e38  56                       push esi
00489e39  89c2                     mov edx, eax
00489e3b  8b5820                   mov ebx, dword ptr [eax + 0x20]
00489e3e  85db                     test ebx, ebx
00489e40  746f                     je 0x489eb1
00489e42  8b03                     mov eax, dword ptr [ebx]
00489e44  e870200000               call 0x48beb9
00489e49  85c0                     test eax, eax
00489e4b  7507                     jne 0x489e54
00489e4d  8b03                     mov eax, dword ptr [ebx]
00489e4f  e820210000               call 0x48bf74
00489e54  837a2401                 cmp dword ptr [edx + 0x24], 1
00489e58  7513                     jne 0x489e6d
00489e5a  89d8                     mov eax, ebx
00489e5c  e8520f0000               call 0x48adb3
00489e61  c7422000000000           mov dword ptr [edx + 0x20], 0
00489e68  5e                       pop esi
00489e69  5a                       pop edx
00489e6a  59                       pop ecx
00489e6b  5b                       pop ebx
00489e6c  c3                       ret
00489e6d  89d8                     mov eax, ebx
00489e6f  e8df0d0000               call 0x48ac53
00489e74  8b4204                   mov eax, dword ptr [edx + 4]
00489e77  8b0a                     mov ecx, dword ptr [edx]
00489e79  89c2                     mov edx, eax
00489e7b  89c8                     mov eax, ecx
00489e7d  e831100000               call 0x48aeb3
00489e82  89c1                     mov ecx, eax
00489e84  85c0                     test eax, eax
00489e86  7422                     je 0x489eaa
00489e88  89c2                     mov edx, eax
00489e8a  8b7020                   mov esi, dword ptr [eax + 0x20]
00489e8d  89d8                     mov eax, ebx
00489e8f  e8780e0000               call 0x48ad0c
00489e94  894120                   mov dword ptr [ecx + 0x20], eax
00489e97  89f0                     mov eax, esi
00489e99  e89e0e0000               call 0x48ad3c
00489e9e  c7412400000000           mov dword ptr [ecx + 0x24], 0
00489ea5  5e                       pop esi
00489ea6  5a                       pop edx
00489ea7  59                       pop ecx
00489ea8  5b                       pop ebx
00489ea9  c3                       ret
00489eaa  89d8                     mov eax, ebx
00489eac  e82b0d0000               call 0x48abdc
00489eb1  5e                       pop esi
00489eb2  5a                       pop edx
00489eb3  59                       pop ecx
00489eb4  5b                       pop ebx
00489eb5  c3                       ret
; DestroyHandle
00489eb6  53                       push ebx
00489eb7  52                       push edx
00489eb8  89c3                     mov ebx, eax
00489eba  31c0                     xor eax, eax
00489ebc  8a4308                   mov al, byte ptr [ebx + 8]
00489ebf  83f801                   cmp eax, 1
00489ec2  7507                     jne 0x489ecb
00489ec4  89d8                     mov eax, ebx
00489ec6  e86affffff               call 0x489e35
00489ecb  8b4328                   mov eax, dword ptr [ebx + 0x28]
00489ece  8338ff                   cmp dword ptr [eax], -1
00489ed1  742e                     je 0x489f01
00489ed3  31d2                     xor edx, edx
00489ed5  8a5308                   mov dl, byte ptr [ebx + 8]
00489ed8  85d2                     test edx, edx
00489eda  7425                     je 0x489f01
00489edc  83fa02                   cmp edx, 2
00489edf  750f                     jne 0x489ef0
00489ee1  ba01000000               mov edx, 1
00489ee6  89d8                     mov eax, ebx
00489ee8  e82e100000               call 0x48af1b
00489eed  5a                       pop edx
00489eee  5b                       pop ebx
00489eef  c3                       ret
00489ef0  c700ffffffff             mov dword ptr [eax], 0xffffffff
00489ef6  c6430800                 mov byte ptr [ebx + 8], 0
00489efa  c7432000000000           mov dword ptr [ebx + 0x20], 0
00489f01  5a                       pop edx
00489f02  5b                       pop ebx
00489f03  c3                       ret
; HandleSnd_DestroyDictator
00489f04  53                       push ebx
00489f05  833d901f520000           cmp dword ptr [0x521f90], 0
00489f0c  7429                     je 0x489f37
00489f0e  31db                     xor ebx, ebx
00489f10  a1b41f5200               mov eax, dword ptr [0x521fb4]
00489f15  891d901f5200             mov dword ptr [0x521f90], ebx
00489f1b  8b00                     mov eax, dword ptr [eax]
00489f1d  e852200000               call 0x48bf74
00489f22  a1b41f5200               mov eax, dword ptr [0x521fb4]
00489f27  e868180000               call 0x48b794
00489f2c  a1bc1f5200               mov eax, dword ptr [0x521fbc]
00489f31  c700ffffffff             mov dword ptr [eax], 0xffffffff
00489f37  5b                       pop ebx
00489f38  c3                       ret
; HandleSnd_InitDictator
00489f39  53                       push ebx
00489f3a  52                       push edx
00489f3b  ba3c534900               mov edx, 0x49533c
00489f40  b808000000               mov eax, 8
00489f45  e8ba220000               call 0x48c204
00489f4a  a3c01f5200               mov dword ptr [0x521fc0], eax
00489f4f  a3b41f5200               mov dword ptr [0x521fb4], eax
00489f54  bb01000000               mov ebx, 1
00489f59  c74004941f5200           mov dword ptr [eax + 4], 0x521f94
00489f60  31d2                     xor edx, edx
00489f62  a1c01f5200               mov eax, dword ptr [0x521fc0]
00489f67  8915901f5200             mov dword ptr [0x521f90], edx
00489f6d  891d8c1f5200             mov dword ptr [0x521f8c], ebx
00489f73  5a                       pop edx
00489f74  5b                       pop ebx
00489f75  c3                       ret
; HandleSnd_FreeDictator
00489f76  52                       push edx
00489f77  ba5c534900               mov edx, 0x49535c
00489f7c  b8c01f5200               mov eax, 0x521fc0
00489f81  e8f9220000               call 0x48c27f
00489f86  31d2                     xor edx, edx
00489f88  8915901f5200             mov dword ptr [0x521f90], edx
00489f8e  89158c1f5200             mov dword ptr [0x521f8c], edx
00489f94  5a                       pop edx
00489f95  c3                       ret
; HandlSnd_ClearListe
00489f96  53                       push ebx
00489f97  51                       push ecx
00489f98  52                       push edx
00489f99  31c9                     xor ecx, ecx
00489f9b  eb1d                     jmp 0x489fba
00489f9d  c700ffffffff             mov dword ptr [eax], 0xffffffff
00489fa3  c6430800                 mov byte ptr [ebx + 8], 0
00489fa7  c7432000000000           mov dword ptr [ebx + 0x20], 0
00489fae  83c108                   add ecx, 8
00489fb1  83f950                   cmp ecx, 0x50
00489fb4  0f8463000000             je 0x48a01d
00489fba  8b916c215200             mov edx, dword ptr [ecx + 0x52216c]
00489fc0  85d2                     test edx, edx
00489fc2  74ea                     je 0x489fae
00489fc4  8b8170215200             mov eax, dword ptr [ecx + 0x522170]
00489fca  8a4008                   mov al, byte ptr [eax + 8]
00489fcd  25ff000000               and eax, 0xff
00489fd2  83f801                   cmp eax, 1
00489fd5  75d7                     jne 0x489fae
00489fd7  89d0                     mov eax, edx
00489fd9  e8db1e0000               call 0x48beb9
00489fde  85c0                     test eax, eax
00489fe0  74cc                     je 0x489fae
00489fe2  8b9970215200             mov ebx, dword ptr [ecx + 0x522170]
00489fe8  31c0                     xor eax, eax
00489fea  8a4308                   mov al, byte ptr [ebx + 8]
00489fed  83f801                   cmp eax, 1
00489ff0  7507                     jne 0x489ff9
00489ff2  89d8                     mov eax, ebx
00489ff4  e83cfeffff               call 0x489e35
00489ff9  8b4328                   mov eax, dword ptr [ebx + 0x28]
00489ffc  8338ff                   cmp dword ptr [eax], -1
00489fff  74ad                     je 0x489fae
0048a001  31d2                     xor edx, edx
0048a003  8a5308                   mov dl, byte ptr [ebx + 8]
0048a006  85d2                     test edx, edx
0048a008  74a4                     je 0x489fae
0048a00a  83fa02                   cmp edx, 2
0048a00d  758e                     jne 0x489f9d
0048a00f  ba01000000               mov edx, 1
0048a014  89d8                     mov eax, ebx
0048a016  e8000f0000               call 0x48af1b
0048a01b  eb91                     jmp 0x489fae
0048a01d  31c9                     xor ecx, ecx
0048a01f  eb1d                     jmp 0x48a03e
0048a021  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a027  c6430800                 mov byte ptr [ebx + 8], 0
0048a02b  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a032  83c108                   add ecx, 8
0048a035  83f950                   cmp ecx, 0x50
0048a038  0f8463000000             je 0x48a0a1
0048a03e  8b911c215200             mov edx, dword ptr [ecx + 0x52211c]
0048a044  85d2                     test edx, edx
0048a046  74ea                     je 0x48a032
0048a048  8b8120215200             mov eax, dword ptr [ecx + 0x522120]
0048a04e  8a4008                   mov al, byte ptr [eax + 8]
0048a051  25ff000000               and eax, 0xff
0048a056  83f801                   cmp eax, 1
0048a059  75d7                     jne 0x48a032
0048a05b  89d0                     mov eax, edx
0048a05d  e8571e0000               call 0x48beb9
0048a062  85c0                     test eax, eax
0048a064  74cc                     je 0x48a032
0048a066  8b9920215200             mov ebx, dword ptr [ecx + 0x522120]
0048a06c  31c0                     xor eax, eax
0048a06e  8a4308                   mov al, byte ptr [ebx + 8]
0048a071  83f801                   cmp eax, 1
0048a074  7507                     jne 0x48a07d
0048a076  89d8                     mov eax, ebx
0048a078  e8b8fdffff               call 0x489e35
0048a07d  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a080  8338ff                   cmp dword ptr [eax], -1
0048a083  74ad                     je 0x48a032
0048a085  31d2                     xor edx, edx
0048a087  8a5308                   mov dl, byte ptr [ebx + 8]
0048a08a  85d2                     test edx, edx
0048a08c  74a4                     je 0x48a032
0048a08e  83fa02                   cmp edx, 2
0048a091  758e                     jne 0x48a021
0048a093  ba01000000               mov edx, 1
0048a098  89d8                     mov eax, ebx
0048a09a  e87c0e0000               call 0x48af1b
0048a09f  eb91                     jmp 0x48a032
0048a0a1  833d901f520000           cmp dword ptr [0x521f90], 0
0048a0a8  7441                     je 0x48a0eb
0048a0aa  a1c01f5200               mov eax, dword ptr [0x521fc0]
0048a0af  8b00                     mov eax, dword ptr [eax]
0048a0b1  e8031e0000               call 0x48beb9
0048a0b6  85c0                     test eax, eax
0048a0b8  7431                     je 0x48a0eb
0048a0ba  833d901f520000           cmp dword ptr [0x521f90], 0
0048a0c1  7428                     je 0x48a0eb
0048a0c3  31c0                     xor eax, eax
0048a0c5  a3901f5200               mov dword ptr [0x521f90], eax
0048a0ca  a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a0cf  8b00                     mov eax, dword ptr [eax]
0048a0d1  e89e1e0000               call 0x48bf74
0048a0d6  a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a0db  e8b4160000               call 0x48b794
0048a0e0  a1bc1f5200               mov eax, dword ptr [0x521fbc]
0048a0e5  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a0eb  b801000000               mov eax, 1
0048a0f0  5a                       pop edx
0048a0f1  59                       pop ecx
0048a0f2  5b                       pop ebx
0048a0f3  c3                       ret
; HndSound_LoadDataInfo
0048a0f4  56                       push esi
0048a0f5  57                       push edi
0048a0f6  89c6                     mov esi, eax
0048a0f8  89d7                     mov edi, edx
0048a0fa  89da                     mov edx, ebx
0048a0fc  89f8                     mov eax, edi
0048a0fe  e88d120000               call 0x48b390
0048a103  894618                   mov dword ptr [esi + 0x18], eax
0048a106  85c0                     test eax, eax
0048a108  743b                     je 0x48a145
0048a10a  893e                     mov dword ptr [esi], edi
0048a10c  89da                     mov edx, ebx
0048a10e  8b4618                   mov eax, dword ptr [esi + 0x18]
0048a111  895e04                   mov dword ptr [esi + 4], ebx
0048a114  e89a120000               call 0x48b3b3
0048a119  89461c                   mov dword ptr [esi + 0x1c], eax
0048a11c  8b4618                   mov eax, dword ptr [esi + 0x18]
0048a11f  894e0c                   mov dword ptr [esi + 0xc], ecx
0048a122  668b4004                 mov ax, word ptr [eax + 4]
0048a126  25ffff0000               and eax, 0xffff
0048a12b  3d00010000               cmp eax, 0x100
0048a130  7404                     je 0x48a136
0048a132  8b44240c                 mov eax, dword ptr [esp + 0xc]
0048a136  894610                   mov dword ptr [esi + 0x10], eax
0048a139  b801000000               mov eax, 1
0048a13e  c7461400000000           mov dword ptr [esi + 0x14], 0
0048a145  5f                       pop edi
0048a146  5e                       pop esi
0048a147  c20400                   ret 4
; HandlSnd_SetVolume
0048a14a  53                       push ebx
0048a14b  51                       push ecx
0048a14c  89c3                     mov ebx, eax
0048a14e  8b08                     mov ecx, dword ptr [eax]
0048a150  83f9ff                   cmp ecx, -1
0048a153  7505                     jne 0x48a15a
0048a155  31c0                     xor eax, eax
0048a157  59                       pop ecx
0048a158  5b                       pop ebx
0048a159  c3                       ret
0048a15a  89c8                     mov eax, ecx
0048a15c  c1e002                   shl eax, 2
0048a15f  29c8                     sub eax, ecx
0048a161  c1e002                   shl eax, 2
0048a164  29c8                     sub eax, ecx
0048a166  c1e002                   shl eax, 2
0048a169  31c9                     xor ecx, ecx
0048a16b  8a8884135200             mov cl, byte ptr [eax + 0x521384]
0048a171  85c9                     test ecx, ecx
0048a173  0f8497000000             je 0x48a210
0048a179  89908c135200             mov dword ptr [eax + 0x52138c], edx
0048a17f  8b1b                     mov ebx, dword ptr [ebx]
0048a181  89d8                     mov eax, ebx
0048a183  c1e002                   shl eax, 2
0048a186  29d8                     sub eax, ebx
0048a188  c1e002                   shl eax, 2
0048a18b  29d8                     sub eax, ebx
0048a18d  c1e002                   shl eax, 2
0048a190  8b9894135200             mov ebx, dword ptr [eax + 0x521394]
0048a196  668b5b04                 mov bx, word ptr [ebx + 4]
0048a19a  81e3ffff0000             and ebx, 0xffff
0048a1a0  81fb00010000             cmp ebx, 0x100
0048a1a6  74ad                     je 0x48a155
0048a1a8  85d2                     test edx, edx
0048a1aa  754b                     jne 0x48a1f7
0048a1ac  057c135200               add eax, 0x52137c
0048a1b1  8a5008                   mov dl, byte ptr [eax + 8]
0048a1b4  89c3                     mov ebx, eax
0048a1b6  83fa01                   cmp edx, 1
0048a1b9  7505                     jne 0x48a1c0
0048a1bb  e875fcffff               call 0x489e35
0048a1c0  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a1c3  8338ff                   cmp dword ptr [eax], -1
0048a1c6  7448                     je 0x48a210
0048a1c8  31d2                     xor edx, edx
0048a1ca  8a5308                   mov dl, byte ptr [ebx + 8]
0048a1cd  85d2                     test edx, edx
0048a1cf  743f                     je 0x48a210
0048a1d1  83fa02                   cmp edx, 2
0048a1d4  750e                     jne 0x48a1e4
0048a1d6  ba01000000               mov edx, 1
0048a1db  89d8                     mov eax, ebx
0048a1dd  e8390d0000               call 0x48af1b
0048a1e2  eb2c                     jmp 0x48a210
0048a1e4  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a1ea  c6430800                 mov byte ptr [ebx + 8], 0
0048a1ee  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a1f5  eb19                     jmp 0x48a210
0048a1f7  31d2                     xor edx, edx
0048a1f9  8a9084135200             mov dl, byte ptr [eax + 0x521384]
0048a1ff  83fa01                   cmp edx, 1
0048a202  750c                     jne 0x48a210
0048a204  8915881f5200             mov dword ptr [0x521f88], edx
0048a20a  899090135200             mov dword ptr [eax + 0x521390], edx
0048a210  b801000000               mov eax, 1
0048a215  59                       pop ecx
0048a216  5b                       pop ebx
0048a217  c3                       ret
; HandlSnd_Insert
0048a218  56                       push esi
0048a219  57                       push edi
0048a21a  55                       push ebp
0048a21b  83ec08                   sub esp, 8
0048a21e  89c5                     mov ebp, eax
0048a220  891424                   mov dword ptr [esp], edx
0048a223  89de                     mov esi, ebx
0048a225  8b13                     mov edx, dword ptr [ebx]
0048a227  83faff                   cmp edx, -1
0048a22a  0f8494010000             je 0x48a3c4
0048a230  837c241800               cmp dword ptr [esp + 0x18], 0
0048a235  0f857e000000             jne 0x48a2b9
0048a23b  8b1b                     mov ebx, dword ptr [ebx]
0048a23d  89d8                     mov eax, ebx
0048a23f  c1e002                   shl eax, 2
0048a242  29d8                     sub eax, ebx
0048a244  c1e002                   shl eax, 2
0048a247  29d8                     sub eax, ebx
0048a249  c1e002                   shl eax, 2
0048a24c  8b9894135200             mov ebx, dword ptr [eax + 0x521394]
0048a252  668b5b04                 mov bx, word ptr [ebx + 4]
0048a256  81e3ffff0000             and ebx, 0xffff
0048a25c  81fb00010000             cmp ebx, 0x100
0048a262  7455                     je 0x48a2b9
0048a264  057c135200               add eax, 0x52137c
0048a269  31db                     xor ebx, ebx
0048a26b  8a5808                   mov bl, byte ptr [eax + 8]
0048a26e  89c6                     mov esi, eax
0048a270  83fb01                   cmp ebx, 1
0048a273  7505                     jne 0x48a27a
0048a275  e8bbfbffff               call 0x489e35
0048a27a  8b4628                   mov eax, dword ptr [esi + 0x28]
0048a27d  8338ff                   cmp dword ptr [eax], -1
0048a280  742d                     je 0x48a2af
0048a282  31db                     xor ebx, ebx
0048a284  8a5e08                   mov bl, byte ptr [esi + 8]
0048a287  85db                     test ebx, ebx
0048a289  7424                     je 0x48a2af
0048a28b  83fb02                   cmp ebx, 2
0048a28e  750e                     jne 0x48a29e
0048a290  ba01000000               mov edx, 1
0048a295  89f0                     mov eax, esi
0048a297  e87f0c0000               call 0x48af1b
0048a29c  eb11                     jmp 0x48a2af
0048a29e  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a2a4  c6460800                 mov byte ptr [esi + 8], 0
0048a2a8  c7462000000000           mov dword ptr [esi + 0x20], 0
0048a2af  b801000000               mov eax, 1
0048a2b4  e976010000               jmp 0x48a42f
0048a2b9  8b1e                     mov ebx, dword ptr [esi]
0048a2bb  89d8                     mov eax, ebx
0048a2bd  c1e002                   shl eax, 2
0048a2c0  29d8                     sub eax, ebx
0048a2c2  c1e002                   shl eax, 2
0048a2c5  29d8                     sub eax, ebx
0048a2c7  c1e002                   shl eax, 2
0048a2ca  3ba87c135200             cmp ebp, dword ptr [eax + 0x52137c]
0048a2d0  7518                     jne 0x48a2ea
0048a2d2  8b1c24                   mov ebx, dword ptr [esp]
0048a2d5  3b9880135200             cmp ebx, dword ptr [eax + 0x521380]
0048a2db  750d                     jne 0x48a2ea
0048a2dd  8b542418                 mov edx, dword ptr [esp + 0x18]
0048a2e1  89f0                     mov eax, esi
0048a2e3  e862feffff               call 0x48a14a
0048a2e8  ebc5                     jmp 0x48a2af
0048a2ea  8b1e                     mov ebx, dword ptr [esi]
0048a2ec  89d8                     mov eax, ebx
0048a2ee  c1e002                   shl eax, 2
0048a2f1  29d8                     sub eax, ebx
0048a2f3  c1e002                   shl eax, 2
0048a2f6  29d8                     sub eax, ebx
0048a2f8  c1e002                   shl eax, 2
0048a2fb  31db                     xor ebx, ebx
0048a2fd  8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048a303  83fb01                   cmp ebx, 1
0048a306  7566                     jne 0x48a36e
0048a308  057c135200               add eax, 0x52137c
0048a30d  0fb67808                 movzx edi, byte ptr [eax + 8]
0048a311  89c3                     mov ebx, eax
0048a313  83ff01                   cmp edi, 1
0048a316  7505                     jne 0x48a31d
0048a318  e818fbffff               call 0x489e35
0048a31d  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a320  8338ff                   cmp dword ptr [eax], -1
0048a323  742c                     je 0x48a351
0048a325  0fb67b08                 movzx edi, byte ptr [ebx + 8]
0048a329  85ff                     test edi, edi
0048a32b  7424                     je 0x48a351
0048a32d  83ff02                   cmp edi, 2
0048a330  750e                     jne 0x48a340
0048a332  ba01000000               mov edx, 1
0048a337  89d8                     mov eax, ebx
0048a339  e8dd0b0000               call 0x48af1b
0048a33e  eb11                     jmp 0x48a351
0048a340  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a346  c6430800                 mov byte ptr [ebx + 8], 0
0048a34a  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a351  e8a20b0000               call 0x48aef8
0048a356  8906                     mov dword ptr [esi], eax
0048a358  83f8ff                   cmp eax, -1
0048a35b  7507                     jne 0x48a364
0048a35d  31c0                     xor eax, eax
0048a35f  e9cb000000               jmp 0x48a42f
0048a364  c705841f520001000000     mov dword ptr [0x521f84], 1
0048a36e  8b442418                 mov eax, dword ptr [esp + 0x18]
0048a372  8b1e                     mov ebx, dword ptr [esi]
0048a374  50                       push eax
0048a375  89d8                     mov eax, ebx
0048a377  c1e002                   shl eax, 2
0048a37a  29d8                     sub eax, ebx
0048a37c  c1e002                   shl eax, 2
0048a37f  29d8                     sub eax, ebx
0048a381  89ea                     mov edx, ebp
0048a383  c1e002                   shl eax, 2
0048a386  8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a38a  057c135200               add eax, 0x52137c
0048a38f  e860fdffff               call 0x48a0f4
0048a394  8b1e                     mov ebx, dword ptr [esi]
0048a396  89d8                     mov eax, ebx
0048a398  c1e002                   shl eax, 2
0048a39b  29d8                     sub eax, ebx
0048a39d  c1e002                   shl eax, 2
0048a3a0  29d8                     sub eax, ebx
0048a3a2  893485a4135200           mov dword ptr [eax*4 + 0x5213a4], esi
0048a3a9  8b1e                     mov ebx, dword ptr [esi]
0048a3ab  89d8                     mov eax, ebx
0048a3ad  c1e002                   shl eax, 2
0048a3b0  29d8                     sub eax, ebx
0048a3b2  c1e002                   shl eax, 2
0048a3b5  29d8                     sub eax, ebx
0048a3b7  c604858413520002         mov byte ptr [eax*4 + 0x521384], 2
0048a3bf  e9ebfeffff               jmp 0x48a2af
0048a3c4  e82f0b0000               call 0x48aef8
0048a3c9  89442404                 mov dword ptr [esp + 4], eax
0048a3cd  39d0                     cmp eax, edx
0048a3cf  7504                     jne 0x48a3d5
0048a3d1  31d0                     xor eax, edx
0048a3d3  eb5a                     jmp 0x48a42f
0048a3d5  8b7c2418                 mov edi, dword ptr [esp + 0x18]
0048a3d9  57                       push edi
0048a3da  89c7                     mov edi, eax
0048a3dc  c1e702                   shl edi, 2
0048a3df  29c7                     sub edi, eax
0048a3e1  c1e702                   shl edi, 2
0048a3e4  8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a3e8  29c7                     sub edi, eax
0048a3ea  b87c135200               mov eax, 0x52137c
0048a3ef  c1e702                   shl edi, 2
0048a3f2  89ea                     mov edx, ebp
0048a3f4  01f8                     add eax, edi
0048a3f6  e8f9fcffff               call 0x48a0f4
0048a3fb  85c0                     test eax, eax
0048a3fd  750a                     jne 0x48a409
0048a3ff  e8cc0b0000               call 0x48afd0
0048a404  e954ffffff               jmp 0x48a35d
0048a409  8b442404                 mov eax, dword ptr [esp + 4]
0048a40d  8906                     mov dword ptr [esi], eax
0048a40f  b402                     mov ah, 2
0048a411  89b7a4135200             mov dword ptr [edi + 0x5213a4], esi
0048a417  31ed                     xor ebp, ebp
0048a419  88a784135200             mov byte ptr [edi + 0x521384], ah
0048a41f  b801000000               mov eax, 1
0048a424  89af90135200             mov dword ptr [edi + 0x521390], ebp
0048a42a  a3841f5200               mov dword ptr [0x521f84], eax
0048a42f  83c408                   add esp, 8
0048a432  5d                       pop ebp
0048a433  5f                       pop edi
0048a434  5e                       pop esi
0048a435  c20400                   ret 4
; HandleSnd_StopHandle
0048a438  53                       push ebx
0048a439  52                       push edx
0048a43a  8b10                     mov edx, dword ptr [eax]
0048a43c  83faff                   cmp edx, -1
0048a43f  7505                     jne 0x48a446
0048a441  31c0                     xor eax, eax
0048a443  5a                       pop edx
0048a444  5b                       pop ebx
0048a445  c3                       ret
0048a446  89d0                     mov eax, edx
0048a448  c1e002                   shl eax, 2
0048a44b  29d0                     sub eax, edx
0048a44d  c1e002                   shl eax, 2
0048a450  29d0                     sub eax, edx
0048a452  c1e002                   shl eax, 2
0048a455  057c135200               add eax, 0x52137c
0048a45a  31d2                     xor edx, edx
0048a45c  8a5008                   mov dl, byte ptr [eax + 8]
0048a45f  89c3                     mov ebx, eax
0048a461  83fa01                   cmp edx, 1
0048a464  7505                     jne 0x48a46b
0048a466  e8caf9ffff               call 0x489e35
0048a46b  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a46e  8338ff                   cmp dword ptr [eax], -1
0048a471  742d                     je 0x48a4a0
0048a473  31d2                     xor edx, edx
0048a475  8a5308                   mov dl, byte ptr [ebx + 8]
0048a478  85d2                     test edx, edx
0048a47a  7424                     je 0x48a4a0
0048a47c  83fa02                   cmp edx, 2
0048a47f  750e                     jne 0x48a48f
0048a481  ba01000000               mov edx, 1
0048a486  89d8                     mov eax, ebx
0048a488  e88e0a0000               call 0x48af1b
0048a48d  eb11                     jmp 0x48a4a0
0048a48f  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a495  c6430800                 mov byte ptr [ebx + 8], 0
0048a499  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a4a0  b801000000               mov eax, 1
0048a4a5  5a                       pop edx
0048a4a6  5b                       pop ebx
0048a4a7  c3                       ret
; HandleSnd_StopAllHandle
0048a4a8  53                       push ebx
0048a4a9  51                       push ecx
0048a4aa  52                       push edx
0048a4ab  31c9                     xor ecx, ecx
0048a4ad  eb20                     jmp 0x48a4cf
0048a4af  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a4b5  c6430800                 mov byte ptr [ebx + 8], 0
0048a4b9  c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a4c0  83c12c                   add ecx, 0x2c
0048a4c3  81f998080000             cmp ecx, 0x898
0048a4c9  0f8421fcffff             je 0x48a0f0
0048a4cf  31c0                     xor eax, eax
0048a4d1  8a8184135200             mov al, byte ptr [ecx + 0x521384]
0048a4d7  85c0                     test eax, eax
0048a4d9  74e5                     je 0x48a4c0
0048a4db  b87c135200               mov eax, 0x52137c
0048a4e0  01c8                     add eax, ecx
0048a4e2  31d2                     xor edx, edx
0048a4e4  8a5008                   mov dl, byte ptr [eax + 8]
0048a4e7  89c3                     mov ebx, eax
0048a4e9  83fa01                   cmp edx, 1
0048a4ec  7505                     jne 0x48a4f3
0048a4ee  e842f9ffff               call 0x489e35
0048a4f3  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a4f6  8338ff                   cmp dword ptr [eax], -1
0048a4f9  74c5                     je 0x48a4c0
0048a4fb  31d2                     xor edx, edx
0048a4fd  8a5308                   mov dl, byte ptr [ebx + 8]
0048a500  85d2                     test edx, edx
0048a502  74bc                     je 0x48a4c0
0048a504  83fa02                   cmp edx, 2
0048a507  75a6                     jne 0x48a4af
0048a509  ba01000000               mov edx, 1
0048a50e  89d8                     mov eax, ebx
0048a510  e8060a0000               call 0x48af1b
0048a515  eba9                     jmp 0x48a4c0
; HandlSnd_AffectVolumeOut
0048a517  53                       push ebx
0048a518  51                       push ecx
0048a519  52                       push edx
0048a51a  56                       push esi
0048a51b  55                       push ebp
0048a51c  833d881f520000           cmp dword ptr [0x521f88], 0
0048a523  750d                     jne 0x48a532
0048a525  833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a52c  0f8424010000             je 0x48a656
0048a532  be7c135200               mov esi, 0x52137c
0048a537  31db                     xor ebx, ebx
0048a539  eb12                     jmp 0x48a54d
0048a53b  83c32c                   add ebx, 0x2c
0048a53e  83c62c                   add esi, 0x2c
0048a541  81fb70030000             cmp ebx, 0x370
0048a547  0f8498000000             je 0x48a5e5
0048a54d  31c0                     xor eax, eax
0048a54f  8a8384135200             mov al, byte ptr [ebx + 0x521384]
0048a555  85c0                     test eax, eax
0048a557  74e2                     je 0x48a53b
0048a559  8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048a55f  8338ff                   cmp dword ptr [eax], -1
0048a562  74d7                     je 0x48a53b
0048a564  8b8b9c135200             mov ecx, dword ptr [ebx + 0x52139c]
0048a56a  85c9                     test ecx, ecx
0048a56c  74cd                     je 0x48a53b
0048a56e  833900                   cmp dword ptr [ecx], 0
0048a571  74c8                     je 0x48a53b
0048a573  83bb9013520001           cmp dword ptr [ebx + 0x521390], 1
0048a57a  7409                     je 0x48a585
0048a57c  833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a583  74b6                     je 0x48a53b
0048a585  8b561c                   mov edx, dword ptr [esi + 0x1c]
0048a588  89f0                     mov eax, esi
0048a58a  8a520d                   mov dl, byte ptr [edx + 0xd]
0048a58d  81e2ff000000             and edx, 0xff
0048a593  7505                     jne 0x48a59a
0048a595  ba00010000               mov edx, 0x100
0048a59a  8b4818                   mov ecx, dword ptr [eax + 0x18]
0048a59d  668b4904                 mov cx, word ptr [ecx + 4]
0048a5a1  81e1ffff0000             and ecx, 0xffff
0048a5a7  81f900010000             cmp ecx, 0x100
0048a5ad  7503                     jne 0x48a5b2
0048a5af  894810                   mov dword ptr [eax + 0x10], ecx
0048a5b2  8b4010                   mov eax, dword ptr [eax + 0x10]
0048a5b5  0fafc2                   imul eax, edx
0048a5b8  0faf05588f4900           imul eax, dword ptr [0x498f58]
0048a5bf  c1f814                   sar eax, 0x14
0048a5c2  8b0c85148f4900           mov ecx, dword ptr [eax*4 + 0x498f14]
0048a5c9  8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048a5cf  51                       push ecx
0048a5d0  8b00                     mov eax, dword ptr [eax]
0048a5d2  50                       push eax
0048a5d3  8b10                     mov edx, dword ptr [eax]
0048a5d5  ff523c                   call dword ptr [edx + 0x3c]
0048a5d8  31c9                     xor ecx, ecx
0048a5da  898b90135200             mov dword ptr [ebx + 0x521390], ecx
0048a5e0  e956ffffff               jmp 0x48a53b
0048a5e5  833d901f520000           cmp dword ptr [0x521f90], 0
0048a5ec  7460                     je 0x48a64e
0048a5ee  833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a5f5  7457                     je 0x48a64e
0048a5f7  8b15b01f5200             mov edx, dword ptr [0x521fb0]
0048a5fd  b8941f5200               mov eax, 0x521f94
0048a602  8a520d                   mov dl, byte ptr [edx + 0xd]
0048a605  81e2ff000000             and edx, 0xff
0048a60b  7505                     jne 0x48a612
0048a60d  ba00010000               mov edx, 0x100
0048a612  8b5818                   mov ebx, dword ptr [eax + 0x18]
0048a615  668b5b04                 mov bx, word ptr [ebx + 4]
0048a619  81e3ffff0000             and ebx, 0xffff
0048a61f  81fb00010000             cmp ebx, 0x100
0048a625  7503                     jne 0x48a62a
0048a627  895810                   mov dword ptr [eax + 0x10], ebx
0048a62a  0faf5010                 imul edx, dword ptr [eax + 0x10]
0048a62e  a1588f4900               mov eax, dword ptr [0x498f58]
0048a633  0fafc2                   imul eax, edx
0048a636  c1f814                   sar eax, 0x14
0048a639  8b1c85148f4900           mov ebx, dword ptr [eax*4 + 0x498f14]
0048a640  a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a645  53                       push ebx
0048a646  8b00                     mov eax, dword ptr [eax]
0048a648  50                       push eax
0048a649  8b10                     mov edx, dword ptr [eax]
0048a64b  ff523c                   call dword ptr [edx + 0x3c]
0048a64e  31ed                     xor ebp, ebp
0048a650  892d881f5200             mov dword ptr [0x521f88], ebp
0048a656  31f6                     xor esi, esi
0048a658  89355c8f4900             mov dword ptr [0x498f5c], esi
0048a65e  5d                       pop ebp
0048a65f  5e                       pop esi
0048a660  5a                       pop edx
0048a661  59                       pop ecx
0048a662  5b                       pop ebx
0048a663  c3                       ret
; HandlSnd_TriWaitingHandle
0048a664  53                       push ebx
0048a665  833d841f520001           cmp dword ptr [0x521f84], 1
0048a66c  750d                     jne 0x48a67b
0048a66e  31db                     xor ebx, ebx
0048a670  e81a0d0000               call 0x48b38f
0048a675  891d841f5200             mov dword ptr [0x521f84], ebx
0048a67b  5b                       pop ebx
0048a67c  c3                       ret
0048a67d  be7c135200               mov esi, 0x52137c
0048a682  01de                     add esi, ebx
0048a684  85d2                     test edx, edx
0048a686  0f8414010000             je 0x48a7a0
0048a68c  e856080000               call 0x48aee7
0048a691  85c0                     test eax, eax
0048a693  740f                     je 0x48a6a4
0048a695  e890060000               call 0x48ad2a
0048a69a  85c0                     test eax, eax
0048a69c  0f854b010000             jne 0x48a7ed
0048a6a2  eb19                     jmp 0x48a6bd
0048a6a4  8b02                     mov eax, dword ptr [edx]
0048a6a6  89f2                     mov edx, esi
0048a6a8  e8b2070000               call 0x48ae5f
0048a6ad  89839c135200             mov dword ptr [ebx + 0x52139c], eax
0048a6b3  85c0                     test eax, eax
0048a6b5  0f85d9000000             jne 0x48a794
0048a6bb  31ff                     xor edi, edi
0048a6bd  83ed2c                   sub ebp, 0x2c
0048a6c0  49                       dec ecx
0048a6c1  83f913                   cmp ecx, 0x13
0048a6c4  0f8e23010000             jle 0x48a7ed
0048a6ca  6bd92c                   imul ebx, ecx, 0x2c
0048a6cd  8b9380135200             mov edx, dword ptr [ebx + 0x521380]
0048a6d3  8b837c135200             mov eax, dword ptr [ebx + 0x52137c]
0048a6d9  e8f5050000               call 0x48acd3
0048a6de  8bb394135200             mov esi, dword ptr [ebx + 0x521394]
0048a6e4  89c2                     mov edx, eax
0048a6e6  31c0                     xor eax, eax
0048a6e8  668b4604                 mov ax, word ptr [esi + 4]
0048a6ec  3d00010000               cmp eax, 0x100
0048a6f1  0f940424                 sete byte ptr [esp]
0048a6f5  31c0                     xor eax, eax
0048a6f7  8a0424                   mov al, byte ptr [esp]
0048a6fa  85c0                     test eax, eax
0048a6fc  0f847bffffff             je 0x48a67d
0048a702  8b15901f5200             mov edx, dword ptr [0x521f90]
0048a708  85d2                     test edx, edx
0048a70a  75b1                     jne 0x48a6bd
0048a70c  8915a01f5200             mov dword ptr [0x521fa0], edx
0048a712  8935ac1f5200             mov dword ptr [0x521fac], esi
0048a718  8b8380135200             mov eax, dword ptr [ebx + 0x521380]
0048a71e  ba00010000               mov edx, 0x100
0048a723  a3981f5200               mov dword ptr [0x521f98], eax
0048a728  8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048a72e  8915a41f5200             mov dword ptr [0x521fa4], edx
0048a734  a3bc1f5200               mov dword ptr [0x521fbc], eax
0048a739  8b837c135200             mov eax, dword ptr [ebx + 0x52137c]
0048a73f  8b15981f5200             mov edx, dword ptr [0x521f98]
0048a745  a3941f5200               mov dword ptr [0x521f94], eax
0048a74a  8b8398135200             mov eax, dword ptr [ebx + 0x521398]
0048a750  bb01000000               mov ebx, 1
0048a755  a3b01f5200               mov dword ptr [0x521fb0], eax
0048a75a  891da81f5200             mov dword ptr [0x521fa8], ebx
0048a760  e86f030000               call 0x48aad4
0048a765  8b15b41f5200             mov edx, dword ptr [0x521fb4]
0048a76b  8902                     mov dword ptr [edx], eax
0048a76d  b8941f5200               mov eax, 0x521f94
0048a772  e87d170000               call 0x48bef4
0048a777  85c0                     test eax, eax
0048a779  7502                     jne 0x48a77d
0048a77b  31ff                     xor edi, edi
0048a77d  89c8                     mov eax, ecx
0048a77f  be01000000               mov esi, 1
0048a784  e894090000               call 0x48b11d
0048a789  8935901f5200             mov dword ptr [0x521f90], esi
0048a78f  e929ffffff               jmp 0x48a6bd
0048a794  c783a013520001000000     mov dword ptr [ebx + 0x5213a0], 1
0048a79e  eb2a                     jmp 0x48a7ca
0048a7a0  e885050000               call 0x48ad2a
0048a7a5  85c0                     test eax, eax
0048a7a7  0f8510ffffff             jne 0x48a6bd
0048a7ad  89f0                     mov eax, esi
0048a7af  e8c4040000               call 0x48ac78
0048a7b4  89839c135200             mov dword ptr [ebx + 0x52139c], eax
0048a7ba  85c0                     test eax, eax
0048a7bc  0f84f9feffff             je 0x48a6bb
0048a7c2  31f6                     xor esi, esi
0048a7c4  89b3a0135200             mov dword ptr [ebx + 0x5213a0], esi
0048a7ca  89e8                     mov eax, ebp
0048a7cc  e823170000               call 0x48bef4
0048a7d1  85c0                     test eax, eax
0048a7d3  7502                     jne 0x48a7d7
0048a7d5  31ff                     xor edi, edi
0048a7d7  89c8                     mov eax, ecx
0048a7d9  e80b0a0000               call 0x48b1e9
0048a7de  c705841f520001000000     mov dword ptr [0x521f84], 1
0048a7e8  e9d0feffff               jmp 0x48a6bd
0048a7ed  89f8                     mov eax, edi
0048a7ef  83c404                   add esp, 4
0048a7f2  5d                       pop ebp
0048a7f3  5f                       pop edi
0048a7f4  5e                       pop esi
0048a7f5  5a                       pop edx
0048a7f6  59                       pop ecx
0048a7f7  5b                       pop ebx
0048a7f8  c3                       ret
; HandlSnd_ValidateListe
0048a7f9  e898f7ffff               call 0x489f96
0048a7fe  e814fdffff               call 0x48a517
; HandlSnd_LaunchWaitingSound
0048a803  53                       push ebx
0048a804  51                       push ecx
0048a805  52                       push edx
0048a806  56                       push esi
0048a807  57                       push edi
0048a808  55                       push ebp
0048a809  83ec04                   sub esp, 4
0048a80c  e8d8070000               call 0x48afe9
0048a811  89c5                     mov ebp, eax
0048a813  c1e502                   shl ebp, 2
0048a816  29c5                     sub ebp, eax
0048a818  c1e502                   shl ebp, 2
0048a81b  29c5                     sub ebp, eax
0048a81d  bf01000000               mov edi, 1
0048a822  c1e502                   shl ebp, 2
0048a825  89c1                     mov ecx, eax
0048a827  81c57c135200             add ebp, 0x52137c
0048a82d  e98ffeffff               jmp 0x48a6c1
; PlaySnd_CreateSoundPath
0048a834  52                       push edx
0048a835  bae8030000               mov edx, 0x3e8
0048a83a  31c0                     xor eax, eax
0048a83c  e8401c0000               call 0x48c481
0048a841  89c2                     mov edx, eax
0048a843  803800                   cmp byte ptr [eax], 0
0048a846  7403                     je 0x48a84b
0048a848  40                       inc eax
0048a849  ebf8                     jmp 0x48a843
0048a84b  8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a84f  750d                     jne 0x48a85e
0048a851  687c534900               push 0x49537c
0048a856  52                       push edx
0048a857  6882534900               push 0x495382
0048a85c  eb0b                     jmp 0x48a869
0048a85e  6887534900               push 0x495387
0048a863  52                       push edx
0048a864  688d534900               push 0x49538d
0048a869  681c205200               push 0x52201c
0048a86e  e848270000               call 0x48cfbb
0048a873  83c410                   add esp, 0x10
0048a876  89d0                     mov eax, edx
0048a878  e8772f0000               call 0x48d7f4
0048a87d  5a                       pop edx
0048a87e  c3                       ret
; SoundFile
0048a87f  50                       push eax
0048a880  681c205200               push 0x52201c
0048a885  6893534900               push 0x495393
0048a88a  52                       push edx
0048a88b  e82b270000               call 0x48cfbb
0048a890  83c410                   add esp, 0x10
0048a893  c3                       ret
; PlaySnd_MakeID
0048a894  c1e010                   shl eax, 0x10
0048a897  c1e208                   shl edx, 8
0048a89a  09d0                     or eax, edx
0048a89c  09d8                     or eax, ebx
0048a89e  c3                       ret
; PlaySnd_InitSoundLib
0048a89f  51                       push ecx
0048a8a0  52                       push edx
0048a8a1  56                       push esi
0048a8a2  81ec00010000             sub esp, 0x100
0048a8a8  803dc41f520000           cmp byte ptr [0x521fc4], 0
0048a8af  7407                     je 0x48a8b8
0048a8b1  30c0                     xor al, al
0048a8b3  e942010000               jmp 0x48a9fa
0048a8b8  a1e8274e00               mov eax, dword ptr [0x4e27e8]
0048a8bd  e835150000               call 0x48bdf7
0048a8c2  85c0                     test eax, eax
0048a8c4  74eb                     je 0x48a8b1
0048a8c6  e8a1180000               call 0x48c16c
0048a8cb  85c0                     test eax, eax
0048a8cd  74e2                     je 0x48a8b1
0048a8cf  bae8030000               mov edx, 0x3e8
0048a8d4  31c0                     xor eax, eax
0048a8d6  e8a61b0000               call 0x48c481
0048a8db  89c2                     mov edx, eax
0048a8dd  803800                   cmp byte ptr [eax], 0
0048a8e0  7403                     je 0x48a8e5
0048a8e2  40                       inc eax
0048a8e3  ebf8                     jmp 0x48a8dd
0048a8e5  8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a8e9  750d                     jne 0x48a8f8
0048a8eb  687c534900               push 0x49537c
0048a8f0  52                       push edx
0048a8f1  6882534900               push 0x495382
0048a8f6  eb0b                     jmp 0x48a903
0048a8f8  6887534900               push 0x495387
0048a8fd  52                       push edx
0048a8fe  688d534900               push 0x49538d
0048a903  681c205200               push 0x52201c
0048a908  e8ae260000               call 0x48cfbb
0048a90d  83c410                   add esp, 0x10
0048a910  89d0                     mov eax, edx
0048a912  e8dd2e0000               call 0x48d7f4
0048a917  6899534900               push 0x495399
0048a91c  681c205200               push 0x52201c
0048a921  31d2                     xor edx, edx
0048a923  6893534900               push 0x495393
0048a928  8d44240c                 lea eax, [esp + 0xc]
0048a92c  8915c81f5200             mov dword ptr [0x521fc8], edx
0048a932  50                       push eax
0048a933  8915e41f5200             mov dword ptr [0x521fe4], edx
0048a939  891500205200             mov dword ptr [0x522000], edx
0048a93f  e877260000               call 0x48cfbb
0048a944  83c410                   add esp, 0x10
0048a947  bac81f5200               mov edx, 0x521fc8
0048a94c  89e0                     mov eax, esp
0048a94e  e8530c0000               call 0x48b5a6
0048a953  85c0                     test eax, eax
0048a955  0f8456ffffff             je 0x48a8b1
0048a95b  689b534900               push 0x49539b
0048a960  681c205200               push 0x52201c
0048a965  6893534900               push 0x495393
0048a96a  8d44240c                 lea eax, [esp + 0xc]
0048a96e  50                       push eax
0048a96f  e847260000               call 0x48cfbb
0048a974  83c410                   add esp, 0x10
0048a977  bae41f5200               mov edx, 0x521fe4
0048a97c  89e0                     mov eax, esp
0048a97e  e8230c0000               call 0x48b5a6
0048a983  85c0                     test eax, eax
0048a985  0f8426ffffff             je 0x48a8b1
0048a98b  689d534900               push 0x49539d
0048a990  681c205200               push 0x52201c
0048a995  6893534900               push 0x495393
0048a99a  8d44240c                 lea eax, [esp + 0xc]
0048a99e  50                       push eax
0048a99f  e817260000               call 0x48cfbb
0048a9a4  83c410                   add esp, 0x10
0048a9a7  ba00205200               mov edx, 0x522000
0048a9ac  89e0                     mov eax, esp
0048a9ae  e8f30b0000               call 0x48b5a6
0048a9b3  85c0                     test eax, eax
0048a9b5  0f84f6feffff             je 0x48a8b1
0048a9bb  e879f5ffff               call 0x489f39
0048a9c0  85c0                     test eax, eax
0048a9c2  0f84e9feffff             je 0x48a8b1
0048a9c8  31c0                     xor eax, eax
0048a9ca  83c02c                   add eax, 0x2c
0048a9cd  30c9                     xor cl, cl
0048a9cf  31f6                     xor esi, esi
0048a9d1  888858135200             mov byte ptr [eax + 0x521358], cl
0048a9d7  89b070135200             mov dword ptr [eax + 0x521370], esi
0048a9dd  89b078135200             mov dword ptr [eax + 0x521378], esi
0048a9e3  89b064135200             mov dword ptr [eax + 0x521364], esi
0048a9e9  3d080c0000               cmp eax, 0xc08
0048a9ee  75da                     jne 0x48a9ca
0048a9f0  b501                     mov ch, 1
0048a9f2  882dc41f5200             mov byte ptr [0x521fc4], ch
0048a9f8  88e8                     mov al, ch
0048a9fa  81c400010000             add esp, 0x100
0048aa00  5e                       pop esi
0048aa01  5a                       pop edx
0048aa02  59                       pop ecx
0048aa03  c3                       ret
; PlaySnd_FreeSoundLib
0048aa04  52                       push edx
0048aa05  803dc41f520000           cmp byte ptr [0x521fc4], 0
0048aa0c  7435                     je 0x48aa43
0048aa0e  e863f5ffff               call 0x489f76
0048aa13  b800205200               mov eax, 0x522000
0048aa18  e86a0c0000               call 0x48b687
0048aa1d  b8e41f5200               mov eax, 0x521fe4
0048aa22  e8600c0000               call 0x48b687
0048aa27  b8c81f5200               mov eax, 0x521fc8
0048aa2c  30d2                     xor dl, dl
0048aa2e  e8540c0000               call 0x48b687
0048aa33  e855170000               call 0x48c18d
0048aa38  e819140000               call 0x48be56
0048aa3d  8815c41f5200             mov byte ptr [0x521fc4], dl
0048aa43  5a                       pop edx
0048aa44  c3                       ret
; PlaySnd_SetGameVolume
0048aa45  51                       push ecx
0048aa46  a3588f4900               mov dword ptr [0x498f58], eax
0048aa4b  3d00010000               cmp eax, 0x100
0048aa50  7e0a                     jle 0x48aa5c
0048aa52  c705588f490000010000     mov dword ptr [0x498f58], 0x100
0048aa5c  833d588f490000           cmp dword ptr [0x498f58], 0
0048aa63  7d08                     jge 0x48aa6d
0048aa65  31c9                     xor ecx, ecx
0048aa67  890d588f4900             mov dword ptr [0x498f58], ecx
0048aa6d  c7055c8f490001000000     mov dword ptr [0x498f5c], 1
0048aa77  59                       pop ecx
0048aa78  c3                       ret
; PlaySnd_PostSound
0048aa79  56                       push esi
0048aa7a  89c6                     mov esi, eax
0048aa7c  89d0                     mov eax, edx
0048aa7e  8b542408                 mov edx, dword ptr [esp + 8]
0048aa82  83fe42                   cmp esi, 0x42
0048aa85  7230                     jb 0x48aab7
0048aa87  761e                     jbe 0x48aaa7
0048aa89  83fe50                   cmp esi, 0x50
0048aa8c  7421                     je 0x48aaaf
0048aa8e  5e                       pop esi
0048aa8f  c20400                   ret 4
0048aa92  52                       push edx
0048aa93  bac81f5200               mov edx, 0x521fc8
0048aa98  81e1ff000000             and ecx, 0xff
0048aa9e  e875f7ffff               call 0x48a218
0048aaa3  5e                       pop esi
0048aaa4  c20400                   ret 4
0048aaa7  52                       push edx
0048aaa8  bae41f5200               mov edx, 0x521fe4
0048aaad  ebe9                     jmp 0x48aa98
0048aaaf  52                       push edx
0048aab0  ba00205200               mov edx, 0x522000
0048aab5  ebe1                     jmp 0x48aa98
0048aab7  83fe41                   cmp esi, 0x41
0048aaba  74d6                     je 0x48aa92
0048aabc  5e                       pop esi
0048aabd  c20400                   ret 4
; PlaySnd_StopSound
0048aac0  e973f9ffff               jmp 0x48a438
; PlaySnd_StopAllSound
0048aac5  e9def9ffff               jmp 0x48a4a8
; PlaySnd_Manage
0048aaca  e92afdffff               jmp 0x48a7f9
; PlaySnd_PostVolume
0048aacf  e976f6ffff               jmp 0x48a14a
; PSB_CreateMySurfaceWithSound
0048aad4  53                       push ebx
0048aad5  51                       push ecx
0048aad6  56                       push esi
0048aad7  57                       push edi
0048aad8  55                       push ebp
0048aad9  89c6                     mov esi, eax
0048aadb  89d7                     mov edi, edx
0048aadd  8b5210                   mov edx, dword ptr [edx + 0x10]
0048aae0  31ed                     xor ebp, ebp
0048aae2  85d2                     test edx, edx
0048aae4  0f850a000000             jne 0x48aaf4
0048aaea  8b4708                   mov eax, dword ptr [edi + 8]
0048aaed  31db                     xor ebx, ebx
0048aaef  e86a150000               call 0x48c05e
0048aaf4  8a460c                   mov al, byte ptr [esi + 0xc]
0048aaf7  84c0                     test al, al
0048aaf9  760c                     jbe 0x48ab07
0048aafb  3c04                     cmp al, 4
0048aafd  745a                     je 0x48ab59
0048aaff  89e8                     mov eax, ebp
0048ab01  5d                       pop ebp
0048ab02  5f                       pop edi
0048ab03  5e                       pop esi
0048ab04  59                       pop ecx
0048ab05  5b                       pop ebx
0048ab06  c3                       ret
0048ab07  8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab0a  31db                     xor ebx, ebx
0048ab0c  31d2                     xor edx, edx
0048ab0e  31c0                     xor eax, eax
0048ab10  8a5e09                   mov bl, byte ptr [esi + 9]
0048ab13  668b560a                 mov dx, word ptr [esi + 0xa]
0048ab17  8a4608                   mov al, byte ptr [esi + 8]
0048ab1a  e8920c0000               call 0x48b7b1
0048ab1f  89c1                     mov ecx, eax
0048ab21  89c5                     mov ebp, eax
0048ab23  85c0                     test eax, eax
0048ab25  74da                     je 0x48ab01
0048ab27  837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab2b  7513                     jne 0x48ab40
0048ab2d  8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab30  8b1e                     mov ebx, dword ptr [esi]
0048ab32  89c8                     mov eax, ecx
0048ab34  01da                     add edx, ebx
0048ab36  8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab39  e86a160000               call 0x48c1a8
0048ab3e  ebbf                     jmp 0x48aaff
0048ab40  8b16                     mov edx, dword ptr [esi]
0048ab42  8b4708                   mov eax, dword ptr [edi + 8]
0048ab45  e8ed150000               call 0x48c137
0048ab4a  89c8                     mov eax, ecx
0048ab4c  8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab4f  8b5708                   mov edx, dword ptr [edi + 8]
0048ab52  e819150000               call 0x48c070
0048ab57  eba6                     jmp 0x48aaff
0048ab59  8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab5c  31db                     xor ebx, ebx
0048ab5e  31d2                     xor edx, edx
0048ab60  31c0                     xor eax, eax
0048ab62  c1e102                   shl ecx, 2
0048ab65  8a5e09                   mov bl, byte ptr [esi + 9]
0048ab68  668b560a                 mov dx, word ptr [esi + 0xa]
0048ab6c  8a4608                   mov al, byte ptr [esi + 8]
0048ab6f  e83d0c0000               call 0x48b7b1
0048ab74  89c5                     mov ebp, eax
0048ab76  85c0                     test eax, eax
0048ab78  7487                     je 0x48ab01
0048ab7a  837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab7e  7507                     jne 0x48ab87
0048ab80  8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab83  0316                     add edx, dword ptr [esi]
0048ab85  eb17                     jmp 0x48ab9e
0048ab87  8b16                     mov edx, dword ptr [esi]
0048ab89  8b4708                   mov eax, dword ptr [edi + 8]
0048ab8c  e8a6150000               call 0x48c137
0048ab91  8b5604                   mov edx, dword ptr [esi + 4]
0048ab94  8b4708                   mov eax, dword ptr [edi + 8]
0048ab97  e8a5150000               call 0x48c141
0048ab9c  89c2                     mov edx, eax
0048ab9e  31c0                     xor eax, eax
0048aba0  8b5e04                   mov ebx, dword ptr [esi + 4]
0048aba3  8a4608                   mov al, byte ptr [esi + 8]
0048aba6  31c9                     xor ecx, ecx
0048aba8  50                       push eax
0048aba9  668b4e0e                 mov cx, word ptr [esi + 0xe]
0048abad  89e8                     mov eax, ebp
0048abaf  e808150000               call 0x48c0bc
0048abb4  e946ffffff               jmp 0x48aaff
; PSB_FindFirstFreePlace
0048abb9  53                       push ebx
0048abba  52                       push edx
0048abbb  8b15608f4900             mov edx, dword ptr [0x498f60]
0048abc1  83fa09                   cmp edx, 9
0048abc4  7c08                     jl 0x48abce
0048abc6  b8ffffffff               mov eax, 0xffffffff
0048abcb  5a                       pop edx
0048abcc  5b                       pop ebx
0048abcd  c3                       ret
0048abce  8d5a01                   lea ebx, [edx + 1]
0048abd1  891d608f4900             mov dword ptr [0x498f60], ebx
0048abd7  89d8                     mov eax, ebx
0048abd9  5a                       pop edx
0048abda  5b                       pop ebx
0048abdb  c3                       ret
; PSB_ReplaceLastSoundInFreePlace
0048abdc  53                       push ebx
0048abdd  52                       push edx
0048abde  56                       push esi
0048abdf  8b15608f4900             mov edx, dword ptr [0x498f60]
0048abe5  85d2                     test edx, edx
0048abe7  7d06                     jge 0x48abef
0048abe9  31c0                     xor eax, eax
0048abeb  5e                       pop esi
0048abec  5a                       pop edx
0048abed  5b                       pop ebx
0048abee  c3                       ret
0048abef  bb1c215200               mov ebx, 0x52211c
0048abf4  c1e203                   shl edx, 3
0048abf7  01d3                     add ebx, edx
0048abf9  39d8                     cmp eax, ebx
0048abfb  750f                     jne 0x48ac0c
0048abfd  b801000000               mov eax, 1
0048ac02  2905608f4900             sub dword ptr [0x498f60], eax
0048ac08  5e                       pop esi
0048ac09  5a                       pop edx
0048ac0a  5b                       pop ebx
0048ac0b  c3                       ret
0048ac0c  8b921c215200             mov edx, dword ptr [edx + 0x52211c]
0048ac12  8910                     mov dword ptr [eax], edx
0048ac14  8b15608f4900             mov edx, dword ptr [0x498f60]
0048ac1a  8b14d520215200           mov edx, dword ptr [edx*8 + 0x522120]
0048ac21  895004                   mov dword ptr [eax + 4], edx
0048ac24  894220                   mov dword ptr [edx + 0x20], eax
0048ac27  a1608f4900               mov eax, dword ptr [0x498f60]
0048ac2c  31db                     xor ebx, ebx
0048ac2e  891cc51c215200           mov dword ptr [eax*8 + 0x52211c], ebx
0048ac35  8b35608f4900             mov esi, dword ptr [0x498f60]
0048ac3b  891cc520215200           mov dword ptr [eax*8 + 0x522120], ebx
0048ac42  b801000000               mov eax, 1
0048ac47  29c6                     sub esi, eax
0048ac49  8935608f4900             mov dword ptr [0x498f60], esi
0048ac4f  5e                       pop esi
0048ac50  5a                       pop edx
0048ac51  5b                       pop ebx
0048ac52  c3                       ret
; PSB_DestroyPhyBuff
0048ac53  52                       push edx
0048ac54  89c2                     mov edx, eax
0048ac56  8b00                     mov eax, dword ptr [eax]
0048ac58  e833120000               call 0x48be90
0048ac5d  85c0                     test eax, eax
0048ac5f  7407                     je 0x48ac68
0048ac61  8b02                     mov eax, dword ptr [edx]
0048ac63  e80c130000               call 0x48bf74
0048ac68  89d0                     mov eax, edx
0048ac6a  e8250b0000               call 0x48b794
0048ac6f  c7420400000000           mov dword ptr [edx + 4], 0
0048ac76  5a                       pop edx
0048ac77  c3                       ret
; PSB_CreatePhySound
0048ac78  53                       push ebx
0048ac79  51                       push ecx
0048ac7a  52                       push edx
0048ac7b  56                       push esi
0048ac7c  89c3                     mov ebx, eax
0048ac7e  8b15608f4900             mov edx, dword ptr [0x498f60]
0048ac84  83fa09                   cmp edx, 9
0048ac87  7c07                     jl 0x48ac90
0048ac89  b9ffffffff               mov ecx, 0xffffffff
0048ac8e  eb09                     jmp 0x48ac99
0048ac90  8d4a01                   lea ecx, [edx + 1]
0048ac93  890d608f4900             mov dword ptr [0x498f60], ecx
0048ac99  83f9ff                   cmp ecx, -1
0048ac9c  7507                     jne 0x48aca5
0048ac9e  31c0                     xor eax, eax
0048aca0  5e                       pop esi
0048aca1  5a                       pop edx
0048aca2  59                       pop ecx
0048aca3  5b                       pop ebx
0048aca4  c3                       ret
0048aca5  8b5304                   mov edx, dword ptr [ebx + 4]
0048aca8  8b431c                   mov eax, dword ptr [ebx + 0x1c]
0048acab  e824feffff               call 0x48aad4
0048acb0  89c2                     mov edx, eax
0048acb2  89c8                     mov eax, ecx
0048acb4  c1e003                   shl eax, 3
0048acb7  89d6                     mov esi, edx
0048acb9  89901c215200             mov dword ptr [eax + 0x52211c], edx
0048acbf  85f6                     test esi, esi
0048acc1  74db                     je 0x48ac9e
0048acc3  899820215200             mov dword ptr [eax + 0x522120], ebx
0048acc9  051c215200               add eax, 0x52211c
0048acce  5e                       pop esi
0048accf  5a                       pop edx
0048acd0  59                       pop ecx
0048acd1  5b                       pop ebx
0048acd2  c3                       ret
; PSB_IsThisSoundLoaded
0048acd3  53                       push ebx
0048acd4  51                       push ecx
0048acd5  56                       push esi
0048acd6  89c1                     mov ecx, eax
0048acd8  89d6                     mov esi, edx
0048acda  8b1d608f4900             mov ebx, dword ptr [0x498f60]
0048ace0  31c0                     xor eax, eax
0048ace2  c1e303                   shl ebx, 3
0048ace5  eb03                     jmp 0x48acea
0048ace7  83c008                   add eax, 8
0048acea  39d8                     cmp eax, ebx
0048acec  7f18                     jg 0x48ad06
0048acee  8b9020215200             mov edx, dword ptr [eax + 0x522120]
0048acf4  3b0a                     cmp ecx, dword ptr [edx]
0048acf6  75ef                     jne 0x48ace7
0048acf8  3b7204                   cmp esi, dword ptr [edx + 4]
0048acfb  75ea                     jne 0x48ace7
0048acfd  051c215200               add eax, 0x52211c
0048ad02  5e                       pop esi
0048ad03  59                       pop ecx
0048ad04  5b                       pop ebx
0048ad05  c3                       ret
0048ad06  31c0                     xor eax, eax
0048ad08  5e                       pop esi
0048ad09  59                       pop ecx
0048ad0a  5b                       pop ebx
0048ad0b  c3                       ret
; PSB_TranfertLogicalSoundInPhysicalTable
0048ad0c  53                       push ebx
0048ad0d  51                       push ecx
0048ad0e  89d3                     mov ebx, edx
0048ad10  8b5220                   mov edx, dword ptr [edx + 0x20]
0048ad13  8b0a                     mov ecx, dword ptr [edx]
0048ad15  8908                     mov dword ptr [eax], ecx
0048ad17  895804                   mov dword ptr [eax + 4], ebx
0048ad1a  c70200000000             mov dword ptr [edx], 0
0048ad20  c7420400000000           mov dword ptr [edx + 4], 0
0048ad27  59                       pop ecx
0048ad28  5b                       pop ebx
0048ad29  c3                       ret
; PSB_IsFullListe
0048ad2a  833d608f490009           cmp dword ptr [0x498f60], 9
0048ad31  0f9dc0                   setge al
0048ad34  25ff000000               and eax, 0xff
0048ad39  c3                       ret
; LSB_ReplaceLastSoundInFreePlace
0048ad3c  53                       push ebx
0048ad3d  52                       push edx
0048ad3e  56                       push esi
0048ad3f  8b15648f4900             mov edx, dword ptr [0x498f64]
0048ad45  85d2                     test edx, edx
0048ad47  7d06                     jge 0x48ad4f
0048ad49  31c0                     xor eax, eax
0048ad4b  5e                       pop esi
0048ad4c  5a                       pop edx
0048ad4d  5b                       pop ebx
0048ad4e  c3                       ret
0048ad4f  bb6c215200               mov ebx, 0x52216c
0048ad54  c1e203                   shl edx, 3
0048ad57  01d3                     add ebx, edx
0048ad59  39d8                     cmp eax, ebx
0048ad5b  750f                     jne 0x48ad6c
0048ad5d  b801000000               mov eax, 1
0048ad62  2905648f4900             sub dword ptr [0x498f64], eax
0048ad68  5e                       pop esi
0048ad69  5a                       pop edx
0048ad6a  5b                       pop ebx
0048ad6b  c3                       ret
0048ad6c  8b926c215200             mov edx, dword ptr [edx + 0x52216c]
0048ad72  8910                     mov dword ptr [eax], edx
0048ad74  8b15648f4900             mov edx, dword ptr [0x498f64]
0048ad7a  8b14d570215200           mov edx, dword ptr [edx*8 + 0x522170]
0048ad81  895004                   mov dword ptr [eax + 4], edx
0048ad84  894220                   mov dword ptr [edx + 0x20], eax
0048ad87  a1648f4900               mov eax, dword ptr [0x498f64]
0048ad8c  31db                     xor ebx, ebx
0048ad8e  891cc56c215200           mov dword ptr [eax*8 + 0x52216c], ebx
0048ad95  8b35648f4900             mov esi, dword ptr [0x498f64]
0048ad9b  891cc570215200           mov dword ptr [eax*8 + 0x522170], ebx
0048ada2  b801000000               mov eax, 1
0048ada7  29c6                     sub esi, eax
0048ada9  8935648f4900             mov dword ptr [0x498f64], esi
0048adaf  5e                       pop esi
0048adb0  5a                       pop edx
0048adb1  5b                       pop ebx
0048adb2  c3                       ret
; LSB_DestroyLogBuff
0048adb3  53                       push ebx
0048adb4  51                       push ecx
0048adb5  52                       push edx
0048adb6  57                       push edi
0048adb7  89c2                     mov edx, eax
0048adb9  8b00                     mov eax, dword ptr [eax]
0048adbb  e8d0100000               call 0x48be90
0048adc0  85c0                     test eax, eax
0048adc2  7407                     je 0x48adcb
0048adc4  8b02                     mov eax, dword ptr [edx]
0048adc6  e8a9110000               call 0x48bf74
0048adcb  89d0                     mov eax, edx
0048adcd  e8c2090000               call 0x48b794
0048add2  c7420400000000           mov dword ptr [edx + 4], 0
0048add9  8b1d648f4900             mov ebx, dword ptr [0x498f64]
0048addf  85db                     test ebx, ebx
0048ade1  7c54                     jl 0x48ae37
0048ade3  89d8                     mov eax, ebx
0048ade5  bb6c215200               mov ebx, 0x52216c
0048adea  c1e003                   shl eax, 3
0048aded  01c3                     add ebx, eax
0048adef  39da                     cmp edx, ebx
0048adf1  750b                     jne 0x48adfe
0048adf3  ff0d648f4900             dec dword ptr [0x498f64]
0048adf9  5f                       pop edi
0048adfa  5a                       pop edx
0048adfb  59                       pop ecx
0048adfc  5b                       pop ebx
0048adfd  c3                       ret
0048adfe  8b806c215200             mov eax, dword ptr [eax + 0x52216c]
0048ae04  8902                     mov dword ptr [edx], eax
0048ae06  a1648f4900               mov eax, dword ptr [0x498f64]
0048ae0b  8b04c570215200           mov eax, dword ptr [eax*8 + 0x522170]
0048ae12  894204                   mov dword ptr [edx + 4], eax
0048ae15  895020                   mov dword ptr [eax + 0x20], edx
0048ae18  8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae1e  31c9                     xor ecx, ecx
0048ae20  890cd56c215200           mov dword ptr [edx*8 + 0x52216c], ecx
0048ae27  8d7aff                   lea edi, [edx - 1]
0048ae2a  890cd570215200           mov dword ptr [edx*8 + 0x522170], ecx
0048ae31  893d648f4900             mov dword ptr [0x498f64], edi
0048ae37  5f                       pop edi
0048ae38  5a                       pop edx
0048ae39  59                       pop ecx
0048ae3a  5b                       pop ebx
0048ae3b  c3                       ret
; LSB_FindFirstFreePlace
0048ae3c  53                       push ebx
0048ae3d  52                       push edx
0048ae3e  8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae44  83fa09                   cmp edx, 9
0048ae47  7c08                     jl 0x48ae51
0048ae49  b8ffffffff               mov eax, 0xffffffff
0048ae4e  5a                       pop edx
0048ae4f  5b                       pop ebx
0048ae50  c3                       ret
0048ae51  8d5a01                   lea ebx, [edx + 1]
0048ae54  891d648f4900             mov dword ptr [0x498f64], ebx
0048ae5a  89d8                     mov eax, ebx
0048ae5c  5a                       pop edx
0048ae5d  5b                       pop ebx
0048ae5e  c3                       ret
; LSB_CreateLogicalSound
0048ae5f  53                       push ebx
0048ae60  51                       push ecx
0048ae61  56                       push esi
0048ae62  89d1                     mov ecx, edx
0048ae64  8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae6a  83fa09                   cmp edx, 9
0048ae6d  7c07                     jl 0x48ae76
0048ae6f  baffffffff               mov edx, 0xffffffff
0048ae74  eb0b                     jmp 0x48ae81
0048ae76  8d5a01                   lea ebx, [edx + 1]
0048ae79  891d648f4900             mov dword ptr [0x498f64], ebx
0048ae7f  89da                     mov edx, ebx
0048ae81  83faff                   cmp edx, -1
0048ae84  7506                     jne 0x48ae8c
0048ae86  31c0                     xor eax, eax
0048ae88  5e                       pop esi
0048ae89  59                       pop ecx
0048ae8a  5b                       pop ebx
0048ae8b  c3                       ret
0048ae8c  e828110000               call 0x48bfb9
0048ae91  89c3                     mov ebx, eax
0048ae93  89d0                     mov eax, edx
0048ae95  c1e003                   shl eax, 3
0048ae98  89de                     mov esi, ebx
0048ae9a  89986c215200             mov dword ptr [eax + 0x52216c], ebx
0048aea0  85f6                     test esi, esi
0048aea2  74e2                     je 0x48ae86
0048aea4  898870215200             mov dword ptr [eax + 0x522170], ecx
0048aeaa  056c215200               add eax, 0x52216c
0048aeaf  5e                       pop esi
0048aeb0  59                       pop ecx
0048aeb1  5b                       pop ebx
0048aeb2  c3                       ret
; LSB_IsThisSoundPresent
0048aeb3  53                       push ebx
0048aeb4  51                       push ecx
0048aeb5  56                       push esi
0048aeb6  89c1                     mov ecx, eax
0048aeb8  89d6                     mov esi, edx
0048aeba  8b1d648f4900             mov ebx, dword ptr [0x498f64]
0048aec0  31c0                     xor eax, eax
0048aec2  c1e303                   shl ebx, 3
0048aec5  eb03                     jmp 0x48aeca
0048aec7  83c008                   add eax, 8
0048aeca  39d8                     cmp eax, ebx
0048aecc  7f11                     jg 0x48aedf
0048aece  8b9070215200             mov edx, dword ptr [eax + 0x522170]
0048aed4  3b0a                     cmp ecx, dword ptr [edx]
0048aed6  75ef                     jne 0x48aec7
0048aed8  3b7204                   cmp esi, dword ptr [edx + 4]
0048aedb  75ea                     jne 0x48aec7
0048aedd  eb02                     jmp 0x48aee1
0048aedf  31d2                     xor edx, edx
0048aee1  89d0                     mov eax, edx
0048aee3  5e                       pop esi
0048aee4  59                       pop ecx
0048aee5  5b                       pop ebx
0048aee6  c3                       ret
; LSB_IsFullListe
0048aee7  833d648f490009           cmp dword ptr [0x498f64], 9
0048aeee  0f9dc0                   setge al
0048aef1  25ff000000               and eax, 0xff
0048aef6  c3                       ret
; WaitSnd_GetFirstFreePlace
0048aef8  53                       push ebx
0048aef9  52                       push edx
0048aefa  8b15688f4900             mov edx, dword ptr [0x498f68]
0048af00  83fa46                   cmp edx, 0x46
0048af03  7508                     jne 0x48af0d
0048af05  b8ffffffff               mov eax, 0xffffffff
0048af0a  5a                       pop edx
0048af0b  5b                       pop ebx
0048af0c  c3                       ret
0048af0d  8d5a01                   lea ebx, [edx + 1]
0048af10  891d688f4900             mov dword ptr [0x498f68], ebx
0048af16  89d8                     mov eax, ebx
0048af18  5a                       pop edx
0048af19  5b                       pop ebx
0048af1a  c3                       ret
; WaitSnd_Compact
0048af1b  53                       push ebx
0048af1c  51                       push ecx
0048af1d  56                       push esi
0048af1e  57                       push edi
0048af1f  55                       push ebp
0048af20  89c3                     mov ebx, eax
0048af22  8b4028                   mov eax, dword ptr [eax + 0x28]
0048af25  8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048af2b  8b28                     mov ebp, dword ptr [eax]
0048af2d  83f913                   cmp ecx, 0x13
0048af30  7507                     jne 0x48af39
0048af32  31c0                     xor eax, eax
0048af34  e991000000               jmp 0x48afca
0048af39  85d2                     test edx, edx
0048af3b  7406                     je 0x48af43
0048af3d  c700ffffffff             mov dword ptr [eax], 0xffffffff
0048af43  8b15688f4900             mov edx, dword ptr [0x498f68]
0048af49  89d0                     mov eax, edx
0048af4b  c1e002                   shl eax, 2
0048af4e  29d0                     sub eax, edx
0048af50  c1e002                   shl eax, 2
0048af53  29d0                     sub eax, edx
0048af55  be7c135200               mov esi, 0x52137c
0048af5a  c1e002                   shl eax, 2
0048af5d  01c6                     add esi, eax
0048af5f  39de                     cmp esi, ebx
0048af61  751d                     jne 0x48af80
0048af63  30f6                     xor dh, dh
0048af65  8b3d688f4900             mov edi, dword ptr [0x498f68]
0048af6b  88b084135200             mov byte ptr [eax + 0x521384], dh
0048af71  b801000000               mov eax, 1
0048af76  29c7                     sub edi, eax
0048af78  893d688f4900             mov dword ptr [0x498f68], edi
0048af7e  eb4a                     jmp 0x48afca
0048af80  b92c000000               mov ecx, 0x2c
0048af85  89df                     mov edi, ebx
0048af87  57                       push edi
0048af88  89c8                     mov eax, ecx
0048af8a  c1e902                   shr ecx, 2
0048af8d  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048af8f  8ac8                     mov cl, al
0048af91  80e103                   and cl, 3
0048af94  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048af96  5f                       pop edi
0048af97  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048af9a  8928                     mov dword ptr [eax], ebp
0048af9c  8b15688f4900             mov edx, dword ptr [0x498f68]
0048afa2  89d0                     mov eax, edx
0048afa4  c1e002                   shl eax, 2
0048afa7  29d0                     sub eax, edx
0048afa9  c1e002                   shl eax, 2
0048afac  29d0                     sub eax, edx
0048afae  30d2                     xor dl, dl
0048afb0  8b35688f4900             mov esi, dword ptr [0x498f68]
0048afb6  88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048afbd  b801000000               mov eax, 1
0048afc2  29c6                     sub esi, eax
0048afc4  8935688f4900             mov dword ptr [0x498f68], esi
0048afca  5d                       pop ebp
0048afcb  5f                       pop edi
0048afcc  5e                       pop esi
0048afcd  59                       pop ecx
0048afce  5b                       pop ebx
0048afcf  c3                       ret
; WaitSnd_SorryGiveBackOnePlace
0048afd0  53                       push ebx
0048afd1  52                       push edx
0048afd2  8b15688f4900             mov edx, dword ptr [0x498f68]
0048afd8  83fa13                   cmp edx, 0x13
0048afdb  7409                     je 0x48afe6
0048afdd  8d5aff                   lea ebx, [edx - 1]
0048afe0  891d688f4900             mov dword ptr [0x498f68], ebx
0048afe6  5a                       pop edx
0048afe7  5b                       pop ebx
0048afe8  c3                       ret
; WaitSnd_GetMaxIndice
0048afe9  a1688f4900               mov eax, dword ptr [0x498f68]
0048afee  c3                       ret
; WaitSnd_FindPlace
0048afef  53                       push ebx
0048aff0  52                       push edx
0048aff1  31d2                     xor edx, edx
0048aff3  31c0                     xor eax, eax
0048aff5  eb04                     jmp 0x48affb
0048aff7  83c02c                   add eax, 0x2c
0048affa  42                       inc edx
0048affb  3d70030000               cmp eax, 0x370
0048b000  7d11                     jge 0x48b013
0048b002  31db                     xor ebx, ebx
0048b004  8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048b00a  85db                     test ebx, ebx
0048b00c  75e9                     jne 0x48aff7
0048b00e  89d0                     mov eax, edx
0048b010  5a                       pop edx
0048b011  5b                       pop ebx
0048b012  c3                       ret
0048b013  b8ffffffff               mov eax, 0xffffffff
0048b018  5a                       pop edx
0048b019  5b                       pop ebx
0048b01a  c3                       ret
; WaitSnd_TransferPlayingSoundToWaitingSound
0048b01b  53                       push ebx
0048b01c  51                       push ecx
0048b01d  52                       push edx
0048b01e  56                       push esi
0048b01f  57                       push edi
0048b020  55                       push ebp
0048b021  8b15688f4900             mov edx, dword ptr [0x498f68]
0048b027  83fa46                   cmp edx, 0x46
0048b02a  7507                     jne 0x48b033
0048b02c  bdffffffff               mov ebp, 0xffffffff
0048b031  eb0b                     jmp 0x48b03e
0048b033  8d5a01                   lea ebx, [edx + 1]
0048b036  891d688f4900             mov dword ptr [0x498f68], ebx
0048b03c  89dd                     mov ebp, ebx
0048b03e  83fdff                   cmp ebp, -1
0048b041  7507                     jne 0x48b04a
0048b043  31c0                     xor eax, eax
0048b045  e982000000               jmp 0x48b0cc
0048b04a  be7c135200               mov esi, 0x52137c
0048b04f  bf7c135200               mov edi, 0x52137c
0048b054  b92c000000               mov ecx, 0x2c
0048b059  89c3                     mov ebx, eax
0048b05b  89ea                     mov edx, ebp
0048b05d  c1e302                   shl ebx, 2
0048b060  c1e202                   shl edx, 2
0048b063  29c3                     sub ebx, eax
0048b065  29ea                     sub edx, ebp
0048b067  c1e302                   shl ebx, 2
0048b06a  c1e202                   shl edx, 2
0048b06d  29c3                     sub ebx, eax
0048b06f  29ea                     sub edx, ebp
0048b071  c1e302                   shl ebx, 2
0048b074  c1e202                   shl edx, 2
0048b077  01de                     add esi, ebx
0048b079  01d7                     add edi, edx
0048b07b  57                       push edi
0048b07c  89c8                     mov eax, ecx
0048b07e  c1e902                   shr ecx, 2
0048b081  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b083  8ac8                     mov cl, al
0048b085  80e103                   and cl, 3
0048b088  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b08a  5f                       pop edi
0048b08b  c6828413520002           mov byte ptr [edx + 0x521384], 2
0048b092  31c9                     xor ecx, ecx
0048b094  8b82a4135200             mov eax, dword ptr [edx + 0x5213a4]
0048b09a  898a9c135200             mov dword ptr [edx + 0x52139c], ecx
0048b0a0  8928                     mov dword ptr [eax], ebp
0048b0a2  30d2                     xor dl, dl
0048b0a4  8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048b0aa  8bb3a0135200             mov esi, dword ptr [ebx + 0x5213a0]
0048b0b0  889384135200             mov byte ptr [ebx + 0x521384], dl
0048b0b6  83fe01                   cmp esi, 1
0048b0b9  7507                     jne 0x48b0c2
0048b0bb  e8f3fcffff               call 0x48adb3
0048b0c0  eb05                     jmp 0x48b0c7
0048b0c2  e88cfbffff               call 0x48ac53
0048b0c7  b801000000               mov eax, 1
0048b0cc  5d                       pop ebp
0048b0cd  5f                       pop edi
0048b0ce  5e                       pop esi
0048b0cf  5a                       pop edx
0048b0d0  59                       pop ecx
0048b0d1  5b                       pop ebx
0048b0d2  c3                       ret
; WaitSnd_TransferALLPlayingSoundToWaitingSound
0048b0d3  53                       push ebx
0048b0d4  51                       push ecx
0048b0d5  56                       push esi
0048b0d6  57                       push edi
0048b0d7  89c7                     mov edi, eax
0048b0d9  89d6                     mov esi, edx
0048b0db  31c9                     xor ecx, ecx
0048b0dd  31db                     xor ebx, ebx
0048b0df  31d2                     xor edx, edx
0048b0e1  eb09                     jmp 0x48b0ec
0048b0e3  43                       inc ebx
0048b0e4  83c22c                   add edx, 0x2c
0048b0e7  83fb14                   cmp ebx, 0x14
0048b0ea  7d2a                     jge 0x48b116
0048b0ec  31c0                     xor eax, eax
0048b0ee  8a8284135200             mov al, byte ptr [edx + 0x521384]
0048b0f4  85c0                     test eax, eax
0048b0f6  74eb                     je 0x48b0e3
0048b0f8  3bba7c135200             cmp edi, dword ptr [edx + 0x52137c]
0048b0fe  75e3                     jne 0x48b0e3
0048b100  3bb280135200             cmp esi, dword ptr [edx + 0x521380]
0048b106  75db                     jne 0x48b0e3
0048b108  89d8                     mov eax, ebx
0048b10a  b901000000               mov ecx, 1
0048b10f  e807ffffff               call 0x48b01b
0048b114  ebcd                     jmp 0x48b0e3
0048b116  89c8                     mov eax, ecx
0048b118  5f                       pop edi
0048b119  5e                       pop esi
0048b11a  59                       pop ecx
0048b11b  5b                       pop ebx
0048b11c  c3                       ret
; WaitSnd_DestroyWaitingSound
0048b11d  53                       push ebx
0048b11e  51                       push ecx
0048b11f  52                       push edx
0048b120  56                       push esi
0048b121  57                       push edi
0048b122  55                       push ebp
0048b123  89c3                     mov ebx, eax
0048b125  c1e002                   shl eax, 2
0048b128  29d8                     sub eax, ebx
0048b12a  8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b130  c1e002                   shl eax, 2
0048b133  8b15688f4900             mov edx, dword ptr [0x498f68]
0048b139  29d8                     sub eax, ebx
0048b13b  49                       dec ecx
0048b13c  c1e002                   shl eax, 2
0048b13f  39d3                     cmp ebx, edx
0048b141  7515                     jne 0x48b158
0048b143  30d3                     xor bl, dl
0048b145  890d688f4900             mov dword ptr [0x498f68], ecx
0048b14b  889884135200             mov byte ptr [eax + 0x521384], bl
0048b151  31c0                     xor eax, eax
0048b153  e974ffffff               jmp 0x48b0cc
0048b158  ba7c135200               mov edx, 0x52137c
0048b15d  01c2                     add edx, eax
0048b15f  8b4228                   mov eax, dword ptr [edx + 0x28]
0048b162  8b1d688f4900             mov ebx, dword ptr [0x498f68]
0048b168  8b28                     mov ebp, dword ptr [eax]
0048b16a  83fb13                   cmp ebx, 0x13
0048b16d  0f8454ffffff             je 0x48b0c7
0048b173  89d8                     mov eax, ebx
0048b175  c1e002                   shl eax, 2
0048b178  29d8                     sub eax, ebx
0048b17a  c1e002                   shl eax, 2
0048b17d  29d8                     sub eax, ebx
0048b17f  be7c135200               mov esi, 0x52137c
0048b184  c1e002                   shl eax, 2
0048b187  01c6                     add esi, eax
0048b189  39d6                     cmp esi, edx
0048b18b  7513                     jne 0x48b1a0
0048b18d  30f6                     xor dh, dh
0048b18f  890d688f4900             mov dword ptr [0x498f68], ecx
0048b195  88b084135200             mov byte ptr [eax + 0x521384], dh
0048b19b  e927ffffff               jmp 0x48b0c7
0048b1a0  b92c000000               mov ecx, 0x2c
0048b1a5  89d7                     mov edi, edx
0048b1a7  57                       push edi
0048b1a8  89c8                     mov eax, ecx
0048b1aa  c1e902                   shr ecx, 2
0048b1ad  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b1af  8ac8                     mov cl, al
0048b1b1  80e103                   and cl, 3
0048b1b4  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b1b6  5f                       pop edi
0048b1b7  8b4228                   mov eax, dword ptr [edx + 0x28]
0048b1ba  8928                     mov dword ptr [eax], ebp
0048b1bc  8b15688f4900             mov edx, dword ptr [0x498f68]
0048b1c2  89d0                     mov eax, edx
0048b1c4  c1e002                   shl eax, 2
0048b1c7  29d0                     sub eax, edx
0048b1c9  8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b1cf  c1e002                   shl eax, 2
0048b1d2  49                       dec ecx
0048b1d3  29d0                     sub eax, edx
0048b1d5  30d2                     xor dl, dl
0048b1d7  890d688f4900             mov dword ptr [0x498f68], ecx
0048b1dd  88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048b1e4  e9defeffff               jmp 0x48b0c7
; WaitSnd_TransferWaitingSoundToPlayingSound
0048b1e9  53                       push ebx
0048b1ea  51                       push ecx
0048b1eb  52                       push edx
0048b1ec  56                       push esi
0048b1ed  57                       push edi
0048b1ee  55                       push ebp
0048b1ef  89c6                     mov esi, eax
0048b1f1  31d2                     xor edx, edx
0048b1f3  31c0                     xor eax, eax
0048b1f5  eb04                     jmp 0x48b1fb
0048b1f7  83c02c                   add eax, 0x2c
0048b1fa  42                       inc edx
0048b1fb  3d70030000               cmp eax, 0x370
0048b200  7d10                     jge 0x48b212
0048b202  31db                     xor ebx, ebx
0048b204  8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048b20a  85db                     test ebx, ebx
0048b20c  75e9                     jne 0x48b1f7
0048b20e  89d5                     mov ebp, edx
0048b210  eb05                     jmp 0x48b217
0048b212  bdffffffff               mov ebp, 0xffffffff
0048b217  83fdff                   cmp ebp, -1
0048b21a  7507                     jne 0x48b223
0048b21c  31c0                     xor eax, eax
0048b21e  e9a9feffff               jmp 0x48b0cc
0048b223  ba7c135200               mov edx, 0x52137c
0048b228  89f0                     mov eax, esi
0048b22a  89eb                     mov ebx, ebp
0048b22c  c1e002                   shl eax, 2
0048b22f  c1e302                   shl ebx, 2
0048b232  29f0                     sub eax, esi
0048b234  29eb                     sub ebx, ebp
0048b236  c1e002                   shl eax, 2
0048b239  c1e302                   shl ebx, 2
0048b23c  29f0                     sub eax, esi
0048b23e  29eb                     sub ebx, ebp
0048b240  c1e002                   shl eax, 2
0048b243  c1e302                   shl ebx, 2
0048b246  01c2                     add edx, eax
0048b248  b87c135200               mov eax, 0x52137c
0048b24d  b92c000000               mov ecx, 0x2c
0048b252  01d8                     add eax, ebx
0048b254  89d6                     mov esi, edx
0048b256  89c7                     mov edi, eax
0048b258  57                       push edi
0048b259  89c8                     mov eax, ecx
0048b25b  c1e902                   shr ecx, 2
0048b25e  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b260  8ac8                     mov cl, al
0048b262  80e103                   and cl, 3
0048b265  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b267  5f                       pop edi
0048b268  8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048b26e  8928                     mov dword ptr [eax], ebp
0048b270  8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048b276  89fe                     mov esi, edi
0048b278  897004                   mov dword ptr [eax + 4], esi
0048b27b  c6838413520001           mov byte ptr [ebx + 0x521384], 1
0048b282  8b4228                   mov eax, dword ptr [edx + 0x28]
0048b285  8b1d688f4900             mov ebx, dword ptr [0x498f68]
0048b28b  8b28                     mov ebp, dword ptr [eax]
0048b28d  83fb13                   cmp ebx, 0x13
0048b290  748a                     je 0x48b21c
0048b292  89d8                     mov eax, ebx
0048b294  c1e002                   shl eax, 2
0048b297  29d8                     sub eax, ebx
0048b299  c1e002                   shl eax, 2
0048b29c  29d8                     sub eax, ebx
0048b29e  be7c135200               mov esi, 0x52137c
0048b2a3  c1e002                   shl eax, 2
0048b2a6  01c6                     add esi, eax
0048b2a8  39d6                     cmp esi, edx
0048b2aa  751c                     jne 0x48b2c8
0048b2ac  30f6                     xor dh, dh
0048b2ae  89de                     mov esi, ebx
0048b2b0  88b084135200             mov byte ptr [eax + 0x521384], dh
0048b2b6  b801000000               mov eax, 1
0048b2bb  29c6                     sub esi, eax
0048b2bd  8935688f4900             mov dword ptr [0x498f68], esi
0048b2c3  e904feffff               jmp 0x48b0cc
0048b2c8  b92c000000               mov ecx, 0x2c
0048b2cd  89d7                     mov edi, edx
0048b2cf  57                       push edi
0048b2d0  89c8                     mov eax, ecx
0048b2d2  c1e902                   shr ecx, 2
0048b2d5  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b2d7  8ac8                     mov cl, al
0048b2d9  80e103                   and cl, 3
0048b2dc  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b2de  5f                       pop edi
0048b2df  8b4228                   mov eax, dword ptr [edx + 0x28]
0048b2e2  8928                     mov dword ptr [eax], ebp
0048b2e4  8b15688f4900             mov edx, dword ptr [0x498f68]
0048b2ea  89d0                     mov eax, edx
0048b2ec  c1e002                   shl eax, 2
0048b2ef  29d0                     sub eax, edx
0048b2f1  c1e002                   shl eax, 2
0048b2f4  29d0                     sub eax, edx
0048b2f6  30d2                     xor dl, dl
0048b2f8  8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b2fe  88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048b305  b801000000               mov eax, 1
0048b30a  29c1                     sub ecx, eax
0048b30c  890d688f4900             mov dword ptr [0x498f68], ecx
0048b312  e9b5fdffff               jmp 0x48b0cc
; WaitSnd_Permute
0048b317  53                       push ebx
0048b318  51                       push ecx
0048b319  56                       push esi
0048b31a  57                       push edi
0048b31b  83ec2c                   sub esp, 0x2c
0048b31e  89c3                     mov ebx, eax
0048b320  b92c000000               mov ecx, 0x2c
0048b325  89e7                     mov edi, esp
0048b327  89c6                     mov esi, eax
0048b329  57                       push edi
0048b32a  89c8                     mov eax, ecx
0048b32c  c1e902                   shr ecx, 2
0048b32f  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b331  8ac8                     mov cl, al
0048b333  80e103                   and cl, 3
0048b336  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b338  5f                       pop edi
0048b339  b92c000000               mov ecx, 0x2c
0048b33e  89d6                     mov esi, edx
0048b340  89df                     mov edi, ebx
0048b342  57                       push edi
0048b343  89c8                     mov eax, ecx
0048b345  c1e902                   shr ecx, 2
0048b348  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b34a  8ac8                     mov cl, al
0048b34c  80e103                   and cl, 3
0048b34f  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b351  5f                       pop edi
0048b352  b92c000000               mov ecx, 0x2c
0048b357  89e6                     mov esi, esp
0048b359  89d7                     mov edi, edx
0048b35b  57                       push edi
0048b35c  89c8                     mov eax, ecx
0048b35e  c1e902                   shr ecx, 2
0048b361  f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b363  8ac8                     mov cl, al
0048b365  80e103                   and cl, 3
0048b368  f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b36a  5f                       pop edi
0048b36b  8b7228                   mov esi, dword ptr [edx + 0x28]
0048b36e  8b4328                   mov eax, dword ptr [ebx + 0x28]
0048b371  8b36                     mov esi, dword ptr [esi]
0048b373  8b38                     mov edi, dword ptr [eax]
0048b375  8930                     mov dword ptr [eax], esi
0048b377  8b4228                   mov eax, dword ptr [edx + 0x28]
0048b37a  8938                     mov dword ptr [eax], edi
0048b37c  8b7220                   mov esi, dword ptr [edx + 0x20]
0048b37f  8b4320                   mov eax, dword ptr [ebx + 0x20]
0048b382  897320                   mov dword ptr [ebx + 0x20], esi
0048b385  894220                   mov dword ptr [edx + 0x20], eax
0048b388  83c42c                   add esp, 0x2c
0048b38b  5f                       pop edi
0048b38c  5e                       pop esi
0048b38d  59                       pop ecx
0048b38e  5b                       pop ebx
; WaitSnd_Trier
0048b38f  c3                       ret
