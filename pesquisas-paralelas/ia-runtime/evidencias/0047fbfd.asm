; IATestUtilite (frame); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047fbfd..0x0047fc1b (end exclusive); labels are original SBL names
0047fbfd  25ff000000               and eax, 0xff
0047fc02  83f801                   cmp eax, 1
0047fc05  75f5                     jne 0x47fbfc
0047fc07  81e2ffff0000             and edx, 0xffff
0047fc0d  89d0                     mov eax, edx
0047fc0f  e8c3420000               call 0x483ed7 ; -> iagMessTestSendMessageEngin
0047fc14  89d0                     mov eax, edx
0047fc16  e9899b0000               jmp 0x4897a4 ; -> iabTestEngin

; shared Watcom tail reached from IATestUtilite; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047fbfc..0x0047fbfd (end exclusive); labels are original SBL names
0047fbfc  c3                       ret
