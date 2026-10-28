; CalculNextReflect (frame); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047fbea..0x0047fbfd (end exclusive); labels are original SBL names
0047fbea  81e2ff000000             and edx, 0xff
0047fbf0  25ff000000               and eax, 0xff
0047fbf5  e82dfdffff               call 0x47f927 ; -> iaCalculPlayer
0047fbfa  b001                     mov al, 1
0047fbfc  c3                       ret
