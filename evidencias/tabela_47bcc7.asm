; tabela_47bcc7: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0047bcc7  53                    push     ebx
0047bcc8  51                    push     ecx
0047bcc9  52                    push     edx
0047bcca  56                    push     esi
0047bccb  ba02000000            mov      edx, 2
0047bcd0  b88cb15000            mov      eax, 0x50b18c
0047bcd5  e887c7fdff            call     0x458461
0047bcda  b2ff                  mov      dl, 0xff
0047bcdc  31c0                  xor      eax, eax
0047bcde  eb07                  jmp      0x47bce7
0047bce0  40                    inc      eax
0047bce1  889023c35000          mov      byte ptr [eax + 0x50c323], dl
0047bce7  31db                  xor      ebx, ebx
0047bce9  668b1d8cb15000        mov      bx, word ptr [0x50b18c]
0047bcf0  39d8                  cmp      eax, ebx
0047bcf2  72ec                  jb       0x47bce0
0047bcf4  6685db                test     bx, bx
0047bcf7  7440                  je       0x47bd39
0047bcf9  b96cb75000            mov      ecx, 0x50b76c
0047bcfe  bb8eb15000            mov      ebx, 0x50b18e
0047bd03  31f6                  xor      esi, esi
0047bd05  eb1f                  jmp      0x47bd26
0047bd07  ba02000000            mov      edx, 2
0047bd0c  89d8                  mov      eax, ebx
0047bd0e  e84ec7fdff            call     0x458461
0047bd13  ba04000000            mov      edx, 4
0047bd18  89c8                  mov      eax, ecx
0047bd1a  46                    inc      esi
0047bd1b  e841c7fdff            call     0x458461
0047bd20  83c302                add      ebx, 2
0047bd23  83c104                add      ecx, 4
0047bd26  31c0                  xor      eax, eax
0047bd28  66a18cb15000          mov      ax, word ptr [0x50b18c]
0047bd2e  39c6                  cmp      esi, eax
0047bd30  72d5                  jb       0x47bd07
0047bd32  b001                  mov      al, 1
0047bd34  5e                    pop      esi
0047bd35  5a                    pop      edx
0047bd36  59                    pop      ecx
0047bd37  5b                    pop      ebx
0047bd38  c3                    ret
0047bd39  30c0                  xor      al, al
0047bd3b  5e                    pop      esi
0047bd3c  5a                    pop      edx
0047bd3d  59                    pop      ecx
0047bd3e  5b                    pop      ebx
