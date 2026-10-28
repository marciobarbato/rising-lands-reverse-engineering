; BatimentModifyMap; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00419e97  53                       push ebx
00419e98  51                       push ecx
00419e99  56                       push esi
00419e9a  57                       push edi
00419e9b  55                       push ebp
00419e9c  83ec1c                   sub esp, 0x1c
00419e9f  88542418                 mov byte ptr [esp + 0x18], dl
00419ea3  31db                     xor ebx, ebx
00419ea5  6689c3                   mov bx, ax
00419ea8  89d8                     mov eax, ebx
00419eaa  c1e004                   shl eax, 4
00419ead  01d8                     add eax, ebx
00419eaf  c1e002                   shl eax, 2
00419eb2  01d8                     add eax, ebx
00419eb4  b9c8a04900               mov ecx, 0x49a0c8
00419eb9  c1e002                   shl eax, 2
00419ebc  01c1                     add ecx, eax
00419ebe  31db                     xor ebx, ebx
00419ec0  8a4108                   mov al, byte ptr [ecx + 8]
00419ec3  88c3                     mov bl, al
00419ec5  89d8                     mov eax, ebx
00419ec7  c1e002                   shl eax, 2
00419eca  29d8                     sub eax, ebx
00419ecc  c1e002                   shl eax, 2
00419ecf  01c3                     add ebx, eax
00419ed1  c1e302                   shl ebx, 2
00419ed4  668b838c5d4900           mov ax, word ptr [ebx + 0x495d8c]
00419edb  89442404                 mov dword ptr [esp + 4], eax
00419edf  668b838e5d4900           mov ax, word ptr [ebx + 0x495d8e]
00419ee6  890424                   mov dword ptr [esp], eax
00419ee9  31db                     xor ebx, ebx
00419eeb  668b5902                 mov bx, word ptr [ecx + 2]
00419eef  be00010000               mov esi, 0x100
00419ef4  89da                     mov edx, ebx
00419ef6  89d8                     mov eax, ebx
00419ef8  c1fa1f                   sar edx, 0x1f
00419efb  f7fe                     idiv esi
00419efd  6689542408               mov word ptr [esp + 8], dx
00419f02  89da                     mov edx, ebx
00419f04  89d8                     mov eax, ebx
00419f06  c1fa1f                   sar edx, 0x1f
00419f09  f7fe                     idiv esi
00419f0b  31d2                     xor edx, edx
00419f0d  668944240c               mov word ptr [esp + 0xc], ax
00419f12  6689542410               mov word ptr [esp + 0x10], dx
00419f17  6689542414               mov word ptr [esp + 0x14], dx
00419f1c  bd06000000               mov ebp, 6
00419f21  eb14                     jmp 0x419f37
00419f23  8a542415                 mov dl, byte ptr [esp + 0x15]
00419f27  8b742410                 mov esi, dword ptr [esp + 0x10]
00419f2b  fec2                     inc dl
00419f2d  46                       inc esi
00419f2e  88542415                 mov byte ptr [esp + 0x15], dl
00419f32  6689742410               mov word ptr [esp + 0x10], si
00419f37  31db                     xor ebx, ebx
00419f39  8b44240e                 mov eax, dword ptr [esp + 0xe]
00419f3d  668b1c24                 mov bx, word ptr [esp]
00419f41  c1f810                   sar eax, 0x10
00419f44  39d8                     cmp eax, ebx
00419f46  0f8d74000000             jge 0x419fc0
00419f4c  8b5c240a                 mov ebx, dword ptr [esp + 0xa]
00419f50  c1fb10                   sar ebx, 0x10
00419f53  01d8                     add eax, ebx
00419f55  85c0                     test eax, eax
00419f57  7cca                     jl 0x419f23
00419f59  3d00010000               cmp eax, 0x100
00419f5e  7dc3                     jge 0x419f23
00419f60  8b742414                 mov esi, dword ptr [esp + 0x14]
00419f64  31ff                     xor edi, edi
00419f66  eb02                     jmp 0x419f6a
00419f68  46                       inc esi
00419f69  47                       inc edi
00419f6a  31db                     xor ebx, ebx
00419f6c  0fbfc7                   movsx eax, di
00419f6f  668b5c2404               mov bx, word ptr [esp + 4]
00419f74  39d8                     cmp eax, ebx
00419f76  7dab                     jge 0x419f23
00419f78  8b5c2406                 mov ebx, dword ptr [esp + 6]
00419f7c  c1fb10                   sar ebx, 0x10
00419f7f  01d8                     add eax, ebx
00419f81  85c0                     test eax, eax
00419f83  7ce3                     jl 0x419f68
00419f85  3d00010000               cmp eax, 0x100
00419f8a  7ddc                     jge 0x419f68
00419f8c  807c241800               cmp byte ptr [esp + 0x18], 0
00419f91  7419                     je 0x419fac
00419f93  668b4102                 mov ax, word ptr [ecx + 2]
00419f97  31db                     xor ebx, ebx
00419f99  01f0                     add eax, esi
00419f9b  6689c3                   mov bx, ax
00419f9e  31c0                     xor eax, eax
00419fa0  89ea                     mov edx, ebp
00419fa2  8a4104                   mov al, byte ptr [ecx + 4]
00419fa5  e8de030500               call 0x46a388
00419faa  ebbc                     jmp 0x419f68
00419fac  668b4102                 mov ax, word ptr [ecx + 2]
00419fb0  31db                     xor ebx, ebx
00419fb2  01f0                     add eax, esi
00419fb4  6689c3                   mov bx, ax
00419fb7  31c0                     xor eax, eax
00419fb9  ba07000000               mov edx, 7
00419fbe  ebe2                     jmp 0x419fa2
00419fc0  83c41c                   add esp, 0x1c
00419fc3  e9d2990000               jmp 0x42399a
