; SetRecolteEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473290  53                       push ebx
00473291  51                       push ecx
00473292  56                       push esi
00473293  57                       push edi
00473294  83ec08                   sub esp, 8
00473297  88442404                 mov byte ptr [esp + 4], al
0047329b  891424                   mov dword ptr [esp], edx
0047329e  31ff                     xor edi, edi
004732a0  31f6                     xor esi, esi
004732a2  eb01                     jmp 0x4732a5
004732a4  46                       inc esi
004732a5  31c9                     xor ecx, ecx
004732a7  8a4c2404                 mov cl, byte ptr [esp + 4]
004732ab  c1e109                   shl ecx, 9
004732ae  663bb128875000           cmp si, word ptr [ecx + 0x508728]
004732b5  0f8348f6ffff             jae 0x472903
004732bb  31d2                     xor edx, edx
004732bd  6689f2                   mov dx, si
004732c0  668b94512a875000         mov dx, word ptr [ecx + edx*2 + 0x50872a]
004732c8  31c9                     xor ecx, ecx
004732ca  6689d1                   mov cx, dx
004732cd  69c114010000             imul eax, ecx, 0x114
004732d3  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004732d9  01c2                     add edx, eax
004732db  89c8                     mov eax, ecx
004732dd  e8cb0afdff               call 0x443dad
004732e2  84c0                     test al, al
004732e4  74be                     je 0x4732a4
004732e6  8a02                     mov al, byte ptr [edx]
004732e8  3a442404                 cmp al, byte ptr [esp + 4]
004732ec  75b6                     jne 0x4732a4
004732ee  31d2                     xor edx, edx
004732f0  89c8                     mov eax, ecx
004732f2  668b1424                 mov dx, word ptr [esp]
004732f6  e8c21bfdff               call 0x444ebd
004732fb  31d2                     xor edx, edx
004732fd  6689fa                   mov dx, di
00473300  83fa01                   cmp edx, 1
00473303  7d9f                     jge 0x4732a4
00473305  8a442404                 mov al, byte ptr [esp + 4]
00473309  8a1541805000             mov dl, byte ptr [0x508041]
0047330f  47                       inc edi
00473310  38d0                     cmp al, dl
00473312  7590                     jne 0x4732a4
00473314  ba0f000000               mov edx, 0xf
00473319  89c8                     mov eax, ecx
0047331b  31db                     xor ebx, ebx
0047331d  e83cdafcff               call 0x440d5e
00473322  eb80                     jmp 0x4732a4
