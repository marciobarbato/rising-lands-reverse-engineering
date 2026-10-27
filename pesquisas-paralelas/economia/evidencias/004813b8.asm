; B_TestStock: limite por próximo símbolo SBL, fim exclusivo 0x00481400.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
004813b8  53                       push     ebx
004813b9  51                       push     ecx
004813ba  52                       push     edx
004813bb  56                       push     esi
004813bc  83ec08                   sub      esp, 8
004813bf  89c6                     mov      esi, eax
004813c1  31c0                     xor      eax, eax
004813c3  8d4c2406                 lea      ecx, [esp + 6]
004813c7  8a461c                   mov      al, byte ptr [esi + 0x1c]
004813ca  8d5c2404                 lea      ebx, [esp + 4]
004813ce  50                       push     eax
004813cf  8d542406                 lea      edx, [esp + 6]
004813d3  8d442404                 lea      eax, [esp + 4]
004813d7  e8c162feff               call     0x46769d
004813dc  8b06                     mov      eax, dword ptr [esi]
004813de  668b0444                 mov      ax, word ptr [esp + eax*2]
004813e2  25ffff0000               and      eax, 0xffff
004813e7  3b4604                   cmp      eax, dword ptr [esi + 4]
004813ea  7c0d                     jl       0x4813f9
004813ec  b801000000               mov      eax, 1
004813f1  83c408                   add      esp, 8
004813f4  5e                       pop      esi
004813f5  5a                       pop      edx
004813f6  59                       pop      ecx
004813f7  5b                       pop      ebx
004813f8  c3                       ret
004813f9  b8ffffffff               mov      eax, 0xffffffff
004813fe  ebf1                     jmp      0x4813f1
