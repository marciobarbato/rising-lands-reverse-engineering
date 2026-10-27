; RotateEngin [0x448599, 0x448704)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00448599  53                     push     ebx
0044859a  51                     push     ecx
0044859b  52                     push     edx
0044859c  31d2                   xor      edx, edx
0044859e  6689c2                 mov      dx, ax
004485a1  89d3                   mov      ebx, edx
004485a3  c1e304                 shl      ebx, 4
004485a6  01d3                   add      ebx, edx
004485a8  c1e302                 shl      ebx, 2
004485ab  01d3                   add      ebx, edx
004485ad  8b15a0194e00           mov      edx, dword ptr [0x4e19a0]
004485b3  c1e302                 shl      ebx, 2
004485b6  01d3                   add      ebx, edx
004485b8  8a5301                 mov      dl, byte ptr [ebx + 1]
004485bb  80fa0c                 cmp      dl, 0xc
004485be  720f                   jb       0x4485cf
004485c0  0f86a6000000           jbe      0x44866c
004485c6  80fa0f                 cmp      dl, 0xf
004485c9  0f849d000000           je       0x44866c
004485cf  30c0                   xor      al, al
004485d1  84c0                   test     al, al
004485d3  7412                   je       0x4485e7
004485d5  8a8390000000           mov      al, byte ptr [ebx + 0x90]
004485db  fec8                   dec      al
004485dd  00c0                   add      al, al
004485df  fec0                   inc      al
004485e1  8883da000000           mov      byte ptr [ebx + 0xda], al
004485e7  8a8390000000           mov      al, byte ptr [ebx + 0x90]
004485ed  3a8391000000           cmp      al, byte ptr [ebx + 0x91]
004485f3  0f849c000000           je       0x448695
004485f9  8a9392000000           mov      dl, byte ptr [ebx + 0x92]
004485ff  fec2                   inc      dl
00448601  889392000000           mov      byte ptr [ebx + 0x92], dl
00448607  3a9393000000           cmp      dl, byte ptr [ebx + 0x93]
0044860d  0f8582000000           jne      0x448695
00448613  8a8390000000           mov      al, byte ptr [ebx + 0x90]
00448619  3a8391000000           cmp      al, byte ptr [ebx + 0x91]
0044861f  7613                   jbe      0x448634
00448621  31c9                   xor      ecx, ecx
00448623  31d2                   xor      edx, edx
00448625  88c1                   mov      cl, al
00448627  8a9391000000           mov      dl, byte ptr [ebx + 0x91]
0044862d  29d1                   sub      ecx, edx
0044862f  83f908                 cmp      ecx, 8
00448632  7c21                   jl       0x448655
00448634  8a8391000000           mov      al, byte ptr [ebx + 0x91]
0044863a  3a8390000000           cmp      al, byte ptr [ebx + 0x90]
00448640  7631                   jbe      0x448673
00448642  31c9                   xor      ecx, ecx
00448644  31d2                   xor      edx, edx
00448646  88c1                   mov      cl, al
00448648  8a9390000000           mov      dl, byte ptr [ebx + 0x90]
0044864e  29d1                   sub      ecx, edx
00448650  83f908                 cmp      ecx, 8
00448653  7e1e                   jle      0x448673
00448655  31d2                   xor      edx, edx
00448657  8a9391000000           mov      dl, byte ptr [ebx + 0x91]
0044865d  b910000000             mov      ecx, 0x10
00448662  89d0                   mov      eax, edx
00448664  c1fa1f                 sar      edx, 0x1f
00448667  f7f9                   idiv     ecx
00448669  42                     inc      edx
0044866a  eb1c                   jmp      0x448688 ; 
0044866c  b001                   mov      al, 1
0044866e  e95effffff             jmp      0x4485d1 ; 
00448673  31d2                   xor      edx, edx
00448675  8a9391000000           mov      dl, byte ptr [ebx + 0x91]
0044867b  83fa01                 cmp      edx, 1
0044867e  7403                   je       0x448683
00448680  4a                     dec      edx
00448681  eb05                   jmp      0x448688 ; 
00448683  ba10000000             mov      edx, 0x10
00448688  889391000000           mov      byte ptr [ebx + 0x91], dl
0044868e  c6839200000000         mov      byte ptr [ebx + 0x92], 0
00448695  5a                     pop      edx
00448696  59                     pop      ecx
00448697  5b                     pop      ebx
00448698  c3                     ret      
00448699  8d4000                 lea      eax, [eax]
0044869c  f8                     clc      
0044869d  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486a1  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486a5  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486a9  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486ad  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486b1  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486b5  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486b9  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486bd  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486c1  8a4400f8               mov      al, byte ptr [eax + eax - 8]
004486c5  8a440027               mov      al, byte ptr [eax + eax + 0x27]
004486c9  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486cd  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486d1  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486d5  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486d9  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486dd  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486e1  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486e5  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486e9  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486ed  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486f1  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486f5  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486f9  8b440027               mov      eax, dword ptr [eax + eax + 0x27]
004486fd  8b4400f8               mov      eax, dword ptr [eax + eax - 8]
