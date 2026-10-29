; BatimentRetireColon; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041dde0  53                       push ebx
0041dde1  51                       push ecx
0041dde2  52                       push edx
0041dde3  56                       push esi
0041dde4  57                       push edi
0041dde5  83ec18                   sub esp, 0x18
0041dde8  50                       push eax
0041dde9  31d2                     xor edx, edx
0041ddeb  6689c2                   mov dx, ax
0041ddee  89d0                     mov eax, edx
0041ddf0  c1e004                   shl eax, 4
0041ddf3  01d0                     add eax, edx
0041ddf5  c1e002                   shl eax, 2
0041ddf8  01d0                     add eax, edx
0041ddfa  bec8a04900               mov esi, 0x49a0c8
0041ddff  c1e002                   shl eax, 2
0041de02  01c6                     add esi, eax
0041de04  bfffff0000               mov edi, 0xffff
0041de09  8a4608                   mov al, byte ptr [esi + 8]
0041de0c  25ff000000               and eax, 0xff
0041de11  83f80c                   cmp eax, 0xc
0041de14  0f846a030000             je 0x41e184
0041de1a  bb09000000               mov ebx, 9
0041de1f  ba01000000               mov edx, 1
0041de24  8d460c                   lea eax, [esi + 0xc]
0041de27  e88c930200               call 0x4471b8
0041de2c  25ffff0000               and eax, 0xffff
0041de31  83f801                   cmp eax, 1
0041de34  0f8469000000             je 0x41dea3
0041de3a  e977000000               jmp 0x41deb6
0041de3f  8a4605                   mov al, byte ptr [esi + 5]
0041de42  25ff000000               and eax, 0xff
0041de47  83f804                   cmp eax, 4
0041de4a  7419                     je 0x41de65
0041de4c  31c0                     xor eax, eax
0041de4e  8a4676                   mov al, byte ptr [esi + 0x76]
0041de51  85c0                     test eax, eax
0041de53  750a                     jne 0x41de5f
0041de55  807e7500                 cmp byte ptr [esi + 0x75], 0
0041de59  7504                     jne 0x41de5f
0041de5b  b001                     mov al, 1
0041de5d  eb02                     jmp 0x41de61
0041de5f  30c0                     xor al, al
0041de61  84c0                     test al, al
0041de63  7551                     jne 0x41deb6
0041de65  31c0                     xor eax, eax
0041de67  8a4604                   mov al, byte ptr [esi + 4]
0041de6a  c68054fb4d0001           mov byte ptr [eax + 0x4dfb54], 1
0041de71  eb22                     jmp 0x41de95
0041de73  8a4605                   mov al, byte ptr [esi + 5]
0041de76  25ff000000               and eax, 0xff
0041de7b  83f804                   cmp eax, 4
0041de7e  7415                     je 0x41de95
0041de80  31c0                     xor eax, eax
0041de82  8a4676                   mov al, byte ptr [esi + 0x76]
0041de85  85c0                     test eax, eax
0041de87  7516                     jne 0x41de9f
0041de89  807e7500                 cmp byte ptr [esi + 0x75], 0
0041de8d  7510                     jne 0x41de9f
0041de8f  b001                     mov al, 1
0041de91  84c0                     test al, al
0041de93  7521                     jne 0x41deb6
0041de95  b8ffff0000               mov eax, 0xffff
0041de9a  e980d4ffff               jmp 0x41b31f
0041de9f  30c0                     xor al, al
0041dea1  ebee                     jmp 0x41de91
0041dea3  8a4608                   mov al, byte ptr [esi + 8]
0041dea6  3c08                     cmp al, 8
0041dea8  7208                     jb 0x41deb2
0041deaa  76c7                     jbe 0x41de73
0041deac  3c0e                     cmp al, 0xe
0041deae  748f                     je 0x41de3f
0041deb0  eb04                     jmp 0x41deb6
0041deb2  3c05                     cmp al, 5
0041deb4  74bd                     je 0x41de73
0041deb6  31db                     xor ebx, ebx
0041deb8  668b1c24                 mov bx, word ptr [esp]
0041debc  89d8                     mov eax, ebx
0041debe  c1e004                   shl eax, 4
0041dec1  01d8                     add eax, ebx
0041dec3  c1e002                   shl eax, 2
0041dec6  01d8                     add eax, ebx
0041dec8  b9c8a04900               mov ecx, 0x49a0c8
0041decd  c1e002                   shl eax, 2
0041ded0  89da                     mov edx, ebx
0041ded2  01c1                     add ecx, eax
0041ded4  31da                     xor edx, ebx
0041ded6  8a4108                   mov al, byte ptr [ecx + 8]
0041ded9  88c2                     mov dl, al
0041dedb  89d0                     mov eax, edx
0041dedd  c1e002                   shl eax, 2
0041dee0  29d0                     sub eax, edx
0041dee2  c1e002                   shl eax, 2
0041dee5  01c2                     add edx, eax
0041dee7  c1e202                   shl edx, 2
0041deea  668b828c5d4900           mov ax, word ptr [edx + 0x495d8c]
0041def1  89442408                 mov dword ptr [esp + 8], eax
0041def5  668b828e5d4900           mov ax, word ptr [edx + 0x495d8e]
0041defc  8b542408                 mov edx, dword ptr [esp + 8]
0041df00  89442410                 mov dword ptr [esp + 0x10], eax
0041df04  66d1ea                   shr dx, 1
0041df07  66d1e8                   shr ax, 1
0041df0a  89542408                 mov dword ptr [esp + 8], edx
0041df0e  89442410                 mov dword ptr [esp + 0x10], eax
0041df12  31c0                     xor eax, eax
0041df14  8a4608                   mov al, byte ptr [esi + 8]
0041df17  83f813                   cmp eax, 0x13
0041df1a  7521                     jne 0x41df3d
0041df1c  8d560c                   lea edx, [esi + 0xc]
0041df1f  89d0                     mov eax, edx
0041df21  e824930200               call 0x44724a
0041df26  84c0                     test al, al
0041df28  0f848f000000             je 0x41dfbd
0041df2e  31c0                     xor eax, eax
0041df30  668b0424                 mov ax, word ptr [esp]
0041df34  e836fbffff               call 0x41da6f
0041df39  89c7                     mov edi, eax
0041df3b  ebe2                     jmp 0x41df1f
0041df3d  83f815                   cmp eax, 0x15
0041df40  0f856e000000             jne 0x41dfb4
0041df46  83c10c                   add ecx, 0xc
0041df49  895c240c                 mov dword ptr [esp + 0xc], ebx
0041df4d  89c8                     mov eax, ecx
0041df4f  31ff                     xor edi, edi
0041df51  e8b1910200               call 0x447107
0041df56  89442404                 mov dword ptr [esp + 4], eax
0041df5a  663b7c2404               cmp di, word ptr [esp + 4]
0041df5f  734d                     jae 0x41dfae
0041df61  89c8                     mov eax, ecx
0041df63  31d2                     xor edx, edx
0041df65  31db                     xor ebx, ebx
0041df67  e863940200               call 0x4473cf
0041df6c  6689c3                   mov bx, ax
0041df6f  89442418                 mov dword ptr [esp + 0x18], eax
0041df73  81fbffff0000             cmp ebx, 0xffff
0041df79  7430                     je 0x41dfab
0041df7b  31c0                     xor eax, eax
0041df7d  89da                     mov edx, ebx
0041df7f  668b44240c               mov ax, word ptr [esp + 0xc]
0041df84  e8c6f7ffff               call 0x41d74f
0041df89  31d2                     xor edx, edx
0041df8b  6689c2                   mov dx, ax
0041df8e  81faffff0000             cmp edx, 0xffff
0041df94  7409                     je 0x41df9f
0041df96  89d8                     mov eax, ebx
0041df98  e81f800200               call 0x445fbc
0041df9d  eb0c                     jmp 0x41dfab
0041df9f  ba01000000               mov edx, 1
0041dfa4  89c8                     mov eax, ecx
0041dfa6  e8d8940200               call 0x447483
0041dfab  47                       inc edi
0041dfac  ebac                     jmp 0x41df5a
0041dfae  8b7c2418                 mov edi, dword ptr [esp + 0x18]
0041dfb2  eb09                     jmp 0x41dfbd
0041dfb4  89d8                     mov eax, ebx
0041dfb6  e876f9ffff               call 0x41d931
0041dfbb  89c7                     mov edi, eax
0041dfbd  31d2                     xor edx, edx
0041dfbf  668b1424                 mov dx, word ptr [esp]
0041dfc3  89d0                     mov eax, edx
0041dfc5  c1e004                   shl eax, 4
0041dfc8  01d0                     add eax, edx
0041dfca  c1e002                   shl eax, 2
0041dfcd  01d0                     add eax, edx
0041dfcf  bac8a04900               mov edx, 0x49a0c8
0041dfd4  c1e002                   shl eax, 2
0041dfd7  01c2                     add edx, eax
0041dfd9  31db                     xor ebx, ebx
0041dfdb  8a4208                   mov al, byte ptr [edx + 8]
0041dfde  88c3                     mov bl, al
0041dfe0  8d420c                   lea eax, [edx + 0xc]
0041dfe3  83fb15                   cmp ebx, 0x15
0041dfe6  750d                     jne 0x41dff5
0041dfe8  e85d920200               call 0x44724a
0041dfed  84c0                     test al, al
0041dfef  7429                     je 0x41e01a
0041dff1  b001                     mov al, 1
0041dff3  eb27                     jmp 0x41e01c
0041dff5  83fb02                   cmp ebx, 2
0041dff8  7509                     jne 0x41e003
0041dffa  e84b920200               call 0x44724a
0041dfff  84c0                     test al, al
0041e001  75ee                     jne 0x41dff1
0041e003  8d420c                   lea eax, [edx + 0xc]
0041e006  bb09000000               mov ebx, 9
0041e00b  ba01000000               mov edx, 1
0041e010  e8a3910200               call 0x4471b8
0041e015  6685c0                   test ax, ax
0041e018  ebd5                     jmp 0x41dfef
0041e01a  30c0                     xor al, al
0041e01c  84c0                     test al, al
0041e01e  0f8560010000             jne 0x41e184
0041e024  31d2                     xor edx, edx
0041e026  668b1424                 mov dx, word ptr [esp]
0041e02a  89d0                     mov eax, edx
0041e02c  c1e004                   shl eax, 4
0041e02f  01d0                     add eax, edx
0041e031  c1e002                   shl eax, 2
0041e034  01d0                     add eax, edx
0041e036  c1e002                   shl eax, 2
0041e039  05c8a04900               add eax, 0x49a0c8
0041e03e  8a4008                   mov al, byte ptr [eax + 8]
0041e041  25ff000000               and eax, 0xff
0041e046  83f809                   cmp eax, 9
0041e049  0f847b000000             je 0x41e0ca
0041e04f  83f80c                   cmp eax, 0xc
0041e052  7541                     jne 0x41e095
0041e054  e971000000               jmp 0x41e0ca
0041e059  c744241414000000         mov dword ptr [esp + 0x14], 0x14
0041e061  eb4b                     jmp 0x41e0ae
0041e063  c74424140a000000         mov dword ptr [esp + 0x14], 0xa
0041e06b  eb41                     jmp 0x41e0ae
0041e06d  c744241408000000         mov dword ptr [esp + 0x14], 8
0041e075  eb37                     jmp 0x41e0ae
0041e077  c744241404000000         mov dword ptr [esp + 0x14], 4
0041e07f  eb2d                     jmp 0x41e0ae
0041e081  c744241405000000         mov dword ptr [esp + 0x14], 5
0041e089  eb23                     jmp 0x41e0ae
0041e08b  c744241407000000         mov dword ptr [esp + 0x14], 7
0041e093  eb19                     jmp 0x41e0ae
0041e095  31db                     xor ebx, ebx
0041e097  8a4608                   mov al, byte ptr [esi + 8]
0041e09a  8a5e04                   mov bl, byte ptr [esi + 4]
0041e09d  3c15                     cmp al, 0x15
0041e09f  770d                     ja 0x41e0ae
0041e0a1  25ff000000               and eax, 0xff
0041e0a6  2eff248588dd4100         jmp dword ptr cs:[eax*4 + 0x41dd88]
0041e0ae  31c0                     xor eax, eax
0041e0b0  31d2                     xor edx, edx
0041e0b2  668b0424                 mov ax, word ptr [esp]
0041e0b6  668b542414               mov dx, word ptr [esp + 0x14]
0041e0bb  e822ceffff               call 0x41aee2
0041e0c0  25ffff0000               and eax, 0xffff
0041e0c5  e8b88d0500               call 0x476e82
0041e0ca  31db                     xor ebx, ebx
0041e0cc  31d2                     xor edx, edx
0041e0ce  668b1c24                 mov bx, word ptr [esp]
0041e0d2  8a5604                   mov dl, byte ptr [esi + 4]
0041e0d5  89d8                     mov eax, ebx
0041e0d7  e83bdfffff               call 0x41c017
0041e0dc  89d8                     mov eax, ebx
0041e0de  c1e004                   shl eax, 4
0041e0e1  01d8                     add eax, ebx
0041e0e3  c1e002                   shl eax, 2
0041e0e6  01d8                     add eax, ebx
0041e0e8  c1e002                   shl eax, 2
0041e0eb  05c8a04900               add eax, 0x49a0c8
0041e0f0  8a4008                   mov al, byte ptr [eax + 8]
0041e0f3  89da                     mov edx, ebx
0041e0f5  3c01                     cmp al, 1
0041e0f7  7210                     jb 0x41e109
0041e0f9  3c02                     cmp al, 2
0041e0fb  0f868a000000             jbe 0x41e18b
0041e101  3c05                     cmp al, 5
0041e103  0f8482000000             je 0x41e18b
0041e109  8a4604                   mov al, byte ptr [esi + 4]
0041e10c  25ff000000               and eax, 0xff
0041e111  66c70445e05b4900ffff     mov word ptr [eax*2 + 0x495be0], 0xffff
0041e11b  31db                     xor ebx, ebx
0041e11d  668b1c24                 mov bx, word ptr [esp]
0041e121  ba01000000               mov edx, 1
0041e126  89d8                     mov eax, ebx
0041e128  c64604c8                 mov byte ptr [esi + 4], 0xc8
0041e12c  e866bdffff               call 0x419e97
0041e131  89d8                     mov eax, ebx
0041e133  c1e004                   shl eax, 4
0041e136  01d8                     add eax, ebx
0041e138  c1e002                   shl eax, 2
0041e13b  01d8                     add eax, ebx
0041e13d  bac8a04900               mov edx, 0x49a0c8
0041e142  c1e002                   shl eax, 2
0041e145  01c2                     add edx, eax
0041e147  8a0d41805000             mov cl, byte ptr [0x508041]
0041e14d  3a4a04                   cmp cl, byte ptr [edx + 4]
0041e150  7532                     jne 0x41e184
0041e152  89d8                     mov eax, ebx
0041e154  e852bfffff               call 0x41a0ab
0041e159  83ba00010000ff           cmp dword ptr [edx + 0x100], -1
0041e160  7522                     jne 0x41e184
0041e162  8d9a00010000             lea ebx, [edx + 0x100]
0041e168  50                       push eax
0041e169  8a5208                   mov dl, byte ptr [edx + 8]
0041e16c  81e2ff000000             and edx, 0xff
0041e172  b842000000               mov eax, 0x42
0041e177  c1e210                   shl edx, 0x10
0041e17a  31c9                     xor ecx, ecx
0041e17c  80ce26                   or dh, 0x26
0041e17f  e8f5c80600               call 0x48aa79
0041e184  89f8                     mov eax, edi
0041e186  e994d1ffff               jmp 0x41b31f
0041e18b  81e2ffff0000             and edx, 0xffff
0041e191  89d0                     mov eax, edx
0041e193  c1e004                   shl eax, 4
0041e196  01d0                     add eax, edx
0041e198  c1e002                   shl eax, 2
0041e19b  01d0                     add eax, edx
0041e19d  c1e002                   shl eax, 2
0041e1a0  05c8a04900               add eax, 0x49a0c8
0041e1a5  66c74078ffff             mov word ptr [eax + 0x78], 0xffff
0041e1ab  c6407bff                 mov byte ptr [eax + 0x7b], 0xff
0041e1af  66c7407c0000             mov word ptr [eax + 0x7c], 0
0041e1b5  31d2                     xor edx, edx
0041e1b7  66c7407e0000             mov word ptr [eax + 0x7e], 0
0041e1bd  8a5008                   mov dl, byte ptr [eax + 8]
0041e1c0  66c78086000000ffff       mov word ptr [eax + 0x86], 0xffff
0041e1c9  83fa14                   cmp edx, 0x14
0041e1cc  7412                     je 0x41e1e0
0041e1ce  66c780800000000000       mov word ptr [eax + 0x80], 0
0041e1d7  66c780820000000000       mov word ptr [eax + 0x82], 0
0041e1e0  c6407400                 mov byte ptr [eax + 0x74], 0
0041e1e4  31d2                     xor edx, edx
0041e1e6  8a5005                   mov dl, byte ptr [eax + 5]
0041e1e9  c7808c00000000000000     mov dword ptr [eax + 0x8c], 0
0041e1f3  83fa03                   cmp edx, 3
0041e1f6  0f840dffffff             je 0x41e109
0041e1fc  c6400505                 mov byte ptr [eax + 5], 5
0041e200  e904ffffff               jmp 0x41e109
0041e205  8d4000                   lea eax, [eax]
0041e208  8ce3                     mov ebx, fs
0041e20a  41                       inc ecx
0041e20b  00e3                     add bl, ah
0041e20d  e341                     jecxz 0x41e250
0041e20f  00ce                     add dh, cl
0041e211  e441                     in al, 0x41
0041e213  00c7                     add bh, al
0041e215  e541                     in eax, 0x41
0041e217  0058ea                   add byte ptr [eax - 0x16], bl
0041e21a  41                       inc ecx
0041e21b  009ae2410052             add byte ptr [edx + 0x520041e2], bl
0041e221  ed                       in eax, dx
0041e222  41                       inc ecx
0041e223  00c1                     add cl, al
0041e225  eb41                     jmp 0x41e268
0041e227  001e                     add byte ptr [esi], bl
0041e229  eb41                     jmp 0x41e26c
0041e22b  008ab7410003             add byte ptr [edx + 0x30041b7], cl
0041e231  ed                       in eax, dx
0041e232  41                       inc ecx
0041e233  0003                     add byte ptr [ebx], al
0041e235  ed                       in eax, dx
0041e236  41                       inc ecx
0041e237  008ab7410016             add byte ptr [edx + 0x160041b7], cl
0041e23d  e741                     out 0x41, eax
0041e23f  008ee74100c2             add byte ptr [esi - 0x3dffbe19], cl
0041e245  e9410048e8               jmp 0xe889e28b
0041e24a  41                       inc ecx
0041e24b  0061e9                   add byte ptr [ecx - 0x17], ah
0041e24e  41                       inc ecx
0041e24f  0066ec                   add byte ptr [esi - 0x14], ah
0041e252  41                       inc ecx
0041e253  00f4                     add ah, dh
0041e255  e84100c2e9               call 0xea03e29b
0041e25a  41                       inc ecx
0041e25b  00f4                     add ah, dh
; 3 trailing bytes are not code (alignment/data): e84100
