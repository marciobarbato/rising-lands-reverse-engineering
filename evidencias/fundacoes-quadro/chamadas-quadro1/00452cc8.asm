00452cc8  53                   push ebx
00452cc9  51                   push ecx
00452cca  52                   push edx
00452ccb  56                   push esi
00452ccc  57                   push edi
00452ccd  89c7                 mov edi, eax
00452ccf  31d2                 xor edx, edx
00452cd1  6689c2               mov dx, ax
00452cd4  89d0                 mov eax, edx
00452cd6  c1e004               shl eax, 4
00452cd9  01d0                 add eax, edx
00452cdb  c1e002               shl eax, 2
00452cde  01d0                 add eax, edx
00452ce0  8b35a0194e00         mov esi, dword ptr [0x4e19a0]
00452ce6  c1e002               shl eax, 2
00452ce9  01c6                 add esi, eax
00452ceb  8a4672               mov al, byte ptr [esi + 0x72]
00452cee  84c0                 test al, al
00452cf0  750d                 jne 0x452cff
00452cf2  e961e0feff           jmp 0x440d58
00452cf7  b001                 mov al, 1
00452cf9  eb1a                 jmp 0x452d15
00452cfb  30c0                 xor al, al
00452cfd  eb16                 jmp 0x452d15
00452cff  8a4601               mov al, byte ptr [esi + 1]
00452d02  2c0b                 sub al, 0xb
00452d04  3c06                 cmp al, 6
00452d06  77f3                 ja 0x452cfb
00452d08  25ff000000           and eax, 0xff
00452d0d  2eff2485ac2c4500     jmp dword ptr cs:[eax*4 + 0x452cac]
00452d15  84c0                 test al, al
00452d17  0f853be0feff         jne 0x440d58
00452d1d  31db                 xor ebx, ebx
00452d1f  8a5e01               mov bl, byte ptr [esi + 1]
00452d22  89d8                 mov eax, ebx
00452d24  c1e002               shl eax, 2
00452d27  29d8                 sub eax, ebx
00452d29  c1e003               shl eax, 3
00452d2c  01d8                 add eax, ebx
00452d2e  668b0c45dc654900     mov cx, word ptr [eax*2 + 0x4965dc]
00452d36  30e4                 xor ah, ah
00452d38  8a86f8000000         mov al, byte ptr [esi + 0xf8]
00452d3e  89da                 mov edx, ebx
00452d40  01c1                 add ecx, eax
00452d42  31c0                 xor eax, eax
00452d44  31da                 xor edx, ebx
00452d46  8a06                 mov al, byte ptr [esi]
00452d48  e8735ffdff           call 0x428cc0
00452d4d  668b5674             mov dx, word ptr [esi + 0x74]
00452d51  42                   inc edx
00452d52  01c1                 add ecx, eax
00452d54  66895674             mov word ptr [esi + 0x74], dx
00452d58  6639d1               cmp cx, dx
00452d5b  0f87f7dffeff         ja 0x440d58
00452d61  31c0                 xor eax, eax
00452d63  668b4604             mov ax, word ptr [esi + 4]
00452d67  85c0                 test eax, eax
00452d69  0f8576010000         jne 0x452ee5
00452d6f  8a06                 mov al, byte ptr [esi]
00452d71  3a0541805000         cmp al, byte ptr [0x508041]
00452d77  7409                 je 0x452d82
00452d79  e9b1000000           jmp 0x452e2f
00452d7e  30c0                 xor al, al
00452d80  eb31                 jmp 0x452db3
00452d82  31d2                 xor edx, edx
00452d84  6689fa               mov dx, di
00452d87  89d0                 mov eax, edx
00452d89  c1e004               shl eax, 4
00452d8c  01d0                 add eax, edx
00452d8e  c1e002               shl eax, 2
00452d91  01d0                 add eax, edx
00452d93  8b15a0194e00         mov edx, dword ptr [0x4e19a0]
00452d99  8a448201             mov al, byte ptr [edx + eax*4 + 1]
00452d9d  3c03                 cmp al, 3
00452d9f  720c                 jb 0x452dad
00452da1  76db                 jbe 0x452d7e
00452da3  3c0a                 cmp al, 0xa
00452da5  720a                 jb 0x452db1
00452da7  76d5                 jbe 0x452d7e
00452da9  3c19                 cmp al, 0x19
00452dab  eb02                 jmp 0x452daf
00452dad  84c0                 test al, al
00452daf  74cd                 je 0x452d7e
00452db1  b001                 mov al, 1
00452db3  84c0                 test al, al
00452db5  0f8474000000         je 0x452e2f
00452dbb  663b4e74             cmp cx, word ptr [esi + 0x74]
00452dbf  756e                 jne 0x452e2f
00452dc1  31c9                 xor ecx, ecx
00452dc3  6689f9               mov cx, di
00452dc6  89c8                 mov eax, ecx
00452dc8  c1e004               shl eax, 4
00452dcb  01c8                 add eax, ecx
00452dcd  c1e002               shl eax, 2
00452dd0  8b1da0194e00         mov ebx, dword ptr [0x4e19a0]
00452dd6  01c8                 add eax, ecx
00452dd8  89ca                 mov edx, ecx
00452dda  c1e002               shl eax, 2
00452ddd  31ca                 xor edx, ecx
00452ddf  01c3                 add ebx, eax
00452de1  31c0                 xor eax, eax
00452de3  8a1541805000         mov dl, byte ptr [0x508041]
00452de9  668b4308             mov ax, word ptr [ebx + 8]
00452ded  e8fe380200           call 0x4766f0
00452df2  84c0                 test al, al
00452df4  7439                 je 0x452e2f
00452df6  89c8                 mov eax, ecx
00452df8  e860defeff           call 0x440c5d
00452dfd  8b9304010000         mov edx, dword ptr [ebx + 0x104]
00452e03  c683f900000000       mov byte ptr [ebx + 0xf9], 0
00452e0a  83faff               cmp edx, -1
00452e0d  7520                 jne 0x452e2f
00452e0f  50                   push eax
00452e10  31d2                 xor edx, edx
00452e12  31c9                 xor ecx, ecx
00452e14  8a5301               mov dl, byte ptr [ebx + 1]
00452e17  8d8304010000         lea eax, [ebx + 0x104]
00452e1d  c1e210               shl edx, 0x10
00452e20  89c3                 mov ebx, eax
00452e22  b850000000           mov eax, 0x50
00452e27  80ce0c               or dh, 0xc
00452e2a  e84a7c0300           call 0x48aa79
00452e2f  81e7ffff0000         and edi, 0xffff
00452e35  89f8                 mov eax, edi
00452e37  c1e004               shl eax, 4
00452e3a  01f8                 add eax, edi
00452e3c  c1e002               shl eax, 2
00452e3f  01f8                 add eax, edi
00452e41  8b0da0194e00         mov ecx, dword ptr [0x4e19a0]
00452e47  c1e002               shl eax, 2
00452e4a  01c1                 add ecx, eax
00452e4c  bb01000000           mov ebx, 1
00452e51  83c10a               add ecx, 0xa
00452e54  ba02000000           mov edx, 2
00452e59  89c8                 mov eax, ecx
00452e5b  e85843ffff           call 0x4471b8
00452e60  6685c0               test ax, ax
00452e63  7424                 je 0x452e89
00452e65  bb01000000           mov ebx, 1
00452e6a  ba02000000           mov edx, 2
00452e6f  89c8                 mov eax, ecx
00452e71  e87444ffff           call 0x4472ea
00452e76  668b4676             mov ax, word ptr [esi + 0x76]
00452e7a  66c746740000         mov word ptr [esi + 0x74], 0
00452e80  66894604             mov word ptr [esi + 4], ax
00452e84  e9cfdefeff           jmp 0x440d58
00452e89  31c0                 xor eax, eax
00452e8b  668b869a000000       mov ax, word ptr [esi + 0x9a]
00452e92  83f814               cmp eax, 0x14
00452e95  7f15                 jg 0x452eac
00452e97  89f8                 mov eax, edi
00452e99  66c7869a0000000000   mov word ptr [esi + 0x9a], 0
00452ea2  e8911affff           call 0x444938
00452ea7  e9acdefeff           jmp 0x440d58
00452eac  89c2                 mov edx, eax
00452eae  83ea14               sub edx, 0x14
00452eb1  6689969a000000       mov word ptr [esi + 0x9a], dx
00452eb8  31d2                 xor edx, edx
00452eba  8a5601               mov dl, byte ptr [esi + 1]
00452ebd  89d0                 mov eax, edx
00452ebf  c1e002               shl eax, 2
00452ec2  29d0                 sub eax, edx
00452ec4  c1e003               shl eax, 3
00452ec7  01d0                 add eax, edx
00452ec9  31d2                 xor edx, edx
00452ecb  668b1445dc654900     mov dx, word ptr [eax*2 + 0x4965dc]
00452ed3  89d0                 mov eax, edx
00452ed5  c1fa1f               sar edx, 0x1f
00452ed8  2bc2                 sub eax, edx
00452eda  d1f8                 sar eax, 1
00452edc  66894674             mov word ptr [esi + 0x74], ax
00452ee0  e973defeff           jmp 0x440d58
00452ee5  89c1                 mov ecx, eax
00452ee7  66c746740000         mov word ptr [esi + 0x74], 0
00452eed  49                   dec ecx
00452eee  66894e04             mov word ptr [esi + 4], cx
00452ef2  e961defeff           jmp 0x440d58
