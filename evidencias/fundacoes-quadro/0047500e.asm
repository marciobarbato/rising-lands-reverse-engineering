0047500e  53                   push ebx
0047500f  51                   push ecx
00475010  52                   push edx
00475011  83ec08               sub esp, 8
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
00475041  89e2                 mov edx, esp
00475043  52                   push edx
00475044  2eff1594325200       call dword ptr cs:[0x523294]
0047504b  8b0424               mov eax, dword ptr [esp]
0047504e  66a3a8995000         mov word ptr [0x5099a8], ax
00475054  8b442404             mov eax, dword ptr [esp + 4]
00475058  66a3aa995000         mov word ptr [0x5099aa], ax
0047505e  e80578fbff           call 0x42c868
00475063  e83026faff           call 0x417698
00475068  803daf99500000       cmp byte ptr [0x5099af], 0
0047506f  740e                 je 0x47507f
00475071  30f6                 xor dh, dh
00475073  8835af995000         mov byte ptr [0x5099af], dh
00475079  8835ae995000         mov byte ptr [0x5099ae], dh
0047507f  803db299500000       cmp byte ptr [0x5099b2], 0
00475086  740e                 je 0x475096
00475088  30c9                 xor cl, cl
0047508a  880db1995000         mov byte ptr [0x5099b1], cl
00475090  880db2995000         mov byte ptr [0x5099b2], cl
00475096  83c408               add esp, 8
00475099  5a                   pop edx
0047509a  59                   pop ecx
0047509b  5b                   pop ebx
0047509c  c3                   ret 
