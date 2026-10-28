; EteintTerrain; intervalo [0x00476e82, 0x00477042)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00476e82  51                       push     ecx
00476e83  56                       push     esi
00476e84  57                       push     edi
00476e85  83ec1c                   sub      esp, 0x1c
00476e88  89d7                     mov      edi, edx
00476e8a  885c2418                 mov      byte ptr [esp + 0x18], bl
00476e8e  31f6                     xor      esi, esi
00476e90  6689c6                   mov      si, ax
00476e93  bb00010000               mov      ebx, 0x100
00476e98  89f2                     mov      edx, esi
00476e9a  89f0                     mov      eax, esi
00476e9c  c1fa1f                   sar      edx, 0x1f
00476e9f  f7fb                     idiv     ebx
00476ea1  89542414                 mov      dword ptr [esp + 0x14], edx
00476ea5  89f2                     mov      edx, esi
00476ea7  89f0                     mov      eax, esi
00476ea9  c1fa1f                   sar      edx, 0x1f
00476eac  f7fb                     idiv     ebx
00476eae  8944240c                 mov      dword ptr [esp + 0xc], eax
00476eb2  89f8                     mov      eax, edi
00476eb4  0fafc7                   imul     eax, edi
00476eb7  31d2                     xor      edx, edx
00476eb9  6689fa                   mov      dx, di
00476ebc  83fa02                   cmp      edx, 2
00476ebf  7c01                     jl       0x476ec2
00476ec1  40                       inc      eax
00476ec2  89442410                 mov      dword ptr [esp + 0x10], eax
00476ec6  89fa                     mov      edx, edi
00476ec8  66897c2408               mov      word ptr [esp + 8], di
00476ecd  f7da                     neg      edx
00476ecf  6689542408               mov      word ptr [esp + 8], dx
00476ed4  89d0                     mov      eax, edx
00476ed6  8b54240c                 mov      edx, dword ptr [esp + 0xc]
00476eda  c1e008                   shl      eax, 8
00476edd  c1e208                   shl      edx, 8
00476ee0  01d0                     add      eax, edx
00476ee2  66890424                 mov      word ptr [esp], ax
00476ee6  eb14                     jmp      0x476efc
00476ee8  8a642401                 mov      ah, byte ptr [esp + 1]
00476eec  8b5c2408                 mov      ebx, dword ptr [esp + 8]
00476ef0  fec4                     inc      ah
00476ef2  43                       inc      ebx
00476ef3  88642401                 mov      byte ptr [esp + 1], ah
00476ef7  66895c2408               mov      word ptr [esp + 8], bx
00476efc  8b442406                 mov      eax, dword ptr [esp + 6]
00476f00  31d2                     xor      edx, edx
00476f02  c1f810                   sar      eax, 0x10
00476f05  6689fa                   mov      dx, di
00476f08  39d0                     cmp      eax, edx
00476f0a  0f8f7c000000             jg       0x476f8c
00476f10  31d2                     xor      edx, edx
00476f12  668b54240c               mov      dx, word ptr [esp + 0xc]
00476f17  01d0                     add      eax, edx
00476f19  85c0                     test     eax, eax
00476f1b  7ccb                     jl       0x476ee8
00476f1d  31d2                     xor      edx, edx
00476f1f  668b156a714900           mov      dx, word ptr [0x49716a]
00476f26  39d0                     cmp      eax, edx
00476f28  7dbe                     jge      0x476ee8
00476f2a  89fb                     mov      ebx, edi
00476f2c  8b0c24                   mov      ecx, dword ptr [esp]
00476f2f  f7db                     neg      ebx
00476f31  8b742414                 mov      esi, dword ptr [esp + 0x14]
00476f35  01d9                     add      ecx, ebx
00476f37  01f1                     add      ecx, esi
00476f39  eb02                     jmp      0x476f3d
00476f3b  41                       inc      ecx
00476f3c  43                       inc      ebx
00476f3d  31c0                     xor      eax, eax
00476f3f  0fbff3                   movsx    esi, bx
00476f42  6689f8                   mov      ax, di
00476f45  39c6                     cmp      esi, eax
00476f47  7f9f                     jg       0x476ee8
00476f49  31c0                     xor      eax, eax
00476f4b  31d2                     xor      edx, edx
00476f4d  668b442408               mov      ax, word ptr [esp + 8]
00476f52  6689da                   mov      dx, bx
00476f55  e8f2250000               call     0x47954c
00476f5a  663b442410               cmp      ax, word ptr [esp + 0x10]
00476f5f  77da                     ja       0x476f3b
00476f61  31c0                     xor      eax, eax
00476f63  668b442414               mov      ax, word ptr [esp + 0x14]
00476f68  01c6                     add      esi, eax
00476f6a  85f6                     test     esi, esi
00476f6c  7ccd                     jl       0x476f3b
00476f6e  31c0                     xor      eax, eax
00476f70  66a168714900             mov      ax, word ptr [0x497168]
00476f76  39c6                     cmp      esi, eax
00476f78  7dc1                     jge      0x476f3b
00476f7a  31d2                     xor      edx, edx
00476f7c  31c0                     xor      eax, eax
00476f7e  8a542418                 mov      dl, byte ptr [esp + 0x18]
00476f82  6689c8                   mov      ax, cx
00476f85  e852fbffff               call     0x476adc
00476f8a  ebaf                     jmp      0x476f3b
00476f8c  89fe                     mov      esi, edi
00476f8e  f7de                     neg      esi
00476f90  8b54240c                 mov      edx, dword ptr [esp + 0xc]
00476f94  89f0                     mov      eax, esi
00476f96  c1e208                   shl      edx, 8
00476f99  c1e008                   shl      eax, 8
00476f9c  01d0                     add      eax, edx
00476f9e  6689442404               mov      word ptr [esp + 4], ax
00476fa3  eb0b                     jmp      0x476fb0
00476fa5  8a542405                 mov      dl, byte ptr [esp + 5]
00476fa9  fec2                     inc      dl
00476fab  46                       inc      esi
00476fac  88542405                 mov      byte ptr [esp + 5], dl
00476fb0  31d2                     xor      edx, edx
00476fb2  0fbfc6                   movsx    eax, si
00476fb5  6689fa                   mov      dx, di
00476fb8  39d0                     cmp      eax, edx
00476fba  0f8fbbfeffff             jg       0x476e7b
00476fc0  31d2                     xor      edx, edx
00476fc2  668b54240c               mov      dx, word ptr [esp + 0xc]
00476fc7  01d0                     add      eax, edx
00476fc9  85c0                     test     eax, eax
00476fcb  7cd8                     jl       0x476fa5
00476fcd  31d2                     xor      edx, edx
00476fcf  668b156a714900           mov      dx, word ptr [0x49716a]
00476fd6  39d0                     cmp      eax, edx
00476fd8  7dcb                     jge      0x476fa5
00476fda  89fb                     mov      ebx, edi
00476fdc  8b4c2404                 mov      ecx, dword ptr [esp + 4]
00476fe0  f7db                     neg      ebx
00476fe2  8b442414                 mov      eax, dword ptr [esp + 0x14]
00476fe6  01d9                     add      ecx, ebx
00476fe8  01c1                     add      ecx, eax
00476fea  eb02                     jmp      0x476fee
00476fec  41                       inc      ecx
00476fed  43                       inc      ebx
00476fee  31d2                     xor      edx, edx
00476ff0  0fbfc3                   movsx    eax, bx
00476ff3  6689fa                   mov      dx, di
00476ff6  39d0                     cmp      eax, edx
00476ff8  7fab                     jg       0x476fa5
00476ffa  31d2                     xor      edx, edx
00476ffc  668b542414               mov      dx, word ptr [esp + 0x14]
00477001  01d0                     add      eax, edx
00477003  85c0                     test     eax, eax
00477005  7ce5                     jl       0x476fec
00477007  31d2                     xor      edx, edx
00477009  668b1568714900           mov      dx, word ptr [0x497168]
00477010  39d0                     cmp      eax, edx
00477012  7dd8                     jge      0x476fec
00477014  31d2                     xor      edx, edx
00477016  31c0                     xor      eax, eax
00477018  6689da                   mov      dx, bx
0047701b  6689f0                   mov      ax, si
0047701e  e829250000               call     0x47954c
00477023  663b442410               cmp      ax, word ptr [esp + 0x10]
00477028  77c2                     ja       0x476fec
0047702a  31c0                     xor      eax, eax
0047702c  31d2                     xor      edx, edx
0047702e  8a442418                 mov      al, byte ptr [esp + 0x18]
00477032  6689ca                   mov      dx, cx
00477035  8b0485887d5000           mov      eax, dword ptr [eax*4 + 0x507d88]
0047703c  f6040210                 test     byte ptr [edx + eax], 0x10
00477040  ebaa                     jmp      0x476fec
