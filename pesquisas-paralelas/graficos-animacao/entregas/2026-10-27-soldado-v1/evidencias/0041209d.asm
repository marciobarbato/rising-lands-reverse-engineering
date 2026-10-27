; AffBallon [0x41209d, 0x4122d5)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041209d  51                     push     ecx
0041209e  56                     push     esi
0041209f  57                     push     edi
004120a0  55                     push     ebp
004120a1  50                     push     eax
004120a2  52                     push     edx
004120a3  89df                   mov      edi, ebx
004120a5  31d2                   xor      edx, edx
004120a7  6689c2                 mov      dx, ax
004120aa  89d6                   mov      esi, edx
004120ac  c1e604                 shl      esi, 4
004120af  01d6                   add      esi, edx
004120b1  c1e602                 shl      esi, 2
004120b4  8b1c24                 mov      ebx, dword ptr [esp]
004120b7  01d6                   add      esi, edx
004120b9  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
004120be  c1e602                 shl      esi, 2
004120c1  83c31e                 add      ebx, 0x1e
004120c4  01c6                   add      esi, eax
004120c6  31d2                   xor      edx, edx
004120c8  89f8                   mov      eax, edi
004120ca  8a96ab000000           mov      dl, byte ptr [esi + 0xab]
004120d0  05c7000000             add      eax, 0xc7
004120d5  83fa23                 cmp      edx, 0x23
004120d8  7d15                   jge      0x4120ef
004120da  b901000000             mov      ecx, 1
004120df  0fbfd0                 movsx    edx, ax
004120e2  0fbfc3                 movsx    eax, bx
004120e5  bb61130000             mov      ebx, 0x1361
004120ea  e974000000             jmp      0x412163 ; 
004120ef  7c17                   jl       0x412108
004120f1  83fa28                 cmp      edx, 0x28
004120f4  7d12                   jge      0x412108
004120f6  b901000000             mov      ecx, 1
004120fb  0fbfd0                 movsx    edx, ax
004120fe  0fbfc3                 movsx    eax, bx
00412101  bb62130000             mov      ebx, 0x1362
00412106  eb5b                   jmp      0x412163 ; 
00412108  31c0                   xor      eax, eax
0041210a  8a86ab000000           mov      al, byte ptr [esi + 0xab]
00412110  83f828                 cmp      eax, 0x28
00412113  7c24                   jl       0x412139
00412115  83f82d                 cmp      eax, 0x2d
00412118  7d1f                   jge      0x412139
0041211a  89f8                   mov      eax, edi
0041211c  05c7000000             add      eax, 0xc7
00412121  0fbfd0                 movsx    edx, ax
00412124  8b0424                 mov      eax, dword ptr [esp]
00412127  b901000000             mov      ecx, 1
0041212c  051e000000             add      eax, 0x1e
00412131  bb63130000             mov      ebx, 0x1363
00412136  98                     cwde     
00412137  eb2a                   jmp      0x412163 ; 
00412139  31c0                   xor      eax, eax
0041213b  8a86ab000000           mov      al, byte ptr [esi + 0xab]
00412141  83f82d                 cmp      eax, 0x2d
00412144  7c22                   jl       0x412168
00412146  89f8                   mov      eax, edi
00412148  05c7000000             add      eax, 0xc7
0041214d  0fbfd0                 movsx    edx, ax
00412150  8b0424                 mov      eax, dword ptr [esp]
00412153  b901000000             mov      ecx, 1
00412158  051e000000             add      eax, 0x1e
0041215d  bb64130000             mov      ebx, 0x1364
00412162  98                     cwde     
00412163  e82e960400             call     0x45b796 ; PasteOmbreCmp
00412168  8b0c24                 mov      ecx, dword ptr [esp]
0041216b  89fb                   mov      ebx, edi
0041216d  8aa6ae000000           mov      ah, byte ptr [esi + 0xae]
00412173  83c14a                 add      ecx, 0x4a
00412176  81c3b8000000           add      ebx, 0xb8
0041217c  84e4                   test     ah, ah
0041217e  0f8486000000           je       0x41220a
00412184  31c0                   xor      eax, eax
00412186  668b442404             mov      ax, word ptr [esp + 4]
0041218b  e8b5fe0200             call     0x442045 ; EnginGetPlayer
00412190  bd03000000             mov      ebp, 3
00412195  31d2                   xor      edx, edx
00412197  25ff000000             and      eax, 0xff
0041219c  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004121a2  50                     push     eax
004121a3  89d0                   mov      eax, edx
004121a5  c1fa1f                 sar      edx, 0x1f
004121a8  f7fd                   idiv     ebp
004121aa  89c2                   mov      edx, eax
004121ac  bd04000000             mov      ebp, 4
004121b1  c1fa1f                 sar      edx, 0x1f
004121b4  f7fd                   idiv     ebp
004121b6  81c239130000           add      edx, 0x1339
004121bc  31c0                   xor      eax, eax
004121be  6689d0                 mov      ax, dx
004121c1  31d2                   xor      edx, edx
004121c3  0fbfe9                 movsx    ebp, cx
004121c6  8a96ab000000           mov      dl, byte ptr [esi + 0xab]
004121cc  b901000000             mov      ecx, 1
004121d1  29d3                   sub      ebx, edx
004121d3  0fbfd3                 movsx    edx, bx
004121d6  89c3                   mov      ebx, eax
004121d8  89e8                   mov      eax, ebp
004121da  e876a20400             call     0x45c455 ; PastePlayerCmp
004121df  31d2                   xor      edx, edx
004121e1  8a96a4000000           mov      dl, byte ptr [esi + 0xa4]
004121e7  bb04000000             mov      ebx, 4
004121ec  89d0                   mov      eax, edx
004121ee  c1fa1f                 sar      edx, 0x1f
004121f1  f7fb                   idiv     ebx
004121f3  81c232130000           add      edx, 0x1332
004121f9  31db                   xor      ebx, ebx
004121fb  31c0                   xor      eax, eax
004121fd  6689d3                 mov      bx, dx
00412200  8a86ab000000           mov      al, byte ptr [esi + 0xab]
00412206  89fa                   mov      edx, edi
00412208  eb5e                   jmp      0x412268 ; 
0041220a  31c0                   xor      eax, eax
0041220c  668b442404             mov      ax, word ptr [esp + 4]
00412211  e82ffe0200             call     0x442045 ; EnginGetPlayer
00412216  25ff000000             and      eax, 0xff
0041221b  50                     push     eax
0041221c  30e4                   xor      ah, ah
0041221e  8a8696000000           mov      al, byte ptr [esi + 0x96]
00412224  053d130000             add      eax, 0x133d
00412229  25ffff0000             and      eax, 0xffff
0041222e  31d2                   xor      edx, edx
00412230  0fbfe9                 movsx    ebp, cx
00412233  8a96ab000000           mov      dl, byte ptr [esi + 0xab]
00412239  b901000000             mov      ecx, 1
0041223e  29d3                   sub      ebx, edx
00412240  0fbfd3                 movsx    edx, bx
00412243  89c3                   mov      ebx, eax
00412245  89e8                   mov      eax, ebp
00412247  e809a20400             call     0x45c455 ; PastePlayerCmp
0041224c  30e4                   xor      ah, ah
0041224e  8a8694000000           mov      al, byte ptr [esi + 0x94]
00412254  31db                   xor      ebx, ebx
00412256  0536130000             add      eax, 0x1336
0041225b  6689c3                 mov      bx, ax
0041225e  31c0                   xor      eax, eax
00412260  89fa                   mov      edx, edi
00412262  8a86ab000000           mov      al, byte ptr [esi + 0xab]
00412268  b901000000             mov      ecx, 1
0041226d  29c2                   sub      edx, eax
0041226f  8b4424fe               mov      eax, dword ptr [esp - 2]
00412273  0fbfd2                 movsx    edx, dx
00412276  c1f810                 sar      eax, 0x10
00412279  e8c98f0400             call     0x45b247 ; PasteBobCmp
0041227e  31c0                   xor      eax, eax
00412280  668b442404             mov      ax, word ptr [esp + 4]
00412285  e8bbfd0200             call     0x442045 ; EnginGetPlayer
0041228a  bb14000000             mov      ebx, 0x14
0041228f  25ff000000             and      eax, 0xff
00412294  31d2                   xor      edx, edx
00412296  50                     push     eax
00412297  a17c8f5000             mov      eax, dword ptr [0x508f7c]
0041229c  f7f3                   div      ebx
0041229e  8d824d130000           lea      eax, [edx + 0x134d]
004122a4  31db                   xor      ebx, ebx
004122a6  6689c3                 mov      bx, ax
004122a9  31c0                   xor      eax, eax
004122ab  83c70f                 add      edi, 0xf
004122ae  8a86ab000000           mov      al, byte ptr [esi + 0xab]
004122b4  29c7                   sub      edi, eax
004122b6  8b442404               mov      eax, dword ptr [esp + 4]
004122ba  b901000000             mov      ecx, 1
004122bf  0560000000             add      eax, 0x60
004122c4  0fbfd7                 movsx    edx, di
004122c7  98                     cwde     
004122c8  e888a10400             call     0x45c455 ; PastePlayerCmp
004122cd  83c408                 add      esp, 8
004122d0  5d                     pop      ebp
004122d1  5f                     pop      edi
004122d2  5e                     pop      esi
004122d3  59                     pop      ecx
004122d4  c3                     ret      
