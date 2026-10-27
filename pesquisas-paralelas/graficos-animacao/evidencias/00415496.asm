; EnginGetSpriteMort [0x415496, 0x41559a)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00415496  52                     push     edx
00415497  88c4                   mov      ah, al
00415499  bab2080000             mov      edx, 0x8b2
0041549e  3c08                   cmp      al, 8
004154a0  0f82ba000000           jb       0x415560
004154a6  762c                   jbe      0x4154d4
004154a8  3c15                   cmp      al, 0x15
004154aa  0f82a2000000           jb       0x415552
004154b0  0f868a000000           jbe      0x415540
004154b6  3c17                   cmp      al, 0x17
004154b8  0f828b000000           jb       0x415549
004154be  0f8661000000           jbe      0x415525
004154c4  3c18                   cmp      al, 0x18
004154c6  0f8662000000           jbe      0x41552e
004154cc  3c19                   cmp      al, 0x19
004154ce  7443                   je       0x415513
004154d0  89d0                   mov      eax, edx
004154d2  5a                     pop      edx
004154d3  c3                     ret      
004154d4  ba320a0000             mov      edx, 0xa32
004154d9  89d0                   mov      eax, edx
004154db  5a                     pop      edx
004154dc  c3                     ret      
004154dd  ba220c0000             mov      edx, 0xc22
004154e2  89d0                   mov      eax, edx
004154e4  5a                     pop      edx
004154e5  c3                     ret      
004154e6  bae2060000             mov      edx, 0x6e2
004154eb  89d0                   mov      eax, edx
004154ed  5a                     pop      edx
004154ee  c3                     ret      
004154ef  ba62070000             mov      edx, 0x762
004154f4  89d0                   mov      eax, edx
004154f6  5a                     pop      edx
004154f7  c3                     ret      
004154f8  bae2070000             mov      edx, 0x7e2
004154fd  89d0                   mov      eax, edx
004154ff  5a                     pop      edx
00415500  c3                     ret      
00415501  ba52090000             mov      edx, 0x952
00415506  89d0                   mov      eax, edx
00415508  5a                     pop      edx
00415509  c3                     ret      
0041550a  bae20d0000             mov      edx, 0xde2
0041550f  89d0                   mov      eax, edx
00415511  5a                     pop      edx
00415512  c3                     ret      
00415513  ba620f0000             mov      edx, 0xf62
00415518  89d0                   mov      eax, edx
0041551a  5a                     pop      edx
0041551b  c3                     ret      
0041551c  ba020b0000             mov      edx, 0xb02
00415521  89d0                   mov      eax, edx
00415523  5a                     pop      edx
00415524  c3                     ret      
00415525  baf5180000             mov      edx, 0x18f5
0041552a  89d0                   mov      eax, edx
0041552c  5a                     pop      edx
0041552d  c3                     ret      
0041552e  ba751a0000             mov      edx, 0x1a75
00415533  89d0                   mov      eax, edx
00415535  5a                     pop      edx
00415536  c3                     ret      
00415537  baf5150000             mov      edx, 0x15f5
0041553c  89d0                   mov      eax, edx
0041553e  5a                     pop      edx
0041553f  c3                     ret      
00415540  ba75140000             mov      edx, 0x1475
00415545  89d0                   mov      eax, edx
00415547  5a                     pop      edx
00415548  c3                     ret      
00415549  ba75170000             mov      edx, 0x1775
0041554e  89d0                   mov      eax, edx
00415550  5a                     pop      edx
00415551  c3                     ret      
00415552  3c0a                   cmp      al, 0xa
00415554  7299                   jb       0x4154ef
00415556  76a0                   jbe      0x4154f8
00415558  3c14                   cmp      al, 0x14
0041555a  74db                   je       0x415537
0041555c  89d0                   mov      eax, edx
0041555e  5a                     pop      edx
0041555f  c3                     ret      
00415560  3c03                   cmp      al, 3
00415562  721d                   jb       0x415581
00415564  76a4                   jbe      0x41550a
00415566  3c05                   cmp      al, 5
00415568  72b2                   jb       0x41551c
0041556a  0f8676ffffff           jbe      0x4154e6
00415570  3c06                   cmp      al, 6
00415572  0f8665ffffff           jbe      0x4154dd
00415578  ba02060000             mov      edx, 0x602
0041557d  89d0                   mov      eax, edx
0041557f  5a                     pop      edx
00415580  c3                     ret      
00415581  3c01                   cmp      al, 1
00415583  720f                   jb       0x415594
00415585  0f8676ffffff           jbe      0x415501
0041558b  ba120d0000             mov      edx, 0xd12
00415590  89d0                   mov      eax, edx
00415592  5a                     pop      edx
00415593  c3                     ret      
00415594  84c0                   test     al, al
00415596  89d0                   mov      eax, edx
00415598  5a                     pop      edx
00415599  c3                     ret      
