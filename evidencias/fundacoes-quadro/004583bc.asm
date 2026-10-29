004583bc  53                   push ebx
004583bd  51                   push ecx
004583be  52                   push edx
004583bf  81ec00010000         sub esp, 0x100
004583c5  bb00010000           mov ebx, 0x100
004583ca  ba01000000           mov edx, 1
004583cf  89e0                 mov eax, esp
004583d1  e8da3f0300           call 0x48c3b0
004583d6  30e4                 xor ah, ah
004583d8  8825181d4e00         mov byte ptr [0x4e1d18], ah
004583de  30c9                 xor cl, cl
004583e0  e838410300           call 0x48c51d
004583e5  31d2                 xor edx, edx
004583e7  88c2                 mov dl, al
004583e9  3a0c14               cmp cl, byte ptr [esp + edx]
004583ec  7504                 jne 0x4583f2
004583ee  fec0                 inc al
004583f0  ebf3                 jmp 0x4583e5
004583f2  880c14               mov byte ptr [esp + edx], cl
004583f5  31db                 xor ebx, ebx
004583f7  8a15181d4e00         mov dl, byte ptr [0x4e1d18]
004583fd  88d3                 mov bl, dl
004583ff  fec2                 inc dl
00458401  8883181c4e00         mov byte ptr [ebx + 0x4e1c18], al
00458407  8815181d4e00         mov byte ptr [0x4e1d18], dl
0045840d  38d1                 cmp cl, dl
0045840f  75cf                 jne 0x4583e0
00458411  81c400010000         add esp, 0x100
00458417  5a                   pop edx
00458418  59                   pop ecx
00458419  5b                   pop ebx
0045841a  c3                   ret 
