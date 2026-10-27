; tabela_47ac30: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0047ac30  53                    push     ebx
0047ac31  51                    push     ecx
0047ac32  52                    push     edx
0047ac33  56                    push     esi
0047ac34  57                    push     edi
0047ac35  55                    push     ebp
0047ac36  83ec0c                sub      esp, 0xc
0047ac39  31d2                  xor      edx, edx
0047ac3b  89542404              mov      dword ptr [esp + 4], edx
0047ac3f  e8bdf9ffff            call     0x47a601
0047ac44  ba02000000            mov      edx, 2
0047ac49  b8cea95000            mov      eax, 0x50a9ce
0047ac4e  e80ed8fdff            call     0x458461
0047ac53  ba02000000            mov      edx, 2
0047ac58  8d442404              lea      eax, [esp + 4]
0047ac5c  bdd0a95000            mov      ebp, 0x50a9d0
0047ac61  e8fbd7fdff            call     0x458461
0047ac66  31d2                  xor      edx, edx
0047ac68  31f6                  xor      esi, esi
0047ac6a  891424                mov      dword ptr [esp], edx
0047ac6d  eb13                  jmp      0x47ac82
0047ac6f  8b3c24                mov      edi, dword ptr [esp]
0047ac72  83c60c                add      esi, 0xc
0047ac75  83c50c                add      ebp, 0xc
0047ac78  47                    inc      edi
0047ac79  8886caa95000          mov      byte ptr [esi + 0x50a9ca], al
0047ac7f  893c24                mov      dword ptr [esp], edi
0047ac82  31ff                  xor      edi, edi
0047ac84  8b1c24                mov      ebx, dword ptr [esp]
0047ac87  668b3dcea95000        mov      di, word ptr [0x50a9ce]
0047ac8e  39df                  cmp      edi, ebx
0047ac90  7e5a                  jle      0x47acec
0047ac92  31d2                  xor      edx, edx
0047ac94  89e8                  mov      eax, ebp
0047ac96  668b542404            mov      dx, word ptr [esp + 4]
0047ac9b  e8c1d7fdff            call     0x458461
0047aca0  668b9ed4a95000        mov      bx, word ptr [esi + 0x50a9d4]
0047aca7  6bc31e                imul     eax, ebx, 0x1e
0047acaa  668986d4a95000        mov      word ptr [esi + 0x50a9d4], ax
0047acb1  31c9                  xor      ecx, ecx
0047acb3  668bbed2a95000        mov      di, word ptr [esi + 0x50a9d2]
0047acba  8a86d6a95000          mov      al, byte ptr [esi + 0x50a9d6]
0047acc0  898ed8a95000          mov      dword ptr [esi + 0x50a9d8], ecx
0047acc6  b410                  mov      ah, 0x10
0047acc8  fec0                  inc      al
0047acca  240f                  and      al, 0xf
0047accc  ba01000000            mov      edx, 1
0047acd1  88c1                  mov      cl, al
0047acd3  d3e2                  shl      edx, cl
0047acd5  31db                  xor      ebx, ebx
0047acd7  81e2ffff0000          and      edx, 0xffff
0047acdd  6689fb                mov      bx, di
0047ace0  85da                  test     edx, ebx
0047ace2  758b                  jne      0x47ac6f
0047ace4  fecc                  dec      ah
0047ace6  75e0                  jne      0x47acc8
0047ace8  b0ff                  mov      al, 0xff
0047acea  eb83                  jmp      0x47ac6f
0047acec  4f                    dec      edi
0047aced  89f9                  mov      ecx, edi
0047acef  c1e102                shl      ecx, 2
0047acf2  29f9                  sub      ecx, edi
0047acf4  c1e102                shl      ecx, 2
0047acf7  eb04                  jmp      0x47acfd
0047acf9  83e90c                sub      ecx, 0xc
0047acfc  4f                    dec      edi
0047acfd  85ff                  test     edi, edi
0047acff  7c61                  jl       0x47ad62
0047ad01  31c0                  xor      eax, eax
0047ad03  668b81d0a95000        mov      ax, word ptr [ecx + 0x50a9d0]
0047ad0a  3dffff0000            cmp      eax, 0xffff
0047ad0f  7509                  jne      0x47ad1a
0047ad11  66ff0dcea95000        dec      word ptr [0x50a9ce]
0047ad18  ebdf                  jmp      0x47acf9
0047ad1a  30e4                  xor      ah, ah
0047ad1c  8d57ff                lea      edx, [edi - 1]
0047ad1f  88642408              mov      byte ptr [esp + 8], ah
0047ad23  6bc20c                imul     eax, edx, 0xc
0047ad26  eb04                  jmp      0x47ad2c
0047ad28  83e80c                sub      eax, 0xc
0047ad2b  4a                    dec      edx
0047ad2c  85c0                  test     eax, eax
0047ad2e  7c2b                  jl       0x47ad5b
0047ad30  31db                  xor      ebx, ebx
0047ad32  668b98d0a95000        mov      bx, word ptr [eax + 0x50a9d0]
0047ad39  81fbffff0000          cmp      ebx, 0xffff
0047ad3f  75e7                  jne      0x47ad28
0047ad41  c644240801            mov      byte ptr [esp + 8], 1
0047ad46  668b91d0a95000        mov      dx, word ptr [ecx + 0x50a9d0]
0047ad4d  668990d0a95000        mov      word ptr [eax + 0x50a9d0], dx
0047ad54  66ff0dcea95000        dec      word ptr [0x50a9ce]
0047ad5b  807c240800            cmp      byte ptr [esp + 8], 0
0047ad60  7597                  jne      0x47acf9
0047ad62  83c40c                add      esp, 0xc
0047ad65  e9acfaffff            jmp      0x47a816
