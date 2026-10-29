00477700  53                   push ebx
00477701  51                   push ecx
00477702  56                   push esi
00477703  57                   push edi
00477704  55                   push ebp
00477705  83ec08               sub esp, 8
00477708  c1e208               shl edx, 8
0047770b  89c3                 mov ebx, eax
0047770d  01d3                 add ebx, edx
0047770f  31d2                 xor edx, edx
00477711  891424               mov dword ptr [esp], edx
00477714  bd95000000           mov ebp, 0x95
00477719  eb0c                 jmp 0x477727
0047771b  ba00010000           mov edx, 0x100
00477720  29fa                 sub edx, edi
00477722  01d3                 add ebx, edx
00477724  ff0424               inc dword ptr [esp]
00477727  8b0424               mov eax, dword ptr [esp]
0047772a  663b0526875000       cmp ax, word ptr [0x508726]
00477731  0f83bbfdffff         jae 0x4774f2
00477737  31f6                 xor esi, esi
00477739  e959010000           jmp 0x477897
0047773e  81f995000000         cmp ecx, 0x95
00477744  0f8c76000000         jl 0x4777c0
0047774a  81f99c000000         cmp ecx, 0x9c
00477750  7f6e                 jg 0x4777c0
00477752  f6057c8f500001       test byte ptr [0x508f7c], 1
00477759  7565                 jne 0x4777c0
0047775b  41                   inc ecx
0047775c  66890a               mov word ptr [edx], cx
0047775f  8b0d707d5000         mov ecx, dword ptr [0x507d70]
00477765  01f9                 add ecx, edi
00477767  31d2                 xor edx, edx
00477769  668b11               mov dx, word ptr [ecx]
0047776c  81fa9d000000         cmp edx, 0x9d
00477772  0f851d010000         jne 0x477895
00477778  a0181d4e00           mov al, byte ptr [0x4e1d18]
0047777d  31d2                 xor edx, edx
0047777f  88c2                 mov dl, al
00477781  88442404             mov byte ptr [esp + 4], al
00477785  8a92181c4e00         mov dl, byte ptr [edx + 0x4e1c18]
0047778b  81e2ff000000         and edx, 0xff
00477791  bf02000000           mov edi, 2
00477796  89d0                 mov eax, edx
00477798  c1fa1f               sar edx, 0x1f
0047779b  f7ff                 idiv edi
0047779d  8a442404             mov al, byte ptr [esp + 4]
004777a1  fec0                 inc al
004777a3  a2181d4e00           mov byte ptr [0x4e1d18], al
004777a8  85d2                 test edx, edx
004777aa  750a                 jne 0x4777b6
004777ac  66c7015d00           mov word ptr [ecx], 0x5d
004777b1  e9df000000           jmp 0x477895
004777b6  66c7019400           mov word ptr [ecx], 0x94
004777bb  e9d5000000           jmp 0x477895
004777c0  31c9                 xor ecx, ecx
004777c2  6689d9               mov cx, bx
004777c5  8b15707d5000         mov edx, dword ptr [0x507d70]
004777cb  01c9                 add ecx, ecx
004777cd  668b1411             mov dx, word ptr [ecx + edx]
004777d1  81e2ffff0000         and edx, 0xffff
004777d7  81fa51020000         cmp edx, 0x251
004777dd  7408                 je 0x4777e7
004777df  81fa52020000         cmp edx, 0x252
004777e5  7525                 jne 0x47780c
004777e7  31d2                 xor edx, edx
004777e9  8b0dac7d5000         mov ecx, dword ptr [0x507dac]
004777ef  6689da               mov dx, bx
004777f2  803c1100             cmp byte ptr [ecx + edx], 0
004777f6  0f8499000000         je 0x477895
004777fc  8b0d707d5000         mov ecx, dword ptr [0x507d70]
00477802  6683045104           add word ptr [ecx + edx*2], 4
00477807  e989000000           jmp 0x477895
0047780c  81fa55020000         cmp edx, 0x255
00477812  7408                 je 0x47781c
00477814  81fa56020000         cmp edx, 0x256
0047781a  7512                 jne 0x47782e
0047781c  31d2                 xor edx, edx
0047781e  8b0d707d5000         mov ecx, dword ptr [0x507d70]
00477824  6689da               mov dx, bx
00477827  66832c5104           sub word ptr [ecx + edx*2], 4
0047782c  eb67                 jmp 0x477895
0047782e  e8e80bfeff           call 0x45841b
00477833  89c2                 mov edx, eax
00477835  bf00040000           mov edi, 0x400
0047783a  c1fa1f               sar edx, 0x1f
0047783d  f7ff                 idiv edi
0047783f  85d2                 test edx, edx
00477841  7552                 jne 0x477895
00477843  8b15707d5000         mov edx, dword ptr [0x507d70]
00477849  01d1                 add ecx, edx
0047784b  31d2                 xor edx, edx
0047784d  668b11               mov dx, word ptr [ecx]
00477850  81fa8b000000         cmp edx, 0x8b
00477856  7c08                 jl 0x477860
00477858  81fa93000000         cmp edx, 0x93
0047785e  7c1d                 jl 0x47787d
00477860  31d2                 xor edx, edx
00477862  6689da               mov dx, bx
00477865  8d0c12               lea ecx, [edx + edx]
00477868  8b15707d5000         mov edx, dword ptr [0x507d70]
0047786e  668b1411             mov dx, word ptr [ecx + edx]
00477872  81e2ffff0000         and edx, 0xffff
00477878  83fa6d               cmp edx, 0x6d
0047787b  7518                 jne 0x477895
0047787d  31c9                 xor ecx, ecx
0047787f  8b15747d5000         mov edx, dword ptr [0x507d74]
00477885  6689d9               mov cx, bx
00477888  01ca                 add edx, ecx
0047788a  31c9                 xor ecx, ecx
0047788c  8a0a                 mov cl, byte ptr [edx]
0047788e  85c9                 test ecx, ecx
00477890  7503                 jne 0x477895
00477892  c6021b               mov byte ptr [edx], 0x1b
00477895  43                   inc ebx
00477896  46                   inc esi
00477897  668b3d24875000       mov di, word ptr [0x508724]
0047789e  6639fe               cmp si, di
004778a1  0f8374feffff         jae 0x47771b
004778a7  31ff                 xor edi, edi
004778a9  6689df               mov di, bx
004778ac  8b15707d5000         mov edx, dword ptr [0x507d70]
004778b2  01ff                 add edi, edi
004778b4  01fa                 add edx, edi
004778b6  31c9                 xor ecx, ecx
004778b8  668b0a               mov cx, word ptr [edx]
004778bb  83f95d               cmp ecx, 0x5d
004778be  740c                 je 0x4778cc
004778c0  81f994000000         cmp ecx, 0x94
004778c6  0f8572feffff         jne 0x47773e
004778cc  8a0d181d4e00         mov cl, byte ptr [0x4e1d18]
004778d2  31d2                 xor edx, edx
004778d4  88ca                 mov dl, cl
004778d6  8a92181c4e00         mov dl, byte ptr [edx + 0x4e1c18]
004778dc  81e2ff000000         and edx, 0xff
004778e2  bf40000000           mov edi, 0x40
004778e7  89d0                 mov eax, edx
004778e9  c1fa1f               sar edx, 0x1f
004778ec  f7ff                 idiv edi
004778ee  fec1                 inc cl
004778f0  880d181d4e00         mov byte ptr [0x4e1d18], cl
004778f6  85d2                 test edx, edx
004778f8  759b                 jne 0x477895
004778fa  31c9                 xor ecx, ecx
004778fc  8b15707d5000         mov edx, dword ptr [0x507d70]
00477902  6689d9               mov cx, bx
00477905  66c7044a9500         mov word ptr [edx + ecx*2], 0x95
0047790b  eb88                 jmp 0x477895
