00475014  ff057c8f5000         inc dword ptr [0x508f7c]
0047501a  f6057c8f500001       test byte ptr [0x508f7c], 1
00475021  7506                 jne 0x475029
00475023  ff05808f5000         inc dword ptr [0x508f80]
00475029  bb03000000           mov ebx, 3
0047502e  a17c8f5000           mov eax, dword ptr [0x508f7c]
00475033  31d2                 xor edx, edx
00475035  f7f3                 div ebx
00475037  85d2                 test edx, edx
00475039  7506                 jne 0x475041
0047503b  ff05848f5000         inc dword ptr [0x508f84]
