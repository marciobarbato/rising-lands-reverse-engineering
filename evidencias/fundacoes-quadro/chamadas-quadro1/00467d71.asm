00467d71  51                   push ecx
00467d72  84db                 test bl, bl
00467d74  7607                 jbe 0x467d7d
00467d76  80fb01               cmp bl, 1
00467d79  7412                 je 0x467d8d
00467d7b  59                   pop ecx
00467d7c  c3                   ret 
00467d7d  88d1                 mov cl, dl
00467d7f  b201                 mov dl, 1
00467d81  d2e2                 shl dl, cl
00467d83  8a18                 mov bl, byte ptr [eax]
00467d85  f6d2                 not dl
00467d87  20d3                 and bl, dl
00467d89  8818                 mov byte ptr [eax], bl
00467d8b  59                   pop ecx
00467d8c  c3                   ret 
00467d8d  88d1                 mov cl, dl
00467d8f  88da                 mov dl, bl
00467d91  d2e2                 shl dl, cl
00467d93  0810                 or byte ptr [eax], dl
00467d95  59                   pop ecx
00467d96  c3                   ret 
