; CreerSac: limite por próximo símbolo SBL, fim exclusivo 0x004760f3.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0047605d  53                       push     ebx
0047605e  51                       push     ecx
0047605f  56                       push     esi
00476060  89c3                     mov      ebx, eax
00476062  88d1                     mov      cl, dl
00476064  31c0                     xor      eax, eax
00476066  8b35747d5000             mov      esi, dword ptr [0x507d74]
0047606c  6689d8                   mov      ax, bx
0047606f  88ca                     mov      dl, cl
00476071  01f0                     add      eax, esi
00476073  80c242                   add      dl, 0x42
00476076  8a30                     mov      dh, byte ptr [eax]
00476078  38f2                     cmp      dl, dh
0047607a  740d                     je       0x476089
0047607c  88f0                     mov      al, dh
0047607e  25ff000000               and      eax, 0xff
00476083  0f8571fbffff             jne      0x475bfa
00476089  a1747d5000               mov      eax, dword ptr [0x507d74]
0047608e  81e3ffff0000             and      ebx, 0xffff
00476094  8a0403                   mov      al, byte ptr [ebx + eax]
00476097  25ff000000               and      eax, 0xff
0047609c  7515                     jne      0x4760b3
0047609e  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004760a3  c6040301                 mov      byte ptr [ebx + eax], 1
004760a7  a1747d5000               mov      eax, dword ptr [0x507d74]
004760ac  881403                   mov      byte ptr [ebx + eax], dl
004760af  5e                       pop      esi
004760b0  59                       pop      ecx
004760b1  5b                       pop      ebx
004760b2  c3                       ret
004760b3  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004760b8  fe0403                   inc      byte ptr [ebx + eax]
004760bb  a1ac7d5000               mov      eax, dword ptr [0x507dac]
004760c0  01d8                     add      eax, ebx
004760c2  0fb630                   movzx    esi, byte ptr [eax]
004760c5  83fe1f                   cmp      esi, 0x1f
004760c8  0f8e2cfbffff             jle      0x475bfa
004760ce  8a28                     mov      ch, byte ptr [eax]
004760d0  fecd                     dec      ch
004760d2  81e2ff000000             and      edx, 0xff
004760d8  8828                     mov      byte ptr [eax], ch
004760da  89d8                     mov      eax, ebx
004760dc  e8cef6ffff               call     0x4757af
004760e1  81e1ff000000             and      ecx, 0xff
004760e7  25ffff0000               and      eax, 0xffff
004760ec  89c3                     mov      ebx, eax
004760ee  e971ffffff               jmp      0x476064
