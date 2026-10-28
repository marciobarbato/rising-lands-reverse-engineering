; CalculGamePortaoEOrdem; intervalo [0x0042d3c0, 0x0042d418)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0042d3c0  8a25782f4e00             mov      ah, byte ptr [0x4e2f78]
0042d3c6  80fc12                   cmp      ah, 0x12
0042d3c9  7416                     je       0x42d3e1
0042d3cb  80fc10                   cmp      ah, 0x10
0042d3ce  0f850e010000             jne      0x42d4e2
0042d3d4  a030074e00               mov      al, byte ptr [0x4e0730]
0042d3d9  84c0                     test     al, al
0042d3db  0f8401010000             je       0x42d4e2
0042d3e1  e8e8c90300               call     0x469dce
0042d3e6  e82afc0200               call     0x45d015
0042d3eb  e854150300               call     0x45e944
0042d3f0  e81a280400               call     0x46fc0f
0042d3f5  e8bb990200               call     0x456db5
0042d3fa  e8c8adffff               call     0x4281c7
0042d3ff  e8583e0400               call     0x47125c
0042d404  e832060400               call     0x46da3b
0042d409  e81a7f0400               call     0x475328
0042d40e  e8f3b30400               call     0x478806
0042d413  e800a30300               call     0x467718
