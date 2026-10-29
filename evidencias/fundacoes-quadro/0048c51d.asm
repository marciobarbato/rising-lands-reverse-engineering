0048c51d  52                   push edx
0048c51e  e8f0ffffff           call 0x48c513
0048c523  85c0                 test eax, eax
0048c525  7418                 je 0x48c53f
0048c527  69106d4ec641         imul edx, dword ptr [eax], 0x41c64e6d
0048c52d  81c239300000         add edx, 0x3039
0048c533  8910                 mov dword ptr [eax], edx
0048c535  89d0                 mov eax, edx
0048c537  c1e810               shr eax, 0x10
0048c53a  25ff7f0000           and eax, 0x7fff
0048c53f  5a                   pop edx
0048c540  c3                   ret 
