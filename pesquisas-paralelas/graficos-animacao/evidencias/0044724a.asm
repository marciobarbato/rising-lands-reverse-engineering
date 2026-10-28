; BagContientTroupe [0x44724a, 0x4472d3)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0044724a  53                     push     ebx
0044724b  51                     push     ecx
0044724c  52                     push     edx
0044724d  89c2                   mov      edx, eax
0044724f  31db                   xor      ebx, ebx
00447251  eb01                   jmp      0x447254 ;
00447253  43                     inc      ebx
00447254  663b5a02               cmp      bx, word ptr [edx + 2]
00447258  0f836f000000           jae      0x4472cd
0044725e  31c9                   xor      ecx, ecx
00447260  6689d9                 mov      cx, bx
00447263  8a441142               mov      al, byte ptr [ecx + edx + 0x42]
00447267  25ff000000             and      eax, 0xff
0044726c  83f801                 cmp      eax, 1
0044726f  7402                   je       0x447273
00447271  ebe0                   jmp      0x447253 ;
00447273  89c8                   mov      eax, ecx
00447275  668b444206             mov      ax, word ptr [edx + eax*2 + 6]
0044727a  25ffff0000             and      eax, 0xffff
0044727f  69c014010000           imul     eax, eax, 0x114
00447285  8b0da0194e00           mov      ecx, dword ptr [0x4e19a0]
0044728b  8a440101               mov      al, byte ptr [ecx + eax + 1]
0044728f  b401                   mov      ah, 1
00447291  3c0e                   cmp      al, 0xe
00447293  7216                   jb       0x4472ab
00447295  7620                   jbe      0x4472b7
00447297  3c12                   cmp      al, 0x12
00447299  721c                   jb       0x4472b7
0044729b  7624                   jbe      0x4472c1
0044729d  3c17                   cmp      al, 0x17
0044729f  7220                   jb       0x4472c1
004472a1  3c18                   cmp      al, 0x18
004472a3  761c                   jbe      0x4472c1
004472a5  3c19                   cmp      al, 0x19
004472a7  740e                   je       0x4472b7
004472a9  eb18                   jmp      0x4472c3 ;
004472ab  3c06                   cmp      al, 6
004472ad  720c                   jb       0x4472bb
004472af  3c08                   cmp      al, 8
004472b1  760e                   jbe      0x4472c1
004472b3  3c0b                   cmp      al, 0xb
004472b5  720a                   jb       0x4472c1
004472b7  30e4                   xor      ah, ah
004472b9  eb08                   jmp      0x4472c3 ;
004472bb  3c03                   cmp      al, 3
004472bd  7202                   jb       0x4472c1
004472bf  76f6                   jbe      0x4472b7
004472c1  b401                   mov      ah, 1
004472c3  84e4                   test     ah, ah
004472c5  748c                   je       0x447253
004472c7  b001                   mov      al, 1
004472c9  5a                     pop      edx
004472ca  59                     pop      ecx
004472cb  5b                     pop      ebx
004472cc  c3                     ret
004472cd  30c0                   xor      al, al
004472cf  5a                     pop      edx
004472d0  59                     pop      ecx
004472d1  5b                     pop      ebx
004472d2  c3                     ret
