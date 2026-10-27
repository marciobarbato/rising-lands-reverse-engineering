; EnginNextEtape_selection; intervalo [0x004546bc, 0x004547e0)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004546bc  31d2                     xor      edx, edx
004546be  6689fa                   mov      dx, di
004546c1  89d0                     mov      eax, edx
004546c3  c1e004                   shl      eax, 4
004546c6  01d0                     add      eax, edx
004546c8  c1e002                   shl      eax, 2
004546cb  01c2                     add      edx, eax
004546cd  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004546d2  c1e202                   shl      edx, 2
004546d5  8a440201                 mov      al, byte ptr [edx + eax + 1]
004546d9  3c0f                     cmp      al, 0xf
004546db  7220                     jb       0x4546fd
004546dd  761a                     jbe      0x4546f9
004546df  3c14                     cmp      al, 0x14
004546e1  720e                     jb       0x4546f1
004546e3  3c16                     cmp      al, 0x16
004546e5  7612                     jbe      0x4546f9
004546e7  3c18                     cmp      al, 0x18
004546e9  760e                     jbe      0x4546f9
004546eb  3c19                     cmp      al, 0x19
004546ed  740a                     je       0x4546f9
004546ef  eb20                     jmp      0x454711
004546f1  3c10                     cmp      al, 0x10
004546f3  7604                     jbe      0x4546f9
004546f5  3c12                     cmp      al, 0x12
004546f7  7218                     jb       0x454711
004546f9  b001                     mov      al, 1
004546fb  eb16                     jmp      0x454713
004546fd  3c03                     cmp      al, 3
004546ff  72f8                     jb       0x4546f9
00454701  76f6                     jbe      0x4546f9
00454703  3c08                     cmp      al, 8
00454705  720a                     jb       0x454711
00454707  76f0                     jbe      0x4546f9
00454709  3c0b                     cmp      al, 0xb
0045470b  7204                     jb       0x454711
0045470d  3c0c                     cmp      al, 0xc
0045470f  76e8                     jbe      0x4546f9
00454711  30c0                     xor      al, al
00454713  84c0                     test     al, al
00454715  0f84c5000000             je       0x4547e0
0045471b  31c0                     xor      eax, eax
0045471d  8a442458                 mov      al, byte ptr [esp + 0x58]
00454721  e8f1900100               call     0x46d817
00454726  88442450                 mov      byte ptr [esp + 0x50], al
0045472a  31c0                     xor      eax, eax
0045472c  8a4602                   mov      al, byte ptr [esi + 2]
0045472f  83f801                   cmp      eax, 1
00454732  0f84a8000000             je       0x4547e0
00454738  83f813                   cmp      eax, 0x13
0045473b  7509                     jne      0x454746
0045473d  e99e000000               jmp      0x4547e0
00454742  b001                     mov      al, 1
00454744  eb12                     jmp      0x454758
00454746  8a4c2460                 mov      cl, byte ptr [esp + 0x60]
0045474a  80f90e                   cmp      cl, 0xe
0045474d  7207                     jb       0x454756
0045474f  76f1                     jbe      0x454742
00454751  80f910                   cmp      cl, 0x10
00454754  74ec                     je       0x454742
00454756  30c0                     xor      al, al
00454758  84c0                     test     al, al
0045475a  7422                     je       0x45477e
0045475c  31d2                     xor      edx, edx
0045475e  6689fa                   mov      dx, di
00454761  89d0                     mov      eax, edx
00454763  c1e004                   shl      eax, 4
00454766  01d0                     add      eax, edx
00454768  c1e002                   shl      eax, 2
0045476b  01d0                     add      eax, edx
0045476d  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
00454773  8a8482da000000           mov      al, byte ptr [edx + eax*4 + 0xda]
0045477a  84c0                     test     al, al
0045477c  7516                     jne      0x454794
0045477e  8a642460                 mov      ah, byte ptr [esp + 0x60]
00454782  80fc0e                   cmp      ah, 0xe
00454785  7207                     jb       0x45478e
00454787  763d                     jbe      0x4547c6
00454789  80fc10                   cmp      ah, 0x10
0045478c  7438                     je       0x4547c6
0045478e  30c0                     xor      al, al
00454790  84c0                     test     al, al
00454792  754c                     jne      0x4547e0
00454794  31c9                     xor      ecx, ecx
00454796  6689f9                   mov      cx, di
00454799  89c8                     mov      eax, ecx
0045479b  31db                     xor      ebx, ebx
0045479d  e8d2f7ffff               call     0x453f74
004547a2  6689c3                   mov      bx, ax
004547a5  81fbffff0000             cmp      ebx, 0xffff
004547ab  7433                     je       0x4547e0
004547ad  31c0                     xor      eax, eax
004547af  8a442450                 mov      al, byte ptr [esp + 0x50]
004547b3  83f802                   cmp      eax, 2
004547b6  7512                     jne      0x4547ca
004547b8  ba49000000               mov      edx, 0x49
004547bd  89c8                     mov      eax, ecx
004547bf  e804e20200               call     0x4829c8
004547c4  eb1a                     jmp      0x4547e0
004547c6  b001                     mov      al, 1
004547c8  ebc6                     jmp      0x454790
004547ca  31c0                     xor      eax, eax
004547cc  8a4602                   mov      al, byte ptr [esi + 2]
004547cf  83f807                   cmp      eax, 7
004547d2  750c                     jne      0x4547e0
004547d4  ba01000000               mov      edx, 1
004547d9  89c8                     mov      eax, ecx
004547db  e85612ffff               call     0x445a36
