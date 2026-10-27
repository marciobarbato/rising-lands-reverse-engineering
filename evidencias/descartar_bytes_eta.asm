; descartar_bytes_eta: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0047c30f  53                    push     ebx
0047c310  52                    push     edx
0047c311  83ec04                sub      esp, 4
0047c314  30db                  xor      bl, bl
0047c316  eb32                  jmp      0x47c34a
0047c318  ba01000000            mov      edx, 1
0047c31d  89e0                  mov      eax, esp
0047c31f  e83dc1fdff            call     0x458461
0047c324  ba01000000            mov      edx, 1
0047c329  89e0                  mov      eax, esp
0047c32b  e831c1fdff            call     0x458461
0047c330  ba01000000            mov      edx, 1
0047c335  89e0                  mov      eax, esp
0047c337  e825c1fdff            call     0x458461
0047c33c  ba01000000            mov      edx, 1
0047c341  89e0                  mov      eax, esp
0047c343  fec3                  inc      bl
0047c345  e817c1fdff            call     0x458461
0047c34a  31c0                  xor      eax, eax
0047c34c  88d8                  mov      al, bl
0047c34e  83f804                cmp      eax, 4
0047c351  7cc5                  jl       0x47c318
0047c353  83c404                add      esp, 4
0047c356  5a                    pop      edx
0047c357  5b                    pop      ebx
0047c358  c3                    ret
