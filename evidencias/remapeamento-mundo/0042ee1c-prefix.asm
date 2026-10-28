; pre_allocation_prefix; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
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
