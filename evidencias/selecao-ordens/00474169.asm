; EnginSelectionnable; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00474169  53                       push ebx
0047416a  51                       push ecx
0047416b  52                       push edx
0047416c  89c2                     mov edx, eax
0047416e  31db                     xor ebx, ebx
00474170  6689c3                   mov bx, ax
00474173  89d8                     mov eax, ebx
00474175  c1e004                   shl eax, 4
00474178  01d8                     add eax, ebx
0047417a  c1e002                   shl eax, 2
0047417d  01d8                     add eax, ebx
0047417f  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00474185  c1e002                   shl eax, 2
00474188  01d8                     add eax, ebx
0047418a  31db                     xor ebx, ebx
0047418c  8a5802                   mov bl, byte ptr [eax + 2]
0047418f  83fb0e                   cmp ebx, 0xe
00474192  742d                     je 0x4741c1
00474194  31c9                     xor ecx, ecx
00474196  8a4801                   mov cl, byte ptr [eax + 1]
00474199  83f910                   cmp ecx, 0x10
0047419c  7515                     jne 0x4741b3
0047419e  83fb0d                   cmp ebx, 0xd
004741a1  7510                     jne 0x4741b3
004741a3  8a80ab000000             mov al, byte ptr [eax + 0xab]
004741a9  25ff000000               and eax, 0xff
004741ae  83f832                   cmp eax, 0x32
004741b1  750e                     jne 0x4741c1
004741b3  31c0                     xor eax, eax
004741b5  6689d0                   mov ax, dx
004741b8  e80224fdff               call 0x4465bf
004741bd  84c0                     test al, al
004741bf  7506                     jne 0x4741c7
004741c1  30c0                     xor al, al
004741c3  5a                       pop edx
004741c4  59                       pop ecx
004741c5  5b                       pop ebx
004741c6  c3                       ret
004741c7  b001                     mov al, 1
004741c9  5a                       pop edx
004741ca  59                       pop ecx
004741cb  5b                       pop ebx
004741cc  c3                       ret
