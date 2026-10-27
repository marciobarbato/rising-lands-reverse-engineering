; TerrainRetireMatiere: limite por próximo símbolo SBL, fim exclusivo 0x004766b1.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00476662  53                       push     ebx
00476663  51                       push     ecx
00476664  52                       push     edx
00476665  56                       push     esi
00476666  89c3                     mov      ebx, eax
00476668  31c9                     xor      ecx, ecx
0047666a  6689c1                   mov      cx, ax
0047666d  a1ac7d5000               mov      eax, dword ptr [0x507dac]
00476672  01c8                     add      eax, ecx
00476674  0fb630                   movzx    esi, byte ptr [eax]
00476677  30d2                     xor      dl, dl
00476679  85f6                     test     esi, esi
0047667b  740d                     je       0x47668a
0047667d  fe08                     dec      byte ptr [eax]
0047667f  a1747d5000               mov      eax, dword ptr [0x507d74]
00476684  8a1401                   mov      dl, byte ptr [ecx + eax]
00476687  80ea42                   sub      dl, 0x42
0047668a  31c0                     xor      eax, eax
0047668c  8b0dac7d5000             mov      ecx, dword ptr [0x507dac]
00476692  6689d8                   mov      ax, bx
00476695  8a0c01                   mov      cl, byte ptr [ecx + eax]
00476698  81e1ff000000             and      ecx, 0xff
0047669e  750a                     jne      0x4766aa
004766a0  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
004766a6  c6040100                 mov      byte ptr [ecx + eax], 0
004766aa  88d0                     mov      al, dl
004766ac  5e                       pop      esi
004766ad  5a                       pop      edx
004766ae  59                       pop      ecx
004766af  5b                       pop      ebx
004766b0  c3                       ret
