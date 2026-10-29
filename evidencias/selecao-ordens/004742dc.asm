; SelectionEngin; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004742dc  51                       push ecx
004742dd  56                       push esi
004742de  57                       push edi
004742df  83ec1c                   sub esp, 0x1c
004742e2  88442418                 mov byte ptr [esp + 0x18], al
004742e6  89d9                     mov ecx, ebx
004742e8  31db                     xor ebx, ebx
004742ea  6689d3                   mov bx, dx
004742ed  bf00010000               mov edi, 0x100
004742f2  89da                     mov edx, ebx
004742f4  89d8                     mov eax, ebx
004742f6  c1fa1f                   sar edx, 0x1f
004742f9  f7ff                     idiv edi
004742fb  89542408                 mov dword ptr [esp + 8], edx
004742ff  89da                     mov edx, ebx
00474301  89d8                     mov eax, ebx
00474303  c1fa1f                   sar edx, 0x1f
00474306  f7ff                     idiv edi
00474308  31db                     xor ebx, ebx
0047430a  6689cb                   mov bx, cx
0047430d  890424                   mov dword ptr [esp], eax
00474310  89da                     mov edx, ebx
00474312  89d8                     mov eax, ebx
00474314  c1fa1f                   sar edx, 0x1f
00474317  f7ff                     idiv edi
00474319  89542410                 mov dword ptr [esp + 0x10], edx
0047431d  89da                     mov edx, ebx
0047431f  89d8                     mov eax, ebx
00474321  c1fa1f                   sar edx, 0x1f
00474324  f7ff                     idiv edi
00474326  8b542410                 mov edx, dword ptr [esp + 0x10]
0047432a  89442404                 mov dword ptr [esp + 4], eax
0047432e  663b542408               cmp dx, word ptr [esp + 8]
00474333  730d                     jae 0x474342
00474335  8d542410                 lea edx, [esp + 0x10]
00474339  8d442408                 lea eax, [esp + 8]
0047433d  e87e39ffff               call 0x467cc0
00474342  8b0424                   mov eax, dword ptr [esp]
00474345  663b442404               cmp ax, word ptr [esp + 4]
0047434a  760b                     jbe 0x474357
0047434c  8d542404                 lea edx, [esp + 4]
00474350  89e0                     mov eax, esp
00474352  e86939ffff               call 0x467cc0
00474357  31c9                     xor ecx, ecx
00474359  31f6                     xor esi, esi
0047435b  894c240c                 mov dword ptr [esp + 0xc], ecx
0047435f  e92b020000               jmp 0x47458f
00474364  b001                     mov al, 1
00474366  84c0                     test al, al
00474368  0f8420020000             je 0x47458e
0047436e  31db                     xor ebx, ebx
00474370  6689f3                   mov bx, si
00474373  89d8                     mov eax, ebx
00474375  e8cbdcfcff               call 0x442045
0047437a  3a442418                 cmp al, byte ptr [esp + 0x18]
0047437e  0f850a020000             jne 0x47458e
00474384  69d314010000             imul edx, ebx, 0x114
0047438a  a1a0194e00               mov eax, dword ptr [0x4e19a0]
0047438f  01c2                     add edx, eax
00474391  80babd00000000           cmp byte ptr [edx + 0xbd], 0
00474398  7419                     je 0x4743b3
0047439a  89d8                     mov eax, ebx
0047439c  c682bd00000000           mov byte ptr [edx + 0xbd], 0
004743a3  31d2                     xor edx, edx
004743a5  e89bdcfcff               call 0x442045
004743aa  88c2                     mov dl, al
004743ac  89d8                     mov eax, ebx
004743ae  e8c3e1ffff               call 0x472576
004743b3  31c0                     xor eax, eax
004743b5  31c9                     xor ecx, ecx
004743b7  31db                     xor ebx, ebx
004743b9  31d2                     xor edx, edx
004743bb  31ff                     xor edi, edi
004743bd  668b442404               mov ax, word ptr [esp + 4]
004743c2  668b4c2410               mov cx, word ptr [esp + 0x10]
004743c7  668b1c24                 mov bx, word ptr [esp]
004743cb  6689f7                   mov di, si
004743ce  50                       push eax
004743cf  668b54240c               mov dx, word ptr [esp + 0xc]
004743d4  89f8                     mov eax, edi
004743d6  e8191efdff               call 0x4461f4
004743db  84c0                     test al, al
004743dd  0f84ab010000             je 0x47458e
004743e3  8a442418                 mov al, byte ptr [esp + 0x18]
004743e7  88442414                 mov byte ptr [esp + 0x14], al
004743eb  89f8                     mov eax, edi
004743ed  89f1                     mov ecx, esi
004743ef  e8b9f9fcff               call 0x443dad
004743f4  84c0                     test al, al
004743f6  0f84d9000000             je 0x4744d5
004743fc  69d714010000             imul edx, edi, 0x114
00474402  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00474407  01c2                     add edx, eax
00474409  31c0                     xor eax, eax
0047440b  8a4202                   mov al, byte ptr [edx + 2]
0047440e  89f3                     mov ebx, esi
00474410  83f80e                   cmp eax, 0xe
00474413  7429                     je 0x47443e
00474415  0fb67a01                 movzx edi, byte ptr [edx + 1]
00474419  83ff10                   cmp edi, 0x10
0047441c  7512                     jne 0x474430
0047441e  83f80d                   cmp eax, 0xd
00474421  750d                     jne 0x474430
00474423  31c0                     xor eax, eax
00474425  8a82ab000000             mov al, byte ptr [edx + 0xab]
0047442b  83f832                   cmp eax, 0x32
0047442e  750e                     jne 0x47443e
00474430  31c0                     xor eax, eax
00474432  6689d8                   mov ax, bx
00474435  e88521fdff               call 0x4465bf
0047443a  84c0                     test al, al
0047443c  7504                     jne 0x474442
0047443e  30c0                     xor al, al
00474440  eb02                     jmp 0x474444
00474442  b001                     mov al, 1
00474444  84c0                     test al, al
00474446  0f8489000000             je 0x4744d5
0047444c  31d2                     xor edx, edx
0047444e  6689ca                   mov dx, cx
00474451  89d0                     mov eax, edx
00474453  e8eddbfcff               call 0x442045
00474458  8a642414                 mov ah, byte ptr [esp + 0x14]
0047445c  38e0                     cmp al, ah
0047445e  0f8571000000             jne 0x4744d5
00474464  69d214010000             imul edx, edx, 0x114
0047446a  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00474470  01d3                     add ebx, edx
00474472  80bbbd00000000           cmp byte ptr [ebx + 0xbd], 0
00474479  755a                     jne 0x4744d5
0047447b  31d2                     xor edx, edx
0047447d  88e2                     mov dl, ah
0047447f  c1e209                   shl edx, 9
00474482  31c0                     xor eax, eax
00474484  668b8228875000           mov ax, word ptr [edx + 0x508728]
0047448b  3dff000000               cmp eax, 0xff
00474490  7d24                     jge 0x4744b6
00474492  89c7                     mov edi, eax
00474494  47                       inc edi
00474495  89f8                     mov eax, edi
00474497  6689ba28875000           mov word ptr [edx + 0x508728], di
0047449e  25ffff0000               and eax, 0xffff
004744a3  66898c4228875000         mov word ptr [edx + eax*2 + 0x508728], cx
004744ab  b001                     mov al, 1
004744ad  c683bd00000001           mov byte ptr [ebx + 0xbd], 1
004744b4  eb02                     jmp 0x4744b8
004744b6  30c0                     xor al, al
004744b8  84c0                     test al, al
004744ba  7419                     je 0x4744d5
004744bc  31c0                     xor eax, eax
004744be  6689c8                   mov ax, cx
004744c1  69c014010000             imul eax, eax, 0x114
004744c7  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004744cd  c68402bd00000001         mov byte ptr [edx + eax + 0xbd], 1
004744d5  31c0                     xor eax, eax
004744d7  668b44240c               mov ax, word ptr [esp + 0xc]
004744dc  83f801                   cmp eax, 1
004744df  0f8da9000000             jge 0x47458e
004744e5  31d2                     xor edx, edx
004744e7  6689f2                   mov dx, si
004744ea  89d0                     mov eax, edx
004744ec  e834dbfcff               call 0x442025
004744f1  25ff000000               and eax, 0xff
004744f6  83f80a                   cmp eax, 0xa
004744f9  0f848f000000             je 0x47458e
004744ff  8a442418                 mov al, byte ptr [esp + 0x18]
00474503  3a0541805000             cmp al, byte ptr [0x508041]
00474509  0f857f000000             jne 0x47458e
0047450f  89d0                     mov eax, edx
00474511  e80fdbfcff               call 0x442025
00474516  25ff000000               and eax, 0xff
0047451b  e824c7fcff               call 0x440c44
00474520  84c0                     test al, al
00474522  756a                     jne 0x47458e
00474524  ff44240c                 inc dword ptr [esp + 0xc]
00474528  89d0                     mov eax, edx
0047452a  e8f6dafcff               call 0x442025
0047452f  25ff000000               and eax, 0xff
00474534  83f807                   cmp eax, 7
00474537  0f85bd000000             jne 0x4745fa
0047453d  89d0                     mov eax, edx
0047453f  e8cdc8fcff               call 0x440e11
00474544  25ff000000               and eax, 0xff
00474549  83f80b                   cmp eax, 0xb
0047454c  7415                     je 0x474563
0047454e  89d0                     mov eax, edx
00474550  e8bcc8fcff               call 0x440e11
00474555  25ff000000               and eax, 0xff
0047455a  83f80f                   cmp eax, 0xf
0047455d  0f8597000000             jne 0x4745fa
00474563  31ff                     xor edi, edi
00474565  6689f7                   mov di, si
00474568  69c714010000             imul eax, edi, 0x114
0047456e  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
00474574  01d0                     add eax, edx
00474576  31db                     xor ebx, ebx
00474578  0504010000               add eax, 0x104
0047457d  ba16000000               mov edx, 0x16
00474582  e839650100               call 0x48aac0
00474587  89f8                     mov eax, edi
00474589  e8d0c7fcff               call 0x440d5e
0047458e  46                       inc esi
0047458f  31d2                     xor edx, edx
00474591  6689f2                   mov dx, si
00474594  81fa20030000             cmp edx, 0x320
0047459a  0f8d68000000             jge 0x474608
004745a0  89d0                     mov eax, edx
004745a2  e806f8fcff               call 0x443dad
004745a7  84c0                     test al, al
004745a9  74e3                     je 0x47458e
004745ab  69c214010000             imul eax, edx, 0x114
004745b1  8b15a0194e00             mov edx, dword ptr [0x4e19a0]
004745b7  01c2                     add edx, eax
004745b9  31c0                     xor eax, eax
004745bb  8a4202                   mov al, byte ptr [edx + 2]
004745be  89f1                     mov ecx, esi
004745c0  83f80e                   cmp eax, 0xe
004745c3  742e                     je 0x4745f3
004745c5  31db                     xor ebx, ebx
004745c7  8a5a01                   mov bl, byte ptr [edx + 1]
004745ca  83fb10                   cmp ebx, 0x10
004745cd  7512                     jne 0x4745e1
004745cf  83f80d                   cmp eax, 0xd
004745d2  750d                     jne 0x4745e1
004745d4  31c0                     xor eax, eax
004745d6  8a82ab000000             mov al, byte ptr [edx + 0xab]
004745dc  83f832                   cmp eax, 0x32
004745df  7512                     jne 0x4745f3
004745e1  31c0                     xor eax, eax
004745e3  6689c8                   mov ax, cx
004745e6  e8d41ffdff               call 0x4465bf
004745eb  84c0                     test al, al
004745ed  0f8571fdffff             jne 0x474364
004745f3  30c0                     xor al, al
004745f5  e96cfdffff               jmp 0x474366
004745fa  ba08000000               mov edx, 8
004745ff  31c0                     xor eax, eax
00474601  31db                     xor ebx, ebx
00474603  6689f0                   mov ax, si
00474606  eb81                     jmp 0x474589
00474608  83c41c                   add esp, 0x1c
0047460b  5f                       pop edi
0047460c  5e                       pop esi
0047460d  59                       pop ecx
0047460e  c3                       ret
; 1 trailing bytes are not code (alignment/data): 00
