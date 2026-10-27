; BallonPrepareSortie: limite por próximo símbolo SBL, fim exclusivo 0x00441e3b.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
00441d4f  53                       push     ebx
00441d50  51                       push     ecx
00441d51  52                       push     edx
00441d52  57                       push     edi
00441d53  88c2                     mov      dl, al
00441d55  31c0                     xor      eax, eax
00441d57  88d0                     mov      al, dl
00441d59  c1e003                   shl      eax, 3
00441d5c  668b98141a4e00           mov      bx, word ptr [eax + 0x4e1a14]
00441d63  6685db                   test     bx, bx
00441d66  0f84ca000000             je       0x441e36
00441d6c  89d9                     mov      ecx, ebx
00441d6e  49                       dec      ecx
00441d6f  31db                     xor      ebx, ebx
00441d71  6689cb                   mov      bx, cx
00441d74  668988141a4e00           mov      word ptr [eax + 0x4e1a14], cx
00441d7b  85db                     test     ebx, ebx
00441d7d  0f85b3000000             jne      0x441e36
00441d83  668b88181a4e00           mov      cx, word ptr [eax + 0x4e1a18]
00441d8a  6689cb                   mov      bx, cx
00441d8d  89d8                     mov      eax, ebx
00441d8f  c1e004                   shl      eax, 4
00441d92  01d8                     add      eax, ebx
00441d94  c1e002                   shl      eax, 2
00441d97  01c3                     add      ebx, eax
00441d99  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00441d9e  c1e302                   shl      ebx, 2
00441da1  b61e                     mov      dh, 0x1e
00441da3  8a440302                 mov      al, byte ptr [ebx + eax + 2]
00441da7  25ff000000               and      eax, 0xff
00441dac  7409                     je       0x441db7
00441dae  83f804                   cmp      eax, 4
00441db1  7404                     je       0x441db7
00441db3  b001                     mov      al, 1
00441db5  eb02                     jmp      0x441db9
00441db7  30c0                     xor      al, al
00441db9  84c0                     test     al, al
00441dbb  7446                     je       0x441e03
00441dbd  31db                     xor      ebx, ebx
00441dbf  6689cb                   mov      bx, cx
00441dc2  89d8                     mov      eax, ebx
00441dc4  c1e004                   shl      eax, 4
00441dc7  01d8                     add      eax, ebx
00441dc9  c1e002                   shl      eax, 2
00441dcc  01d8                     add      eax, ebx
00441dce  8b1da0194e00             mov      ebx, dword ptr [0x4e19a0]
00441dd4  88748302                 mov      byte ptr [ebx + eax*4 + 2], dh
00441dd8  663b0d04634900           cmp      cx, word ptr [0x496304]
00441ddf  7522                     jne      0x441e03
00441de1  bfffff0000               mov      edi, 0xffff
00441de6  30e4                     xor      ah, ah
00441de8  31db                     xor      ebx, ebx
00441dea  8825360f4e00             mov      byte ptr [0x4e0f36], ah
00441df0  8825370f4e00             mov      byte ptr [0x4e0f37], ah
00441df6  891d3c0f4e00             mov      dword ptr [0x4e0f3c], ebx
00441dfc  66893d04634900           mov      word ptr [0x496304], di
00441e03  31db                     xor      ebx, ebx
00441e05  88d3                     mov      bl, dl
00441e07  31c0                     xor      eax, eax
00441e09  31d2                     xor      edx, edx
00441e0b  668b04dd181a4e00         mov      ax, word ptr [ebx*8 + 0x4e1a18]
00441e13  668b14dd1a1a4e00         mov      dx, word ptr [ebx*8 + 0x4e1a1a]
00441e1b  e8b3390000               call     0x4457d3
00441e20  31c0                     xor      eax, eax
00441e22  ba44000000               mov      edx, 0x44
00441e27  668b04dd181a4e00         mov      ax, word ptr [ebx*8 + 0x4e1a18]
00441e2f  31db                     xor      ebx, ebx
00441e31  e8920b0400               call     0x4829c8
00441e36  5f                       pop      edi
00441e37  5a                       pop      edx
00441e38  59                       pop      ecx
00441e39  5b                       pop      ebx
00441e3a  c3                       ret
