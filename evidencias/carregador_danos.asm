; carregador_danos: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00441792  53                    push     ebx
00441793  51                    push     ecx
00441794  52                    push     edx
00441795  56                    push     esi
00441796  55                    push     ebp
00441797  89e5                  mov      ebp, esp
00441799  81ec04010000          sub      esp, 0x104
0044179f  81ed86000000          sub      ebp, 0x86
004417a5  888582000000          mov      byte ptr [ebp + 0x82], al
004417ab  31db                  xor      ebx, ebx
004417ad  88c3                  mov      bl, al
004417af  83fb1a                cmp      ebx, 0x1a
004417b2  7d31                  jge      0x4417e5
004417b4  68948f5000            push     0x508f94
004417b9  68fa000000            push     0xfa
004417be  8d4582                lea      eax, [ebp - 0x7e]
004417c1  50                    push     eax
004417c2  89d8                  mov      eax, ebx
004417c4  c1e002                shl      eax, 2
004417c7  29d8                  sub      eax, ebx
004417c9  c1e003                shl      eax, 3
004417cc  01d8                  add      eax, ebx
004417ce  01c0                  add      eax, eax
004417d0  68f4474900            push     0x4947f4
004417d5  05ae654900            add      eax, 0x4965ae
004417da  68f5474900            push     0x4947f5 ; 'DEGAT'
004417df  83c00c                add      eax, 0xc
004417e2  50                    push     eax
004417e3  eb1d                  jmp      0x441802
004417e5  68948f5000            push     0x508f94
004417ea  68fa000000            push     0xfa
004417ef  8d4582                lea      eax, [ebp - 0x7e]
004417f2  50                    push     eax
004417f3  68fb474900            push     0x4947fb
004417f8  68fc474900            push     0x4947fc ; 'DEGAT'
004417fd  6802484900            push     0x494802 ; 'MINE'
00441802  2eff15b0315200        call     dword ptr cs:[0x5231b0] ; KERNEL32.dll!GetPrivateProfileStringA
00441809  31d2                  xor      edx, edx
0044180b  31c9                  xor      ecx, ecx
0044180d  eb15                  jmp      0x441824
0044180f  31c0                  xor      eax, eax
00441811  6689d0                mov      ax, dx
00441814  8b84287fffffff        mov      eax, dword ptr [eax + ebp - 0x81]
0044181b  c1f818                sar      eax, 0x18
0044181e  85c0                  test     eax, eax
00441820  7401                  je       0x441823
00441822  42                    inc      edx
00441823  41                    inc      ecx
00441824  31db                  xor      ebx, ebx
00441826  6689cb                mov      bx, cx
00441829  83fb1b                cmp      ebx, 0x1b
0044182c  7d51                  jge      0x44187f
0044182e  8d457e                lea      eax, [ebp + 0x7e]
00441831  50                    push     eax
00441832  31c0                  xor      eax, eax
00441834  8d7582                lea      esi, [ebp - 0x7e]
00441837  6689d0                mov      ax, dx
0044183a  6807484900            push     0x494807
0044183f  01f0                  add      eax, esi
00441841  50                    push     eax
00441842  e8d5ab0400            call     0x48c41c
00441847  31c0                  xor      eax, eax
00441849  8b359c194e00          mov      esi, dword ptr [0x4e199c]
0044184f  8a8582000000          mov      al, byte ptr [ebp + 0x82]
00441855  8b0486                mov      eax, dword ptr [esi + eax*4]
00441858  01c3                  add      ebx, eax
0044185a  8a457e                mov      al, byte ptr [ebp + 0x7e]
0044185d  83c40c                add      esp, 0xc
00441860  8803                  mov      byte ptr [ebx], al
00441862  31c0                  xor      eax, eax
00441864  6689d0                mov      ax, dx
00441867  8b9c287fffffff        mov      ebx, dword ptr [eax + ebp - 0x81]
0044186e  c1fb18                sar      ebx, 0x18
00441871  85db                  test     ebx, ebx
00441873  749a                  je       0x44180f
00441875  807c28822c            cmp      byte ptr [eax + ebp - 0x7e], 0x2c
0044187a  7493                  je       0x44180f
0044187c  42                    inc      edx
0044187d  ebe3                  jmp      0x441862
0044187f  8da586000000          lea      esp, [ebp + 0x86]
00441885  5d                    pop      ebp
00441886  5e                    pop      esi
00441887  5a                    pop      edx
00441888  59                    pop      ecx
00441889  5b                    pop      ebx
0044188a  c3                    ret
