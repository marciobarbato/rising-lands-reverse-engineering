; DecouvreCase; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047670a  53                       push ebx
0047670b  51                       push ecx
0047670c  56                       push esi
0047670d  57                       push edi
0047670e  89c6                     mov esi, eax
00476710  88d1                     mov cl, dl
00476712  31db                     xor ebx, ebx
00476714  6689c3                   mov bx, ax
00476717  bf00010000               mov edi, 0x100
0047671c  89da                     mov edx, ebx
0047671e  89d8                     mov eax, ebx
00476720  c1fa1f                   sar edx, 0x1f
00476723  f7ff                     idiv edi
00476725  89d7                     mov edi, edx
00476727  89da                     mov edx, ebx
00476729  89d8                     mov eax, ebx
0047672b  c1fa1f                   sar edx, 0x1f
0047672e  c1e208                   shl edx, 8
00476731  1bc2                     sbb eax, edx
00476733  c1f808                   sar eax, 8
00476736  89c2                     mov edx, eax
00476738  31c0                     xor eax, eax
0047673a  6689f8                   mov ax, di
0047673d  85c0                     test eax, eax
0047673f  7412                     je 0x476753
00476741  31c0                     xor eax, eax
00476743  88c8                     mov al, cl
00476745  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
0047674c  806403fffd               and byte ptr [ebx + eax - 1], 0xfd
00476751  eb0d                     jmp 0x476760
00476753  88c8                     mov al, cl
00476755  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
0047675c  802403f7                 and byte ptr [ebx + eax], 0xf7
00476760  31c0                     xor eax, eax
00476762  6689d0                   mov ax, dx
00476765  85c0                     test eax, eax
00476767  741a                     je 0x476783
00476769  31c0                     xor eax, eax
0047676b  31db                     xor ebx, ebx
0047676d  88c8                     mov al, cl
0047676f  6689f3                   mov bx, si
00476772  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
00476779  80a40300fffffffe         and byte ptr [ebx + eax - 0x100], 0xfe
00476781  eb12                     jmp 0x476795
00476783  31db                     xor ebx, ebx
00476785  88c8                     mov al, cl
00476787  6689f3                   mov bx, si
0047678a  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
00476791  802403fb                 and byte ptr [ebx + eax], 0xfb
00476795  31c0                     xor eax, eax
00476797  31db                     xor ebx, ebx
00476799  66a168714900             mov ax, word ptr [0x497168]
0047679f  6689fb                   mov bx, di
004767a2  48                       dec eax
004767a3  39c3                     cmp ebx, eax
004767a5  7417                     je 0x4767be
004767a7  31c0                     xor eax, eax
004767a9  31db                     xor ebx, ebx
004767ab  88c8                     mov al, cl
004767ad  6689f3                   mov bx, si
004767b0  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
004767b7  80640301f7               and byte ptr [ebx + eax + 1], 0xf7
004767bc  eb14                     jmp 0x4767d2
004767be  31c0                     xor eax, eax
004767c0  31db                     xor ebx, ebx
004767c2  88c8                     mov al, cl
004767c4  6689f3                   mov bx, si
004767c7  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
004767ce  802403fd                 and byte ptr [ebx + eax], 0xfd
004767d2  31c0                     xor eax, eax
004767d4  66a16a714900             mov ax, word ptr [0x49716a]
004767da  81e2ffff0000             and edx, 0xffff
004767e0  48                       dec eax
004767e1  39c2                     cmp edx, eax
004767e3  741a                     je 0x4767ff
004767e5  31c0                     xor eax, eax
004767e7  31db                     xor ebx, ebx
004767e9  88c8                     mov al, cl
004767eb  6689f3                   mov bx, si
004767ee  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
004767f5  80a40300010000fb         and byte ptr [ebx + eax + 0x100], 0xfb
004767fd  eb14                     jmp 0x476813
004767ff  31c0                     xor eax, eax
00476801  31db                     xor ebx, ebx
00476803  88c8                     mov al, cl
00476805  6689f3                   mov bx, si
00476808  8b0485787d5000           mov eax, dword ptr [eax*4 + 0x507d78]
0047680f  802403fe                 and byte ptr [ebx + eax], 0xfe
00476813  31c0                     xor eax, eax
00476815  31db                     xor ebx, ebx
00476817  88c8                     mov al, cl
00476819  6689f3                   mov bx, si
0047681c  8b1485787d5000           mov edx, dword ptr [eax*4 + 0x507d78]
00476823  8a141a                   mov dl, byte ptr [edx + ebx]
00476826  81e2ff000000             and edx, 0xff
0047682c  740a                     je 0x476838
0047682e  ba01000000               mov edx, 1
00476833  e8503bffff               call 0x46a388
00476838  31c0                     xor eax, eax
0047683a  31d2                     xor edx, edx
0047683c  88c8                     mov al, cl
0047683e  6689f2                   mov dx, si
00476841  8b1c85787d5000           mov ebx, dword ptr [eax*4 + 0x507d78]
00476848  80241aef                 and byte ptr [edx + ebx], 0xef
0047684c  5f                       pop edi
0047684d  5e                       pop esi
0047684e  59                       pop ecx
0047684f  5b                       pop ebx
00476850  c3                       ret
