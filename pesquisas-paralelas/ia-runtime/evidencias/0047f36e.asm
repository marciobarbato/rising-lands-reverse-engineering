; IaReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047f36e..0x0047f62b (end exclusive); labels are original SBL names
0047f36e  53                       push ebx
0047f36f  51                       push ecx
0047f370  52                       push edx
0047f371  56                       push esi
0047f372  57                       push edi
0047f373  55                       push ebp
0047f374  83ec1c                   sub esp, 0x1c
0047f377  31d2                     xor edx, edx
0047f379  bd8ca95100               mov ebp, 0x51a98c
0047f37e  89542410                 mov dword ptr [esp + 0x10], edx
0047f382  e9e9010000               jmp 0x47f570
0047f387  83ff01                   cmp edi, 1
0047f38a  740c                     je 0x47f398
0047f38c  b804000000               mov eax, 4
0047f391  e892a30000               call 0x489728 ; -> iaRandom
0047f396  89c7                     mov edi, eax
0047f398  b814000000               mov eax, 0x14
0047f39d  ba64000000               mov edx, 0x64
0047f3a2  e881a30000               call 0x489728 ; -> iaRandom
0047f3a7  83c01e                   add eax, 0x1e
0047f3aa  c744241403000000         mov dword ptr [esp + 0x14], 3
0047f3b2  89442418                 mov dword ptr [esp + 0x18], eax
0047f3b6  89c3                     mov ebx, eax
0047f3b8  29c2                     sub edx, eax
0047f3ba  31c3                     xor ebx, eax
0047f3bc  89d0                     mov eax, edx
0047f3be  c1fa1f                   sar edx, 0x1f
0047f3c1  f77c2414                 idiv dword ptr [esp + 0x14]
0047f3c5  31c9                     xor ecx, ecx
0047f3c7  89442404                 mov dword ptr [esp + 4], eax
0047f3cb  8b442408                 mov eax, dword ptr [esp + 8]
0047f3cf  eb0e                     jmp 0x47f3df
0047f3d1  035c2404                 add ebx, dword ptr [esp + 4]
0047f3d5  40                       inc eax
0047f3d6  41                       inc ecx
0047f3d7  885804                   mov byte ptr [eax + 4], bl
0047f3da  83f903                   cmp ecx, 3
0047f3dd  7d0a                     jge 0x47f3e9
0047f3df  39f9                     cmp ecx, edi
0047f3e1  75ee                     jne 0x47f3d1
0047f3e3  035c2418                 add ebx, dword ptr [esp + 0x18]
0047f3e7  ebec                     jmp 0x47f3d5
0047f3e9  8b442408                 mov eax, dword ptr [esp + 8]
0047f3ed  c6400864                 mov byte ptr [eax + 8], 0x64
0047f3f1  8b4602                   mov eax, dword ptr [esi + 2]
0047f3f4  c1f818                   sar eax, 0x18
0047f3f7  83f8ff                   cmp eax, -1
0047f3fa  7525                     jne 0x47f421
0047f3fc  8b4603                   mov eax, dword ptr [esi + 3]
0047f3ff  c1f818                   sar eax, 0x18
0047f402  83f8ff                   cmp eax, -1
0047f405  751a                     jne 0x47f421
0047f407  8b4604                   mov eax, dword ptr [esi + 4]
0047f40a  c1f818                   sar eax, 0x18
0047f40d  83f8ff                   cmp eax, -1
0047f410  750f                     jne 0x47f421
0047f412  8b4605                   mov eax, dword ptr [esi + 5]
0047f415  c1f818                   sar eax, 0x18
0047f418  83f8ff                   cmp eax, -1
0047f41b  0f84ae000000             je 0x47f4cf
0047f421  89f1                     mov ecx, esi
0047f423  31db                     xor ebx, ebx
0047f425  eb07                     jmp 0x47f42e
0047f427  43                       inc ebx
0047f428  41                       inc ecx
0047f429  83fb04                   cmp ebx, 4
0047f42c  7d25                     jge 0x47f453
0047f42e  31c0                     xor eax, eax
0047f430  31d2                     xor edx, edx
0047f432  8a0424                   mov al, byte ptr [esp]
0047f435  6689da                   mov dx, bx
0047f438  0fb6bb64844900           movzx edi, byte ptr [ebx + 0x498464]
0047f43f  e87e23ffff               call 0x4717c2 ; -> RechercheGetNiveau
0047f444  25ffff0000               and eax, 0xffff
0047f449  39f8                     cmp eax, edi
0047f44b  7cda                     jl 0x47f427
0047f44d  c64105ff                 mov byte ptr [ecx + 5], 0xff
0047f451  ebd4                     jmp 0x47f427
0047f453  bfffffffff               mov edi, 0xffffffff
0047f458  b864000000               mov eax, 0x64
0047f45d  e8c6a20000               call 0x489728 ; -> iaRandom
0047f462  31db                     xor ebx, ebx
0047f464  89c1                     mov ecx, eax
0047f466  89f0                     mov eax, esi
0047f468  83fb04                   cmp ebx, 4
0047f46b  7d0e                     jge 0x47f47b
0047f46d  8b5002                   mov edx, dword ptr [eax + 2]
0047f470  c1fa18                   sar edx, 0x18
0047f473  39d1                     cmp ecx, edx
0047f475  7c04                     jl 0x47f47b
0047f477  40                       inc eax
0047f478  43                       inc ebx
0047f479  ebed                     jmp 0x47f468
0047f47b  8b441e02                 mov eax, dword ptr [esi + ebx + 2]
0047f47f  c1f818                   sar eax, 0x18
0047f482  89da                     mov edx, ebx
0047f484  83f8ff                   cmp eax, -1
0047f487  7522                     jne 0x47f4ab
0047f489  89fa                     mov edx, edi
0047f48b  89f0                     mov eax, esi
0047f48d  31db                     xor ebx, ebx
0047f48f  eb02                     jmp 0x47f493
0047f491  40                       inc eax
0047f492  43                       inc ebx
0047f493  83fb04                   cmp ebx, 4
0047f496  7d13                     jge 0x47f4ab
0047f498  83faff                   cmp edx, -1
0047f49b  750e                     jne 0x47f4ab
0047f49d  8b4802                   mov ecx, dword ptr [eax + 2]
0047f4a0  c1f918                   sar ecx, 0x18
0047f4a3  39d1                     cmp ecx, edx
0047f4a5  74ea                     je 0x47f491
0047f4a7  89da                     mov edx, ebx
0047f4a9  ebe6                     jmp 0x47f491
0047f4ab  83fa03                   cmp edx, 3
0047f4ae  750f                     jne 0x47f4bf
0047f4b0  e865ccfeff               call 0x46c11a ; -> MissionGetNum
0047f4b5  25ffff0000               and eax, 0xffff
0047f4ba  83f807                   cmp eax, 7
0047f4bd  7c99                     jl 0x47f458
0047f4bf  31c0                     xor eax, eax
0047f4c1  81e2ff000000             and edx, 0xff
0047f4c7  8a0424                   mov al, byte ptr [esp]
0047f4ca  e86816ffff               call 0x470b37 ; -> RechercheSetBranche
0047f4cf  8b4c2410                 mov ecx, dword ptr [esp + 0x10]
0047f4d3  31db                     xor ebx, ebx
0047f4d5  eb01                     jmp 0x47f4d8
0047f4d7  43                       inc ebx
0047f4d8  31d2                     xor edx, edx
0047f4da  6689da                   mov dx, bx
0047f4dd  81fa20030000             cmp edx, 0x320
0047f4e3  7d26                     jge 0x47f50b
0047f4e5  89d0                     mov eax, edx
0047f4e7  e8c148fcff               call 0x443dad ; -> EnginEstVivant
0047f4ec  84c0                     test al, al
0047f4ee  74e7                     je 0x47f4d7
0047f4f0  69d214010000             imul edx, edx, 0x114
0047f4f6  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0047f4fb  8a0402                   mov al, byte ptr [edx + eax]
0047f4fe  25ff000000               and eax, 0xff
0047f503  39c8                     cmp eax, ecx
0047f505  75d0                     jne 0x47f4d7
0047f507  b001                     mov al, 1
0047f509  eb02                     jmp 0x47f50d
0047f50b  30c0                     xor al, al
0047f50d  25ff000000               and eax, 0xff
0047f512  750a                     jne 0x47f51e
0047f514  8b44240c                 mov eax, dword ptr [esp + 0xc]
0047f518  c6400401                 mov byte ptr [eax + 4], 1
0047f51c  eb41                     jmp 0x47f55f
0047f51e  8b44240c                 mov eax, dword ptr [esp + 0xc]
0047f522  31d2                     xor edx, edx
0047f524  c6400400                 mov byte ptr [eax + 4], 0
0047f528  8b442410                 mov eax, dword ptr [esp + 0x10]
0047f52c  c6450000                 mov byte ptr [ebp], 0
0047f530  e872510000               call 0x4846a7 ; -> iagVilleSetMode
0047f535  8b442410                 mov eax, dword ptr [esp + 0x10]
0047f539  31d2                     xor edx, edx
0047f53b  e85a610000               call 0x48569a ; -> iagRessSetMode
0047f540  8b442410                 mov eax, dword ptr [esp + 0x10]
0047f544  31d2                     xor edx, edx
0047f546  e85c770000               call 0x486ca7 ; -> iagWarSetMode
0047f54b  8b44240c                 mov eax, dword ptr [esp + 0xc]
0047f54f  c6400100                 mov byte ptr [eax + 1], 0
0047f553  c6400201                 mov byte ptr [eax + 2], 1
0047f557  c6400300                 mov byte ptr [eax + 3], 0
0047f55b  c6400900                 mov byte ptr [eax + 9], 0
0047f55f  8b5c2410                 mov ebx, dword ptr [esp + 0x10]
0047f563  43                       inc ebx
0047f564  83c510                   add ebp, 0x10
0047f567  895c2410                 mov dword ptr [esp + 0x10], ebx
0047f56b  83fb04                   cmp ebx, 4
0047f56e  7d72                     jge 0x47f5e2
0047f570  31c0                     xor eax, eax
0047f572  8a442410                 mov al, byte ptr [esp + 0x10]
0047f576  e89ce2feff               call 0x46d817 ; -> PlayerGetType
0047f57b  25ff000000               and eax, 0xff
0047f580  83f802                   cmp eax, 2
0047f583  75da                     jne 0x47f55f
0047f585  8b442410                 mov eax, dword ptr [esp + 0x10]
0047f589  890424                   mov dword ptr [esp], eax
0047f58c  8b4502                   mov eax, dword ptr [ebp + 2]
0047f58f  896c240c                 mov dword ptr [esp + 0xc], ebp
0047f593  c1f818                   sar eax, 0x18
0047f596  89ee                     mov esi, ebp
0047f598  85c0                     test eax, eax
0047f59a  0f8551feffff             jne 0x47f3f1
0047f5a0  8b4503                   mov eax, dword ptr [ebp + 3]
0047f5a3  c1f818                   sar eax, 0x18
0047f5a6  85c0                     test eax, eax
0047f5a8  0f8543feffff             jne 0x47f3f1
0047f5ae  8b4504                   mov eax, dword ptr [ebp + 4]
0047f5b1  c1f818                   sar eax, 0x18
0047f5b4  85c0                     test eax, eax
0047f5b6  0f8535feffff             jne 0x47f3f1
0047f5bc  8b4505                   mov eax, dword ptr [ebp + 5]
0047f5bf  c1f818                   sar eax, 0x18
0047f5c2  85c0                     test eax, eax
0047f5c4  0f8527feffff             jne 0x47f3f1
0047f5ca  8b7c2410                 mov edi, dword ptr [esp + 0x10]
0047f5ce  896c2408                 mov dword ptr [esp + 8], ebp
0047f5d2  83ff03                   cmp edi, 3
0047f5d5  0f85acfdffff             jne 0x47f387
0047f5db  31ff                     xor edi, edi
0047f5dd  e9b6fdffff               jmp 0x47f398
0047f5e2  e839dcffff               call 0x47d220 ; -> iaProbReset
0047f5e7  85c0                     test eax, eax
0047f5e9  7404                     je 0x47f5ef
0047f5eb  89c1                     mov ecx, eax
0047f5ed  eb30                     jmp 0x47f61f
0047f5ef  e817310000               call 0x48270b ; -> iagUnitReset
0047f5f4  85c0                     test eax, eax
0047f5f6  75f3                     jne 0x47f5eb
0047f5f8  e8134d0000               call 0x484310 ; -> iagVilleReset
0047f5fd  85c0                     test eax, eax
0047f5ff  75ea                     jne 0x47f5eb
0047f601  e8461d0000               call 0x48134c ; -> iafRessourceReset
0047f606  e8f7590000               call 0x485002 ; -> iagRessReset
0047f60b  85c0                     test eax, eax
0047f60d  75dc                     jne 0x47f5eb
0047f60f  e8ad6e0000               call 0x4864c1 ; -> iagWarReset
0047f614  85c0                     test eax, eax
0047f616  75d3                     jne 0x47f5eb
0047f618  e873b9ffff               call 0x47af90 ; -> InitMissionMonstre
0047f61d  31c9                     xor ecx, ecx
0047f61f  89c8                     mov eax, ecx
0047f621  83c41c                   add esp, 0x1c
0047f624  5d                       pop ebp
0047f625  5f                       pop edi
0047f626  5e                       pop esi
0047f627  5a                       pop edx
0047f628  59                       pop ecx
0047f629  5b                       pop ebx
0047f62a  c3                       ret
