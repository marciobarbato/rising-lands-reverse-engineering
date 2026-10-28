; CaseEstIlluminee [0x47693a, 0x476951)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0047693a  81e2ff000000           and      edx, 0xff
00476940  25ffff0000             and      eax, 0xffff
00476945  8b1495887d5000         mov      edx, dword ptr [edx*4 + 0x507d88]
0047694c  e997fdffff             jmp      0x4766e8 ;
