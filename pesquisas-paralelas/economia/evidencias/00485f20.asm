; B_TestMaxRocheDansStock: limite por próximo símbolo SBL, fim exclusivo 0x00485fa3.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00485f20  53                       push     ebx
00485f21  51                       push     ecx
00485f22  52                       push     edx
00485f23  56                       push     esi
00485f24  83ec10                   sub      esp, 0x10
00485f27  89c6                     mov      esi, eax
00485f29  31c0                     xor      eax, eax
00485f2b  8d4c2408                 lea      ecx, [esp + 8]
00485f2f  8a461c                   mov      al, byte ptr [esi + 0x1c]
00485f32  8d5c2404                 lea      ebx, [esp + 4]
00485f36  50                       push     eax
00485f37  8d542410                 lea      edx, [esp + 0x10]
00485f3b  8d442404                 lea      eax, [esp + 4]
00485f3f  e85917feff               call     0x46769d
00485f44  8b561c                   mov      edx, dword ptr [esi + 0x1c]
00485f47  89d0                     mov      eax, edx
00485f49  c1e002                   shl      eax, 2
00485f4c  29d0                     sub      eax, edx
00485f4e  31d2                     xor      edx, edx
00485f50  668b14452efb4d00         mov      dx, word ptr [eax*2 + 0x4dfb2e]
00485f58  668b04452cfb4d00         mov      ax, word ptr [eax*2 + 0x4dfb2c]
00485f60  25ffff0000               and      eax, 0xffff
00485f65  0fafd0                   imul     edx, eax
00485f68  0faf15f8bc5100           imul     edx, dword ptr [0x51bcf8]
00485f6f  8b0df8bc5100             mov      ecx, dword ptr [0x51bcf8]
00485f75  8b1df4bc5100             mov      ebx, dword ptr [0x51bcf4]
00485f7b  89d0                     mov      eax, edx
00485f7d  c1fa1f                   sar      edx, 0x1f
00485f80  01cb                     add      ebx, ecx
00485f82  f7fb                     idiv     ebx
00485f84  31d2                     xor      edx, edx
00485f86  668b54240c               mov      dx, word ptr [esp + 0xc]
00485f8b  39c2                     cmp      edx, eax
00485f8d  7e07                     jle      0x485f96
00485f8f  b801000000               mov      eax, 1
00485f94  eb05                     jmp      0x485f9b
00485f96  b8ffffffff               mov      eax, 0xffffffff
00485f9b  83c410                   add      esp, 0x10
00485f9e  5e                       pop      esi
00485f9f  5a                       pop      edx
00485fa0  59                       pop      ecx
00485fa1  5b                       pop      ebx
00485fa2  c3                       ret
