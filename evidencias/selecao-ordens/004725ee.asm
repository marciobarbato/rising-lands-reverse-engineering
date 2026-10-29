; SelectionAddEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004725ee  53                       push ebx
004725ef  89c3                     mov ebx, eax
004725f1  31c0                     xor eax, eax
004725f3  88d0                     mov al, dl
004725f5  c1e009                   shl eax, 9
004725f8  31d2                     xor edx, edx
004725fa  668b9028875000           mov dx, word ptr [eax + 0x508728]
00472601  81faff000000             cmp edx, 0xff
00472607  7d3b                     jge 0x472644
00472609  42                       inc edx
0047260a  66899028875000           mov word ptr [eax + 0x508728], dx
00472611  81e2ffff0000             and edx, 0xffff
00472617  66899c5028875000         mov word ptr [eax + edx*2 + 0x508728], bx
0047261f  31d2                     xor edx, edx
00472621  6689da                   mov dx, bx
00472624  89d0                     mov eax, edx
00472626  c1e004                   shl eax, 4
00472629  01d0                     add eax, edx
0047262b  c1e002                   shl eax, 2
0047262e  01c2                     add edx, eax
00472630  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00472635  c1e202                   shl edx, 2
00472638  c68402bd00000001         mov byte ptr [edx + eax + 0xbd], 1
00472640  b001                     mov al, 1
00472642  5b                       pop ebx
00472643  c3                       ret
00472644  30c0                     xor al, al
00472646  5b                       pop ebx
00472647  c3                       ret
