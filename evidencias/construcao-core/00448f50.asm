; CalculNextCase; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00448f50  53                       push ebx
00448f51  51                       push ecx
00448f52  52                       push edx
00448f53  56                       push esi
00448f54  57                       push edi
00448f55  89c7                     mov edi, eax
00448f57  31c0                     xor eax, eax
00448f59  6689f8                   mov ax, di
00448f5c  89c3                     mov ebx, eax
00448f5e  c1e304                   shl ebx, 4
00448f61  01c3                     add ebx, eax
00448f63  c1e302                   shl ebx, 2
00448f66  01c3                     add ebx, eax
00448f68  8b35a0194e00             mov esi, dword ptr [0x4e19a0]
00448f6e  c1e302                   shl ebx, 2
00448f71  01de                     add esi, ebx
00448f73  8b9683000000             mov edx, dword ptr [esi + 0x83]
00448f79  c1fa18                   sar edx, 0x18
00448f7c  85d2                     test edx, edx
00448f7e  7528                     jne 0x448fa8
00448f80  8b9684000000             mov edx, dword ptr [esi + 0x84]
00448f86  c1fa18                   sar edx, 0x18
00448f89  85d2                     test edx, edx
00448f8b  751b                     jne 0x448fa8
00448f8d  8a9688000000             mov dl, byte ptr [esi + 0x88]
00448f93  85d2                     test edx, edx
00448f95  7507                     jne 0x448f9e
00448f97  e86cfdffff               call 0x448d08
00448f9c  eb0a                     jmp 0x448fa8
00448f9e  83fa05                   cmp edx, 5
00448fa1  7505                     jne 0x448fa8
00448fa3  e8f7fbffff               call 0x448b9f
00448fa8  668b467c                 mov ax, word ptr [esi + 0x7c]
00448fac  663b4608                 cmp ax, word ptr [esi + 8]
00448fb0  7511                     jne 0x448fc3
00448fb2  e9a17dffff               jmp 0x440d58
00448fb7  89d0                     mov eax, edx
00448fb9  e871ebffff               call 0x447b2f
00448fbe  e985000000               jmp 0x449048
00448fc3  31d2                     xor edx, edx
00448fc5  6689fa                   mov dx, di
00448fc8  89d3                     mov ebx, edx
00448fca  c1e304                   shl ebx, 4
00448fcd  01d3                     add ebx, edx
00448fcf  c1e302                   shl ebx, 2
00448fd2  01d3                     add ebx, edx
00448fd4  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00448fd9  c1e302                   shl ebx, 2
00448fdc  01c3                     add ebx, eax
00448fde  8a4301                   mov al, byte ptr [ebx + 1]
00448fe1  3c0b                     cmp al, 0xb
00448fe3  7224                     jb 0x449009
00448fe5  7624                     jbe 0x44900b
00448fe7  3c12                     cmp al, 0x12
00448fe9  7210                     jb 0x448ffb
00448feb  761e                     jbe 0x44900b
00448fed  3c17                     cmp al, 0x17
00448fef  721a                     jb 0x44900b
00448ff1  3c18                     cmp al, 0x18
00448ff3  7616                     jbe 0x44900b
00448ff5  3c19                     cmp al, 0x19
00448ff7  7412                     je 0x44900b
00448ff9  eb4d                     jmp 0x449048
00448ffb  3c0e                     cmp al, 0xe
00448ffd  720c                     jb 0x44900b
00448fff  3c0f                     cmp al, 0xf
00449001  7608                     jbe 0x44900b
00449003  3c11                     cmp al, 0x11
00449005  74b0                     je 0x448fb7
00449007  eb3f                     jmp 0x449048
00449009  3c03                     cmp al, 3
0044900b  8aa3a9000000             mov ah, byte ptr [ebx + 0xa9]
00449011  fec4                     inc ah
00449013  8a93a7000000             mov dl, byte ptr [ebx + 0xa7]
00449019  88a3a9000000             mov byte ptr [ebx + 0xa9], ah
0044901f  38d4                     cmp ah, dl
00449021  7525                     jne 0x449048
00449023  31d2                     xor edx, edx
00449025  8a93a4000000             mov dl, byte ptr [ebx + 0xa4]
0044902b  31c9                     xor ecx, ecx
0044902d  42                       inc edx
0044902e  8a8ba5000000             mov cl, byte ptr [ebx + 0xa5]
00449034  89d0                     mov eax, edx
00449036  c1fa1f                   sar edx, 0x1f
00449039  f7f9                     idiv ecx
0044903b  c683a900000000           mov byte ptr [ebx + 0xa9], 0
00449042  8893a4000000             mov byte ptr [ebx + 0xa4], dl
00449048  8a8691000000             mov al, byte ptr [esi + 0x91]
0044904e  3a8690000000             cmp al, byte ptr [esi + 0x90]
00449054  740a                     je 0x449060
00449056  31c0                     xor eax, eax
00449058  6689f8                   mov ax, di
0044905b  e839f5ffff               call 0x448599
00449060  8a1d41805000             mov bl, byte ptr [0x508041]
00449066  3a1e                     cmp bl, byte ptr [esi]
00449068  7409                     je 0x449073
0044906a  e98e000000               jmp 0x4490fd
0044906f  b001                     mov al, 1
00449071  eb18                     jmp 0x44908b
00449073  8a4601                   mov al, byte ptr [esi + 1]
00449076  2c0b                     sub al, 0xb
00449078  3c05                     cmp al, 5
0044907a  770d                     ja 0x449089
0044907c  25ff000000               and eax, 0xff
00449081  2eff2485388f4400         jmp dword ptr cs:[eax*4 + 0x448f38]
00449089  30c0                     xor al, al
0044908b  84c0                     test al, al
0044908d  746e                     je 0x4490fd
0044908f  31c9                     xor ecx, ecx
00449091  6689f9                   mov cx, di
00449094  89cb                     mov ebx, ecx
00449096  c1e304                   shl ebx, 4
00449099  01cb                     add ebx, ecx
0044909b  c1e302                   shl ebx, 2
0044909e  01cb                     add ebx, ecx
004490a0  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004490a5  c1e302                   shl ebx, 2
004490a8  31d2                     xor edx, edx
004490aa  01c3                     add ebx, eax
004490ac  31c0                     xor eax, eax
004490ae  8a1541805000             mov dl, byte ptr [0x508041]
004490b4  668b4308                 mov ax, word ptr [ebx + 8]
004490b8  e833d60200               call 0x4766f0
004490bd  84c0                     test al, al
004490bf  743c                     je 0x4490fd
004490c1  89c8                     mov eax, ecx
004490c3  e8957bffff               call 0x440c5d
004490c8  8b9304010000             mov edx, dword ptr [ebx + 0x104]
004490ce  c683f900000001           mov byte ptr [ebx + 0xf9], 1
004490d5  83faff                   cmp edx, -1
004490d8  7523                     jne 0x4490fd
004490da  b901000000               mov ecx, 1
004490df  31d2                     xor edx, edx
004490e1  50                       push eax
004490e2  8a5301                   mov dl, byte ptr [ebx + 1]
004490e5  8d8304010000             lea eax, [ebx + 0x104]
004490eb  c1e210                   shl edx, 0x10
004490ee  89c3                     mov ebx, eax
004490f0  b850000000               mov eax, 0x50
004490f5  80ce08                   or dh, 8
004490f8  e87c190400               call 0x48aa79
004490fd  8a8690000000             mov al, byte ptr [esi + 0x90]
00449103  8a9e91000000             mov bl, byte ptr [esi + 0x91]
00449109  fec8                     dec al
0044910b  fecb                     dec bl
0044910d  38d8                     cmp al, bl
0044910f  7504                     jne 0x449115
00449111  b001                     mov al, 1
00449113  eb48                     jmp 0x44915d
00449115  0fb6f0                   movzx esi, al
00449118  8d5601                   lea edx, [esi + 1]
0044911b  b910000000               mov ecx, 0x10
00449120  89d0                     mov eax, edx
00449122  c1fa1f                   sar edx, 0x1f
00449125  f7f9                     idiv ecx
00449127  81e3ff000000             and ebx, 0xff
0044912d  39da                     cmp edx, ebx
0044912f  74e0                     je 0x449111
00449131  8d5602                   lea edx, [esi + 2]
00449134  89d0                     mov eax, edx
00449136  c1fa1f                   sar edx, 0x1f
00449139  f7f9                     idiv ecx
0044913b  39da                     cmp edx, ebx
0044913d  74d2                     je 0x449111
0044913f  8d560f                   lea edx, [esi + 0xf]
00449142  89d0                     mov eax, edx
00449144  c1fa1f                   sar edx, 0x1f
00449147  f7f9                     idiv ecx
00449149  39da                     cmp edx, ebx
0044914b  74c4                     je 0x449111
0044914d  8d560e                   lea edx, [esi + 0xe]
00449150  89d0                     mov eax, edx
00449152  c1fa1f                   sar edx, 0x1f
00449155  f7f9                     idiv ecx
00449157  39da                     cmp edx, ebx
00449159  74b6                     je 0x449111
0044915b  30c0                     xor al, al
0044915d  84c0                     test al, al
0044915f  0f84f37bffff             je 0x440d58
00449165  31c0                     xor eax, eax
00449167  31d2                     xor edx, edx
00449169  6689f8                   mov ax, di
0044916c  e893f5ffff               call 0x448704
00449171  e9e27bffff               jmp 0x440d58
