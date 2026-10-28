; atributos_e_tile; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047622e  53                       push ebx
0047622f  31db                     xor ebx, ebx
00476231  6689c3                   mov bx, ax
00476234  a1a87d5000               mov eax, dword ptr [0x507da8]
00476239  081403                   or byte ptr [ebx + eax], dl
0047623c  5b                       pop ebx
0047623d  c3                       ret
0047623e  53                       push ebx
0047623f  8b1da87d5000             mov ebx, dword ptr [0x507da8]
00476245  25ffff0000               and eax, 0xffff
0047624a  f6d2                     not dl
0047624c  201403                   and byte ptr [ebx + eax], dl
0047624f  5b                       pop ebx
00476250  c3                       ret
00476251  53                       push ebx
00476252  8b1d707d5000             mov ebx, dword ptr [0x507d70]
00476258  25ffff0000               and eax, 0xffff
0047625d  66891443                 mov word ptr [ebx + eax*2], dx
00476261  5b                       pop ebx
00476262  c3                       ret
