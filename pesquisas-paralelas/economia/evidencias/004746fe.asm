; SortilegeGetCoutApprentissage: limite por próximo símbolo SBL, fim exclusivo 0x00474734.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004746fe  56                       push     esi
004746ff  89de                     mov      esi, ebx
00474701  31db                     xor      ebx, ebx
00474703  88c3                     mov      bl, al
00474705  89d8                     mov      eax, ebx
00474707  c1e002                   shl      eax, 2
0047470a  29d8                     sub      eax, ebx
0047470c  c1e003                   shl      eax, 3
0047470f  29d8                     sub      eax, ebx
00474711  668b1c4578714900         mov      bx, word ptr [eax*2 + 0x497178]
00474719  66891a                   mov      word ptr [edx], bx
0047471c  668b144576714900         mov      dx, word ptr [eax*2 + 0x497176]
00474724  668916                   mov      word ptr [esi], dx
00474727  668b04457a714900         mov      ax, word ptr [eax*2 + 0x49717a]
0047472f  668901                   mov      word ptr [ecx], ax
00474732  5e                       pop      esi
00474733  c3                       ret
