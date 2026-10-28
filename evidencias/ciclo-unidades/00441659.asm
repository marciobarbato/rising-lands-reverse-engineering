; EnginResetAll; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441659  53                       push ebx
0044165a  51                       push ecx
0044165b  52                       push edx
0044165c  56                       push esi
0044165d  83ec04                   sub esp, 4
00441660  31d2                     xor edx, edx
00441662  891424                   mov dword ptr [esp], edx
00441665  eb03                     jmp 0x44166a
00441667  ff0424                   inc dword ptr [esp]
0044166a  31c0                     xor eax, eax
0044166c  668b0424                 mov ax, word ptr [esp]
00441670  83f804                   cmp eax, 4
00441673  7d59                     jge 0x4416ce
00441675  31f6                     xor esi, esi
00441677  eb1a                     jmp 0x441693
00441679  89c3                     mov ebx, eax
0044167b  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
00441682  42                       inc edx
00441683  c644014200               mov byte ptr [ecx + eax + 0x42], 0
00441688  31c0                     xor eax, eax
0044168a  6689d0                   mov ax, dx
0044168d  83f81e                   cmp eax, 0x1e
00441690  7ce7                     jl 0x441679
00441692  46                       inc esi
00441693  31db                     xor ebx, ebx
00441695  6689f3                   mov bx, si
00441698  83fb1a                   cmp ebx, 0x1a
0044169b  7dca                     jge 0x441667
0044169d  6bdb68                   imul ebx, ebx, 0x68
004416a0  31c0                     xor eax, eax
004416a2  8b0db8194e00             mov ecx, dword ptr [0x4e19b8]
004416a8  668b0424                 mov ax, word ptr [esp]
004416ac  8b0481                   mov eax, dword ptr [ecx + eax*4]
004416af  01d8                     add eax, ebx
004416b1  66c7000000               mov word ptr [eax], 0
004416b6  66c740660000             mov word ptr [eax + 0x66], 0
004416bc  31d2                     xor edx, edx
004416be  66c740040000             mov word ptr [eax + 4], 0
004416c4  89c1                     mov ecx, eax
004416c6  66c740020000             mov word ptr [eax + 2], 0
004416cc  ebba                     jmp 0x441688
004416ce  31f6                     xor esi, esi
004416d0  eb1a                     jmp 0x4416ec
004416d2  89c3                     mov ebx, eax
004416d4  66c74459060000           mov word ptr [ecx + ebx*2 + 6], 0
004416db  42                       inc edx
004416dc  c644014200               mov byte ptr [ecx + eax + 0x42], 0
004416e1  31c0                     xor eax, eax
004416e3  6689d0                   mov ax, dx
004416e6  83f81e                   cmp eax, 0x1e
004416e9  7ce7                     jl 0x4416d2
004416eb  46                       inc esi
004416ec  31c0                     xor eax, eax
004416ee  6689f0                   mov ax, si
004416f1  3d20030000               cmp eax, 0x320
004416f6  7d75                     jge 0x44176d
004416f8  69c014010000             imul eax, eax, 0x114
004416fe  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00441704  8a440302                 mov al, byte ptr [ebx + eax + 2]
00441708  25ff000000               and eax, 0xff
0044170d  0f95c0                   setne al
00441710  84c0                     test al, al
00441712  74d7                     je 0x4416eb
00441714  31c0                     xor eax, eax
00441716  6689f0                   mov ax, si
00441719  69c014010000             imul eax, eax, 0x114
0044171f  66c784039a0000000000     mov word ptr [ebx + eax + 0x9a], 0
00441729  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044172f  c644030200               mov byte ptr [ebx + eax + 2], 0
00441734  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
0044173a  c68403af00000000         mov byte ptr [ebx + eax + 0xaf], 0
00441742  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00441748  01d8                     add eax, ebx
0044174a  83c00a                   add eax, 0xa
0044174d  66c740660000             mov word ptr [eax + 0x66], 0
00441753  66c740040000             mov word ptr [eax + 4], 0
00441759  31d2                     xor edx, edx
0044175b  66c740020000             mov word ptr [eax + 2], 0
00441761  89c1                     mov ecx, eax
00441763  66c7000000               mov word ptr [eax], 0
00441768  e974ffffff               jmp 0x4416e1
0044176d  83c404                   add esp, 4
00441770  5e                       pop esi
00441771  5a                       pop edx
00441772  59                       pop ecx
00441773  5b                       pop ebx
00441774  c3                       ret
