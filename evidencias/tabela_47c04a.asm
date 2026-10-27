; tabela_47c04a: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0047c04a  53                    push     ebx
0047c04b  52                    push     edx
0047c04c  83ec08                sub      esp, 8
0047c04f  bbffff0000            mov      ebx, 0xffff
0047c054  31d2                  xor      edx, edx
0047c056  eb20                  jmp      0x47c078
0047c058  6bc00a                imul     eax, eax, 0xa
0047c05b  66899814c65000        mov      word ptr [eax + 0x50c614], bx
0047c062  66899816c65000        mov      word ptr [eax + 0x50c616], bx
0047c069  66899818c65000        mov      word ptr [eax + 0x50c618], bx
0047c070  42                    inc      edx
0047c071  6689981ac65000        mov      word ptr [eax + 0x50c61a], bx
0047c078  31c0                  xor      eax, eax
0047c07a  6689d0                mov      ax, dx
0047c07d  3d90010000            cmp      eax, 0x190
0047c082  7cd4                  jl       0x47c058
0047c084  ba02000000            mov      edx, 2
0047c089  8d442404              lea      eax, [esp + 4]
0047c08d  e8cfc3fdff            call     0x458461
0047c092  ba02000000            mov      edx, 2
0047c097  89e0                  mov      eax, esp
0047c099  31db                  xor      ebx, ebx
0047c09b  eb14                  jmp      0x47c0b1
0047c09d  31c0                  xor      eax, eax
0047c09f  6689d8                mov      ax, bx
0047c0a2  6bc00a                imul     eax, eax, 0xa
0047c0a5  31d2                  xor      edx, edx
0047c0a7  668b1424              mov      dx, word ptr [esp]
0047c0ab  0514c65000            add      eax, 0x50c614
0047c0b0  43                    inc      ebx
0047c0b1  e8abc3fdff            call     0x458461
0047c0b6  663b5c2404            cmp      bx, word ptr [esp + 4]
0047c0bb  72e0                  jb       0x47c09d
