; ResetMarche; exclusive end 0x004663d6.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046634e  53                       push     ebx
0046634f  51                       push     ecx
00466350  56                       push     esi
00466351  57                       push     edi
00466352  b301                     mov      bl, 1
00466354  b1ff                     mov      cl, 0xff
00466356  25ff000000               and      eax, 0xff
0046635b  30f6                     xor      dh, dh
0046635d  31f6                     xor      esi, esi
0046635f  88b07c2e4e00             mov      byte ptr [eax + 0x4e2e7c], dh
00466365  88982c294e00             mov      byte ptr [eax + 0x4e292c], bl
0046636b  88b028294e00             mov      byte ptr [eax + 0x4e2928], dh
00466371  88888c6f4900             mov      byte ptr [eax + 0x496f8c], cl
00466377  6689344530294e00         mov      word ptr [eax*2 + 0x4e2930], si
0046637f  30ff                     xor      bh, bh
00466381  31c9                     xor      ecx, ecx
00466383  30db                     xor      bl, bl
00466385  66890c4540294e00         mov      word ptr [eax*2 + 0x4e2940], cx
0046638d  66891c4538294e00         mov      word ptr [eax*2 + 0x4e2938], bx
00466395  31c0                     xor      eax, eax
00466397  88d0                     mov      al, dl
00466399  31ff                     xor      edi, edi
0046639b  b3ff                     mov      bl, 0xff
0046639d  88b07c2e4e00             mov      byte ptr [eax + 0x4e2e7c], dh
004663a3  b201                     mov      dl, 1
004663a5  88988c6f4900             mov      byte ptr [eax + 0x496f8c], bl
004663ab  88902c294e00             mov      byte ptr [eax + 0x4e292c], dl
004663b1  88b028294e00             mov      byte ptr [eax + 0x4e2928], dh
004663b7  30d2                     xor      dl, dl
004663b9  66893c4538294e00         mov      word ptr [eax*2 + 0x4e2938], di
004663c1  6689144540294e00         mov      word ptr [eax*2 + 0x4e2940], dx
004663c9  6689144530294e00         mov      word ptr [eax*2 + 0x4e2930], dx
004663d1  5f                       pop      edi
004663d2  5e                       pop      esi
004663d3  59                       pop      ecx
004663d4  5b                       pop      ebx
004663d5  c3                       ret
