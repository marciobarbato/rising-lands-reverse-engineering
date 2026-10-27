; gerador_aleatorio: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00489728  53                    push     ebx
00489729  51                    push     ecx
0048972a  52                    push     edx
0048972b  56                    push     esi
0048972c  89c3                  mov      ebx, eax
0048972e  85c0                  test     eax, eax
00489730  7e43                  jle      0x489775
00489732  b91df30100            mov      ecx, 0x1f31d
00489737  a1b48d4900            mov      eax, dword ptr [0x498db4]
0048973c  31d2                  xor      edx, edx
0048973e  f7f1                  div      ecx
00489740  69f0140b0000          imul     esi, eax, 0xb14
00489746  31d2                  xor      edx, edx
00489748  a1b48d4900            mov      eax, dword ptr [0x498db4]
0048974d  f7f1                  div      ecx
0048974f  69c2a7410000          imul     eax, edx, 0x41a7
00489755  29f0                  sub      eax, esi
00489757  85c0                  test     eax, eax
00489759  7f05                  jg       0x489760
0048975b  05ffffff7f            add      eax, 0x7fffffff
00489760  a3b48d4900            mov      dword ptr [0x498db4], eax
00489765  a1b48d4900            mov      eax, dword ptr [0x498db4]
0048976a  31d2                  xor      edx, edx
0048976c  f7f3                  div      ebx
0048976e  89d0                  mov      eax, edx
00489770  5e                    pop      esi
00489771  5a                    pop      edx
00489772  59                    pop      ecx
00489773  5b                    pop      ebx
00489774  c3                    ret
00489775  7d12                  jge      0x489789
00489777  89c2                  mov      edx, eax
00489779  f7da                  neg      edx
0048977b  bbffffff7f            mov      ebx, 0x7fffffff
00489780  89d0                  mov      eax, edx
00489782  c1fa1f                sar      edx, 0x1f
00489785  f7fb                  idiv     ebx
00489787  eb0e                  jmp      0x489797
00489789  e896a20000            call     0x493a24
0048978e  bbffffff7f            mov      ebx, 0x7fffffff
00489793  31d2                  xor      edx, edx
00489795  f7f3                  div      ebx
00489797  8915b48d4900          mov      dword ptr [0x498db4], edx
0048979d  31c0                  xor      eax, eax
0048979f  5e                    pop      esi
004897a0  5a                    pop      edx
004897a1  59                    pop      ecx
004897a2  5b                    pop      ebx
004897a3  c3                    ret
