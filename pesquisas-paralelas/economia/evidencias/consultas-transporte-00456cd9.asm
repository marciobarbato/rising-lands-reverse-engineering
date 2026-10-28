; EnginRentreMatiere; exclusive end0x456d35.
; Original EXE SHA-256:6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
00456cd9  53                       push     ebx
00456cda  88d3                     mov      bl, dl
00456cdc  31d2                     xor      edx, edx
00456cde  6689c2                   mov      dx, ax
00456ce1  89d0                     mov      eax, edx
00456ce3  c1e004                   shl      eax, 4
00456ce6  01d0                     add      eax, edx
00456ce8  c1e002                   shl      eax, 2
00456ceb  01c2                     add      edx, eax
00456ced  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00456cf2  c1e202                   shl      edx, 2
00456cf5  01d0                     add      eax, edx
00456cf7  31d2                     xor      edx, edx
00456cf9  8a5002                   mov      dl, byte ptr [eax + 2]
00456cfc  83fa05                   cmp      edx, 5
00456cff  740a                     je       0x456d0b
00456d01  83fa12                   cmp      edx, 0x12
00456d04  7405                     je       0x456d0b
00456d06  83fa11                   cmp      edx, 0x11
00456d09  7526                     jne      0x456d31
00456d0b  31d2                     xor      edx, edx
00456d0d  8a9082000000             mov      dl, byte ptr [eax + 0x82]
00456d13  83fa02                   cmp      edx, 2
00456d16  7519                     jne      0x456d31
00456d18  668b8080000000           mov      ax, word ptr [eax + 0x80]
00456d1f  25ffff0000               and      eax, 0xffff
00456d24  e8cb37fcff               call     0x41a4f4
00456d29  38d8                     cmp      al, bl
00456d2b  7504                     jne      0x456d31
00456d2d  b001                     mov      al, 1
00456d2f  5b                       pop      ebx
00456d30  c3                       ret
00456d31  30c0                     xor      al, al
00456d33  5b                       pop      ebx
00456d34  c3                       ret
