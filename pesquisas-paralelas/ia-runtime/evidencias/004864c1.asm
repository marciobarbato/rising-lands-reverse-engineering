; iagWarReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004864c1..0x004866d4 (end exclusive); labels are original SBL names
004864c1  53                       push ebx
004864c2  51                       push ecx
004864c3  52                       push edx
004864c4  56                       push esi
004864c5  57                       push edi
004864c6  55                       push ebp
004864c7  83ec0c                   sub esp, 0xc
004864ca  31d2                     xor edx, edx
004864cc  bbfcbc5100               mov ebx, 0x51bcfc
004864d1  89542408                 mov dword ptr [esp + 8], edx
004864d5  891c24                   mov dword ptr [esp], ebx
004864d8  eb1e                     jmp 0x4864f8
004864da  8b0c24                   mov ecx, dword ptr [esp]
004864dd  8b742408                 mov esi, dword ptr [esp + 8]
004864e1  81c144110000             add ecx, 0x1144
004864e7  46                       inc esi
004864e8  890c24                   mov dword ptr [esp], ecx
004864eb  89742408                 mov dword ptr [esp + 8], esi
004864ef  83fe04                   cmp esi, 4
004864f2  0f8dfa000000             jge 0x4865f2
004864f8  31c0                     xor eax, eax
004864fa  8a442408                 mov al, byte ptr [esp + 8]
004864fe  e81473feff               call 0x46d817 ; -> PlayerGetType
00486503  25ff000000               and eax, 0xff
00486508  83f802                   cmp eax, 2
0048650b  75cd                     jne 0x4864da
0048650d  696c240844110000         imul ebp, dword ptr [esp + 8], 0x1144
00486515  8b0424                   mov eax, dword ptr [esp]
00486518  8b4c2408                 mov ecx, dword ptr [esp + 8]
0048651c  ba09000000               mov edx, 9
00486521  c7400cff000000           mov dword ptr [eax + 0xc], 0xff
00486528  89442404                 mov dword ptr [esp + 4], eax
0048652c  c74014ff000000           mov dword ptr [eax + 0x14], 0xff
00486533  89c7                     mov edi, eax
00486535  c74010ff000000           mov dword ptr [eax + 0x10], 0xff
0048653c  89c8                     mov eax, ecx
0048653e  89fb                     mov ebx, edi
00486540  e893d6ffff               call 0x483bd8 ; -> iaGroupNew
00486545  894304                   mov dword ptr [ebx + 4], eax
00486548  85c0                     test eax, eax
0048654a  745d                     je 0x4865a9
0048654c  31f6                     xor esi, esi
0048654e  ba09000000               mov edx, 9
00486553  89c8                     mov eax, ecx
00486555  31db                     xor ebx, ebx
00486557  e829d1ffff               call 0x483685 ; -> iagUnitFindSuitableForGroupIntoPool
0048655c  6689c3                   mov bx, ax
0048655f  81fbffff0000             cmp ebx, 0xffff
00486565  7442                     je 0x4865a9
00486567  89c8                     mov eax, ecx
00486569  e828e6ffff               call 0x484b96 ; -> iagVilleGetNbBatBuiltTotal
0048656e  0faf8504bd5100           imul eax, dword ptr [ebp + 0x51bd04]
00486575  39c6                     cmp esi, eax
00486577  7d30                     jge 0x4865a9
00486579  89da                     mov edx, ebx
0048657b  89c8                     mov eax, ecx
0048657d  e804cdffff               call 0x483286 ; -> iagUnitRemoveFromPool
00486582  89da                     mov edx, ebx
00486584  69db14010000             imul ebx, ebx, 0x114
0048658a  8b4704                   mov eax, dword ptr [edi + 4]
0048658d  e8a7c3ffff               call 0x482939 ; -> iagUnitAddToGroup
00486592  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00486597  8a440301                 mov al, byte ptr [ebx + eax + 1]
0048659b  25ff000000               and eax, 0xff
004865a0  033485f48c4900           add esi, dword ptr [eax*4 + 0x498cf4]
004865a7  eba5                     jmp 0x48654e
004865a9  8b442404                 mov eax, dword ptr [esp + 4]
004865ad  8d9800110000             lea ebx, [eax + 0x1100]
004865b3  0510010000               add eax, 0x110
004865b8  c78018ffffffffffffff     mov dword ptr [eax - 0xe8], 0xffffffff
004865c2  c7801cffffffffffffff     mov dword ptr [eax - 0xe4], 0xffffffff
004865cc  c78020ffffffffffffff     mov dword ptr [eax - 0xe0], 0xffffffff
004865d6  66c78024ffffff0000       mov word ptr [eax - 0xdc], 0
004865df  66c78026ffffff0000       mov word ptr [eax - 0xda], 0
004865e8  39d8                     cmp eax, ebx
004865ea  0f84eafeffff             je 0x4864da
004865f0  ebc1                     jmp 0x4865b3
004865f2  b80c025200               mov eax, 0x52020c
004865f7  8d8800110000             lea ecx, [eax + 0x1100]
004865fd  0510010000               add eax, 0x110
00486602  c78018ffffffffffffff     mov dword ptr [eax - 0xe8], 0xffffffff
0048660c  c7801cffffffffffffff     mov dword ptr [eax - 0xe4], 0xffffffff
00486616  66c78024ffffff0000       mov word ptr [eax - 0xdc], 0
0048661f  66c78026ffffff0000       mov word ptr [eax - 0xda], 0
00486628  39c8                     cmp eax, ecx
0048662a  75d1                     jne 0x4865fd
0048662c  31c8                     xor eax, ecx
0048662e  83c40c                   add esp, 0xc
00486631  5d                       pop ebp
00486632  5f                       pop edi
00486633  5e                       pop esi
00486634  5a                       pop edx
00486635  59                       pop ecx
00486636  5b                       pop ebx
00486637  c3                       ret
; 0x00486638..0x004866d4 not reached by any static path (padding or data):
00486638  .byte 53515256575589c1c1e00401c8c1e002
00486648  .byte 89c5bffcbc5100c1e506ba0900000001
00486658  .byte c589c801efe876d5ffff89470485c075
00486668  .byte 07b80f001a1aebc131f6ba0900000089
00486678  .byte c831dbe805d0ffff6689c381fbffff00
00486688  .byte 00744289c8e804e5ffff0faf8504bd51
00486698  .byte 0039c67d3089da89c8e8e0cbffff89da
004866a8  .byte 69db140100008b4704e883c2ffffa1a0
004866b8  .byte 194e008a44030125ff000000033485f4
004866c8  .byte 8c4900eba531c0e95dffffff
