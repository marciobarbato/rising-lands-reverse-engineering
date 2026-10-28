; ProjectileAvance; intervalo [0x0046eaf8, 0x0046fc0f)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046eaf8  53                       push     ebx
0046eaf9  51                       push     ecx
0046eafa  52                       push     edx
0046eafb  56                       push     esi
0046eafc  57                       push     edi
0046eafd  55                       push     ebp
0046eafe  81ecc4010000             sub      esp, 0x1c4
0046eb04  89c6                     mov      esi, eax
0046eb06  8a00                     mov      al, byte ptr [eax]
0046eb08  3c14                     cmp      al, 0x14
0046eb0a  0f828e100000             jb       0x46fb9e
0046eb10  3c17                     cmp      al, 0x17
0046eb12  0f864e040000             jbe      0x46ef66
0046eb18  3c1c                     cmp      al, 0x1c
0046eb1a  0f8263100000             jb       0x46fb83
0046eb20  0f8687030000             jbe      0x46eead
0046eb26  3c1f                     cmp      al, 0x1f
0046eb28  0f822a040000             jb       0x46ef58
0046eb2e  3c20                     cmp      al, 0x20
0046eb30  0f8601040000             jbe      0x46ef37
0046eb36  3c21                     cmp      al, 0x21
0046eb38  760d                     jbe      0x46eb47
0046eb3a  3c22                     cmp      al, 0x22
0046eb3c  0f8474100000             je       0x46fbb6
0046eb42  e9bb100000               jmp      0x46fc02
0046eb47  31c0                     xor      eax, eax
0046eb49  8a4618                   mov      al, byte ptr [esi + 0x18]
0046eb4c  83f814                   cmp      eax, 0x14
0046eb4f  0f85ad100000             jne      0x46fc02
0046eb55  b829000000               mov      eax, 0x29
0046eb5a  668b7e16                 mov      di, word ptr [esi + 0x16]
0046eb5e  e879190000               call     0x4704dc
0046eb63  a801                     test     al, 1
0046eb65  0f85b1000000             jne      0x46ec1c
0046eb6b  31db                     xor      ebx, ebx
0046eb6d  6689fb                   mov      bx, di
0046eb70  b900010000               mov      ecx, 0x100
0046eb75  89da                     mov      edx, ebx
0046eb77  89d8                     mov      eax, ebx
0046eb79  c1fa1f                   sar      edx, 0x1f
0046eb7c  f7f9                     idiv     ecx
0046eb7e  89d1                     mov      ecx, edx
0046eb80  89da                     mov      edx, ebx
0046eb82  89d8                     mov      eax, ebx
0046eb84  c1fa1f                   sar      edx, 0x1f
0046eb87  c1e208                   shl      edx, 8
0046eb8a  1bc2                     sbb      eax, edx
0046eb8c  c1f808                   sar      eax, 8
0046eb8f  31ff                     xor      edi, edi
0046eb91  bb03000000               mov      ebx, 3
0046eb96  6689cf                   mov      di, cx
0046eb99  89da                     mov      edx, ebx
0046eb9b  85ff                     test     edi, edi
0046eb9d  7407                     je       0x46eba6
0046eb9f  4f                       dec      edi
0046eba0  897c2464                 mov      dword ptr [esp + 0x64], edi
0046eba4  eb09                     jmp      0x46ebaf
0046eba6  bb02000000               mov      ebx, 2
0046ebab  894c2464                 mov      dword ptr [esp + 0x64], ecx
0046ebaf  31ff                     xor      edi, edi
0046ebb1  6689c7                   mov      di, ax
0046ebb4  85ff                     test     edi, edi
0046ebb6  7407                     je       0x46ebbf
0046ebb8  4f                       dec      edi
0046ebb9  897c2468                 mov      dword ptr [esp + 0x68], edi
0046ebbd  eb05                     jmp      0x46ebc4
0046ebbf  89442468                 mov      dword ptr [esp + 0x68], eax
0046ebc3  4a                       dec      edx
0046ebc4  81e1ffff0000             and      ecx, 0xffff
0046ebca  81f9ff000000             cmp      ecx, 0xff
0046ebd0  7501                     jne      0x46ebd3
0046ebd2  4b                       dec      ebx
0046ebd3  25ffff0000               and      eax, 0xffff
0046ebd8  3dff000000               cmp      eax, 0xff
0046ebdd  7501                     jne      0x46ebe0
0046ebdf  4a                       dec      edx
0046ebe0  31c9                     xor      ecx, ecx
0046ebe2  b82a000000               mov      eax, 0x2a
0046ebe7  6689d1                   mov      cx, dx
0046ebea  31d2                     xor      edx, edx
0046ebec  e8eb180000               call     0x4704dc
0046ebf1  f7f1                     div      ecx
0046ebf3  b82b000000               mov      eax, 0x2b
0046ebf8  89d1                     mov      ecx, edx
0046ebfa  e8dd180000               call     0x4704dc
0046ebff  81e3ffff0000             and      ebx, 0xffff
0046ec05  31d2                     xor      edx, edx
0046ec07  f7f3                     div      ebx
0046ec09  8b442468                 mov      eax, dword ptr [esp + 0x68]
0046ec0d  01c8                     add      eax, ecx
0046ec0f  8b5c2464                 mov      ebx, dword ptr [esp + 0x64]
0046ec13  c1e008                   shl      eax, 8
0046ec16  89d7                     mov      edi, edx
0046ec18  01d8                     add      eax, ebx
0046ec1a  01c7                     add      edi, eax
0046ec1c  b82c000000               mov      eax, 0x2c
0046ec21  bb03000000               mov      ebx, 3
0046ec26  31d2                     xor      edx, edx
0046ec28  e8af180000               call     0x4704dc
0046ec2d  f7f3                     div      ebx
0046ec2f  89d0                     mov      eax, edx
0046ec31  83fa01                   cmp      edx, 1
0046ec34  0f825b020000             jb       0x46ee95
0046ec3a  0f86c9000000             jbe      0x46ed09
0046ec40  83fa02                   cmp      edx, 2
0046ec43  0f8486010000             je       0x46edcf
0046ec49  e94f020000               jmp      0x46ee9d
0046ec4e  b606                     mov      dh, 6
0046ec50  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046ec56  89bc24a0000000           mov      dword ptr [esp + 0xa0], edi
0046ec5d  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ec61  8a6e22                   mov      ch, byte ptr [esi + 0x22]
0046ec64  88b4247c010000           mov      byte ptr [esp + 0x17c], dh
0046ec6b  8944245c                 mov      dword ptr [esp + 0x5c], eax
0046ec6f  8a4e23                   mov      cl, byte ptr [esi + 0x23]
0046ec72  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046ec75  31d2                     xor      edx, edx
0046ec77  88842488010000           mov      byte ptr [esp + 0x188], al
0046ec7e  6689542434               mov      word ptr [esp + 0x34], dx
0046ec83  668b4620                 mov      ax, word ptr [esi + 0x20]
0046ec87  66899424a8000000         mov      word ptr [esp + 0xa8], dx
0046ec8f  89442430                 mov      dword ptr [esp + 0x30], eax
0046ec93  31c0                     xor      eax, eax
0046ec95  31d2                     xor      edx, edx
0046ec97  6689c2                   mov      dx, ax
0046ec9a  83fa64                   cmp      edx, 0x64
0046ec9d  7d0e                     jge      0x46ecad
0046ec9f  6bd238                   imul     edx, edx, 0x38
0046eca2  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046eca6  84d2                     test     dl, dl
0046eca8  7403                     je       0x46ecad
0046ecaa  40                       inc      eax
0046ecab  ebe8                     jmp      0x46ec95
0046ecad  25ffff0000               and      eax, 0xffff
0046ecb2  83f864                   cmp      eax, 0x64
0046ecb5  0f84e2010000             je       0x46ee9d
0046ecbb  31d2                     xor      edx, edx
0046ecbd  88ca                     mov      dl, cl
0046ecbf  52                       push     edx
0046ecc0  8b9424aa000000           mov      edx, dword ptr [esp + 0xaa]
0046ecc7  c1fa10                   sar      edx, 0x10
0046ecca  52                       push     edx
0046eccb  8b54243a                 mov      edx, dword ptr [esp + 0x3a]
0046eccf  c1fa10                   sar      edx, 0x10
0046ecd2  52                       push     edx
0046ecd3  31d2                     xor      edx, edx
0046ecd5  88ea                     mov      dl, ch
0046ecd7  52                       push     edx
0046ecd8  31d2                     xor      edx, edx
0046ecda  668b542440               mov      dx, word ptr [esp + 0x40]
0046ecdf  31db                     xor      ebx, ebx
0046ece1  52                       push     edx
0046ece2  31d2                     xor      edx, edx
0046ece4  668b9c24b4000000         mov      bx, word ptr [esp + 0xb4]
0046ecec  8a94249c010000           mov      dl, byte ptr [esp + 0x19c]
0046ecf3  31c9                     xor      ecx, ecx
0046ecf5  52                       push     edx
0046ecf6  31d2                     xor      edx, edx
0046ecf8  668b4c2474               mov      cx, word ptr [esp + 0x74]
0046ecfd  8a942494010000           mov      dl, byte ptr [esp + 0x194]
0046ed04  e9bc000000               jmp      0x46edc5
0046ed09  b207                     mov      dl, 7
0046ed0b  89bc24c0000000           mov      dword ptr [esp + 0xc0], edi
0046ed12  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ed16  8a6e1f                   mov      ch, byte ptr [esi + 0x1f]
0046ed19  31db                     xor      ebx, ebx
0046ed1b  8894249c010000           mov      byte ptr [esp + 0x19c], dl
0046ed22  8944241c                 mov      dword ptr [esp + 0x1c], eax
0046ed26  66899c24c8000000         mov      word ptr [esp + 0xc8], bx
0046ed2e  66899c24cc000000         mov      word ptr [esp + 0xcc], bx
0046ed36  668b4620                 mov      ax, word ptr [esi + 0x20]
0046ed3a  8a4e23                   mov      cl, byte ptr [esi + 0x23]
0046ed3d  89442438                 mov      dword ptr [esp + 0x38], eax
0046ed41  8a4622                   mov      al, byte ptr [esi + 0x22]
0046ed44  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046ed4a  888424a8010000           mov      byte ptr [esp + 0x1a8], al
0046ed51  31c0                     xor      eax, eax
0046ed53  31d2                     xor      edx, edx
0046ed55  6689c2                   mov      dx, ax
0046ed58  83fa64                   cmp      edx, 0x64
0046ed5b  7d0e                     jge      0x46ed6b
0046ed5d  6bd238                   imul     edx, edx, 0x38
0046ed60  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046ed64  84d2                     test     dl, dl
0046ed66  7403                     je       0x46ed6b
0046ed68  40                       inc      eax
0046ed69  ebe8                     jmp      0x46ed53
0046ed6b  0fb7e8                   movzx    ebp, ax
0046ed6e  83fd64                   cmp      ebp, 0x64
0046ed71  0f8426010000             je       0x46ee9d
0046ed77  31c0                     xor      eax, eax
0046ed79  88c8                     mov      al, cl
0046ed7b  50                       push     eax
0046ed7c  8b8424ce000000           mov      eax, dword ptr [esp + 0xce]
0046ed83  c1f810                   sar      eax, 0x10
0046ed86  50                       push     eax
0046ed87  8b8424ce000000           mov      eax, dword ptr [esp + 0xce]
0046ed8e  c1f810                   sar      eax, 0x10
0046ed91  50                       push     eax
0046ed92  31c0                     xor      eax, eax
0046ed94  8a8424b4010000           mov      al, byte ptr [esp + 0x1b4]
0046ed9b  31db                     xor      ebx, ebx
0046ed9d  50                       push     eax
0046ed9e  31c0                     xor      eax, eax
0046eda0  31d2                     xor      edx, edx
0046eda2  668b442448               mov      ax, word ptr [esp + 0x48]
0046eda7  668b9c24d0000000         mov      bx, word ptr [esp + 0xd0]
0046edaf  50                       push     eax
0046edb0  31c0                     xor      eax, eax
0046edb2  8a9424b0010000           mov      dl, byte ptr [esp + 0x1b0]
0046edb9  88e8                     mov      al, ch
0046edbb  31c9                     xor      ecx, ecx
0046edbd  50                       push     eax
0046edbe  668b4c2434               mov      cx, word ptr [esp + 0x34]
0046edc3  89e8                     mov      eax, ebp
0046edc5  e83ef4ffff               call     0x46e208
0046edca  e9ce000000               jmp      0x46ee9d
0046edcf  c68424b401000008         mov      byte ptr [esp + 0x1b4], 8
0046edd7  668b4616                 mov      ax, word ptr [esi + 0x16]
0046eddb  89442460                 mov      dword ptr [esp + 0x60], eax
0046eddf  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046ede2  888424b8010000           mov      byte ptr [esp + 0x1b8], al
0046ede9  8a4622                   mov      al, byte ptr [esi + 0x22]
0046edec  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046edf2  888424bc010000           mov      byte ptr [esp + 0x1bc], al
0046edf9  31c0                     xor      eax, eax
0046edfb  89bc24e4000000           mov      dword ptr [esp + 0xe4], edi
0046ee02  66898424f0000000         mov      word ptr [esp + 0xf0], ax
0046ee0a  6689442448               mov      word ptr [esp + 0x48], ax
0046ee0f  8a4623                   mov      al, byte ptr [esi + 0x23]
0046ee12  668b4e20                 mov      cx, word ptr [esi + 0x20]
0046ee16  888424c0010000           mov      byte ptr [esp + 0x1c0], al
0046ee1d  31c0                     xor      eax, eax
0046ee1f  31d2                     xor      edx, edx
0046ee21  6689c2                   mov      dx, ax
0046ee24  83fa64                   cmp      edx, 0x64
0046ee27  7d0e                     jge      0x46ee37
0046ee29  6bd238                   imul     edx, edx, 0x38
0046ee2c  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046ee30  84d2                     test     dl, dl
0046ee32  7403                     je       0x46ee37
0046ee34  40                       inc      eax
0046ee35  ebe8                     jmp      0x46ee1f
0046ee37  0fb7e8                   movzx    ebp, ax
0046ee3a  83fd64                   cmp      ebp, 0x64
0046ee3d  745e                     je       0x46ee9d
0046ee3f  31c0                     xor      eax, eax
0046ee41  8a8424c0010000           mov      al, byte ptr [esp + 0x1c0]
0046ee48  50                       push     eax
0046ee49  8b44244a                 mov      eax, dword ptr [esp + 0x4a]
0046ee4d  c1f810                   sar      eax, 0x10
0046ee50  50                       push     eax
0046ee51  8b8424f6000000           mov      eax, dword ptr [esp + 0xf6]
0046ee58  c1f810                   sar      eax, 0x10
0046ee5b  50                       push     eax
0046ee5c  31c0                     xor      eax, eax
0046ee5e  8a8424c8010000           mov      al, byte ptr [esp + 0x1c8]
0046ee65  31db                     xor      ebx, ebx
0046ee67  50                       push     eax
0046ee68  31c0                     xor      eax, eax
0046ee6a  31d2                     xor      edx, edx
0046ee6c  6689c8                   mov      ax, cx
0046ee6f  668b9c24f4000000         mov      bx, word ptr [esp + 0xf4]
0046ee77  50                       push     eax
0046ee78  31c0                     xor      eax, eax
0046ee7a  8a9424c8010000           mov      dl, byte ptr [esp + 0x1c8]
0046ee81  8a8424cc010000           mov      al, byte ptr [esp + 0x1cc]
0046ee88  31c9                     xor      ecx, ecx
0046ee8a  50                       push     eax
0046ee8b  668b4c2478               mov      cx, word ptr [esp + 0x78]
0046ee90  e92effffff               jmp      0x46edc3
0046ee95  85d2                     test     edx, edx
0046ee97  0f84b1fdffff             je       0x46ec4e
0046ee9d  89f0                     mov      eax, esi
0046ee9f  66897e16                 mov      word ptr [esi + 0x16], di
0046eea3  e856f7ffff               call     0x46e5fe
0046eea8  e998000000               jmp      0x46ef45
0046eead  31d2                     xor      edx, edx
0046eeaf  31c0                     xor      eax, eax
0046eeb1  8a5618                   mov      dl, byte ptr [esi + 0x18]
0046eeb4  e896580000               call     0x47474f
0046eeb9  25ffff0000               and      eax, 0xffff
0046eebe  39c2                     cmp      edx, eax
0046eec0  0f853c0d0000             jne      0x46fc02
0046eec6  31db                     xor      ebx, ebx
0046eec8  31c0                     xor      eax, eax
0046eeca  31d2                     xor      edx, edx
0046eecc  8a5e20                   mov      bl, byte ptr [esi + 0x20]
0046eecf  e860580000               call     0x474734
0046eed4  6689c2                   mov      dx, ax
0046eed7  31c0                     xor      eax, eax
0046eed9  668b4616                 mov      ax, word ptr [esi + 0x16]
0046eedd  e8a07f0000               call     0x476e82
0046eee2  e95e000000               jmp      0x46ef45
0046eee7  31c0                     xor      eax, eax
0046eee9  8a4618                   mov      al, byte ptr [esi + 0x18]
0046eeec  83f820                   cmp      eax, 0x20
0046eeef  0f850d0d0000             jne      0x46fc02
0046eef5  89f0                     mov      eax, esi
0046eef7  ebaa                     jmp      0x46eea3
0046eef9  31c0                     xor      eax, eax
0046eefb  8a4618                   mov      al, byte ptr [esi + 0x18]
0046eefe  83f820                   cmp      eax, 0x20
0046ef01  0f85fb0c0000             jne      0x46fc02
0046ef07  89f0                     mov      eax, esi
0046ef09  bb06000000               mov      ebx, 6
0046ef0e  e8ebf6ffff               call     0x46e5fe
0046ef13  b82d000000               mov      eax, 0x2d
0046ef18  31d2                     xor      edx, edx
0046ef1a  e8bd150000               call     0x4704dc
0046ef1f  f7f3                     div      ebx
0046ef21  83c238                   add      edx, 0x38
0046ef24  31c0                     xor      eax, eax
0046ef26  81e2ff000000             and      edx, 0xff
0046ef2c  668b4616                 mov      ax, word ptr [esi + 0x16]
0046ef30  e8db670000               call     0x475710
0046ef35  eb0e                     jmp      0x46ef45
0046ef37  31c0                     xor      eax, eax
0046ef39  8a4618                   mov      al, byte ptr [esi + 0x18]
0046ef3c  83f820                   cmp      eax, 0x20
0046ef3f  0f85bd0c0000             jne      0x46fc02
0046ef45  c6460200                 mov      byte ptr [esi + 2], 0
0046ef49  e9b40c0000               jmp      0x46fc02
0046ef4e  31c0                     xor      eax, eax
0046ef50  8a4618                   mov      al, byte ptr [esi + 0x18]
0046ef53  83f810                   cmp      eax, 0x10
0046ef56  ebe7                     jmp      0x46ef3f
0046ef58  31c0                     xor      eax, eax
0046ef5a  8a4618                   mov      al, byte ptr [esi + 0x18]
0046ef5d  83f80c                   cmp      eax, 0xc
0046ef60  0f8c9c0c0000             jl       0x46fc02
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
0046f07c  89f0                     mov      eax, esi
0046f07e  e87bf5ffff               call     0x46e5fe
0046f083  e9bdfeffff               jmp      0x46ef45
0046f088  b50f                     mov      ch, 0xf
0046f08a  31db                     xor      ebx, ebx
0046f08c  882d44fb4d00             mov      byte ptr [0x4dfb44], ch
0046f092  668b5e16                 mov      bx, word ptr [esi + 0x16]
0046f096  b900010000               mov      ecx, 0x100
0046f09b  89da                     mov      edx, ebx
0046f09d  89d8                     mov      eax, ebx
0046f09f  c1fa1f                   sar      edx, 0x1f
0046f0a2  f7f9                     idiv     ecx
0046f0a4  899424e8000000           mov      dword ptr [esp + 0xe8], edx
0046f0ab  89da                     mov      edx, ebx
0046f0ad  89d8                     mov      eax, ebx
0046f0af  c1fa1f                   sar      edx, 0x1f
0046f0b2  f7f9                     idiv     ecx
0046f0b4  bf0f000000               mov      edi, 0xf
0046f0b9  898424ec000000           mov      dword ptr [esp + 0xec], eax
0046f0c0  8944246c                 mov      dword ptr [esp + 0x6c], eax
0046f0c4  31c0                     xor      eax, eax
0046f0c6  897c2470                 mov      dword ptr [esp + 0x70], edi
0046f0ca  668b8424e8000000         mov      ax, word ptr [esp + 0xe8]
0046f0d2  89bc24f4000000           mov      dword ptr [esp + 0xf4], edi
0046f0d9  83f807                   cmp      eax, 7
0046f0dc  7e0c                     jle      0x46f0ea
0046f0de  83e807                   sub      eax, 7
0046f0e1  898424fc000000           mov      dword ptr [esp + 0xfc], eax
0046f0e8  eb1d                     jmp      0x46f107
0046f0ea  b807000000               mov      eax, 7
0046f0ef  2b8424e8000000           sub      eax, dword ptr [esp + 0xe8]
0046f0f6  89fa                     mov      edx, edi
0046f0f8  31db                     xor      ebx, ebx
0046f0fa  29c2                     sub      edx, eax
0046f0fc  899c24fc000000           mov      dword ptr [esp + 0xfc], ebx
0046f103  89542470                 mov      dword ptr [esp + 0x70], edx
0046f107  31c0                     xor      eax, eax
0046f109  668b44246c               mov      ax, word ptr [esp + 0x6c]
0046f10e  83f807                   cmp      eax, 7
0046f111  7e0b                     jle      0x46f11e
0046f113  89c2                     mov      edx, eax
0046f115  83ea07                   sub      edx, 7
0046f118  8954246c                 mov      dword ptr [esp + 0x6c], edx
0046f11c  eb21                     jmp      0x46f13f
0046f11e  b807000000               mov      eax, 7
0046f123  8b4c246c                 mov      ecx, dword ptr [esp + 0x6c]
0046f127  8bbc24f4000000           mov      edi, dword ptr [esp + 0xf4]
0046f12e  29c8                     sub      eax, ecx
0046f130  29c7                     sub      edi, eax
0046f132  31c0                     xor      eax, eax
0046f134  89bc24f4000000           mov      dword ptr [esp + 0xf4], edi
0046f13b  8944246c                 mov      dword ptr [esp + 0x6c], eax
0046f13f  8b7c246c                 mov      edi, dword ptr [esp + 0x6c]
0046f143  8b9c24fc000000           mov      ebx, dword ptr [esp + 0xfc]
0046f14a  8b44246c                 mov      eax, dword ptr [esp + 0x6c]
0046f14e  8b4c2470                 mov      ecx, dword ptr [esp + 0x70]
0046f152  898424dc000000           mov      dword ptr [esp + 0xdc], eax
0046f159  b800010000               mov      eax, 0x100
0046f15e  c1e708                   shl      edi, 8
0046f161  29c8                     sub      eax, ecx
0046f163  01df                     add      edi, ebx
0046f165  89842408010000           mov      dword ptr [esp + 0x108], eax
0046f16c  31ed                     xor      ebp, ebp
0046f16e  eb18                     jmp      0x46f188
0046f170  8b9424dc000000           mov      edx, dword ptr [esp + 0xdc]
0046f177  8b842408010000           mov      eax, dword ptr [esp + 0x108]
0046f17e  42                       inc      edx
0046f17f  01c7                     add      edi, eax
0046f181  899424dc000000           mov      dword ptr [esp + 0xdc], edx
0046f188  31d2                     xor      edx, edx
0046f18a  31c0                     xor      eax, eax
0046f18c  668b54246c               mov      dx, word ptr [esp + 0x6c]
0046f191  668b8424f4000000         mov      ax, word ptr [esp + 0xf4]
0046f199  01c2                     add      edx, eax
0046f19b  31c0                     xor      eax, eax
0046f19d  668b8424dc000000         mov      ax, word ptr [esp + 0xdc]
0046f1a5  39d0                     cmp      eax, edx
0046f1a7  0f8d98fdffff             jge      0x46ef45
0046f1ad  3d00010000               cmp      eax, 0x100
0046f1b2  7dbc                     jge      0x46f170
0046f1b4  8b8424fc000000           mov      eax, dword ptr [esp + 0xfc]
0046f1bb  89442474                 mov      dword ptr [esp + 0x74], eax
0046f1bf  e9cc000000               jmp      0x46f290
0046f1c4  b106                     mov      cl, 6
0046f1c6  893c24                   mov      dword ptr [esp], edi
0046f1c9  668b4616                 mov      ax, word ptr [esi + 0x16]
0046f1cd  31d2                     xor      edx, edx
0046f1cf  888c2470010000           mov      byte ptr [esp + 0x170], cl
0046f1d6  89842404010000           mov      dword ptr [esp + 0x104], eax
0046f1dd  6689942400010000         mov      word ptr [esp + 0x100], dx
0046f1e5  6689942494000000         mov      word ptr [esp + 0x94], dx
0046f1ed  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f1f0  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046f1f3  88842474010000           mov      byte ptr [esp + 0x174], al
0046f1fa  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f1fe  8a6e23                   mov      ch, byte ptr [esi + 0x23]
0046f201  8984248c000000           mov      dword ptr [esp + 0x8c], eax
0046f208  31c0                     xor      eax, eax
0046f20a  31d2                     xor      edx, edx
0046f20c  6689c2                   mov      dx, ax
0046f20f  83fa64                   cmp      edx, 0x64
0046f212  7d14                     jge      0x46f228
0046f214  6bda38                   imul     ebx, edx, 0x38
0046f217  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046f21d  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f221  84d2                     test     dl, dl
0046f223  7403                     je       0x46f228
0046f225  40                       inc      eax
0046f226  ebe2                     jmp      0x46f20a
0046f228  25ffff0000               and      eax, 0xffff
0046f22d  83f864                   cmp      eax, 0x64
0046f230  7454                     je       0x46f286
0046f232  31d2                     xor      edx, edx
0046f234  88ea                     mov      dl, ch
0046f236  52                       push     edx
0046f237  8b942496000000           mov      edx, dword ptr [esp + 0x96]
0046f23e  c1fa10                   sar      edx, 0x10
0046f241  52                       push     edx
0046f242  8b942406010000           mov      edx, dword ptr [esp + 0x106]
0046f249  c1fa10                   sar      edx, 0x10
0046f24c  52                       push     edx
0046f24d  31d2                     xor      edx, edx
0046f24f  88ca                     mov      dl, cl
0046f251  52                       push     edx
0046f252  31d2                     xor      edx, edx
0046f254  668b94249c000000         mov      dx, word ptr [esp + 0x9c]
0046f25c  31db                     xor      ebx, ebx
0046f25e  52                       push     edx
0046f25f  31d2                     xor      edx, edx
0046f261  668b5c2414               mov      bx, word ptr [esp + 0x14]
0046f266  8a942488010000           mov      dl, byte ptr [esp + 0x188]
0046f26d  31c9                     xor      ecx, ecx
0046f26f  52                       push     edx
0046f270  31d2                     xor      edx, edx
0046f272  668b8c241c010000         mov      cx, word ptr [esp + 0x11c]
0046f27a  8a942488010000           mov      dl, byte ptr [esp + 0x188]
0046f281  e882efffff               call     0x46e208
0046f286  8b4c2474                 mov      ecx, dword ptr [esp + 0x74]
0046f28a  41                       inc      ecx
0046f28b  47                       inc      edi
0046f28c  894c2474                 mov      dword ptr [esp + 0x74], ecx
0046f290  31d2                     xor      edx, edx
0046f292  31c0                     xor      eax, eax
0046f294  31db                     xor      ebx, ebx
0046f296  668b9424fc000000         mov      dx, word ptr [esp + 0xfc]
0046f29e  668b442470               mov      ax, word ptr [esp + 0x70]
0046f2a3  668b5c2474               mov      bx, word ptr [esp + 0x74]
0046f2a8  01d0                     add      eax, edx
0046f2aa  39c3                     cmp      ebx, eax
0046f2ac  0f8dbefeffff             jge      0x46f170
0046f2b2  81fb00010000             cmp      ebx, 0x100
0046f2b8  7dcc                     jge      0x46f286
0046f2ba  31c9                     xor      ecx, ecx
0046f2bc  31d2                     xor      edx, edx
0046f2be  31c0                     xor      eax, eax
0046f2c0  668b8c24dc000000         mov      cx, word ptr [esp + 0xdc]
0046f2c8  668b9424ec000000         mov      dx, word ptr [esp + 0xec]
0046f2d0  668b8424e8000000         mov      ax, word ptr [esp + 0xe8]
0046f2d8  e878a20000               call     0x479555
0046f2dd  663d3100                 cmp      ax, 0x31
0046f2e1  0f86a3010000             jbe      0x46f48a
0046f2e7  eb9d                     jmp      0x46f286
0046f2e9  b707                     mov      bh, 7
0046f2eb  89bc24b0000000           mov      dword ptr [esp + 0xb0], edi
0046f2f2  668b4e16                 mov      cx, word ptr [esi + 0x16]
0046f2f6  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f2f9  88bc2490010000           mov      byte ptr [esp + 0x190], bh
0046f300  88842494010000           mov      byte ptr [esp + 0x194], al
0046f307  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f30b  31db                     xor      ebx, ebx
0046f30d  8944242c                 mov      dword ptr [esp + 0x2c], eax
0046f311  66899c24b8000000         mov      word ptr [esp + 0xb8], bx
0046f319  8a4622                   mov      al, byte ptr [esi + 0x22]
0046f31c  66899c24bc000000         mov      word ptr [esp + 0xbc], bx
0046f324  88842498010000           mov      byte ptr [esp + 0x198], al
0046f32b  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f32e  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046f334  88842424010000           mov      byte ptr [esp + 0x124], al
0046f33b  31c0                     xor      eax, eax
0046f33d  31d2                     xor      edx, edx
0046f33f  6689c2                   mov      dx, ax
0046f342  83fa64                   cmp      edx, 0x64
0046f345  7d0e                     jge      0x46f355
0046f347  6bd238                   imul     edx, edx, 0x38
0046f34a  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f34e  84d2                     test     dl, dl
0046f350  7403                     je       0x46f355
0046f352  40                       inc      eax
0046f353  ebe8                     jmp      0x46f33d
0046f355  25ffff0000               and      eax, 0xffff
0046f35a  83f864                   cmp      eax, 0x64
0046f35d  0f8423ffffff             je       0x46f286
0046f363  31d2                     xor      edx, edx
0046f365  8a942424010000           mov      dl, byte ptr [esp + 0x124]
0046f36c  52                       push     edx
0046f36d  8b9424be000000           mov      edx, dword ptr [esp + 0xbe]
0046f374  c1fa10                   sar      edx, 0x10
0046f377  52                       push     edx
0046f378  8b9424be000000           mov      edx, dword ptr [esp + 0xbe]
0046f37f  c1fa10                   sar      edx, 0x10
0046f382  52                       push     edx
0046f383  31d2                     xor      edx, edx
0046f385  8a9424a4010000           mov      dl, byte ptr [esp + 0x1a4]
0046f38c  52                       push     edx
0046f38d  31d2                     xor      edx, edx
0046f38f  668b54243c               mov      dx, word ptr [esp + 0x3c]
0046f394  52                       push     edx
0046f395  31d2                     xor      edx, edx
0046f397  8a9424a8010000           mov      dl, byte ptr [esp + 0x1a8]
0046f39e  52                       push     edx
0046f39f  81e1ffff0000             and      ecx, 0xffff
0046f3a5  31db                     xor      ebx, ebx
0046f3a7  31d2                     xor      edx, edx
0046f3a9  668b9c24c8000000         mov      bx, word ptr [esp + 0xc8]
0046f3b1  8a9424a8010000           mov      dl, byte ptr [esp + 0x1a8]
0046f3b8  e9c4feffff               jmp      0x46f281
0046f3bd  b308                     mov      bl, 8
0046f3bf  89bc24d0000000           mov      dword ptr [esp + 0xd0], edi
0046f3c6  668b4616                 mov      ax, word ptr [esi + 0x16]
0046f3ca  8a4e1f                   mov      cl, byte ptr [esi + 0x1f]
0046f3cd  898424d4000000           mov      dword ptr [esp + 0xd4], eax
0046f3d4  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f3d8  889c24b0010000           mov      byte ptr [esp + 0x1b0], bl
0046f3df  898424d8000000           mov      dword ptr [esp + 0xd8], eax
0046f3e6  31c0                     xor      eax, eax
0046f3e8  8a6e22                   mov      ch, byte ptr [esi + 0x22]
0046f3eb  668984240c010000         mov      word ptr [esp + 0x10c], ax
0046f3f3  668984249c000000         mov      word ptr [esp + 0x9c], ax
0046f3fb  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f3fe  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046f404  8884241c010000           mov      byte ptr [esp + 0x11c], al
0046f40b  31c0                     xor      eax, eax
0046f40d  31d2                     xor      edx, edx
0046f40f  6689c2                   mov      dx, ax
0046f412  83fa64                   cmp      edx, 0x64
0046f415  7d0e                     jge      0x46f425
0046f417  6bd238                   imul     edx, edx, 0x38
0046f41a  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f41e  84d2                     test     dl, dl
0046f420  7403                     je       0x46f425
0046f422  40                       inc      eax
0046f423  ebe8                     jmp      0x46f40d
0046f425  25ffff0000               and      eax, 0xffff
0046f42a  83f864                   cmp      eax, 0x64
0046f42d  0f8453feffff             je       0x46f286
0046f433  31d2                     xor      edx, edx
0046f435  8a94241c010000           mov      dl, byte ptr [esp + 0x11c]
0046f43c  52                       push     edx
0046f43d  8b94249e000000           mov      edx, dword ptr [esp + 0x9e]
0046f444  c1fa10                   sar      edx, 0x10
0046f447  52                       push     edx
0046f448  8b942412010000           mov      edx, dword ptr [esp + 0x112]
0046f44f  c1fa10                   sar      edx, 0x10
0046f452  52                       push     edx
0046f453  31d2                     xor      edx, edx
0046f455  88ea                     mov      dl, ch
0046f457  52                       push     edx
0046f458  31d2                     xor      edx, edx
0046f45a  668b9424e8000000         mov      dx, word ptr [esp + 0xe8]
0046f462  52                       push     edx
0046f463  31d2                     xor      edx, edx
0046f465  31db                     xor      ebx, ebx
0046f467  88ca                     mov      dl, cl
0046f469  668b9c24e4000000         mov      bx, word ptr [esp + 0xe4]
0046f471  52                       push     edx
0046f472  31c9                     xor      ecx, ecx
0046f474  31d2                     xor      edx, edx
0046f476  668b8c24ec000000         mov      cx, word ptr [esp + 0xec]
0046f47e  8a9424c8010000           mov      dl, byte ptr [esp + 0x1c8]
0046f485  e9f7fdffff               jmp      0x46f281
0046f48a  6a00                     push     0
0046f48c  ba04000000               mov      edx, 4
0046f491  31c9                     xor      ecx, ecx
0046f493  31c0                     xor      eax, eax
0046f495  31db                     xor      ebx, ebx
0046f497  6689f8                   mov      ax, di
0046f49a  8a0e                     mov      cl, byte ptr [esi]
0046f49c  668b5e20                 mov      bx, word ptr [esi + 0x20]
0046f4a0  e8cf13feff               call     0x450874
0046f4a5  b82f000000               mov      eax, 0x2f
0046f4aa  bb03000000               mov      ebx, 3
0046f4af  31d2                     xor      edx, edx
0046f4b1  e826100000               call     0x4704dc
0046f4b6  f7f3                     div      ebx
0046f4b8  83fa01                   cmp      edx, 1
0046f4bb  7214                     jb       0x46f4d1
0046f4bd  0f8626feffff             jbe      0x46f2e9
0046f4c3  83fa02                   cmp      edx, 2
0046f4c6  0f84f1feffff             je       0x46f3bd
0046f4cc  e9b5fdffff               jmp      0x46f286
0046f4d1  85d2                     test     edx, edx
0046f4d3  0f84ebfcffff             je       0x46f1c4
0046f4d9  e9a8fdffff               jmp      0x46f286
0046f4de  89f0                     mov      eax, esi
0046f4e0  e819f1ffff               call     0x46e5fe
0046f4e5  31db                     xor      ebx, ebx
0046f4e7  668b4616                 mov      ax, word ptr [esi + 0x16]
0046f4eb  6689c3                   mov      bx, ax
0046f4ee  b900010000               mov      ecx, 0x100
0046f4f3  89da                     mov      edx, ebx
0046f4f5  89d8                     mov      eax, ebx
0046f4f7  c1fa1f                   sar      edx, 0x1f
0046f4fa  f7f9                     idiv     ecx
0046f4fc  89d1                     mov      ecx, edx
0046f4fe  89da                     mov      edx, ebx
0046f500  89d8                     mov      eax, ebx
0046f502  c1fa1f                   sar      edx, 0x1f
0046f505  c1e208                   shl      edx, 8
0046f508  1bc2                     sbb      eax, edx
0046f50a  c1f808                   sar      eax, 8
0046f50d  bf03000000               mov      edi, 3
0046f512  31d2                     xor      edx, edx
0046f514  89bc2418010000           mov      dword ptr [esp + 0x118], edi
0046f51b  6689ca                   mov      dx, cx
0046f51e  89bc24ac000000           mov      dword ptr [esp + 0xac], edi
0046f525  85d2                     test     edx, edx
0046f527  7405                     je       0x46f52e
0046f529  89cf                     mov      edi, ecx
0046f52b  4f                       dec      edi
0046f52c  eb0e                     jmp      0x46f53c
0046f52e  bb02000000               mov      ebx, 2
0046f533  89cf                     mov      edi, ecx
0046f535  899c2418010000           mov      dword ptr [esp + 0x118], ebx
0046f53c  31d2                     xor      edx, edx
0046f53e  6689c2                   mov      dx, ax
0046f541  85d2                     test     edx, edx
0046f543  7403                     je       0x46f548
0046f545  4a                       dec      edx
0046f546  eb07                     jmp      0x46f54f
0046f548  ff8c24ac000000           dec      dword ptr [esp + 0xac]
0046f54f  31db                     xor      ebx, ebx
0046f551  6689cb                   mov      bx, cx
0046f554  81fbff000000             cmp      ebx, 0xff
0046f55a  7507                     jne      0x46f563
0046f55c  ff8c2418010000           dec      dword ptr [esp + 0x118]
0046f563  25ffff0000               and      eax, 0xffff
0046f568  3dff000000               cmp      eax, 0xff
0046f56d  7507                     jne      0x46f576
0046f56f  ff8c24ac000000           dec      dword ptr [esp + 0xac]
0046f576  b800010000               mov      eax, 0x100
0046f57b  c1e208                   shl      edx, 8
0046f57e  8b9c24ac000000           mov      ebx, dword ptr [esp + 0xac]
0046f585  01d7                     add      edi, edx
0046f587  29d8                     sub      eax, ebx
0046f589  31d2                     xor      edx, edx
0046f58b  89442478                 mov      dword ptr [esp + 0x78], eax
0046f58f  89942414010000           mov      dword ptr [esp + 0x114], edx
0046f596  eb15                     jmp      0x46f5ad
0046f598  8b8c2414010000           mov      ecx, dword ptr [esp + 0x114]
0046f59f  8b5c2478                 mov      ebx, dword ptr [esp + 0x78]
0046f5a3  41                       inc      ecx
0046f5a4  01df                     add      edi, ebx
0046f5a6  898c2414010000           mov      dword ptr [esp + 0x114], ecx
0046f5ad  8b842414010000           mov      eax, dword ptr [esp + 0x114]
0046f5b4  663b8424ac000000         cmp      ax, word ptr [esp + 0xac]
0046f5bc  0f8383f9ffff             jae      0x46ef45
0046f5c2  31c9                     xor      ecx, ecx
0046f5c4  e9c0000000               jmp      0x46f689
0046f5c9  b406                     mov      ah, 6
0046f5cb  897c2404                 mov      dword ptr [esp + 4], edi
0046f5cf  8a6e1f                   mov      ch, byte ptr [esi + 0x1f]
0046f5d2  31d2                     xor      edx, edx
0046f5d4  88a4244c010000           mov      byte ptr [esp + 0x14c], ah
0046f5db  668b4616                 mov      ax, word ptr [esi + 0x16]
0046f5df  668954240c               mov      word ptr [esp + 0xc], dx
0046f5e4  89442454                 mov      dword ptr [esp + 0x54], eax
0046f5e8  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f5ec  6689942490000000         mov      word ptr [esp + 0x90], dx
0046f5f4  89842488000000           mov      dword ptr [esp + 0x88], eax
0046f5fb  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f5fe  8a4e22                   mov      cl, byte ptr [esi + 0x22]
0046f601  88842478010000           mov      byte ptr [esp + 0x178], al
0046f608  31c0                     xor      eax, eax
0046f60a  31d2                     xor      edx, edx
0046f60c  6689c2                   mov      dx, ax
0046f60f  83fa64                   cmp      edx, 0x64
0046f612  7d14                     jge      0x46f628
0046f614  6bda38                   imul     ebx, edx, 0x38
0046f617  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046f61d  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f621  84d2                     test     dl, dl
0046f623  7403                     je       0x46f628
0046f625  40                       inc      eax
0046f626  ebe2                     jmp      0x46f60a
0046f628  25ffff0000               and      eax, 0xffff
0046f62d  83f864                   cmp      eax, 0x64
0046f630  744e                     je       0x46f680
0046f632  31d2                     xor      edx, edx
0046f634  8a942478010000           mov      dl, byte ptr [esp + 0x178]
0046f63b  52                       push     edx
0046f63c  8b942492000000           mov      edx, dword ptr [esp + 0x92]
0046f643  c1fa10                   sar      edx, 0x10
0046f646  52                       push     edx
0046f647  8b542412                 mov      edx, dword ptr [esp + 0x12]
0046f64b  c1fa10                   sar      edx, 0x10
0046f64e  52                       push     edx
0046f64f  31d2                     xor      edx, edx
0046f651  88ca                     mov      dl, cl
0046f653  52                       push     edx
0046f654  31d2                     xor      edx, edx
0046f656  668b942498000000         mov      dx, word ptr [esp + 0x98]
0046f65e  52                       push     edx
0046f65f  31d2                     xor      edx, edx
0046f661  31db                     xor      ebx, ebx
0046f663  88ea                     mov      dl, ch
0046f665  668b5c2418               mov      bx, word ptr [esp + 0x18]
0046f66a  52                       push     edx
0046f66b  31c9                     xor      ecx, ecx
0046f66d  31d2                     xor      edx, edx
0046f66f  668b4c246c               mov      cx, word ptr [esp + 0x6c]
0046f674  8a942464010000           mov      dl, byte ptr [esp + 0x164]
0046f67b  e888ebffff               call     0x46e208
0046f680  8b8c24f8000000           mov      ecx, dword ptr [esp + 0xf8]
0046f687  41                       inc      ecx
0046f688  47                       inc      edi
0046f689  898c24f8000000           mov      dword ptr [esp + 0xf8], ecx
0046f690  8b8424f8000000           mov      eax, dword ptr [esp + 0xf8]
0046f697  663b842418010000         cmp      ax, word ptr [esp + 0x118]
0046f69f  0f83f3feffff             jae      0x46f598
0046f6a5  b82f000000               mov      eax, 0x2f
0046f6aa  bb03000000               mov      ebx, 3
0046f6af  31d2                     xor      edx, edx
0046f6b1  e8260e0000               call     0x4704dc
0046f6b6  f7f3                     div      ebx
0046f6b8  83fa01                   cmp      edx, 1
0046f6bb  0f829c010000             jb       0x46f85d
0046f6c1  760b                     jbe      0x46f6ce
0046f6c3  83fa02                   cmp      edx, 2
0046f6c6  0f84c9000000             je       0x46f795
0046f6cc  ebb2                     jmp      0x46f680
0046f6ce  b007                     mov      al, 7
0046f6d0  897c2424                 mov      dword ptr [esp + 0x24], edi
0046f6d4  668b4e20                 mov      cx, word ptr [esi + 0x20]
0046f6d8  88842438010000           mov      byte ptr [esp + 0x138], al
0046f6df  668b4616                 mov      ax, word ptr [esi + 0x16]
0046f6e3  31db                     xor      ebx, ebx
0046f6e5  89442414                 mov      dword ptr [esp + 0x14], eax
0046f6e9  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f6ec  66899c24b4000000         mov      word ptr [esp + 0xb4], bx
0046f6f4  8884242c010000           mov      byte ptr [esp + 0x12c], al
0046f6fb  8a4622                   mov      al, byte ptr [esi + 0x22]
0046f6fe  66895c247c               mov      word ptr [esp + 0x7c], bx
0046f703  88842454010000           mov      byte ptr [esp + 0x154], al
0046f70a  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f70d  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046f713  88842448010000           mov      byte ptr [esp + 0x148], al
0046f71a  31c0                     xor      eax, eax
0046f71c  31d2                     xor      edx, edx
0046f71e  6689c2                   mov      dx, ax
0046f721  83fa64                   cmp      edx, 0x64
0046f724  7d0e                     jge      0x46f734
0046f726  6bd238                   imul     edx, edx, 0x38
0046f729  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f72d  84d2                     test     dl, dl
0046f72f  7403                     je       0x46f734
0046f731  40                       inc      eax
0046f732  ebe8                     jmp      0x46f71c
0046f734  25ffff0000               and      eax, 0xffff
0046f739  83f864                   cmp      eax, 0x64
0046f73c  0f843effffff             je       0x46f680
0046f742  31d2                     xor      edx, edx
0046f744  8a942448010000           mov      dl, byte ptr [esp + 0x148]
0046f74b  52                       push     edx
0046f74c  8b54247e                 mov      edx, dword ptr [esp + 0x7e]
0046f750  c1fa10                   sar      edx, 0x10
0046f753  52                       push     edx
0046f754  8b9424ba000000           mov      edx, dword ptr [esp + 0xba]
0046f75b  c1fa10                   sar      edx, 0x10
0046f75e  52                       push     edx
0046f75f  31d2                     xor      edx, edx
0046f761  8a942460010000           mov      dl, byte ptr [esp + 0x160]
0046f768  52                       push     edx
0046f769  31d2                     xor      edx, edx
0046f76b  6689ca                   mov      dx, cx
0046f76e  31db                     xor      ebx, ebx
0046f770  52                       push     edx
0046f771  31d2                     xor      edx, edx
0046f773  668b5c2438               mov      bx, word ptr [esp + 0x38]
0046f778  8a942440010000           mov      dl, byte ptr [esp + 0x140]
0046f77f  31c9                     xor      ecx, ecx
0046f781  52                       push     edx
0046f782  31d2                     xor      edx, edx
0046f784  668b4c242c               mov      cx, word ptr [esp + 0x2c]
0046f789  8a942450010000           mov      dl, byte ptr [esp + 0x150]
0046f790  e9e6feffff               jmp      0x46f67b
0046f795  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f798  b508                     mov      ch, 8
0046f79a  88842458010000           mov      byte ptr [esp + 0x158], al
0046f7a1  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f7a5  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046f7ab  8944244c                 mov      dword ptr [esp + 0x4c], eax
0046f7af  8a4622                   mov      al, byte ptr [esi + 0x22]
0046f7b2  897c2458                 mov      dword ptr [esp + 0x58], edi
0046f7b6  88842444010000           mov      byte ptr [esp + 0x144], al
0046f7bd  31c0                     xor      eax, eax
0046f7bf  88ac2440010000           mov      byte ptr [esp + 0x140], ch
0046f7c6  6689842410010000         mov      word ptr [esp + 0x110], ax
0046f7ce  6689442428               mov      word ptr [esp + 0x28], ax
0046f7d3  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f7d6  668b4e16                 mov      cx, word ptr [esi + 0x16]
0046f7da  88842420010000           mov      byte ptr [esp + 0x120], al
0046f7e1  31c0                     xor      eax, eax
0046f7e3  31d2                     xor      edx, edx
0046f7e5  6689c2                   mov      dx, ax
0046f7e8  83fa64                   cmp      edx, 0x64
0046f7eb  7d0e                     jge      0x46f7fb
0046f7ed  6bd238                   imul     edx, edx, 0x38
0046f7f0  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f7f4  84d2                     test     dl, dl
0046f7f6  7403                     je       0x46f7fb
0046f7f8  40                       inc      eax
0046f7f9  ebe8                     jmp      0x46f7e3
0046f7fb  25ffff0000               and      eax, 0xffff
0046f800  83f864                   cmp      eax, 0x64
0046f803  0f8477feffff             je       0x46f680
0046f809  31d2                     xor      edx, edx
0046f80b  8a942420010000           mov      dl, byte ptr [esp + 0x120]
0046f812  52                       push     edx
0046f813  8b54242a                 mov      edx, dword ptr [esp + 0x2a]
0046f817  c1fa10                   sar      edx, 0x10
0046f81a  52                       push     edx
0046f81b  8b942416010000           mov      edx, dword ptr [esp + 0x116]
0046f822  c1fa10                   sar      edx, 0x10
0046f825  52                       push     edx
0046f826  31d2                     xor      edx, edx
0046f828  8a942450010000           mov      dl, byte ptr [esp + 0x150]
0046f82f  52                       push     edx
0046f830  31d2                     xor      edx, edx
0046f832  668b54245c               mov      dx, word ptr [esp + 0x5c]
0046f837  52                       push     edx
0046f838  31d2                     xor      edx, edx
0046f83a  8a94246c010000           mov      dl, byte ptr [esp + 0x16c]
0046f841  52                       push     edx
0046f842  81e1ffff0000             and      ecx, 0xffff
0046f848  31db                     xor      ebx, ebx
0046f84a  31d2                     xor      edx, edx
0046f84c  668b5c2470               mov      bx, word ptr [esp + 0x70]
0046f851  8a942458010000           mov      dl, byte ptr [esp + 0x158]
0046f858  e91efeffff               jmp      0x46f67b
0046f85d  85d2                     test     edx, edx
0046f85f  0f8464fdffff             je       0x46f5c9
0046f865  e916feffff               jmp      0x46f680
0046f86a  b206                     mov      dl, 6
0046f86c  668b4e16                 mov      cx, word ptr [esi + 0x16]
0046f870  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f873  8894245c010000           mov      byte ptr [esp + 0x15c], dl
0046f87a  898c2498000000           mov      dword ptr [esp + 0x98], ecx
0046f881  88842464010000           mov      byte ptr [esp + 0x164], al
0046f888  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f88c  31d2                     xor      edx, edx
0046f88e  898424e0000000           mov      dword ptr [esp + 0xe0], eax
0046f895  8a4622                   mov      al, byte ptr [esi + 0x22]
0046f898  6689942480000000         mov      word ptr [esp + 0x80], dx
0046f8a0  88842468010000           mov      byte ptr [esp + 0x168], al
0046f8a7  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f8aa  66899424c4000000         mov      word ptr [esp + 0xc4], dx
0046f8b2  88842428010000           mov      byte ptr [esp + 0x128], al
0046f8b9  31c0                     xor      eax, eax
0046f8bb  31d2                     xor      edx, edx
0046f8bd  6689c2                   mov      dx, ax
0046f8c0  83fa64                   cmp      edx, 0x64
0046f8c3  7d14                     jge      0x46f8d9
0046f8c5  6bda38                   imul     ebx, edx, 0x38
0046f8c8  8b15f0805000             mov      edx, dword ptr [0x5080f0]
0046f8ce  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f8d2  84d2                     test     dl, dl
0046f8d4  7403                     je       0x46f8d9
0046f8d6  40                       inc      eax
0046f8d7  ebe2                     jmp      0x46f8bb
0046f8d9  31ff                     xor      edi, edi
0046f8db  6689c7                   mov      di, ax
0046f8de  83ff64                   cmp      edi, 0x64
0046f8e1  0f845ef6ffff             je       0x46ef45
0046f8e7  31c0                     xor      eax, eax
0046f8e9  8a842428010000           mov      al, byte ptr [esp + 0x128]
0046f8f0  50                       push     eax
0046f8f1  8b8424c6000000           mov      eax, dword ptr [esp + 0xc6]
0046f8f8  c1f810                   sar      eax, 0x10
0046f8fb  50                       push     eax
0046f8fc  8b842486000000           mov      eax, dword ptr [esp + 0x86]
0046f903  c1f810                   sar      eax, 0x10
0046f906  50                       push     eax
0046f907  31c0                     xor      eax, eax
0046f909  8a842474010000           mov      al, byte ptr [esp + 0x174]
0046f910  50                       push     eax
0046f911  31c0                     xor      eax, eax
0046f913  668b8424f0000000         mov      ax, word ptr [esp + 0xf0]
0046f91b  50                       push     eax
0046f91c  31c0                     xor      eax, eax
0046f91e  31db                     xor      ebx, ebx
0046f920  8a842478010000           mov      al, byte ptr [esp + 0x178]
0046f927  31d2                     xor      edx, edx
0046f929  50                       push     eax
0046f92a  31c0                     xor      eax, eax
0046f92c  8a942474010000           mov      dl, byte ptr [esp + 0x174]
0046f933  668b8424b0000000         mov      ax, word ptr [esp + 0xb0]
0046f93b  6689cb                   mov      bx, cx
0046f93e  89c1                     mov      ecx, eax
0046f940  89f8                     mov      eax, edi
0046f942  e8c1e8ffff               call     0x46e208
0046f947  e9f9f5ffff               jmp      0x46ef45
0046f94c  b407                     mov      ah, 7
0046f94e  668b4e16                 mov      cx, word ptr [esi + 0x16]
0046f952  31db                     xor      ebx, ebx
0046f954  88a42480010000           mov      byte ptr [esp + 0x180], ah
0046f95b  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046f95e  89cf                     mov      edi, ecx
0046f960  88842484010000           mov      byte ptr [esp + 0x184], al
0046f967  668b4620                 mov      ax, word ptr [esi + 0x20]
0046f96b  66899c24a4000000         mov      word ptr [esp + 0xa4], bx
0046f973  89442410                 mov      dword ptr [esp + 0x10], eax
0046f977  8a4622                   mov      al, byte ptr [esi + 0x22]
0046f97a  66895c2440               mov      word ptr [esp + 0x40], bx
0046f97f  8884248c010000           mov      byte ptr [esp + 0x18c], al
0046f986  8a4623                   mov      al, byte ptr [esi + 0x23]
0046f989  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046f98f  88842450010000           mov      byte ptr [esp + 0x150], al
0046f996  31c0                     xor      eax, eax
0046f998  31d2                     xor      edx, edx
0046f99a  6689c2                   mov      dx, ax
0046f99d  83fa64                   cmp      edx, 0x64
0046f9a0  7d0e                     jge      0x46f9b0
0046f9a2  6bd238                   imul     edx, edx, 0x38
0046f9a5  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046f9a9  84d2                     test     dl, dl
0046f9ab  7403                     je       0x46f9b0
0046f9ad  40                       inc      eax
0046f9ae  ebe8                     jmp      0x46f998
0046f9b0  25ffff0000               and      eax, 0xffff
0046f9b5  83f864                   cmp      eax, 0x64
0046f9b8  0f8487f5ffff             je       0x46ef45
0046f9be  31d2                     xor      edx, edx
0046f9c0  8a942450010000           mov      dl, byte ptr [esp + 0x150]
0046f9c7  52                       push     edx
0046f9c8  8b542442                 mov      edx, dword ptr [esp + 0x42]
0046f9cc  c1fa10                   sar      edx, 0x10
0046f9cf  52                       push     edx
0046f9d0  8b9424aa000000           mov      edx, dword ptr [esp + 0xaa]
0046f9d7  c1fa10                   sar      edx, 0x10
0046f9da  52                       push     edx
0046f9db  31d2                     xor      edx, edx
0046f9dd  8a942498010000           mov      dl, byte ptr [esp + 0x198]
0046f9e4  31db                     xor      ebx, ebx
0046f9e6  52                       push     edx
0046f9e7  31d2                     xor      edx, edx
0046f9e9  6689fb                   mov      bx, di
0046f9ec  668b542420               mov      dx, word ptr [esp + 0x20]
0046f9f1  31ff                     xor      edi, edi
0046f9f3  52                       push     edx
0046f9f4  31d2                     xor      edx, edx
0046f9f6  6689cf                   mov      di, cx
0046f9f9  8a942498010000           mov      dl, byte ptr [esp + 0x198]
0046fa00  89d9                     mov      ecx, ebx
0046fa02  52                       push     edx
0046fa03  31d2                     xor      edx, edx
0046fa05  89fb                     mov      ebx, edi
0046fa07  8a942498010000           mov      dl, byte ptr [esp + 0x198]
0046fa0e  e92fffffff               jmp      0x46f942
0046fa13  c68424a001000008         mov      byte ptr [esp + 0x1a0], 8
0046fa1b  8a461f                   mov      al, byte ptr [esi + 0x1f]
0046fa1e  888424a4010000           mov      byte ptr [esp + 0x1a4], al
0046fa25  668b4620                 mov      ax, word ptr [esi + 0x20]
0046fa29  8944243c                 mov      dword ptr [esp + 0x3c], eax
0046fa2d  8a4622                   mov      al, byte ptr [esi + 0x22]
0046fa30  8b1df0805000             mov      ebx, dword ptr [0x5080f0]
0046fa36  888424ac010000           mov      byte ptr [esp + 0x1ac], al
0046fa3d  31c0                     xor      eax, eax
0046fa3f  668b4e16                 mov      cx, word ptr [esi + 0x16]
0046fa43  6689842484000000         mov      word ptr [esp + 0x84], ax
0046fa4b  6689442450               mov      word ptr [esp + 0x50], ax
0046fa50  8a4623                   mov      al, byte ptr [esi + 0x23]
0046fa53  89cf                     mov      edi, ecx
0046fa55  8884243c010000           mov      byte ptr [esp + 0x13c], al
0046fa5c  31c0                     xor      eax, eax
0046fa5e  31d2                     xor      edx, edx
0046fa60  6689c2                   mov      dx, ax
0046fa63  83fa64                   cmp      edx, 0x64
0046fa66  7d0e                     jge      0x46fa76
0046fa68  6bd238                   imul     edx, edx, 0x38
0046fa6b  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
0046fa6f  84d2                     test     dl, dl
0046fa71  7403                     je       0x46fa76
0046fa73  40                       inc      eax
0046fa74  ebe8                     jmp      0x46fa5e
0046fa76  25ffff0000               and      eax, 0xffff
0046fa7b  83f864                   cmp      eax, 0x64
0046fa7e  0f84c1f4ffff             je       0x46ef45
0046fa84  31d2                     xor      edx, edx
0046fa86  8a94243c010000           mov      dl, byte ptr [esp + 0x13c]
0046fa8d  52                       push     edx
0046fa8e  8b542452                 mov      edx, dword ptr [esp + 0x52]
0046fa92  c1fa10                   sar      edx, 0x10
0046fa95  52                       push     edx
0046fa96  8b94248a000000           mov      edx, dword ptr [esp + 0x8a]
0046fa9d  c1fa10                   sar      edx, 0x10
0046faa0  52                       push     edx
0046faa1  31d2                     xor      edx, edx
0046faa3  8a9424b8010000           mov      dl, byte ptr [esp + 0x1b8]
0046faaa  52                       push     edx
0046faab  31d2                     xor      edx, edx
0046faad  668b54244c               mov      dx, word ptr [esp + 0x4c]
0046fab2  52                       push     edx
0046fab3  31d2                     xor      edx, edx
0046fab5  8a9424b8010000           mov      dl, byte ptr [esp + 0x1b8]
0046fabc  52                       push     edx
0046fabd  81e7ffff0000             and      edi, 0xffff
0046fac3  31d2                     xor      edx, edx
0046fac5  31db                     xor      ebx, ebx
0046fac7  8a9424b8010000           mov      dl, byte ptr [esp + 0x1b8]
0046face  6689cb                   mov      bx, cx
0046fad1  89f9                     mov      ecx, edi
0046fad3  e96afeffff               jmp      0x46f942
0046fad8  89f0                     mov      eax, esi
0046fada  bb03000000               mov      ebx, 3
0046fadf  e81aebffff               call     0x46e5fe
0046fae4  b830000000               mov      eax, 0x30
0046fae9  31d2                     xor      edx, edx
0046faeb  e8ec090000               call     0x4704dc
0046faf0  f7f3                     div      ebx
0046faf2  89d0                     mov      eax, edx
0046faf4  83fa01                   cmp      edx, 1
0046faf7  7214                     jb       0x46fb0d
0046faf9  0f864dfeffff             jbe      0x46f94c
0046faff  83fa02                   cmp      edx, 2
0046fb02  0f840bffffff             je       0x46fa13
0046fb08  e938f4ffff               jmp      0x46ef45
0046fb0d  85d2                     test     edx, edx
0046fb0f  0f8455fdffff             je       0x46f86a
0046fb15  e92bf4ffff               jmp      0x46ef45
0046fb1a  8a06                     mov      al, byte ptr [esi]
0046fb1c  3c15                     cmp      al, 0x15
0046fb1e  7231                     jb       0x46fb51
0046fb20  0f8656f5ffff             jbe      0x46f07c
0046fb26  3c17                     cmp      al, 0x17
0046fb28  0f82b0f9ffff             jb       0x46f4de
0046fb2e  3c19                     cmp      al, 0x19
0046fb30  0f8646f5ffff             jbe      0x46f07c
0046fb36  3c1d                     cmp      al, 0x1d
0046fb38  0f8207f4ffff             jb       0x46ef45
0046fb3e  0f869af9ffff             jbe      0x46f4de
0046fb44  3c1e                     cmp      al, 0x1e
0046fb46  0f843cf5ffff             je       0x46f088
0046fb4c  e9f4f3ffff               jmp      0x46ef45
0046fb51  3c09                     cmp      al, 9
0046fb53  7221                     jb       0x46fb76
0046fb55  0f8621f5ffff             jbe      0x46f07c
0046fb5b  3c11                     cmp      al, 0x11
0046fb5d  0f82e2f3ffff             jb       0x46ef45
0046fb63  0f8613f5ffff             jbe      0x46f07c
0046fb69  3c14                     cmp      al, 0x14
0046fb6b  0f846df9ffff             je       0x46f4de
0046fb71  e9cff3ffff               jmp      0x46ef45
0046fb76  3c01                     cmp      al, 1
0046fb78  0f845affffff             je       0x46fad8
0046fb7e  e9c2f3ffff               jmp      0x46ef45
0046fb83  3c19                     cmp      al, 0x19
0046fb85  0f825cf3ffff             jb       0x46eee7
0046fb8b  0f8668f3ffff             jbe      0x46eef9
0046fb91  31c0                     xor      eax, eax
0046fb93  8a4618                   mov      al, byte ptr [esi + 0x18]
0046fb96  83f808                   cmp      eax, 8
0046fb99  e9a1f3ffff               jmp      0x46ef3f
0046fb9e  3c0e                     cmp      al, 0xe
0046fba0  724b                     jb       0x46fbed
0046fba2  0f86a6f3ffff             jbe      0x46ef4e
0046fba8  3c11                     cmp      al, 0x11
0046fbaa  0f829ef3ffff             jb       0x46ef4e
0046fbb0  0f86b0f3ffff             jbe      0x46ef66
0046fbb6  31c0                     xor      eax, eax
0046fbb8  8a4618                   mov      al, byte ptr [esi + 0x18]
0046fbbb  83f820                   cmp      eax, 0x20
0046fbbe  7542                     jne      0x46fc02
0046fbc0  b82e000000               mov      eax, 0x2e
0046fbc5  bb06000000               mov      ebx, 6
0046fbca  c6460200                 mov      byte ptr [esi + 2], 0
0046fbce  31d2                     xor      edx, edx
0046fbd0  e807090000               call     0x4704dc
0046fbd5  f7f3                     div      ebx
0046fbd7  83c238                   add      edx, 0x38
0046fbda  31c0                     xor      eax, eax
0046fbdc  81e2ff000000             and      edx, 0xff
0046fbe2  668b4616                 mov      ax, word ptr [esi + 0x16]
0046fbe6  e8255b0000               call     0x475710
0046fbeb  eb15                     jmp      0x46fc02
0046fbed  3c06                     cmp      al, 6
0046fbef  7209                     jb       0x46fbfa
0046fbf1  3c08                     cmp      al, 8
0046fbf3  76c1                     jbe      0x46fbb6
0046fbf5  e96cf3ffff               jmp      0x46ef66
0046fbfa  3c01                     cmp      al, 1
0046fbfc  0f8364f3ffff             jae      0x46ef66
0046fc02  81c4c4010000             add      esp, 0x1c4
0046fc08  5d                       pop      ebp
0046fc09  5f                       pop      edi
0046fc0a  5e                       pop      esi
0046fc0b  5a                       pop      edx
0046fc0c  59                       pop      ecx
0046fc0d  5b                       pop      ebx
0046fc0e  c3                       ret
