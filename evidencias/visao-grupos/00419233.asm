; BatimentIllumine; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419233  51                       push ecx
00419234  56                       push esi
00419235  57                       push edi
00419236  83ec1c                   sub esp, 0x1c
00419239  88542414                 mov byte ptr [esp + 0x14], dl
0041923d  885c2418                 mov byte ptr [esp + 0x18], bl
00419241  31d2                     xor edx, edx
00419243  6689c2                   mov dx, ax
00419246  89d0                     mov eax, edx
00419248  c1e004                   shl eax, 4
0041924b  01d0                     add eax, edx
0041924d  c1e002                   shl eax, 2
00419250  01d0                     add eax, edx
00419252  b9c8a04900               mov ecx, 0x49a0c8
00419257  c1e002                   shl eax, 2
0041925a  01c1                     add ecx, eax
0041925c  31d2                     xor edx, edx
0041925e  8a4108                   mov al, byte ptr [ecx + 8]
00419261  88c2                     mov dl, al
00419263  89d0                     mov eax, edx
00419265  c1e002                   shl eax, 2
00419268  29d0                     sub eax, edx
0041926a  c1e002                   shl eax, 2
0041926d  01c2                     add edx, eax
0041926f  c1e202                   shl edx, 2
00419272  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
00419279  890424                   mov dword ptr [esp], eax
0041927c  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
00419283  31db                     xor ebx, ebx
00419285  89442408                 mov dword ptr [esp + 8], eax
00419289  668b5902                 mov bx, word ptr [ecx + 2]
0041928d  be00010000               mov esi, 0x100
00419292  89da                     mov edx, ebx
00419294  89d8                     mov eax, ebx
00419296  c1fa1f                   sar edx, 0x1f
00419299  f7fe                     idiv esi
0041929b  89d7                     mov edi, edx
0041929d  89da                     mov edx, ebx
0041929f  89d8                     mov eax, ebx
004192a1  c1fa1f                   sar edx, 0x1f
004192a4  f7fe                     idiv esi
004192a6  31d2                     xor edx, edx
004192a8  89442404                 mov dword ptr [esp + 4], eax
004192ac  89542410                 mov dword ptr [esp + 0x10], edx
004192b0  668954240c               mov word ptr [esp + 0xc], dx
004192b5  eb08                     jmp 0x4192bf
004192b7  fe44240d                 inc byte ptr [esp + 0xd]
004192bb  ff442410                 inc dword ptr [esp + 0x10]
004192bf  8b442410                 mov eax, dword ptr [esp + 0x10]
004192c3  663b442408               cmp ax, word ptr [esp + 8]
004192c8  0f837a000000             jae 0x419348
004192ce  31c0                     xor eax, eax
004192d0  31d2                     xor edx, edx
004192d2  668b442404               mov ax, word ptr [esp + 4]
004192d7  668b542410               mov dx, word ptr [esp + 0x10]
004192dc  01d0                     add eax, edx
004192de  85c0                     test eax, eax
004192e0  7cd5                     jl 0x4192b7
004192e2  3d00010000               cmp eax, 0x100
004192e7  7dce                     jge 0x4192b7
004192e9  8b74240c                 mov esi, dword ptr [esp + 0xc]
004192ed  31db                     xor ebx, ebx
004192ef  eb19                     jmp 0x41930a
004192f1  668b4102                 mov ax, word ptr [ecx + 2]
004192f5  31d2                     xor edx, edx
004192f7  01d8                     add eax, ebx
004192f9  8a542414                 mov dl, byte ptr [esp + 0x14]
004192fd  01f0                     add eax, esi
004192ff  25ffff0000               and eax, 0xffff
00419304  e8d3d70500               call 0x476adc
00419309  43                       inc ebx
0041930a  663b1c24                 cmp bx, word ptr [esp]
0041930e  73a7                     jae 0x4192b7
00419310  31d2                     xor edx, edx
00419312  31c0                     xor eax, eax
00419314  6689fa                   mov dx, di
00419317  6689d8                   mov ax, bx
0041931a  01d0                     add eax, edx
0041931c  85c0                     test eax, eax
0041931e  7ce9                     jl 0x419309
00419320  3d00010000               cmp eax, 0x100
00419325  7de2                     jge 0x419309
00419327  807c241800               cmp byte ptr [esp + 0x18], 0
0041932c  74c3                     je 0x4192f1
0041932e  668b4102                 mov ax, word ptr [ecx + 2]
00419332  31d2                     xor edx, edx
00419334  01d8                     add eax, ebx
00419336  8a542414                 mov dl, byte ptr [esp + 0x14]
0041933a  01f0                     add eax, esi
0041933c  25ffff0000               and eax, 0xffff
00419341  e822d60500               call 0x476968
00419346  ebc1                     jmp 0x419309
00419348  83c41c                   add esp, 0x1c
0041934b  5f                       pop edi
0041934c  5e                       pop esi
0041934d  59                       pop ecx
0041934e  c3                       ret
