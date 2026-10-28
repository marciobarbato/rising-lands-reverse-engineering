; iagVilleSendMessage (messages); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x00484808..0x0048491f (end exclusive); labels are original SBL names
00484808  51                       push ecx
00484809  56                       push esi
0048480a  55                       push ebp
0048480b  89e5                     mov ebp, esp
0048480d  83ec08                   sub esp, 8
00484810  89c6                     mov esi, eax
00484812  8855fc                   mov byte ptr [ebp - 4], dl
00484815  89da                     mov edx, ebx
00484817  31db                     xor ebx, ebx
00484819  6689c3                   mov bx, ax
0048481c  89d8                     mov eax, ebx
0048481e  e86958f9ff               call 0x41a08c ; -> BatimentGetPlayer
00484823  25ff000000               and eax, 0xff
00484828  8945f8                   mov dword ptr [ebp - 8], eax
0048482b  83f804                   cmp eax, 4
0048482e  0f8de5000000             jge 0x484919
00484834  31c0                     xor eax, eax
00484836  8a45f8                   mov al, byte ptr [ebp - 8]
00484839  e8d98ffeff               call 0x46d817 ; -> PlayerGetType
0048483e  25ff000000               and eax, 0xff
00484843  83f802                   cmp eax, 2
00484846  0f85cd000000             jne 0x484919
0048484c  8b45f8                   mov eax, dword ptr [ebp - 8]
0048484f  89c1                     mov ecx, eax
00484851  c1e105                   shl ecx, 5
00484854  29c1                     sub ecx, eax
00484856  8a45fc                   mov al, byte ptr [ebp - 4]
00484859  c1e102                   shl ecx, 2
0048485c  fec8                     dec al
0048485e  81c14cb85100             add ecx, 0x51b84c
00484864  3c03                     cmp al, 3
00484866  0f87ad000000             ja 0x484919
0048486c  25ff000000               and eax, 0xff
00484871  2eff2485f8474800         jmp dword ptr cs:[eax*4 + 0x4847f8]
00484879  89d8                     mov eax, ebx
0048487b  e8745cf9ff               call 0x41a4f4 ; -> BatimentGetType
00484880  0fb6f0                   movzx esi, al
00484883  83fe03                   cmp esi, 3
00484886  750a                     jne 0x484892
00484888  8b45f8                   mov eax, dword ptr [ebp - 8]
0048488b  89da                     mov edx, ebx
0048488d  e893170000               call 0x486025 ; -> iagRessAddToCaveList
00484892  89f3                     mov ebx, esi
00484894  31d2                     xor edx, edx
00484896  89c8                     mov eax, ecx
00484898  8a55fc                   mov dl, byte ptr [ebp - 4]
0048489b  e8fd000000               call 0x48499d
004848a0  e974000000               jmp 0x484919
004848a5  89d8                     mov eax, ebx
004848a7  31d2                     xor edx, edx
004848a9  e8465cf9ff               call 0x41a4f4 ; -> BatimentGetType
004848ae  88c2                     mov dl, al
004848b0  89d0                     mov eax, edx
004848b2  66ff0c41                 dec word ptr [ecx + eax*2]
004848b6  ff496c                   dec dword ptr [ecx + 0x6c]
004848b9  83fa03                   cmp edx, 3
004848bc  750a                     jne 0x4848c8
004848be  8b45f8                   mov eax, dword ptr [ebp - 8]
004848c1  89da                     mov edx, ebx
004848c3  e89d170000               call 0x486065 ; -> iagRessRemoveFromCaveList
004848c8  89c8                     mov eax, ecx
004848ca  31d2                     xor edx, edx
004848cc  31db                     xor ebx, ebx
004848ce  8a55fc                   mov dl, byte ptr [ebp - 4]
004848d1  6689f3                   mov bx, si
004848d4  ebc5                     jmp 0x48489b
004848d6  31c9                     xor ecx, ecx
004848d8  6689d1                   mov cx, dx
004848db  89c8                     mov eax, ecx
004848dd  31d2                     xor edx, edx
004848df  e85ac8fbff               call 0x44113e ; -> EnginGetCase
004848e4  6689c2                   mov dx, ax
004848e7  8b45f8                   mov eax, dword ptr [ebp - 8]
004848ea  e8a52c0000               call 0x487594 ; -> iagWarSearchBattleFromPos
004848ef  83f8ff                   cmp eax, -1
004848f2  7519                     jne 0x48490d
004848f4  6a00                     push 0
004848f6  6a00                     push 0
004848f8  6a00                     push 0
004848fa  ba13000000               mov edx, 0x13
004848ff  6a00                     push 0
00484901  8b45f8                   mov eax, dword ptr [ebp - 8]
00484904  31c9                     xor ecx, ecx
00484906  e81590ffff               call 0x47d920 ; -> iaProbPost
0048490b  eb0c                     jmp 0x484919
0048490d  89cb                     mov ebx, ecx
0048490f  89c2                     mov edx, eax
00484911  8b45f8                   mov eax, dword ptr [ebp - 8]
00484914  e85f320000               call 0x487b78 ; -> iagWarAddEnnemyToBattle
00484919  89ec                     mov esp, ebp
0048491b  5d                       pop ebp
0048491c  5e                       pop esi
0048491d  59                       pop ecx
0048491e  c3                       ret
