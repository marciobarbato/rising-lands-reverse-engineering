; EnginCalculTransporte and shared epilogue; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044ea78  53                       push ebx
0044ea79  51                       push ecx
0044ea7a  52                       push edx
0044ea7b  56                       push esi
0044ea7c  57                       push edi
0044ea7d  55                       push ebp
0044ea7e  83ec14                   sub esp, 0x14
0044ea81  89c7                     mov edi, eax
0044ea83  0fb7e8                   movzx ebp, ax
0044ea86  89ee                     mov esi, ebp
0044ea88  c1e604                   shl esi, 4
0044ea8b  01ee                     add esi, ebp
0044ea8d  c1e602                   shl esi, 2
0044ea90  01ee                     add esi, ebp
0044ea92  c1e602                   shl esi, 2
0044ea95  893424                   mov dword ptr [esp], esi
0044ea98  8b1424                   mov edx, dword ptr [esp]
0044ea9b  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
0044eaa1  30e4                     xor ah, ah
0044eaa3  01d6                     add esi, edx
0044eaa5  88642410                 mov byte ptr [esp + 0x10], ah
0044eaa9  8a8689000000             mov al, byte ptr [esi + 0x89]
0044eaaf  3c03                     cmp al, 3
0044eab1  0f87e3070000             ja 0x44f29a
0044eab7  25ff000000               and eax, 0xff
0044eabc  2eff248568ea4400         jmp dword ptr cs:[eax*4 + 0x44ea68]
0044eac4  8d5e0a                   lea ebx, [esi + 0xa]
0044eac7  31d2                     xor edx, edx
0044eac9  31c0                     xor eax, eax
0044eacb  668b5366                 mov dx, word ptr [ebx + 0x66]
0044eacf  668b4302                 mov ax, word ptr [ebx + 2]
0044ead3  42                       inc edx
0044ead4  39c2                     cmp edx, eax
0044ead6  0f9ec0                   setle al
0044ead9  84c0                     test al, al
0044eadb  0f84e8000000             je 0x44ebc9
0044eae1  668b467e                 mov ax, word ptr [esi + 0x7e]
0044eae5  668b5e08                 mov bx, word ptr [esi + 8]
0044eae9  6639d8                   cmp ax, bx
0044eaec  740f                     je 0x44eafd
0044eaee  31c0                     xor eax, eax
0044eaf0  6689f8                   mov ax, di
0044eaf3  e814a8ffff               call 0x44930c
0044eaf8  e99d070000               jmp 0x44f29a
0044eafd  31c0                     xor eax, eax
0044eaff  31d2                     xor edx, edx
0044eb01  6689d8                   mov ax, bx
0044eb04  668b9684000000           mov dx, word ptr [esi + 0x84]
0044eb0b  e828750200               call 0x476038
0044eb10  25ff000000               and eax, 0xff
0044eb15  39d0                     cmp eax, edx
0044eb17  751a                     jne 0x44eb33
0044eb19  c6868900000001           mov byte ptr [esi + 0x89], 1
0044eb20  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044eb27  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044eb2e  e967070000               jmp 0x44f29a
0044eb33  ba05000000               mov edx, 5
0044eb38  0fb7ef                   movzx ebp, di
0044eb3b  8a8684000000             mov al, byte ptr [esi + 0x84]
0044eb41  31db                     xor ebx, ebx
0044eb43  0442                     add al, 0x42
0044eb45  55                       push ebp
0044eb46  88c3                     mov bl, al
0044eb48  31c0                     xor eax, eax
0044eb4a  89d9                     mov ecx, ebx
0044eb4c  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044eb53  e81c900200               call 0x477b74
0044eb58  31d2                     xor edx, edx
0044eb5a  6689c2                   mov dx, ax
0044eb5d  81faffff0000             cmp edx, 0xffff
0044eb63  7452                     je 0x44ebb7
0044eb65  89ee                     mov esi, ebp
0044eb67  c1e604                   shl esi, 4
0044eb6a  01ee                     add esi, ebp
0044eb6c  c1e602                   shl esi, 2
0044eb6f  01ee                     add esi, ebp
0044eb71  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044eb77  c1e602                   shl esi, 2
0044eb7a  01f3                     add ebx, esi
0044eb7c  6689437e                 mov word ptr [ebx + 0x7e], ax
0044eb80  663b3d04634900           cmp di, word ptr [0x496304]
0044eb87  7522                     jne 0x44ebab
0044eb89  beffff0000               mov esi, 0xffff
0044eb8e  30c9                     xor cl, cl
0044eb90  31ed                     xor ebp, ebp
0044eb92  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044eb98  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044eb9e  892d3c0f4e00             mov dword ptr [0x4e0f3c], ebp
0044eba4  66893504634900           mov word ptr [0x496304], si
0044ebab  c6838800000000           mov byte ptr [ebx + 0x88], 0
0044ebb2  e9e3060000               jmp 0x44f29a
0044ebb7  31d2                     xor edx, edx
0044ebb9  89e8                     mov eax, ebp
0044ebbb  668b567c                 mov dx, word ptr [esi + 0x7c]
0044ebbf  e80f6cffff               call 0x4457d3
0044ebc4  e9d1060000               jmp 0x44f29a
0044ebc9  c6868900000001           mov byte ptr [esi + 0x89], 1
0044ebd0  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044ebd7  8886a4000000             mov byte ptr [esi + 0xa4], al
0044ebdd  e9b8060000               jmp 0x44f29a
0044ebe2  8d5e0a                   lea ebx, [esi + 0xa]
0044ebe5  31c0                     xor eax, eax
0044ebe7  668b4366                 mov ax, word ptr [ebx + 0x66]
0044ebeb  8d5001                   lea edx, [eax + 1]
0044ebee  31c0                     xor eax, eax
0044ebf0  668b4302                 mov ax, word ptr [ebx + 2]
0044ebf4  39c2                     cmp edx, eax
0044ebf6  0f9ec0                   setle al
0044ebf9  84c0                     test al, al
0044ebfb  0f8444010000             je 0x44ed45
0044ec01  fe8e8b000000             dec byte ptr [esi + 0x8b]
0044ec07  31c0                     xor eax, eax
0044ec09  8a868b000000             mov al, byte ptr [esi + 0x8b]
0044ec0f  85c0                     test eax, eax
0044ec11  0f8533010000             jne 0x44ed4a
0044ec17  668b4608                 mov ax, word ptr [esi + 8]
0044ec1b  e8427a0200               call 0x476662
0044ec20  8d6e0a                   lea ebp, [esi + 0xa]
0044ec23  30ff                     xor bh, bh
0044ec25  31d2                     xor edx, edx
0044ec27  88c3                     mov bl, al
0044ec29  668b4d66                 mov cx, word ptr [ebp + 0x66]
0044ec2d  668b4500                 mov ax, word ptr [ebp]
0044ec31  41                       inc ecx
0044ec32  6689c2                   mov dx, ax
0044ec35  66894d66                 mov word ptr [ebp + 0x66], cx
0044ec39  89d0                     mov eax, edx
0044ec3b  c6442a4202               mov byte ptr [edx + ebp + 0x42], 2
0044ec40  66895c4506               mov word ptr [ebp + eax*2 + 6], bx
0044ec45  668b4500                 mov ax, word ptr [ebp]
0044ec49  40                       inc eax
0044ec4a  31c9                     xor ecx, ecx
0044ec4c  66894500                 mov word ptr [ebp], ax
0044ec50  31c0                     xor eax, eax
0044ec52  ba05000000               mov edx, 5
0044ec57  6689f8                   mov ax, di
0044ec5a  89542404                 mov dword ptr [esp + 4], edx
0044ec5e  50                       push eax
0044ec5f  8a8684000000             mov al, byte ptr [esi + 0x84]
0044ec65  31db                     xor ebx, ebx
0044ec67  0442                     add al, 0x42
0044ec69  31d2                     xor edx, edx
0044ec6b  88c3                     mov bl, al
0044ec6d  b81d000000               mov eax, 0x1d
0044ec72  668b4e08                 mov cx, word ptr [esi + 8]
0044ec76  e861180200               call 0x4704dc
0044ec7b  f7742408                 div dword ptr [esp + 8]
0044ec7f  01d1                     add ecx, edx
0044ec81  b81e000000               mov eax, 0x1e
0044ec86  894c2408                 mov dword ptr [esp + 8], ecx
0044ec8a  31d2                     xor edx, edx
0044ec8c  b905000000               mov ecx, 5
0044ec91  e846180200               call 0x4704dc
0044ec96  f7f1                     div ecx
0044ec98  c1e208                   shl edx, 8
0044ec9b  8b442408                 mov eax, dword ptr [esp + 8]
0044ec9f  81ea00020000             sub edx, 0x200
0044eca5  83e802                   sub eax, 2
0044eca8  01d0                     add eax, edx
0044ecaa  ba05000000               mov edx, 5
0044ecaf  25ffff0000               and eax, 0xffff
0044ecb4  89d9                     mov ecx, ebx
0044ecb6  e8b98e0200               call 0x477b74
0044ecbb  89c1                     mov ecx, eax
0044ecbd  25ffff0000               and eax, 0xffff
0044ecc2  3dffff0000               cmp eax, 0xffff
0044ecc7  0f8478000000             je 0x44ed45
0044eccd  31c0                     xor eax, eax
0044eccf  31d2                     xor edx, edx
0044ecd1  668b4566                 mov ax, word ptr [ebp + 0x66]
0044ecd5  668b5502                 mov dx, word ptr [ebp + 2]
0044ecd9  40                       inc eax
0044ecda  39d0                     cmp eax, edx
0044ecdc  0f9ec0                   setle al
0044ecdf  84c0                     test al, al
0044ece1  7462                     je 0x44ed45
0044ece3  31c0                     xor eax, eax
0044ece5  6689f8                   mov ax, di
0044ece8  89c5                     mov ebp, eax
0044ecea  c1e504                   shl ebp, 4
0044eced  01c5                     add ebp, eax
0044ecef  c1e502                   shl ebp, 2
0044ecf2  c686a400000000           mov byte ptr [esi + 0xa4], 0
0044ecf9  01c5                     add ebp, eax
0044ecfb  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044ed01  c1e502                   shl ebp, 2
0044ed04  01eb                     add ebx, ebp
0044ed06  66894b7e                 mov word ptr [ebx + 0x7e], cx
0044ed0a  663b3d04634900           cmp di, word ptr [0x496304]
0044ed11  7522                     jne 0x44ed35
0044ed13  30f6                     xor dh, dh
0044ed15  31c9                     xor ecx, ecx
0044ed17  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044ed1d  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044ed23  b9ffff0000               mov ecx, 0xffff
0044ed28  8835370f4e00             mov byte ptr [0x4e0f37], dh
0044ed2e  66890d04634900           mov word ptr [0x496304], cx
0044ed35  c6838800000000           mov byte ptr [ebx + 0x88], 0
0044ed3c  c6868900000000           mov byte ptr [esi + 0x89], 0
0044ed43  eb05                     jmp 0x44ed4a
0044ed45  c644241001               mov byte ptr [esp + 0x10], 1
0044ed4a  807c241000               cmp byte ptr [esp + 0x10], 0
0044ed4f  0f8445050000             je 0x44f29a
0044ed55  31c0                     xor eax, eax
0044ed57  8a8682000000             mov al, byte ptr [esi + 0x82]
0044ed5d  83f802                   cmp eax, 2
0044ed60  0f858c000000             jne 0x44edf2
0044ed66  668b8680000000           mov ax, word ptr [esi + 0x80]
0044ed6d  668986c0000000           mov word ptr [esi + 0xc0], ax
0044ed74  31c0                     xor eax, eax
0044ed76  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044ed7d  3dffff0000               cmp eax, 0xffff
0044ed82  7462                     je 0x44ede6
0044ed84  e859c1fcff               call 0x41aee2
0044ed89  89c2                     mov edx, eax
0044ed8b  31c0                     xor eax, eax
0044ed8d  6689f8                   mov ax, di
0044ed90  c6868900000002           mov byte ptr [esi + 0x89], 2
0044ed97  89c6                     mov esi, eax
0044ed99  c1e604                   shl esi, 4
0044ed9c  01c6                     add esi, eax
0044ed9e  c1e602                   shl esi, 2
0044eda1  01c6                     add esi, eax
0044eda3  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044eda9  c1e602                   shl esi, 2
0044edac  01f3                     add ebx, esi
0044edae  6689537e                 mov word ptr [ebx + 0x7e], dx
0044edb2  663b3d04634900           cmp di, word ptr [0x496304]
0044edb9  0f85ecfdffff             jne 0x44ebab
0044edbf  30d2                     xor dl, dl
0044edc1  31ff                     xor edi, edi
0044edc3  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044edc9  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044edcf  baffff0000               mov edx, 0xffff
0044edd4  893d3c0f4e00             mov dword ptr [0x4e0f3c], edi
0044edda  66891504634900           mov word ptr [0x496304], dx
0044ede1  e9c5fdffff               jmp 0x44ebab
0044ede6  31c0                     xor eax, eax
0044ede8  31d2                     xor edx, edx
0044edea  6689f8                   mov ax, di
0044eded  e9c9fdffff               jmp 0x44ebbb
0044edf2  83f801                   cmp eax, 1
0044edf5  0f859f040000             jne 0x44f29a
0044edfb  31db                     xor ebx, ebx
0044edfd  668b8680000000           mov ax, word ptr [esi + 0x80]
0044ee04  6689fb                   mov bx, di
0044ee07  c6868900000002           mov byte ptr [esi + 0x89], 2
0044ee0e  89de                     mov esi, ebx
0044ee10  c1e604                   shl esi, 4
0044ee13  01de                     add esi, ebx
0044ee15  c1e602                   shl esi, 2
0044ee18  01de                     add esi, ebx
0044ee1a  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044ee20  c1e602                   shl esi, 2
0044ee23  01f3                     add ebx, esi
0044ee25  6689437e                 mov word ptr [ebx + 0x7e], ax
0044ee29  663b3d04634900           cmp di, word ptr [0x496304]
0044ee30  0f8575fdffff             jne 0x44ebab
0044ee36  bfffff0000               mov edi, 0xffff
0044ee3b  30c0                     xor al, al
0044ee3d  31f6                     xor esi, esi
0044ee3f  a2360f4e00               mov byte ptr [0x4e0f36], al
0044ee44  a2370f4e00               mov byte ptr [0x4e0f37], al
0044ee49  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044ee4f  66893d04634900           mov word ptr [0x496304], di
0044ee56  e950fdffff               jmp 0x44ebab
0044ee5b  31c0                     xor eax, eax
0044ee5d  8a8682000000             mov al, byte ptr [esi + 0x82]
0044ee63  83f802                   cmp eax, 2
0044ee66  756e                     jne 0x44eed6
0044ee68  31c0                     xor eax, eax
0044ee6a  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044ee71  e895b8fcff               call 0x41a70b
0044ee76  84c0                     test al, al
0044ee78  740d                     je 0x44ee87
0044ee7a  31d2                     xor edx, edx
0044ee7c  89e8                     mov eax, ebp
0044ee7e  668b567e                 mov dx, word ptr [esi + 0x7e]
0044ee82  e938fdffff               jmp 0x44ebbf
0044ee87  8b8683000000             mov eax, dword ptr [esi + 0x83]
0044ee8d  c1f818                   sar eax, 0x18
0044ee90  85c0                     test eax, eax
0044ee92  0f8556fcffff             jne 0x44eaee
0044ee98  8b8684000000             mov eax, dword ptr [esi + 0x84]
0044ee9e  c1f818                   sar eax, 0x18
0044eea1  85c0                     test eax, eax
0044eea3  0f8545fcffff             jne 0x44eaee
0044eea9  31d2                     xor edx, edx
0044eeab  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044eeb2  668b5608                 mov dx, word ptr [esi + 8]
0044eeb6  e86449fdff               call 0x42381f
0044eebb  84c0                     test al, al
0044eebd  0f842bfcffff             je 0x44eaee
0044eec3  c6868900000003           mov byte ptr [esi + 0x89], 3
0044eeca  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044eed1  e9c4030000               jmp 0x44f29a
0044eed6  83f801                   cmp eax, 1
0044eed9  0f85bb030000             jne 0x44f29a
0044eedf  668b4608                 mov ax, word ptr [esi + 8]
0044eee3  663b467e                 cmp ax, word ptr [esi + 0x7e]
0044eee7  7407                     je 0x44eef0
0044eee9  89e8                     mov eax, ebp
0044eeeb  e903fcffff               jmp 0x44eaf3
0044eef0  31db                     xor ebx, ebx
0044eef2  668b9e80000000           mov bx, word ptr [esi + 0x80]
0044eef9  89da                     mov edx, ebx
0044eefb  89d8                     mov eax, ebx
0044eefd  c1fa1f                   sar edx, 0x1f
0044ef00  c1e208                   shl edx, 8
0044ef03  1bc2                     sbb eax, edx
0044ef05  c1f808                   sar eax, 8
0044ef08  31c9                     xor ecx, ecx
0044ef0a  6689c1                   mov cx, ax
0044ef0d  89da                     mov edx, ebx
0044ef0f  b800010000               mov eax, 0x100
0044ef14  c1fa1f                   sar edx, 0x1f
0044ef17  8944240c                 mov dword ptr [esp + 0xc], eax
0044ef1b  89d8                     mov eax, ebx
0044ef1d  f77c240c                 idiv dword ptr [esp + 0xc]
0044ef21  31c0                     xor eax, eax
0044ef23  31db                     xor ebx, ebx
0044ef25  6689d0                   mov ax, dx
0044ef28  668b5e08                 mov bx, word ptr [esi + 8]
0044ef2c  89442404                 mov dword ptr [esp + 4], eax
0044ef30  89da                     mov edx, ebx
0044ef32  89d8                     mov eax, ebx
0044ef34  c1fa1f                   sar edx, 0x1f
0044ef37  c1e208                   shl edx, 8
0044ef3a  1bc2                     sbb eax, edx
0044ef3c  c1f808                   sar eax, 8
0044ef3f  25ffff0000               and eax, 0xffff
0044ef44  89da                     mov edx, ebx
0044ef46  89442408                 mov dword ptr [esp + 8], eax
0044ef4a  b800010000               mov eax, 0x100
0044ef4f  c1fa1f                   sar edx, 0x1f
0044ef52  8944240c                 mov dword ptr [esp + 0xc], eax
0044ef56  89d8                     mov eax, ebx
0044ef58  f77c240c                 idiv dword ptr [esp + 0xc]
0044ef5c  31c0                     xor eax, eax
0044ef5e  8b5c2404                 mov ebx, dword ptr [esp + 4]
0044ef62  6689d0                   mov ax, dx
0044ef65  8b542408                 mov edx, dword ptr [esp + 8]
0044ef69  e8e7a50200               call 0x479555
0044ef6e  83f810                   cmp eax, 0x10
0044ef71  0f8787000000             ja 0x44effe
0044ef77  8a8684000000             mov al, byte ptr [esi + 0x84]
0044ef7d  31d2                     xor edx, edx
0044ef7f  0442                     add al, 0x42
0044ef81  88c2                     mov dl, al
0044ef83  31c0                     xor eax, eax
0044ef85  668b4608                 mov ax, word ptr [esi + 8]
0044ef89  e8d5670200               call 0x475763
0044ef8e  84c0                     test al, al
0044ef90  0f852dffffff             jne 0x44eec3
0044ef96  8a8684000000             mov al, byte ptr [esi + 0x84]
0044ef9c  31d2                     xor edx, edx
0044ef9e  0442                     add al, 0x42
0044efa0  88c2                     mov dl, al
0044efa2  31c0                     xor eax, eax
0044efa4  89eb                     mov ebx, ebp
0044efa6  668b8680000000           mov ax, word ptr [esi + 0x80]
0044efad  e84c6c0200               call 0x475bfe
0044efb2  31d2                     xor edx, edx
0044efb4  6689c2                   mov dx, ax
0044efb7  81faffff0000             cmp edx, 0xffff
0044efbd  0f84d7020000             je 0x44f29a
0044efc3  8b2c24                   mov ebp, dword ptr [esp]
0044efc6  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044efcc  01eb                     add ebx, ebp
0044efce  6689437e                 mov word ptr [ebx + 0x7e], ax
0044efd2  663b3d04634900           cmp di, word ptr [0x496304]
0044efd9  0f85ccfbffff             jne 0x44ebab
0044efdf  baffff0000               mov edx, 0xffff
0044efe4  30c9                     xor cl, cl
0044efe6  31c0                     xor eax, eax
0044efe8  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044efee  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044eff4  a33c0f4e00               mov dword ptr [0x4e0f3c], eax
0044eff9  e9dcfdffff               jmp 0x44edda
0044effe  8b0c24                   mov ecx, dword ptr [esp]
0044f001  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044f007  01cb                     add ebx, ecx
0044f009  668b8680000000           mov ax, word ptr [esi + 0x80]
0044f010  6689437e                 mov word ptr [ebx + 0x7e], ax
0044f014  663b3d04634900           cmp di, word ptr [0x496304]
0044f01b  0f858afbffff             jne 0x44ebab
0044f021  30d2                     xor dl, dl
0044f023  31f6                     xor esi, esi
0044f025  8815360f4e00             mov byte ptr [0x4e0f36], dl
0044f02b  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044f031  beffff0000               mov esi, 0xffff
0044f036  8815370f4e00             mov byte ptr [0x4e0f37], dl
0044f03c  e963fbffff               jmp 0x44eba4
0044f041  31c0                     xor eax, eax
0044f043  668b86c0000000           mov ax, word ptr [esi + 0xc0]
0044f04a  e8bcb6fcff               call 0x41a70b
0044f04f  84c0                     test al, al
0044f051  740d                     je 0x44f060
0044f053  31d2                     xor edx, edx
0044f055  89e8                     mov eax, ebp
0044f057  668b567e                 mov dx, word ptr [esi + 0x7e]
0044f05b  e87367ffff               call 0x4457d3
0044f060  8a968b000000             mov dl, byte ptr [esi + 0x8b]
0044f066  31c0                     xor eax, eax
0044f068  feca                     dec dl
0044f06a  88d0                     mov al, dl
0044f06c  88968b000000             mov byte ptr [esi + 0x8b], dl
0044f072  85c0                     test eax, eax
0044f074  0f8520020000             jne 0x44f29a
0044f07a  ba02000000               mov edx, 2
0044f07f  8d6e0a                   lea ebp, [esi + 0xa]
0044f082  31db                     xor ebx, ebx
0044f084  89e8                     mov eax, ebp
0044f086  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f08d  c6868b0000000a           mov byte ptr [esi + 0x8b], 0xa
0044f094  e81f81ffff               call 0x4471b8
0044f099  25ffff0000               and eax, 0xffff
0044f09e  746c                     je 0x44f10c
0044f0a0  31c0                     xor eax, eax
0044f0a2  8a8682000000             mov al, byte ptr [esi + 0x82]
0044f0a8  83f802                   cmp eax, 2
0044f0ab  7539                     jne 0x44f0e6
0044f0ad  ba01000000               mov edx, 1
0044f0b2  31c9                     xor ecx, ecx
0044f0b4  31db                     xor ebx, ebx
0044f0b6  31c0                     xor eax, eax
0044f0b8  668b8e80000000           mov cx, word ptr [esi + 0x80]
0044f0bf  8a1e                     mov bl, byte ptr [esi]
0044f0c1  8a8684000000             mov al, byte ptr [esi + 0x84]
0044f0c7  e84343fdff               call 0x42340f
0044f0cc  ba02000000               mov edx, 2
0044f0d1  31db                     xor ebx, ebx
0044f0d3  89e8                     mov eax, ebp
0044f0d5  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f0dc  e80982ffff               call 0x4472ea
0044f0e1  e9e4fdffff               jmp 0x44eeca
0044f0e6  83f801                   cmp eax, 1
0044f0e9  0f85ab010000             jne 0x44f29a
0044f0ef  ba02000000               mov edx, 2
0044f0f4  31c0                     xor eax, eax
0044f0f6  31db                     xor ebx, ebx
0044f0f8  6689f8                   mov ax, di
0044f0fb  668b9e84000000           mov bx, word ptr [esi + 0x84]
0044f102  e8d147ffff               call 0x4438d8
0044f107  e9befdffff               jmp 0x44eeca
0044f10c  668b86b2000000           mov ax, word ptr [esi + 0xb2]
0044f113  3dffff0000               cmp eax, 0xffff
0044f118  0f84fe000000             je 0x44f21c
0044f11e  0fb7ef                   movzx ebp, di
0044f121  8a9684000000             mov dl, byte ptr [esi + 0x84]
0044f127  31db                     xor ebx, ebx
0044f129  80c242                   add dl, 0x42
0044f12c  55                       push ebp
0044f12d  88d3                     mov bl, dl
0044f12f  ba05000000               mov edx, 5
0044f134  89d9                     mov ecx, ebx
0044f136  e8398a0200               call 0x477b74
0044f13b  89eb                     mov ebx, ebp
0044f13d  c1e504                   shl ebp, 4
0044f140  01dd                     add ebp, ebx
0044f142  c1e502                   shl ebp, 2
0044f145  31d2                     xor edx, edx
0044f147  01dd                     add ebp, ebx
0044f149  6689c2                   mov dx, ax
0044f14c  c1e502                   shl ebp, 2
0044f14f  81faffff0000             cmp edx, 0xffff
0044f155  7571                     jne 0x44f1c8
0044f157  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f15c  b207                     mov dl, 7
0044f15e  8a442802                 mov al, byte ptr [eax + ebp + 2]
0044f162  25ff000000               and eax, 0xff
0044f167  7409                     je 0x44f172
0044f169  83f804                   cmp eax, 4
0044f16c  7404                     je 0x44f172
0044f16e  b001                     mov al, 1
0044f170  eb02                     jmp 0x44f174
0044f172  30c0                     xor al, al
0044f174  84c0                     test al, al
0044f176  0f841e010000             je 0x44f29a
0044f17c  31c0                     xor eax, eax
0044f17e  6689f8                   mov ax, di
0044f181  89c6                     mov esi, eax
0044f183  c1e604                   shl esi, 4
0044f186  01c6                     add esi, eax
0044f188  c1e602                   shl esi, 2
0044f18b  01c6                     add esi, eax
0044f18d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f192  8854b002                 mov byte ptr [eax + esi*4 + 2], dl
0044f196  663b3d04634900           cmp di, word ptr [0x496304]
0044f19d  0f85f7000000             jne 0x44f29a
0044f1a3  baffff0000               mov edx, 0xffff
0044f1a8  30c0                     xor al, al
0044f1aa  31f6                     xor esi, esi
0044f1ac  a2360f4e00               mov byte ptr [0x4e0f36], al
0044f1b1  a2370f4e00               mov byte ptr [0x4e0f37], al
0044f1b6  89353c0f4e00             mov dword ptr [0x4e0f3c], esi
0044f1bc  66891504634900           mov word ptr [0x496304], dx
0044f1c3  e9d2000000               jmp 0x44f29a
0044f1c8  663b8680000000           cmp ax, word ptr [esi + 0x80]
0044f1cf  0f84c5000000             je 0x44f29a
0044f1d5  c6868900000000           mov byte ptr [esi + 0x89], 0
0044f1dc  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044f1e2  01eb                     add ebx, ebp
0044f1e4  6689437e                 mov word ptr [ebx + 0x7e], ax
0044f1e8  663b3d04634900           cmp di, word ptr [0x496304]
0044f1ef  0f85b6f9ffff             jne 0x44ebab
0044f1f5  30c9                     xor cl, cl
0044f1f7  beffff0000               mov esi, 0xffff
0044f1fc  880d360f4e00             mov byte ptr [0x4e0f36], cl
0044f202  880d370f4e00             mov byte ptr [0x4e0f37], cl
0044f208  31c9                     xor ecx, ecx
0044f20a  66893504634900           mov word ptr [0x496304], si
0044f211  890d3c0f4e00             mov dword ptr [0x4e0f3c], ecx
0044f217  e98ff9ffff               jmp 0x44ebab
0044f21c  31c0                     xor eax, eax
0044f21e  6689f8                   mov ax, di
0044f221  89c6                     mov esi, eax
0044f223  c1e604                   shl esi, 4
0044f226  01c6                     add esi, eax
0044f228  c1e602                   shl esi, 2
0044f22b  01c6                     add esi, eax
0044f22d  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f232  b307                     mov bl, 7
0044f234  89fa                     mov edx, edi
0044f236  8a44b002                 mov al, byte ptr [eax + esi*4 + 2]
0044f23a  25ff000000               and eax, 0xff
0044f23f  7409                     je 0x44f24a
0044f241  83f804                   cmp eax, 4
0044f244  7404                     je 0x44f24a
0044f246  b001                     mov al, 1
0044f248  eb02                     jmp 0x44f24c
0044f24a  30c0                     xor al, al
0044f24c  84c0                     test al, al
0044f24e  744a                     je 0x44f29a
0044f250  31c0                     xor eax, eax
0044f252  6689d0                   mov ax, dx
0044f255  89c6                     mov esi, eax
0044f257  c1e604                   shl esi, 4
0044f25a  01c6                     add esi, eax
0044f25c  c1e602                   shl esi, 2
0044f25f  01c6                     add esi, eax
0044f261  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0044f266  885cb002                 mov byte ptr [eax + esi*4 + 2], bl
0044f26a  668b1d04634900           mov bx, word ptr [0x496304]
0044f271  6639da                   cmp dx, bx
0044f274  7524                     jne 0x44f29a
0044f276  b9ffff0000               mov ecx, 0xffff
0044f27b  30fe                     xor dh, bh
0044f27d  30db                     xor bl, bl
0044f27f  8835360f4e00             mov byte ptr [0x4e0f36], dh
0044f285  881d370f4e00             mov byte ptr [0x4e0f37], bl
0044f28b  31db                     xor ebx, ebx
0044f28d  66890d04634900           mov word ptr [0x496304], cx
0044f294  891d3c0f4e00             mov dword ptr [0x4e0f3c], ebx
0044f29a  83c414                   add esp, 0x14
0044f29d  5d                       pop ebp
0044f29e  e9b51affff               jmp 0x440d58
