0048c541  52                   push edx
0048c542  89c2                 mov edx, eax
0048c544  e8caffffff           call 0x48c513
0048c549  85c0                 test eax, eax
0048c54b  7402                 je 0x48c54f
0048c54d  8910                 mov dword ptr [eax], edx
0048c54f  5a                   pop edx
0048c550  c3                   ret 
