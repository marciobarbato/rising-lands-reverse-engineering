; MurRetire; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043e8b7  53                       push ebx
0043e8b8  51                       push ecx
0043e8b9  52                       push edx
0043e8ba  56                       push esi
0043e8bb  57                       push edi
0043e8bc  55                       push ebp
0043e8bd  83ec04                   sub esp, 4
0043e8c0  89c6                     mov esi, eax
0043e8c2  31c0                     xor eax, eax
0043e8c4  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e8ca  6689f0                   mov ax, si
0043e8cd  8a0402                   mov al, byte ptr [edx + eax]
0043e8d0  25ff000000               and eax, 0xff
0043e8d5  0f847e020000             je 0x43eb59
0043e8db  30db                     xor bl, bl
0043e8dd  89f7                     mov edi, esi
0043e8df  b701                     mov bh, 1
0043e8e1  81e7ff000000             and edi, 0xff
0043e8e7  eb47                     jmp 0x43e930
0043e8e9  31c9                     xor ecx, ecx
0043e8eb  668b0d68714900           mov cx, word ptr [0x497168]
0043e8f2  49                       dec ecx
0043e8f3  39ca                     cmp edx, ecx
0043e8f5  7f67                     jg 0x43e95e
0043e8f7  85c0                     test eax, eax
0043e8f9  7c63                     jl 0x43e95e
0043e8fb  31c9                     xor ecx, ecx
0043e8fd  668b0d6a714900           mov cx, word ptr [0x49716a]
0043e904  49                       dec ecx
0043e905  39c8                     cmp eax, ecx
0043e907  7f55                     jg 0x43e95e
0043e909  c1e008                   shl eax, 8
0043e90c  01c2                     add edx, eax
0043e90e  31c0                     xor eax, eax
0043e910  6689d0                   mov ax, dx
0043e913  3dffff0000               cmp eax, 0xffff
0043e918  744b                     je 0x43e965
0043e91a  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e920  01c2                     add edx, eax
0043e922  31c0                     xor eax, eax
0043e924  88d8                     mov al, bl
0043e926  8a12                     mov dl, byte ptr [edx]
0043e928  881404                   mov byte ptr [esp + eax], dl
0043e92b  80c704                   add bh, 4
0043e92e  fec3                     inc bl
0043e930  31c0                     xor eax, eax
0043e932  88d8                     mov al, bl
0043e934  83f804                   cmp eax, 4
0043e937  7d34                     jge 0x43e96d
0043e939  31d2                     xor edx, edx
0043e93b  31c9                     xor ecx, ecx
0043e93d  31c0                     xor eax, eax
0043e93f  88f9                     mov cl, bh
0043e941  6689fa                   mov dx, di
0043e944  6689f0                   mov ax, si
0043e947  8b2ccd08634900           mov ebp, dword ptr [ecx*8 + 0x496308]
0043e94e  c1f808                   sar eax, 8
0043e951  01ea                     add edx, ebp
0043e953  0304cd0c634900           add eax, dword ptr [ecx*8 + 0x49630c]
0043e95a  85d2                     test edx, edx
0043e95c  7d8b                     jge 0x43e8e9
0043e95e  baffff0000               mov edx, 0xffff
0043e963  eba9                     jmp 0x43e90e
0043e965  31c0                     xor eax, eax
0043e967  88d8                     mov al, bl
0043e969  30d2                     xor dl, dl
0043e96b  ebbb                     jmp 0x43e928
0043e96d  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e973  89f7                     mov edi, esi
0043e975  31c0                     xor eax, eax
0043e977  30db                     xor bl, bl
0043e979  6689f0                   mov ax, si
0043e97c  b701                     mov bh, 1
0043e97e  81e7ff000000             and edi, 0xff
0043e984  c6040200                 mov byte ptr [edx + eax], 0
0043e988  e996000000               jmp 0x43ea23
0043e98d  31c9                     xor ecx, ecx
0043e98f  668b0d68714900           mov cx, word ptr [0x497168]
0043e996  49                       dec ecx
0043e997  39c8                     cmp eax, ecx
0043e999  0f8fb6000000             jg 0x43ea55
0043e99f  85d2                     test edx, edx
0043e9a1  0f8cae000000             jl 0x43ea55
0043e9a7  31c9                     xor ecx, ecx
0043e9a9  668b0d6a714900           mov cx, word ptr [0x49716a]
0043e9b0  49                       dec ecx
0043e9b1  39ca                     cmp edx, ecx
0043e9b3  0f8f9c000000             jg 0x43ea55
0043e9b9  c1e208                   shl edx, 8
0043e9bc  01d0                     add eax, edx
0043e9be  89c1                     mov ecx, eax
0043e9c0  25ffff0000               and eax, 0xffff
0043e9c5  3dffff0000               cmp eax, 0xffff
0043e9ca  7452                     je 0x43ea1e
0043e9cc  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e9d2  01d0                     add eax, edx
0043e9d4  31d2                     xor edx, edx
0043e9d6  8a10                     mov dl, byte ptr [eax]
0043e9d8  85d2                     test edx, edx
0043e9da  7442                     je 0x43ea1e
0043e9dc  31d2                     xor edx, edx
0043e9de  88da                     mov dl, bl
0043e9e0  8a00                     mov al, byte ptr [eax]
0043e9e2  3a0414                   cmp al, byte ptr [esp + edx]
0043e9e5  7537                     jne 0x43ea1e
0043e9e7  31c0                     xor eax, eax
0043e9e9  a070154e00               mov al, byte ptr [0x4e1570]
0043e9ee  85c0                     test eax, eax
0043e9f0  741a                     je 0x43ea0c
0043e9f2  8a9070154e00             mov dl, byte ptr [eax + 0x4e1570]
0043e9f8  31c0                     xor eax, eax
0043e9fa  88d0                     mov al, dl
0043e9fc  30f6                     xor dh, dh
0043e9fe  88b070164e00             mov byte ptr [eax + 0x4e1670], dh
0043ea04  fe0d70154e00             dec byte ptr [0x4e1570]
0043ea0a  eb02                     jmp 0x43ea0e
0043ea0c  30da                     xor dl, bl
0043ea0e  31c0                     xor eax, eax
0043ea10  81e2ff000000             and edx, 0xff
0043ea16  6689c8                   mov ax, cx
0043ea19  e846faffff               call 0x43e464
0043ea1e  80c704                   add bh, 4
0043ea21  fec3                     inc bl
0043ea23  31c0                     xor eax, eax
0043ea25  88d8                     mov al, bl
0043ea27  83f804                   cmp eax, 4
0043ea2a  7d33                     jge 0x43ea5f
0043ea2c  31c0                     xor eax, eax
0043ea2e  31c9                     xor ecx, ecx
0043ea30  31d2                     xor edx, edx
0043ea32  88f9                     mov cl, bh
0043ea34  6689f8                   mov ax, di
0043ea37  6689f2                   mov dx, si
0043ea3a  8b2ccd08634900           mov ebp, dword ptr [ecx*8 + 0x496308]
0043ea41  c1fa08                   sar edx, 8
0043ea44  01e8                     add eax, ebp
0043ea46  0314cd0c634900           add edx, dword ptr [ecx*8 + 0x49630c]
0043ea4d  85c0                     test eax, eax
0043ea4f  0f8d38ffffff             jge 0x43e98d
0043ea55  b8ffff0000               mov eax, 0xffff
0043ea5a  e95fffffff               jmp 0x43e9be
0043ea5f  31c0                     xor eax, eax
0043ea61  a070154e00               mov al, byte ptr [0x4e1570]
0043ea66  3dff000000               cmp eax, 0xff
0043ea6b  7d31                     jge 0x43ea9e
0043ea6d  31d2                     xor edx, edx
0043ea6f  8a1424                   mov dl, byte ptr [esp]
0043ea72  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043ea79  7523                     jne 0x43ea9e
0043ea7b  84d2                     test dl, dl
0043ea7d  741f                     je 0x43ea9e
0043ea7f  88c1                     mov cl, al
0043ea81  fec1                     inc cl
0043ea83  880d70154e00             mov byte ptr [0x4e1570], cl
0043ea89  31c9                     xor ecx, ecx
0043ea8b  8a0d70154e00             mov cl, byte ptr [0x4e1570]
0043ea91  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043ea97  c68270164e0001           mov byte ptr [edx + 0x4e1670], 1
0043ea9e  31c0                     xor eax, eax
0043eaa0  a070154e00               mov al, byte ptr [0x4e1570]
0043eaa5  3dff000000               cmp eax, 0xff
0043eaaa  7d33                     jge 0x43eadf
0043eaac  31d2                     xor edx, edx
0043eaae  8a542401                 mov dl, byte ptr [esp + 1]
0043eab2  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043eab9  7524                     jne 0x43eadf
0043eabb  84d2                     test dl, dl
0043eabd  7420                     je 0x43eadf
0043eabf  8a1d70154e00             mov bl, byte ptr [0x4e1570]
0043eac5  31c9                     xor ecx, ecx
0043eac7  fec3                     inc bl
0043eac9  88d9                     mov cl, bl
0043eacb  881d70154e00             mov byte ptr [0x4e1570], bl
0043ead1  b701                     mov bh, 1
0043ead3  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043ead9  88ba70164e00             mov byte ptr [edx + 0x4e1670], bh
0043eadf  31c0                     xor eax, eax
0043eae1  a070154e00               mov al, byte ptr [0x4e1570]
0043eae6  3dff000000               cmp eax, 0xff
0043eaeb  7d2c                     jge 0x43eb19
0043eaed  31d2                     xor edx, edx
0043eaef  8a542402                 mov dl, byte ptr [esp + 2]
0043eaf3  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043eafa  751d                     jne 0x43eb19
0043eafc  84d2                     test dl, dl
0043eafe  7419                     je 0x43eb19
0043eb00  fec0                     inc al
0043eb02  31c9                     xor ecx, ecx
0043eb04  88c1                     mov cl, al
0043eb06  a270154e00               mov byte ptr [0x4e1570], al
0043eb0b  b401                     mov ah, 1
0043eb0d  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043eb13  88a270164e00             mov byte ptr [edx + 0x4e1670], ah
0043eb19  31c0                     xor eax, eax
0043eb1b  a070154e00               mov al, byte ptr [0x4e1570]
0043eb20  3dff000000               cmp eax, 0xff
0043eb25  7d32                     jge 0x43eb59
0043eb27  31d2                     xor edx, edx
0043eb29  8a542403                 mov dl, byte ptr [esp + 3]
0043eb2d  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043eb34  7523                     jne 0x43eb59
0043eb36  84d2                     test dl, dl
0043eb38  741f                     je 0x43eb59
0043eb3a  88c1                     mov cl, al
0043eb3c  fec1                     inc cl
0043eb3e  880d70154e00             mov byte ptr [0x4e1570], cl
0043eb44  31c9                     xor ecx, ecx
0043eb46  8a0d70154e00             mov cl, byte ptr [0x4e1570]
0043eb4c  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043eb52  c68270164e0001           mov byte ptr [edx + 0x4e1670], 1
0043eb59  83c404                   add esp, 4
0043eb5c  e97906ffff               jmp 0x42f1da
0043eb61  0000                     add byte ptr [eax], al
; 1 trailing bytes are not code (alignment/data): 00
