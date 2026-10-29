; SetTransporteEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473212  53                       push ebx
00473213  51                       push ecx
00473214  56                       push esi
00473215  57                       push edi
00473216  83ec08                   sub esp, 8
00473219  88442404                 mov byte ptr [esp + 4], al
0047321d  891424                   mov dword ptr [esp], edx
00473220  31ff                     xor edi, edi
00473222  31f6                     xor esi, esi
00473224  eb01                     jmp 0x473227
00473226  46                       inc esi
00473227  31c9                     xor ecx, ecx
00473229  8a4c2404                 mov cl, byte ptr [esp + 4]
0047322d  c1e109                   shl ecx, 9
00473230  663bb128875000           cmp si, word ptr [ecx + 0x508728]
00473237  0f83c6f6ffff             jae 0x472903
0047323d  31d2                     xor edx, edx
0047323f  6689f2                   mov dx, si
00473242  668b94512a875000         mov dx, word ptr [ecx + edx*2 + 0x50872a]
0047324a  31c9                     xor ecx, ecx
0047324c  6689d1                   mov cx, dx
0047324f  89c8                     mov eax, ecx
00473251  e8570bfdff               call 0x443dad
00473256  84c0                     test al, al
00473258  74cc                     je 0x473226
0047325a  31d2                     xor edx, edx
0047325c  89c8                     mov eax, ecx
0047325e  668b1424                 mov dx, word ptr [esp]
00473262  e8181cfdff               call 0x444e7f
00473267  31d2                     xor edx, edx
00473269  6689fa                   mov dx, di
0047326c  83fa01                   cmp edx, 1
0047326f  7db5                     jge 0x473226
00473271  8a442404                 mov al, byte ptr [esp + 4]
00473275  8a2541805000             mov ah, byte ptr [0x508041]
0047327b  47                       inc edi
0047327c  38e0                     cmp al, ah
0047327e  75a6                     jne 0x473226
00473280  ba0f000000               mov edx, 0xf
00473285  89c8                     mov eax, ecx
00473287  31db                     xor ebx, ebx
00473289  e8d0dafcff               call 0x440d5e
0047328e  eb96                     jmp 0x473226
