; EnginAsk; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00440d5e  51                       push ecx
00440d5f  56                       push esi
00440d60  57                       push edi
00440d61  89d7                     mov edi, edx
00440d63  88d9                     mov cl, bl
00440d65  31f6                     xor esi, esi
00440d67  6689c6                   mov si, ax
00440d6a  89f0                     mov eax, esi
00440d6c  c1e004                   shl eax, 4
00440d6f  01f0                     add eax, esi
00440d71  c1e002                   shl eax, 2
00440d74  01f0                     add eax, esi
00440d76  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00440d7c  c1e002                   shl eax, 2
00440d7f  31d2                     xor edx, edx
00440d81  01c3                     add ebx, eax
00440d83  31c0                     xor eax, eax
00440d85  8a1541805000             mov dl, byte ptr [0x508041]
00440d8b  668b4308                 mov ax, word ptr [ebx + 8]
00440d8f  e85c590300               call 0x4766f0
00440d94  84c0                     test al, al
00440d96  7454                     je 0x440dec
00440d98  31d2                     xor edx, edx
00440d9a  89f0                     mov eax, esi
00440d9c  6689fa                   mov dx, di
00440d9f  e8b9feffff               call 0x440c5d
00440da4  83fa10                   cmp edx, 0x10
00440da7  7505                     jne 0x440dae
00440da9  b800010000               mov eax, 0x100
00440dae  8b9304010000             mov edx, dword ptr [ebx + 0x104]
00440db4  888bf9000000             mov byte ptr [ebx + 0xf9], cl
00440dba  83faff                   cmp edx, -1
00440dbd  752d                     jne 0x440dec
00440dbf  50                       push eax
00440dc0  31d2                     xor edx, edx
00440dc2  8d8304010000             lea eax, [ebx + 0x104]
00440dc8  8a5301                   mov dl, byte ptr [ebx + 1]
00440dcb  89d3                     mov ebx, edx
00440dcd  31d2                     xor edx, edx
00440dcf  6689fa                   mov dx, di
00440dd2  c1e310                   shl ebx, 0x10
00440dd5  c1e208                   shl edx, 8
00440dd8  81e1ff000000             and ecx, 0xff
00440dde  09da                     or edx, ebx
00440de0  89c3                     mov ebx, eax
00440de2  b850000000               mov eax, 0x50
00440de7  e88d9c0400               call 0x48aa79
00440dec  5f                       pop edi
00440ded  5e                       pop esi
00440dee  59                       pop ecx
00440def  c3                       ret
