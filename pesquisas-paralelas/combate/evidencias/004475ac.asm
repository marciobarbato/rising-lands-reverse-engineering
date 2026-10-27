; EnginTypeGetCapacite; intervalo [0x004475ac, 0x004475ef)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004475ac  52                       push     edx
004475ad  88c2                     mov      dl, al
004475af  31c0                     xor      eax, eax
004475b1  80fa19                   cmp      dl, 0x19
004475b4  0f870bffffff             ja       0x4474c5
004475ba  81e2ff000000             and      edx, 0xff
004475c0  2eff249544754400         jmp      dword ptr cs:[edx*4 + 0x447544]
004475c8  b802000000               mov      eax, 2
004475cd  5a                       pop      edx
004475ce  c3                       ret
004475cf  b801000000               mov      eax, 1
004475d4  5a                       pop      edx
004475d5  c3                       ret
004475d6  b805000000               mov      eax, 5
004475db  5a                       pop      edx
004475dc  c3                       ret
004475dd  b803000000               mov      eax, 3
004475e2  5a                       pop      edx
004475e3  c3                       ret
004475e4  b806000000               mov      eax, 6
004475e9  5a                       pop      edx
004475ea  c3                       ret
004475eb  31c0                     xor      eax, eax
004475ed  5a                       pop      edx
004475ee  c3                       ret
