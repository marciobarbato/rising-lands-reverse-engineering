; DDFlipPagePreparaImpacto; intervalo [0x0043f14f, 0x0043f247)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0043f14f  53                       push     ebx
0043f150  51                       push     ecx
0043f151  52                       push     edx
0043f152  56                       push     esi
0043f153  57                       push     edi
0043f154  55                       push     ebp
0043f155  83ec14                   sub      esp, 0x14
0043f158  88442410                 mov      byte ptr [esp + 0x10], al
0043f15c  31db                     xor      ebx, ebx
0043f15e  8a1d44fb4d00             mov      bl, byte ptr [0x4dfb44]
0043f164  30c0                     xor      al, al
0043f166  85db                     test     ebx, ebx
0043f168  743c                     je       0x43f1a6
0043f16a  8a0d181d4e00             mov      cl, byte ptr [0x4e1d18]
0043f170  31d2                     xor      edx, edx
0043f172  88ca                     mov      dl, cl
0043f174  8a92181c4e00             mov      dl, byte ptr [edx + 0x4e1c18]
0043f17a  81e2ff000000             and      edx, 0xff
0043f180  89d0                     mov      eax, edx
0043f182  c1fa1f                   sar      edx, 0x1f
0043f185  f7fb                     idiv     ebx
0043f187  88d0                     mov      al, dl
0043f189  fec1                     inc      cl
0043f18b  8a257c8f5000             mov      ah, byte ptr [0x508f7c]
0043f191  880d181d4e00             mov      byte ptr [0x4e1d18], cl
0043f197  f6c401                   test     ah, 1
0043f19a  750a                     jne      0x43f1a6
0043f19c  88da                     mov      dl, bl
0043f19e  feca                     dec      dl
0043f1a0  881544fb4d00             mov      byte ptr [0x4dfb44], dl
0043f1a6  31d2                     xor      edx, edx
0043f1a8  668b1518a04900           mov      dx, word ptr [0x49a018]
0043f1af  81fa20030000             cmp      edx, 0x320
0043f1b5  753d                     jne      0x43f1f4
0043f1b7  8b158d8f5000             mov      edx, dword ptr [0x508f8d]
0043f1bd  c1fa18                   sar      edx, 0x18
0043f1c0  c1e205                   shl      edx, 5
0043f1c3  891424                   mov      dword ptr [esp], edx
0043f1c6  25ff000000               and      eax, 0xff
0043f1cb  01c2                     add      edx, eax
0043f1cd  31c0                     xor      eax, eax
0043f1cf  66a126875000             mov      ax, word ptr [0x508726]
0043f1d5  8b1c24                   mov      ebx, dword ptr [esp]
0043f1d8  c1e005                   shl      eax, 5
0043f1db  29d8                     sub      eax, ebx
0043f1dd  8944240c                 mov      dword ptr [esp + 0xc], eax
0043f1e1  31c0                     xor      eax, eax
0043f1e3  66a124875000             mov      ax, word ptr [0x508724]
0043f1e9  c1e005                   shl      eax, 5
0043f1ec  29d8                     sub      eax, ebx
0043f1ee  89542404                 mov      dword ptr [esp + 4], edx
0043f1f2  eb28                     jmp      0x43f21c
0043f1f4  31d2                     xor      edx, edx
0043f1f6  891424                   mov      dword ptr [esp], edx
0043f1f9  25ff000000               and      eax, 0xff
0043f1fe  89442404                 mov      dword ptr [esp + 4], eax
0043f202  31c0                     xor      eax, eax
0043f204  66a126875000             mov      ax, word ptr [0x508726]
0043f20a  c1e005                   shl      eax, 5
0043f20d  8944240c                 mov      dword ptr [esp + 0xc], eax
0043f211  31c0                     xor      eax, eax
0043f213  66a124875000             mov      ax, word ptr [0x508724]
0043f219  c1e005                   shl      eax, 5
0043f21c  89442408                 mov      dword ptr [esp + 8], eax
0043f220  6a10                     push     0x10
0043f222  8d5c2404                 lea      ebx, [esp + 4]
0043f226  53                       push     ebx
0043f227  8b1d8d8f5000             mov      ebx, dword ptr [0x508f8d]
0043f22d  8b3590174e00             mov      esi, dword ptr [0x4e1790]
0043f233  c1fb18                   sar      ebx, 0x18
0043f236  56                       push     esi
0043f237  c1e305                   shl      ebx, 5
0043f23a  53                       push     ebx
0043f23b  a18c174e00               mov      eax, dword ptr [0x4e178c]
0043f240  53                       push     ebx
0043f241  8b10                     mov      edx, dword ptr [eax]
0043f243  50                       push     eax
0043f244  ff521c                   call     dword ptr [edx + 0x1c]
