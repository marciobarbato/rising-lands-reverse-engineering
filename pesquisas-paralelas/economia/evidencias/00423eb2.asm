; corpo_compartilhado_de_CalculStatusRecrute: limite por trecho auxiliar até RET; não é uma função independente, fim exclusivo 0x00423f83.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00423eb2  8b988c000000             mov      ebx, dword ptr [eax + 0x8c]
00423eb8  31c0                     xor      eax, eax
00423eba  88f0                     mov      al, dh
00423ebc  31c9                     xor      ecx, ecx
00423ebe  e8f4d10100               call     0x4410b7
00423ec3  6689c1                   mov      cx, ax
00423ec6  31d2                     xor      edx, edx
00423ec8  89d8                     mov      eax, ebx
00423eca  f7f1                     div      ecx
00423ecc  89c3                     mov      ebx, eax
00423ece  89d8                     mov      eax, ebx
00423ed0  59                       pop      ecx
00423ed1  5b                       pop      ebx
00423ed2  c3                       ret
00423ed3  8b988c000000             mov      ebx, dword ptr [eax + 0x8c]
00423ed9  31c0                     xor      eax, eax
00423edb  88f0                     mov      al, dh
00423edd  31c9                     xor      ecx, ecx
00423edf  e886080500               call     0x47476a
00423ee4  ebdd                     jmp      0x423ec3
00423ee6  8b988c000000             mov      ebx, dword ptr [eax + 0x8c]
00423eec  668b8088000000           mov      ax, word ptr [eax + 0x88]
00423ef3  25ffff0000               and      eax, 0xffff
00423ef8  e80bd20100               call     0x441108
00423efd  31c9                     xor      ecx, ecx
00423eff  31d2                     xor      edx, edx
00423f01  6689c1                   mov      cx, ax
00423f04  ebc2                     jmp      0x423ec8
00423f06  8a507a                   mov      dl, byte ptr [eax + 0x7a]
00423f09  8b988c000000             mov      ebx, dword ptr [eax + 0x8c]
00423f0f  84d2                     test     dl, dl
00423f11  75d9                     jne      0x423eec
00423f13  eba3                     jmp      0x423eb8
00423f15  89c8                     mov      eax, ecx
00423f17  c1e004                   shl      eax, 4
00423f1a  01c8                     add      eax, ecx
00423f1c  c1e002                   shl      eax, 2
00423f1f  01c8                     add      eax, ecx
00423f21  c1e002                   shl      eax, 2
00423f24  05c8a04900               add      eax, 0x49a0c8
00423f29  8a5008                   mov      dl, byte ptr [eax + 8]
00423f2c  80fa0e                   cmp      dl, 0xe
00423f2f  7226                     jb       0x423f57
00423f31  76b3                     jbe      0x423ee6
00423f33  80fa10                   cmp      dl, 0x10
00423f36  0f8276ffffff             jb       0x423eb2
00423f3c  0f8670ffffff             jbe      0x423eb2
00423f42  80fa12                   cmp      dl, 0x12
00423f45  7237                     jb       0x423f7e
00423f47  76bd                     jbe      0x423f06
00423f49  80fa14                   cmp      dl, 0x14
00423f4c  0f8460ffffff             je       0x423eb2
00423f52  89d8                     mov      eax, ebx
00423f54  59                       pop      ecx
00423f55  5b                       pop      ebx
00423f56  c3                       ret
00423f57  80fa05                   cmp      dl, 5
00423f5a  7214                     jb       0x423f70
00423f5c  0f8650ffffff             jbe      0x423eb2
00423f62  80fa06                   cmp      dl, 6
00423f65  0f8668ffffff             jbe      0x423ed3
00423f6b  80fa0d                   cmp      dl, 0xd
00423f6e  ebdc                     jmp      0x423f4c
00423f70  80fa01                   cmp      dl, 1
00423f73  7209                     jb       0x423f7e
00423f75  80fa02                   cmp      dl, 2
00423f78  0f8634ffffff             jbe      0x423eb2
00423f7e  89d8                     mov      eax, ebx
00423f80  59                       pop      ecx
00423f81  5b                       pop      ebx
00423f82  c3                       ret
