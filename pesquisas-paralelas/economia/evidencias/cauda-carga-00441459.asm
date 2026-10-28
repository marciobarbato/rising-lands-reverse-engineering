; EnginInitTechnologie: EnginSetTechnologie for DL owners 0..3; exclusive end 0x00441470.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00441459  52                       push     edx
0044145a  30d2                     xor      dl, dl
0044145c  eb07                     jmp      0x441465
0044145e  e87efdffff               call     0x4411e1
00441463  fec2                     inc      dl
00441465  31c0                     xor      eax, eax
00441467  88d0                     mov      al, dl
00441469  83f804                   cmp      eax, 4
0044146c  7cf0                     jl       0x44145e
0044146e  5a                       pop      edx
0044146f  c3                       ret
