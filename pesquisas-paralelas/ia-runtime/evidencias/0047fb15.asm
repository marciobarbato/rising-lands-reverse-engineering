; IaAlloc (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047fb15..0x0047fb6c (end exclusive); labels are original SBL names
0047fb15  31c0                     xor eax, eax
0047fb17  e80c9c0000               call 0x489728 ; -> iaRandom
0047fb1c  b8844f4900               mov eax, 0x494f84
0047fb21  e8d7da0000               call 0x48d5fd ; -> debugSymLoad
0047fb26  e879d6ffff               call 0x47d1a4 ; -> iaProbInit
0047fb2b  85c0                     test eax, eax
0047fb2d  0f8554ffffff             jne 0x47fa87
0047fb33  e86c2b0000               call 0x4826a4 ; -> iagUnitInit
0047fb38  85c0                     test eax, eax
0047fb3a  0f8547ffffff             jne 0x47fa87
0047fb40  e87f500000               call 0x484bc4 ; -> iagRessInit
0047fb45  85c0                     test eax, eax
0047fb47  0f853affffff             jne 0x47fa87
0047fb4d  e8c2460000               call 0x484214 ; -> iagVilleInit
0047fb52  85c0                     test eax, eax
0047fb54  0f852dffffff             jne 0x47fa87
0047fb5a  e8ed650000               call 0x48614c ; -> iagWarInit
0047fb5f  85c0                     test eax, eax
0047fb61  0f8520ffffff             jne 0x47fa87
0047fb67  e92ddb0000               jmp 0x48d699 ; -> debugSymUnload

; shared Watcom tail reached from IaAlloc; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047fa87..0x0047fa88 (end exclusive); labels are original SBL names
0047fa87  c3                       ret
