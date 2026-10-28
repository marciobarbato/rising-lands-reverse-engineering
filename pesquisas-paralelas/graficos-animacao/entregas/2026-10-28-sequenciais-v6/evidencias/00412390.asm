; AffDeplaceEngin [0x412390, 0x41374c)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00412390  51                     push     ecx
00412391  56                     push     esi
00412392  57                     push     edi
00412393  55                     push     ebp
00412394  83ec38                 sub      esp, 0x38
00412397  89c1                   mov      ecx, eax
00412399  89d7                   mov      edi, edx
0041239b  895c240c               mov      dword ptr [esp + 0xc], ebx
0041239f  31d2                   xor      edx, edx
004123a1  6689da                 mov      dx, bx
004123a4  89d0                   mov      eax, edx
004123a6  c1e004                 shl      eax, 4
004123a9  01d0                   add      eax, edx
004123ab  c1e002                 shl      eax, 2
004123ae  8b35a0194e00           mov      esi, dword ptr [0x4e19a0]
004123b4  01d0                   add      eax, edx
004123b6  31da                   xor      edx, ebx
004123b8  c1e002                 shl      eax, 2
004123bb  668954241c             mov      word ptr [esp + 0x1c], dx
004123c0  01c6                   add      esi, eax
004123c2  31db                   xor      ebx, ebx
004123c4  8d542418               lea      edx, [esp + 0x18]
004123c8  660fbe8686000000       movsx    ax, byte ptr [esi + 0x86]
004123d0  66895c2420             mov      word ptr [esp + 0x20], bx
004123d5  01c1                   add      ecx, eax
004123d7  660fbe8687000000       movsx    ax, byte ptr [esi + 0x87]
004123df  895c2418               mov      dword ptr [esp + 0x18], ebx
004123e3  895c2408               mov      dword ptr [esp + 8], ebx
004123e7  01c7                   add      edi, eax
004123e9  31c0                   xor      eax, eax
004123eb  8d5c2408               lea      ebx, [esp + 8]
004123ef  8a4601                 mov      al, byte ptr [esi + 1]
004123f2  e8d5ebffff             call     0x410fcc ; AffCorpsEnginDecalage
004123f7  668b4608               mov      ax, word ptr [esi + 8]
004123fb  668b567e               mov      dx, word ptr [esi + 0x7e]
004123ff  66894c2428             mov      word ptr [esp + 0x28], cx
00412404  6639d0                 cmp      ax, dx
00412407  0f849c000000           je       0x4124a9
0041240d  80be9900000000         cmp      byte ptr [esi + 0x99], 0
00412414  0f848f000000           je       0x4124a9
0041241a  8b8683000000           mov      eax, dword ptr [esi + 0x83]
00412420  c1f818                 sar      eax, 0x18
00412423  85c0                   test     eax, eax
00412425  0f847e000000           je       0x4124a9
0041242b  8b8684000000           mov      eax, dword ptr [esi + 0x84]
00412431  c1f818                 sar      eax, 0x18
00412434  85c0                   test     eax, eax
00412436  7471                   je       0x4124a9
00412438  31c0                   xor      eax, eax
0041243a  8a8691000000           mov      al, byte ptr [esi + 0x91]
00412440  83f805                 cmp      eax, 5
00412443  7405                   je       0x41244a
00412445  83f80d                 cmp      eax, 0xd
00412448  7532                   jne      0x41247c
0041244a  a0181d4e00             mov      al, byte ptr [0x4e1d18]
0041244f  31d2                   xor      edx, edx
00412451  88c2                   mov      dl, al
00412453  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00412459  81e2ff000000           and      edx, 0xff
0041245f  fec0                   inc      al
00412461  31db                   xor      ebx, ebx
00412463  a2181d4e00             mov      byte ptr [0x4e1d18], al
00412468  89d0                   mov      eax, edx
0041246a  8a9e99000000           mov      bl, byte ptr [esi + 0x99]
00412470  c1fa1f                 sar      edx, 0x1f
00412473  f7fb                   idiv     ebx
00412475  6601542428             add      word ptr [esp + 0x28], dx
0041247a  eb2d                   jmp      0x4124a9 ;
0041247c  a0181d4e00             mov      al, byte ptr [0x4e1d18]
00412481  31d2                   xor      edx, edx
00412483  88c2                   mov      dl, al
00412485  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0041248b  81e2ff000000           and      edx, 0xff
00412491  fec0                   inc      al
00412493  31db                   xor      ebx, ebx
00412495  a2181d4e00             mov      byte ptr [0x4e1d18], al
0041249a  89d0                   mov      eax, edx
0041249c  8a9e99000000           mov      bl, byte ptr [esi + 0x99]
004124a2  c1fa1f                 sar      edx, 0x1f
004124a5  f7fb                   idiv     ebx
004124a7  01d7                   add      edi, edx
004124a9  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
004124b0  0f8469010000           je       0x41261f
004124b6  8a3541805000           mov      dh, byte ptr [0x508041]
004124bc  3a36                   cmp      dh, byte ptr [esi]
004124be  0f855b010000           jne      0x41261f
004124c4  8b442428               mov      eax, dword ptr [esp + 0x28]
004124c8  8d5c2410               lea      ebx, [esp + 0x10]
004124cc  89442430               mov      dword ptr [esp + 0x30], eax
004124d0  31c0                   xor      eax, eax
004124d2  8d54242c               lea      edx, [esp + 0x2c]
004124d6  668b44240c             mov      ax, word ptr [esp + 0xc]
004124db  e88ceb0200             call     0x44106c ; EnginGetTaille
004124e0  31c0                   xor      eax, eax
004124e2  668b44242c             mov      ax, word ptr [esp + 0x2c]
004124e7  89f9                   mov      ecx, edi
004124e9  83f801                 cmp      eax, 1
004124ec  751a                   jne      0x412508
004124ee  39c0                   cmp      eax, eax
004124f0  7516                   jne      0x412508
004124f2  8b442426               mov      eax, dword ptr [esp + 0x26]
004124f6  b901000000             mov      ecx, 1
004124fb  bb1e2a0000             mov      ebx, 0x2a1e
00412500  0fbfd7                 movsx    edx, di
00412503  c1f810                 sar      eax, 0x10
00412506  eb1a                   jmp      0x412522 ;
00412508  89c8                   mov      eax, ecx
0041250a  83e820                 sub      eax, 0x20
0041250d  0fbfd0                 movsx    edx, ax
00412510  8b442430               mov      eax, dword ptr [esp + 0x30]
00412514  bb1f2a0000             mov      ebx, 0x2a1f
00412519  83e820                 sub      eax, 0x20
0041251c  b901000000             mov      ecx, 1
00412521  98                     cwde
00412522  e8208d0400             call     0x45b247 ; PasteBobCmp
00412527  31c0                   xor      eax, eax
00412529  8a4601                 mov      al, byte ptr [esi + 1]
0041252c  83f80e                 cmp      eax, 0xe
0041252f  0f85dc000000           jne      0x412611
00412535  31c0                   xor      eax, eax
00412537  668b86d8000000         mov      ax, word ptr [esi + 0xd8]
0041253e  85c0                   test     eax, eax
00412540  0f84cb000000           je       0x412611
00412546  31c9                   xor      ecx, ecx
00412548  894c2424               mov      dword ptr [esp + 0x24], ecx
0041254c  eb04                   jmp      0x412552 ;
0041254e  ff442424               inc      dword ptr [esp + 0x24]
00412552  8b442424               mov      eax, dword ptr [esp + 0x24]
00412556  663b86d8000000         cmp      ax, word ptr [esi + 0xd8]
0041255d  0f83ae000000           jae      0x412611
00412563  31db                   xor      ebx, ebx
00412565  6689c3                 mov      bx, ax
00412568  668b9c5ec4000000       mov      bx, word ptr [esi + ebx*2 + 0xc4]
00412570  81e3ffff0000           and      ebx, 0xffff
00412576  b900010000             mov      ecx, 0x100
0041257b  89da                   mov      edx, ebx
0041257d  89d8                   mov      eax, ebx
0041257f  c1fa1f                 sar      edx, 0x1f
00412582  f7f9                   idiv     ecx
00412584  89d1                   mov      ecx, edx
00412586  89da                   mov      edx, ebx
00412588  89d8                   mov      eax, ebx
0041258a  c1fa1f                 sar      edx, 0x1f
0041258d  c1e208                 shl      edx, 8
00412590  1bc2                   sbb      eax, edx
00412592  c1f808                 sar      eax, 8
00412595  89c3                   mov      ebx, eax
00412597  66a120875000           mov      ax, word ptr [0x508720]
0041259d  6639c1                 cmp      cx, ax
004125a0  72ac                   jb       0x41254e
004125a2  31d2                   xor      edx, edx
004125a4  6689c2                 mov      dx, ax
004125a7  31c0                   xor      eax, eax
004125a9  66a124875000           mov      ax, word ptr [0x508724]
004125af  01d0                   add      eax, edx
004125b1  31d2                   xor      edx, edx
004125b3  6689ca                 mov      dx, cx
004125b6  39c2                   cmp      edx, eax
004125b8  7d94                   jge      0x41254e
004125ba  663b1d22875000         cmp      bx, word ptr [0x508722]
004125c1  728b                   jb       0x41254e
004125c3  31d2                   xor      edx, edx
004125c5  31c0                   xor      eax, eax
004125c7  668b1522875000         mov      dx, word ptr [0x508722]
004125ce  66a126875000           mov      ax, word ptr [0x508726]
004125d4  01d0                   add      eax, edx
004125d6  31d2                   xor      edx, edx
004125d8  6689da                 mov      dx, bx
004125db  39c2                   cmp      edx, eax
004125dd  0f8d6bffffff           jge      0x41254e
004125e3  662b1d22875000         sub      bx, word ptr [0x508722]
004125ea  c1e305                 shl      ebx, 5
004125ed  0fbfd3                 movsx    edx, bx
004125f0  662b0d20875000         sub      cx, word ptr [0x508720]
004125f7  c1e105                 shl      ecx, 5
004125fa  bbcf1c0000             mov      ebx, 0x1ccf
004125ff  0fbfc1                 movsx    eax, cx
00412602  b901000000             mov      ecx, 1
00412607  e83b8c0400             call     0x45b247 ; PasteBobCmp
0041260c  e93dffffff             jmp      0x41254e ;
00412611  31c0                   xor      eax, eax
00412613  8a4602                 mov      al, byte ptr [esi + 2]
00412616  83f811                 cmp      eax, 0x11
00412619  0f8504030000           jne      0x412923
0041261f  8a4601                 mov      al, byte ptr [esi + 1]
00412622  3c19                   cmp      al, 0x19
00412624  0f8729040000           ja       0x412a53
0041262a  25ff000000             and      eax, 0xff
0041262f  2eff248528234100       jmp      dword ptr cs:[eax*4 + 0x412328]
00412637  31db                   xor      ebx, ebx
00412639  668b9eb2000000         mov      bx, word ptr [esi + 0xb2]
00412640  b900010000             mov      ecx, 0x100
00412645  89da                   mov      edx, ebx
00412647  89d8                   mov      eax, ebx
00412649  c1fa1f                 sar      edx, 0x1f
0041264c  f7f9                   idiv     ecx
0041264e  89d1                   mov      ecx, edx
00412650  89da                   mov      edx, ebx
00412652  89d8                   mov      eax, ebx
00412654  c1fa1f                 sar      edx, 0x1f
00412657  c1e208                 shl      edx, 8
0041265a  1bc2                   sbb      eax, edx
0041265c  c1f808                 sar      eax, 8
0041265f  668b1520875000         mov      dx, word ptr [0x508720]
00412666  6639d1                 cmp      cx, dx
00412669  726b                   jb       0x4126d6
0041266b  31db                   xor      ebx, ebx
0041266d  6689d3                 mov      bx, dx
00412670  31d2                   xor      edx, edx
00412672  668b1524875000         mov      dx, word ptr [0x508724]
00412679  01da                   add      edx, ebx
0041267b  31db                   xor      ebx, ebx
0041267d  6689cb                 mov      bx, cx
00412680  39d3                   cmp      ebx, edx
00412682  7d52                   jge      0x4126d6
00412684  663b0522875000         cmp      ax, word ptr [0x508722]
0041268b  7249                   jb       0x4126d6
0041268d  31db                   xor      ebx, ebx
0041268f  31d2                   xor      edx, edx
00412691  668b1d22875000         mov      bx, word ptr [0x508722]
00412698  668b1526875000         mov      dx, word ptr [0x508726]
0041269f  01da                   add      edx, ebx
004126a1  31db                   xor      ebx, ebx
004126a3  6689c3                 mov      bx, ax
004126a6  39d3                   cmp      ebx, edx
004126a8  7d2c                   jge      0x4126d6
004126aa  8b1424                 mov      edx, dword ptr [esp]
004126ad  31db                   xor      ebx, ebx
004126af  6689d3                 mov      bx, dx
004126b2  662b0522875000         sub      ax, word ptr [0x508722]
004126b9  c1e005                 shl      eax, 5
004126bc  0fbfd0                 movsx    edx, ax
004126bf  662b0d20875000         sub      cx, word ptr [0x508720]
004126c6  c1e105                 shl      ecx, 5
004126c9  0fbfc1                 movsx    eax, cx
004126cc  b901000000             mov      ecx, 1
004126d1  e8718b0400             call     0x45b247 ; PasteBobCmp
004126d6  31c0                   xor      eax, eax
004126d8  668b8680000000         mov      ax, word ptr [esi + 0x80]
004126df  31d2                   xor      edx, edx
004126e1  e8fc870000             call     0x41aee2 ; BatimentGetCase
004126e6  6689c2                 mov      dx, ax
004126e9  bb00010000             mov      ebx, 0x100
004126ee  89d0                   mov      eax, edx
004126f0  c1fa1f                 sar      edx, 0x1f
004126f3  f7fb                   idiv     ebx
004126f5  31c0                   xor      eax, eax
004126f7  89d3                   mov      ebx, edx
004126f9  668b8680000000         mov      ax, word ptr [esi + 0x80]
00412700  31d2                   xor      edx, edx
00412702  e8db870000             call     0x41aee2 ; BatimentGetCase
00412707  6689c2                 mov      dx, ax
0041270a  89d0                   mov      eax, edx
0041270c  c1fa1f                 sar      edx, 0x1f
0041270f  c1e208                 shl      edx, 8
00412712  1bc2                   sbb      eax, edx
00412714  c1f808                 sar      eax, 8
00412717  668b1520875000         mov      dx, word ptr [0x508720]
0041271e  89c1                   mov      ecx, eax
00412720  6639d3                 cmp      bx, dx
00412723  0f82f6feffff           jb       0x41261f
00412729  31d2                   xor      edx, edx
0041272b  31c0                   xor      eax, eax
0041272d  668b1520875000         mov      dx, word ptr [0x508720]
00412734  66a124875000           mov      ax, word ptr [0x508724]
0041273a  01d0                   add      eax, edx
0041273c  31d2                   xor      edx, edx
0041273e  6689da                 mov      dx, bx
00412741  39c2                   cmp      edx, eax
00412743  0f8dd6feffff           jge      0x41261f
00412749  66a122875000           mov      ax, word ptr [0x508722]
0041274f  6639c1                 cmp      cx, ax
00412752  0f82c7feffff           jb       0x41261f
00412758  31d2                   xor      edx, edx
0041275a  6689c2                 mov      dx, ax
0041275d  31c0                   xor      eax, eax
0041275f  66a126875000           mov      ax, word ptr [0x508726]
00412765  01d0                   add      eax, edx
00412767  31d2                   xor      edx, edx
00412769  6689ca                 mov      dx, cx
0041276c  39c2                   cmp      edx, eax
0041276e  0f8dabfeffff           jge      0x41261f
00412774  bd05000000             mov      ebp, 5
00412779  a17c8f5000             mov      eax, dword ptr [0x508f7c]
0041277e  31d2                   xor      edx, edx
00412780  f7f5                   div      ebp
00412782  83e001                 and      eax, 1
00412785  31d2                   xor      edx, edx
00412787  05451e0000             add      eax, 0x1e45
0041278c  6689c2                 mov      dx, ax
0041278f  662b0d22875000         sub      cx, word ptr [0x508722]
00412796  c1e105                 shl      ecx, 5
00412799  0fbfe9                 movsx    ebp, cx
0041279c  662b1d20875000         sub      bx, word ptr [0x508720]
004127a3  c1e305                 shl      ebx, 5
004127a6  b901000000             mov      ecx, 1
004127ab  0fbfc3                 movsx    eax, bx
004127ae  89d3                   mov      ebx, edx
004127b0  89ea                   mov      edx, ebp
004127b2  e8908a0400             call     0x45b247 ; PasteBobCmp
004127b7  e963feffff             jmp      0x41261f ;
004127bc  31db                   xor      ebx, ebx
004127be  668b9eb2000000         mov      bx, word ptr [esi + 0xb2]
004127c5  b900010000             mov      ecx, 0x100
004127ca  89da                   mov      edx, ebx
004127cc  89d8                   mov      eax, ebx
004127ce  c1fa1f                 sar      edx, 0x1f
004127d1  f7f9                   idiv     ecx
004127d3  89d1                   mov      ecx, edx
004127d5  89da                   mov      edx, ebx
004127d7  89d8                   mov      eax, ebx
004127d9  c1fa1f                 sar      edx, 0x1f
004127dc  c1e208                 shl      edx, 8
004127df  1bc2                   sbb      eax, edx
004127e1  c1f808                 sar      eax, 8
004127e4  668b1520875000         mov      dx, word ptr [0x508720]
004127eb  6639d1                 cmp      cx, dx
004127ee  726b                   jb       0x41285b
004127f0  31db                   xor      ebx, ebx
004127f2  6689d3                 mov      bx, dx
004127f5  31d2                   xor      edx, edx
004127f7  668b1524875000         mov      dx, word ptr [0x508724]
004127fe  01da                   add      edx, ebx
00412800  31db                   xor      ebx, ebx
00412802  6689cb                 mov      bx, cx
00412805  39d3                   cmp      ebx, edx
00412807  7d52                   jge      0x41285b
00412809  663b0522875000         cmp      ax, word ptr [0x508722]
00412810  7249                   jb       0x41285b
00412812  31db                   xor      ebx, ebx
00412814  31d2                   xor      edx, edx
00412816  668b1d22875000         mov      bx, word ptr [0x508722]
0041281d  668b1526875000         mov      dx, word ptr [0x508726]
00412824  01da                   add      edx, ebx
00412826  31db                   xor      ebx, ebx
00412828  6689c3                 mov      bx, ax
0041282b  39d3                   cmp      ebx, edx
0041282d  7d2c                   jge      0x41285b
0041282f  8b1424                 mov      edx, dword ptr [esp]
00412832  31db                   xor      ebx, ebx
00412834  6689d3                 mov      bx, dx
00412837  662b0522875000         sub      ax, word ptr [0x508722]
0041283e  c1e005                 shl      eax, 5
00412841  0fbfd0                 movsx    edx, ax
00412844  662b0d20875000         sub      cx, word ptr [0x508720]
0041284b  c1e105                 shl      ecx, 5
0041284e  0fbfc1                 movsx    eax, cx
00412851  b901000000             mov      ecx, 1
00412856  e8ec890400             call     0x45b247 ; PasteBobCmp
0041285b  31db                   xor      ebx, ebx
0041285d  668b9e80000000         mov      bx, word ptr [esi + 0x80]
00412864  b900010000             mov      ecx, 0x100
00412869  89da                   mov      edx, ebx
0041286b  89d8                   mov      eax, ebx
0041286d  c1fa1f                 sar      edx, 0x1f
00412870  f7f9                   idiv     ecx
00412872  89d1                   mov      ecx, edx
00412874  89da                   mov      edx, ebx
00412876  89d8                   mov      eax, ebx
00412878  c1fa1f                 sar      edx, 0x1f
0041287b  c1e208                 shl      edx, 8
0041287e  1bc2                   sbb      eax, edx
00412880  c1f808                 sar      eax, 8
00412883  668b1520875000         mov      dx, word ptr [0x508720]
0041288a  89c3                   mov      ebx, eax
0041288c  6639d1                 cmp      cx, dx
0041288f  0f828afdffff           jb       0x41261f
00412895  31d2                   xor      edx, edx
00412897  31c0                   xor      eax, eax
00412899  668b1520875000         mov      dx, word ptr [0x508720]
004128a0  66a124875000           mov      ax, word ptr [0x508724]
004128a6  01d0                   add      eax, edx
004128a8  31d2                   xor      edx, edx
004128aa  6689ca                 mov      dx, cx
004128ad  39c2                   cmp      edx, eax
004128af  0f8d6afdffff           jge      0x41261f
004128b5  66a122875000           mov      ax, word ptr [0x508722]
004128bb  6639c3                 cmp      bx, ax
004128be  0f825bfdffff           jb       0x41261f
004128c4  31d2                   xor      edx, edx
004128c6  6689c2                 mov      dx, ax
004128c9  31c0                   xor      eax, eax
004128cb  66a126875000           mov      ax, word ptr [0x508726]
004128d1  01d0                   add      eax, edx
004128d3  31d2                   xor      edx, edx
004128d5  6689da                 mov      dx, bx
004128d8  39c2                   cmp      edx, eax
004128da  0f8d3ffdffff           jge      0x41261f
004128e0  bd05000000             mov      ebp, 5
004128e5  a17c8f5000             mov      eax, dword ptr [0x508f7c]
004128ea  31d2                   xor      edx, edx
004128ec  f7f5                   div      ebp
004128ee  83e001                 and      eax, 1
004128f1  05451e0000             add      eax, 0x1e45
004128f6  662b1d22875000         sub      bx, word ptr [0x508722]
004128fd  c1e305                 shl      ebx, 5
00412900  0fbfd3                 movsx    edx, bx
00412903  662b0d20875000         sub      cx, word ptr [0x508720]
0041290a  25ffff0000             and      eax, 0xffff
0041290f  c1e105                 shl      ecx, 5
00412912  89c3                   mov      ebx, eax
00412914  0fbfe9                 movsx    ebp, cx
00412917  b901000000             mov      ecx, 1
0041291c  89e8                   mov      eax, ebp
0041291e  e98ffeffff             jmp      0x4127b2 ;
00412923  8a9e82000000           mov      bl, byte ptr [esi + 0x82]
00412929  80fb01                 cmp      bl, 1
0041292c  0f82edfcffff           jb       0x41261f
00412932  b905000000             mov      ecx, 5
00412937  a17c8f5000             mov      eax, dword ptr [0x508f7c]
0041293c  31d2                   xor      edx, edx
0041293e  f7f1                   div      ecx
00412940  83e001                 and      eax, 1
00412943  05431e0000             add      eax, 0x1e43
00412948  890424                 mov      dword ptr [esp], eax
0041294b  80fb01                 cmp      bl, 1
0041294e  0f8668feffff           jbe      0x4127bc
00412954  80fb02                 cmp      bl, 2
00412957  0f84dafcffff           je       0x412637
0041295d  e9bdfcffff             jmp      0x41261f ;
00412962  89f8                   mov      eax, edi
00412964  051a000000             add      eax, 0x1a
00412969  0fbfd0                 movsx    edx, ax
0041296c  8b442428               mov      eax, dword ptr [esp + 0x28]
00412970  b901000000             mov      ecx, 1
00412975  0502000000             add      eax, 2
0041297a  bb202a0000             mov      ebx, 0x2a20
0041297f  98                     cwde
00412980  e8118e0400             call     0x45b796 ; PasteOmbreCmp
00412985  31d2                   xor      edx, edx
00412987  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041298d  42                     inc      edx
0041298e  89d0                   mov      eax, edx
00412990  c1fa1f                 sar      edx, 0x1f
00412993  2bc2                   sub      eax, edx
00412995  d1f8                   sar      eax, 1
00412997  31d2                   xor      edx, edx
00412999  48                     dec      eax
0041299a  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004129a0  0fafd0                 imul     edx, eax
004129a3  31c0                   xor      eax, eax
004129a5  81c292090000           add      edx, 0x992
004129ab  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
004129b1  e902030000             jmp      0x412cb8 ;
004129b6  8d460a                 lea      eax, [esi + 0xa]
004129b9  8b5c2428               mov      ebx, dword ptr [esp + 0x28]
004129bd  e8f7460300             call     0x4470b9 ; BagVide
004129c2  89fa                   mov      edx, edi
004129c4  83c302                 add      ebx, 2
004129c7  83c21a                 add      edx, 0x1a
004129ca  84c0                   test     al, al
004129cc  0f84cd000000           je       0x412a9f
004129d2  b901000000             mov      ecx, 1
004129d7  0fbfd2                 movsx    edx, dx
004129da  0fbfc3                 movsx    eax, bx
004129dd  bb202a0000             mov      ebx, 0x2a20
004129e2  e8af8d0400             call     0x45b796 ; PasteOmbreCmp
004129e7  31d2                   xor      edx, edx
004129e9  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004129ef  42                     inc      edx
004129f0  89d0                   mov      eax, edx
004129f2  c1fa1f                 sar      edx, 0x1f
004129f5  2bc2                   sub      eax, edx
004129f7  d1f8                   sar      eax, 1
004129f9  31d2                   xor      edx, edx
004129fb  48                     dec      eax
004129fc  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412a02  0fafc2                 imul     eax, edx
00412a05  31d2                   xor      edx, edx
00412a07  0542050000             add      eax, 0x542
00412a0c  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00412a12  31db                   xor      ebx, ebx
00412a14  01d0                   add      eax, edx
00412a16  6689c3                 mov      bx, ax
00412a19  8b442408               mov      eax, dword ptr [esp + 8]
00412a1d  01f8                   add      eax, edi
00412a1f  0fbfd0                 movsx    edx, ax
00412a22  8b442428               mov      eax, dword ptr [esp + 0x28]
00412a26  03442418               add      eax, dword ptr [esp + 0x18]
00412a2a  6689442434             mov      word ptr [esp + 0x34], ax
00412a2f  31c9                   xor      ecx, ecx
00412a31  8b442432               mov      eax, dword ptr [esp + 0x32]
00412a35  668b4c240c             mov      cx, word ptr [esp + 0xc]
00412a3a  c1f810                 sar      eax, 0x10
00412a3d  e805e7ffff             call     0x411147 ; AffCorpsEngin
00412a42  8b442428               mov      eax, dword ptr [esp + 0x28]
00412a46  83ef09                 sub      edi, 9
00412a49  668944241c             mov      word ptr [esp + 0x1c], ax
00412a4e  66897c2420             mov      word ptr [esp + 0x20], di
00412a53  8a1d41805000           mov      bl, byte ptr [0x508041]
00412a59  3a1e                   cmp      bl, byte ptr [esi]
00412a5b  7509                   jne      0x412a66
00412a5d  80bebd00000000         cmp      byte ptr [esi + 0xbd], 0
00412a64  751a                   jne      0x412a80
00412a66  8b7c240c               mov      edi, dword ptr [esp + 0xc]
00412a6a  663b3dc26a4900         cmp      di, word ptr [0x496ac2]
00412a71  740d                   je       0x412a80
00412a73  803d8f8f500000         cmp      byte ptr [0x508f8f], 0
00412a7a  0f84e80a0000           je       0x413568
00412a80  8b54241e               mov      edx, dword ptr [esp + 0x1e]
00412a84  31db                   xor      ebx, ebx
00412a86  8b44241a               mov      eax, dword ptr [esp + 0x1a]
00412a8a  668b5c240c             mov      bx, word ptr [esp + 0xc]
00412a8f  c1fa10                 sar      edx, 0x10
00412a92  c1f810                 sar      eax, 0x10
00412a95  e84ae1ffff             call     0x410be4 ; AffInfoSelection
00412a9a  e93d0c0000             jmp      0x4136dc ;
00412a9f  b901000000             mov      ecx, 1
00412aa4  0fbfd2                 movsx    edx, dx
00412aa7  0fbfc3                 movsx    eax, bx
00412aaa  bb202a0000             mov      ebx, 0x2a20
00412aaf  e8e28c0400             call     0x45b796 ; PasteOmbreCmp
00412ab4  31d2                   xor      edx, edx
00412ab6  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412abc  42                     inc      edx
00412abd  89d0                   mov      eax, edx
00412abf  c1fa1f                 sar      edx, 0x1f
00412ac2  2bc2                   sub      eax, edx
00412ac4  d1f8                   sar      eax, 1
00412ac6  31d2                   xor      edx, edx
00412ac8  48                     dec      eax
00412ac9  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412acf  0fafd0                 imul     edx, eax
00412ad2  31c0                   xor      eax, eax
00412ad4  81c2c2050000           add      edx, 0x5c2
00412ada  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00412ae0  e92dffffff             jmp      0x412a12 ;
00412ae5  8d460a                 lea      eax, [esi + 0xa]
00412ae8  8b5c2428               mov      ebx, dword ptr [esp + 0x28]
00412aec  e8c8450300             call     0x4470b9 ; BagVide
00412af1  89fa                   mov      edx, edi
00412af3  83c302                 add      ebx, 2
00412af6  83c21a                 add      edx, 0x1a
00412af9  84c0                   test     al, al
00412afb  743f                   je       0x412b3c
00412afd  b901000000             mov      ecx, 1
00412b02  0fbfd2                 movsx    edx, dx
00412b05  0fbfc3                 movsx    eax, bx
00412b08  bb202a0000             mov      ebx, 0x2a20
00412b0d  e8848c0400             call     0x45b796 ; PasteOmbreCmp
00412b12  31d2                   xor      edx, edx
00412b14  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412b1a  42                     inc      edx
00412b1b  89d0                   mov      eax, edx
00412b1d  c1fa1f                 sar      edx, 0x1f
00412b20  2bc2                   sub      eax, edx
00412b22  d1f8                   sar      eax, 1
00412b24  31d2                   xor      edx, edx
00412b26  48                     dec      eax
00412b27  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412b2d  0fafc2                 imul     eax, edx
00412b30  31d2                   xor      edx, edx
00412b32  05a20b0000             add      eax, 0xba2
00412b37  e9d0feffff             jmp      0x412a0c ;
00412b3c  b901000000             mov      ecx, 1
00412b41  0fbfd2                 movsx    edx, dx
00412b44  0fbfc3                 movsx    eax, bx
00412b47  bb202a0000             mov      ebx, 0x2a20
00412b4c  e8458c0400             call     0x45b796 ; PasteOmbreCmp
00412b51  31d2                   xor      edx, edx
00412b53  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412b59  42                     inc      edx
00412b5a  89d0                   mov      eax, edx
00412b5c  c1fa1f                 sar      edx, 0x1f
00412b5f  2bc2                   sub      eax, edx
00412b61  d1f8                   sar      eax, 1
00412b63  31d2                   xor      edx, edx
00412b65  48                     dec      eax
00412b66  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412b6c  0fafc2                 imul     eax, edx
00412b6f  31d2                   xor      edx, edx
00412b71  05e20b0000             add      eax, 0xbe2
00412b76  e991feffff             jmp      0x412a0c ;
00412b7b  8d460a                 lea      eax, [esi + 0xa]
00412b7e  8b5c2428               mov      ebx, dword ptr [esp + 0x28]
00412b82  e832450300             call     0x4470b9 ; BagVide
00412b87  88c2                   mov      dl, al
00412b89  89f8                   mov      eax, edi
00412b8b  83c302                 add      ebx, 2
00412b8e  051a000000             add      eax, 0x1a
00412b93  84d2                   test     dl, dl
00412b95  7446                   je       0x412bdd
00412b97  b901000000             mov      ecx, 1
00412b9c  0fbfd0                 movsx    edx, ax
00412b9f  0fbfc3                 movsx    eax, bx
00412ba2  bb202a0000             mov      ebx, 0x2a20
00412ba7  e8ea8b0400             call     0x45b796 ; PasteOmbreCmp
00412bac  31d2                   xor      edx, edx
00412bae  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412bb4  42                     inc      edx
00412bb5  89d0                   mov      eax, edx
00412bb7  c1fa1f                 sar      edx, 0x1f
00412bba  2bc2                   sub      eax, edx
00412bbc  d1f8                   sar      eax, 1
00412bbe  31d2                   xor      edx, edx
00412bc0  48                     dec      eax
00412bc1  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412bc7  0fafd0                 imul     edx, eax
00412bca  31c0                   xor      eax, eax
00412bcc  81c242060000           add      edx, 0x642
00412bd2  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00412bd8  e935feffff             jmp      0x412a12 ;
00412bdd  b901000000             mov      ecx, 1
00412be2  0fbfd0                 movsx    edx, ax
00412be5  0fbfc3                 movsx    eax, bx
00412be8  bb202a0000             mov      ebx, 0x2a20
00412bed  e8a48b0400             call     0x45b796 ; PasteOmbreCmp
00412bf2  31d2                   xor      edx, edx
00412bf4  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412bfa  42                     inc      edx
00412bfb  89d0                   mov      eax, edx
00412bfd  c1fa1f                 sar      edx, 0x1f
00412c00  2bc2                   sub      eax, edx
00412c02  d1f8                   sar      eax, 1
00412c04  31d2                   xor      edx, edx
00412c06  48                     dec      eax
00412c07  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412c0d  0fafc2                 imul     eax, edx
00412c10  31d2                   xor      edx, edx
00412c12  05a2060000             add      eax, 0x6a2
00412c17  e9f0fdffff             jmp      0x412a0c ;
00412c1c  89f8                   mov      eax, edi
00412c1e  051a000000             add      eax, 0x1a
00412c23  0fbfd0                 movsx    edx, ax
00412c26  8b442428               mov      eax, dword ptr [esp + 0x28]
00412c2a  b901000000             mov      ecx, 1
00412c2f  0502000000             add      eax, 2
00412c34  bb202a0000             mov      ebx, 0x2a20
00412c39  98                     cwde
00412c3a  e8578b0400             call     0x45b796 ; PasteOmbreCmp
00412c3f  31d2                   xor      edx, edx
00412c41  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412c47  42                     inc      edx
00412c48  89d0                   mov      eax, edx
00412c4a  c1fa1f                 sar      edx, 0x1f
00412c4d  2bc2                   sub      eax, edx
00412c4f  d1f8                   sar      eax, 1
00412c51  31d2                   xor      edx, edx
00412c53  48                     dec      eax
00412c54  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412c5a  0fafd0                 imul     edx, eax
00412c5d  31c0                   xor      eax, eax
00412c5f  81c222070000           add      edx, 0x722
00412c65  e941fdffff             jmp      0x4129ab ;
00412c6a  89f8                   mov      eax, edi
00412c6c  051a000000             add      eax, 0x1a
00412c71  0fbfd0                 movsx    edx, ax
00412c74  8b442428               mov      eax, dword ptr [esp + 0x28]
00412c78  b901000000             mov      ecx, 1
00412c7d  0502000000             add      eax, 2
00412c82  bb202a0000             mov      ebx, 0x2a20
00412c87  98                     cwde
00412c88  e8098b0400             call     0x45b796 ; PasteOmbreCmp
00412c8d  31d2                   xor      edx, edx
00412c8f  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412c95  42                     inc      edx
00412c96  89d0                   mov      eax, edx
00412c98  c1fa1f                 sar      edx, 0x1f
00412c9b  2bc2                   sub      eax, edx
00412c9d  d1f8                   sar      eax, 1
00412c9f  31d2                   xor      edx, edx
00412ca1  48                     dec      eax
00412ca2  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412ca8  0fafc2                 imul     eax, edx
00412cab  31d2                   xor      edx, edx
00412cad  05a2070000             add      eax, 0x7a2
00412cb2  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00412cb8  31db                   xor      ebx, ebx
00412cba  01d0                   add      eax, edx
00412cbc  6689c3                 mov      bx, ax
00412cbf  8b442408               mov      eax, dword ptr [esp + 8]
00412cc3  01f8                   add      eax, edi
00412cc5  0fbfd0                 movsx    edx, ax
00412cc8  8b442428               mov      eax, dword ptr [esp + 0x28]
00412ccc  03442418               add      eax, dword ptr [esp + 0x18]
00412cd0  6689442434             mov      word ptr [esp + 0x34], ax
00412cd5  31c9                   xor      ecx, ecx
00412cd7  8b442432               mov      eax, dword ptr [esp + 0x32]
00412cdb  668b4c240c             mov      cx, word ptr [esp + 0xc]
00412ce0  c1f810                 sar      eax, 0x10
00412ce3  83ef09                 sub      edi, 9
00412ce6  e85ce4ffff             call     0x411147 ; AffCorpsEngin
00412ceb  8b442428               mov      eax, dword ptr [esp + 0x28]
00412cef  66897c2420             mov      word ptr [esp + 0x20], di
00412cf4  668944241c             mov      word ptr [esp + 0x1c], ax
00412cf9  e955fdffff             jmp      0x412a53 ;
00412cfe  89f8                   mov      eax, edi
00412d00  051a000000             add      eax, 0x1a
00412d05  0fbfd0                 movsx    edx, ax
00412d08  8b442428               mov      eax, dword ptr [esp + 0x28]
00412d0c  b901000000             mov      ecx, 1
00412d11  0502000000             add      eax, 2
00412d16  bb202a0000             mov      ebx, 0x2a20
00412d1b  98                     cwde
00412d1c  e8758a0400             call     0x45b796 ; PasteOmbreCmp
00412d21  31d2                   xor      edx, edx
00412d23  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412d29  42                     inc      edx
00412d2a  89d0                   mov      eax, edx
00412d2c  c1fa1f                 sar      edx, 0x1f
00412d2f  2bc2                   sub      eax, edx
00412d31  d1f8                   sar      eax, 1
00412d33  31d2                   xor      edx, edx
00412d35  48                     dec      eax
00412d36  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412d3c  0fafd0                 imul     edx, eax
00412d3f  31c0                   xor      eax, eax
00412d41  81c222080000           add      edx, 0x822
00412d47  e95ffcffff             jmp      0x4129ab ;
00412d4c  89f8                   mov      eax, edi
00412d4e  051a000000             add      eax, 0x1a
00412d53  0fbfd0                 movsx    edx, ax
00412d56  8b442428               mov      eax, dword ptr [esp + 0x28]
00412d5a  b901000000             mov      ecx, 1
00412d5f  0502000000             add      eax, 2
00412d64  bb202a0000             mov      ebx, 0x2a20
00412d69  98                     cwde
00412d6a  e8278a0400             call     0x45b796 ; PasteOmbreCmp
00412d6f  31d2                   xor      edx, edx
00412d71  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412d77  42                     inc      edx
00412d78  89d0                   mov      eax, edx
00412d7a  c1fa1f                 sar      edx, 0x1f
00412d7d  2bc2                   sub      eax, edx
00412d7f  d1f8                   sar      eax, 1
00412d81  31d2                   xor      edx, edx
00412d83  48                     dec      eax
00412d84  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412d8a  0fafc2                 imul     eax, edx
00412d8d  31d2                   xor      edx, edx
00412d8f  05f2080000             add      eax, 0x8f2
00412d94  e919ffffff             jmp      0x412cb2 ;
00412d99  31d2                   xor      edx, edx
00412d9b  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412da1  42                     inc      edx
00412da2  89d0                   mov      eax, edx
00412da4  c1fa1f                 sar      edx, 0x1f
00412da7  2bc2                   sub      eax, edx
00412da9  d1f8                   sar      eax, 1
00412dab  31d2                   xor      edx, edx
00412dad  48                     dec      eax
00412dae  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412db4  0fafd0                 imul     edx, eax
00412db7  31c0                   xor      eax, eax
00412db9  81c2220e0000           add      edx, 0xe22
00412dbf  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00412dc5  31db                   xor      ebx, ebx
00412dc7  01d0                   add      eax, edx
00412dc9  6689c3                 mov      bx, ax
00412dcc  8b442408               mov      eax, dword ptr [esp + 8]
00412dd0  01f8                   add      eax, edi
00412dd2  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00412dd6  0fbfd0                 movsx    edx, ax
00412dd9  8b442428               mov      eax, dword ptr [esp + 0x28]
00412ddd  01c8                   add      eax, ecx
00412ddf  b901000000             mov      ecx, 1
00412de4  98                     cwde
00412de5  e8ac890400             call     0x45b796 ; PasteOmbreCmp
00412dea  31d2                   xor      edx, edx
00412dec  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412df2  42                     inc      edx
00412df3  89d0                   mov      eax, edx
00412df5  c1fa1f                 sar      edx, 0x1f
00412df8  2bc2                   sub      eax, edx
00412dfa  d1f8                   sar      eax, 1
00412dfc  31d2                   xor      edx, edx
00412dfe  48                     dec      eax
00412dff  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412e05  0fafc2                 imul     eax, edx
00412e08  31d2                   xor      edx, edx
00412e0a  05620d0000             add      eax, 0xd62
00412e0f  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00412e15  31db                   xor      ebx, ebx
00412e17  01d0                   add      eax, edx
00412e19  6689c3                 mov      bx, ax
00412e1c  8b442408               mov      eax, dword ptr [esp + 8]
00412e20  01f8                   add      eax, edi
00412e22  0fbfd0                 movsx    edx, ax
00412e25  8b442428               mov      eax, dword ptr [esp + 0x28]
00412e29  03442418               add      eax, dword ptr [esp + 0x18]
00412e2d  6689442434             mov      word ptr [esp + 0x34], ax
00412e32  31c9                   xor      ecx, ecx
00412e34  8b442432               mov      eax, dword ptr [esp + 0x32]
00412e38  668b4c240c             mov      cx, word ptr [esp + 0xc]
00412e3d  c1f810                 sar      eax, 0x10
00412e40  e802e3ffff             call     0x411147 ; AffCorpsEngin
00412e45  8b442428               mov      eax, dword ptr [esp + 0x28]
00412e49  83ef18                 sub      edi, 0x18
00412e4c  83e80f                 sub      eax, 0xf
00412e4f  e99bfeffff             jmp      0x412cef ;
00412e54  31d2                   xor      edx, edx
00412e56  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412e5c  42                     inc      edx
00412e5d  89d0                   mov      eax, edx
00412e5f  c1fa1f                 sar      edx, 0x1f
00412e62  2bc2                   sub      eax, edx
00412e64  d1f8                   sar      eax, 1
00412e66  31d2                   xor      edx, edx
00412e68  48                     dec      eax
00412e69  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412e6f  0fafc2                 imul     eax, edx
00412e72  31d2                   xor      edx, edx
00412e74  05a20f0000             add      eax, 0xfa2
00412e79  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
00412e7f  31db                   xor      ebx, ebx
00412e81  01d0                   add      eax, edx
00412e83  6689c3                 mov      bx, ax
00412e86  8b442408               mov      eax, dword ptr [esp + 8]
00412e8a  01f8                   add      eax, edi
00412e8c  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00412e90  0fbfd0                 movsx    edx, ax
00412e93  8b442428               mov      eax, dword ptr [esp + 0x28]
00412e97  01c8                   add      eax, ecx
00412e99  b901000000             mov      ecx, 1
00412e9e  98                     cwde
00412e9f  e8f2880400             call     0x45b796 ; PasteOmbreCmp
00412ea4  31d2                   xor      edx, edx
00412ea6  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412eac  42                     inc      edx
00412ead  89d0                   mov      eax, edx
00412eaf  c1fa1f                 sar      edx, 0x1f
00412eb2  2bc2                   sub      eax, edx
00412eb4  d1f8                   sar      eax, 1
00412eb6  31d2                   xor      edx, edx
00412eb8  48                     dec      eax
00412eb9  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412ebf  0fafc2                 imul     eax, edx
00412ec2  31d2                   xor      edx, edx
00412ec4  05e20e0000             add      eax, 0xee2
00412ec9  e941ffffff             jmp      0x412e0f ;
00412ece  89f8                   mov      eax, edi
00412ed0  051a000000             add      eax, 0x1a
00412ed5  0fbfd0                 movsx    edx, ax
00412ed8  8b442428               mov      eax, dword ptr [esp + 0x28]
00412edc  b901000000             mov      ecx, 1
00412ee1  0502000000             add      eax, 2
00412ee6  bb202a0000             mov      ebx, 0x2a20
00412eeb  98                     cwde
00412eec  e8a5880400             call     0x45b796 ; PasteOmbreCmp
00412ef1  31d2                   xor      edx, edx
00412ef3  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412ef9  42                     inc      edx
00412efa  89d0                   mov      eax, edx
00412efc  c1fa1f                 sar      edx, 0x1f
00412eff  2bc2                   sub      eax, edx
00412f01  d1f8                   sar      eax, 1
00412f03  31d2                   xor      edx, edx
00412f05  48                     dec      eax
00412f06  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412f0c  0fafd0                 imul     edx, eax
00412f0f  31c0                   xor      eax, eax
00412f11  81c2820c0000           add      edx, 0xc82
00412f17  e98ffaffff             jmp      0x4129ab ;
00412f1c  89f8                   mov      eax, edi
00412f1e  051a000000             add      eax, 0x1a
00412f23  0fbfd0                 movsx    edx, ax
00412f26  8b442428               mov      eax, dword ptr [esp + 0x28]
00412f2a  b901000000             mov      ecx, 1
00412f2f  0502000000             add      eax, 2
00412f34  bb202a0000             mov      ebx, 0x2a20
00412f39  98                     cwde
00412f3a  e857880400             call     0x45b796 ; PasteOmbreCmp
00412f3f  31d2                   xor      edx, edx
00412f41  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00412f47  42                     inc      edx
00412f48  89d0                   mov      eax, edx
00412f4a  c1fa1f                 sar      edx, 0x1f
00412f4d  2bc2                   sub      eax, edx
00412f4f  d1f8                   sar      eax, 1
00412f51  31d2                   xor      edx, edx
00412f53  48                     dec      eax
00412f54  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412f5a  0fafc2                 imul     eax, edx
00412f5d  31d2                   xor      edx, edx
00412f5f  05720a0000             add      eax, 0xa72
00412f64  e949fdffff             jmp      0x412cb2 ;
00412f69  31db                   xor      ebx, ebx
00412f6b  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00412f71  89da                   mov      edx, ebx
00412f73  89d8                   mov      eax, ebx
00412f75  c1fa1f                 sar      edx, 0x1f
00412f78  2bc2                   sub      eax, edx
00412f7a  d1f8                   sar      eax, 1
00412f7c  31d2                   xor      edx, edx
00412f7e  89c1                   mov      ecx, eax
00412f80  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00412f86  0fafca                 imul     ecx, edx
00412f89  8d53ff                 lea      edx, [ebx - 1]
00412f8c  89d0                   mov      eax, edx
00412f8e  c1fa1f                 sar      edx, 0x1f
00412f91  2bc2                   sub      eax, edx
00412f93  d1f8                   sar      eax, 1
00412f95  bd02000000             mov      ebp, 2
00412f9a  89da                   mov      edx, ebx
00412f9c  01c1                   add      ecx, eax
00412f9e  89d8                   mov      eax, ebx
00412fa0  c1fa1f                 sar      edx, 0x1f
00412fa3  f7fd                   idiv     ebp
00412fa5  31c0                   xor      eax, eax
00412fa7  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00412fad  0fafc2                 imul     eax, edx
00412fb0  01c8                   add      eax, ecx
00412fb2  31db                   xor      ebx, ebx
00412fb4  89442404               mov      dword ptr [esp + 4], eax
00412fb8  0572120000             add      eax, 0x1272
00412fbd  6689c3                 mov      bx, ax
00412fc0  8b442408               mov      eax, dword ptr [esp + 8]
00412fc4  01f8                   add      eax, edi
00412fc6  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00412fca  0fbfd0                 movsx    edx, ax
00412fcd  8b442428               mov      eax, dword ptr [esp + 0x28]
00412fd1  01c8                   add      eax, ecx
00412fd3  b901000000             mov      ecx, 1
00412fd8  98                     cwde
00412fd9  e8b8870400             call     0x45b796 ; PasteOmbreCmp
00412fde  8b442404               mov      eax, dword ptr [esp + 4]
00412fe2  31db                   xor      ebx, ebx
00412fe4  0512120000             add      eax, 0x1212
00412fe9  e9cefcffff             jmp      0x412cbc ;
00412fee  31db                   xor      ebx, ebx
00412ff0  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00412ff6  89da                   mov      edx, ebx
00412ff8  89d8                   mov      eax, ebx
00412ffa  c1fa1f                 sar      edx, 0x1f
00412ffd  2bc2                   sub      eax, edx
00412fff  d1f8                   sar      eax, 1
00413001  31d2                   xor      edx, edx
00413003  89c1                   mov      ecx, eax
00413005  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041300b  0fafca                 imul     ecx, edx
0041300e  8d53ff                 lea      edx, [ebx - 1]
00413011  89d0                   mov      eax, edx
00413013  c1fa1f                 sar      edx, 0x1f
00413016  2bc2                   sub      eax, edx
00413018  d1f8                   sar      eax, 1
0041301a  8d2c01                 lea      ebp, [ecx + eax]
0041301d  89da                   mov      edx, ebx
0041301f  b902000000             mov      ecx, 2
00413024  89d8                   mov      eax, ebx
00413026  c1fa1f                 sar      edx, 0x1f
00413029  f7f9                   idiv     ecx
0041302b  31c0                   xor      eax, eax
0041302d  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413033  0fafc2                 imul     eax, edx
00413036  01e8                   add      eax, ebp
00413038  31db                   xor      ebx, ebx
0041303a  89442404               mov      dword ptr [esp + 4], eax
0041303e  05ad130000             add      eax, 0x13ad
00413043  6689c3                 mov      bx, ax
00413046  8b442408               mov      eax, dword ptr [esp + 8]
0041304a  01f8                   add      eax, edi
0041304c  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00413050  0fbfd0                 movsx    edx, ax
00413053  8b442428               mov      eax, dword ptr [esp + 0x28]
00413057  01c8                   add      eax, ecx
00413059  b901000000             mov      ecx, 1
0041305e  98                     cwde
0041305f  e832870400             call     0x45b796 ; PasteOmbreCmp
00413064  8b442404               mov      eax, dword ptr [esp + 4]
00413068  31db                   xor      ebx, ebx
0041306a  0565130000             add      eax, 0x1365
0041306f  6689c3                 mov      bx, ax
00413072  8b442408               mov      eax, dword ptr [esp + 8]
00413076  01f8                   add      eax, edi
00413078  83e814                 sub      eax, 0x14
0041307b  89442434               mov      dword ptr [esp + 0x34], eax
0041307f  31c0                   xor      eax, eax
00413081  8b542434               mov      edx, dword ptr [esp + 0x34]
00413085  8a86ab000000           mov      al, byte ptr [esi + 0xab]
0041308b  29c2                   sub      edx, eax
0041308d  8b442428               mov      eax, dword ptr [esp + 0x28]
00413091  03442418               add      eax, dword ptr [esp + 0x18]
00413095  31c9                   xor      ecx, ecx
00413097  6689442434             mov      word ptr [esp + 0x34], ax
0041309c  668b4c240c             mov      cx, word ptr [esp + 0xc]
004130a1  8b442432               mov      eax, dword ptr [esp + 0x32]
004130a5  0fbfd2                 movsx    edx, dx
004130a8  c1f810                 sar      eax, 0x10
004130ab  e897e0ffff             call     0x411147 ; AffCorpsEngin
004130b0  8b442428               mov      eax, dword ptr [esp + 0x28]
004130b4  83ef29                 sub      edi, 0x29
004130b7  83e820                 sub      eax, 0x20
004130ba  e930fcffff             jmp      0x412cef ;
004130bf  31db                   xor      ebx, ebx
004130c1  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
004130c7  89da                   mov      edx, ebx
004130c9  89d8                   mov      eax, ebx
004130cb  c1fa1f                 sar      edx, 0x1f
004130ce  2bc2                   sub      eax, edx
004130d0  d1f8                   sar      eax, 1
004130d2  31d2                   xor      edx, edx
004130d4  89c5                   mov      ebp, eax
004130d6  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004130dc  0fafea                 imul     ebp, edx
004130df  8d53ff                 lea      edx, [ebx - 1]
004130e2  89d0                   mov      eax, edx
004130e4  c1fa1f                 sar      edx, 0x1f
004130e7  2bc2                   sub      eax, edx
004130e9  d1f8                   sar      eax, 1
004130eb  b902000000             mov      ecx, 2
004130f0  89da                   mov      edx, ebx
004130f2  01c5                   add      ebp, eax
004130f4  89d8                   mov      eax, ebx
004130f6  c1fa1f                 sar      edx, 0x1f
004130f9  f7f9                   idiv     ecx
004130fb  31c0                   xor      eax, eax
004130fd  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413103  0fafc2                 imul     eax, edx
00413106  01e8                   add      eax, ebp
00413108  31db                   xor      ebx, ebx
0041310a  89442404               mov      dword ptr [esp + 4], eax
0041310e  059a100000             add      eax, 0x109a
00413113  6689c3                 mov      bx, ax
00413116  8b442408               mov      eax, dword ptr [esp + 8]
0041311a  01f8                   add      eax, edi
0041311c  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00413120  0fbfd0                 movsx    edx, ax
00413123  8b442428               mov      eax, dword ptr [esp + 0x28]
00413127  01c8                   add      eax, ecx
00413129  b901000000             mov      ecx, 1
0041312e  98                     cwde
0041312f  e862860400             call     0x45b796 ; PasteOmbreCmp
00413134  8b442404               mov      eax, dword ptr [esp + 4]
00413138  31db                   xor      ebx, ebx
0041313a  0562100000             add      eax, 0x1062
0041313f  e978fbffff             jmp      0x412cbc ;
00413144  31db                   xor      ebx, ebx
00413146  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
0041314c  89da                   mov      edx, ebx
0041314e  89d8                   mov      eax, ebx
00413150  c1fa1f                 sar      edx, 0x1f
00413153  2bc2                   sub      eax, edx
00413155  d1f8                   sar      eax, 1
00413157  31d2                   xor      edx, edx
00413159  89c1                   mov      ecx, eax
0041315b  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00413161  0fafca                 imul     ecx, edx
00413164  8d53ff                 lea      edx, [ebx - 1]
00413167  89d0                   mov      eax, edx
00413169  c1fa1f                 sar      edx, 0x1f
0041316c  2bc2                   sub      eax, edx
0041316e  d1f8                   sar      eax, 1
00413170  8d2c01                 lea      ebp, [ecx + eax]
00413173  89da                   mov      edx, ebx
00413175  b902000000             mov      ecx, 2
0041317a  89d8                   mov      eax, ebx
0041317c  c1fa1f                 sar      edx, 0x1f
0041317f  f7f9                   idiv     ecx
00413181  31c0                   xor      eax, eax
00413183  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413189  0fafc2                 imul     eax, edx
0041318c  01e8                   add      eax, ebp
0041318e  31db                   xor      ebx, ebx
00413190  89442404               mov      dword ptr [esp + 4], eax
00413194  0502130000             add      eax, 0x1302
00413199  6689c3                 mov      bx, ax
0041319c  8b442408               mov      eax, dword ptr [esp + 8]
004131a0  01f8                   add      eax, edi
004131a2  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
004131a6  0fbfd0                 movsx    edx, ax
004131a9  8b442428               mov      eax, dword ptr [esp + 0x28]
004131ad  01c8                   add      eax, ecx
004131af  b901000000             mov      ecx, 1
004131b4  98                     cwde
004131b5  e8dc850400             call     0x45b796 ; PasteOmbreCmp
004131ba  8b442404               mov      eax, dword ptr [esp + 4]
004131be  31db                   xor      ebx, ebx
004131c0  05d2120000             add      eax, 0x12d2
004131c5  e9f2faffff             jmp      0x412cbc ;
004131ca  31db                   xor      ebx, ebx
004131cc  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
004131d2  89da                   mov      edx, ebx
004131d4  89d8                   mov      eax, ebx
004131d6  c1fa1f                 sar      edx, 0x1f
004131d9  2bc2                   sub      eax, edx
004131db  d1f8                   sar      eax, 1
004131dd  31d2                   xor      edx, edx
004131df  89c1                   mov      ecx, eax
004131e1  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004131e7  0fafca                 imul     ecx, edx
004131ea  8d53ff                 lea      edx, [ebx - 1]
004131ed  89d0                   mov      eax, edx
004131ef  c1fa1f                 sar      edx, 0x1f
004131f2  2bc2                   sub      eax, edx
004131f4  d1f8                   sar      eax, 1
004131f6  8d2c01                 lea      ebp, [ecx + eax]
004131f9  89da                   mov      edx, ebx
004131fb  b902000000             mov      ecx, 2
00413200  89d8                   mov      eax, ebx
00413202  c1fa1f                 sar      edx, 0x1f
00413205  f7f9                   idiv     ecx
00413207  31c0                   xor      eax, eax
00413209  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
0041320f  0fafd0                 imul     edx, eax
00413212  01ea                   add      edx, ebp
00413214  89d0                   mov      eax, edx
00413216  31db                   xor      ebx, ebx
00413218  05b2110000             add      eax, 0x11b2
0041321d  6689c3                 mov      bx, ax
00413220  8b442408               mov      eax, dword ptr [esp + 8]
00413224  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00413228  01f8                   add      eax, edi
0041322a  89542404               mov      dword ptr [esp + 4], edx
0041322e  0fbfd0                 movsx    edx, ax
00413231  8b442428               mov      eax, dword ptr [esp + 0x28]
00413235  01c8                   add      eax, ecx
00413237  b901000000             mov      ecx, 1
0041323c  98                     cwde
0041323d  e854850400             call     0x45b796 ; PasteOmbreCmp
00413242  8b442404               mov      eax, dword ptr [esp + 4]
00413246  31db                   xor      ebx, ebx
00413248  0552110000             add      eax, 0x1152
0041324d  e96afaffff             jmp      0x412cbc ;
00413252  8b442408               mov      eax, dword ptr [esp + 8]
00413256  01f8                   add      eax, edi
00413258  8b542418               mov      edx, dword ptr [esp + 0x18]
0041325c  0fbfd8                 movsx    ebx, ax
0041325f  8b442428               mov      eax, dword ptr [esp + 0x28]
00413263  01d0                   add      eax, edx
00413265  0fbfd0                 movsx    edx, ax
00413268  31c0                   xor      eax, eax
0041326a  668b44240c             mov      ax, word ptr [esp + 0xc]
0041326f  e829eeffff             call     0x41209d ; AffBallon
00413274  8b442428               mov      eax, dword ptr [esp + 0x28]
00413278  83ef09                 sub      edi, 9
0041327b  e937feffff             jmp      0x4130b7 ;
00413280  31db                   xor      ebx, ebx
00413282  8a9e91000000           mov      bl, byte ptr [esi + 0x91]
00413288  89da                   mov      edx, ebx
0041328a  89d8                   mov      eax, ebx
0041328c  c1fa1f                 sar      edx, 0x1f
0041328f  2bc2                   sub      eax, edx
00413291  d1f8                   sar      eax, 1
00413293  31d2                   xor      edx, edx
00413295  89c1                   mov      ecx, eax
00413297  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041329d  0fafca                 imul     ecx, edx
004132a0  8d53ff                 lea      edx, [ebx - 1]
004132a3  89d0                   mov      eax, edx
004132a5  c1fa1f                 sar      edx, 0x1f
004132a8  2bc2                   sub      eax, edx
004132aa  d1f8                   sar      eax, 1
004132ac  8d2c01                 lea      ebp, [ecx + eax]
004132af  89da                   mov      edx, ebx
004132b1  b902000000             mov      ecx, 2
004132b6  89d8                   mov      eax, ebx
004132b8  c1fa1f                 sar      edx, 0x1f
004132bb  f7f9                   idiv     ecx
004132bd  31c0                   xor      eax, eax
004132bf  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
004132c5  0fafc2                 imul     eax, edx
004132c8  01e8                   add      eax, ebp
004132ca  31db                   xor      ebx, ebx
004132cc  89442404               mov      dword ptr [esp + 4], eax
004132d0  0512110000             add      eax, 0x1112
004132d5  6689c3                 mov      bx, ax
004132d8  8b442408               mov      eax, dword ptr [esp + 8]
004132dc  01f8                   add      eax, edi
004132de  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
004132e2  0fbfd0                 movsx    edx, ax
004132e5  8b442428               mov      eax, dword ptr [esp + 0x28]
004132e9  01c8                   add      eax, ecx
004132eb  b901000000             mov      ecx, 1
004132f0  98                     cwde
004132f1  e8a0840400             call     0x45b796 ; PasteOmbreCmp
004132f6  8b442404               mov      eax, dword ptr [esp + 4]
004132fa  31db                   xor      ebx, ebx
004132fc  05d2100000             add      eax, 0x10d2
00413301  e9b6f9ffff             jmp      0x412cbc ;
00413306  31d2                   xor      edx, edx
00413308  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041330e  42                     inc      edx
0041330f  89d0                   mov      eax, edx
00413311  c1fa1f                 sar      edx, 0x1f
00413314  2bc2                   sub      eax, edx
00413316  d1f8                   sar      eax, 1
00413318  31d2                   xor      edx, edx
0041331a  48                     dec      eax
0041331b  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00413321  0fafd0                 imul     edx, eax
00413324  31c0                   xor      eax, eax
00413326  81c235160000           add      edx, 0x1635
0041332c  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
00413332  31db                   xor      ebx, ebx
00413334  01d0                   add      eax, edx
00413336  6689c3                 mov      bx, ax
00413339  8b442408               mov      eax, dword ptr [esp + 8]
0041333d  01f8                   add      eax, edi
0041333f  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00413343  0fbfd0                 movsx    edx, ax
00413346  8b442428               mov      eax, dword ptr [esp + 0x28]
0041334a  01c8                   add      eax, ecx
0041334c  b901000000             mov      ecx, 1
00413351  98                     cwde
00413352  e83f840400             call     0x45b796 ; PasteOmbreCmp
00413357  31d2                   xor      edx, edx
00413359  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041335f  42                     inc      edx
00413360  89d0                   mov      eax, edx
00413362  c1fa1f                 sar      edx, 0x1f
00413365  2bc2                   sub      eax, edx
00413367  d1f8                   sar      eax, 1
00413369  31d2                   xor      edx, edx
0041336b  48                     dec      eax
0041336c  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
00413372  0fafc2                 imul     eax, edx
00413375  31d2                   xor      edx, edx
00413377  0575150000             add      eax, 0x1575
0041337c  e931f9ffff             jmp      0x412cb2 ;
00413381  31d2                   xor      edx, edx
00413383  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413389  42                     inc      edx
0041338a  89d0                   mov      eax, edx
0041338c  c1fa1f                 sar      edx, 0x1f
0041338f  2bc2                   sub      eax, edx
00413391  d1f8                   sar      eax, 1
00413393  31d2                   xor      edx, edx
00413395  48                     dec      eax
00413396  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041339c  0fafd0                 imul     edx, eax
0041339f  31c0                   xor      eax, eax
004133a1  81c2b5140000           add      edx, 0x14b5
004133a7  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
004133ad  31db                   xor      ebx, ebx
004133af  01d0                   add      eax, edx
004133b1  6689c3                 mov      bx, ax
004133b4  8b442408               mov      eax, dword ptr [esp + 8]
004133b8  01f8                   add      eax, edi
004133ba  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
004133be  0fbfd0                 movsx    edx, ax
004133c1  8b442428               mov      eax, dword ptr [esp + 0x28]
004133c5  01c8                   add      eax, ecx
004133c7  b901000000             mov      ecx, 1
004133cc  98                     cwde
004133cd  e8c4830400             call     0x45b796 ; PasteOmbreCmp
004133d2  31d2                   xor      edx, edx
004133d4  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004133da  42                     inc      edx
004133db  89d0                   mov      eax, edx
004133dd  c1fa1f                 sar      edx, 0x1f
004133e0  2bc2                   sub      eax, edx
004133e2  d1f8                   sar      eax, 1
004133e4  31d2                   xor      edx, edx
004133e6  48                     dec      eax
004133e7  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004133ed  0fafc2                 imul     eax, edx
004133f0  31d2                   xor      edx, edx
004133f2  05f5130000             add      eax, 0x13f5
004133f7  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004133fd  01c2                   add      edx, eax
004133ff  8b442408               mov      eax, dword ptr [esp + 8]
00413403  31db                   xor      ebx, ebx
00413405  01f8                   add      eax, edi
00413407  6689d3                 mov      bx, dx
0041340a  e9b6f8ffff             jmp      0x412cc5 ;
0041340f  31d2                   xor      edx, edx
00413411  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413417  42                     inc      edx
00413418  89d0                   mov      eax, edx
0041341a  c1fa1f                 sar      edx, 0x1f
0041341d  2bc2                   sub      eax, edx
0041341f  d1f8                   sar      eax, 1
00413421  31d2                   xor      edx, edx
00413423  48                     dec      eax
00413424  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041342a  0fafd0                 imul     edx, eax
0041342d  31c0                   xor      eax, eax
0041342f  81c235190000           add      edx, 0x1935
00413435  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
0041343b  31db                   xor      ebx, ebx
0041343d  01d0                   add      eax, edx
0041343f  6689c3                 mov      bx, ax
00413442  8b442408               mov      eax, dword ptr [esp + 8]
00413446  01f8                   add      eax, edi
00413448  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
0041344c  0fbfd0                 movsx    edx, ax
0041344f  8b442428               mov      eax, dword ptr [esp + 0x28]
00413453  01c8                   add      eax, ecx
00413455  b901000000             mov      ecx, 1
0041345a  98                     cwde
0041345b  e836830400             call     0x45b796 ; PasteOmbreCmp
00413460  31d2                   xor      edx, edx
00413462  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413468  42                     inc      edx
00413469  89d0                   mov      eax, edx
0041346b  c1fa1f                 sar      edx, 0x1f
0041346e  2bc2                   sub      eax, edx
00413470  d1f8                   sar      eax, 1
00413472  31d2                   xor      edx, edx
00413474  48                     dec      eax
00413475  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041347b  0fafc2                 imul     eax, edx
0041347e  31d2                   xor      edx, edx
00413480  0575180000             add      eax, 0x1875
00413485  e96dffffff             jmp      0x4133f7 ;
0041348a  31d2                   xor      edx, edx
0041348c  8a9691000000           mov      dl, byte ptr [esi + 0x91]
00413492  42                     inc      edx
00413493  89d0                   mov      eax, edx
00413495  c1fa1f                 sar      edx, 0x1f
00413498  2bc2                   sub      eax, edx
0041349a  d1f8                   sar      eax, 1
0041349c  31d2                   xor      edx, edx
0041349e  48                     dec      eax
0041349f  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004134a5  0fafc2                 imul     eax, edx
004134a8  31d2                   xor      edx, edx
004134aa  05b51a0000             add      eax, 0x1ab5
004134af  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004134b5  31db                   xor      ebx, ebx
004134b7  01d0                   add      eax, edx
004134b9  6689c3                 mov      bx, ax
004134bc  8b442408               mov      eax, dword ptr [esp + 8]
004134c0  01f8                   add      eax, edi
004134c2  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
004134c6  0fbfd0                 movsx    edx, ax
004134c9  8b442428               mov      eax, dword ptr [esp + 0x28]
004134cd  01c8                   add      eax, ecx
004134cf  b901000000             mov      ecx, 1
004134d4  98                     cwde
004134d5  e8bc820400             call     0x45b796 ; PasteOmbreCmp
004134da  31d2                   xor      edx, edx
004134dc  8a9691000000           mov      dl, byte ptr [esi + 0x91]
004134e2  42                     inc      edx
004134e3  89d0                   mov      eax, edx
004134e5  c1fa1f                 sar      edx, 0x1f
004134e8  2bc2                   sub      eax, edx
004134ea  d1f8                   sar      eax, 1
004134ec  31d2                   xor      edx, edx
004134ee  48                     dec      eax
004134ef  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
004134f5  0fafc2                 imul     eax, edx
004134f8  31d2                   xor      edx, edx
004134fa  05f5190000             add      eax, 0x19f5
004134ff  e9aef7ffff             jmp      0x412cb2 ;
00413504  31d2                   xor      edx, edx
00413506  8a9691000000           mov      dl, byte ptr [esi + 0x91]
0041350c  42                     inc      edx
0041350d  89d0                   mov      eax, edx
0041350f  c1fa1f                 sar      edx, 0x1f
00413512  2bc2                   sub      eax, edx
00413514  d1f8                   sar      eax, 1
00413516  31d2                   xor      edx, edx
00413518  48                     dec      eax
00413519  8a96a5000000           mov      dl, byte ptr [esi + 0xa5]
0041351f  0fafd0                 imul     edx, eax
00413522  31c0                   xor      eax, eax
00413524  8a86a4000000           mov      al, byte ptr [esi + 0xa4]
0041352a  01d0                   add      eax, edx
0041352c  31db                   xor      ebx, ebx
0041352e  89442414               mov      dword ptr [esp + 0x14], eax
00413532  05b5170000             add      eax, 0x17b5
00413537  6689c3                 mov      bx, ax
0041353a  8b442408               mov      eax, dword ptr [esp + 8]
0041353e  01f8                   add      eax, edi
00413540  8b4c2418               mov      ecx, dword ptr [esp + 0x18]
00413544  0fbfd0                 movsx    edx, ax
00413547  8b442428               mov      eax, dword ptr [esp + 0x28]
0041354b  01c8                   add      eax, ecx
0041354d  b901000000             mov      ecx, 1
00413552  98                     cwde
00413553  e83e820400             call     0x45b796 ; PasteOmbreCmp
00413558  8b442414               mov      eax, dword ptr [esp + 0x14]
0041355c  31db                   xor      ebx, ebx
0041355e  05f5160000             add      eax, 0x16f5
00413563  e954f7ffff             jmp      0x412cbc ;
00413568  31d2                   xor      edx, edx
0041356a  6689fa                 mov      dx, di
0041356d  89d0                   mov      eax, edx
0041356f  c1e004                 shl      eax, 4
00413572  01d0                   add      eax, edx
00413574  c1e002                 shl      eax, 2
00413577  01d0                   add      eax, edx
00413579  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
0041357f  c1e002                 shl      eax, 2
00413582  01d0                   add      eax, edx
00413584  668b5004               mov      dx, word ptr [eax + 4]
00413588  663b5076               cmp      dx, word ptr [eax + 0x76]
0041358c  7512                   jne      0x4135a0
0041358e  668b4074               mov      ax, word ptr [eax + 0x74]
00413592  25ffff0000             and      eax, 0xffff
00413597  83f864                 cmp      eax, 0x64
0041359a  7d04                   jge      0x4135a0
0041359c  b001                   mov      al, 1
0041359e  eb02                   jmp      0x4135a2 ;
004135a0  30c0                   xor      al, al
004135a2  84c0                   test     al, al
004135a4  0f84ab000000           je       0x413655
004135aa  31d2                   xor      edx, edx
004135ac  668b5674               mov      dx, word ptr [esi + 0x74]
004135b0  bb05000000             mov      ebx, 5
004135b5  89d0                   mov      eax, edx
004135b7  c1fa1f                 sar      edx, 0x1f
004135ba  f7fb                   idiv     ebx
004135bc  89c2                   mov      edx, eax
004135be  bb02000000             mov      ebx, 2
004135c3  c1fa1f                 sar      edx, 0x1f
004135c6  f7fb                   idiv     ebx
004135c8  85d2                   test     edx, edx
004135ca  0f8585000000           jne      0x413655
004135d0  668b54240c             mov      dx, word ptr [esp + 0xc]
004135d5  89d0                   mov      eax, edx
004135d7  c1e004                 shl      eax, 4
004135da  01d0                   add      eax, edx
004135dc  c1e002                 shl      eax, 2
004135df  01d0                   add      eax, edx
004135e1  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
004135e7  c1e002                 shl      eax, 2
004135ea  01c2                   add      edx, eax
004135ec  31c0                   xor      eax, eax
004135ee  8a4201                 mov      al, byte ptr [edx + 1]
004135f1  e83ef60200             call     0x442c34 ; TypeEnginSeFatigue
004135f6  84c0                   test     al, al
004135f8  745b                   je       0x413655
004135fa  8b4c241c               mov      ecx, dword ptr [esp + 0x1c]
004135fe  8b442420               mov      eax, dword ptr [esp + 0x20]
00413602  31db                   xor      ebx, ebx
00413604  83e908                 sub      ecx, 8
00413607  8a1a                   mov      bl, byte ptr [edx]
00413609  83e802                 sub      eax, 2
0041360c  81fbc8000000           cmp      ebx, 0xc8
00413612  7521                   jne      0x413635
00413614  668b5204               mov      dx, word ptr [edx + 4]
00413618  31db                   xor      ebx, ebx
0041361a  81c22b1e0000           add      edx, 0x1e2b
00413620  6689d3                 mov      bx, dx
00413623  0fbfd0                 movsx    edx, ax
00413626  0fbfc1                 movsx    eax, cx
00413629  b901000000             mov      ecx, 1
0041362e  e8147c0400             call     0x45b247 ; PasteBobCmp
00413633  eb20                   jmp      0x413655 ;
00413635  668b5204               mov      dx, word ptr [edx + 4]
00413639  53                     push     ebx
0041363a  81c22b1e0000           add      edx, 0x1e2b
00413640  31db                   xor      ebx, ebx
00413642  6689d3                 mov      bx, dx
00413645  0fbfd0                 movsx    edx, ax
00413648  0fbfc1                 movsx    eax, cx
0041364b  b901000000             mov      ecx, 1
00413650  e8008e0400             call     0x45c455 ; PastePlayerCmp
00413655  80beba00000000         cmp      byte ptr [esi + 0xba], 0
0041365c  0f847a000000           je       0x4136dc
00413662  bb05000000             mov      ebx, 5
00413667  a17c8f5000             mov      eax, dword ptr [0x508f7c]
0041366c  31d2                   xor      edx, edx
0041366e  f7f3                   div      ebx
00413670  85d2                   test     edx, edx
00413672  7568                   jne      0x4136dc
00413674  31db                   xor      ebx, ebx
00413676  668b5c240c             mov      bx, word ptr [esp + 0xc]
0041367b  89d8                   mov      eax, ebx
0041367d  c1e004                 shl      eax, 4
00413680  01d8                   add      eax, ebx
00413682  c1e002                 shl      eax, 2
00413685  01d8                   add      eax, ebx
00413687  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
0041368d  c1e002                 shl      eax, 2
00413690  01c2                   add      edx, eax
00413692  89d8                   mov      eax, ebx
00413694  30ff                   xor      bh, bh
00413696  e80bc30300             call     0x44f9a6 ; EnginGetLevelExperience
0041369b  88c3                   mov      bl, al
0041369d  31c0                   xor      eax, eax
0041369f  8a4201                 mov      al, byte ptr [edx + 1]
004136a2  e809ec0200             call     0x4422b0 ; TypeEnginGagneXP
004136a7  84c0                   test     al, al
004136a9  7431                   je       0x4136dc
004136ab  31c0                   xor      eax, eax
004136ad  6689d8                 mov      ax, bx
004136b0  85c0                   test     eax, eax
004136b2  7428                   je       0x4136dc
004136b4  81c3461e0000           add      ebx, 0x1e46
004136ba  8b442420               mov      eax, dword ptr [esp + 0x20]
004136be  83e802                 sub      eax, 2
004136c1  0fbfd0                 movsx    edx, ax
004136c4  8b44241c               mov      eax, dword ptr [esp + 0x1c]
004136c8  b901000000             mov      ecx, 1
004136cd  83e808                 sub      eax, 8
004136d0  81e3ffff0000           and      ebx, 0xffff
004136d6  98                     cwde
004136d7  e86b7b0400             call     0x45b247 ; PasteBobCmp
004136dc  83c438                 add      esp, 0x38
004136df  5d                     pop      ebp
004136e0  5f                     pop      edi
004136e1  5e                     pop      esi
004136e2  59                     pop      ecx
004136e3  c3                     ret
004136e4  043a                   add      al, 0x3a
004136e6  41                     inc      ecx
004136e7  00583a                 add      byte ptr [eax + 0x3a], bl
004136ea  41                     inc      ecx
004136eb  00c7                   add      bh, al
004136ed  3b4100                 cmp      eax, dword ptr [ecx]
004136f0  a5                     movsd    dword ptr es:[edi], dword ptr [esi]
004136f1  3a4100                 cmp      al, byte ptr [ecx]
004136f4  143c                   adc      al, 0x3c
004136f6  41                     inc      ecx
004136f7  00b8394100b8           add      byte ptr [eax - 0x47ffbec7], bh
004136fd  394100                 cmp      dword ptr [ecx], eax
00413700  b839410029             mov      eax, 0x29004139
00413705  394100                 cmp      dword ptr [ecx], eax
00413708  b8394100b8             mov      eax, 0xb8004139
0041370d  394100                 cmp      dword ptr [ecx], eax
00413710  7f3d                   jg       0x41374f
00413712  41                     inc      ecx
00413713  00f9                   add      cl, bh
00413715  3c41                   cmp      al, 0x41
00413717  00b839410073           add      byte ptr [eax + 0x73004139], bh
0041371d  3f                     aas
0041371e  41                     inc      ecx
0041371f  00f5                   add      ch, dh
00413721  3f                     aas
00413722  41                     inc      ecx
00413723  0001                   add      byte ptr [ecx], al
00413725  3e41                   inc      ecx
00413727  00b8404100b8           add      byte ptr [eax - 0x47ffbec0], bh
0041372d  394100                 cmp      dword ptr [ecx], eax
00413730  b8394100c4             mov      eax, 0xc4004139
00413735  40                     inc      eax
00413736  41                     inc      ecx
00413737  003c41                 add      byte ptr [ecx + eax*2], bh
0041373a  41                     inc      ecx
0041373b  00a4424100b441         add      byte ptr [edx + eax*2 + 0x41b40041], ah
00413742  41                     inc      ecx
00413743  002c42                 add      byte ptr [edx + eax*2], ch
00413746  41                     inc      ecx
00413747  00563b                 add      byte ptr [esi + 0x3b], dl
0041374a  41                     inc      ecx
