; ProcessInputGame tags 6/7/8/0x10/0x13/0x21 0x45efe2..0x45f22f; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045efe2  31c0                     xor eax, eax
0045efe4  8a0424                   mov al, byte ptr [esp]
0045efe7  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045efee  31d2                     xor edx, edx
0045eff0  668b5002                 mov dx, word ptr [eax + 2]
0045eff4  31c0                     xor eax, eax
0045eff6  8a0424                   mov al, byte ptr [esp]
0045eff9  e826430100               call 0x473324
0045effe  31c0                     xor eax, eax
0045f000  8a0424                   mov al, byte ptr [esp]
0045f003  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f00a  31c9                     xor ecx, ecx
0045f00c  8a4808                   mov cl, byte ptr [eax + 8]
0045f00f  31c0                     xor eax, eax
0045f011  8a0424                   mov al, byte ptr [esp]
0045f014  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f01b  31db                     xor ebx, ebx
0045f01d  668b5806                 mov bx, word ptr [eax + 6]
0045f021  31c0                     xor eax, eax
0045f023  8a0424                   mov al, byte ptr [esp]
0045f026  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f02d  31d2                     xor edx, edx
0045f02f  8a5004                   mov dl, byte ptr [eax + 4]
0045f032  31c0                     xor eax, eax
0045f034  8a0424                   mov al, byte ptr [esp]
0045f037  e8f0400100               call 0x47312c
0045f03c  e99d020000               jmp 0x45f2de
0045f041  31c0                     xor eax, eax
0045f043  8a0424                   mov al, byte ptr [esp]
0045f046  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f04d  31d2                     xor edx, edx
0045f04f  668b5002                 mov dx, word ptr [eax + 2]
0045f053  31c0                     xor eax, eax
0045f055  8a0424                   mov al, byte ptr [esp]
0045f058  e833420100               call 0x473290
0045f05d  eb9f                     jmp 0x45effe
0045f05f  31c0                     xor eax, eax
0045f061  8a0424                   mov al, byte ptr [esp]
0045f064  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f06b  31d2                     xor edx, edx
0045f06d  668b5002                 mov dx, word ptr [eax + 2]
0045f071  31c0                     xor eax, eax
0045f073  8a0424                   mov al, byte ptr [esp]
0045f076  e897410100               call 0x473212
0045f07b  eb81                     jmp 0x45effe
0045f07d  31d2                     xor edx, edx
0045f07f  668b5002                 mov dx, word ptr [eax + 2]
0045f083  89f0                     mov eax, esi
0045f085  e80a410100               call 0x473194
0045f08a  8b8358244e00             mov eax, dword ptr [ebx + 0x4e2458]
0045f090  31c9                     xor ecx, ecx
0045f092  31d2                     xor edx, edx
0045f094  8a4808                   mov cl, byte ptr [eax + 8]
0045f097  31db                     xor ebx, ebx
0045f099  8a5004                   mov dl, byte ptr [eax + 4]
0045f09c  668b5806                 mov bx, word ptr [eax + 6]
0045f0a0  89f0                     mov eax, esi
0045f0a2  eb93                     jmp 0x45f037
0045f0a4  31d2                     xor edx, edx
0045f0a6  31c0                     xor eax, eax
0045f0a8  8a1424                   mov dl, byte ptr [esp]
0045f0ab  88d0                     mov al, dl
0045f0ad  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f0b4  668b4002                 mov ax, word ptr [eax + 2]
0045f0b8  25ffff0000               and eax, 0xffff
0045f0bd  e81dfdfbff               call 0x41eddf
0045f0c2  e917020000               jmp 0x45f2de
0045f0c7  31c0                     xor eax, eax
0045f0c9  8a0424                   mov al, byte ptr [esp]
0045f0cc  e8e5b3fbff               call 0x41a4b6
0045f0d1  25ffff0000               and eax, 0xffff
0045f0d6  3dffff0000               cmp eax, 0xffff
0045f0db  7532                     jne 0x45f10f
0045f0dd  31c0                     xor eax, eax
0045f0df  8a0424                   mov al, byte ptr [esp]
0045f0e2  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f0e9  31db                     xor ebx, ebx
0045f0eb  668b5804                 mov bx, word ptr [eax + 4]
0045f0ef  31c0                     xor eax, eax
0045f0f1  8a0424                   mov al, byte ptr [esp]
0045f0f4  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f0fb  31d2                     xor edx, edx
0045f0fd  8a5002                   mov dl, byte ptr [eax + 2]
0045f100  31c0                     xor eax, eax
0045f102  8a0424                   mov al, byte ptr [esp]
0045f105  e8b54c0100               call 0x473dbf
0045f10a  e9cf010000               jmp 0x45f2de
0045f10f  31c0                     xor eax, eax
0045f111  8a0424                   mov al, byte ptr [esp]
0045f114  8b1c8558244e00           mov ebx, dword ptr [eax*4 + 0x4e2458]
0045f11b  668b5b04                 mov bx, word ptr [ebx + 4]
0045f11f  31c0                     xor eax, eax
0045f121  8a0424                   mov al, byte ptr [esp]
0045f124  8b148558244e00           mov edx, dword ptr [eax*4 + 0x4e2458]
0045f12b  81e3ffff0000             and ebx, 0xffff
0045f131  8a5202                   mov dl, byte ptr [edx + 2]
0045f134  31c0                     xor eax, eax
0045f136  81e2ff000000             and edx, 0xff
0045f13c  8a0424                   mov al, byte ptr [esp]
0045f13f  e88851fcff               call 0x4242cc
0045f144  e995010000               jmp 0x45f2de
0045f149  89f0                     mov eax, esi
0045f14b  e810b7fbff               call 0x41a860
0045f150  e989010000               jmp 0x45f2de
0045f155  31d2                     xor edx, edx
0045f157  668b5002                 mov dx, word ptr [eax + 2]
0045f15b  89f0                     mov eax, esi
0045f15d  e8054f0100               call 0x474067
0045f162  e977010000               jmp 0x45f2de
0045f167  31d2                     xor edx, edx
0045f169  668b5002                 mov dx, word ptr [eax + 2]
0045f16d  83fa01                   cmp edx, 1
0045f170  7512                     jne 0x45f184
0045f172  31d2                     xor edx, edx
0045f174  668b5004                 mov dx, word ptr [eax + 4]
0045f178  89f0                     mov eax, esi
0045f17a  e8434f0100               call 0x4740c2
0045f17f  e95a010000               jmp 0x45f2de
0045f184  83fa03                   cmp edx, 3
0045f187  0f8551010000             jne 0x45f2de
0045f18d  31d2                     xor edx, edx
0045f18f  668b5004                 mov dx, word ptr [eax + 4]
0045f193  89f0                     mov eax, esi
0045f195  e8b14d0100               call 0x473f4b
0045f19a  e93f010000               jmp 0x45f2de
0045f19f  8a4002                   mov al, byte ptr [eax + 2]
0045f1a2  25ff000000               and eax, 0xff
0045f1a7  89f2                     mov edx, esi
0045f1a9  e83492fcff               call 0x4283e2
0045f1ae  e92b010000               jmp 0x45f2de
0045f1b3  31c0                     xor eax, eax
0045f1b5  8a0424                   mov al, byte ptr [esp]
0045f1b8  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f1bf  8a4008                   mov al, byte ptr [eax + 8]
0045f1c2  30e4                     xor ah, ah
0045f1c4  31c9                     xor ecx, ecx
0045f1c6  6689c1                   mov cx, ax
0045f1c9  31c0                     xor eax, eax
0045f1cb  8a0424                   mov al, byte ptr [esp]
0045f1ce  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f1d5  8a4006                   mov al, byte ptr [eax + 6]
0045f1d8  30e4                     xor ah, ah
0045f1da  31db                     xor ebx, ebx
0045f1dc  6689c3                   mov bx, ax
0045f1df  31c0                     xor eax, eax
0045f1e1  8a0424                   mov al, byte ptr [esp]
0045f1e4  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f1eb  31d2                     xor edx, edx
0045f1ed  8a5004                   mov dl, byte ptr [eax + 4]
0045f1f0  31c0                     xor eax, eax
0045f1f2  8a0424                   mov al, byte ptr [esp]
0045f1f5  8b048558244e00           mov eax, dword ptr [eax*4 + 0x4e2458]
0045f1fc  668b4002                 mov ax, word ptr [eax + 2]
0045f200  25ffff0000               and eax, 0xffff
0045f205  e82953feff               call 0x444533
0045f20a  e9cf000000               jmp 0x45f2de
0045f20f  31d2                     xor edx, edx
0045f211  668b5002                 mov dx, word ptr [eax + 2]
0045f215  89f0                     mov eax, esi
0045f217  e8104b0100               call 0x473d2c
0045f21c  e9bd000000               jmp 0x45f2de
0045f221  668b4002                 mov ax, word ptr [eax + 2]
0045f225  25ffff0000               and eax, 0xffff
0045f22a  e8b1ebfbff               call 0x41dde0
