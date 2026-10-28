; PlayerResetAllie; [0x0046d8cb,0x0046d927)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046d8cb  53                       push     ebx
0046d8cc  51                       push     ecx
0046d8cd  88c3                     mov      bl, al
0046d8cf  38d0                     cmp      al, dl
0046d8d1  7451                     je       0x46d924
0046d8d3  31c0                     xor      eax, eax
0046d8d5  88d8                     mov      al, bl
0046d8d7  83f804                   cmp      eax, 4
0046d8da  7f48                     jg       0x46d924
0046d8dc  31c9                     xor      ecx, ecx
0046d8de  88d1                     mov      cl, dl
0046d8e0  83f904                   cmp      ecx, 4
0046d8e3  7f3f                     jg       0x46d924
0046d8e5  b701                     mov      bh, 1
0046d8e7  d2e7                     shl      bh, cl
0046d8e9  89c1                     mov      ecx, eax
0046d8eb  c1e002                   shl      eax, 2
0046d8ee  01c8                     add      eax, ecx
0046d8f0  8b0da8805000             mov      ecx, dword ptr [0x5080a8]
0046d8f6  8a748106                 mov      dh, byte ptr [ecx + eax*4 + 6]
0046d8fa  f6d6                     not      dh
0046d8fc  08fe                     or       dh, bh
0046d8fe  f6d6                     not      dh
0046d900  88748106                 mov      byte ptr [ecx + eax*4 + 6], dh
0046d904  3a1d41805000             cmp      bl, byte ptr [0x508041]
0046d90a  7518                     jne      0x46d924
0046d90c  30e4                     xor      ah, ah
0046d90e  88d0                     mov      al, dl
0046d910  0592010000               add      eax, 0x192
0046d915  31d2                     xor      edx, edx
0046d917  6689c2                   mov      dx, ax
0046d91a  b80a000000               mov      eax, 0xa
0046d91f  e827c0ffff               call     0x46994b
0046d924  59                       pop      ecx
0046d925  5b                       pop      ebx
0046d926  c3                       ret
