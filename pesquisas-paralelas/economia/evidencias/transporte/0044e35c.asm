; CalculDechargeCaveEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044e35c  53                       push ebx
0044e35d  51                       push ecx
0044e35e  52                       push edx
0044e35f  56                       push esi
0044e360  57                       push edi
0044e361  55                       push ebp
0044e362  89e5                     mov ebp, esp
0044e364  83ec28                   sub esp, 0x28
0044e367  89c7                     mov edi, eax
0044e369  31c0                     xor eax, eax
0044e36b  6689f8                   mov ax, di
0044e36e  8945e8                   mov dword ptr [ebp - 0x18], eax
0044e371  89c3                     mov ebx, eax
0044e373  c1e004                   shl eax, 4
0044e376  01d8                     add eax, ebx
0044e378  c1e002                   shl eax, 2
0044e37b  01d8                     add eax, ebx
0044e37d  c1e002                   shl eax, 2
0044e380  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044e386  8945e4                   mov dword ptr [ebp - 0x1c], eax
0044e389  01c6                     add esi, eax
0044e38b  30e4                     xor ah, ah
0044e38d  8865fc                   mov byte ptr [ebp - 4], ah
0044e390  8a8689000000             mov al, byte ptr [esi + 0x89]
0044e396  3c03                     cmp al, 3
0044e398  0f87c2060000             ja 0x44ea60
0044e39e  25ff000000               and eax, 0xff
0044e3a3  2eff24854ce34400         jmp dword ptr cs:[eax*4 + 0x44e34c]
0044e3ab  b901000000               mov ecx, 1
0044e3b0  eb0e                     jmp 0x44e3c0
0044e3b2  b202                     mov dl, 2
0044e3b4  8d460a                   lea eax, [esi + 0xa]
0044e3b7  38d2                     cmp dl, dl
0044e3b9  76f0                     jbe 0x44e3ab
0044e3bb  80fa04                   cmp dl, 4
0044e3be  76eb                     jbe 0x44e3ab
0044e3c0  31db                     xor ebx, ebx
0044e3c2  31d2                     xor edx, edx
0044e3c4  6689cb                   mov bx, cx
0044e3c7  668b5066                 mov dx, word ptr [eax + 0x66]
0044e3cb  668b4002                 mov ax, word ptr [eax + 2]
0044e3cf  01da                     add edx, ebx
0044e3d1  25ffff0000               and eax, 0xffff
0044e3d6  39c2                     cmp edx, eax
0044e3d8  0f9ec0                   setle al
0044e3db  84c0                     test al, al
0044e3dd  7448                     je 0x44e427
0044e3df  668b4608                 mov ax, word ptr [esi + 8]
0044e3e3  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044e3e7  7426                     je 0x44e40f
0044e3e9  31d2                     xor edx, edx
0044e3eb  6689c2                   mov dx, ax
0044e3ee  31c0                     xor eax, eax
0044e3f0  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044e3f7  e82354fdff               call 0x42381f
0044e3fc  84c0                     test al, al
0044e3fe  750f                     jne 0x44e40f
0044e400  31c0                     xor eax, eax
0044e402  6689f8                   mov ax, di
0044e405  e802afffff               call 0x44930c
0044e40a  e951060000               jmp 0x44ea60
0044e40f  31d2                     xor edx, edx
0044e411  31c0                     xor eax, eax
0044e413  668b5608                 mov dx, word ptr [esi + 8]
0044e417  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044e41e  e8fc53fdff               call 0x42381f
0044e423  84c0                     test al, al
0044e425  7413                     je 0x44e43a
0044e427  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044e42e  c6868900000001           mov byte ptr [esi + 0x89], 1
0044e435  e926060000               jmp 0x44ea60
0044e43a  31db                     xor ebx, ebx
0044e43c  6689fb                   mov bx, di
0044e43f  89da                     mov edx, ebx
0044e441  31c0                     xor eax, eax
0044e443  c1e204                   shl edx, 4
0044e446  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044e44d  01da                     add edx, ebx
0044e44f  e88ecafcff               call 0x41aee2
0044e454  c1e202                   shl edx, 2
0044e457  89c6                     mov esi, eax
0044e459  01da                     add edx, ebx
0044e45b  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e460  c1e202                   shl edx, 2
0044e463  01d0                     add eax, edx
0044e465  6689707e                 mov word ptr [eax + 0x7e], si
0044e469  663b3d04634900           cmp di, word ptr [0x496304]
0044e470  7522                     jne 0x44e494
0044e472  b9ffff0000               mov ecx, 0xffff
0044e477  30d2                     xor dl, dl
0044e479  31f6                     xor esi, esi
0044e47b  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044e481  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044e487  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044e48d  66890d04634900           mov word ptr [0x496304], cx
0044e494  c6808800000000           mov byte ptr [eax + 0x88], 0
0044e49b  e9c0050000               jmp 0x44ea60
0044e4a0  c745f401000000           mov dword ptr [ebp - 0xc], 1
0044e4a7  eb0e                     jmp 0x44e4b7
0044e4a9  b202                     mov dl, 2
0044e4ab  8d460a                   lea eax, [esi + 0xa]
0044e4ae  38d2                     cmp dl, dl
0044e4b0  76ee                     jbe 0x44e4a0
0044e4b2  80fa04                   cmp dl, 4
0044e4b5  76e9                     jbe 0x44e4a0
0044e4b7  31db                     xor ebx, ebx
0044e4b9  31d2                     xor edx, edx
0044e4bb  668b5df4                 mov bx, word ptr [ebp - 0xc]
0044e4bf  668b5066                 mov dx, word ptr [eax + 0x66]
0044e4c3  668b4002                 mov ax, word ptr [eax + 2]
0044e4c7  01da                     add edx, ebx
0044e4c9  25ffff0000               and eax, 0xffff
0044e4ce  39c2                     cmp edx, eax
0044e4d0  0f9ec0                   setle al
0044e4d3  84c0                     test al, al
0044e4d5  0f84c6000000             je 0x44e5a1
0044e4db  8a8e8b000000             mov cl, byte ptr [esi + 0x8b]
0044e4e1  31c0                     xor eax, eax
0044e4e3  fec9                     dec cl
0044e4e5  88c8                     mov al, cl
0044e4e7  888e8b000000             mov byte ptr [esi + 0x8b], cl
0044e4ed  85c0                     test eax, eax
0044e4ef  0f85b0000000             jne 0x44e5a5
0044e4f5  8a06                     mov al, byte ptr [esi]
0044e4f7  50                       push eax
0044e4f8  31c0                     xor eax, eax
0044e4fa  668b8684000000           mov ax, word ptr [esi + 0x84]
0044e501  31c9                     xor ecx, ecx
0044e503  85c0                     test eax, eax
0044e505  0f94c0                   sete al
0044e508  25ff000000               and eax, 0xff
0044e50d  31db                     xor ebx, ebx
0044e50f  6689c3                   mov bx, ax
0044e512  31c0                     xor eax, eax
0044e514  668b8684000000           mov ax, word ptr [esi + 0x84]
0044e51b  83f802                   cmp eax, 2
0044e51e  0f94c0                   sete al
0044e521  25ff000000               and eax, 0xff
0044e526  31d2                     xor edx, edx
0044e528  6689c2                   mov dx, ax
0044e52b  31c0                     xor eax, eax
0044e52d  668b8684000000           mov ax, word ptr [esi + 0x84]
0044e534  83f801                   cmp eax, 1
0044e537  0f9445f8                 sete byte ptr [ebp - 8]
0044e53b  31c0                     xor eax, eax
0044e53d  8a45f8                   mov al, byte ptr [ebp - 8]
0044e540  8945f0                   mov dword ptr [ebp - 0x10], eax
0044e543  8b45f0                   mov eax, dword ptr [ebp - 0x10]
0044e546  25ffff0000               and eax, 0xffff
0044e54b  e895910100               call 0x4676e5
0044e550  84c0                     test al, al
0044e552  7451                     je 0x44e5a5
0044e554  ba01000000               mov edx, 1
0044e559  31db                     xor ebx, ebx
0044e55b  31c0                     xor eax, eax
0044e55d  8a1e                     mov bl, byte ptr [esi]
0044e55f  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e565  e85350fdff               call 0x4235bd
0044e56a  8d460a                   lea eax, [esi + 0xa]
0044e56d  668b5866                 mov bx, word ptr [eax + 0x66]
0044e571  668b8e84000000           mov cx, word ptr [esi + 0x84]
0044e578  43                       inc ebx
0044e579  668b10                   mov dx, word ptr [eax]
0044e57c  66895866                 mov word ptr [eax + 0x66], bx
0044e580  81e2ffff0000             and edx, 0xffff
0044e586  c644024202               mov byte ptr [edx + eax + 0x42], 2
0044e58b  66894c5006               mov word ptr [eax + edx*2 + 6], cx
0044e590  66ff00                   inc word ptr [eax]
0044e593  30ed                     xor ch, ch
0044e595  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044e59c  886dfc                   mov byte ptr [ebp - 4], ch
0044e59f  eb04                     jmp 0x44e5a5
0044e5a1  c645fc01                 mov byte ptr [ebp - 4], 1
0044e5a5  807dfc00                 cmp byte ptr [ebp - 4], 0
0044e5a9  0f84b1040000             je 0x44ea60
0044e5af  31c0                     xor eax, eax
0044e5b1  8a8682000000             mov al, byte ptr [esi + 0x82]
0044e5b7  83f802                   cmp eax, 2
0044e5ba  0f85f9000000             jne 0x44e6b9
0044e5c0  31c0                     xor eax, eax
0044e5c2  668b8680000000           mov ax, word ptr [esi + 0x80]
0044e5c9  3dffff0000               cmp eax, 0xffff
0044e5ce  745f                     je 0x44e62f
0044e5d0  31db                     xor ebx, ebx
0044e5d2  e80bc9fcff               call 0x41aee2
0044e5d7  6689fb                   mov bx, di
0044e5da  89c2                     mov edx, eax
0044e5dc  89d8                     mov eax, ebx
0044e5de  c1e004                   shl eax, 4
0044e5e1  01d8                     add eax, ebx
0044e5e3  c1e002                   shl eax, 2
0044e5e6  c6868900000002           mov byte ptr [esi + 0x89], 2
0044e5ed  01d8                     add eax, ebx
0044e5ef  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044e5f5  c1e002                   shl eax, 2
0044e5f8  01d8                     add eax, ebx
0044e5fa  6689507e                 mov word ptr [eax + 0x7e], dx
0044e5fe  663b3d04634900           cmp di, word ptr [0x496304]
0044e605  0f8589feffff             jne 0x44e494
0044e60b  30c9                     xor cl, cl
0044e60d  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044e613  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044e619  31c9                     xor ecx, ecx
0044e61b  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044e621  66c70504634900ffff       mov word ptr [0x496304], 0xffff
0044e62a  e965feffff               jmp 0x44e494
0044e62f  31db                     xor ebx, ebx
0044e631  6689fb                   mov bx, di
0044e634  89d8                     mov eax, ebx
0044e636  c1e004                   shl eax, 4
0044e639  01d8                     add eax, ebx
0044e63b  c1e002                   shl eax, 2
0044e63e  b107                     mov cl, 7
0044e640  01c3                     add ebx, eax
0044e642  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e647  c1e302                   shl ebx, 2
0044e64a  89fa                     mov edx, edi
0044e64c  8a440302                 mov al, byte ptr [ebx + eax + 2]
0044e650  25ff000000               and eax, 0xff
0044e655  7409                     je 0x44e660
0044e657  83f804                   cmp eax, 4
0044e65a  7404                     je 0x44e660
0044e65c  b001                     mov al, 1
0044e65e  eb02                     jmp 0x44e662
0044e660  30c0                     xor al, al
0044e662  84c0                     test al, al
0044e664  0f84f6030000             je 0x44ea60
0044e66a  31db                     xor ebx, ebx
0044e66c  6689d3                   mov bx, dx
0044e66f  89d8                     mov eax, ebx
0044e671  c1e004                   shl eax, 4
0044e674  01d8                     add eax, ebx
0044e676  c1e002                   shl eax, 2
0044e679  01d8                     add eax, ebx
0044e67b  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044e681  884c8302                 mov byte ptr [ebx + eax*4 + 2], cl
0044e685  663b1504634900           cmp dx, word ptr [0x496304]
0044e68c  0f85ce030000             jne 0x44ea60
0044e692  30db                     xor bl, bl
0044e694  baffff0000               mov edx, 0xffff
0044e699  881d360f4e00             mov byte ptr [0x4e0f36], bl
0044e69f  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044e6a5  31db                     xor ebx, ebx
0044e6a7  66891504634900           mov word ptr [0x496304], dx
0044e6ae  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044e6b4  e9a7030000               jmp 0x44ea60
0044e6b9  83f801                   cmp eax, 1
0044e6bc  0f859e030000             jne 0x44ea60
0044e6c2  31db                     xor ebx, ebx
0044e6c4  6689fb                   mov bx, di
0044e6c7  89d8                     mov eax, ebx
0044e6c9  c1e004                   shl eax, 4
0044e6cc  01d8                     add eax, ebx
0044e6ce  c1e002                   shl eax, 2
0044e6d1  c6868900000002           mov byte ptr [esi + 0x89], 2
0044e6d8  01c3                     add ebx, eax
0044e6da  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e6df  c1e302                   shl ebx, 2
0044e6e2  01d8                     add eax, ebx
0044e6e4  668b9680000000           mov dx, word ptr [esi + 0x80]
0044e6eb  6689507e                 mov word ptr [eax + 0x7e], dx
0044e6ef  663b3d04634900           cmp di, word ptr [0x496304]
0044e6f6  0f8598fdffff             jne 0x44e494
0044e6fc  30d2                     xor dl, dl
0044e6fe  bfffff0000               mov edi, 0xffff
0044e703  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044e709  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044e70f  31d2                     xor edx, edx
0044e711  66893d04634900           mov word ptr [0x496304], di
0044e718  89153c0f4e00             mov dword ptr [0x4e0f3c], edx
0044e71e  e971fdffff               jmp 0x44e494
0044e723  31c0                     xor eax, eax
0044e725  8a8682000000             mov al, byte ptr [esi + 0x82]
0044e72b  83f802                   cmp eax, 2
0044e72e  7556                     jne 0x44e786
0044e730  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044e736  c1f818                   sar eax, 0x18
0044e739  85c0                     test eax, eax
0044e73b  0f85bffcffff             jne 0x44e400
0044e741  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044e747  c1f818                   sar eax, 0x18
0044e74a  85c0                     test eax, eax
0044e74c  0f85aefcffff             jne 0x44e400
0044e752  31d2                     xor edx, edx
0044e754  668b8680000000           mov ax, word ptr [esi + 0x80]
0044e75b  668b5608                 mov dx, word ptr [esi + 8]
0044e75f  e8bb50fdff               call 0x42381f
0044e764  84c0                     test al, al
0044e766  0f8494fcffff             je 0x44e400
0044e76c  89d8                     mov eax, ebx
0044e76e  e8d53e0200               call 0x472648
0044e773  c6868900000003           mov byte ptr [esi + 0x89], 3
0044e77a  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044e781  e9da020000               jmp 0x44ea60
0044e786  83f801                   cmp eax, 1
0044e789  0f85d1020000             jne 0x44ea60
0044e78f  668b4608                 mov ax, word ptr [esi + 8]
0044e793  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044e797  7407                     je 0x44e7a0
0044e799  89d8                     mov eax, ebx
0044e79b  e965fcffff               jmp 0x44e405
0044e7a0  31db                     xor ebx, ebx
0044e7a2  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044e7a9  89da                     mov edx, ebx
0044e7ab  89d8                     mov eax, ebx
0044e7ad  c1fa1f                   sar edx, 0x1f
0044e7b0  c1e208                   shl edx, 8
0044e7b3  1bc2                     sbb eax, edx
0044e7b5  c1f808                   sar eax, 8
0044e7b8  31c9                     xor ecx, ecx
0044e7ba  6689c1                   mov cx, ax
0044e7bd  89da                     mov edx, ebx
0044e7bf  b800010000               mov eax, 0x100
0044e7c4  c1fa1f                   sar edx, 0x1f
0044e7c7  8945ec                   mov dword ptr [ebp - 0x14], eax
0044e7ca  89d8                     mov eax, ebx
0044e7cc  f77dec                   idiv dword ptr [ebp - 0x14]
0044e7cf  31c0                     xor eax, eax
0044e7d1  31db                     xor ebx, ebx
0044e7d3  6689d0                   mov ax, dx
0044e7d6  668b5e08                 mov bx, word ptr [esi + 8]
0044e7da  8945dc                   mov dword ptr [ebp - 0x24], eax
0044e7dd  89da                     mov edx, ebx
0044e7df  89d8                     mov eax, ebx
0044e7e1  c1fa1f                   sar edx, 0x1f
0044e7e4  c1e208                   shl edx, 8
0044e7e7  1bc2                     sbb eax, edx
0044e7e9  c1f808                   sar eax, 8
0044e7ec  25ffff0000               and eax, 0xffff
0044e7f1  89da                     mov edx, ebx
0044e7f3  8945e0                   mov dword ptr [ebp - 0x20], eax
0044e7f6  b800010000               mov eax, 0x100
0044e7fb  c1fa1f                   sar edx, 0x1f
0044e7fe  8945ec                   mov dword ptr [ebp - 0x14], eax
0044e801  89d8                     mov eax, ebx
0044e803  f77dec                   idiv dword ptr [ebp - 0x14]
0044e806  31c0                     xor eax, eax
0044e808  8b5ddc                   mov ebx, dword ptr [ebp - 0x24]
0044e80b  6689d0                   mov ax, dx
0044e80e  8b55e0                   mov edx, dword ptr [ebp - 0x20]
0044e811  e83fad0200               call 0x479555
0044e816  83f810                   cmp eax, 0x10
0044e819  0f8790000000             ja 0x44e8af
0044e81f  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e825  31d2                     xor edx, edx
0044e827  0442                     add al, 0x42
0044e829  88c2                     mov dl, al
0044e82b  31c0                     xor eax, eax
0044e82d  668b4608                 mov ax, word ptr [esi + 8]
0044e831  e82d6f0200               call 0x475763
0044e836  84c0                     test al, al
0044e838  0f8535ffffff             jne 0x44e773
0044e83e  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e844  31d2                     xor edx, edx
0044e846  0442                     add al, 0x42
0044e848  88c2                     mov dl, al
0044e84a  31c0                     xor eax, eax
0044e84c  8b5de8                   mov ebx, dword ptr [ebp - 0x18]
0044e84f  668b8680000000           mov ax, word ptr [esi + 0x80]
0044e856  e8a3730200               call 0x475bfe
0044e85b  89c3                     mov ebx, eax
0044e85d  31c0                     xor eax, eax
0044e85f  6689d8                   mov ax, bx
0044e862  3dffff0000               cmp eax, 0xffff
0044e867  0f84f3010000             je 0x44ea60
0044e86d  8b55e4                   mov edx, dword ptr [ebp - 0x1c]
0044e870  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e875  01d0                     add eax, edx
0044e877  6689587e                 mov word ptr [eax + 0x7e], bx
0044e87b  663b3d04634900           cmp di, word ptr [0x496304]
0044e882  0f850cfcffff             jne 0x44e494
0044e888  bfffff0000               mov edi, 0xffff
0044e88d  30f6                     xor dh, dh
0044e88f  31db                     xor ebx, ebx
0044e891  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044e897  8835370f4e00             mov byte ptr [0x4e0f37], dh
0044e89d  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044e8a3  66893d04634900           mov word ptr [0x496304], di
0044e8aa  e9e5fbffff               jmp 0x44e494
0044e8af  8b4de4                   mov ecx, dword ptr [ebp - 0x1c]
0044e8b2  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e8b7  01c8                     add eax, ecx
0044e8b9  668b9680000000           mov dx, word ptr [esi + 0x80]
0044e8c0  6689507e                 mov word ptr [eax + 0x7e], dx
0044e8c4  663b3d04634900           cmp di, word ptr [0x496304]
0044e8cb  0f85c3fbffff             jne 0x44e494
0044e8d1  30ed                     xor ch, ch
0044e8d3  31f6                     xor esi, esi
0044e8d5  882d360f4e00             mov byte ptr [0x4e0f36], ch
0044e8db  882d370f4e00             mov byte ptr [0x4e0f37], ch
0044e8e1  b9ffff0000               mov ecx, 0xffff
0044e8e6  e99cfbffff               jmp 0x44e487
0044e8eb  8a968b000000             mov dl, byte ptr [esi + 0x8b]
0044e8f1  31c0                     xor eax, eax
0044e8f3  feca                     dec dl
0044e8f5  88d0                     mov al, dl
0044e8f7  88968b000000             mov byte ptr [esi + 0x8b], dl
0044e8fd  85c0                     test eax, eax
0044e8ff  0f855b010000             jne 0x44ea60
0044e905  ba02000000               mov edx, 2
0044e90a  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044e911  31db                     xor ebx, ebx
0044e913  8d460a                   lea eax, [esi + 0xa]
0044e916  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044e91d  8945d8                   mov dword ptr [ebp - 0x28], eax
0044e920  e89388ffff               call 0x4471b8
0044e925  25ffff0000               and eax, 0xffff
0044e92a  746b                     je 0x44e997
0044e92c  31c0                     xor eax, eax
0044e92e  8a8682000000             mov al, byte ptr [esi + 0x82]
0044e934  83f802                   cmp eax, 2
0044e937  753a                     jne 0x44e973
0044e939  ba01000000               mov edx, 1
0044e93e  31c9                     xor ecx, ecx
0044e940  31db                     xor ebx, ebx
0044e942  31c0                     xor eax, eax
0044e944  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044e94b  8a1e                     mov bl, byte ptr [esi]
0044e94d  8a8684000000             mov al, byte ptr [esi + 0x84]
0044e953  e8b74afdff               call 0x42340f
0044e958  ba02000000               mov edx, 2
0044e95d  31db                     xor ebx, ebx
0044e95f  8b45d8                   mov eax, dword ptr [ebp - 0x28]
0044e962  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044e969  e87c89ffff               call 0x4472ea
0044e96e  e9ed000000               jmp 0x44ea60
0044e973  83f801                   cmp eax, 1
0044e976  0f85e4000000             jne 0x44ea60
0044e97c  ba02000000               mov edx, 2
0044e981  31db                     xor ebx, ebx
0044e983  8b45e8                   mov eax, dword ptr [ebp - 0x18]
0044e986  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044e98d  e8464fffff               call 0x4438d8
0044e992  e9c9000000               jmp 0x44ea60
0044e997  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044e99e  3dffff0000               cmp eax, 0xffff
0044e9a3  7450                     je 0x44e9f5
0044e9a5  c6868900000000           mov byte ptr [esi + 0x89], 0
0044e9ac  668b96b2000000           mov dx, word ptr [esi + 0xb2]
0044e9b3  8b75e4                   mov esi, dword ptr [ebp - 0x1c]
0044e9b6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e9bb  01f0                     add eax, esi
0044e9bd  6689507e                 mov word ptr [eax + 0x7e], dx
0044e9c1  663b3d04634900           cmp di, word ptr [0x496304]
0044e9c8  0f85c6faffff             jne 0x44e494
0044e9ce  beffff0000               mov esi, 0xffff
0044e9d3  30ff                     xor bh, bh
0044e9d5  31ff                     xor edi, edi
0044e9d7  883d360f4e00             mov byte ptr [0x4e0f36], bh
0044e9dd  883d370f4e00             mov byte ptr [0x4e0f37], bh
0044e9e3  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044e9e9  66893504634900           mov word ptr [0x496304], si
0044e9f0  e99ffaffff               jmp 0x44e494
0044e9f5  8b5de4                   mov ebx, dword ptr [ebp - 0x1c]
0044e9f8  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044e9fd  01d8                     add eax, ebx
0044e9ff  b107                     mov cl, 7
0044ea01  8a4002                   mov al, byte ptr [eax + 2]
0044ea04  25ff000000               and eax, 0xff
0044ea09  7409                     je 0x44ea14
0044ea0b  83f804                   cmp eax, 4
0044ea0e  7404                     je 0x44ea14
0044ea10  b001                     mov al, 1
0044ea12  eb02                     jmp 0x44ea16
0044ea14  30c0                     xor al, al
0044ea16  84c0                     test al, al
0044ea18  7446                     je 0x44ea60
0044ea1a  31db                     xor ebx, ebx
0044ea1c  6689fb                   mov bx, di
0044ea1f  89d8                     mov eax, ebx
0044ea21  c1e004                   shl eax, 4
0044ea24  01d8                     add eax, ebx
0044ea26  c1e002                   shl eax, 2
0044ea29  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
0044ea2f  01d8                     add eax, ebx
0044ea31  884c8202                 mov byte ptr [edx + eax*4 + 2], cl
0044ea35  663b3d04634900           cmp di, word ptr [0x496304]
0044ea3c  7522                     jne 0x44ea60
0044ea3e  bbffff0000               mov ebx, 0xffff
0044ea43  30f6                     xor dh, dh
0044ea45  31c9                     xor ecx, ecx
0044ea47  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044ea4d  8835370f4e00             mov byte ptr [0x4e0f37], dh
0044ea53  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044ea59  66891d04634900           mov word ptr [0x496304], bx
0044ea60  89ec                     mov esp, ebp
0044ea62  e936080000               jmp 0x44f29d
