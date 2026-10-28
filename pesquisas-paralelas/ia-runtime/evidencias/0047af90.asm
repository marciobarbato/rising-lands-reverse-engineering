; InitMissionMonstre (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047af90..0x0047b283 (end exclusive); labels are original SBL names
0047af90  53                       push ebx
0047af91  51                       push ecx
0047af92  52                       push edx
0047af93  56                       push esi
0047af94  57                       push edi
0047af95  55                       push ebp
0047af96  83ec30                   sub esp, 0x30
0047af99  30e4                     xor ah, ah
0047af9b  31d2                     xor edx, edx
0047af9d  8825cca95000             mov byte ptr [0x50a9cc], ah
0047afa3  891580ae5000             mov dword ptr [0x50ae80], edx
0047afa9  882534b15000             mov byte ptr [0x50b134], ah
0047afaf  891578b15000             mov dword ptr [0x50b178], edx
0047afb5  ba10000000               mov edx, 0x10
0047afba  b804000000               mov eax, 4
0047afbf  e8148c0000               call 0x483bd8 ; -> iaGroupNew
0047afc4  89c1                     mov ecx, eax
0047afc6  83f8ff                   cmp eax, -1
0047afc9  0f84ac020000             je 0x47b27b
0047afcf  31f6                     xor esi, esi
0047afd1  89742420                 mov dword ptr [esp + 0x20], esi
0047afd5  eb11                     jmp 0x47afe8
0047afd7  8b7c2420                 mov edi, dword ptr [esp + 0x20]
0047afdb  47                       inc edi
0047afdc  897c2420                 mov dword ptr [esp + 0x20], edi
0047afe0  81ff20030000             cmp edi, 0x320
0047afe6  7d44                     jge 0x47b02c
0047afe8  31db                     xor ebx, ebx
0047afea  668b5c2420               mov bx, word ptr [esp + 0x20]
0047afef  89d8                     mov eax, ebx
0047aff1  e8b78dfcff               call 0x443dad ; -> EnginEstVivant
0047aff6  84c0                     test al, al
0047aff8  74dd                     je 0x47afd7
0047affa  89d8                     mov eax, ebx
0047affc  e82470fcff               call 0x442025 ; -> EnginGetType
0047b001  25ff000000               and eax, 0xff
0047b006  e8d272fcff               call 0x4422dd ; -> TypeEnginEstMonstre
0047b00b  84c0                     test al, al
0047b00d  74c8                     je 0x47afd7
0047b00f  89da                     mov edx, ebx
0047b011  89c8                     mov eax, ecx
0047b013  e821790000               call 0x482939 ; -> iagUnitAddToGroup
0047b018  ba04000000               mov edx, 4
0047b01d  89d8                     mov eax, ebx
0047b01f  e8e480fcff               call 0x443108 ; -> EnginSetPlayer
0047b024  ff0578b15000             inc dword ptr [0x50b178]
0047b02a  ebab                     jmp 0x47afd7
0047b02c  e8e910ffff               call 0x46c11a ; -> MissionGetNum
0047b031  25ffff0000               and eax, 0xffff
0047b036  83f817                   cmp eax, 0x17
0047b039  751c                     jne 0x47b057
0047b03b  a034b15000               mov al, byte ptr [0x50b134]
0047b040  31db                     xor ebx, ebx
0047b042  88c3                     mov bl, al
0047b044  fec0                     inc al
0047b046  890c9d38b15000           mov dword ptr [ebx*4 + 0x50b138], ecx
0047b04d  a234b15000               mov byte ptr [0x50b134], al
0047b052  e924020000               jmp 0x47b27b
0047b057  31c0                     xor eax, eax
0047b059  89442428                 mov dword ptr [esp + 0x28], eax
0047b05d  89442420                 mov dword ptr [esp + 0x20], eax
0047b061  eb0e                     jmp 0x47b071
0047b063  8b742420                 mov esi, dword ptr [esp + 0x20]
0047b067  46                       inc esi
0047b068  89742420                 mov dword ptr [esp + 0x20], esi
0047b06c  83fe10                   cmp esi, 0x10
0047b06f  7d36                     jge 0x47b0a7
0047b071  8b5c2420                 mov ebx, dword ptr [esp + 0x20]
0047b075  31c0                     xor eax, eax
0047b077  8a8324b15000             mov al, byte ptr [ebx + 0x50b124]
0047b07d  85c0                     test eax, eax
0047b07f  74e2                     je 0x47b063
0047b081  8b442428                 mov eax, dword ptr [esp + 0x28]
0047b085  8a5c2420                 mov bl, byte ptr [esp + 0x20]
0047b089  885c0410                 mov byte ptr [esp + eax + 0x10], bl
0047b08d  8b442420                 mov eax, dword ptr [esp + 0x20]
0047b091  8b5c2428                 mov ebx, dword ptr [esp + 0x28]
0047b095  8a8024b15000             mov al, byte ptr [eax + 0x50b124]
0047b09b  88041c                   mov byte ptr [esp + ebx], al
0047b09e  8d4301                   lea eax, [ebx + 1]
0047b0a1  89442428                 mov dword ptr [esp + 0x28], eax
0047b0a5  ebbc                     jmp 0x47b063
0047b0a7  31ed                     xor ebp, ebp
0047b0a9  8b742428                 mov esi, dword ptr [esp + 0x28]
0047b0ad  896c2420                 mov dword ptr [esp + 0x20], ebp
0047b0b1  4e                       dec esi
0047b0b2  eb04                     jmp 0x47b0b8
0047b0b4  ff442420                 inc dword ptr [esp + 0x20]
0047b0b8  8b542420                 mov edx, dword ptr [esp + 0x20]
0047b0bc  39d6                     cmp esi, edx
0047b0be  7e3b                     jle 0x47b0fb
0047b0c0  8d5a01                   lea ebx, [edx + 1]
0047b0c3  eb01                     jmp 0x47b0c6
0047b0c5  43                       inc ebx
0047b0c6  3b5c2428                 cmp ebx, dword ptr [esp + 0x28]
0047b0ca  7de8                     jge 0x47b0b4
0047b0cc  8b442420                 mov eax, dword ptr [esp + 0x20]
0047b0d0  8a341c                   mov dh, byte ptr [esp + ebx]
0047b0d3  3a3404                   cmp dh, byte ptr [esp + eax]
0047b0d6  76ed                     jbe 0x47b0c5
0047b0d8  8b442420                 mov eax, dword ptr [esp + 0x20]
0047b0dc  8b7c2420                 mov edi, dword ptr [esp + 0x20]
0047b0e0  8a0404                   mov al, byte ptr [esp + eax]
0047b0e3  88343c                   mov byte ptr [esp + edi], dh
0047b0e6  88041c                   mov byte ptr [esp + ebx], al
0047b0e9  8a443c10                 mov al, byte ptr [esp + edi + 0x10]
0047b0ed  8a641c10                 mov ah, byte ptr [esp + ebx + 0x10]
0047b0f1  88643c10                 mov byte ptr [esp + edi + 0x10], ah
0047b0f5  88441c10                 mov byte ptr [esp + ebx + 0x10], al
0047b0f9  ebca                     jmp 0x47b0c5
0047b0fb  31db                     xor ebx, ebx
0047b0fd  895c2420                 mov dword ptr [esp + 0x20], ebx
0047b101  eb04                     jmp 0x47b107
0047b103  ff442420                 inc dword ptr [esp + 0x20]
0047b107  8b442420                 mov eax, dword ptr [esp + 0x20]
0047b10b  3b442428                 cmp eax, dword ptr [esp + 0x28]
0047b10f  0f8d0e010000             jge 0x47b223
0047b115  833d78b1500032           cmp dword ptr [0x50b178], 0x32
0047b11c  0f8d01010000             jge 0x47b223
0047b122  31c0                     xor eax, eax
0047b124  a034b15000               mov al, byte ptr [0x50b134]
0047b129  83f810                   cmp eax, 0x10
0047b12c  0f8df1000000             jge 0x47b223
0047b132  c644242c01               mov byte ptr [esp + 0x2c], 1
0047b137  807c242c00               cmp byte ptr [esp + 0x2c], 0
0047b13c  74c5                     je 0x47b103
0047b13e  833d78b1500032           cmp dword ptr [0x50b178], 0x32
0047b145  7dbc                     jge 0x47b103
0047b147  31c0                     xor eax, eax
0047b149  a034b15000               mov al, byte ptr [0x50b134]
0047b14e  83f810                   cmp eax, 0x10
0047b151  7db0                     jge 0x47b103
0047b153  ba10000000               mov edx, 0x10
0047b158  b804000000               mov eax, 4
0047b15d  e8768a0000               call 0x483bd8 ; -> iaGroupNew
0047b162  89c5                     mov ebp, eax
0047b164  83f8ff                   cmp eax, -1
0047b167  749a                     je 0x47b103
0047b169  31ff                     xor edi, edi
0047b16b  eb3c                     jmp 0x47b1a9
0047b16d  81e3ffff0000             and ebx, 0xffff
0047b173  89c8                     mov eax, ecx
0047b175  89da                     mov edx, ebx
0047b177  e835810000               call 0x4832b1 ; -> iagUnitRemoveFromGroup
0047b17c  89da                     mov edx, ebx
0047b17e  89e8                     mov eax, ebp
0047b180  46                       inc esi
0047b181  e8b3770000               call 0x482939 ; -> iagUnitAddToGroup
0047b186  3b742424                 cmp esi, dword ptr [esp + 0x24]
0047b18a  7d1c                     jge 0x47b1a8
0047b18c  89ca                     mov edx, ecx
0047b18e  89f8                     mov eax, edi
0047b190  31db                     xor ebx, ebx
0047b192  e8b0850000               call 0x483747 ; -> iagUnitFindTypeIntoGroup
0047b197  6689c3                   mov bx, ax
0047b19a  81fbffff0000             cmp ebx, 0xffff
0047b1a0  75cb                     jne 0x47b16d
0047b1a2  30c0                     xor al, al
0047b1a4  8844242c                 mov byte ptr [esp + 0x2c], al
0047b1a8  47                       inc edi
0047b1a9  83ff1a                   cmp edi, 0x1a
0047b1ac  7d27                     jge 0x47b1d5
0047b1ae  833d78b1500032           cmp dword ptr [0x50b178], 0x32
0047b1b5  7d1e                     jge 0x47b1d5
0047b1b7  8b442420                 mov eax, dword ptr [esp + 0x20]
0047b1bb  31db                     xor ebx, ebx
0047b1bd  8a5c0410                 mov bl, byte ptr [esp + eax + 0x10]
0047b1c1  6bdb1a                   imul ebx, ebx, 0x1a
0047b1c4  31c0                     xor eax, eax
0047b1c6  8a841f84af5000           mov al, byte ptr [edi + ebx + 0x50af84]
0047b1cd  31f6                     xor esi, esi
0047b1cf  89442424                 mov dword ptr [esp + 0x24], eax
0047b1d3  ebb1                     jmp 0x47b186
0047b1d5  89e8                     mov eax, ebp
0047b1d7  e814860000               call 0x4837f0 ; -> iagUnitGetFirstUnitInGroup
0047b1dc  25ffff0000               and eax, 0xffff
0047b1e1  3dffff0000               cmp eax, 0xffff
0047b1e6  7511                     jne 0x47b1f9
0047b1e8  b804000000               mov eax, 4
0047b1ed  89ea                     mov edx, ebp
0047b1ef  e8f38a0000               call 0x483ce7 ; -> iaGroupDelete
0047b1f4  e93effffff               jmp 0x47b137
0047b1f9  31c0                     xor eax, eax
0047b1fb  a034b15000               mov al, byte ptr [0x50b134]
0047b200  83f810                   cmp eax, 0x10
0047b203  0f8dfafeffff             jge 0x47b103
0047b209  88c3                     mov bl, al
0047b20b  31c0                     xor eax, eax
0047b20d  88d8                     mov al, bl
0047b20f  fec3                     inc bl
0047b211  892c8538b15000           mov dword ptr [eax*4 + 0x50b138], ebp
0047b218  881d34b15000             mov byte ptr [0x50b134], bl
0047b21e  e914ffffff               jmp 0x47b137
0047b223  89c8                     mov eax, ecx
0047b225  e8c6850000               call 0x4837f0 ; -> iagUnitGetFirstUnitInGroup
0047b22a  25ffff0000               and eax, 0xffff
0047b22f  3dffff0000               cmp eax, 0xffff
0047b234  750e                     jne 0x47b244
0047b236  b804000000               mov eax, 4
0047b23b  89ca                     mov edx, ecx
0047b23d  e8a58a0000               call 0x483ce7 ; -> iaGroupDelete
0047b242  eb21                     jmp 0x47b265
0047b244  31c0                     xor eax, eax
0047b246  a034b15000               mov al, byte ptr [0x50b134]
0047b24b  83f810                   cmp eax, 0x10
0047b24e  7d15                     jge 0x47b265
0047b250  88c3                     mov bl, al
0047b252  31c0                     xor eax, eax
0047b254  88d8                     mov al, bl
0047b256  fec3                     inc bl
0047b258  890c8538b15000           mov dword ptr [eax*4 + 0x50b138], ecx
0047b25f  881d34b15000             mov byte ptr [0x50b134], bl
0047b265  b9ffff0000               mov ecx, 0xffff
0047b26a  be03000000               mov esi, 3
0047b26f  890d80b15000             mov dword ptr [0x50b180], ecx
0047b275  89357cb15000             mov dword ptr [0x50b17c], esi
0047b27b  83c430                   add esp, 0x30
0047b27e  e993f5ffff               jmp 0x47a816

; shared Watcom tail reached from InitMissionMonstre; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047a816..0x0047a81d (end exclusive); labels are original SBL names
0047a816  5d                       pop ebp
0047a817  5f                       pop edi
0047a818  5e                       pop esi
0047a819  5a                       pop edx
0047a81a  59                       pop ecx
0047a81b  5b                       pop ebx
0047a81c  c3                       ret
