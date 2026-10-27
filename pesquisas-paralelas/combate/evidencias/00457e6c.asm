; CreerEngin; intervalo [0x00457e6c, 0x00458088)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00457e6c  56                       push     esi
00457e6d  57                       push     edi
00457e6e  83ec04                   sub      esp, 4
00457e71  50                       push     eax
00457e72  88542404                 mov      byte ptr [esp + 4], dl
00457e76  88dc                     mov      ah, bl
00457e78  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00457e7e  31ff                     xor      edi, edi
00457e80  31d2                     xor      edx, edx
00457e82  6689fa                   mov      dx, di
00457e85  81fa20030000             cmp      edx, 0x320
00457e8b  7d1a                     jge      0x457ea7
00457e8d  69d214010000             imul     edx, edx, 0x114
00457e93  8a541a02                 mov      dl, byte ptr [edx + ebx + 2]
00457e97  81e2ff000000             and      edx, 0xff
00457e9d  0f95c0                   setne    al
00457ea0  84c0                     test     al, al
00457ea2  7403                     je       0x457ea7
00457ea4  47                       inc      edi
00457ea5  ebd9                     jmp      0x457e80
00457ea7  31db                     xor      ebx, ebx
00457ea9  6689fb                   mov      bx, di
00457eac  81fb20030000             cmp      ebx, 0x320
00457eb2  7512                     jne      0x457ec6
00457eb4  b8ffff0000               mov      eax, 0xffff
00457eb9  e90fd9feff               jmp      0x4457cd
00457ebe  b001                     mov      al, 1
00457ec0  eb2f                     jmp      0x457ef1
00457ec2  30c0                     xor      al, al
00457ec4  eb2b                     jmp      0x457ef1
00457ec6  89da                     mov      edx, ebx
00457ec8  c1e204                   shl      edx, 4
00457ecb  01da                     add      edx, ebx
00457ecd  c1e202                   shl      edx, 2
00457ed0  8b35a0194e00             mov      esi, dword ptr [0x4e19a0]
00457ed6  01da                     add      edx, ebx
00457ed8  88e0                     mov      al, ah
00457eda  c1e202                   shl      edx, 2
00457edd  2c0b                     sub      al, 0xb
00457edf  01d6                     add      esi, edx
00457ee1  3c06                     cmp      al, 6
00457ee3  77dd                     ja       0x457ec2
00457ee5  31d2                     xor      edx, edx
00457ee7  88c2                     mov      dl, al
00457ee9  2eff2495507e4500         jmp      dword ptr cs:[edx*4 + 0x457e50]
00457ef1  84c0                     test     al, al
00457ef3  7413                     je       0x457f08
00457ef5  31d2                     xor      edx, edx
00457ef7  88e2                     mov      dl, ah
00457ef9  83fa11                   cmp      edx, 0x11
00457efc  740a                     je       0x457f08
00457efe  83fa10                   cmp      edx, 0x10
00457f01  7405                     je       0x457f08
00457f03  c606c8                   mov      byte ptr [esi], 0xc8
00457f06  eb02                     jmp      0x457f0a
00457f08  880e                     mov      byte ptr [esi], cl
00457f0a  31c9                     xor      ecx, ecx
00457f0c  31db                     xor      ebx, ebx
00457f0e  31d2                     xor      edx, edx
00457f10  8a5c2404                 mov      bl, byte ptr [esp + 4]
00457f14  88e1                     mov      cl, ah
00457f16  31c0                     xor      eax, eax
00457f18  668b1424                 mov      dx, word ptr [esp]
00457f1c  6689f8                   mov      ax, di
00457f1f  e863fcffff               call     0x457b87
00457f24  c686dc00000000           mov      byte ptr [esi + 0xdc], 0
00457f2b  c6460207                 mov      byte ptr [esi + 2], 7
00457f2f  66c7869a0000006400       mov      word ptr [esi + 0x9a], 0x64
00457f38  c6467200                 mov      byte ptr [esi + 0x72], 0
00457f3c  66c746740000             mov      word ptr [esi + 0x74], 0
00457f42  66c786c0000000ffff       mov      word ptr [esi + 0xc0], 0xffff
00457f4b  c686be000000ff           mov      byte ptr [esi + 0xbe], 0xff
00457f52  c686bc000000ff           mov      byte ptr [esi + 0xbc], 0xff
00457f59  c686bd00000000           mov      byte ptr [esi + 0xbd], 0
00457f60  c686af00000000           mov      byte ptr [esi + 0xaf], 0
00457f67  c78604010000ffffffff     mov      dword ptr [esi + 0x104], 0xffffffff
00457f71  c7860c010000ffffffff     mov      dword ptr [esi + 0x10c], 0xffffffff
00457f7b  c686f500000000           mov      byte ptr [esi + 0xf5], 0
00457f82  c686f600000000           mov      byte ptr [esi + 0xf6], 0
00457f89  c686f700000000           mov      byte ptr [esi + 0xf7], 0
00457f90  c686f800000000           mov      byte ptr [esi + 0xf8], 0
00457f97  c7861001000000000000     mov      dword ptr [esi + 0x110], 0
00457fa1  668b4676                 mov      ax, word ptr [esi + 0x76]
00457fa5  c6869400000001           mov      byte ptr [esi + 0x94], 1
00457fac  66894604                 mov      word ptr [esi + 4], ax
00457fb0  31c0                     xor      eax, eax
00457fb2  eb12                     jmp      0x457fc6
00457fb4  31d2                     xor      edx, edx
00457fb6  6689c2                   mov      dx, ax
00457fb9  c644324c00               mov      byte ptr [edx + esi + 0x4c], 0
00457fbe  40                       inc      eax
00457fbf  66c74456100000           mov      word ptr [esi + edx*2 + 0x10], 0
00457fc6  663b460c                 cmp      ax, word ptr [esi + 0xc]
00457fca  72e8                     jb       0x457fb4
00457fcc  31d2                     xor      edx, edx
00457fce  6689fa                   mov      dx, di
00457fd1  89d6                     mov      esi, edx
00457fd3  c1e604                   shl      esi, 4
00457fd6  01d6                     add      esi, edx
00457fd8  89d0                     mov      eax, edx
00457fda  c1e602                   shl      esi, 2
00457fdd  e8b201ffff               call     0x448194
00457fe2  01d6                     add      esi, edx
00457fe4  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00457fea  c1e602                   shl      esi, 2
00457fed  01f2                     add      edx, esi
00457fef  31c0                     xor      eax, eax
00457ff1  8a4201                   mov      al, byte ptr [edx + 1]
00457ff4  83f804                   cmp      eax, 4
00457ff7  7526                     jne      0x45801f
00457ff9  31db                     xor      ebx, ebx
00457ffb  88c3                     mov      bl, al
00457ffd  8a02                     mov      al, byte ptr [edx]
00457fff  ba0c000000               mov      edx, 0xc
00458004  25ff000000               and      eax, 0xff
00458009  e8b20cfdff               call     0x428cc0
0045800e  88c2                     mov      dl, al
00458010  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00458015  80c20a                   add      dl, 0xa
00458018  889406da000000           mov      byte ptr [esi + eax + 0xda], dl
0045801f  31db                     xor      ebx, ebx
00458021  6689fb                   mov      bx, di
00458024  89da                     mov      edx, ebx
00458026  c1e204                   shl      edx, 4
00458029  01da                     add      edx, ebx
0045802b  c1e202                   shl      edx, 2
0045802e  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00458033  01da                     add      edx, ebx
00458035  8a449001                 mov      al, byte ptr [eax + edx*4 + 1]
00458039  25ff000000               and      eax, 0xff
0045803e  83f810                   cmp      eax, 0x10
00458041  7405                     je       0x458048
00458043  83f80e                   cmp      eax, 0xe
00458046  7522                     jne      0x45806a
00458048  31db                     xor      ebx, ebx
0045804a  6689fb                   mov      bx, di
0045804d  89d8                     mov      eax, ebx
0045804f  c1e004                   shl      eax, 4
00458052  01d8                     add      eax, ebx
00458054  c1e002                   shl      eax, 2
00458057  01d8                     add      eax, ebx
00458059  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
0045805f  c1e002                   shl      eax, 2
00458062  c68402da00000000         mov      byte ptr [edx + eax + 0xda], 0
0045806a  89f8                     mov      eax, edi
0045806c  e95cd7feff               jmp      0x4457cd
00458071  0000                     add      byte ptr [eax], al
00458073  0030                     add      byte ptr [eax], dh
00458075  c0c300                   rol      bl, 0
00458078  30c0                     xor      al, al
0045807a  c3                       ret
0045807b  0030                     add      byte ptr [eax], dh
0045807d  c0c300                   rol      bl, 0
00458080  30c0                     xor      al, al
00458082  c3                       ret
00458083  0030                     add      byte ptr [eax], dh
00458085  c0c300                   rol      bl, 0
