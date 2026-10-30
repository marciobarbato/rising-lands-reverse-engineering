; EnginNextEtape state 13 body; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004558e4  31c0                     xor eax, eax
004558e6  668b86c0000000           mov ax, word ptr [esi + 0xc0]
004558ed  3dffff0000               cmp eax, 0xffff
004558f2  0f84ba000000             je 0x4559b2
004558f8  31c0                     xor eax, eax
004558fa  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455901  e8054efcff               call 0x41a70b
00455906  84c0                     test al, al
00455908  0f8589f4ffff             jne 0x454d97
0045590e  31c0                     xor eax, eax
00455910  8a4601                   mov al, byte ptr [esi + 1]
00455913  83f80a                   cmp eax, 0xa
00455916  754d                     jne 0x455965
00455918  31c0                     xor eax, eax
0045591a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455921  e86647fcff               call 0x41a08c
00455926  25ff000000               and eax, 0xff
0045592b  3dc8000000               cmp eax, 0xc8
00455930  0f8461f4ffff             je 0x454d97
00455936  31c0                     xor eax, eax
00455938  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045593f  e84847fcff               call 0x41a08c
00455944  3a06                     cmp al, byte ptr [esi]
00455946  755b                     jne 0x4559a3
00455948  31c0                     xor eax, eax
0045594a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455951  e89e4bfcff               call 0x41a4f4
00455956  25ff000000               and eax, 0xff
0045595b  83f810                   cmp eax, 0x10
0045595e  7543                     jne 0x4559a3
00455960  e932f4ffff               jmp 0x454d97
00455965  31c0                     xor eax, eax
00455967  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0045596e  e81947fcff               call 0x41a08c
00455973  3a06                     cmp al, byte ptr [esi]
00455975  742c                     je 0x4559a3
00455977  31c0                     xor eax, eax
00455979  668b86c0000000           mov ax, word ptr [esi + 0xc0]
00455980  e80747fcff               call 0x41a08c
00455985  25ff000000               and eax, 0xff
0045598a  3dc8000000               cmp eax, 0xc8
0045598f  0f8502f4ffff             jne 0x454d97
00455995  31c0                     xor eax, eax
00455997  8a4601                   mov al, byte ptr [esi + 1]
0045599a  83f809                   cmp eax, 9
0045599d  0f85f4f3ffff             jne 0x454d97
004559a3  31c0                     xor eax, eax
004559a5  6689f8                   mov ax, di
004559a8  e8693dffff               call 0x449716
004559ad  e91bf3ffff               jmp 0x454ccd
004559b2  31c0                     xor eax, eax
004559b4  668b86b8000000           mov ax, word ptr [esi + 0xb8]
004559bb  3dffff0000               cmp eax, 0xffff
004559c0  0f8407f3ffff             je 0x454ccd
004559c6  31d2                     xor edx, edx
004559c8  6689c2                   mov dx, ax
004559cb  89c3                     mov ebx, eax
004559cd  89d0                     mov eax, edx
004559cf  c1e004                   shl eax, 4
004559d2  01d0                     add eax, edx
004559d4  c1e002                   shl eax, 2
004559d7  01d0                     add eax, edx
004559d9  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004559df  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
004559e3  25ff000000               and eax, 0xff
004559e8  7429                     je 0x455a13
004559ea  31d2                     xor edx, edx
004559ec  6689da                   mov dx, bx
004559ef  89d0                     mov eax, edx
004559f1  c1e004                   shl eax, 4
004559f4  01d0                     add eax, edx
004559f6  c1e002                   shl eax, 2
004559f9  01d0                     add eax, edx
004559fb  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455a01  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00455a05  25ff000000               and eax, 0xff
00455a0a  83f804                   cmp eax, 4
00455a0d  7404                     je 0x455a13
00455a0f  b001                     mov al, 1
00455a11  eb02                     jmp 0x455a15
00455a13  30c0                     xor al, al
00455a15  84c0                     test al, al
00455a17  0f8475faffff             je 0x455492
00455a1d  668b86b8000000           mov ax, word ptr [esi + 0xb8]
00455a24  31d2                     xor edx, edx
00455a26  6689c2                   mov dx, ax
00455a29  89d0                     mov eax, edx
00455a2b  c1e004                   shl eax, 4
00455a2e  01d0                     add eax, edx
00455a30  c1e002                   shl eax, 2
00455a33  01d0                     add eax, edx
00455a35  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00455a3b  8a0482                   mov al, byte ptr [edx + eax*4]
00455a3e  3a06                     cmp al, byte ptr [esi]
00455a40  7410                     je 0x455a52
00455a42  25ff000000               and eax, 0xff
00455a47  3dc8000000               cmp eax, 0xc8
00455a4c  0f8540faffff             jne 0x455492
00455a52  31c0                     xor eax, eax
00455a54  6689f8                   mov ax, di
00455a57  e89148ffff               call 0x44a2ed
00455a5c  e96cf2ffff               jmp 0x454ccd
