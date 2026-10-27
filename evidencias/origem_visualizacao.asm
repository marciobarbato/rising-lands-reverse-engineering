; origem_visualizacao: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00474b08  51                    push     ecx
00474b09  52                    push     edx
00474b0a  56                    push     esi
00474b0b  57                    push     edi
00474b0c  81ec00010000          sub      esp, 0x100
00474b12  be94945000            mov      esi, 0x509494
00474b17  89e7                  mov      edi, esp
00474b19  57                    push     edi
00474b1a  8a06                  mov      al, byte ptr [esi]
00474b1c  8807                  mov      byte ptr [edi], al
00474b1e  3c00                  cmp      al, 0
00474b20  7410                  je       0x474b32
00474b22  8a4601                mov      al, byte ptr [esi + 1]
00474b25  83c602                add      esi, 2
00474b28  884701                mov      byte ptr [edi + 1], al
00474b2b  83c702                add      edi, 2
00474b2e  3c00                  cmp      al, 0
00474b30  75e8                  jne      0x474b1a
00474b32  5f                    pop      edi
00474b33  be444d4900            mov      esi, 0x494d44 ; '\\platgame.pie'
00474b38  89e7                  mov      edi, esp
00474b3a  57                    push     edi
00474b3b  2bc9                  sub      ecx, ecx
00474b3d  49                    dec      ecx
00474b3e  b000                  mov      al, 0
00474b40  f2ae                  repne scasb al, byte ptr es:[edi]
00474b42  4f                    dec      edi
00474b43  8a06                  mov      al, byte ptr [esi]
00474b45  8807                  mov      byte ptr [edi], al
00474b47  3c00                  cmp      al, 0
00474b49  7410                  je       0x474b5b
00474b4b  8a4601                mov      al, byte ptr [esi + 1]
00474b4e  83c602                add      esi, 2
00474b51  884701                mov      byte ptr [edi + 1], al
00474b54  83c702                add      edi, 2
00474b57  3c00                  cmp      al, 0
00474b59  75e8                  jne      0x474b43
00474b5b  5f                    pop      edi
00474b5c  e853a8fcff            call     0x43f3b4
00474b61  a3708f5000            mov      dword ptr [0x508f70], eax
00474b66  89c2                  mov      edx, eax
00474b68  89e0                  mov      eax, esp
00474b6a  e8554e0000            call     0x4799c4
00474b6f  31d2                  xor      edx, edx
00474b71  31c0                  xor      eax, eax
00474b73  668b1522875000        mov      dx, word ptr [0x508722]
00474b7a  66a120875000          mov      ax, word ptr [0x508720]
00474b80  e809bbf9ff            call     0x41068e ; entrada_render_terreno
00474b85  a1708f5000            mov      eax, dword ptr [0x508f70]
00474b8a  e8b6a8fcff            call     0x43f445
00474b8f  b801000000            mov      eax, 1
00474b94  e8b6a5fcff            call     0x43f14f ; apresentar_superficie
00474b99  a1b0244e00            mov      eax, dword ptr [0x4e24b0]
00474b9e  e88ea2fcff            call     0x43ee31
00474ba3  e80ca8fcff            call     0x43f3b4
00474ba8  a3708f5000            mov      dword ptr [0x508f70], eax
00474bad  89c2                  mov      edx, eax
00474baf  89e0                  mov      eax, esp
00474bb1  e80e4e0000            call     0x4799c4
00474bb6  31d2                  xor      edx, edx
00474bb8  31c0                  xor      eax, eax
00474bba  668b1522875000        mov      dx, word ptr [0x508722]
00474bc1  66a120875000          mov      ax, word ptr [0x508720]
00474bc7  e8c2baf9ff            call     0x41068e ; entrada_render_terreno
00474bcc  a1708f5000            mov      eax, dword ptr [0x508f70]
00474bd1  e86fa8fcff            call     0x43f445
00474bd6  b801000000            mov      eax, 1
00474bdb  e86fa5fcff            call     0x43f14f ; apresentar_superficie
00474be0  81c400010000          add      esp, 0x100
00474be6  5f                    pop      edi
00474be7  5e                    pop      esi
00474be8  5a                    pop      edx
00474be9  59                    pop      ecx
00474bea  c3                    ret
