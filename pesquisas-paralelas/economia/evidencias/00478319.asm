; ScanNouvellePatate: limite por próximo símbolo SBL, fim exclusivo 0x00478806.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00478319  53                       push     ebx
0047831a  51                       push     ecx
0047831b  52                       push     edx
0047831c  56                       push     esi
0047831d  89c2                     mov      edx, eax
0047831f  89d3                     mov      ebx, edx
00478321  30c0                     xor      al, al
00478323  4b                       dec      ebx
00478324  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
0047832a  81e3ffff0000             and      ebx, 0xffff
00478330  8a1c19                   mov      bl, byte ptr [ecx + ebx]
00478333  81e3ff000000             and      ebx, 0xff
00478339  83fb1d                   cmp      ebx, 0x1d
0047833c  7c09                     jl       0x478347
0047833e  83fb35                   cmp      ebx, 0x35
00478341  7d04                     jge      0x478347
00478343  b401                     mov      ah, 1
00478345  eb02                     jmp      0x478349
00478347  30e4                     xor      ah, ah
00478349  84e4                     test     ah, ah
0047834b  0f85c1000000             jne      0x478412
00478351  89d3                     mov      ebx, edx
00478353  4b                       dec      ebx
00478354  89de                     mov      esi, ebx
00478356  89d9                     mov      ecx, ebx
00478358  81e1ffff0000             and      ecx, 0xffff
0047835e  8b1d707d5000             mov      ebx, dword ptr [0x507d70]
00478364  01c9                     add      ecx, ecx
00478366  668b1c19                 mov      bx, word ptr [ecx + ebx]
0047836a  81e3ffff0000             and      ebx, 0xffff
00478370  81fb9d000000             cmp      ebx, 0x9d
00478376  7c08                     jl       0x478380
00478378  81fbdd000000             cmp      ebx, 0xdd
0047837e  7c25                     jl       0x4783a5
00478380  31db                     xor      ebx, ebx
00478382  8b0d707d5000             mov      ecx, dword ptr [0x507d70]
00478388  6689f3                   mov      bx, si
0047838b  668b1c59                 mov      bx, word ptr [ecx + ebx*2]
0047838f  81e3ffff0000             and      ebx, 0xffff
00478395  81fb84000000             cmp      ebx, 0x84
0047839b  7c0c                     jl       0x4783a9
0047839d  81fb87000000             cmp      ebx, 0x87
004783a3  7d04                     jge      0x4783a9
004783a5  b401                     mov      ah, 1
004783a7  eb02                     jmp      0x4783ab
004783a9  30e4                     xor      ah, ah
004783ab  84e4                     test     ah, ah
004783ad  7463                     je       0x478412
004783af  89d0                     mov      eax, edx
004783b1  31c9                     xor      ecx, ecx
004783b3  48                       dec      eax
004783b4  6689c1                   mov      cx, ax
004783b7  89c3                     mov      ebx, eax
004783b9  a1747d5000               mov      eax, dword ptr [0x507d74]
004783be  8a0401                   mov      al, byte ptr [ecx + eax]
004783c1  25ff000000               and      eax, 0xff
004783c6  7548                     jne      0x478410
004783c8  a1a87d5000               mov      eax, dword ptr [0x507da8]
004783cd  8a0401                   mov      al, byte ptr [ecx + eax]
004783d0  25ff000000               and      eax, 0xff
004783d5  a801                     test     al, 1
004783d7  0f95c0                   setne    al
004783da  84c0                     test     al, al
004783dc  7532                     jne      0x478410
004783de  b836000000               mov      eax, 0x36
004783e3  e8f480ffff               call     0x4704dc
004783e8  a801                     test     al, 1
004783ea  7511                     jne      0x4783fd
004783ec  31c0                     xor      eax, eax
004783ee  6689d8                   mov      ax, bx
004783f1  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
004783f7  c604031d                 mov      byte ptr [ebx + eax], 0x1d
004783fb  eb0f                     jmp      0x47840c
004783fd  31c0                     xor      eax, eax
004783ff  6689d8                   mov      ax, bx
00478402  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
00478408  c6040329                 mov      byte ptr [ebx + eax], 0x29
0047840c  b001                     mov      al, 1
0047840e  eb02                     jmp      0x478412
00478410  30c0                     xor      al, al
00478412  84c0                     test     al, al
00478414  0f854b010000             jne      0x478565
0047841a  89d3                     mov      ebx, edx
0047841c  43                       inc      ebx
0047841d  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
00478423  81e3ffff0000             and      ebx, 0xffff
00478429  8a1c19                   mov      bl, byte ptr [ecx + ebx]
0047842c  81e3ff000000             and      ebx, 0xff
00478432  83fb1d                   cmp      ebx, 0x1d
00478435  7c09                     jl       0x478440
00478437  83fb35                   cmp      ebx, 0x35
0047843a  7d04                     jge      0x478440
0047843c  b401                     mov      ah, 1
0047843e  eb02                     jmp      0x478442
00478440  30e4                     xor      ah, ah
00478442  84e4                     test     ah, ah
00478444  0f851b010000             jne      0x478565
0047844a  89d3                     mov      ebx, edx
0047844c  43                       inc      ebx
0047844d  89d9                     mov      ecx, ebx
0047844f  89de                     mov      esi, ebx
00478451  81e6ffff0000             and      esi, 0xffff
00478457  8b1d707d5000             mov      ebx, dword ptr [0x507d70]
0047845d  01f6                     add      esi, esi
0047845f  668b1c1e                 mov      bx, word ptr [esi + ebx]
00478463  81e3ffff0000             and      ebx, 0xffff
00478469  81fb9d000000             cmp      ebx, 0x9d
0047846f  7c08                     jl       0x478479
00478471  81fbdd000000             cmp      ebx, 0xdd
00478477  7c26                     jl       0x47849f
00478479  8b1d707d5000             mov      ebx, dword ptr [0x507d70]
0047847f  81e1ffff0000             and      ecx, 0xffff
00478485  668b1c4b                 mov      bx, word ptr [ebx + ecx*2]
00478489  81e3ffff0000             and      ebx, 0xffff
0047848f  81fb84000000             cmp      ebx, 0x84
00478495  7c0c                     jl       0x4784a3
00478497  81fb87000000             cmp      ebx, 0x87
0047849d  7d04                     jge      0x4784a3
0047849f  b401                     mov      ah, 1
004784a1  eb02                     jmp      0x4784a5
004784a3  30e4                     xor      ah, ah
004784a5  84e4                     test     ah, ah
004784a7  0f84b8000000             je       0x478565
004784ad  89d3                     mov      ebx, edx
004784af  43                       inc      ebx
004784b0  8b0da87d5000             mov      ecx, dword ptr [0x507da8]
004784b6  81e3ffff0000             and      ebx, 0xffff
004784bc  8a1c19                   mov      bl, byte ptr [ecx + ebx]
004784bf  81e3ff000000             and      ebx, 0xff
004784c5  f6c301                   test     bl, 1
004784c8  0f95c4                   setne    ah
004784cb  84e4                     test     ah, ah
004784cd  0f8592000000             jne      0x478565
004784d3  89d3                     mov      ebx, edx
004784d5  43                       inc      ebx
004784d6  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
004784dc  81e3ffff0000             and      ebx, 0xffff
004784e2  8a1c19                   mov      bl, byte ptr [ecx + ebx]
004784e5  81e3ff000000             and      ebx, 0xff
004784eb  83fb42                   cmp      ebx, 0x42
004784ee  7c09                     jl       0x4784f9
004784f0  83fb44                   cmp      ebx, 0x44
004784f3  7f04                     jg       0x4784f9
004784f5  b401                     mov      ah, 1
004784f7  eb02                     jmp      0x4784fb
004784f9  30e4                     xor      ah, ah
004784fb  84e4                     test     ah, ah
004784fd  7566                     jne      0x478565
004784ff  89d0                     mov      eax, edx
00478501  40                       inc      eax
00478502  89c3                     mov      ebx, eax
00478504  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
0047850a  25ffff0000               and      eax, 0xffff
0047850f  8a0c01                   mov      cl, byte ptr [ecx + eax]
00478512  81e1ff000000             and      ecx, 0xff
00478518  7549                     jne      0x478563
0047851a  8b0da87d5000             mov      ecx, dword ptr [0x507da8]
00478520  8a0401                   mov      al, byte ptr [ecx + eax]
00478523  25ff000000               and      eax, 0xff
00478528  a801                     test     al, 1
0047852a  0f95c0                   setne    al
0047852d  84c0                     test     al, al
0047852f  7532                     jne      0x478563
00478531  b836000000               mov      eax, 0x36
00478536  e8a17fffff               call     0x4704dc
0047853b  a801                     test     al, 1
0047853d  7511                     jne      0x478550
0047853f  a1747d5000               mov      eax, dword ptr [0x507d74]
00478544  81e3ffff0000             and      ebx, 0xffff
0047854a  c604031d                 mov      byte ptr [ebx + eax], 0x1d
0047854e  eb0f                     jmp      0x47855f
00478550  31c0                     xor      eax, eax
00478552  6689d8                   mov      ax, bx
00478555  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
0047855b  c6040329                 mov      byte ptr [ebx + eax], 0x29
0047855f  b001                     mov      al, 1
00478561  eb02                     jmp      0x478565
00478563  30c0                     xor      al, al
00478565  84c0                     test     al, al
00478567  0f855b010000             jne      0x4786c8
0047856d  89d3                     mov      ebx, edx
0047856f  81eb00010000             sub      ebx, 0x100
00478575  8b0d747d5000             mov      ecx, dword ptr [0x507d74]
0047857b  81e3ffff0000             and      ebx, 0xffff
00478581  8a1c19                   mov      bl, byte ptr [ecx + ebx]
00478584  81e3ff000000             and      ebx, 0xff
0047858a  83fb1d                   cmp      ebx, 0x1d
0047858d  7c09                     jl       0x478598
0047858f  83fb35                   cmp      ebx, 0x35
00478592  7d04                     jge      0x478598
00478594  b401                     mov      ah, 1
00478596  eb02                     jmp      0x47859a
00478598  30e4                     xor      ah, ah
0047859a  84e4                     test     ah, ah
0047859c  0f8526010000             jne      0x4786c8
004785a2  89d3                     mov      ebx, edx
004785a4  81eb00010000             sub      ebx, 0x100
004785aa  89de                     mov      esi, ebx
004785ac  8b0d707d5000             mov      ecx, dword ptr [0x507d70]
004785b2  81e3ffff0000             and      ebx, 0xffff
004785b8  668b1c59                 mov      bx, word ptr [ecx + ebx*2]
004785bc  81e3ffff0000             and      ebx, 0xffff
004785c2  81fb9d000000             cmp      ebx, 0x9d
004785c8  7c08                     jl       0x4785d2
004785ca  81fbdd000000             cmp      ebx, 0xdd
004785d0  7c25                     jl       0x4785f7
004785d2  31db                     xor      ebx, ebx
004785d4  8b0d707d5000             mov      ecx, dword ptr [0x507d70]
004785da  6689f3                   mov      bx, si
004785dd  668b1c59                 mov      bx, word ptr [ecx + ebx*2]
004785e1  81e3ffff0000             and      ebx, 0xffff
004785e7  81fb84000000             cmp      ebx, 0x84
004785ed  7c0c                     jl       0x4785fb
004785ef  81fb87000000             cmp      ebx, 0x87
004785f5  7d04                     jge      0x4785fb
004785f7  b401                     mov      ah, 1
004785f9  eb02                     jmp      0x4785fd
004785fb  30e4                     xor      ah, ah
004785fd  84e4                     test     ah, ah
004785ff  0f84c3000000             je       0x4786c8
00478605  89d3                     mov      ebx, edx
00478607  81eb00010000             sub      ebx, 0x100
0047860d  8b0da87d5000             mov      ecx, dword ptr [0x507da8]
00478613  81e3ffff0000             and      ebx, 0xffff
00478619  8a1c19                   mov      bl, byte ptr [ecx + ebx]
0047861c  81e3ff000000             and      ebx, 0xff
00478622  f6c301                   test     bl, 1
00478625  0f95c4                   setne    ah
00478628  84e4                     test     ah, ah
0047862a  0f8598000000             jne      0x4786c8
00478630  89d3                     mov      ebx, edx
00478632  31c9                     xor      ecx, ecx
00478634  81eb00010000             sub      ebx, 0x100
0047863a  6689d9                   mov      cx, bx
0047863d  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
00478643  8a1c19                   mov      bl, byte ptr [ecx + ebx]
00478646  81e3ff000000             and      ebx, 0xff
0047864c  83fb42                   cmp      ebx, 0x42
0047864f  7c09                     jl       0x47865a
00478651  83fb44                   cmp      ebx, 0x44
00478654  7f04                     jg       0x47865a
00478656  b401                     mov      ah, 1
00478658  eb02                     jmp      0x47865c
0047865a  30e4                     xor      ah, ah
0047865c  84e4                     test     ah, ah
0047865e  7568                     jne      0x4786c8
00478660  89d0                     mov      eax, edx
00478662  31c9                     xor      ecx, ecx
00478664  81e800010000             sub      eax, 0x100
0047866a  6689c1                   mov      cx, ax
0047866d  89c3                     mov      ebx, eax
0047866f  a1747d5000               mov      eax, dword ptr [0x507d74]
00478674  8a0401                   mov      al, byte ptr [ecx + eax]
00478677  25ff000000               and      eax, 0xff
0047867c  7548                     jne      0x4786c6
0047867e  a1a87d5000               mov      eax, dword ptr [0x507da8]
00478683  8a0401                   mov      al, byte ptr [ecx + eax]
00478686  25ff000000               and      eax, 0xff
0047868b  a801                     test     al, 1
0047868d  0f95c0                   setne    al
00478690  84c0                     test     al, al
00478692  7532                     jne      0x4786c6
00478694  b836000000               mov      eax, 0x36
00478699  e83e7effff               call     0x4704dc
0047869e  a801                     test     al, 1
004786a0  7511                     jne      0x4786b3
004786a2  31c0                     xor      eax, eax
004786a4  6689d8                   mov      ax, bx
004786a7  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
004786ad  c604031d                 mov      byte ptr [ebx + eax], 0x1d
004786b1  eb0f                     jmp      0x4786c2
004786b3  a1747d5000               mov      eax, dword ptr [0x507d74]
004786b8  81e3ffff0000             and      ebx, 0xffff
004786be  c6040329                 mov      byte ptr [ebx + eax], 0x29
004786c2  b001                     mov      al, 1
004786c4  eb02                     jmp      0x4786c8
004786c6  30c0                     xor      al, al
004786c8  84c0                     test     al, al
004786ca  0f8531010000             jne      0x478801
004786d0  89d0                     mov      eax, edx
004786d2  31db                     xor      ebx, ebx
004786d4  fec4                     inc      ah
004786d6  6689c3                   mov      bx, ax
004786d9  a1747d5000               mov      eax, dword ptr [0x507d74]
004786de  8a0403                   mov      al, byte ptr [ebx + eax]
004786e1  25ff000000               and      eax, 0xff
004786e6  83f81d                   cmp      eax, 0x1d
004786e9  7c09                     jl       0x4786f4
004786eb  83f835                   cmp      eax, 0x35
004786ee  7d04                     jge      0x4786f4
004786f0  b001                     mov      al, 1
004786f2  eb02                     jmp      0x4786f6
004786f4  30c0                     xor      al, al
004786f6  84c0                     test     al, al
004786f8  0f8503010000             jne      0x478801
004786fe  89d0                     mov      eax, edx
00478700  fec4                     inc      ah
00478702  89c1                     mov      ecx, eax
00478704  8b1d707d5000             mov      ebx, dword ptr [0x507d70]
0047870a  25ffff0000               and      eax, 0xffff
0047870f  668b0443                 mov      ax, word ptr [ebx + eax*2]
00478713  25ffff0000               and      eax, 0xffff
00478718  3d9d000000               cmp      eax, 0x9d
0047871d  7c07                     jl       0x478726
0047871f  3ddd000000               cmp      eax, 0xdd
00478724  7c22                     jl       0x478748
00478726  31c0                     xor      eax, eax
00478728  8b1d707d5000             mov      ebx, dword ptr [0x507d70]
0047872e  6689c8                   mov      ax, cx
00478731  668b0443                 mov      ax, word ptr [ebx + eax*2]
00478735  25ffff0000               and      eax, 0xffff
0047873a  3d84000000               cmp      eax, 0x84
0047873f  7c0b                     jl       0x47874c
00478741  3d87000000               cmp      eax, 0x87
00478746  7d04                     jge      0x47874c
00478748  b001                     mov      al, 1
0047874a  eb02                     jmp      0x47874e
0047874c  30c0                     xor      al, al
0047874e  84c0                     test     al, al
00478750  0f84ab000000             je       0x478801
00478756  89d0                     mov      eax, edx
00478758  fec4                     inc      ah
0047875a  8b1da87d5000             mov      ebx, dword ptr [0x507da8]
00478760  25ffff0000               and      eax, 0xffff
00478765  8a0403                   mov      al, byte ptr [ebx + eax]
00478768  25ff000000               and      eax, 0xff
0047876d  a801                     test     al, 1
0047876f  0f95c0                   setne    al
00478772  84c0                     test     al, al
00478774  0f8587000000             jne      0x478801
0047877a  89d0                     mov      eax, edx
0047877c  31db                     xor      ebx, ebx
0047877e  fec4                     inc      ah
00478780  6689c3                   mov      bx, ax
00478783  a1747d5000               mov      eax, dword ptr [0x507d74]
00478788  8a0403                   mov      al, byte ptr [ebx + eax]
0047878b  25ff000000               and      eax, 0xff
00478790  83f842                   cmp      eax, 0x42
00478793  7c09                     jl       0x47879e
00478795  83f844                   cmp      eax, 0x44
00478798  7f04                     jg       0x47879e
0047879a  b001                     mov      al, 1
0047879c  eb02                     jmp      0x4787a0
0047879e  30c0                     xor      al, al
004787a0  84c0                     test     al, al
004787a2  755d                     jne      0x478801
004787a4  fec6                     inc      dh
004787a6  31db                     xor      ebx, ebx
004787a8  a1747d5000               mov      eax, dword ptr [0x507d74]
004787ad  6689d3                   mov      bx, dx
004787b0  8a0403                   mov      al, byte ptr [ebx + eax]
004787b3  25ff000000               and      eax, 0xff
004787b8  7547                     jne      0x478801
004787ba  a1a87d5000               mov      eax, dword ptr [0x507da8]
004787bf  8a0403                   mov      al, byte ptr [ebx + eax]
004787c2  25ff000000               and      eax, 0xff
004787c7  a801                     test     al, 1
004787c9  0f95c0                   setne    al
004787cc  84c0                     test     al, al
004787ce  7531                     jne      0x478801
004787d0  b836000000               mov      eax, 0x36
004787d5  e8027dffff               call     0x4704dc
004787da  a801                     test     al, 1
004787dc  7514                     jne      0x4787f2
004787de  31c0                     xor      eax, eax
004787e0  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
004787e6  6689d0                   mov      ax, dx
004787e9  c604031d                 mov      byte ptr [ebx + eax], 0x1d
004787ed  5e                       pop      esi
004787ee  5a                       pop      edx
004787ef  59                       pop      ecx
004787f0  5b                       pop      ebx
004787f1  c3                       ret
004787f2  31c0                     xor      eax, eax
004787f4  8b1d747d5000             mov      ebx, dword ptr [0x507d74]
004787fa  6689d0                   mov      ax, dx
004787fd  c6040329                 mov      byte ptr [ebx + eax], 0x29
00478801  5e                       pop      esi
00478802  5a                       pop      edx
00478803  59                       pop      ecx
00478804  5b                       pop      ebx
00478805  c3                       ret
