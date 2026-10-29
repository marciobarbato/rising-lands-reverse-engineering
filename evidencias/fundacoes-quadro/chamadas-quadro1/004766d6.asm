004766d6  81e2ff000000         and edx, 0xff
004766dc  25ffff0000           and eax, 0xffff
004766e1  8b1495787d5000       mov edx, dword ptr [edx*4 + 0x507d78]
004766e8  f6040210             test byte ptr [edx + eax], 0x10
004766ec  0f94c0               sete al
004766ef  c3                   ret 
