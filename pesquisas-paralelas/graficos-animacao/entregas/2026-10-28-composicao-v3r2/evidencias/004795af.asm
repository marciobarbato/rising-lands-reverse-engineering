; Distance3d [0x4795af, 0x479610)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004795af  53                     push     ebx
004795b0  51                     push     ecx
004795b1  56                     push     esi
004795b2  57                     push     edi
004795b3  0fb638                 movzx    edi, byte ptr [eax]
004795b6  0fb67002               movzx    esi, byte ptr [eax + 2]
004795ba  31c9                   xor      ecx, ecx
004795bc  31db                   xor      ebx, ebx
004795be  8a4801                 mov      cl, byte ptr [eax + 1]
004795c1  31c0                   xor      eax, eax
004795c3  8a5a01                 mov      bl, byte ptr [edx + 1]
004795c6  8a02                   mov      al, byte ptr [edx]
004795c8  8a5202                 mov      dl, byte ptr [edx + 2]
004795cb  81e2ff000000           and      edx, 0xff
004795d1  39c7                   cmp      edi, eax
004795d3  7609                   jbe      0x4795de
004795d5  29c7                   sub      edi, eax
004795d7  89f8                   mov      eax, edi
004795d9  0fafc7                 imul     eax, edi
004795dc  eb05                   jmp      0x4795e3 ;
004795de  29f8                   sub      eax, edi
004795e0  0fafc0                 imul     eax, eax
004795e3  39d9                   cmp      ecx, ebx
004795e5  7607                   jbe      0x4795ee
004795e7  29d9                   sub      ecx, ebx
004795e9  0fafc9                 imul     ecx, ecx
004795ec  eb07                   jmp      0x4795f5 ;
004795ee  29cb                   sub      ebx, ecx
004795f0  89d9                   mov      ecx, ebx
004795f2  0fafcb                 imul     ecx, ebx
004795f5  01c8                   add      eax, ecx
004795f7  39d6                   cmp      esi, edx
004795f9  7607                   jbe      0x479602
004795fb  29d6                   sub      esi, edx
004795fd  0faff6                 imul     esi, esi
00479600  eb07                   jmp      0x479609 ;
00479602  29f2                   sub      edx, esi
00479604  89d6                   mov      esi, edx
00479606  0faff2                 imul     esi, edx
00479609  01f0                   add      eax, esi
0047960b  5f                     pop      edi
0047960c  5e                     pop      esi
0047960d  59                     pop      ecx
0047960e  5b                     pop      ebx
0047960f  c3                     ret
