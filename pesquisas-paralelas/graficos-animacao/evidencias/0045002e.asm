; EnginEstTerreur [0x45002e, 0x450054)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0045002e  52                     push     edx
0045002f  31d2                   xor      edx, edx
00450031  6689c2                 mov      dx, ax
00450034  89d0                   mov      eax, edx
00450036  c1e004                 shl      eax, 4
00450039  01d0                   add      eax, edx
0045003b  c1e002                 shl      eax, 2
0045003e  01d0                   add      eax, edx
00450040  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
00450046  8a8482dc000000         mov      al, byte ptr [edx + eax*4 + 0xdc]
0045004d  ba01000000             mov      edx, 1
00450052  ebce                   jmp      0x450022 ;
