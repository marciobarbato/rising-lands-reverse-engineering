; MarcheOrdreEchange; exclusive end 0x00461c4f.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Original instruction listing; unit branches are captured but unsupported.
00461bea  53                       push     ebx
00461beb  51                       push     ecx
00461bec  88c3                     mov      bl, al
00461bee  31c0                     xor      eax, eax
00461bf0  88d8                     mov      al, bl
00461bf2  80b868294e0000           cmp      byte ptr [eax + 0x4e2968], 0
00461bf9  0f94c7                   sete     bh
00461bfc  31c0                     xor      eax, eax
00461bfe  31c9                     xor      ecx, ecx
00461c00  88d8                     mov      al, bl
00461c02  88d1                     mov      cl, dl
00461c04  88b868294e00             mov      byte ptr [eax + 0x4e2968], bh
00461c0a  80b968294e0000           cmp      byte ptr [ecx + 0x4e2968], 0
00461c11  750f                     jne      0x461c22
00461c13  e8ffbb0000               call     0x46d817
00461c18  25ff000000               and      eax, 0xff
00461c1d  83f802                   cmp      eax, 2
00461c20  752a                     jne      0x461c4c
00461c22  31c9                     xor      ecx, ecx
00461c24  88d1                     mov      cl, dl
00461c26  81e3ff000000             and      ebx, 0xff
00461c2c  89ca                     mov      edx, ecx
00461c2e  89d8                     mov      eax, ebx
00461c30  e8ecf9ffff               call     0x461621
00461c35  89ca                     mov      edx, ecx
00461c37  89d8                     mov      eax, ebx
00461c39  e85cfcffff               call     0x46189a
00461c3e  30c0                     xor      al, al
00461c40  888368294e00             mov      byte ptr [ebx + 0x4e2968], al
00461c46  888168294e00             mov      byte ptr [ecx + 0x4e2968], al
00461c4c  59                       pop      ecx
00461c4d  5b                       pop      ebx
00461c4e  c3                       ret
