; SetEnginSelectRentreBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473f4b  53                       push ebx
00473f4c  51                       push ecx
00473f4d  56                       push esi
00473f4e  57                       push edi
00473f4f  83ec10                   sub esp, 0x10
00473f52  88442408                 mov byte ptr [esp + 8], al
00473f56  891424                   mov dword ptr [esp], edx
00473f59  31c0                     xor eax, eax
00473f5b  31ff                     xor edi, edi
00473f5d  6689d0                   mov ax, dx
00473f60  31f6                     xor esi, esi
00473f62  e88d65faff               call 0x41a4f4
00473f67  8844240c                 mov byte ptr [esp + 0xc], al
00473f6b  eb18                     jmp 0x473f85
00473f6d  31c0                     xor eax, eax
00473f6f  88d8                     mov al, bl
00473f71  83f80a                   cmp eax, 0xa
00473f74  740e                     je 0x473f84
00473f76  ba0a000000               mov edx, 0xa
00473f7b  89c8                     mov eax, ecx
00473f7d  31db                     xor ebx, ebx
00473f7f  e8dacdfcff               call 0x440d5e
00473f84  46                       inc esi
00473f85  31c9                     xor ecx, ecx
00473f87  8a4c2408                 mov cl, byte ptr [esp + 8]
00473f8b  c1e109                   shl ecx, 9
00473f8e  663bb128875000           cmp si, word ptr [ecx + 0x508728]
00473f95  0f83c4000000             jae 0x47405f
00473f9b  31c0                     xor eax, eax
00473f9d  6689f0                   mov ax, si
00473fa0  668b84412a875000         mov ax, word ptr [ecx + eax*2 + 0x50872a]
00473fa8  31c9                     xor ecx, ecx
00473faa  6689c1                   mov cx, ax
00473fad  89442404                 mov dword ptr [esp + 4], eax
00473fb1  89c8                     mov eax, ecx
00473fb3  e8f5fdfcff               call 0x443dad
00473fb8  84c0                     test al, al
00473fba  74c8                     je 0x473f84
00473fbc  89c8                     mov eax, ecx
00473fbe  31d2                     xor edx, edx
00473fc0  e860e0fcff               call 0x442025
00473fc5  668b1424                 mov dx, word ptr [esp]
00473fc9  88c3                     mov bl, al
00473fcb  89c8                     mov eax, ecx
00473fcd  e83e1bfdff               call 0x445b10
00473fd2  31c0                     xor eax, eax
00473fd4  6689f8                   mov ax, di
00473fd7  83f801                   cmp eax, 1
00473fda  7da8                     jge 0x473f84
00473fdc  8a442408                 mov al, byte ptr [esp + 8]
00473fe0  8a2541805000             mov ah, byte ptr [0x508041]
00473fe6  47                       inc edi
00473fe7  38e0                     cmp al, ah
00473fe9  743b                     je 0x474026
00473feb  eb97                     jmp 0x473f84
00473fed  31d2                     xor edx, edx
00473fef  88da                     mov dl, bl
00473ff1  83fa09                   cmp edx, 9
00473ff4  750a                     jne 0x474000
00473ff6  ba19000000               mov edx, 0x19
00473ffb  e97bffffff               jmp 0x473f7b
00474000  83fa0a                   cmp edx, 0xa
00474003  0f857bffffff             jne 0x473f84
00474009  ba24000000               mov edx, 0x24
0047400e  e968ffffff               jmp 0x473f7b
00474013  ba0e000000               mov edx, 0xe
00474018  31c0                     xor eax, eax
0047401a  31db                     xor ebx, ebx
0047401c  668b442404               mov ax, word ptr [esp + 4]
00474021  e959ffffff               jmp 0x473f7f
00474026  8a54240c                 mov dl, byte ptr [esp + 0xc]
0047402a  80fa0a                   cmp dl, 0xa
0047402d  7217                     jb 0x474046
0047402f  76e2                     jbe 0x474013
00474031  80fa0d                   cmp dl, 0xd
00474034  0f824affffff             jb 0x473f84
0047403a  76d7                     jbe 0x474013
0047403c  80fa10                   cmp dl, 0x10
0047403f  74ac                     je 0x473fed
00474041  e93effffff               jmp 0x473f84
00474046  80fa01                   cmp dl, 1
00474049  0f8235ffffff             jb 0x473f84
0047404f  76c2                     jbe 0x474013
00474051  80fa02                   cmp dl, 2
00474054  0f8413ffffff             je 0x473f6d
0047405a  e925ffffff               jmp 0x473f84
0047405f  83c410                   add esp, 0x10
00474062  5f                       pop edi
00474063  5e                       pop esi
00474064  59                       pop ecx
00474065  5b                       pop ebx
00474066  c3                       ret
