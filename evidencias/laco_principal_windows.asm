; laco_principal_windows: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00460170  53                    push     ebx
00460171  83ec1c                sub      esp, 0x1c
00460174  6815494900            push     0x494915 ; 'Rising Lands'
00460179  30e4                  xor      ah, ah
0046017b  6822494900            push     0x494922 ; 'RISING LANDS'
00460180  8825ec284e00          mov      byte ptr [0x4e28ec], ah
00460186  2eff158c325200        call     dword ptr cs:[0x52328c] ; USER32.dll!FindWindowA
0046018d  85c0                  test     eax, eax
0046018f  7407                  je       0x460198
00460191  31c0                  xor      eax, eax
00460193  e9da000000            jmp      0x460272
00460198  8b542428              mov      edx, dword ptr [esp + 0x28]
0046019c  8b442424              mov      eax, dword ptr [esp + 0x24]
004601a0  e8c7feffff            call     0x46006c
004601a5  e8c2cd0100            call     0x47cf6c
004601aa  a1e8274e00            mov      eax, dword ptr [0x4e27e8]
004601af  31db                  xor      ebx, ebx
004601b1  e8d27ffbff            call     0x418188
004601b6  e8e4a60200            call     0x48a89f
004601bb  e836790000            call     0x467af6
004601c0  3a1d59a04900          cmp      bl, byte ptr [0x49a059]
004601c6  755f                  jne      0x460227
004601c8  53                    push     ebx
004601c9  53                    push     ebx
004601ca  53                    push     ebx
004601cb  53                    push     ebx
004601cc  8d442410              lea      eax, [esp + 0x10]
004601d0  50                    push     eax
004601d1  2eff15b8325200        call     dword ptr cs:[0x5232b8] ; USER32.dll!PeekMessageA
004601d8  85c0                  test     eax, eax
004601da  7429                  je       0x460205
004601dc  53                    push     ebx
004601dd  53                    push     ebx
004601de  53                    push     ebx
004601df  8d44240c              lea      eax, [esp + 0xc]
004601e3  50                    push     eax
004601e4  2eff1598325200        call     dword ptr cs:[0x523298] ; USER32.dll!GetMessageA
004601eb  85c0                  test     eax, eax
004601ed  7438                  je       0x460227
004601ef  89e0                  mov      eax, esp
004601f1  50                    push     eax
004601f2  2eff15d8325200        call     dword ptr cs:[0x5232d8] ; USER32.dll!TranslateMessage
004601f9  89e0                  mov      eax, esp
004601fb  50                    push     eax
004601fc  2eff1584325200        call     dword ptr cs:[0x523284] ; USER32.dll!DispatchMessageA
00460203  eb16                  jmp      0x46021b
00460205  3a1d58a04900          cmp      bl, byte ptr [0x49a058]
0046020b  7407                  je       0x460214
0046020d  e8fc4d0100            call     0x47500e ; ciclo_atualizacao_desenho
00460212  eb07                  jmp      0x46021b
00460214  2eff15e4325200        call     dword ptr cs:[0x5232e4] ; USER32.dll!WaitMessage
0046021b  e8aaa80200            call     0x48aaca
00460220  e8cb790000            call     0x467bf0
00460225  eb99                  jmp      0x4601c0
00460227  e859790000            call     0x467b85
0046022c  e8d3a70200            call     0x48aa04
00460231  a1e8274e00            mov      eax, dword ptr [0x4e27e8]
00460236  e8617ffbff            call     0x41819c
0046023b  8b15e4274e00          mov      edx, dword ptr [0x4e27e4]
00460241  52                    push     edx
00460242  68d8484900            push     0x4948d8 ; 'RISING LANDS'
00460247  2eff15dc325200        call     dword ptr cs:[0x5232dc] ; USER32.dll!UnregisterClassA
0046024e  31c0                  xor      eax, eax
00460250  a0ec284e00            mov      al, byte ptr [0x4e28ec]
00460255  85c0                  test     eax, eax
00460257  7415                  je       0x46026e
00460259  6a00                  push     0
0046025b  68ec274e00            push     0x4e27ec
00460260  682f494900            push     0x49492f ; 'Rising error'
00460265  6a00                  push     0
00460267  2eff15b0325200        call     dword ptr cs:[0x5232b0] ; USER32.dll!MessageBoxA
0046026e  8b442408              mov      eax, dword ptr [esp + 8]
00460272  83c41c                add      esp, 0x1c
00460275  5b                    pop      ebx
00460276  c2                    .byte    0xc2
