; AffConstruireBatiment [0x414495, 0x414a8a)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00414495  51                     push     ecx
00414496  56                     push     esi
00414497  57                     push     edi
00414498  83ec2c                 sub      esp, 0x2c
0041449b  50                     push     eax
0041449c  89d7                   mov      edi, edx
0041449e  895c2420               mov      dword ptr [esp + 0x20], ebx
004144a2  31c9                   xor      ecx, ecx
004144a4  6689d9                 mov      cx, bx
004144a7  89c8                   mov      eax, ecx
004144a9  c1e004                 shl      eax, 4
004144ac  01c8                   add      eax, ecx
004144ae  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
004144b4  c1e002                 shl      eax, 2
004144b7  89ca                   mov      edx, ecx
004144b9  01c8                   add      eax, ecx
004144bb  31da                   xor      edx, ebx
004144bd  c1e002                 shl      eax, 2
004144c0  668954241c             mov      word ptr [esp + 0x1c], dx
004144c5  01c6                   add      esi, eax
004144c7  b401                   mov      ah, 1
004144c9  8b1424                 mov      edx, dword ptr [esp]
004144cc  8864242c               mov      byte ptr [esp + 0x2c], ah
004144d0  660fbe8686000000       movsx    ax, byte ptr [esi + 0x86]
004144d8  31db                   xor      ebx, ebx
004144da  01c2                   add      edx, eax
004144dc  66895c2418             mov      word ptr [esp + 0x18], bx
004144e1  6689542424             mov      word ptr [esp + 0x24], dx
004144e6  660fbe8687000000       movsx    ax, byte ptr [esi + 0x87]
004144ee  8d542404               lea      edx, [esp + 4]
004144f2  895c2404               mov      dword ptr [esp + 4], ebx
004144f6  895c2408               mov      dword ptr [esp + 8], ebx
004144fa  01c7                   add      edi, eax
004144fc  31c0                   xor      eax, eax
004144fe  8d5c2408               lea      ebx, [esp + 8]
00414502  8a4601                 mov      al, byte ptr [esi + 1]
00414505  e8c2caffff             call     0x410fcc ; AffCorpsEnginDecalage
0041450a  8a96bd000000           mov      dl, byte ptr [esi + 0xbd]
00414510  66897c2428             mov      word ptr [esp + 0x28], di
00414515  84d2                   test     dl, dl
00414517  0f8476030000           je       0x414893
0041451d  8b442428               mov      eax, dword ptr [esp + 0x28]
00414521  8d5c2414               lea      ebx, [esp + 0x14]
00414525  8d54240c               lea      edx, [esp + 0xc]
00414529  89442410               mov      dword ptr [esp + 0x10], eax
0041452d  89c8                   mov      eax, ecx
0041452f  e838cb0200             call     0x44106c ; EnginGetTaille
00414534  31c0                   xor      eax, eax
00414536  668b44240c             mov      ax, word ptr [esp + 0xc]
0041453b  8b7c2424               mov      edi, dword ptr [esp + 0x24]
0041453f  83f801                 cmp      eax, 1
00414542  751e                   jne      0x414562
00414544  39c0                   cmp      eax, eax
00414546  751a                   jne      0x414562
00414548  8b542426               mov      edx, dword ptr [esp + 0x26]
0041454c  8b442422               mov      eax, dword ptr [esp + 0x22]
00414550  b901000000             mov      ecx, 1
00414555  bb1e2a0000             mov      ebx, 0x2a1e
0041455a  c1fa10                 sar      edx, 0x10
0041455d  c1f810                 sar      eax, 0x10
00414560  eb1a                   jmp      0x41457c ; 
00414562  8b442410               mov      eax, dword ptr [esp + 0x10]
00414566  83e820                 sub      eax, 0x20
00414569  0fbfd0                 movsx    edx, ax
0041456c  89f8                   mov      eax, edi
0041456e  b901000000             mov      ecx, 1
00414573  83e820                 sub      eax, 0x20
00414576  bb1f2a0000             mov      ebx, 0x2a1f
0041457b  98                     cwde     
0041457c  e8c66c0400             call     0x45b247 ; PasteBobCmp
00414581  31c0                   xor      eax, eax
00414583  8a4601                 mov      al, byte ptr [esi + 1]
00414586  83f807                 cmp      eax, 7
00414589  0f8504030000           jne      0x414893
0041458f  31c0                   xor      eax, eax
00414591  8a86be000000           mov      al, byte ptr [esi + 0xbe]
00414597  83f809                 cmp      eax, 9
0041459a  0f85f3020000           jne      0x414893
004145a0  31c0                   xor      eax, eax
004145a2  668b86d8000000         mov      ax, word ptr [esi + 0xd8]
004145a9  85c0                   test     eax, eax
004145ab  0f84e2020000           je       0x414893
004145b1  31ff                   xor      edi, edi
004145b3  eb01                   jmp      0x4145b6 ; 
004145b5  47                     inc      edi
004145b6  663bbed8000000         cmp      di, word ptr [esi + 0xd8]
004145bd  0f83d0020000           jae      0x414893
004145c3  31db                   xor      ebx, ebx
004145c5  6689fb                 mov      bx, di
004145c8  668b9c5ec4000000       mov      bx, word ptr [esi + ebx*2 + 0xc4]
004145d0  81e3ffff0000           and      ebx, 0xffff
004145d6  b900010000             mov      ecx, 0x100
004145db  89da                   mov      edx, ebx
004145dd  89d8                   mov      eax, ebx
004145df  c1fa1f                 sar      edx, 0x1f
004145e2  f7f9                   idiv     ecx
004145e4  89d1                   mov      ecx, edx
004145e6  89da                   mov      edx, ebx
004145e8  89d8                   mov      eax, ebx
004145ea  c1fa1f                 sar      edx, 0x1f
004145ed  c1e208                 shl      edx, 8
004145f0  1bc2                   sbb      eax, edx
004145f2  c1f808                 sar      eax, 8
004145f5  89c3                   mov      ebx, eax
004145f7  66a120875000           mov      ax, word ptr [0x508720]
004145fd  6639c1                 cmp      cx, ax
00414600  72b3                   jb       0x4145b5
00414602  31d2                   xor      edx, edx
00414604  6689c2                 mov      dx, ax
00414607  31c0                   xor      eax, eax
00414609  66a124875000           mov      ax, word ptr [0x508724]
0041460f  01d0                   add      eax, edx
00414611  31d2                   xor      edx, edx
00414613  6689ca                 mov      dx, cx
00414616  39c2                   cmp      edx, eax
00414618  7d9b                   jge      0x4145b5
0041461a  663b1d22875000         cmp      bx, word ptr [0x508722]
00414621  7292                   jb       0x4145b5
00414623  31d2                   xor      edx, edx
00414625  31c0                   xor      eax, eax
00414627  668b1522875000         mov      dx, word ptr [0x508722]
0041462e  66a126875000           mov      ax, word ptr [0x508726]
00414634  01d0                   add      eax, edx
00414636  31d2                   xor      edx, edx
00414638  6689da                 mov      dx, bx
0041463b  39c2                   cmp      edx, eax
0041463d  0f8d72ffffff           jge      0x4145b5
00414643  662b1d22875000         sub      bx, word ptr [0x508722]
0041464a  c1e305                 shl      ebx, 5
0041464d  0fbfd3                 movsx    edx, bx
00414650  662b0d20875000         sub      cx, word ptr [0x508720]
00414657  c1e105                 shl      ecx, 5
0041465a  bbcf1c0000             mov      ebx, 0x1ccf
0041465f  0fbfc1                 movsx    eax, cx
00414662  b901000000             mov      ecx, 1
00414667  e8db6b0400             call     0x45b247 ; PasteBobCmp
0041466c  e944ffffff             jmp      0x4145b5 ; 
00414671  e8432a0300             call     0x4470b9 ; BagVide
00414676  84c0                   test     al, al
00414678  746b                   je       0x4146e5
0041467a  b901000000             mov      ecx, 1
0041467f  0fbfc3                 movsx    eax, bx
00414682  0fbffa                 movsx    edi, dx
00414685  bb202a0000             mov      ebx, 0x2a20
0041468a  89c2                   mov      edx, eax
0041468c  89f8                   mov      eax, edi
0041468e  e803710400             call     0x45b796 ; PasteOmbreCmp
00414693  31d2                   xor      edx, edx
00414695  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041469b  42                     inc      edx
0041469c  89d0                   mov      eax, edx
0041469e  c1fa1f                 sar      edx, 0x1f
004146a1  2bc2                   sub      eax, edx
004146a3  d1f8                   sar      eax, 1
004146a5  c1e003                 shl      eax, 3
004146a8  31d2                   xor      edx, edx
004146aa  053a050000             add      eax, 0x53a
004146af  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004146b5  31db                   xor      ebx, ebx
004146b7  01d0                   add      eax, edx
004146b9  8b542408               mov      edx, dword ptr [esp + 8]
004146bd  6689c3                 mov      bx, ax
004146c0  8b442428               mov      eax, dword ptr [esp + 0x28]
004146c4  01d0                   add      eax, edx
004146c6  8b7c2404               mov      edi, dword ptr [esp + 4]
004146ca  0fbfd0                 movsx    edx, ax
004146cd  8b442424               mov      eax, dword ptr [esp + 0x24]
004146d1  31c9                   xor      ecx, ecx
004146d3  01f8                   add      eax, edi
004146d5  668b4c2420             mov      cx, word ptr [esp + 0x20]
004146da  98                     cwde     
004146db  e867caffff             call     0x411147 ; AffCorpsEngin
004146e0  e999000000             jmp      0x41477e ; 
004146e5  b901000000             mov      ecx, 1
004146ea  0fbfc3                 movsx    eax, bx
004146ed  0fbffa                 movsx    edi, dx
004146f0  bb202a0000             mov      ebx, 0x2a20
004146f5  89c2                   mov      edx, eax
004146f7  89f8                   mov      eax, edi
004146f9  e898700400             call     0x45b796 ; PasteOmbreCmp
004146fe  31d2                   xor      edx, edx
00414700  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414706  42                     inc      edx
00414707  89d0                   mov      eax, edx
00414709  c1fa1f                 sar      edx, 0x1f
0041470c  2bc2                   sub      eax, edx
0041470e  d1f8                   sar      eax, 1
00414710  c1e003                 shl      eax, 3
00414713  31d2                   xor      edx, edx
00414715  05ba050000             add      eax, 0x5ba
0041471a  eb93                   jmp      0x4146af ; 
0041471c  b901000000             mov      ecx, 1
00414721  0fbffb                 movsx    edi, bx
00414724  0fbfc2                 movsx    eax, dx
00414727  bb202a0000             mov      ebx, 0x2a20
0041472c  89fa                   mov      edx, edi
0041472e  e863700400             call     0x45b796 ; PasteOmbreCmp
00414733  31d2                   xor      edx, edx
00414735  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041473b  42                     inc      edx
0041473c  89d0                   mov      eax, edx
0041473e  c1fa1f                 sar      edx, 0x1f
00414741  2bc2                   sub      eax, edx
00414743  d1f8                   sar      eax, 1
00414745  c1e003                 shl      eax, 3
00414748  31d2                   xor      edx, edx
0041474a  057a050000             add      eax, 0x57a
0041474f  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00414755  31db                   xor      ebx, ebx
00414757  01d0                   add      eax, edx
00414759  8b7c2408               mov      edi, dword ptr [esp + 8]
0041475d  6689c3                 mov      bx, ax
00414760  8b442428               mov      eax, dword ptr [esp + 0x28]
00414764  01f8                   add      eax, edi
00414766  e95bffffff             jmp      0x4146c6 ; 
0041476b  8a8e89000000           mov      cl, byte ptr [esi + 0x89]
00414771  84c9                   test     cl, cl
00414773  0f86f8feffff           jbe      0x414671
00414779  80f901                 cmp      cl, 1
0041477c  749e                   je       0x41471c
0041477e  8b442424               mov      eax, dword ptr [esp + 0x24]
00414782  668944241c             mov      word ptr [esp + 0x1c], ax
00414787  8b442428               mov      eax, dword ptr [esp + 0x28]
0041478b  83e809                 sub      eax, 9
0041478e  6689442418             mov      word ptr [esp + 0x18], ax
00414793  e922010000             jmp      0x4148ba ; 
00414798  e81c290300             call     0x4470b9 ; BagVide
0041479d  84c0                   test     al, al
0041479f  7469                   je       0x41480a
004147a1  b901000000             mov      ecx, 1
004147a6  0fbffb                 movsx    edi, bx
004147a9  0fbfc2                 movsx    eax, dx
004147ac  bb202a0000             mov      ebx, 0x2a20
004147b1  89fa                   mov      edx, edi
004147b3  e8de6f0400             call     0x45b796 ; PasteOmbreCmp
004147b8  31d2                   xor      edx, edx
004147ba  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004147c0  42                     inc      edx
004147c1  89d0                   mov      eax, edx
004147c3  c1fa1f                 sar      edx, 0x1f
004147c6  2bc2                   sub      eax, edx
004147c8  d1f8                   sar      eax, 1
004147ca  c1e003                 shl      eax, 3
004147cd  31d2                   xor      edx, edx
004147cf  059a0b0000             add      eax, 0xb9a
004147d4  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004147da  31db                   xor      ebx, ebx
004147dc  01d0                   add      eax, edx
004147de  8b542408               mov      edx, dword ptr [esp + 8]
004147e2  6689c3                 mov      bx, ax
004147e5  8b442428               mov      eax, dword ptr [esp + 0x28]
004147e9  01d0                   add      eax, edx
004147eb  8b7c2404               mov      edi, dword ptr [esp + 4]
004147ef  0fbfd0                 movsx    edx, ax
004147f2  8b442424               mov      eax, dword ptr [esp + 0x24]
004147f6  31c9                   xor      ecx, ecx
004147f8  01f8                   add      eax, edi
004147fa  668b4c2420             mov      cx, word ptr [esp + 0x20]
004147ff  98                     cwde     
00414800  e842c9ffff             call     0x411147 ; AffCorpsEngin
00414805  e974ffffff             jmp      0x41477e ; 
0041480a  b901000000             mov      ecx, 1
0041480f  0fbfc3                 movsx    eax, bx
00414812  0fbffa                 movsx    edi, dx
00414815  bb202a0000             mov      ebx, 0x2a20
0041481a  89c2                   mov      edx, eax
0041481c  89f8                   mov      eax, edi
0041481e  e8736f0400             call     0x45b796 ; PasteOmbreCmp
00414823  31d2                   xor      edx, edx
00414825  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041482b  42                     inc      edx
0041482c  89d0                   mov      eax, edx
0041482e  c1fa1f                 sar      edx, 0x1f
00414831  2bc2                   sub      eax, edx
00414833  d1f8                   sar      eax, 1
00414835  c1e003                 shl      eax, 3
00414838  31d2                   xor      edx, edx
0041483a  05da0b0000             add      eax, 0xbda
0041483f  eb93                   jmp      0x4147d4 ; 
00414841  b901000000             mov      ecx, 1
00414846  0fbfc3                 movsx    eax, bx
00414849  0fbffa                 movsx    edi, dx
0041484c  bb202a0000             mov      ebx, 0x2a20
00414851  89c2                   mov      edx, eax
00414853  89f8                   mov      eax, edi
00414855  e83c6f0400             call     0x45b796 ; PasteOmbreCmp
0041485a  31d2                   xor      edx, edx
0041485c  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00414862  42                     inc      edx
00414863  89d0                   mov      eax, edx
00414865  c1fa1f                 sar      edx, 0x1f
00414868  2bc2                   sub      eax, edx
0041486a  d1f8                   sar      eax, 1
0041486c  c1e002                 shl      eax, 2
0041486f  31d2                   xor      edx, edx
00414871  055e0c0000             add      eax, 0xc5e
00414876  e959ffffff             jmp      0x4147d4 ; 
0041487b  8a8e89000000           mov      cl, byte ptr [esi + 0x89]
00414881  84c9                   test     cl, cl
00414883  0f860fffffff           jbe      0x414798
00414889  80f901                 cmp      cl, 1
0041488c  74b3                   je       0x414841
0041488e  e9ebfeffff             jmp      0x41477e ; 
00414893  8a4e01                 mov      cl, byte ptr [esi + 1]
00414896  80f906                 cmp      cl, 6
00414899  721f                   jb       0x4148ba
0041489b  8b542424               mov      edx, dword ptr [esp + 0x24]
0041489f  8b5c2428               mov      ebx, dword ptr [esp + 0x28]
004148a3  8d460a                 lea      eax, [esi + 0xa]
004148a6  83c202                 add      edx, 2
004148a9  83c31a                 add      ebx, 0x1a
004148ac  80f906                 cmp      cl, 6
004148af  76ca                   jbe      0x41487b
004148b1  80f907                 cmp      cl, 7
004148b4  0f84b1feffff           je       0x41476b
004148ba  807c242c00             cmp      byte ptr [esp + 0x2c], 0
004148bf  0f84be010000           je       0x414a83
004148c5  8a1d41805000           mov      bl, byte ptr [0x508041]
004148cb  3a1e                   cmp      bl, byte ptr [esi]
004148cd  7509                   jne      0x4148d8
004148cf  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
004148d6  7516                   jne      0x4148ee
004148d8  8b542420               mov      edx, dword ptr [esp + 0x20]
004148dc  663b15c26a4900         cmp      dx, word ptr [0x496ac2]
004148e3  7409                   je       0x4148ee
004148e5  803d8f8f500000         cmp      byte ptr [0x508f8f], 0
004148ec  741f                   je       0x41490d
004148ee  8b542416               mov      edx, dword ptr [esp + 0x16]
004148f2  31db                   xor      ebx, ebx
004148f4  8b44241a               mov      eax, dword ptr [esp + 0x1a]
004148f8  668b5c2420             mov      bx, word ptr [esp + 0x20]
004148fd  c1fa10                 sar      edx, 0x10
00414900  c1f810                 sar      eax, 0x10
00414903  e8dcc2ffff             call     0x410be4 ; AffInfoSelection
00414908  e976010000             jmp      0x414a83 ; 
0041490d  31d2                   xor      edx, edx
0041490f  668b542420             mov      dx, word ptr [esp + 0x20]
00414914  89d0                   mov      eax, edx
00414916  c1e004                 shl      eax, 4
00414919  01d0                   add      eax, edx
0041491b  c1e002                 shl      eax, 2
0041491e  01c2                   add      edx, eax
00414920  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00414925  c1e202                 shl      edx, 2
00414928  01d0                   add      eax, edx
0041492a  668b5004               mov      dx, word ptr [eax + 4]
0041492e  663b5076               cmp      dx, word ptr [eax + 0x76]
00414932  7512                   jne      0x414946
00414934  668b4074               mov      ax, word ptr [eax + 0x74]
00414938  25ffff0000             and      eax, 0xffff
0041493d  83f864                 cmp      eax, 0x64
00414940  7d04                   jge      0x414946
00414942  b001                   mov      al, 1
00414944  eb02                   jmp      0x414948 ; 
00414946  30c0                   xor      al, al
00414948  84c0                   test     al, al
0041494a  0f84ab000000           je       0x4149fb
00414950  31d2                   xor      edx, edx
00414952  668b5674               mov      dx, word ptr [esi + 0x74]
00414956  bb05000000             mov      ebx, 5
0041495b  89d0                   mov      eax, edx
0041495d  c1fa1f                 sar      edx, 0x1f
00414960  f7fb                   idiv     ebx
00414962  89c2                   mov      edx, eax
00414964  bb02000000             mov      ebx, 2
00414969  c1fa1f                 sar      edx, 0x1f
0041496c  f7fb                   idiv     ebx
0041496e  85d2                   test     edx, edx
00414970  0f8585000000           jne      0x4149fb
00414976  668b542420             mov      dx, word ptr [esp + 0x20]
0041497b  89d0                   mov      eax, edx
0041497d  c1e004                 shl      eax, 4
00414980  01d0                   add      eax, edx
00414982  c1e002                 shl      eax, 2
00414985  01d0                   add      eax, edx
00414987  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
0041498d  c1e002                 shl      eax, 2
00414990  01c2                   add      edx, eax
00414992  31c0                   xor      eax, eax
00414994  8a4201                 mov      al, byte ptr [edx + 1]
00414997  e898e20200             call     0x442c34 ; TypeEnginSeFatigue
0041499c  84c0                   test     al, al
0041499e  745b                   je       0x4149fb
004149a0  8b4c241c               mov      ecx, dword ptr [esp + 0x1c]
004149a4  8b442418               mov      eax, dword ptr [esp + 0x18]
004149a8  31db                   xor      ebx, ebx
004149aa  83e908                 sub      ecx, 8
004149ad  8a1a                   mov      bl, byte ptr [edx]
004149af  83e802                 sub      eax, 2
004149b2  81fbc8000000           cmp      ebx, 0xc8
004149b8  7521                   jne      0x4149db
004149ba  668b5204               mov      dx, word ptr [edx + 4]
004149be  31db                   xor      ebx, ebx
004149c0  81c22b1e0000           add      edx, 0x1e2b
004149c6  6689d3                 mov      bx, dx
004149c9  0fbfd0                 movsx    edx, ax
004149cc  0fbfc1                 movsx    eax, cx
004149cf  b901000000             mov      ecx, 1
004149d4  e86e680400             call     0x45b247 ; PasteBobCmp
004149d9  eb20                   jmp      0x4149fb ; 
004149db  668b5204               mov      dx, word ptr [edx + 4]
004149df  53                     push     ebx
004149e0  81c22b1e0000           add      edx, 0x1e2b
004149e6  31db                   xor      ebx, ebx
004149e8  6689d3                 mov      bx, dx
004149eb  0fbfd0                 movsx    edx, ax
004149ee  0fbfc1                 movsx    eax, cx
004149f1  b901000000             mov      ecx, 1
004149f6  e85a7a0400             call     0x45c455 ; PastePlayerCmp
004149fb  80beba00000000         cmp      byte ptr [esi + 0xba], 0
00414a02  0f847b000000           je       0x414a83
00414a08  bb05000000             mov      ebx, 5
00414a0d  a17c8f5000             mov      eax, dword ptr [0x508f7c]
00414a12  31d2                   xor      edx, edx
00414a14  f7f3                   div      ebx
00414a16  85d2                   test     edx, edx
00414a18  7569                   jne      0x414a83
00414a1a  31db                   xor      ebx, ebx
00414a1c  668b5c2420             mov      bx, word ptr [esp + 0x20]
00414a21  89d8                   mov      eax, ebx
00414a23  c1e004                 shl      eax, 4
00414a26  01d8                   add      eax, ebx
00414a28  c1e002                 shl      eax, 2
00414a2b  01d8                   add      eax, ebx
00414a2d  8b0da0194e00           mov      ecx, dword ptr [0x4e19a0]
00414a33  c1e002                 shl      eax, 2
00414a36  89da                   mov      edx, ebx
00414a38  01c1                   add      ecx, eax
00414a3a  89d8                   mov      eax, ebx
00414a3c  30fe                   xor      dh, bh
00414a3e  e863af0300             call     0x44f9a6 ; EnginGetLevelExperience
00414a43  88c2                   mov      dl, al
00414a45  31c0                   xor      eax, eax
00414a47  8a4101                 mov      al, byte ptr [ecx + 1]
00414a4a  e861d80200             call     0x4422b0 ; TypeEnginGagneXP
00414a4f  84c0                   test     al, al
00414a51  7430                   je       0x414a83
00414a53  31c0                   xor      eax, eax
00414a55  6689d0                 mov      ax, dx
00414a58  85c0                   test     eax, eax
00414a5a  7427                   je       0x414a83
00414a5c  8b442418               mov      eax, dword ptr [esp + 0x18]
00414a60  81c2461e0000           add      edx, 0x1e46
00414a66  31db                   xor      ebx, ebx
00414a68  83e802                 sub      eax, 2
00414a6b  6689d3                 mov      bx, dx
00414a6e  0fbfd0                 movsx    edx, ax
00414a71  8b44241c               mov      eax, dword ptr [esp + 0x1c]
00414a75  83e808                 sub      eax, 8
00414a78  b901000000             mov      ecx, 1
00414a7d  98                     cwde     
00414a7e  e8c4670400             call     0x45b247 ; PasteBobCmp
00414a83  83c430                 add      esp, 0x30
00414a86  5f                     pop      edi
00414a87  5e                     pop      esi
00414a88  59                     pop      ecx
00414a89  c3                     ret      
