; IllumineCase; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476968  53                       push ebx
00476969  51                       push ecx
0047696a  56                       push esi
0047696b  57                       push edi
0047696c  83ec04                   sub esp, 4
0047696f  89c6                     mov esi, eax
00476971  88d1                     mov cl, dl
00476973  31db                     xor ebx, ebx
00476975  6689c3                   mov bx, ax
00476978  bf00010000               mov edi, 0x100
0047697d  89da                     mov edx, ebx
0047697f  89d8                     mov eax, ebx
00476981  c1fa1f                   sar edx, 0x1f
00476984  f7ff                     idiv edi
00476986  891424                   mov dword ptr [esp], edx
00476989  89da                     mov edx, ebx
0047698b  89d8                     mov eax, ebx
0047698d  c1fa1f                   sar edx, 0x1f
00476990  f7ff                     idiv edi
00476992  89c7                     mov edi, eax
00476994  31c0                     xor eax, eax
00476996  88c8                     mov al, cl
00476998  c1e002                   shl eax, 2
0047699b  8b90987d5000             mov edx, dword ptr [eax + 0x507d98]
004769a1  8a141a                   mov dl, byte ptr [edx + ebx]
004769a4  81e2ff000000             and edx, 0xff
004769aa  0f85f2000000             jne 0x476aa2
004769b0  668b1424                 mov dx, word ptr [esp]
004769b4  85d2                     test edx, edx
004769b6  740d                     je 0x4769c5
004769b8  8b80887d5000             mov eax, dword ptr [eax + 0x507d88]
004769be  806403fffd               and byte ptr [ebx + eax - 1], 0xfd
004769c3  eb0a                     jmp 0x4769cf
004769c5  8b80887d5000             mov eax, dword ptr [eax + 0x507d88]
004769cb  802403f7                 and byte ptr [ebx + eax], 0xf7
004769cf  31c0                     xor eax, eax
004769d1  6689f8                   mov ax, di
004769d4  85c0                     test eax, eax
004769d6  741a                     je 0x4769f2
004769d8  31c0                     xor eax, eax
004769da  31d2                     xor edx, edx
004769dc  88c8                     mov al, cl
004769de  6689f2                   mov dx, si
004769e1  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
004769e8  80a40200fffffffe         and byte ptr [edx + eax - 0x100], 0xfe
004769f0  eb12                     jmp 0x476a04
004769f2  31d2                     xor edx, edx
004769f4  88c8                     mov al, cl
004769f6  6689f2                   mov dx, si
004769f9  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476a00  802402fb                 and byte ptr [edx + eax], 0xfb
00476a04  31d2                     xor edx, edx
00476a06  31c0                     xor eax, eax
00476a08  668b1568714900           mov dx, word ptr [0x497168]
00476a0f  668b0424                 mov ax, word ptr [esp]
00476a13  4a                       dec edx
00476a14  39d0                     cmp eax, edx
00476a16  7417                     je 0x476a2f
00476a18  31c0                     xor eax, eax
00476a1a  31d2                     xor edx, edx
00476a1c  88c8                     mov al, cl
00476a1e  6689f2                   mov dx, si
00476a21  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476a28  80640201f7               and byte ptr [edx + eax + 1], 0xf7
00476a2d  eb14                     jmp 0x476a43
00476a2f  31d0                     xor eax, edx
00476a31  31d2                     xor edx, edx
00476a33  88c8                     mov al, cl
00476a35  6689f2                   mov dx, si
00476a38  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476a3f  802402fd                 and byte ptr [edx + eax], 0xfd
00476a43  31c0                     xor eax, eax
00476a45  31d2                     xor edx, edx
00476a47  66a16a714900             mov ax, word ptr [0x49716a]
00476a4d  6689fa                   mov dx, di
00476a50  48                       dec eax
00476a51  39c2                     cmp edx, eax
00476a53  741a                     je 0x476a6f
00476a55  31c0                     xor eax, eax
00476a57  31d2                     xor edx, edx
00476a59  88c8                     mov al, cl
00476a5b  6689f2                   mov dx, si
00476a5e  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476a65  80a40200010000fb         and byte ptr [edx + eax + 0x100], 0xfb
00476a6d  eb14                     jmp 0x476a83
00476a6f  31c0                     xor eax, eax
00476a71  31d2                     xor edx, edx
00476a73  88c8                     mov al, cl
00476a75  6689f2                   mov dx, si
00476a78  8b0485887d5000           mov eax, dword ptr [eax*4 + 0x507d88]
00476a7f  802402fe                 and byte ptr [edx + eax], 0xfe
00476a83  31db                     xor ebx, ebx
00476a85  0fb6f9                   movzx edi, cl
00476a88  6689f3                   mov bx, si
00476a8b  8b04bd887d5000           mov eax, dword ptr [edi*4 + 0x507d88]
00476a92  802403ef                 and byte ptr [ebx + eax], 0xef
00476a96  ba02000000               mov edx, 2
00476a9b  89f8                     mov eax, edi
00476a9d  e8e638ffff               call 0x46a388
00476aa2  31c0                     xor eax, eax
00476aa4  88c8                     mov al, cl
00476aa6  3dc8000000               cmp eax, 0xc8
00476aab  7427                     je 0x476ad4
00476aad  31ff                     xor edi, edi
00476aaf  8b1c85987d5000           mov ebx, dword ptr [eax*4 + 0x507d98]
00476ab6  6689f7                   mov di, si
00476ab9  89c2                     mov edx, eax
00476abb  01fb                     add ebx, edi
00476abd  31c2                     xor edx, eax
00476abf  8a13                     mov dl, byte ptr [ebx]
00476ac1  81faff000000             cmp edx, 0xff
00476ac7  740b                     je 0x476ad4
00476ac9  83f804                   cmp eax, 4
00476acc  7406                     je 0x476ad4
00476ace  88d6                     mov dh, dl
00476ad0  fec6                     inc dh
00476ad2  8833                     mov byte ptr [ebx], dh
00476ad4  83c404                   add esp, 4
00476ad7  5f                       pop edi
00476ad8  5e                       pop esi
00476ad9  59                       pop ecx
00476ada  5b                       pop ebx
00476adb  c3                       ret
