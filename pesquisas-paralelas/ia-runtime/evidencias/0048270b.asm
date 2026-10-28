; iagUnitReset (ai-tables); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0048270b..0x0048292e (end exclusive); labels are original SBL names
0048270b  53                       push ebx
0048270c  51                       push ecx
0048270d  52                       push edx
0048270e  56                       push esi
0048270f  57                       push edi
00482710  55                       push ebp
00482711  83ec0c                   sub esp, 0xc
00482714  31c0                     xor eax, eax
00482716  83c020                   add eax, 0x20
00482719  baffffffff               mov edx, 0xffffffff
0048271e  8990c0a95100             mov dword ptr [eax + 0x51a9c0], edx
00482724  31db                     xor ebx, ebx
00482726  8990c4a95100             mov dword ptr [eax + 0x51a9c4], edx
0048272c  b9ff7f0000               mov ecx, 0x7fff
00482731  668998d2a95100           mov word ptr [eax + 0x51a9d2], bx
00482738  beffff0000               mov esi, 0xffff
0048273d  668988d4a95100           mov word ptr [eax + 0x51a9d4], cx
00482744  6689b0d6a95100           mov word ptr [eax + 0x51a9d6], si
0048274b  baffff0000               mov edx, 0xffff
00482750  b3ff                     mov bl, 0xff
00482752  668990d0a95100           mov word ptr [eax + 0x51a9d0], dx
00482759  31c9                     xor ecx, ecx
0048275b  8898daa95100             mov byte ptr [eax + 0x51a9da], bl
00482761  beffffffff               mov esi, 0xffffffff
00482766  8988dca95100             mov dword ptr [eax + 0x51a9dc], ecx
0048276c  89b0c8a95100             mov dword ptr [eax + 0x51a9c8], esi
00482772  8898dba95100             mov byte ptr [eax + 0x51a9db], bl
00482778  89b0cca95100             mov dword ptr [eax + 0x51a9cc], esi
0048277e  30d2                     xor dl, dl
00482780  8890d8a95100             mov byte ptr [eax + 0x51a9d8], dl
00482786  30f6                     xor dh, dh
00482788  88b0d9a95100             mov byte ptr [eax + 0x51a9d9], dh
0048278e  3d800c0000               cmp eax, 0xc80
00482793  7581                     jne 0x482716
00482795  b864b65100               mov eax, 0x51b664
0048279a  ba64b65100               mov edx, 0x51b664
0048279f  890d60b65100             mov dword ptr [0x51b660], ecx
004827a5  890c24                   mov dword ptr [esp], ecx
004827a8  83c050                   add eax, 0x50
004827ab  89542408                 mov dword ptr [esp + 8], edx
004827af  89442404                 mov dword ptr [esp + 4], eax
004827b3  eb26                     jmp 0x4827db
004827b5  8b5c2404                 mov ebx, dword ptr [esp + 4]
004827b9  8b4c2408                 mov ecx, dword ptr [esp + 8]
004827bd  8b3424                   mov esi, dword ptr [esp]
004827c0  83c360                   add ebx, 0x60
004827c3  83c160                   add ecx, 0x60
004827c6  46                       inc esi
004827c7  895c2404                 mov dword ptr [esp + 4], ebx
004827cb  894c2408                 mov dword ptr [esp + 8], ecx
004827cf  893424                   mov dword ptr [esp], esi
004827d2  83fe04                   cmp esi, 4
004827d5  0f8fb1000000             jg 0x48288c
004827db  31c0                     xor eax, eax
004827dd  8a0424                   mov al, byte ptr [esp]
004827e0  e832b0feff               call 0x46d817 ; -> PlayerGetType
004827e5  25ff000000               and eax, 0xff
004827ea  83f802                   cmp eax, 2
004827ed  75c6                     jne 0x4827b5
004827ef  8b4c2408                 mov ecx, dword ptr [esp + 8]
004827f3  8b542404                 mov edx, dword ptr [esp + 4]
004827f7  89c8                     mov eax, ecx
004827f9  c700ffffffff             mov dword ptr [eax], 0xffffffff
004827ff  83c004                   add eax, 4
00482802  39d0                     cmp eax, edx
00482804  75f3                     jne 0x4827f9
00482806  8b2c24                   mov ebp, dword ptr [esp]
00482809  c74150ffffffff           mov dword ptr [ecx + 0x50], 0xffffffff
00482810  83fd04                   cmp ebp, 4
00482813  74a0                     je 0x4827b5
00482815  89e8                     mov eax, ebp
00482817  31d2                     xor edx, edx
00482819  8b742408                 mov esi, dword ptr [esp + 8]
0048281d  e8b6130000               call 0x483bd8 ; -> iaGroupNew
00482822  83f8ff                   cmp eax, -1
00482825  748e                     je 0x4827b5
00482827  31db                     xor ebx, ebx
00482829  eb01                     jmp 0x48282c
0048282b  43                       inc ebx
0048282c  31d2                     xor edx, edx
0048282e  6689da                   mov dx, bx
00482831  81fa20030000             cmp edx, 0x320
00482837  0f8d78ffffff             jge 0x4827b5
0048283d  89d0                     mov eax, edx
0048283f  e86915fcff               call 0x443dad ; -> EnginEstVivant
00482844  84c0                     test al, al
00482846  74e3                     je 0x48282b
00482848  69c214010000             imul eax, edx, 0x114
0048284e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00482854  01c2                     add edx, eax
00482856  31c0                     xor eax, eax
00482858  8a02                     mov al, byte ptr [edx]
0048285a  39e8                     cmp eax, ebp
0048285c  75cd                     jne 0x48282b
0048285e  8b0e                     mov ecx, dword ptr [esi]
00482860  89c8                     mov eax, ecx
00482862  c1e005                   shl eax, 5
00482865  05e0a95100               add eax, 0x51a9e0
0048286a  74bf                     je 0x48282b
0048286c  668b7810                 mov di, word ptr [eax + 0x10]
00482870  6689ba08010000           mov word ptr [edx + 0x108], di
00482877  898a0c010000             mov dword ptr [edx + 0x10c], ecx
0048287d  668b7812                 mov di, word ptr [eax + 0x12]
00482881  66895810                 mov word ptr [eax + 0x10], bx
00482885  47                       inc edi
00482886  66897812                 mov word ptr [eax + 0x12], di
0048288a  eb9f                     jmp 0x48282b
0048288c  31c0                     xor eax, eax
0048288e  83c40c                   add esp, 0xc
00482891  5d                       pop ebp
00482892  5f                       pop edi
00482893  5e                       pop esi
00482894  5a                       pop edx
00482895  59                       pop ecx
00482896  5b                       pop ebx
00482897  c3                       ret
; 0x00482898..0x0048292e not reached by any static path (padding or data):
00482898  .byte 53515256575589c589c2c1e00229e8be
004828a8  .byte 64b65100c1e00531ea01c689e8e81e13
004828b8  .byte 000083f8ff7507b80f001a1aebcb31db
004828c8  .byte eb014331d26689da81fa200300007d4f
004828d8  .byte 89d0e8ce14fcff84c074e769c2140100
004828e8  .byte 008b15a0194e0001c231c08a0239e875
004828f8  .byte d18b0e89c8c1e00505e0a9510074c366
00482908  .byte 8b78106689ba08010000898a0c010000
00482918  .byte 668b5012668958104266895012eba331
00482928  .byte c0e963ffffff
