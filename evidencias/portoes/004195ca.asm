; RemonteTouteHerse; SHA-256 do EXE original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004195ca  53                       push ebx
004195cb  51                       push ecx
004195cc  56                       push esi
004195cd  57                       push edi
004195ce  55                       push ebp
004195cf  81ec04020000             sub esp, 0x204
004195d5  89c6                     mov esi, eax
004195d7  89942400020000           mov dword ptr [esp + 0x200], edx
004195de  bfffff0000               mov edi, 0xffff
004195e3  31db                     xor ebx, ebx
004195e5  30c9                     xor cl, cl
004195e7  31c0                     xor eax, eax
004195e9  eb05                     jmp 0x4195f0
004195eb  40                       inc eax
004195ec  66893c54                 mov word ptr [esp + edx*2], di
004195f0  31d2                     xor edx, edx
004195f2  6689c2                   mov dx, ax
004195f5  81faff000000             cmp edx, 0xff
004195fb  7cee                     jl 0x4195eb
004195fd  31ff                     xor edi, edi
004195ff  6689df                   mov di, bx
00419602  6689347c                 mov word ptr [esp + edi*2], si
00419606  89f7                     mov edi, esi
00419608  81e7ffff0000             and edi, 0xffff
0041960e  be00010000               mov esi, 0x100
00419613  89fa                     mov edx, edi
00419615  89f8                     mov eax, edi
00419617  c1fa1f                   sar edx, 0x1f
0041961a  f7fe                     idiv esi
0041961c  89d6                     mov esi, edx
0041961e  89fa                     mov edx, edi
00419620  89f8                     mov eax, edi
00419622  c1fa1f                   sar edx, 0x1f
00419625  c1e208                   shl edx, 8
00419628  1bc2                     sbb eax, edx
0041962a  c1f808                   sar eax, 8
0041962d  31ff                     xor edi, edi
0041962f  668bbc2400020000         mov di, word ptr [esp + 0x200]
00419637  89c2                     mov edx, eax
00419639  89f8                     mov eax, edi
0041963b  c1e004                   shl eax, 4
0041963e  01f8                     add eax, edi
00419640  c1e002                   shl eax, 2
00419643  01f8                     add eax, edi
00419645  c1e002                   shl eax, 2
00419648  05c8a04900               add eax, 0x49a0c8
0041964d  668b407c                 mov ax, word ptr [eax + 0x7c]
00419651  25ffff0000               and eax, 0xffff
00419656  0f94c0                   sete al
00419659  84c0                     test al, al
0041965b  0f845a010000             je 0x4197bb
00419661  8b3d747d5000             mov edi, dword ptr [0x507d74]
00419667  84c9                     test cl, cl
00419669  7555                     jne 0x4196c0
0041966b  31c0                     xor eax, eax
0041966d  6689d8                   mov ax, bx
00419670  01c0                     add eax, eax
00419672  31d2                     xor edx, edx
00419674  668b1404                 mov dx, word ptr [esp + eax]
00419678  8a543aff                 mov dl, byte ptr [edx + edi - 1]
0041967c  3a15f95b4900             cmp dl, byte ptr [0x495bf9]
00419682  752d                     jne 0x4196b1
00419684  668b1404                 mov dx, word ptr [esp + eax]
00419688  43                       inc ebx
00419689  6689540402               mov word ptr [esp + eax + 2], dx
0041968e  31c0                     xor eax, eax
00419690  6689d8                   mov ax, bx
00419693  668b3444                 mov si, word ptr [esp + eax*2]
00419697  31d2                     xor edx, edx
00419699  4e                       dec esi
0041969a  6689f2                   mov dx, si
0041969d  66893444                 mov word ptr [esp + eax*2], si
004196a1  be00010000               mov esi, 0x100
004196a6  89d0                     mov eax, edx
004196a8  c1fa1f                   sar edx, 0x1f
004196ab  f7fe                     idiv esi
004196ad  89d6                     mov esi, edx
004196af  eb02                     jmp 0x4196b3
004196b1  b101                     mov cl, 1
004196b3  31c0                     xor eax, eax
004196b5  6689f0                   mov ax, si
004196b8  85c0                     test eax, eax
004196ba  75ab                     jne 0x419667
004196bc  b101                     mov cl, 1
004196be  eba7                     jmp 0x419667
004196c0  31c0                     xor eax, eax
004196c2  30c9                     xor cl, cl
004196c4  6689d8                   mov ax, bx
004196c7  8a2df95b4900             mov ch, byte ptr [0x495bf9]
004196cd  668b0444                 mov ax, word ptr [esp + eax*2]
004196d1  31db                     xor ebx, ebx
004196d3  66890424                 mov word ptr [esp], ax
004196d7  84c9                     test cl, cl
004196d9  7555                     jne 0x419730
004196db  31c0                     xor eax, eax
004196dd  6689d8                   mov ax, bx
004196e0  01c0                     add eax, eax
004196e2  31d2                     xor edx, edx
004196e4  8b3d747d5000             mov edi, dword ptr [0x507d74]
004196ea  668b1404                 mov dx, word ptr [esp + eax]
004196ee  3a6c3a01                 cmp ch, byte ptr [edx + edi + 1]
004196f2  752d                     jne 0x419721
004196f4  668b1404                 mov dx, word ptr [esp + eax]
004196f8  43                       inc ebx
004196f9  6689540402               mov word ptr [esp + eax + 2], dx
004196fe  31c0                     xor eax, eax
00419700  6689d8                   mov ax, bx
00419703  668b3c44                 mov di, word ptr [esp + eax*2]
00419707  31d2                     xor edx, edx
00419709  47                       inc edi
0041970a  be00010000               mov esi, 0x100
0041970f  6689fa                   mov dx, di
00419712  66893c44                 mov word ptr [esp + eax*2], di
00419716  89d0                     mov eax, edx
00419718  c1fa1f                   sar edx, 0x1f
0041971b  f7fe                     idiv esi
0041971d  89d6                     mov esi, edx
0041971f  eb02                     jmp 0x419723
00419721  b101                     mov cl, 1
00419723  31c0                     xor eax, eax
00419725  6689f0                   mov ax, si
00419728  85c0                     test eax, eax
0041972a  75ab                     jne 0x4196d7
0041972c  b101                     mov cl, 1
0041972e  eba7                     jmp 0x4196d7
00419730  31f6                     xor esi, esi
00419732  eb01                     jmp 0x419735
00419734  46                       inc esi
00419735  31c0                     xor eax, eax
00419737  6689f0                   mov ax, si
0041973a  3dff000000               cmp eax, 0xff
0041973f  7d24                     jge 0x419765
00419741  668b0444                 mov ax, word ptr [esp + eax*2]
00419745  25ffff0000               and eax, 0xffff
0041974a  3dffff0000               cmp eax, 0xffff
0041974f  74e3                     je 0x419734
00419751  ba01000000               mov edx, 1
00419756  e879ca0500               call 0x4761d4
0041975b  84c0                     test al, al
0041975d  0f85a9010000             jne 0x41990c
00419763  ebcf                     jmp 0x419734
00419765  31f6                     xor esi, esi
00419767  eb01                     jmp 0x41976a
00419769  46                       inc esi
0041976a  31c0                     xor eax, eax
0041976c  6689f0                   mov ax, si
0041976f  3de8030000               cmp eax, 0x3e8
00419774  0f8d92010000             jge 0x41990c
0041977a  31db                     xor ebx, ebx
0041977c  eb01                     jmp 0x41977f
0041977e  43                       inc ebx
0041977f  31d2                     xor edx, edx
00419781  6689da                   mov dx, bx
00419784  81faff000000             cmp edx, 0xff
0041978a  7ddd                     jge 0x419769
0041978c  01d2                     add edx, edx
0041978e  31c0                     xor eax, eax
00419790  668b0414                 mov ax, word ptr [esp + edx]
00419794  3dffff0000               cmp eax, 0xffff
00419799  74e3                     je 0x41977e
0041979b  31c0                     xor eax, eax
0041979d  6689f0                   mov ax, si
004197a0  69c014010000             imul eax, eax, 0x114
004197a6  668b88caa04900           mov cx, word ptr [eax + 0x49a0ca]
004197ad  663b0c14                 cmp cx, word ptr [esp + edx]
004197b1  75cb                     jne 0x41977e
004197b3  fe803ea14900             inc byte ptr [eax + 0x49a13e]
004197b9  ebc3                     jmp 0x41977e
004197bb  8b2d747d5000             mov ebp, dword ptr [0x507d74]
004197c1  84c9                     test cl, cl
004197c3  7558                     jne 0x41981d
004197c5  31c0                     xor eax, eax
004197c7  6689d8                   mov ax, bx
004197ca  01c0                     add eax, eax
004197cc  31ff                     xor edi, edi
004197ce  668b3c04                 mov di, word ptr [esp + eax]
004197d2  01ef                     add edi, ebp
004197d4  8aaf00ffffff             mov ch, byte ptr [edi - 0x100]
004197da  3a2df95b4900             cmp ch, byte ptr [0x495bf9]
004197e0  752c                     jne 0x41980e
004197e2  668b1404                 mov dx, word ptr [esp + eax]
004197e6  43                       inc ebx
004197e7  6689540402               mov word ptr [esp + eax + 2], dx
004197ec  31c0                     xor eax, eax
004197ee  6689d8                   mov ax, bx
004197f1  66812c440001             sub word ptr [esp + eax*2], 0x100
004197f7  31d2                     xor edx, edx
004197f9  668b1444                 mov dx, word ptr [esp + eax*2]
004197fd  89d0                     mov eax, edx
004197ff  c1fa1f                   sar edx, 0x1f
00419802  c1e208                   shl edx, 8
00419805  1bc2                     sbb eax, edx
00419807  c1f808                   sar eax, 8
0041980a  89c2                     mov edx, eax
0041980c  eb02                     jmp 0x419810
0041980e  b101                     mov cl, 1
00419810  31c0                     xor eax, eax
00419812  6689f0                   mov ax, si
00419815  85c0                     test eax, eax
00419817  75a8                     jne 0x4197c1
00419819  b101                     mov cl, 1
0041981b  eba4                     jmp 0x4197c1
0041981d  31c0                     xor eax, eax
0041981f  6689d8                   mov ax, bx
00419822  8b3d747d5000             mov edi, dword ptr [0x507d74]
00419828  30c9                     xor cl, cl
0041982a  668b0444                 mov ax, word ptr [esp + eax*2]
0041982e  31db                     xor ebx, ebx
00419830  66890424                 mov word ptr [esp], ax
00419834  84c9                     test cl, cl
00419836  7551                     jne 0x419889
00419838  31c0                     xor eax, eax
0041983a  6689d8                   mov ax, bx
0041983d  01c0                     add eax, eax
0041983f  31f6                     xor esi, esi
00419841  668b3404                 mov si, word ptr [esp + eax]
00419845  8aac3700010000           mov ch, byte ptr [edi + esi + 0x100]
0041984c  3a2df95b4900             cmp ch, byte ptr [0x495bf9]
00419852  7526                     jne 0x41987a
00419854  43                       inc ebx
00419855  6689740402               mov word ptr [esp + eax + 2], si
0041985a  31c0                     xor eax, eax
0041985c  6689d8                   mov ax, bx
0041985f  fe444401                 inc byte ptr [esp + eax*2 + 1]
00419863  31d2                     xor edx, edx
00419865  668b1444                 mov dx, word ptr [esp + eax*2]
00419869  89d0                     mov eax, edx
0041986b  c1fa1f                   sar edx, 0x1f
0041986e  c1e208                   shl edx, 8
00419871  1bc2                     sbb eax, edx
00419873  c1f808                   sar eax, 8
00419876  89c2                     mov edx, eax
00419878  eb02                     jmp 0x41987c
0041987a  b101                     mov cl, 1
0041987c  31c0                     xor eax, eax
0041987e  6689d0                   mov ax, dx
00419881  85c0                     test eax, eax
00419883  75af                     jne 0x419834
00419885  b101                     mov cl, 1
00419887  ebab                     jmp 0x419834
00419889  31f6                     xor esi, esi
0041988b  eb01                     jmp 0x41988e
0041988d  46                       inc esi
0041988e  31c0                     xor eax, eax
00419890  6689f0                   mov ax, si
00419893  3dff000000               cmp eax, 0xff
00419898  7d20                     jge 0x4198ba
0041989a  668b0444                 mov ax, word ptr [esp + eax*2]
0041989e  25ffff0000               and eax, 0xffff
004198a3  3dffff0000               cmp eax, 0xffff
004198a8  74e3                     je 0x41988d
004198aa  ba01000000               mov edx, 1
004198af  e820c90500               call 0x4761d4
004198b4  84c0                     test al, al
004198b6  7554                     jne 0x41990c
004198b8  ebd3                     jmp 0x41988d
004198ba  31f6                     xor esi, esi
004198bc  eb01                     jmp 0x4198bf
004198be  46                       inc esi
004198bf  31c0                     xor eax, eax
004198c1  6689f0                   mov ax, si
004198c4  3de8030000               cmp eax, 0x3e8
004198c9  7d41                     jge 0x41990c
004198cb  31db                     xor ebx, ebx
004198cd  eb01                     jmp 0x4198d0
004198cf  43                       inc ebx
004198d0  31d2                     xor edx, edx
004198d2  6689da                   mov dx, bx
004198d5  81faff000000             cmp edx, 0xff
004198db  7de1                     jge 0x4198be
004198dd  01d2                     add edx, edx
004198df  31c0                     xor eax, eax
004198e1  668b0414                 mov ax, word ptr [esp + edx]
004198e5  3dffff0000               cmp eax, 0xffff
004198ea  74e3                     je 0x4198cf
004198ec  31c0                     xor eax, eax
004198ee  6689f0                   mov ax, si
004198f1  69c014010000             imul eax, eax, 0x114
004198f7  668b88caa04900           mov cx, word ptr [eax + 0x49a0ca]
004198fe  663b0c14                 cmp cx, word ptr [esp + edx]
00419902  75cb                     jne 0x4198cf
00419904  fe803ea14900             inc byte ptr [eax + 0x49a13e]
0041990a  ebc3                     jmp 0x4198cf
0041990c  81c404020000             add esp, 0x204
00419912  e983a00000               jmp 0x42399a
