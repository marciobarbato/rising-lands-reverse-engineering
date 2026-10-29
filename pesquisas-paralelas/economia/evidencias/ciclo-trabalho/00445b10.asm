; SetEnginRentreBatiment; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00445b10  53                       push ebx
00445b11  51                       push ecx
00445b12  56                       push esi
00445b13  57                       push edi
00445b14  55                       push ebp
00445b15  83ec14                   sub esp, 0x14
00445b18  89c1                     mov ecx, eax
00445b1a  89d6                     mov esi, edx
00445b1c  0fb7e9                   movzx ebp, cx
00445b1f  89eb                     mov ebx, ebp
00445b21  c1e304                   shl ebx, 4
00445b24  31ff                     xor edi, edi
00445b26  01eb                     add ebx, ebp
00445b28  6689d7                   mov di, dx
00445b2b  c1e302                   shl ebx, 2
00445b2e  89f8                     mov eax, edi
00445b30  01eb                     add ebx, ebp
00445b32  e8bd49fdff               call 0x41a4f4
00445b37  c1e302                   shl ebx, 2
00445b3a  31d2                     xor edx, edx
00445b3c  891c24                   mov dword ptr [esp], ebx
00445b3f  88c2                     mov dl, al
00445b41  8b0424                   mov eax, dword ptr [esp]
00445b44  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00445b4a  01c3                     add ebx, eax
00445b4c  83fa08                   cmp edx, 8
00445b4f  0f8502010000             jne 0x445c57
00445b55  8a4301                   mov al, byte ptr [ebx + 1]
00445b58  8844240c                 mov byte ptr [esp + 0xc], al
00445b5c  31c0                     xor eax, eax
00445b5e  8a44240c                 mov al, byte ptr [esp + 0xc]
00445b62  83f809                   cmp eax, 9
00445b65  0f84ec000000             je 0x445c57
00445b6b  89ea                     mov edx, ebp
00445b6d  89f8                     mov eax, edi
00445b6f  e8e374fdff               call 0x41d057
00445b74  8b3c24                   mov edi, dword ptr [esp]
00445b77  668983b2000000           mov word ptr [ebx + 0xb2], ax
00445b7e  89c2                     mov edx, eax
00445b80  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445b85  01f8                     add eax, edi
00445b87  6689507e                 mov word ptr [eax + 0x7e], dx
00445b8b  663b0d04634900           cmp cx, word ptr [0x496304]
00445b92  7522                     jne 0x445bb6
00445b94  30d2                     xor dl, dl
00445b96  31ed                     xor ebp, ebp
00445b98  8815360f4e00             mov byte ptr [0x4e0f36], dl
00445b9e  8815370f4e00             mov byte ptr [0x4e0f37], dl
00445ba4  baffff0000               mov edx, 0xffff
00445ba9  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
00445baf  66891504634900           mov word ptr [0x496304], dx
00445bb6  c6808800000000           mov byte ptr [eax + 0x88], 0
00445bbd  6689b3c0000000           mov word ptr [ebx + 0xc0], si
00445bc4  c644241015               mov byte ptr [esp + 0x10], 0x15
00445bc9  31db                     xor ebx, ebx
00445bcb  6689cb                   mov bx, cx
00445bce  89d8                     mov eax, ebx
00445bd0  c1e004                   shl eax, 4
00445bd3  01d8                     add eax, ebx
00445bd5  c1e002                   shl eax, 2
00445bd8  01c3                     add ebx, eax
00445bda  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445bdf  c1e302                   shl ebx, 2
00445be2  89ca                     mov edx, ecx
00445be4  8a440302                 mov al, byte ptr [ebx + eax + 2]
00445be8  25ff000000               and eax, 0xff
00445bed  7409                     je 0x445bf8
00445bef  83f804                   cmp eax, 4
00445bf2  7404                     je 0x445bf8
00445bf4  b001                     mov al, 1
00445bf6  eb02                     jmp 0x445bfa
00445bf8  30c0                     xor al, al
00445bfa  84c0                     test al, al
00445bfc  0f8422030000             je 0x445f24
00445c02  31c0                     xor eax, eax
00445c04  6689d0                   mov ax, dx
00445c07  89c3                     mov ebx, eax
00445c09  c1e304                   shl ebx, 4
00445c0c  01c3                     add ebx, eax
00445c0e  c1e302                   shl ebx, 2
00445c11  01c3                     add ebx, eax
00445c13  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445c18  c1e302                   shl ebx, 2
00445c1b  01d8                     add eax, ebx
00445c1d  8a5c2410                 mov bl, byte ptr [esp + 0x10]
00445c21  885802                   mov byte ptr [eax + 2], bl
00445c24  663b1504634900           cmp dx, word ptr [0x496304]
00445c2b  0f85f3020000             jne 0x445f24
00445c31  b9ffff0000               mov ecx, 0xffff
00445c36  30ff                     xor bh, bh
00445c38  31c0                     xor eax, eax
00445c3a  883d360f4e00             mov byte ptr [0x4e0f36], bh
00445c40  883d370f4e00             mov byte ptr [0x4e0f37], bh
00445c46  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
00445c4b  66890d04634900           mov word ptr [0x496304], cx
00445c52  e9cd020000               jmp 0x445f24
00445c57  83fa0e                   cmp edx, 0xe
00445c5a  740d                     je 0x445c69
00445c5c  e955010000               jmp 0x445db6
00445c61  b001                     mov al, 1
00445c63  eb32                     jmp 0x445c97
00445c65  30c0                     xor al, al
00445c67  eb2e                     jmp 0x445c97
00445c69  31ff                     xor edi, edi
00445c6b  6689cf                   mov di, cx
00445c6e  89f8                     mov eax, edi
00445c70  c1e004                   shl eax, 4
00445c73  01f8                     add eax, edi
00445c75  c1e002                   shl eax, 2
00445c78  01f8                     add eax, edi
00445c7a  8b3da0194e00             mov edi, dword ptr [0x4e19a0]
00445c80  8a448701                 mov al, byte ptr [edi + eax*4 + 1]
00445c84  2c0b                     sub al, 0xb
00445c86  3c06                     cmp al, 6
00445c88  77db                     ja 0x445c65
00445c8a  25ff000000               and eax, 0xff
00445c8f  2eff2485f45a4400         jmp dword ptr cs:[eax*4 + 0x445af4]
00445c97  25ff000000               and eax, 0xff
00445c9c  83f801                   cmp eax, 1
00445c9f  0f8511010000             jne 0x445db6
00445ca5  31ff                     xor edi, edi
00445ca7  6689f7                   mov di, si
00445caa  89f8                     mov eax, edi
00445cac  e83b4afdff               call 0x41a6ec
00445cb1  25ff000000               and eax, 0xff
00445cb6  83f804                   cmp eax, 4
00445cb9  0f84f7000000             je 0x445db6
00445cbf  0fb7e9                   movzx ebp, cx
00445cc2  89f8                     mov eax, edi
00445cc4  89ea                     mov edx, ebp
00445cc6  e88c73fdff               call 0x41d057
00445ccb  89ea                     mov edx, ebp
00445ccd  c1e204                   shl edx, 4
00445cd0  01ea                     add edx, ebp
00445cd2  89c7                     mov edi, eax
00445cd4  c1e202                   shl edx, 2
00445cd7  668983b2000000           mov word ptr [ebx + 0xb2], ax
00445cde  01ea                     add edx, ebp
00445ce0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445ce5  c1e202                   shl edx, 2
00445ce8  01d0                     add eax, edx
00445cea  6689787e                 mov word ptr [eax + 0x7e], di
00445cee  663b0d04634900           cmp cx, word ptr [0x496304]
00445cf5  751f                     jne 0x445d16
00445cf7  30f6                     xor dh, dh
00445cf9  8835360f4e00             mov byte ptr [0x4e0f36], dh
00445cff  8835370f4e00             mov byte ptr [0x4e0f37], dh
00445d05  31d2                     xor edx, edx
00445d07  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00445d0d  66c70504634900ffff       mov word ptr [0x496304], 0xffff
00445d16  c64424080d               mov byte ptr [esp + 8], 0xd
00445d1b  31d2                     xor edx, edx
00445d1d  6689ca                   mov dx, cx
00445d20  c6808800000000           mov byte ptr [eax + 0x88], 0
00445d27  89d0                     mov eax, edx
00445d29  c1e004                   shl eax, 4
00445d2c  01d0                     add eax, edx
00445d2e  c1e002                   shl eax, 2
00445d31  6689b3c0000000           mov word ptr [ebx + 0xc0], si
00445d38  01d0                     add eax, edx
00445d3a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00445d40  89ce                     mov esi, ecx
00445d42  8a448202                 mov al, byte ptr [edx + eax*4 + 2]
00445d46  25ff000000               and eax, 0xff
00445d4b  7409                     je 0x445d56
00445d4d  83f804                   cmp eax, 4
00445d50  7404                     je 0x445d56
00445d52  b001                     mov al, 1
00445d54  eb02                     jmp 0x445d58
00445d56  30c0                     xor al, al
00445d58  84c0                     test al, al
00445d5a  0f84c4010000             je 0x445f24
00445d60  31db                     xor ebx, ebx
00445d62  6689f3                   mov bx, si
00445d65  89da                     mov edx, ebx
00445d67  c1e204                   shl edx, 4
00445d6a  01da                     add edx, ebx
00445d6c  c1e202                   shl edx, 2
00445d6f  01da                     add edx, ebx
00445d71  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445d76  c1e202                   shl edx, 2
00445d79  01d0                     add eax, edx
00445d7b  8a542408                 mov dl, byte ptr [esp + 8]
00445d7f  885002                   mov byte ptr [eax + 2], dl
00445d82  663b3504634900           cmp si, word ptr [0x496304]
00445d89  0f8595010000             jne 0x445f24
00445d8f  30db                     xor bl, bl
00445d91  b9ffff0000               mov ecx, 0xffff
00445d96  881d360f4e00             mov byte ptr [0x4e0f36], bl
00445d9c  881d370f4e00             mov byte ptr [0x4e0f37], bl
00445da2  31db                     xor ebx, ebx
00445da4  66890d04634900           mov word ptr [0x496304], cx
00445dab  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
00445db1  e96e010000               jmp 0x445f24
00445db6  83fa12                   cmp edx, 0x12
00445db9  0f8577000000             jne 0x445e36
00445dbf  31d2                     xor edx, edx
00445dc1  6689ca                   mov dx, cx
00445dc4  89d7                     mov edi, edx
00445dc6  c1e704                   shl edi, 4
00445dc9  01d7                     add edi, edx
00445dcb  c1e702                   shl edi, 2
00445dce  01d7                     add edi, edx
00445dd0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445dd5  c1e702                   shl edi, 2
00445dd8  8a440701                 mov al, byte ptr [edi + eax + 1]
00445ddc  25ff000000               and eax, 0xff
00445de1  83f810                   cmp eax, 0x10
00445de4  7550                     jne 0x445e36
00445de6  31c0                     xor eax, eax
00445de8  6689f0                   mov ax, si
00445deb  e8f250fdff               call 0x41aee2
00445df0  40                       inc eax
00445df1  668983b2000000           mov word ptr [ebx + 0xb2], ax
00445df8  89c2                     mov edx, eax
00445dfa  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445dff  01f8                     add eax, edi
00445e01  6689507e                 mov word ptr [eax + 0x7e], dx
00445e05  663b0d04634900           cmp cx, word ptr [0x496304]
00445e0c  0f857b000000             jne 0x445e8d
00445e12  30d2                     xor dl, dl
00445e14  31ff                     xor edi, edi
00445e16  8815360f4e00             mov byte ptr [0x4e0f36], dl
00445e1c  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
00445e22  bfffff0000               mov edi, 0xffff
00445e27  8815370f4e00             mov byte ptr [0x4e0f37], dl
00445e2d  66893d04634900           mov word ptr [0x496304], di
00445e34  eb57                     jmp 0x445e8d
00445e36  31c0                     xor eax, eax
00445e38  6689f0                   mov ax, si
00445e3b  31d2                     xor edx, edx
00445e3d  e8a050fdff               call 0x41aee2
00445e42  6689ca                   mov dx, cx
00445e45  89c7                     mov edi, eax
00445e47  89d0                     mov eax, edx
00445e49  c1e004                   shl eax, 4
00445e4c  01d0                     add eax, edx
00445e4e  c1e002                   shl eax, 2
00445e51  01d0                     add eax, edx
00445e53  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00445e59  c1e002                   shl eax, 2
00445e5c  01d0                     add eax, edx
00445e5e  6689787e                 mov word ptr [eax + 0x7e], di
00445e62  663b0d04634900           cmp cx, word ptr [0x496304]
00445e69  7522                     jne 0x445e8d
00445e6b  30d2                     xor dl, dl
00445e6d  bfffff0000               mov edi, 0xffff
00445e72  8815360f4e00             mov byte ptr [0x4e0f36], dl
00445e78  8815370f4e00             mov byte ptr [0x4e0f37], dl
00445e7e  31d2                     xor edx, edx
00445e80  66893d04634900           mov word ptr [0x496304], di
00445e87  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
00445e8d  c6808800000000           mov byte ptr [eax + 0x88], 0
00445e94  31d2                     xor edx, edx
00445e96  b00d                     mov al, 0xd
00445e98  6689ca                   mov dx, cx
00445e9b  88442404                 mov byte ptr [esp + 4], al
00445e9f  89d0                     mov eax, edx
00445ea1  c1e004                   shl eax, 4
00445ea4  01d0                     add eax, edx
00445ea6  c1e002                   shl eax, 2
00445ea9  6689b3c0000000           mov word ptr [ebx + 0xc0], si
00445eb0  01c2                     add edx, eax
00445eb2  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00445eb7  c1e202                   shl edx, 2
00445eba  89cb                     mov ebx, ecx
00445ebc  8a440202                 mov al, byte ptr [edx + eax + 2]
00445ec0  25ff000000               and eax, 0xff
00445ec5  7409                     je 0x445ed0
00445ec7  83f804                   cmp eax, 4
00445eca  7404                     je 0x445ed0
00445ecc  b001                     mov al, 1
00445ece  eb02                     jmp 0x445ed2
00445ed0  30c0                     xor al, al
00445ed2  84c0                     test al, al
00445ed4  744e                     je 0x445f24
00445ed6  31d2                     xor edx, edx
00445ed8  6689da                   mov dx, bx
00445edb  89d0                     mov eax, edx
00445edd  c1e004                   shl eax, 4
00445ee0  01d0                     add eax, edx
00445ee2  c1e002                   shl eax, 2
00445ee5  01d0                     add eax, edx
00445ee7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00445eed  c1e002                   shl eax, 2
00445ef0  01d0                     add eax, edx
00445ef2  8a542404                 mov dl, byte ptr [esp + 4]
00445ef6  885002                   mov byte ptr [eax + 2], dl
00445ef9  663b1d04634900           cmp bx, word ptr [0x496304]
00445f00  7522                     jne 0x445f24
00445f02  baffff0000               mov edx, 0xffff
00445f07  30e4                     xor ah, ah
00445f09  31ed                     xor ebp, ebp
00445f0b  8825360f4e00             mov byte ptr [0x4e0f36], ah
00445f11  8825370f4e00             mov byte ptr [0x4e0f37], ah
00445f17  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
00445f1d  66891504634900           mov word ptr [0x496304], dx
00445f24  83c414                   add esp, 0x14
00445f27  5d                       pop ebp
00445f28  5f                       pop edi
00445f29  5e                       pop esi
00445f2a  59                       pop ecx
00445f2b  5b                       pop ebx
00445f2c  c3                       ret
