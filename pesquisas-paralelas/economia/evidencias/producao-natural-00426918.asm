; BatimentNextEtape: Branch for types 1/2/13/16: inline BatimentEstHabiter, then CalculTroupe; exclusive end 0x0042698d.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00426918  31d2                     xor      edx, edx
0042691a  6689fa                   mov      dx, di
0042691d  89d0                     mov      eax, edx
0042691f  c1e004                   shl      eax, 4
00426922  01d0                     add      eax, edx
00426924  c1e002                   shl      eax, 2
00426927  01d0                     add      eax, edx
00426929  bac8a04900               mov      edx, 0x49a0c8
0042692e  c1e002                   shl      eax, 2
00426931  01c2                     add      edx, eax
00426933  31db                     xor      ebx, ebx
00426935  8a4208                   mov      al, byte ptr [edx + 8]
00426938  88c3                     mov      bl, al
0042693a  8d420c                   lea      eax, [edx + 0xc]
0042693d  83fb15                   cmp      ebx, 0x15
00426940  750d                     jne      0x42694f
00426942  e803090200               call     0x44724a
00426947  84c0                     test     al, al
00426949  7429                     je       0x426974
0042694b  b001                     mov      al, 1
0042694d  eb27                     jmp      0x426976
0042694f  83fb02                   cmp      ebx, 2
00426952  7509                     jne      0x42695d
00426954  e8f1080200               call     0x44724a
00426959  84c0                     test     al, al
0042695b  75ee                     jne      0x42694b
0042695d  8d420c                   lea      eax, [edx + 0xc]
00426960  bb09000000               mov      ebx, 9
00426965  ba01000000               mov      edx, 1
0042696a  e849080200               call     0x4471b8
0042696f  6685c0                   test     ax, ax
00426972  ebd5                     jmp      0x426949
00426974  30c0                     xor      al, al
00426976  84c0                     test     al, al
00426978  0f8442180000             je       0x4281c0
0042697e  31c0                     xor      eax, eax
00426980  6689f8                   mov      ax, di
00426983  e85ef0ffff               call     0x4259e6
00426988  e933180000               jmp      0x4281c0
