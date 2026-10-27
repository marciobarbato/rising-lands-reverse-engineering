; carregador_atributos: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0044188b  53                    push     ebx
0044188c  51                    push     ecx
0044188d  52                    push     edx
0044188e  56                    push     esi
0044188f  57                    push     edi
00441890  55                    push     ebp
00441891  89e5                  mov      ebp, esp
00441893  83ec04                sub      esp, 4
00441896  68948f5000            push     0x508f94
0044189b  6a02                  push     2
0044189d  680a484900            push     0x49480a ; 'BONUSCAPITAINE'
004418a2  6819484900            push     0x494819 ; 'DIVERS'
004418a7  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004418ae  66a3ac654900          mov      word ptr [0x4965ac], ax
004418b4  b81a000000            mov      eax, 0x1a
004418b9  31d2                  xor      edx, edx
004418bb  e8d2feffff            call     0x441792 ; carregador_danos
004418c0  668955fc              mov      word ptr [ebp - 4], dx
004418c4  eb6c                  jmp      0x441932
004418c6  56                    push     esi
004418c7  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004418ce  68948f5000            push     0x508f94
004418d3  6a01                  push     1
004418d5  685e484900            push     0x49485e ; 'COUTROCHE'
004418da  56                    push     esi
004418db  668983b0654900        mov      word ptr [ebx + 0x4965b0], ax
004418e2  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004418e9  68948f5000            push     0x508f94
004418ee  6a01                  push     1
004418f0  6868484900            push     0x494868 ; 'COUTPIECE'
004418f5  56                    push     esi
004418f6  668983b4654900        mov      word ptr [ebx + 0x4965b4], ax
004418fd  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
00441904  668983b2654900        mov      word ptr [ebx + 0x4965b2], ax
0044190b  b8ae654900            mov      eax, 0x4965ae
00441910  68948f5000            push     0x508f94
00441915  01d8                  add      eax, ebx
00441917  6a1e                  push     0x1e
00441919  83c00c                add      eax, 0xc
0044191c  50                    push     eax
0044191d  56                    push     esi
0044191e  89fb                  mov      ebx, edi
00441920  6872484900            push     0x494872 ; 'NAME'
00441925  43                    inc      ebx
00441926  56                    push     esi
00441927  66895dfc              mov      word ptr [ebp - 4], bx
0044192b  2eff15b0315200        call     dword ptr cs:[0x5231b0] ; KERNEL32.dll!GetPrivateProfileStringA
00441932  31ff                  xor      edi, edi
00441934  668b7dfc              mov      di, word ptr [ebp - 4]
00441938  83ff1a                cmp      edi, 0x1a
0044193b  0f8d1fd10000          jge      0x44ea60
00441941  31db                  xor      ebx, ebx
00441943  8a5dfc                mov      bl, byte ptr [ebp - 4]
00441946  89d8                  mov      eax, ebx
00441948  6bdb32                imul     ebx, ebx, 0x32
0044194b  81c3ae654900          add      ebx, 0x4965ae
00441951  8d730c                lea      esi, [ebx + 0xc]
00441954  6bdf32                imul     ebx, edi, 0x32
00441957  e836feffff            call     0x441792 ; carregador_danos
0044195c  68948f5000            push     0x508f94
00441961  6a05                  push     5
00441963  6820484900            push     0x494820 ; 'BLINDAGE'
00441968  56                    push     esi
00441969  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
00441970  68948f5000            push     0x508f94
00441975  6a05                  push     5
00441977  6829484900            push     0x494829 ; 'RAYON'
0044197c  56                    push     esi
0044197d  8883b9654900          mov      byte ptr [ebx + 0x4965b9], al
00441983  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
0044198a  68948f5000            push     0x508f94
0044198f  6a01                  push     1
00441991  682f484900            push     0x49482f ; 'PORTEE'
00441996  56                    push     esi
00441997  668983d8654900        mov      word ptr [ebx + 0x4965d8], ax
0044199e  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004419a5  668983da654900        mov      word ptr [ebx + 0x4965da], ax
004419ac  0fafc0                imul     eax, eax
004419af  68948f5000            push     0x508f94
004419b4  68b80b0000            push     0xbb8
004419b9  6836484900            push     0x494836 ; 'FATIGUE'
004419be  56                    push     esi
004419bf  668983da654900        mov      word ptr [ebx + 0x4965da], ax
004419c6  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004419cd  68948f5000            push     0x508f94
004419d2  6a64                  push     0x64
004419d4  683e484900            push     0x49483e ; 'RECHARGE'
004419d9  56                    push     esi
004419da  668983dc654900        mov      word ptr [ebx + 0x4965dc], ax
004419e1  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
004419e8  68948f5000            push     0x508f94
004419ed  6a78                  push     0x78
004419ef  6847484900            push     0x494847 ; 'TMPSRECRUTE'
004419f4  56                    push     esi
004419f5  668983de654900        mov      word ptr [ebx + 0x4965de], ax
004419fc  2eff15ac315200        call     dword ptr cs:[0x5231ac] ; KERNEL32.dll!GetPrivateProfileIntA
00441a03  68948f5000            push     0x508f94
00441a08  6a01                  push     1
00441a0a  668983ae654900        mov      word ptr [ebx + 0x4965ae], ax
00441a11  6853484900            push     0x494853 ; 'COUTPATATE'
00441a16  e9abfeffff            jmp      0x4418c6
