; CreerBatiment_first_free_scan; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041fea2  51                       push ecx
0041fea3  56                       push esi
0041fea4  57                       push edi
0041fea5  55                       push ebp
0041fea6  83ec54                   sub esp, 0x54
0041fea9  50                       push eax
0041feaa  88542454                 mov byte ptr [esp + 0x54], dl
0041feae  885c2450                 mov byte ptr [esp + 0x50], bl
0041feb2  31d2                     xor edx, edx
0041feb4  89542428                 mov dword ptr [esp + 0x28], edx
0041feb8  8954240c                 mov dword ptr [esp + 0xc], edx
0041febc  8954241c                 mov dword ptr [esp + 0x1c], edx
0041fec0  89542424                 mov dword ptr [esp + 0x24], edx
0041fec4  31c0                     xor eax, eax
0041fec6  668b442424               mov ax, word ptr [esp + 0x24]
0041fecb  3de8030000               cmp eax, 0x3e8
0041fed0  7d20                     jge 0x41fef2
0041fed2  69c014010000             imul eax, eax, 0x114
0041fed8  05c8a04900               add eax, 0x49a0c8
0041fedd  8a4005                   mov al, byte ptr [eax + 5]
0041fee0  25ff000000               and eax, 0xff
0041fee5  0f95c0                   setne al
0041fee8  84c0                     test al, al
0041feea  7406                     je 0x41fef2
0041feec  ff442424                 inc dword ptr [esp + 0x24]
0041fef0  ebd2                     jmp 0x41fec4
0041fef2  31c0                     xor eax, eax
0041fef4  668b442424               mov ax, word ptr [esp + 0x24]
0041fef9  3de8030000               cmp eax, 0x3e8
0041fefe  0f84bd030000             je 0x4202c1
