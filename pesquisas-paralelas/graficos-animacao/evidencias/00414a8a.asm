; AffWorkEngin [0x414a8a, 0x415496)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00414a8a  51                     push     ecx
00414a8b  56                     push     esi
00414a8c  57                     push     edi
00414a8d  55                     push     ebp
00414a8e  83ec40                 sub      esp, 0x40
00414a91  89c7                   mov      edi, eax
00414a93  8954241c               mov      dword ptr [esp + 0x1c], edx
00414a97  895c2430               mov      dword ptr [esp + 0x30], ebx
00414a9b  31c9                   xor      ecx, ecx
00414a9d  6689d9                 mov      cx, bx
00414aa0  89c8                   mov      eax, ecx
00414aa2  c1e004                 shl      eax, 4
00414aa5  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
00414aab  01c8                   add      eax, ecx
00414aad  89ca                   mov      edx, ecx
00414aaf  c1e002                 shl      eax, 2
00414ab2  31da                   xor      edx, ebx
00414ab4  01c8                   add      eax, ecx
00414ab6  6689542424             mov      word ptr [esp + 0x24], dx
00414abb  c1e002                 shl      eax, 2
00414abe  31db                   xor      ebx, ebx
00414ac0  01c6                   add      esi, eax
00414ac2  b401                   mov      ah, 1
00414ac4  8b54241c               mov      edx, dword ptr [esp + 0x1c]
00414ac8  8864243c               mov      byte ptr [esp + 0x3c], ah
00414acc  660fbe8686000000       movsx    ax, byte ptr [esi + 0x86]
00414ad4  66895c2420             mov      word ptr [esp + 0x20], bx
00414ad9  01c7                   add      edi, eax
00414adb  660fbe8687000000       movsx    ax, byte ptr [esi + 0x87]
00414ae3  895c2410               mov      dword ptr [esp + 0x10], ebx
00414ae7  895c240c               mov      dword ptr [esp + 0xc], ebx
00414aeb  01c2                   add      edx, eax
00414aed  8d5c240c               lea      ebx, [esp + 0xc]
00414af1  6689542434             mov      word ptr [esp + 0x34], dx
00414af6  31c0                   xor      eax, eax
00414af8  8d542410               lea      edx, [esp + 0x10]
00414afc  8a4601                 mov      al, byte ptr [esi + 1]
00414aff  e8c8c4ffff             call     0x410fcc ; AffCorpsEnginDecalage
00414b04  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
00414b0b  0f8413020000           je       0x414d24
00414b11  8a3541805000           mov      dh, byte ptr [0x508041]
00414b17  3a36                   cmp      dh, byte ptr [esi]
00414b19  0f8505020000           jne      0x414d24
00414b1f  8b442434               mov      eax, dword ptr [esp + 0x34]
00414b23  8d5c2408               lea      ebx, [esp + 8]
00414b27  8d542404               lea      edx, [esp + 4]
00414b2b  89442418               mov      dword ptr [esp + 0x18], eax
00414b2f  89c8                   mov      eax, ecx
00414b31  e836c50200             call     0x44106c ; EnginGetTaille
00414b36  31c0                   xor      eax, eax
00414b38  668b442404             mov      ax, word ptr [esp + 4]
00414b3d  897c2414               mov      dword ptr [esp + 0x14], edi
00414b41  83f801                 cmp      eax, 1
00414b44  751a                   jne      0x414b60
00414b46  39c0                   cmp      eax, eax
00414b48  7516                   jne      0x414b60
00414b4a  8b542432               mov      edx, dword ptr [esp + 0x32]
00414b4e  b901000000             mov      ecx, 1
00414b53  bb1e2a0000             mov      ebx, 0x2a1e
00414b58  0fbfc7                 movsx    eax, di
00414b5b  c1fa10                 sar      edx, 0x10
00414b5e  eb1c                   jmp      0x414b7c ; 
00414b60  8b442418               mov      eax, dword ptr [esp + 0x18]
00414b64  83e820                 sub      eax, 0x20
00414b67  0fbfd0                 movsx    edx, ax
00414b6a  8b442414               mov      eax, dword ptr [esp + 0x14]
00414b6e  b901000000             mov      ecx, 1
00414b73  83e820                 sub      eax, 0x20
00414b76  bb1f2a0000             mov      ebx, 0x2a1f
00414b7b  98                     cwde     
00414b7c  e8c6660400             call     0x45b247 ; PasteBobCmp
00414b81  31c0                   xor      eax, eax
00414b83  8a8682000000           mov      al, byte ptr [esi + 0x82]
00414b89  85c0                   test     eax, eax
00414b8b  0f8493010000           je       0x414d24
00414b91  31db                   xor      ebx, ebx
00414b93  668b9eb2000000         mov      bx, word ptr [esi + 0xb2]
00414b9a  b900010000             mov      ecx, 0x100
00414b9f  89da                   mov      edx, ebx
00414ba1  89d8                   mov      eax, ebx
00414ba3  c1fa1f                 sar      edx, 0x1f
00414ba6  f7f9                   idiv     ecx
00414ba8  89542428               mov      dword ptr [esp + 0x28], edx
00414bac  89da                   mov      edx, ebx
00414bae  89d8                   mov      eax, ebx
00414bb0  c1fa1f                 sar      edx, 0x1f
00414bb3  f7f9                   idiv     ecx
00414bb5  668b1d20875000         mov      bx, word ptr [0x508720]
00414bbc  8944242c               mov      dword ptr [esp + 0x2c], eax
00414bc0  663b5c2428             cmp      bx, word ptr [esp + 0x28]
00414bc5  0f8792000000           ja       0x414c5d
00414bcb  31c0                   xor      eax, eax
00414bcd  31d2                   xor      edx, edx
00414bcf  66a124875000           mov      ax, word ptr [0x508724]
00414bd5  6689da                 mov      dx, bx
00414bd8  01d0                   add      eax, edx
00414bda  31d2                   xor      edx, edx
00414bdc  668b542428             mov      dx, word ptr [esp + 0x28]
00414be1  39c2                   cmp      edx, eax
00414be3  0f8d74000000           jge      0x414c5d
00414be9  8b44242c               mov      eax, dword ptr [esp + 0x2c]
00414bed  668b0d22875000         mov      cx, word ptr [0x508722]
00414bf4  6639c8                 cmp      ax, cx
00414bf7  0f8260000000           jb       0x414c5d
00414bfd  31c0                   xor      eax, eax
00414bff  31d2                   xor      edx, edx
00414c01  66a126875000           mov      ax, word ptr [0x508726]
00414c07  6689ca                 mov      dx, cx
00414c0a  01d0                   add      eax, edx
00414c0c  31d2                   xor      edx, edx
00414c0e  668b54242c             mov      dx, word ptr [esp + 0x2c]
00414c13  39c2                   cmp      edx, eax
00414c15  0f8d42000000           jge      0x414c5d
00414c1b  bb05000000             mov      ebx, 5
00414c20  a17c8f5000             mov      eax, dword ptr [0x508f7c]
00414c25  31d2                   xor      edx, edx
00414c27  f7f3                   div      ebx
00414c29  83e001                 and      eax, 1
00414c2c  31db                   xor      ebx, ebx
00414c2e  05431e0000             add      eax, 0x1e43
00414c33  6689c3                 mov      bx, ax
00414c36  8b44242c               mov      eax, dword ptr [esp + 0x2c]
00414c3a  29c8                   sub      eax, ecx
00414c3c  c1e005                 shl      eax, 5
00414c3f  668b0d20875000         mov      cx, word ptr [0x508720]
00414c46  0fbfd0                 movsx    edx, ax
00414c49  8b442428               mov      eax, dword ptr [esp + 0x28]
00414c4d  29c8                   sub      eax, ecx
00414c4f  c1e005                 shl      eax, 5
00414c52  b901000000             mov      ecx, 1
00414c57  98                     cwde     
00414c58  e8ea650400             call     0x45b247 ; PasteBobCmp
00414c5d  8a8682000000           mov      al, byte ptr [esi + 0x82]
00414c63  3c01                   cmp      al, 1
00414c65  720e                   jb       0x414c75
00414c67  0f8620010000           jbe      0x414d8d
00414c6d  3c02                   cmp      al, 2
00414c6f  0f84e1000000           je       0x414d56
00414c75  8b442428               mov      eax, dword ptr [esp + 0x28]
00414c79  663b0520875000         cmp      ax, word ptr [0x508720]
00414c80  0f829e000000           jb       0x414d24
00414c86  31d2                   xor      edx, edx
00414c88  31c0                   xor      eax, eax
00414c8a  668b1520875000         mov      dx, word ptr [0x508720]
00414c91  66a124875000           mov      ax, word ptr [0x508724]
00414c97  01d0                   add      eax, edx
00414c99  31d2                   xor      edx, edx
00414c9b  668b542428             mov      dx, word ptr [esp + 0x28]
00414ca0  39c2                   cmp      edx, eax
00414ca2  0f8d7c000000           jge      0x414d24
00414ca8  8b44242c               mov      eax, dword ptr [esp + 0x2c]
00414cac  668b1d22875000         mov      bx, word ptr [0x508722]
00414cb3  6639d8                 cmp      ax, bx
00414cb6  0f8268000000           jb       0x414d24
00414cbc  31d2                   xor      edx, edx
00414cbe  31c0                   xor      eax, eax
00414cc0  668b1526875000         mov      dx, word ptr [0x508726]
00414cc7  6689d8                 mov      ax, bx
00414cca  01d0                   add      eax, edx
00414ccc  31d2                   xor      edx, edx
00414cce  668b54242c             mov      dx, word ptr [esp + 0x2c]
00414cd3  39c2                   cmp      edx, eax
00414cd5  0f8d49000000           jge      0x414d24
00414cdb  bb05000000             mov      ebx, 5
00414ce0  a17c8f5000             mov      eax, dword ptr [0x508f7c]
00414ce5  31d2                   xor      edx, edx
00414ce7  f7f3                   div      ebx
00414ce9  83e001                 and      eax, 1
00414cec  31db                   xor      ebx, ebx
00414cee  05451e0000             add      eax, 0x1e45
00414cf3  668b0d22875000         mov      cx, word ptr [0x508722]
00414cfa  6689c3                 mov      bx, ax
00414cfd  8b44242c               mov      eax, dword ptr [esp + 0x2c]
00414d01  29c8                   sub      eax, ecx
00414d03  c1e005                 shl      eax, 5
00414d06  668b0d20875000         mov      cx, word ptr [0x508720]
00414d0d  0fbfd0                 movsx    edx, ax
00414d10  8b442428               mov      eax, dword ptr [esp + 0x28]
00414d14  29c8                   sub      eax, ecx
00414d16  c1e005                 shl      eax, 5
00414d19  b901000000             mov      ecx, 1
00414d1e  98                     cwde     
00414d1f  e823650400             call     0x45b247 ; PasteBobCmp
00414d24  8b5c2434               mov      ebx, dword ptr [esp + 0x34]
00414d28  89fa                   mov      edx, edi
00414d2a  8a4601                 mov      al, byte ptr [esi + 1]
00414d2d  83c202                 add      edx, 2
00414d30  83c31a                 add      ebx, 0x1a
00414d33  3c06                   cmp      al, 6
00414d35  0f8286050000           jb       0x4152c1
00414d3b  0f8667050000           jbe      0x4152a8
00414d41  3c07                   cmp      al, 7
00414d43  0f8657040000           jbe      0x4151a0
00414d49  3c0d                   cmp      al, 0xd
00414d4b  0f8409020000           je       0x414f5a
00414d51  e973050000             jmp      0x4152c9 ; 
00414d56  31c0                   xor      eax, eax
00414d58  668b8680000000         mov      ax, word ptr [esi + 0x80]
00414d5f  31db                   xor      ebx, ebx
00414d61  e87c610000             call     0x41aee2 ; BatimentGetCase
00414d66  6689c3                 mov      bx, ax
00414d69  b900010000             mov      ecx, 0x100
00414d6e  89da                   mov      edx, ebx
00414d70  89d8                   mov      eax, ebx
00414d72  c1fa1f                 sar      edx, 0x1f
00414d75  f7f9                   idiv     ecx
00414d77  89542428               mov      dword ptr [esp + 0x28], edx
00414d7b  89da                   mov      edx, ebx
00414d7d  89d8                   mov      eax, ebx
00414d7f  c1fa1f                 sar      edx, 0x1f
00414d82  f7f9                   idiv     ecx
00414d84  8944242c               mov      dword ptr [esp + 0x2c], eax
00414d88  e9e8feffff             jmp      0x414c75 ; 
00414d8d  31db                   xor      ebx, ebx
00414d8f  668b9e80000000         mov      bx, word ptr [esi + 0x80]
00414d96  ebd1                   jmp      0x414d69 ; 
00414d98  31db                   xor      ebx, ebx
00414d9a  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00414da0  89da                   mov      edx, ebx
00414da2  89d8                   mov      eax, ebx
00414da4  c1fa1f                 sar      edx, 0x1f
00414da7  2bc2                   sub      eax, edx
00414da9  d1f8                   sar      eax, 1
00414dab  31c9                   xor      ecx, ecx
00414dad  8a8ea5000000           mov      cl, byte ptr [esi + 0xa5]
00414db3  0fafc8                 imul     ecx, eax
00414db6  8d53ff                 lea      edx, [ebx - 1]
00414db9  89d0                   mov      eax, edx
00414dbb  c1fa1f                 sar      edx, 0x1f
00414dbe  2bc2                   sub      eax, edx
00414dc0  d1f8                   sar      eax, 1
00414dc2  bd02000000             mov      ebp, 2
00414dc7  89da                   mov      edx, ebx
00414dc9  01c1                   add      ecx, eax
00414dcb  89d8                   mov      eax, ebx
00414dcd  c1fa1f                 sar      edx, 0x1f
00414dd0  f7fd                   idiv     ebp
00414dd2  31c0                   xor      eax, eax
00414dd4  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414dda  0fafc2                 imul     eax, edx
00414ddd  01c8                   add      eax, ecx
00414ddf  31db                   xor      ebx, ebx
00414de1  0512110000             add      eax, 0x1112
00414de6  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00414dea  6689c3                 mov      bx, ax
00414ded  8b442434               mov      eax, dword ptr [esp + 0x34]
00414df1  01c8                   add      eax, ecx
00414df3  0fbfd0                 movsx    edx, ax
00414df6  8b442410               mov      eax, dword ptr [esp + 0x10]
00414dfa  01f8                   add      eax, edi
00414dfc  b901000000             mov      ecx, 1
00414e01  98                     cwde     
00414e02  e88f690400             call     0x45b796 ; PasteOmbreCmp
00414e07  31db                   xor      ebx, ebx
00414e09  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00414e0f  89da                   mov      edx, ebx
00414e11  89d8                   mov      eax, ebx
00414e13  c1fa1f                 sar      edx, 0x1f
00414e16  f7fd                   idiv     ebp
00414e18  31d2                   xor      edx, edx
00414e1a  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00414e20  0fafc2                 imul     eax, edx
00414e23  8d53ff                 lea      edx, [ebx - 1]
00414e26  890424                 mov      dword ptr [esp], eax
00414e29  89d0                   mov      eax, edx
00414e2b  c1fa1f                 sar      edx, 0x1f
00414e2e  f7fd                   idiv     ebp
00414e30  8b2c24                 mov      ebp, dword ptr [esp]
00414e33  89da                   mov      edx, ebx
00414e35  01c5                   add      ebp, eax
00414e37  b802000000             mov      eax, 2
00414e3c  c1fa1f                 sar      edx, 0x1f
00414e3f  890424                 mov      dword ptr [esp], eax
00414e42  89d8                   mov      eax, ebx
00414e44  f73c24                 idiv     dword ptr [esp]
00414e47  31c0                   xor      eax, eax
00414e49  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414e4f  0fafc2                 imul     eax, edx
00414e52  01e8                   add      eax, ebp
00414e54  31db                   xor      ebx, ebx
00414e56  05d2100000             add      eax, 0x10d2
00414e5b  8b54240c               mov      edx, dword ptr [esp + 0xc]
00414e5f  6689c3                 mov      bx, ax
00414e62  8b442434               mov      eax, dword ptr [esp + 0x34]
00414e66  01d0                   add      eax, edx
00414e68  0fbfd0                 movsx    edx, ax
00414e6b  8b442410               mov      eax, dword ptr [esp + 0x10]
00414e6f  01f8                   add      eax, edi
00414e71  6689442438             mov      word ptr [esp + 0x38], ax
00414e76  31c9                   xor      ecx, ecx
00414e78  8b442436               mov      eax, dword ptr [esp + 0x36]
00414e7c  668b4c2430             mov      cx, word ptr [esp + 0x30]
00414e81  c1f810                 sar      eax, 0x10
00414e84  e8bec2ffff             call     0x411147 ; AffCorpsEngin
00414e89  e9ee000000             jmp      0x414f7c ; 
00414e8e  31db                   xor      ebx, ebx
00414e90  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00414e96  89da                   mov      edx, ebx
00414e98  89d8                   mov      eax, ebx
00414e9a  c1fa1f                 sar      edx, 0x1f
00414e9d  2bc2                   sub      eax, edx
00414e9f  d1f8                   sar      eax, 1
00414ea1  31c9                   xor      ecx, ecx
00414ea3  8a8ea5000000           mov      cl, byte ptr [esi + 0xa5]
00414ea9  0fafc8                 imul     ecx, eax
00414eac  8d53ff                 lea      edx, [ebx - 1]
00414eaf  89d0                   mov      eax, edx
00414eb1  c1fa1f                 sar      edx, 0x1f
00414eb4  2bc2                   sub      eax, edx
00414eb6  d1f8                   sar      eax, 1
00414eb8  bd02000000             mov      ebp, 2
00414ebd  89da                   mov      edx, ebx
00414ebf  01c1                   add      ecx, eax
00414ec1  89d8                   mov      eax, ebx
00414ec3  c1fa1f                 sar      edx, 0x1f
00414ec6  f7fd                   idiv     ebp
00414ec8  31c0                   xor      eax, eax
00414eca  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414ed0  0fafc2                 imul     eax, edx
00414ed3  8b54240c               mov      edx, dword ptr [esp + 0xc]
00414ed7  01c1                   add      ecx, eax
00414ed9  8b442434               mov      eax, dword ptr [esp + 0x34]
00414edd  31db                   xor      ebx, ebx
00414edf  01d0                   add      eax, edx
00414ee1  81c132110000           add      ecx, 0x1132
00414ee7  0fbfd0                 movsx    edx, ax
00414eea  8b442410               mov      eax, dword ptr [esp + 0x10]
00414eee  6689cb                 mov      bx, cx
00414ef1  01f8                   add      eax, edi
00414ef3  b901000000             mov      ecx, 1
00414ef8  98                     cwde     
00414ef9  e898680400             call     0x45b796 ; PasteOmbreCmp
00414efe  31db                   xor      ebx, ebx
00414f00  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00414f06  89da                   mov      edx, ebx
00414f08  89d8                   mov      eax, ebx
00414f0a  c1fa1f                 sar      edx, 0x1f
00414f0d  f7fd                   idiv     ebp
00414f0f  31d2                   xor      edx, edx
00414f11  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00414f17  0fafc2                 imul     eax, edx
00414f1a  8d53ff                 lea      edx, [ebx - 1]
00414f1d  890424                 mov      dword ptr [esp], eax
00414f20  89d0                   mov      eax, edx
00414f22  c1fa1f                 sar      edx, 0x1f
00414f25  f7fd                   idiv     ebp
00414f27  ba02000000             mov      edx, 2
00414f2c  8b2c24                 mov      ebp, dword ptr [esp]
00414f2f  891424                 mov      dword ptr [esp], edx
00414f32  01c5                   add      ebp, eax
00414f34  89d8                   mov      eax, ebx
00414f36  89da                   mov      edx, ebx
00414f38  8b1c24                 mov      ebx, dword ptr [esp]
00414f3b  c1fa1f                 sar      edx, 0x1f
00414f3e  f7fb                   idiv     ebx
00414f40  31c0                   xor      eax, eax
00414f42  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414f48  0fafd0                 imul     edx, eax
00414f4b  8d042a                 lea      eax, [edx + ebp]
00414f4e  31db                   xor      ebx, ebx
00414f50  05f2100000             add      eax, 0x10f2
00414f55  e901ffffff             jmp      0x414e5b ; 
00414f5a  8a8689000000           mov      al, byte ptr [esi + 0x89]
00414f60  3c01                   cmp      al, 1
00414f62  7210                   jb       0x414f74
00414f64  0f8624ffffff           jbe      0x414e8e
00414f6a  3c04                   cmp      al, 4
00414f6c  0f8626feffff           jbe      0x414d98
00414f72  eb08                   jmp      0x414f7c ; 
00414f74  84c0                   test     al, al
00414f76  0f841cfeffff           je       0x414d98
00414f7c  8b442434               mov      eax, dword ptr [esp + 0x34]
00414f80  83e809                 sub      eax, 9
00414f83  66897c2424             mov      word ptr [esp + 0x24], di
00414f88  6689442420             mov      word ptr [esp + 0x20], ax
00414f8d  e937030000             jmp      0x4152c9 ; 
00414f92  8d460a                 lea      eax, [esi + 0xa]
00414f95  8b5c2434               mov      ebx, dword ptr [esp + 0x34]
00414f99  e81b210300             call     0x4470b9 ; BagVide
00414f9e  88c2                   mov      dl, al
00414fa0  89f8                   mov      eax, edi
00414fa2  83c31a                 add      ebx, 0x1a
00414fa5  0502000000             add      eax, 2
00414faa  84d2                   test     dl, dl
00414fac  743a                   je       0x414fe8
00414fae  b901000000             mov      ecx, 1
00414fb3  0fbfd3                 movsx    edx, bx
00414fb6  98                     cwde     
00414fb7  bb202a0000             mov      ebx, 0x2a20
00414fbc  e8d5670400             call     0x45b796 ; PasteOmbreCmp
00414fc1  31d2                   xor      edx, edx
00414fc3  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414fc9  42                     inc      edx
00414fca  89d0                   mov      eax, edx
00414fcc  c1fa1f                 sar      edx, 0x1f
00414fcf  2bc2                   sub      eax, edx
00414fd1  d1f8                   sar      eax, 1
00414fd3  89c2                   mov      edx, eax
00414fd5  c1e203                 shl      edx, 3
00414fd8  31c0                   xor      eax, eax
00414fda  81c23a060000           add      edx, 0x63a
00414fe0  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414fe6  eb35                   jmp      0x41501d ; 
00414fe8  b901000000             mov      ecx, 1
00414fed  0fbfd3                 movsx    edx, bx
00414ff0  98                     cwde     
00414ff1  bb202a0000             mov      ebx, 0x2a20
00414ff6  e89b670400             call     0x45b796 ; PasteOmbreCmp
00414ffb  31d2                   xor      edx, edx
00414ffd  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415003  42                     inc      edx
00415004  89d0                   mov      eax, edx
00415006  c1fa1f                 sar      edx, 0x1f
00415009  2bc2                   sub      eax, edx
0041500b  d1f8                   sar      eax, 1
0041500d  c1e003                 shl      eax, 3
00415010  31d2                   xor      edx, edx
00415012  059a060000             add      eax, 0x69a
00415017  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
0041501d  31db                   xor      ebx, ebx
0041501f  01d0                   add      eax, edx
00415021  8b54240c               mov      edx, dword ptr [esp + 0xc]
00415025  6689c3                 mov      bx, ax
00415028  8b442434               mov      eax, dword ptr [esp + 0x34]
0041502c  01d0                   add      eax, edx
0041502e  0fbfd0                 movsx    edx, ax
00415031  8b442410               mov      eax, dword ptr [esp + 0x10]
00415035  01f8                   add      eax, edi
00415037  6689442438             mov      word ptr [esp + 0x38], ax
0041503c  31c9                   xor      ecx, ecx
0041503e  8b442436               mov      eax, dword ptr [esp + 0x36]
00415042  668b4c2430             mov      cx, word ptr [esp + 0x30]
00415047  c1f810                 sar      eax, 0x10
0041504a  e8f8c0ffff             call     0x411147 ; AffCorpsEngin
0041504f  e928ffffff             jmp      0x414f7c ; 
00415054  b901000000             mov      ecx, 1
00415059  0fbfeb                 movsx    ebp, bx
0041505c  0fbfc2                 movsx    eax, dx
0041505f  bb202a0000             mov      ebx, 0x2a20
00415064  89ea                   mov      edx, ebp
00415066  e82b670400             call     0x45b796 ; PasteOmbreCmp
0041506b  31d2                   xor      edx, edx
0041506d  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415073  42                     inc      edx
00415074  89d0                   mov      eax, edx
00415076  c1fa1f                 sar      edx, 0x1f
00415079  2bc2                   sub      eax, edx
0041507b  d1f8                   sar      eax, 1
0041507d  c1e002                 shl      eax, 2
00415080  31d2                   xor      edx, edx
00415082  057e060000             add      eax, 0x67e
00415087  eb8e                   jmp      0x415017 ; 
00415089  8a8689000000           mov      al, byte ptr [esi + 0x89]
0041508f  3c01                   cmp      al, 1
00415091  720f                   jb       0x4150a2
00415093  76bf                   jbe      0x415054
00415095  3c03                   cmp      al, 3
00415097  0f86f5feffff           jbe      0x414f92
0041509d  e9dafeffff             jmp      0x414f7c ; 
004150a2  84c0                   test     al, al
004150a4  0f84e8feffff           je       0x414f92
004150aa  e9cdfeffff             jmp      0x414f7c ; 
004150af  8b542434               mov      edx, dword ptr [esp + 0x34]
004150b3  8d460a                 lea      eax, [esi + 0xa]
004150b6  89fb                   mov      ebx, edi
004150b8  e8fc1f0300             call     0x4470b9 ; BagVide
004150bd  83c302                 add      ebx, 2
004150c0  83c21a                 add      edx, 0x1a
004150c3  84c0                   test     al, al
004150c5  746e                   je       0x415135
004150c7  b901000000             mov      ecx, 1
004150cc  0fbfd2                 movsx    edx, dx
004150cf  0fbfc3                 movsx    eax, bx
004150d2  bb202a0000             mov      ebx, 0x2a20
004150d7  e8ba660400             call     0x45b796 ; PasteOmbreCmp
004150dc  31d2                   xor      edx, edx
004150de  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004150e4  42                     inc      edx
004150e5  89d0                   mov      eax, edx
004150e7  c1fa1f                 sar      edx, 0x1f
004150ea  2bc2                   sub      eax, edx
004150ec  d1f8                   sar      eax, 1
004150ee  c1e003                 shl      eax, 3
004150f1  31d2                   xor      edx, edx
004150f3  053a050000             add      eax, 0x53a
004150f8  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004150fe  31db                   xor      ebx, ebx
00415100  01d0                   add      eax, edx
00415102  8b54240c               mov      edx, dword ptr [esp + 0xc]
00415106  6689c3                 mov      bx, ax
00415109  8b442434               mov      eax, dword ptr [esp + 0x34]
0041510d  01d0                   add      eax, edx
0041510f  0fbfd0                 movsx    edx, ax
00415112  8b442410               mov      eax, dword ptr [esp + 0x10]
00415116  01f8                   add      eax, edi
00415118  6689442438             mov      word ptr [esp + 0x38], ax
0041511d  31c9                   xor      ecx, ecx
0041511f  8b442436               mov      eax, dword ptr [esp + 0x36]
00415123  668b4c2430             mov      cx, word ptr [esp + 0x30]
00415128  c1f810                 sar      eax, 0x10
0041512b  e817c0ffff             call     0x411147 ; AffCorpsEngin
00415130  e947feffff             jmp      0x414f7c ; 
00415135  b901000000             mov      ecx, 1
0041513a  0fbfd2                 movsx    edx, dx
0041513d  0fbfc3                 movsx    eax, bx
00415140  bb202a0000             mov      ebx, 0x2a20
00415145  e84c660400             call     0x45b796 ; PasteOmbreCmp
0041514a  31d2                   xor      edx, edx
0041514c  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415152  42                     inc      edx
00415153  89d0                   mov      eax, edx
00415155  c1fa1f                 sar      edx, 0x1f
00415158  2bc2                   sub      eax, edx
0041515a  d1f8                   sar      eax, 1
0041515c  c1e003                 shl      eax, 3
0041515f  31d2                   xor      edx, edx
00415161  05ba050000             add      eax, 0x5ba
00415166  eb90                   jmp      0x4150f8 ; 
00415168  b901000000             mov      ecx, 1
0041516d  0fbfeb                 movsx    ebp, bx
00415170  0fbfc2                 movsx    eax, dx
00415173  bb202a0000             mov      ebx, 0x2a20
00415178  89ea                   mov      edx, ebp
0041517a  e817660400             call     0x45b796 ; PasteOmbreCmp
0041517f  31d2                   xor      edx, edx
00415181  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415187  42                     inc      edx
00415188  89d0                   mov      eax, edx
0041518a  c1fa1f                 sar      edx, 0x1f
0041518d  2bc2                   sub      eax, edx
0041518f  d1f8                   sar      eax, 1
00415191  c1e003                 shl      eax, 3
00415194  31d2                   xor      edx, edx
00415196  057a050000             add      eax, 0x57a
0041519b  e958ffffff             jmp      0x4150f8 ; 
004151a0  8a8689000000           mov      al, byte ptr [esi + 0x89]
004151a6  3c03                   cmp      al, 3
004151a8  7217                   jb       0x4151c1
004151aa  0f86fffeffff           jbe      0x4150af
004151b0  3c05                   cmp      al, 5
004151b2  0f86f7feffff           jbe      0x4150af
004151b8  3c0c                   cmp      al, 0xc
004151ba  74ac                   je       0x415168
004151bc  e9bbfdffff             jmp      0x414f7c ; 
004151c1  84c0                   test     al, al
004151c3  0f86e6feffff           jbe      0x4150af
004151c9  30db                   xor      bl, bl
004151cb  885c243c               mov      byte ptr [esp + 0x3c], bl
004151cf  e9a8fdffff             jmp      0x414f7c ; 
004151d4  8d460a                 lea      eax, [esi + 0xa]
004151d7  e8dd1e0300             call     0x4470b9 ; BagVide
004151dc  84c0                   test     al, al
004151de  7437                   je       0x415217
004151e0  b901000000             mov      ecx, 1
004151e5  0fbfc3                 movsx    eax, bx
004151e8  0fbfea                 movsx    ebp, dx
004151eb  bb202a0000             mov      ebx, 0x2a20
004151f0  89c2                   mov      edx, eax
004151f2  89e8                   mov      eax, ebp
004151f4  e89d650400             call     0x45b796 ; PasteOmbreCmp
004151f9  31d2                   xor      edx, edx
004151fb  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415201  42                     inc      edx
00415202  89d0                   mov      eax, edx
00415204  c1fa1f                 sar      edx, 0x1f
00415207  2bc2                   sub      eax, edx
00415209  d1f8                   sar      eax, 1
0041520b  c1e003                 shl      eax, 3
0041520e  31d2                   xor      edx, edx
00415210  059a0b0000             add      eax, 0xb9a
00415215  eb35                   jmp      0x41524c ; 
00415217  b901000000             mov      ecx, 1
0041521c  0fbfc3                 movsx    eax, bx
0041521f  0fbfea                 movsx    ebp, dx
00415222  bb202a0000             mov      ebx, 0x2a20
00415227  89c2                   mov      edx, eax
00415229  89e8                   mov      eax, ebp
0041522b  e866650400             call     0x45b796 ; PasteOmbreCmp
00415230  31d2                   xor      edx, edx
00415232  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00415238  42                     inc      edx
00415239  89d0                   mov      eax, edx
0041523b  c1fa1f                 sar      edx, 0x1f
0041523e  2bc2                   sub      eax, edx
00415240  d1f8                   sar      eax, 1
00415242  c1e003                 shl      eax, 3
00415245  31d2                   xor      edx, edx
00415247  05da0b0000             add      eax, 0xbda
0041524c  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00415252  31db                   xor      ebx, ebx
00415254  01d0                   add      eax, edx
00415256  8b54240c               mov      edx, dword ptr [esp + 0xc]
0041525a  6689c3                 mov      bx, ax
0041525d  8b442434               mov      eax, dword ptr [esp + 0x34]
00415261  01d0                   add      eax, edx
00415263  0fbfd0                 movsx    edx, ax
00415266  8b442410               mov      eax, dword ptr [esp + 0x10]
0041526a  01f8                   add      eax, edi
0041526c  6689442438             mov      word ptr [esp + 0x38], ax
00415271  31c9                   xor      ecx, ecx
00415273  8b442436               mov      eax, dword ptr [esp + 0x36]
00415277  668b4c2430             mov      cx, word ptr [esp + 0x30]
0041527c  c1f810                 sar      eax, 0x10
0041527f  e8c3beffff             call     0x411147 ; AffCorpsEngin
00415284  e9f3fcffff             jmp      0x414f7c ; 
00415289  b901000000             mov      ecx, 1
0041528e  0fbfeb                 movsx    ebp, bx
00415291  0fbfc2                 movsx    eax, dx
00415294  bb202a0000             mov      ebx, 0x2a20
00415299  89ea                   mov      edx, ebp
0041529b  eb8e                   jmp      0x41522b ; 
0041529d  30ff                   xor      bh, bh
0041529f  887c243c               mov      byte ptr [esp + 0x3c], bh
004152a3  e9d4fcffff             jmp      0x414f7c ; 
004152a8  8a8689000000           mov      al, byte ptr [esi + 0x89]
004152ae  3c02                   cmp      al, 2
004152b0  0f821effffff           jb       0x4151d4
004152b6  76d1                   jbe      0x415289
004152b8  3c03                   cmp      al, 3
004152ba  74e1                   je       0x41529d
004152bc  e9bbfcffff             jmp      0x414f7c ; 
004152c1  3c05                   cmp      al, 5
004152c3  0f84c0fdffff           je       0x415089
004152c9  807c243c00             cmp      byte ptr [esp + 0x3c], 0
004152ce  0f84ba010000           je       0x41548e
004152d4  8a2d41805000           mov      ch, byte ptr [0x508041]
004152da  3a2e                   cmp      ch, byte ptr [esi]
004152dc  7509                   jne      0x4152e7
004152de  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
004152e5  7516                   jne      0x4152fd
004152e7  8b5c2430               mov      ebx, dword ptr [esp + 0x30]
004152eb  663b1dc26a4900         cmp      bx, word ptr [0x496ac2]
004152f2  7409                   je       0x4152fd
004152f4  803d8f8f500000         cmp      byte ptr [0x508f8f], 0
004152fb  741f                   je       0x41531c
004152fd  8b54241e               mov      edx, dword ptr [esp + 0x1e]
00415301  31db                   xor      ebx, ebx
00415303  8b442422               mov      eax, dword ptr [esp + 0x22]
00415307  668b5c2430             mov      bx, word ptr [esp + 0x30]
0041530c  c1fa10                 sar      edx, 0x10
0041530f  c1f810                 sar      eax, 0x10
00415312  e8cdb8ffff             call     0x410be4 ; AffInfoSelection
00415317  e972010000             jmp      0x41548e ; 
0041531c  31d2                   xor      edx, edx
0041531e  6689da                 mov      dx, bx
00415321  89d0                   mov      eax, edx
00415323  c1e004                 shl      eax, 4
00415326  01d0                   add      eax, edx
00415328  c1e002                 shl      eax, 2
0041532b  01d0                   add      eax, edx
0041532d  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00415333  c1e002                 shl      eax, 2
00415336  01d0                   add      eax, edx
00415338  668b5004               mov      dx, word ptr [eax + 4]
0041533c  663b5076               cmp      dx, word ptr [eax + 0x76]
00415340  7512                   jne      0x415354
00415342  668b4074               mov      ax, word ptr [eax + 0x74]
00415346  25ffff0000             and      eax, 0xffff
0041534b  83f864                 cmp      eax, 0x64
0041534e  7d04                   jge      0x415354
00415350  b001                   mov      al, 1
00415352  eb02                   jmp      0x415356 ; 
00415354  30c0                   xor      al, al
00415356  84c0                   test     al, al
00415358  0f84a8000000           je       0x415406
0041535e  31d2                   xor      edx, edx
00415360  668b5674               mov      dx, word ptr [esi + 0x74]
00415364  bb05000000             mov      ebx, 5
00415369  89d0                   mov      eax, edx
0041536b  c1fa1f                 sar      edx, 0x1f
0041536e  f7fb                   idiv     ebx
00415370  89c2                   mov      edx, eax
00415372  bb02000000             mov      ebx, 2
00415377  c1fa1f                 sar      edx, 0x1f
0041537a  f7fb                   idiv     ebx
0041537c  85d2                   test     edx, edx
0041537e  0f8582000000           jne      0x415406
00415384  668b542430             mov      dx, word ptr [esp + 0x30]
00415389  89d0                   mov      eax, edx
0041538b  c1e004                 shl      eax, 4
0041538e  01d0                   add      eax, edx
00415390  c1e002                 shl      eax, 2
00415393  01d0                   add      eax, edx
00415395  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
0041539b  c1e002                 shl      eax, 2
0041539e  01c3                   add      ebx, eax
004153a0  31c0                   xor      eax, eax
004153a2  8a4301                 mov      al, byte ptr [ebx + 1]
004153a5  e88ad80200             call     0x442c34 ; TypeEnginSeFatigue
004153aa  84c0                   test     al, al
004153ac  7458                   je       0x415406
004153ae  8b4c2424               mov      ecx, dword ptr [esp + 0x24]
004153b2  8b542420               mov      edx, dword ptr [esp + 0x20]
004153b6  31c0                   xor      eax, eax
004153b8  83e908                 sub      ecx, 8
004153bb  8a03                   mov      al, byte ptr [ebx]
004153bd  83ea02                 sub      edx, 2
004153c0  3dc8000000             cmp      eax, 0xc8
004153c5  7520                   jne      0x4153e7
004153c7  668b4304               mov      ax, word ptr [ebx + 4]
004153cb  052b1e0000             add      eax, 0x1e2b
004153d0  31db                   xor      ebx, ebx
004153d2  0fbfd2                 movsx    edx, dx
004153d5  6689c3                 mov      bx, ax
004153d8  0fbfc1                 movsx    eax, cx
004153db  b901000000             mov      ecx, 1
004153e0  e8625e0400             call     0x45b247 ; PasteBobCmp
004153e5  eb1f                   jmp      0x415406 ; 
004153e7  50                     push     eax
004153e8  668b4304               mov      ax, word ptr [ebx + 4]
004153ec  052b1e0000             add      eax, 0x1e2b
004153f1  31db                   xor      ebx, ebx
004153f3  0fbfd2                 movsx    edx, dx
004153f6  6689c3                 mov      bx, ax
004153f9  0fbfc1                 movsx    eax, cx
004153fc  b901000000             mov      ecx, 1
00415401  e84f700400             call     0x45c455 ; PastePlayerCmp
00415406  80beba00000000         cmp      byte ptr [esi + 0xba], 0
0041540d  0f847b000000           je       0x41548e
00415413  bb05000000             mov      ebx, 5
00415418  a17c8f5000             mov      eax, dword ptr [0x508f7c]
0041541d  31d2                   xor      edx, edx
0041541f  f7f3                   div      ebx
00415421  85d2                   test     edx, edx
00415423  7569                   jne      0x41548e
00415425  31db                   xor      ebx, ebx
00415427  668b5c2430             mov      bx, word ptr [esp + 0x30]
0041542c  89d8                   mov      eax, ebx
0041542e  c1e004                 shl      eax, 4
00415431  01d8                   add      eax, ebx
00415433  c1e002                 shl      eax, 2
00415436  01d8                   add      eax, ebx
00415438  8b0da0194e00           mov      ecx, dword ptr [0x4e19a0]
0041543e  c1e002                 shl      eax, 2
00415441  89da                   mov      edx, ebx
00415443  01c1                   add      ecx, eax
00415445  89d8                   mov      eax, ebx
00415447  30fe                   xor      dh, bh
00415449  e858a50300             call     0x44f9a6 ; EnginGetLevelExperience
0041544e  88c2                   mov      dl, al
00415450  31c0                   xor      eax, eax
00415452  8a4101                 mov      al, byte ptr [ecx + 1]
00415455  e856ce0200             call     0x4422b0 ; TypeEnginGagneXP
0041545a  84c0                   test     al, al
0041545c  7430                   je       0x41548e
0041545e  31c0                   xor      eax, eax
00415460  6689d0                 mov      ax, dx
00415463  85c0                   test     eax, eax
00415465  7427                   je       0x41548e
00415467  8b442420               mov      eax, dword ptr [esp + 0x20]
0041546b  81c2461e0000           add      edx, 0x1e46
00415471  31db                   xor      ebx, ebx
00415473  83e802                 sub      eax, 2
00415476  6689d3                 mov      bx, dx
00415479  0fbfd0                 movsx    edx, ax
0041547c  8b442424               mov      eax, dword ptr [esp + 0x24]
00415480  83e808                 sub      eax, 8
00415483  b901000000             mov      ecx, 1
00415488  98                     cwde     
00415489  e8b95d0400             call     0x45b247 ; PasteBobCmp
0041548e  83c440                 add      esp, 0x40
00415491  5d                     pop      ebp
00415492  5f                     pop      edi
00415493  5e                     pop      esi
00415494  59                     pop      ecx
00415495  c3                     ret      
