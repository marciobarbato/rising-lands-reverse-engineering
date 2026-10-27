; AngleCalcul; intervalo [0x004796cb, 0x004798b0)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004796cb  56                       push     esi
004796cc  57                       push     edi
004796cd  55                       push     ebp
004796ce  83ec40                   sub      esp, 0x40
004796d1  89c6                     mov      esi, eax
004796d3  31c0                     xor      eax, eax
004796d5  668b442450               mov      ax, word ptr [esp + 0x50]
004796da  89442428                 mov      dword ptr [esp + 0x28], eax
004796de  db442428                 fild     dword ptr [esp + 0x28]
004796e2  dc3d0c4e4900             fdivr    qword ptr [0x494e0c]
004796e8  dd5c2420                 fstp     qword ptr [esp + 0x20]
004796ec  6639de                   cmp      si, bx
004796ef  7206                     jb       0x4796f7
004796f1  89f0                     mov      eax, esi
004796f3  29d8                     sub      eax, ebx
004796f5  eb04                     jmp      0x4796fb
004796f7  89d8                     mov      eax, ebx
004796f9  29f0                     sub      eax, esi
004796fb  8944243c                 mov      dword ptr [esp + 0x3c], eax
004796ff  6639ca                   cmp      dx, cx
00479702  7206                     jb       0x47970a
00479704  89d0                     mov      eax, edx
00479706  29c8                     sub      eax, ecx
00479708  eb04                     jmp      0x47970e
0047970a  89c8                     mov      eax, ecx
0047970c  29d0                     sub      eax, edx
0047970e  89442434                 mov      dword ptr [esp + 0x34], eax
00479712  8b44243c                 mov      eax, dword ptr [esp + 0x3c]
00479716  bf44174154               mov      edi, 0x54411744
0047971b  bdfb210940               mov      ebp, 0x400921fb
00479720  8944242c                 mov      dword ptr [esp + 0x2c], eax
00479724  897c2418                 mov      dword ptr [esp + 0x18], edi
00479728  896c241c                 mov      dword ptr [esp + 0x1c], ebp
0047972c  31c0                     xor      eax, eax
0047972e  31ff                     xor      edi, edi
00479730  668b44243c               mov      ax, word ptr [esp + 0x3c]
00479735  668b7c2434               mov      di, word ptr [esp + 0x34]
0047973a  89c5                     mov      ebp, eax
0047973c  0fafef                   imul     ebp, edi
0047973f  85ed                     test     ebp, ebp
00479741  0f8488000000             je       0x4797cf
00479747  31ff                     xor      edi, edi
00479749  897c2430                 mov      dword ptr [esp + 0x30], edi
0047974d  8b7c2434                 mov      edi, dword ptr [esp + 0x34]
00479751  897c2438                 mov      dword ptr [esp + 0x38], edi
00479755  0fafc0                   imul     eax, eax
00479758  8b7c2430                 mov      edi, dword ptr [esp + 0x30]
0047975c  663b7c2438               cmp      di, word ptr [esp + 0x38]
00479761  7618                     jbe      0x47977b
00479763  31ff                     xor      edi, edi
00479765  668b7c2430               mov      di, word ptr [esp + 0x30]
0047976a  897c2428                 mov      dword ptr [esp + 0x28], edi
0047976e  31ff                     xor      edi, edi
00479770  8b6c2428                 mov      ebp, dword ptr [esp + 0x28]
00479774  668b7c2438               mov      di, word ptr [esp + 0x38]
00479779  eb16                     jmp      0x479791
0047977b  31ff                     xor      edi, edi
0047977d  668b7c2438               mov      di, word ptr [esp + 0x38]
00479782  897c2428                 mov      dword ptr [esp + 0x28], edi
00479786  31ff                     xor      edi, edi
00479788  8b6c2428                 mov      ebp, dword ptr [esp + 0x28]
0047978c  668b7c2430               mov      di, word ptr [esp + 0x30]
00479791  29fd                     sub      ebp, edi
00479793  89ef                     mov      edi, ebp
00479795  0faffd                   imul     edi, ebp
00479798  01f8                     add      eax, edi
0047979a  31ff                     xor      edi, edi
0047979c  89442410                 mov      dword ptr [esp + 0x10], eax
004797a0  897c2414                 mov      dword ptr [esp + 0x14], edi
004797a4  df6c2410                 fild     qword ptr [esp + 0x10]
004797a8  d9fa                     fsqrt
004797aa  31c0                     xor      eax, eax
004797ac  668b44242c               mov      ax, word ptr [esp + 0x2c]
004797b1  89442428                 mov      dword ptr [esp + 0x28], eax
004797b5  db442428                 fild     dword ptr [esp + 0x28]
004797b9  def1                     fdivrp   st(1)
004797bb  e80e3e0100               call     0x48d5ce
004797c0  dc0d144e4900             fmul     qword ptr [0x494e14]
004797c6  dc742418                 fdiv     qword ptr [esp + 0x18]
004797ca  dd1c24                   fstp     qword ptr [esp]
004797cd  eb1d                     jmp      0x4797ec
004797cf  85ff                     test     edi, edi
004797d1  7509                     jne      0x4797dc
004797d3  892c24                   mov      dword ptr [esp], ebp
004797d6  896c2404                 mov      dword ptr [esp + 4], ebp
004797da  eb10                     jmp      0x4797ec
004797dc  85c0                     test     eax, eax
004797de  750c                     jne      0x4797ec
004797e0  bf00805640               mov      edi, 0x40568000
004797e5  892c24                   mov      dword ptr [esp], ebp
004797e8  897c2404                 mov      dword ptr [esp + 4], edi
004797ec  8b0424                   mov      eax, dword ptr [esp]
004797ef  89442408                 mov      dword ptr [esp + 8], eax
004797f3  8b442404                 mov      eax, dword ptr [esp + 4]
004797f7  8944240c                 mov      dword ptr [esp + 0xc], eax
004797fb  6639de                   cmp      si, bx
004797fe  761d                     jbe      0x47981d
00479800  6639ca                   cmp      dx, cx
00479803  720b                     jb       0x479810
00479805  dd0424                   fld      qword ptr [esp]
00479808  dc05144e4900             fadd     qword ptr [0x494e14]
0047980e  eb1d                     jmp      0x47982d
00479810  731f                     jae      0x479831
00479812  dd05144e4900             fld      qword ptr [0x494e14]
00479818  dc2424                   fsub     qword ptr [esp]
0047981b  eb10                     jmp      0x47982d
0047981d  7712                     ja       0x479831
0047981f  6639ca                   cmp      dx, cx
00479822  760d                     jbe      0x479831
00479824  dd050c4e4900             fld      qword ptr [0x494e0c]
0047982a  dc2424                   fsub     qword ptr [esp]
0047982d  dd5c2408                 fstp     qword ptr [esp + 8]
00479831  dd442420                 fld      qword ptr [esp + 0x20]
00479835  dc0d1c4e4900             fmul     qword ptr [0x494e1c]
0047983b  dc442408                 fadd     qword ptr [esp + 8]
0047983f  dd542408                 fst      qword ptr [esp + 8]
00479843  dc1d0c4e4900             fcomp    qword ptr [0x494e0c]
00479849  dfe0                     fnstsw   ax
0047984b  9e                       sahf
0047984c  720e                     jb       0x47985c
0047984e  dd442408                 fld      qword ptr [esp + 8]
00479852  dc05244e4900             fadd     qword ptr [0x494e24]
00479858  dd5c2408                 fstp     qword ptr [esp + 8]
0047985c  dd442408                 fld      qword ptr [esp + 8]
00479860  dc742420                 fdiv     qword ptr [esp + 0x20]
00479864  31d2                     xor      edx, edx
00479866  31db                     xor      ebx, ebx
00479868  e8d12b0100               call     0x48c43e
0047986d  db5c2428                 fistp    dword ptr [esp + 0x28]
00479871  8b442428                 mov      eax, dword ptr [esp + 0x28]
00479875  668b5c2450               mov      bx, word ptr [esp + 0x50]
0047987a  6689c2                   mov      dx, ax
0047987d  89d0                     mov      eax, edx
0047987f  c1fa1f                   sar      edx, 0x1f
00479882  f7fb                     idiv     ebx
00479884  89d0                     mov      eax, edx
00479886  25ffff0000               and      eax, 0xffff
0047988b  89da                     mov      edx, ebx
0047988d  8d3c18                   lea      edi, [eax + ebx]
00479890  c1fa1f                   sar      edx, 0x1f
00479893  89d8                     mov      eax, ebx
00479895  2bc2                     sub      eax, edx
00479897  d1f8                     sar      eax, 1
00479899  89fa                     mov      edx, edi
0047989b  29c2                     sub      edx, eax
0047989d  89d0                     mov      eax, edx
0047989f  c1fa1f                   sar      edx, 0x1f
004798a2  f7fb                     idiv     ebx
004798a4  8d4201                   lea      eax, [edx + 1]
004798a7  83c440                   add      esp, 0x40
004798aa  5d                       pop      ebp
004798ab  5f                       pop      edi
004798ac  5e                       pop      esi
004798ad  c20400                   ret      4
