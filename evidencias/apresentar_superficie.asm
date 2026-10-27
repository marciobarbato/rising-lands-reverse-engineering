; apresentar_superficie: trecho estático, nomes atribuídos pela pesquisa.
; SHA-256 RISING.EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Endereços virtuais da imagem preferencial; fim exclusivo.
; As anotações não recuperam nomes originais nem comprovam execução.
0043f14f  53                    push     ebx
0043f150  51                    push     ecx
0043f151  52                    push     edx
0043f152  56                    push     esi
0043f153  57                    push     edi
0043f154  55                    push     ebp
0043f155  83ec14                sub      esp, 0x14
0043f158  88442410              mov      byte ptr [esp + 0x10], al
0043f15c  31db                  xor      ebx, ebx
0043f15e  8a1d44fb4d00          mov      bl, byte ptr [0x4dfb44]
0043f164  30c0                  xor      al, al
0043f166  85db                  test     ebx, ebx
0043f168  743c                  je       0x43f1a6
0043f16a  8a0d181d4e00          mov      cl, byte ptr [0x4e1d18]
0043f170  31d2                  xor      edx, edx
0043f172  88ca                  mov      dl, cl
0043f174  8a92181c4e00          mov      dl, byte ptr [edx + 0x4e1c18]
0043f17a  81e2ff000000          and      edx, 0xff
0043f180  89d0                  mov      eax, edx
0043f182  c1fa1f                sar      edx, 0x1f
0043f185  f7fb                  idiv     ebx
0043f187  88d0                  mov      al, dl
0043f189  fec1                  inc      cl
0043f18b  8a257c8f5000          mov      ah, byte ptr [0x508f7c]
0043f191  880d181d4e00          mov      byte ptr [0x4e1d18], cl
0043f197  f6c401                test     ah, 1
0043f19a  750a                  jne      0x43f1a6
0043f19c  88da                  mov      dl, bl
0043f19e  feca                  dec      dl
0043f1a0  881544fb4d00          mov      byte ptr [0x4dfb44], dl
0043f1a6  31d2                  xor      edx, edx
0043f1a8  668b1518a04900        mov      dx, word ptr [0x49a018]
0043f1af  81fa20030000          cmp      edx, 0x320
0043f1b5  753d                  jne      0x43f1f4
0043f1b7  8b158d8f5000          mov      edx, dword ptr [0x508f8d]
0043f1bd  c1fa18                sar      edx, 0x18
0043f1c0  c1e205                shl      edx, 5
0043f1c3  891424                mov      dword ptr [esp], edx
0043f1c6  25ff000000            and      eax, 0xff
0043f1cb  01c2                  add      edx, eax
0043f1cd  31c0                  xor      eax, eax
0043f1cf  66a126875000          mov      ax, word ptr [0x508726]
0043f1d5  8b1c24                mov      ebx, dword ptr [esp]
0043f1d8  c1e005                shl      eax, 5
0043f1db  29d8                  sub      eax, ebx
0043f1dd  8944240c              mov      dword ptr [esp + 0xc], eax
0043f1e1  31c0                  xor      eax, eax
0043f1e3  66a124875000          mov      ax, word ptr [0x508724]
0043f1e9  c1e005                shl      eax, 5
0043f1ec  29d8                  sub      eax, ebx
0043f1ee  89542404              mov      dword ptr [esp + 4], edx
0043f1f2  eb28                  jmp      0x43f21c
0043f1f4  31d2                  xor      edx, edx
0043f1f6  891424                mov      dword ptr [esp], edx
0043f1f9  25ff000000            and      eax, 0xff
0043f1fe  89442404              mov      dword ptr [esp + 4], eax
0043f202  31c0                  xor      eax, eax
0043f204  66a126875000          mov      ax, word ptr [0x508726]
0043f20a  c1e005                shl      eax, 5
0043f20d  8944240c              mov      dword ptr [esp + 0xc], eax
0043f211  31c0                  xor      eax, eax
0043f213  66a124875000          mov      ax, word ptr [0x508724]
0043f219  c1e005                shl      eax, 5
0043f21c  89442408              mov      dword ptr [esp + 8], eax
0043f220  6a10                  push     0x10
0043f222  8d5c2404              lea      ebx, [esp + 4]
0043f226  53                    push     ebx
0043f227  8b1d8d8f5000          mov      ebx, dword ptr [0x508f8d]
0043f22d  8b3590174e00          mov      esi, dword ptr [0x4e1790]
0043f233  c1fb18                sar      ebx, 0x18
0043f236  56                    push     esi
0043f237  c1e305                shl      ebx, 5
0043f23a  53                    push     ebx
0043f23b  a18c174e00            mov      eax, dword ptr [0x4e178c]
0043f240  53                    push     ebx
0043f241  8b10                  mov      edx, dword ptr [eax]
0043f243  50                    push     eax
0043f244  ff521c                call     dword ptr [edx + 0x1c]
0043f247  89c2                  mov      edx, eax
0043f249  85c0                  test     eax, eax
0043f24b  7420                  je       0x43f26d
0043f24d  3dc2017688            cmp      eax, 0x887601c2
0043f252  7511                  jne      0x43f265
0043f254  a18c174e00            mov      eax, dword ptr [0x4e178c]
0043f259  50                    push     eax
0043f25a  8b10                  mov      edx, dword ptr [eax]
0043f25c  ff526c                call     dword ptr [edx + 0x6c]
0043f25f  89c2                  mov      edx, eax
0043f261  85c0                  test     eax, eax
0043f263  7508                  jne      0x43f26d
0043f265  81fa1c027688          cmp      edx, 0x8876021c
0043f26b  74b3                  je       0x43f220
0043f26d  807c241000            cmp      byte ptr [esp + 0x10], 0
0043f272  0f849a000000          je       0x43f312
0043f278  31c0                  xor      eax, eax
0043f27a  66a118a04900          mov      ax, word ptr [0x49a018]
0043f280  3d20030000            cmp      eax, 0x320
0043f285  751d                  jne      0x43f2a4
0043f287  b920020000            mov      ecx, 0x220
0043f28c  bf58020000            mov      edi, 0x258
0043f291  31db                  xor      ebx, ebx
0043f293  89442408              mov      dword ptr [esp + 8], eax
0043f297  891c24                mov      dword ptr [esp], ebx
0043f29a  894c2404              mov      dword ptr [esp + 4], ecx
0043f29e  897c240c              mov      dword ptr [esp + 0xc], edi
0043f2a2  eb20                  jmp      0x43f2c4
0043f2a4  bd20020000            mov      ebp, 0x220
0043f2a9  b880020000            mov      eax, 0x280
0043f2ae  31ff                  xor      edi, edi
0043f2b0  ba58020000            mov      edx, 0x258
0043f2b5  893c24                mov      dword ptr [esp], edi
0043f2b8  896c2404              mov      dword ptr [esp + 4], ebp
0043f2bc  89442408              mov      dword ptr [esp + 8], eax
0043f2c0  8954240c              mov      dword ptr [esp + 0xc], edx
0043f2c4  6a10                  push     0x10
0043f2c6  8d5c2404              lea      ebx, [esp + 4]
0043f2ca  53                    push     ebx
0043f2cb  31db                  xor      ebx, ebx
0043f2cd  8b2d90174e00          mov      ebp, dword ptr [0x4e1790]
0043f2d3  668b1d26875000        mov      bx, word ptr [0x508726]
0043f2da  55                    push     ebp
0043f2db  c1e305                shl      ebx, 5
0043f2de  53                    push     ebx
0043f2df  a18c174e00            mov      eax, dword ptr [0x4e178c]
0043f2e4  6a00                  push     0
0043f2e6  8b10                  mov      edx, dword ptr [eax]
0043f2e8  50                    push     eax
0043f2e9  ff521c                call     dword ptr [edx + 0x1c]
0043f2ec  89c2                  mov      edx, eax
0043f2ee  85c0                  test     eax, eax
0043f2f0  7420                  je       0x43f312
0043f2f2  3dc2017688            cmp      eax, 0x887601c2
0043f2f7  7511                  jne      0x43f30a
0043f2f9  a18c174e00            mov      eax, dword ptr [0x4e178c]
0043f2fe  50                    push     eax
0043f2ff  8b10                  mov      edx, dword ptr [eax]
0043f301  ff526c                call     dword ptr [edx + 0x6c]
0043f304  89c2                  mov      edx, eax
0043f306  85c0                  test     eax, eax
0043f308  7508                  jne      0x43f312
0043f30a  81fa1c027688          cmp      edx, 0x8876021c
0043f310  74b2                  je       0x43f2c4
0043f312  83c414                add      esp, 0x14
0043f315  5d                    pop      ebp
0043f316  5f                    pop      edi
0043f317  5e                    pop      esi
0043f318  5a                    pop      edx
0043f319  59                    pop      ecx
0043f31a  5b                    pop      ebx
0043f31b  c3                    ret
