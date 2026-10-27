; BatimentGetRessource: limite por RET antes dos dados seguintes, fim exclusivo 0x0041ab04.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0041aace  56                       push     esi
0041aacf  89de                     mov      esi, ebx
0041aad1  31db                     xor      ebx, ebx
0041aad3  88c3                     mov      bl, al
0041aad5  89d8                     mov      eax, ebx
0041aad7  c1e002                   shl      eax, 2
0041aada  29d8                     sub      eax, ebx
0041aadc  c1e002                   shl      eax, 2
0041aadf  01d8                     add      eax, ebx
0041aae1  668b1c85985d4900         mov      bx, word ptr [eax*4 + 0x495d98]
0041aae9  66891a                   mov      word ptr [edx], bx
0041aaec  668b14859a5d4900         mov      dx, word ptr [eax*4 + 0x495d9a]
0041aaf4  668916                   mov      word ptr [esi], dx
0041aaf7  668b04859c5d4900         mov      ax, word ptr [eax*4 + 0x495d9c]
0041aaff  668901                   mov      word ptr [ecx], ax
0041ab02  5e                       pop      esi
0041ab03  c3                       ret
