00467d97  51                   push ecx
00467d98  25ff000000           and eax, 0xff
00467d9d  88d1                 mov cl, dl
00467d9f  d3f8                 sar eax, cl
00467da1  83e001               and eax, 1
00467da4  59                   pop ecx
00467da5  c3                   ret 
