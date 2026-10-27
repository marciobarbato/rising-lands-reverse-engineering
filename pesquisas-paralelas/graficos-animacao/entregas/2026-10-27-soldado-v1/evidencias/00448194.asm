; EnginEnArret [0x448194, 0x448228)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
00448194  53                     push     ebx
00448195  52                     push     edx
00448196  31d2                   xor      edx, edx
00448198  6689c2                 mov      dx, ax
0044819b  89d0                   mov      eax, edx
0044819d  c1e004                 shl      eax, 4
004481a0  01d0                   add      eax, edx
004481a2  c1e002                 shl      eax, 2
004481a5  01c2                   add      edx, eax
004481a7  a1a0194e00             mov      eax, dword ptr [0x4e19a0]
004481ac  c1e202                 shl      edx, 2
004481af  01d0                   add      eax, edx
004481b1  30d2                   xor      dl, dl
004481b3  8a7001                 mov      dh, byte ptr [eax + 1]
004481b6  80fe19                 cmp      dh, 0x19
004481b9  7768                   ja       0x448223
004481bb  31db                   xor      ebx, ebx
004481bd  88f3                   mov      bl, dh
004481bf  2eff249d2c814400       jmp      dword ptr cs:[ebx*4 + 0x44812c]
004481c7  b201                   mov      dl, 1
004481c9  c680a400000002         mov      byte ptr [eax + 0xa4], 2
004481d0  88d0                   mov      al, dl
004481d2  5a                     pop      edx
004481d3  5b                     pop      ebx
004481d4  c3                     ret      
004481d5  b201                   mov      dl, 1
004481d7  c680a400000007         mov      byte ptr [eax + 0xa4], 7
004481de  88d0                   mov      al, dl
004481e0  5a                     pop      edx
004481e1  5b                     pop      ebx
004481e2  c3                     ret      
004481e3  b201                   mov      dl, 1
004481e5  c680a400000003         mov      byte ptr [eax + 0xa4], 3
004481ec  88d0                   mov      al, dl
004481ee  5a                     pop      edx
004481ef  5b                     pop      ebx
004481f0  c3                     ret      
004481f1  b201                   mov      dl, 1
004481f3  c680a400000006         mov      byte ptr [eax + 0xa4], 6
004481fa  88d0                   mov      al, dl
004481fc  5a                     pop      edx
004481fd  5b                     pop      ebx
004481fe  c3                     ret      
004481ff  b201                   mov      dl, 1
00448201  c680a400000005         mov      byte ptr [eax + 0xa4], 5
00448208  88d0                   mov      al, dl
0044820a  5a                     pop      edx
0044820b  5b                     pop      ebx
0044820c  c3                     ret      
0044820d  8890a4000000           mov      byte ptr [eax + 0xa4], dl
00448213  b201                   mov      dl, 1
00448215  88d0                   mov      al, dl
00448217  5a                     pop      edx
00448218  5b                     pop      ebx
00448219  c3                     ret      
0044821a  b201                   mov      dl, 1
0044821c  c680a400000001         mov      byte ptr [eax + 0xa4], 1
00448223  88d0                   mov      al, dl
00448225  5a                     pop      edx
00448226  5b                     pop      ebx
00448227  c3                     ret      
