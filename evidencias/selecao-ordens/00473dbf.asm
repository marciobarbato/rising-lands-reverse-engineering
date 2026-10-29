; SetAttaqueEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473dbf  51                       push ecx
00473dc0  56                       push esi
00473dc1  57                       push edi
00473dc2  83ec0c                   sub esp, 0xc
00473dc5  88442408                 mov byte ptr [esp + 8], al
00473dc9  88542404                 mov byte ptr [esp + 4], dl
00473dcd  891c24                   mov dword ptr [esp], ebx
00473dd0  31ff                     xor edi, edi
00473dd2  31f6                     xor esi, esi
00473dd4  eb01                     jmp 0x473dd7
00473dd6  46                       inc esi
00473dd7  31c0                     xor eax, eax
00473dd9  8a442408                 mov al, byte ptr [esp + 8]
00473ddd  c1e009                   shl eax, 9
00473de0  663bb028875000           cmp si, word ptr [eax + 0x508728]
00473de7  0f83ccfcffff             jae 0x473ab9
00473ded  31d2                     xor edx, edx
00473def  6689f2                   mov dx, si
00473df2  31c9                     xor ecx, ecx
00473df4  668b84502a875000         mov ax, word ptr [eax + edx*2 + 0x50872a]
00473dfc  6689c1                   mov cx, ax
00473dff  89c8                     mov eax, ecx
00473e01  e8a7fffcff               call 0x443dad
00473e06  84c0                     test al, al
00473e08  74cc                     je 0x473dd6
00473e0a  69d114010000             imul edx, ecx, 0x114
00473e10  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00473e15  01d0                     add eax, edx
00473e17  8a10                     mov dl, byte ptr [eax]
00473e19  3a542408                 cmp dl, byte ptr [esp + 8]
00473e1d  75b7                     jne 0x473dd6
00473e1f  31db                     xor ebx, ebx
00473e21  8b157c8f5000             mov edx, dword ptr [0x508f7c]
00473e27  668b1c24                 mov bx, word ptr [esp]
00473e2b  899010010000             mov dword ptr [eax + 0x110], edx
00473e31  31d2                     xor edx, edx
00473e33  89c8                     mov eax, ecx
00473e35  8a542404                 mov dl, byte ptr [esp + 4]
00473e39  e8f81bfdff               call 0x445a36
00473e3e  31c0                     xor eax, eax
00473e40  6689f8                   mov ax, di
00473e43  83f801                   cmp eax, 1
00473e46  7d8e                     jge 0x473dd6
00473e48  8a442408                 mov al, byte ptr [esp + 8]
00473e4c  8a1d41805000             mov bl, byte ptr [0x508041]
00473e52  47                       inc edi
00473e53  38d8                     cmp al, bl
00473e55  0f857bffffff             jne 0x473dd6
00473e5b  ba17000000               mov edx, 0x17
00473e60  89c8                     mov eax, ecx
00473e62  31db                     xor ebx, ebx
00473e64  e8f5cefcff               call 0x440d5e
00473e69  e968ffffff               jmp 0x473dd6
