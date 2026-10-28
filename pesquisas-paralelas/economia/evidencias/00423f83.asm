; GetStatusRecrute: limite por próximo símbolo SBL, fim exclusivo 0x00423f9d.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423f83  88d4                     mov      ah, dl
00423f85  31d2                     xor      edx, edx
00423f87  88c2                     mov      dl, al
00423f89  88e0                     mov      al, ah
00423f8b  25ff000000               and      eax, 0xff
00423f90  668b0445e05b4900         mov      ax, word ptr [eax*2 + 0x495be0]
00423f98  25ffff0000               and      eax, 0xffff
