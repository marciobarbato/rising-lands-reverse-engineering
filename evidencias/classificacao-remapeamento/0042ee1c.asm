; Chemin_Remap; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042ee1c  53                       push ebx
0042ee1d  51                       push ecx
0042ee1e  52                       push edx
0042ee1f  56                       push esi
0042ee20  57                       push edi
0042ee21  55                       push ebp
0042ee22  83ec20                   sub esp, 0x20
0042ee25  66a104634900             mov ax, word ptr [0x496304]
0042ee2b  6639c0                   cmp ax, ax
0042ee2e  7522                     jne 0x42ee52
0042ee30  bbffff0000               mov ebx, 0xffff
0042ee35  30e4                     xor ah, ah
0042ee37  31d2                     xor edx, edx
0042ee39  8825360f4e00             mov byte ptr [0x4e0f36], ah
0042ee3f  8825370f4e00             mov byte ptr [0x4e0f37], ah
0042ee45  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0042ee4b  66891d04634900           mov word ptr [0x496304], bx
0042ee52  bb00000100               mov ebx, 0x10000
0042ee57  a16c154e00               mov eax, dword ptr [0x4e156c]
0042ee5c  31d2                     xor edx, edx
0042ee5e  e84dd50500               call 0x48c3b0
0042ee63  bb00010000               mov ebx, 0x100
0042ee68  ba01000000               mov edx, 1
0042ee6d  b870164e00               mov eax, 0x4e1670
0042ee72  e839d50500               call 0x48c3b0
0042ee77  b6ff                     mov dh, 0xff
0042ee79  bb01000000               mov ebx, 1
0042ee7e  883570154e00             mov byte ptr [0x4e1570], dh
0042ee84  895c2414                 mov dword ptr [esp + 0x14], ebx
0042ee88  8b442414                 mov eax, dword ptr [esp + 0x14]
0042ee8c  8a542414                 mov dl, byte ptr [esp + 0x14]
0042ee90  8d4801                   lea ecx, [eax + 1]
0042ee93  889070154e00             mov byte ptr [eax + 0x4e1570], dl
0042ee99  894c2414                 mov dword ptr [esp + 0x14], ecx
0042ee9d  81f900010000             cmp ecx, 0x100
0042eea3  7ce3                     jl 0x42ee88
0042eea5  bb00000200               mov ebx, 0x20000
0042eeaa  a1380f4e00               mov eax, dword ptr [0x4e0f38]
0042eeaf  31d2                     xor edx, edx
0042eeb1  e8fad40500               call 0x48c3b0
0042eeb6  6800000100               push 0x10000
0042eebb  6a00                     push 0
0042eebd  2eff15c0315200           call dword ptr cs:[0x5231c0]
0042eec4  50                       push eax
0042eec5  2eff15d0315200           call dword ptr cs:[0x5231d0]
0042eecc  8944240c                 mov dword ptr [esp + 0xc], eax
0042eed0  85c0                     test eax, eax
0042eed2  7507                     jne 0x42eedb
0042eed4  30c0                     xor al, al
0042eed6  e9fc020000               jmp 0x42f1d7
0042eedb  31ff                     xor edi, edi
0042eedd  897c2414                 mov dword ptr [esp + 0x14], edi
0042eee1  8b6c2414                 mov ebp, dword ptr [esp + 0x14]
0042eee5  8b15a87d5000             mov edx, dword ptr [0x507da8]
0042eeeb  01ea                     add edx, ebp
0042eeed  8a12                     mov dl, byte ptr [edx]
0042eeef  80e201                   and dl, 1
0042eef2  8810                     mov byte ptr [eax], dl
0042eef4  8d5501                   lea edx, [ebp + 1]
0042eef7  40                       inc eax
0042eef8  89542414                 mov dword ptr [esp + 0x14], edx
0042eefc  81fa00000100             cmp edx, 0x10000
0042ef02  7cdd                     jl 0x42eee1
0042ef04  31c9                     xor ecx, ecx
0042ef06  8b54240c                 mov edx, dword ptr [esp + 0xc]
0042ef0a  894c2414                 mov dword ptr [esp + 0x14], ecx
0042ef0e  eb12                     jmp 0x42ef22
0042ef10  8b742414                 mov esi, dword ptr [esp + 0x14]
0042ef14  46                       inc esi
0042ef15  42                       inc edx
0042ef16  89742414                 mov dword ptr [esp + 0x14], esi
0042ef1a  81fe00000100             cmp esi, 0x10000
0042ef20  7d18                     jge 0x42ef3a
0042ef22  31c0                     xor eax, eax
0042ef24  668b442414               mov ax, word ptr [esp + 0x14]
0042ef29  e88a630400               call 0x4752b8
0042ef2e  25ff000000               and eax, 0xff
0042ef33  75db                     jne 0x42ef10
0042ef35  c60200                   mov byte ptr [edx], 0
0042ef38  ebd6                     jmp 0x42ef10
0042ef3a  31c9                     xor ecx, ecx
0042ef3c  31ed                     xor ebp, ebp
0042ef3e  31c0                     xor eax, eax
0042ef40  894c2418                 mov dword ptr [esp + 0x18], ecx
0042ef44  896c2414                 mov dword ptr [esp + 0x14], ebp
0042ef48  890424                   mov dword ptr [esp], eax
0042ef4b  eb3e                     jmp 0x42ef8b
0042ef4d  55                       push ebp
0042ef4e  2eff15cc315200           call dword ptr cs:[0x5231cc]
0042ef55  50                       push eax
0042ef56  2eff15d8315200           call dword ptr cs:[0x5231d8]
0042ef5d  55                       push ebp
0042ef5e  2eff15cc315200           call dword ptr cs:[0x5231cc]
0042ef65  50                       push eax
0042ef66  2eff15c8315200           call dword ptr cs:[0x5231c8]
0042ef6d  8b1424                   mov edx, dword ptr [esp]
0042ef70  8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0042ef74  83c202                   add edx, 2
0042ef77  43                       inc ebx
0042ef78  891424                   mov dword ptr [esp], edx
0042ef7b  895c2414                 mov dword ptr [esp + 0x14], ebx
0042ef7f  81fb00000100             cmp ebx, 0x10000
0042ef85  0f8d92010000             jge 0x42f11d
0042ef8b  8b3c24                   mov edi, dword ptr [esp]
0042ef8e  a1380f4e00               mov eax, dword ptr [0x4e0f38]
0042ef93  01f8                     add eax, edi
0042ef95  668b00                   mov ax, word ptr [eax]
0042ef98  25ffff0000               and eax, 0xffff
0042ef9d  75ce                     jne 0x42ef6d
0042ef9f  8b742418                 mov esi, dword ptr [esp + 0x18]
0042efa3  6800001000               push 0x100000
0042efa8  8b542418                 mov edx, dword ptr [esp + 0x18]
0042efac  46                       inc esi
0042efad  6a00                     push 0
0042efaf  6689f0                   mov ax, si
0042efb2  89542424                 mov dword ptr [esp + 0x24], edx
0042efb6  89442410                 mov dword ptr [esp + 0x10], eax
0042efba  2eff15c0315200           call dword ptr cs:[0x5231c0]
0042efc1  50                       push eax
0042efc2  8974241c                 mov dword ptr [esp + 0x1c], esi
0042efc6  8b742410                 mov esi, dword ptr [esp + 0x10]
0042efca  2eff15d0315200           call dword ptr cs:[0x5231d0]
0042efd1  8b542414                 mov edx, dword ptr [esp + 0x14]
0042efd5  89442410                 mov dword ptr [esp + 0x10], eax
0042efd9  668910                   mov word ptr [eax], dx
0042efdc  83c002                   add eax, 2
0042efdf  8b6c2410                 mov ebp, dword ptr [esp + 0x10]
0042efe3  39e8                     cmp eax, ebp
0042efe5  0f8462ffffff             je 0x42ef4d
0042efeb  83e802                   sub eax, 2
0042efee  31c9                     xor ecx, ecx
0042eff0  668b10                   mov dx, word ptr [eax]
0042eff3  6689d1                   mov cx, dx
0042eff6  0fb76c241c               movzx ebp, word ptr [esp + 0x1c]
0042effb  8a1c31                   mov bl, byte ptr [ecx + esi]
0042effe  3a1c2e                   cmp bl, byte ptr [esi + ebp]
0042f001  75dc                     jne 0x42efdf
0042f003  8b3d380f4e00             mov edi, dword ptr [0x4e0f38]
0042f009  8d1c09                   lea ebx, [ecx + ecx]
0042f00c  01fb                     add ebx, edi
0042f00e  31ff                     xor edi, edi
0042f010  668b3b                   mov di, word ptr [ebx]
0042f013  85ff                     test edi, edi
0042f015  75c8                     jne 0x42efdf
0042f017  8b7c2408                 mov edi, dword ptr [esp + 8]
0042f01b  c1f908                   sar ecx, 8
0042f01e  66893b                   mov word ptr [ebx], di
0042f021  88d7                     mov bh, dl
0042f023  88cb                     mov bl, cl
0042f025  31c9                     xor ecx, ecx
0042f027  88d1                     mov cl, dl
0042f029  83f901                   cmp ecx, 1
0042f02c  7c09                     jl 0x42f037
0042f02e  89d1                     mov ecx, edx
0042f030  49                       dec ecx
0042f031  668908                   mov word ptr [eax], cx
0042f034  83c002                   add eax, 2
0042f037  31c9                     xor ecx, ecx
0042f039  88f9                     mov cl, bh
0042f03b  81f9fe000000             cmp ecx, 0xfe
0042f041  7f09                     jg 0x42f04c
0042f043  89d1                     mov ecx, edx
0042f045  41                       inc ecx
0042f046  668908                   mov word ptr [eax], cx
0042f049  83c002                   add eax, 2
0042f04c  31c9                     xor ecx, ecx
0042f04e  88d9                     mov cl, bl
0042f050  81f9fe000000             cmp ecx, 0xfe
0042f056  7f0a                     jg 0x42f062
0042f058  89d1                     mov ecx, edx
0042f05a  fec5                     inc ch
0042f05c  668908                   mov word ptr [eax], cx
0042f05f  83c002                   add eax, 2
0042f062  31c9                     xor ecx, ecx
0042f064  88d9                     mov cl, bl
0042f066  83f901                   cmp ecx, 1
0042f069  7c0e                     jl 0x42f079
0042f06b  89d1                     mov ecx, edx
0042f06d  81e900010000             sub ecx, 0x100
0042f073  668908                   mov word ptr [eax], cx
0042f076  83c002                   add eax, 2
0042f079  31ff                     xor edi, edi
0042f07b  668b7c241c               mov di, word ptr [esp + 0x1c]
0042f080  803c3700                 cmp byte ptr [edi + esi], 0
0042f084  0f8555ffffff             jne 0x42efdf
0042f08a  31c9                     xor ecx, ecx
0042f08c  88f9                     mov cl, bh
0042f08e  83f901                   cmp ecx, 1
0042f091  7c17                     jl 0x42f0aa
0042f093  31c9                     xor ecx, ecx
0042f095  88d9                     mov cl, bl
0042f097  83f901                   cmp ecx, 1
0042f09a  7c0e                     jl 0x42f0aa
0042f09c  89d1                     mov ecx, edx
0042f09e  81e901010000             sub ecx, 0x101
0042f0a4  668908                   mov word ptr [eax], cx
0042f0a7  83c002                   add eax, 2
0042f0aa  31c9                     xor ecx, ecx
0042f0ac  88f9                     mov cl, bh
0042f0ae  83f901                   cmp ecx, 1
0042f0b1  7c1a                     jl 0x42f0cd
0042f0b3  31c9                     xor ecx, ecx
0042f0b5  88d9                     mov cl, bl
0042f0b7  81f9fe000000             cmp ecx, 0xfe
0042f0bd  7f0e                     jg 0x42f0cd
0042f0bf  89d1                     mov ecx, edx
0042f0c1  81c1ff000000             add ecx, 0xff
0042f0c7  668908                   mov word ptr [eax], cx
0042f0ca  83c002                   add eax, 2
0042f0cd  31c9                     xor ecx, ecx
0042f0cf  88f9                     mov cl, bh
0042f0d1  81f9fe000000             cmp ecx, 0xfe
0042f0d7  7f17                     jg 0x42f0f0
0042f0d9  31c9                     xor ecx, ecx
0042f0db  88d9                     mov cl, bl
0042f0dd  83f901                   cmp ecx, 1
0042f0e0  7c0e                     jl 0x42f0f0
0042f0e2  89d1                     mov ecx, edx
0042f0e4  81e9ff000000             sub ecx, 0xff
0042f0ea  668908                   mov word ptr [eax], cx
0042f0ed  83c002                   add eax, 2
0042f0f0  31c9                     xor ecx, ecx
0042f0f2  88f9                     mov cl, bh
0042f0f4  81f9fe000000             cmp ecx, 0xfe
0042f0fa  0f8fdffeffff             jg 0x42efdf
0042f100  81e3ff000000             and ebx, 0xff
0042f106  81fbfe000000             cmp ebx, 0xfe
0042f10c  0f8fcdfeffff             jg 0x42efdf
0042f112  81c201010000             add edx, 0x101
0042f118  e9bcfeffff               jmp 0x42efd9
0042f11d  31d2                     xor edx, edx
0042f11f  89542404                 mov dword ptr [esp + 4], edx
0042f123  bd00010000               mov ebp, 0x100
0042f128  eb17                     jmp 0x42f141
0042f12a  8b5c2404                 mov ebx, dword ptr [esp + 4]
0042f12e  81c300020000             add ebx, 0x200
0042f134  42                       inc edx
0042f135  895c2404                 mov dword ptr [esp + 4], ebx
0042f139  81fa00010000             cmp edx, 0x100
0042f13f  7d5a                     jge 0x42f19b
0042f141  31c0                     xor eax, eax
0042f143  66a16a714900             mov ax, word ptr [0x49716a]
0042f149  39c2                     cmp edx, eax
0042f14b  7d0a                     jge 0x42f157
0042f14d  31c0                     xor eax, eax
0042f14f  66a168714900             mov ax, word ptr [0x497168]
0042f155  eb02                     jmp 0x42f159
0042f157  31c0                     xor eax, eax
0042f159  8b7c2404                 mov edi, dword ptr [esp + 4]
0042f15d  89442414                 mov dword ptr [esp + 0x14], eax
0042f161  89d6                     mov esi, edx
0042f163  01c0                     add eax, eax
0042f165  c1e608                   shl esi, 8
0042f168  01f8                     add eax, edi
0042f16a  eb25                     jmp 0x42f191
0042f16c  8d0c33                   lea ecx, [ebx + esi]
0042f16f  8b1d380f4e00             mov ebx, dword ptr [0x4e0f38]
0042f175  66c704030000             mov word ptr [ebx + eax], 0
0042f17b  8b1da87d5000             mov ebx, dword ptr [0x507da8]
0042f181  c6041901                 mov byte ptr [ecx + ebx], 1
0042f185  8b4c2414                 mov ecx, dword ptr [esp + 0x14]
0042f189  41                       inc ecx
0042f18a  83c002                   add eax, 2
0042f18d  894c2414                 mov dword ptr [esp + 0x14], ecx
0042f191  8b5c2414                 mov ebx, dword ptr [esp + 0x14]
0042f195  39dd                     cmp ebp, ebx
0042f197  7e91                     jle 0x42f12a
0042f199  ebd1                     jmp 0x42f16c
0042f19b  8b4c240c                 mov ecx, dword ptr [esp + 0xc]
0042f19f  51                       push ecx
0042f1a0  2eff15cc315200           call dword ptr cs:[0x5231cc]
0042f1a7  50                       push eax
0042f1a8  8b742410                 mov esi, dword ptr [esp + 0x10]
0042f1ac  2eff15d8315200           call dword ptr cs:[0x5231d8]
0042f1b3  56                       push esi
0042f1b4  2eff15cc315200           call dword ptr cs:[0x5231cc]
0042f1bb  50                       push eax
0042f1bc  2eff15c8315200           call dword ptr cs:[0x5231c8]
0042f1c3  31c0                     xor eax, eax
0042f1c5  668b442418               mov ax, word ptr [esp + 0x18]
0042f1ca  3d00400000               cmp eax, 0x4000
0042f1cf  0f8dfffcffff             jge 0x42eed4
0042f1d5  b001                     mov al, 1
0042f1d7  83c420                   add esp, 0x20
0042f1da  5d                       pop ebp
0042f1db  5f                       pop edi
0042f1dc  5e                       pop esi
0042f1dd  5a                       pop edx
0042f1de  59                       pop ecx
0042f1df  5b                       pop ebx
0042f1e0  c3                       ret
