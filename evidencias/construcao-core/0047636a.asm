; TerrainEstHerbe; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047636a  53                       push ebx
0047636b  52                       push edx
0047636c  31d2                     xor edx, edx
0047636e  6689c2                   mov dx, ax
00476371  8d1c12                   lea ebx, [edx + edx]
00476374  8b15707d5000             mov edx, dword ptr [0x507d70]
0047637a  668b141a                 mov dx, word ptr [edx + ebx]
0047637e  81e2ffff0000             and edx, 0xffff
00476384  81fa5d010000             cmp edx, 0x15d
0047638a  7c08                     jl 0x476394
0047638c  81fa9d010000             cmp edx, 0x19d
00476392  7c22                     jl 0x4763b6
00476394  8b15707d5000             mov edx, dword ptr [0x507d70]
0047639a  25ffff0000               and eax, 0xffff
0047639f  668b0442                 mov ax, word ptr [edx + eax*2]
004763a3  25ffff0000               and eax, 0xffff
004763a8  3d9d010000               cmp eax, 0x19d
004763ad  7c0c                     jl 0x4763bb
004763af  3da5010000               cmp eax, 0x1a5
004763b4  7d05                     jge 0x4763bb
004763b6  b001                     mov al, 1
004763b8  5a                       pop edx
004763b9  5b                       pop ebx
004763ba  c3                       ret
004763bb  30c0                     xor al, al
004763bd  5a                       pop edx
004763be  5b                       pop ebx
004763bf  c3                       ret
