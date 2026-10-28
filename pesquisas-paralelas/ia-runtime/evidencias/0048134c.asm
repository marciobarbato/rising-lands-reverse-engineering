; iafRessourceReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0048134c..0x0048135f (end exclusive); labels are original SBL names
0048134c  52                       push edx
0048134d  31c0                     xor eax, eax
0048134f  40                       inc eax
00481350  30d2                     xor dl, dl
00481352  8890cba95100             mov byte ptr [eax + 0x51a9cb], dl
00481358  83f814                   cmp eax, 0x14
0048135b  72f2                     jb 0x48134f
0048135d  5a                       pop edx
0048135e  c3                       ret
