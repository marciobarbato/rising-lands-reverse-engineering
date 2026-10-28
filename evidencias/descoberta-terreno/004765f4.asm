; TerrainGetColor; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004765f4  53                       push ebx
004765f5  52                       push edx
004765f6  31db                     xor ebx, ebx
004765f8  8b15747d5000             mov edx, dword ptr [0x507d74]
004765fe  6689c3                   mov bx, ax
00476601  8a141a                   mov dl, byte ptr [edx + ebx]
00476604  81e2ff000000             and edx, 0xff
0047660a  83fa1d                   cmp edx, 0x1d
0047660d  7c09                     jl 0x476618
0047660f  83fa35                   cmp edx, 0x35
00476612  7d04                     jge 0x476618
00476614  b201                     mov dl, 1
00476616  eb02                     jmp 0x47661a
00476618  30d2                     xor dl, dl
0047661a  84d2                     test dl, dl
0047661c  7405                     je 0x476623
0047661e  b01e                     mov al, 0x1e
00476620  5a                       pop edx
00476621  5b                       pop ebx
00476622  c3                       ret
00476623  8b15707d5000             mov edx, dword ptr [0x507d70]
00476629  25ffff0000               and eax, 0xffff
0047662e  668b0442                 mov ax, word ptr [edx + eax*2]
00476632  25ffff0000               and eax, 0xffff
00476637  3dbe020000               cmp eax, 0x2be
0047663c  7de0                     jge 0x47661e
0047663e  8a8094965000             mov al, byte ptr [eax + 0x509694]
00476644  5a                       pop edx
00476645  5b                       pop ebx
00476646  c3                       ret
