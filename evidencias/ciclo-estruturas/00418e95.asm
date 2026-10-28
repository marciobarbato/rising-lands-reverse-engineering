; BatimentAlloc_prefix; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00418e95  53                       push ebx
00418e96  51                       push ecx
00418e97  52                       push edx
00418e98  56                       push esi
00418e99  57                       push edi
00418e9a  31c9                     xor ecx, ecx
00418e9c  eb1c                     jmp 0x418eba
00418e9e  31db                     xor ebx, ebx
00418ea0  6689cb                   mov bx, cx
00418ea3  6bdb16                   imul ebx, ebx, 0x16
00418ea6  40                       inc eax
00418ea7  c6841a70a0490000         mov byte ptr [edx + ebx + 0x49a070], 0
00418eaf  31d2                     xor edx, edx
00418eb1  6689c2                   mov dx, ax
00418eb4  83fa16                   cmp edx, 0x16
00418eb7  7ce5                     jl 0x418e9e
00418eb9  41                       inc ecx
00418eba  31c0                     xor eax, eax
00418ebc  6689c8                   mov ax, cx
00418ebf  83f804                   cmp eax, 4
00418ec2  7d04                     jge 0x418ec8
00418ec4  31c8                     xor eax, ecx
00418ec6  ebe7                     jmp 0x418eaf
00418ec8  31c9                     xor ecx, ecx
00418eca  eb1f                     jmp 0x418eeb
00418ecc  31db                     xor ebx, ebx
00418ece  6689cb                   mov bx, cx
00418ed1  69db14010000             imul ebx, ebx, 0x114
00418ed7  40                       inc eax
00418ed8  c6841ad8a1490000         mov byte ptr [edx + ebx + 0x49a1d8], 0
00418ee0  31d2                     xor edx, edx
00418ee2  6689c2                   mov dx, ax
00418ee5  83fa04                   cmp edx, 4
00418ee8  7ce2                     jl 0x418ecc
00418eea  41                       inc ecx
00418eeb  31c0                     xor eax, eax
00418eed  6689c8                   mov ax, cx
00418ef0  3de8030000               cmp eax, 0x3e8
00418ef5  0f8d09010000             jge 0x419004
00418efb  69c014010000             imul eax, eax, 0x114
00418f01  30d2                     xor dl, dl
00418f03  31db                     xor ebx, ebx
00418f05  8890cda04900             mov byte ptr [eax + 0x49a0cd], dl
00418f0b  bfffff0000               mov edi, 0xffff
00418f10  668998d2a04900           mov word ptr [eax + 0x49a0d2], bx
00418f17  6689b840a14900           mov word ptr [eax + 0x49a140], di
00418f1e  6689b84ea14900           mov word ptr [eax + 0x49a14e], di
00418f25  6689b850a14900           mov word ptr [eax + 0x49a150], di
00418f2c  30f6                     xor dh, dh
00418f2e  b701                     mov bh, 1
00418f30  668990cea04900           mov word ptr [eax + 0x49a0ce], dx
00418f37  88b858a14900             mov byte ptr [eax + 0x49a158], bh
00418f3d  b6ff                     mov dh, 0xff
00418f3f  88b0c8a04900             mov byte ptr [eax + 0x49a0c8], dh
00418f45  88903ca14900             mov byte ptr [eax + 0x49a13c], dl
00418f4b  88903da14900             mov byte ptr [eax + 0x49a13d], dl
00418f51  89fb                     mov ebx, edi
00418f53  88903ea14900             mov byte ptr [eax + 0x49a13e], dl
00418f59  31fb                     xor ebx, edi
00418f5b  88b043a14900             mov byte ptr [eax + 0x49a143], dh
00418f61  30f6                     xor dh, dh
00418f63  6689984aa14900           mov word ptr [eax + 0x49a14a], bx
00418f6a  66899044a14900           mov word ptr [eax + 0x49a144], dx
00418f71  889042a14900             mov byte ptr [eax + 0x49a142], dl
00418f77  31ff                     xor edi, edi
00418f79  66899048a14900           mov word ptr [eax + 0x49a148], dx
00418f80  6689b846a14900           mov word ptr [eax + 0x49a146], di
00418f87  6689b88ca14900           mov word ptr [eax + 0x49a18c], di
00418f8e  6689b88ea14900           mov word ptr [eax + 0x49a18e], di
00418f95  bbc8000000               mov ebx, 0xc8
00418f9a  6689b88aa14900           mov word ptr [eax + 0x49a18a], di
00418fa1  baffff0000               mov edx, 0xffff
00418fa6  6689984ca14900           mov word ptr [eax + 0x49a14c], bx
00418fad  bfffff0000               mov edi, 0xffff
00418fb2  66899090a14900           mov word ptr [eax + 0x49a190], dx
00418fb9  30db                     xor bl, bl
00418fbb  6689b8caa04900           mov word ptr [eax + 0x49a0ca], di
00418fc2  b201                     mov dl, 1
00418fc4  8898cca14900             mov byte ptr [eax + 0x49a1cc], bl
00418fca  889052a14900             mov byte ptr [eax + 0x49a152], dl
00418fd0  bfffffffff               mov edi, 0xffffffff
00418fd5  889053a14900             mov byte ptr [eax + 0x49a153], dl
00418fdb  b7ff                     mov bh, 0xff
00418fdd  89b8c8a14900             mov dword ptr [eax + 0x49a1c8], edi
00418fe3  88b8cca04900             mov byte ptr [eax + 0x49a0cc], bh
00418fe9  31d2                     xor edx, edx
00418feb  88b8d0a04900             mov byte ptr [eax + 0x49a0d0], bh
00418ff1  899054a14900             mov dword ptr [eax + 0x49a154], edx
00418ff7  8990d0a14900             mov dword ptr [eax + 0x49a1d0], edx
00418ffd  31c0                     xor eax, eax
00418fff  e9dcfeffff               jmp 0x418ee0
