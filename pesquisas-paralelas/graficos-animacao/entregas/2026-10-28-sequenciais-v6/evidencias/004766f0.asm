; TerrainEstDecouvert [0x4766f0, 0x47670a)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004766f0  81e2ff000000           and      edx, 0xff
004766f6  25ffff0000             and      eax, 0xffff
004766fb  8b1495787d5000         mov      edx, dword ptr [edx*4 + 0x507d78]
00476702  f604021f               test     byte ptr [edx + eax], 0x1f
00476706  0f94c0                 sete     al
00476709  c3                     ret
