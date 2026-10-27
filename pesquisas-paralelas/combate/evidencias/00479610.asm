; AngleQuart; intervalo [0x00479610, 0x004796cb)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00479610  53                       push     ebx
00479611  51                       push     ecx
00479612  56                       push     esi
00479613  55                       push     ebp
00479614  83ec1c                   sub      esp, 0x1c
00479617  89c3                     mov      ebx, eax
00479619  b944174154               mov      ecx, 0x54411744
0047961e  befb210940               mov      esi, 0x400921fb
00479623  31c0                     xor      eax, eax
00479625  894c2408                 mov      dword ptr [esp + 8], ecx
00479629  8974240c                 mov      dword ptr [esp + 0xc], esi
0047962d  6689d8                   mov      ax, bx
00479630  31c9                     xor      ecx, ecx
00479632  89c6                     mov      esi, eax
00479634  6689d1                   mov      cx, dx
00479637  0faff1                   imul     esi, ecx
0047963a  85f6                     test     esi, esi
0047963c  7465                     je       0x4796a3
0047963e  31d1                     xor      ecx, edx
00479640  0fafc0                   imul     eax, eax
00479643  6639d1                   cmp      cx, dx
00479646  7615                     jbe      0x47965d
00479648  81e1ffff0000             and      ecx, 0xffff
0047964e  81e2ffff0000             and      edx, 0xffff
00479654  29d1                     sub      ecx, edx
00479656  89ca                     mov      edx, ecx
00479658  0fafd1                   imul     edx, ecx
0047965b  eb11                     jmp      0x47966e
0047965d  81e2ffff0000             and      edx, 0xffff
00479663  81e1ffff0000             and      ecx, 0xffff
00479669  29ca                     sub      edx, ecx
0047966b  0fafd2                   imul     edx, edx
0047966e  01d0                     add      eax, edx
00479670  31c9                     xor      ecx, ecx
00479672  89442410                 mov      dword ptr [esp + 0x10], eax
00479676  894c2414                 mov      dword ptr [esp + 0x14], ecx
0047967a  df6c2410                 fild     qword ptr [esp + 0x10]
0047967e  d9fa                     fsqrt
00479680  31c0                     xor      eax, eax
00479682  6689d8                   mov      ax, bx
00479685  89442418                 mov      dword ptr [esp + 0x18], eax
00479689  db442418                 fild     dword ptr [esp + 0x18]
0047968d  def1                     fdivrp   st(1)
0047968f  e83a3f0100               call     0x48d5ce
00479694  dc0d044e4900             fmul     qword ptr [0x494e04]
0047969a  dc742408                 fdiv     qword ptr [esp + 8]
0047969e  dd1c24                   fstp     qword ptr [esp]
004796a1  eb1d                     jmp      0x4796c0
004796a3  85c9                     test     ecx, ecx
004796a5  7509                     jne      0x4796b0
004796a7  893424                   mov      dword ptr [esp], esi
004796aa  89742404                 mov      dword ptr [esp + 4], esi
004796ae  eb10                     jmp      0x4796c0
004796b0  85c0                     test     eax, eax
004796b2  750c                     jne      0x4796c0
004796b4  bd00805640               mov      ebp, 0x40568000
004796b9  893424                   mov      dword ptr [esp], esi
004796bc  896c2404                 mov      dword ptr [esp + 4], ebp
004796c0  dd0424                   fld      qword ptr [esp]
004796c3  83c41c                   add      esp, 0x1c
004796c6  5d                       pop      ebp
004796c7  5e                       pop      esi
004796c8  59                       pop      ecx
004796c9  5b                       pop      ebx
004796ca  c3                       ret
