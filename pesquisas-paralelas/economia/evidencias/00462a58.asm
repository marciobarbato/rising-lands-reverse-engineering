; GetNbRessource: limite por próximo símbolo SBL, fim exclusivo 0x00462abd.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00462a58  53                       push     ebx
00462a59  51                       push     ecx
00462a5a  83ec14                   sub      esp, 0x14
00462a5d  88442410                 mov      byte ptr [esp + 0x10], al
00462a61  89e1                     mov      ecx, esp
00462a63  31db                     xor      ebx, ebx
00462a65  31c0                     xor      eax, eax
00462a67  895c2404                 mov      dword ptr [esp + 4], ebx
00462a6b  895c2408                 mov      dword ptr [esp + 8], ebx
00462a6f  895c240c                 mov      dword ptr [esp + 0xc], ebx
00462a73  891c24                   mov      dword ptr [esp], ebx
00462a76  88d0                     mov      al, dl
00462a78  8d5c240c                 lea      ebx, [esp + 0xc]
00462a7c  50                       push     eax
00462a7d  8d54240c                 lea      edx, [esp + 0xc]
00462a81  8d442408                 lea      eax, [esp + 8]
00462a85  e8e64b0000               call     0x467670
00462a8a  8a642410                 mov      ah, byte ptr [esp + 0x10]
00462a8e  80fc01                   cmp      ah, 1
00462a91  721b                     jb       0x462aae
00462a93  7607                     jbe      0x462a9c
00462a95  80fc02                   cmp      ah, 2
00462a98  7408                     je       0x462aa2
00462a9a  eb16                     jmp      0x462ab2
00462a9c  8b442404                 mov      eax, dword ptr [esp + 4]
00462aa0  eb15                     jmp      0x462ab7
00462aa2  8b442408                 mov      eax, dword ptr [esp + 8]
00462aa6  eb0f                     jmp      0x462ab7
00462aa8  8b44240c                 mov      eax, dword ptr [esp + 0xc]
00462aac  eb09                     jmp      0x462ab7
00462aae  84e4                     test     ah, ah
00462ab0  74f6                     je       0x462aa8
00462ab2  b8ffff0000               mov      eax, 0xffff
00462ab7  83c414                   add      esp, 0x14
00462aba  59                       pop      ecx
00462abb  5b                       pop      ebx
00462abc  c3                       ret
