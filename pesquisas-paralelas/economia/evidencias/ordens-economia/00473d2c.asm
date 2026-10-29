; SetRamasseEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00473d2c  53                       push ebx
00473d2d  51                       push ecx
00473d2e  56                       push esi
00473d2f  57                       push edi
00473d30  83ec08                   sub esp, 8
00473d33  88442404                 mov byte ptr [esp + 4], al
00473d37  891424                   mov dword ptr [esp], edx
00473d3a  31ff                     xor edi, edi
00473d3c  31f6                     xor esi, esi
00473d3e  eb01                     jmp 0x473d41
00473d40  46                       inc esi
00473d41  31c9                     xor ecx, ecx
00473d43  8a4c2404                 mov cl, byte ptr [esp + 4]
00473d47  c1e109                   shl ecx, 9
00473d4a  663bb128875000           cmp si, word ptr [ecx + 0x508728]
00473d51  0f83acebffff             jae 0x472903
00473d57  31c0                     xor eax, eax
00473d59  6689f0                   mov ax, si
00473d5c  668b84412a875000         mov ax, word ptr [ecx + eax*2 + 0x50872a]
00473d64  31c9                     xor ecx, ecx
00473d66  6689c1                   mov cx, ax
00473d69  89c8                     mov eax, ecx
00473d6b  e83d00fdff               call 0x443dad
00473d70  84c0                     test al, al
00473d72  74cc                     je 0x473d40
00473d74  69c114010000             imul eax, ecx, 0x114
00473d7a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00473d80  8a0402                   mov al, byte ptr [edx + eax]
00473d83  3a442404                 cmp al, byte ptr [esp + 4]
00473d87  75b7                     jne 0x473d40
00473d89  31d2                     xor edx, edx
00473d8b  89c8                     mov eax, ecx
00473d8d  668b1424                 mov dx, word ptr [esp]
00473d91  e8b11bfdff               call 0x445947
00473d96  31c0                     xor eax, eax
00473d98  6689f8                   mov ax, di
00473d9b  83f801                   cmp eax, 1
00473d9e  7da0                     jge 0x473d40
00473da0  8a442404                 mov al, byte ptr [esp + 4]
00473da4  8a1541805000             mov dl, byte ptr [0x508041]
00473daa  47                       inc edi
00473dab  38d0                     cmp al, dl
00473dad  7591                     jne 0x473d40
00473daf  ba0f000000               mov edx, 0xf
00473db4  89c8                     mov eax, ecx
00473db6  31db                     xor ebx, ebx
00473db8  e8a1cffcff               call 0x440d5e
00473dbd  eb81                     jmp 0x473d40
