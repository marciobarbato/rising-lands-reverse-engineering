; Intact executable SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Static evidence only, not translated sound semantics.
; MCICD_GetTrackStop
004679d0 53                       push ebx
004679d1 51                       push ecx
004679d2 52                       push edx
004679d3 83ec50                   sub esp, 0x50
004679d6 89c3                     mov ebx, eax
004679d8 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
004679df 7504                     jne 0x4679e5
004679e1 31c0                     xor eax, eax
004679e3 eb61                     jmp 0x467a46
004679e5 6a00                     push 0
004679e7 6a00                     push 0
004679e9 6a00                     push 0
004679eb 683c494900               push 0x49493c
004679f0 e829c00200               call 0x493a1e
004679f5 85c0                     test eax, eax
004679f7 75e8                     jne 0x4679e1
004679f9 53                       push ebx
004679fa 685a494900               push 0x49495a
004679ff 8d442408                 lea eax, [esp + 8]
00467a03 50                       push eax
00467a04 e8b2550200               call 0x48cfbb
00467a09 83c40c                   add esp, 0xc
00467a0c 6a00                     push 0
00467a0e 6a28                     push 0x28
00467a10 8d442430                 lea eax, [esp + 0x30]
00467a14 50                       push eax
00467a15 8d44240c                 lea eax, [esp + 0xc]
00467a19 50                       push eax
00467a1a e8ffbf0200               call 0x493a1e
00467a1f 85c0                     test eax, eax
00467a21 75be                     jne 0x4679e1
00467a23 50                       push eax
00467a24 50                       push eax
00467a25 50                       push eax
00467a26 687c494900               push 0x49497c
00467a2b e8eebf0200               call 0x493a1e
00467a30 85c0                     test eax, eax
00467a32 75ad                     jne 0x4679e1
00467a34 8d442428                 lea eax, [esp + 0x28]
00467a38 e8095a0200               call 0x48d446
00467a3d 89c3                     mov ebx, eax
00467a3f e8e0bf0200               call 0x493a24
00467a44 01d8                     add eax, ebx
00467a46 83c450                   add esp, 0x50
00467a49 5a                       pop edx
00467a4a 59                       pop ecx
00467a4b 5b                       pop ebx
00467a4c c3                       ret
; MCICD_Stop
00467a4d 51                       push ecx
00467a4e 52                       push edx
00467a4f 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
00467a56 7505                     jne 0x467a5d
00467a58 30c0                     xor al, al
00467a5a 5a                       pop edx
00467a5b 59                       pop ecx
00467a5c c3                       ret
00467a5d 803d282f4e0000           cmp byte ptr [0x4e2f28], 0
00467a64 74f2                     je 0x467a58
00467a66 30f6                     xor dh, dh
00467a68 8835282f4e00             mov byte ptr [0x4e2f28], dh
00467a6e 31d2                     xor edx, edx
00467a70 52                       push edx
00467a71 52                       push edx
00467a72 52                       push edx
00467a73 689c494900               push 0x49499c
00467a78 8915302f4e00             mov dword ptr [0x4e2f30], edx
00467a7e e89bbf0200               call 0x493a1e
00467a83 85c0                     test eax, eax
00467a85 75d1                     jne 0x467a58
00467a87 b001                     mov al, 1
00467a89 5a                       pop edx
00467a8a 59                       pop ecx
00467a8b c3                       ret
; MCICD_Play
00467a8c 53                       push ebx
00467a8d 51                       push ecx
00467a8e 83ec54                   sub esp, 0x54
00467a91 89c3                     mov ebx, eax
00467a93 88542450                 mov byte ptr [esp + 0x50], dl
00467a97 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
00467a9e 7504                     jne 0x467aa4
00467aa0 30c0                     xor al, al
00467aa2 eb4c                     jmp 0x467af0
00467aa4 89d8                     mov eax, ebx
00467aa6 e825ffffff               call 0x4679d0
00467aab 53                       push ebx
00467aac 68ac494900               push 0x4949ac
00467ab1 a3302f4e00               mov dword ptr [0x4e2f30], eax
00467ab6 8d442408                 lea eax, [esp + 8]
00467aba 50                       push eax
00467abb e8fb540200               call 0x48cfbb
00467ac0 83c40c                   add esp, 0xc
00467ac3 6a00                     push 0
00467ac5 6a00                     push 0
00467ac7 6a00                     push 0
00467ac9 8d44240c                 lea eax, [esp + 0xc]
00467acd 50                       push eax
00467ace e84bbf0200               call 0x493a1e
00467ad3 85c0                     test eax, eax
00467ad5 75c9                     jne 0x467aa0
00467ad7 8a442450                 mov al, byte ptr [esp + 0x50]
00467adb b201                     mov dl, 1
00467add 891ddc6f4900             mov dword ptr [0x496fdc], ebx
00467ae3 a22a2f4e00               mov byte ptr [0x4e2f2a], al
00467ae8 8815282f4e00             mov byte ptr [0x4e2f28], dl
00467aee 88d0                     mov al, dl
00467af0 83c454                   add esp, 0x54
00467af3 59                       pop ecx
00467af4 5b                       pop ebx
00467af5 c3                       ret
; MCICD_Init
00467af6 51                       push ecx
00467af7 52                       push edx
00467af8 83ec50                   sub esp, 0x50
00467afb 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
00467b02 7407                     je 0x467b0b
00467b04 30c0                     xor al, al
00467b06 e974000000               jmp 0x467b7f
00467b0b a191955000               mov eax, dword ptr [0x509591]
00467b10 c1f818                   sar eax, 0x18
00467b13 50                       push eax
00467b14 68bf494900               push 0x4949bf
00467b19 8d442408                 lea eax, [esp + 8]
00467b1d 50                       push eax
00467b1e e898540200               call 0x48cfbb
00467b23 83c40c                   add esp, 0xc
00467b26 6a00                     push 0
00467b28 6a00                     push 0
00467b2a 6a00                     push 0
00467b2c 8d44240c                 lea eax, [esp + 0xc]
00467b30 50                       push eax
00467b31 e8e8be0200               call 0x493a1e
00467b36 85c0                     test eax, eax
00467b38 75ca                     jne 0x467b04
00467b3a 50                       push eax
00467b3b 6a0c                     push 0xc
00467b3d 8d442408                 lea eax, [esp + 8]
00467b41 50                       push eax
00467b42 68e6494900               push 0x4949e6
00467b47 e8d2be0200               call 0x493a1e
00467b4c 85c0                     test eax, eax
00467b4e 75b4                     jne 0x467b04
00467b50 50                       push eax
00467b51 50                       push eax
00467b52 50                       push eax
00467b53 68094a4900               push 0x494a09
00467b58 e8c1be0200               call 0x493a1e
00467b5d 85c0                     test eax, eax
00467b5f 75a3                     jne 0x467b04
00467b61 89e0                     mov eax, esp
00467b63 b201                     mov dl, 1
00467b65 e8dc580200               call 0x48d446
00467b6a 8815292f4e00             mov byte ptr [0x4e2f29], dl
00467b70 30f6                     xor dh, dh
00467b72 a32c2f4e00               mov dword ptr [0x4e2f2c], eax
00467b77 8835282f4e00             mov byte ptr [0x4e2f28], dh
00467b7d 88d0                     mov al, dl
00467b7f 83c450                   add esp, 0x50
00467b82 5a                       pop edx
00467b83 59                       pop ecx
00467b84 c3                       ret
; MCICD_Free
00467b85 53                       push ebx
00467b86 51                       push ecx
00467b87 52                       push edx
00467b88 8a25292f4e00             mov ah, byte ptr [0x4e2f29]
00467b8e 84e4                     test ah, ah
00467b90 7506                     jne 0x467b98
00467b92 30c0                     xor al, al
00467b94 5a                       pop edx
00467b95 59                       pop ecx
00467b96 5b                       pop ebx
00467b97 c3                       ret
00467b98 7504                     jne 0x467b9e
00467b9a 30c0                     xor al, al
00467b9c eb2c                     jmp 0x467bca
00467b9e 803d282f4e0000           cmp byte ptr [0x4e2f28], 0
00467ba5 74f3                     je 0x467b9a
00467ba7 31d2                     xor edx, edx
00467ba9 52                       push edx
00467baa 52                       push edx
00467bab 52                       push edx
00467bac 30db                     xor bl, bl
00467bae 689c494900               push 0x49499c
00467bb3 881d282f4e00             mov byte ptr [0x4e2f28], bl
00467bb9 8915302f4e00             mov dword ptr [0x4e2f30], edx
00467bbf e85abe0200               call 0x493a1e
00467bc4 85c0                     test eax, eax
00467bc6 75d2                     jne 0x467b9a
00467bc8 b001                     mov al, 1
00467bca 84c0                     test al, al
00467bcc 741e                     je 0x467bec
00467bce 6a00                     push 0
00467bd0 6a00                     push 0
00467bd2 6a00                     push 0
00467bd4 68294a4900               push 0x494a29
00467bd9 e840be0200               call 0x493a1e
00467bde 85c0                     test eax, eax
00467be0 75b0                     jne 0x467b92
00467be2 30ff                     xor bh, bh
00467be4 b001                     mov al, 1
00467be6 883d292f4e00             mov byte ptr [0x4e2f29], bh
00467bec 5a                       pop edx
00467bed 59                       pop ecx
00467bee 5b                       pop ebx
00467bef c3                       ret
; MCICD_Manage
00467bf0 53                       push ebx
00467bf1 51                       push ecx
00467bf2 52                       push edx
00467bf3 83ec50                   sub esp, 0x50
00467bf6 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
00467bfd 0f8443feffff             je 0x467a46
00467c03 803d282f4e0000           cmp byte ptr [0x4e2f28], 0
00467c0a 0f8436feffff             je 0x467a46
00467c10 e80fbe0200               call 0x493a24
00467c15 3b05302f4e00             cmp eax, dword ptr [0x4e2f30]
00467c1b 0f8225feffff             jb 0x467a46
00467c21 803d292f4e0000           cmp byte ptr [0x4e2f29], 0
00467c28 7426                     je 0x467c50
00467c2a 803d282f4e0000           cmp byte ptr [0x4e2f28], 0
00467c31 741d                     je 0x467c50
00467c33 30ff                     xor bh, bh
00467c35 883d282f4e00             mov byte ptr [0x4e2f28], bh
00467c3b 31db                     xor ebx, ebx
00467c3d 53                       push ebx
00467c3e 53                       push ebx
00467c3f 53                       push ebx
00467c40 689c494900               push 0x49499c
00467c45 891d302f4e00             mov dword ptr [0x4e2f30], ebx
00467c4b e8cebd0200               call 0x493a1e
00467c50 803d2a2f4e0000           cmp byte ptr [0x4e2f2a], 0
00467c57 0f84e9fdffff             je 0x467a46
00467c5d 8a2d292f4e00             mov ch, byte ptr [0x4e2f29]
00467c63 8b1ddc6f4900             mov ebx, dword ptr [0x496fdc]
00467c69 84ed                     test ch, ch
00467c6b 0f84d5fdffff             je 0x467a46
00467c71 89d8                     mov eax, ebx
00467c73 e858fdffff               call 0x4679d0
00467c78 53                       push ebx
00467c79 68ac494900               push 0x4949ac
00467c7e a3302f4e00               mov dword ptr [0x4e2f30], eax
00467c83 8d442408                 lea eax, [esp + 8]
00467c87 50                       push eax
00467c88 e82e530200               call 0x48cfbb
00467c8d 83c40c                   add esp, 0xc
00467c90 6a00                     push 0
00467c92 6a00                     push 0
00467c94 6a00                     push 0
00467c96 8d44240c                 lea eax, [esp + 0xc]
00467c9a 50                       push eax
00467c9b e87ebd0200               call 0x493a1e
00467ca0 85c0                     test eax, eax
00467ca2 0f859efdffff             jne 0x467a46
00467ca8 b001                     mov al, 1
00467caa 891ddc6f4900             mov dword ptr [0x496fdc], ebx
00467cb0 a22a2f4e00               mov byte ptr [0x4e2f2a], al
00467cb5 a2282f4e00               mov byte ptr [0x4e2f28], al
00467cba e987fdffff               jmp 0x467a46
; HandlSnd_GetAverageVolume
00489dac 53                       push ebx
00489dad 52                       push edx
00489dae 8b501c                   mov edx, dword ptr [eax + 0x1c]
00489db1 8a520d                   mov dl, byte ptr [edx + 0xd]
00489db4 81e2ff000000             and edx, 0xff
00489dba 7505                     jne 0x489dc1
00489dbc ba00010000               mov edx, 0x100
00489dc1 8b5818                   mov ebx, dword ptr [eax + 0x18]
00489dc4 668b5b04                 mov bx, word ptr [ebx + 4]
00489dc8 81e3ffff0000             and ebx, 0xffff
00489dce 81fb00010000             cmp ebx, 0x100
00489dd4 7503                     jne 0x489dd9
00489dd6 895810                   mov dword ptr [eax + 0x10], ebx
00489dd9 8b4010                   mov eax, dword ptr [eax + 0x10]
00489ddc 0fafc2                   imul eax, edx
00489ddf 0faf05588f4900           imul eax, dword ptr [0x498f58]
00489de6 c1f814                   sar eax, 0x14
00489de9 8b0485148f4900           mov eax, dword ptr [eax*4 + 0x498f14]
00489df0 5a                       pop edx
00489df1 5b                       pop ebx
00489df2 c3                       ret
; DeleteHandle
00489df3 53                       push ebx
00489df4 52                       push edx
00489df5 8b5028                   mov edx, dword ptr [eax + 0x28]
00489df8 833aff                   cmp dword ptr [edx], -1
00489dfb 7505                     jne 0x489e02
00489dfd 31c0                     xor eax, eax
00489dff 5a                       pop edx
00489e00 5b                       pop ebx
00489e01 c3                       ret
00489e02 31db                     xor ebx, ebx
00489e04 8a5808                   mov bl, byte ptr [eax + 8]
00489e07 85db                     test ebx, ebx
00489e09 74f2                     je 0x489dfd
00489e0b 83fb02                   cmp ebx, 2
00489e0e 750c                     jne 0x489e1c
00489e10 ba01000000               mov edx, 1
00489e15 e801110000               call 0x48af1b
00489e1a eb11                     jmp 0x489e2d
00489e1c c702ffffffff             mov dword ptr [edx], 0xffffffff
00489e22 c6400800                 mov byte ptr [eax + 8], 0
00489e26 c7402000000000           mov dword ptr [eax + 0x20], 0
00489e2d b801000000               mov eax, 1
00489e32 5a                       pop edx
00489e33 5b                       pop ebx
00489e34 c3                       ret
; DestroyOnlySound
00489e35 53                       push ebx
00489e36 51                       push ecx
00489e37 52                       push edx
00489e38 56                       push esi
00489e39 89c2                     mov edx, eax
00489e3b 8b5820                   mov ebx, dword ptr [eax + 0x20]
00489e3e 85db                     test ebx, ebx
00489e40 746f                     je 0x489eb1
00489e42 8b03                     mov eax, dword ptr [ebx]
00489e44 e870200000               call 0x48beb9
00489e49 85c0                     test eax, eax
00489e4b 7507                     jne 0x489e54
00489e4d 8b03                     mov eax, dword ptr [ebx]
00489e4f e820210000               call 0x48bf74
00489e54 837a2401                 cmp dword ptr [edx + 0x24], 1
00489e58 7513                     jne 0x489e6d
00489e5a 89d8                     mov eax, ebx
00489e5c e8520f0000               call 0x48adb3
00489e61 c7422000000000           mov dword ptr [edx + 0x20], 0
00489e68 5e                       pop esi
00489e69 5a                       pop edx
00489e6a 59                       pop ecx
00489e6b 5b                       pop ebx
00489e6c c3                       ret
00489e6d 89d8                     mov eax, ebx
00489e6f e8df0d0000               call 0x48ac53
00489e74 8b4204                   mov eax, dword ptr [edx + 4]
00489e77 8b0a                     mov ecx, dword ptr [edx]
00489e79 89c2                     mov edx, eax
00489e7b 89c8                     mov eax, ecx
00489e7d e831100000               call 0x48aeb3
00489e82 89c1                     mov ecx, eax
00489e84 85c0                     test eax, eax
00489e86 7422                     je 0x489eaa
00489e88 89c2                     mov edx, eax
00489e8a 8b7020                   mov esi, dword ptr [eax + 0x20]
00489e8d 89d8                     mov eax, ebx
00489e8f e8780e0000               call 0x48ad0c
00489e94 894120                   mov dword ptr [ecx + 0x20], eax
00489e97 89f0                     mov eax, esi
00489e99 e89e0e0000               call 0x48ad3c
00489e9e c7412400000000           mov dword ptr [ecx + 0x24], 0
00489ea5 5e                       pop esi
00489ea6 5a                       pop edx
00489ea7 59                       pop ecx
00489ea8 5b                       pop ebx
00489ea9 c3                       ret
00489eaa 89d8                     mov eax, ebx
00489eac e82b0d0000               call 0x48abdc
00489eb1 5e                       pop esi
00489eb2 5a                       pop edx
00489eb3 59                       pop ecx
00489eb4 5b                       pop ebx
00489eb5 c3                       ret
; DestroyHandle
00489eb6 53                       push ebx
00489eb7 52                       push edx
00489eb8 89c3                     mov ebx, eax
00489eba 31c0                     xor eax, eax
00489ebc 8a4308                   mov al, byte ptr [ebx + 8]
00489ebf 83f801                   cmp eax, 1
00489ec2 7507                     jne 0x489ecb
00489ec4 89d8                     mov eax, ebx
00489ec6 e86affffff               call 0x489e35
00489ecb 8b4328                   mov eax, dword ptr [ebx + 0x28]
00489ece 8338ff                   cmp dword ptr [eax], -1
00489ed1 742e                     je 0x489f01
00489ed3 31d2                     xor edx, edx
00489ed5 8a5308                   mov dl, byte ptr [ebx + 8]
00489ed8 85d2                     test edx, edx
00489eda 7425                     je 0x489f01
00489edc 83fa02                   cmp edx, 2
00489edf 750f                     jne 0x489ef0
00489ee1 ba01000000               mov edx, 1
00489ee6 89d8                     mov eax, ebx
00489ee8 e82e100000               call 0x48af1b
00489eed 5a                       pop edx
00489eee 5b                       pop ebx
00489eef c3                       ret
00489ef0 c700ffffffff             mov dword ptr [eax], 0xffffffff
00489ef6 c6430800                 mov byte ptr [ebx + 8], 0
00489efa c7432000000000           mov dword ptr [ebx + 0x20], 0
00489f01 5a                       pop edx
00489f02 5b                       pop ebx
00489f03 c3                       ret
; HandleSnd_DestroyDictator
00489f04 53                       push ebx
00489f05 833d901f520000           cmp dword ptr [0x521f90], 0
00489f0c 7429                     je 0x489f37
00489f0e 31db                     xor ebx, ebx
00489f10 a1b41f5200               mov eax, dword ptr [0x521fb4]
00489f15 891d901f5200             mov dword ptr [0x521f90], ebx
00489f1b 8b00                     mov eax, dword ptr [eax]
00489f1d e852200000               call 0x48bf74
00489f22 a1b41f5200               mov eax, dword ptr [0x521fb4]
00489f27 e868180000               call 0x48b794
00489f2c a1bc1f5200               mov eax, dword ptr [0x521fbc]
00489f31 c700ffffffff             mov dword ptr [eax], 0xffffffff
00489f37 5b                       pop ebx
00489f38 c3                       ret
; HandleSnd_InitDictator
00489f39 53                       push ebx
00489f3a 52                       push edx
00489f3b ba3c534900               mov edx, 0x49533c
00489f40 b808000000               mov eax, 8
00489f45 e8ba220000               call 0x48c204
00489f4a a3c01f5200               mov dword ptr [0x521fc0], eax
00489f4f a3b41f5200               mov dword ptr [0x521fb4], eax
00489f54 bb01000000               mov ebx, 1
00489f59 c74004941f5200           mov dword ptr [eax + 4], 0x521f94
00489f60 31d2                     xor edx, edx
00489f62 a1c01f5200               mov eax, dword ptr [0x521fc0]
00489f67 8915901f5200             mov dword ptr [0x521f90], edx
00489f6d 891d8c1f5200             mov dword ptr [0x521f8c], ebx
00489f73 5a                       pop edx
00489f74 5b                       pop ebx
00489f75 c3                       ret
; HandleSnd_FreeDictator
00489f76 52                       push edx
00489f77 ba5c534900               mov edx, 0x49535c
00489f7c b8c01f5200               mov eax, 0x521fc0
00489f81 e8f9220000               call 0x48c27f
00489f86 31d2                     xor edx, edx
00489f88 8915901f5200             mov dword ptr [0x521f90], edx
00489f8e 89158c1f5200             mov dword ptr [0x521f8c], edx
00489f94 5a                       pop edx
00489f95 c3                       ret
; HandlSnd_ClearListe
00489f96 53                       push ebx
00489f97 51                       push ecx
00489f98 52                       push edx
00489f99 31c9                     xor ecx, ecx
00489f9b eb1d                     jmp 0x489fba
00489f9d c700ffffffff             mov dword ptr [eax], 0xffffffff
00489fa3 c6430800                 mov byte ptr [ebx + 8], 0
00489fa7 c7432000000000           mov dword ptr [ebx + 0x20], 0
00489fae 83c108                   add ecx, 8
00489fb1 83f950                   cmp ecx, 0x50
00489fb4 0f8463000000             je 0x48a01d
00489fba 8b916c215200             mov edx, dword ptr [ecx + 0x52216c]
00489fc0 85d2                     test edx, edx
00489fc2 74ea                     je 0x489fae
00489fc4 8b8170215200             mov eax, dword ptr [ecx + 0x522170]
00489fca 8a4008                   mov al, byte ptr [eax + 8]
00489fcd 25ff000000               and eax, 0xff
00489fd2 83f801                   cmp eax, 1
00489fd5 75d7                     jne 0x489fae
00489fd7 89d0                     mov eax, edx
00489fd9 e8db1e0000               call 0x48beb9
00489fde 85c0                     test eax, eax
00489fe0 74cc                     je 0x489fae
00489fe2 8b9970215200             mov ebx, dword ptr [ecx + 0x522170]
00489fe8 31c0                     xor eax, eax
00489fea 8a4308                   mov al, byte ptr [ebx + 8]
00489fed 83f801                   cmp eax, 1
00489ff0 7507                     jne 0x489ff9
00489ff2 89d8                     mov eax, ebx
00489ff4 e83cfeffff               call 0x489e35
00489ff9 8b4328                   mov eax, dword ptr [ebx + 0x28]
00489ffc 8338ff                   cmp dword ptr [eax], -1
00489fff 74ad                     je 0x489fae
0048a001 31d2                     xor edx, edx
0048a003 8a5308                   mov dl, byte ptr [ebx + 8]
0048a006 85d2                     test edx, edx
0048a008 74a4                     je 0x489fae
0048a00a 83fa02                   cmp edx, 2
0048a00d 758e                     jne 0x489f9d
0048a00f ba01000000               mov edx, 1
0048a014 89d8                     mov eax, ebx
0048a016 e8000f0000               call 0x48af1b
0048a01b eb91                     jmp 0x489fae
0048a01d 31c9                     xor ecx, ecx
0048a01f eb1d                     jmp 0x48a03e
0048a021 c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a027 c6430800                 mov byte ptr [ebx + 8], 0
0048a02b c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a032 83c108                   add ecx, 8
0048a035 83f950                   cmp ecx, 0x50
0048a038 0f8463000000             je 0x48a0a1
0048a03e 8b911c215200             mov edx, dword ptr [ecx + 0x52211c]
0048a044 85d2                     test edx, edx
0048a046 74ea                     je 0x48a032
0048a048 8b8120215200             mov eax, dword ptr [ecx + 0x522120]
0048a04e 8a4008                   mov al, byte ptr [eax + 8]
0048a051 25ff000000               and eax, 0xff
0048a056 83f801                   cmp eax, 1
0048a059 75d7                     jne 0x48a032
0048a05b 89d0                     mov eax, edx
0048a05d e8571e0000               call 0x48beb9
0048a062 85c0                     test eax, eax
0048a064 74cc                     je 0x48a032
0048a066 8b9920215200             mov ebx, dword ptr [ecx + 0x522120]
0048a06c 31c0                     xor eax, eax
0048a06e 8a4308                   mov al, byte ptr [ebx + 8]
0048a071 83f801                   cmp eax, 1
0048a074 7507                     jne 0x48a07d
0048a076 89d8                     mov eax, ebx
0048a078 e8b8fdffff               call 0x489e35
0048a07d 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a080 8338ff                   cmp dword ptr [eax], -1
0048a083 74ad                     je 0x48a032
0048a085 31d2                     xor edx, edx
0048a087 8a5308                   mov dl, byte ptr [ebx + 8]
0048a08a 85d2                     test edx, edx
0048a08c 74a4                     je 0x48a032
0048a08e 83fa02                   cmp edx, 2
0048a091 758e                     jne 0x48a021
0048a093 ba01000000               mov edx, 1
0048a098 89d8                     mov eax, ebx
0048a09a e87c0e0000               call 0x48af1b
0048a09f eb91                     jmp 0x48a032
0048a0a1 833d901f520000           cmp dword ptr [0x521f90], 0
0048a0a8 7441                     je 0x48a0eb
0048a0aa a1c01f5200               mov eax, dword ptr [0x521fc0]
0048a0af 8b00                     mov eax, dword ptr [eax]
0048a0b1 e8031e0000               call 0x48beb9
0048a0b6 85c0                     test eax, eax
0048a0b8 7431                     je 0x48a0eb
0048a0ba 833d901f520000           cmp dword ptr [0x521f90], 0
0048a0c1 7428                     je 0x48a0eb
0048a0c3 31c0                     xor eax, eax
0048a0c5 a3901f5200               mov dword ptr [0x521f90], eax
0048a0ca a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a0cf 8b00                     mov eax, dword ptr [eax]
0048a0d1 e89e1e0000               call 0x48bf74
0048a0d6 a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a0db e8b4160000               call 0x48b794
0048a0e0 a1bc1f5200               mov eax, dword ptr [0x521fbc]
0048a0e5 c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a0eb b801000000               mov eax, 1
0048a0f0 5a                       pop edx
0048a0f1 59                       pop ecx
0048a0f2 5b                       pop ebx
0048a0f3 c3                       ret
; HndSound_LoadDataInfo
0048a0f4 56                       push esi
0048a0f5 57                       push edi
0048a0f6 89c6                     mov esi, eax
0048a0f8 89d7                     mov edi, edx
0048a0fa 89da                     mov edx, ebx
0048a0fc 89f8                     mov eax, edi
0048a0fe e88d120000               call 0x48b390
0048a103 894618                   mov dword ptr [esi + 0x18], eax
0048a106 85c0                     test eax, eax
0048a108 743b                     je 0x48a145
0048a10a 893e                     mov dword ptr [esi], edi
0048a10c 89da                     mov edx, ebx
0048a10e 8b4618                   mov eax, dword ptr [esi + 0x18]
0048a111 895e04                   mov dword ptr [esi + 4], ebx
0048a114 e89a120000               call 0x48b3b3
0048a119 89461c                   mov dword ptr [esi + 0x1c], eax
0048a11c 8b4618                   mov eax, dword ptr [esi + 0x18]
0048a11f 894e0c                   mov dword ptr [esi + 0xc], ecx
0048a122 668b4004                 mov ax, word ptr [eax + 4]
0048a126 25ffff0000               and eax, 0xffff
0048a12b 3d00010000               cmp eax, 0x100
0048a130 7404                     je 0x48a136
0048a132 8b44240c                 mov eax, dword ptr [esp + 0xc]
0048a136 894610                   mov dword ptr [esi + 0x10], eax
0048a139 b801000000               mov eax, 1
0048a13e c7461400000000           mov dword ptr [esi + 0x14], 0
0048a145 5f                       pop edi
0048a146 5e                       pop esi
0048a147 c20400                   ret 4
; HandlSnd_SetVolume
0048a14a 53                       push ebx
0048a14b 51                       push ecx
0048a14c 89c3                     mov ebx, eax
0048a14e 8b08                     mov ecx, dword ptr [eax]
0048a150 83f9ff                   cmp ecx, -1
0048a153 7505                     jne 0x48a15a
0048a155 31c0                     xor eax, eax
0048a157 59                       pop ecx
0048a158 5b                       pop ebx
0048a159 c3                       ret
0048a15a 89c8                     mov eax, ecx
0048a15c c1e002                   shl eax, 2
0048a15f 29c8                     sub eax, ecx
0048a161 c1e002                   shl eax, 2
0048a164 29c8                     sub eax, ecx
0048a166 c1e002                   shl eax, 2
0048a169 31c9                     xor ecx, ecx
0048a16b 8a8884135200             mov cl, byte ptr [eax + 0x521384]
0048a171 85c9                     test ecx, ecx
0048a173 0f8497000000             je 0x48a210
0048a179 89908c135200             mov dword ptr [eax + 0x52138c], edx
0048a17f 8b1b                     mov ebx, dword ptr [ebx]
0048a181 89d8                     mov eax, ebx
0048a183 c1e002                   shl eax, 2
0048a186 29d8                     sub eax, ebx
0048a188 c1e002                   shl eax, 2
0048a18b 29d8                     sub eax, ebx
0048a18d c1e002                   shl eax, 2
0048a190 8b9894135200             mov ebx, dword ptr [eax + 0x521394]
0048a196 668b5b04                 mov bx, word ptr [ebx + 4]
0048a19a 81e3ffff0000             and ebx, 0xffff
0048a1a0 81fb00010000             cmp ebx, 0x100
0048a1a6 74ad                     je 0x48a155
0048a1a8 85d2                     test edx, edx
0048a1aa 754b                     jne 0x48a1f7
0048a1ac 057c135200               add eax, 0x52137c
0048a1b1 8a5008                   mov dl, byte ptr [eax + 8]
0048a1b4 89c3                     mov ebx, eax
0048a1b6 83fa01                   cmp edx, 1
0048a1b9 7505                     jne 0x48a1c0
0048a1bb e875fcffff               call 0x489e35
0048a1c0 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a1c3 8338ff                   cmp dword ptr [eax], -1
0048a1c6 7448                     je 0x48a210
0048a1c8 31d2                     xor edx, edx
0048a1ca 8a5308                   mov dl, byte ptr [ebx + 8]
0048a1cd 85d2                     test edx, edx
0048a1cf 743f                     je 0x48a210
0048a1d1 83fa02                   cmp edx, 2
0048a1d4 750e                     jne 0x48a1e4
0048a1d6 ba01000000               mov edx, 1
0048a1db 89d8                     mov eax, ebx
0048a1dd e8390d0000               call 0x48af1b
0048a1e2 eb2c                     jmp 0x48a210
0048a1e4 c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a1ea c6430800                 mov byte ptr [ebx + 8], 0
0048a1ee c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a1f5 eb19                     jmp 0x48a210
0048a1f7 31d2                     xor edx, edx
0048a1f9 8a9084135200             mov dl, byte ptr [eax + 0x521384]
0048a1ff 83fa01                   cmp edx, 1
0048a202 750c                     jne 0x48a210
0048a204 8915881f5200             mov dword ptr [0x521f88], edx
0048a20a 899090135200             mov dword ptr [eax + 0x521390], edx
0048a210 b801000000               mov eax, 1
0048a215 59                       pop ecx
0048a216 5b                       pop ebx
0048a217 c3                       ret
; HandlSnd_Insert
0048a218 56                       push esi
0048a219 57                       push edi
0048a21a 55                       push ebp
0048a21b 83ec08                   sub esp, 8
0048a21e 89c5                     mov ebp, eax
0048a220 891424                   mov dword ptr [esp], edx
0048a223 89de                     mov esi, ebx
0048a225 8b13                     mov edx, dword ptr [ebx]
0048a227 83faff                   cmp edx, -1
0048a22a 0f8494010000             je 0x48a3c4
0048a230 837c241800               cmp dword ptr [esp + 0x18], 0
0048a235 0f857e000000             jne 0x48a2b9
0048a23b 8b1b                     mov ebx, dword ptr [ebx]
0048a23d 89d8                     mov eax, ebx
0048a23f c1e002                   shl eax, 2
0048a242 29d8                     sub eax, ebx
0048a244 c1e002                   shl eax, 2
0048a247 29d8                     sub eax, ebx
0048a249 c1e002                   shl eax, 2
0048a24c 8b9894135200             mov ebx, dword ptr [eax + 0x521394]
0048a252 668b5b04                 mov bx, word ptr [ebx + 4]
0048a256 81e3ffff0000             and ebx, 0xffff
0048a25c 81fb00010000             cmp ebx, 0x100
0048a262 7455                     je 0x48a2b9
0048a264 057c135200               add eax, 0x52137c
0048a269 31db                     xor ebx, ebx
0048a26b 8a5808                   mov bl, byte ptr [eax + 8]
0048a26e 89c6                     mov esi, eax
0048a270 83fb01                   cmp ebx, 1
0048a273 7505                     jne 0x48a27a
0048a275 e8bbfbffff               call 0x489e35
0048a27a 8b4628                   mov eax, dword ptr [esi + 0x28]
0048a27d 8338ff                   cmp dword ptr [eax], -1
0048a280 742d                     je 0x48a2af
0048a282 31db                     xor ebx, ebx
0048a284 8a5e08                   mov bl, byte ptr [esi + 8]
0048a287 85db                     test ebx, ebx
0048a289 7424                     je 0x48a2af
0048a28b 83fb02                   cmp ebx, 2
0048a28e 750e                     jne 0x48a29e
0048a290 ba01000000               mov edx, 1
0048a295 89f0                     mov eax, esi
0048a297 e87f0c0000               call 0x48af1b
0048a29c eb11                     jmp 0x48a2af
0048a29e c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a2a4 c6460800                 mov byte ptr [esi + 8], 0
0048a2a8 c7462000000000           mov dword ptr [esi + 0x20], 0
0048a2af b801000000               mov eax, 1
0048a2b4 e976010000               jmp 0x48a42f
0048a2b9 8b1e                     mov ebx, dword ptr [esi]
0048a2bb 89d8                     mov eax, ebx
0048a2bd c1e002                   shl eax, 2
0048a2c0 29d8                     sub eax, ebx
0048a2c2 c1e002                   shl eax, 2
0048a2c5 29d8                     sub eax, ebx
0048a2c7 c1e002                   shl eax, 2
0048a2ca 3ba87c135200             cmp ebp, dword ptr [eax + 0x52137c]
0048a2d0 7518                     jne 0x48a2ea
0048a2d2 8b1c24                   mov ebx, dword ptr [esp]
0048a2d5 3b9880135200             cmp ebx, dword ptr [eax + 0x521380]
0048a2db 750d                     jne 0x48a2ea
0048a2dd 8b542418                 mov edx, dword ptr [esp + 0x18]
0048a2e1 89f0                     mov eax, esi
0048a2e3 e862feffff               call 0x48a14a
0048a2e8 ebc5                     jmp 0x48a2af
0048a2ea 8b1e                     mov ebx, dword ptr [esi]
0048a2ec 89d8                     mov eax, ebx
0048a2ee c1e002                   shl eax, 2
0048a2f1 29d8                     sub eax, ebx
0048a2f3 c1e002                   shl eax, 2
0048a2f6 29d8                     sub eax, ebx
0048a2f8 c1e002                   shl eax, 2
0048a2fb 31db                     xor ebx, ebx
0048a2fd 8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048a303 83fb01                   cmp ebx, 1
0048a306 7566                     jne 0x48a36e
0048a308 057c135200               add eax, 0x52137c
0048a30d 0fb67808                 movzx edi, byte ptr [eax + 8]
0048a311 89c3                     mov ebx, eax
0048a313 83ff01                   cmp edi, 1
0048a316 7505                     jne 0x48a31d
0048a318 e818fbffff               call 0x489e35
0048a31d 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a320 8338ff                   cmp dword ptr [eax], -1
0048a323 742c                     je 0x48a351
0048a325 0fb67b08                 movzx edi, byte ptr [ebx + 8]
0048a329 85ff                     test edi, edi
0048a32b 7424                     je 0x48a351
0048a32d 83ff02                   cmp edi, 2
0048a330 750e                     jne 0x48a340
0048a332 ba01000000               mov edx, 1
0048a337 89d8                     mov eax, ebx
0048a339 e8dd0b0000               call 0x48af1b
0048a33e eb11                     jmp 0x48a351
0048a340 c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a346 c6430800                 mov byte ptr [ebx + 8], 0
0048a34a c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a351 e8a20b0000               call 0x48aef8
0048a356 8906                     mov dword ptr [esi], eax
0048a358 83f8ff                   cmp eax, -1
0048a35b 7507                     jne 0x48a364
0048a35d 31c0                     xor eax, eax
0048a35f e9cb000000               jmp 0x48a42f
0048a364 c705841f520001000000     mov dword ptr [0x521f84], 1
0048a36e 8b442418                 mov eax, dword ptr [esp + 0x18]
0048a372 8b1e                     mov ebx, dword ptr [esi]
0048a374 50                       push eax
0048a375 89d8                     mov eax, ebx
0048a377 c1e002                   shl eax, 2
0048a37a 29d8                     sub eax, ebx
0048a37c c1e002                   shl eax, 2
0048a37f 29d8                     sub eax, ebx
0048a381 89ea                     mov edx, ebp
0048a383 c1e002                   shl eax, 2
0048a386 8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a38a 057c135200               add eax, 0x52137c
0048a38f e860fdffff               call 0x48a0f4
0048a394 8b1e                     mov ebx, dword ptr [esi]
0048a396 89d8                     mov eax, ebx
0048a398 c1e002                   shl eax, 2
0048a39b 29d8                     sub eax, ebx
0048a39d c1e002                   shl eax, 2
0048a3a0 29d8                     sub eax, ebx
0048a3a2 893485a4135200           mov dword ptr [eax*4 + 0x5213a4], esi
0048a3a9 8b1e                     mov ebx, dword ptr [esi]
0048a3ab 89d8                     mov eax, ebx
0048a3ad c1e002                   shl eax, 2
0048a3b0 29d8                     sub eax, ebx
0048a3b2 c1e002                   shl eax, 2
0048a3b5 29d8                     sub eax, ebx
0048a3b7 c604858413520002         mov byte ptr [eax*4 + 0x521384], 2
0048a3bf e9ebfeffff               jmp 0x48a2af
0048a3c4 e82f0b0000               call 0x48aef8
0048a3c9 89442404                 mov dword ptr [esp + 4], eax
0048a3cd 39d0                     cmp eax, edx
0048a3cf 7504                     jne 0x48a3d5
0048a3d1 31d0                     xor eax, edx
0048a3d3 eb5a                     jmp 0x48a42f
0048a3d5 8b7c2418                 mov edi, dword ptr [esp + 0x18]
0048a3d9 57                       push edi
0048a3da 89c7                     mov edi, eax
0048a3dc c1e702                   shl edi, 2
0048a3df 29c7                     sub edi, eax
0048a3e1 c1e702                   shl edi, 2
0048a3e4 8b5c2404                 mov ebx, dword ptr [esp + 4]
0048a3e8 29c7                     sub edi, eax
0048a3ea b87c135200               mov eax, 0x52137c
0048a3ef c1e702                   shl edi, 2
0048a3f2 89ea                     mov edx, ebp
0048a3f4 01f8                     add eax, edi
0048a3f6 e8f9fcffff               call 0x48a0f4
0048a3fb 85c0                     test eax, eax
0048a3fd 750a                     jne 0x48a409
0048a3ff e8cc0b0000               call 0x48afd0
0048a404 e954ffffff               jmp 0x48a35d
0048a409 8b442404                 mov eax, dword ptr [esp + 4]
0048a40d 8906                     mov dword ptr [esi], eax
0048a40f b402                     mov ah, 2
0048a411 89b7a4135200             mov dword ptr [edi + 0x5213a4], esi
0048a417 31ed                     xor ebp, ebp
0048a419 88a784135200             mov byte ptr [edi + 0x521384], ah
0048a41f b801000000               mov eax, 1
0048a424 89af90135200             mov dword ptr [edi + 0x521390], ebp
0048a42a a3841f5200               mov dword ptr [0x521f84], eax
0048a42f 83c408                   add esp, 8
0048a432 5d                       pop ebp
0048a433 5f                       pop edi
0048a434 5e                       pop esi
0048a435 c20400                   ret 4
; HandleSnd_StopHandle
0048a438 53                       push ebx
0048a439 52                       push edx
0048a43a 8b10                     mov edx, dword ptr [eax]
0048a43c 83faff                   cmp edx, -1
0048a43f 7505                     jne 0x48a446
0048a441 31c0                     xor eax, eax
0048a443 5a                       pop edx
0048a444 5b                       pop ebx
0048a445 c3                       ret
0048a446 89d0                     mov eax, edx
0048a448 c1e002                   shl eax, 2
0048a44b 29d0                     sub eax, edx
0048a44d c1e002                   shl eax, 2
0048a450 29d0                     sub eax, edx
0048a452 c1e002                   shl eax, 2
0048a455 057c135200               add eax, 0x52137c
0048a45a 31d2                     xor edx, edx
0048a45c 8a5008                   mov dl, byte ptr [eax + 8]
0048a45f 89c3                     mov ebx, eax
0048a461 83fa01                   cmp edx, 1
0048a464 7505                     jne 0x48a46b
0048a466 e8caf9ffff               call 0x489e35
0048a46b 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a46e 8338ff                   cmp dword ptr [eax], -1
0048a471 742d                     je 0x48a4a0
0048a473 31d2                     xor edx, edx
0048a475 8a5308                   mov dl, byte ptr [ebx + 8]
0048a478 85d2                     test edx, edx
0048a47a 7424                     je 0x48a4a0
0048a47c 83fa02                   cmp edx, 2
0048a47f 750e                     jne 0x48a48f
0048a481 ba01000000               mov edx, 1
0048a486 89d8                     mov eax, ebx
0048a488 e88e0a0000               call 0x48af1b
0048a48d eb11                     jmp 0x48a4a0
0048a48f c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a495 c6430800                 mov byte ptr [ebx + 8], 0
0048a499 c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a4a0 b801000000               mov eax, 1
0048a4a5 5a                       pop edx
0048a4a6 5b                       pop ebx
0048a4a7 c3                       ret
; HandleSnd_StopAllHandle
0048a4a8 53                       push ebx
0048a4a9 51                       push ecx
0048a4aa 52                       push edx
0048a4ab 31c9                     xor ecx, ecx
0048a4ad eb20                     jmp 0x48a4cf
0048a4af c700ffffffff             mov dword ptr [eax], 0xffffffff
0048a4b5 c6430800                 mov byte ptr [ebx + 8], 0
0048a4b9 c7432000000000           mov dword ptr [ebx + 0x20], 0
0048a4c0 83c12c                   add ecx, 0x2c
0048a4c3 81f998080000             cmp ecx, 0x898
0048a4c9 0f8421fcffff             je 0x48a0f0
0048a4cf 31c0                     xor eax, eax
0048a4d1 8a8184135200             mov al, byte ptr [ecx + 0x521384]
0048a4d7 85c0                     test eax, eax
0048a4d9 74e5                     je 0x48a4c0
0048a4db b87c135200               mov eax, 0x52137c
0048a4e0 01c8                     add eax, ecx
0048a4e2 31d2                     xor edx, edx
0048a4e4 8a5008                   mov dl, byte ptr [eax + 8]
0048a4e7 89c3                     mov ebx, eax
0048a4e9 83fa01                   cmp edx, 1
0048a4ec 7505                     jne 0x48a4f3
0048a4ee e842f9ffff               call 0x489e35
0048a4f3 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048a4f6 8338ff                   cmp dword ptr [eax], -1
0048a4f9 74c5                     je 0x48a4c0
0048a4fb 31d2                     xor edx, edx
0048a4fd 8a5308                   mov dl, byte ptr [ebx + 8]
0048a500 85d2                     test edx, edx
0048a502 74bc                     je 0x48a4c0
0048a504 83fa02                   cmp edx, 2
0048a507 75a6                     jne 0x48a4af
0048a509 ba01000000               mov edx, 1
0048a50e 89d8                     mov eax, ebx
0048a510 e8060a0000               call 0x48af1b
0048a515 eba9                     jmp 0x48a4c0
; HandlSnd_AffectVolumeOut
0048a517 53                       push ebx
0048a518 51                       push ecx
0048a519 52                       push edx
0048a51a 56                       push esi
0048a51b 55                       push ebp
0048a51c 833d881f520000           cmp dword ptr [0x521f88], 0
0048a523 750d                     jne 0x48a532
0048a525 833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a52c 0f8424010000             je 0x48a656
0048a532 be7c135200               mov esi, 0x52137c
0048a537 31db                     xor ebx, ebx
0048a539 eb12                     jmp 0x48a54d
0048a53b 83c32c                   add ebx, 0x2c
0048a53e 83c62c                   add esi, 0x2c
0048a541 81fb70030000             cmp ebx, 0x370
0048a547 0f8498000000             je 0x48a5e5
0048a54d 31c0                     xor eax, eax
0048a54f 8a8384135200             mov al, byte ptr [ebx + 0x521384]
0048a555 85c0                     test eax, eax
0048a557 74e2                     je 0x48a53b
0048a559 8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048a55f 8338ff                   cmp dword ptr [eax], -1
0048a562 74d7                     je 0x48a53b
0048a564 8b8b9c135200             mov ecx, dword ptr [ebx + 0x52139c]
0048a56a 85c9                     test ecx, ecx
0048a56c 74cd                     je 0x48a53b
0048a56e 833900                   cmp dword ptr [ecx], 0
0048a571 74c8                     je 0x48a53b
0048a573 83bb9013520001           cmp dword ptr [ebx + 0x521390], 1
0048a57a 7409                     je 0x48a585
0048a57c 833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a583 74b6                     je 0x48a53b
0048a585 8b561c                   mov edx, dword ptr [esi + 0x1c]
0048a588 89f0                     mov eax, esi
0048a58a 8a520d                   mov dl, byte ptr [edx + 0xd]
0048a58d 81e2ff000000             and edx, 0xff
0048a593 7505                     jne 0x48a59a
0048a595 ba00010000               mov edx, 0x100
0048a59a 8b4818                   mov ecx, dword ptr [eax + 0x18]
0048a59d 668b4904                 mov cx, word ptr [ecx + 4]
0048a5a1 81e1ffff0000             and ecx, 0xffff
0048a5a7 81f900010000             cmp ecx, 0x100
0048a5ad 7503                     jne 0x48a5b2
0048a5af 894810                   mov dword ptr [eax + 0x10], ecx
0048a5b2 8b4010                   mov eax, dword ptr [eax + 0x10]
0048a5b5 0fafc2                   imul eax, edx
0048a5b8 0faf05588f4900           imul eax, dword ptr [0x498f58]
0048a5bf c1f814                   sar eax, 0x14
0048a5c2 8b0c85148f4900           mov ecx, dword ptr [eax*4 + 0x498f14]
0048a5c9 8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048a5cf 51                       push ecx
0048a5d0 8b00                     mov eax, dword ptr [eax]
0048a5d2 50                       push eax
0048a5d3 8b10                     mov edx, dword ptr [eax]
0048a5d5 ff523c                   call dword ptr [edx + 0x3c]
0048a5d8 31c9                     xor ecx, ecx
0048a5da 898b90135200             mov dword ptr [ebx + 0x521390], ecx
0048a5e0 e956ffffff               jmp 0x48a53b
0048a5e5 833d901f520000           cmp dword ptr [0x521f90], 0
0048a5ec 7460                     je 0x48a64e
0048a5ee 833d5c8f490000           cmp dword ptr [0x498f5c], 0
0048a5f5 7457                     je 0x48a64e
0048a5f7 8b15b01f5200             mov edx, dword ptr [0x521fb0]
0048a5fd b8941f5200               mov eax, 0x521f94
0048a602 8a520d                   mov dl, byte ptr [edx + 0xd]
0048a605 81e2ff000000             and edx, 0xff
0048a60b 7505                     jne 0x48a612
0048a60d ba00010000               mov edx, 0x100
0048a612 8b5818                   mov ebx, dword ptr [eax + 0x18]
0048a615 668b5b04                 mov bx, word ptr [ebx + 4]
0048a619 81e3ffff0000             and ebx, 0xffff
0048a61f 81fb00010000             cmp ebx, 0x100
0048a625 7503                     jne 0x48a62a
0048a627 895810                   mov dword ptr [eax + 0x10], ebx
0048a62a 0faf5010                 imul edx, dword ptr [eax + 0x10]
0048a62e a1588f4900               mov eax, dword ptr [0x498f58]
0048a633 0fafc2                   imul eax, edx
0048a636 c1f814                   sar eax, 0x14
0048a639 8b1c85148f4900           mov ebx, dword ptr [eax*4 + 0x498f14]
0048a640 a1b41f5200               mov eax, dword ptr [0x521fb4]
0048a645 53                       push ebx
0048a646 8b00                     mov eax, dword ptr [eax]
0048a648 50                       push eax
0048a649 8b10                     mov edx, dword ptr [eax]
0048a64b ff523c                   call dword ptr [edx + 0x3c]
0048a64e 31ed                     xor ebp, ebp
0048a650 892d881f5200             mov dword ptr [0x521f88], ebp
0048a656 31f6                     xor esi, esi
0048a658 89355c8f4900             mov dword ptr [0x498f5c], esi
0048a65e 5d                       pop ebp
0048a65f 5e                       pop esi
0048a660 5a                       pop edx
0048a661 59                       pop ecx
0048a662 5b                       pop ebx
0048a663 c3                       ret
; HandlSnd_TriWaitingHandle
0048a664 53                       push ebx
0048a665 833d841f520001           cmp dword ptr [0x521f84], 1
0048a66c 750d                     jne 0x48a67b
0048a66e 31db                     xor ebx, ebx
0048a670 e81a0d0000               call 0x48b38f
0048a675 891d841f5200             mov dword ptr [0x521f84], ebx
0048a67b 5b                       pop ebx
0048a67c c3                       ret
0048a67d be7c135200               mov esi, 0x52137c
0048a682 01de                     add esi, ebx
0048a684 85d2                     test edx, edx
0048a686 0f8414010000             je 0x48a7a0
0048a68c e856080000               call 0x48aee7
0048a691 85c0                     test eax, eax
0048a693 740f                     je 0x48a6a4
0048a695 e890060000               call 0x48ad2a
0048a69a 85c0                     test eax, eax
0048a69c 0f854b010000             jne 0x48a7ed
0048a6a2 eb19                     jmp 0x48a6bd
0048a6a4 8b02                     mov eax, dword ptr [edx]
0048a6a6 89f2                     mov edx, esi
0048a6a8 e8b2070000               call 0x48ae5f
0048a6ad 89839c135200             mov dword ptr [ebx + 0x52139c], eax
0048a6b3 85c0                     test eax, eax
0048a6b5 0f85d9000000             jne 0x48a794
0048a6bb 31ff                     xor edi, edi
0048a6bd 83ed2c                   sub ebp, 0x2c
0048a6c0 49                       dec ecx
0048a6c1 83f913                   cmp ecx, 0x13
0048a6c4 0f8e23010000             jle 0x48a7ed
0048a6ca 6bd92c                   imul ebx, ecx, 0x2c
0048a6cd 8b9380135200             mov edx, dword ptr [ebx + 0x521380]
0048a6d3 8b837c135200             mov eax, dword ptr [ebx + 0x52137c]
0048a6d9 e8f5050000               call 0x48acd3
0048a6de 8bb394135200             mov esi, dword ptr [ebx + 0x521394]
0048a6e4 89c2                     mov edx, eax
0048a6e6 31c0                     xor eax, eax
0048a6e8 668b4604                 mov ax, word ptr [esi + 4]
0048a6ec 3d00010000               cmp eax, 0x100
0048a6f1 0f940424                 sete byte ptr [esp]
0048a6f5 31c0                     xor eax, eax
0048a6f7 8a0424                   mov al, byte ptr [esp]
0048a6fa 85c0                     test eax, eax
0048a6fc 0f847bffffff             je 0x48a67d
0048a702 8b15901f5200             mov edx, dword ptr [0x521f90]
0048a708 85d2                     test edx, edx
0048a70a 75b1                     jne 0x48a6bd
0048a70c 8915a01f5200             mov dword ptr [0x521fa0], edx
0048a712 8935ac1f5200             mov dword ptr [0x521fac], esi
0048a718 8b8380135200             mov eax, dword ptr [ebx + 0x521380]
0048a71e ba00010000               mov edx, 0x100
0048a723 a3981f5200               mov dword ptr [0x521f98], eax
0048a728 8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048a72e 8915a41f5200             mov dword ptr [0x521fa4], edx
0048a734 a3bc1f5200               mov dword ptr [0x521fbc], eax
0048a739 8b837c135200             mov eax, dword ptr [ebx + 0x52137c]
0048a73f 8b15981f5200             mov edx, dword ptr [0x521f98]
0048a745 a3941f5200               mov dword ptr [0x521f94], eax
0048a74a 8b8398135200             mov eax, dword ptr [ebx + 0x521398]
0048a750 bb01000000               mov ebx, 1
0048a755 a3b01f5200               mov dword ptr [0x521fb0], eax
0048a75a 891da81f5200             mov dword ptr [0x521fa8], ebx
0048a760 e86f030000               call 0x48aad4
0048a765 8b15b41f5200             mov edx, dword ptr [0x521fb4]
0048a76b 8902                     mov dword ptr [edx], eax
0048a76d b8941f5200               mov eax, 0x521f94
0048a772 e87d170000               call 0x48bef4
0048a777 85c0                     test eax, eax
0048a779 7502                     jne 0x48a77d
0048a77b 31ff                     xor edi, edi
0048a77d 89c8                     mov eax, ecx
0048a77f be01000000               mov esi, 1
0048a784 e894090000               call 0x48b11d
0048a789 8935901f5200             mov dword ptr [0x521f90], esi
0048a78f e929ffffff               jmp 0x48a6bd
0048a794 c783a013520001000000     mov dword ptr [ebx + 0x5213a0], 1
0048a79e eb2a                     jmp 0x48a7ca
0048a7a0 e885050000               call 0x48ad2a
0048a7a5 85c0                     test eax, eax
0048a7a7 0f8510ffffff             jne 0x48a6bd
0048a7ad 89f0                     mov eax, esi
0048a7af e8c4040000               call 0x48ac78
0048a7b4 89839c135200             mov dword ptr [ebx + 0x52139c], eax
0048a7ba 85c0                     test eax, eax
0048a7bc 0f84f9feffff             je 0x48a6bb
0048a7c2 31f6                     xor esi, esi
0048a7c4 89b3a0135200             mov dword ptr [ebx + 0x5213a0], esi
0048a7ca 89e8                     mov eax, ebp
0048a7cc e823170000               call 0x48bef4
0048a7d1 85c0                     test eax, eax
0048a7d3 7502                     jne 0x48a7d7
0048a7d5 31ff                     xor edi, edi
0048a7d7 89c8                     mov eax, ecx
0048a7d9 e80b0a0000               call 0x48b1e9
0048a7de c705841f520001000000     mov dword ptr [0x521f84], 1
0048a7e8 e9d0feffff               jmp 0x48a6bd
0048a7ed 89f8                     mov eax, edi
0048a7ef 83c404                   add esp, 4
0048a7f2 5d                       pop ebp
0048a7f3 5f                       pop edi
0048a7f4 5e                       pop esi
0048a7f5 5a                       pop edx
0048a7f6 59                       pop ecx
0048a7f7 5b                       pop ebx
0048a7f8 c3                       ret
; HandlSnd_ValidateListe
0048a7f9 e898f7ffff               call 0x489f96
0048a7fe e814fdffff               call 0x48a517
; HandlSnd_LaunchWaitingSound
0048a803 53                       push ebx
0048a804 51                       push ecx
0048a805 52                       push edx
0048a806 56                       push esi
0048a807 57                       push edi
0048a808 55                       push ebp
0048a809 83ec04                   sub esp, 4
0048a80c e8d8070000               call 0x48afe9
0048a811 89c5                     mov ebp, eax
0048a813 c1e502                   shl ebp, 2
0048a816 29c5                     sub ebp, eax
0048a818 c1e502                   shl ebp, 2
0048a81b 29c5                     sub ebp, eax
0048a81d bf01000000               mov edi, 1
0048a822 c1e502                   shl ebp, 2
0048a825 89c1                     mov ecx, eax
0048a827 81c57c135200             add ebp, 0x52137c
0048a82d e98ffeffff               jmp 0x48a6c1
; PlaySnd_CreateSoundPath
0048a834 52                       push edx
0048a835 bae8030000               mov edx, 0x3e8
0048a83a 31c0                     xor eax, eax
0048a83c e8401c0000               call 0x48c481
0048a841 89c2                     mov edx, eax
0048a843 803800                   cmp byte ptr [eax], 0
0048a846 7403                     je 0x48a84b
0048a848 40                       inc eax
0048a849 ebf8                     jmp 0x48a843
0048a84b 8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a84f 750d                     jne 0x48a85e
0048a851 687c534900               push 0x49537c
0048a856 52                       push edx
0048a857 6882534900               push 0x495382
0048a85c eb0b                     jmp 0x48a869
0048a85e 6887534900               push 0x495387
0048a863 52                       push edx
0048a864 688d534900               push 0x49538d
0048a869 681c205200               push 0x52201c
0048a86e e848270000               call 0x48cfbb
0048a873 83c410                   add esp, 0x10
0048a876 89d0                     mov eax, edx
0048a878 e8772f0000               call 0x48d7f4
0048a87d 5a                       pop edx
0048a87e c3                       ret
; SoundFile
0048a87f 50                       push eax
0048a880 681c205200               push 0x52201c
0048a885 6893534900               push 0x495393
0048a88a 52                       push edx
0048a88b e82b270000               call 0x48cfbb
0048a890 83c410                   add esp, 0x10
0048a893 c3                       ret
; PlaySnd_MakeID
0048a894 c1e010                   shl eax, 0x10
0048a897 c1e208                   shl edx, 8
0048a89a 09d0                     or eax, edx
0048a89c 09d8                     or eax, ebx
0048a89e c3                       ret
; PlaySnd_InitSoundLib
0048a89f 51                       push ecx
0048a8a0 52                       push edx
0048a8a1 56                       push esi
0048a8a2 81ec00010000             sub esp, 0x100
0048a8a8 803dc41f520000           cmp byte ptr [0x521fc4], 0
0048a8af 7407                     je 0x48a8b8
0048a8b1 30c0                     xor al, al
0048a8b3 e942010000               jmp 0x48a9fa
0048a8b8 a1e8274e00               mov eax, dword ptr [0x4e27e8]
0048a8bd e835150000               call 0x48bdf7
0048a8c2 85c0                     test eax, eax
0048a8c4 74eb                     je 0x48a8b1
0048a8c6 e8a1180000               call 0x48c16c
0048a8cb 85c0                     test eax, eax
0048a8cd 74e2                     je 0x48a8b1
0048a8cf bae8030000               mov edx, 0x3e8
0048a8d4 31c0                     xor eax, eax
0048a8d6 e8a61b0000               call 0x48c481
0048a8db 89c2                     mov edx, eax
0048a8dd 803800                   cmp byte ptr [eax], 0
0048a8e0 7403                     je 0x48a8e5
0048a8e2 40                       inc eax
0048a8e3 ebf8                     jmp 0x48a8dd
0048a8e5 8078ff5c                 cmp byte ptr [eax - 1], 0x5c
0048a8e9 750d                     jne 0x48a8f8
0048a8eb 687c534900               push 0x49537c
0048a8f0 52                       push edx
0048a8f1 6882534900               push 0x495382
0048a8f6 eb0b                     jmp 0x48a903
0048a8f8 6887534900               push 0x495387
0048a8fd 52                       push edx
0048a8fe 688d534900               push 0x49538d
0048a903 681c205200               push 0x52201c
0048a908 e8ae260000               call 0x48cfbb
0048a90d 83c410                   add esp, 0x10
0048a910 89d0                     mov eax, edx
0048a912 e8dd2e0000               call 0x48d7f4
0048a917 6899534900               push 0x495399
0048a91c 681c205200               push 0x52201c
0048a921 31d2                     xor edx, edx
0048a923 6893534900               push 0x495393
0048a928 8d44240c                 lea eax, [esp + 0xc]
0048a92c 8915c81f5200             mov dword ptr [0x521fc8], edx
0048a932 50                       push eax
0048a933 8915e41f5200             mov dword ptr [0x521fe4], edx
0048a939 891500205200             mov dword ptr [0x522000], edx
0048a93f e877260000               call 0x48cfbb
0048a944 83c410                   add esp, 0x10
0048a947 bac81f5200               mov edx, 0x521fc8
0048a94c 89e0                     mov eax, esp
0048a94e e8530c0000               call 0x48b5a6
0048a953 85c0                     test eax, eax
0048a955 0f8456ffffff             je 0x48a8b1
0048a95b 689b534900               push 0x49539b
0048a960 681c205200               push 0x52201c
0048a965 6893534900               push 0x495393
0048a96a 8d44240c                 lea eax, [esp + 0xc]
0048a96e 50                       push eax
0048a96f e847260000               call 0x48cfbb
0048a974 83c410                   add esp, 0x10
0048a977 bae41f5200               mov edx, 0x521fe4
0048a97c 89e0                     mov eax, esp
0048a97e e8230c0000               call 0x48b5a6
0048a983 85c0                     test eax, eax
0048a985 0f8426ffffff             je 0x48a8b1
0048a98b 689d534900               push 0x49539d
0048a990 681c205200               push 0x52201c
0048a995 6893534900               push 0x495393
0048a99a 8d44240c                 lea eax, [esp + 0xc]
0048a99e 50                       push eax
0048a99f e817260000               call 0x48cfbb
0048a9a4 83c410                   add esp, 0x10
0048a9a7 ba00205200               mov edx, 0x522000
0048a9ac 89e0                     mov eax, esp
0048a9ae e8f30b0000               call 0x48b5a6
0048a9b3 85c0                     test eax, eax
0048a9b5 0f84f6feffff             je 0x48a8b1
0048a9bb e879f5ffff               call 0x489f39
0048a9c0 85c0                     test eax, eax
0048a9c2 0f84e9feffff             je 0x48a8b1
0048a9c8 31c0                     xor eax, eax
0048a9ca 83c02c                   add eax, 0x2c
0048a9cd 30c9                     xor cl, cl
0048a9cf 31f6                     xor esi, esi
0048a9d1 888858135200             mov byte ptr [eax + 0x521358], cl
0048a9d7 89b070135200             mov dword ptr [eax + 0x521370], esi
0048a9dd 89b078135200             mov dword ptr [eax + 0x521378], esi
0048a9e3 89b064135200             mov dword ptr [eax + 0x521364], esi
0048a9e9 3d080c0000               cmp eax, 0xc08
0048a9ee 75da                     jne 0x48a9ca
0048a9f0 b501                     mov ch, 1
0048a9f2 882dc41f5200             mov byte ptr [0x521fc4], ch
0048a9f8 88e8                     mov al, ch
0048a9fa 81c400010000             add esp, 0x100
0048aa00 5e                       pop esi
0048aa01 5a                       pop edx
0048aa02 59                       pop ecx
0048aa03 c3                       ret
; PlaySnd_FreeSoundLib
0048aa04 52                       push edx
0048aa05 803dc41f520000           cmp byte ptr [0x521fc4], 0
0048aa0c 7435                     je 0x48aa43
0048aa0e e863f5ffff               call 0x489f76
0048aa13 b800205200               mov eax, 0x522000
0048aa18 e86a0c0000               call 0x48b687
0048aa1d b8e41f5200               mov eax, 0x521fe4
0048aa22 e8600c0000               call 0x48b687
0048aa27 b8c81f5200               mov eax, 0x521fc8
0048aa2c 30d2                     xor dl, dl
0048aa2e e8540c0000               call 0x48b687
0048aa33 e855170000               call 0x48c18d
0048aa38 e819140000               call 0x48be56
0048aa3d 8815c41f5200             mov byte ptr [0x521fc4], dl
0048aa43 5a                       pop edx
0048aa44 c3                       ret
; PlaySnd_SetGameVolume
0048aa45 51                       push ecx
0048aa46 a3588f4900               mov dword ptr [0x498f58], eax
0048aa4b 3d00010000               cmp eax, 0x100
0048aa50 7e0a                     jle 0x48aa5c
0048aa52 c705588f490000010000     mov dword ptr [0x498f58], 0x100
0048aa5c 833d588f490000           cmp dword ptr [0x498f58], 0
0048aa63 7d08                     jge 0x48aa6d
0048aa65 31c9                     xor ecx, ecx
0048aa67 890d588f4900             mov dword ptr [0x498f58], ecx
0048aa6d c7055c8f490001000000     mov dword ptr [0x498f5c], 1
0048aa77 59                       pop ecx
0048aa78 c3                       ret
; PlaySnd_PostSound
0048aa79 56                       push esi
0048aa7a 89c6                     mov esi, eax
0048aa7c 89d0                     mov eax, edx
0048aa7e 8b542408                 mov edx, dword ptr [esp + 8]
0048aa82 83fe42                   cmp esi, 0x42
0048aa85 7230                     jb 0x48aab7
0048aa87 761e                     jbe 0x48aaa7
0048aa89 83fe50                   cmp esi, 0x50
0048aa8c 7421                     je 0x48aaaf
0048aa8e 5e                       pop esi
0048aa8f c20400                   ret 4
0048aa92 52                       push edx
0048aa93 bac81f5200               mov edx, 0x521fc8
0048aa98 81e1ff000000             and ecx, 0xff
0048aa9e e875f7ffff               call 0x48a218
0048aaa3 5e                       pop esi
0048aaa4 c20400                   ret 4
0048aaa7 52                       push edx
0048aaa8 bae41f5200               mov edx, 0x521fe4
0048aaad ebe9                     jmp 0x48aa98
0048aaaf 52                       push edx
0048aab0 ba00205200               mov edx, 0x522000
0048aab5 ebe1                     jmp 0x48aa98
0048aab7 83fe41                   cmp esi, 0x41
0048aaba 74d6                     je 0x48aa92
0048aabc 5e                       pop esi
0048aabd c20400                   ret 4
; PlaySnd_StopSound
0048aac0 e973f9ffff               jmp 0x48a438
; PlaySnd_StopAllSound
0048aac5 e9def9ffff               jmp 0x48a4a8
; PlaySnd_Manage
0048aaca e92afdffff               jmp 0x48a7f9
; PlaySnd_PostVolume
0048aacf e976f6ffff               jmp 0x48a14a
; PSB_CreateMySurfaceWithSound
0048aad4 53                       push ebx
0048aad5 51                       push ecx
0048aad6 56                       push esi
0048aad7 57                       push edi
0048aad8 55                       push ebp
0048aad9 89c6                     mov esi, eax
0048aadb 89d7                     mov edi, edx
0048aadd 8b5210                   mov edx, dword ptr [edx + 0x10]
0048aae0 31ed                     xor ebp, ebp
0048aae2 85d2                     test edx, edx
0048aae4 0f850a000000             jne 0x48aaf4
0048aaea 8b4708                   mov eax, dword ptr [edi + 8]
0048aaed 31db                     xor ebx, ebx
0048aaef e86a150000               call 0x48c05e
0048aaf4 8a460c                   mov al, byte ptr [esi + 0xc]
0048aaf7 84c0                     test al, al
0048aaf9 760c                     jbe 0x48ab07
0048aafb 3c04                     cmp al, 4
0048aafd 745a                     je 0x48ab59
0048aaff 89e8                     mov eax, ebp
0048ab01 5d                       pop ebp
0048ab02 5f                       pop edi
0048ab03 5e                       pop esi
0048ab04 59                       pop ecx
0048ab05 5b                       pop ebx
0048ab06 c3                       ret
0048ab07 8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab0a 31db                     xor ebx, ebx
0048ab0c 31d2                     xor edx, edx
0048ab0e 31c0                     xor eax, eax
0048ab10 8a5e09                   mov bl, byte ptr [esi + 9]
0048ab13 668b560a                 mov dx, word ptr [esi + 0xa]
0048ab17 8a4608                   mov al, byte ptr [esi + 8]
0048ab1a e8920c0000               call 0x48b7b1
0048ab1f 89c1                     mov ecx, eax
0048ab21 89c5                     mov ebp, eax
0048ab23 85c0                     test eax, eax
0048ab25 74da                     je 0x48ab01
0048ab27 837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab2b 7513                     jne 0x48ab40
0048ab2d 8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab30 8b1e                     mov ebx, dword ptr [esi]
0048ab32 89c8                     mov eax, ecx
0048ab34 01da                     add edx, ebx
0048ab36 8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab39 e86a160000               call 0x48c1a8
0048ab3e ebbf                     jmp 0x48aaff
0048ab40 8b16                     mov edx, dword ptr [esi]
0048ab42 8b4708                   mov eax, dword ptr [edi + 8]
0048ab45 e8ed150000               call 0x48c137
0048ab4a 89c8                     mov eax, ecx
0048ab4c 8b5e04                   mov ebx, dword ptr [esi + 4]
0048ab4f 8b5708                   mov edx, dword ptr [edi + 8]
0048ab52 e819150000               call 0x48c070
0048ab57 eba6                     jmp 0x48aaff
0048ab59 8b4e04                   mov ecx, dword ptr [esi + 4]
0048ab5c 31db                     xor ebx, ebx
0048ab5e 31d2                     xor edx, edx
0048ab60 31c0                     xor eax, eax
0048ab62 c1e102                   shl ecx, 2
0048ab65 8a5e09                   mov bl, byte ptr [esi + 9]
0048ab68 668b560a                 mov dx, word ptr [esi + 0xa]
0048ab6c 8a4608                   mov al, byte ptr [esi + 8]
0048ab6f e83d0c0000               call 0x48b7b1
0048ab74 89c5                     mov ebp, eax
0048ab76 85c0                     test eax, eax
0048ab78 7487                     je 0x48ab01
0048ab7a 837f1001                 cmp dword ptr [edi + 0x10], 1
0048ab7e 7507                     jne 0x48ab87
0048ab80 8b5714                   mov edx, dword ptr [edi + 0x14]
0048ab83 0316                     add edx, dword ptr [esi]
0048ab85 eb17                     jmp 0x48ab9e
0048ab87 8b16                     mov edx, dword ptr [esi]
0048ab89 8b4708                   mov eax, dword ptr [edi + 8]
0048ab8c e8a6150000               call 0x48c137
0048ab91 8b5604                   mov edx, dword ptr [esi + 4]
0048ab94 8b4708                   mov eax, dword ptr [edi + 8]
0048ab97 e8a5150000               call 0x48c141
0048ab9c 89c2                     mov edx, eax
0048ab9e 31c0                     xor eax, eax
0048aba0 8b5e04                   mov ebx, dword ptr [esi + 4]
0048aba3 8a4608                   mov al, byte ptr [esi + 8]
0048aba6 31c9                     xor ecx, ecx
0048aba8 50                       push eax
0048aba9 668b4e0e                 mov cx, word ptr [esi + 0xe]
0048abad 89e8                     mov eax, ebp
0048abaf e808150000               call 0x48c0bc
0048abb4 e946ffffff               jmp 0x48aaff
; PSB_FindFirstFreePlace
0048abb9 53                       push ebx
0048abba 52                       push edx
0048abbb 8b15608f4900             mov edx, dword ptr [0x498f60]
0048abc1 83fa09                   cmp edx, 9
0048abc4 7c08                     jl 0x48abce
0048abc6 b8ffffffff               mov eax, 0xffffffff
0048abcb 5a                       pop edx
0048abcc 5b                       pop ebx
0048abcd c3                       ret
0048abce 8d5a01                   lea ebx, [edx + 1]
0048abd1 891d608f4900             mov dword ptr [0x498f60], ebx
0048abd7 89d8                     mov eax, ebx
0048abd9 5a                       pop edx
0048abda 5b                       pop ebx
0048abdb c3                       ret
; PSB_ReplaceLastSoundInFreePlace
0048abdc 53                       push ebx
0048abdd 52                       push edx
0048abde 56                       push esi
0048abdf 8b15608f4900             mov edx, dword ptr [0x498f60]
0048abe5 85d2                     test edx, edx
0048abe7 7d06                     jge 0x48abef
0048abe9 31c0                     xor eax, eax
0048abeb 5e                       pop esi
0048abec 5a                       pop edx
0048abed 5b                       pop ebx
0048abee c3                       ret
0048abef bb1c215200               mov ebx, 0x52211c
0048abf4 c1e203                   shl edx, 3
0048abf7 01d3                     add ebx, edx
0048abf9 39d8                     cmp eax, ebx
0048abfb 750f                     jne 0x48ac0c
0048abfd b801000000               mov eax, 1
0048ac02 2905608f4900             sub dword ptr [0x498f60], eax
0048ac08 5e                       pop esi
0048ac09 5a                       pop edx
0048ac0a 5b                       pop ebx
0048ac0b c3                       ret
0048ac0c 8b921c215200             mov edx, dword ptr [edx + 0x52211c]
0048ac12 8910                     mov dword ptr [eax], edx
0048ac14 8b15608f4900             mov edx, dword ptr [0x498f60]
0048ac1a 8b14d520215200           mov edx, dword ptr [edx*8 + 0x522120]
0048ac21 895004                   mov dword ptr [eax + 4], edx
0048ac24 894220                   mov dword ptr [edx + 0x20], eax
0048ac27 a1608f4900               mov eax, dword ptr [0x498f60]
0048ac2c 31db                     xor ebx, ebx
0048ac2e 891cc51c215200           mov dword ptr [eax*8 + 0x52211c], ebx
0048ac35 8b35608f4900             mov esi, dword ptr [0x498f60]
0048ac3b 891cc520215200           mov dword ptr [eax*8 + 0x522120], ebx
0048ac42 b801000000               mov eax, 1
0048ac47 29c6                     sub esi, eax
0048ac49 8935608f4900             mov dword ptr [0x498f60], esi
0048ac4f 5e                       pop esi
0048ac50 5a                       pop edx
0048ac51 5b                       pop ebx
0048ac52 c3                       ret
; PSB_DestroyPhyBuff
0048ac53 52                       push edx
0048ac54 89c2                     mov edx, eax
0048ac56 8b00                     mov eax, dword ptr [eax]
0048ac58 e833120000               call 0x48be90
0048ac5d 85c0                     test eax, eax
0048ac5f 7407                     je 0x48ac68
0048ac61 8b02                     mov eax, dword ptr [edx]
0048ac63 e80c130000               call 0x48bf74
0048ac68 89d0                     mov eax, edx
0048ac6a e8250b0000               call 0x48b794
0048ac6f c7420400000000           mov dword ptr [edx + 4], 0
0048ac76 5a                       pop edx
0048ac77 c3                       ret
; PSB_CreatePhySound
0048ac78 53                       push ebx
0048ac79 51                       push ecx
0048ac7a 52                       push edx
0048ac7b 56                       push esi
0048ac7c 89c3                     mov ebx, eax
0048ac7e 8b15608f4900             mov edx, dword ptr [0x498f60]
0048ac84 83fa09                   cmp edx, 9
0048ac87 7c07                     jl 0x48ac90
0048ac89 b9ffffffff               mov ecx, 0xffffffff
0048ac8e eb09                     jmp 0x48ac99
0048ac90 8d4a01                   lea ecx, [edx + 1]
0048ac93 890d608f4900             mov dword ptr [0x498f60], ecx
0048ac99 83f9ff                   cmp ecx, -1
0048ac9c 7507                     jne 0x48aca5
0048ac9e 31c0                     xor eax, eax
0048aca0 5e                       pop esi
0048aca1 5a                       pop edx
0048aca2 59                       pop ecx
0048aca3 5b                       pop ebx
0048aca4 c3                       ret
0048aca5 8b5304                   mov edx, dword ptr [ebx + 4]
0048aca8 8b431c                   mov eax, dword ptr [ebx + 0x1c]
0048acab e824feffff               call 0x48aad4
0048acb0 89c2                     mov edx, eax
0048acb2 89c8                     mov eax, ecx
0048acb4 c1e003                   shl eax, 3
0048acb7 89d6                     mov esi, edx
0048acb9 89901c215200             mov dword ptr [eax + 0x52211c], edx
0048acbf 85f6                     test esi, esi
0048acc1 74db                     je 0x48ac9e
0048acc3 899820215200             mov dword ptr [eax + 0x522120], ebx
0048acc9 051c215200               add eax, 0x52211c
0048acce 5e                       pop esi
0048accf 5a                       pop edx
0048acd0 59                       pop ecx
0048acd1 5b                       pop ebx
0048acd2 c3                       ret
; PSB_IsThisSoundLoaded
0048acd3 53                       push ebx
0048acd4 51                       push ecx
0048acd5 56                       push esi
0048acd6 89c1                     mov ecx, eax
0048acd8 89d6                     mov esi, edx
0048acda 8b1d608f4900             mov ebx, dword ptr [0x498f60]
0048ace0 31c0                     xor eax, eax
0048ace2 c1e303                   shl ebx, 3
0048ace5 eb03                     jmp 0x48acea
0048ace7 83c008                   add eax, 8
0048acea 39d8                     cmp eax, ebx
0048acec 7f18                     jg 0x48ad06
0048acee 8b9020215200             mov edx, dword ptr [eax + 0x522120]
0048acf4 3b0a                     cmp ecx, dword ptr [edx]
0048acf6 75ef                     jne 0x48ace7
0048acf8 3b7204                   cmp esi, dword ptr [edx + 4]
0048acfb 75ea                     jne 0x48ace7
0048acfd 051c215200               add eax, 0x52211c
0048ad02 5e                       pop esi
0048ad03 59                       pop ecx
0048ad04 5b                       pop ebx
0048ad05 c3                       ret
0048ad06 31c0                     xor eax, eax
0048ad08 5e                       pop esi
0048ad09 59                       pop ecx
0048ad0a 5b                       pop ebx
0048ad0b c3                       ret
; PSB_TranfertLogicalSoundInPhysicalTable
0048ad0c 53                       push ebx
0048ad0d 51                       push ecx
0048ad0e 89d3                     mov ebx, edx
0048ad10 8b5220                   mov edx, dword ptr [edx + 0x20]
0048ad13 8b0a                     mov ecx, dword ptr [edx]
0048ad15 8908                     mov dword ptr [eax], ecx
0048ad17 895804                   mov dword ptr [eax + 4], ebx
0048ad1a c70200000000             mov dword ptr [edx], 0
0048ad20 c7420400000000           mov dword ptr [edx + 4], 0
0048ad27 59                       pop ecx
0048ad28 5b                       pop ebx
0048ad29 c3                       ret
; PSB_IsFullListe
0048ad2a 833d608f490009           cmp dword ptr [0x498f60], 9
0048ad31 0f9dc0                   setge al
0048ad34 25ff000000               and eax, 0xff
0048ad39 c3                       ret
; LSB_ReplaceLastSoundInFreePlace
0048ad3c 53                       push ebx
0048ad3d 52                       push edx
0048ad3e 56                       push esi
0048ad3f 8b15648f4900             mov edx, dword ptr [0x498f64]
0048ad45 85d2                     test edx, edx
0048ad47 7d06                     jge 0x48ad4f
0048ad49 31c0                     xor eax, eax
0048ad4b 5e                       pop esi
0048ad4c 5a                       pop edx
0048ad4d 5b                       pop ebx
0048ad4e c3                       ret
0048ad4f bb6c215200               mov ebx, 0x52216c
0048ad54 c1e203                   shl edx, 3
0048ad57 01d3                     add ebx, edx
0048ad59 39d8                     cmp eax, ebx
0048ad5b 750f                     jne 0x48ad6c
0048ad5d b801000000               mov eax, 1
0048ad62 2905648f4900             sub dword ptr [0x498f64], eax
0048ad68 5e                       pop esi
0048ad69 5a                       pop edx
0048ad6a 5b                       pop ebx
0048ad6b c3                       ret
0048ad6c 8b926c215200             mov edx, dword ptr [edx + 0x52216c]
0048ad72 8910                     mov dword ptr [eax], edx
0048ad74 8b15648f4900             mov edx, dword ptr [0x498f64]
0048ad7a 8b14d570215200           mov edx, dword ptr [edx*8 + 0x522170]
0048ad81 895004                   mov dword ptr [eax + 4], edx
0048ad84 894220                   mov dword ptr [edx + 0x20], eax
0048ad87 a1648f4900               mov eax, dword ptr [0x498f64]
0048ad8c 31db                     xor ebx, ebx
0048ad8e 891cc56c215200           mov dword ptr [eax*8 + 0x52216c], ebx
0048ad95 8b35648f4900             mov esi, dword ptr [0x498f64]
0048ad9b 891cc570215200           mov dword ptr [eax*8 + 0x522170], ebx
0048ada2 b801000000               mov eax, 1
0048ada7 29c6                     sub esi, eax
0048ada9 8935648f4900             mov dword ptr [0x498f64], esi
0048adaf 5e                       pop esi
0048adb0 5a                       pop edx
0048adb1 5b                       pop ebx
0048adb2 c3                       ret
; LSB_DestroyLogBuff
0048adb3 53                       push ebx
0048adb4 51                       push ecx
0048adb5 52                       push edx
0048adb6 57                       push edi
0048adb7 89c2                     mov edx, eax
0048adb9 8b00                     mov eax, dword ptr [eax]
0048adbb e8d0100000               call 0x48be90
0048adc0 85c0                     test eax, eax
0048adc2 7407                     je 0x48adcb
0048adc4 8b02                     mov eax, dword ptr [edx]
0048adc6 e8a9110000               call 0x48bf74
0048adcb 89d0                     mov eax, edx
0048adcd e8c2090000               call 0x48b794
0048add2 c7420400000000           mov dword ptr [edx + 4], 0
0048add9 8b1d648f4900             mov ebx, dword ptr [0x498f64]
0048addf 85db                     test ebx, ebx
0048ade1 7c54                     jl 0x48ae37
0048ade3 89d8                     mov eax, ebx
0048ade5 bb6c215200               mov ebx, 0x52216c
0048adea c1e003                   shl eax, 3
0048aded 01c3                     add ebx, eax
0048adef 39da                     cmp edx, ebx
0048adf1 750b                     jne 0x48adfe
0048adf3 ff0d648f4900             dec dword ptr [0x498f64]
0048adf9 5f                       pop edi
0048adfa 5a                       pop edx
0048adfb 59                       pop ecx
0048adfc 5b                       pop ebx
0048adfd c3                       ret
0048adfe 8b806c215200             mov eax, dword ptr [eax + 0x52216c]
0048ae04 8902                     mov dword ptr [edx], eax
0048ae06 a1648f4900               mov eax, dword ptr [0x498f64]
0048ae0b 8b04c570215200           mov eax, dword ptr [eax*8 + 0x522170]
0048ae12 894204                   mov dword ptr [edx + 4], eax
0048ae15 895020                   mov dword ptr [eax + 0x20], edx
0048ae18 8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae1e 31c9                     xor ecx, ecx
0048ae20 890cd56c215200           mov dword ptr [edx*8 + 0x52216c], ecx
0048ae27 8d7aff                   lea edi, [edx - 1]
0048ae2a 890cd570215200           mov dword ptr [edx*8 + 0x522170], ecx
0048ae31 893d648f4900             mov dword ptr [0x498f64], edi
0048ae37 5f                       pop edi
0048ae38 5a                       pop edx
0048ae39 59                       pop ecx
0048ae3a 5b                       pop ebx
0048ae3b c3                       ret
; LSB_FindFirstFreePlace
0048ae3c 53                       push ebx
0048ae3d 52                       push edx
0048ae3e 8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae44 83fa09                   cmp edx, 9
0048ae47 7c08                     jl 0x48ae51
0048ae49 b8ffffffff               mov eax, 0xffffffff
0048ae4e 5a                       pop edx
0048ae4f 5b                       pop ebx
0048ae50 c3                       ret
0048ae51 8d5a01                   lea ebx, [edx + 1]
0048ae54 891d648f4900             mov dword ptr [0x498f64], ebx
0048ae5a 89d8                     mov eax, ebx
0048ae5c 5a                       pop edx
0048ae5d 5b                       pop ebx
0048ae5e c3                       ret
; LSB_CreateLogicalSound
0048ae5f 53                       push ebx
0048ae60 51                       push ecx
0048ae61 56                       push esi
0048ae62 89d1                     mov ecx, edx
0048ae64 8b15648f4900             mov edx, dword ptr [0x498f64]
0048ae6a 83fa09                   cmp edx, 9
0048ae6d 7c07                     jl 0x48ae76
0048ae6f baffffffff               mov edx, 0xffffffff
0048ae74 eb0b                     jmp 0x48ae81
0048ae76 8d5a01                   lea ebx, [edx + 1]
0048ae79 891d648f4900             mov dword ptr [0x498f64], ebx
0048ae7f 89da                     mov edx, ebx
0048ae81 83faff                   cmp edx, -1
0048ae84 7506                     jne 0x48ae8c
0048ae86 31c0                     xor eax, eax
0048ae88 5e                       pop esi
0048ae89 59                       pop ecx
0048ae8a 5b                       pop ebx
0048ae8b c3                       ret
0048ae8c e828110000               call 0x48bfb9
0048ae91 89c3                     mov ebx, eax
0048ae93 89d0                     mov eax, edx
0048ae95 c1e003                   shl eax, 3
0048ae98 89de                     mov esi, ebx
0048ae9a 89986c215200             mov dword ptr [eax + 0x52216c], ebx
0048aea0 85f6                     test esi, esi
0048aea2 74e2                     je 0x48ae86
0048aea4 898870215200             mov dword ptr [eax + 0x522170], ecx
0048aeaa 056c215200               add eax, 0x52216c
0048aeaf 5e                       pop esi
0048aeb0 59                       pop ecx
0048aeb1 5b                       pop ebx
0048aeb2 c3                       ret
; LSB_IsThisSoundPresent
0048aeb3 53                       push ebx
0048aeb4 51                       push ecx
0048aeb5 56                       push esi
0048aeb6 89c1                     mov ecx, eax
0048aeb8 89d6                     mov esi, edx
0048aeba 8b1d648f4900             mov ebx, dword ptr [0x498f64]
0048aec0 31c0                     xor eax, eax
0048aec2 c1e303                   shl ebx, 3
0048aec5 eb03                     jmp 0x48aeca
0048aec7 83c008                   add eax, 8
0048aeca 39d8                     cmp eax, ebx
0048aecc 7f11                     jg 0x48aedf
0048aece 8b9070215200             mov edx, dword ptr [eax + 0x522170]
0048aed4 3b0a                     cmp ecx, dword ptr [edx]
0048aed6 75ef                     jne 0x48aec7
0048aed8 3b7204                   cmp esi, dword ptr [edx + 4]
0048aedb 75ea                     jne 0x48aec7
0048aedd eb02                     jmp 0x48aee1
0048aedf 31d2                     xor edx, edx
0048aee1 89d0                     mov eax, edx
0048aee3 5e                       pop esi
0048aee4 59                       pop ecx
0048aee5 5b                       pop ebx
0048aee6 c3                       ret
; LSB_IsFullListe
0048aee7 833d648f490009           cmp dword ptr [0x498f64], 9
0048aeee 0f9dc0                   setge al
0048aef1 25ff000000               and eax, 0xff
0048aef6 c3                       ret
; WaitSnd_GetFirstFreePlace
0048aef8 53                       push ebx
0048aef9 52                       push edx
0048aefa 8b15688f4900             mov edx, dword ptr [0x498f68]
0048af00 83fa46                   cmp edx, 0x46
0048af03 7508                     jne 0x48af0d
0048af05 b8ffffffff               mov eax, 0xffffffff
0048af0a 5a                       pop edx
0048af0b 5b                       pop ebx
0048af0c c3                       ret
0048af0d 8d5a01                   lea ebx, [edx + 1]
0048af10 891d688f4900             mov dword ptr [0x498f68], ebx
0048af16 89d8                     mov eax, ebx
0048af18 5a                       pop edx
0048af19 5b                       pop ebx
0048af1a c3                       ret
; WaitSnd_Compact
0048af1b 53                       push ebx
0048af1c 51                       push ecx
0048af1d 56                       push esi
0048af1e 57                       push edi
0048af1f 55                       push ebp
0048af20 89c3                     mov ebx, eax
0048af22 8b4028                   mov eax, dword ptr [eax + 0x28]
0048af25 8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048af2b 8b28                     mov ebp, dword ptr [eax]
0048af2d 83f913                   cmp ecx, 0x13
0048af30 7507                     jne 0x48af39
0048af32 31c0                     xor eax, eax
0048af34 e991000000               jmp 0x48afca
0048af39 85d2                     test edx, edx
0048af3b 7406                     je 0x48af43
0048af3d c700ffffffff             mov dword ptr [eax], 0xffffffff
0048af43 8b15688f4900             mov edx, dword ptr [0x498f68]
0048af49 89d0                     mov eax, edx
0048af4b c1e002                   shl eax, 2
0048af4e 29d0                     sub eax, edx
0048af50 c1e002                   shl eax, 2
0048af53 29d0                     sub eax, edx
0048af55 be7c135200               mov esi, 0x52137c
0048af5a c1e002                   shl eax, 2
0048af5d 01c6                     add esi, eax
0048af5f 39de                     cmp esi, ebx
0048af61 751d                     jne 0x48af80
0048af63 30f6                     xor dh, dh
0048af65 8b3d688f4900             mov edi, dword ptr [0x498f68]
0048af6b 88b084135200             mov byte ptr [eax + 0x521384], dh
0048af71 b801000000               mov eax, 1
0048af76 29c7                     sub edi, eax
0048af78 893d688f4900             mov dword ptr [0x498f68], edi
0048af7e eb4a                     jmp 0x48afca
0048af80 b92c000000               mov ecx, 0x2c
0048af85 89df                     mov edi, ebx
0048af87 57                       push edi
0048af88 89c8                     mov eax, ecx
0048af8a c1e902                   shr ecx, 2
0048af8d f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048af8f 8ac8                     mov cl, al
0048af91 80e103                   and cl, 3
0048af94 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048af96 5f                       pop edi
0048af97 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048af9a 8928                     mov dword ptr [eax], ebp
0048af9c 8b15688f4900             mov edx, dword ptr [0x498f68]
0048afa2 89d0                     mov eax, edx
0048afa4 c1e002                   shl eax, 2
0048afa7 29d0                     sub eax, edx
0048afa9 c1e002                   shl eax, 2
0048afac 29d0                     sub eax, edx
0048afae 30d2                     xor dl, dl
0048afb0 8b35688f4900             mov esi, dword ptr [0x498f68]
0048afb6 88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048afbd b801000000               mov eax, 1
0048afc2 29c6                     sub esi, eax
0048afc4 8935688f4900             mov dword ptr [0x498f68], esi
0048afca 5d                       pop ebp
0048afcb 5f                       pop edi
0048afcc 5e                       pop esi
0048afcd 59                       pop ecx
0048afce 5b                       pop ebx
0048afcf c3                       ret
; WaitSnd_SorryGiveBackOnePlace
0048afd0 53                       push ebx
0048afd1 52                       push edx
0048afd2 8b15688f4900             mov edx, dword ptr [0x498f68]
0048afd8 83fa13                   cmp edx, 0x13
0048afdb 7409                     je 0x48afe6
0048afdd 8d5aff                   lea ebx, [edx - 1]
0048afe0 891d688f4900             mov dword ptr [0x498f68], ebx
0048afe6 5a                       pop edx
0048afe7 5b                       pop ebx
0048afe8 c3                       ret
; WaitSnd_GetMaxIndice
0048afe9 a1688f4900               mov eax, dword ptr [0x498f68]
0048afee c3                       ret
; WaitSnd_FindPlace
0048afef 53                       push ebx
0048aff0 52                       push edx
0048aff1 31d2                     xor edx, edx
0048aff3 31c0                     xor eax, eax
0048aff5 eb04                     jmp 0x48affb
0048aff7 83c02c                   add eax, 0x2c
0048affa 42                       inc edx
0048affb 3d70030000               cmp eax, 0x370
0048b000 7d11                     jge 0x48b013
0048b002 31db                     xor ebx, ebx
0048b004 8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048b00a 85db                     test ebx, ebx
0048b00c 75e9                     jne 0x48aff7
0048b00e 89d0                     mov eax, edx
0048b010 5a                       pop edx
0048b011 5b                       pop ebx
0048b012 c3                       ret
0048b013 b8ffffffff               mov eax, 0xffffffff
0048b018 5a                       pop edx
0048b019 5b                       pop ebx
0048b01a c3                       ret
; WaitSnd_TransferPlayingSoundToWaitingSound
0048b01b 53                       push ebx
0048b01c 51                       push ecx
0048b01d 52                       push edx
0048b01e 56                       push esi
0048b01f 57                       push edi
0048b020 55                       push ebp
0048b021 8b15688f4900             mov edx, dword ptr [0x498f68]
0048b027 83fa46                   cmp edx, 0x46
0048b02a 7507                     jne 0x48b033
0048b02c bdffffffff               mov ebp, 0xffffffff
0048b031 eb0b                     jmp 0x48b03e
0048b033 8d5a01                   lea ebx, [edx + 1]
0048b036 891d688f4900             mov dword ptr [0x498f68], ebx
0048b03c 89dd                     mov ebp, ebx
0048b03e 83fdff                   cmp ebp, -1
0048b041 7507                     jne 0x48b04a
0048b043 31c0                     xor eax, eax
0048b045 e982000000               jmp 0x48b0cc
0048b04a be7c135200               mov esi, 0x52137c
0048b04f bf7c135200               mov edi, 0x52137c
0048b054 b92c000000               mov ecx, 0x2c
0048b059 89c3                     mov ebx, eax
0048b05b 89ea                     mov edx, ebp
0048b05d c1e302                   shl ebx, 2
0048b060 c1e202                   shl edx, 2
0048b063 29c3                     sub ebx, eax
0048b065 29ea                     sub edx, ebp
0048b067 c1e302                   shl ebx, 2
0048b06a c1e202                   shl edx, 2
0048b06d 29c3                     sub ebx, eax
0048b06f 29ea                     sub edx, ebp
0048b071 c1e302                   shl ebx, 2
0048b074 c1e202                   shl edx, 2
0048b077 01de                     add esi, ebx
0048b079 01d7                     add edi, edx
0048b07b 57                       push edi
0048b07c 89c8                     mov eax, ecx
0048b07e c1e902                   shr ecx, 2
0048b081 f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b083 8ac8                     mov cl, al
0048b085 80e103                   and cl, 3
0048b088 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b08a 5f                       pop edi
0048b08b c6828413520002           mov byte ptr [edx + 0x521384], 2
0048b092 31c9                     xor ecx, ecx
0048b094 8b82a4135200             mov eax, dword ptr [edx + 0x5213a4]
0048b09a 898a9c135200             mov dword ptr [edx + 0x52139c], ecx
0048b0a0 8928                     mov dword ptr [eax], ebp
0048b0a2 30d2                     xor dl, dl
0048b0a4 8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048b0aa 8bb3a0135200             mov esi, dword ptr [ebx + 0x5213a0]
0048b0b0 889384135200             mov byte ptr [ebx + 0x521384], dl
0048b0b6 83fe01                   cmp esi, 1
0048b0b9 7507                     jne 0x48b0c2
0048b0bb e8f3fcffff               call 0x48adb3
0048b0c0 eb05                     jmp 0x48b0c7
0048b0c2 e88cfbffff               call 0x48ac53
0048b0c7 b801000000               mov eax, 1
0048b0cc 5d                       pop ebp
0048b0cd 5f                       pop edi
0048b0ce 5e                       pop esi
0048b0cf 5a                       pop edx
0048b0d0 59                       pop ecx
0048b0d1 5b                       pop ebx
0048b0d2 c3                       ret
; WaitSnd_TransferALLPlayingSoundToWaitingSound
0048b0d3 53                       push ebx
0048b0d4 51                       push ecx
0048b0d5 56                       push esi
0048b0d6 57                       push edi
0048b0d7 89c7                     mov edi, eax
0048b0d9 89d6                     mov esi, edx
0048b0db 31c9                     xor ecx, ecx
0048b0dd 31db                     xor ebx, ebx
0048b0df 31d2                     xor edx, edx
0048b0e1 eb09                     jmp 0x48b0ec
0048b0e3 43                       inc ebx
0048b0e4 83c22c                   add edx, 0x2c
0048b0e7 83fb14                   cmp ebx, 0x14
0048b0ea 7d2a                     jge 0x48b116
0048b0ec 31c0                     xor eax, eax
0048b0ee 8a8284135200             mov al, byte ptr [edx + 0x521384]
0048b0f4 85c0                     test eax, eax
0048b0f6 74eb                     je 0x48b0e3
0048b0f8 3bba7c135200             cmp edi, dword ptr [edx + 0x52137c]
0048b0fe 75e3                     jne 0x48b0e3
0048b100 3bb280135200             cmp esi, dword ptr [edx + 0x521380]
0048b106 75db                     jne 0x48b0e3
0048b108 89d8                     mov eax, ebx
0048b10a b901000000               mov ecx, 1
0048b10f e807ffffff               call 0x48b01b
0048b114 ebcd                     jmp 0x48b0e3
0048b116 89c8                     mov eax, ecx
0048b118 5f                       pop edi
0048b119 5e                       pop esi
0048b11a 59                       pop ecx
0048b11b 5b                       pop ebx
0048b11c c3                       ret
; WaitSnd_DestroyWaitingSound
0048b11d 53                       push ebx
0048b11e 51                       push ecx
0048b11f 52                       push edx
0048b120 56                       push esi
0048b121 57                       push edi
0048b122 55                       push ebp
0048b123 89c3                     mov ebx, eax
0048b125 c1e002                   shl eax, 2
0048b128 29d8                     sub eax, ebx
0048b12a 8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b130 c1e002                   shl eax, 2
0048b133 8b15688f4900             mov edx, dword ptr [0x498f68]
0048b139 29d8                     sub eax, ebx
0048b13b 49                       dec ecx
0048b13c c1e002                   shl eax, 2
0048b13f 39d3                     cmp ebx, edx
0048b141 7515                     jne 0x48b158
0048b143 30d3                     xor bl, dl
0048b145 890d688f4900             mov dword ptr [0x498f68], ecx
0048b14b 889884135200             mov byte ptr [eax + 0x521384], bl
0048b151 31c0                     xor eax, eax
0048b153 e974ffffff               jmp 0x48b0cc
0048b158 ba7c135200               mov edx, 0x52137c
0048b15d 01c2                     add edx, eax
0048b15f 8b4228                   mov eax, dword ptr [edx + 0x28]
0048b162 8b1d688f4900             mov ebx, dword ptr [0x498f68]
0048b168 8b28                     mov ebp, dword ptr [eax]
0048b16a 83fb13                   cmp ebx, 0x13
0048b16d 0f8454ffffff             je 0x48b0c7
0048b173 89d8                     mov eax, ebx
0048b175 c1e002                   shl eax, 2
0048b178 29d8                     sub eax, ebx
0048b17a c1e002                   shl eax, 2
0048b17d 29d8                     sub eax, ebx
0048b17f be7c135200               mov esi, 0x52137c
0048b184 c1e002                   shl eax, 2
0048b187 01c6                     add esi, eax
0048b189 39d6                     cmp esi, edx
0048b18b 7513                     jne 0x48b1a0
0048b18d 30f6                     xor dh, dh
0048b18f 890d688f4900             mov dword ptr [0x498f68], ecx
0048b195 88b084135200             mov byte ptr [eax + 0x521384], dh
0048b19b e927ffffff               jmp 0x48b0c7
0048b1a0 b92c000000               mov ecx, 0x2c
0048b1a5 89d7                     mov edi, edx
0048b1a7 57                       push edi
0048b1a8 89c8                     mov eax, ecx
0048b1aa c1e902                   shr ecx, 2
0048b1ad f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b1af 8ac8                     mov cl, al
0048b1b1 80e103                   and cl, 3
0048b1b4 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b1b6 5f                       pop edi
0048b1b7 8b4228                   mov eax, dword ptr [edx + 0x28]
0048b1ba 8928                     mov dword ptr [eax], ebp
0048b1bc 8b15688f4900             mov edx, dword ptr [0x498f68]
0048b1c2 89d0                     mov eax, edx
0048b1c4 c1e002                   shl eax, 2
0048b1c7 29d0                     sub eax, edx
0048b1c9 8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b1cf c1e002                   shl eax, 2
0048b1d2 49                       dec ecx
0048b1d3 29d0                     sub eax, edx
0048b1d5 30d2                     xor dl, dl
0048b1d7 890d688f4900             mov dword ptr [0x498f68], ecx
0048b1dd 88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048b1e4 e9defeffff               jmp 0x48b0c7
; WaitSnd_TransferWaitingSoundToPlayingSound
0048b1e9 53                       push ebx
0048b1ea 51                       push ecx
0048b1eb 52                       push edx
0048b1ec 56                       push esi
0048b1ed 57                       push edi
0048b1ee 55                       push ebp
0048b1ef 89c6                     mov esi, eax
0048b1f1 31d2                     xor edx, edx
0048b1f3 31c0                     xor eax, eax
0048b1f5 eb04                     jmp 0x48b1fb
0048b1f7 83c02c                   add eax, 0x2c
0048b1fa 42                       inc edx
0048b1fb 3d70030000               cmp eax, 0x370
0048b200 7d10                     jge 0x48b212
0048b202 31db                     xor ebx, ebx
0048b204 8a9884135200             mov bl, byte ptr [eax + 0x521384]
0048b20a 85db                     test ebx, ebx
0048b20c 75e9                     jne 0x48b1f7
0048b20e 89d5                     mov ebp, edx
0048b210 eb05                     jmp 0x48b217
0048b212 bdffffffff               mov ebp, 0xffffffff
0048b217 83fdff                   cmp ebp, -1
0048b21a 7507                     jne 0x48b223
0048b21c 31c0                     xor eax, eax
0048b21e e9a9feffff               jmp 0x48b0cc
0048b223 ba7c135200               mov edx, 0x52137c
0048b228 89f0                     mov eax, esi
0048b22a 89eb                     mov ebx, ebp
0048b22c c1e002                   shl eax, 2
0048b22f c1e302                   shl ebx, 2
0048b232 29f0                     sub eax, esi
0048b234 29eb                     sub ebx, ebp
0048b236 c1e002                   shl eax, 2
0048b239 c1e302                   shl ebx, 2
0048b23c 29f0                     sub eax, esi
0048b23e 29eb                     sub ebx, ebp
0048b240 c1e002                   shl eax, 2
0048b243 c1e302                   shl ebx, 2
0048b246 01c2                     add edx, eax
0048b248 b87c135200               mov eax, 0x52137c
0048b24d b92c000000               mov ecx, 0x2c
0048b252 01d8                     add eax, ebx
0048b254 89d6                     mov esi, edx
0048b256 89c7                     mov edi, eax
0048b258 57                       push edi
0048b259 89c8                     mov eax, ecx
0048b25b c1e902                   shr ecx, 2
0048b25e f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b260 8ac8                     mov cl, al
0048b262 80e103                   and cl, 3
0048b265 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b267 5f                       pop edi
0048b268 8b83a4135200             mov eax, dword ptr [ebx + 0x5213a4]
0048b26e 8928                     mov dword ptr [eax], ebp
0048b270 8b839c135200             mov eax, dword ptr [ebx + 0x52139c]
0048b276 89fe                     mov esi, edi
0048b278 897004                   mov dword ptr [eax + 4], esi
0048b27b c6838413520001           mov byte ptr [ebx + 0x521384], 1
0048b282 8b4228                   mov eax, dword ptr [edx + 0x28]
0048b285 8b1d688f4900             mov ebx, dword ptr [0x498f68]
0048b28b 8b28                     mov ebp, dword ptr [eax]
0048b28d 83fb13                   cmp ebx, 0x13
0048b290 748a                     je 0x48b21c
0048b292 89d8                     mov eax, ebx
0048b294 c1e002                   shl eax, 2
0048b297 29d8                     sub eax, ebx
0048b299 c1e002                   shl eax, 2
0048b29c 29d8                     sub eax, ebx
0048b29e be7c135200               mov esi, 0x52137c
0048b2a3 c1e002                   shl eax, 2
0048b2a6 01c6                     add esi, eax
0048b2a8 39d6                     cmp esi, edx
0048b2aa 751c                     jne 0x48b2c8
0048b2ac 30f6                     xor dh, dh
0048b2ae 89de                     mov esi, ebx
0048b2b0 88b084135200             mov byte ptr [eax + 0x521384], dh
0048b2b6 b801000000               mov eax, 1
0048b2bb 29c6                     sub esi, eax
0048b2bd 8935688f4900             mov dword ptr [0x498f68], esi
0048b2c3 e904feffff               jmp 0x48b0cc
0048b2c8 b92c000000               mov ecx, 0x2c
0048b2cd 89d7                     mov edi, edx
0048b2cf 57                       push edi
0048b2d0 89c8                     mov eax, ecx
0048b2d2 c1e902                   shr ecx, 2
0048b2d5 f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b2d7 8ac8                     mov cl, al
0048b2d9 80e103                   and cl, 3
0048b2dc f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b2de 5f                       pop edi
0048b2df 8b4228                   mov eax, dword ptr [edx + 0x28]
0048b2e2 8928                     mov dword ptr [eax], ebp
0048b2e4 8b15688f4900             mov edx, dword ptr [0x498f68]
0048b2ea 89d0                     mov eax, edx
0048b2ec c1e002                   shl eax, 2
0048b2ef 29d0                     sub eax, edx
0048b2f1 c1e002                   shl eax, 2
0048b2f4 29d0                     sub eax, edx
0048b2f6 30d2                     xor dl, dl
0048b2f8 8b0d688f4900             mov ecx, dword ptr [0x498f68]
0048b2fe 88148584135200           mov byte ptr [eax*4 + 0x521384], dl
0048b305 b801000000               mov eax, 1
0048b30a 29c1                     sub ecx, eax
0048b30c 890d688f4900             mov dword ptr [0x498f68], ecx
0048b312 e9b5fdffff               jmp 0x48b0cc
; WaitSnd_Permute
0048b317 53                       push ebx
0048b318 51                       push ecx
0048b319 56                       push esi
0048b31a 57                       push edi
0048b31b 83ec2c                   sub esp, 0x2c
0048b31e 89c3                     mov ebx, eax
0048b320 b92c000000               mov ecx, 0x2c
0048b325 89e7                     mov edi, esp
0048b327 89c6                     mov esi, eax
0048b329 57                       push edi
0048b32a 89c8                     mov eax, ecx
0048b32c c1e902                   shr ecx, 2
0048b32f f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b331 8ac8                     mov cl, al
0048b333 80e103                   and cl, 3
0048b336 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b338 5f                       pop edi
0048b339 b92c000000               mov ecx, 0x2c
0048b33e 89d6                     mov esi, edx
0048b340 89df                     mov edi, ebx
0048b342 57                       push edi
0048b343 89c8                     mov eax, ecx
0048b345 c1e902                   shr ecx, 2
0048b348 f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b34a 8ac8                     mov cl, al
0048b34c 80e103                   and cl, 3
0048b34f f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b351 5f                       pop edi
0048b352 b92c000000               mov ecx, 0x2c
0048b357 89e6                     mov esi, esp
0048b359 89d7                     mov edi, edx
0048b35b 57                       push edi
0048b35c 89c8                     mov eax, ecx
0048b35e c1e902                   shr ecx, 2
0048b361 f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048b363 8ac8                     mov cl, al
0048b365 80e103                   and cl, 3
0048b368 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048b36a 5f                       pop edi
0048b36b 8b7228                   mov esi, dword ptr [edx + 0x28]
0048b36e 8b4328                   mov eax, dword ptr [ebx + 0x28]
0048b371 8b36                     mov esi, dword ptr [esi]
0048b373 8b38                     mov edi, dword ptr [eax]
0048b375 8930                     mov dword ptr [eax], esi
0048b377 8b4228                   mov eax, dword ptr [edx + 0x28]
0048b37a 8938                     mov dword ptr [eax], edi
0048b37c 8b7220                   mov esi, dword ptr [edx + 0x20]
0048b37f 8b4320                   mov eax, dword ptr [ebx + 0x20]
0048b382 897320                   mov dword ptr [ebx + 0x20], esi
0048b385 894220                   mov dword ptr [edx + 0x20], eax
0048b388 83c42c                   add esp, 0x2c
0048b38b 5f                       pop edi
0048b38c 5e                       pop esi
0048b38d 59                       pop ecx
0048b38e 5b                       pop ebx
; WaitSnd_Trier
0048b38f c3                       ret
; UseBank_FindIdInBanque
0048b390 53                       push ebx
0048b391 51                       push ecx
0048b392 89c1                     mov ecx, eax
0048b394 89d3                     mov ebx, edx
0048b396 8b420c                   mov eax, dword ptr [edx + 0xc]
0048b399 31d2                     xor edx, edx
0048b39b eb04                     jmp 0x48b3a1
0048b39d 83c00c                   add eax, 0xc
0048b3a0 42                       inc edx
0048b3a1 663b5304                 cmp dx, word ptr [ebx + 4]
0048b3a5 7307                     jae 0x48b3ae
0048b3a7 3b08                     cmp ecx, dword ptr [eax]
0048b3a9 75f2                     jne 0x48b39d
0048b3ab 59                       pop ecx
0048b3ac 5b                       pop ebx
0048b3ad c3                       ret
0048b3ae 31c0                     xor eax, eax
0048b3b0 59                       pop ecx
0048b3b1 5b                       pop ebx
0048b3b2 c3                       ret
; UseBank_GetDataHeader
0048b3b3 53                       push ebx
0048b3b4 51                       push ecx
0048b3b5 56                       push esi
0048b3b6 ff05bc215200             inc dword ptr [0x5221bc]
0048b3bc 31db                     xor ebx, ebx
0048b3be 668b5806                 mov bx, word ptr [eax + 6]
0048b3c2 4b                       dec ebx
0048b3c3 85db                     test ebx, ebx
0048b3c5 7e17                     jle 0x48b3de
0048b3c7 8b35bc215200             mov esi, dword ptr [0x5221bc]
0048b3cd 8b4808                   mov ecx, dword ptr [eax + 8]
0048b3d0 89d8                     mov eax, ebx
0048b3d2 8b520c                   mov edx, dword ptr [edx + 0xc]
0048b3d5 21f0                     and eax, esi
0048b3d7 01ca                     add edx, ecx
0048b3d9 c1e004                   shl eax, 4
0048b3dc eb06                     jmp 0x48b3e4
0048b3de 8b520c                   mov edx, dword ptr [edx + 0xc]
0048b3e1 8b4008                   mov eax, dword ptr [eax + 8]
0048b3e4 01d0                     add eax, edx
0048b3e6 5e                       pop esi
0048b3e7 59                       pop ecx
0048b3e8 5b                       pop ebx
0048b3e9 c3                       ret
; BanqSon_OpenDataFile
0048b3ec 51                       push ecx
0048b3ed 52                       push edx
0048b3ee 56                       push esi
0048b3ef 57                       push edi
0048b3f0 bfc0215200               mov edi, 0x5221c0
0048b3f5 89c6                     mov esi, eax
0048b3f7 57                       push edi
0048b3f8 8a06                     mov al, byte ptr [esi]
0048b3fa 8807                     mov byte ptr [edi], al
0048b3fc 3c00                     cmp al, 0
0048b3fe 7410                     je 0x48b410
0048b400 8a4601                   mov al, byte ptr [esi + 1]
0048b403 83c602                   add esi, 2
0048b406 884701                   mov byte ptr [edi + 1], al
0048b409 83c702                   add edi, 2
0048b40c 3c00                     cmp al, 0
0048b40e 75e8                     jne 0x48b3f8
0048b410 5f                       pop edi
0048b411 bea0534900               mov esi, 0x4953a0
0048b416 31d2                     xor edx, edx
0048b418 57                       push edi
0048b419 2bc9                     sub ecx, ecx
0048b41b 49                       dec ecx
0048b41c b000                     mov al, 0
0048b41e f2ae                     repne scasb al, byte ptr es:[edi]
0048b420 4f                       dec edi
0048b421 8a06                     mov al, byte ptr [esi]
0048b423 8807                     mov byte ptr [edi], al
0048b425 3c00                     cmp al, 0
0048b427 7410                     je 0x48b439
0048b429 8a4601                   mov al, byte ptr [esi + 1]
0048b42c 83c602                   add esi, 2
0048b42f 884701                   mov byte ptr [edi + 1], al
0048b432 83c702                   add edi, 2
0048b435 3c00                     cmp al, 0
0048b437 75e8                     jne 0x48b421
0048b439 5f                       pop edi
0048b43a 89f8                     mov eax, edi
0048b43c e8d60b0000               call 0x48c017
0048b441 5f                       pop edi
0048b442 5e                       pop esi
0048b443 5a                       pop edx
0048b444 59                       pop ecx
0048b445 c3                       ret
; BanqSon_CloseDataFile
0048b446 8b4008                   mov eax, dword ptr [eax + 8]
0048b449 e9d80b0000               jmp 0x48c026
; BanqSon_ControleValiditeHeader
0048b44e 51                       push ecx
0048b44f 56                       push esi
0048b450 83ec10                   sub esp, 0x10
0048b453 89d6                     mov esi, edx
0048b455 89d9                     mov ecx, ebx
0048b457 bb10000000               mov ebx, 0x10
0048b45c 89e2                     mov edx, esp
0048b45e e8db0b0000               call 0x48c03e
0048b463 813c2441424344           cmp dword ptr [esp], 0x44434241
0048b46a 740a                     je 0x48b476
0048b46c c70600000000             mov dword ptr [esi], 0
0048b472 31c0                     xor eax, eax
0048b474 eb1a                     jmp 0x48b490
0048b476 8b442404                 mov eax, dword ptr [esp + 4]
0048b47a 8906                     mov dword ptr [esi], eax
0048b47c 8b44240c                 mov eax, dword ptr [esp + 0xc]
0048b480 66894104                 mov word ptr [ecx + 4], ax
0048b484 8b442408                 mov eax, dword ptr [esp + 8]
0048b488 894118                   mov dword ptr [ecx + 0x18], eax
0048b48b b801000000               mov eax, 1
0048b490 83c410                   add esp, 0x10
0048b493 5e                       pop esi
0048b494 59                       pop ecx
0048b495 c3                       ret
; BanqSon_LoadHeader
0048b496 53                       push ebx
0048b497 51                       push ecx
0048b498 56                       push esi
0048b499 57                       push edi
0048b49a 55                       push ebp
0048b49b 83ec18                   sub esp, 0x18
0048b49e 89d5                     mov ebp, edx
0048b4a0 bfc0215200               mov edi, 0x5221c0
0048b4a5 89c6                     mov esi, eax
0048b4a7 57                       push edi
0048b4a8 8a06                     mov al, byte ptr [esi]
0048b4aa 8807                     mov byte ptr [edi], al
0048b4ac 3c00                     cmp al, 0
0048b4ae 7410                     je 0x48b4c0
0048b4b0 8a4601                   mov al, byte ptr [esi + 1]
0048b4b3 83c602                   add esi, 2
0048b4b6 884701                   mov byte ptr [edi + 1], al
0048b4b9 83c702                   add edi, 2
0048b4bc 3c00                     cmp al, 0
0048b4be 75e8                     jne 0x48b4a8
0048b4c0 5f                       pop edi
0048b4c1 bea5534900               mov esi, 0x4953a5
0048b4c6 31d2                     xor edx, edx
0048b4c8 57                       push edi
0048b4c9 2bc9                     sub ecx, ecx
0048b4cb 49                       dec ecx
0048b4cc b000                     mov al, 0
0048b4ce f2ae                     repne scasb al, byte ptr es:[edi]
0048b4d0 4f                       dec edi
0048b4d1 8a06                     mov al, byte ptr [esi]
0048b4d3 8807                     mov byte ptr [edi], al
0048b4d5 3c00                     cmp al, 0
0048b4d7 7410                     je 0x48b4e9
0048b4d9 8a4601                   mov al, byte ptr [esi + 1]
0048b4dc 83c602                   add esi, 2
0048b4df 884701                   mov byte ptr [edi + 1], al
0048b4e2 83c702                   add edi, 2
0048b4e5 3c00                     cmp al, 0
0048b4e7 75e8                     jne 0x48b4d1
0048b4e9 5f                       pop edi
0048b4ea 89f8                     mov eax, edi
0048b4ec e8260b0000               call 0x48c017
0048b4f1 89c1                     mov ecx, eax
0048b4f3 83f8ff                   cmp eax, -1
0048b4f6 7446                     je 0x48b53e
0048b4f8 bb10000000               mov ebx, 0x10
0048b4fd 89e2                     mov edx, esp
0048b4ff e83a0b0000               call 0x48c03e
0048b504 813c2441424344           cmp dword ptr [esp], 0x44434241
0048b50b 740a                     je 0x48b517
0048b50d 31db                     xor ebx, ebx
0048b50f 31c0                     xor eax, eax
0048b511 895c2414                 mov dword ptr [esp + 0x14], ebx
0048b515 eb1c                     jmp 0x48b533
0048b517 8b442404                 mov eax, dword ptr [esp + 4]
0048b51b 89442414                 mov dword ptr [esp + 0x14], eax
0048b51f 8b44240c                 mov eax, dword ptr [esp + 0xc]
0048b523 66894504                 mov word ptr [ebp + 4], ax
0048b527 8b442408                 mov eax, dword ptr [esp + 8]
0048b52b 894518                   mov dword ptr [ebp + 0x18], eax
0048b52e b801000000               mov eax, 1
0048b533 85c0                     test eax, eax
0048b535 750b                     jne 0x48b542
0048b537 89c8                     mov eax, ecx
0048b539 e8e80a0000               call 0x48c026
0048b53e 31c0                     xor eax, eax
0048b540 eb4b                     jmp 0x48b58d
0048b542 baaa534900               mov edx, 0x4953aa
0048b547 8b442414                 mov eax, dword ptr [esp + 0x14]
0048b54b e8b40c0000               call 0x48c204
0048b550 89442410                 mov dword ptr [esp + 0x10], eax
0048b554 85c0                     test eax, eax
0048b556 74df                     je 0x48b537
0048b558 8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0048b55c 89c2                     mov edx, eax
0048b55e 89c8                     mov eax, ecx
0048b560 e8d90a0000               call 0x48c03e
0048b565 3b442414                 cmp eax, dword ptr [esp + 0x14]
0048b569 7417                     je 0x48b582
0048b56b 89c8                     mov eax, ecx
0048b56d bad6534900               mov edx, 0x4953d6
0048b572 e8af0a0000               call 0x48c026
0048b577 8d442410                 lea eax, [esp + 0x10]
0048b57b e8ff0c0000               call 0x48c27f
0048b580 ebbc                     jmp 0x48b53e
0048b582 89c8                     mov eax, ecx
0048b584 e89d0a0000               call 0x48c026
0048b589 8b442410                 mov eax, dword ptr [esp + 0x10]
0048b58d 83c418                   add esp, 0x18
0048b590 5d                       pop ebp
0048b591 5f                       pop edi
0048b592 5e                       pop esi
0048b593 59                       pop ecx
0048b594 5b                       pop ebx
0048b595 c3                       ret
; BanqSon_FreeHeader
0048b596 52                       push edx
0048b597 ba05544900               mov edx, 0x495405
0048b59c 83c00c                   add eax, 0xc
0048b59f e8db0c0000               call 0x48c27f
0048b5a4 5a                       pop edx
0048b5a5 c3                       ret
; BanqSon_Open
0048b5a6 53                       push ebx
0048b5a7 51                       push ecx
0048b5a8 56                       push esi
0048b5a9 57                       push edi
0048b5aa 89c6                     mov esi, eax
0048b5ac 89d3                     mov ebx, edx
0048b5ae 833a01                   cmp dword ptr [edx], 1
0048b5b1 7507                     jne 0x48b5ba
0048b5b3 31c0                     xor eax, eax
0048b5b5 5f                       pop edi
0048b5b6 5e                       pop esi
0048b5b7 59                       pop ecx
0048b5b8 5b                       pop ebx
0048b5b9 c3                       ret
0048b5ba 89da                     mov edx, ebx
0048b5bc e8d5feffff               call 0x48b496
0048b5c1 89430c                   mov dword ptr [ebx + 0xc], eax
0048b5c4 85c0                     test eax, eax
0048b5c6 0f847f000000             je 0x48b64b
0048b5cc bfc0215200               mov edi, 0x5221c0
0048b5d1 57                       push edi
0048b5d2 8a06                     mov al, byte ptr [esi]
0048b5d4 8807                     mov byte ptr [edi], al
0048b5d6 3c00                     cmp al, 0
0048b5d8 7410                     je 0x48b5ea
0048b5da 8a4601                   mov al, byte ptr [esi + 1]
0048b5dd 83c602                   add esi, 2
0048b5e0 884701                   mov byte ptr [edi + 1], al
0048b5e3 83c702                   add edi, 2
0048b5e6 3c00                     cmp al, 0
0048b5e8 75e8                     jne 0x48b5d2
0048b5ea 5f                       pop edi
0048b5eb bea0534900               mov esi, 0x4953a0
0048b5f0 31d2                     xor edx, edx
0048b5f2 57                       push edi
0048b5f3 2bc9                     sub ecx, ecx
0048b5f5 49                       dec ecx
0048b5f6 b000                     mov al, 0
0048b5f8 f2ae                     repne scasb al, byte ptr es:[edi]
0048b5fa 4f                       dec edi
0048b5fb 8a06                     mov al, byte ptr [esi]
0048b5fd 8807                     mov byte ptr [edi], al
0048b5ff 3c00                     cmp al, 0
0048b601 7410                     je 0x48b613
0048b603 8a4601                   mov al, byte ptr [esi + 1]
0048b606 83c602                   add esi, 2
0048b609 884701                   mov byte ptr [edi + 1], al
0048b60c 83c702                   add edi, 2
0048b60f 3c00                     cmp al, 0
0048b611 75e8                     jne 0x48b5fb
0048b613 5f                       pop edi
0048b614 89f8                     mov eax, edi
0048b616 e8fc090000               call 0x48c017
0048b61b 894308                   mov dword ptr [ebx + 8], eax
0048b61e 83f8ff                   cmp eax, -1
0048b621 750f                     jne 0x48b632
0048b623 ba05544900               mov edx, 0x495405
0048b628 8d430c                   lea eax, [ebx + 0xc]
0048b62b e84f0c0000               call 0x48c27f
0048b630 eb81                     jmp 0x48b5b3
0048b632 c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b639 c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b640 b801000000               mov eax, 1
0048b645 c70301000000             mov dword ptr [ebx], 1
0048b64b 5f                       pop edi
0048b64c 5e                       pop esi
0048b64d 59                       pop ecx
0048b64e 5b                       pop ebx
0048b64f c3                       ret
; BanqSon_FreeDataInMemory
0048b650 53                       push ebx
0048b651 52                       push edx
0048b652 89c3                     mov ebx, eax
0048b654 833800                   cmp dword ptr [eax], 0
0048b657 7505                     jne 0x48b65e
0048b659 31c0                     xor eax, eax
0048b65b 5a                       pop edx
0048b65c 5b                       pop ebx
0048b65d c3                       ret
0048b65e 83781000                 cmp dword ptr [eax + 0x10], 0
0048b662 74f5                     je 0x48b659
0048b664 ba18544900               mov edx, 0x495418
0048b669 83c014                   add eax, 0x14
0048b66c e80e0c0000               call 0x48c27f
0048b671 c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b678 b801000000               mov eax, 1
0048b67d c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b684 5a                       pop edx
0048b685 5b                       pop ebx
0048b686 c3                       ret
; BanqSon_Close
0048b687 53                       push ebx
0048b688 51                       push ecx
0048b689 52                       push edx
0048b68a 89c3                     mov ebx, eax
0048b68c 8b10                     mov edx, dword ptr [eax]
0048b68e 85d2                     test edx, edx
0048b690 7506                     jne 0x48b698
0048b692 31c0                     xor eax, eax
0048b694 5a                       pop edx
0048b695 59                       pop ecx
0048b696 5b                       pop ebx
0048b697 c3                       ret
0048b698 8b4810                   mov ecx, dword ptr [eax + 0x10]
0048b69b 83f901                   cmp ecx, 1
0048b69e 7523                     jne 0x48b6c3
0048b6a0 85d2                     test edx, edx
0048b6a2 741f                     je 0x48b6c3
0048b6a4 85c9                     test ecx, ecx
0048b6a6 741b                     je 0x48b6c3
0048b6a8 ba18544900               mov edx, 0x495418
0048b6ad 83c014                   add eax, 0x14
0048b6b0 e8ca0b0000               call 0x48c27f
0048b6b5 c7431400000000           mov dword ptr [ebx + 0x14], 0
0048b6bc c7431000000000           mov dword ptr [ebx + 0x10], 0
0048b6c3 ba05544900               mov edx, 0x495405
0048b6c8 8d430c                   lea eax, [ebx + 0xc]
0048b6cb e8af0b0000               call 0x48c27f
0048b6d0 8b4308                   mov eax, dword ptr [ebx + 8]
0048b6d3 e84e090000               call 0x48c026
0048b6d8 b801000000               mov eax, 1
0048b6dd c70300000000             mov dword ptr [ebx], 0
0048b6e3 5a                       pop edx
0048b6e4 59                       pop ecx
0048b6e5 5b                       pop ebx
0048b6e6 c3                       ret
; BanqSon_LoadAllData
0048b6e7 53                       push ebx
0048b6e8 51                       push ecx
0048b6e9 52                       push edx
0048b6ea 56                       push esi
0048b6eb 83ec04                   sub esp, 4
0048b6ee 89c1                     mov ecx, eax
0048b6f0 ba52544900               mov edx, 0x495452
0048b6f5 8b4018                   mov eax, dword ptr [eax + 0x18]
0048b6f8 e8070b0000               call 0x48c204
0048b6fd 890424                   mov dword ptr [esp], eax
0048b700 85c0                     test eax, eax
0048b702 7427                     je 0x48b72b
0048b704 89c2                     mov edx, eax
0048b706 8b7108                   mov esi, dword ptr [ecx + 8]
0048b709 8b5918                   mov ebx, dword ptr [ecx + 0x18]
0048b70c 89f0                     mov eax, esi
0048b70e e82b090000               call 0x48c03e
0048b713 3b4118                   cmp eax, dword ptr [ecx + 0x18]
0048b716 7410                     je 0x48b728
0048b718 ba85544900               mov edx, 0x495485
0048b71d 89e0                     mov eax, esp
0048b71f e85b0b0000               call 0x48c27f
0048b724 31c0                     xor eax, eax
0048b726 eb03                     jmp 0x48b72b
0048b728 8b0424                   mov eax, dword ptr [esp]
0048b72b 83c404                   add esp, 4
0048b72e 5e                       pop esi
0048b72f 5a                       pop edx
0048b730 59                       pop ecx
0048b731 5b                       pop ebx
0048b732 c3                       ret
; BanqSon_LoadDataInMemory
0048b733 53                       push ebx
0048b734 51                       push ecx
0048b735 52                       push edx
0048b736 56                       push esi
0048b737 83ec04                   sub esp, 4
0048b73a 89c1                     mov ecx, eax
0048b73c 833800                   cmp dword ptr [eax], 0
0048b73f 7504                     jne 0x48b745
0048b741 31c0                     xor eax, eax
0048b743 ebe6                     jmp 0x48b72b
0048b745 ba52544900               mov edx, 0x495452
0048b74a 8b4018                   mov eax, dword ptr [eax + 0x18]
0048b74d e8b20a0000               call 0x48c204
0048b752 890424                   mov dword ptr [esp], eax
0048b755 85c0                     test eax, eax
0048b757 7427                     je 0x48b780
0048b759 89c2                     mov edx, eax
0048b75b 8b7108                   mov esi, dword ptr [ecx + 8]
0048b75e 8b5918                   mov ebx, dword ptr [ecx + 0x18]
0048b761 89f0                     mov eax, esi
0048b763 e8d6080000               call 0x48c03e
0048b768 3b4118                   cmp eax, dword ptr [ecx + 0x18]
0048b76b 7410                     je 0x48b77d
0048b76d ba85544900               mov edx, 0x495485
0048b772 89e0                     mov eax, esp
0048b774 e8060b0000               call 0x48c27f
0048b779 31c0                     xor eax, eax
0048b77b eb03                     jmp 0x48b780
0048b77d 8b0424                   mov eax, dword ptr [esp]
0048b780 894114                   mov dword ptr [ecx + 0x14], eax
0048b783 b801000000               mov eax, 1
0048b788 c7411001000000           mov dword ptr [ecx + 0x10], 1
0048b78f eb9a                     jmp 0x48b72b
; DSB_Destroy
0048b794 53                       push ebx
0048b795 51                       push ecx
0048b796 52                       push edx
0048b797 89c3                     mov ebx, eax
0048b799 8b10                     mov edx, dword ptr [eax]
0048b79b 85d2                     test edx, edx
0048b79d 740e                     je 0x48b7ad
0048b79f 89d0                     mov eax, edx
0048b7a1 50                       push eax
0048b7a2 8b12                     mov edx, dword ptr [edx]
0048b7a4 ff5208                   call dword ptr [edx + 8]
0048b7a7 c70300000000             mov dword ptr [ebx], 0
0048b7ad 5a                       pop edx
0048b7ae 59                       pop ecx
0048b7af 5b                       pop ebx
0048b7b0 c3                       ret
; DSB_CreateEmptySoundBuffer
0048b7b1 56                       push esi
0048b7b2 57                       push edi
0048b7b3 55                       push ebp
0048b7b4 83ec28                   sub esp, 0x28
0048b7b7 833d2822520000           cmp dword ptr [0x522228], 0
0048b7be 747a                     je 0x48b83a
0048b7c0 6689442416               mov word ptr [esp + 0x16], ax
0048b7c5 0fafc3                   imul eax, ebx
0048b7c8 c1f803                   sar eax, 3
0048b7cb 6689442420               mov word ptr [esp + 0x20], ax
0048b7d0 31c0                     xor eax, eax
0048b7d2 668b442420               mov ax, word ptr [esp + 0x20]
0048b7d7 89542418                 mov dword ptr [esp + 0x18], edx
0048b7db 0fafd0                   imul edx, eax
0048b7de be01000000               mov esi, 1
0048b7e3 bf14000000               mov edi, 0x14
0048b7e8 bde0000000               mov ebp, 0xe0
0048b7ed 66895c2422               mov word ptr [esp + 0x22], bx
0048b7f2 bb14000000               mov ebx, 0x14
0048b7f7 89e0                     mov eax, esp
0048b7f9 8954241c                 mov dword ptr [esp + 0x1c], edx
0048b7fd 31d2                     xor edx, edx
0048b7ff 6689742414               mov word ptr [esp + 0x14], si
0048b804 e8a70b0000               call 0x48c3b0
0048b809 8d442414                 lea eax, [esp + 0x14]
0048b80d 6a00                     push 0
0048b80f 8d5c2428                 lea ebx, [esp + 0x28]
0048b813 897c2404                 mov dword ptr [esp + 4], edi
0048b817 896c2408                 mov dword ptr [esp + 8], ebp
0048b81b 89442414                 mov dword ptr [esp + 0x14], eax
0048b81f 53                       push ebx
0048b820 8d5c2408                 lea ebx, [esp + 8]
0048b824 a128225200               mov eax, dword ptr [0x522228]
0048b829 894c2410                 mov dword ptr [esp + 0x10], ecx
0048b82d 53                       push ebx
0048b82e 8b10                     mov edx, dword ptr [eax]
0048b830 50                       push eax
0048b831 ff520c                   call dword ptr [edx + 0xc]
0048b834 8b442424                 mov eax, dword ptr [esp + 0x24]
0048b838 eb02                     jmp 0x48b83c
0048b83a 31c0                     xor eax, eax
0048b83c 83c428                   add esp, 0x28
0048b83f 5d                       pop ebp
0048b840 5f                       pop edi
0048b841 5e                       pop esi
0048b842 c3                       ret
; imaadpcmNextStepIndex
0048b844 53                       push ebx
0048b845 89c3                     mov ebx, eax
0048b847 89d0                     mov eax, edx
0048b849 89da                     mov edx, ebx
0048b84b 8b14556a8f4900           mov edx, dword ptr [edx*2 + 0x498f6a]
0048b852 c1fa10                   sar edx, 0x10
0048b855 01d0                     add eax, edx
0048b857 85c0                     test eax, eax
0048b859 7d04                     jge 0x48b85f
0048b85b 31c0                     xor eax, eax
0048b85d 5b                       pop ebx
0048b85e c3                       ret
0048b85f 83f858                   cmp eax, 0x58
0048b862 7e05                     jle 0x48b869
0048b864 b858000000               mov eax, 0x58
0048b869 5b                       pop ebx
0048b86a c3                       ret
; imaadpcmSampleDecode
0048b86b 51                       push ecx
0048b86c 56                       push esi
0048b86d 89c1                     mov ecx, eax
0048b86f 89d8                     mov eax, ebx
0048b871 c1f803                   sar eax, 3
0048b874 f6c104                   test cl, 4
0048b877 7402                     je 0x48b87b
0048b879 01d8                     add eax, ebx
0048b87b f6c102                   test cl, 2
0048b87e 7406                     je 0x48b886
0048b880 89de                     mov esi, ebx
0048b882 d1fe                     sar esi, 1
0048b884 01f0                     add eax, esi
0048b886 f6c101                   test cl, 1
0048b889 7405                     je 0x48b890
0048b88b c1fb02                   sar ebx, 2
0048b88e 01d8                     add eax, ebx
0048b890 f6c108                   test cl, 8
0048b893 7402                     je 0x48b897
0048b895 f7d8                     neg eax
0048b897 01d0                     add eax, edx
0048b899 0fbfd0                   movsx edx, ax
0048b89c 39c2                     cmp edx, eax
0048b89e 7414                     je 0x48b8b4
0048b8a0 3d0080ffff               cmp eax, 0xffff8000
0048b8a5 7d08                     jge 0x48b8af
0048b8a7 b80080ffff               mov eax, 0xffff8000
0048b8ac 5e                       pop esi
0048b8ad 59                       pop ecx
0048b8ae c3                       ret
0048b8af b8ff7f0000               mov eax, 0x7fff
0048b8b4 5e                       pop esi
0048b8b5 59                       pop ecx
0048b8b6 c3                       ret
; imaadpcmValidStepIndex
0048b8b7 85c0                     test eax, eax
0048b8b9 7c0b                     jl 0x48b8c6
0048b8bb 83f858                   cmp eax, 0x58
0048b8be 7f06                     jg 0x48b8c6
0048b8c0 b801000000               mov eax, 1
0048b8c5 c3                       ret
0048b8c6 31c0                     xor eax, eax
0048b8c8 c3                       ret
; imaadpcmDecode4Bit_M16
0048b8c9 56                       push esi
0048b8ca 57                       push edi
0048b8cb 55                       push ebp
0048b8cc 83ec2c                   sub esp, 0x2c
0048b8cf 89c6                     mov esi, eax
0048b8d1 8954240c                 mov dword ptr [esp + 0xc], edx
0048b8d5 894c2408                 mov dword ptr [esp + 8], ecx
0048b8d9 895c2404                 mov dword ptr [esp + 4], ebx
0048b8dd 8b54240c                 mov edx, dword ptr [esp + 0xc]
0048b8e1 83fa04                   cmp edx, 4
0048b8e4 0f829b010000             jb 0x48ba85
0048b8ea 8b7c2408                 mov edi, dword ptr [esp + 8]
0048b8ee 39fa                     cmp edx, edi
0048b8f0 7304                     jae 0x48b8f6
0048b8f2 89d0                     mov eax, edx
0048b8f4 eb02                     jmp 0x48b8f8
0048b8f6 89f8                     mov eax, edi
0048b8f8 8b6c240c                 mov ebp, dword ptr [esp + 0xc]
0048b8fc 29c5                     sub ebp, eax
0048b8fe 83e804                   sub eax, 4
0048b901 89442420                 mov dword ptr [esp + 0x20], eax
0048b905 8b06                     mov eax, dword ptr [esi]
0048b907 0fbfd0                   movsx edx, ax
0048b90a c1e810                   shr eax, 0x10
0048b90d 896c240c                 mov dword ptr [esp + 0xc], ebp
0048b911 25ffff0000               and eax, 0xffff
0048b916 25ff000000               and eax, 0xff
0048b91b 83c604                   add esi, 4
0048b91e 89442424                 mov dword ptr [esp + 0x24], eax
0048b922 85c0                     test eax, eax
0048b924 7c0c                     jl 0x48b932
0048b926 83f858                   cmp eax, 0x58
0048b929 7f07                     jg 0x48b932
0048b92b b801000000               mov eax, 1
0048b930 eb02                     jmp 0x48b934
0048b932 31c0                     xor eax, eax
0048b934 85c0                     test eax, eax
0048b936 0f8451010000             je 0x48ba8d
0048b93c 668913                   mov word ptr [ebx], dx
0048b93f 83c302                   add ebx, 2
0048b942 8b7c2420                 mov edi, dword ptr [esp + 0x20]
0048b946 4f                       dec edi
0048b947 897c2420                 mov dword ptr [esp + 0x20], edi
0048b94b 83ffff                   cmp edi, -1
0048b94e 748d                     je 0x48b8dd
0048b950 8b6c2424                 mov ebp, dword ptr [esp + 0x24]
0048b954 8a06                     mov al, byte ptr [esi]
0048b956 89542410                 mov dword ptr [esp + 0x10], edx
0048b95a 88442428                 mov byte ptr [esp + 0x28], al
0048b95e 46                       inc esi
0048b95f 8b2c6d8a8f4900           mov ebp, dword ptr [ebp*2 + 0x498f8a]
0048b966 240f                     and al, 0xf
0048b968 c1fd10                   sar ebp, 0x10
0048b96b 0fb6f8                   movzx edi, al
0048b96e 896c2418                 mov dword ptr [esp + 0x18], ebp
0048b972 89e8                     mov eax, ebp
0048b974 89f9                     mov ecx, edi
0048b976 c1f803                   sar eax, 3
0048b979 66f7c70400               test di, 4
0048b97e 7402                     je 0x48b982
0048b980 01e8                     add eax, ebp
0048b982 f6c102                   test cl, 2
0048b985 7408                     je 0x48b98f
0048b987 8b542418                 mov edx, dword ptr [esp + 0x18]
0048b98b d1fa                     sar edx, 1
0048b98d 01d0                     add eax, edx
0048b98f f6c101                   test cl, 1
0048b992 7409                     je 0x48b99d
0048b994 8b542418                 mov edx, dword ptr [esp + 0x18]
0048b998 c1fa02                   sar edx, 2
0048b99b 01d0                     add eax, edx
0048b99d f6c108                   test cl, 8
0048b9a0 7402                     je 0x48b9a4
0048b9a2 f7d8                     neg eax
0048b9a4 03442410                 add eax, dword ptr [esp + 0x10]
0048b9a8 0fbfd0                   movsx edx, ax
0048b9ab 39c2                     cmp edx, eax
0048b9ad 7413                     je 0x48b9c2
0048b9af 3d0080ffff               cmp eax, 0xffff8000
0048b9b4 7d07                     jge 0x48b9bd
0048b9b6 b80080ffff               mov eax, 0xffff8000
0048b9bb eb05                     jmp 0x48b9c2
0048b9bd b8ff7f0000               mov eax, 0x7fff
0048b9c2 89c2                     mov edx, eax
0048b9c4 8b047d6a8f4900           mov eax, dword ptr [edi*2 + 0x498f6a]
0048b9cb 8b4c2424                 mov ecx, dword ptr [esp + 0x24]
0048b9cf c1f810                   sar eax, 0x10
0048b9d2 01c8                     add eax, ecx
0048b9d4 85c0                     test eax, eax
0048b9d6 7d04                     jge 0x48b9dc
0048b9d8 31c0                     xor eax, eax
0048b9da eb0a                     jmp 0x48b9e6
0048b9dc 83f858                   cmp eax, 0x58
0048b9df 7e05                     jle 0x48b9e6
0048b9e1 b858000000               mov eax, 0x58
0048b9e6 0fb67c2428               movzx edi, byte ptr [esp + 0x28]
0048b9eb 890424                   mov dword ptr [esp], eax
0048b9ee 89542414                 mov dword ptr [esp + 0x14], edx
0048b9f2 668913                   mov word ptr [ebx], dx
0048b9f5 c1ff04                   sar edi, 4
0048b9f8 8b2c458a8f4900           mov ebp, dword ptr [eax*2 + 0x498f8a]
0048b9ff 83c302                   add ebx, 2
0048ba02 c1fd10                   sar ebp, 0x10
0048ba05 89f9                     mov ecx, edi
0048ba07 89e8                     mov eax, ebp
0048ba09 896c241c                 mov dword ptr [esp + 0x1c], ebp
0048ba0d c1f803                   sar eax, 3
0048ba10 66f7c70400               test di, 4
0048ba15 7402                     je 0x48ba19
0048ba17 01e8                     add eax, ebp
0048ba19 f6c102                   test cl, 2
0048ba1c 7408                     je 0x48ba26
0048ba1e 8b54241c                 mov edx, dword ptr [esp + 0x1c]
0048ba22 d1fa                     sar edx, 1
0048ba24 01d0                     add eax, edx
0048ba26 f6c101                   test cl, 1
0048ba29 7409                     je 0x48ba34
0048ba2b 8b54241c                 mov edx, dword ptr [esp + 0x1c]
0048ba2f c1fa02                   sar edx, 2
0048ba32 01d0                     add eax, edx
0048ba34 f6c108                   test cl, 8
0048ba37 7402                     je 0x48ba3b
0048ba39 f7d8                     neg eax
0048ba3b 03442414                 add eax, dword ptr [esp + 0x14]
0048ba3f 0fbfd0                   movsx edx, ax
0048ba42 39c2                     cmp edx, eax
0048ba44 7413                     je 0x48ba59
0048ba46 3d0080ffff               cmp eax, 0xffff8000
0048ba4b 7d07                     jge 0x48ba54
0048ba4d b80080ffff               mov eax, 0xffff8000
0048ba52 eb05                     jmp 0x48ba59
0048ba54 b8ff7f0000               mov eax, 0x7fff
0048ba59 89c2                     mov edx, eax
0048ba5b 8b047d6a8f4900           mov eax, dword ptr [edi*2 + 0x498f6a]
0048ba62 8b0c24                   mov ecx, dword ptr [esp]
0048ba65 c1f810                   sar eax, 0x10
0048ba68 01c8                     add eax, ecx
0048ba6a 85c0                     test eax, eax
0048ba6c 7d04                     jge 0x48ba72
0048ba6e 31c0                     xor eax, eax
0048ba70 eb0a                     jmp 0x48ba7c
0048ba72 83f858                   cmp eax, 0x58
0048ba75 7e05                     jle 0x48ba7c
0048ba77 b858000000               mov eax, 0x58
0048ba7c 89442424                 mov dword ptr [esp + 0x24], eax
0048ba80 e9b7feffff               jmp 0x48b93c
0048ba85 8b4c2404                 mov ecx, dword ptr [esp + 4]
0048ba89 89d8                     mov eax, ebx
0048ba8b 29c8                     sub eax, ecx
0048ba8d 83c42c                   add esp, 0x2c
0048ba90 5d                       pop ebp
0048ba91 5f                       pop edi
0048ba92 5e                       pop esi
0048ba93 c20c00                   ret 0xc
; imaadpcmDecode4Bit_S16
0048ba96 56                       push esi
0048ba97 57                       push edi
0048ba98 55                       push ebp
0048ba99 83ec3c                   sub esp, 0x3c
0048ba9c 89c5                     mov ebp, eax
0048ba9e 89542410                 mov dword ptr [esp + 0x10], edx
0048baa2 894c240c                 mov dword ptr [esp + 0xc], ecx
0048baa6 8d41f8                   lea eax, [ecx - 8]
0048baa9 895c2404                 mov dword ptr [esp + 4], ebx
0048baad 89442408                 mov dword ptr [esp + 8], eax
0048bab1 8b542410                 mov edx, dword ptr [esp + 0x10]
0048bab5 85d2                     test edx, edx
0048bab7 0f8445020000             je 0x48bd02
0048babd 8b44240c                 mov eax, dword ptr [esp + 0xc]
0048bac1 89d6                     mov esi, edx
0048bac3 29c6                     sub esi, eax
0048bac5 8b442408                 mov eax, dword ptr [esp + 8]
0048bac9 89442414                 mov dword ptr [esp + 0x14], eax
0048bacd 8b4500                   mov eax, dword ptr [ebp]
0048bad0 89742410                 mov dword ptr [esp + 0x10], esi
0048bad4 0fbfd0                   movsx edx, ax
0048bad7 c1e810                   shr eax, 0x10
0048bada 89542428                 mov dword ptr [esp + 0x28], edx
0048bade 25ffff0000               and eax, 0xffff
0048bae3 25ff000000               and eax, 0xff
0048bae8 83c504                   add ebp, 4
0048baeb 8944242c                 mov dword ptr [esp + 0x2c], eax
0048baef 85c0                     test eax, eax
0048baf1 7c0c                     jl 0x48baff
0048baf3 83f858                   cmp eax, 0x58
0048baf6 7f07                     jg 0x48baff
0048baf8 b801000000               mov eax, 1
0048bafd eb02                     jmp 0x48bb01
0048baff 31c0                     xor eax, eax
0048bb01 85c0                     test eax, eax
0048bb03 0f8401020000             je 0x48bd0a
0048bb09 8b4500                   mov eax, dword ptr [ebp]
0048bb0c 0fbfd0                   movsx edx, ax
0048bb0f c1e810                   shr eax, 0x10
0048bb12 89542424                 mov dword ptr [esp + 0x24], edx
0048bb16 25ffff0000               and eax, 0xffff
0048bb1b 25ff000000               and eax, 0xff
0048bb20 83c504                   add ebp, 4
0048bb23 89442430                 mov dword ptr [esp + 0x30], eax
0048bb27 85c0                     test eax, eax
0048bb29 7c0c                     jl 0x48bb37
0048bb2b 83f858                   cmp eax, 0x58
0048bb2e 7f07                     jg 0x48bb37
0048bb30 b801000000               mov eax, 1
0048bb35 eb02                     jmp 0x48bb39
0048bb37 31c0                     xor eax, eax
0048bb39 85c0                     test eax, eax
0048bb3b 0f84c9010000             je 0x48bd0a
0048bb41 31c0                     xor eax, eax
0048bb43 668b442424               mov ax, word ptr [esp + 0x24]
0048bb48 89c2                     mov edx, eax
0048bb4a 31c0                     xor eax, eax
0048bb4c c1e210                   shl edx, 0x10
0048bb4f 668b442428               mov ax, word ptr [esp + 0x28]
0048bb54 09d0                     or eax, edx
0048bb56 8903                     mov dword ptr [ebx], eax
0048bb58 83c304                   add ebx, 4
0048bb5b 8b742414                 mov esi, dword ptr [esp + 0x14]
0048bb5f 85f6                     test esi, esi
0048bb61 0f844affffff             je 0x48bab1
0048bb67 8d7ef8                   lea edi, [esi - 8]
0048bb6a 8b4500                   mov eax, dword ptr [ebp]
0048bb6d 83c504                   add ebp, 4
0048bb70 89442434                 mov dword ptr [esp + 0x34], eax
0048bb74 897c2414                 mov dword ptr [esp + 0x14], edi
0048bb78 8b4500                   mov eax, dword ptr [ebp]
0048bb7b bf08000000               mov edi, 8
0048bb80 89442438                 mov dword ptr [esp + 0x38], eax
0048bb84 83c504                   add ebp, 4
0048bb87 e901010000               jmp 0x48bc8d
0048bb8c b8ff7f0000               mov eax, 0x7fff
0048bb91 89442428                 mov dword ptr [esp + 0x28], eax
0048bb95 8b04756a8f4900           mov eax, dword ptr [esi*2 + 0x498f6a]
0048bb9c 8b74242c                 mov esi, dword ptr [esp + 0x2c]
0048bba0 c1f810                   sar eax, 0x10
0048bba3 01f0                     add eax, esi
0048bba5 85c0                     test eax, eax
0048bba7 7d04                     jge 0x48bbad
0048bba9 31c0                     xor eax, eax
0048bbab eb0a                     jmp 0x48bbb7
0048bbad 83f858                   cmp eax, 0x58
0048bbb0 7e05                     jle 0x48bbb7
0048bbb2 b858000000               mov eax, 0x58
0048bbb7 8b742438                 mov esi, dword ptr [esp + 0x38]
0048bbbb 8b4c2430                 mov ecx, dword ptr [esp + 0x30]
0048bbbf 8944242c                 mov dword ptr [esp + 0x2c], eax
0048bbc3 8b442424                 mov eax, dword ptr [esp + 0x24]
0048bbc7 8b0c4d8a8f4900           mov ecx, dword ptr [ecx*2 + 0x498f8a]
0048bbce 83e60f                   and esi, 0xf
0048bbd1 c1f910                   sar ecx, 0x10
0048bbd4 89f2                     mov edx, esi
0048bbd6 89442418                 mov dword ptr [esp + 0x18], eax
0048bbda 89c8                     mov eax, ecx
0048bbdc 894c241c                 mov dword ptr [esp + 0x1c], ecx
0048bbe0 c1f803                   sar eax, 3
0048bbe3 66f7c60400               test si, 4
0048bbe8 7402                     je 0x48bbec
0048bbea 01c8                     add eax, ecx
0048bbec f6c202                   test dl, 2
0048bbef 7408                     je 0x48bbf9
0048bbf1 8b4c241c                 mov ecx, dword ptr [esp + 0x1c]
0048bbf5 d1f9                     sar ecx, 1
0048bbf7 01c8                     add eax, ecx
0048bbf9 f6c201                   test dl, 1
0048bbfc 7409                     je 0x48bc07
0048bbfe 8b4c241c                 mov ecx, dword ptr [esp + 0x1c]
0048bc02 c1f902                   sar ecx, 2
0048bc05 01c8                     add eax, ecx
0048bc07 f6c208                   test dl, 8
0048bc0a 7402                     je 0x48bc0e
0048bc0c f7d8                     neg eax
0048bc0e 03442418                 add eax, dword ptr [esp + 0x18]
0048bc12 0fbfd0                   movsx edx, ax
0048bc15 39c2                     cmp edx, eax
0048bc17 7413                     je 0x48bc2c
0048bc19 3d0080ffff               cmp eax, 0xffff8000
0048bc1e 7d07                     jge 0x48bc27
0048bc20 b80080ffff               mov eax, 0xffff8000
0048bc25 eb05                     jmp 0x48bc2c
0048bc27 b8ff7f0000               mov eax, 0x7fff
0048bc2c 89442424                 mov dword ptr [esp + 0x24], eax
0048bc30 8b04756a8f4900           mov eax, dword ptr [esi*2 + 0x498f6a]
0048bc37 8b4c2430                 mov ecx, dword ptr [esp + 0x30]
0048bc3b c1f810                   sar eax, 0x10
0048bc3e 01c8                     add eax, ecx
0048bc40 85c0                     test eax, eax
0048bc42 7d04                     jge 0x48bc48
0048bc44 31c0                     xor eax, eax
0048bc46 eb0a                     jmp 0x48bc52
0048bc48 83f858                   cmp eax, 0x58
0048bc4b 7e05                     jle 0x48bc52
0048bc4d b858000000               mov eax, 0x58
0048bc52 89442430                 mov dword ptr [esp + 0x30], eax
0048bc56 31c0                     xor eax, eax
0048bc58 31d2                     xor edx, edx
0048bc5a 668b442424               mov ax, word ptr [esp + 0x24]
0048bc5f 668b542428               mov dx, word ptr [esp + 0x28]
0048bc64 c1e010                   shl eax, 0x10
0048bc67 4f                       dec edi
0048bc68 09c2                     or edx, eax
0048bc6a 8b442434                 mov eax, dword ptr [esp + 0x34]
0048bc6e 8913                     mov dword ptr [ebx], edx
0048bc70 8b542438                 mov edx, dword ptr [esp + 0x38]
0048bc74 c1e804                   shr eax, 4
0048bc77 83c304                   add ebx, 4
0048bc7a c1ea04                   shr edx, 4
0048bc7d 89442434                 mov dword ptr [esp + 0x34], eax
0048bc81 89542438                 mov dword ptr [esp + 0x38], edx
0048bc85 85ff                     test edi, edi
0048bc87 0f8ecefeffff             jle 0x48bb5b
0048bc8d 8b742434                 mov esi, dword ptr [esp + 0x34]
0048bc91 8b54242c                 mov edx, dword ptr [esp + 0x2c]
0048bc95 8b442428                 mov eax, dword ptr [esp + 0x28]
0048bc99 83e60f                   and esi, 0xf
0048bc9c 8b14558a8f4900           mov edx, dword ptr [edx*2 + 0x498f8a]
0048bca3 890424                   mov dword ptr [esp], eax
0048bca6 c1fa10                   sar edx, 0x10
0048bca9 89f1                     mov ecx, esi
0048bcab 89d0                     mov eax, edx
0048bcad 89542420                 mov dword ptr [esp + 0x20], edx
0048bcb1 c1f803                   sar eax, 3
0048bcb4 66f7c60400               test si, 4
0048bcb9 7402                     je 0x48bcbd
0048bcbb 01d0                     add eax, edx
0048bcbd f6c102                   test cl, 2
0048bcc0 7408                     je 0x48bcca
0048bcc2 8b542420                 mov edx, dword ptr [esp + 0x20]
0048bcc6 d1fa                     sar edx, 1
0048bcc8 01d0                     add eax, edx
0048bcca f6c101                   test cl, 1
0048bccd 7409                     je 0x48bcd8
0048bccf 8b542420                 mov edx, dword ptr [esp + 0x20]
0048bcd3 c1fa02                   sar edx, 2
0048bcd6 01d0                     add eax, edx
0048bcd8 f6c108                   test cl, 8
0048bcdb 7402                     je 0x48bcdf
0048bcdd f7d8                     neg eax
0048bcdf 030424                   add eax, dword ptr [esp]
0048bce2 0fbfd0                   movsx edx, ax
0048bce5 39c2                     cmp edx, eax
0048bce7 0f84a4feffff             je 0x48bb91
0048bced 3d0080ffff               cmp eax, 0xffff8000
0048bcf2 0f8d94feffff             jge 0x48bb8c
0048bcf8 b80080ffff               mov eax, 0xffff8000
0048bcfd e98ffeffff               jmp 0x48bb91
0048bd02 8b4c2404                 mov ecx, dword ptr [esp + 4]
0048bd06 89d8                     mov eax, ebx
0048bd08 29c8                     sub eax, ecx
0048bd0a 83c43c                   add esp, 0x3c
0048bd0d e97efdffff               jmp 0x48ba90
; SetPrimaryFormatDirectSound
0048bd14 56                       push esi
0048bd15 57                       push edi
0048bd16 83ec28                   sub esp, 0x28
0048bd19 50                       push eax
0048bd1a 89d7                     mov edi, edx
0048bd1c 89de                     mov esi, ebx
0048bd1e 31d2                     xor edx, edx
0048bd20 8b1d28225200             mov ebx, dword ptr [0x522228]
0048bd26 89542428                 mov dword ptr [esp + 0x28], edx
0048bd2a 85db                     test ebx, ebx
0048bd2c 7507                     jne 0x48bd35
0048bd2e 31c0                     xor eax, eax
0048bd30 e9bc000000               jmp 0x48bdf1
0048bd35 bb10000000               mov ebx, 0x10
0048bd3a 8d442418                 lea eax, [esp + 0x18]
0048bd3e e86d060000               call 0x48c3b0
0048bd43 8b0424                   mov eax, dword ptr [esp]
0048bd46 668944241a               mov word ptr [esp + 0x1a], ax
0048bd4b 31c0                     xor eax, eax
0048bd4d ba01000000               mov edx, 1
0048bd52 6689f8                   mov ax, di
0048bd55 6689542418               mov word ptr [esp + 0x18], dx
0048bd5a 8944241c                 mov dword ptr [esp + 0x1c], eax
0048bd5e 31c0                     xor eax, eax
0048bd60 8b54241c                 mov edx, dword ptr [esp + 0x1c]
0048bd64 6689f0                   mov ax, si
0048bd67 0fafd0                   imul edx, eax
0048bd6a bb14000000               mov ebx, 0x14
0048bd6f 6689742424               mov word ptr [esp + 0x24], si
0048bd74 66894c2426               mov word ptr [esp + 0x26], cx
0048bd79 b914000000               mov ecx, 0x14
0048bd7e 31ff                     xor edi, edi
0048bd80 8d442404                 lea eax, [esp + 4]
0048bd84 89542420                 mov dword ptr [esp + 0x20], edx
0048bd88 31d2                     xor edx, edx
0048bd8a be01000000               mov esi, 1
0048bd8f e81c060000               call 0x48c3b0
0048bd94 8d5c2428                 lea ebx, [esp + 0x28]
0048bd98 a128225200               mov eax, dword ptr [0x522228]
0048bd9d 894c2404                 mov dword ptr [esp + 4], ecx
0048bda1 57                       push edi
0048bda2 8974240c                 mov dword ptr [esp + 0xc], esi
0048bda6 897c2410                 mov dword ptr [esp + 0x10], edi
0048bdaa 53                       push ebx
0048bdab 8d5c240c                 lea ebx, [esp + 0xc]
0048bdaf 897c241c                 mov dword ptr [esp + 0x1c], edi
0048bdb3 53                       push ebx
0048bdb4 8b10                     mov edx, dword ptr [eax]
0048bdb6 50                       push eax
0048bdb7 ff520c                   call dword ptr [edx + 0xc]
0048bdba 85c0                     test eax, eax
0048bdbc 0f856cffffff             jne 0x48bd2e
0048bdc2 8b442428                 mov eax, dword ptr [esp + 0x28]
0048bdc6 85c0                     test eax, eax
0048bdc8 7427                     je 0x48bdf1
0048bdca 8d542418                 lea edx, [esp + 0x18]
0048bdce 52                       push edx
0048bdcf 8b54242c                 mov edx, dword ptr [esp + 0x2c]
0048bdd3 8b00                     mov eax, dword ptr [eax]
0048bdd5 52                       push edx
0048bdd6 ff5038                   call dword ptr [eax + 0x38]
0048bdd9 85c0                     test eax, eax
0048bddb 0f854dffffff             jne 0x48bd2e
0048bde1 8b5c2428                 mov ebx, dword ptr [esp + 0x28]
0048bde5 8b442428                 mov eax, dword ptr [esp + 0x28]
0048bde9 53                       push ebx
0048bdea 8b00                     mov eax, dword ptr [eax]
0048bdec ff5008                   call dword ptr [eax + 8]
0048bdef 89f0                     mov eax, esi
0048bdf1 83c42c                   add esp, 0x2c
0048bdf4 5f                       pop edi
0048bdf5 5e                       pop esi
0048bdf6 c3                       ret
; InitDirectSound
0048bdf7 53                       push ebx
0048bdf8 51                       push ecx
0048bdf9 52                       push edx
0048bdfa 56                       push esi
0048bdfb 89c3                     mov ebx, eax
0048bdfd 8b1528225200             mov edx, dword ptr [0x522228]
0048be03 85d2                     test edx, edx
0048be05 7407                     je 0x48be0e
0048be07 31c0                     xor eax, eax
0048be09 5e                       pop esi
0048be0a 5a                       pop edx
0048be0b 59                       pop ecx
0048be0c 5b                       pop ebx
0048be0d c3                       ret
0048be0e 52                       push edx
0048be0f 6828225200               push 0x522228
0048be14 52                       push edx
0048be15 891524225200             mov dword ptr [0x522224], edx
0048be1b e8e07b0000               call 0x493a00
0048be20 8b3528225200             mov esi, dword ptr [0x522228]
0048be26 85f6                     test esi, esi
0048be28 74dd                     je 0x48be07
0048be2a 6a02                     push 2
0048be2c 53                       push ebx
0048be2d 8b16                     mov edx, dword ptr [esi]
0048be2f 56                       push esi
0048be30 bb04000000               mov ebx, 4
0048be35 ff5218                   call dword ptr [edx + 0x18]
0048be38 b910000000               mov ecx, 0x10
0048be3d ba22560000               mov edx, 0x5622
0048be42 b802000000               mov eax, 2
0048be47 e8c8feffff               call 0x48bd14
0048be4c b801000000               mov eax, 1
0048be51 5e                       pop esi
0048be52 5a                       pop edx
0048be53 59                       pop ecx
0048be54 5b                       pop ebx
0048be55 c3                       ret
; FreeDirectSound
0048be56 51                       push ecx
0048be57 52                       push edx
0048be58 8b1528225200             mov edx, dword ptr [0x522228]
0048be5e 85d2                     test edx, edx
0048be60 7505                     jne 0x48be67
0048be62 31c0                     xor eax, eax
0048be64 5a                       pop edx
0048be65 59                       pop ecx
0048be66 c3                       ret
0048be67 89d0                     mov eax, edx
0048be69 50                       push eax
0048be6a 8b12                     mov edx, dword ptr [edx]
0048be6c ff5208                   call dword ptr [edx + 8]
0048be6f 85c0                     test eax, eax
0048be71 75ef                     jne 0x48be62
0048be73 a328225200               mov dword ptr [0x522228], eax
0048be78 b801000000               mov eax, 1
0048be7d 5a                       pop edx
0048be7e 59                       pop ecx
0048be7f c3                       ret
; IsInitDirectSound
0048be80 833d2822520000           cmp dword ptr [0x522228], 0
0048be87 0f95c0                   setne al
0048be8a 25ff000000               and eax, 0xff
0048be8f c3                       ret
; DSB_IsPlaying
0048be90 53                       push ebx
0048be91 51                       push ecx
0048be92 52                       push edx
0048be93 83ec04                   sub esp, 4
0048be96 85c0                     test eax, eax
0048be98 7418                     je 0x48beb2
0048be9a 89e3                     mov ebx, esp
0048be9c 53                       push ebx
0048be9d 8b10                     mov edx, dword ptr [eax]
0048be9f 50                       push eax
0048bea0 ff5224                   call dword ptr [edx + 0x24]
0048bea3 f6042401                 test byte ptr [esp], 1
0048bea7 7407                     je 0x48beb0
0048bea9 b801000000               mov eax, 1
0048beae eb02                     jmp 0x48beb2
0048beb0 31c0                     xor eax, eax
0048beb2 83c404                   add esp, 4
0048beb5 5a                       pop edx
0048beb6 59                       pop ecx
0048beb7 5b                       pop ebx
0048beb8 c3                       ret
; DSB_IsStopped
0048beb9 53                       push ebx
0048beba 51                       push ecx
0048bebb 52                       push edx
0048bebc 83ec04                   sub esp, 4
0048bebf 85c0                     test eax, eax
0048bec1 7507                     jne 0x48beca
0048bec3 b801000000               mov eax, 1
0048bec8 ebe8                     jmp 0x48beb2
0048beca 89e3                     mov ebx, esp
0048becc 53                       push ebx
0048becd 8b10                     mov edx, dword ptr [eax]
0048becf 50                       push eax
0048bed0 ff5224                   call dword ptr [edx + 0x24]
0048bed3 f6042405                 test byte ptr [esp], 5
0048bed7 74ea                     je 0x48bec3
0048bed9 ebd5                     jmp 0x48beb0
; DSD_IsLooped
0048bedb 53                       push ebx
0048bedc 51                       push ecx
0048bedd 52                       push edx
0048bede 83ec04                   sub esp, 4
0048bee1 85c0                     test eax, eax
0048bee3 74cd                     je 0x48beb2
0048bee5 89e3                     mov ebx, esp
0048bee7 53                       push ebx
0048bee8 8b10                     mov edx, dword ptr [eax]
0048beea 50                       push eax
0048beeb ff5224                   call dword ptr [edx + 0x24]
0048beee f6042404                 test byte ptr [esp], 4
0048bef2 ebb3                     jmp 0x48bea7
; DSB_Play
0048bef4 53                       push ebx
0048bef5 51                       push ecx
0048bef6 52                       push edx
0048bef7 56                       push esi
0048bef8 57                       push edi
0048bef9 83ec04                   sub esp, 4
0048befc 8b5820                   mov ebx, dword ptr [eax + 0x20]
0048beff 8b780c                   mov edi, dword ptr [eax + 0xc]
0048bf02 8b1b                     mov ebx, dword ptr [ebx]
0048bf04 e8a3deffff               call 0x489dac
0048bf09 89c6                     mov esi, eax
0048bf0b 85db                     test ebx, ebx
0048bf0d 7504                     jne 0x48bf13
0048bf0f 31c0                     xor eax, eax
0048bf11 eb58                     jmp 0x48bf6b
0048bf13 7416                     je 0x48bf2b
0048bf15 89e2                     mov edx, esp
0048bf17 52                       push edx
0048bf18 8b03                     mov eax, dword ptr [ebx]
0048bf1a 53                       push ebx
0048bf1b ff5024                   call dword ptr [eax + 0x24]
0048bf1e f6042401                 test byte ptr [esp], 1
0048bf22 7407                     je 0x48bf2b
0048bf24 b801000000               mov eax, 1
0048bf29 eb02                     jmp 0x48bf2d
0048bf2b 31c0                     xor eax, eax
0048bf2d 83f801                   cmp eax, 1
0048bf30 7439                     je 0x48bf6b
0048bf32 6a00                     push 0
0048bf34 8b03                     mov eax, dword ptr [ebx]
0048bf36 53                       push ebx
0048bf37 ff5034                   call dword ptr [eax + 0x34]
0048bf3a 85c0                     test eax, eax
0048bf3c 75d1                     jne 0x48bf0f
0048bf3e 56                       push esi
0048bf3f 8b03                     mov eax, dword ptr [ebx]
0048bf41 53                       push ebx
0048bf42 ff503c                   call dword ptr [eax + 0x3c]
0048bf45 85c0                     test eax, eax
0048bf47 75c6                     jne 0x48bf0f
0048bf49 89da                     mov edx, ebx
0048bf4b 8b03                     mov eax, dword ptr [ebx]
0048bf4d 83ff01                   cmp edi, 1
0048bf50 0f94c3                   sete bl
0048bf53 81e3ff000000             and ebx, 0xff
0048bf59 53                       push ebx
0048bf5a 6a00                     push 0
0048bf5c 6a00                     push 0
0048bf5e 52                       push edx
0048bf5f ff5030                   call dword ptr [eax + 0x30]
0048bf62 85c0                     test eax, eax
0048bf64 75a9                     jne 0x48bf0f
0048bf66 b801000000               mov eax, 1
0048bf6b 83c404                   add esp, 4
0048bf6e 5f                       pop edi
0048bf6f 5e                       pop esi
0048bf70 5a                       pop edx
0048bf71 59                       pop ecx
0048bf72 5b                       pop ebx
0048bf73 c3                       ret
; DSB_Stop
0048bf74 53                       push ebx
0048bf75 51                       push ecx
0048bf76 52                       push edx
0048bf77 83ec04                   sub esp, 4
0048bf7a 89c3                     mov ebx, eax
0048bf7c 85c0                     test eax, eax
0048bf7e 0f8425ffffff             je 0x48bea9
0048bf84 7507                     jne 0x48bf8d
0048bf86 b801000000               mov eax, 1
0048bf8b eb11                     jmp 0x48bf9e
0048bf8d 89e2                     mov edx, esp
0048bf8f 52                       push edx
0048bf90 8b00                     mov eax, dword ptr [eax]
0048bf92 53                       push ebx
0048bf93 ff5024                   call dword ptr [eax + 0x24]
0048bf96 f6042405                 test byte ptr [esp], 5
0048bf9a 74ea                     je 0x48bf86
0048bf9c 31c0                     xor eax, eax
0048bf9e 85c0                     test eax, eax
0048bfa0 0f8503ffffff             jne 0x48bea9
0048bfa6 53                       push ebx
0048bfa7 8b03                     mov eax, dword ptr [ebx]
0048bfa9 ff5048                   call dword ptr [eax + 0x48]
0048bfac 85c0                     test eax, eax
0048bfae 0f84f5feffff             je 0x48bea9
0048bfb4 e9f7feffff               jmp 0x48beb0
; DSB_DuplicateHeader
0048bfb9 53                       push ebx
0048bfba 51                       push ecx
0048bfbb 52                       push edx
0048bfbc 83ec04                   sub esp, 4
0048bfbf 89c2                     mov edx, eax
0048bfc1 8b1d28225200             mov ebx, dword ptr [0x522228]
0048bfc7 85db                     test ebx, ebx
0048bfc9 7507                     jne 0x48bfd2
0048bfcb 31c0                     xor eax, eax
0048bfcd e9e0feffff               jmp 0x48beb2
0048bfd2 85c0                     test eax, eax
0048bfd4 0f84d8feffff             je 0x48beb2
0048bfda 89e1                     mov ecx, esp
0048bfdc 51                       push ecx
0048bfdd 52                       push edx
0048bfde 89d8                     mov eax, ebx
0048bfe0 8b1b                     mov ebx, dword ptr [ebx]
0048bfe2 50                       push eax
0048bfe3 ff5314                   call dword ptr [ebx + 0x14]
0048bfe6 85c0                     test eax, eax
0048bfe8 75e1                     jne 0x48bfcb
0048bfea 8b0c24                   mov ecx, dword ptr [esp]
0048bfed 85c9                     test ecx, ecx
0048bfef 0f84bdfeffff             je 0x48beb2
0048bff5 6a00                     push 0
0048bff7 8b01                     mov eax, dword ptr [ecx]
0048bff9 51                       push ecx
0048bffa ff5034                   call dword ptr [eax + 0x34]
0048bffd 8b0424                   mov eax, dword ptr [esp]
0048c000 e9adfeffff               jmp 0x48beb2
; CreatM
0048c008 51                       push ecx
0048c009 52                       push edx
0048c00a 50                       push eax
0048c00b 2eff15f4315200           call dword ptr cs:[0x5231f4]
0048c012 83f8ff                   cmp eax, -1
0048c015 59                       pop ecx
0048c016 c3                       ret
; OpenM
0048c017 51                       push ecx
0048c018 52                       push edx
0048c019 50                       push eax
0048c01a 2eff15fc315200           call dword ptr cs:[0x5231fc]
0048c021 83f8ff                   cmp eax, -1
0048c024 59                       pop ecx
0048c025 c3                       ret
; CloseM
0048c026 51                       push ecx
0048c027 52                       push edx
0048c028 50                       push eax
0048c029 2eff15f0315200           call dword ptr cs:[0x5231f0]
0048c030 83f8ff                   cmp eax, -1
0048c033 0f95c0                   setne al
0048c036 25ff000000               and eax, 0xff
0048c03b 5a                       pop edx
0048c03c 59                       pop ecx
0048c03d c3                       ret
; ReadM
0048c03e 51                       push ecx
0048c03f 53                       push ebx
0048c040 52                       push edx
0048c041 50                       push eax
0048c042 2eff15e8315200           call dword ptr cs:[0x5231e8]
0048c049 83f8ff                   cmp eax, -1
0048c04c 59                       pop ecx
0048c04d c3                       ret
; WriteM
0048c04e 51                       push ecx
0048c04f 53                       push ebx
0048c050 52                       push edx
0048c051 50                       push eax
0048c052 2eff15ec315200           call dword ptr cs:[0x5231ec]
0048c059 83f8ff                   cmp eax, -1
0048c05c 59                       pop ecx
0048c05d c3                       ret
; SeekM
0048c05e 51                       push ecx
0048c05f 53                       push ebx
0048c060 52                       push edx
0048c061 50                       push eax
0048c062 2eff15f8315200           call dword ptr cs:[0x5231f8]
0048c069 83f8ff                   cmp eax, -1
0048c06c 59                       pop ecx
0048c06d c3                       ret
; LoadSoundBuffer_LoadDataFromFileInSoundBuffer
0048c070 51                       push ecx
0048c071 56                       push esi
0048c072 57                       push edi
0048c073 83ec08                   sub esp, 8
0048c076 89c6                     mov esi, eax
0048c078 89d7                     mov edi, edx
0048c07a 85c0                     test eax, eax
0048c07c 7437                     je 0x48c0b5
0048c07e 6a00                     push 0
0048c080 6a00                     push 0
0048c082 6a00                     push 0
0048c084 8d542410                 lea edx, [esp + 0x10]
0048c088 52                       push edx
0048c089 8d542410                 lea edx, [esp + 0x10]
0048c08d 52                       push edx
0048c08e 53                       push ebx
0048c08f 6a00                     push 0
0048c091 8b00                     mov eax, dword ptr [eax]
0048c093 56                       push esi
0048c094 ff502c                   call dword ptr [eax + 0x2c]
0048c097 8b1424                   mov edx, dword ptr [esp]
0048c09a 89f8                     mov eax, edi
0048c09c e89dffffff               call 0x48c03e
0048c0a1 6a00                     push 0
0048c0a3 6a00                     push 0
0048c0a5 8b54240c                 mov edx, dword ptr [esp + 0xc]
0048c0a9 52                       push edx
0048c0aa 8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c0ae 53                       push ebx
0048c0af 8b06                     mov eax, dword ptr [esi]
0048c0b1 56                       push esi
0048c0b2 ff504c                   call dword ptr [eax + 0x4c]
0048c0b5 83c408                   add esp, 8
0048c0b8 5f                       pop edi
0048c0b9 5e                       pop esi
0048c0ba 59                       pop ecx
0048c0bb c3                       ret
; LoadSoundBuffer_DecompactInSoundBuffer
0048c0bc 56                       push esi
0048c0bd 57                       push edi
0048c0be 55                       push ebp
0048c0bf 83ec08                   sub esp, 8
0048c0c2 89c6                     mov esi, eax
0048c0c4 89d5                     mov ebp, edx
0048c0c6 89df                     mov edi, ebx
0048c0c8 89cb                     mov ebx, ecx
0048c0ca 85c0                     test eax, eax
0048c0cc 7460                     je 0x48c12e
0048c0ce 6a00                     push 0
0048c0d0 6a00                     push 0
0048c0d2 6a00                     push 0
0048c0d4 8d542410                 lea edx, [esp + 0x10]
0048c0d8 52                       push edx
0048c0d9 8d542410                 lea edx, [esp + 0x10]
0048c0dd 52                       push edx
0048c0de 57                       push edi
0048c0df 6a00                     push 0
0048c0e1 8b00                     mov eax, dword ptr [eax]
0048c0e3 56                       push esi
0048c0e4 ff502c                   call dword ptr [eax + 0x2c]
0048c0e7 837c241801               cmp dword ptr [esp + 0x18], 1
0048c0ec 7517                     jne 0x48c105
0048c0ee 6a00                     push 0
0048c0f0 6a00                     push 0
0048c0f2 89d9                     mov ecx, ebx
0048c0f4 89fa                     mov edx, edi
0048c0f6 6a00                     push 0
0048c0f8 89e8                     mov eax, ebp
0048c0fa 8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c0fe e8c6f7ffff               call 0x48b8c9
0048c103 eb15                     jmp 0x48c11a
0048c105 6a00                     push 0
0048c107 6a00                     push 0
0048c109 89d9                     mov ecx, ebx
0048c10b 89fa                     mov edx, edi
0048c10d 6a00                     push 0
0048c10f 89e8                     mov eax, ebp
0048c111 8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c115 e87cf9ffff               call 0x48ba96
0048c11a 6a00                     push 0
0048c11c 6a00                     push 0
0048c11e 8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c122 53                       push ebx
0048c123 8b4c240c                 mov ecx, dword ptr [esp + 0xc]
0048c127 51                       push ecx
0048c128 8b06                     mov eax, dword ptr [esi]
0048c12a 56                       push esi
0048c12b ff504c                   call dword ptr [eax + 0x4c]
0048c12e 83c408                   add esp, 8
0048c131 5d                       pop ebp
0048c132 5f                       pop edi
0048c133 5e                       pop esi
0048c134 c20400                   ret 4
; LoadSoundBuffer_PlaceOnSample
0048c137 53                       push ebx
0048c138 31db                     xor ebx, ebx
0048c13a e81fffffff               call 0x48c05e
0048c13f 5b                       pop ebx
0048c140 c3                       ret
; LoadSoundBuffer_LoadCompactedData
0048c141 53                       push ebx
0048c142 51                       push ecx
0048c143 89d1                     mov ecx, edx
0048c145 8b152c225200             mov edx, dword ptr [0x52222c]
0048c14b 85d2                     test edx, edx
0048c14d 7505                     jne 0x48c154
0048c14f 89d0                     mov eax, edx
0048c151 59                       pop ecx
0048c152 5b                       pop ebx
0048c153 c3                       ret
0048c154 89cb                     mov ebx, ecx
0048c156 e8e3feffff               call 0x48c03e
0048c15b 39c1                     cmp ecx, eax
0048c15d 7405                     je 0x48c164
0048c15f 31c0                     xor eax, eax
0048c161 59                       pop ecx
0048c162 5b                       pop ebx
0048c163 c3                       ret
0048c164 a12c225200               mov eax, dword ptr [0x52222c]
0048c169 59                       pop ecx
0048c16a 5b                       pop ebx
0048c16b c3                       ret
; LoadSoundBuffer_InitCompressedBuffer
0048c16c 52                       push edx
0048c16d bab0544900               mov edx, 0x4954b0
0048c172 b800710200               mov eax, 0x27100
0048c177 e888000000               call 0x48c204
0048c17c a32c225200               mov dword ptr [0x52222c], eax
0048c181 85c0                     test eax, eax
0048c183 0f95c0                   setne al
0048c186 25ff000000               and eax, 0xff
0048c18b 5a                       pop edx
0048c18c c3                       ret
; LoadSoundBuffer_FreeCompressedBuffer
0048c18d 52                       push edx
0048c18e 833d2c22520000           cmp dword ptr [0x52222c], 0
0048c195 740f                     je 0x48c1a6
0048c197 bae8544900               mov edx, 0x4954e8
0048c19c b82c225200               mov eax, 0x52222c
0048c1a1 e8d9000000               call 0x48c27f
0048c1a6 5a                       pop edx
0048c1a7 c3                       ret
; LoadSoundBuffer_LoadDataFromMemoryInSoundBuffer
0048c1a8 51                       push ecx
0048c1a9 56                       push esi
0048c1aa 57                       push edi
0048c1ab 55                       push ebp
0048c1ac 83ec08                   sub esp, 8
0048c1af 89c5                     mov ebp, eax
0048c1b1 89d6                     mov esi, edx
0048c1b3 85c0                     test eax, eax
0048c1b5 7443                     je 0x48c1fa
0048c1b7 6a00                     push 0
0048c1b9 6a00                     push 0
0048c1bb 6a00                     push 0
0048c1bd 8d542410                 lea edx, [esp + 0x10]
0048c1c1 52                       push edx
0048c1c2 8d542410                 lea edx, [esp + 0x10]
0048c1c6 52                       push edx
0048c1c7 53                       push ebx
0048c1c8 6a00                     push 0
0048c1ca 8b00                     mov eax, dword ptr [eax]
0048c1cc 55                       push ebp
0048c1cd ff502c                   call dword ptr [eax + 0x2c]
0048c1d0 8b3c24                   mov edi, dword ptr [esp]
0048c1d3 89d9                     mov ecx, ebx
0048c1d5 57                       push edi
0048c1d6 89c8                     mov eax, ecx
0048c1d8 c1e902                   shr ecx, 2
0048c1db f2a5                     movsd dword ptr es:[edi], dword ptr [esi]
0048c1dd 8ac8                     mov cl, al
0048c1df 80e103                   and cl, 3
0048c1e2 f2a4                     repne movsb byte ptr es:[edi], byte ptr [esi]
0048c1e4 5f                       pop edi
0048c1e5 6a00                     push 0
0048c1e7 6a00                     push 0
0048c1e9 8b54240c                 mov edx, dword ptr [esp + 0xc]
0048c1ed 52                       push edx
0048c1ee 8b5c240c                 mov ebx, dword ptr [esp + 0xc]
0048c1f2 53                       push ebx
0048c1f3 8b4500                   mov eax, dword ptr [ebp]
0048c1f6 55                       push ebp
0048c1f7 ff504c                   call dword ptr [eax + 0x4c]
0048c1fa 83c408                   add esp, 8
0048c1fd 5d                       pop ebp
0048c1fe 5f                       pop edi
0048c1ff 5e                       pop esi
0048c200 59                       pop ecx
0048c201 c3                       ret
