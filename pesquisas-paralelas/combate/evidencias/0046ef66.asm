; ProjectileAvance_contador_e_passo; intervalo [0x0046ef66, 0x0046f07c)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046ef66  8a5e03                   mov      bl, byte ptr [esi + 3]
0046ef69  fec3                     inc      bl
0046ef6b  885e03                   mov      byte ptr [esi + 3], bl
0046ef6e  807e1900                 cmp      byte ptr [esi + 0x19], 0
0046ef72  0f84d5000000             je       0x46f04d
0046ef78  3a5e04                   cmp      bl, byte ptr [esi + 4]
0046ef7b  0f85cc000000             jne      0x46f04d
0046ef81  8a06                     mov      al, byte ptr [esi]
0046ef83  fec0                     inc      al
0046ef85  88842460010000           mov      byte ptr [esp + 0x160], al
0046ef8c  668b4614                 mov      ax, word ptr [esi + 0x14]
0046ef90  89442408                 mov      dword ptr [esp + 8], eax
0046ef94  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ef98  89442444                 mov      dword ptr [esp + 0x44], eax
0046ef9c  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046ef9f  88842430010000           mov      byte ptr [esp + 0x130], al
0046efa6  668b4620                 mov      ax, word ptr [esi + 0x20]
0046efaa  89442418                 mov      dword ptr [esp + 0x18], eax
0046efae  8a4622                   mov      al, byte ptr [esi + 0x22]
0046efb1  8884246c010000           mov      byte ptr [esp + 0x16c], al
0046efb8  668b4612                 mov      ax, word ptr [esi + 0x12]
0046efbc  6689442420               mov      word ptr [esp + 0x20], ax
0046efc1  8a4623                   mov      al, byte ptr [esi + 0x23]
0046efc4  668b4e10                 mov      cx, word ptr [esi + 0x10]
0046efc8  88842434010000           mov      byte ptr [esp + 0x134], al
0046efcf  31c0                     xor      eax, eax
0046efd1  31d2                     xor      edx, edx
0046efd3  6689c2                   mov      dx, ax
0046efd6  83fa64                   cmp      edx, 0x64
0046efd9  7d14                     jge      0x46efef
0046efdb  6bda38                   imul     ebx, edx, 0x38
0046efde  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046efe4  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046efe8  84d2                     test     dl, dl
0046efea  7403                     je       0x46efef
0046efec  40                       inc      eax
0046efed  ebe2                     jmp      0x46efd1
0046efef  31ff                     xor      edi, edi
0046eff1  6689c7                   mov      di, ax
0046eff4  83ff64                   cmp      edi, 0x64
0046eff7  7450                     je       0x46f049
0046eff9  31c0                     xor      eax, eax
0046effb  8a842434010000           mov      al, byte ptr [esp + 0x134]
0046f002  50                       push     eax
0046f003  8b442422                 mov      eax, dword ptr [esp + 0x22]
0046f007  c1f810                   sar      eax, 0x10
0046f00a  50                       push     eax
0046f00b  0fbfc1                   movsx    eax, cx
0046f00e  50                       push     eax
0046f00f  31c0                     xor      eax, eax
0046f011  8a842478010000           mov      al, byte ptr [esp + 0x178]
0046f018  31db                     xor      ebx, ebx
0046f01a  50                       push     eax
0046f01b  31c0                     xor      eax, eax
0046f01d  31d2                     xor      edx, edx
0046f01f  668b442428               mov      ax, word ptr [esp + 0x28]
0046f024  668b5c2418               mov      bx, word ptr [esp + 0x18]
0046f029  50                       push     eax
0046f02a  31c0                     xor      eax, eax
0046f02c  8a942474010000           mov      dl, byte ptr [esp + 0x174]
0046f033  8a842444010000           mov      al, byte ptr [esp + 0x144]
0046f03a  31c9                     xor      ecx, ecx
0046f03c  50                       push     eax
0046f03d  668b4c245c               mov      cx, word ptr [esp + 0x5c]
0046f042  89f8                     mov      eax, edi
0046f044  e8bff1ffff               call     0x46e208
0046f049  c6461900                 mov      byte ptr [esi + 0x19], 0
0046f04d  66837e3400               cmp      word ptr [esi + 0x34], 0
0046f052  0f84c20a0000             je       0x46fb1a
0046f058  89f0                     mov      eax, esi
0046f05a  e86bf4ffff               call     0x46e4ca
0046f05f  807e2300                 cmp      byte ptr [esi + 0x23], 0
0046f063  0f84990b0000             je       0x46fc02
0046f069  31c0                     xor      eax, eax
0046f06b  8b5624                   mov      edx, dword ptr [esi + 0x24]
0046f06e  668b4628                 mov      ax, word ptr [esi + 0x28]
0046f072  01c2                     add      edx, eax
0046f074  895624                   mov      dword ptr [esi + 0x24], edx
0046f077  e9860b0000               jmp      0x46fc02
