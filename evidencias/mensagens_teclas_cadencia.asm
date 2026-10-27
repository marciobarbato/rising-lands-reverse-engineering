; mensagens_teclas_cadencia: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
004181a1  53                    push     ebx
004181a2  83ec40                sub      esp, 0x40
004181a5  8b5c2448              mov      ebx, dword ptr [esp + 0x48]
004181a9  8b44244c              mov      eax, dword ptr [esp + 0x4c]
004181ad  8b542450              mov      edx, dword ptr [esp + 0x50]
004181b1  8b4c2454              mov      ecx, dword ptr [esp + 0x54]
004181b5  3d05010000            cmp      eax, 0x105
004181ba  0f827d030000          jb       0x41853d
004181c0  0f86d3000000          jbe      0x418299
004181c6  3d02020000            cmp      eax, 0x202
004181cb  0f825a030000          jb       0x41852b
004181d1  0f8680000000          jbe      0x418257
004181d7  3d04020000            cmp      eax, 0x204
004181dc  7245                  jb       0x418223
004181de  0f867c000000          jbe      0x418260
004181e4  3d05020000            cmp      eax, 0x205
004181e9  0f847a000000          je       0x418269
004181ef  e989030000            jmp      0x41857d
004181f4  b101                  mov      cl, 1
004181f6  881558a04900          mov      byte ptr [0x49a058], dl
004181fc  880da2054e00          mov      byte ptr [0x4e05a2], cl
00418202  e947000000            jmp      0x41824e
00418207  89c8                  mov      eax, ecx
00418209  c1e810                shr      eax, 0x10
0041820c  25ffff0000            and      eax, 0xffff
00418211  66890da8995000        mov      word ptr [0x5099a8], cx
00418218  66a3aa995000          mov      word ptr [0x5099aa], ax
0041821e  e92b000000            jmp      0x41824e
00418223  31c0                  xor      eax, eax
00418225  31d2                  xor      edx, edx
00418227  66a126875000          mov      ax, word ptr [0x508726]
0041822d  668b15aa995000        mov      dx, word ptr [0x5099aa]
00418234  c1e005                shl      eax, 5
00418237  39c2                  cmp      edx, eax
00418239  7d0c                  jge      0x418247
0041823b  c605b099500001        mov      byte ptr [0x5099b0], 1
00418242  e907000000            jmp      0x41824e
00418247  c605ae99500001        mov      byte ptr [0x5099ae], 1
0041824e  31c0                  xor      eax, eax
00418250  83c440                add      esp, 0x40
00418253  5b                    pop      ebx
00418254  c21000                ret      0x10
00418257  c605af99500001        mov      byte ptr [0x5099af], 1
0041825e  ebee                  jmp      0x41824e
00418260  c605b199500001        mov      byte ptr [0x5099b1], 1
00418267  ebe5                  jmp      0x41824e
00418269  c605b299500001        mov      byte ptr [0x5099b2], 1
00418270  ebdc                  jmp      0x41824e
00418272  89e0                  mov      eax, esp
00418274  50                    push     eax
00418275  53                    push     ebx
00418276  2eff1578325200        call     dword ptr cs:[0x523278] ; USER32.dll!BeginPaint
0041827d  89e0                  mov      eax, esp
0041827f  50                    push     eax
00418280  53                    push     ebx
00418281  2eff1588325200        call     dword ptr cs:[0x523288] ; USER32.dll!EndPaint
00418288  ebc4                  jmp      0x41824e
0041828a  30ed                  xor      ch, ch
0041828c  e8906b0200            call     0x43ee21
00418291  882d58a04900          mov      byte ptr [0x49a058], ch
00418297  ebb5                  jmp      0x41824e
00418299  83fa09                cmp      edx, 9
0041829c  74ec                  je       0x41828a
0041829e  ebae                  jmp      0x41824e
004182a0  b901000000            mov      ecx, 1
004182a5  8a2585724900          mov      ah, byte ptr [0x497285]
004182ab  31db                  xor      ebx, ebx
004182ad  84e4                  test     ah, ah
004182af  0f94c0                sete     al
004182b2  31d2                  xor      edx, edx
004182b4  a285724900            mov      byte ptr [0x497285], al
004182b9  89c8                  mov      eax, ecx
004182bb  e870950500            call     0x471830
004182c0  eb8c                  jmp      0x41824e
004182c2  e8e9400100            call     0x42c3b0
004182c7  84c0                  test     al, al
004182c9  7583                  jne      0x41824e
004182cb  31d2                  xor      edx, edx
004182cd  8a155ba04900          mov      dl, byte ptr [0x49a05b]
004182d3  42                    inc      edx
004182d4  bb04000000            mov      ebx, 4
004182d9  89d0                  mov      eax, edx
004182db  c1fa1f                sar      edx, 0x1f
004182de  f7fb                  idiv     ebx
004182e0  88155ba04900          mov      byte ptr [0x49a05b], dl
004182e6  e963ffffff            jmp      0x41824e
004182eb  83fa74                cmp      edx, 0x74
004182ee  7207                  jb       0x4182f7
004182f0  76d0                  jbe      0x4182c2
004182f2  e957ffffff            jmp      0x41824e
004182f7  83fa09                cmp      edx, 9
004182fa  74a4                  je       0x4182a0
004182fc  e94dffffff            jmp      0x41824e
00418301  803d782f4e0012        cmp      byte ptr [0x4e2f78], 0x12
00418308  0f84b0010000          je       0x4184be
0041830e  e93bffffff            jmp      0x41824e
00418313  80ea30                sub      dl, 0x30
00418316  88155aa04900          mov      byte ptr [0x49a05a], dl
0041831c  e92dffffff            jmp      0x41824e
00418321  c6058472490001        mov      byte ptr [0x497284], 1
00418328  e921ffffff            jmp      0x41824e
0041832d  c6058472490002        mov      byte ptr [0x497284], 2
00418334  e915ffffff            jmp      0x41824e
00418339  c6058472490003        mov      byte ptr [0x497284], 3
00418340  e909ffffff            jmp      0x41824e
00418345  c6058472490004        mov      byte ptr [0x497284], 4
0041834c  e9fdfeffff            jmp      0x41824e
00418351  a18d8f5000            mov      eax, dword ptr [0x508f8d]
00418356  c1f818                sar      eax, 0x18
00418359  85c0                  test     eax, eax
0041835b  0f8eedfeffff          jle      0x41824e
00418361  31c0                  xor      eax, eax
00418363  66a118a04900          mov      ax, word ptr [0x49a018]
00418369  3d20030000            cmp      eax, 0x320
0041836e  0f85dafeffff          jne      0x41824e
00418374  b801000000            mov      eax, 1
00418379  8a3d908f5000          mov      bh, byte ptr [0x508f90]
0041837f  31c9                  xor      ecx, ecx
00418381  fecf                  dec      bh
00418383  31d2                  xor      edx, edx
00418385  883d908f5000          mov      byte ptr [0x508f90], bh
0041838b  883d918f5000          mov      byte ptr [0x508f91], bh
00418391  31db                  xor      ebx, ebx
00418393  e898940500            call     0x471830
00418398  668b1526875000        mov      dx, word ptr [0x508726]
0041839f  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
004183a7  c1e205                shl      edx, 5
004183aa  c1e005                shl      eax, 5
004183ad  4a                    dec      edx
004183ae  31c9                  xor      ecx, ecx
004183b0  29c2                  sub      edx, eax
004183b2  6689d1                mov      cx, dx
004183b5  668b1524875000        mov      dx, word ptr [0x508724]
004183bc  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
004183c4  c1e205                shl      edx, 5
004183c7  c1e005                shl      eax, 5
004183ca  4a                    dec      edx
004183cb  31db                  xor      ebx, ebx
004183cd  29c2                  sub      edx, eax
004183cf  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
004183d7  6689d3                mov      bx, dx
004183da  c1e005                shl      eax, 5
004183dd  31d2                  xor      edx, edx
004183df  6689c2                mov      dx, ax
004183e2  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
004183ea  c1e005                shl      eax, 5
004183ed  25ffff0000            and      eax, 0xffff
004183f2  e82271ffff            call     0x40f519
004183f7  e952feffff            jmp      0x41824e
004183fc  a18d8f5000            mov      eax, dword ptr [0x508f8d]
00418401  c1f818                sar      eax, 0x18
00418404  83f803                cmp      eax, 3
00418407  0f8d41feffff          jge      0x41824e
0041840d  31c0                  xor      eax, eax
0041840f  66a118a04900          mov      ax, word ptr [0x49a018]
00418415  3d20030000            cmp      eax, 0x320
0041841a  0f852efeffff          jne      0x41824e
00418420  b601                  mov      dh, 1
00418422  8a1d908f5000          mov      bl, byte ptr [0x508f90]
00418428  31c9                  xor      ecx, ecx
0041842a  00f3                  add      bl, dh
0041842c  8835928f5000          mov      byte ptr [0x508f92], dh
00418432  881d908f5000          mov      byte ptr [0x508f90], bl
00418438  881d918f5000          mov      byte ptr [0x508f91], bl
0041843e  e8d81b0500            call     0x46a01b
00418443  31d2                  xor      edx, edx
00418445  b801000000            mov      eax, 1
0041844a  31db                  xor      ebx, ebx
0041844c  e8df930500            call     0x471830
00418451  66a126875000          mov      ax, word ptr [0x508726]
00418457  660fbe15908f5000      movsx    dx, byte ptr [0x508f90]
0041845f  c1e005                shl      eax, 5
00418462  c1e205                shl      edx, 5
00418465  48                    dec      eax
00418466  31c9                  xor      ecx, ecx
00418468  29d0                  sub      eax, edx
0041846a  668b1524875000        mov      dx, word ptr [0x508724]
00418471  6689c1                mov      cx, ax
00418474  c1e205                shl      edx, 5
00418477  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
0041847f  4a                    dec      edx
00418480  c1e005                shl      eax, 5
00418483  e943ffffff            jmp      0x4183cb
00418488  31d0                  xor      eax, edx
0041848a  66a118a04900          mov      ax, word ptr [0x49a018]
00418490  3d80020000            cmp      eax, 0x280
00418495  7509                  jne      0x4184a0
00418497  ba01000000            mov      edx, 1
0041849c  89d8                  mov      eax, ebx
0041849e  eb04                  jmp      0x4184a4
004184a0  89d8                  mov      eax, ebx
004184a2  31d2                  xor      edx, edx
004184a4  e89c71ffff            call     0x40f645
004184a9  e86d1b0500            call     0x46a01b
004184ae  b801000000            mov      eax, 1
004184b3  31c9                  xor      ecx, ecx
004184b5  31db                  xor      ebx, ebx
004184b7  31d2                  xor      edx, edx
004184b9  e9fdfdffff            jmp      0x4182bb
004184be  89d0                  mov      eax, edx
004184c0  83fa70                cmp      edx, 0x70
004184c3  7228                  jb       0x4184ed
004184c5  0f8656feffff          jbe      0x418321
004184cb  83fa72                cmp      edx, 0x72
004184ce  0f8259feffff          jb       0x41832d
004184d4  0f865ffeffff          jbe      0x418339
004184da  83fa73                cmp      edx, 0x73
004184dd  0f8662feffff          jbe      0x418345
004184e3  83fa7a                cmp      edx, 0x7a
004184e6  74a0                  je       0x418488
004184e8  e961fdffff            jmp      0x41824e
004184ed  83fa6b                cmp      edx, 0x6b
004184f0  7214                  jb       0x418506
004184f2  0f8659feffff          jbe      0x418351
004184f8  83fa6d                cmp      edx, 0x6d
004184fb  0f84fbfeffff          je       0x4183fc
00418501  e948fdffff            jmp      0x41824e
00418506  83fa31                cmp      edx, 0x31
00418509  0f823ffdffff          jb       0x41824e
0041850f  83fa39                cmp      edx, 0x39
00418512  0f86fbfdffff          jbe      0x418313
00418518  e931fdffff            jmp      0x41824e
0041851d  6a00                  push     0
0041851f  2eff15bc325200        call     dword ptr cs:[0x5232bc] ; USER32.dll!PostQuitMessage
00418526  e923fdffff            jmp      0x41824e
0041852b  3d00020000            cmp      eax, 0x200
00418530  724b                  jb       0x41857d
00418532  0f86cffcffff          jbe      0x418207
00418538  e90afdffff            jmp      0x418247
0041853d  83f814                cmp      eax, 0x14
00418540  722b                  jb       0x41856d
00418542  0f8606fdffff          jbe      0x41824e
00418548  3d00010000            cmp      eax, 0x100
0041854d  7213                  jb       0x418562
0041854f  0f86acfdffff          jbe      0x418301
00418555  3d01010000            cmp      eax, 0x101
0041855a  0f848bfdffff          je       0x4182eb
00418560  eb1b                  jmp      0x41857d
00418562  83f81c                cmp      eax, 0x1c
00418565  0f8489fcffff          je       0x4181f4
0041856b  eb10                  jmp      0x41857d
0041856d  83f802                cmp      eax, 2
00418570  720b                  jb       0x41857d
00418572  76a9                  jbe      0x41851d
00418574  83f80f                cmp      eax, 0xf
00418577  0f84f5fcffff          je       0x418272
0041857d  51                    push     ecx
0041857e  52                    push     edx
0041857f  50                    push     eax
00418580  53                    push     ebx
00418581  2eff1580325200        call     dword ptr cs:[0x523280] ; USER32.dll!DefWindowProcA
00418588  e9c3fcffff            jmp      0x418250
