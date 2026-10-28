; TypeBatimentGetDegat_selector_bodies; [0x418b42,0x418b97)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00418b42  31c0                     xor      eax, eax
00418b44  88d8                     mov      al, bl
00418b46  8a8064fb4d00             mov      al, byte ptr [eax + 0x4dfb64]
00418b4c  30e4                     xor      ah, ah
00418b4e  c3                       ret
00418b4f  30e4                     xor      ah, ah
00418b51  a07efb4d00               mov      al, byte ptr [0x4dfb7e]
00418b56  c3                       ret
00418b57  80fa01                   cmp      dl, 1
00418b5a  7238                     jb       0x418b94
00418b5c  76e4                     jbe      0x418b42
00418b5e  80fa03                   cmp      dl, 3
00418b61  74ec                     je       0x418b4f
00418b63  31c0                     xor      eax, eax
00418b65  c3                       ret
00418b66  31c0                     xor      eax, eax
00418b68  88d8                     mov      al, bl
00418b6a  8a8080fb4d00             mov      al, byte ptr [eax + 0x4dfb80]
00418b70  30e4                     xor      ah, ah
00418b72  c3                       ret
00418b73  30e4                     xor      ah, ah
00418b75  a09afb4d00               mov      al, byte ptr [0x4dfb9a]
00418b7a  c3                       ret
00418b7b  80fa01                   cmp      dl, 1
00418b7e  7214                     jb       0x418b94
00418b80  76e4                     jbe      0x418b66
00418b82  80fa03                   cmp      dl, 3
00418b85  74ec                     je       0x418b73
00418b87  31c0                     xor      eax, eax
00418b89  c3                       ret
00418b8a  3c0a                     cmp      al, 0xa
00418b8c  7206                     jb       0x418b94
00418b8e  76eb                     jbe      0x418b7b
00418b90  3c0b                     cmp      al, 0xb
00418b92  74c3                     je       0x418b57
00418b94  31c0                     xor      eax, eax
00418b96  c3                       ret
