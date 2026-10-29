00419c3f  b201                 mov dl, 1
00419c41  88d0                 mov al, dl
00419c43  83c418               add esp, 0x18
00419c46  5f                   pop edi
00419c47  5e                   pop esi
00419c48  59                   pop ecx
00419c49  5b                   pop ebx
00419c4a  c3                   ret 
00419c4b  30d2                 xor dl, dl
00419c4d  ebf2                 jmp 0x419c41
