; SetConstruitBatimentSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473a07  51                       push ecx
00473a08  56                       push esi
00473a09  57                       push edi
00473a0a  83ec0c                   sub esp, 0xc
00473a0d  88442408                 mov byte ptr [esp + 8], al
00473a11  88542404                 mov byte ptr [esp + 4], dl
00473a15  891c24                   mov dword ptr [esp], ebx
00473a18  31ff                     xor edi, edi
00473a1a  31f6                     xor esi, esi
00473a1c  eb01                     jmp 0x473a1f
00473a1e  46                       inc esi
00473a1f  31d2                     xor edx, edx
00473a21  8a542408                 mov dl, byte ptr [esp + 8]
00473a25  c1e209                   shl edx, 9
00473a28  663bb228875000           cmp si, word ptr [edx + 0x508728]
00473a2f  0f8384000000             jae 0x473ab9
00473a35  31db                     xor ebx, ebx
00473a37  6689f3                   mov bx, si
00473a3a  31c9                     xor ecx, ecx
00473a3c  668b945a2a875000         mov dx, word ptr [edx + ebx*2 + 0x50872a]
00473a44  6689d1                   mov cx, dx
00473a47  69d114010000             imul edx, ecx, 0x114
00473a4d  89c8                     mov eax, ecx
00473a4f  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00473a55  e85303fdff               call 0x443dad
00473a5a  01da                     add edx, ebx
00473a5c  84c0                     test al, al
00473a5e  74be                     je 0x473a1e
00473a60  8a02                     mov al, byte ptr [edx]
00473a62  3a442408                 cmp al, byte ptr [esp + 8]
00473a66  75b6                     jne 0x473a1e
00473a68  8a5201                   mov dl, byte ptr [edx + 1]
00473a6b  81e2ff000000             and edx, 0xff
00473a71  83fa07                   cmp edx, 7
00473a74  75a8                     jne 0x473a1e
00473a76  89c8                     mov eax, ecx
00473a78  31db                     xor ebx, ebx
00473a7a  31d2                     xor edx, edx
00473a7c  668b1c24                 mov bx, word ptr [esp]
00473a80  8a542404                 mov dl, byte ptr [esp + 4]
00473a84  e8451afdff               call 0x4454ce
00473a89  31d2                     xor edx, edx
00473a8b  6689fa                   mov dx, di
00473a8e  83fa01                   cmp edx, 1
00473a91  7d8b                     jge 0x473a1e
00473a93  8a442408                 mov al, byte ptr [esp + 8]
00473a97  8a1541805000             mov dl, byte ptr [0x508041]
00473a9d  47                       inc edi
00473a9e  38d0                     cmp al, dl
00473aa0  0f8578ffffff             jne 0x473a1e
00473aa6  ba11000000               mov edx, 0x11
00473aab  89c8                     mov eax, ecx
00473aad  31db                     xor ebx, ebx
00473aaf  e8aad2fcff               call 0x440d5e
00473ab4  e965ffffff               jmp 0x473a1e
00473ab9  83c40c                   add esp, 0xc
00473abc  5f                       pop edi
00473abd  5e                       pop esi
00473abe  59                       pop ecx
00473abf  c3                       ret
