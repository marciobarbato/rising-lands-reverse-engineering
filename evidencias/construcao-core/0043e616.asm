; MurAjoute; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043e616  53                       push ebx
0043e617  51                       push ecx
0043e618  52                       push edx
0043e619  56                       push esi
0043e61a  57                       push edi
0043e61b  55                       push ebp
0043e61c  83ec0c                   sub esp, 0xc
0043e61f  89c7                     mov edi, eax
0043e621  30db                     xor bl, bl
0043e623  89c6                     mov esi, eax
0043e625  b701                     mov bh, 1
0043e627  81e6ff000000             and esi, 0xff
0043e62d  eb5a                     jmp 0x43e689
0043e62f  31c9                     xor ecx, ecx
0043e631  668b0d68714900           mov cx, word ptr [0x497168]
0043e638  49                       dec ecx
0043e639  39c8                     cmp eax, ecx
0043e63b  0f8f7a000000             jg 0x43e6bb
0043e641  85d2                     test edx, edx
0043e643  0f8c72000000             jl 0x43e6bb
0043e649  31c9                     xor ecx, ecx
0043e64b  668b0d6a714900           mov cx, word ptr [0x49716a]
0043e652  49                       dec ecx
0043e653  39ca                     cmp edx, ecx
0043e655  7f64                     jg 0x43e6bb
0043e657  c1e208                   shl edx, 8
0043e65a  01d0                     add eax, edx
0043e65c  25ffff0000               and eax, 0xffff
0043e661  3dffff0000               cmp eax, 0xffff
0043e666  7413                     je 0x43e67b
0043e668  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e66e  01c2                     add edx, eax
0043e670  31c0                     xor eax, eax
0043e672  88d8                     mov al, bl
0043e674  8a12                     mov dl, byte ptr [edx]
0043e676  881404                   mov byte ptr [esp + eax], dl
0043e679  eb09                     jmp 0x43e684
0043e67b  31c0                     xor eax, eax
0043e67d  88d8                     mov al, bl
0043e67f  30c9                     xor cl, cl
0043e681  880c04                   mov byte ptr [esp + eax], cl
0043e684  80c704                   add bh, 4
0043e687  fec3                     inc bl
0043e689  31c0                     xor eax, eax
0043e68b  88d8                     mov al, bl
0043e68d  83f804                   cmp eax, 4
0043e690  7d30                     jge 0x43e6c2
0043e692  31c0                     xor eax, eax
0043e694  31c9                     xor ecx, ecx
0043e696  31d2                     xor edx, edx
0043e698  88f9                     mov cl, bh
0043e69a  6689f0                   mov ax, si
0043e69d  6689fa                   mov dx, di
0043e6a0  8b2ccd08634900           mov ebp, dword ptr [ecx*8 + 0x496308]
0043e6a7  c1fa08                   sar edx, 8
0043e6aa  01e8                     add eax, ebp
0043e6ac  0314cd0c634900           add edx, dword ptr [ecx*8 + 0x49630c]
0043e6b3  85c0                     test eax, eax
0043e6b5  0f8d74ffffff             jge 0x43e62f
0043e6bb  b8ffff0000               mov eax, 0xffff
0043e6c0  eb9a                     jmp 0x43e65c
0043e6c2  31c0                     xor eax, eax
0043e6c4  a070154e00               mov al, byte ptr [0x4e1570]
0043e6c9  85c0                     test eax, eax
0043e6cb  7422                     je 0x43e6ef
0043e6cd  8a1d70154e00             mov bl, byte ptr [0x4e1570]
0043e6d3  8a9070154e00             mov dl, byte ptr [eax + 0x4e1570]
0043e6d9  31c0                     xor eax, eax
0043e6db  fecb                     dec bl
0043e6dd  88d0                     mov al, dl
0043e6df  30f6                     xor dh, dh
0043e6e1  881d70154e00             mov byte ptr [0x4e1570], bl
0043e6e7  88b070164e00             mov byte ptr [eax + 0x4e1670], dh
0043e6ed  eb02                     jmp 0x43e6f1
0043e6ef  30d2                     xor dl, dl
0043e6f1  88542408                 mov byte ptr [esp + 8], dl
0043e6f5  89f8                     mov eax, edi
0043e6f7  30db                     xor bl, bl
0043e6f9  30e4                     xor ah, ah
0043e6fb  b701                     mov bh, 1
0043e6fd  89442404                 mov dword ptr [esp + 4], eax
0043e701  eb67                     jmp 0x43e76a
0043e703  31c9                     xor ecx, ecx
0043e705  668b0d68714900           mov cx, word ptr [0x497168]
0043e70c  49                       dec ecx
0043e70d  39c8                     cmp eax, ecx
0043e70f  0f8f8b000000             jg 0x43e7a0
0043e715  85d2                     test edx, edx
0043e717  0f8c83000000             jl 0x43e7a0
0043e71d  31c9                     xor ecx, ecx
0043e71f  668b0d6a714900           mov cx, word ptr [0x49716a]
0043e726  49                       dec ecx
0043e727  39ca                     cmp edx, ecx
0043e729  0f8f71000000             jg 0x43e7a0
0043e72f  c1e208                   shl edx, 8
0043e732  01d0                     add eax, edx
0043e734  25ffff0000               and eax, 0xffff
0043e739  3dffff0000               cmp eax, 0xffff
0043e73e  7425                     je 0x43e765
0043e740  8b156c154e00             mov edx, dword ptr [0x4e156c]
0043e746  01c2                     add edx, eax
0043e748  31c9                     xor ecx, ecx
0043e74a  8a0a                     mov cl, byte ptr [edx]
0043e74c  85c9                     test ecx, ecx
0043e74e  7415                     je 0x43e765
0043e750  0fb6f3                   movzx esi, bl
0043e753  88ca                     mov dl, cl
0043e755  3a1434                   cmp dl, byte ptr [esp + esi]
0043e758  750b                     jne 0x43e765
0043e75a  31d2                     xor edx, edx
0043e75c  8a542408                 mov dl, byte ptr [esp + 8]
0043e760  e8fffcffff               call 0x43e464
0043e765  80c704                   add bh, 4
0043e768  fec3                     inc bl
0043e76a  31c0                     xor eax, eax
0043e76c  88d8                     mov al, bl
0043e76e  83f804                   cmp eax, 4
0043e771  7d34                     jge 0x43e7a7
0043e773  31c0                     xor eax, eax
0043e775  31d2                     xor edx, edx
0043e777  31c9                     xor ecx, ecx
0043e779  668b442404               mov ax, word ptr [esp + 4]
0043e77e  6689fa                   mov dx, di
0043e781  88f9                     mov cl, bh
0043e783  c1fa08                   sar edx, 8
0043e786  8b34cd08634900           mov esi, dword ptr [ecx*8 + 0x496308]
0043e78d  8b2ccd0c634900           mov ebp, dword ptr [ecx*8 + 0x49630c]
0043e794  01f0                     add eax, esi
0043e796  01ea                     add edx, ebp
0043e798  85c0                     test eax, eax
0043e79a  0f8d63ffffff             jge 0x43e703
0043e7a0  b8ffff0000               mov eax, 0xffff
0043e7a5  eb8d                     jmp 0x43e734
0043e7a7  31d2                     xor edx, edx
0043e7a9  a16c154e00               mov eax, dword ptr [0x4e156c]
0043e7ae  6689fa                   mov dx, di
0043e7b1  01d0                     add eax, edx
0043e7b3  8a542408                 mov dl, byte ptr [esp + 8]
0043e7b7  8810                     mov byte ptr [eax], dl
0043e7b9  31c0                     xor eax, eax
0043e7bb  a070154e00               mov al, byte ptr [0x4e1570]
0043e7c0  3dff000000               cmp eax, 0xff
0043e7c5  7d2e                     jge 0x43e7f5
0043e7c7  31d2                     xor edx, edx
0043e7c9  8a1424                   mov dl, byte ptr [esp]
0043e7cc  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043e7d3  7520                     jne 0x43e7f5
0043e7d5  84d2                     test dl, dl
0043e7d7  741c                     je 0x43e7f5
0043e7d9  88c4                     mov ah, al
0043e7db  31c9                     xor ecx, ecx
0043e7dd  fec4                     inc ah
0043e7df  b301                     mov bl, 1
0043e7e1  88e1                     mov cl, ah
0043e7e3  882570154e00             mov byte ptr [0x4e1570], ah
0043e7e9  889a70164e00             mov byte ptr [edx + 0x4e1670], bl
0043e7ef  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043e7f5  31c0                     xor eax, eax
0043e7f7  a070154e00               mov al, byte ptr [0x4e1570]
0043e7fc  3dff000000               cmp eax, 0xff
0043e801  7d33                     jge 0x43e836
0043e803  31d2                     xor edx, edx
0043e805  8a542401                 mov dl, byte ptr [esp + 1]
0043e809  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043e810  7524                     jne 0x43e836
0043e812  84d2                     test dl, dl
0043e814  7420                     je 0x43e836
0043e816  88c5                     mov ch, al
0043e818  fec5                     inc ch
0043e81a  882d70154e00             mov byte ptr [0x4e1570], ch
0043e820  31c9                     xor ecx, ecx
0043e822  b001                     mov al, 1
0043e824  8a0d70154e00             mov cl, byte ptr [0x4e1570]
0043e82a  888270164e00             mov byte ptr [edx + 0x4e1670], al
0043e830  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043e836  31c0                     xor eax, eax
0043e838  a070154e00               mov al, byte ptr [0x4e1570]
0043e83d  3dff000000               cmp eax, 0xff
0043e842  7d2e                     jge 0x43e872
0043e844  31d2                     xor edx, edx
0043e846  8a542402                 mov dl, byte ptr [esp + 2]
0043e84a  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043e851  751f                     jne 0x43e872
0043e853  84d2                     test dl, dl
0043e855  741b                     je 0x43e872
0043e857  88c7                     mov bh, al
0043e859  31c9                     xor ecx, ecx
0043e85b  fec7                     inc bh
0043e85d  88f9                     mov cl, bh
0043e85f  883d70154e00             mov byte ptr [0x4e1570], bh
0043e865  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043e86b  c68270164e0001           mov byte ptr [edx + 0x4e1670], 1
0043e872  31c0                     xor eax, eax
0043e874  a070154e00               mov al, byte ptr [0x4e1570]
0043e879  3dff000000               cmp eax, 0xff
0043e87e  7d2f                     jge 0x43e8af
0043e880  31d2                     xor edx, edx
0043e882  8a542403                 mov dl, byte ptr [esp + 3]
0043e886  80ba70164e0000           cmp byte ptr [edx + 0x4e1670], 0
0043e88d  7520                     jne 0x43e8af
0043e88f  84d2                     test dl, dl
0043e891  741c                     je 0x43e8af
0043e893  88c4                     mov ah, al
0043e895  31c9                     xor ecx, ecx
0043e897  fec4                     inc ah
0043e899  b301                     mov bl, 1
0043e89b  88e1                     mov cl, ah
0043e89d  882570154e00             mov byte ptr [0x4e1570], ah
0043e8a3  889a70164e00             mov byte ptr [edx + 0x4e1670], bl
0043e8a9  889170154e00             mov byte ptr [ecx + 0x4e1570], dl
0043e8af  83c40c                   add esp, 0xc
0043e8b2  e92309ffff               jmp 0x42f1da
