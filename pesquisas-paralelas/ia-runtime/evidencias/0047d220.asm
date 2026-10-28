; iaProbReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047d220..0x0047d26e (end exclusive); labels are original SBL names
0047d220  53                       push ebx
0047d221  51                       push ecx
0047d222  52                       push edx
0047d223  56                       push esi
0047d224  57                       push edi
0047d225  6a01                     push 1
0047d227  b960000000               mov ecx, 0x60
0047d22c  bb64000000               mov ebx, 0x64
0047d231  ba20235100               mov edx, 0x512320
0047d236  b8a0485100               mov eax, 0x5148a0
0047d23b  beb0485100               mov esi, 0x5148b0
0047d240  e88bfdffff               call 0x47cfd0 ; -> listInit
0047d245  8d7e50                   lea edi, [esi + 0x50]
0047d248  6a00                     push 0
0047d24a  b960000000               mov ecx, 0x60
0047d24f  bb64000000               mov ebx, 0x64
0047d254  ba20235100               mov edx, 0x512320
0047d259  89f0                     mov eax, esi
0047d25b  83c610                   add esi, 0x10
0047d25e  e86dfdffff               call 0x47cfd0 ; -> listInit
0047d263  39fe                     cmp esi, edi
0047d265  75e1                     jne 0x47d248
0047d267  31c0                     xor eax, eax
0047d269  e990000000               jmp 0x47d2fe

; shared Watcom tail reached from iaProbReset; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047d2fe..0x0047d304 (end exclusive); labels are original SBL names
0047d2fe  5f                       pop edi
0047d2ff  5e                       pop esi
0047d300  5a                       pop edx
0047d301  59                       pop ecx
0047d302  5b                       pop ebx
0047d303  c3                       ret
