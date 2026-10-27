; leitura_arquivo: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00458420  e8fa420300            call     0x48c71f
00458425  a31c1d4e00            mov      dword ptr [0x4e1d1c], eax
0045842a  85c0                  test     eax, eax
0045842c  0f95c0                setne    al
0045842f  c3                    ret
00458430  52                    push     edx
00458431  ba88484900            mov      edx, 0x494888
00458436  e8e4420300            call     0x48c71f
0045843b  85c0                  test     eax, eax
0045843d  7504                  jne      0x458443
0045843f  30c0                  xor      al, al
00458441  5a                    pop      edx
00458442  c3                    ret
00458443  e8c3430300            call     0x48c80b
00458448  b001                  mov      al, 1
0045844a  5a                    pop      edx
0045844b  c3                    ret
0045844c  52                    push     edx
0045844d  a11c1d4e00            mov      eax, dword ptr [0x4e1d1c]
00458452  31d2                  xor      edx, edx
00458454  e8b2430300            call     0x48c80b
00458459  89151c1d4e00          mov      dword ptr [0x4e1d1c], edx
0045845f  5a                    pop      edx
00458460  c3                    ret
00458461  53                    push     ebx
00458462  51                    push     ecx
00458463  bb01000000            mov      ebx, 1
00458468  8b0d1c1d4e00          mov      ecx, dword ptr [0x4e1d1c]
0045846e  e808450300            call     0x48c97b
00458473  59                    pop      ecx
00458474  5b                    pop      ebx
00458475  c3                    ret
00458476  53                    push     ebx
00458477  51                    push     ecx
00458478  bb01000000            mov      ebx, 1
0045847d  8b0d1c1d4e00          mov      ecx, dword ptr [0x4e1d1c]
00458483  e8f2460300            call     0x48cb7a
00458488  59                    pop      ecx
00458489  5b                    pop      ebx
0045848a  c3                    ret
0045848b  53                    push     ebx
0045848c  51                    push     ecx
0045848d  31db                  xor      ebx, ebx
0045848f  8b0d1c1d4e00          mov      ecx, dword ptr [0x4e1d1c]
00458495  88d3                  mov      bl, dl
00458497  89c2                  mov      edx, eax
00458499  89c8                  mov      eax, ecx
0045849b  e802490300            call     0x48cda2
004584a0  59                    pop      ecx
004584a1  5b                    pop      ebx
004584a2  c3                    ret
