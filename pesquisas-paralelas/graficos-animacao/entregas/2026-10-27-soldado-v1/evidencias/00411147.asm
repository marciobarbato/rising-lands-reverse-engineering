; AffCorpsEngin [0x411147, 0x41209d)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00411147  56                     push     esi
00411148  57                     push     edi
00411149  55                     push     ebp
0041114a  81ec9c000000           sub      esp, 0x9c
00411150  89c7                   mov      edi, eax
00411152  6689942494000000       mov      word ptr [esp + 0x94], dx
0041115a  899c2490000000         mov      dword ptr [esp + 0x90], ebx
00411161  89ce                   mov      esi, ecx
00411163  0fb7e9                 movzx    ebp, cx
00411166  89e8                   mov      eax, ebp
00411168  e8d80e0300             call     0x442045 ; EnginGetPlayer
0041116d  88842498000000         mov      byte ptr [esp + 0x98], al
00411174  3c04                   cmp      al, 4
00411176  0f82a80d0000           jb       0x411f24
0041117c  0f86710a0000           jbe      0x411bf3
00411182  3cc8                   cmp      al, 0xc8
00411184  0f8464040000           je       0x4115ee
0041118a  31d2                   xor      edx, edx
0041118c  6689f2                 mov      dx, si
0041118f  89d0                   mov      eax, edx
00411191  e868ee0300             call     0x44fffe ; EnginEstMiroir
00411196  84c0                   test     al, al
00411198  750b                   jne      0x4111a5
0041119a  89d0                   mov      eax, edx
0041119c  e88dee0300             call     0x45002e ; EnginEstTerreur
004111a1  84c0                   test     al, al
004111a3  7444                   je       0x4111e9
004111a5  31c0                   xor      eax, eax
004111a7  6689f0                 mov      ax, si
004111aa  e84fee0300             call     0x44fffe ; EnginEstMiroir
004111af  84c0                   test     al, al
004111b1  0f84700b0000           je       0x411d27
004111b7  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
004111bd  31d2                   xor      edx, edx
004111bf  88da                   mov      dl, bl
004111c1  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
004111c7  81e2ff000000           and      edx, 0xff
004111cd  bd02000000             mov      ebp, 2
004111d2  89d0                   mov      eax, edx
004111d4  c1fa1f                 sar      edx, 0x1f
004111d7  f7fd                   idiv     ebp
004111d9  fec3                   inc      bl
004111db  881d181d4e00           mov      byte ptr [0x4e1d18], bl
004111e1  85d2                   test     edx, edx
004111e3  0f853e0b0000           jne      0x411d27
004111e9  8bac2492000000         mov      ebp, dword ptr [esp + 0x92]
004111f0  31c0                   xor      eax, eax
004111f2  b901000000             mov      ecx, 1
004111f7  8a842498000000         mov      al, byte ptr [esp + 0x98]
004111fe  c1fd10                 sar      ebp, 0x10
00411201  89442444               mov      dword ptr [esp + 0x44], eax
00411205  89c3                   mov      ebx, eax
00411207  50                     push     eax
00411208  89ea                   mov      edx, ebp
0041120a  31c3                   xor      ebx, eax
0041120c  0fbfc7                 movsx    eax, di
0041120f  668b9c2494000000       mov      bx, word ptr [esp + 0x94]
00411217  89442428               mov      dword ptr [esp + 0x28], eax
0041121b  e835b20400             call     0x45c455 ; PastePlayerCmp
00411220  31d2                   xor      edx, edx
00411222  6689f2                 mov      dx, si
00411225  89d0                   mov      eax, edx
00411227  e8f90d0300             call     0x442025 ; EnginGetType
0041122c  25ff000000             and      eax, 0xff
00411231  83f80f                 cmp      eax, 0xf
00411234  0f85b40a0000           jne      0x411cee
0041123a  8b442444               mov      eax, dword ptr [esp + 0x44]
0041123e  50                     push     eax
0041123f  89d0                   mov      eax, edx
00411241  e8ebfb0200             call     0x440e31 ; EnginGetTourDir
00411246  30e4                   xor      ah, ah
00411248  48                     dec      eax
00411249  b901000000             mov      ecx, 1
0041124e  01c0                   add      eax, eax
00411250  31db                   xor      ebx, ebx
00411252  0572110000             add      eax, 0x1172
00411257  89ea                   mov      edx, ebp
00411259  6689c3                 mov      bx, ax
0041125c  8b442428               mov      eax, dword ptr [esp + 0x28]
00411260  e8f0b10400             call     0x45c455 ; PastePlayerCmp
00411265  0fb7ee                 movzx    ebp, si
00411268  89e8                   mov      eax, ebp
0041126a  e8e5ed0300             call     0x450054 ; EnginEstArmure
0041126f  84c0                   test     al, al
00411271  0f84eb0c0000           je       0x411f62
00411277  31d2                   xor      edx, edx
00411279  89e8                   mov      eax, ebp
0041127b  89942484000000         mov      dword ptr [esp + 0x84], edx
00411282  8954247c               mov      dword ptr [esp + 0x7c], edx
00411286  e89a0d0300             call     0x442025 ; EnginGetType
0041128b  8d5c247c               lea      ebx, [esp + 0x7c]
0041128f  8d942484000000         lea      edx, [esp + 0x84]
00411296  25ff000000             and      eax, 0xff
0041129b  e82cfdffff             call     0x410fcc ; AffCorpsEnginDecalage
004112a0  8b44247c               mov      eax, dword ptr [esp + 0x7c]
004112a4  8b942494000000         mov      edx, dword ptr [esp + 0x94]
004112ab  29c2                   sub      edx, eax
004112ad  8d9c2480000000         lea      ebx, [esp + 0x80]
004112b4  6689942494000000       mov      word ptr [esp + 0x94], dx
004112bc  89e8                   mov      eax, ebp
004112be  8d94248c000000         lea      edx, [esp + 0x8c]
004112c5  8b8c2484000000         mov      ecx, dword ptr [esp + 0x84]
004112cc  e89bfd0200             call     0x44106c ; EnginGetTaille
004112d1  31c0                   xor      eax, eax
004112d3  668b84248c000000       mov      ax, word ptr [esp + 0x8c]
004112db  29cf                   sub      edi, ecx
004112dd  83f802                 cmp      eax, 2
004112e0  0f854b0c0000           jne      0x411f31
004112e6  31c0                   xor      eax, eax
004112e8  668b842480000000       mov      ax, word ptr [esp + 0x80]
004112f0  83f802                 cmp      eax, 2
004112f3  0f85380c0000           jne      0x411f31
004112f9  66a17c8f5000           mov      ax, word ptr [0x508f7c]
004112ff  30e4                   xor      ah, ah
00411301  243f                   and      al, 0x3f
00411303  31db                   xor      ebx, ebx
00411305  053d2b0000             add      eax, 0x2b3d
0041130a  6689c3                 mov      bx, ax
0041130d  8b842494000000         mov      eax, dword ptr [esp + 0x94]
00411314  83e82a                 sub      eax, 0x2a
00411317  0fbfd0                 movsx    edx, ax
0041131a  89f8                   mov      eax, edi
0041131c  83e82a                 sub      eax, 0x2a
0041131f  e9330c0000             jmp      0x411f57 ; 
00411324  89e8                   mov      eax, ebp
00411326  e8d3ec0300             call     0x44fffe ; EnginEstMiroir
0041132b  84c0                   test     al, al
0041132d  750b                   jne      0x41133a
0041132f  89e8                   mov      eax, ebp
00411331  e8f8ec0300             call     0x45002e ; EnginEstTerreur
00411336  84c0                   test     al, al
00411338  7444                   je       0x41137e
0041133a  31c0                   xor      eax, eax
0041133c  6689f0                 mov      ax, si
0041133f  e8baec0300             call     0x44fffe ; EnginEstMiroir
00411344  84c0                   test     al, al
00411346  0f84c9000000           je       0x411415
0041134c  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00411352  31d2                   xor      edx, edx
00411354  88da                   mov      dl, bl
00411356  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
0041135c  81e2ff000000           and      edx, 0xff
00411362  bd02000000             mov      ebp, 2
00411367  89d0                   mov      eax, edx
00411369  c1fa1f                 sar      edx, 0x1f
0041136c  f7fd                   idiv     ebp
0041136e  fec3                   inc      bl
00411370  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00411376  85d2                   test     edx, edx
00411378  0f8597000000           jne      0x411415
0041137e  8bac2492000000         mov      ebp, dword ptr [esp + 0x92]
00411385  b901000000             mov      ecx, 1
0041138a  0fbfc7                 movsx    eax, di
0041138d  31db                   xor      ebx, ebx
0041138f  c1fd10                 sar      ebp, 0x10
00411392  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
0041139a  89ea                   mov      edx, ebp
0041139c  89442460               mov      dword ptr [esp + 0x60], eax
004113a0  e8a29e0400             call     0x45b247 ; PasteBobCmp
004113a5  31d2                   xor      edx, edx
004113a7  6689f2                 mov      dx, si
004113aa  89d0                   mov      eax, edx
004113ac  e8740c0300             call     0x442025 ; EnginGetType
004113b1  25ff000000             and      eax, 0xff
004113b6  83f80f                 cmp      eax, 0xf
004113b9  752b                   jne      0x4113e6
004113bb  89d0                   mov      eax, edx
004113bd  e86ffa0200             call     0x440e31 ; EnginGetTourDir
004113c2  30e4                   xor      ah, ah
004113c4  48                     dec      eax
004113c5  b901000000             mov      ecx, 1
004113ca  01c0                   add      eax, eax
004113cc  31db                   xor      ebx, ebx
004113ce  0572110000             add      eax, 0x1172
004113d3  89ea                   mov      edx, ebp
004113d5  6689c3                 mov      bx, ax
004113d8  8b442460               mov      eax, dword ptr [esp + 0x60]
004113dc  e8669e0400             call     0x45b247 ; PasteBobCmp
004113e1  e97ffeffff             jmp      0x411265 ; 
004113e6  89d0                   mov      eax, edx
004113e8  e8380c0300             call     0x442025 ; EnginGetType
004113ed  25ff000000             and      eax, 0xff
004113f2  83f80c                 cmp      eax, 0xc
004113f5  0f856afeffff           jne      0x411265
004113fb  89d0                   mov      eax, edx
004113fd  e82ffa0200             call     0x440e31 ; EnginGetTourDir
00411402  30e4                   xor      ah, ah
00411404  48                     dec      eax
00411405  b901000000             mov      ecx, 1
0041140a  01c0                   add      eax, eax
0041140c  31db                   xor      ebx, ebx
0041140e  0532120000             add      eax, 0x1232
00411413  ebbe                   jmp      0x4113d3 ; 
00411415  0fb7ee                 movzx    ebp, si
00411418  89e8                   mov      eax, ebp
0041141a  e80fec0300             call     0x45002e ; EnginEstTerreur
0041141f  84c0                   test     al, al
00411421  0f8423010000           je       0x41154a
00411427  8b842492000000         mov      eax, dword ptr [esp + 0x92]
0041142e  b901000000             mov      ecx, 1
00411433  31db                   xor      ebx, ebx
00411435  c1f810                 sar      eax, 0x10
00411438  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411440  8944240c               mov      dword ptr [esp + 0xc], eax
00411444  0fbfc7                 movsx    eax, di
00411447  8b54240c               mov      edx, dword ptr [esp + 0xc]
0041144b  89442450               mov      dword ptr [esp + 0x50], eax
0041144f  e8f39d0400             call     0x45b247 ; PasteBobCmp
00411454  89e8                   mov      eax, ebp
00411456  e8ca0b0300             call     0x442025 ; EnginGetType
0041145b  25ff000000             and      eax, 0xff
00411460  83f80f                 cmp      eax, 0xf
00411463  751a                   jne      0x41147f
00411465  89e8                   mov      eax, ebp
00411467  e8c5f90200             call     0x440e31 ; EnginGetTourDir
0041146c  30e4                   xor      ah, ah
0041146e  48                     dec      eax
0041146f  b901000000             mov      ecx, 1
00411474  01c0                   add      eax, eax
00411476  31db                   xor      ebx, ebx
00411478  0572110000             add      eax, 0x1172
0041147d  eb29                   jmp      0x4114a8 ; 
0041147f  89e8                   mov      eax, ebp
00411481  e89f0b0300             call     0x442025 ; EnginGetType
00411486  25ff000000             and      eax, 0xff
0041148b  83f80c                 cmp      eax, 0xc
0041148e  7528                   jne      0x4114b8
00411490  89e8                   mov      eax, ebp
00411492  e89af90200             call     0x440e31 ; EnginGetTourDir
00411497  30e4                   xor      ah, ah
00411499  48                     dec      eax
0041149a  b901000000             mov      ecx, 1
0041149f  01c0                   add      eax, eax
004114a1  31db                   xor      ebx, ebx
004114a3  0532120000             add      eax, 0x1232
004114a8  8b54240c               mov      edx, dword ptr [esp + 0xc]
004114ac  6689c3                 mov      bx, ax
004114af  8b442450               mov      eax, dword ptr [esp + 0x50]
004114b3  e88f9d0400             call     0x45b247 ; PasteBobCmp
004114b8  8bac2492000000         mov      ebp, dword ptr [esp + 0x92]
004114bf  b901000000             mov      ecx, 1
004114c4  0fbfc7                 movsx    eax, di
004114c7  31db                   xor      ebx, ebx
004114c9  c1fd10                 sar      ebp, 0x10
004114cc  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
004114d4  89ea                   mov      edx, ebp
004114d6  89442410               mov      dword ptr [esp + 0x10], eax
004114da  e8d1a70400             call     0x45bcb0 ; PasteGrisCmp
004114df  31d2                   xor      edx, edx
004114e1  6689f2                 mov      dx, si
004114e4  89d0                   mov      eax, edx
004114e6  e83a0b0300             call     0x442025 ; EnginGetType
004114eb  25ff000000             and      eax, 0xff
004114f0  83f80f                 cmp      eax, 0xf
004114f3  7526                   jne      0x41151b
004114f5  89d0                   mov      eax, edx
004114f7  e835f90200             call     0x440e31 ; EnginGetTourDir
004114fc  30e4                   xor      ah, ah
004114fe  48                     dec      eax
004114ff  b901000000             mov      ecx, 1
00411504  01c0                   add      eax, eax
00411506  31db                   xor      ebx, ebx
00411508  0572110000             add      eax, 0x1172
0041150d  89ea                   mov      edx, ebp
0041150f  6689c3                 mov      bx, ax
00411512  8b442410               mov      eax, dword ptr [esp + 0x10]
00411516  e927090000             jmp      0x411e42 ; 
0041151b  89d0                   mov      eax, edx
0041151d  e8030b0300             call     0x442025 ; EnginGetType
00411522  25ff000000             and      eax, 0xff
00411527  83f80c                 cmp      eax, 0xc
0041152a  0f8535fdffff           jne      0x411265
00411530  89d0                   mov      eax, edx
00411532  e8faf80200             call     0x440e31 ; EnginGetTourDir
00411537  30e4                   xor      ah, ah
00411539  48                     dec      eax
0041153a  b901000000             mov      ecx, 1
0041153f  01c0                   add      eax, eax
00411541  31db                   xor      ebx, ebx
00411543  0532120000             add      eax, 0x1232
00411548  ebc3                   jmp      0x41150d ; 
0041154a  89e8                   mov      eax, ebp
0041154c  e8adea0300             call     0x44fffe ; EnginEstMiroir
00411551  84c0                   test     al, al
00411553  0f840cfdffff           je       0x411265
00411559  8b842492000000         mov      eax, dword ptr [esp + 0x92]
00411560  b901000000             mov      ecx, 1
00411565  31db                   xor      ebx, ebx
00411567  c1f810                 sar      eax, 0x10
0041156a  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411572  89442418               mov      dword ptr [esp + 0x18], eax
00411576  0fbfc7                 movsx    eax, di
00411579  8b542418               mov      edx, dword ptr [esp + 0x18]
0041157d  89442420               mov      dword ptr [esp + 0x20], eax
00411581  e89da40400             call     0x45ba23 ; PasteEclairCmp
00411586  89e8                   mov      eax, ebp
00411588  e8980a0300             call     0x442025 ; EnginGetType
0041158d  25ff000000             and      eax, 0xff
00411592  83f80f                 cmp      eax, 0xf
00411595  7528                   jne      0x4115bf
00411597  89e8                   mov      eax, ebp
00411599  e893f80200             call     0x440e31 ; EnginGetTourDir
0041159e  30e4                   xor      ah, ah
004115a0  48                     dec      eax
004115a1  b901000000             mov      ecx, 1
004115a6  01c0                   add      eax, eax
004115a8  31db                   xor      ebx, ebx
004115aa  0572110000             add      eax, 0x1172
004115af  8b542418               mov      edx, dword ptr [esp + 0x18]
004115b3  6689c3                 mov      bx, ax
004115b6  8b442420               mov      eax, dword ptr [esp + 0x20]
004115ba  e92c090000             jmp      0x411eeb ; 
004115bf  89e8                   mov      eax, ebp
004115c1  e85f0a0300             call     0x442025 ; EnginGetType
004115c6  25ff000000             and      eax, 0xff
004115cb  83f80c                 cmp      eax, 0xc
004115ce  0f8591fcffff           jne      0x411265
004115d4  89e8                   mov      eax, ebp
004115d6  e856f80200             call     0x440e31 ; EnginGetTourDir
004115db  30e4                   xor      ah, ah
004115dd  48                     dec      eax
004115de  b901000000             mov      ecx, 1
004115e3  01c0                   add      eax, eax
004115e5  31db                   xor      ebx, ebx
004115e7  0532120000             add      eax, 0x1232
004115ec  ebc1                   jmp      0x4115af ; 
004115ee  31c0                   xor      eax, eax
004115f0  6689d8                 mov      ax, bx
004115f3  89442434               mov      dword ptr [esp + 0x34], eax
004115f7  8b842492000000         mov      eax, dword ptr [esp + 0x92]
004115fe  b901000000             mov      ecx, 1
00411603  c1f810                 sar      eax, 0x10
00411606  8b5c2434               mov      ebx, dword ptr [esp + 0x34]
0041160a  89442438               mov      dword ptr [esp + 0x38], eax
0041160e  0fbfc7                 movsx    eax, di
00411611  8b542438               mov      edx, dword ptr [esp + 0x38]
00411615  8944246c               mov      dword ptr [esp + 0x6c], eax
00411619  e8299c0400             call     0x45b247 ; PasteBobCmp
0041161e  b901000000             mov      ecx, 1
00411623  8b5c2434               mov      ebx, dword ptr [esp + 0x34]
00411627  8b542438               mov      edx, dword ptr [esp + 0x38]
0041162b  8b44246c               mov      eax, dword ptr [esp + 0x6c]
0041162f  e87ca60400             call     0x45bcb0 ; PasteGrisCmp
00411634  89e8                   mov      eax, ebp
00411636  e8ea090300             call     0x442025 ; EnginGetType
0041163b  25ff000000             and      eax, 0xff
00411640  83f80f                 cmp      eax, 0xf
00411643  7550                   jne      0x411695
00411645  89e8                   mov      eax, ebp
00411647  e8e5f70200             call     0x440e31 ; EnginGetTourDir
0041164c  30e4                   xor      ah, ah
0041164e  48                     dec      eax
0041164f  b901000000             mov      ecx, 1
00411654  01c0                   add      eax, eax
00411656  31db                   xor      ebx, ebx
00411658  0572110000             add      eax, 0x1172
0041165d  8b542438               mov      edx, dword ptr [esp + 0x38]
00411661  6689c3                 mov      bx, ax
00411664  8b44246c               mov      eax, dword ptr [esp + 0x6c]
00411668  e8da9b0400             call     0x45b247 ; PasteBobCmp
0041166d  89e8                   mov      eax, ebp
0041166f  e8bdf70200             call     0x440e31 ; EnginGetTourDir
00411674  30e4                   xor      ah, ah
00411676  48                     dec      eax
00411677  b901000000             mov      ecx, 1
0041167c  01c0                   add      eax, eax
0041167e  31db                   xor      ebx, ebx
00411680  0572110000             add      eax, 0x1172
00411685  8b542438               mov      edx, dword ptr [esp + 0x38]
00411689  6689c3                 mov      bx, ax
0041168c  8b44246c               mov      eax, dword ptr [esp + 0x6c]
00411690  e9ad070000             jmp      0x411e42 ; 
00411695  89e8                   mov      eax, ebp
00411697  e889090300             call     0x442025 ; EnginGetType
0041169c  25ff000000             and      eax, 0xff
004116a1  83f80c                 cmp      eax, 0xc
004116a4  0f85bbfbffff           jne      0x411265
004116aa  89e8                   mov      eax, ebp
004116ac  e880f70200             call     0x440e31 ; EnginGetTourDir
004116b1  30e4                   xor      ah, ah
004116b3  48                     dec      eax
004116b4  b901000000             mov      ecx, 1
004116b9  01c0                   add      eax, eax
004116bb  31db                   xor      ebx, ebx
004116bd  0532120000             add      eax, 0x1232
004116c2  8b542438               mov      edx, dword ptr [esp + 0x38]
004116c6  6689c3                 mov      bx, ax
004116c9  8b44246c               mov      eax, dword ptr [esp + 0x6c]
004116cd  e8759b0400             call     0x45b247 ; PasteBobCmp
004116d2  89e8                   mov      eax, ebp
004116d4  e858f70200             call     0x440e31 ; EnginGetTourDir
004116d9  30e4                   xor      ah, ah
004116db  48                     dec      eax
004116dc  b901000000             mov      ecx, 1
004116e1  01c0                   add      eax, eax
004116e3  31db                   xor      ebx, ebx
004116e5  0532120000             add      eax, 0x1232
004116ea  eb99                   jmp      0x411685 ; 
004116ec  31d2                   xor      edx, edx
004116ee  6689f2                 mov      dx, si
004116f1  89d0                   mov      eax, edx
004116f3  e806e90300             call     0x44fffe ; EnginEstMiroir
004116f8  84c0                   test     al, al
004116fa  750b                   jne      0x411707
004116fc  89d0                   mov      eax, edx
004116fe  e82be90300             call     0x45002e ; EnginEstTerreur
00411703  84c0                   test     al, al
00411705  7444                   je       0x41174b
00411707  31c0                   xor      eax, eax
00411709  6689f0                 mov      ax, si
0041170c  e8ede80300             call     0x44fffe ; EnginEstMiroir
00411711  84c0                   test     al, al
00411713  0f84c9000000           je       0x4117e2
00411719  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
0041171f  31d2                   xor      edx, edx
00411721  88da                   mov      dl, bl
00411723  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00411729  81e2ff000000           and      edx, 0xff
0041172f  bd02000000             mov      ebp, 2
00411734  89d0                   mov      eax, edx
00411736  c1fa1f                 sar      edx, 0x1f
00411739  f7fd                   idiv     ebp
0041173b  fec3                   inc      bl
0041173d  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00411743  85d2                   test     edx, edx
00411745  0f8597000000           jne      0x4117e2
0041174b  8bac2492000000         mov      ebp, dword ptr [esp + 0x92]
00411752  b901000000             mov      ecx, 1
00411757  0fbfc7                 movsx    eax, di
0041175a  31db                   xor      ebx, ebx
0041175c  c1fd10                 sar      ebp, 0x10
0041175f  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411767  89ea                   mov      edx, ebp
00411769  8944243c               mov      dword ptr [esp + 0x3c], eax
0041176d  e8d59a0400             call     0x45b247 ; PasteBobCmp
00411772  31d2                   xor      edx, edx
00411774  6689f2                 mov      dx, si
00411777  89d0                   mov      eax, edx
00411779  e8a7080300             call     0x442025 ; EnginGetType
0041177e  25ff000000             and      eax, 0xff
00411783  83f80f                 cmp      eax, 0xf
00411786  752b                   jne      0x4117b3
00411788  89d0                   mov      eax, edx
0041178a  e8a2f60200             call     0x440e31 ; EnginGetTourDir
0041178f  30e4                   xor      ah, ah
00411791  48                     dec      eax
00411792  b901000000             mov      ecx, 1
00411797  01c0                   add      eax, eax
00411799  31db                   xor      ebx, ebx
0041179b  0572110000             add      eax, 0x1172
004117a0  89ea                   mov      edx, ebp
004117a2  6689c3                 mov      bx, ax
004117a5  8b44243c               mov      eax, dword ptr [esp + 0x3c]
004117a9  e8999a0400             call     0x45b247 ; PasteBobCmp
004117ae  e9d7f9ffff             jmp      0x41118a ; 
004117b3  89d0                   mov      eax, edx
004117b5  e86b080300             call     0x442025 ; EnginGetType
004117ba  25ff000000             and      eax, 0xff
004117bf  83f80c                 cmp      eax, 0xc
004117c2  0f85c2f9ffff           jne      0x41118a
004117c8  89d0                   mov      eax, edx
004117ca  e862f60200             call     0x440e31 ; EnginGetTourDir
004117cf  30e4                   xor      ah, ah
004117d1  48                     dec      eax
004117d2  b901000000             mov      ecx, 1
004117d7  01c0                   add      eax, eax
004117d9  31db                   xor      ebx, ebx
004117db  0532120000             add      eax, 0x1232
004117e0  ebbe                   jmp      0x4117a0 ; 
004117e2  0fb7ee                 movzx    ebp, si
004117e5  89e8                   mov      eax, ebp
004117e7  e842e80300             call     0x45002e ; EnginEstTerreur
004117ec  84c0                   test     al, al
004117ee  0f8423010000           je       0x411917
004117f4  8b842492000000         mov      eax, dword ptr [esp + 0x92]
004117fb  b901000000             mov      ecx, 1
00411800  31db                   xor      ebx, ebx
00411802  c1f810                 sar      eax, 0x10
00411805  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
0041180d  89442468               mov      dword ptr [esp + 0x68], eax
00411811  0fbfc7                 movsx    eax, di
00411814  8b542468               mov      edx, dword ptr [esp + 0x68]
00411818  8944242c               mov      dword ptr [esp + 0x2c], eax
0041181c  e8269a0400             call     0x45b247 ; PasteBobCmp
00411821  89e8                   mov      eax, ebp
00411823  e8fd070300             call     0x442025 ; EnginGetType
00411828  25ff000000             and      eax, 0xff
0041182d  83f80f                 cmp      eax, 0xf
00411830  751a                   jne      0x41184c
00411832  89e8                   mov      eax, ebp
00411834  e8f8f50200             call     0x440e31 ; EnginGetTourDir
00411839  30e4                   xor      ah, ah
0041183b  48                     dec      eax
0041183c  b901000000             mov      ecx, 1
00411841  01c0                   add      eax, eax
00411843  31db                   xor      ebx, ebx
00411845  0572110000             add      eax, 0x1172
0041184a  eb29                   jmp      0x411875 ; 
0041184c  89e8                   mov      eax, ebp
0041184e  e8d2070300             call     0x442025 ; EnginGetType
00411853  25ff000000             and      eax, 0xff
00411858  83f80c                 cmp      eax, 0xc
0041185b  7528                   jne      0x411885
0041185d  89e8                   mov      eax, ebp
0041185f  e8cdf50200             call     0x440e31 ; EnginGetTourDir
00411864  30e4                   xor      ah, ah
00411866  48                     dec      eax
00411867  b901000000             mov      ecx, 1
0041186c  01c0                   add      eax, eax
0041186e  31db                   xor      ebx, ebx
00411870  0532120000             add      eax, 0x1232
00411875  8b542468               mov      edx, dword ptr [esp + 0x68]
00411879  6689c3                 mov      bx, ax
0041187c  8b44242c               mov      eax, dword ptr [esp + 0x2c]
00411880  e8c2990400             call     0x45b247 ; PasteBobCmp
00411885  8bac2492000000         mov      ebp, dword ptr [esp + 0x92]
0041188c  b901000000             mov      ecx, 1
00411891  0fbfc7                 movsx    eax, di
00411894  31db                   xor      ebx, ebx
00411896  c1fd10                 sar      ebp, 0x10
00411899  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
004118a1  89ea                   mov      edx, ebp
004118a3  89442414               mov      dword ptr [esp + 0x14], eax
004118a7  e804a40400             call     0x45bcb0 ; PasteGrisCmp
004118ac  31d2                   xor      edx, edx
004118ae  6689f2                 mov      dx, si
004118b1  89d0                   mov      eax, edx
004118b3  e86d070300             call     0x442025 ; EnginGetType
004118b8  25ff000000             and      eax, 0xff
004118bd  83f80f                 cmp      eax, 0xf
004118c0  7526                   jne      0x4118e8
004118c2  89d0                   mov      eax, edx
004118c4  e868f50200             call     0x440e31 ; EnginGetTourDir
004118c9  30e4                   xor      ah, ah
004118cb  48                     dec      eax
004118cc  b901000000             mov      ecx, 1
004118d1  01c0                   add      eax, eax
004118d3  31db                   xor      ebx, ebx
004118d5  0572110000             add      eax, 0x1172
004118da  89ea                   mov      edx, ebp
004118dc  6689c3                 mov      bx, ax
004118df  8b442414               mov      eax, dword ptr [esp + 0x14]
004118e3  e929020000             jmp      0x411b11 ; 
004118e8  89d0                   mov      eax, edx
004118ea  e836070300             call     0x442025 ; EnginGetType
004118ef  25ff000000             and      eax, 0xff
004118f4  83f80c                 cmp      eax, 0xc
004118f7  0f858df8ffff           jne      0x41118a
004118fd  89d0                   mov      eax, edx
004118ff  e82df50200             call     0x440e31 ; EnginGetTourDir
00411904  30e4                   xor      ah, ah
00411906  48                     dec      eax
00411907  b901000000             mov      ecx, 1
0041190c  01c0                   add      eax, eax
0041190e  31db                   xor      ebx, ebx
00411910  0532120000             add      eax, 0x1232
00411915  ebc3                   jmp      0x4118da ; 
00411917  89e8                   mov      eax, ebp
00411919  e8e0e60300             call     0x44fffe ; EnginEstMiroir
0041191e  84c0                   test     al, al
00411920  0f8464f8ffff           je       0x41118a
00411926  8b842492000000         mov      eax, dword ptr [esp + 0x92]
0041192d  b901000000             mov      ecx, 1
00411932  31db                   xor      ebx, ebx
00411934  c1f810                 sar      eax, 0x10
00411937  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
0041193f  89442440               mov      dword ptr [esp + 0x40], eax
00411943  0fbfc7                 movsx    eax, di
00411946  8b542440               mov      edx, dword ptr [esp + 0x40]
0041194a  89442408               mov      dword ptr [esp + 8], eax
0041194e  e8d0a00400             call     0x45ba23 ; PasteEclairCmp
00411953  89e8                   mov      eax, ebp
00411955  e8cb060300             call     0x442025 ; EnginGetType
0041195a  25ff000000             and      eax, 0xff
0041195f  83f80f                 cmp      eax, 0xf
00411962  7528                   jne      0x41198c
00411964  89e8                   mov      eax, ebp
00411966  e8c6f40200             call     0x440e31 ; EnginGetTourDir
0041196b  30e4                   xor      ah, ah
0041196d  48                     dec      eax
0041196e  b901000000             mov      ecx, 1
00411973  01c0                   add      eax, eax
00411975  31db                   xor      ebx, ebx
00411977  0572110000             add      eax, 0x1172
0041197c  8b542440               mov      edx, dword ptr [esp + 0x40]
00411980  6689c3                 mov      bx, ax
00411983  8b442408               mov      eax, dword ptr [esp + 8]
00411987  e92e020000             jmp      0x411bba ; 
0041198c  89e8                   mov      eax, ebp
0041198e  e892060300             call     0x442025 ; EnginGetType
00411993  25ff000000             and      eax, 0xff
00411998  83f80c                 cmp      eax, 0xc
0041199b  0f85e9f7ffff           jne      0x41118a
004119a1  89e8                   mov      eax, ebp
004119a3  e889f40200             call     0x440e31 ; EnginGetTourDir
004119a8  30e4                   xor      ah, ah
004119aa  48                     dec      eax
004119ab  b901000000             mov      ecx, 1
004119b0  01c0                   add      eax, eax
004119b2  31db                   xor      ebx, ebx
004119b4  0532120000             add      eax, 0x1232
004119b9  ebc1                   jmp      0x41197c ; 
004119bb  89d0                   mov      eax, edx
004119bd  e863060300             call     0x442025 ; EnginGetType
004119c2  25ff000000             and      eax, 0xff
004119c7  83f80c                 cmp      eax, 0xc
004119ca  0f85baf7ffff           jne      0x41118a
004119d0  8b442430               mov      eax, dword ptr [esp + 0x30]
004119d4  50                     push     eax
004119d5  89d0                   mov      eax, edx
004119d7  e855f40200             call     0x440e31 ; EnginGetTourDir
004119dc  30e4                   xor      ah, ah
004119de  48                     dec      eax
004119df  b901000000             mov      ecx, 1
004119e4  01c0                   add      eax, eax
004119e6  31db                   xor      ebx, ebx
004119e8  0532120000             add      eax, 0x1232
004119ed  e9e9020000             jmp      0x411cdb ; 
004119f2  0fb7ee                 movzx    ebp, si
004119f5  89e8                   mov      eax, ebp
004119f7  e832e60300             call     0x45002e ; EnginEstTerreur
004119fc  84c0                   test     al, al
004119fe  0f8446010000           je       0x411b4a
00411a04  31c0                   xor      eax, eax
00411a06  8a842498000000         mov      al, byte ptr [esp + 0x98]
00411a0d  b901000000             mov      ecx, 1
00411a12  89442454               mov      dword ptr [esp + 0x54], eax
00411a16  50                     push     eax
00411a17  8b842496000000         mov      eax, dword ptr [esp + 0x96]
00411a1e  31db                   xor      ebx, ebx
00411a20  c1f810                 sar      eax, 0x10
00411a23  668b9c2494000000       mov      bx, word ptr [esp + 0x94]
00411a2b  8944245c               mov      dword ptr [esp + 0x5c], eax
00411a2f  0fbfc7                 movsx    eax, di
00411a32  8b54245c               mov      edx, dword ptr [esp + 0x5c]
00411a36  8944247c               mov      dword ptr [esp + 0x7c], eax
00411a3a  e816aa0400             call     0x45c455 ; PastePlayerCmp
00411a3f  89e8                   mov      eax, ebp
00411a41  e8df050300             call     0x442025 ; EnginGetType
00411a46  25ff000000             and      eax, 0xff
00411a4b  83f80f                 cmp      eax, 0xf
00411a4e  7523                   jne      0x411a73
00411a50  8b4c2454               mov      ecx, dword ptr [esp + 0x54]
00411a54  51                     push     ecx
00411a55  89e8                   mov      eax, ebp
00411a57  e8d5f30200             call     0x440e31 ; EnginGetTourDir
00411a5c  30e4                   xor      ah, ah
00411a5e  48                     dec      eax
00411a5f  8b54245c               mov      edx, dword ptr [esp + 0x5c]
00411a63  01c0                   add      eax, eax
00411a65  31db                   xor      ebx, ebx
00411a67  0572110000             add      eax, 0x1172
00411a6c  b901000000             mov      ecx, 1
00411a71  eb32                   jmp      0x411aa5 ; 
00411a73  89e8                   mov      eax, ebp
00411a75  e8ab050300             call     0x442025 ; EnginGetType
00411a7a  25ff000000             and      eax, 0xff
00411a7f  83f80c                 cmp      eax, 0xc
00411a82  752d                   jne      0x411ab1
00411a84  8b5c2454               mov      ebx, dword ptr [esp + 0x54]
00411a88  53                     push     ebx
00411a89  89e8                   mov      eax, ebp
00411a8b  e8a1f30200             call     0x440e31 ; EnginGetTourDir
00411a90  30e4                   xor      ah, ah
00411a92  48                     dec      eax
00411a93  b901000000             mov      ecx, 1
00411a98  01c0                   add      eax, eax
00411a9a  31db                   xor      ebx, ebx
00411a9c  0532120000             add      eax, 0x1232
00411aa1  8b54245c               mov      edx, dword ptr [esp + 0x5c]
00411aa5  6689c3                 mov      bx, ax
00411aa8  8b44247c               mov      eax, dword ptr [esp + 0x7c]
00411aac  e8a4a90400             call     0x45c455 ; PastePlayerCmp
00411ab1  8b842492000000         mov      eax, dword ptr [esp + 0x92]
00411ab8  b901000000             mov      ecx, 1
00411abd  0fbfef                 movsx    ebp, di
00411ac0  31db                   xor      ebx, ebx
00411ac2  c1f810                 sar      eax, 0x10
00411ac5  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411acd  89442428               mov      dword ptr [esp + 0x28], eax
00411ad1  89c2                   mov      edx, eax
00411ad3  89e8                   mov      eax, ebp
00411ad5  e8d6a10400             call     0x45bcb0 ; PasteGrisCmp
00411ada  31d2                   xor      edx, edx
00411adc  6689f2                 mov      dx, si
00411adf  89d0                   mov      eax, edx
00411ae1  e83f050300             call     0x442025 ; EnginGetType
00411ae6  25ff000000             and      eax, 0xff
00411aeb  83f80f                 cmp      eax, 0xf
00411aee  752b                   jne      0x411b1b
00411af0  89d0                   mov      eax, edx
00411af2  e83af30200             call     0x440e31 ; EnginGetTourDir
00411af7  30e4                   xor      ah, ah
00411af9  48                     dec      eax
00411afa  b901000000             mov      ecx, 1
00411aff  01c0                   add      eax, eax
00411b01  31db                   xor      ebx, ebx
00411b03  0572110000             add      eax, 0x1172
00411b08  8b542428               mov      edx, dword ptr [esp + 0x28]
00411b0c  6689c3                 mov      bx, ax
00411b0f  89e8                   mov      eax, ebp
00411b11  e89aa10400             call     0x45bcb0 ; PasteGrisCmp
00411b16  e96ff6ffff             jmp      0x41118a ; 
00411b1b  89d0                   mov      eax, edx
00411b1d  e803050300             call     0x442025 ; EnginGetType
00411b22  25ff000000             and      eax, 0xff
00411b27  83f80c                 cmp      eax, 0xc
00411b2a  0f855af6ffff           jne      0x41118a
00411b30  89d0                   mov      eax, edx
00411b32  e8faf20200             call     0x440e31 ; EnginGetTourDir
00411b37  30e4                   xor      ah, ah
00411b39  48                     dec      eax
00411b3a  b901000000             mov      ecx, 1
00411b3f  01c0                   add      eax, eax
00411b41  31db                   xor      ebx, ebx
00411b43  0532120000             add      eax, 0x1232
00411b48  ebbe                   jmp      0x411b08 ; 
00411b4a  89e8                   mov      eax, ebp
00411b4c  e8ade40300             call     0x44fffe ; EnginEstMiroir
00411b51  84c0                   test     al, al
00411b53  0f8431f6ffff           je       0x41118a
00411b59  8b842492000000         mov      eax, dword ptr [esp + 0x92]
00411b60  b901000000             mov      ecx, 1
00411b65  31db                   xor      ebx, ebx
00411b67  c1f810                 sar      eax, 0x10
00411b6a  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411b72  89442448               mov      dword ptr [esp + 0x48], eax
00411b76  0fbfc7                 movsx    eax, di
00411b79  8b542448               mov      edx, dword ptr [esp + 0x48]
00411b7d  89442470               mov      dword ptr [esp + 0x70], eax
00411b81  e89d9e0400             call     0x45ba23 ; PasteEclairCmp
00411b86  89e8                   mov      eax, ebp
00411b88  e898040300             call     0x442025 ; EnginGetType
00411b8d  25ff000000             and      eax, 0xff
00411b92  83f80f                 cmp      eax, 0xf
00411b95  752d                   jne      0x411bc4
00411b97  89e8                   mov      eax, ebp
00411b99  e893f20200             call     0x440e31 ; EnginGetTourDir
00411b9e  30e4                   xor      ah, ah
00411ba0  48                     dec      eax
00411ba1  b901000000             mov      ecx, 1
00411ba6  01c0                   add      eax, eax
00411ba8  31db                   xor      ebx, ebx
00411baa  0572110000             add      eax, 0x1172
00411baf  8b542448               mov      edx, dword ptr [esp + 0x48]
00411bb3  6689c3                 mov      bx, ax
00411bb6  8b442470               mov      eax, dword ptr [esp + 0x70]
00411bba  e8649e0400             call     0x45ba23 ; PasteEclairCmp
00411bbf  e9c6f5ffff             jmp      0x41118a ; 
00411bc4  89e8                   mov      eax, ebp
00411bc6  e85a040300             call     0x442025 ; EnginGetType
00411bcb  25ff000000             and      eax, 0xff
00411bd0  83f80c                 cmp      eax, 0xc
00411bd3  0f85b1f5ffff           jne      0x41118a
00411bd9  89e8                   mov      eax, ebp
00411bdb  e851f20200             call     0x440e31 ; EnginGetTourDir
00411be0  30e4                   xor      ah, ah
00411be2  48                     dec      eax
00411be3  b901000000             mov      ecx, 1
00411be8  01c0                   add      eax, eax
00411bea  31db                   xor      ebx, ebx
00411bec  0532120000             add      eax, 0x1232
00411bf1  ebbc                   jmp      0x411baf ; 
00411bf3  89e8                   mov      eax, ebp
00411bf5  e82b040300             call     0x442025 ; EnginGetType
00411bfa  3c14                   cmp      al, 0x14
00411bfc  7210                   jb       0x411c0e
00411bfe  3c16                   cmp      al, 0x16
00411c00  0f86e6faffff           jbe      0x4116ec
00411c06  3c18                   cmp      al, 0x18
00411c08  0f86defaffff           jbe      0x4116ec
00411c0e  31d2                   xor      edx, edx
00411c10  6689f2                 mov      dx, si
00411c13  89d0                   mov      eax, edx
00411c15  e8e4e30300             call     0x44fffe ; EnginEstMiroir
00411c1a  84c0                   test     al, al
00411c1c  750b                   jne      0x411c29
00411c1e  89d0                   mov      eax, edx
00411c20  e809e40300             call     0x45002e ; EnginEstTerreur
00411c25  84c0                   test     al, al
00411c27  7444                   je       0x411c6d
00411c29  31c0                   xor      eax, eax
00411c2b  6689f0                 mov      ax, si
00411c2e  e8cbe30300             call     0x44fffe ; EnginEstMiroir
00411c33  84c0                   test     al, al
00411c35  0f84b7fdffff           je       0x4119f2
00411c3b  8a1d181d4e00           mov      bl, byte ptr [0x4e1d18]
00411c41  31d2                   xor      edx, edx
00411c43  88da                   mov      dl, bl
00411c45  8a92181c4e00           mov      dl, byte ptr [edx + 0x4e1c18]
00411c4b  81e2ff000000           and      edx, 0xff
00411c51  bd02000000             mov      ebp, 2
00411c56  89d0                   mov      eax, edx
00411c58  c1fa1f                 sar      edx, 0x1f
00411c5b  f7fd                   idiv     ebp
00411c5d  fec3                   inc      bl
00411c5f  881d181d4e00           mov      byte ptr [0x4e1d18], bl
00411c65  85d2                   test     edx, edx
00411c67  0f8585fdffff           jne      0x4119f2
00411c6d  31c0                   xor      eax, eax
00411c6f  b901000000             mov      ecx, 1
00411c74  8a842498000000         mov      al, byte ptr [esp + 0x98]
00411c7b  0fbfef                 movsx    ebp, di
00411c7e  89442430               mov      dword ptr [esp + 0x30], eax
00411c82  50                     push     eax
00411c83  8b842496000000         mov      eax, dword ptr [esp + 0x96]
00411c8a  31db                   xor      ebx, ebx
00411c8c  c1f810                 sar      eax, 0x10
00411c8f  668b9c2494000000       mov      bx, word ptr [esp + 0x94]
00411c97  89442404               mov      dword ptr [esp + 4], eax
00411c9b  89c2                   mov      edx, eax
00411c9d  89e8                   mov      eax, ebp
00411c9f  e8b1a70400             call     0x45c455 ; PastePlayerCmp
00411ca4  31d2                   xor      edx, edx
00411ca6  6689f2                 mov      dx, si
00411ca9  89d0                   mov      eax, edx
00411cab  e875030300             call     0x442025 ; EnginGetType
00411cb0  25ff000000             and      eax, 0xff
00411cb5  83f80f                 cmp      eax, 0xf
00411cb8  0f85fdfcffff           jne      0x4119bb
00411cbe  8b5c2430               mov      ebx, dword ptr [esp + 0x30]
00411cc2  53                     push     ebx
00411cc3  89d0                   mov      eax, edx
00411cc5  e867f10200             call     0x440e31 ; EnginGetTourDir
00411cca  30e4                   xor      ah, ah
00411ccc  48                     dec      eax
00411ccd  b901000000             mov      ecx, 1
00411cd2  01c0                   add      eax, eax
00411cd4  31db                   xor      ebx, ebx
00411cd6  0572110000             add      eax, 0x1172
00411cdb  8b542404               mov      edx, dword ptr [esp + 4]
00411cdf  6689c3                 mov      bx, ax
00411ce2  89e8                   mov      eax, ebp
00411ce4  e86ca70400             call     0x45c455 ; PastePlayerCmp
00411ce9  e99cf4ffff             jmp      0x41118a ; 
00411cee  89d0                   mov      eax, edx
00411cf0  e830030300             call     0x442025 ; EnginGetType
00411cf5  25ff000000             and      eax, 0xff
00411cfa  83f80c                 cmp      eax, 0xc
00411cfd  0f8562f5ffff           jne      0x411265
00411d03  8b4c2444               mov      ecx, dword ptr [esp + 0x44]
00411d07  51                     push     ecx
00411d08  89d0                   mov      eax, edx
00411d0a  e822f10200             call     0x440e31 ; EnginGetTourDir
00411d0f  30e4                   xor      ah, ah
00411d11  48                     dec      eax
00411d12  31db                   xor      ebx, ebx
00411d14  01c0                   add      eax, eax
00411d16  89ea                   mov      edx, ebp
00411d18  0532120000             add      eax, 0x1232
00411d1d  b901000000             mov      ecx, 1
00411d22  e932f5ffff             jmp      0x411259 ; 
00411d27  0fb7ee                 movzx    ebp, si
00411d2a  89e8                   mov      eax, ebp
00411d2c  e8fde20300             call     0x45002e ; EnginEstTerreur
00411d31  84c0                   test     al, al
00411d33  0f8442010000           je       0x411e7b
00411d39  31c0                   xor      eax, eax
00411d3b  8a842498000000         mov      al, byte ptr [esp + 0x98]
00411d42  b901000000             mov      ecx, 1
00411d47  8944245c               mov      dword ptr [esp + 0x5c], eax
00411d4b  50                     push     eax
00411d4c  8b842496000000         mov      eax, dword ptr [esp + 0x96]
00411d53  31db                   xor      ebx, ebx
00411d55  c1f810                 sar      eax, 0x10
00411d58  668b9c2494000000       mov      bx, word ptr [esp + 0x94]
00411d60  89442408               mov      dword ptr [esp + 8], eax
00411d64  0fbfc7                 movsx    eax, di
00411d67  8b542408               mov      edx, dword ptr [esp + 8]
00411d6b  89442450               mov      dword ptr [esp + 0x50], eax
00411d6f  e8e1a60400             call     0x45c455 ; PastePlayerCmp
00411d74  89e8                   mov      eax, ebp
00411d76  e8aa020300             call     0x442025 ; EnginGetType
00411d7b  25ff000000             and      eax, 0xff
00411d80  83f80f                 cmp      eax, 0xf
00411d83  751f                   jne      0x411da4
00411d85  8b54245c               mov      edx, dword ptr [esp + 0x5c]
00411d89  52                     push     edx
00411d8a  89e8                   mov      eax, ebp
00411d8c  e8a0f00200             call     0x440e31 ; EnginGetTourDir
00411d91  30e4                   xor      ah, ah
00411d93  48                     dec      eax
00411d94  b901000000             mov      ecx, 1
00411d99  01c0                   add      eax, eax
00411d9b  31db                   xor      ebx, ebx
00411d9d  0572110000             add      eax, 0x1172
00411da2  eb2e                   jmp      0x411dd2 ; 
00411da4  89e8                   mov      eax, ebp
00411da6  e87a020300             call     0x442025 ; EnginGetType
00411dab  25ff000000             and      eax, 0xff
00411db0  83f80c                 cmp      eax, 0xc
00411db3  752d                   jne      0x411de2
00411db5  8b44245c               mov      eax, dword ptr [esp + 0x5c]
00411db9  50                     push     eax
00411dba  89e8                   mov      eax, ebp
00411dbc  e870f00200             call     0x440e31 ; EnginGetTourDir
00411dc1  30e4                   xor      ah, ah
00411dc3  48                     dec      eax
00411dc4  b901000000             mov      ecx, 1
00411dc9  01c0                   add      eax, eax
00411dcb  31db                   xor      ebx, ebx
00411dcd  0532120000             add      eax, 0x1232
00411dd2  8b542408               mov      edx, dword ptr [esp + 8]
00411dd6  6689c3                 mov      bx, ax
00411dd9  8b442450               mov      eax, dword ptr [esp + 0x50]
00411ddd  e873a60400             call     0x45c455 ; PastePlayerCmp
00411de2  8b842492000000         mov      eax, dword ptr [esp + 0x92]
00411de9  b901000000             mov      ecx, 1
00411dee  0fbfef                 movsx    ebp, di
00411df1  31db                   xor      ebx, ebx
00411df3  c1f810                 sar      eax, 0x10
00411df6  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411dfe  8944241c               mov      dword ptr [esp + 0x1c], eax
00411e02  89c2                   mov      edx, eax
00411e04  89e8                   mov      eax, ebp
00411e06  e8a59e0400             call     0x45bcb0 ; PasteGrisCmp
00411e0b  31d2                   xor      edx, edx
00411e0d  6689f2                 mov      dx, si
00411e10  89d0                   mov      eax, edx
00411e12  e80e020300             call     0x442025 ; EnginGetType
00411e17  25ff000000             and      eax, 0xff
00411e1c  83f80f                 cmp      eax, 0xf
00411e1f  752b                   jne      0x411e4c
00411e21  89d0                   mov      eax, edx
00411e23  e809f00200             call     0x440e31 ; EnginGetTourDir
00411e28  30e4                   xor      ah, ah
00411e2a  48                     dec      eax
00411e2b  b901000000             mov      ecx, 1
00411e30  01c0                   add      eax, eax
00411e32  31db                   xor      ebx, ebx
00411e34  0572110000             add      eax, 0x1172
00411e39  8b54241c               mov      edx, dword ptr [esp + 0x1c]
00411e3d  6689c3                 mov      bx, ax
00411e40  89e8                   mov      eax, ebp
00411e42  e8699e0400             call     0x45bcb0 ; PasteGrisCmp
00411e47  e919f4ffff             jmp      0x411265 ; 
00411e4c  89d0                   mov      eax, edx
00411e4e  e8d2010300             call     0x442025 ; EnginGetType
00411e53  25ff000000             and      eax, 0xff
00411e58  83f80c                 cmp      eax, 0xc
00411e5b  0f8504f4ffff           jne      0x411265
00411e61  89d0                   mov      eax, edx
00411e63  e8c9ef0200             call     0x440e31 ; EnginGetTourDir
00411e68  30e4                   xor      ah, ah
00411e6a  48                     dec      eax
00411e6b  b901000000             mov      ecx, 1
00411e70  01c0                   add      eax, eax
00411e72  31db                   xor      ebx, ebx
00411e74  0532120000             add      eax, 0x1232
00411e79  ebbe                   jmp      0x411e39 ; 
00411e7b  89e8                   mov      eax, ebp
00411e7d  e87ce10300             call     0x44fffe ; EnginEstMiroir
00411e82  84c0                   test     al, al
00411e84  0f84dbf3ffff           je       0x411265
00411e8a  8b842492000000         mov      eax, dword ptr [esp + 0x92]
00411e91  b901000000             mov      ecx, 1
00411e96  31db                   xor      ebx, ebx
00411e98  c1f810                 sar      eax, 0x10
00411e9b  668b9c2490000000       mov      bx, word ptr [esp + 0x90]
00411ea3  89442464               mov      dword ptr [esp + 0x64], eax
00411ea7  0fbfc7                 movsx    eax, di
00411eaa  8b542464               mov      edx, dword ptr [esp + 0x64]
00411eae  89442474               mov      dword ptr [esp + 0x74], eax
00411eb2  e86c9b0400             call     0x45ba23 ; PasteEclairCmp
00411eb7  89e8                   mov      eax, ebp
00411eb9  e867010300             call     0x442025 ; EnginGetType
00411ebe  25ff000000             and      eax, 0xff
00411ec3  83f80f                 cmp      eax, 0xf
00411ec6  752d                   jne      0x411ef5
00411ec8  89e8                   mov      eax, ebp
00411eca  e862ef0200             call     0x440e31 ; EnginGetTourDir
00411ecf  30e4                   xor      ah, ah
00411ed1  48                     dec      eax
00411ed2  b901000000             mov      ecx, 1
00411ed7  01c0                   add      eax, eax
00411ed9  31db                   xor      ebx, ebx
00411edb  0572110000             add      eax, 0x1172
00411ee0  8b542464               mov      edx, dword ptr [esp + 0x64]
00411ee4  6689c3                 mov      bx, ax
00411ee7  8b442474               mov      eax, dword ptr [esp + 0x74]
00411eeb  e8339b0400             call     0x45ba23 ; PasteEclairCmp
00411ef0  e970f3ffff             jmp      0x411265 ; 
00411ef5  89e8                   mov      eax, ebp
00411ef7  e829010300             call     0x442025 ; EnginGetType
00411efc  25ff000000             and      eax, 0xff
00411f01  83f80c                 cmp      eax, 0xc
00411f04  0f855bf3ffff           jne      0x411265
00411f0a  89e8                   mov      eax, ebp
00411f0c  e820ef0200             call     0x440e31 ; EnginGetTourDir
00411f11  30e4                   xor      ah, ah
00411f13  48                     dec      eax
00411f14  b901000000             mov      ecx, 1
00411f19  01c0                   add      eax, eax
00411f1b  31db                   xor      ebx, ebx
00411f1d  0532120000             add      eax, 0x1232
00411f22  ebbc                   jmp      0x411ee0 ; 
00411f24  84c0                   test     al, al
00411f26  0f84f8f3ffff           je       0x411324
00411f2c  e959f2ffff             jmp      0x41118a ; 
00411f31  66a17c8f5000           mov      ax, word ptr [0x508f7c]
00411f37  30e4                   xor      ah, ah
00411f39  243f                   and      al, 0x3f
00411f3b  31db                   xor      ebx, ebx
00411f3d  057d2b0000             add      eax, 0x2b7d
00411f42  6689c3                 mov      bx, ax
00411f45  8b842494000000         mov      eax, dword ptr [esp + 0x94]
00411f4c  83e80e                 sub      eax, 0xe
00411f4f  0fbfd0                 movsx    edx, ax
00411f52  89f8                   mov      eax, edi
00411f54  83e80e                 sub      eax, 0xe
00411f57  b901000000             mov      ecx, 1
00411f5c  98                     cwde     
00411f5d  e8c19a0400             call     0x45ba23 ; PasteEclairCmp
00411f62  31d2                   xor      edx, edx
00411f64  6689f2                 mov      dx, si
00411f67  89d0                   mov      eax, edx
00411f69  e8b7000300             call     0x442025 ; EnginGetType
00411f6e  25ff000000             and      eax, 0xff
00411f73  83f804                 cmp      eax, 4
00411f76  0f8517010000           jne      0x412093
00411f7c  89d0                   mov      eax, edx
00411f7e  e808630300             call     0x44828b ; EnginGetMana
00411f83  30ed                   xor      ch, ch
00411f85  88c3                   mov      bl, al
00411f87  88c1                   mov      cl, al
00411f89  89d0                   mov      eax, edx
00411f8b  e8b5000300             call     0x442045 ; EnginGetPlayer
00411f90  25ff000000             and      eax, 0xff
00411f95  31d2                   xor      edx, edx
00411f97  e8d4620300             call     0x448270 ; EnginGetMaxMana
00411f9c  88c2                   mov      dl, al
00411f9e  be05000000             mov      esi, 5
00411fa3  89d0                   mov      eax, edx
00411fa5  c1fa1f                 sar      edx, 0x1f
00411fa8  f7fe                   idiv     esi
00411faa  89c6                   mov      esi, eax
00411fac  31c0                   xor      eax, eax
00411fae  88d8                   mov      al, bl
00411fb0  85c0                   test     eax, eax
00411fb2  0f84db000000           je       0x412093
00411fb8  31d2                   xor      edx, edx
00411fba  6689ca                 mov      dx, cx
00411fbd  31db                   xor      ebx, ebx
00411fbf  4a                     dec      edx
00411fc0  6689f3                 mov      bx, si
00411fc3  89d0                   mov      eax, edx
00411fc5  c1fa1f                 sar      edx, 0x1f
00411fc8  f7fb                   idiv     ebx
00411fca  c1e007                 shl      eax, 7
00411fcd  057d2c0000             add      eax, 0x2c7d
00411fd2  89842488000000         mov      dword ptr [esp + 0x88], eax
00411fd9  66a17c8f5000           mov      ax, word ptr [0x508f7c]
00411fdf  30e4                   xor      ah, ah
00411fe1  8b9c2488000000         mov      ebx, dword ptr [esp + 0x88]
00411fe8  241f                   and      al, 0x1f
00411fea  01d8                   add      eax, ebx
00411fec  31db                   xor      ebx, ebx
00411fee  6689c3                 mov      bx, ax
00411ff1  8b842494000000         mov      eax, dword ptr [esp + 0x94]
00411ff8  83c726                 add      edi, 0x26
00411ffb  0508000000             add      eax, 8
00412000  b901000000             mov      ecx, 1
00412005  0fbfe8                 movsx    ebp, ax
00412008  0fbff7                 movsx    esi, di
0041200b  89ea                   mov      edx, ebp
0041200d  89f0                   mov      eax, esi
0041200f  e80f9a0400             call     0x45ba23 ; PasteEclairCmp
00412014  66a17c8f5000           mov      ax, word ptr [0x508f7c]
0041201a  8b942488000000         mov      edx, dword ptr [esp + 0x88]
00412021  30e4                   xor      ah, ah
00412023  83c220                 add      edx, 0x20
00412026  241f                   and      al, 0x1f
00412028  31db                   xor      ebx, ebx
0041202a  01d0                   add      eax, edx
0041202c  b901000000             mov      ecx, 1
00412031  6689c3                 mov      bx, ax
00412034  89ea                   mov      edx, ebp
00412036  89f0                   mov      eax, esi
00412038  e8e6990400             call     0x45ba23 ; PasteEclairCmp
0041203d  66a17c8f5000           mov      ax, word ptr [0x508f7c]
00412043  8b942488000000         mov      edx, dword ptr [esp + 0x88]
0041204a  30e4                   xor      ah, ah
0041204c  83c240                 add      edx, 0x40
0041204f  241f                   and      al, 0x1f
00412051  31db                   xor      ebx, ebx
00412053  01d0                   add      eax, edx
00412055  b901000000             mov      ecx, 1
0041205a  6689c3                 mov      bx, ax
0041205d  89ea                   mov      edx, ebp
0041205f  89f0                   mov      eax, esi
00412061  e8bd990400             call     0x45ba23 ; PasteEclairCmp
00412066  668b157c8f5000         mov      dx, word ptr [0x508f7c]
0041206d  8b842488000000         mov      eax, dword ptr [esp + 0x88]
00412074  30f6                   xor      dh, dh
00412076  0560000000             add      eax, 0x60
0041207b  80e21f                 and      dl, 0x1f
0041207e  31db                   xor      ebx, ebx
00412080  01d0                   add      eax, edx
00412082  b901000000             mov      ecx, 1
00412087  6689c3                 mov      bx, ax
0041208a  89ea                   mov      edx, ebp
0041208c  89f0                   mov      eax, esi
0041208e  e890990400             call     0x45ba23 ; PasteEclairCmp
00412093  81c49c000000           add      esp, 0x9c
00412099  5d                     pop      ebp
0041209a  5f                     pop      edi
0041209b  5e                     pop      esi
0041209c  c3                     ret      
