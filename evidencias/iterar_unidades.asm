; iterar_unidades: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
00456db5  53                    push     ebx
00456db6  51                    push     ecx
00456db7  52                    push     edx
00456db8  56                    push     esi
00456db9  31d2                  xor      edx, edx
00456dbb  30c9                  xor      cl, cl
00456dbd  668915381a4e00        mov      word ptr [0x4e1a38], dx
00456dc4  6689153a1a4e00        mov      word ptr [0x4e1a3a], dx
00456dcb  31f6                  xor      esi, esi
00456dcd  eb28                  jmp      0x456df7
00456dcf  31db                  xor      ebx, ebx
00456dd1  88cb                  mov      bl, cl
00456dd3  6bdb34                imul     ebx, ebx, 0x34
00456dd6  40                    inc      eax
00456dd7  6689b4533c1a4e00      mov      word ptr [ebx + edx*2 + 0x4e1a3c], si
00456ddf  31d2                  xor      edx, edx
00456de1  6689c2                mov      dx, ax
00456de4  83fa1a                cmp      edx, 0x1a
00456de7  7ce6                  jl       0x456dcf
00456de9  31d2                  xor      edx, edx
00456deb  88ca                  mov      dl, cl
00456ded  fec1                  inc      cl
00456def  6689345528194e00      mov      word ptr [edx*2 + 0x4e1928], si
00456df7  31c0                  xor      eax, eax
00456df9  88c8                  mov      al, cl
00456dfb  83f804                cmp      eax, 4
00456dfe  7d04                  jge      0x456e04
00456e00  89f0                  mov      eax, esi
00456e02  ebdb                  jmp      0x456ddf
00456e04  31c9                  xor      ecx, ecx
00456e06  31db                  xor      ebx, ebx
00456e08  66890d30194e00        mov      word ptr [0x4e1930], cx
00456e0f  e99f000000            jmp      0x456eb3
00456e14  30c0                  xor      al, al
00456e16  84c0                  test     al, al
00456e18  0f848a000000          je       0x456ea8
00456e1e  31c0                  xor      eax, eax
00456e20  6689d8                mov      ax, bx
00456e23  69c014010000          imul     eax, eax, 0x114
00456e29  8b15a0194e00          mov      edx, dword ptr [0x4e19a0]
00456e2f  01c2                  add      edx, eax
00456e31  8a4201                mov      al, byte ptr [edx + 1]
00456e34  88c1                  mov      cl, al
00456e36  8a22                  mov      ah, byte ptr [edx]
00456e38  31d2                  xor      edx, edx
00456e3a  88e2                  mov      dl, ah
00456e3c  88e5                  mov      ch, ah
00456e3e  81fac8000000          cmp      edx, 0xc8
00456e44  7415                  je       0x456e5b
00456e46  83fa04                cmp      edx, 4
00456e49  7410                  je       0x456e5b
00456e4b  6bd234                imul     edx, edx, 0x34
00456e4e  25ff000000            and      eax, 0xff
00456e53  66ff84423c1a4e00      inc      word ptr [edx + eax*2 + 0x4e1a3c]
00456e5b  31d2                  xor      edx, edx
00456e5d  b801000000            mov      eax, 1
00456e62  6689da                mov      dx, bx
00456e65  e8938d0200            call     0x47fbfd
00456e6a  31c0                  xor      eax, eax
00456e6c  88c8                  mov      al, cl
00456e6e  83f811                cmp      eax, 0x11
00456e71  7418                  je       0x456e8b
00456e73  3a2d41805000          cmp      ch, byte ptr [0x508041]
00456e79  7409                  je       0x456e84
00456e7b  66ff05381a4e00        inc      word ptr [0x4e1a38]
00456e82  eb07                  jmp      0x456e8b
00456e84  66ff053a1a4e00        inc      word ptr [0x4e1a3a]
00456e8b  31d2                  xor      edx, edx
00456e8d  88ea                  mov      dl, ch
00456e8f  81fac8000000          cmp      edx, 0xc8
00456e95  7411                  je       0x456ea8
00456e97  31c0                  xor      eax, eax
00456e99  88c8                  mov      al, cl
00456e9b  83f805                cmp      eax, 5
00456e9e  7408                  je       0x456ea8
00456ea0  66ff045528194e00      inc      word ptr [edx*2 + 0x4e1928]
00456ea8  31c0                  xor      eax, eax
00456eaa  6689d8                mov      ax, bx
00456ead  e87ad5ffff            call     0x45442c
00456eb2  43                    inc      ebx
00456eb3  31c0                  xor      eax, eax
00456eb5  6689d8                mov      ax, bx
00456eb8  3d20030000            cmp      eax, 0x320
00456ebd  0f8ddaa8ffff          jge      0x45179d
00456ec3  69c014010000          imul     eax, eax, 0x114
00456ec9  8b15a0194e00          mov      edx, dword ptr [0x4e19a0]
00456ecf  8a440202              mov      al, byte ptr [edx + eax + 2]
00456ed3  25ff000000            and      eax, 0xff
00456ed8  0f95c0                setne    al
00456edb  84c0                  test     al, al
00456edd  74d3                  je       0x456eb2
00456edf  31c0                  xor      eax, eax
00456ee1  6689d8                mov      ax, bx
00456ee4  69c014010000          imul     eax, eax, 0x114
00456eea  8a540202              mov      dl, byte ptr [edx + eax + 2]
00456eee  81e2ff000000          and      edx, 0xff
00456ef4  0f841affffff          je       0x456e14
00456efa  83fa04                cmp      edx, 4
00456efd  0f8411ffffff          je       0x456e14
00456f03  b001                  mov      al, 1
00456f05  e90cffffff            jmp      0x456e16
