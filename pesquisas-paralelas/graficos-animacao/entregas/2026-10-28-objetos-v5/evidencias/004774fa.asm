; NextAnimVegetFullMap [0x4774fa, 0x477700)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
004774fa  53                     push     ebx
004774fb  51                     push     ecx
004774fc  52                     push     edx
004774fd  56                     push     esi
004774fe  57                     push     edi
004774ff  55                     push     ebp
00477500  83ec08                 sub      esp, 8
00477503  31db                   xor      ebx, ebx
00477505  31ff                   xor      edi, edi
00477507  bd01000000             mov      ebp, 1
0047750c  eb01                   jmp      0x47750f ;
0047750e  47                     inc      edi
0047750f  31c0                   xor      eax, eax
00477511  6689f8                 mov      ax, di
00477514  3d00010000             cmp      eax, 0x100
00477519  0f8dd7010000           jge      0x4776f6
0047751f  31f6                   xor      esi, esi
00477521  e981000000             jmp      0x4775a7 ;
00477526  f6057c8f500003         test     byte ptr [0x508f7c], 3
0047752d  0f8572000000           jne      0x4775a5
00477533  a0181d4e00             mov      al, byte ptr [0x4e1d18]
00477538  31c9                   xor      ecx, ecx
0047753a  88c1                   mov      cl, al
0047753c  fec0                   inc      al
0047753e  a2181d4e00             mov      byte ptr [0x4e1d18], al
00477543  f681181c4e0003         test     byte ptr [ecx + 0x4e1c18], 3
0047754a  0f8555000000           jne      0x4775a5
00477550  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00477555  01c2                   add      edx, eax
00477557  8a02                   mov      al, byte ptr [edx]
00477559  fec0                   inc      al
0047755b  2403                   and      al, 3
0047755d  8802                   mov      byte ptr [edx], al
0047755f  eb44                   jmp      0x4775a5 ;
00477561  f6057c8f500001         test     byte ptr [0x508f7c], 1
00477568  750e                   jne      0x477578
0047756a  31c0                   xor      eax, eax
0047756c  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00477572  6689d8                 mov      ax, bx
00477575  fe0402                 inc      byte ptr [edx + eax]
00477578  31c0                   xor      eax, eax
0047757a  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00477580  6689d8                 mov      ax, bx
00477583  8a1402                 mov      dl, byte ptr [edx + eax]
00477586  81e2ff000000           and      edx, 0xff
0047758c  83fa10                 cmp      edx, 0x10
0047758f  7514                   jne      0x4775a5
00477591  8b15747d5000           mov      edx, dword ptr [0x507d74]
00477597  c6040200               mov      byte ptr [edx + eax], 0
0047759b  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004775a1  c6040200               mov      byte ptr [edx + eax], 0
004775a5  43                     inc      ebx
004775a6  46                     inc      esi
004775a7  31c0                   xor      eax, eax
004775a9  6689f0                 mov      ax, si
004775ac  3d00010000             cmp      eax, 0x100
004775b1  0f8d57ffffff           jge      0x47750e
004775b7  31d2                   xor      edx, edx
004775b9  a1747d5000             mov      eax, dword ptr [0x507d74]
004775be  6689da                 mov      dx, bx
004775c1  01d0                   add      eax, edx
004775c3  8a08                   mov      cl, byte ptr [eax]
004775c5  84c9                   test     cl, cl
004775c7  0f85bc000000           jne      0x477689
004775cd  ebd6                   jmp      0x4775a5 ;
004775cf  f6057c8f500001         test     byte ptr [0x508f7c], 1
004775d6  7508                   jne      0x4775e0
004775d8  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004775dd  fe0402                 inc      byte ptr [edx + eax]
004775e0  31c0                   xor      eax, eax
004775e2  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
004775e8  6689d8                 mov      ax, bx
004775eb  8a1402                 mov      dl, byte ptr [edx + eax]
004775ee  81e2ff000000           and      edx, 0xff
004775f4  83fa40                 cmp      edx, 0x40
004775f7  75ac                   jne      0x4775a5
004775f9  8b15747d5000           mov      edx, dword ptr [0x507d74]
004775ff  01c2                   add      edx, eax
00477601  31c9                   xor      ecx, ecx
00477603  8a0a                   mov      cl, byte ptr [edx]
00477605  83f93b                 cmp      ecx, 0x3b
00477608  7405                   je       0x47760f
0047760a  83f938                 cmp      ecx, 0x38
0047760d  7510                   jne      0x47761f
0047760f  31c0                   xor      eax, eax
00477611  8b15747d5000           mov      edx, dword ptr [0x507d74]
00477617  6689d8                 mov      ax, bx
0047761a  e978ffffff             jmp      0x477597 ;
0047761f  30ed                   xor      ch, ch
00477621  882a                   mov      byte ptr [edx], ch
00477623  8b15ac7d5000           mov      edx, dword ptr [0x507dac]
00477629  66890c24               mov      word ptr [esp], cx
0047762d  882c02                 mov      byte ptr [edx + eax], ch
00477630  8a1424                 mov      dl, byte ptr [esp]
00477633  feca                   dec      dl
00477635  88542404               mov      byte ptr [esp + 4], dl
00477639  8b15747d5000           mov      edx, dword ptr [0x507d74]
0047763f  01c2                   add      edx, eax
00477641  31c9                   xor      ecx, ecx
00477643  8a0a                   mov      cl, byte ptr [edx]
00477645  85c9                   test     ecx, ecx
00477647  0f8558ffffff           jne      0x4775a5
0047764d  8a4c2404               mov      cl, byte ptr [esp + 4]
00477651  880a                   mov      byte ptr [edx], cl
00477653  e943ffffff             jmp      0x47759b ;
00477658  a1ac7d5000             mov      eax, dword ptr [0x507dac]
0047765d  fe0402                 inc      byte ptr [edx + eax]
00477660  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00477665  8a0402                 mov      al, byte ptr [edx + eax]
00477668  25ff000000             and      eax, 0xff
0047766d  83f820                 cmp      eax, 0x20
00477670  0f852fffffff           jne      0x4775a5
00477676  a1747d5000             mov      eax, dword ptr [0x507d74]
0047767b  c6040200               mov      byte ptr [edx + eax], 0
0047767f  a1ac7d5000             mov      eax, dword ptr [0x507dac]
00477684  e918ffffff             jmp      0x4775a1 ;
00477689  88c8                   mov      al, cl
0047768b  80f91b                 cmp      cl, 0x1b
0047768e  722c                   jb       0x4776bc
00477690  0f86cbfeffff           jbe      0x477561
00477696  80f938                 cmp      cl, 0x38
00477699  7213                   jb       0x4776ae
0047769b  80f93d                 cmp      cl, 0x3d
0047769e  0f862bffffff           jbe      0x4775cf
004776a4  80f941                 cmp      cl, 0x41
004776a7  76af                   jbe      0x477658
004776a9  e9f7feffff             jmp      0x4775a5 ;
004776ae  80f937                 cmp      cl, 0x37
004776b1  0f84aafeffff           je       0x477561
004776b7  e9e9feffff             jmp      0x4775a5 ;
004776bc  80f901                 cmp      cl, 1
004776bf  0f82e0feffff           jb       0x4775a5
004776c5  80f90b                 cmp      cl, 0xb
004776c8  0f8658feffff           jbe      0x477526
004776ce  80f917                 cmp      cl, 0x17
004776d1  0f82cefeffff           jb       0x4775a5
004776d7  f6057c8f500001         test     byte ptr [0x508f7c], 1
004776de  0f85c1feffff           jne      0x4775a5
004776e4  a1ac7d5000             mov      eax, dword ptr [0x507dac]
004776e9  01c2                   add      edx, eax
004776eb  8a02                   mov      al, byte ptr [edx]
004776ed  fec0                   inc      al
004776ef  240f                   and      al, 0xf
004776f1  e967feffff             jmp      0x47755d ;
004776f6  83c408                 add      esp, 8
004776f9  5d                     pop      ebp
004776fa  5f                     pop      edi
004776fb  5e                     pop      esi
004776fc  5a                     pop      edx
004776fd  59                     pop      ecx
004776fe  5b                     pop      ebx
004776ff  c3                     ret
