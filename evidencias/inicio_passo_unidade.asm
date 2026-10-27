; inicio_passo_unidade: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00448704  53                    push     ebx
00448705  51                    push     ecx
00448706  56                    push     esi
00448707  57                    push     edi
00448708  55                    push     ebp
00448709  83ec08                sub      esp, 8
0044870c  89c7                  mov      edi, eax
0044870e  31db                  xor      ebx, ebx
00448710  6689c3                mov      bx, ax
00448713  89d9                  mov      ecx, ebx
00448715  c1e104                shl      ecx, 4
00448718  01d9                  add      ecx, ebx
0044871a  c1e102                shl      ecx, 2
0044871d  01d9                  add      ecx, ebx
0044871f  8b35a0194e00          mov      esi, dword ptr [0x4e19a0]
00448725  c1e102                shl      ecx, 2
00448728  01ce                  add      esi, ecx
0044872a  8a8e90000000          mov      cl, byte ptr [esi + 0x90]
00448730  80f907                cmp      cl, 7
00448733  0f8231010000          jb       0x44886a
00448739  0f8693000000          jbe      0x4487d2
0044873f  80f90b                cmp      cl, 0xb
00448742  0f821b010000          jb       0x448863
00448748  0f86ba000000          jbe      0x448808
0044874e  80f90d                cmp      cl, 0xd
00448751  0f8232010000          jb       0x448889
00448757  0f86d6000000          jbe      0x448833
0044875d  80f90f                cmp      cl, 0xf
00448760  0f84df000000          je       0x448845
00448766  e91e010000            jmp      0x448889
0044876b  8a8698000000          mov      al, byte ptr [esi + 0x98]
00448771  8aae86000000          mov      ch, byte ptr [esi + 0x86]
00448777  28d0                  sub      al, dl
00448779  28c5                  sub      ch, al
0044877b  88ae86000000          mov      byte ptr [esi + 0x86], ch
00448781  e903010000            jmp      0x448889
00448786  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044878c  8abe86000000          mov      bh, byte ptr [esi + 0x86]
00448792  28d0                  sub      al, dl
00448794  28c7                  sub      bh, al
00448796  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044879c  8a8e87000000          mov      cl, byte ptr [esi + 0x87]
004487a2  28d0                  sub      al, dl
004487a4  88be86000000          mov      byte ptr [esi + 0x86], bh
004487aa  28c1                  sub      cl, al
004487ac  888e87000000          mov      byte ptr [esi + 0x87], cl
004487b2  e9d2000000            jmp      0x448889
004487b7  8a8698000000          mov      al, byte ptr [esi + 0x98]
004487bd  8a9e87000000          mov      bl, byte ptr [esi + 0x87]
004487c3  28d0                  sub      al, dl
004487c5  28c3                  sub      bl, al
004487c7  889e87000000          mov      byte ptr [esi + 0x87], bl
004487cd  e9b7000000            jmp      0x448889
004487d2  8a8698000000          mov      al, byte ptr [esi + 0x98]
004487d8  28d0                  sub      al, dl
004487da  008686000000          add      byte ptr [esi + 0x86], al
004487e0  8a8698000000          mov      al, byte ptr [esi + 0x98]
004487e6  28d0                  sub      al, dl
004487e8  288687000000          sub      byte ptr [esi + 0x87], al
004487ee  e996000000            jmp      0x448889
004487f3  8a8698000000          mov      al, byte ptr [esi + 0x98]
004487f9  8aae86000000          mov      ch, byte ptr [esi + 0x86]
004487ff  28d0                  sub      al, dl
00448801  00c5                  add      ch, al
00448803  e973ffffff            jmp      0x44877b
00448808  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044880e  8abe86000000          mov      bh, byte ptr [esi + 0x86]
00448814  28d0                  sub      al, dl
00448816  00c7                  add      bh, al
00448818  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044881e  8a8e87000000          mov      cl, byte ptr [esi + 0x87]
00448824  28d0                  sub      al, dl
00448826  88be86000000          mov      byte ptr [esi + 0x86], bh
0044882c  00c1                  add      cl, al
0044882e  e979ffffff            jmp      0x4487ac
00448833  8a8698000000          mov      al, byte ptr [esi + 0x98]
00448839  8a9e87000000          mov      bl, byte ptr [esi + 0x87]
0044883f  28d0                  sub      al, dl
00448841  00c3                  add      bl, al
00448843  eb82                  jmp      0x4487c7
00448845  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044884b  28d0                  sub      al, dl
0044884d  288686000000          sub      byte ptr [esi + 0x86], al
00448853  8a8698000000          mov      al, byte ptr [esi + 0x98]
00448859  28d0                  sub      al, dl
0044885b  008687000000          add      byte ptr [esi + 0x87], al
00448861  eb26                  jmp      0x448889
00448863  80f909                cmp      cl, 9
00448866  748b                  je       0x4487f3
00448868  eb1f                  jmp      0x448889
0044886a  80f903                cmp      cl, 3
0044886d  7211                  jb       0x448880
0044886f  0f8611ffffff          jbe      0x448786
00448875  80f905                cmp      cl, 5
00448878  0f8439ffffff          je       0x4487b7
0044887e  eb09                  jmp      0x448889
00448880  80f901                cmp      cl, 1
00448883  0f84e2feffff          je       0x44876b
00448889  8a8698000000          mov      al, byte ptr [esi + 0x98]
0044888f  28d0                  sub      al, dl
00448891  008697000000          add      byte ptr [esi + 0x97], al
00448897  31c0                  xor      eax, eax
00448899  8a8697000000          mov      al, byte ptr [esi + 0x97]
0044889f  83f81f                cmp      eax, 0x1f
004488a2  0f8e1e020000          jle      0x448ac6
