; BallonInit; original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441b6c  53                       push ebx
00441b6d  51                       push ecx
00441b6e  52                       push edx
00441b6f  b9ffff0000               mov ecx, 0xffff
00441b74  30d2                     xor dl, dl
00441b76  eb25                     jmp 0x441b9d
00441b78  66890cc5181a4e00         mov word ptr [eax*8 + 0x4e1a18], cx
00441b80  31db                     xor ebx, ebx
00441b82  66890cc51a1a4e00         mov word ptr [eax*8 + 0x4e1a1a], cx
00441b8a  30f6                     xor dh, dh
00441b8c  66891cc5141a4e00         mov word ptr [eax*8 + 0x4e1a14], bx
00441b94  8834c5161a4e00           mov byte ptr [eax*8 + 0x4e1a16], dh
00441b9b  fec2                     inc dl
00441b9d  31c0                     xor eax, eax
00441b9f  88d0                     mov al, dl
00441ba1  83f804                   cmp eax, 4
00441ba4  7cd2                     jl 0x441b78
00441ba6  5a                       pop edx
00441ba7  59                       pop ecx
00441ba8  5b                       pop ebx
00441ba9  c3                       ret
