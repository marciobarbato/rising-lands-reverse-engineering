; AffAttaqueEngin [0x41374c, 0x414495)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041374c  51                     push     ecx
0041374d  56                     push     esi
0041374e  57                     push     edi
0041374f  55                     push     ebp
00413750  83ec3c                 sub      esp, 0x3c
00413753  89c7                   mov      edi, eax
00413755  89542418               mov      dword ptr [esp + 0x18], edx
00413759  895c242c               mov      dword ptr [esp + 0x2c], ebx
0041375d  31c9                   xor      ecx, ecx
0041375f  6689d9                 mov      cx, bx
00413762  89c8                   mov      eax, ecx
00413764  c1e004                 shl      eax, 4
00413767  01c8                   add      eax, ecx
00413769  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
0041376f  c1e002                 shl      eax, 2
00413772  89ca                   mov      edx, ecx
00413774  01c8                   add      eax, ecx
00413776  31da                   xor      edx, ebx
00413778  c1e002                 shl      eax, 2
0041377b  6689542428             mov      word ptr [esp + 0x28], dx
00413780  01c6                   add      esi, eax
00413782  31db                   xor      ebx, ebx
00413784  8d54240c               lea      edx, [esp + 0xc]
00413788  660fbe8686000000       movsx    ax, byte ptr [esi + 0x86]
00413790  66895c2424             mov      word ptr [esp + 0x24], bx
00413795  01c7                   add      edi, eax
00413797  8b442418               mov      eax, dword ptr [esp + 0x18]
0041379b  66897c2434             mov      word ptr [esp + 0x34], di
004137a0  660fbebe87000000       movsx    di, byte ptr [esi + 0x87]
004137a8  895c240c               mov      dword ptr [esp + 0xc], ebx
004137ac  895c2408               mov      dword ptr [esp + 8], ebx
004137b0  01c7                   add      edi, eax
004137b2  31c0                   xor      eax, eax
004137b4  8d5c2408               lea      ebx, [esp + 8]
004137b8  8a4601                 mov      al, byte ptr [esi + 1]
004137bb  e80cd8ffff             call     0x410fcc ; AffCorpsEnginDecalage
004137c0  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
004137c7  0f843b0b0000           je       0x414308
004137cd  8a1541805000           mov      dl, byte ptr [0x508041]
004137d3  3a16                   cmp      dl, byte ptr [esi]
004137d5  0f852d0b0000           jne      0x414308
004137db  8b442434               mov      eax, dword ptr [esp + 0x34]
004137df  8d5c2404               lea      ebx, [esp + 4]
004137e3  8d542420               lea      edx, [esp + 0x20]
004137e7  89442414               mov      dword ptr [esp + 0x14], eax
004137eb  89c8                   mov      eax, ecx
004137ed  e87ad80200             call     0x44106c ; EnginGetTaille
004137f2  31c0                   xor      eax, eax
004137f4  668b442420             mov      ax, word ptr [esp + 0x20]
004137f9  897c2410               mov      dword ptr [esp + 0x10], edi
004137fd  83f801                 cmp      eax, 1
00413800  751a                   jne      0x41381c
00413802  39c0                   cmp      eax, eax
00413804  7516                   jne      0x41381c
00413806  8b442432               mov      eax, dword ptr [esp + 0x32]
0041380a  b901000000             mov      ecx, 1
0041380f  bb1e2a0000             mov      ebx, 0x2a1e
00413814  0fbfd7                 movsx    edx, di
00413817  c1f810                 sar      eax, 0x10
0041381a  eb1c                   jmp      0x413838 ;
0041381c  8b442410               mov      eax, dword ptr [esp + 0x10]
00413820  83e820                 sub      eax, 0x20
00413823  0fbfd0                 movsx    edx, ax
00413826  8b442414               mov      eax, dword ptr [esp + 0x14]
0041382a  b901000000             mov      ecx, 1
0041382f  83e820                 sub      eax, 0x20
00413832  bb1f2a0000             mov      ebx, 0x2a1f
00413837  98                     cwde
00413838  e80a7a0400             call     0x45b247 ; PasteBobCmp
0041383d  31c0                   xor      eax, eax
0041383f  8a4601                 mov      al, byte ptr [esi + 1]
00413842  83f80e                 cmp      eax, 0xe
00413845  0f85bd0a0000           jne      0x414308
0041384b  31c0                   xor      eax, eax
0041384d  668b86d8000000         mov      ax, word ptr [esi + 0xd8]
00413854  85c0                   test     eax, eax
00413856  0f84ac0a0000           je       0x414308
0041385c  31c9                   xor      ecx, ecx
0041385e  894c2430               mov      dword ptr [esp + 0x30], ecx
00413862  eb04                   jmp      0x413868 ;
00413864  ff442430               inc      dword ptr [esp + 0x30]
00413868  8b442430               mov      eax, dword ptr [esp + 0x30]
0041386c  663b86d8000000         cmp      ax, word ptr [esi + 0xd8]
00413873  0f838f0a0000           jae      0x414308
00413879  31c0                   xor      eax, eax
0041387b  668b442430             mov      ax, word ptr [esp + 0x30]
00413880  668b9c46c4000000       mov      bx, word ptr [esi + eax*2 + 0xc4]
00413888  81e3ffff0000           and      ebx, 0xffff
0041388e  b900010000             mov      ecx, 0x100
00413893  89da                   mov      edx, ebx
00413895  89d8                   mov      eax, ebx
00413897  c1fa1f                 sar      edx, 0x1f
0041389a  f7f9                   idiv     ecx
0041389c  89d1                   mov      ecx, edx
0041389e  89da                   mov      edx, ebx
004138a0  89d8                   mov      eax, ebx
004138a2  c1fa1f                 sar      edx, 0x1f
004138a5  c1e208                 shl      edx, 8
004138a8  1bc2                   sbb      eax, edx
004138aa  c1f808                 sar      eax, 8
004138ad  89c3                   mov      ebx, eax
004138af  66a120875000           mov      ax, word ptr [0x508720]
004138b5  6639c1                 cmp      cx, ax
004138b8  72aa                   jb       0x413864
004138ba  31d2                   xor      edx, edx
004138bc  6689c2                 mov      dx, ax
004138bf  31c0                   xor      eax, eax
004138c1  66a124875000           mov      ax, word ptr [0x508724]
004138c7  01d0                   add      eax, edx
004138c9  31d2                   xor      edx, edx
004138cb  6689ca                 mov      dx, cx
004138ce  39c2                   cmp      edx, eax
004138d0  7d92                   jge      0x413864
004138d2  663b1d22875000         cmp      bx, word ptr [0x508722]
004138d9  7289                   jb       0x413864
004138db  31d2                   xor      edx, edx
004138dd  31c0                   xor      eax, eax
004138df  668b1522875000         mov      dx, word ptr [0x508722]
004138e6  66a126875000           mov      ax, word ptr [0x508726]
004138ec  01d0                   add      eax, edx
004138ee  31d2                   xor      edx, edx
004138f0  6689da                 mov      dx, bx
004138f3  39c2                   cmp      edx, eax
004138f5  0f8d69ffffff           jge      0x413864
004138fb  662b1d22875000         sub      bx, word ptr [0x508722]
00413902  c1e305                 shl      ebx, 5
00413905  0fbfd3                 movsx    edx, bx
00413908  662b0d20875000         sub      cx, word ptr [0x508720]
0041390f  c1e105                 shl      ecx, 5
00413912  bbcf1c0000             mov      ebx, 0x1ccf
00413917  0fbfc1                 movsx    eax, cx
0041391a  b901000000             mov      ecx, 1
0041391f  e823790400             call     0x45b247 ; PasteBobCmp
00413924  e93bffffff             jmp      0x413864 ;
00413929  89f8                   mov      eax, edi
0041392b  051a000000             add      eax, 0x1a
00413930  0fbfd0                 movsx    edx, ax
00413933  8b442434               mov      eax, dword ptr [esp + 0x34]
00413937  b901000000             mov      ecx, 1
0041393c  0502000000             add      eax, 2
00413941  bb202a0000             mov      ebx, 0x2a20
00413946  98                     cwde
00413947  e84a7e0400             call     0x45b796 ; PasteOmbreCmp
0041394c  31d2                   xor      edx, edx
0041394e  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413954  42                     inc      edx
00413955  89d0                   mov      eax, edx
00413957  c1fa1f                 sar      edx, 0x1f
0041395a  2bc2                   sub      eax, edx
0041395c  d1f8                   sar      eax, 1
0041395e  31d2                   xor      edx, edx
00413960  48                     dec      eax
00413961  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413967  0fafc2                 imul     eax, edx
0041396a  31d2                   xor      edx, edx
0041396c  05e2090000             add      eax, 0x9e2
00413971  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413977  31db                   xor      ebx, ebx
00413979  01d0                   add      eax, edx
0041397b  6689c3                 mov      bx, ax
0041397e  8b442408               mov      eax, dword ptr [esp + 8]
00413982  01f8                   add      eax, edi
00413984  0fbfd0                 movsx    edx, ax
00413987  8b442434               mov      eax, dword ptr [esp + 0x34]
0041398b  0344240c               add      eax, dword ptr [esp + 0xc]
0041398f  6689442438             mov      word ptr [esp + 0x38], ax
00413994  31c9                   xor      ecx, ecx
00413996  8b442436               mov      eax, dword ptr [esp + 0x36]
0041399a  668b4c242c             mov      cx, word ptr [esp + 0x2c]
0041399f  c1f810                 sar      eax, 0x10
004139a2  83ef09                 sub      edi, 9
004139a5  e89dd7ffff             call     0x411147 ; AffCorpsEngin
004139aa  8b442434               mov      eax, dword ptr [esp + 0x34]
004139ae  66897c2424             mov      word ptr [esp + 0x24], di
004139b3  6689442428             mov      word ptr [esp + 0x28], ax
004139b8  8a3541805000           mov      dh, byte ptr [0x508041]
004139be  3a36                   cmp      dh, byte ptr [esi]
004139c0  7509                   jne      0x4139cb
004139c2  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
004139c9  751a                   jne      0x4139e5
004139cb  8b7c242c               mov      edi, dword ptr [esp + 0x2c]
004139cf  663b3dc26a4900         cmp      di, word ptr [0x496ac2]
004139d6  740d                   je       0x4139e5
004139d8  803d8f8f500000         cmp      byte ptr [0x508f8f], 0
004139df  0f843b090000           je       0x414320
004139e5  8b542422               mov      edx, dword ptr [esp + 0x22]
004139e9  31db                   xor      ebx, ebx
004139eb  8b442426               mov      eax, dword ptr [esp + 0x26]
004139ef  668b5c242c             mov      bx, word ptr [esp + 0x2c]
004139f4  c1fa10                 sar      edx, 0x10
004139f7  c1f810                 sar      eax, 0x10
004139fa  e8e5d1ffff             call     0x410be4 ; AffInfoSelection
004139ff  e9890a0000             jmp      0x41448d ;
00413a04  89f8                   mov      eax, edi
00413a06  051a000000             add      eax, 0x1a
00413a0b  0fbfd0                 movsx    edx, ax
00413a0e  8b442434               mov      eax, dword ptr [esp + 0x34]
00413a12  b901000000             mov      ecx, 1
00413a17  0502000000             add      eax, 2
00413a1c  bb202a0000             mov      ebx, 0x2a20
00413a21  98                     cwde
00413a22  e86f7d0400             call     0x45b796 ; PasteOmbreCmp
00413a27  31d2                   xor      edx, edx
00413a29  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413a2f  42                     inc      edx
00413a30  89d0                   mov      eax, edx
00413a32  c1fa1f                 sar      edx, 0x1f
00413a35  2bc2                   sub      eax, edx
00413a37  d1f8                   sar      eax, 1
00413a39  31d2                   xor      edx, edx
00413a3b  48                     dec      eax
00413a3c  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413a42  0fafd0                 imul     edx, eax
00413a45  31c0                   xor      eax, eax
00413a47  81c262080000           add      edx, 0x862
00413a4d  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413a53  e91fffffff             jmp      0x413977 ;
00413a58  89f8                   mov      eax, edi
00413a5a  051a000000             add      eax, 0x1a
00413a5f  0fbfd0                 movsx    edx, ax
00413a62  8b442434               mov      eax, dword ptr [esp + 0x34]
00413a66  b901000000             mov      ecx, 1
00413a6b  0502000000             add      eax, 2
00413a70  bb202a0000             mov      ebx, 0x2a20
00413a75  98                     cwde
00413a76  e81b7d0400             call     0x45b796 ; PasteOmbreCmp
00413a7b  31d2                   xor      edx, edx
00413a7d  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413a83  42                     inc      edx
00413a84  89d0                   mov      eax, edx
00413a86  c1fa1f                 sar      edx, 0x1f
00413a89  2bc2                   sub      eax, edx
00413a8b  d1f8                   sar      eax, 1
00413a8d  31d2                   xor      edx, edx
00413a8f  48                     dec      eax
00413a90  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413a96  0fafc2                 imul     eax, edx
00413a99  31d2                   xor      edx, edx
00413a9b  0532090000             add      eax, 0x932
00413aa0  e9ccfeffff             jmp      0x413971 ;
00413aa5  31d2                   xor      edx, edx
00413aa7  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413aad  42                     inc      edx
00413aae  89d0                   mov      eax, edx
00413ab0  c1fa1f                 sar      edx, 0x1f
00413ab3  2bc2                   sub      eax, edx
00413ab5  d1f8                   sar      eax, 1
00413ab7  c1e003                 shl      eax, 3
00413aba  31d2                   xor      edx, edx
00413abc  055a0e0000             add      eax, 0xe5a
00413ac1  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413ac7  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413acb  01c2                   add      edx, eax
00413acd  8b442408               mov      eax, dword ptr [esp + 8]
00413ad1  31db                   xor      ebx, ebx
00413ad3  01f8                   add      eax, edi
00413ad5  6689d3                 mov      bx, dx
00413ad8  0fbfd0                 movsx    edx, ax
00413adb  8b442434               mov      eax, dword ptr [esp + 0x34]
00413adf  01c8                   add      eax, ecx
00413ae1  b901000000             mov      ecx, 1
00413ae6  98                     cwde
00413ae7  e8aa7c0400             call     0x45b796 ; PasteOmbreCmp
00413aec  31d2                   xor      edx, edx
00413aee  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413af4  42                     inc      edx
00413af5  89d0                   mov      eax, edx
00413af7  c1fa1f                 sar      edx, 0x1f
00413afa  2bc2                   sub      eax, edx
00413afc  d1f8                   sar      eax, 1
00413afe  31d2                   xor      edx, edx
00413b00  48                     dec      eax
00413b01  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413b07  0fafc2                 imul     eax, edx
00413b0a  31d2                   xor      edx, edx
00413b0c  05a20d0000             add      eax, 0xda2
00413b11  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413b17  31db                   xor      ebx, ebx
00413b19  01d0                   add      eax, edx
00413b1b  6689c3                 mov      bx, ax
00413b1e  8b442408               mov      eax, dword ptr [esp + 8]
00413b22  01f8                   add      eax, edi
00413b24  0fbfd0                 movsx    edx, ax
00413b27  8b442434               mov      eax, dword ptr [esp + 0x34]
00413b2b  0344240c               add      eax, dword ptr [esp + 0xc]
00413b2f  6689442438             mov      word ptr [esp + 0x38], ax
00413b34  31c9                   xor      ecx, ecx
00413b36  8b442436               mov      eax, dword ptr [esp + 0x36]
00413b3a  668b4c242c             mov      cx, word ptr [esp + 0x2c]
00413b3f  c1f810                 sar      eax, 0x10
00413b42  e800d6ffff             call     0x411147 ; AffCorpsEngin
00413b47  8b442434               mov      eax, dword ptr [esp + 0x34]
00413b4b  83ef18                 sub      edi, 0x18
00413b4e  83e80f                 sub      eax, 0xf
00413b51  e958feffff             jmp      0x4139ae ;
00413b56  31d2                   xor      edx, edx
00413b58  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413b5e  42                     inc      edx
00413b5f  89d0                   mov      eax, edx
00413b61  c1fa1f                 sar      edx, 0x1f
00413b64  2bc2                   sub      eax, edx
00413b66  d1f8                   sar      eax, 1
00413b68  c1e003                 shl      eax, 3
00413b6b  31d2                   xor      edx, edx
00413b6d  05da0f0000             add      eax, 0xfda
00413b72  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413b78  31db                   xor      ebx, ebx
00413b7a  01d0                   add      eax, edx
00413b7c  6689c3                 mov      bx, ax
00413b7f  8b442408               mov      eax, dword ptr [esp + 8]
00413b83  01f8                   add      eax, edi
00413b85  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413b89  0fbfd0                 movsx    edx, ax
00413b8c  8b442434               mov      eax, dword ptr [esp + 0x34]
00413b90  01c8                   add      eax, ecx
00413b92  b901000000             mov      ecx, 1
00413b97  98                     cwde
00413b98  e8f97b0400             call     0x45b796 ; PasteOmbreCmp
00413b9d  31d2                   xor      edx, edx
00413b9f  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413ba5  42                     inc      edx
00413ba6  89d0                   mov      eax, edx
00413ba8  c1fa1f                 sar      edx, 0x1f
00413bab  2bc2                   sub      eax, edx
00413bad  d1f8                   sar      eax, 1
00413baf  31d2                   xor      edx, edx
00413bb1  48                     dec      eax
00413bb2  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413bb8  0fafc2                 imul     eax, edx
00413bbb  31d2                   xor      edx, edx
00413bbd  05220f0000             add      eax, 0xf22
00413bc2  e94affffff             jmp      0x413b11 ;
00413bc7  89f8                   mov      eax, edi
00413bc9  051a000000             add      eax, 0x1a
00413bce  0fbfd0                 movsx    edx, ax
00413bd1  8b442434               mov      eax, dword ptr [esp + 0x34]
00413bd5  b901000000             mov      ecx, 1
00413bda  0502000000             add      eax, 2
00413bdf  bb202a0000             mov      ebx, 0x2a20
00413be4  98                     cwde
00413be5  e8ac7b0400             call     0x45b796 ; PasteOmbreCmp
00413bea  31d2                   xor      edx, edx
00413bec  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413bf2  42                     inc      edx
00413bf3  89d0                   mov      eax, edx
00413bf5  c1fa1f                 sar      edx, 0x1f
00413bf8  2bc2                   sub      eax, edx
00413bfa  d1f8                   sar      eax, 1
00413bfc  31d2                   xor      edx, edx
00413bfe  48                     dec      eax
00413bff  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413c05  0fafc2                 imul     eax, edx
00413c08  31d2                   xor      edx, edx
00413c0a  05c20c0000             add      eax, 0xcc2
00413c0f  e95dfdffff             jmp      0x413971 ;
00413c14  89f8                   mov      eax, edi
00413c16  051a000000             add      eax, 0x1a
00413c1b  0fbfd0                 movsx    edx, ax
00413c1e  8b442434               mov      eax, dword ptr [esp + 0x34]
00413c22  b901000000             mov      ecx, 1
00413c27  0502000000             add      eax, 2
00413c2c  bb202a0000             mov      ebx, 0x2a20
00413c31  98                     cwde
00413c32  e85f7b0400             call     0x45b796 ; PasteOmbreCmp
00413c37  31c9                   xor      ecx, ecx
00413c39  668b4c242c             mov      cx, word ptr [esp + 0x2c]
00413c3e  89c8                   mov      eax, ecx
00413c40  e8ccd10200             call     0x440e11 ; EnginGetEtat
00413c45  25ff000000             and      eax, 0xff
00413c4a  83f801                 cmp      eax, 1
00413c4d  752f                   jne      0x413c7e
00413c4f  31d2                   xor      edx, edx
00413c51  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413c57  01c2                   add      edx, eax
00413c59  89d0                   mov      eax, edx
00413c5b  c1fa1f                 sar      edx, 0x1f
00413c5e  2bc2                   sub      eax, edx
00413c60  d1f8                   sar      eax, 1
00413c62  31d2                   xor      edx, edx
00413c64  48                     dec      eax
00413c65  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413c6b  0fafd0                 imul     edx, eax
00413c6e  31c0                   xor      eax, eax
00413c70  81c2b20a0000           add      edx, 0xab2
00413c76  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413c7c  eb3c                   jmp      0x413cba ;
00413c7e  89c8                   mov      eax, ecx
00413c80  e88cd10200             call     0x440e11 ; EnginGetEtat
00413c85  25ff000000             and      eax, 0xff
00413c8a  83f818                 cmp      eax, 0x18
00413c8d  7554                   jne      0x413ce3
00413c8f  31d2                   xor      edx, edx
00413c91  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413c97  42                     inc      edx
00413c98  89d0                   mov      eax, edx
00413c9a  c1fa1f                 sar      edx, 0x1f
00413c9d  2bc2                   sub      eax, edx
00413c9f  d1f8                   sar      eax, 1
00413ca1  31d2                   xor      edx, edx
00413ca3  48                     dec      eax
00413ca4  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413caa  0fafc2                 imul     eax, edx
00413cad  31d2                   xor      edx, edx
00413caf  05520b0000             add      eax, 0xb52
00413cb4  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413cba  31db                   xor      ebx, ebx
00413cbc  01d0                   add      eax, edx
00413cbe  6689c3                 mov      bx, ax
00413cc1  8b442408               mov      eax, dword ptr [esp + 8]
00413cc5  01f8                   add      eax, edi
00413cc7  0fbfd0                 movsx    edx, ax
00413cca  8b442434               mov      eax, dword ptr [esp + 0x34]
00413cce  0344240c               add      eax, dword ptr [esp + 0xc]
00413cd2  6689442438             mov      word ptr [esp + 0x38], ax
00413cd7  8b442436               mov      eax, dword ptr [esp + 0x36]
00413cdb  c1f810                 sar      eax, 0x10
00413cde  e864d4ffff             call     0x411147 ; AffCorpsEngin
00413ce3  8b442434               mov      eax, dword ptr [esp + 0x34]
00413ce7  83ef09                 sub      edi, 9
00413cea  6689442428             mov      word ptr [esp + 0x28], ax
00413cef  66897c2424             mov      word ptr [esp + 0x24], di
00413cf4  e9bffcffff             jmp      0x4139b8 ;
00413cf9  31db                   xor      ebx, ebx
00413cfb  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00413d01  89da                   mov      edx, ebx
00413d03  89d8                   mov      eax, ebx
00413d05  c1fa1f                 sar      edx, 0x1f
00413d08  2bc2                   sub      eax, edx
00413d0a  d1f8                   sar      eax, 1
00413d0c  31d2                   xor      edx, edx
00413d0e  89c1                   mov      ecx, eax
00413d10  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00413d16  0fafca                 imul     ecx, edx
00413d19  8d53ff                 lea      edx, [ebx - 1]
00413d1c  89d0                   mov      eax, edx
00413d1e  c1fa1f                 sar      edx, 0x1f
00413d21  2bc2                   sub      eax, edx
00413d23  d1f8                   sar      eax, 1
00413d25  8d2c01                 lea      ebp, [ecx + eax]
00413d28  89da                   mov      edx, ebx
00413d2a  b902000000             mov      ecx, 2
00413d2f  89d8                   mov      eax, ebx
00413d31  c1fa1f                 sar      edx, 0x1f
00413d34  f7f9                   idiv     ecx
00413d36  31c0                   xor      eax, eax
00413d38  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413d3e  0fafc2                 imul     eax, edx
00413d41  01e8                   add      eax, ebp
00413d43  31db                   xor      ebx, ebx
00413d45  8944241c               mov      dword ptr [esp + 0x1c], eax
00413d49  0572120000             add      eax, 0x1272
00413d4e  6689c3                 mov      bx, ax
00413d51  8b442408               mov      eax, dword ptr [esp + 8]
00413d55  01f8                   add      eax, edi
00413d57  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413d5b  0fbfd0                 movsx    edx, ax
00413d5e  8b442434               mov      eax, dword ptr [esp + 0x34]
00413d62  01c8                   add      eax, ecx
00413d64  b901000000             mov      ecx, 1
00413d69  98                     cwde
00413d6a  e8277a0400             call     0x45b796 ; PasteOmbreCmp
00413d6f  8b44241c               mov      eax, dword ptr [esp + 0x1c]
00413d73  31db                   xor      ebx, ebx
00413d75  0512120000             add      eax, 0x1212
00413d7a  e9fcfbffff             jmp      0x41397b ;
00413d7f  31d2                   xor      edx, edx
00413d81  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413d87  4a                     dec      edx
00413d88  89d0                   mov      eax, edx
00413d8a  c1fa1f                 sar      edx, 0x1f
00413d8d  2bc2                   sub      eax, edx
00413d8f  d1f8                   sar      eax, 1
00413d91  31d2                   xor      edx, edx
00413d93  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413d99  0fafd0                 imul     edx, eax
00413d9c  31c0                   xor      eax, eax
00413d9e  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413da4  01d0                   add      eax, edx
00413da6  31db                   xor      ebx, ebx
00413da8  05ba100000             add      eax, 0x10ba
00413dad  6689c3                 mov      bx, ax
00413db0  8b442408               mov      eax, dword ptr [esp + 8]
00413db4  01f8                   add      eax, edi
00413db6  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413dba  0fbfd0                 movsx    edx, ax
00413dbd  8b442434               mov      eax, dword ptr [esp + 0x34]
00413dc1  01c8                   add      eax, ecx
00413dc3  b901000000             mov      ecx, 1
00413dc8  98                     cwde
00413dc9  e8c8790400             call     0x45b796 ; PasteOmbreCmp
00413dce  31d2                   xor      edx, edx
00413dd0  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413dd6  4a                     dec      edx
00413dd7  89d0                   mov      eax, edx
00413dd9  c1fa1f                 sar      edx, 0x1f
00413ddc  2bc2                   sub      eax, edx
00413dde  d1f8                   sar      eax, 1
00413de0  31d2                   xor      edx, edx
00413de2  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413de8  0fafc2                 imul     eax, edx
00413deb  31d2                   xor      edx, edx
00413ded  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413df3  01d0                   add      eax, edx
00413df5  31db                   xor      ebx, ebx
00413df7  0582100000             add      eax, 0x1082
00413dfc  e97afbffff             jmp      0x41397b ;
00413e01  31db                   xor      ebx, ebx
00413e03  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00413e09  89da                   mov      edx, ebx
00413e0b  89d8                   mov      eax, ebx
00413e0d  c1fa1f                 sar      edx, 0x1f
00413e10  2bc2                   sub      eax, edx
00413e12  d1f8                   sar      eax, 1
00413e14  31c9                   xor      ecx, ecx
00413e16  8a8ea5000000           mov      cl, byte ptr [esi + 0xa5]
00413e1c  0fafc8                 imul     ecx, eax
00413e1f  8d53ff                 lea      edx, [ebx - 1]
00413e22  89d0                   mov      eax, edx
00413e24  c1fa1f                 sar      edx, 0x1f
00413e27  2bc2                   sub      eax, edx
00413e29  d1f8                   sar      eax, 1
00413e2b  8d2c01                 lea      ebp, [ecx + eax]
00413e2e  89da                   mov      edx, ebx
00413e30  b902000000             mov      ecx, 2
00413e35  89d8                   mov      eax, ebx
00413e37  c1fa1f                 sar      edx, 0x1f
00413e3a  f7f9                   idiv     ecx
00413e3c  31c0                   xor      eax, eax
00413e3e  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413e44  0fafc2                 imul     eax, edx
00413e47  01e8                   add      eax, ebp
00413e49  31db                   xor      ebx, ebx
00413e4b  8944241c               mov      dword ptr [esp + 0x1c], eax
00413e4f  05ad130000             add      eax, 0x13ad
00413e54  6689c3                 mov      bx, ax
00413e57  8b442408               mov      eax, dword ptr [esp + 8]
00413e5b  01f8                   add      eax, edi
00413e5d  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413e61  0fbfd0                 movsx    edx, ax
00413e64  8b442434               mov      eax, dword ptr [esp + 0x34]
00413e68  01c8                   add      eax, ecx
00413e6a  b901000000             mov      ecx, 1
00413e6f  98                     cwde
00413e70  e821790400             call     0x45b796 ; PasteOmbreCmp
00413e75  8b44241c               mov      eax, dword ptr [esp + 0x1c]
00413e79  31db                   xor      ebx, ebx
00413e7b  0565130000             add      eax, 0x1365
00413e80  6689c3                 mov      bx, ax
00413e83  8b442408               mov      eax, dword ptr [esp + 8]
00413e87  31d2                   xor      edx, edx
00413e89  01f8                   add      eax, edi
00413e8b  8a96ab000000           mov      dl, byte ptr [esi + 0xab]
00413e91  83e814                 sub      eax, 0x14
00413e94  29d0                   sub      eax, edx
00413e96  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413e9a  0fbfd0                 movsx    edx, ax
00413e9d  8b442434               mov      eax, dword ptr [esp + 0x34]
00413ea1  01c8                   add      eax, ecx
00413ea3  0fb76c242c             movzx    ebp, word ptr [esp + 0x2c]
00413ea8  98                     cwde
00413ea9  89e9                   mov      ecx, ebp
00413eab  e897d2ffff             call     0x411147 ; AffCorpsEngin
00413eb0  31db                   xor      ebx, ebx
00413eb2  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00413eb8  89da                   mov      edx, ebx
00413eba  89d8                   mov      eax, ebx
00413ebc  c1fa1f                 sar      edx, 0x1f
00413ebf  2bc2                   sub      eax, edx
00413ec1  d1f8                   sar      eax, 1
00413ec3  31d2                   xor      edx, edx
00413ec5  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00413ecb  0fafc2                 imul     eax, edx
00413ece  8d53ff                 lea      edx, [ebx - 1]
00413ed1  890424                 mov      dword ptr [esp], eax
00413ed4  89d0                   mov      eax, edx
00413ed6  c1fa1f                 sar      edx, 0x1f
00413ed9  2bc2                   sub      eax, edx
00413edb  d1f8                   sar      eax, 1
00413edd  8b0c24                 mov      ecx, dword ptr [esp]
00413ee0  ba02000000             mov      edx, 2
00413ee5  01c1                   add      ecx, eax
00413ee7  891424                 mov      dword ptr [esp], edx
00413eea  89d8                   mov      eax, ebx
00413eec  89da                   mov      edx, ebx
00413eee  8b1c24                 mov      ebx, dword ptr [esp]
00413ef1  c1fa1f                 sar      edx, 0x1f
00413ef4  f7fb                   idiv     ebx
00413ef6  31c0                   xor      eax, eax
00413ef8  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413efe  0fafd0                 imul     edx, eax
00413f01  01ca                   add      edx, ecx
00413f03  89d0                   mov      eax, edx
00413f05  31db                   xor      ebx, ebx
00413f07  05ad130000             add      eax, 0x13ad
00413f0c  6689c3                 mov      bx, ax
00413f0f  8b442408               mov      eax, dword ptr [esp + 8]
00413f13  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413f17  01f8                   add      eax, edi
00413f19  8954241c               mov      dword ptr [esp + 0x1c], edx
00413f1d  0fbfd0                 movsx    edx, ax
00413f20  8b442434               mov      eax, dword ptr [esp + 0x34]
00413f24  01c8                   add      eax, ecx
00413f26  b901000000             mov      ecx, 1
00413f2b  98                     cwde
00413f2c  e865780400             call     0x45b796 ; PasteOmbreCmp
00413f31  8b44241c               mov      eax, dword ptr [esp + 0x1c]
00413f35  31db                   xor      ebx, ebx
00413f37  0565130000             add      eax, 0x1365
00413f3c  8b542408               mov      edx, dword ptr [esp + 8]
00413f40  6689c3                 mov      bx, ax
00413f43  31c0                   xor      eax, eax
00413f45  01fa                   add      edx, edi
00413f47  8a86ab000000           mov      al, byte ptr [esi + 0xab]
00413f4d  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413f51  29c2                   sub      edx, eax
00413f53  8b442434               mov      eax, dword ptr [esp + 0x34]
00413f57  01c8                   add      eax, ecx
00413f59  0fbfd2                 movsx    edx, dx
00413f5c  98                     cwde
00413f5d  89e9                   mov      ecx, ebp
00413f5f  e8e3d1ffff             call     0x411147 ; AffCorpsEngin
00413f64  8b442434               mov      eax, dword ptr [esp + 0x34]
00413f68  83ef29                 sub      edi, 0x29
00413f6b  83e820                 sub      eax, 0x20
00413f6e  e93bfaffff             jmp      0x4139ae ;
00413f73  31d2                   xor      edx, edx
00413f75  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413f7b  4a                     dec      edx
00413f7c  89d0                   mov      eax, edx
00413f7e  c1fa1f                 sar      edx, 0x1f
00413f81  2bc2                   sub      eax, edx
00413f83  d1f8                   sar      eax, 1
00413f85  31db                   xor      ebx, ebx
00413f87  8a9ea6000000           mov      bl, byte ptr [esi + 0xa6]
00413f8d  0fafc3                 imul     eax, ebx
00413f90  31d2                   xor      edx, edx
00413f92  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00413f98  01d0                   add      eax, edx
00413f9a  31db                   xor      ebx, ebx
00413f9c  0522130000             add      eax, 0x1322
00413fa1  6689c3                 mov      bx, ax
00413fa4  8b442408               mov      eax, dword ptr [esp + 8]
00413fa8  01f8                   add      eax, edi
00413faa  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00413fae  0fbfd0                 movsx    edx, ax
00413fb1  8b442434               mov      eax, dword ptr [esp + 0x34]
00413fb5  01c8                   add      eax, ecx
00413fb7  b901000000             mov      ecx, 1
00413fbc  98                     cwde
00413fbd  e8d4770400             call     0x45b796 ; PasteOmbreCmp
00413fc2  31d2                   xor      edx, edx
00413fc4  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413fca  4a                     dec      edx
00413fcb  89d0                   mov      eax, edx
00413fcd  c1fa1f                 sar      edx, 0x1f
00413fd0  2bc2                   sub      eax, edx
00413fd2  d1f8                   sar      eax, 1
00413fd4  31d2                   xor      edx, edx
00413fd6  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00413fdc  0fafd0                 imul     edx, eax
00413fdf  31c0                   xor      eax, eax
00413fe1  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413fe7  01d0                   add      eax, edx
00413fe9  31db                   xor      ebx, ebx
00413feb  05f2120000             add      eax, 0x12f2
00413ff0  e986f9ffff             jmp      0x41397b ;
00413ff5  31db                   xor      ebx, ebx
00413ff7  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00413ffd  89da                   mov      edx, ebx
00413fff  89d8                   mov      eax, ebx
00414001  c1fa1f                 sar      edx, 0x1f
00414004  2bc2                   sub      eax, edx
00414006  d1f8                   sar      eax, 1
00414008  31c9                   xor      ecx, ecx
0041400a  8a8ea5000000           mov      cl, byte ptr [esi + 0xa5]
00414010  0fafc8                 imul     ecx, eax
00414013  8d53ff                 lea      edx, [ebx - 1]
00414016  89d0                   mov      eax, edx
00414018  c1fa1f                 sar      edx, 0x1f
0041401b  2bc2                   sub      eax, edx
0041401d  d1f8                   sar      eax, 1
0041401f  bd02000000             mov      ebp, 2
00414024  89da                   mov      edx, ebx
00414026  01c1                   add      ecx, eax
00414028  89d8                   mov      eax, ebx
0041402a  c1fa1f                 sar      edx, 0x1f
0041402d  f7fd                   idiv     ebp
0041402f  31c0                   xor      eax, eax
00414031  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00414037  0fafc2                 imul     eax, edx
0041403a  01c8                   add      eax, ecx
0041403c  31db                   xor      ebx, ebx
0041403e  05b2110000             add      eax, 0x11b2
00414043  6689c3                 mov      bx, ax
00414046  8b442408               mov      eax, dword ptr [esp + 8]
0041404a  01f8                   add      eax, edi
0041404c  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00414050  0fbfd0                 movsx    edx, ax
00414053  8b442434               mov      eax, dword ptr [esp + 0x34]
00414057  01c8                   add      eax, ecx
00414059  b901000000             mov      ecx, 1
0041405e  98                     cwde
0041405f  e832770400             call     0x45b796 ; PasteOmbreCmp
00414064  31db                   xor      ebx, ebx
00414066  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
0041406c  89da                   mov      edx, ebx
0041406e  89d8                   mov      eax, ebx
00414070  c1fa1f                 sar      edx, 0x1f
00414073  f7fd                   idiv     ebp
00414075  0fb6aea5000000         movzx    ebp, byte ptr [esi + 0xa5]
0041407c  0fafe8                 imul     ebp, eax
0041407f  8d53ff                 lea      edx, [ebx - 1]
00414082  89d0                   mov      eax, edx
00414084  c1fa1f                 sar      edx, 0x1f
00414087  2bc2                   sub      eax, edx
00414089  d1f8                   sar      eax, 1
0041408b  89da                   mov      edx, ebx
0041408d  01c5                   add      ebp, eax
0041408f  b802000000             mov      eax, 2
00414094  c1fa1f                 sar      edx, 0x1f
00414097  890424                 mov      dword ptr [esp], eax
0041409a  89d8                   mov      eax, ebx
0041409c  f73c24                 idiv     dword ptr [esp]
0041409f  31c0                   xor      eax, eax
004140a1  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
004140a7  0fafc2                 imul     eax, edx
004140aa  01e8                   add      eax, ebp
004140ac  31db                   xor      ebx, ebx
004140ae  0552110000             add      eax, 0x1152
004140b3  e9c3f8ffff             jmp      0x41397b ;
004140b8  8b442434               mov      eax, dword ptr [esp + 0x34]
004140bc  83ef09                 sub      edi, 9
004140bf  e9a7feffff             jmp      0x413f6b ;
004140c4  31d2                   xor      edx, edx
004140c6  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004140cc  4a                     dec      edx
004140cd  89d0                   mov      eax, edx
004140cf  c1fa1f                 sar      edx, 0x1f
004140d2  2bc2                   sub      eax, edx
004140d4  d1f8                   sar      eax, 1
004140d6  31d2                   xor      edx, edx
004140d8  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
004140de  0fafc2                 imul     eax, edx
004140e1  31d2                   xor      edx, edx
004140e3  0575160000             add      eax, 0x1675
004140e8  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004140ee  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
004140f2  01c2                   add      edx, eax
004140f4  8b442408               mov      eax, dword ptr [esp + 8]
004140f8  31db                   xor      ebx, ebx
004140fa  01f8                   add      eax, edi
004140fc  6689d3                 mov      bx, dx
004140ff  0fbfd0                 movsx    edx, ax
00414102  8b442434               mov      eax, dword ptr [esp + 0x34]
00414106  01c8                   add      eax, ecx
00414108  b901000000             mov      ecx, 1
0041410d  98                     cwde
0041410e  e883760400             call     0x45b796 ; PasteOmbreCmp
00414113  31d2                   xor      edx, edx
00414115  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041411b  4a                     dec      edx
0041411c  89d0                   mov      eax, edx
0041411e  c1fa1f                 sar      edx, 0x1f
00414121  2bc2                   sub      eax, edx
00414123  d1f8                   sar      eax, 1
00414125  31d2                   xor      edx, edx
00414127  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
0041412d  0fafc2                 imul     eax, edx
00414130  31d2                   xor      edx, edx
00414132  05b5150000             add      eax, 0x15b5
00414137  e935f8ffff             jmp      0x413971 ;
0041413c  31d2                   xor      edx, edx
0041413e  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414144  4a                     dec      edx
00414145  89d0                   mov      eax, edx
00414147  c1fa1f                 sar      edx, 0x1f
0041414a  2bc2                   sub      eax, edx
0041414c  d1f8                   sar      eax, 1
0041414e  31d2                   xor      edx, edx
00414150  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00414156  0fafc2                 imul     eax, edx
00414159  31d2                   xor      edx, edx
0041415b  05f5140000             add      eax, 0x14f5
00414160  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00414166  31db                   xor      ebx, ebx
00414168  01d0                   add      eax, edx
0041416a  6689c3                 mov      bx, ax
0041416d  8b442408               mov      eax, dword ptr [esp + 8]
00414171  01f8                   add      eax, edi
00414173  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00414177  0fbfd0                 movsx    edx, ax
0041417a  8b442434               mov      eax, dword ptr [esp + 0x34]
0041417e  01c8                   add      eax, ecx
00414180  b901000000             mov      ecx, 1
00414185  98                     cwde
00414186  e80b760400             call     0x45b796 ; PasteOmbreCmp
0041418b  31d2                   xor      edx, edx
0041418d  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414193  4a                     dec      edx
00414194  89d0                   mov      eax, edx
00414196  c1fa1f                 sar      edx, 0x1f
00414199  2bc2                   sub      eax, edx
0041419b  d1f8                   sar      eax, 1
0041419d  31d2                   xor      edx, edx
0041419f  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
004141a5  0fafc2                 imul     eax, edx
004141a8  31d2                   xor      edx, edx
004141aa  0535140000             add      eax, 0x1435
004141af  e9bdf7ffff             jmp      0x413971 ;
004141b4  31d2                   xor      edx, edx
004141b6  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004141bc  4a                     dec      edx
004141bd  89d0                   mov      eax, edx
004141bf  c1fa1f                 sar      edx, 0x1f
004141c2  2bc2                   sub      eax, edx
004141c4  d1f8                   sar      eax, 1
004141c6  31d2                   xor      edx, edx
004141c8  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
004141ce  0fafc2                 imul     eax, edx
004141d1  31d2                   xor      edx, edx
004141d3  0575190000             add      eax, 0x1975
004141d8  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004141de  31db                   xor      ebx, ebx
004141e0  01d0                   add      eax, edx
004141e2  6689c3                 mov      bx, ax
004141e5  8b442408               mov      eax, dword ptr [esp + 8]
004141e9  01f8                   add      eax, edi
004141eb  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
004141ef  0fbfd0                 movsx    edx, ax
004141f2  8b442434               mov      eax, dword ptr [esp + 0x34]
004141f6  01c8                   add      eax, ecx
004141f8  b901000000             mov      ecx, 1
004141fd  98                     cwde
004141fe  e893750400             call     0x45b796 ; PasteOmbreCmp
00414203  31d2                   xor      edx, edx
00414205  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041420b  4a                     dec      edx
0041420c  89d0                   mov      eax, edx
0041420e  c1fa1f                 sar      edx, 0x1f
00414211  2bc2                   sub      eax, edx
00414213  d1f8                   sar      eax, 1
00414215  31d2                   xor      edx, edx
00414217  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
0041421d  0fafc2                 imul     eax, edx
00414220  31d2                   xor      edx, edx
00414222  05b5180000             add      eax, 0x18b5
00414227  e945f7ffff             jmp      0x413971 ;
0041422c  31d2                   xor      edx, edx
0041422e  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414234  4a                     dec      edx
00414235  89d0                   mov      eax, edx
00414237  c1fa1f                 sar      edx, 0x1f
0041423a  2bc2                   sub      eax, edx
0041423c  d1f8                   sar      eax, 1
0041423e  31d2                   xor      edx, edx
00414240  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00414246  0fafc2                 imul     eax, edx
00414249  31d2                   xor      edx, edx
0041424b  05f51a0000             add      eax, 0x1af5
00414250  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00414256  31db                   xor      ebx, ebx
00414258  01d0                   add      eax, edx
0041425a  6689c3                 mov      bx, ax
0041425d  8b442408               mov      eax, dword ptr [esp + 8]
00414261  01f8                   add      eax, edi
00414263  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
00414267  0fbfd0                 movsx    edx, ax
0041426a  8b442434               mov      eax, dword ptr [esp + 0x34]
0041426e  01c8                   add      eax, ecx
00414270  b901000000             mov      ecx, 1
00414275  98                     cwde
00414276  e81b750400             call     0x45b796 ; PasteOmbreCmp
0041427b  31d2                   xor      edx, edx
0041427d  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414283  4a                     dec      edx
00414284  89d0                   mov      eax, edx
00414286  c1fa1f                 sar      edx, 0x1f
00414289  2bc2                   sub      eax, edx
0041428b  d1f8                   sar      eax, 1
0041428d  31d2                   xor      edx, edx
0041428f  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
00414295  0fafc2                 imul     eax, edx
00414298  31d2                   xor      edx, edx
0041429a  05351a0000             add      eax, 0x1a35
0041429f  e9cdf6ffff             jmp      0x413971 ;
004142a4  31d2                   xor      edx, edx
004142a6  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004142ac  42                     inc      edx
004142ad  89d0                   mov      eax, edx
004142af  c1fa1f                 sar      edx, 0x1f
004142b2  2bc2                   sub      eax, edx
004142b4  d1f8                   sar      eax, 1
004142b6  31d2                   xor      edx, edx
004142b8  48                     dec      eax
004142b9  8a96a6000000           mov      dl, byte ptr [esi + 0xa6]
004142bf  0fafd0                 imul     edx, eax
004142c2  31c0                   xor      eax, eax
004142c4  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
004142ca  01d0                   add      eax, edx
004142cc  31db                   xor      ebx, ebx
004142ce  8944241c               mov      dword ptr [esp + 0x1c], eax
004142d2  05f5170000             add      eax, 0x17f5
004142d7  6689c3                 mov      bx, ax
004142da  8b442408               mov      eax, dword ptr [esp + 8]
004142de  01f8                   add      eax, edi
004142e0  8b4c240c               mov      ecx, dword ptr [esp + 0xc]
004142e4  0fbfd0                 movsx    edx, ax
004142e7  8b442434               mov      eax, dword ptr [esp + 0x34]
004142eb  01c8                   add      eax, ecx
004142ed  b901000000             mov      ecx, 1
004142f2  98                     cwde
004142f3  e89e740400             call     0x45b796 ; PasteOmbreCmp
004142f8  8b44241c               mov      eax, dword ptr [esp + 0x1c]
004142fc  31db                   xor      ebx, ebx
004142fe  0535170000             add      eax, 0x1735
00414303  e973f6ffff             jmp      0x41397b ;
00414308  8a4601                 mov      al, byte ptr [esi + 1]
0041430b  3c19                   cmp      al, 0x19
0041430d  0f87a5f6ffff           ja       0x4139b8
00414313  25ff000000             and      eax, 0xff
00414318  2eff2485e4364100       jmp      dword ptr cs:[eax*4 + 0x4136e4]
00414320  31d2                   xor      edx, edx
00414322  6689fa                 mov      dx, di
00414325  89d0                   mov      eax, edx
00414327  c1e004                 shl      eax, 4
0041432a  01d0                   add      eax, edx
0041432c  c1e002                 shl      eax, 2
0041432f  01d0                   add      eax, edx
00414331  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00414337  c1e002                 shl      eax, 2
0041433a  01d0                   add      eax, edx
0041433c  668b5004               mov      dx, word ptr [eax + 4]
00414340  663b5076               cmp      dx, word ptr [eax + 0x76]
00414344  7512                   jne      0x414358
00414346  668b4074               mov      ax, word ptr [eax + 0x74]
0041434a  25ffff0000             and      eax, 0xffff
0041434f  83f864                 cmp      eax, 0x64
00414352  7d04                   jge      0x414358
00414354  b001                   mov      al, 1
00414356  eb02                   jmp      0x41435a ;
00414358  30c0                   xor      al, al
0041435a  84c0                   test     al, al
0041435c  0f84a7000000           je       0x414409
00414362  31d2                   xor      edx, edx
00414364  668b5674               mov      dx, word ptr [esi + 0x74]
00414368  bb05000000             mov      ebx, 5
0041436d  89d0                   mov      eax, edx
0041436f  c1fa1f                 sar      edx, 0x1f
00414372  f7fb                   idiv     ebx
00414374  89c2                   mov      edx, eax
00414376  bb02000000             mov      ebx, 2
0041437b  c1fa1f                 sar      edx, 0x1f
0041437e  f7fb                   idiv     ebx
00414380  85d2                   test     edx, edx
00414382  0f8581000000           jne      0x414409
00414388  668b54242c             mov      dx, word ptr [esp + 0x2c]
0041438d  89d0                   mov      eax, edx
0041438f  c1e004                 shl      eax, 4
00414392  01d0                   add      eax, edx
00414394  c1e002                 shl      eax, 2
00414397  01d0                   add      eax, edx
00414399  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
0041439f  c1e002                 shl      eax, 2
004143a2  01c2                   add      edx, eax
004143a4  31c0                   xor      eax, eax
004143a6  8a4201                 mov      al, byte ptr [edx + 1]
004143a9  e886e80200             call     0x442c34 ; TypeEnginSeFatigue
004143ae  84c0                   test     al, al
004143b0  7457                   je       0x414409
004143b2  8b442428               mov      eax, dword ptr [esp + 0x28]
004143b6  8b4c2424               mov      ecx, dword ptr [esp + 0x24]
004143ba  31db                   xor      ebx, ebx
004143bc  83e808                 sub      eax, 8
004143bf  8a1a                   mov      bl, byte ptr [edx]
004143c1  83e902                 sub      ecx, 2
004143c4  81fbc8000000           cmp      ebx, 0xc8
004143ca  751f                   jne      0x4143eb
004143cc  668b5204               mov      dx, word ptr [edx + 4]
004143d0  31db                   xor      ebx, ebx
004143d2  81c22b1e0000           add      edx, 0x1e2b
004143d8  98                     cwde
004143d9  6689d3                 mov      bx, dx
004143dc  0fbfd1                 movsx    edx, cx
004143df  b901000000             mov      ecx, 1
004143e4  e85e6e0400             call     0x45b247 ; PasteBobCmp
004143e9  eb1e                   jmp      0x414409 ;
004143eb  668b5204               mov      dx, word ptr [edx + 4]
004143ef  53                     push     ebx
004143f0  81c22b1e0000           add      edx, 0x1e2b
004143f6  31db                   xor      ebx, ebx
004143f8  98                     cwde
004143f9  6689d3                 mov      bx, dx
004143fc  0fbfd1                 movsx    edx, cx
004143ff  b901000000             mov      ecx, 1
00414404  e84c800400             call     0x45c455 ; PastePlayerCmp
00414409  80beba00000000         cmp      byte ptr [esi + 0xba], 0
00414410  0f8477000000           je       0x41448d
00414416  bb05000000             mov      ebx, 5
0041441b  a17c8f5000             mov      eax, dword ptr [0x508f7c]
00414420  31d2                   xor      edx, edx
00414422  f7f3                   div      ebx
00414424  85d2                   test     edx, edx
00414426  7565                   jne      0x41448d
00414428  668b54242c             mov      dx, word ptr [esp + 0x2c]
0041442d  89d0                   mov      eax, edx
0041442f  c1e004                 shl      eax, 4
00414432  01d0                   add      eax, edx
00414434  c1e002                 shl      eax, 2
00414437  01d0                   add      eax, edx
00414439  8b1da0194e00           mov      ebx, dword ptr [0x4e19a0]
0041443f  c1e002                 shl      eax, 2
00414442  01c3                   add      ebx, eax
00414444  89d0                   mov      eax, edx
00414446  30f6                   xor      dh, dh
00414448  e859b50300             call     0x44f9a6 ; EnginGetLevelExperience
0041444d  88c2                   mov      dl, al
0041444f  31c0                   xor      eax, eax
00414451  8a4301                 mov      al, byte ptr [ebx + 1]
00414454  e857de0200             call     0x4422b0 ; TypeEnginGagneXP
00414459  84c0                   test     al, al
0041445b  7430                   je       0x41448d
0041445d  31c0                   xor      eax, eax
0041445f  6689d0                 mov      ax, dx
00414462  85c0                   test     eax, eax
00414464  7427                   je       0x41448d
00414466  8b442424               mov      eax, dword ptr [esp + 0x24]
0041446a  81c2461e0000           add      edx, 0x1e46
00414470  31db                   xor      ebx, ebx
00414472  83e802                 sub      eax, 2
00414475  6689d3                 mov      bx, dx
00414478  0fbfd0                 movsx    edx, ax
0041447b  8b442428               mov      eax, dword ptr [esp + 0x28]
0041447f  83e808                 sub      eax, 8
00414482  b901000000             mov      ecx, 1
00414487  98                     cwde
00414488  e8ba6d0400             call     0x45b247 ; PasteBobCmp
0041448d  83c43c                 add      esp, 0x3c
00414490  5d                     pop      ebp
00414491  5f                     pop      edi
00414492  5e                     pop      esi
00414493  59                     pop      ecx
00414494  c3                     ret
