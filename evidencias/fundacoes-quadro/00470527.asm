00470527  53                   push ebx
00470528  52                   push edx
00470529  85c0                 test eax, eax
0047052b  750d                 jne 0x47053a
0047052d  c7056471490001000000 mov dword ptr [0x497164], 1
00470537  5a                   pop edx
00470538  5b                   pop ebx
00470539  c3                   ret 
0047053a  bbffffff7f           mov ebx, 0x7fffffff
0047053f  31d2                 xor edx, edx
00470541  f7f3                 div ebx
00470543  891564714900         mov dword ptr [0x497164], edx
00470549  5a                   pop edx
0047054a  5b                   pop ebx
0047054b  c3                   ret 
