; BatimentNextEtape type-3 (CAVE) body 0x426aff..0x426c10; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00426aff  31d2                     xor edx, edx
00426b01  6689fa                   mov dx, di
00426b04  89d0                     mov eax, edx
00426b06  c1e004                   shl eax, 4
00426b09  01d0                     add eax, edx
00426b0b  c1e002                   shl eax, 2
00426b0e  b9c8a04900               mov ecx, 0x49a0c8
00426b13  01d0                     add eax, edx
00426b15  31d2                     xor edx, edx
00426b17  c1e002                   shl eax, 2
00426b1a  6689fa                   mov dx, di
00426b1d  01c1                     add ecx, eax
00426b1f  89d0                     mov eax, edx
00426b21  c1e004                   shl eax, 4
00426b24  01d0                     add eax, edx
00426b26  c1e002                   shl eax, 2
00426b29  01d0                     add eax, edx
00426b2b  bac8a04900               mov edx, 0x49a0c8
00426b30  89fb                     mov ebx, edi
00426b32  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426b36  25ff000000               and eax, 0xff
00426b3b  83f815                   cmp eax, 0x15
00426b3e  7510                     jne 0x426b50
00426b40  8d410c                   lea eax, [ecx + 0xc]
00426b43  e802070200               call 0x44724a
00426b48  84c0                     test al, al
00426b4a  744b                     je 0x426b97
00426b4c  b001                     mov al, 1
00426b4e  eb49                     jmp 0x426b99
00426b50  31d2                     xor edx, edx
00426b52  6689fa                   mov dx, di
00426b55  89d0                     mov eax, edx
00426b57  c1e004                   shl eax, 4
00426b5a  01d0                     add eax, edx
00426b5c  c1e002                   shl eax, 2
00426b5f  01d0                     add eax, edx
00426b61  bac8a04900               mov edx, 0x49a0c8
00426b66  8a448208                 mov al, byte ptr [edx + eax*4 + 8]
00426b6a  25ff000000               and eax, 0xff
00426b6f  83f802                   cmp eax, 2
00426b72  750c                     jne 0x426b80
00426b74  8d410c                   lea eax, [ecx + 0xc]
00426b77  e8ce060200               call 0x44724a
00426b7c  84c0                     test al, al
00426b7e  75cc                     jne 0x426b4c
00426b80  bb09000000               mov ebx, 9
00426b85  ba01000000               mov edx, 1
00426b8a  8d410c                   lea eax, [ecx + 0xc]
00426b8d  e826060200               call 0x4471b8
00426b92  6685c0                   test ax, ax
00426b95  ebb3                     jmp 0x426b4a
00426b97  30c0                     xor al, al
00426b99  84c0                     test al, al
00426b9b  0f841f160000             je 0x4281c0
00426ba1  31d2                     xor edx, edx
00426ba3  6689fa                   mov dx, di
00426ba6  89d0                     mov eax, edx
00426ba8  c1e004                   shl eax, 4
00426bab  01d0                     add eax, edx
00426bad  c1e002                   shl eax, 2
00426bb0  01d0                     add eax, edx
00426bb2  bec8a04900               mov esi, 0x49a0c8
00426bb7  c1e002                   shl eax, 2
00426bba  01c6                     add esi, eax
00426bbc  31c0                     xor eax, eax
00426bbe  8a4608                   mov al, byte ptr [esi + 8]
00426bc1  83f803                   cmp eax, 3
00426bc4  0f85f6150000             jne 0x4281c0
00426bca  f605808f500001           test byte ptr [0x508f80], 1
00426bd1  0f85e9150000             jne 0x4281c0
00426bd7  807e7500                 cmp byte ptr [esi + 0x75], 0
00426bdb  741a                     je 0x426bf7
00426bdd  31c0                     xor eax, eax
00426bdf  8a4676                   mov al, byte ptr [esi + 0x76]
00426be2  83f80f                   cmp eax, 0xf
00426be5  0f8dd5150000             jge 0x4281c0
00426beb  88c2                     mov dl, al
00426bed  fec2                     inc dl
00426bef  885676                   mov byte ptr [esi + 0x76], dl
00426bf2  e9c9150000               jmp 0x4281c0
00426bf7  31c0                     xor eax, eax
00426bf9  8a4676                   mov al, byte ptr [esi + 0x76]
00426bfc  85c0                     test eax, eax
00426bfe  0f84bc150000             je 0x4281c0
00426c04  88c4                     mov ah, al
00426c06  fecc                     dec ah
00426c08  886676                   mov byte ptr [esi + 0x76], ah
00426c0b  e9b0150000               jmp 0x4281c0
