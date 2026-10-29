; RetireEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00457058  53                       push ebx
00457059  51                       push ecx
0045705a  52                       push edx
0045705b  56                       push esi
0045705c  31db                     xor ebx, ebx
0045705e  6689c3                   mov bx, ax
00457061  89d9                     mov ecx, ebx
00457063  c1e104                   shl ecx, 4
00457066  01d9                     add ecx, ebx
00457068  c1e102                   shl ecx, 2
0045706b  01d9                     add ecx, ebx
0045706d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00457072  c1e102                   shl ecx, 2
00457075  01c1                     add ecx, eax
00457077  31d2                     xor edx, edx
00457079  89d8                     mov eax, ebx
0045707b  668b7108                 mov si, word ptr [ecx + 8]
0045707f  e8c4b50100               call 0x472648
00457084  6689f2                   mov dx, si
00457087  89d8                     mov eax, ebx
00457089  e81ebefeff               call 0x442eac
0045708e  668b4108                 mov ax, word ptr [ecx + 8]
00457092  663b417c                 cmp ax, word ptr [ecx + 0x7c]
00457096  740d                     je 0x4570a5
00457098  31d2                     xor edx, edx
0045709a  89d8                     mov eax, ebx
0045709c  668b517c                 mov dx, word ptr [ecx + 0x7c]
004570a0  e807befeff               call 0x442eac
004570a5  ba05000000               mov edx, 5
004570aa  31db                     xor ebx, ebx
004570ac  31c0                     xor eax, eax
004570ae  6689f3                   mov bx, si
004570b1  8a01                     mov al, byte ptr [ecx]
004570b3  c6417200                 mov byte ptr [ecx + 0x72], 0
004570b7  e8cc320100               call 0x46a388
004570bc  31db                     xor ebx, ebx
004570be  8a19                     mov bl, byte ptr [ecx]
004570c0  81fbc8000000             cmp ebx, 0xc8
004570c6  7427                     je 0x4570ef
004570c8  83fb04                   cmp ebx, 4
004570cb  7422                     je 0x4570ef
004570cd  30e4                     xor ah, ah
004570cf  30f6                     xor dh, dh
004570d1  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
004570d7  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
004570dd  01d0                     add eax, edx
004570df  31d2                     xor edx, edx
004570e1  6689c2                   mov dx, ax
004570e4  31c0                     xor eax, eax
004570e6  668b4108                 mov ax, word ptr [ecx + 8]
004570ea  e893fd0100               call 0x476e82
004570ef  5e                       pop esi
004570f0  5a                       pop edx
004570f1  59                       pop ecx
004570f2  5b                       pop ebx
004570f3  c3                       ret
