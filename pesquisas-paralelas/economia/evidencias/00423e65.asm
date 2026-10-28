; CalculNovaRecrute: limite por RET antes dos dados seguintes, fim exclusivo 0x00423eb2.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423e65  53                       push     ebx
00423e66  51                       push     ecx
00423e67  52                       push     edx
00423e68  31db                     xor      ebx, ebx
00423e6a  25ffff0000               and      eax, 0xffff
00423e6f  3dffff0000               cmp      eax, 0xffff
00423e74  7436                     je       0x423eac
00423e76  89c3                     mov      ebx, eax
00423e78  c1e004                   shl      eax, 4
00423e7b  01d8                     add      eax, ebx
00423e7d  c1e002                   shl      eax, 2
00423e80  01d8                     add      eax, ebx
00423e82  bbc8a04900               mov      ebx, 0x49a0c8
00423e87  8b9c8308010000           mov      ebx, dword ptr [ebx + eax*4 + 0x108]
00423e8e  89d8                     mov      eax, ebx
00423e90  c1e002                   shl      eax, 2
00423e93  29d8                     sub      eax, ebx
00423e95  31c9                     xor      ecx, ecx
00423e97  c1e003                   shl      eax, 3
00423e9a  31d2                     xor      edx, edx
00423e9c  01d8                     add      eax, ebx
00423e9e  668b0df05b4900           mov      cx, word ptr [0x495bf0]
00423ea5  c1e002                   shl      eax, 2
00423ea8  f7f1                     div      ecx
00423eaa  89c3                     mov      ebx, eax
00423eac  89d8                     mov      eax, ebx
00423eae  5a                       pop      edx
00423eaf  59                       pop      ecx
00423eb0  5b                       pop      ebx
00423eb1  c3                       ret
