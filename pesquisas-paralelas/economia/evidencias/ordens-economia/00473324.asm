; SetMineEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473324  53                       push ebx
00473325  51                       push ecx
00473326  56                       push esi
00473327  57                       push edi
00473328  83ec08                   sub esp, 8
0047332b  88442404                 mov byte ptr [esp + 4], al
0047332f  891424                   mov dword ptr [esp], edx
00473332  31ff                     xor edi, edi
00473334  31f6                     xor esi, esi
00473336  eb01                     jmp 0x473339
00473338  46                       inc esi
00473339  31c9                     xor ecx, ecx
0047333b  8a4c2404                 mov cl, byte ptr [esp + 4]
0047333f  c1e109                   shl ecx, 9
00473342  663bb128875000           cmp si, word ptr [ecx + 0x508728]
00473349  0f83b4f5ffff             jae 0x472903
0047334f  31d2                     xor edx, edx
00473351  6689f2                   mov dx, si
00473354  668b94512a875000         mov dx, word ptr [ecx + edx*2 + 0x50872a]
0047335c  31c9                     xor ecx, ecx
0047335e  6689d1                   mov cx, dx
00473361  69c114010000             imul eax, ecx, 0x114
00473367  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0047336d  01c2                     add edx, eax
0047336f  89c8                     mov eax, ecx
00473371  e8370afdff               call 0x443dad
00473376  84c0                     test al, al
00473378  74be                     je 0x473338
0047337a  8a02                     mov al, byte ptr [edx]
0047337c  3a442404                 cmp al, byte ptr [esp + 4]
00473380  75b6                     jne 0x473338
00473382  31d2                     xor edx, edx
00473384  89c8                     mov eax, ecx
00473386  668b1424                 mov dx, word ptr [esp]
0047338a  e8b91bfdff               call 0x444f48
0047338f  31d2                     xor edx, edx
00473391  6689fa                   mov dx, di
00473394  83fa01                   cmp edx, 1
00473397  7d9f                     jge 0x473338
00473399  8a442404                 mov al, byte ptr [esp + 4]
0047339d  8a1541805000             mov dl, byte ptr [0x508041]
004733a3  47                       inc edi
004733a4  38d0                     cmp al, dl
004733a6  7590                     jne 0x473338
004733a8  ba0f000000               mov edx, 0xf
004733ad  89c8                     mov eax, ecx
004733af  31db                     xor ebx, ebx
004733b1  e8a8d9fcff               call 0x440d5e
004733b6  eb80                     jmp 0x473338
