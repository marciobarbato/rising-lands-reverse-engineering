0047622e  53                   push ebx
0047622f  31db                 xor ebx, ebx
00476231  6689c3               mov bx, ax
00476234  a1a87d5000           mov eax, dword ptr [0x507da8]
00476239  081403               or byte ptr [ebx + eax], dl
0047623c  5b                   pop ebx
0047623d  c3                   ret 
