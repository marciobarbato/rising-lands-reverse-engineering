; direcao_entre_celulas: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00477042  53                    push     ebx
00477043  51                    push     ecx
00477044  56                    push     esi
00477045  57                    push     edi
00477046  89c3                  mov      ebx, eax
00477048  31c9                  xor      ecx, ecx
0047704a  6689d1                mov      cx, dx
0047704d  be00010000            mov      esi, 0x100
00477052  89ca                  mov      edx, ecx
00477054  89c8                  mov      eax, ecx
00477056  c1fa1f                sar      edx, 0x1f
00477059  f7fe                  idiv     esi
0047705b  89d6                  mov      esi, edx
0047705d  81e3ffff0000          and      ebx, 0xffff
00477063  bf00010000            mov      edi, 0x100
00477068  89da                  mov      edx, ebx
0047706a  89d8                  mov      eax, ebx
0047706c  c1fa1f                sar      edx, 0x1f
0047706f  f7ff                  idiv     edi
00477071  29d6                  sub      esi, edx
00477073  89ca                  mov      edx, ecx
00477075  89c8                  mov      eax, ecx
00477077  c1fa1f                sar      edx, 0x1f
0047707a  f7ff                  idiv     edi
0047707c  89c1                  mov      ecx, eax
0047707e  89da                  mov      edx, ebx
00477080  89d8                  mov      eax, ebx
00477082  c1fa1f                sar      edx, 0x1f
00477085  f7ff                  idiv     edi
00477087  29c1                  sub      ecx, eax
00477089  0fbfd6                movsx    edx, si
0047708c  89c8                  mov      eax, ecx
0047708e  85d2                  test     edx, edx
00477090  7e1e                  jle      0x4770b0
00477092  0fbfc1                movsx    eax, cx
00477095  85c0                  test     eax, eax
00477097  7d07                  jge      0x4770a0
00477099  b007                  mov      al, 7
0047709b  5f                    pop      edi
0047709c  5e                    pop      esi
0047709d  59                    pop      ecx
0047709e  5b                    pop      ebx
0047709f  c3                    ret
004770a0  7507                  jne      0x4770a9
004770a2  b009                  mov      al, 9
004770a4  5f                    pop      edi
004770a5  5e                    pop      esi
004770a6  59                    pop      ecx
004770a7  5b                    pop      ebx
004770a8  c3                    ret
004770a9  b00b                  mov      al, 0xb
004770ab  5f                    pop      edi
004770ac  5e                    pop      esi
004770ad  59                    pop      ecx
004770ae  5b                    pop      ebx
004770af  c3                    ret
004770b0  7d1e                  jge      0x4770d0
004770b2  0fbfd1                movsx    edx, cx
004770b5  85d2                  test     edx, edx
004770b7  7d07                  jge      0x4770c0
004770b9  b003                  mov      al, 3
004770bb  5f                    pop      edi
004770bc  5e                    pop      esi
004770bd  59                    pop      ecx
004770be  5b                    pop      ebx
004770bf  c3                    ret
004770c0  7507                  jne      0x4770c9
004770c2  b001                  mov      al, 1
004770c4  5f                    pop      edi
004770c5  5e                    pop      esi
004770c6  59                    pop      ecx
004770c7  5b                    pop      ebx
004770c8  c3                    ret
004770c9  b00f                  mov      al, 0xf
004770cb  5f                    pop      edi
004770cc  5e                    pop      esi
004770cd  59                    pop      ecx
004770ce  5b                    pop      ebx
004770cf  c3                    ret
004770d0  0fbfc1                movsx    eax, cx
004770d3  85c0                  test     eax, eax
004770d5  7d07                  jge      0x4770de
004770d7  b005                  mov      al, 5
004770d9  5f                    pop      edi
004770da  5e                    pop      esi
004770db  59                    pop      ecx
004770dc  5b                    pop      ebx
004770dd  c3                    ret
004770de  7e07                  jle      0x4770e7
004770e0  b00d                  mov      al, 0xd
004770e2  5f                    pop      edi
004770e3  5e                    pop      esi
004770e4  59                    pop      ecx
004770e5  5b                    pop      ebx
004770e6  c3                    ret
004770e7  30c0                  xor      al, al
004770e9  5f                    pop      edi
004770ea  5e                    pop      esi
004770eb  59                    pop      ecx
004770ec  5b                    pop      ebx
004770ed  c3                    ret
