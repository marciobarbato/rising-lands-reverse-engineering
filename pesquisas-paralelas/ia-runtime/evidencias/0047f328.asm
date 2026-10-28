; iaInit (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047f328..0x0047f36e (end exclusive); labels are original SBL names
0047f328  31c0                     xor eax, eax
0047f32a  e8f9a30000               call 0x489728 ; -> iaRandom
0047f32f  b8844f4900               mov eax, 0x494f84
0047f334  e8c4e20000               call 0x48d5fd ; -> debugSymLoad
0047f339  e866deffff               call 0x47d1a4 ; -> iaProbInit
0047f33e  85c0                     test eax, eax
0047f340  752b                     jne 0x47f36d
0047f342  e85d330000               call 0x4826a4 ; -> iagUnitInit
0047f347  85c0                     test eax, eax
0047f349  7522                     jne 0x47f36d
0047f34b  e874580000               call 0x484bc4 ; -> iagRessInit
0047f350  85c0                     test eax, eax
0047f352  7519                     jne 0x47f36d
0047f354  e8bb4e0000               call 0x484214 ; -> iagVilleInit
0047f359  85c0                     test eax, eax
0047f35b  7510                     jne 0x47f36d
0047f35d  e8ea6d0000               call 0x48614c ; -> iagWarInit
0047f362  85c0                     test eax, eax
0047f364  7507                     jne 0x47f36d
0047f366  e82ee30000               call 0x48d699 ; -> debugSymUnload
0047f36b  31c0                     xor eax, eax
0047f36d  c3                       ret
