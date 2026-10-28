; AffSprite [0x416864, 0x416e41)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00416864  53                     push     ebx
00416865  51                     push     ecx
00416866  56                     push     esi
00416867  57                     push     edi
00416868  55                     push     ebp
00416869  81ec40070000           sub      esp, 0x740
0041686f  50                     push     eax
00416870  52                     push     edx
00416871  bd00010000             mov      ebp, 0x100
00416876  31f6                   xor      esi, esi
00416878  31c9                   xor      ecx, ecx
0041687a  eb01                   jmp      0x41687d ;
0041687c  41                     inc      ecx
0041687d  0fbfd1                 movsx    edx, cx
00416880  81fa20030000           cmp      edx, 0x320
00416886  0f8dba000000           jge      0x416946
0041688c  31c0                   xor      eax, eax
0041688e  6689c8                 mov      ax, cx
00416891  e869b70200             call     0x441fff ; ExisteEngin
00416896  84c0                   test     al, al
00416898  74e2                   je       0x41687c
0041689a  69c214010000           imul     eax, edx, 0x114
004168a0  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
004168a6  31db                   xor      ebx, ebx
004168a8  668b440208             mov      ax, word ptr [edx + eax + 8]
004168ad  31d2                   xor      edx, edx
004168af  6689c3                 mov      bx, ax
004168b2  8a1541805000           mov      dl, byte ptr [0x508041]
004168b8  89d8                   mov      eax, ebx
004168ba  e831fe0500             call     0x4766f0 ; TerrainEstDecouvert
004168bf  84c0                   test     al, al
004168c1  74b9                   je       0x41687c
004168c3  31d2                   xor      edx, edx
004168c5  89d8                   mov      eax, ebx
004168c7  8a1541805000           mov      dl, byte ptr [0x508041]
004168cd  e868000600             call     0x47693a ; CaseEstIlluminee
004168d2  84c0                   test     al, al
004168d4  74a6                   je       0x41687c
004168d6  89da                   mov      edx, ebx
004168d8  89d8                   mov      eax, ebx
004168da  c1fa1f                 sar      edx, 0x1f
004168dd  f7fd                   idiv     ebp
004168df  89d7                   mov      edi, edx
004168e1  89da                   mov      edx, ebx
004168e3  89d8                   mov      eax, ebx
004168e5  c1fa1f                 sar      edx, 0x1f
004168e8  f7fd                   idiv     ebp
004168ea  8b5c2404               mov      ebx, dword ptr [esp + 4]
004168ee  6639df                 cmp      di, bx
004168f1  7c89                   jl       0x41687c
004168f3  663b0424               cmp      ax, word ptr [esp]
004168f7  7c83                   jl       0x41687c
004168f9  31d2                   xor      edx, edx
004168fb  6689da                 mov      dx, bx
004168fe  31db                   xor      ebx, ebx
00416900  668b1d24875000         mov      bx, word ptr [0x508724]
00416907  01da                   add      edx, ebx
00416909  0fbfdf                 movsx    ebx, di
0041690c  83c202                 add      edx, 2
0041690f  39d3                   cmp      ebx, edx
00416911  0f8d65ffffff           jge      0x41687c
00416917  31d2                   xor      edx, edx
00416919  31db                   xor      ebx, ebx
0041691b  668b1424               mov      dx, word ptr [esp]
0041691f  668b1d26875000         mov      bx, word ptr [0x508726]
00416926  01d3                   add      ebx, edx
00416928  0fbfd0                 movsx    edx, ax
0041692b  8d430a                 lea      eax, [ebx + 0xa]
0041692e  39c2                   cmp      edx, eax
00416930  0f8d46ffffff           jge      0x41687c
00416936  31c0                   xor      eax, eax
00416938  6689f0                 mov      ax, si
0041693b  46                     inc      esi
0041693c  66894c4408             mov      word ptr [esp + eax*2 + 8], cx
00416941  e936ffffff             jmp      0x41687c ;
00416946  31d2                   xor      edx, edx
00416948  6689942430070000       mov      word ptr [esp + 0x730], dx
00416950  eb2b                   jmp      0x41697d ;
00416952  31d2                   xor      edx, edx
00416954  8b84242e070000         mov      eax, dword ptr [esp + 0x72e]
0041695b  6689fa                 mov      dx, di
0041695e  c1f810                 sar      eax, 0x10
00416961  668b4c5408             mov      cx, word ptr [esp + edx*2 + 8]
00416966  668b5c4408             mov      bx, word ptr [esp + eax*2 + 8]
0041696b  66894c4408             mov      word ptr [esp + eax*2 + 8], cx
00416970  66895c5408             mov      word ptr [esp + edx*2 + 8], bx
00416975  66ff842430070000       inc      word ptr [esp + 0x730]
0041697d  8b84242e070000         mov      eax, dword ptr [esp + 0x72e]
00416984  31d2                   xor      edx, edx
00416986  c1f810                 sar      eax, 0x10
00416989  6689f2                 mov      dx, si
0041698c  39d0                   cmp      eax, edx
0041698e  0f8dd8000000           jge      0x416a6c
00416994  31db                   xor      ebx, ebx
00416996  668b5c4408             mov      bx, word ptr [esp + eax*2 + 8]
0041699b  69db14010000           imul     ebx, ebx, 0x114
004169a1  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
004169a6  8bbc2430070000         mov      edi, dword ptr [esp + 0x730]
004169ad  668b5c0308             mov      bx, word ptr [ebx + eax + 8]
004169b2  89f8                   mov      eax, edi
004169b4  40                     inc      eax
004169b5  6639f0                 cmp      ax, si
004169b8  7398                   jae      0x416952
004169ba  31d2                   xor      edx, edx
004169bc  6689c2                 mov      dx, ax
004169bf  0fb76c5408             movzx    ebp, word ptr [esp + edx*2 + 8]
004169c4  69ed14010000           imul     ebp, ebp, 0x114
004169ca  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
004169d0  01ea                   add      edx, ebp
004169d2  668b4a08               mov      cx, word ptr [edx + 8]
004169d6  6639cb                 cmp      bx, cx
004169d9  7710                   ja       0x4169eb
004169db  762f                   jbe      0x416a0c
004169dd  8a5202                 mov      dl, byte ptr [edx + 2]
004169e0  81e2ff000000           and      edx, 0xff
004169e6  83fa04                 cmp      edx, 4
004169e9  7521                   jne      0x416a0c
004169eb  31d2                   xor      edx, edx
004169ed  6689c2                 mov      dx, ax
004169f0  31db                   xor      ebx, ebx
004169f2  668b5c5408             mov      bx, word ptr [esp + edx*2 + 8]
004169f7  69db14010000           imul     ebx, ebx, 0x114
004169fd  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00416a03  89c7                   mov      edi, eax
00416a05  668b5c1a08             mov      bx, word ptr [edx + ebx + 8]
00416a0a  eba8                   jmp      0x4169b4 ;
00416a0c  31d2                   xor      edx, edx
00416a0e  6689c2                 mov      dx, ax
00416a11  668b545408             mov      dx, word ptr [esp + edx*2 + 8]
00416a16  81e2ffff0000           and      edx, 0xffff
00416a1c  69d214010000           imul     edx, edx, 0x114
00416a22  8b2da0194e00           mov      ebp, dword ptr [0x4e19a0]
00416a28  01ea                   add      edx, ebp
00416a2a  668b4a08               mov      cx, word ptr [edx + 8]
00416a2e  89ac2418070000         mov      dword ptr [esp + 0x718], ebp
00416a35  6639cb                 cmp      bx, cx
00416a38  0f8576ffffff           jne      0x4169b4
00416a3e  0fb7ef                 movzx    ebp, di
00416a41  0fb76c6c08             movzx    ebp, word ptr [esp + ebp*2 + 8]
00416a46  69ed14010000           imul     ebp, ebp, 0x114
00416a4c  03ac2418070000         add      ebp, dword ptr [esp + 0x718]
00416a53  8a92ab000000           mov      dl, byte ptr [edx + 0xab]
00416a59  3a95ab000000           cmp      dl, byte ptr [ebp + 0xab]
00416a5f  0f834fffffff           jae      0x4169b4
00416a65  89c7                   mov      edi, eax
00416a67  e948ffffff             jmp      0x4169b4 ;
00416a6c  8d842448060000         lea      eax, [esp + 0x648]
00416a73  8b3c24                 mov      edi, dword ptr [esp]
00416a76  8b5c2404               mov      ebx, dword ptr [esp + 4]
00416a7a  e80c920500             call     0x46fc8b ; ProjectileTrierAffichage
00416a7f  31c9                   xor      ecx, ecx
00416a81  89842434070000         mov      dword ptr [esp + 0x734], eax
00416a88  c1e708                 shl      edi, 8
00416a8b  66898c243c070000       mov      word ptr [esp + 0x73c], cx
00416a93  8b0424                 mov      eax, dword ptr [esp]
00416a96  01df                   add      edi, ebx
00416a98  eb2e                   jmp      0x416ac8 ;
00416a9a  8b9c243c070000         mov      ebx, dword ptr [esp + 0x73c]
00416aa1  66a124875000           mov      ax, word ptr [0x508724]
00416aa7  ba00010000             mov      edx, 0x100
00416aac  0508000000             add      eax, 8
00416ab1  83c320                 add      ebx, 0x20
00416ab4  29c2                   sub      edx, eax
00416ab6  8b84242c070000         mov      eax, dword ptr [esp + 0x72c]
00416abd  66899c243c070000       mov      word ptr [esp + 0x73c], bx
00416ac5  40                     inc      eax
00416ac6  01d7                   add      edi, edx
00416ac8  8984242c070000         mov      dword ptr [esp + 0x72c], eax
00416acf  31d2                   xor      edx, edx
00416ad1  31c0                   xor      eax, eax
00416ad3  668b1424               mov      dx, word ptr [esp]
00416ad7  66a126875000           mov      ax, word ptr [0x508726]
00416add  01d0                   add      eax, edx
00416adf  31d2                   xor      edx, edx
00416ae1  83c005                 add      eax, 5
00416ae4  668b94242c070000       mov      dx, word ptr [esp + 0x72c]
00416aec  39c2                   cmp      edx, eax
00416aee  0f8d70010000           jge      0x416c64
00416af4  31d2                   xor      edx, edx
00416af6  8b442404               mov      eax, dword ptr [esp + 4]
00416afa  6689942428070000       mov      word ptr [esp + 0x728], dx
00416b02  89842420070000         mov      dword ptr [esp + 0x720], eax
00416b09  eb22                   jmp      0x416b2d ;
00416b0b  8b942428070000         mov      edx, dword ptr [esp + 0x728]
00416b12  8b9c2420070000         mov      ebx, dword ptr [esp + 0x720]
00416b19  47                     inc      edi
00416b1a  83c220                 add      edx, 0x20
00416b1d  43                     inc      ebx
00416b1e  6689942428070000       mov      word ptr [esp + 0x728], dx
00416b26  899c2420070000         mov      dword ptr [esp + 0x720], ebx
00416b2d  31d2                   xor      edx, edx
00416b2f  31c0                   xor      eax, eax
00416b31  668b542404             mov      dx, word ptr [esp + 4]
00416b36  66a124875000           mov      ax, word ptr [0x508724]
00416b3c  01d0                   add      eax, edx
00416b3e  31d2                   xor      edx, edx
00416b40  83c008                 add      eax, 8
00416b43  668b942420070000       mov      dx, word ptr [esp + 0x720]
00416b4b  39c2                   cmp      edx, eax
00416b4d  0f8d47ffffff           jge      0x416a9a
00416b53  31db                   xor      ebx, ebx
00416b55  a1747d5000             mov      eax, dword ptr [0x507d74]
00416b5a  6689fb                 mov      bx, di
00416b5d  803c0300               cmp      byte ptr [ebx + eax], 0
00416b61  742c                   je       0x416b8f
00416b63  31d2                   xor      edx, edx
00416b65  89d8                   mov      eax, ebx
00416b67  8a1541805000           mov      dl, byte ptr [0x508041]
00416b6d  e87efb0500             call     0x4766f0 ; TerrainEstDecouvert
00416b72  84c0                   test     al, al
00416b74  7419                   je       0x416b8f
00416b76  8b94243a070000         mov      edx, dword ptr [esp + 0x73a]
00416b7d  8b842426070000         mov      eax, dword ptr [esp + 0x726]
00416b84  c1fa10                 sar      edx, 0x10
00416b87  c1f810                 sar      eax, 0x10
00416b8a  e840efffff             call     0x415acf ; AffVeget
00416b8f  8b84243a070000         mov      eax, dword ptr [esp + 0x73a]
00416b96  c1f810                 sar      eax, 0x10
00416b99  0fb7ef                 movzx    ebp, di
00416b9c  89842410070000         mov      dword ptr [esp + 0x710], eax
00416ba3  8b842426070000         mov      eax, dword ptr [esp + 0x726]
00416baa  89eb                   mov      ebx, ebp
00416bac  c1f810                 sar      eax, 0x10
00416baf  8b942410070000         mov      edx, dword ptr [esp + 0x710]
00416bb6  89842414070000         mov      dword ptr [esp + 0x714], eax
00416bbd  e81112ffff             call     0x407dd3 ; AffBatiments
00416bc2  8b942410070000         mov      edx, dword ptr [esp + 0x710]
00416bc9  8b842414070000         mov      eax, dword ptr [esp + 0x714]
00416bd0  89eb                   mov      ebx, ebp
00416bd2  e8c488ffff             call     0x40f49b ; AffBatimentOmbre
00416bd7  31d2                   xor      edx, edx
00416bd9  0fbfc1                 movsx    eax, cx
00416bdc  6689f2                 mov      dx, si
00416bdf  39d0                   cmp      eax, edx
00416be1  7d27                   jge      0x416c0a
00416be3  668b444408             mov      ax, word ptr [esp + eax*2 + 8]
00416be8  25ffff0000             and      eax, 0xffff
00416bed  69c014010000           imul     eax, eax, 0x114
00416bf3  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00416bf9  8a8402ab000000         mov      al, byte ptr [edx + eax + 0xab]
00416c00  25ff000000             and      eax, 0xff
00416c05  7403                   je       0x416c0a
00416c07  41                     inc      ecx
00416c08  ebcd                   jmp      0x416bd7 ;
00416c0a  31c0                   xor      eax, eax
00416c0c  0fbfd1                 movsx    edx, cx
00416c0f  6689f0                 mov      ax, si
00416c12  39c2                   cmp      edx, eax
00416c14  0f8df1feffff           jge      0x416b0b
00416c1a  31db                   xor      ebx, ebx
00416c1c  668b5c5408             mov      bx, word ptr [esp + edx*2 + 8]
00416c21  69d314010000           imul     edx, ebx, 0x114
00416c27  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00416c2c  01c2                   add      edx, eax
00416c2e  663b7a08               cmp      di, word ptr [edx + 8]
00416c32  0f85d3feffff           jne      0x416b0b
00416c38  31c0                   xor      eax, eax
00416c3a  8a82ab000000           mov      al, byte ptr [edx + 0xab]
00416c40  85c0                   test     eax, eax
00416c42  0f85c3feffff           jne      0x416b0b
00416c48  8b94243a070000         mov      edx, dword ptr [esp + 0x73a]
00416c4f  8b842426070000         mov      eax, dword ptr [esp + 0x726]
00416c56  c1fa10                 sar      edx, 0x10
00416c59  c1f810                 sar      eax, 0x10
00416c5c  41                     inc      ecx
00416c5d  e8bdecffff             call     0x41591f ; AffEngin
00416c62  eba6                   jmp      0x416c0a ;
00416c64  8b0424                 mov      eax, dword ptr [esp]
00416c67  8b542404               mov      edx, dword ptr [esp + 4]
00416c6b  31c9                   xor      ecx, ecx
00416c6d  31ff                   xor      edi, edi
00416c6f  c1e008                 shl      eax, 8
00416c72  66898c2424070000       mov      word ptr [esp + 0x724], cx
00416c7a  01c2                   add      edx, eax
00416c7c  8b0424                 mov      eax, dword ptr [esp]
00416c7f  89942444070000         mov      dword ptr [esp + 0x744], edx
00416c86  eb3c                   jmp      0x416cc4 ;
00416c88  8b942424070000         mov      edx, dword ptr [esp + 0x724]
00416c8f  66a124875000           mov      ax, word ptr [0x508724]
00416c95  83c220                 add      edx, 0x20
00416c98  0508000000             add      eax, 8
00416c9d  6689942424070000       mov      word ptr [esp + 0x724], dx
00416ca5  ba00010000             mov      edx, 0x100
00416caa  8b9c2444070000         mov      ebx, dword ptr [esp + 0x744]
00416cb1  29c2                   sub      edx, eax
00416cb3  8b84241c070000         mov      eax, dword ptr [esp + 0x71c]
00416cba  01d3                   add      ebx, edx
00416cbc  40                     inc      eax
00416cbd  899c2444070000         mov      dword ptr [esp + 0x744], ebx
00416cc4  8984241c070000         mov      dword ptr [esp + 0x71c], eax
00416ccb  31c0                   xor      eax, eax
00416ccd  31d2                   xor      edx, edx
00416ccf  668b0424               mov      ax, word ptr [esp]
00416cd3  668b1526875000         mov      dx, word ptr [0x508726]
00416cda  01d0                   add      eax, edx
00416cdc  31d2                   xor      edx, edx
00416cde  83c00a                 add      eax, 0xa
00416ce1  668b94241c070000       mov      dx, word ptr [esp + 0x71c]
00416ce9  39c2                   cmp      edx, eax
00416ceb  0f8d45010000           jge      0x416e36
00416cf1  31c0                   xor      eax, eax
00416cf3  6689842438070000       mov      word ptr [esp + 0x738], ax
00416cfb  8b442404               mov      eax, dword ptr [esp + 4]
00416cff  89842440070000         mov      dword ptr [esp + 0x740], eax
00416d06  eb32                   jmp      0x416d3a ;
00416d08  8b842438070000         mov      eax, dword ptr [esp + 0x738]
00416d0f  8b942444070000         mov      edx, dword ptr [esp + 0x744]
00416d16  8b9c2440070000         mov      ebx, dword ptr [esp + 0x740]
00416d1d  0520000000             add      eax, 0x20
00416d22  42                     inc      edx
00416d23  43                     inc      ebx
00416d24  6689842438070000       mov      word ptr [esp + 0x738], ax
00416d2c  89942444070000         mov      dword ptr [esp + 0x744], edx
00416d33  899c2440070000         mov      dword ptr [esp + 0x740], ebx
00416d3a  31c0                   xor      eax, eax
00416d3c  31d2                   xor      edx, edx
00416d3e  668b442404             mov      ax, word ptr [esp + 4]
00416d43  668b1524875000         mov      dx, word ptr [0x508724]
00416d4a  01d0                   add      eax, edx
00416d4c  31d2                   xor      edx, edx
00416d4e  83c008                 add      eax, 8
00416d51  668b942440070000       mov      dx, word ptr [esp + 0x740]
00416d59  39c2                   cmp      edx, eax
00416d5b  0f8d27ffffff           jge      0x416c88
00416d61  8b9c2444070000         mov      ebx, dword ptr [esp + 0x744]
00416d68  31c0                   xor      eax, eax
00416d6a  0fbfd7                 movsx    edx, di
00416d6d  668b842434070000       mov      ax, word ptr [esp + 0x734]
00416d75  39c2                   cmp      edx, eax
00416d77  7d28                   jge      0x416da1
00416d79  01d2                   add      edx, edx
00416d7b  31c0                   xor      eax, eax
00416d7d  668b841448060000       mov      ax, word ptr [esp + edx + 0x648]
00416d85  e810910500             call     0x46fe9a ; ProjectileGetCase
00416d8a  6639d8                 cmp      ax, bx
00416d8d  7512                   jne      0x416da1
00416d8f  31c0                   xor      eax, eax
00416d91  668b841448060000       mov      ax, word ptr [esp + edx + 0x648]
00416d99  47                     inc      edi
00416d9a  e8d1910500             call     0x46ff70 ; AffProjectile
00416d9f  ebc7                   jmp      0x416d68 ;
00416da1  31c0                   xor      eax, eax
00416da3  0fbfd1                 movsx    edx, cx
00416da6  6689f0                 mov      ax, si
00416da9  39c2                   cmp      edx, eax
00416dab  7d23                   jge      0x416dd0
00416dad  31c0                   xor      eax, eax
00416daf  668b445408             mov      ax, word ptr [esp + edx*2 + 8]
00416db4  69d014010000           imul     edx, eax, 0x114
00416dba  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00416dbf  8a8402ab000000         mov      al, byte ptr [edx + eax + 0xab]
00416dc6  25ff000000             and      eax, 0xff
00416dcb  7503                   jne      0x416dd0
00416dcd  41                     inc      ecx
00416dce  ebd1                   jmp      0x416da1 ;
00416dd0  31c0                   xor      eax, eax
00416dd2  0fbfd9                 movsx    ebx, cx
00416dd5  6689f0                 mov      ax, si
00416dd8  39c3                   cmp      ebx, eax
00416dda  0f8d28ffffff           jge      0x416d08
00416de0  668b5c5c08             mov      bx, word ptr [esp + ebx*2 + 8]
00416de5  81e3ffff0000           and      ebx, 0xffff
00416deb  69d314010000           imul     edx, ebx, 0x114
00416df1  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
00416df6  01c2                   add      edx, eax
00416df8  668b4208               mov      ax, word ptr [edx + 8]
00416dfc  663b842444070000       cmp      ax, word ptr [esp + 0x744]
00416e04  0f85fefeffff           jne      0x416d08
00416e0a  31c0                   xor      eax, eax
00416e0c  8a82ab000000           mov      al, byte ptr [edx + 0xab]
00416e12  85c0                   test     eax, eax
00416e14  0f84eefeffff           je       0x416d08
00416e1a  8b942422070000         mov      edx, dword ptr [esp + 0x722]
00416e21  8b842436070000         mov      eax, dword ptr [esp + 0x736]
00416e28  c1fa10                 sar      edx, 0x10
00416e2b  c1f810                 sar      eax, 0x10
00416e2e  41                     inc      ecx
00416e2f  e8ebeaffff             call     0x41591f ; AffEngin
00416e34  eb9a                   jmp      0x416dd0 ;
00416e36  81c448070000           add      esp, 0x748
00416e3c  e9379affff             jmp      0x410878 ;
