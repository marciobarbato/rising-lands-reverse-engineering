; AffVegetTerrain [0x410085, 0x41068e)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00410085  51                     push     ecx
00410086  56                     push     esi
00410087  57                     push     edi
00410088  55                     push     ebp
00410089  83ec0c                 sub      esp, 0xc
0041008c  89c6                   mov      esi, eax
0041008e  89d1                   mov      ecx, edx
00410090  895c2404               mov      dword ptr [esp + 4], ebx
00410094  30e4                   xor      ah, ah
00410096  31d2                   xor      edx, edx
00410098  31ff                   xor      edi, edi
0041009a  8a1541805000           mov      dl, byte ptr [0x508041]
004100a0  6689df                 mov      di, bx
004100a3  88642408               mov      byte ptr [esp + 8], ah
004100a7  89f8                   mov      eax, edi
004100a9  e842660600             call     0x4766f0 ; TerrainEstDecouvert
004100ae  84c0                   test     al, al
004100b0  0f84ba000000           je       0x410170
004100b6  31d2                   xor      edx, edx
004100b8  89f8                   mov      eax, edi
004100ba  8a1541805000           mov      dl, byte ptr [0x508041]
004100c0  e875680600             call     0x47693a ; CaseEstIlluminee
004100c5  84c0                   test     al, al
004100c7  0f8405000000           je       0x4100d2
004100cd  c644240801             mov      byte ptr [esp + 8], 1
004100d2  31ff                   xor      edi, edi
004100d4  a1747d5000             mov      eax, dword ptr [0x507d74]
004100d9  668b7c2404             mov      di, word ptr [esp + 4]
004100de  8a0407                 mov      al, byte ptr [edi + eax]
004100e1  88c4                   mov      ah, al
004100e3  3c15                   cmp      al, 0x15
004100e5  0f821d050000           jb       0x410608
004100eb  0f86f9010000           jbe      0x4102ea
004100f1  3c1a                   cmp      al, 0x1a
004100f3  0f82aa040000           jb       0x4105a3
004100f9  0f86e3020000           jbe      0x4103e2
004100ff  89f2                   mov      edx, esi
00410101  83ea04                 sub      edx, 4
00410104  3c42                   cmp      al, 0x42
00410106  0f828e040000           jb       0x41059a
0041010c  0f869d030000           jbe      0x4104af
00410112  3c44                   cmp      al, 0x44
00410114  0f8697030000           jbe      0x4104b1
0041011a  3c46                   cmp      al, 0x46
0041011c  0f840f030000           je       0x410431
00410122  31c0                   xor      eax, eax
00410124  8b15747d5000           mov      edx, dword ptr [0x507d74]
0041012a  668b442404             mov      ax, word ptr [esp + 4]
0041012f  01d0                   add      eax, edx
00410131  31d2                   xor      edx, edx
00410133  8a10                   mov      dl, byte ptr [eax]
00410135  83fa1c                 cmp      edx, 0x1c
00410138  0f8c32000000           jl       0x410170
0041013e  83fa35                 cmp      edx, 0x35
00410141  0f8d29000000           jge      0x410170
00410147  807c240800             cmp      byte ptr [esp + 8], 0
0041014c  0f8535040000           jne      0x410587
00410152  8a00                   mov      al, byte ptr [eax]
00410154  0fbfd1                 movsx    edx, cx
00410157  30e4                   xor      ah, ah
00410159  31db                   xor      ebx, ebx
0041015b  057c290000             add      eax, 0x297c
00410160  b901000000             mov      ecx, 1
00410165  6689c3                 mov      bx, ax
00410168  0fbfc6                 movsx    eax, si
0041016b  e8d7b00400             call     0x45b247 ; PasteBobCmp
00410170  83c40c                 add      esp, 0xc
00410173  5d                     pop      ebp
00410174  5f                     pop      edi
00410175  5e                     pop      esi
00410176  59                     pop      ecx
00410177  c3                     ret
00410178  8a742408               mov      dh, byte ptr [esp + 8]
0041017c  bb4d290000             mov      ebx, 0x294d
00410181  84f6                   test     dh, dh
00410183  7410                   je       0x410195
00410185  b801000000             mov      eax, 1
0041018a  81e3ffff0000           and      ebx, 0xffff
00410190  e9c7000000             jmp      0x41025c ;
00410195  b801000000             mov      eax, 1
0041019a  bb8d290000             mov      ebx, 0x298d
0041019f  e9b8000000             jmp      0x41025c ;
004101a4  8a642408               mov      ah, byte ptr [esp + 8]
004101a8  ba4e290000             mov      edx, 0x294e
004101ad  84e4                   test     ah, ah
004101af  7415                   je       0x4101c6
004101b1  b801000000             mov      eax, 1
004101b6  83c110                 add      ecx, 0x10
004101b9  31db                   xor      ebx, ebx
004101bb  83c610                 add      esi, 0x10
004101be  6689d3                 mov      bx, dx
004101c1  e9c5000000             jmp      0x41028b ;
004101c6  ba01000000             mov      edx, 1
004101cb  bb8e290000             mov      ebx, 0x298e
004101d0  83c110                 add      ecx, 0x10
004101d3  83c610                 add      esi, 0x10
004101d6  0fbff9                 movsx    edi, cx
004101d9  0fbfc6                 movsx    eax, si
004101dc  89d1                   mov      ecx, edx
004101de  89fa                   mov      edx, edi
004101e0  eb89                   jmp      0x41016b ;
004101e2  8a442408               mov      al, byte ptr [esp + 8]
004101e6  bb4f290000             mov      ebx, 0x294f
004101eb  84c0                   test     al, al
004101ed  7596                   jne      0x410185
004101ef  b801000000             mov      eax, 1
004101f4  bb8f290000             mov      ebx, 0x298f
004101f9  eb61                   jmp      0x41025c ;
004101fb  bf01000000             mov      edi, 1
00410200  bb90290000             mov      ebx, 0x2990
00410205  83c10b                 add      ecx, 0xb
00410208  83c612                 add      esi, 0x12
0041020b  0fbfd1                 movsx    edx, cx
0041020e  0fbfc6                 movsx    eax, si
00410211  89f9                   mov      ecx, edi
00410213  e953ffffff             jmp      0x41016b ;
00410218  8a542408               mov      dl, byte ptr [esp + 8]
0041021c  bb51290000             mov      ebx, 0x2951
00410221  84d2                   test     dl, dl
00410223  740d                   je       0x410232
00410225  b801000000             mov      eax, 1
0041022a  81e3ffff0000           and      ebx, 0xffff
00410230  eb27                   jmp      0x410259 ;
00410232  b801000000             mov      eax, 1
00410237  bb91290000             mov      ebx, 0x2991
0041023c  eb1b                   jmp      0x410259 ;
0041023e  8a642408               mov      ah, byte ptr [esp + 8]
00410242  bb52290000             mov      ebx, 0x2952
00410247  84e4                   test     ah, ah
00410249  7419                   je       0x410264
0041024b  b801000000             mov      eax, 1
00410250  81e3ffff0000           and      ebx, 0xffff
00410256  83c119                 add      ecx, 0x19
00410259  83c612                 add      esi, 0x12
0041025c  0fbfd1                 movsx    edx, cx
0041025f  0fbff6                 movsx    esi, si
00410262  eb2d                   jmp      0x410291 ;
00410264  b801000000             mov      eax, 1
00410269  bb92290000             mov      ebx, 0x2992
0041026e  ebe6                   jmp      0x410256 ;
00410270  8a442408               mov      al, byte ptr [esp + 8]
00410274  bb53290000             mov      ebx, 0x2953
00410279  84c0                   test     al, al
0041027b  741d                   je       0x41029a
0041027d  b801000000             mov      eax, 1
00410282  81e3ffff0000           and      ebx, 0xffff
00410288  83c119                 add      ecx, 0x19
0041028b  0fbff6                 movsx    esi, si
0041028e  0fbfd1                 movsx    edx, cx
00410291  89c1                   mov      ecx, eax
00410293  89f0                   mov      eax, esi
00410295  e9d1feffff             jmp      0x41016b ;
0041029a  b801000000             mov      eax, 1
0041029f  bb93290000             mov      ebx, 0x2993
004102a4  ebe2                   jmp      0x410288 ;
004102a6  8a7c2408               mov      bh, byte ptr [esp + 8]
004102aa  b854290000             mov      eax, 0x2954
004102af  84ff                   test     bh, bh
004102b1  7419                   je       0x4102cc
004102b3  bb01000000             mov      ebx, 1
004102b8  31ff                   xor      edi, edi
004102ba  0fbfd1                 movsx    edx, cx
004102bd  6689c7                 mov      di, ax
004102c0  89d9                   mov      ecx, ebx
004102c2  0fbfc6                 movsx    eax, si
004102c5  89fb                   mov      ebx, edi
004102c7  e99ffeffff             jmp      0x41016b ;
004102cc  bf01000000             mov      edi, 1
004102d1  bb94290000             mov      ebx, 0x2994
004102d6  e930ffffff             jmp      0x41020b ;
004102db  ba01000000             mov      edx, 1
004102e0  bb95290000             mov      ebx, 0x2995
004102e5  e9ecfeffff             jmp      0x4101d6 ;
004102ea  8a542408               mov      dl, byte ptr [esp + 8]
004102ee  b856290000             mov      eax, 0x2956
004102f3  84d2                   test     dl, dl
004102f5  7415                   je       0x41030c
004102f7  bf01000000             mov      edi, 1
004102fc  83e905                 sub      ecx, 5
004102ff  31db                   xor      ebx, ebx
00410301  83ee03                 sub      esi, 3
00410304  6689c3                 mov      bx, ax
00410307  e9fffeffff             jmp      0x41020b ;
0041030c  bb96290000             mov      ebx, 0x2996
00410311  83e905                 sub      ecx, 5
00410314  83ee03                 sub      esi, 3
00410317  0fbfd1                 movsx    edx, cx
0041031a  0fbfc6                 movsx    eax, si
0041031d  eb15                   jmp      0x410334 ;
0041031f  8a7c2408               mov      bh, byte ptr [esp + 8]
00410323  89f0                   mov      eax, esi
00410325  49                     dec      ecx
00410326  48                     dec      eax
00410327  84ff                   test     bh, bh
00410329  7413                   je       0x41033e
0041032b  bb57290000             mov      ebx, 0x2957
00410330  0fbfd1                 movsx    edx, cx
00410333  98                     cwde
00410334  b901000000             mov      ecx, 1
00410339  e92dfeffff             jmp      0x41016b ;
0041033e  bb97290000             mov      ebx, 0x2997
00410343  ebeb                   jmp      0x410330 ;
00410345  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041034a  8a0407                 mov      al, byte ptr [edi + eax]
0041034d  0fbfe9                 movsx    ebp, cx
00410350  0fbff6                 movsx    esi, si
00410353  30e4                   xor      ah, ah
00410355  31db                   xor      ebx, ebx
00410357  b901000000             mov      ecx, 1
0041035c  0585230000             add      eax, 0x2385
00410361  89ea                   mov      edx, ebp
00410363  6689c3                 mov      bx, ax
00410366  89f0                   mov      eax, esi
00410368  e8daae0400             call     0x45b247 ; PasteBobCmp
0041036d  807c240800             cmp      byte ptr [esp + 8], 0
00410372  0f85f8fdffff           jne      0x410170
00410378  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041037d  01c7                   add      edi, eax
0041037f  30e4                   xor      ah, ah
00410381  b901000000             mov      ecx, 1
00410386  8a07                   mov      al, byte ptr [edi]
00410388  31db                   xor      ebx, ebx
0041038a  0585230000             add      eax, 0x2385
0041038f  89ea                   mov      edx, ebp
00410391  e90a010000             jmp      0x4104a0 ;
00410396  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041039b  8a0407                 mov      al, byte ptr [edi + eax]
0041039e  0fbfe9                 movsx    ebp, cx
004103a1  0fbff6                 movsx    esi, si
004103a4  30e4                   xor      ah, ah
004103a6  31db                   xor      ebx, ebx
004103a8  b901000000             mov      ecx, 1
004103ad  0595230000             add      eax, 0x2395
004103b2  89ea                   mov      edx, ebp
004103b4  6689c3                 mov      bx, ax
004103b7  89f0                   mov      eax, esi
004103b9  e889ae0400             call     0x45b247 ; PasteBobCmp
004103be  807c240800             cmp      byte ptr [esp + 8], 0
004103c3  0f85a7fdffff           jne      0x410170
004103c9  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004103ce  01c7                   add      edi, eax
004103d0  30e4                   xor      ah, ah
004103d2  b901000000             mov      ecx, 1
004103d7  8a07                   mov      al, byte ptr [edi]
004103d9  31db                   xor      ebx, ebx
004103db  0595230000             add      eax, 0x2395
004103e0  ebad                   jmp      0x41038f ;
004103e2  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004103e7  8a0407                 mov      al, byte ptr [edi + eax]
004103ea  0fbfe9                 movsx    ebp, cx
004103ed  0fbff6                 movsx    esi, si
004103f0  30e4                   xor      ah, ah
004103f2  31db                   xor      ebx, ebx
004103f4  b901000000             mov      ecx, 1
004103f9  05b5230000             add      eax, 0x23b5
004103fe  89ea                   mov      edx, ebp
00410400  6689c3                 mov      bx, ax
00410403  89f0                   mov      eax, esi
00410405  e83dae0400             call     0x45b247 ; PasteBobCmp
0041040a  807c240800             cmp      byte ptr [esp + 8], 0
0041040f  0f855bfdffff           jne      0x410170
00410415  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0041041a  01c7                   add      edi, eax
0041041c  30e4                   xor      ah, ah
0041041e  b901000000             mov      ecx, 1
00410423  8a07                   mov      al, byte ptr [edi]
00410425  31db                   xor      ebx, ebx
00410427  05b5230000             add      eax, 0x23b5
0041042c  e95effffff             jmp      0x41038f ;
00410431  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00410436  8a3541805000           mov      dh, byte ptr [0x508041]
0041043c  3a3407                 cmp      dh, byte ptr [edi + eax]
0041043f  0f852bfdffff           jne      0x410170
00410445  668b157c8f5000         mov      dx, word ptr [0x508f7c]
0041044c  89f8                   mov      eax, edi
0041044e  83c108                 add      ecx, 8
00410451  83c608                 add      esi, 8
00410454  31db                   xor      ebx, ebx
00410456  01d0                   add      eax, edx
00410458  0fbff9                 movsx    edi, cx
0041045b  30e4                   xor      ah, ah
0041045d  0fbff6                 movsx    esi, si
00410460  240f                   and      al, 0xf
00410462  b901000000             mov      ecx, 1
00410467  0575230000             add      eax, 0x2375
0041046c  89fa                   mov      edx, edi
0041046e  6689c3                 mov      bx, ax
00410471  89f0                   mov      eax, esi
00410473  e8cfad0400             call     0x45b247 ; PasteBobCmp
00410478  807c240800             cmp      byte ptr [esp + 8], 0
0041047d  0f85edfcffff           jne      0x410170
00410483  8b442404               mov      eax, dword ptr [esp + 4]
00410487  6603057c8f5000         add      ax, word ptr [0x508f7c]
0041048e  30e4                   xor      ah, ah
00410490  b901000000             mov      ecx, 1
00410495  240f                   and      al, 0xf
00410497  31db                   xor      ebx, ebx
00410499  0575230000             add      eax, 0x2375
0041049e  89fa                   mov      edx, edi
004104a0  6689c3                 mov      bx, ax
004104a3  89f0                   mov      eax, esi
004104a5  e8ecb20400             call     0x45b796 ; PasteOmbreCmp
004104aa  e9c1fcffff             jmp      0x410170 ;
004104af  89d6                   mov      esi, edx
004104b1  0fb76c2404             movzx    ebp, word ptr [esp + 4]
004104b6  a1747d5000             mov      eax, dword ptr [0x507d74]
004104bb  8a0428                 mov      al, byte ptr [eax + ebp]
004104be  30e4                   xor      ah, ah
004104c0  89c3                   mov      ebx, eax
004104c2  83eb42                 sub      ebx, 0x42
004104c5  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004104cb  c1e304                 shl      ebx, 4
004104ce  8a142a                 mov      dl, byte ptr [edx + ebp]
004104d1  81c3472a0000           add      ebx, 0x2a47
004104d7  81e2ff000000           and      edx, 0xff
004104dd  89d0                   mov      eax, edx
004104df  c1fa1f                 sar      edx, 0x1f
004104e2  2bc2                   sub      eax, edx
004104e4  d1f8                   sar      eax, 1
004104e6  0fbff9                 movsx    edi, cx
004104e9  31d2                   xor      edx, edx
004104eb  0fbff6                 movsx    esi, si
004104ee  6689da                 mov      dx, bx
004104f1  b901000000             mov      ecx, 1
004104f6  01d0                   add      eax, edx
004104f8  31db                   xor      ebx, ebx
004104fa  891424                 mov      dword ptr [esp], edx
004104fd  6689c3                 mov      bx, ax
00410500  89fa                   mov      edx, edi
00410502  89f0                   mov      eax, esi
00410504  e83ead0400             call     0x45b247 ; PasteBobCmp
00410509  807c240800             cmp      byte ptr [esp + 8], 0
0041050e  0f855cfcffff           jne      0x410170
00410514  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
0041051a  8a142a                 mov      dl, byte ptr [edx + ebp]
0041051d  81e2ff000000           and      edx, 0xff
00410523  89d0                   mov      eax, edx
00410525  c1fa1f                 sar      edx, 0x1f
00410528  2bc2                   sub      eax, edx
0041052a  d1f8                   sar      eax, 1
0041052c  8b1c24                 mov      ebx, dword ptr [esp]
0041052f  b901000000             mov      ecx, 1
00410534  01d8                   add      eax, ebx
00410536  31db                   xor      ebx, ebx
00410538  e961ffffff             jmp      0x41049e ;
0041053d  807c240800             cmp      byte ptr [esp + 8], 0
00410542  7417                   je       0x41055b
00410544  bb472a0000             mov      ebx, 0x2a47
00410549  0fbff1                 movsx    esi, cx
0041054c  0fbfc2                 movsx    eax, dx
0041054f  b901000000             mov      ecx, 1
00410554  89f2                   mov      edx, esi
00410556  e910fcffff             jmp      0x41016b ;
0041055b  bb472a0000             mov      ebx, 0x2a47
00410560  0fbff1                 movsx    esi, cx
00410563  0fbffa                 movsx    edi, dx
00410566  b901000000             mov      ecx, 1
0041056b  89f2                   mov      edx, esi
0041056d  89f8                   mov      eax, edi
0041056f  e8d3ac0400             call     0x45b247 ; PasteBobCmp
00410574  b901000000             mov      ecx, 1
00410579  bb472a0000             mov      ebx, 0x2a47
0041057e  89f2                   mov      edx, esi
00410580  89f8                   mov      eax, edi
00410582  e91effffff             jmp      0x4104a5 ;
00410587  8a00                   mov      al, byte ptr [eax]
00410589  0fbfd1                 movsx    edx, cx
0041058c  30e4                   xor      ah, ah
0041058e  31db                   xor      ebx, ebx
00410590  053c290000             add      eax, 0x293c
00410595  e9c6fbffff             jmp      0x410160 ;
0041059a  3c36                   cmp      al, 0x36
0041059c  749f                   je       0x41053d
0041059e  e97ffbffff             jmp      0x410122 ;
004105a3  3c17                   cmp      al, 0x17
004105a5  0f8274fdffff           jb       0x41031f
004105ab  0f8694fdffff           jbe      0x410345
004105b1  3c18                   cmp      al, 0x18
004105b3  0f86ddfdffff           jbe      0x410396
004105b9  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004105be  8a0407                 mov      al, byte ptr [edi + eax]
004105c1  0fbfe9                 movsx    ebp, cx
004105c4  0fbff6                 movsx    esi, si
004105c7  30e4                   xor      ah, ah
004105c9  31db                   xor      ebx, ebx
004105cb  b901000000             mov      ecx, 1
004105d0  05a5230000             add      eax, 0x23a5
004105d5  89ea                   mov      edx, ebp
004105d7  6689c3                 mov      bx, ax
004105da  89f0                   mov      eax, esi
004105dc  e866ac0400             call     0x45b247 ; PasteBobCmp
004105e1  807c240800             cmp      byte ptr [esp + 8], 0
004105e6  0f8584fbffff           jne      0x410170
004105ec  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004105f1  01c7                   add      edi, eax
004105f3  30e4                   xor      ah, ah
004105f5  b901000000             mov      ecx, 1
004105fa  8a07                   mov      al, byte ptr [edi]
004105fc  31db                   xor      ebx, ebx
004105fe  05a5230000             add      eax, 0x23a5
00410603  e987fdffff             jmp      0x41038f ;
00410608  3c10                   cmp      al, 0x10
0041060a  723f                   jb       0x41064b
0041060c  0f8606fcffff           jbe      0x410218
00410612  3c12                   cmp      al, 0x12
00410614  0f8224fcffff           jb       0x41023e
0041061a  0f8650fcffff           jbe      0x410270
00410620  3c13                   cmp      al, 0x13
00410622  0f867efcffff           jbe      0x4102a6
00410628  8a5c2408               mov      bl, byte ptr [esp + 8]
0041062c  ba55290000             mov      edx, 0x2955
00410631  84db                   test     bl, bl
00410633  0f84a2fcffff           je       0x4102db
00410639  b801000000             mov      eax, 1
0041063e  31db                   xor      ebx, ebx
00410640  0fbff6                 movsx    esi, si
00410643  6689d3                 mov      bx, dx
00410646  e943fcffff             jmp      0x41028e ;
0041064b  3c0d                   cmp      al, 0xd
0041064d  7232                   jb       0x410681
0041064f  0f864ffbffff           jbe      0x4101a4
00410655  3c0e                   cmp      al, 0xe
00410657  0f8685fbffff           jbe      0x4101e2
0041065d  8a742408               mov      dh, byte ptr [esp + 8]
00410661  bb50290000             mov      ebx, 0x2950
00410666  84f6                   test     dh, dh
00410668  0f848dfbffff           je       0x4101fb
0041066e  b801000000             mov      eax, 1
00410673  81e3ffff0000           and      ebx, 0xffff
00410679  83c10b                 add      ecx, 0xb
0041067c  e9d8fbffff             jmp      0x410259 ;
00410681  3c0c                   cmp      al, 0xc
00410683  0f84effaffff           je       0x410178
00410689  e994faffff             jmp      0x410122 ;
