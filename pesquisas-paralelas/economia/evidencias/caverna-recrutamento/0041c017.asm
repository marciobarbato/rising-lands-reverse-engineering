; InitBatimentNeutre; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041c017  53                       push ebx
0041c018  51                       push ecx
0041c019  56                       push esi
0041c01a  57                       push edi
0041c01b  31ff                     xor edi, edi
0041c01d  6689c7                   mov di, ax
0041c020  89fe                     mov esi, edi
0041c022  c1e604                   shl esi, 4
0041c025  01fe                     add esi, edi
0041c027  c1e602                   shl esi, 2
0041c02a  01fe                     add esi, edi
0041c02c  c1e602                   shl esi, 2
0041c02f  81c6c8a04900             add esi, 0x49a0c8
0041c035  8a4608                   mov al, byte ptr [esi + 8]
0041c038  3c06                     cmp al, 6
0041c03a  0f823d010000             jb 0x41c17d
0041c040  0f86f1000000             jbe 0x41c137
0041c046  3c12                     cmp al, 0x12
0041c048  0f8237010000             jb 0x41c185
0041c04e  760d                     jbe 0x41c05d
0041c050  3c14                     cmp al, 0x14
0041c052  0f840b010000             je 0x41c163
0041c058  5f                       pop edi
0041c059  5e                       pop esi
0041c05a  59                       pop ecx
0041c05b  5b                       pop ebx
0041c05c  c3                       ret
0041c05d  31db                     xor ebx, ebx
0041c05f  88d3                     mov bl, dl
0041c061  89d8                     mov eax, ebx
0041c063  e8e75c0200               call 0x441d4f
0041c068  fe8b4cfb4d00             dec byte ptr [ebx + 0x4dfb4c]
0041c06e  31c0                     xor eax, eax
0041c070  8a4604                   mov al, byte ptr [esi + 4]
0041c073  ba10000000               mov edx, 0x10
0041c078  0fb6b04cfb4d00           movzx esi, byte ptr [eax + 0x4dfb4c]
0041c07f  e80ead0300               call 0x456d92
0041c084  25ffff0000               and eax, 0xffff
0041c089  39c6                     cmp esi, eax
0041c08b  0f8ff4000000             jg 0x41c185
0041c091  89de                     mov esi, ebx
0041c093  c1e603                   shl esi, 3
0041c096  01de                     add esi, ebx
0041c098  c1e604                   shl esi, 4
0041c09b  29de                     sub esi, ebx
0041c09d  c1e604                   shl esi, 4
0041c0a0  81c6e8d64d00             add esi, 0x4dd6e8
0041c0a6  81c650070000             add esi, 0x750
0041c0ac  ba01000000               mov edx, 1
0041c0b1  89f0                     mov eax, esi
0041c0b3  bb10000000               mov ebx, 0x10
0041c0b8  e88bb00200               call 0x447148
0041c0bd  ba06000000               mov edx, 6
0041c0c2  89f0                     mov eax, esi
0041c0c4  e821b20200               call 0x4472ea
0041c0c9  5f                       pop edi
0041c0ca  5e                       pop esi
0041c0cb  59                       pop ecx
0041c0cc  5b                       pop ebx
0041c0cd  c3                       ret
0041c0ce  31db                     xor ebx, ebx
0041c0d0  88d3                     mov bl, dl
0041c0d2  89d8                     mov eax, ebx
0041c0d4  c1e002                   shl eax, 2
0041c0d7  29d8                     sub eax, ebx
0041c0d9  66ff0c452cfb4d00         dec word ptr [eax*2 + 0x4dfb2c]
0041c0e1  31c0                     xor eax, eax
0041c0e3  8a4605                   mov al, byte ptr [esi + 5]
0041c0e6  83f803                   cmp eax, 3
0041c0e9  0f8496000000             je 0x41c185
0041c0ef  6a00                     push 0
0041c0f1  668b4602                 mov ax, word ptr [esi + 2]
0041c0f5  31db                     xor ebx, ebx
0041c0f7  0502020000               add eax, 0x202
0041c0fc  89fa                     mov edx, edi
0041c0fe  6689c3                   mov bx, ax
0041c101  31c0                     xor eax, eax
0041c103  31c9                     xor ecx, ecx
0041c105  a0b8fa4d00               mov al, byte ptr [0x4dfab8]
0041c10a  e87bfaffff               call 0x41bb8a
0041c10f  6a00                     push 0
0041c111  668b4602                 mov ax, word ptr [esi + 2]
0041c115  31db                     xor ebx, ebx
0041c117  0502020000               add eax, 0x202
0041c11c  b901000000               mov ecx, 1
0041c121  6689c3                   mov bx, ax
0041c124  31c0                     xor eax, eax
0041c126  89fa                     mov edx, edi
0041c128  a0b8fa4d00               mov al, byte ptr [0x4dfab8]
0041c12d  e858faffff               call 0x41bb8a
0041c132  5f                       pop edi
0041c133  5e                       pop esi
0041c134  59                       pop ecx
0041c135  5b                       pop ebx
0041c136  c3                       ret
0041c137  0fb6f2                   movzx esi, dl
0041c13a  8a9648fb4d00             mov dl, byte ptr [esi + 0x4dfb48]
0041c140  31c0                     xor eax, eax
0041c142  feca                     dec dl
0041c144  88d0                     mov al, dl
0041c146  889648fb4d00             mov byte ptr [esi + 0x4dfb48], dl
0041c14c  85c0                     test eax, eax
0041c14e  7535                     jne 0x41c185
0041c150  89f0                     mov eax, esi
0041c152  e873880500               call 0x4749ca
0041c157  89f0                     mov eax, esi
0041c159  e8da880500               call 0x474a38
0041c15e  5f                       pop edi
0041c15f  5e                       pop esi
0041c160  59                       pop ecx
0041c161  5b                       pop ebx
0041c162  c3                       ret
0041c163  c6467a00                 mov byte ptr [esi + 0x7a], 0
0041c167  c6860401000000           mov byte ptr [esi + 0x104], 0
0041c16e  c7860801000001000000     mov dword ptr [esi + 0x108], 1
0041c178  5f                       pop edi
0041c179  5e                       pop esi
0041c17a  59                       pop ecx
0041c17b  5b                       pop ebx
0041c17c  c3                       ret
0041c17d  3c03                     cmp al, 3
0041c17f  0f8449ffffff             je 0x41c0ce
0041c185  5f                       pop edi
0041c186  5e                       pop esi
0041c187  59                       pop ecx
0041c188  5b                       pop ebx
0041c189  c3                       ret
