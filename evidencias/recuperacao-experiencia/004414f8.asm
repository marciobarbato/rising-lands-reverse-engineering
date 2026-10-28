; Engin_StoreExperimente (provenance); original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004414f8  53                       push ebx
004414f9  51                       push ecx
004414fa  52                       push edx
004414fb  56                       push esi
004414fc  57                       push edi
004414fd  83ec04                   sub esp, 4
00441500  31f6                     xor esi, esi
00441502  31c9                     xor ecx, ecx
00441504  eb23                     jmp 0x441529
00441506  31db                     xor ebx, ebx
00441508  6689f3                   mov bx, si
0044150b  6bdb0a                   imul ebx, ebx, 0xa
0044150e  c68443ec194e00ff         mov byte ptr [ebx + eax*2 + 0x4e19ec], 0xff
00441516  42                       inc edx
00441517  888c43ed194e00           mov byte ptr [ebx + eax*2 + 0x4e19ed], cl
0044151e  31c0                     xor eax, eax
00441520  6689d0                   mov ax, dx
00441523  83f805                   cmp eax, 5
00441526  7cde                     jl 0x441506
00441528  46                       inc esi
00441529  31c0                     xor eax, eax
0044152b  6689f0                   mov ax, si
0044152e  83f804                   cmp eax, 4
00441531  7d04                     jge 0x441537
00441533  89ca                     mov edx, ecx
00441535  ebe7                     jmp 0x44151e
00441537  31ff                     xor edi, edi
00441539  e98b000000               jmp 0x4415c9
0044153e  30c0                     xor al, al
00441540  84c0                     test al, al
00441542  0f8480000000             je 0x4415c8
00441548  31c0                     xor eax, eax
0044154a  6689f8                   mov ax, di
0044154d  69c014010000             imul eax, eax, 0x114
00441553  8b1da0194e00             mov ebx, dword ptr [0x4e19a0]
00441559  01c3                     add ebx, eax
0044155b  31c9                     xor ecx, ecx
0044155d  8a0b                     mov cl, byte ptr [ebx]
0044155f  6bc90a                   imul ecx, ecx, 0xa
00441562  30e4                     xor ah, ah
00441564  ba01000000               mov edx, 1
00441569  882424                   mov byte ptr [esp], ah
0044156c  8a89ed194e00             mov cl, byte ptr [ecx + 0x4e19ed]
00441572  eb01                     jmp 0x441575
00441574  42                       inc edx
00441575  31c0                     xor eax, eax
00441577  6689d0                   mov ax, dx
0044157a  83f805                   cmp eax, 5
0044157d  7d1b                     jge 0x44159a
0044157f  0fb633                   movzx esi, byte ptr [ebx]
00441582  6bf60a                   imul esi, esi, 0xa
00441585  01c0                     add eax, eax
00441587  01f0                     add eax, esi
00441589  8aa8ed194e00             mov ch, byte ptr [eax + 0x4e19ed]
0044158f  38e9                     cmp cl, ch
00441591  76e1                     jbe 0x441574
00441593  88e9                     mov cl, ch
00441595  881424                   mov byte ptr [esp], dl
00441598  ebda                     jmp 0x441574
0044159a  8a93af000000             mov dl, byte ptr [ebx + 0xaf]
004415a0  38d1                     cmp cl, dl
004415a2  7324                     jae 0x4415c8
004415a4  31c0                     xor eax, eax
004415a6  8a03                     mov al, byte ptr [ebx]
004415a8  6bc80a                   imul ecx, eax, 0xa
004415ab  31c0                     xor eax, eax
004415ad  8a0424                   mov al, byte ptr [esp]
004415b0  889441ed194e00           mov byte ptr [ecx + eax*2 + 0x4e19ed], dl
004415b7  31c9                     xor ecx, ecx
004415b9  8a0b                     mov cl, byte ptr [ebx]
004415bb  6bc90a                   imul ecx, ecx, 0xa
004415be  8a5301                   mov dl, byte ptr [ebx + 1]
004415c1  889441ec194e00           mov byte ptr [ecx + eax*2 + 0x4e19ec], dl
004415c8  47                       inc edi
004415c9  31c0                     xor eax, eax
004415cb  6689f8                   mov ax, di
004415ce  3d20030000               cmp eax, 0x320
004415d3  0f8d7cf7ffff             jge 0x440d55
004415d9  69d814010000             imul ebx, eax, 0x114
004415df  a1a0194e00               mov eax, dword ptr [0x4e19a0]
004415e4  8a440302                 mov al, byte ptr [ebx + eax + 2]
004415e8  25ff000000               and eax, 0xff
004415ed  0f95c0                   setne al
004415f0  84c0                     test al, al
004415f2  74d4                     je 0x4415c8
004415f4  31c0                     xor eax, eax
004415f6  6689f8                   mov ax, di
004415f9  69d814010000             imul ebx, eax, 0x114
004415ff  a1a0194e00               mov eax, dword ptr [0x4e19a0]
00441604  8a440302                 mov al, byte ptr [ebx + eax + 2]
00441608  25ff000000               and eax, 0xff
0044160d  0f842bffffff             je 0x44153e
00441613  83f804                   cmp eax, 4
00441616  0f8422ffffff             je 0x44153e
0044161c  b001                     mov al, 1
0044161e  e91dffffff               jmp 0x441540
