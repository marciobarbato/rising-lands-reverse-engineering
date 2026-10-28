; iagVilleReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00484310..0x00484539 (end exclusive); labels are original SBL names
00484310  53                       push ebx
00484311  51                       push ecx
00484312  52                       push edx
00484313  56                       push esi
00484314  57                       push edi
00484315  55                       push ebp
00484316  83ec0c                   sub esp, 0xc
00484319  b84cb85100               mov eax, 0x51b84c
0048431e  31ed                     xor ebp, ebp
00484320  bb4cb85100               mov ebx, 0x51b84c
00484325  896c2408                 mov dword ptr [esp + 8], ebp
00484329  83c02c                   add eax, 0x2c
0048432c  895c2404                 mov dword ptr [esp + 4], ebx
00484330  890424                   mov dword ptr [esp], eax
00484333  e911010000               jmp 0x484449
00484338  41                       inc ecx
00484339  81f9e8030000             cmp ecx, 0x3e8
0048433f  7d53                     jge 0x484394
00484341  31db                     xor ebx, ebx
00484343  6689cb                   mov bx, cx
00484346  89d8                     mov eax, ebx
00484348  e8e863f9ff               call 0x41a735 ; -> BatimentExiste
0048434d  84c0                     test al, al
0048434f  74e7                     je 0x484338
00484351  89d8                     mov eax, ebx
00484353  e8345df9ff               call 0x41a08c ; -> BatimentGetPlayer
00484358  25ff000000               and eax, 0xff
0048435d  39e8                     cmp eax, ebp
0048435f  75d7                     jne 0x484338
00484361  89d8                     mov eax, ebx
00484363  e88c61f9ff               call 0x41a4f4 ; -> BatimentGetType
00484368  25ff000000               and eax, 0xff
0048436d  66ff0446                 inc word ptr [esi + eax*2]
00484371  8b7e6c                   mov edi, dword ptr [esi + 0x6c]
00484374  47                       inc edi
00484375  89d8                     mov eax, ebx
00484377  897e6c                   mov dword ptr [esi + 0x6c], edi
0048437a  e87561f9ff               call 0x41a4f4 ; -> BatimentGetType
0048437f  25ff000000               and eax, 0xff
00484384  83f803                   cmp eax, 3
00484387  75af                     jne 0x484338
00484389  89ca                     mov edx, ecx
0048438b  89e8                     mov eax, ebp
0048438d  e8931c0000               call 0x486025 ; -> iagRessAddToCaveList
00484392  eba4                     jmp 0x484338
00484394  8b4c2404                 mov ecx, dword ptr [esp + 4]
00484398  ba0a000000               mov edx, 0xa
0048439d  89e8                     mov eax, ebp
0048439f  89ef                     mov edi, ebp
004843a1  e832f8ffff               call 0x483bd8 ; -> iaGroupNew
004843a6  894160                   mov dword ptr [ecx + 0x60], eax
004843a9  83f8ff                   cmp eax, -1
004843ac  0f846b000000             je 0x48441d
004843b2  ba0b000000               mov edx, 0xb
004843b7  89e8                     mov eax, ebp
004843b9  e81af8ffff               call 0x483bd8 ; -> iaGroupNew
004843be  89415c                   mov dword ptr [ecx + 0x5c], eax
004843c1  83f8ff                   cmp eax, -1
004843c4  7457                     je 0x48441d
004843c6  ba09000000               mov edx, 9
004843cb  89f8                     mov eax, edi
004843cd  31db                     xor ebx, ebx
004843cf  e8bcf3ffff               call 0x483790 ; -> iagUnitFindTypeIntoPool
004843d4  6689c3                   mov bx, ax
004843d7  81fbffff0000             cmp ebx, 0xffff
004843dd  743e                     je 0x48441d
004843df  89da                     mov edx, ebx
004843e1  89f8                     mov eax, edi
004843e3  e89eeeffff               call 0x483286 ; -> iagUnitRemoveFromPool
004843e8  89d8                     mov eax, ebx
004843ea  e822cafbff               call 0x440e11 ; -> EnginGetEtat
004843ef  25ff000000               and eax, 0xff
004843f4  83f80e                   cmp eax, 0xe
004843f7  750c                     jne 0x484405
004843f9  89da                     mov edx, ebx
004843fb  8b4160                   mov eax, dword ptr [ecx + 0x60]
004843fe  e836e5ffff               call 0x482939 ; -> iagUnitAddToGroup
00484403  ebc1                     jmp 0x4843c6
00484405  89d8                     mov eax, ebx
00484407  e805cafbff               call 0x440e11 ; -> EnginGetEtat
0048440c  25ff000000               and eax, 0xff
00484411  83f807                   cmp eax, 7
00484414  75b0                     jne 0x4843c6
00484416  89da                     mov edx, ebx
00484418  8b415c                   mov eax, dword ptr [ecx + 0x5c]
0048441b  ebe1                     jmp 0x4843fe
0048441d  c74668ffffffff           mov dword ptr [esi + 0x68], 0xffffffff
00484424  8b4c2408                 mov ecx, dword ptr [esp + 8]
00484428  8b3424                   mov esi, dword ptr [esp]
0048442b  8b7c2404                 mov edi, dword ptr [esp + 4]
0048442f  45                       inc ebp
00484430  83c114                   add ecx, 0x14
00484433  83c67c                   add esi, 0x7c
00484436  83c77c                   add edi, 0x7c
00484439  894c2408                 mov dword ptr [esp + 8], ecx
0048443d  893424                   mov dword ptr [esp], esi
00484440  897c2404                 mov dword ptr [esp + 4], edi
00484444  83fd04                   cmp ebp, 4
00484447  7d41                     jge 0x48448a
00484449  8b542408                 mov edx, dword ptr [esp + 8]
0048444d  a1a8805000               mov eax, dword ptr [0x5080a8]
00484452  01d0                     add eax, edx
00484454  8a4001                   mov al, byte ptr [eax + 1]
00484457  25ff000000               and eax, 0xff
0048445c  83f802                   cmp eax, 2
0048445f  75c3                     jne 0x484424
00484461  8b742404                 mov esi, dword ptr [esp + 4]
00484465  8b0424                   mov eax, dword ptr [esp]
00484468  89f3                     mov ebx, esi
0048446a  66c7030000               mov word ptr [ebx], 0
0048446f  83c302                   add ebx, 2
00484472  66c7432a0000             mov word ptr [ebx + 0x2a], 0
00484478  39c3                     cmp ebx, eax
0048447a  75ee                     jne 0x48446a
0048447c  c7466c00000000           mov dword ptr [esi + 0x6c], 0
00484483  31c9                     xor ecx, ecx
00484485  e9b7feffff               jmp 0x484341
0048448a  31c0                     xor eax, eax
0048448c  83c40c                   add esp, 0xc
0048448f  e90c020000               jmp 0x4846a0
; 0x00484494..0x00484539 not reached by any static path (padding or data):
00484494  .byte 5351525689c6c1e00529f0b94cb85100
004844a4  .byte c1e002ba0a00000001c189f0e823f7ff
004844b4  .byte ff89416083f8ff750ab80f001a1a5e5a
004844c4  .byte 595bc3ba0b00000089f0e805f7ffff89
004844d4  .byte 415c83f8ff74e2ba0900000089f031db
004844e4  .byte e8a7f2ffff6689c381fbffff0000743e
004844f4  .byte 89da89f0e889edffff89d8e80dc9fbff
00484504  .byte 25ff00000083f80e750c89da8b4160e8
00484514  .byte 21e4ffffebc189d8e8f0c8fbff25ff00
00484524  .byte 000083f80775b089da8b415cebe131c0
00484534  .byte 5e5a595bc3

; shared Watcom tail reached from iagVilleReset; intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x004846a0..0x004846a7 (end exclusive); labels are original SBL names
004846a0  5d                       pop ebp
004846a1  5f                       pop edi
004846a2  5e                       pop esi
004846a3  5a                       pop edx
004846a4  59                       pop ecx
004846a5  5b                       pop ebx
004846a6  c3                       ret
