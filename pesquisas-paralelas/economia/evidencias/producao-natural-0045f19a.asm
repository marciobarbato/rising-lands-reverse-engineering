; ProcessInputGame: Player-input caller of InitRecruteTroupe; exclusive end 0x0045f1ae.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0045f19a  e93f010000               jmp      0x45f2de
0045f19f  8a4002                   mov      al, byte ptr [eax + 2]
0045f1a2  25ff000000               and      eax, 0xff
0045f1a7  89f2                     mov      edx, esi
0045f1a9  e83492fcff               call     0x4283e2
