; entrada_render_terreno: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0041068e  53                    push     ebx
0041068f  51                    push     ecx
00410690  56                    push     esi
00410691  57                    push     edi
00410692  55                    push     ebp
00410693  83ec18                sub      esp, 0x18
00410696  89c3                  mov      ebx, eax
00410698  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
004106a0  89d9                  mov      ecx, ebx
004106a2  01c2                  add      edx, eax
004106a4  01c1                  add      ecx, eax
004106a6  c1e208                shl      edx, 8
004106a9  01d1                  add      ecx, edx
004106ab  31d2                  xor      edx, edx
004106ad  6689ca                mov      dx, cx
004106b0  8b35707d5000          mov      esi, dword ptr [0x507d70]
004106b6  01d2                  add      edx, edx
004106b8  01d6                  add      esi, edx
004106ba  8b158d8f5000          mov      edx, dword ptr [0x508f8d]
004106c0  c1fa18                sar      edx, 0x18
004106c3  31db                  xor      ebx, ebx
004106c5  c1e205                shl      edx, 5
004106c8  668b1d18a04900        mov      bx, word ptr [0x49a018]
004106cf  89d7                  mov      edi, edx
004106d1  0faffb                imul     edi, ebx
004106d4  8b1d708f5000          mov      ebx, dword ptr [0x508f70]
004106da  c1e005                shl      eax, 5
004106dd  01fb                  add      ebx, edi
004106df  89442408              mov      dword ptr [esp + 8], eax
004106e3  01d3                  add      ebx, edx
004106e5  31d2                  xor      edx, edx
004106e7  891c24                mov      dword ptr [esp], ebx
004106ea  89542414              mov      dword ptr [esp + 0x14], edx
004106ee  eb4f                  jmp      0x41073f
004106f0  8b15a0174e00          mov      edx, dword ptr [0x4e17a0]
004106f6  8b1c24                mov      ebx, dword ptr [esp]
004106f9  c1e205                shl      edx, 5
004106fc  01d3                  add      ebx, edx
004106fe  ba00010000            mov      edx, 0x100
00410703  29c2                  sub      edx, eax
00410705  8d0412                lea      eax, [edx + edx]
00410708  01c6                  add      esi, eax
0041070a  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
00410712  668b1524875000        mov      dx, word ptr [0x508724]
00410719  01c0                  add      eax, eax
0041071b  8b7c2408              mov      edi, dword ptr [esp + 8]
0041071f  29c2                  sub      edx, eax
00410721  83c720                add      edi, 0x20
00410724  89d0                  mov      eax, edx
00410726  ba00010000            mov      edx, 0x100
0041072b  897c2408              mov      dword ptr [esp + 8], edi
0041072f  29c2                  sub      edx, eax
00410731  8b442414              mov      eax, dword ptr [esp + 0x14]
00410735  891c24                mov      dword ptr [esp], ebx
00410738  40                    inc      eax
00410739  01d1                  add      ecx, edx
0041073b  89442414              mov      dword ptr [esp + 0x14], eax
0041073f  a18d8f5000            mov      eax, dword ptr [0x508f8d]
00410744  31d2                  xor      edx, edx
00410746  c1f818                sar      eax, 0x18
00410749  668b1526875000        mov      dx, word ptr [0x508726]
00410750  01c0                  add      eax, eax
00410752  29c2                  sub      edx, eax
00410754  31c0                  xor      eax, eax
00410756  668b442414            mov      ax, word ptr [esp + 0x14]
0041075b  39d0                  cmp      eax, edx
0041075d  0f8d12010000          jge      0x410875
00410763  8b3c24                mov      edi, dword ptr [esp]
00410766  660fbe05908f5000      movsx    ax, byte ptr [0x508f90]
0041076e  31db                  xor      ebx, ebx
00410770  c1e005                shl      eax, 5
00410773  895c2410              mov      dword ptr [esp + 0x10], ebx
00410777  8944240c              mov      dword ptr [esp + 0xc], eax
0041077b  eb4c                  jmp      0x4107c9
0041077d  8b156c8f5000          mov      edx, dword ptr [0x508f6c]
00410783  25ffff0000            and      eax, 0xffff
00410788  31db                  xor      ebx, ebx
0041078a  8b4482fc              mov      eax, dword ptr [edx + eax*4 - 4]
0041078e  83c602                add      esi, 2
00410791  6689cb                mov      bx, cx
00410794  8b5008                mov      edx, dword ptr [eax + 8]
00410797  89f8                  mov      eax, edi
00410799  41                    inc      ecx
0041079a  e88bbf0400            call     0x45c72a
0041079f  31d2                  xor      edx, edx
004107a1  31c0                  xor      eax, eax
004107a3  668b542408            mov      dx, word ptr [esp + 8]
004107a8  668b44240c            mov      ax, word ptr [esp + 0xc]
004107ad  83c720                add      edi, 0x20
004107b0  e8d0f8ffff            call     0x410085
004107b5  8b54240c              mov      edx, dword ptr [esp + 0xc]
004107b9  8b5c2410              mov      ebx, dword ptr [esp + 0x10]
004107bd  83c220                add      edx, 0x20
004107c0  43                    inc      ebx
004107c1  8954240c              mov      dword ptr [esp + 0xc], edx
004107c5  895c2410              mov      dword ptr [esp + 0x10], ebx
004107c9  8b158d8f5000          mov      edx, dword ptr [0x508f8d]
004107cf  31c0                  xor      eax, eax
004107d1  c1fa18                sar      edx, 0x18
004107d4  66a124875000          mov      ax, word ptr [0x508724]
004107da  01d2                  add      edx, edx
004107dc  29d0                  sub      eax, edx
004107de  31d2                  xor      edx, edx
004107e0  668b542410            mov      dx, word ptr [esp + 0x10]
004107e5  39c2                  cmp      edx, eax
004107e7  0f8d03ffffff          jge      0x4106f0
004107ed  31db                  xor      ebx, ebx
004107ef  6689cb                mov      bx, cx
004107f2  89d8                  mov      eax, ebx
004107f4  e834280100            call     0x42302d
004107f9  84c0                  test     al, al
004107fb  746c                  je       0x410869
004107fd  31d2                  xor      edx, edx
004107ff  89d8                  mov      eax, ebx
00410801  8a1541805000          mov      dl, byte ptr [0x508041]
00410807  e82e610600            call     0x47693a
0041080c  84c0                  test     al, al
0041080e  7559                  jne      0x410869
00410810  bd00010000            mov      ebp, 0x100
00410815  89da                  mov      edx, ebx
00410817  89d8                  mov      eax, ebx
00410819  c1fa1f                sar      edx, 0x1f
0041081c  f7fd                  idiv     ebp
0041081e  bd08000000            mov      ebp, 8
00410823  89d0                  mov      eax, edx
00410825  c1fa1f                sar      edx, 0x1f
00410828  f7fd                  idiv     ebp
0041082a  89d5                  mov      ebp, edx
0041082c  89da                  mov      edx, ebx
0041082e  89d8                  mov      eax, ebx
00410830  c1fa1f                sar      edx, 0x1f
00410833  c1e208                shl      edx, 8
00410836  1bc2                  sbb      eax, edx
00410838  c1f808                sar      eax, 8
0041083b  89c2                  mov      edx, eax
0041083d  c744240408000000      mov      dword ptr [esp + 4], 8
00410845  c1fa1f                sar      edx, 0x1f
00410848  f77c2404              idiv     dword ptr [esp + 4]
0041084c  81c55d010000          add      ebp, 0x15d
00410852  c1e203                shl      edx, 3
00410855  8d042a                lea      eax, [edx + ebp]
00410858  25ffff0000            and      eax, 0xffff
0041085d  89da                  mov      edx, ebx
0041085f  e831f5ffff            call     0x40fd95
00410864  e914ffffff            jmp      0x41077d
00410869  31d2                  xor      edx, edx
0041086b  31c0                  xor      eax, eax
0041086d  6689ca                mov      dx, cx
00410870  668b06                mov      ax, word ptr [esi]
00410873  ebea                  jmp      0x41085f
00410875  83c418                add      esp, 0x18
00410878  5d                    pop      ebp
00410879  5f                    pop      edi
0041087a  5e                    pop      esi
0041087b  59                    pop      ecx
0041087c  5b                    pop      ebx
