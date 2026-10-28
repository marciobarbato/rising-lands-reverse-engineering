; BaisseTouteHerse; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004193d4  53                       push ebx
004193d5  51                       push ecx
004193d6  56                       push esi
004193d7  57                       push edi
004193d8  52                       push edx
004193d9  31ff                     xor edi, edi
004193db  be00010000               mov esi, 0x100
004193e0  6689c7                   mov di, ax
004193e3  89c3                     mov ebx, eax
004193e5  89fa                     mov edx, edi
004193e7  89f8                     mov eax, edi
004193e9  c1fa1f                   sar edx, 0x1f
004193ec  f7fe                     idiv esi
004193ee  89d6                     mov esi, edx
004193f0  89fa                     mov edx, edi
004193f2  89f8                     mov eax, edi
004193f4  c1fa1f                   sar edx, 0x1f
004193f7  c1e208                   shl edx, 8
004193fa  1bc2                     sbb eax, edx
004193fc  c1f808                   sar eax, 8
004193ff  31ff                     xor edi, edi
00419401  668b3c24                 mov di, word ptr [esp]
00419405  89c2                     mov edx, eax
00419407  89f8                     mov eax, edi
00419409  c1e004                   shl eax, 4
0041940c  01f8                     add eax, edi
0041940e  c1e002                   shl eax, 2
00419411  01f8                     add eax, edi
00419413  c1e002                   shl eax, 2
00419416  05c8a04900               add eax, 0x49a0c8
0041941b  30c9                     xor cl, cl
0041941d  668b407c                 mov ax, word ptr [eax + 0x7c]
00419421  25ffff0000               and eax, 0xffff
00419426  0f94c0                   sete al
00419429  84c0                     test al, al
0041942b  0f84d3000000             je 0x419504
00419431  84c9                     test cl, cl
00419433  753c                     jne 0x419471
00419435  31c0                     xor eax, eax
00419437  8b15747d5000             mov edx, dword ptr [0x507d74]
0041943d  6689d8                   mov ax, bx
00419440  8a4402ff                 mov al, byte ptr [edx + eax - 1]
00419444  3a05f95b4900             cmp al, byte ptr [0x495bf9]
0041944a  7516                     jne 0x419462
0041944c  4b                       dec ebx
0041944d  31d2                     xor edx, edx
0041944f  6689da                   mov dx, bx
00419452  be00010000               mov esi, 0x100
00419457  89d0                     mov eax, edx
00419459  c1fa1f                   sar edx, 0x1f
0041945c  f7fe                     idiv esi
0041945e  89d6                     mov esi, edx
00419460  eb02                     jmp 0x419464
00419462  b101                     mov cl, 1
00419464  31c0                     xor eax, eax
00419466  6689f0                   mov ax, si
00419469  85c0                     test eax, eax
0041946b  75c4                     jne 0x419431
0041946d  b101                     mov cl, 1
0041946f  ebc0                     jmp 0x419431
00419471  30c9                     xor cl, cl
00419473  8a2df95b4900             mov ch, byte ptr [0x495bf9]
00419479  84c9                     test cl, cl
0041947b  0f85fe330000             jne 0x41c87f
00419481  31d2                     xor edx, edx
00419483  a1747d5000               mov eax, dword ptr [0x507d74]
00419488  6689da                   mov dx, bx
0041948b  3a2c02                   cmp ch, byte ptr [edx + eax]
0041948e  7555                     jne 0x4194e5
00419490  a1380f4e00               mov eax, dword ptr [0x4e0f38]
00419495  01d2                     add edx, edx
00419497  01c2                     add edx, eax
00419499  f6420180                 test byte ptr [edx + 1], 0x80
0041949d  7412                     je 0x4194b1
0041949f  668b02                   mov ax, word ptr [edx]
004194a2  25e07f0000               and eax, 0x7fe0
004194a7  25ffff0000               and eax, 0xffff
004194ac  c1f805                   sar eax, 5
004194af  eb05                     jmp 0x4194b6
004194b1  b8ffff0000               mov eax, 0xffff
004194b6  31d2                     xor edx, edx
004194b8  6689c2                   mov dx, ax
004194bb  81faffff0000             cmp edx, 0xffff
004194c1  740c                     je 0x4194cf
004194c3  69d214010000             imul edx, edx, 0x114
004194c9  fe823ea14900             inc byte ptr [edx + 0x49a13e]
004194cf  43                       inc ebx
004194d0  31d2                     xor edx, edx
004194d2  6689da                   mov dx, bx
004194d5  be00010000               mov esi, 0x100
004194da  89d0                     mov eax, edx
004194dc  c1fa1f                   sar edx, 0x1f
004194df  f7fe                     idiv esi
004194e1  89d6                     mov esi, edx
004194e3  eb02                     jmp 0x4194e7
004194e5  b101                     mov cl, 1
004194e7  31c0                     xor eax, eax
004194e9  6689f0                   mov ax, si
004194ec  3dff000000               cmp eax, 0xff
004194f1  7586                     jne 0x419479
004194f3  b101                     mov cl, 1
004194f5  eb82                     jmp 0x419479
004194f7  b101                     mov cl, 1
004194f9  31c0                     xor eax, eax
004194fb  6689d0                   mov ax, dx
004194fe  85c0                     test eax, eax
00419500  7502                     jne 0x419504
00419502  b101                     mov cl, 1
00419504  84c9                     test cl, cl
00419506  7535                     jne 0x41953d
00419508  31f6                     xor esi, esi
0041950a  a1747d5000               mov eax, dword ptr [0x507d74]
0041950f  6689de                   mov si, bx
00419512  8a840600ffffff           mov al, byte ptr [esi + eax - 0x100]
00419519  3a05f95b4900             cmp al, byte ptr [0x495bf9]
0041951f  75d6                     jne 0x4194f7
00419521  81eb00010000             sub ebx, 0x100
00419527  31d2                     xor edx, edx
00419529  6689da                   mov dx, bx
0041952c  89d0                     mov eax, edx
0041952e  c1fa1f                   sar edx, 0x1f
00419531  c1e208                   shl edx, 8
00419534  1bc2                     sbb eax, edx
00419536  c1f808                   sar eax, 8
00419539  89c2                     mov edx, eax
0041953b  ebbc                     jmp 0x4194f9
0041953d  8b35747d5000             mov esi, dword ptr [0x507d74]
00419543  30c9                     xor cl, cl
00419545  84c9                     test cl, cl
00419547  0f8532330000             jne 0x41c87f
0041954d  31c0                     xor eax, eax
0041954f  6689d8                   mov ax, bx
00419552  8a2c06                   mov ch, byte ptr [esi + eax]
00419555  3a2df95b4900             cmp ch, byte ptr [0x495bf9]
0041955b  7558                     jne 0x4195b5
0041955d  8b15380f4e00             mov edx, dword ptr [0x4e0f38]
00419563  01c0                     add eax, eax
00419565  01c2                     add edx, eax
00419567  f6420180                 test byte ptr [edx + 1], 0x80
0041956b  7412                     je 0x41957f
0041956d  668b02                   mov ax, word ptr [edx]
00419570  25e07f0000               and eax, 0x7fe0
00419575  25ffff0000               and eax, 0xffff
0041957a  c1f805                   sar eax, 5
0041957d  eb05                     jmp 0x419584
0041957f  b8ffff0000               mov eax, 0xffff
00419584  31d2                     xor edx, edx
00419586  6689c2                   mov dx, ax
00419589  81faffff0000             cmp edx, 0xffff
0041958f  740c                     je 0x41959d
00419591  69d214010000             imul edx, edx, 0x114
00419597  fe823ea14900             inc byte ptr [edx + 0x49a13e]
0041959d  fec7                     inc bh
0041959f  31d2                     xor edx, edx
004195a1  6689da                   mov dx, bx
004195a4  89d0                     mov eax, edx
004195a6  c1fa1f                   sar edx, 0x1f
004195a9  c1e208                   shl edx, 8
004195ac  1bc2                     sbb eax, edx
004195ae  c1f808                   sar eax, 8
004195b1  89c2                     mov edx, eax
004195b3  eb02                     jmp 0x4195b7
004195b5  b101                     mov cl, 1
004195b7  31c0                     xor eax, eax
004195b9  6689d0                   mov ax, dx
004195bc  3dff000000               cmp eax, 0xff
004195c1  7582                     jne 0x419545
004195c3  b101                     mov cl, 1
004195c5  e97bffffff               jmp 0x419545
