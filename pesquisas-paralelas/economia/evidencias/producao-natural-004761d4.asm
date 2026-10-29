; TerrainEnCollision: (byte [0x507da8]+AX & DL) != 0; exclusive end 0x004761f1.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004761d4  53                       push     ebx
004761d5  8b1da87d5000             mov      ebx, dword ptr [0x507da8]
004761db  25ffff0000               and      eax, 0xffff
004761e0  01d8                     add      eax, ebx
004761e2  31db                     xor      ebx, ebx
004761e4  8a18                     mov      bl, byte ptr [eax]
004761e6  31c0                     xor      eax, eax
004761e8  88d0                     mov      al, dl
004761ea  85c3                     test     ebx, eax
004761ec  0f95c0                   setne    al
004761ef  5b                       pop      ebx
004761f0  c3                       ret
