; contador_frequencia: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0043f710  53                    push     ebx
0043f711  51                    push     ecx
0043f712  52                    push     edx
0043f713  66ff05ae174e00        inc      word ptr [0x4e17ae]
0043f71a  2eff15b8315200        call     dword ptr cs:[0x5231b8] ; KERNEL32.dll!GetTickCount
0043f721  8b1db0174e00          mov      ebx, dword ptr [0x4e17b0]
0043f727  89c2                  mov      edx, eax
0043f729  29da                  sub      edx, ebx
0043f72b  a3b4174e00            mov      dword ptr [0x4e17b4], eax
0043f730  81fae8030000          cmp      edx, 0x3e8
0043f736  725d                  jb       0x43f795
0043f738  a3b0174e00            mov      dword ptr [0x4e17b0], eax
0043f73d  31c0                  xor      eax, eax
0043f73f  66a1ae174e00          mov      ax, word ptr [0x4e17ae]
0043f745  83f863                cmp      eax, 0x63
0043f748  7e09                  jle      0x43f753
0043f74a  66c705ae174e006300    mov      word ptr [0x4e17ae], 0x63
0043f753  31db                  xor      ebx, ebx
0043f755  668b1dae174e00        mov      bx, word ptr [0x4e17ae]
0043f75c  b90a000000            mov      ecx, 0xa
0043f761  89da                  mov      edx, ebx
0043f763  89d8                  mov      eax, ebx
0043f765  c1fa1f                sar      edx, 0x1f
0043f768  f7f9                  idiv     ecx
0043f76a  83c030                add      eax, 0x30
0043f76d  89da                  mov      edx, ebx
0043f76f  a294634900            mov      byte ptr [0x496394], al
0043f774  c1fa1f                sar      edx, 0x1f
0043f777  89d8                  mov      eax, ebx
0043f779  f7f9                  idiv     ecx
0043f77b  83c230                add      edx, 0x30
0043f77e  30e4                  xor      ah, ah
0043f780  31c9                  xor      ecx, ecx
0043f782  881595634900          mov      byte ptr [0x496395], dl
0043f788  882596634900          mov      byte ptr [0x496396], ah
0043f78e  66890dae174e00        mov      word ptr [0x4e17ae], cx
0043f795  bb0a000000            mov      ebx, 0xa
0043f79a  31c0                  xor      eax, eax
0043f79c  bab4634900            mov      edx, 0x4963b4 ; '0000000000'
0043f7a1  a05ba04900            mov      al, byte ptr [0x49a05b]
0043f7a6  e8e0cb0400            call     0x48c38b
0043f7ab  5a                    pop      edx
0043f7ac  59                    pop      ecx
0043f7ad  5b                    pop      ebx
0043f7ae  c3                    ret
