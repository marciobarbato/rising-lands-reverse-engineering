; IllumineTerrain; intervalo [0x00476cb3, 0x00476e82)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476cb3  51                       push     ecx
00476cb4  56                       push     esi
00476cb5  57                       push     edi
00476cb6  83ec1c                   sub      esp, 0x1c
00476cb9  89d6                     mov      esi, edx
00476cbb  885c2418                 mov      byte ptr [esp + 0x18], bl
00476cbf  31db                     xor      ebx, ebx
00476cc1  6689c3                   mov      bx, ax
00476cc4  b900010000               mov      ecx, 0x100
00476cc9  89da                     mov      edx, ebx
00476ccb  89d8                     mov      eax, ebx
00476ccd  c1fa1f                   sar      edx, 0x1f
00476cd0  f7f9                     idiv     ecx
00476cd2  89d7                     mov      edi, edx
00476cd4  89da                     mov      edx, ebx
00476cd6  89d8                     mov      eax, ebx
00476cd8  c1fa1f                   sar      edx, 0x1f
00476cdb  f7f9                     idiv     ecx
00476cdd  66890424                 mov      word ptr [esp], ax
00476ce1  89f0                     mov      eax, esi
00476ce3  0fafc6                   imul     eax, esi
00476ce6  31d2                     xor      edx, edx
00476ce8  6689f2                   mov      dx, si
00476ceb  83fa02                   cmp      edx, 2
00476cee  7c01                     jl       0x476cf1
00476cf0  40                       inc      eax
00476cf1  89442410                 mov      dword ptr [esp + 0x10], eax
00476cf5  89f2                     mov      edx, esi
00476cf7  6689742414               mov      word ptr [esp + 0x14], si
00476cfc  f7da                     neg      edx
00476cfe  6689542414               mov      word ptr [esp + 0x14], dx
00476d03  89d0                     mov      eax, edx
00476d05  8b1424                   mov      edx, dword ptr [esp]
00476d08  c1e008                   shl      eax, 8
00476d0b  c1e208                   shl      edx, 8
00476d0e  01d0                     add      eax, edx
00476d10  6689442404               mov      word ptr [esp + 4], ax
00476d15  eb14                     jmp      0x476d2b
00476d17  8a642405                 mov      ah, byte ptr [esp + 5]
00476d1b  8b5c2414                 mov      ebx, dword ptr [esp + 0x14]
00476d1f  fec4                     inc      ah
00476d21  43                       inc      ebx
00476d22  88642405                 mov      byte ptr [esp + 5], ah
00476d26  66895c2414               mov      word ptr [esp + 0x14], bx
00476d2b  8b442412                 mov      eax, dword ptr [esp + 0x12]
00476d2f  31d2                     xor      edx, edx
00476d31  c1f810                   sar      eax, 0x10
00476d34  6689f2                   mov      dx, si
00476d37  39d0                     cmp      eax, edx
00476d39  0f8f76000000             jg       0x476db5
00476d3f  8b5424fe                 mov      edx, dword ptr [esp - 2]
00476d43  c1fa10                   sar      edx, 0x10
00476d46  01d0                     add      eax, edx
00476d48  85c0                     test     eax, eax
00476d4a  7ccb                     jl       0x476d17
00476d4c  31d2                     xor      edx, edx
00476d4e  668b156a714900           mov      dx, word ptr [0x49716a]
00476d55  39d0                     cmp      eax, edx
00476d57  7dbe                     jge      0x476d17
00476d59  89f3                     mov      ebx, esi
00476d5b  8b4c2404                 mov      ecx, dword ptr [esp + 4]
00476d5f  f7db                     neg      ebx
00476d61  01d9                     add      ecx, ebx
00476d63  01f9                     add      ecx, edi
00476d65  eb02                     jmp      0x476d69
00476d67  41                       inc      ecx
00476d68  43                       inc      ebx
00476d69  31d2                     xor      edx, edx
00476d6b  0fbfc3                   movsx    eax, bx
00476d6e  6689f2                   mov      dx, si
00476d71  39d0                     cmp      eax, edx
00476d73  7fa2                     jg       0x476d17
00476d75  0fbfd7                   movsx    edx, di
00476d78  01d0                     add      eax, edx
00476d7a  85c0                     test     eax, eax
00476d7c  7ce9                     jl       0x476d67
00476d7e  31d2                     xor      edx, edx
00476d80  668b1568714900           mov      dx, word ptr [0x497168]
00476d87  39d0                     cmp      eax, edx
00476d89  7ddc                     jge      0x476d67
00476d8b  31c0                     xor      eax, eax
00476d8d  31d2                     xor      edx, edx
00476d8f  668b442414               mov      ax, word ptr [esp + 0x14]
00476d94  6689da                   mov      dx, bx
00476d97  e8b0270000               call     0x47954c
00476d9c  663b442410               cmp      ax, word ptr [esp + 0x10]
00476da1  77c4                     ja       0x476d67
00476da3  31d2                     xor      edx, edx
00476da5  31c0                     xor      eax, eax
00476da7  8a542418                 mov      dl, byte ptr [esp + 0x18]
00476dab  6689c8                   mov      ax, cx
00476dae  e8b5fbffff               call     0x476968
00476db3  ebb2                     jmp      0x476d67
00476db5  89f3                     mov      ebx, esi
00476db7  f7db                     neg      ebx
00476db9  8b1424                   mov      edx, dword ptr [esp]
00476dbc  89d8                     mov      eax, ebx
00476dbe  c1e208                   shl      edx, 8
00476dc1  c1e008                   shl      eax, 8
00476dc4  668974240c               mov      word ptr [esp + 0xc], si
00476dc9  01d0                     add      eax, edx
00476dcb  66895c240c               mov      word ptr [esp + 0xc], bx
00476dd0  6689442408               mov      word ptr [esp + 8], ax
00476dd5  eb14                     jmp      0x476deb
00476dd7  8a542409                 mov      dl, byte ptr [esp + 9]
00476ddb  8b5c240c                 mov      ebx, dword ptr [esp + 0xc]
00476ddf  fec2                     inc      dl
00476de1  43                       inc      ebx
00476de2  88542409                 mov      byte ptr [esp + 9], dl
00476de6  66895c240c               mov      word ptr [esp + 0xc], bx
00476deb  8b44240a                 mov      eax, dword ptr [esp + 0xa]
00476def  31d2                     xor      edx, edx
00476df1  c1f810                   sar      eax, 0x10
00476df4  6689f2                   mov      dx, si
00476df7  39d0                     cmp      eax, edx
00476df9  0f8f7c000000             jg       0x476e7b
00476dff  8b5424fe                 mov      edx, dword ptr [esp - 2]
00476e03  c1fa10                   sar      edx, 0x10
00476e06  01d0                     add      eax, edx
00476e08  85c0                     test     eax, eax
00476e0a  7ccb                     jl       0x476dd7
00476e0c  31d2                     xor      edx, edx
00476e0e  668b156a714900           mov      dx, word ptr [0x49716a]
00476e15  39d0                     cmp      eax, edx
00476e17  7dbe                     jge      0x476dd7
00476e19  89f3                     mov      ebx, esi
00476e1b  8b4c2408                 mov      ecx, dword ptr [esp + 8]
00476e1f  f7db                     neg      ebx
00476e21  01d9                     add      ecx, ebx
00476e23  01f9                     add      ecx, edi
00476e25  eb02                     jmp      0x476e29
00476e27  41                       inc      ecx
00476e28  43                       inc      ebx
00476e29  31d2                     xor      edx, edx
00476e2b  0fbfc3                   movsx    eax, bx
00476e2e  6689f2                   mov      dx, si
00476e31  39d0                     cmp      eax, edx
00476e33  7fa2                     jg       0x476dd7
00476e35  0fbfd7                   movsx    edx, di
00476e38  01d0                     add      eax, edx
00476e3a  85c0                     test     eax, eax
00476e3c  7ce9                     jl       0x476e27
00476e3e  31d2                     xor      edx, edx
00476e40  668b1568714900           mov      dx, word ptr [0x497168]
00476e47  39d0                     cmp      eax, edx
00476e49  7ddc                     jge      0x476e27
00476e4b  31c0                     xor      eax, eax
00476e4d  31d2                     xor      edx, edx
00476e4f  668b44240c               mov      ax, word ptr [esp + 0xc]
00476e54  6689da                   mov      dx, bx
00476e57  e8f0260000               call     0x47954c
00476e5c  663b442410               cmp      ax, word ptr [esp + 0x10]
00476e61  77c4                     ja       0x476e27
00476e63  31c0                     xor      eax, eax
00476e65  31d2                     xor      edx, edx
00476e67  8a442418                 mov      al, byte ptr [esp + 0x18]
00476e6b  6689ca                   mov      dx, cx
00476e6e  8b0485887d5000           mov      eax, dword ptr [eax*4 + 0x507d88]
00476e75  f6040210                 test     byte ptr [edx + eax], 0x10
00476e79  ebac                     jmp      0x476e27
00476e7b  83c41c                   add      esp, 0x1c
00476e7e  5f                       pop      edi
00476e7f  5e                       pop      esi
00476e80  59                       pop      ecx
00476e81  c3                       ret
