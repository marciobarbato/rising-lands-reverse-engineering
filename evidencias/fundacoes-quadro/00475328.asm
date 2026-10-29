00475328  53                   push ebx
00475329  52                   push edx
0047532a  a17c8f5000           mov eax, dword ptr [0x508f7c]
0047532f  31db                 xor ebx, ebx
00475331  31d2                 xor edx, edx
00475333  668b1dea734900       mov bx, word ptr [0x4973ea]
0047533a  f7f3                 div ebx
0047533c  85d2                 test edx, edx
0047533e  7507                 jne 0x475347
00475340  c6055299500001       mov byte ptr [0x509952], 1
00475347  5a                   pop edx
00475348  5b                   pop ebx
00475349  c3                   ret 
