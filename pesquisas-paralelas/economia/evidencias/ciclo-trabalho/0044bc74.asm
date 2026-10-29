; CalculWorkEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044bc74  53                       push ebx
0044bc75  51                       push ecx
0044bc76  52                       push edx
0044bc77  56                       push esi
0044bc78  57                       push edi
0044bc79  55                       push ebp
0044bc7a  83ec58                   sub esp, 0x58
0044bc7d  89c7                     mov edi, eax
0044bc7f  0fb7e8                   movzx ebp, ax
0044bc82  89e9                     mov ecx, ebp
0044bc84  c1e104                   shl ecx, 4
0044bc87  01e9                     add ecx, ebp
0044bc89  c1e102                   shl ecx, 2
0044bc8c  01e9                     add ecx, ebp
0044bc8e  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044bc94  c1e102                   shl ecx, 2
0044bc97  30e4                     xor ah, ah
0044bc99  01ce                     add esi, ecx
0044bc9b  88642444                 mov byte ptr [esp + 0x44], ah
0044bc9f  8a5e01                   mov bl, byte ptr [esi + 1]
0044bca2  890c24                   mov dword ptr [esp], ecx
0044bca5  80fb06                   cmp bl, 6
0044bca8  0f8291260000             jb 0x44e33f
0044bcae  0f8630110000             jbe 0x44cde4
0044bcb4  80fb07                   cmp bl, 7
0044bcb7  0f86650f0000             jbe 0x44cc22
0044bcbd  80fb0d                   cmp bl, 0xd
0044bcc0  0f84951b0000             je 0x44d85b
0044bcc6  e979260000               jmp 0x44e344
0044bccb  c744241001000000         mov dword ptr [esp + 0x10], 1
0044bcd3  eb0d                     jmp 0x44bce2
0044bcd5  b002                     mov al, 2
0044bcd7  8d560a                   lea edx, [esi + 0xa]
0044bcda  38c0                     cmp al, al
0044bcdc  76ed                     jbe 0x44bccb
0044bcde  3c04                     cmp al, 4
0044bce0  76e9                     jbe 0x44bccb
0044bce2  31db                     xor ebx, ebx
0044bce4  31c0                     xor eax, eax
0044bce6  668b5c2410               mov bx, word ptr [esp + 0x10]
0044bceb  668b4266                 mov ax, word ptr [edx + 0x66]
0044bcef  01c3                     add ebx, eax
0044bcf1  31c0                     xor eax, eax
0044bcf3  668b4202                 mov ax, word ptr [edx + 2]
0044bcf7  39c3                     cmp ebx, eax
0044bcf9  0f9ec0                   setle al
0044bcfc  84c0                     test al, al
0044bcfe  0f843a020000             je 0x44bf3e
0044bd04  668b467e                 mov ax, word ptr [esi + 0x7e]
0044bd08  668b4e08                 mov cx, word ptr [esi + 8]
0044bd0c  6639c8                   cmp ax, cx
0044bd0f  740f                     je 0x44bd20
0044bd11  31c0                     xor eax, eax
0044bd13  6689f8                   mov ax, di
0044bd16  e8f1d5ffff               call 0x44930c
0044bd1b  e924260000               jmp 0x44e344
0044bd20  668b96b2000000           mov dx, word ptr [esi + 0xb2]
0044bd27  6639d1                   cmp cx, dx
0044bd2a  0f85bf010000             jne 0x44beef
0044bd30  31c0                     xor eax, eax
0044bd32  668b4608                 mov ax, word ptr [esi + 8]
0044bd36  e8c7960200               call 0x475402
0044bd3b  84c0                     test al, al
0044bd3d  744b                     je 0x44bd8a
0044bd3f  31c0                     xor eax, eax
0044bd41  668b4608                 mov ax, word ptr [esi + 8]
0044bd45  e85d970200               call 0x4754a7
0044bd4a  31c0                     xor eax, eax
0044bd4c  6689f8                   mov ax, di
0044bd4f  31db                     xor ebx, ebx
0044bd51  e802b30000               call 0x457058
0044bd56  8a5e01                   mov bl, byte ptr [esi + 1]
0044bd59  ba03000000               mov edx, 3
0044bd5e  89d9                     mov ecx, ebx
0044bd60  c6868900000001           mov byte ptr [esi + 0x89], 1
0044bd67  c1e102                   shl ecx, 2
0044bd6a  89d8                     mov eax, ebx
0044bd6c  29d9                     sub ecx, ebx
0044bd6e  31d8                     xor eax, ebx
0044bd70  c1e103                   shl ecx, 3
0044bd73  8a06                     mov al, byte ptr [esi]
0044bd75  01d9                     add ecx, ebx
0044bd77  e844cffdff               call 0x428cc0
0044bd7c  89c2                     mov edx, eax
0044bd7e  8a044dde654900           mov al, byte ptr [ecx*2 + 0x4965de]
0044bd85  e9821b0000               jmp 0x44d90c
0044bd8a  f6057c8f50001f           test byte ptr [0x508f7c], 0x1f
0044bd91  0f85ad250000             jne 0x44e344
0044bd97  31db                     xor ebx, ebx
0044bd99  6689fb                   mov bx, di
0044bd9c  89d9                     mov ecx, ebx
0044bd9e  c1e104                   shl ecx, 4
0044bda1  01d9                     add ecx, ebx
0044bda3  c1e102                   shl ecx, 2
0044bda6  01d9                     add ecx, ebx
0044bda8  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044bdad  c1e102                   shl ecx, 2
0044bdb0  01c1                     add ecx, eax
0044bdb2  8a01                     mov al, byte ptr [ecx]
0044bdb4  8a2541805000             mov ah, byte ptr [0x508041]
0044bdba  38e0                     cmp al, ah
0044bdbc  0f8558000000             jne 0x44be1a
0044bdc2  31d2                     xor edx, edx
0044bdc4  88e2                     mov dl, ah
0044bdc6  31c0                     xor eax, eax
0044bdc8  668b4108                 mov ax, word ptr [ecx + 8]
0044bdcc  e81fa90200               call 0x4766f0
0044bdd1  84c0                     test al, al
0044bdd3  0f8441000000             je 0x44be1a
0044bdd9  89d8                     mov eax, ebx
0044bddb  e87d4effff               call 0x440c5d
0044bde0  8b8104010000             mov eax, dword ptr [ecx + 0x104]
0044bde6  c681f900000000           mov byte ptr [ecx + 0xf9], 0
0044bded  83f8ff                   cmp eax, -1
0044bdf0  0f8524000000             jne 0x44be1a
0044bdf6  31c0                     xor eax, eax
0044bdf8  8a4101                   mov al, byte ptr [ecx + 1]
0044bdfb  6800010000               push 0x100
0044be00  c1e010                   shl eax, 0x10
0044be03  8d9904010000             lea ebx, [ecx + 0x104]
0044be09  80cc10                   or ah, 0x10
0044be0c  31c9                     xor ecx, ecx
0044be0e  89c2                     mov edx, eax
0044be10  b850000000               mov eax, 0x50
0044be15  e85fec0300               call 0x48aa79
0044be1a  8a8682000000             mov al, byte ptr [esi + 0x82]
0044be20  3c01                     cmp al, 1
0044be22  0f821c250000             jb 0x44e344
0044be28  766a                     jbe 0x44be94
0044be2a  3c02                     cmp al, 2
0044be2c  0f8512250000             jne 0x44e344
0044be32  31d2                     xor edx, edx
0044be34  6689fa                   mov dx, di
0044be37  89d1                     mov ecx, edx
0044be39  c1e104                   shl ecx, 4
0044be3c  31c0                     xor eax, eax
0044be3e  01d1                     add ecx, edx
0044be40  668b8680000000           mov ax, word ptr [esi + 0x80]
0044be47  c1e102                   shl ecx, 2
0044be4a  e893f0fcff               call 0x41aee2
0044be4f  01d1                     add ecx, edx
0044be51  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044be57  c1e102                   shl ecx, 2
0044be5a  01ca                     add edx, ecx
0044be5c  6689427e                 mov word ptr [edx + 0x7e], ax
0044be60  663b3d04634900           cmp di, word ptr [0x496304]
0044be67  0f85470a0000             jne 0x44c8b4
0044be6d  30db                     xor bl, bl
0044be6f  bfffff0000               mov edi, 0xffff
0044be74  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044be7a  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044be80  31db                     xor ebx, ebx
0044be82  66893d04634900           mov word ptr [0x496304], di
0044be89  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044be8f  e9200a0000               jmp 0x44c8b4
0044be94  31c0                     xor eax, eax
0044be96  6689f8                   mov ax, di
0044be99  89c1                     mov ecx, eax
0044be9b  c1e104                   shl ecx, 4
0044be9e  01c1                     add ecx, eax
0044bea0  c1e102                   shl ecx, 2
0044bea3  01c1                     add ecx, eax
0044bea5  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044beab  c1e102                   shl ecx, 2
0044beae  01ca                     add edx, ecx
0044beb0  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044beb7  66895a7e                 mov word ptr [edx + 0x7e], bx
0044bebb  663b3d04634900           cmp di, word ptr [0x496304]
0044bec2  0f85ec090000             jne 0x44c8b4
0044bec8  30c9                     xor cl, cl
0044beca  bbffff0000               mov ebx, 0xffff
0044becf  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044bed5  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044bedb  31c9                     xor ecx, ecx
0044bedd  66891d04634900           mov word ptr [0x496304], bx
0044bee4  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044beea  e9c5090000               jmp 0x44c8b4
0044beef  89d0                     mov eax, edx
0044bef1  31d2                     xor edx, edx
0044bef3  6689fa                   mov dx, di
0044bef6  89d1                     mov ecx, edx
0044bef8  c1e104                   shl ecx, 4
0044befb  01d1                     add ecx, edx
0044befd  c1e102                   shl ecx, 2
0044bf00  01d1                     add ecx, edx
0044bf02  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044bf08  c1e102                   shl ecx, 2
0044bf0b  01ca                     add edx, ecx
0044bf0d  6689427e                 mov word ptr [edx + 0x7e], ax
0044bf11  663b3d04634900           cmp di, word ptr [0x496304]
0044bf18  0f8596090000             jne 0x44c8b4
0044bf1e  b9ffff0000               mov ecx, 0xffff
0044bf23  30ff                     xor bh, bh
0044bf25  31ed                     xor ebp, ebp
0044bf27  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044bf2d  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044bf33  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044bf39  e96f090000               jmp 0x44c8ad
0044bf3e  31c0                     xor eax, eax
0044bf40  8a8682000000             mov al, byte ptr [esi + 0x82]
0044bf46  85c0                     test eax, eax
0044bf48  0f8593000000             jne 0x44bfe1
0044bf4e  e9f1230000               jmp 0x44e344
0044bf53  668b8680000000           mov ax, word ptr [esi + 0x80]
0044bf5a  668986c0000000           mov word ptr [esi + 0xc0], ax
0044bf61  31c0                     xor eax, eax
0044bf63  668b8680000000           mov ax, word ptr [esi + 0x80]
0044bf6a  e8b87bfdff               call 0x423b27
0044bf6f  89442424                 mov dword ptr [esp + 0x24], eax
0044bf73  e977000000               jmp 0x44bfef
0044bf78  668b8680000000           mov ax, word ptr [esi + 0x80]
0044bf7f  ba02000000               mov edx, 2
0044bf84  0fb7e8                   movzx ebp, ax
0044bf87  89442424                 mov dword ptr [esp + 0x24], eax
0044bf8b  89e8                     mov eax, ebp
0044bf8d  e8d1970200               call 0x475763
0044bf92  84c0                     test al, al
0044bf94  7559                     jne 0x44bfef
0044bf96  b944000000               mov ecx, 0x44
0044bf9b  ba0a000000               mov edx, 0xa
0044bfa0  89e8                     mov eax, ebp
0044bfa2  89cb                     mov ebx, ecx
0044bfa4  e864b90200               call 0x47790d
0044bfa9  89442424                 mov dword ptr [esp + 0x24], eax
0044bfad  25ffff0000               and eax, 0xffff
0044bfb2  3dffff0000               cmp eax, 0xffff
0044bfb7  751b                     jne 0x44bfd4
0044bfb9  ba0a000000               mov edx, 0xa
0044bfbe  31c0                     xor eax, eax
0044bfc0  31c9                     xor ecx, ecx
0044bfc2  31db                     xor ebx, ebx
0044bfc4  668b8680000000           mov ax, word ptr [esi + 0x80]
0044bfcb  e83db90200               call 0x47790d
0044bfd0  89442424                 mov dword ptr [esp + 0x24], eax
0044bfd4  8b442424                 mov eax, dword ptr [esp + 0x24]
0044bfd8  66898680000000           mov word ptr [esi + 0x80], ax
0044bfdf  eb0e                     jmp 0x44bfef
0044bfe1  3c01                     cmp al, 1
0044bfe3  720a                     jb 0x44bfef
0044bfe5  7691                     jbe 0x44bf78
0044bfe7  3c02                     cmp al, 2
0044bfe9  0f8464ffffff             je 0x44bf53
0044bfef  31c0                     xor eax, eax
0044bff1  668b442424               mov ax, word ptr [esp + 0x24]
0044bff6  3dffff0000               cmp eax, 0xffff
0044bffb  7458                     je 0x44c055
0044bffd  31c0                     xor eax, eax
0044bfff  6689f8                   mov ax, di
0044c002  89c1                     mov ecx, eax
0044c004  c1e104                   shl ecx, 4
0044c007  01c1                     add ecx, eax
0044c009  c1e102                   shl ecx, 2
0044c00c  c6868900000003           mov byte ptr [esi + 0x89], 3
0044c013  01c1                     add ecx, eax
0044c015  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c01b  c1e102                   shl ecx, 2
0044c01e  01ca                     add edx, ecx
0044c020  8b442424                 mov eax, dword ptr [esp + 0x24]
0044c024  6689427e                 mov word ptr [edx + 0x7e], ax
0044c028  663b3d04634900           cmp di, word ptr [0x496304]
0044c02f  0f857f080000             jne 0x44c8b4
0044c035  bbffff0000               mov ebx, 0xffff
0044c03a  30e4                     xor ah, ah
0044c03c  31ff                     xor edi, edi
0044c03e  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044c044  8825370f4e00             mov byte ptr [0x4e0f37], ah
0044c04a  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044c050  e9cf110000               jmp 0x44d224
0044c055  31d2                     xor edx, edx
0044c057  b107                     mov cl, 7
0044c059  6689fa                   mov dx, di
0044c05c  884c2434                 mov byte ptr [esp + 0x34], cl
0044c060  89d1                     mov ecx, edx
0044c062  c1e104                   shl ecx, 4
0044c065  01d1                     add ecx, edx
0044c067  c1e102                   shl ecx, 2
0044c06a  01d1                     add ecx, edx
0044c06c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c072  31c0                     xor eax, eax
0044c074  8a448a02                 mov al, byte ptr [edx + ecx*4 + 2]
0044c078  89fb                     mov ebx, edi
0044c07a  85c0                     test eax, eax
0044c07c  7409                     je 0x44c087
0044c07e  83f804                   cmp eax, 4
0044c081  7404                     je 0x44c087
0044c083  b001                     mov al, 1
0044c085  eb02                     jmp 0x44c089
0044c087  30c0                     xor al, al
0044c089  84c0                     test al, al
0044c08b  0f84b3220000             je 0x44e344
0044c091  31c0                     xor eax, eax
0044c093  6689d8                   mov ax, bx
0044c096  89c1                     mov ecx, eax
0044c098  c1e104                   shl ecx, 4
0044c09b  01c1                     add ecx, eax
0044c09d  c1e102                   shl ecx, 2
0044c0a0  01c1                     add ecx, eax
0044c0a2  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c0a7  8a542434                 mov dl, byte ptr [esp + 0x34]
0044c0ab  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044c0af  663b1d04634900           cmp bx, word ptr [0x496304]
0044c0b6  0f8588220000             jne 0x44e344
0044c0bc  30ed                     xor ch, ch
0044c0be  31f6                     xor esi, esi
0044c0c0  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044c0c6  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044c0cc  beffff0000               mov esi, 0xffff
0044c0d1  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044c0d7  66893504634900           mov word ptr [0x496304], si
0044c0de  e961220000               jmp 0x44e344
0044c0e3  31c0                     xor eax, eax
0044c0e5  6689f8                   mov ax, di
0044c0e8  e86bbeffff               call 0x447f58
0044c0ed  8a8e8b000000             mov cl, byte ptr [esi + 0x8b]
0044c0f3  31c0                     xor eax, eax
0044c0f5  fec9                     dec cl
0044c0f7  88c8                     mov al, cl
0044c0f9  888e8b000000             mov byte ptr [esi + 0x8b], cl
0044c0ff  85c0                     test eax, eax
0044c101  740f                     je 0x44c112
0044c103  e93c220000               jmp 0x44e344
0044c108  c744240801000000         mov dword ptr [esp + 8], 1
0044c110  eb11                     jmp 0x44c123
0044c112  b002                     mov al, 2
0044c114  8d560a                   lea edx, [esi + 0xa]
0044c117  3c01                     cmp al, 1
0044c119  7208                     jb 0x44c123
0044c11b  38c0                     cmp al, al
0044c11d  76e9                     jbe 0x44c108
0044c11f  3c04                     cmp al, 4
0044c121  76e5                     jbe 0x44c108
0044c123  31db                     xor ebx, ebx
0044c125  31c0                     xor eax, eax
0044c127  668b5c2408               mov bx, word ptr [esp + 8]
0044c12c  668b4266                 mov ax, word ptr [edx + 0x66]
0044c130  01c3                     add ebx, eax
0044c132  31c0                     xor eax, eax
0044c134  668b4202                 mov ax, word ptr [edx + 2]
0044c138  39c3                     cmp ebx, eax
0044c13a  0f9ec0                   setle al
0044c13d  84c0                     test al, al
0044c13f  0f84ea010000             je 0x44c32f
0044c145  31c0                     xor eax, eax
0044c147  668b4608                 mov ax, word ptr [esi + 8]
0044c14b  e857940200               call 0x4755a7
0044c150  6685c0                   test ax, ax
0044c153  742c                     je 0x44c181
0044c155  8d4e0a                   lea ecx, [esi + 0xa]
0044c158  66ff4166                 inc word ptr [ecx + 0x66]
0044c15c  31d2                     xor edx, edx
0044c15e  668b01                   mov ax, word ptr [ecx]
0044c161  6689c2                   mov dx, ax
0044c164  89d0                     mov eax, edx
0044c166  c644114202               mov byte ptr [ecx + edx + 0x42], 2
0044c16b  66c74441060200           mov word ptr [ecx + eax*2 + 6], 2
0044c172  66ff01                   inc word ptr [ecx]
0044c175  c6868b00000032           mov byte ptr [esi + 0x8b], 0x32
0044c17c  e9c3210000               jmp 0x44e344
0044c181  31c0                     xor eax, eax
0044c183  668b4608                 mov ax, word ptr [esi + 8]
0044c187  e852930200               call 0x4754de
0044c18c  31c0                     xor eax, eax
0044c18e  6689f8                   mov ax, di
0044c191  89c1                     mov ecx, eax
0044c193  c1e104                   shl ecx, 4
0044c196  01c1                     add ecx, eax
0044c198  c1e102                   shl ecx, 2
0044c19b  01c1                     add ecx, eax
0044c19d  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044c1a3  c1e102                   shl ecx, 2
0044c1a6  668b541908               mov dx, word ptr [ecx + ebx + 8]
0044c1ab  81e2ffff0000             and edx, 0xffff
0044c1b1  e8fe6affff               call 0x442cb4
0044c1b6  c644197201               mov byte ptr [ecx + ebx + 0x72], 1
0044c1bb  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c1c0  01c1                     add ecx, eax
0044c1c2  31db                     xor ebx, ebx
0044c1c4  668b4108                 mov ax, word ptr [ecx + 8]
0044c1c8  8a19                     mov bl, byte ptr [ecx]
0044c1ca  89442420                 mov dword ptr [esp + 0x20], eax
0044c1ce  81fbc8000000             cmp ebx, 0xc8
0044c1d4  745d                     je 0x44c233
0044c1d6  83fb04                   cmp ebx, 4
0044c1d9  7458                     je 0x44c233
0044c1db  30e4                     xor ah, ah
0044c1dd  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0044c1e3  0502000000               add eax, 2
0044c1e8  89442428                 mov dword ptr [esp + 0x28], eax
0044c1ec  30e4                     xor ah, ah
0044c1ee  8b542428                 mov edx, dword ptr [esp + 0x28]
0044c1f2  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0044c1f8  01d0                     add eax, edx
0044c1fa  31d2                     xor edx, edx
0044c1fc  0fb76c2420               movzx ebp, word ptr [esp + 0x20]
0044c201  6689c2                   mov dx, ax
0044c204  89e8                     mov eax, ebp
0044c206  e846a60200               call 0x476851
0044c20b  30e4                     xor ah, ah
0044c20d  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0044c213  89442428                 mov dword ptr [esp + 0x28], eax
0044c217  8b542428                 mov edx, dword ptr [esp + 0x28]
0044c21b  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0044c221  31db                     xor ebx, ebx
0044c223  01d0                     add eax, edx
0044c225  31d2                     xor edx, edx
0044c227  8a19                     mov bl, byte ptr [ecx]
0044c229  6689c2                   mov dx, ax
0044c22c  89e8                     mov eax, ebp
0044c22e  e880aa0200               call 0x476cb3
0044c233  ba04000000               mov edx, 4
0044c238  31db                     xor ebx, ebx
0044c23a  31c0                     xor eax, eax
0044c23c  668b5c2420               mov bx, word ptr [esp + 0x20]
0044c241  8a01                     mov al, byte ptr [ecx]
0044c243  e840e10100               call 0x46a388
0044c248  31c0                     xor eax, eax
0044c24a  6689f8                   mov ax, di
0044c24d  89c1                     mov ecx, eax
0044c24f  c1e104                   shl ecx, 4
0044c252  01c1                     add ecx, eax
0044c254  c1e102                   shl ecx, 2
0044c257  01c1                     add ecx, eax
0044c259  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c25f  c1e102                   shl ecx, 2
0044c262  01ca                     add edx, ecx
0044c264  668b5e08                 mov bx, word ptr [esi + 8]
0044c268  66895a7e                 mov word ptr [edx + 0x7e], bx
0044c26c  663b3d04634900           cmp di, word ptr [0x496304]
0044c273  7522                     jne 0x44c297
0044c275  30ed                     xor ch, ch
0044c277  31db                     xor ebx, ebx
0044c279  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044c27f  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044c285  b9ffff0000               mov ecx, 0xffff
0044c28a  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044c290  66890d04634900           mov word ptr [0x496304], cx
0044c297  c6828800000000           mov byte ptr [edx + 0x88], 0
0044c29e  31d2                     xor edx, edx
0044c2a0  6689fa                   mov dx, di
0044c2a3  89d1                     mov ecx, edx
0044c2a5  c1e104                   shl ecx, 4
0044c2a8  01d1                     add ecx, edx
0044c2aa  b407                     mov ah, 7
0044c2ac  c1e102                   shl ecx, 2
0044c2af  88642450                 mov byte ptr [esp + 0x50], ah
0044c2b3  01d1                     add ecx, edx
0044c2b5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c2ba  c1e102                   shl ecx, 2
0044c2bd  01c1                     add ecx, eax
0044c2bf  31c0                     xor eax, eax
0044c2c1  8a4102                   mov al, byte ptr [ecx + 2]
0044c2c4  89fb                     mov ebx, edi
0044c2c6  85c0                     test eax, eax
0044c2c8  7409                     je 0x44c2d3
0044c2ca  83f804                   cmp eax, 4
0044c2cd  7404                     je 0x44c2d3
0044c2cf  b001                     mov al, 1
0044c2d1  eb02                     jmp 0x44c2d5
0044c2d3  30c0                     xor al, al
0044c2d5  84c0                     test al, al
0044c2d7  0f8467200000             je 0x44e344
0044c2dd  31c0                     xor eax, eax
0044c2df  6689d8                   mov ax, bx
0044c2e2  89c1                     mov ecx, eax
0044c2e4  c1e104                   shl ecx, 4
0044c2e7  01c1                     add ecx, eax
0044c2e9  c1e102                   shl ecx, 2
0044c2ec  01c1                     add ecx, eax
0044c2ee  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c2f3  8a542450                 mov dl, byte ptr [esp + 0x50]
0044c2f7  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044c2fb  663b1d04634900           cmp bx, word ptr [0x496304]
0044c302  0f853c200000             jne 0x44e344
0044c308  bfffff0000               mov edi, 0xffff
0044c30d  30d2                     xor dl, dl
0044c30f  31c9                     xor ecx, ecx
0044c311  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044c317  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044c31d  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044c323  66893d04634900           mov word ptr [0x496304], di
0044c32a  e915200000               jmp 0x44e344
0044c32f  c6868900000002           mov byte ptr [esi + 0x89], 2
0044c336  e909200000               jmp 0x44e344
0044c33b  bb01000000               mov ebx, 1
0044c340  31c9                     xor ecx, ecx
0044c342  31c0                     xor eax, eax
0044c344  31d2                     xor edx, edx
0044c346  6689f8                   mov ax, di
0044c349  668b5608                 mov dx, word ptr [esi + 8]
0044c34d  e81663ffff               call 0x442668
0044c352  84c0                     test al, al
0044c354  0f84ea1f0000             je 0x44e344
0044c35a  31c0                     xor eax, eax
0044c35c  668b4608                 mov ax, word ptr [esi + 8]
0044c360  e879910200               call 0x4754de
0044c365  31c0                     xor eax, eax
0044c367  6689f8                   mov ax, di
0044c36a  89c1                     mov ecx, eax
0044c36c  c1e104                   shl ecx, 4
0044c36f  01c1                     add ecx, eax
0044c371  c1e102                   shl ecx, 2
0044c374  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044c37a  01c1                     add ecx, eax
0044c37c  31d2                     xor edx, edx
0044c37e  668b448b08               mov ax, word ptr [ebx + ecx*4 + 8]
0044c383  6689c2                   mov dx, ax
0044c386  31c0                     xor eax, eax
0044c388  6689f8                   mov ax, di
0044c38b  e82469ffff               call 0x442cb4
0044c390  89f8                     mov eax, edi
0044c392  c6448b7201               mov byte ptr [ebx + ecx*4 + 0x72], 1
0044c397  25ffff0000               and eax, 0xffff
0044c39c  89c1                     mov ecx, eax
0044c39e  c1e104                   shl ecx, 4
0044c3a1  01c1                     add ecx, eax
0044c3a3  c1e102                   shl ecx, 2
0044c3a6  01c1                     add ecx, eax
0044c3a8  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c3ad  c1e102                   shl ecx, 2
0044c3b0  01c1                     add ecx, eax
0044c3b2  668b4108                 mov ax, word ptr [ecx + 8]
0044c3b6  8944240c                 mov dword ptr [esp + 0xc], eax
0044c3ba  31c0                     xor eax, eax
0044c3bc  8a01                     mov al, byte ptr [ecx]
0044c3be  3dc8000000               cmp eax, 0xc8
0044c3c3  7462                     je 0x44c427
0044c3c5  31c0                     xor eax, eax
0044c3c7  8a01                     mov al, byte ptr [ecx]
0044c3c9  83f804                   cmp eax, 4
0044c3cc  7459                     je 0x44c427
0044c3ce  31db                     xor ebx, ebx
0044c3d0  88c3                     mov bl, al
0044c3d2  30e4                     xor ah, ah
0044c3d4  30f6                     xor dh, dh
0044c3d6  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0044c3dc  8a91f5000000             mov dl, byte ptr [ecx + 0xf5]
0044c3e2  0502000000               add eax, 2
0044c3e7  01d0                     add eax, edx
0044c3e9  31d2                     xor edx, edx
0044c3eb  6689c2                   mov dx, ax
0044c3ee  31c0                     xor eax, eax
0044c3f0  668b44240c               mov ax, word ptr [esp + 0xc]
0044c3f5  e857a40200               call 0x476851
0044c3fa  30e4                     xor ah, ah
0044c3fc  8a81bb000000             mov al, byte ptr [ecx + 0xbb]
0044c402  89442428                 mov dword ptr [esp + 0x28], eax
0044c406  8b542428                 mov edx, dword ptr [esp + 0x28]
0044c40a  8a81f5000000             mov al, byte ptr [ecx + 0xf5]
0044c410  01d0                     add eax, edx
0044c412  31d2                     xor edx, edx
0044c414  31db                     xor ebx, ebx
0044c416  6689c2                   mov dx, ax
0044c419  31c0                     xor eax, eax
0044c41b  8a19                     mov bl, byte ptr [ecx]
0044c41d  668b44240c               mov ax, word ptr [esp + 0xc]
0044c422  e88ca80200               call 0x476cb3
0044c427  ba04000000               mov edx, 4
0044c42c  31db                     xor ebx, ebx
0044c42e  31c0                     xor eax, eax
0044c430  668b5c240c               mov bx, word ptr [esp + 0xc]
0044c435  8a01                     mov al, byte ptr [ecx]
0044c437  e84cdf0100               call 0x46a388
0044c43c  31c0                     xor eax, eax
0044c43e  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c444  85c0                     test eax, eax
0044c446  0f85c9000000             jne 0x44c515
0044c44c  b507                     mov ch, 7
0044c44e  6689f8                   mov ax, di
0044c451  886c2430                 mov byte ptr [esp + 0x30], ch
0044c455  89c1                     mov ecx, eax
0044c457  c1e104                   shl ecx, 4
0044c45a  01c1                     add ecx, eax
0044c45c  c1e102                   shl ecx, 2
0044c45f  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044c465  01c1                     add ecx, eax
0044c467  31c0                     xor eax, eax
0044c469  8a448b02                 mov al, byte ptr [ebx + ecx*4 + 2]
0044c46d  89fa                     mov edx, edi
0044c46f  85c0                     test eax, eax
0044c471  0f848f010000             je 0x44c606
0044c477  83f804                   cmp eax, 4
0044c47a  0f8486010000             je 0x44c606
0044c480  b001                     mov al, 1
0044c482  e981010000               jmp 0x44c608
0044c487  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c48e  668986c0000000           mov word ptr [esi + 0xc0], ax
0044c495  31c0                     xor eax, eax
0044c497  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c49e  e88476fdff               call 0x423b27
0044c4a3  89442424                 mov dword ptr [esp + 0x24], eax
0044c4a7  e977000000               jmp 0x44c523
0044c4ac  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c4b3  ba02000000               mov edx, 2
0044c4b8  0fb7e8                   movzx ebp, ax
0044c4bb  89442424                 mov dword ptr [esp + 0x24], eax
0044c4bf  89e8                     mov eax, ebp
0044c4c1  e89d920200               call 0x475763
0044c4c6  84c0                     test al, al
0044c4c8  7559                     jne 0x44c523
0044c4ca  b944000000               mov ecx, 0x44
0044c4cf  ba0a000000               mov edx, 0xa
0044c4d4  89e8                     mov eax, ebp
0044c4d6  89cb                     mov ebx, ecx
0044c4d8  e830b40200               call 0x47790d
0044c4dd  89442424                 mov dword ptr [esp + 0x24], eax
0044c4e1  25ffff0000               and eax, 0xffff
0044c4e6  3dffff0000               cmp eax, 0xffff
0044c4eb  751b                     jne 0x44c508
0044c4ed  ba0a000000               mov edx, 0xa
0044c4f2  31c0                     xor eax, eax
0044c4f4  31c9                     xor ecx, ecx
0044c4f6  31db                     xor ebx, ebx
0044c4f8  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c4ff  e809b40200               call 0x47790d
0044c504  89442424                 mov dword ptr [esp + 0x24], eax
0044c508  8b442424                 mov eax, dword ptr [esp + 0x24]
0044c50c  66898680000000           mov word ptr [esi + 0x80], ax
0044c513  eb0e                     jmp 0x44c523
0044c515  3c01                     cmp al, 1
0044c517  720a                     jb 0x44c523
0044c519  7691                     jbe 0x44c4ac
0044c51b  3c02                     cmp al, 2
0044c51d  0f8464ffffff             je 0x44c487
0044c523  31c0                     xor eax, eax
0044c525  668b442424               mov ax, word ptr [esp + 0x24]
0044c52a  3dffff0000               cmp eax, 0xffff
0044c52f  7453                     je 0x44c584
0044c531  31d2                     xor edx, edx
0044c533  6689fa                   mov dx, di
0044c536  89d1                     mov ecx, edx
0044c538  c1e104                   shl ecx, 4
0044c53b  01d1                     add ecx, edx
0044c53d  c1e102                   shl ecx, 2
0044c540  c6868900000003           mov byte ptr [esi + 0x89], 3
0044c547  01d1                     add ecx, edx
0044c549  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c54f  c1e102                   shl ecx, 2
0044c552  01ca                     add edx, ecx
0044c554  6689427e                 mov word ptr [edx + 0x7e], ax
0044c558  663b3d04634900           cmp di, word ptr [0x496304]
0044c55f  0f854f030000             jne 0x44c8b4
0044c565  30db                     xor bl, bl
0044c567  31c0                     xor eax, eax
0044c569  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044c56f  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044c575  bbffff0000               mov ebx, 0xffff
0044c57a  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044c57f  e9a00c0000               jmp 0x44d224
0044c584  31c0                     xor eax, eax
0044c586  6689f8                   mov ax, di
0044c589  89c1                     mov ecx, eax
0044c58b  c1e104                   shl ecx, 4
0044c58e  01c1                     add ecx, eax
0044c590  c1e102                   shl ecx, 2
0044c593  01c1                     add ecx, eax
0044c595  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c59a  c1e102                   shl ecx, 2
0044c59d  01c1                     add ecx, eax
0044c59f  31c0                     xor eax, eax
0044c5a1  b307                     mov bl, 7
0044c5a3  8a4102                   mov al, byte ptr [ecx + 2]
0044c5a6  89fa                     mov edx, edi
0044c5a8  85c0                     test eax, eax
0044c5aa  7409                     je 0x44c5b5
0044c5ac  83f804                   cmp eax, 4
0044c5af  7404                     je 0x44c5b5
0044c5b1  b001                     mov al, 1
0044c5b3  eb02                     jmp 0x44c5b7
0044c5b5  30c0                     xor al, al
0044c5b7  84c0                     test al, al
0044c5b9  0f84851d0000             je 0x44e344
0044c5bf  31c0                     xor eax, eax
0044c5c1  6689d0                   mov ax, dx
0044c5c4  89c1                     mov ecx, eax
0044c5c6  c1e104                   shl ecx, 4
0044c5c9  01c1                     add ecx, eax
0044c5cb  c1e102                   shl ecx, 2
0044c5ce  01c1                     add ecx, eax
0044c5d0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c5d5  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044c5d9  663b1504634900           cmp dx, word ptr [0x496304]
0044c5e0  0f855e1d0000             jne 0x44e344
0044c5e6  bfffff0000               mov edi, 0xffff
0044c5eb  30d2                     xor dl, dl
0044c5ed  31ed                     xor ebp, ebp
0044c5ef  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044c5f5  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044c5fb  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044c601  e91dfdffff               jmp 0x44c323
0044c606  30c0                     xor al, al
0044c608  84c0                     test al, al
0044c60a  0f84341d0000             je 0x44e344
0044c610  31c0                     xor eax, eax
0044c612  6689d0                   mov ax, dx
0044c615  89c1                     mov ecx, eax
0044c617  c1e104                   shl ecx, 4
0044c61a  01c1                     add ecx, eax
0044c61c  c1e102                   shl ecx, 2
0044c61f  01c1                     add ecx, eax
0044c621  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044c626  8a5c2430                 mov bl, byte ptr [esp + 0x30]
0044c62a  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044c62e  663b1504634900           cmp dx, word ptr [0x496304]
0044c635  0f85091d0000             jne 0x44e344
0044c63b  b9ffff0000               mov ecx, 0xffff
0044c640  30c0                     xor al, al
0044c642  31ff                     xor edi, edi
0044c644  a2360f4e00               mov byte ptr [0x4e0f36], al
0044c649  a2370f4e00               mov byte ptr [0x4e0f37], al
0044c64e  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044c654  66890d04634900           mov word ptr [0x496304], cx
0044c65b  e9e41c0000               jmp 0x44e344
0044c660  31c0                     xor eax, eax
0044c662  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c668  83f802                   cmp eax, 2
0044c66b  0f85a7000000             jne 0x44c718
0044c671  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044c677  c1f818                   sar eax, 0x18
0044c67a  85c0                     test eax, eax
0044c67c  7523                     jne 0x44c6a1
0044c67e  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044c684  c1f818                   sar eax, 0x18
0044c687  85c0                     test eax, eax
0044c689  7516                     jne 0x44c6a1
0044c68b  31d2                     xor edx, edx
0044c68d  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044c694  668b5608                 mov dx, word ptr [esi + 8]
0044c698  e88271fdff               call 0x42381f
0044c69d  84c0                     test al, al
0044c69f  756b                     jne 0x44c70c
0044c6a1  668b4608                 mov ax, word ptr [esi + 8]
0044c6a5  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044c6a9  0f8562f6ffff             jne 0x44bd11
0044c6af  31c0                     xor eax, eax
0044c6b1  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c6b8  e825e8fcff               call 0x41aee2
0044c6bd  89c3                     mov ebx, eax
0044c6bf  31c0                     xor eax, eax
0044c6c1  6689f8                   mov ax, di
0044c6c4  89c1                     mov ecx, eax
0044c6c6  c1e104                   shl ecx, 4
0044c6c9  01c1                     add ecx, eax
0044c6cb  c1e102                   shl ecx, 2
0044c6ce  01c1                     add ecx, eax
0044c6d0  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c6d6  c1e102                   shl ecx, 2
0044c6d9  01ca                     add edx, ecx
0044c6db  66895a7e                 mov word ptr [edx + 0x7e], bx
0044c6df  663b3d04634900           cmp di, word ptr [0x496304]
0044c6e6  0f85c8010000             jne 0x44c8b4
0044c6ec  b9ffff0000               mov ecx, 0xffff
0044c6f1  30ff                     xor bh, bh
0044c6f3  31f6                     xor esi, esi
0044c6f5  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044c6fb  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044c701  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044c707  e9a1010000               jmp 0x44c8ad
0044c70c  c6868900000004           mov byte ptr [esi + 0x89], 4
0044c713  e95dfaffff               jmp 0x44c175
0044c718  31c0                     xor eax, eax
0044c71a  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c720  83f801                   cmp eax, 1
0044c723  0f851b1c0000             jne 0x44e344
0044c729  668b4608                 mov ax, word ptr [esi + 8]
0044c72d  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044c731  0f85daf5ffff             jne 0x44bd11
0044c737  31d2                     xor edx, edx
0044c739  668b9680000000           mov dx, word ptr [esi + 0x80]
0044c740  89d0                     mov eax, edx
0044c742  c1fa1f                   sar edx, 0x1f
0044c745  c1e208                   shl edx, 8
0044c748  1bc2                     sbb eax, edx
0044c74a  c1f808                   sar eax, 8
0044c74d  bb00010000               mov ebx, 0x100
0044c752  31d2                     xor edx, edx
0044c754  31c9                     xor ecx, ecx
0044c756  668b9680000000           mov dx, word ptr [esi + 0x80]
0044c75d  6689c1                   mov cx, ax
0044c760  89d0                     mov eax, edx
0044c762  c1fa1f                   sar edx, 0x1f
0044c765  f7fb                     idiv ebx
0044c767  31db                     xor ebx, ebx
0044c769  6689d3                   mov bx, dx
0044c76c  31d2                     xor edx, edx
0044c76e  668b5608                 mov dx, word ptr [esi + 8]
0044c772  89d0                     mov eax, edx
0044c774  c1fa1f                   sar edx, 0x1f
0044c777  c1e208                   shl edx, 8
0044c77a  1bc2                     sbb eax, edx
0044c77c  c1f808                   sar eax, 8
0044c77f  0fb7e8                   movzx ebp, ax
0044c782  31d2                     xor edx, edx
0044c784  b800010000               mov eax, 0x100
0044c789  668b5608                 mov dx, word ptr [esi + 8]
0044c78d  89442404                 mov dword ptr [esp + 4], eax
0044c791  89d0                     mov eax, edx
0044c793  c1fa1f                   sar edx, 0x1f
0044c796  f77c2404                 idiv dword ptr [esp + 4]
0044c79a  31c0                     xor eax, eax
0044c79c  6689d0                   mov ax, dx
0044c79f  89ea                     mov edx, ebp
0044c7a1  e8afcd0200               call 0x479555
0044c7a6  83f810                   cmp eax, 0x10
0044c7a9  0f83b3000000             jae 0x44c862
0044c7af  8a8684000000             mov al, byte ptr [esi + 0x84]
0044c7b5  31d2                     xor edx, edx
0044c7b7  0442                     add al, 0x42
0044c7b9  88c2                     mov dl, al
0044c7bb  31c0                     xor eax, eax
0044c7bd  668b4608                 mov ax, word ptr [esi + 8]
0044c7c1  e89d8f0200               call 0x475763
0044c7c6  84c0                     test al, al
0044c7c8  741e                     je 0x44c7e8
0044c7ca  c6868900000004           mov byte ptr [esi + 0x89], 4
0044c7d1  668b4608                 mov ax, word ptr [esi + 8]
0044c7d5  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044c7dc  66898680000000           mov word ptr [esi + 0x80], ax
0044c7e3  e95c1b0000               jmp 0x44e344
0044c7e8  8a8684000000             mov al, byte ptr [esi + 0x84]
0044c7ee  31d2                     xor edx, edx
0044c7f0  0442                     add al, 0x42
0044c7f2  88c2                     mov dl, al
0044c7f4  31c0                     xor eax, eax
0044c7f6  668b8680000000           mov ax, word ptr [esi + 0x80]
0044c7fd  e8ad8f0200               call 0x4757af
0044c802  31d2                     xor edx, edx
0044c804  6689c2                   mov dx, ax
0044c807  81faffff0000             cmp edx, 0xffff
0044c80d  0f84311b0000             je 0x44e344
0044c813  89c3                     mov ebx, eax
0044c815  31c0                     xor eax, eax
0044c817  6689f8                   mov ax, di
0044c81a  89c1                     mov ecx, eax
0044c81c  c1e104                   shl ecx, 4
0044c81f  01c1                     add ecx, eax
0044c821  c1e102                   shl ecx, 2
0044c824  01c1                     add ecx, eax
0044c826  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c82c  c1e102                   shl ecx, 2
0044c82f  01ca                     add edx, ecx
0044c831  66895a7e                 mov word ptr [edx + 0x7e], bx
0044c835  663b3d04634900           cmp di, word ptr [0x496304]
0044c83c  7576                     jne 0x44c8b4
0044c83e  bfffff0000               mov edi, 0xffff
0044c843  30e4                     xor ah, ah
0044c845  31c9                     xor ecx, ecx
0044c847  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044c84d  8825370f4e00             mov byte ptr [0x4e0f37], ah
0044c853  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044c859  66893d04634900           mov word ptr [0x496304], di
0044c860  eb52                     jmp 0x44c8b4
0044c862  31c0                     xor eax, eax
0044c864  6689f8                   mov ax, di
0044c867  89c1                     mov ecx, eax
0044c869  c1e104                   shl ecx, 4
0044c86c  01c1                     add ecx, eax
0044c86e  c1e102                   shl ecx, 2
0044c871  01c1                     add ecx, eax
0044c873  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044c879  c1e102                   shl ecx, 2
0044c87c  01ca                     add edx, ecx
0044c87e  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044c885  66895a7e                 mov word ptr [edx + 0x7e], bx
0044c889  663b3d04634900           cmp di, word ptr [0x496304]
0044c890  7522                     jne 0x44c8b4
0044c892  30ed                     xor ch, ch
0044c894  31db                     xor ebx, ebx
0044c896  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044c89c  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044c8a2  b9ffff0000               mov ecx, 0xffff
0044c8a7  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044c8ad  66890d04634900           mov word ptr [0x496304], cx
0044c8b4  c6828800000000           mov byte ptr [edx + 0x88], 0
0044c8bb  e9841a0000               jmp 0x44e344
0044c8c0  31c0                     xor eax, eax
0044c8c2  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c8c8  83f802                   cmp eax, 2
0044c8cb  0f858e000000             jne 0x44c95f
0044c8d1  8a8e8b000000             mov cl, byte ptr [esi + 0x8b]
0044c8d7  31c0                     xor eax, eax
0044c8d9  fec9                     dec cl
0044c8db  88c8                     mov al, cl
0044c8dd  888e8b000000             mov byte ptr [esi + 0x8b], cl
0044c8e3  85c0                     test eax, eax
0044c8e5  0f85591a0000             jne 0x44e344
0044c8eb  bb02000000               mov ebx, 2
0044c8f0  8d460a                   lea eax, [esi + 0xa]
0044c8f3  89da                     mov edx, ebx
0044c8f5  e8bea8ffff               call 0x4471b8
0044c8fa  6685c0                   test ax, ax
0044c8fd  7454                     je 0x44c953
0044c8ff  bb02000000               mov ebx, 2
0044c904  8d460a                   lea eax, [esi + 0xa]
0044c907  89da                     mov edx, ebx
0044c909  31c9                     xor ecx, ecx
0044c90b  e8daa9ffff               call 0x4472ea
0044c910  ba01000000               mov edx, 1
0044c915  b802000000               mov eax, 2
0044c91a  31db                     xor ebx, ebx
0044c91c  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044c923  8a1e                     mov bl, byte ptr [esi]
0044c925  e8e56afdff               call 0x42340f
0044c92a  31d2                     xor edx, edx
0044c92c  8a5601                   mov dl, byte ptr [esi + 1]
0044c92f  89d1                     mov ecx, edx
0044c931  c1e102                   shl ecx, 2
0044c934  29d1                     sub ecx, edx
0044c936  c1e103                   shl ecx, 3
0044c939  01d1                     add ecx, edx
0044c93b  31d2                     xor edx, edx
0044c93d  668b144dde654900         mov dx, word ptr [ecx*2 + 0x4965de]
0044c945  89d0                     mov eax, edx
0044c947  c1fa1f                   sar edx, 0x1f
0044c94a  2bc2                     sub eax, edx
0044c94c  d1f8                     sar eax, 1
0044c94e  e9f60b0000               jmp 0x44d549
0044c953  c6868900000005           mov byte ptr [esi + 0x89], 5
0044c95a  e9e5190000               jmp 0x44e344
0044c95f  31c0                     xor eax, eax
0044c961  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c967  83f801                   cmp eax, 1
0044c96a  0f85d4190000             jne 0x44e344
0044c970  8abe8b000000             mov bh, byte ptr [esi + 0x8b]
0044c976  31c0                     xor eax, eax
0044c978  fecf                     dec bh
0044c97a  88f8                     mov al, bh
0044c97c  88be8b000000             mov byte ptr [esi + 0x8b], bh
0044c982  85c0                     test eax, eax
0044c984  0f85ba190000             jne 0x44e344
0044c98a  bb02000000               mov ebx, 2
0044c98f  8d460a                   lea eax, [esi + 0xa]
0044c992  89da                     mov edx, ebx
0044c994  e81fa8ffff               call 0x4471b8
0044c999  6685c0                   test ax, ax
0044c99c  74b5                     je 0x44c953
0044c99e  bb02000000               mov ebx, 2
0044c9a3  31c0                     xor eax, eax
0044c9a5  89da                     mov edx, ebx
0044c9a7  6689f8                   mov ax, di
0044c9aa  e8296fffff               call 0x4438d8
0044c9af  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044c9b6  e989190000               jmp 0x44e344
0044c9bb  31c0                     xor eax, eax
0044c9bd  8a8682000000             mov al, byte ptr [esi + 0x82]
0044c9c3  83f802                   cmp eax, 2
0044c9c6  0f853d010000             jne 0x44cb09
0044c9cc  bb01000000               mov ebx, 1
0044c9d1  31c9                     xor ecx, ecx
0044c9d3  31c0                     xor eax, eax
0044c9d5  31d2                     xor edx, edx
0044c9d7  6689f8                   mov ax, di
0044c9da  668b5608                 mov dx, word ptr [esi + 8]
0044c9de  e8855cffff               call 0x442668
0044c9e3  84c0                     test al, al
0044c9e5  0f8459190000             je 0x44e344
0044c9eb  31c0                     xor eax, eax
0044c9ed  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044c9f4  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
0044c9fd  3dffff0000               cmp eax, 0xffff
0044ca02  7476                     je 0x44ca7a
0044ca04  31c0                     xor eax, eax
0044ca06  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044ca0d  e83a8a0200               call 0x47544c
0044ca12  25ffff0000               and eax, 0xffff
0044ca17  e8258b0200               call 0x475541
0044ca1c  25ffff0000               and eax, 0xffff
0044ca21  85c0                     test eax, eax
0044ca23  7e55                     jle 0x44ca7a
0044ca25  31d2                     xor edx, edx
0044ca27  6689fa                   mov dx, di
0044ca2a  89d1                     mov ecx, edx
0044ca2c  c1e104                   shl ecx, 4
0044ca2f  01d1                     add ecx, edx
0044ca31  c1e102                   shl ecx, 2
0044ca34  c6868900000000           mov byte ptr [esi + 0x89], 0
0044ca3b  01d1                     add ecx, edx
0044ca3d  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ca43  c1e102                   shl ecx, 2
0044ca46  01ca                     add edx, ecx
0044ca48  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044ca4f  6689427e                 mov word ptr [edx + 0x7e], ax
0044ca53  663b3d04634900           cmp di, word ptr [0x496304]
0044ca5a  0f8554feffff             jne 0x44c8b4
0044ca60  b9ffff0000               mov ecx, 0xffff
0044ca65  30e4                     xor ah, ah
0044ca67  31ed                     xor ebp, ebp
0044ca69  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044ca6f  8825370f4e00             mov byte ptr [0x4e0f37], ah
0044ca75  e9b9f4ffff               jmp 0x44bf33
0044ca7a  31d2                     xor edx, edx
0044ca7c  b107                     mov cl, 7
0044ca7e  6689fa                   mov dx, di
0044ca81  884c244c                 mov byte ptr [esp + 0x4c], cl
0044ca85  89d1                     mov ecx, edx
0044ca87  c1e104                   shl ecx, 4
0044ca8a  01d1                     add ecx, edx
0044ca8c  c1e102                   shl ecx, 2
0044ca8f  01d1                     add ecx, edx
0044ca91  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044ca96  c1e102                   shl ecx, 2
0044ca99  01c1                     add ecx, eax
0044ca9b  31c0                     xor eax, eax
0044ca9d  8a4102                   mov al, byte ptr [ecx + 2]
0044caa0  89fb                     mov ebx, edi
0044caa2  85c0                     test eax, eax
0044caa4  7409                     je 0x44caaf
0044caa6  83f804                   cmp eax, 4
0044caa9  7404                     je 0x44caaf
0044caab  b001                     mov al, 1
0044caad  eb02                     jmp 0x44cab1
0044caaf  30c0                     xor al, al
0044cab1  84c0                     test al, al
0044cab3  7448                     je 0x44cafd
0044cab5  31c0                     xor eax, eax
0044cab7  6689d8                   mov ax, bx
0044caba  89c1                     mov ecx, eax
0044cabc  c1e104                   shl ecx, 4
0044cabf  01c1                     add ecx, eax
0044cac1  c1e102                   shl ecx, 2
0044cac4  01c1                     add ecx, eax
0044cac6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cacb  8a54244c                 mov dl, byte ptr [esp + 0x4c]
0044cacf  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044cad3  663b1d04634900           cmp bx, word ptr [0x496304]
0044cada  7521                     jne 0x44cafd
0044cadc  b8ffff0000               mov eax, 0xffff
0044cae1  30ed                     xor ch, ch
0044cae3  31ff                     xor edi, edi
0044cae5  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044caeb  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044caf1  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044caf7  66a304634900             mov word ptr [0x496304], ax
0044cafd  c6868200000000           mov byte ptr [esi + 0x82], 0
0044cb04  e93b180000               jmp 0x44e344
0044cb09  31c0                     xor eax, eax
0044cb0b  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044cb12  3dffff0000               cmp eax, 0xffff
0044cb17  7464                     je 0x44cb7d
0044cb19  31d2                     xor edx, edx
0044cb1b  6689fa                   mov dx, di
0044cb1e  89d1                     mov ecx, edx
0044cb20  c1e104                   shl ecx, 4
0044cb23  01d1                     add ecx, edx
0044cb25  c1e102                   shl ecx, 2
0044cb28  c6868900000000           mov byte ptr [esi + 0x89], 0
0044cb2f  01d1                     add ecx, edx
0044cb31  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cb36  c1e102                   shl ecx, 2
0044cb39  01c8                     add eax, ecx
0044cb3b  668b9eb2000000           mov bx, word ptr [esi + 0xb2]
0044cb42  6689587e                 mov word ptr [eax + 0x7e], bx
0044cb46  663b3d04634900           cmp di, word ptr [0x496304]
0044cb4d  7522                     jne 0x44cb71
0044cb4f  b9ffff0000               mov ecx, 0xffff
0044cb54  30d2                     xor dl, dl
0044cb56  31f6                     xor esi, esi
0044cb58  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044cb5e  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044cb64  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044cb6a  66890d04634900           mov word ptr [0x496304], cx
0044cb71  c6808800000000           mov byte ptr [eax + 0x88], 0
0044cb78  e9c7170000               jmp 0x44e344
0044cb7d  89fa                     mov edx, edi
0044cb7f  31c0                     xor eax, eax
0044cb81  6689d0                   mov ax, dx
0044cb84  89c1                     mov ecx, eax
0044cb86  c1e104                   shl ecx, 4
0044cb89  01c1                     add ecx, eax
0044cb8b  c1e102                   shl ecx, 2
0044cb8e  01c1                     add ecx, eax
0044cb90  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cb95  b307                     mov bl, 7
0044cb97  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044cb9b  25ff000000               and eax, 0xff
0044cba0  7428                     je 0x44cbca
0044cba2  31c0                     xor eax, eax
0044cba4  6689d0                   mov ax, dx
0044cba7  89c1                     mov ecx, eax
0044cba9  c1e104                   shl ecx, 4
0044cbac  01c1                     add ecx, eax
0044cbae  c1e102                   shl ecx, 2
0044cbb1  01c1                     add ecx, eax
0044cbb3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cbb8  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044cbbc  25ff000000               and eax, 0xff
0044cbc1  83f804                   cmp eax, 4
0044cbc4  7404                     je 0x44cbca
0044cbc6  b001                     mov al, 1
0044cbc8  eb02                     jmp 0x44cbcc
0044cbca  30c0                     xor al, al
0044cbcc  84c0                     test al, al
0044cbce  0f8429ffffff             je 0x44cafd
0044cbd4  31d2                     xor edx, edx
0044cbd6  6689fa                   mov dx, di
0044cbd9  89d1                     mov ecx, edx
0044cbdb  c1e104                   shl ecx, 4
0044cbde  01d1                     add ecx, edx
0044cbe0  c1e102                   shl ecx, 2
0044cbe3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cbe8  01d1                     add ecx, edx
0044cbea  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044cbee  663b3d04634900           cmp di, word ptr [0x496304]
0044cbf5  0f8502ffffff             jne 0x44cafd
0044cbfb  30ed                     xor ch, ch
0044cbfd  baffff0000               mov edx, 0xffff
0044cc02  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044cc08  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044cc0e  31c9                     xor ecx, ecx
0044cc10  66891504634900           mov word ptr [0x496304], dx
0044cc17  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044cc1d  e9dbfeffff               jmp 0x44cafd
0044cc22  8a8689000000             mov al, byte ptr [esi + 0x89]
0044cc28  3c05                     cmp al, 5
0044cc2a  0f8714170000             ja 0x44e344
0044cc30  25ff000000               and eax, 0xff
0044cc35  2eff248538bc4400         jmp dword ptr cs:[eax*4 + 0x44bc38]
0044cc3d  31c0                     xor eax, eax
0044cc3f  6689f8                   mov ax, di
0044cc42  e8c5c6ffff               call 0x44930c
0044cc47  31c0                     xor eax, eax
0044cc49  668b4608                 mov ax, word ptr [esi + 8]
0044cc4d  e8bd940200               call 0x47610f
0044cc52  84c0                     test al, al
0044cc54  0f84ea160000             je 0x44e344
0044cc5a  31c0                     xor eax, eax
0044cc5c  8d4e0a                   lea ecx, [esi + 0xa]
0044cc5f  668b4608                 mov ax, word ptr [esi + 8]
0044cc63  b302                     mov bl, 2
0044cc65  e8f8990200               call 0x476662
0044cc6a  668b5166                 mov dx, word ptr [ecx + 0x66]
0044cc6e  b001                     mov al, 1
0044cc70  42                       inc edx
0044cc71  31f6                     xor esi, esi
0044cc73  66895166                 mov word ptr [ecx + 0x66], dx
0044cc77  84c0                     test al, al
0044cc79  7419                     je 0x44cc94
0044cc7b  668b11                   mov dx, word ptr [ecx]
0044cc7e  31c0                     xor eax, eax
0044cc80  6689d0                   mov ax, dx
0044cc83  885c0142                 mov byte ptr [ecx + eax + 0x42], bl
0044cc87  31c0                     xor eax, eax
0044cc89  6689d0                   mov ax, dx
0044cc8c  6689744106               mov word ptr [ecx + eax*2 + 6], si
0044cc91  66ff01                   inc word ptr [ecx]
0044cc94  c644245407               mov byte ptr [esp + 0x54], 7
0044cc99  31d2                     xor edx, edx
0044cc9b  6689fa                   mov dx, di
0044cc9e  89d1                     mov ecx, edx
0044cca0  c1e104                   shl ecx, 4
0044cca3  01d1                     add ecx, edx
0044cca5  c1e102                   shl ecx, 2
0044cca8  01d1                     add ecx, edx
0044ccaa  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044ccaf  c1e102                   shl ecx, 2
0044ccb2  01c1                     add ecx, eax
0044ccb4  31c0                     xor eax, eax
0044ccb6  8a4102                   mov al, byte ptr [ecx + 2]
0044ccb9  89fb                     mov ebx, edi
0044ccbb  85c0                     test eax, eax
0044ccbd  7409                     je 0x44ccc8
0044ccbf  83f804                   cmp eax, 4
0044ccc2  7404                     je 0x44ccc8
0044ccc4  b001                     mov al, 1
0044ccc6  eb02                     jmp 0x44ccca
0044ccc8  30c0                     xor al, al
0044ccca  84c0                     test al, al
0044cccc  0f8472160000             je 0x44e344
0044ccd2  31c0                     xor eax, eax
0044ccd4  6689d8                   mov ax, bx
0044ccd7  89c1                     mov ecx, eax
0044ccd9  c1e104                   shl ecx, 4
0044ccdc  01c1                     add ecx, eax
0044ccde  c1e102                   shl ecx, 2
0044cce1  01c1                     add ecx, eax
0044cce3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cce8  8a542454                 mov dl, byte ptr [esp + 0x54]
0044ccec  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044ccf0  668b0d04634900           mov cx, word ptr [0x496304]
0044ccf7  6639cb                   cmp bx, cx
0044ccfa  0f8544160000             jne 0x44e344
0044cd00  beffff0000               mov esi, 0xffff
0044cd05  30f6                     xor dh, dh
0044cd07  30cb                     xor bl, cl
0044cd09  31ed                     xor ebp, ebp
0044cd0b  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044cd11  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044cd17  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044cd1d  e9b5f3ffff               jmp 0x44c0d7
0044cd22  31c0                     xor eax, eax
0044cd24  6689f8                   mov ax, di
0044cd27  e8e0c5ffff               call 0x44930c
0044cd2c  668b467e                 mov ax, word ptr [esi + 0x7e]
0044cd30  663b4608                 cmp ax, word ptr [esi + 8]
0044cd34  0f850a160000             jne 0x44e344
0044cd3a  89fa                     mov edx, edi
0044cd3c  31c0                     xor eax, eax
0044cd3e  6689d0                   mov ax, dx
0044cd41  89c1                     mov ecx, eax
0044cd43  c1e104                   shl ecx, 4
0044cd46  01c1                     add ecx, eax
0044cd48  c1e102                   shl ecx, 2
0044cd4b  01c1                     add ecx, eax
0044cd4d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cd52  b307                     mov bl, 7
0044cd54  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044cd58  25ff000000               and eax, 0xff
0044cd5d  7428                     je 0x44cd87
0044cd5f  31c0                     xor eax, eax
0044cd61  6689d0                   mov ax, dx
0044cd64  89c1                     mov ecx, eax
0044cd66  c1e104                   shl ecx, 4
0044cd69  01c1                     add ecx, eax
0044cd6b  c1e102                   shl ecx, 2
0044cd6e  01c1                     add ecx, eax
0044cd70  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cd75  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044cd79  25ff000000               and eax, 0xff
0044cd7e  83f804                   cmp eax, 4
0044cd81  7404                     je 0x44cd87
0044cd83  b001                     mov al, 1
0044cd85  eb02                     jmp 0x44cd89
0044cd87  30c0                     xor al, al
0044cd89  84c0                     test al, al
0044cd8b  7443                     je 0x44cdd0
0044cd8d  31d2                     xor edx, edx
0044cd8f  6689fa                   mov dx, di
0044cd92  89d1                     mov ecx, edx
0044cd94  c1e104                   shl ecx, 4
0044cd97  01d1                     add ecx, edx
0044cd99  c1e102                   shl ecx, 2
0044cd9c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cda1  01d1                     add ecx, edx
0044cda3  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044cda7  663b3d04634900           cmp di, word ptr [0x496304]
0044cdae  7520                     jne 0x44cdd0
0044cdb0  baffff0000               mov edx, 0xffff
0044cdb5  30c0                     xor al, al
0044cdb7  31ff                     xor edi, edi
0044cdb9  a2360f4e00               mov byte ptr [0x4e0f36], al
0044cdbe  a2370f4e00               mov byte ptr [0x4e0f37], al
0044cdc3  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044cdc9  66891504634900           mov word ptr [0x496304], dx
0044cdd0  66c746040000             mov word ptr [esi + 4], 0
0044cdd6  66c786b2000000ffff       mov word ptr [esi + 0xb2], 0xffff
0044cddf  e960150000               jmp 0x44e344
0044cde4  8a8689000000             mov al, byte ptr [esi + 0x89]
0044cdea  3c01                     cmp al, 1
0044cdec  0f8252150000             jb 0x44e344
0044cdf2  0f8645feffff             jbe 0x44cc3d
0044cdf8  3c02                     cmp al, 2
0044cdfa  0f8422ffffff             je 0x44cd22
0044ce00  e93f150000               jmp 0x44e344
0044ce05  668b467e                 mov ax, word ptr [esi + 0x7e]
0044ce09  668b4e08                 mov cx, word ptr [esi + 8]
0044ce0d  6639c8                   cmp ax, cx
0044ce10  0f85fbeeffff             jne 0x44bd11
0044ce16  31c0                     xor eax, eax
0044ce18  6689c8                   mov ax, cx
0044ce1b  e899940200               call 0x4762b9
0044ce20  84c0                     test al, al
0044ce22  742a                     je 0x44ce4e
0044ce24  31d2                     xor edx, edx
0044ce26  8a5601                   mov dl, byte ptr [esi + 1]
0044ce29  89d1                     mov ecx, edx
0044ce2b  31db                     xor ebx, ebx
0044ce2d  c1e102                   shl ecx, 2
0044ce30  31c0                     xor eax, eax
0044ce32  29d1                     sub ecx, edx
0044ce34  8a06                     mov al, byte ptr [esi]
0044ce36  c1e103                   shl ecx, 3
0044ce39  88d3                     mov bl, dl
0044ce3b  01d1                     add ecx, edx
0044ce3d  ba03000000               mov edx, 3
0044ce42  c6868900000001           mov byte ptr [esi + 0x89], 1
0044ce49  e9a90a0000               jmp 0x44d8f7
0044ce4e  ba05000000               mov edx, 5
0044ce53  31db                     xor ebx, ebx
0044ce55  31c0                     xor eax, eax
0044ce57  6689fb                   mov bx, di
0044ce5a  668b4608                 mov ax, word ptr [esi + 8]
0044ce5e  e84ab00200               call 0x477ead
0044ce63  31d2                     xor edx, edx
0044ce65  6689c2                   mov dx, ax
0044ce68  81faffff0000             cmp edx, 0xffff
0044ce6e  745e                     je 0x44cece
0044ce70  31d2                     xor edx, edx
0044ce72  6689fa                   mov dx, di
0044ce75  89d1                     mov ecx, edx
0044ce77  c1e104                   shl ecx, 4
0044ce7a  01d1                     add ecx, edx
0044ce7c  c1e102                   shl ecx, 2
0044ce7f  01d1                     add ecx, edx
0044ce81  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ce87  c1e102                   shl ecx, 2
0044ce8a  01ca                     add edx, ecx
0044ce8c  6689427e                 mov word ptr [edx + 0x7e], ax
0044ce90  663b3d04634900           cmp di, word ptr [0x496304]
0044ce97  7522                     jne 0x44cebb
0044ce99  30ff                     xor bh, bh
0044ce9b  b9ffff0000               mov ecx, 0xffff
0044cea0  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044cea6  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044ceac  31db                     xor ebx, ebx
0044ceae  66890d04634900           mov word ptr [0x496304], cx
0044ceb5  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044cebb  c6828800000000           mov byte ptr [edx + 0x88], 0
0044cec2  668986b2000000           mov word ptr [esi + 0xb2], ax
0044cec9  e976140000               jmp 0x44e344
0044cece  89f8                     mov eax, edi
0044ced0  31d2                     xor edx, edx
0044ced2  6689c2                   mov dx, ax
0044ced5  89d1                     mov ecx, edx
0044ced7  c1e104                   shl ecx, 4
0044ceda  01d1                     add ecx, edx
0044cedc  c1e102                   shl ecx, 2
0044cedf  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cee4  01d1                     add ecx, edx
0044cee6  8a0488                   mov al, byte ptr [eax + ecx*4]
0044cee9  3a0541805000             cmp al, byte ptr [0x508041]
0044ceef  0f858f000000             jne 0x44cf84
0044cef5  31d2                     xor edx, edx
0044cef7  6689fa                   mov dx, di
0044cefa  89d0                     mov eax, edx
0044cefc  c1e004                   shl eax, 4
0044ceff  01d0                     add eax, edx
0044cf01  be10000000               mov esi, 0x10
0044cf06  c1e002                   shl eax, 2
0044cf09  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
0044cf0f  01d0                     add eax, edx
0044cf11  c1e002                   shl eax, 2
0044cf14  31d2                     xor edx, edx
0044cf16  01c1                     add ecx, eax
0044cf18  31c0                     xor eax, eax
0044cf1a  8a1541805000             mov dl, byte ptr [0x508041]
0044cf20  668b4108                 mov ax, word ptr [ecx + 8]
0044cf24  30db                     xor bl, bl
0044cf26  e8c5970200               call 0x4766f0
0044cf2b  84c0                     test al, al
0044cf2d  7455                     je 0x44cf84
0044cf2f  31c0                     xor eax, eax
0044cf31  31d2                     xor edx, edx
0044cf33  6689f8                   mov ax, di
0044cf36  6689f2                   mov dx, si
0044cf39  e81f3dffff               call 0x440c5d
0044cf3e  83fa10                   cmp edx, 0x10
0044cf41  7505                     jne 0x44cf48
0044cf43  b800010000               mov eax, 0x100
0044cf48  8ba904010000             mov ebp, dword ptr [ecx + 0x104]
0044cf4e  8899f9000000             mov byte ptr [ecx + 0xf9], bl
0044cf54  83fdff                   cmp ebp, -1
0044cf57  752b                     jne 0x44cf84
0044cf59  50                       push eax
0044cf5a  31d2                     xor edx, edx
0044cf5c  31c0                     xor eax, eax
0044cf5e  8a5101                   mov dl, byte ptr [ecx + 1]
0044cf61  88d8                     mov al, bl
0044cf63  8d9904010000             lea ebx, [ecx + 0x104]
0044cf69  89d1                     mov ecx, edx
0044cf6b  31d2                     xor edx, edx
0044cf6d  6689f2                   mov dx, si
0044cf70  c1e110                   shl ecx, 0x10
0044cf73  c1e208                   shl edx, 8
0044cf76  09ca                     or edx, ecx
0044cf78  89c1                     mov ecx, eax
0044cf7a  b850000000               mov eax, 0x50
0044cf7f  e8f5da0300               call 0x48aa79
0044cf84  31c0                     xor eax, eax
0044cf86  6689f8                   mov ax, di
0044cf89  89c1                     mov ecx, eax
0044cf8b  c1e104                   shl ecx, 4
0044cf8e  b207                     mov dl, 7
0044cf90  01c1                     add ecx, eax
0044cf92  88542448                 mov byte ptr [esp + 0x48], dl
0044cf96  c1e102                   shl ecx, 2
0044cf99  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044cf9f  01c1                     add ecx, eax
0044cfa1  31c0                     xor eax, eax
0044cfa3  8a448a02                 mov al, byte ptr [edx + ecx*4 + 2]
0044cfa7  89fb                     mov ebx, edi
0044cfa9  85c0                     test eax, eax
0044cfab  7409                     je 0x44cfb6
0044cfad  83f804                   cmp eax, 4
0044cfb0  7404                     je 0x44cfb6
0044cfb2  b001                     mov al, 1
0044cfb4  eb02                     jmp 0x44cfb8
0044cfb6  30c0                     xor al, al
0044cfb8  84c0                     test al, al
0044cfba  0f8484130000             je 0x44e344
0044cfc0  31d2                     xor edx, edx
0044cfc2  6689da                   mov dx, bx
0044cfc5  89d1                     mov ecx, edx
0044cfc7  c1e104                   shl ecx, 4
0044cfca  01d1                     add ecx, edx
0044cfcc  c1e102                   shl ecx, 2
0044cfcf  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044cfd4  01d1                     add ecx, edx
0044cfd6  8a542448                 mov dl, byte ptr [esp + 0x48]
0044cfda  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044cfde  663b1d04634900           cmp bx, word ptr [0x496304]
0044cfe5  0f8559130000             jne 0x44e344
0044cfeb  bfffff0000               mov edi, 0xffff
0044cff0  30fe                     xor dh, bh
0044cff2  31c0                     xor eax, eax
0044cff4  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044cffa  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044cfff  30db                     xor bl, bl
0044d001  66893d04634900           mov word ptr [0x496304], di
0044d008  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044d00e  e931130000               jmp 0x44e344
0044d013  c744241801000000         mov dword ptr [esp + 0x18], 1
0044d01b  eb0d                     jmp 0x44d02a
0044d01d  b002                     mov al, 2
0044d01f  8d560a                   lea edx, [esi + 0xa]
0044d022  38c0                     cmp al, al
0044d024  76ed                     jbe 0x44d013
0044d026  3c04                     cmp al, 4
0044d028  76e9                     jbe 0x44d013
0044d02a  31db                     xor ebx, ebx
0044d02c  31c0                     xor eax, eax
0044d02e  668b5c2418               mov bx, word ptr [esp + 0x18]
0044d033  668b4266                 mov ax, word ptr [edx + 0x66]
0044d037  01c3                     add ebx, eax
0044d039  31c0                     xor eax, eax
0044d03b  668b4202                 mov ax, word ptr [edx + 2]
0044d03f  39c3                     cmp ebx, eax
0044d041  0f9ec0                   setle al
0044d044  84c0                     test al, al
0044d046  0f8436010000             je 0x44d182
0044d04c  31db                     xor ebx, ebx
0044d04e  6689fb                   mov bx, di
0044d051  89d8                     mov eax, ebx
0044d053  e800afffff               call 0x447f58
0044d058  8aae8b000000             mov ch, byte ptr [esi + 0x8b]
0044d05e  31c0                     xor eax, eax
0044d060  fecd                     dec ch
0044d062  88e8                     mov al, ch
0044d064  88ae8b000000             mov byte ptr [esi + 0x8b], ch
0044d06a  85c0                     test eax, eax
0044d06c  0f8515010000             jne 0x44d187
0044d072  668b4608                 mov ax, word ptr [esi + 8]
0044d076  8d4e0a                   lea ecx, [esi + 0xa]
0044d079  e86ab10200               call 0x4781e8
0044d07e  66ff4166                 inc word ptr [ecx + 0x66]
0044d082  668b01                   mov ax, word ptr [ecx]
0044d085  25ffff0000               and eax, 0xffff
0044d08a  c644014202               mov byte ptr [ecx + eax + 0x42], 2
0044d08f  66c74441060100           mov word ptr [ecx + eax*2 + 6], 1
0044d096  668b11                   mov dx, word ptr [ecx]
0044d099  42                       inc edx
0044d09a  31c0                     xor eax, eax
0044d09c  668911                   mov word ptr [ecx], dx
0044d09f  668b4608                 mov ax, word ptr [esi + 8]
0044d0a3  bd05000000               mov ebp, 5
0044d0a8  89442404                 mov dword ptr [esp + 4], eax
0044d0ac  b819000000               mov eax, 0x19
0044d0b1  31d2                     xor edx, edx
0044d0b3  e824340200               call 0x4704dc
0044d0b8  f7f5                     div ebp
0044d0ba  8b442404                 mov eax, dword ptr [esp + 4]
0044d0be  01d0                     add eax, edx
0044d0c0  89442404                 mov dword ptr [esp + 4], eax
0044d0c4  b81a000000               mov eax, 0x1a
0044d0c9  31d2                     xor edx, edx
0044d0cb  e80c340200               call 0x4704dc
0044d0d0  f7f5                     div ebp
0044d0d2  c1e208                   shl edx, 8
0044d0d5  8b442404                 mov eax, dword ptr [esp + 4]
0044d0d9  81ea00020000             sub edx, 0x200
0044d0df  83e802                   sub eax, 2
0044d0e2  01d0                     add eax, edx
0044d0e4  25ffff0000               and eax, 0xffff
0044d0e9  89ea                     mov edx, ebp
0044d0eb  e8bdad0200               call 0x477ead
0044d0f0  89c3                     mov ebx, eax
0044d0f2  25ffff0000               and eax, 0xffff
0044d0f7  3dffff0000               cmp eax, 0xffff
0044d0fc  0f8480000000             je 0x44d182
0044d102  31c0                     xor eax, eax
0044d104  668b4166                 mov ax, word ptr [ecx + 0x66]
0044d108  8d5001                   lea edx, [eax + 1]
0044d10b  31c0                     xor eax, eax
0044d10d  668b4102                 mov ax, word ptr [ecx + 2]
0044d111  39c2                     cmp edx, eax
0044d113  0f9ec0                   setle al
0044d116  84c0                     test al, al
0044d118  7468                     je 0x44d182
0044d11a  31d2                     xor edx, edx
0044d11c  6689fa                   mov dx, di
0044d11f  89d1                     mov ecx, edx
0044d121  c1e104                   shl ecx, 4
0044d124  01d1                     add ecx, edx
0044d126  c1e102                   shl ecx, 2
0044d129  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044d130  01d1                     add ecx, edx
0044d132  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d138  c1e102                   shl ecx, 2
0044d13b  01ca                     add edx, ecx
0044d13d  66895a7e                 mov word ptr [edx + 0x7e], bx
0044d141  663b3d04634900           cmp di, word ptr [0x496304]
0044d148  7521                     jne 0x44d16b
0044d14a  30e4                     xor ah, ah
0044d14c  31c9                     xor ecx, ecx
0044d14e  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044d154  8825370f4e00             mov byte ptr [0x4e0f37], ah
0044d15a  b8ffff0000               mov eax, 0xffff
0044d15f  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044d165  66a304634900             mov word ptr [0x496304], ax
0044d16b  c6828800000000           mov byte ptr [edx + 0x88], 0
0044d172  c6868900000000           mov byte ptr [esi + 0x89], 0
0044d179  66899eb2000000           mov word ptr [esi + 0xb2], bx
0044d180  eb05                     jmp 0x44d187
0044d182  c644244401               mov byte ptr [esp + 0x44], 1
0044d187  807c244400               cmp byte ptr [esp + 0x44], 0
0044d18c  0f84b2110000             je 0x44e344
0044d192  31c0                     xor eax, eax
0044d194  8a8682000000             mov al, byte ptr [esi + 0x82]
0044d19a  83f802                   cmp eax, 2
0044d19d  0f858d000000             jne 0x44d230
0044d1a3  668b8680000000           mov ax, word ptr [esi + 0x80]
0044d1aa  668986c0000000           mov word ptr [esi + 0xc0], ax
0044d1b1  31c0                     xor eax, eax
0044d1b3  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d1ba  e82066fdff               call 0x4237df
0044d1bf  31c0                     xor eax, eax
0044d1c1  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d1c8  e85a69fdff               call 0x423b27
0044d1cd  89c3                     mov ebx, eax
0044d1cf  31c0                     xor eax, eax
0044d1d1  6689f8                   mov ax, di
0044d1d4  89c1                     mov ecx, eax
0044d1d6  c1e104                   shl ecx, 4
0044d1d9  01c1                     add ecx, eax
0044d1db  c1e102                   shl ecx, 2
0044d1de  c6868900000002           mov byte ptr [esi + 0x89], 2
0044d1e5  01c1                     add ecx, eax
0044d1e7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d1ed  c1e102                   shl ecx, 2
0044d1f0  01ca                     add edx, ecx
0044d1f2  81ebfe000000             sub ebx, 0xfe
0044d1f8  66895a7e                 mov word ptr [edx + 0x7e], bx
0044d1fc  663b3d04634900           cmp di, word ptr [0x496304]
0044d203  0f85abf6ffff             jne 0x44c8b4
0044d209  bbffff0000               mov ebx, 0xffff
0044d20e  30ed                     xor ch, ch
0044d210  31f6                     xor esi, esi
0044d212  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044d218  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044d21e  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044d224  66891d04634900           mov word ptr [0x496304], bx
0044d22b  e984f6ffff               jmp 0x44c8b4
0044d230  83f801                   cmp eax, 1
0044d233  0f8581010000             jne 0x44d3ba
0044d239  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044d240  0fb7eb                   movzx ebp, bx
0044d243  89c2                     mov edx, eax
0044d245  89e8                     mov eax, ebp
0044d247  e817850200               call 0x475763
0044d24c  84c0                     test al, al
0044d24e  7541                     jne 0x44d291
0044d250  b943000000               mov ecx, 0x43
0044d255  ba0a000000               mov edx, 0xa
0044d25a  89e8                     mov eax, ebp
0044d25c  89cb                     mov ebx, ecx
0044d25e  e8aaa60200               call 0x47790d
0044d263  89c3                     mov ebx, eax
0044d265  25ffff0000               and eax, 0xffff
0044d26a  3dffff0000               cmp eax, 0xffff
0044d26f  7519                     jne 0x44d28a
0044d271  ba0a000000               mov edx, 0xa
0044d276  31c0                     xor eax, eax
0044d278  31c9                     xor ecx, ecx
0044d27a  31db                     xor ebx, ebx
0044d27c  668b8680000000           mov ax, word ptr [esi + 0x80]
0044d283  e885a60200               call 0x47790d
0044d288  89c3                     mov ebx, eax
0044d28a  66899e80000000           mov word ptr [esi + 0x80], bx
0044d291  31c0                     xor eax, eax
0044d293  6689d8                   mov ax, bx
0044d296  3dffff0000               cmp eax, 0xffff
0044d29b  744e                     je 0x44d2eb
0044d29d  31d2                     xor edx, edx
0044d29f  6689fa                   mov dx, di
0044d2a2  89d1                     mov ecx, edx
0044d2a4  c1e104                   shl ecx, 4
0044d2a7  01d1                     add ecx, edx
0044d2a9  c1e102                   shl ecx, 2
0044d2ac  c6868900000002           mov byte ptr [esi + 0x89], 2
0044d2b3  01d1                     add ecx, edx
0044d2b5  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d2bb  c1e102                   shl ecx, 2
0044d2be  01ca                     add edx, ecx
0044d2c0  66895a7e                 mov word ptr [edx + 0x7e], bx
0044d2c4  663b3d04634900           cmp di, word ptr [0x496304]
0044d2cb  0f85e3f5ffff             jne 0x44c8b4
0044d2d1  bfffff0000               mov edi, 0xffff
0044d2d6  30ff                     xor bh, bh
0044d2d8  31c9                     xor ecx, ecx
0044d2da  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044d2e0  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044d2e6  e968f5ffff               jmp 0x44c853
0044d2eb  31d2                     xor edx, edx
0044d2ed  b107                     mov cl, 7
0044d2ef  6689fa                   mov dx, di
0044d2f2  884c2438                 mov byte ptr [esp + 0x38], cl
0044d2f6  89d1                     mov ecx, edx
0044d2f8  c1e104                   shl ecx, 4
0044d2fb  01d1                     add ecx, edx
0044d2fd  c1e102                   shl ecx, 2
0044d300  01d1                     add ecx, edx
0044d302  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d307  c1e102                   shl ecx, 2
0044d30a  01c1                     add ecx, eax
0044d30c  31c0                     xor eax, eax
0044d30e  8a4102                   mov al, byte ptr [ecx + 2]
0044d311  89fb                     mov ebx, edi
0044d313  85c0                     test eax, eax
0044d315  7409                     je 0x44d320
0044d317  83f804                   cmp eax, 4
0044d31a  7404                     je 0x44d320
0044d31c  b001                     mov al, 1
0044d31e  eb02                     jmp 0x44d322
0044d320  30c0                     xor al, al
0044d322  84c0                     test al, al
0044d324  7449                     je 0x44d36f
0044d326  31d2                     xor edx, edx
0044d328  6689da                   mov dx, bx
0044d32b  89d1                     mov ecx, edx
0044d32d  c1e104                   shl ecx, 4
0044d330  01d1                     add ecx, edx
0044d332  c1e102                   shl ecx, 2
0044d335  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d33a  01d1                     add ecx, edx
0044d33c  8a542438                 mov dl, byte ptr [esp + 0x38]
0044d340  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044d344  663b1d04634900           cmp bx, word ptr [0x496304]
0044d34b  7522                     jne 0x44d36f
0044d34d  30ed                     xor ch, ch
0044d34f  31d2                     xor edx, edx
0044d351  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044d357  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0044d35d  baffff0000               mov edx, 0xffff
0044d362  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044d368  66891504634900           mov word ptr [0x496304], dx
0044d36f  31c0                     xor eax, eax
0044d371  6689f8                   mov ax, di
0044d374  89c1                     mov ecx, eax
0044d376  c1e104                   shl ecx, 4
0044d379  01c1                     add ecx, eax
0044d37b  c1e102                   shl ecx, 2
0044d37e  01c1                     add ecx, eax
0044d380  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d386  c1e102                   shl ecx, 2
0044d389  01ca                     add edx, ecx
0044d38b  668b5e7c                 mov bx, word ptr [esi + 0x7c]
0044d38f  66895a7e                 mov word ptr [edx + 0x7e], bx
0044d393  663b3d04634900           cmp di, word ptr [0x496304]
0044d39a  0f8514f5ffff             jne 0x44c8b4
0044d3a0  b9ffff0000               mov ecx, 0xffff
0044d3a5  30e4                     xor ah, ah
0044d3a7  31db                     xor ebx, ebx
0044d3a9  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044d3af  8825370f4e00             mov byte ptr [0x4e0f37], ah
0044d3b5  e9edf4ffff               jmp 0x44c8a7
0044d3ba  31c0                     xor eax, eax
0044d3bc  6689f8                   mov ax, di
0044d3bf  89c1                     mov ecx, eax
0044d3c1  c1e104                   shl ecx, 4
0044d3c4  01c1                     add ecx, eax
0044d3c6  c1e102                   shl ecx, 2
0044d3c9  01c1                     add ecx, eax
0044d3cb  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d3d0  b307                     mov bl, 7
0044d3d2  89fa                     mov edx, edi
0044d3d4  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044d3d8  25ff000000               and eax, 0xff
0044d3dd  7409                     je 0x44d3e8
0044d3df  83f804                   cmp eax, 4
0044d3e2  7404                     je 0x44d3e8
0044d3e4  b001                     mov al, 1
0044d3e6  eb02                     jmp 0x44d3ea
0044d3e8  30c0                     xor al, al
0044d3ea  84c0                     test al, al
0044d3ec  7443                     je 0x44d431
0044d3ee  31c0                     xor eax, eax
0044d3f0  6689d0                   mov ax, dx
0044d3f3  89c1                     mov ecx, eax
0044d3f5  c1e104                   shl ecx, 4
0044d3f8  01c1                     add ecx, eax
0044d3fa  c1e102                   shl ecx, 2
0044d3fd  01c1                     add ecx, eax
0044d3ff  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d404  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044d408  663b1504634900           cmp dx, word ptr [0x496304]
0044d40f  7520                     jne 0x44d431
0044d411  b9ffff0000               mov ecx, 0xffff
0044d416  30c0                     xor al, al
0044d418  31ed                     xor ebp, ebp
0044d41a  a2360f4e00               mov byte ptr [0x4e0f36], al
0044d41f  a2370f4e00               mov byte ptr [0x4e0f37], al
0044d424  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044d42a  66890d04634900           mov word ptr [0x496304], cx
0044d431  31c0                     xor eax, eax
0044d433  6689f8                   mov ax, di
0044d436  89c1                     mov ecx, eax
0044d438  c1e104                   shl ecx, 4
0044d43b  01c1                     add ecx, eax
0044d43d  c1e102                   shl ecx, 2
0044d440  01c1                     add ecx, eax
0044d442  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d448  c1e102                   shl ecx, 2
0044d44b  01ca                     add edx, ecx
0044d44d  668b5e7c                 mov bx, word ptr [esi + 0x7c]
0044d451  66895a7e                 mov word ptr [edx + 0x7e], bx
0044d455  663b3d04634900           cmp di, word ptr [0x496304]
0044d45c  0f8552f4ffff             jne 0x44c8b4
0044d462  bfffff0000               mov edi, 0xffff
0044d467  30db                     xor bl, bl
0044d469  31c0                     xor eax, eax
0044d46b  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044d471  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044d477  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044d47c  e9d8f3ffff               jmp 0x44c859
0044d481  668b467e                 mov ax, word ptr [esi + 0x7e]
0044d485  668b5608                 mov dx, word ptr [esi + 8]
0044d489  6639d0                   cmp ax, dx
0044d48c  0f857fe8ffff             jne 0x44bd11
0044d492  31c0                     xor eax, eax
0044d494  8a8682000000             mov al, byte ptr [esi + 0x82]
0044d49a  83f802                   cmp eax, 2
0044d49d  7567                     jne 0x44d506
0044d49f  31c0                     xor eax, eax
0044d4a1  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d4a8  e87a66fdff               call 0x423b27
0044d4ad  25ffff0000               and eax, 0xffff
0044d4b2  31d2                     xor edx, edx
0044d4b4  2dfe000000               sub eax, 0xfe
0044d4b9  668b5608                 mov dx, word ptr [esi + 8]
0044d4bd  39c2                     cmp edx, eax
0044d4bf  7524                     jne 0x44d4e5
0044d4c1  31c0                     xor eax, eax
0044d4c3  8a4601                   mov al, byte ptr [esi + 1]
0044d4c6  89c1                     mov ecx, eax
0044d4c8  c1e102                   shl ecx, 2
0044d4cb  29c1                     sub ecx, eax
0044d4cd  c1e103                   shl ecx, 3
0044d4d0  c6868900000003           mov byte ptr [esi + 0x89], 3
0044d4d7  01c1                     add ecx, eax
0044d4d9  c6869000000009           mov byte ptr [esi + 0x90], 9
0044d4e0  e956f4ffff               jmp 0x44c93b
0044d4e5  31c0                     xor eax, eax
0044d4e7  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d4ee  e83466fdff               call 0x423b27
0044d4f3  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d4f9  01ca                     add edx, ecx
0044d4fb  81e8fe000000             sub eax, 0xfe
0044d501  e94ef0ffff               jmp 0x44c554
0044d506  83f801                   cmp eax, 1
0044d509  0f85350e0000             jne 0x44e344
0044d50f  668b8680000000           mov ax, word ptr [esi + 0x80]
0044d516  6639d0                   cmp ax, dx
0044d519  7539                     jne 0x44d554
0044d51b  31c0                     xor eax, eax
0044d51d  8a4601                   mov al, byte ptr [esi + 1]
0044d520  89c1                     mov ecx, eax
0044d522  c1e102                   shl ecx, 2
0044d525  29c1                     sub ecx, eax
0044d527  c1e103                   shl ecx, 3
0044d52a  01c1                     add ecx, eax
0044d52c  c6868900000004           mov byte ptr [esi + 0x89], 4
0044d533  31d2                     xor edx, edx
0044d535  668b144dde654900         mov dx, word ptr [ecx*2 + 0x4965de]
0044d53d  bb0a000000               mov ebx, 0xa
0044d542  89d0                     mov eax, edx
0044d544  c1fa1f                   sar edx, 0x1f
0044d547  f7fb                     idiv ebx
0044d549  88868b000000             mov byte ptr [esi + 0x8b], al
0044d54f  e9f00d0000               jmp 0x44e344
0044d554  bb01000000               mov ebx, 1
0044d559  31d2                     xor edx, edx
0044d55b  31c9                     xor ecx, ecx
0044d55d  6689c2                   mov dx, ax
0044d560  89e8                     mov eax, ebp
0044d562  e80151ffff               call 0x442668
0044d567  84c0                     test al, al
0044d569  7446                     je 0x44d5b1
0044d56b  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044d571  668b8680000000           mov ax, word ptr [esi + 0x80]
0044d578  031424                   add edx, dword ptr [esp]
0044d57b  6689427e                 mov word ptr [edx + 0x7e], ax
0044d57f  663b3d04634900           cmp di, word ptr [0x496304]
0044d586  0f8528f3ffff             jne 0x44c8b4
0044d58c  beffff0000               mov esi, 0xffff
0044d591  30c0                     xor al, al
0044d593  31ff                     xor edi, edi
0044d595  a2360f4e00               mov byte ptr [0x4e0f36], al
0044d59a  a2370f4e00               mov byte ptr [0x4e0f37], al
0044d59f  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044d5a5  66893504634900           mov word ptr [0x496304], si
0044d5ac  e903f3ffff               jmp 0x44c8b4
0044d5b1  31c9                     xor ecx, ecx
0044d5b3  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044d5ba  89ca                     mov edx, ecx
0044d5bc  89c8                     mov eax, ecx
0044d5be  c1fa1f                   sar edx, 0x1f
0044d5c1  c1e208                   shl edx, 8
0044d5c4  1bc2                     sbb eax, edx
0044d5c6  c1f808                   sar eax, 8
0044d5c9  bb00010000               mov ebx, 0x100
0044d5ce  0fb7e8                   movzx ebp, ax
0044d5d1  89ca                     mov edx, ecx
0044d5d3  89c8                     mov eax, ecx
0044d5d5  c1fa1f                   sar edx, 0x1f
0044d5d8  f7fb                     idiv ebx
0044d5da  31c9                     xor ecx, ecx
0044d5dc  31db                     xor ebx, ebx
0044d5de  668b4e08                 mov cx, word ptr [esi + 8]
0044d5e2  6689d3                   mov bx, dx
0044d5e5  89ca                     mov edx, ecx
0044d5e7  89c8                     mov eax, ecx
0044d5e9  c1fa1f                   sar edx, 0x1f
0044d5ec  c1e208                   shl edx, 8
0044d5ef  1bc2                     sbb eax, edx
0044d5f1  c1f808                   sar eax, 8
0044d5f4  31ff                     xor edi, edi
0044d5f6  6689c7                   mov di, ax
0044d5f9  89ca                     mov edx, ecx
0044d5fb  b800010000               mov eax, 0x100
0044d600  c1fa1f                   sar edx, 0x1f
0044d603  89442404                 mov dword ptr [esp + 4], eax
0044d607  89c8                     mov eax, ecx
0044d609  f77c2404                 idiv dword ptr [esp + 4]
0044d60d  31c0                     xor eax, eax
0044d60f  89e9                     mov ecx, ebp
0044d611  6689d0                   mov ax, dx
0044d614  89fa                     mov edx, edi
0044d616  e83abf0200               call 0x479555
0044d61b  83f810                   cmp eax, 0x10
0044d61e  0f83200d0000             jae 0x44e344
0044d624  31d2                     xor edx, edx
0044d626  8a5601                   mov dl, byte ptr [esi + 1]
0044d629  89d1                     mov ecx, edx
0044d62b  c1e102                   shl ecx, 2
0044d62e  29d1                     sub ecx, edx
0044d630  668b4608                 mov ax, word ptr [esi + 8]
0044d634  c1e103                   shl ecx, 3
0044d637  c6868900000004           mov byte ptr [esi + 0x89], 4
0044d63e  01d1                     add ecx, edx
0044d640  66898680000000           mov word ptr [esi + 0x80], ax
0044d647  e9e7feffff               jmp 0x44d533
0044d64c  8a8690000000             mov al, byte ptr [esi + 0x90]
0044d652  3a8691000000             cmp al, byte ptr [esi + 0x91]
0044d658  740c                     je 0x44d666
0044d65a  89e8                     mov eax, ebp
0044d65c  e838afffff               call 0x448599
0044d661  e9de0c0000               jmp 0x44e344
0044d666  31c0                     xor eax, eax
0044d668  ba01000000               mov edx, 1
0044d66d  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d674  e8e3cffcff               call 0x41a65c
0044d679  31c0                     xor eax, eax
0044d67b  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d682  e8f535fdff               call 0x420c7c
0044d687  84c0                     test al, al
0044d689  0f84b50c0000             je 0x44e344
0044d68f  31c0                     xor eax, eax
0044d691  8a4601                   mov al, byte ptr [esi + 1]
0044d694  89c1                     mov ecx, eax
0044d696  c1e102                   shl ecx, 2
0044d699  29c1                     sub ecx, eax
0044d69b  c1e103                   shl ecx, 3
0044d69e  01c1                     add ecx, eax
0044d6a0  c6868900000004           mov byte ptr [esi + 0x89], 4
0044d6a7  e98ff2ffff               jmp 0x44c93b
0044d6ac  bb01000000               mov ebx, 1
0044d6b1  8d4e0a                   lea ecx, [esi + 0xa]
0044d6b4  ba02000000               mov edx, 2
0044d6b9  89c8                     mov eax, ecx
0044d6bb  e8f89affff               call 0x4471b8
0044d6c0  25ffff0000               and eax, 0xffff
0044d6c5  0f8531010000             jne 0x44d7fc
0044d6cb  8a8682000000             mov al, byte ptr [esi + 0x82]
0044d6d1  83f802                   cmp eax, 2
0044d6d4  7527                     jne 0x44d6fd
0044d6d6  31c0                     xor eax, eax
0044d6d8  31d2                     xor edx, edx
0044d6da  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d6e1  e876cffcff               call 0x41a65c
0044d6e6  31c0                     xor eax, eax
0044d6e8  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044d6ef  e80b61fdff               call 0x4237ff
0044d6f4  66c786c0000000ffff       mov word ptr [esi + 0xc0], 0xffff
0044d6fd  31c0                     xor eax, eax
0044d6ff  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044d706  3dffff0000               cmp eax, 0xffff
0044d70b  7461                     je 0x44d76e
0044d70d  31c0                     xor eax, eax
0044d70f  6689f8                   mov ax, di
0044d712  89c1                     mov ecx, eax
0044d714  c1e104                   shl ecx, 4
0044d717  01c1                     add ecx, eax
0044d719  c1e102                   shl ecx, 2
0044d71c  c6868900000000           mov byte ptr [esi + 0x89], 0
0044d723  01c1                     add ecx, eax
0044d725  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d72a  c1e102                   shl ecx, 2
0044d72d  01c8                     add eax, ecx
0044d72f  668b96b2000000           mov dx, word ptr [esi + 0xb2]
0044d736  6689507e                 mov word ptr [eax + 0x7e], dx
0044d73a  663b3d04634900           cmp di, word ptr [0x496304]
0044d741  0f852af4ffff             jne 0x44cb71
0044d747  bfffff0000               mov edi, 0xffff
0044d74c  30ff                     xor bh, bh
0044d74e  31c9                     xor ecx, ecx
0044d750  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044d756  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044d75c  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044d762  66893d04634900           mov word ptr [0x496304], di
0044d769  e903f4ffff               jmp 0x44cb71
0044d76e  31c0                     xor eax, eax
0044d770  6689f8                   mov ax, di
0044d773  89c1                     mov ecx, eax
0044d775  c1e104                   shl ecx, 4
0044d778  01c1                     add ecx, eax
0044d77a  c1e102                   shl ecx, 2
0044d77d  01c1                     add ecx, eax
0044d77f  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d784  c1e102                   shl ecx, 2
0044d787  01c1                     add ecx, eax
0044d789  31c0                     xor eax, eax
0044d78b  b307                     mov bl, 7
0044d78d  8a4102                   mov al, byte ptr [ecx + 2]
0044d790  89fa                     mov edx, edi
0044d792  85c0                     test eax, eax
0044d794  7409                     je 0x44d79f
0044d796  83f804                   cmp eax, 4
0044d799  7404                     je 0x44d79f
0044d79b  b001                     mov al, 1
0044d79d  eb02                     jmp 0x44d7a1
0044d79f  30c0                     xor al, al
0044d7a1  84c0                     test al, al
0044d7a3  0f849b0b0000             je 0x44e344
0044d7a9  31c0                     xor eax, eax
0044d7ab  6689d0                   mov ax, dx
0044d7ae  89c1                     mov ecx, eax
0044d7b0  c1e104                   shl ecx, 4
0044d7b3  01c1                     add ecx, eax
0044d7b5  c1e102                   shl ecx, 2
0044d7b8  01c1                     add ecx, eax
0044d7ba  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044d7bf  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044d7c3  668b1d04634900           mov bx, word ptr [0x496304]
0044d7ca  6639da                   cmp dx, bx
0044d7cd  0f85710b0000             jne 0x44e344
0044d7d3  b9ffff0000               mov ecx, 0xffff
0044d7d8  30fe                     xor dh, bh
0044d7da  30db                     xor bl, bl
0044d7dc  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044d7e2  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044d7e8  31db                     xor ebx, ebx
0044d7ea  66890d04634900           mov word ptr [0x496304], cx
0044d7f1  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044d7f7  e9480b0000               jmp 0x44e344
0044d7fc  8a968b000000             mov dl, byte ptr [esi + 0x8b]
0044d802  31c0                     xor eax, eax
0044d804  feca                     dec dl
0044d806  88d0                     mov al, dl
0044d808  88968b000000             mov byte ptr [esi + 0x8b], dl
0044d80e  85c0                     test eax, eax
0044d810  0f852e0b0000             jne 0x44e344
0044d816  8a8682000000             mov al, byte ptr [esi + 0x82]
0044d81c  83f802                   cmp eax, 2
0044d81f  751e                     jne 0x44d83f
0044d821  bb01000000               mov ebx, 1
0044d826  89c2                     mov edx, eax
0044d828  89c8                     mov eax, ecx
0044d82a  e8bb9affff               call 0x4472ea
0044d82f  ba01000000               mov edx, 1
0044d834  31c9                     xor ecx, ecx
0044d836  31db                     xor ebx, ebx
0044d838  89d0                     mov eax, edx
0044d83a  e9ddf0ffff               jmp 0x44c91c
0044d83f  83f801                   cmp eax, 1
0044d842  0f85fc0a0000             jne 0x44e344
0044d848  ba02000000               mov edx, 2
0044d84d  89c3                     mov ebx, eax
0044d84f  89e8                     mov eax, ebp
0044d851  e88260ffff               call 0x4438d8
0044d856  e9e90a0000               jmp 0x44e344
0044d85b  8a8689000000             mov al, byte ptr [esi + 0x89]
0044d861  3c04                     cmp al, 4
0044d863  0f87db0a0000             ja 0x44e344
0044d869  25ff000000               and eax, 0xff
0044d86e  2eff248550bc4400         jmp dword ptr cs:[eax*4 + 0x44bc50]
0044d876  c744242c01000000         mov dword ptr [esp + 0x2c], 1
0044d87e  eb11                     jmp 0x44d891
0044d880  b002                     mov al, 2
0044d882  8d560a                   lea edx, [esi + 0xa]
0044d885  3c01                     cmp al, 1
0044d887  7208                     jb 0x44d891
0044d889  38c0                     cmp al, al
0044d88b  76e9                     jbe 0x44d876
0044d88d  3c04                     cmp al, 4
0044d88f  76e5                     jbe 0x44d876
0044d891  31c0                     xor eax, eax
0044d893  31db                     xor ebx, ebx
0044d895  668b44242c               mov ax, word ptr [esp + 0x2c]
0044d89a  668b5a66                 mov bx, word ptr [edx + 0x66]
0044d89e  668b5202                 mov dx, word ptr [edx + 2]
0044d8a2  01d8                     add eax, ebx
0044d8a4  81e2ffff0000             and edx, 0xffff
0044d8aa  39d0                     cmp eax, edx
0044d8ac  0f9ec0                   setle al
0044d8af  84c0                     test al, al
0044d8b1  0f847b010000             je 0x44da32
0044d8b7  668b467e                 mov ax, word ptr [esi + 0x7e]
0044d8bb  668b5608                 mov dx, word ptr [esi + 8]
0044d8bf  6639d0                   cmp ax, dx
0044d8c2  0f8549e4ffff             jne 0x44bd11
0044d8c8  31c0                     xor eax, eax
0044d8ca  6689d0                   mov ax, dx
0044d8cd  e8e7890200               call 0x4762b9
0044d8d2  84c0                     test al, al
0044d8d4  743d                     je 0x44d913
0044d8d6  31db                     xor ebx, ebx
0044d8d8  8a5e01                   mov bl, byte ptr [esi + 1]
0044d8db  89d9                     mov ecx, ebx
0044d8dd  ba03000000               mov edx, 3
0044d8e2  c1e102                   shl ecx, 2
0044d8e5  c6868900000001           mov byte ptr [esi + 0x89], 1
0044d8ec  29d9                     sub ecx, ebx
0044d8ee  31c0                     xor eax, eax
0044d8f0  c1e103                   shl ecx, 3
0044d8f3  8a06                     mov al, byte ptr [esi]
0044d8f5  01d9                     add ecx, ebx
0044d8f7  e8c4b3fdff               call 0x428cc0
0044d8fc  89c2                     mov edx, eax
0044d8fe  8a044dde654900           mov al, byte ptr [ecx*2 + 0x4965de]
0044d905  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044d90c  28d0                     sub al, dl
0044d90e  e936fcffff               jmp 0x44d549
0044d913  ba05000000               mov edx, 5
0044d918  0fb7ef                   movzx ebp, di
0044d91b  31c0                     xor eax, eax
0044d91d  89eb                     mov ebx, ebp
0044d91f  89e9                     mov ecx, ebp
0044d921  668b4608                 mov ax, word ptr [esi + 8]
0044d925  c1e104                   shl ecx, 4
0044d928  e880a50200               call 0x477ead
0044d92d  01e9                     add ecx, ebp
0044d92f  8944241c                 mov dword ptr [esp + 0x1c], eax
0044d933  c1e102                   shl ecx, 2
0044d936  31db                     xor ebx, ebx
0044d938  8d1429                   lea edx, [ecx + ebp]
0044d93b  6689c3                   mov bx, ax
0044d93e  c1e202                   shl edx, 2
0044d941  81fbffff0000             cmp ebx, 0xffff
0044d947  743f                     je 0x44d988
0044d949  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044d94f  01da                     add edx, ebx
0044d951  6689427e                 mov word ptr [edx + 0x7e], ax
0044d955  663b3d04634900           cmp di, word ptr [0x496304]
0044d95c  7521                     jne 0x44d97f
0044d95e  b9ffff0000               mov ecx, 0xffff
0044d963  30db                     xor bl, bl
0044d965  31c0                     xor eax, eax
0044d967  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044d96d  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044d973  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044d978  66890d04634900           mov word ptr [0x496304], cx
0044d97f  8b44241c                 mov eax, dword ptr [esp + 0x1c]
0044d983  e933f5ffff               jmp 0x44cebb
0044d988  8b0da0194e00             mov ecx, dword ptr [0x4e19a0]
0044d98e  01d1                     add ecx, edx
0044d990  8a01                     mov al, byte ptr [ecx]
0044d992  8a2541805000             mov ah, byte ptr [0x508041]
0044d998  38e0                     cmp al, ah
0044d99a  754e                     jne 0x44d9ea
0044d99c  31d2                     xor edx, edx
0044d99e  88e2                     mov dl, ah
0044d9a0  31c0                     xor eax, eax
0044d9a2  668b4108                 mov ax, word ptr [ecx + 8]
0044d9a6  e8458d0200               call 0x4766f0
0044d9ab  84c0                     test al, al
0044d9ad  743b                     je 0x44d9ea
0044d9af  89e8                     mov eax, ebp
0044d9b1  e8a732ffff               call 0x440c5d
0044d9b6  8ba904010000             mov ebp, dword ptr [ecx + 0x104]
0044d9bc  c681f900000000           mov byte ptr [ecx + 0xf9], 0
0044d9c3  83fdff                   cmp ebp, -1
0044d9c6  7522                     jne 0x44d9ea
0044d9c8  6800010000               push 0x100
0044d9cd  31d2                     xor edx, edx
0044d9cf  b850000000               mov eax, 0x50
0044d9d4  8a5101                   mov dl, byte ptr [ecx + 1]
0044d9d7  8d9904010000             lea ebx, [ecx + 0x104]
0044d9dd  c1e210                   shl edx, 0x10
0044d9e0  31c9                     xor ecx, ecx
0044d9e2  80ce10                   or dh, 0x10
0044d9e5  e88fd00300               call 0x48aa79
0044d9ea  31c0                     xor eax, eax
0044d9ec  8a8682000000             mov al, byte ptr [esi + 0x82]
0044d9f2  83f802                   cmp eax, 2
0044d9f5  7522                     jne 0x44da19
0044d9f7  31c0                     xor eax, eax
0044d9f9  668b8680000000           mov ax, word ptr [esi + 0x80]
0044da00  31d2                     xor edx, edx
0044da02  e82061fdff               call 0x423b27
0044da07  6689c2                   mov dx, ax
0044da0a  31c0                     xor eax, eax
0044da0c  6689f8                   mov ax, di
0044da0f  e8bf7dffff               call 0x4457d3
0044da14  e92b090000               jmp 0x44e344
0044da19  83f801                   cmp eax, 1
0044da1c  0f8522090000             jne 0x44e344
0044da22  31c0                     xor eax, eax
0044da24  31d2                     xor edx, edx
0044da26  6689f8                   mov ax, di
0044da29  668b9680000000           mov dx, word ptr [esi + 0x80]
0044da30  ebdd                     jmp 0x44da0f
0044da32  31db                     xor ebx, ebx
0044da34  8a5e01                   mov bl, byte ptr [esi + 1]
0044da37  ba03000000               mov edx, 3
0044da3c  89d9                     mov ecx, ebx
0044da3e  c6868900000001           mov byte ptr [esi + 0x89], 1
0044da45  c1e102                   shl ecx, 2
0044da48  89d8                     mov eax, ebx
0044da4a  29d9                     sub ecx, ebx
0044da4c  31d8                     xor eax, ebx
0044da4e  e99dfeffff               jmp 0x44d8f0
0044da53  c744241401000000         mov dword ptr [esp + 0x14], 1
0044da5b  eb11                     jmp 0x44da6e
0044da5d  b002                     mov al, 2
0044da5f  8d560a                   lea edx, [esi + 0xa]
0044da62  3c01                     cmp al, 1
0044da64  7208                     jb 0x44da6e
0044da66  38c0                     cmp al, al
0044da68  76e9                     jbe 0x44da53
0044da6a  3c04                     cmp al, 4
0044da6c  76e5                     jbe 0x44da53
0044da6e  31db                     xor ebx, ebx
0044da70  31c0                     xor eax, eax
0044da72  668b5c2414               mov bx, word ptr [esp + 0x14]
0044da77  668b4266                 mov ax, word ptr [edx + 0x66]
0044da7b  01c3                     add ebx, eax
0044da7d  31c0                     xor eax, eax
0044da7f  668b4202                 mov ax, word ptr [edx + 2]
0044da83  39c3                     cmp ebx, eax
0044da85  0f9ec0                   setle al
0044da88  84c0                     test al, al
0044da8a  0f847c010000             je 0x44dc0c
0044da90  31c0                     xor eax, eax
0044da92  6689f8                   mov ax, di
0044da95  e8bea4ffff               call 0x447f58
0044da9a  8ab68b000000             mov dh, byte ptr [esi + 0x8b]
0044daa0  31c0                     xor eax, eax
0044daa2  fece                     dec dh
0044daa4  88f0                     mov al, dh
0044daa6  88b68b000000             mov byte ptr [esi + 0x8b], dh
0044daac  85c0                     test eax, eax
0044daae  0f855d010000             jne 0x44dc11
0044dab4  668b4608                 mov ax, word ptr [esi + 8]
0044dab8  8d4e0a                   lea ecx, [esi + 0xa]
0044dabb  e828a70200               call 0x4781e8
0044dac0  668b5166                 mov dx, word ptr [ecx + 0x66]
0044dac4  42                       inc edx
0044dac5  668b01                   mov ax, word ptr [ecx]
0044dac8  66895166                 mov word ptr [ecx + 0x66], dx
0044dacc  25ffff0000               and eax, 0xffff
0044dad1  c644014202               mov byte ptr [ecx + eax + 0x42], 2
0044dad6  66c74441060100           mov word ptr [ecx + eax*2 + 6], 1
0044dadd  31c0                     xor eax, eax
0044dadf  668b4166                 mov ax, word ptr [ecx + 0x66]
0044dae3  8d5001                   lea edx, [eax + 1]
0044dae6  668b19                   mov bx, word ptr [ecx]
0044dae9  31c0                     xor eax, eax
0044daeb  43                       inc ebx
0044daec  668b4102                 mov ax, word ptr [ecx + 2]
0044daf0  668919                   mov word ptr [ecx], bx
0044daf3  39c2                     cmp edx, eax
0044daf5  0f9ec0                   setle al
0044daf8  84c0                     test al, al
0044dafa  7436                     je 0x44db32
0044dafc  ba07000000               mov edx, 7
0044db01  31db                     xor ebx, ebx
0044db03  31c0                     xor eax, eax
0044db05  8a5e01                   mov bl, byte ptr [esi + 1]
0044db08  8a06                     mov al, byte ptr [esi]
0044db0a  e8b1b1fdff               call 0x428cc0
0044db0f  6685c0                   test ax, ax
0044db12  741e                     je 0x44db32
0044db14  8d4e0a                   lea ecx, [esi + 0xa]
0044db17  66ff4166                 inc word ptr [ecx + 0x66]
0044db1b  668b01                   mov ax, word ptr [ecx]
0044db1e  25ffff0000               and eax, 0xffff
0044db23  c644014202               mov byte ptr [ecx + eax + 0x42], 2
0044db28  66c74441060100           mov word ptr [ecx + eax*2 + 6], 1
0044db2f  66ff01                   inc word ptr [ecx]
0044db32  b81b000000               mov eax, 0x1b
0044db37  bb05000000               mov ebx, 5
0044db3c  31c9                     xor ecx, ecx
0044db3e  31d2                     xor edx, edx
0044db40  668b4e08                 mov cx, word ptr [esi + 8]
0044db44  e893290200               call 0x4704dc
0044db49  f7f3                     div ebx
0044db4b  b81c000000               mov eax, 0x1c
0044db50  01d1                     add ecx, edx
0044db52  31d2                     xor edx, edx
0044db54  e883290200               call 0x4704dc
0044db59  f7f3                     div ebx
0044db5b  c1e208                   shl edx, 8
0044db5e  83e902                   sub ecx, 2
0044db61  8d8200feffff             lea eax, [edx - 0x200]
0044db67  01c8                     add eax, ecx
0044db69  25ffff0000               and eax, 0xffff
0044db6e  89da                     mov edx, ebx
0044db70  e857a60200               call 0x4781cc
0044db75  89c3                     mov ebx, eax
0044db77  25ffff0000               and eax, 0xffff
0044db7c  3dffff0000               cmp eax, 0xffff
0044db81  0f8485000000             je 0x44dc0c
0044db87  8d560a                   lea edx, [esi + 0xa]
0044db8a  31c0                     xor eax, eax
0044db8c  668b4266                 mov ax, word ptr [edx + 0x66]
0044db90  40                       inc eax
0044db91  668b5202                 mov dx, word ptr [edx + 2]
0044db95  81e2ffff0000             and edx, 0xffff
0044db9b  39d0                     cmp eax, edx
0044db9d  0f9ec0                   setle al
0044dba0  84c0                     test al, al
0044dba2  7468                     je 0x44dc0c
0044dba4  31d2                     xor edx, edx
0044dba6  6689fa                   mov dx, di
0044dba9  89d1                     mov ecx, edx
0044dbab  c1e104                   shl ecx, 4
0044dbae  01d1                     add ecx, edx
0044dbb0  c1e102                   shl ecx, 2
0044dbb3  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044dbba  01d1                     add ecx, edx
0044dbbc  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044dbc2  c1e102                   shl ecx, 2
0044dbc5  01ca                     add edx, ecx
0044dbc7  66895a7e                 mov word ptr [edx + 0x7e], bx
0044dbcb  663b3d04634900           cmp di, word ptr [0x496304]
0044dbd2  7521                     jne 0x44dbf5
0044dbd4  b8ffff0000               mov eax, 0xffff
0044dbd9  30c9                     xor cl, cl
0044dbdb  31ed                     xor ebp, ebp
0044dbdd  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044dbe3  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044dbe9  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044dbef  66a304634900             mov word ptr [0x496304], ax
0044dbf5  c6828800000000           mov byte ptr [edx + 0x88], 0
0044dbfc  c6868900000000           mov byte ptr [esi + 0x89], 0
0044dc03  66899eb2000000           mov word ptr [esi + 0xb2], bx
0044dc0a  eb05                     jmp 0x44dc11
0044dc0c  c644244401               mov byte ptr [esp + 0x44], 1
0044dc11  807c244400               cmp byte ptr [esp + 0x44], 0
0044dc16  0f8428070000             je 0x44e344
0044dc1c  31c0                     xor eax, eax
0044dc1e  8a8682000000             mov al, byte ptr [esi + 0x82]
0044dc24  83f802                   cmp eax, 2
0044dc27  0f8505010000             jne 0x44dd32
0044dc2d  668b8680000000           mov ax, word ptr [esi + 0x80]
0044dc34  668986c0000000           mov word ptr [esi + 0xc0], ax
0044dc3b  31c0                     xor eax, eax
0044dc3d  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044dc44  3dffff0000               cmp eax, 0xffff
0044dc49  7455                     je 0x44dca0
0044dc4b  e892d2fcff               call 0x41aee2
0044dc50  89c3                     mov ebx, eax
0044dc52  31c0                     xor eax, eax
0044dc54  6689f8                   mov ax, di
0044dc57  89c1                     mov ecx, eax
0044dc59  c1e104                   shl ecx, 4
0044dc5c  01c1                     add ecx, eax
0044dc5e  c1e102                   shl ecx, 2
0044dc61  c6868900000002           mov byte ptr [esi + 0x89], 2
0044dc68  01c1                     add ecx, eax
0044dc6a  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044dc70  c1e102                   shl ecx, 2
0044dc73  01ca                     add edx, ecx
0044dc75  66895a7e                 mov word ptr [edx + 0x7e], bx
0044dc79  663b3d04634900           cmp di, word ptr [0x496304]
0044dc80  0f852eecffff             jne 0x44c8b4
0044dc86  30db                     xor bl, bl
0044dc88  31f6                     xor esi, esi
0044dc8a  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044dc90  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044dc96  bbffff0000               mov ebx, 0xffff
0044dc9b  e97ef5ffff               jmp 0x44d21e
0044dca0  c644243c07               mov byte ptr [esp + 0x3c], 7
0044dca5  31c0                     xor eax, eax
0044dca7  6689f8                   mov ax, di
0044dcaa  89c1                     mov ecx, eax
0044dcac  c1e104                   shl ecx, 4
0044dcaf  01c1                     add ecx, eax
0044dcb1  c1e102                   shl ecx, 2
0044dcb4  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044dcba  01c1                     add ecx, eax
0044dcbc  31c0                     xor eax, eax
0044dcbe  8a448b02                 mov al, byte ptr [ebx + ecx*4 + 2]
0044dcc2  89fa                     mov edx, edi
0044dcc4  85c0                     test eax, eax
0044dcc6  7409                     je 0x44dcd1
0044dcc8  83f804                   cmp eax, 4
0044dccb  7404                     je 0x44dcd1
0044dccd  b001                     mov al, 1
0044dccf  eb02                     jmp 0x44dcd3
0044dcd1  30c0                     xor al, al
0044dcd3  84c0                     test al, al
0044dcd5  0f8469060000             je 0x44e344
0044dcdb  31c0                     xor eax, eax
0044dcdd  6689d0                   mov ax, dx
0044dce0  89c1                     mov ecx, eax
0044dce2  c1e104                   shl ecx, 4
0044dce5  01c1                     add ecx, eax
0044dce7  c1e102                   shl ecx, 2
0044dcea  01c1                     add ecx, eax
0044dcec  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044dcf1  8a5c243c                 mov bl, byte ptr [esp + 0x3c]
0044dcf5  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044dcf9  668b0d04634900           mov cx, word ptr [0x496304]
0044dd00  6639ca                   cmp dx, cx
0044dd03  0f853b060000             jne 0x44e344
0044dd09  beffff0000               mov esi, 0xffff
0044dd0e  30e4                     xor ah, ah
0044dd10  30ca                     xor dl, cl
0044dd12  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044dd18  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044dd1e  31c9                     xor ecx, ecx
0044dd20  66893504634900           mov word ptr [0x496304], si
0044dd27  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044dd2d  e912060000               jmp 0x44e344
0044dd32  83f801                   cmp eax, 1
0044dd35  0f8544010000             jne 0x44de7f
0044dd3b  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044dd42  0fb7eb                   movzx ebp, bx
0044dd45  ba43000000               mov edx, 0x43
0044dd4a  89e8                     mov eax, ebp
0044dd4c  e8127a0200               call 0x475763
0044dd51  84c0                     test al, al
0044dd53  7541                     jne 0x44dd96
0044dd55  b943000000               mov ecx, 0x43
0044dd5a  ba0a000000               mov edx, 0xa
0044dd5f  89e8                     mov eax, ebp
0044dd61  89cb                     mov ebx, ecx
0044dd63  e8a59b0200               call 0x47790d
0044dd68  89c3                     mov ebx, eax
0044dd6a  25ffff0000               and eax, 0xffff
0044dd6f  3dffff0000               cmp eax, 0xffff
0044dd74  7519                     jne 0x44dd8f
0044dd76  ba0a000000               mov edx, 0xa
0044dd7b  31c0                     xor eax, eax
0044dd7d  31c9                     xor ecx, ecx
0044dd7f  31db                     xor ebx, ebx
0044dd81  668b8680000000           mov ax, word ptr [esi + 0x80]
0044dd88  e8809b0200               call 0x47790d
0044dd8d  89c3                     mov ebx, eax
0044dd8f  66899e80000000           mov word ptr [esi + 0x80], bx
0044dd96  31c0                     xor eax, eax
0044dd98  6689d8                   mov ax, bx
0044dd9b  3dffff0000               cmp eax, 0xffff
0044dda0  7454                     je 0x44ddf6
0044dda2  31d2                     xor edx, edx
0044dda4  6689fa                   mov dx, di
0044dda7  89d1                     mov ecx, edx
0044dda9  c1e104                   shl ecx, 4
0044ddac  01d1                     add ecx, edx
0044ddae  c1e102                   shl ecx, 2
0044ddb1  c6868900000002           mov byte ptr [esi + 0x89], 2
0044ddb8  01d1                     add ecx, edx
0044ddba  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ddc0  c1e102                   shl ecx, 2
0044ddc3  01ca                     add edx, ecx
0044ddc5  66895a7e                 mov word ptr [edx + 0x7e], bx
0044ddc9  663b3d04634900           cmp di, word ptr [0x496304]
0044ddd0  0f85deeaffff             jne 0x44c8b4
0044ddd6  30c9                     xor cl, cl
0044ddd8  31db                     xor ebx, ebx
0044ddda  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044dde0  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044dde6  bbffff0000               mov ebx, 0xffff
0044ddeb  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044ddf1  e92ef4ffff               jmp 0x44d224
0044ddf6  c644244007               mov byte ptr [esp + 0x40], 7
0044ddfb  31d2                     xor edx, edx
0044ddfd  6689fa                   mov dx, di
0044de00  89d1                     mov ecx, edx
0044de02  c1e104                   shl ecx, 4
0044de05  01d1                     add ecx, edx
0044de07  c1e102                   shl ecx, 2
0044de0a  01d1                     add ecx, edx
0044de0c  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044de11  c1e102                   shl ecx, 2
0044de14  01c1                     add ecx, eax
0044de16  31c0                     xor eax, eax
0044de18  8a4102                   mov al, byte ptr [ecx + 2]
0044de1b  89fb                     mov ebx, edi
0044de1d  85c0                     test eax, eax
0044de1f  7409                     je 0x44de2a
0044de21  83f804                   cmp eax, 4
0044de24  7404                     je 0x44de2a
0044de26  b001                     mov al, 1
0044de28  eb02                     jmp 0x44de2c
0044de2a  30c0                     xor al, al
0044de2c  84c0                     test al, al
0044de2e  0f8410050000             je 0x44e344
0044de34  31c0                     xor eax, eax
0044de36  6689d8                   mov ax, bx
0044de39  89c1                     mov ecx, eax
0044de3b  c1e104                   shl ecx, 4
0044de3e  01c1                     add ecx, eax
0044de40  c1e102                   shl ecx, 2
0044de43  01c1                     add ecx, eax
0044de45  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044de4a  8a542440                 mov dl, byte ptr [esp + 0x40]
0044de4e  88548802                 mov byte ptr [eax + ecx*4 + 2], dl
0044de52  663b1d04634900           cmp bx, word ptr [0x496304]
0044de59  0f85e5040000             jne 0x44e344
0044de5f  bfffff0000               mov edi, 0xffff
0044de64  30db                     xor bl, bl
0044de66  31d2                     xor edx, edx
0044de68  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044de6e  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044de74  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0044de7a  e9a4e4ffff               jmp 0x44c323
0044de7f  31c0                     xor eax, eax
0044de81  6689f8                   mov ax, di
0044de84  89c1                     mov ecx, eax
0044de86  c1e104                   shl ecx, 4
0044de89  01c1                     add ecx, eax
0044de8b  c1e102                   shl ecx, 2
0044de8e  01c1                     add ecx, eax
0044de90  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044de95  c1e102                   shl ecx, 2
0044de98  01c1                     add ecx, eax
0044de9a  31c0                     xor eax, eax
0044de9c  b307                     mov bl, 7
0044de9e  8a4102                   mov al, byte ptr [ecx + 2]
0044dea1  89fa                     mov edx, edi
0044dea3  85c0                     test eax, eax
0044dea5  7409                     je 0x44deb0
0044dea7  83f804                   cmp eax, 4
0044deaa  7404                     je 0x44deb0
0044deac  b001                     mov al, 1
0044deae  eb02                     jmp 0x44deb2
0044deb0  30c0                     xor al, al
0044deb2  84c0                     test al, al
0044deb4  0f848a040000             je 0x44e344
0044deba  31c0                     xor eax, eax
0044debc  6689d0                   mov ax, dx
0044debf  89c1                     mov ecx, eax
0044dec1  c1e104                   shl ecx, 4
0044dec4  01c1                     add ecx, eax
0044dec6  c1e102                   shl ecx, 2
0044dec9  01c1                     add ecx, eax
0044decb  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044ded0  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044ded4  668b1d04634900           mov bx, word ptr [0x496304]
0044dedb  6639da                   cmp dx, bx
0044dede  0f8560040000             jne 0x44e344
0044dee4  b9ffff0000               mov ecx, 0xffff
0044dee9  30e4                     xor ah, ah
0044deeb  30da                     xor dl, bl
0044deed  8825360f4e00             mov byte ptr [0x4e0f36], ah
0044def3  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044def9  31c0                     xor eax, eax
0044defb  66890d04634900           mov word ptr [0x496304], cx
0044df02  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044df07  e938040000               jmp 0x44e344
0044df0c  31c0                     xor eax, eax
0044df0e  8a8682000000             mov al, byte ptr [esi + 0x82]
0044df14  83f802                   cmp eax, 2
0044df17  0f85bf000000             jne 0x44dfdc
0044df1d  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044df23  c1f818                   sar eax, 0x18
0044df26  85c0                     test eax, eax
0044df28  7523                     jne 0x44df4d
0044df2a  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044df30  c1f818                   sar eax, 0x18
0044df33  85c0                     test eax, eax
0044df35  7516                     jne 0x44df4d
0044df37  31d2                     xor edx, edx
0044df39  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044df40  668b5608                 mov dx, word ptr [esi + 8]
0044df44  e8d658fdff               call 0x42381f
0044df49  84c0                     test al, al
0044df4b  7563                     jne 0x44dfb0
0044df4d  668b4608                 mov ax, word ptr [esi + 8]
0044df51  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044df55  0f85b6ddffff             jne 0x44bd11
0044df5b  31c0                     xor eax, eax
0044df5d  668b8680000000           mov ax, word ptr [esi + 0x80]
0044df64  e879cffcff               call 0x41aee2
0044df69  89c3                     mov ebx, eax
0044df6b  31c0                     xor eax, eax
0044df6d  6689f8                   mov ax, di
0044df70  89c1                     mov ecx, eax
0044df72  c1e104                   shl ecx, 4
0044df75  01c1                     add ecx, eax
0044df77  c1e102                   shl ecx, 2
0044df7a  01c1                     add ecx, eax
0044df7c  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044df82  c1e102                   shl ecx, 2
0044df85  01ca                     add edx, ecx
0044df87  66895a7e                 mov word ptr [edx + 0x7e], bx
0044df8b  663b3d04634900           cmp di, word ptr [0x496304]
0044df92  0f851ce9ffff             jne 0x44c8b4
0044df98  b9ffff0000               mov ecx, 0xffff
0044df9d  30c0                     xor al, al
0044df9f  31f6                     xor esi, esi
0044dfa1  a2360f4e00               mov byte ptr [0x4e0f36], al
0044dfa6  a2370f4e00               mov byte ptr [0x4e0f37], al
0044dfab  e951e7ffff               jmp 0x44c701
0044dfb0  31c0                     xor eax, eax
0044dfb2  8a4601                   mov al, byte ptr [esi + 1]
0044dfb5  89c1                     mov ecx, eax
0044dfb7  c1e102                   shl ecx, 2
0044dfba  29c1                     sub ecx, eax
0044dfbc  c1e103                   shl ecx, 3
0044dfbf  01c1                     add ecx, eax
0044dfc1  c6868900000003           mov byte ptr [esi + 0x89], 3
0044dfc8  31d2                     xor edx, edx
0044dfca  668b144dde654900         mov dx, word ptr [ecx*2 + 0x4965de]
0044dfd2  bb05000000               mov ebx, 5
0044dfd7  e966f5ffff               jmp 0x44d542
0044dfdc  31c0                     xor eax, eax
0044dfde  8a8682000000             mov al, byte ptr [esi + 0x82]
0044dfe4  83f801                   cmp eax, 1
0044dfe7  0f8557030000             jne 0x44e344
0044dfed  668b4608                 mov ax, word ptr [esi + 8]
0044dff1  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044dff5  0f8516ddffff             jne 0x44bd11
0044dffb  31d2                     xor edx, edx
0044dffd  668b9680000000           mov dx, word ptr [esi + 0x80]
0044e004  89d0                     mov eax, edx
0044e006  c1fa1f                   sar edx, 0x1f
0044e009  c1e208                   shl edx, 8
0044e00c  1bc2                     sbb eax, edx
0044e00e  c1f808                   sar eax, 8
0044e011  bb00010000               mov ebx, 0x100
0044e016  31d2                     xor edx, edx
0044e018  31c9                     xor ecx, ecx
0044e01a  668b9680000000           mov dx, word ptr [esi + 0x80]
0044e021  6689c1                   mov cx, ax
0044e024  89d0                     mov eax, edx
0044e026  c1fa1f                   sar edx, 0x1f
0044e029  f7fb                     idiv ebx
0044e02b  31db                     xor ebx, ebx
0044e02d  6689d3                   mov bx, dx
0044e030  31d2                     xor edx, edx
0044e032  668b5608                 mov dx, word ptr [esi + 8]
0044e036  89d0                     mov eax, edx
0044e038  c1fa1f                   sar edx, 0x1f
0044e03b  c1e208                   shl edx, 8
0044e03e  1bc2                     sbb eax, edx
0044e040  c1f808                   sar eax, 8
0044e043  0fb7e8                   movzx ebp, ax
0044e046  31d2                     xor edx, edx
0044e048  b800010000               mov eax, 0x100
0044e04d  668b5608                 mov dx, word ptr [esi + 8]
0044e051  89442404                 mov dword ptr [esp + 4], eax
0044e055  89d0                     mov eax, edx
0044e057  c1fa1f                   sar edx, 0x1f
0044e05a  f77c2404                 idiv dword ptr [esp + 4]
0044e05e  31c0                     xor eax, eax
0044e060  6689d0                   mov ax, dx
0044e063  89ea                     mov edx, ebp
0044e065  e8ebb40200               call 0x479555
0044e06a  83f810                   cmp eax, 0x10
0044e06d  0f83be000000             jae 0x44e131
0044e073  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e079  31d2                     xor edx, edx
0044e07b  0442                     add al, 0x42
0044e07d  88c2                     mov dl, al
0044e07f  31c0                     xor eax, eax
0044e081  668b4608                 mov ax, word ptr [esi + 8]
0044e085  e8d9760200               call 0x475763
0044e08a  84c0                     test al, al
0044e08c  7428                     je 0x44e0b6
0044e08e  668b4608                 mov ax, word ptr [esi + 8]
0044e092  66898680000000           mov word ptr [esi + 0x80], ax
0044e099  31c0                     xor eax, eax
0044e09b  8a4601                   mov al, byte ptr [esi + 1]
0044e09e  89c1                     mov ecx, eax
0044e0a0  c1e102                   shl ecx, 2
0044e0a3  29c1                     sub ecx, eax
0044e0a5  c1e103                   shl ecx, 3
0044e0a8  01c1                     add ecx, eax
0044e0aa  c6868900000003           mov byte ptr [esi + 0x89], 3
0044e0b1  e97df4ffff               jmp 0x44d533
0044e0b6  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e0bc  31d2                     xor edx, edx
0044e0be  0442                     add al, 0x42
0044e0c0  88c2                     mov dl, al
0044e0c2  31c0                     xor eax, eax
0044e0c4  668b8680000000           mov ax, word ptr [esi + 0x80]
0044e0cb  e8df760200               call 0x4757af
0044e0d0  31d2                     xor edx, edx
0044e0d2  6689c2                   mov dx, ax
0044e0d5  81faffff0000             cmp edx, 0xffff
0044e0db  0f8463020000             je 0x44e344
0044e0e1  89c3                     mov ebx, eax
0044e0e3  31c0                     xor eax, eax
0044e0e5  6689f8                   mov ax, di
0044e0e8  89c1                     mov ecx, eax
0044e0ea  c1e104                   shl ecx, 4
0044e0ed  01c1                     add ecx, eax
0044e0ef  c1e102                   shl ecx, 2
0044e0f2  01c1                     add ecx, eax
0044e0f4  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044e0fa  c1e102                   shl ecx, 2
0044e0fd  01ca                     add edx, ecx
0044e0ff  66895a7e                 mov word ptr [edx + 0x7e], bx
0044e103  663b3d04634900           cmp di, word ptr [0x496304]
0044e10a  0f85a4e7ffff             jne 0x44c8b4
0044e110  30c9                     xor cl, cl
0044e112  bfffff0000               mov edi, 0xffff
0044e117  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044e11d  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044e123  31c9                     xor ecx, ecx
0044e125  66893d04634900           mov word ptr [0x496304], di
0044e12c  e9b3ddffff               jmp 0x44bee4
0044e131  31d2                     xor edx, edx
0044e133  6689fa                   mov dx, di
0044e136  89d1                     mov ecx, edx
0044e138  c1e104                   shl ecx, 4
0044e13b  01d1                     add ecx, edx
0044e13d  c1e102                   shl ecx, 2
0044e140  01d1                     add ecx, edx
0044e142  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044e148  c1e102                   shl ecx, 2
0044e14b  01ca                     add edx, ecx
0044e14d  668b8680000000           mov ax, word ptr [esi + 0x80]
0044e154  6689427e                 mov word ptr [edx + 0x7e], ax
0044e158  663b3d04634900           cmp di, word ptr [0x496304]
0044e15f  0f854fe7ffff             jne 0x44c8b4
0044e165  30db                     xor bl, bl
0044e167  b9ffff0000               mov ecx, 0xffff
0044e16c  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044e172  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044e178  31db                     xor ebx, ebx
0044e17a  66890d04634900           mov word ptr [0x496304], cx
0044e181  e903ddffff               jmp 0x44be89
0044e186  8abe8b000000             mov bh, byte ptr [esi + 0x8b]
0044e18c  31c0                     xor eax, eax
0044e18e  fecf                     dec bh
0044e190  88f8                     mov al, bh
0044e192  88be8b000000             mov byte ptr [esi + 0x8b], bh
0044e198  85c0                     test eax, eax
0044e19a  0f85a4010000             jne 0x44e344
0044e1a0  bb01000000               mov ebx, 1
0044e1a5  ba02000000               mov edx, 2
0044e1aa  8d460a                   lea eax, [esi + 0xa]
0044e1ad  e80690ffff               call 0x4471b8
0044e1b2  25ffff0000               and eax, 0xffff
0044e1b7  7475                     je 0x44e22e
0044e1b9  31c0                     xor eax, eax
0044e1bb  8a8682000000             mov al, byte ptr [esi + 0x82]
0044e1c1  83f802                   cmp eax, 2
0044e1c4  7530                     jne 0x44e1f6
0044e1c6  ba01000000               mov edx, 1
0044e1cb  31c9                     xor ecx, ecx
0044e1cd  31db                     xor ebx, ebx
0044e1cf  89d0                     mov eax, edx
0044e1d1  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044e1d8  8a1e                     mov bl, byte ptr [esi]
0044e1da  e83052fdff               call 0x42340f
0044e1df  bb01000000               mov ebx, 1
0044e1e4  ba02000000               mov edx, 2
0044e1e9  8d460a                   lea eax, [esi + 0xa]
0044e1ec  e8f990ffff               call 0x4472ea
0044e1f1  e97fdfffff               jmp 0x44c175
0044e1f6  31c0                     xor eax, eax
0044e1f8  8a8682000000             mov al, byte ptr [esi + 0x82]
0044e1fe  83f801                   cmp eax, 1
0044e201  0f853d010000             jne 0x44e344
0044e207  89c3                     mov ebx, eax
0044e209  31c0                     xor eax, eax
0044e20b  ba02000000               mov edx, 2
0044e210  6689f8                   mov ax, di
0044e213  e8c056ffff               call 0x4438d8
0044e218  31c0                     xor eax, eax
0044e21a  8a4601                   mov al, byte ptr [esi + 1]
0044e21d  89c1                     mov ecx, eax
0044e21f  c1e102                   shl ecx, 2
0044e222  29c1                     sub ecx, eax
0044e224  c1e103                   shl ecx, 3
0044e227  01c1                     add ecx, eax
0044e229  e905f3ffff               jmp 0x44d533
0044e22e  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044e235  3dffff0000               cmp eax, 0xffff
0044e23a  7453                     je 0x44e28f
0044e23c  31d2                     xor edx, edx
0044e23e  6689fa                   mov dx, di
0044e241  89d1                     mov ecx, edx
0044e243  c1e104                   shl ecx, 4
0044e246  01d1                     add ecx, edx
0044e248  c1e102                   shl ecx, 2
0044e24b  c6868900000000           mov byte ptr [esi + 0x89], 0
0044e252  01d1                     add ecx, edx
0044e254  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044e25a  c1e102                   shl ecx, 2
0044e25d  01ca                     add edx, ecx
0044e25f  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044e266  6689427e                 mov word ptr [edx + 0x7e], ax
0044e26a  663b3d04634900           cmp di, word ptr [0x496304]
0044e271  0f853de6ffff             jne 0x44c8b4
0044e277  b9ffff0000               mov ecx, 0xffff
0044e27c  30c0                     xor al, al
0044e27e  31db                     xor ebx, ebx
0044e280  a2360f4e00               mov byte ptr [0x4e0f36], al
0044e285  a2370f4e00               mov byte ptr [0x4e0f37], al
0044e28a  e918e6ffff               jmp 0x44c8a7
0044e28f  89fa                     mov edx, edi
0044e291  31c0                     xor eax, eax
0044e293  6689d0                   mov ax, dx
0044e296  89c1                     mov ecx, eax
0044e298  c1e104                   shl ecx, 4
0044e29b  01c1                     add ecx, eax
0044e29d  c1e102                   shl ecx, 2
0044e2a0  01c1                     add ecx, eax
0044e2a2  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e2a7  b307                     mov bl, 7
0044e2a9  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044e2ad  25ff000000               and eax, 0xff
0044e2b2  7428                     je 0x44e2dc
0044e2b4  31c0                     xor eax, eax
0044e2b6  6689d0                   mov ax, dx
0044e2b9  89c1                     mov ecx, eax
0044e2bb  c1e104                   shl ecx, 4
0044e2be  01c1                     add ecx, eax
0044e2c0  c1e102                   shl ecx, 2
0044e2c3  01c1                     add ecx, eax
0044e2c5  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e2ca  8a448802                 mov al, byte ptr [eax + ecx*4 + 2]
0044e2ce  25ff000000               and eax, 0xff
0044e2d3  83f804                   cmp eax, 4
0044e2d6  7404                     je 0x44e2dc
0044e2d8  b001                     mov al, 1
0044e2da  eb02                     jmp 0x44e2de
0044e2dc  30c0                     xor al, al
0044e2de  84c0                     test al, al
0044e2e0  7462                     je 0x44e344
0044e2e2  31c0                     xor eax, eax
0044e2e4  6689f8                   mov ax, di
0044e2e7  89c1                     mov ecx, eax
0044e2e9  c1e104                   shl ecx, 4
0044e2ec  01c1                     add ecx, eax
0044e2ee  c1e102                   shl ecx, 2
0044e2f1  01c1                     add ecx, eax
0044e2f3  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e2f8  885c8802                 mov byte ptr [eax + ecx*4 + 2], bl
0044e2fc  663b3d04634900           cmp di, word ptr [0x496304]
0044e303  753f                     jne 0x44e344
0044e305  baffff0000               mov edx, 0xffff
0044e30a  30c9                     xor cl, cl
0044e30c  31c0                     xor eax, eax
0044e30e  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044e314  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044e31a  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044e31f  66891504634900           mov word ptr [0x496304], dx
0044e326  eb1c                     jmp 0x44e344
0044e328  8a8689000000             mov al, byte ptr [esi + 0x89]
0044e32e  3c03                     cmp al, 3
0044e330  7712                     ja 0x44e344
0044e332  25ff000000               and eax, 0xff
0044e337  2eff248564bc4400         jmp dword ptr cs:[eax*4 + 0x44bc64]
0044e33f  80fb05                   cmp bl, 5
0044e342  74e4                     je 0x44e328
0044e344  83c458                   add esp, 0x58
0044e347  e9510f0000               jmp 0x44f29d
