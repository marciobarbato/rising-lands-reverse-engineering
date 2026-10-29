; SetTerrain; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476251  53                       push ebx
00476252  8b1d707d5000             mov ebx, dword ptr [0x507d70]
00476258  25ffff0000               and eax, 0xffff
0047625d  66891443                 mov word ptr [ebx + eax*2], dx
00476261  5b                       pop ebx
00476262  c3                       ret
