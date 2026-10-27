; AffBoxSelection [0x4122d5, 0x412390)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004122d5  51                     push     ecx
004122d6  56                     push     esi
004122d7  83ec08                 sub      esp, 8
004122da  89d1                   mov      ecx, edx
004122dc  89de                   mov      esi, ebx
004122de  8d5c2404               lea      ebx, [esp + 4]
004122e2  89e2                   mov      edx, esp
004122e4  25ffff0000             and      eax, 0xffff
004122e9  e87eed0200             call     0x44106c ; EnginGetTaille
004122ee  31c0                   xor      eax, eax
004122f0  668b0424               mov      ax, word ptr [esp]
004122f4  83f801                 cmp      eax, 1
004122f7  750b                   jne      0x412304
004122f9  39c0                   cmp      eax, eax
004122fb  7507                   jne      0x412304
004122fd  bb1e2a0000             mov      ebx, 0x2a1e
00412302  eb0b                   jmp      0x41230f ; 
00412304  bb1f2a0000             mov      ebx, 0x2a1f
00412309  83ee20                 sub      esi, 0x20
0041230c  83e920                 sub      ecx, 0x20
0041230f  0fbfd6                 movsx    edx, si
00412312  0fbfc1                 movsx    eax, cx
00412315  b901000000             mov      ecx, 1
0041231a  e8288f0400             call     0x45b247 ; PasteBobCmp
0041231f  83c408                 add      esp, 8
00412322  5e                     pop      esi
00412323  59                     pop      ecx
00412324  c3                     ret      
00412325  8d4000                 lea      eax, [eax]
