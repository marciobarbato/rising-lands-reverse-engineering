; carregador_cmp: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
004186ba  53                    push     ebx
004186bb  51                    push     ecx
004186bc  52                    push     edx
004186bd  56                    push     esi
004186be  89c6                  mov      esi, eax
004186c0  b808000000            mov      eax, 8
004186c5  bad3414900            mov      edx, 0x4941d3
004186ca  e8d7f70400            call     0x467ea6
004186cf  89c3                  mov      ebx, eax
004186d1  89c1                  mov      ecx, eax
004186d3  89f0                  mov      eax, esi
004186d5  e846fd0300            call     0x458420 ; leitura_arquivo
004186da  25ff000000            and      eax, 0xff
004186df  0f8490000000          je       0x418775
004186e5  ba02000000            mov      edx, 2
004186ea  89d8                  mov      eax, ebx
004186ec  e870fd0300            call     0x458461
004186f1  31c0                  xor      eax, eax
004186f3  668b03                mov      ax, word ptr [ebx]
004186f6  c1e002                shl      eax, 2
004186f9  31f6                  xor      esi, esi
004186fb  e8a6f70400            call     0x467ea6
00418700  894304                mov      dword ptr [ebx + 4], eax
00418703  eb01                  jmp      0x418706
00418705  46                    inc      esi
00418706  663b31                cmp      si, word ptr [ecx]
00418709  7363                  jae      0x41876e
0041870b  b80c000000            mov      eax, 0xc
00418710  e891f70400            call     0x467ea6
00418715  89c3                  mov      ebx, eax
00418717  85c0                  test     eax, eax
00418719  743f                  je       0x41875a
0041871b  ba02000000            mov      edx, 2
00418720  e83cfd0300            call     0x458461
00418725  ba02000000            mov      edx, 2
0041872a  8d4302                lea      eax, [ebx + 2]
0041872d  e82ffd0300            call     0x458461
00418732  ba04000000            mov      edx, 4
00418737  8d4304                lea      eax, [ebx + 4]
0041873a  e822fd0300            call     0x458461
0041873f  8b4304                mov      eax, dword ptr [ebx + 4]
00418742  e85ff70400            call     0x467ea6
00418747  894308                mov      dword ptr [ebx + 8], eax
0041874a  85c0                  test     eax, eax
0041874c  7504                  jne      0x418752
0041874e  31db                  xor      ebx, ebx
00418750  eb08                  jmp      0x41875a
00418752  8b5304                mov      edx, dword ptr [ebx + 4]
00418755  e807fd0300            call     0x458461
0041875a  31d2                  xor      edx, edx
0041875c  8b4104                mov      eax, dword ptr [ecx + 4]
0041875f  6689f2                mov      dx, si
00418762  891c90                mov      dword ptr [eax + edx*4], ebx
00418765  8b4104                mov      eax, dword ptr [ecx + 4]
00418768  833c9000              cmp      dword ptr [eax + edx*4], 0
0041876c  7597                  jne      0x418705
0041876e  e8d9fc0300            call     0x45844c
00418773  89c8                  mov      eax, ecx
00418775  5e                    pop      esi
00418776  5a                    pop      edx
00418777  59                    pop      ecx
00418778  5b                    pop      ebx
00418779  c3                    ret
