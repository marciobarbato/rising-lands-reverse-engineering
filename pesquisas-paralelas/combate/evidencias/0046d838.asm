; PlayerEstAllie; intervalo [0x0046d838, 0x0046d877)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046d838  51                       push     ecx
0046d839  38d0                     cmp      al, dl
0046d83b  7436                     je       0x46d873
0046d83d  25ff000000               and      eax, 0xff
0046d842  83f804                   cmp      eax, 4
0046d845  7f09                     jg       0x46d850
0046d847  31c9                     xor      ecx, ecx
0046d849  88d1                     mov      cl, dl
0046d84b  83f904                   cmp      ecx, 4
0046d84e  7e04                     jle      0x46d854
0046d850  30c0                     xor      al, al
0046d852  59                       pop      ecx
0046d853  c3                       ret
0046d854  b201                     mov      dl, 1
0046d856  d2e2                     shl      dl, cl
0046d858  89c1                     mov      ecx, eax
0046d85a  c1e002                   shl      eax, 2
0046d85d  01c8                     add      eax, ecx
0046d85f  8b0da8805000             mov      ecx, dword ptr [0x5080a8]
0046d865  8b4c8103                 mov      ecx, dword ptr [ecx + eax*4 + 3]
0046d869  c1f918                   sar      ecx, 0x18
0046d86c  0fbec2                   movsx    eax, dl
0046d86f  85c1                     test     ecx, eax
0046d871  74dd                     je       0x46d850
0046d873  b001                     mov      al, 1
0046d875  59                       pop      ecx
0046d876  c3                       ret
