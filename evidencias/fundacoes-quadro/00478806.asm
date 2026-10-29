00478806  53                   push ebx
00478807  51                   push ecx
00478808  52                   push edx
00478809  56                   push esi
0047880a  803d5299500000       cmp byte ptr [0x509952], 0
00478811  7511                 jne 0x478824
00478813  31c0                 xor eax, eax
00478815  66a1e8734900         mov ax, word ptr [0x4973e8]
0047881b  83f801               cmp eax, 1
0047881e  0f8ed8010000         jle 0x4789fc
00478824  b901000000           mov ecx, 1
00478829  e9e9000000           jmp 0x478917
0047882e  30c0                 xor al, al
00478830  84c0                 test al, al
00478832  0f84de000000         je 0x478916
00478838  b838000000           mov eax, 0x38
0047883d  be0a000000           mov esi, 0xa
00478842  31d2                 xor edx, edx
00478844  e8937cffff           call 0x4704dc
00478849  f7f6                 div esi
0047884b  85d2                 test edx, edx
0047884d  0f85c3000000         jne 0x478916
00478853  668b1de8734900       mov bx, word ptr [0x4973e8]
0047885a  c1e308               shl ebx, 8
0047885d  01cb                 add ebx, ecx
0047885f  a1747d5000           mov eax, dword ptr [0x507d74]
00478864  6689da               mov dx, bx
00478867  89de                 mov esi, ebx
00478869  8a0402               mov al, byte ptr [edx + eax]
0047886c  25ff000000           and eax, 0xff
00478871  83f81d               cmp eax, 0x1d
00478874  7c09                 jl 0x47887f
00478876  83f828               cmp eax, 0x28
00478879  7d04                 jge 0x47887f
0047887b  b001                 mov al, 1
0047887d  eb1e                 jmp 0x47889d
0047887f  31d2                 xor edx, edx
00478881  a1747d5000           mov eax, dword ptr [0x507d74]
00478886  6689f2               mov dx, si
00478889  8a0402               mov al, byte ptr [edx + eax]
0047888c  25ff000000           and eax, 0xff
00478891  83f829               cmp eax, 0x29
00478894  7c05                 jl 0x47889b
00478896  83f834               cmp eax, 0x34
00478899  7ce0                 jl 0x47887b
0047889b  30c0                 xor al, al
0047889d  84c0                 test al, al
0047889f  0f8414010000         je 0x4789b9
004788a5  31d2                 xor edx, edx
004788a7  a1747d5000           mov eax, dword ptr [0x507d74]
004788ac  6689da               mov dx, bx
004788af  8a0402               mov al, byte ptr [edx + eax]
004788b2  25ff000000           and eax, 0xff
004788b7  83f823               cmp eax, 0x23
004788ba  7e05                 jle 0x4788c1
004788bc  83f828               cmp eax, 0x28
004788bf  7c24                 jl 0x4788e5
004788c1  31d2                 xor edx, edx
004788c3  a1747d5000           mov eax, dword ptr [0x507d74]
004788c8  6689da               mov dx, bx
004788cb  8a0402               mov al, byte ptr [edx + eax]
004788ce  25ff000000           and eax, 0xff
004788d3  83f82f               cmp eax, 0x2f
004788d6  0f8ece000000         jle 0x4789aa
004788dc  83f834               cmp eax, 0x34
004788df  0f8dc5000000         jge 0x4789aa
004788e5  b839000000           mov eax, 0x39
004788ea  be05000000           mov esi, 5
004788ef  31d2                 xor edx, edx
004788f1  e8e67bffff           call 0x4704dc
004788f6  f7f6                 div esi
004788f8  85d2                 test edx, edx
004788fa  7510                 jne 0x47890c
004788fc  31c0                 xor eax, eax
004788fe  8b15747d5000         mov edx, dword ptr [0x507d74]
00478904  6689d8               mov ax, bx
00478907  fe0402               inc byte ptr [edx + eax]
0047890a  eb0a                 jmp 0x478916
0047890c  31c0                 xor eax, eax
0047890e  6689d8               mov ax, bx
00478911  e803faffff           call 0x478319
00478916  41                   inc ecx
00478917  31c0                 xor eax, eax
00478919  6689c8               mov ax, cx
0047891c  3dff000000           cmp eax, 0xff
00478921  0f8da6000000         jge 0x4789cd
00478927  31d2                 xor edx, edx
00478929  668b15e8734900       mov dx, word ptr [0x4973e8]
00478930  c1e208               shl edx, 8
00478933  01d0                 add eax, edx
00478935  8b15747d5000         mov edx, dword ptr [0x507d74]
0047893b  8a0402               mov al, byte ptr [edx + eax]
0047893e  25ff000000           and eax, 0xff
00478943  83f81c               cmp eax, 0x1c
00478946  752c                 jne 0x478974
00478948  b837000000           mov eax, 0x37
0047894d  be05000000           mov esi, 5
00478952  31d2                 xor edx, edx
00478954  e8837bffff           call 0x4704dc
00478959  f7f6                 div esi
0047895b  85d2                 test edx, edx
0047895d  7515                 jne 0x478974
0047895f  66a1e8734900         mov ax, word ptr [0x4973e8]
00478965  c1e008               shl eax, 8
00478968  01c8                 add eax, ecx
0047896a  25ffff0000           and eax, 0xffff
0047896f  e8a5f9ffff           call 0x478319
00478974  66a1e8734900         mov ax, word ptr [0x4973e8]
0047897a  c1e008               shl eax, 8
0047897d  31d2                 xor edx, edx
0047897f  01c8                 add eax, ecx
00478981  6689c2               mov dx, ax
00478984  a1747d5000           mov eax, dword ptr [0x507d74]
00478989  8a0402               mov al, byte ptr [edx + eax]
0047898c  25ff000000           and eax, 0xff
00478991  83f81d               cmp eax, 0x1d
00478994  0f8c94feffff         jl 0x47882e
0047899a  83f834               cmp eax, 0x34
0047899d  0f8f8bfeffff         jg 0x47882e
004789a3  b001                 mov al, 1
004789a5  e986feffff           jmp 0x478830
004789aa  31d2                 xor edx, edx
004789ac  a1747d5000           mov eax, dword ptr [0x507d74]
004789b1  6689da               mov dx, bx
004789b4  e94effffff           jmp 0x478907
004789b9  31c0                 xor eax, eax
004789bb  8b15747d5000         mov edx, dword ptr [0x507d74]
004789c1  6689d8               mov ax, bx
004789c4  c6040200             mov byte ptr [edx + eax], 0
004789c8  e944ffffff           jmp 0x478911
004789cd  668b15e8734900       mov dx, word ptr [0x4973e8]
004789d4  31c0                 xor eax, eax
004789d6  42                   inc edx
004789d7  6689d0               mov ax, dx
004789da  668915e8734900       mov word ptr [0x4973e8], dx
004789e1  3dff000000           cmp eax, 0xff
004789e6  7e14                 jle 0x4789fc
004789e8  30d2                 xor dl, dl
004789ea  bb01000000           mov ebx, 1
004789ef  881552995000         mov byte ptr [0x509952], dl
004789f5  66891de8734900       mov word ptr [0x4973e8], bx
004789fc  5e                   pop esi
004789fd  5a                   pop edx
004789fe  59                   pop ecx
004789ff  5b                   pop ebx
00478a00  c3                   ret 
