; AnimAttaqueEngin; intervalo [0x004479c4, 0x00447acf)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004479c4  53                       push     ebx
004479c5  51                       push     ecx
004479c6  52                       push     edx
004479c7  31d2                     xor      edx, edx
004479c9  6689c2                   mov      dx, ax
004479cc  89d3                     mov      ebx, edx
004479ce  c1e304                   shl      ebx, 4
004479d1  01d3                     add      ebx, edx
004479d3  c1e302                   shl      ebx, 2
004479d6  01d3                     add      ebx, edx
004479d8  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004479de  c1e302                   shl      ebx, 2
004479e1  01d3                     add      ebx, edx
004479e3  8a4301                   mov      al, byte ptr [ebx + 1]
004479e6  3c0c                     cmp      al, 0xc
004479e8  0f82c1000000             jb       0x447aaf
004479ee  3c0d                     cmp      al, 0xd
004479f0  0f86d5000000             jbe      0x447acb
004479f6  3c13                     cmp      al, 0x13
004479f8  0f82a7000000             jb       0x447aa5
004479fe  0f868b000000             jbe      0x447a8f
00447a04  3c17                     cmp      al, 0x17
00447a06  0f8283000000             jb       0x447a8f
00447a0c  3c18                     cmp      al, 0x18
00447a0e  0f867b000000             jbe      0x447a8f
00447a14  3c19                     cmp      al, 0x19
00447a16  e9ae000000               jmp      0x447ac9
00447a1b  8ab3a9000000             mov      dh, byte ptr [ebx + 0xa9]
00447a21  fec6                     inc      dh
00447a23  8a8ba7000000             mov      cl, byte ptr [ebx + 0xa7]
00447a29  88b3a9000000             mov      byte ptr [ebx + 0xa9], dh
00447a2f  38ce                     cmp      dh, cl
00447a31  0f8594000000             jne      0x447acb
00447a37  31d2                     xor      edx, edx
00447a39  8a93a4000000             mov      dl, byte ptr [ebx + 0xa4]
00447a3f  31c9                     xor      ecx, ecx
00447a41  42                       inc      edx
00447a42  8a8ba5000000             mov      cl, byte ptr [ebx + 0xa5]
00447a48  89d0                     mov      eax, edx
00447a4a  c1fa1f                   sar      edx, 0x1f
00447a4d  f7f9                     idiv     ecx
00447a4f  c683a900000000           mov      byte ptr [ebx + 0xa9], 0
00447a56  8893a4000000             mov      byte ptr [ebx + 0xa4], dl
00447a5c  5a                       pop      edx
00447a5d  59                       pop      ecx
00447a5e  5b                       pop      ebx
00447a5f  c3                       ret
00447a60  8aa3a9000000             mov      ah, byte ptr [ebx + 0xa9]
00447a66  fec4                     inc      ah
00447a68  8a93a8000000             mov      dl, byte ptr [ebx + 0xa8]
00447a6e  88a3a9000000             mov      byte ptr [ebx + 0xa9], ah
00447a74  38d4                     cmp      ah, dl
00447a76  0f854f000000             jne      0x447acb
00447a7c  31d2                     xor      edx, edx
00447a7e  8a93a4000000             mov      dl, byte ptr [ebx + 0xa4]
00447a84  31c9                     xor      ecx, ecx
00447a86  42                       inc      edx
00447a87  8a8ba6000000             mov      cl, byte ptr [ebx + 0xa6]
00447a8d  ebb9                     jmp      0x447a48
00447a8f  8a838a000000             mov      al, byte ptr [ebx + 0x8a]
00447a95  3c03                     cmp      al, 3
00447a97  7732                     ja       0x447acb
00447a99  31d2                     xor      edx, edx
00447a9b  88c2                     mov      dl, al
00447a9d  2eff2495b4794400         jmp      dword ptr cs:[edx*4 + 0x4479b4]
00447aa5  3c0f                     cmp      al, 0xf
00447aa7  72e6                     jb       0x447a8f
00447aa9  76e4                     jbe      0x447a8f
00447aab  3c12                     cmp      al, 0x12
00447aad  eb1a                     jmp      0x447ac9
00447aaf  3c03                     cmp      al, 3
00447ab1  7210                     jb       0x447ac3
00447ab3  76da                     jbe      0x447a8f
00447ab5  3c08                     cmp      al, 8
00447ab7  7206                     jb       0x447abf
00447ab9  76d4                     jbe      0x447a8f
00447abb  3c0b                     cmp      al, 0xb
00447abd  eb0a                     jmp      0x447ac9
00447abf  3c04                     cmp      al, 4
00447ac1  eb06                     jmp      0x447ac9
00447ac3  3c01                     cmp      al, 1
00447ac5  73c8                     jae      0x447a8f
00447ac7  84c0                     test     al, al
00447ac9  74c4                     je       0x447a8f
00447acb  5a                       pop      edx
00447acc  59                       pop      ecx
00447acd  5b                       pop      ebx
00447ace  c3                       ret
