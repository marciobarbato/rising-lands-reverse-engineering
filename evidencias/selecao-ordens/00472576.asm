; RetireSelectionEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00472576  53                       push ebx
00472577  51                       push ecx
00472578  56                       push esi
00472579  57                       push edi
0047257a  83ec04                   sub esp, 4
0047257d  89c6                     mov esi, eax
0047257f  81e2ff000000             and edx, 0xff
00472585  bb28875000               mov ebx, 0x508728
0047258a  c1e209                   shl edx, 9
0047258d  01d3                     add ebx, edx
0047258f  668b03                   mov ax, word ptr [ebx]
00472592  30c9                     xor cl, cl
00472594  890424                   mov dword ptr [esp], eax
00472597  b801000000               mov eax, 1
0047259c  eb27                     jmp 0x4725c5
0047259e  31d2                     xor edx, edx
004725a0  6689c2                   mov dx, ax
004725a3  663b3453                 cmp si, word ptr [ebx + edx*2]
004725a7  7502                     jne 0x4725ab
004725a9  b101                     mov cl, 1
004725ab  31d2                     xor edx, edx
004725ad  6689f2                   mov dx, si
004725b0  69fa14010000             imul edi, edx, 0x114
004725b6  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004725bc  c6843abd00000000         mov byte ptr [edx + edi + 0xbd], 0
004725c4  40                       inc eax
004725c5  663b0424                 cmp ax, word ptr [esp]
004725c9  7714                     ja 0x4725df
004725cb  84c9                     test cl, cl
004725cd  74cf                     je 0x47259e
004725cf  31d2                     xor edx, edx
004725d1  6689c2                   mov dx, ax
004725d4  668b3c53                 mov di, word ptr [ebx + edx*2]
004725d8  66897c53fe               mov word ptr [ebx + edx*2 - 2], di
004725dd  ebe5                     jmp 0x4725c4
004725df  84c9                     test cl, cl
004725e1  7403                     je 0x4725e6
004725e3  66ff0b                   dec word ptr [ebx]
004725e6  83c404                   add esp, 4
004725e9  5f                       pop edi
004725ea  5e                       pop esi
004725eb  59                       pop ecx
004725ec  5b                       pop ebx
004725ed  c3                       ret
