; iaProbInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047d1a4..0x0047d1b8 (end exclusive); labels are original SBL names
0047d1a4  52                       push edx
0047d1a5  ba01000000               mov edx, 1
0047d1aa  b8284f4900               mov eax, 0x494f28
0047d1af  e883120000               call 0x47e437 ; -> iaProbLoadBinaryRules
0047d1b4  85c0                     test eax, eax
0047d1b6  5a                       pop edx
0047d1b7  c3                       ret
