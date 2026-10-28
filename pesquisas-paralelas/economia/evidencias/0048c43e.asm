; __CHP: limite por RET antes dos dados seguintes, fim exclusivo 0x0048c45b.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0048c43e  50                       push     eax
0048c43f  9b                       wait
0048c440  d93c24                   fnstcw   word ptr [esp]
0048c443  9b                       wait
0048c444  ff3424                   push     dword ptr [esp]
0048c447  c64424011f               mov      byte ptr [esp + 1], 0x1f
0048c44c  d92c24                   fldcw    word ptr [esp]
0048c44f  d9fc                     frndint
0048c451  d96c2404                 fldcw    word ptr [esp + 4]
0048c455  9b                       wait
0048c456  8d642408                 lea      esp, [esp + 8]
0048c45a  c3                       ret
