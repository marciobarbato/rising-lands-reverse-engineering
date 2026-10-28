; ProgIteration [0x47500e, 0x475118)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0047500e  53                     push     ebx
0047500f  51                     push     ecx
00475010  52                     push     edx
00475011  83ec08                 sub      esp, 8
00475014  ff057c8f5000           inc      dword ptr [0x508f7c]
0047501a  f6057c8f500001         test     byte ptr [0x508f7c], 1
00475021  7506                   jne      0x475029
00475023  ff05808f5000           inc      dword ptr [0x508f80]
00475029  bb03000000             mov      ebx, 3
0047502e  a17c8f5000             mov      eax, dword ptr [0x508f7c]
00475033  31d2                   xor      edx, edx
00475035  f7f3                   div      ebx
00475037  85d2                   test     edx, edx
00475039  7506                   jne      0x475041
0047503b  ff05848f5000           inc      dword ptr [0x508f84]
00475041  89e2                   mov      edx, esp
00475043  52                     push     edx
00475044  2eff1594325200         call     dword ptr cs:[0x523294]
0047504b  8b0424                 mov      eax, dword ptr [esp]
0047504e  66a3a8995000           mov      word ptr [0x5099a8], ax
00475054  8b442404               mov      eax, dword ptr [esp + 4]
00475058  66a3aa995000           mov      word ptr [0x5099aa], ax
0047505e  e80578fbff             call     0x42c868 ; CalculGame
00475063  e83026faff             call     0x417698 ; AffGame
00475068  803daf99500000         cmp      byte ptr [0x5099af], 0
0047506f  740e                   je       0x47507f
00475071  30f6                   xor      dh, dh
00475073  8835af995000           mov      byte ptr [0x5099af], dh
00475079  8835ae995000           mov      byte ptr [0x5099ae], dh
0047507f  803db299500000         cmp      byte ptr [0x5099b2], 0
00475086  740e                   je       0x475096
00475088  30c9                   xor      cl, cl
0047508a  880db1995000           mov      byte ptr [0x5099b1], cl
00475090  880db2995000           mov      byte ptr [0x5099b2], cl
00475096  83c408                 add      esp, 8
00475099  5a                     pop      edx
0047509a  59                     pop      ecx
0047509b  5b                     pop      ebx
0047509c  c3                     ret
0047509d  51                     push     ecx
0047509e  52                     push     edx
0047509f  56                     push     esi
004750a0  57                     push     edi
004750a1  81ec00010000           sub      esp, 0x100
004750a7  be94945000             mov      esi, 0x509494
004750ac  a1b0244e00             mov      eax, dword ptr [0x4e24b0]
004750b1  89e7                   mov      edi, esp
004750b3  e8799dfcff             call     0x43ee31 ; DDSetPalette
004750b8  e8f7a2fcff             call     0x43f3b4 ; DDLockSurface
004750bd  a3708f5000             mov      dword ptr [0x508f70], eax
004750c2  57                     push     edi
004750c3  8a06                   mov      al, byte ptr [esi]
004750c5  8807                   mov      byte ptr [edi], al
004750c7  3c00                   cmp      al, 0
004750c9  7410                   je       0x4750db
004750cb  8a4601                 mov      al, byte ptr [esi + 1]
004750ce  83c602                 add      esi, 2
004750d1  884701                 mov      byte ptr [edi + 1], al
004750d4  83c702                 add      edi, 2
004750d7  3c00                   cmp      al, 0
004750d9  75e8                   jne      0x4750c3
004750db  5f                     pop      edi
004750dc  be964d4900             mov      esi, 0x494d96
004750e1  89e7                   mov      edi, esp
004750e3  57                     push     edi
004750e4  2bc9                   sub      ecx, ecx
004750e6  49                     dec      ecx
004750e7  b000                   mov      al, 0
004750e9  f2ae                   repne scasb al, byte ptr es:[edi]
004750eb  4f                     dec      edi
004750ec  8a06                   mov      al, byte ptr [esi]
004750ee  8807                   mov      byte ptr [edi], al
004750f0  3c00                   cmp      al, 0
004750f2  7410                   je       0x475104
004750f4  8a4601                 mov      al, byte ptr [esi + 1]
004750f7  83c602                 add      esi, 2
004750fa  884701                 mov      byte ptr [edi + 1], al
004750fd  83c702                 add      edi, 2
00475100  3c00                   cmp      al, 0
00475102  75e8                   jne      0x4750ec
00475104  5f                     pop      edi
00475105  89e0                   mov      eax, esp
00475107  8b15708f5000           mov      edx, dword ptr [0x508f70]
0047510d  e8b2480000             call     0x4799c4 ; LoadPie
00475112  e9b5faffff             jmp      0x474bcc ;
