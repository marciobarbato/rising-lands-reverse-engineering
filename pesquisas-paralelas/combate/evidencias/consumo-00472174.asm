; EnginEstSelectionne; [0x00472174, 0x004721a8)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00472174  53                       push     ebx
00472175  88c3                     mov      bl, al
00472177  81e2ffff0000             and      edx, 0xffff
0047217d  89d0                     mov      eax, edx
0047217f  c1e004                   shl      eax, 4
00472182  01d0                     add      eax, edx
00472184  c1e002                   shl      eax, 2
00472187  01c2                     add      edx, eax
00472189  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
0047218e  c1e202                   shl      edx, 2
00472191  01d0                     add      eax, edx
00472193  80b8bd00000000           cmp      byte ptr [eax + 0xbd], 0
0047219a  7408                     je       0x4721a4
0047219c  3a18                     cmp      bl, byte ptr [eax]
0047219e  7504                     jne      0x4721a4
004721a0  b001                     mov      al, 1
004721a2  5b                       pop      ebx
004721a3  c3                       ret
004721a4  30c0                     xor      al, al
004721a6  5b                       pop      ebx
004721a7  c3                       ret
