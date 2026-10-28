; BonusSetEngin; exclusive end 0x00428c8a.
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Original instruction listing; capacity refresh remains an explicit dependency.
00428878  56                       push     esi
00428879  57                       push     edi
0042887a  83ec0c                   sub      esp, 0xc
0042887d  88442404                 mov      byte ptr [esp + 4], al
00428881  80fa0c                   cmp      dl, 0xc
00428884  0f87fa030000             ja       0x428c84
0042888a  31c0                     xor      eax, eax
0042888c  88d0                     mov      al, dl
0042888e  2eff248544884200         jmp      dword ptr cs:[eax*4 + 0x428844]
00428896  81e3ff000000             and      ebx, 0xff
0042889c  83fb1e                   cmp      ebx, 0x1e
0042889f  7451                     je       0x4288f2
004288a1  89d8                     mov      eax, ebx
004288a3  c1e002                   shl      eax, 2
004288a6  29d8                     sub      eax, ebx
004288a8  c1e003                   shl      eax, 3
004288ab  01d8                     add      eax, ebx
004288ad  89da                     mov      edx, ebx
004288af  668b0445dc654900         mov      ax, word ptr [eax*2 + 0x4965dc]
004288b7  31da                     xor      edx, ebx
004288b9  25ffff0000               and      eax, 0xffff
004288be  6689ca                   mov      dx, cx
004288c1  0fafd0                   imul     edx, eax
004288c4  be0a000000               mov      esi, 0xa
004288c9  89d0                     mov      eax, edx
004288cb  c1fa1f                   sar      edx, 0x1f
004288ce  f7fe                     idiv     esi
004288d0  31d2                     xor      edx, edx
004288d2  8a542404                 mov      dl, byte ptr [esp + 4]
004288d6  69d2d4010000             imul     edx, edx, 0x1d4
004288dc  89c1                     mov      ecx, eax
004288de  89d8                     mov      eax, ebx
004288e0  c1e003                   shl      eax, 3
004288e3  01d8                     add      eax, ebx
004288e5  66898c42a0fb4d00         mov      word ptr [edx + eax*2 + 0x4dfba0], cx
004288ed  e992030000               jmp      0x428c84
004288f2  30d2                     xor      dl, dl
004288f4  881424                   mov      byte ptr [esp], dl
004288f7  eb3e                     jmp      0x428937
004288f9  6bd332                   imul     edx, ebx, 0x32
004288fc  31c0                     xor      eax, eax
004288fe  668b82dc654900           mov      ax, word ptr [edx + 0x4965dc]
00428905  31d2                     xor      edx, edx
00428907  6689ca                   mov      dx, cx
0042890a  0fafd0                   imul     edx, eax
0042890d  be0a000000               mov      esi, 0xa
00428912  89d0                     mov      eax, edx
00428914  c1fa1f                   sar      edx, 0x1f
00428917  f7fe                     idiv     esi
00428919  89c6                     mov      esi, eax
0042891b  31c0                     xor      eax, eax
0042891d  8a442404                 mov      al, byte ptr [esp + 4]
00428921  69d0d4010000             imul     edx, eax, 0x1d4
00428927  6bc312                   imul     eax, ebx, 0x12
0042892a  fec3                     inc      bl
0042892c  6689b402a0fb4d00         mov      word ptr [edx + eax + 0x4dfba0], si
00428934  881c24                   mov      byte ptr [esp], bl
00428937  31db                     xor      ebx, ebx
00428939  8a1c24                   mov      bl, byte ptr [esp]
0042893c  83fb1a                   cmp      ebx, 0x1a
0042893f  7cb8                     jl       0x4288f9
00428941  e93e030000               jmp      0x428c84
00428946  31c0                     xor      eax, eax
00428948  8a442404                 mov      al, byte ptr [esp + 4]
0042894c  69f0d4010000             imul     esi, eax, 0x1d4
00428952  31d2                     xor      edx, edx
00428954  88da                     mov      dl, bl
00428956  89d0                     mov      eax, edx
00428958  c1e003                   shl      eax, 3
0042895b  01d0                     add      eax, edx
0042895d  888c46a2fb4d00           mov      byte ptr [esi + eax*2 + 0x4dfba2], cl
00428964  e91b030000               jmp      0x428c84
00428969  0fb6742404               movzx    esi, byte ptr [esp + 4]
0042896e  69f6d4010000             imul     esi, esi, 0x1d4
00428974  31d2                     xor      edx, edx
00428976  88da                     mov      dl, bl
00428978  89d0                     mov      eax, edx
0042897a  c1e003                   shl      eax, 3
0042897d  01d0                     add      eax, edx
0042897f  888c46adfb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbad], cl
00428986  e9f9020000               jmp      0x428c84
0042898b  31c0                     xor      eax, eax
0042898d  8a442404                 mov      al, byte ptr [esp + 4]
00428991  69f0d4010000             imul     esi, eax, 0x1d4
00428997  31d2                     xor      edx, edx
00428999  88da                     mov      dl, bl
0042899b  89d0                     mov      eax, edx
0042899d  c1e003                   shl      eax, 3
004289a0  01d0                     add      eax, edx
004289a2  888c46aefb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbae], cl
004289a9  e9d6020000               jmp      0x428c84
004289ae  31d2                     xor      edx, edx
004289b0  6689ca                   mov      dx, cx
004289b3  89d0                     mov      eax, edx
004289b5  c1e002                   shl      eax, 2
004289b8  01c2                     add      edx, eax
004289ba  01d2                     add      edx, edx
004289bc  be0a000000               mov      esi, 0xa
004289c1  89d0                     mov      eax, edx
004289c3  c1fa1f                   sar      edx, 0x1f
004289c6  f7fe                     idiv     esi
004289c8  29f0                     sub      eax, esi
004289ca  0fb6742404               movzx    esi, byte ptr [esp + 4]
004289cf  69f6d4010000             imul     esi, esi, 0x1d4
004289d5  31d2                     xor      edx, edx
004289d7  88c7                     mov      bh, al
004289d9  88da                     mov      dl, bl
004289db  89d0                     mov      eax, edx
004289dd  c1e003                   shl      eax, 3
004289e0  01d0                     add      eax, edx
004289e2  88bc46b0fb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbb0], bh
004289e9  e996020000               jmp      0x428c84
004289ee  0fb6742404               movzx    esi, byte ptr [esp + 4]
004289f3  69f6d4010000             imul     esi, esi, 0x1d4
004289f9  31d2                     xor      edx, edx
004289fb  88da                     mov      dl, bl
004289fd  89d0                     mov      eax, edx
004289ff  c1e003                   shl      eax, 3
00428a02  01d0                     add      eax, edx
00428a04  888c46affb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbaf], cl
00428a0b  e974020000               jmp      0x428c84
00428a10  0fb6742404               movzx    esi, byte ptr [esp + 4]
00428a15  69f6d4010000             imul     esi, esi, 0x1d4
00428a1b  31d2                     xor      edx, edx
00428a1d  88da                     mov      dl, bl
00428a1f  89d0                     mov      eax, edx
00428a21  c1e003                   shl      eax, 3
00428a24  01d0                     add      eax, edx
00428a26  888c46b1fb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbb1], cl
00428a2d  e952020000               jmp      0x428c84
00428a32  81e3ff000000             and      ebx, 0xff
00428a38  83fb1e                   cmp      ebx, 0x1e
00428a3b  744e                     je       0x428a8b
00428a3d  89d8                     mov      eax, ebx
00428a3f  c1e002                   shl      eax, 2
00428a42  29d8                     sub      eax, ebx
00428a44  c1e003                   shl      eax, 3
00428a47  01d8                     add      eax, ebx
00428a49  31f6                     xor      esi, esi
00428a4b  668b3445de654900         mov      si, word ptr [eax*2 + 0x4965de]
00428a53  89f0                     mov      eax, esi
00428a55  c1e002                   shl      eax, 2
00428a58  8d1406                   lea      edx, [esi + eax]
00428a5b  31ff                     xor      edi, edi
00428a5d  01d2                     add      edx, edx
00428a5f  6689cf                   mov      di, cx
00428a62  89d0                     mov      eax, edx
00428a64  c1fa1f                   sar      edx, 0x1f
00428a67  f7ff                     idiv     edi
00428a69  31d2                     xor      edx, edx
00428a6b  8a542404                 mov      dl, byte ptr [esp + 4]
00428a6f  69d2d4010000             imul     edx, edx, 0x1d4
00428a75  29c6                     sub      esi, eax
00428a77  89d8                     mov      eax, ebx
00428a79  c1e003                   shl      eax, 3
00428a7c  01d8                     add      eax, ebx
00428a7e  6689b442a4fb4d00         mov      word ptr [edx + eax*2 + 0x4dfba4], si
00428a86  e9f9010000               jmp      0x428c84
00428a8b  30e4                     xor      ah, ah
00428a8d  88642408                 mov      byte ptr [esp + 8], ah
00428a91  eb04                     jmp      0x428a97
00428a93  fe442408                 inc      byte ptr [esp + 8]
00428a97  31db                     xor      ebx, ebx
00428a99  8a5c2408                 mov      bl, byte ptr [esp + 8]
00428a9d  83fb1a                   cmp      ebx, 0x1a
00428aa0  0f8dde010000             jge      0x428c84
00428aa6  89d8                     mov      eax, ebx
00428aa8  e85f980100               call     0x44230c
00428aad  84c0                     test     al, al
00428aaf  74e2                     je       0x428a93
00428ab1  6bf332                   imul     esi, ebx, 0x32
00428ab4  668bb6de654900           mov      si, word ptr [esi + 0x4965de]
00428abb  81e6ffff0000             and      esi, 0xffff
00428ac1  6bd60a                   imul     edx, esi, 0xa
00428ac4  31ff                     xor      edi, edi
00428ac6  6689cf                   mov      di, cx
00428ac9  89d0                     mov      eax, edx
00428acb  c1fa1f                   sar      edx, 0x1f
00428ace  f7ff                     idiv     edi
00428ad0  6bd312                   imul     edx, ebx, 0x12
00428ad3  29c6                     sub      esi, eax
00428ad5  31c0                     xor      eax, eax
00428ad7  8a442404                 mov      al, byte ptr [esp + 4]
00428adb  69c0d4010000             imul     eax, eax, 0x1d4
00428ae1  6689b402a4fb4d00         mov      word ptr [edx + eax + 0x4dfba4], si
00428ae9  eba8                     jmp      0x428a93
00428aeb  31d2                     xor      edx, edx
00428aed  88da                     mov      dl, bl
00428aef  83fa1e                   cmp      edx, 0x1e
00428af2  741f                     je       0x428b13
00428af4  31c0                     xor      eax, eax
00428af6  8a442404                 mov      al, byte ptr [esp + 4]
00428afa  69d8d4010000             imul     ebx, eax, 0x1d4
00428b00  89d0                     mov      eax, edx
00428b02  c1e003                   shl      eax, 3
00428b05  01d0                     add      eax, edx
00428b07  888c43a6fb4d00           mov      byte ptr [ebx + eax*2 + 0x4dfba6], cl
00428b0e  e971010000               jmp      0x428c84
00428b13  30da                     xor      dl, bl
00428b15  eb02                     jmp      0x428b19
00428b17  fec2                     inc      dl
00428b19  31db                     xor      ebx, ebx
00428b1b  88d3                     mov      bl, dl
00428b1d  83fb1a                   cmp      ebx, 0x1a
00428b20  0f8d5e010000             jge      0x428c84
00428b26  89d8                     mov      eax, ebx
00428b28  e8df970100               call     0x44230c
00428b2d  84c0                     test     al, al
00428b2f  74e6                     je       0x428b17
00428b31  6bdb12                   imul     ebx, ebx, 0x12
00428b34  31c0                     xor      eax, eax
00428b36  8a442404                 mov      al, byte ptr [esp + 4]
00428b3a  69c0d4010000             imul     eax, eax, 0x1d4
00428b40  888c03a6fb4d00           mov      byte ptr [ebx + eax + 0x4dfba6], cl
00428b47  ebce                     jmp      0x428b17
00428b49  31d2                     xor      edx, edx
00428b4b  88da                     mov      dl, bl
00428b4d  83fa1e                   cmp      edx, 0x1e
00428b50  7420                     je       0x428b72
00428b52  31db                     xor      ebx, ebx
00428b54  8a5c2404                 mov      bl, byte ptr [esp + 4]
00428b58  69dbd4010000             imul     ebx, ebx, 0x1d4
00428b5e  89d0                     mov      eax, edx
00428b60  c1e003                   shl      eax, 3
00428b63  01d0                     add      eax, edx
00428b65  66898c43a8fb4d00         mov      word ptr [ebx + eax*2 + 0x4dfba8], cx
00428b6d  e912010000               jmp      0x428c84
00428b72  30db                     xor      bl, bl
00428b74  eb02                     jmp      0x428b78
00428b76  fec3                     inc      bl
00428b78  31d2                     xor      edx, edx
00428b7a  88da                     mov      dl, bl
00428b7c  83fa1a                   cmp      edx, 0x1a
00428b7f  0f8dff000000             jge      0x428c84
00428b85  89d0                     mov      eax, edx
00428b87  e880970100               call     0x44230c
00428b8c  84c0                     test     al, al
00428b8e  74e6                     je       0x428b76
00428b90  6bd212                   imul     edx, edx, 0x12
00428b93  31c0                     xor      eax, eax
00428b95  8a442404                 mov      al, byte ptr [esp + 4]
00428b99  69c0d4010000             imul     eax, eax, 0x1d4
00428b9f  66898c02a8fb4d00         mov      word ptr [edx + eax + 0x4dfba8], cx
00428ba7  ebcd                     jmp      0x428b76
00428ba9  31d2                     xor      edx, edx
00428bab  88da                     mov      dl, bl
00428bad  83fa1e                   cmp      edx, 0x1e
00428bb0  741f                     je       0x428bd1
00428bb2  31db                     xor      ebx, ebx
00428bb4  8a5c2404                 mov      bl, byte ptr [esp + 4]
00428bb8  69dbd4010000             imul     ebx, ebx, 0x1d4
00428bbe  89d0                     mov      eax, edx
00428bc0  c1e003                   shl      eax, 3
00428bc3  01d0                     add      eax, edx
00428bc5  888c43aafb4d00           mov      byte ptr [ebx + eax*2 + 0x4dfbaa], cl
00428bcc  e9b3000000               jmp      0x428c84
00428bd1  30da                     xor      dl, bl
00428bd3  eb18                     jmp      0x428bed
00428bd5  6bdb12                   imul     ebx, ebx, 0x12
00428bd8  31c0                     xor      eax, eax
00428bda  8a442404                 mov      al, byte ptr [esp + 4]
00428bde  69c0d4010000             imul     eax, eax, 0x1d4
00428be4  fec2                     inc      dl
00428be6  888c03aafb4d00           mov      byte ptr [ebx + eax + 0x4dfbaa], cl
00428bed  31db                     xor      ebx, ebx
00428bef  88d3                     mov      bl, dl
00428bf1  83fb1a                   cmp      ebx, 0x1a
00428bf4  7cdf                     jl       0x428bd5
00428bf6  e989000000               jmp      0x428c84
00428bfb  31d2                     xor      edx, edx
00428bfd  88da                     mov      dl, bl
00428bff  83fa1e                   cmp      edx, 0x1e
00428c02  741c                     je       0x428c20
00428c04  31db                     xor      ebx, ebx
00428c06  8a5c2404                 mov      bl, byte ptr [esp + 4]
00428c0a  69dbd4010000             imul     ebx, ebx, 0x1d4
00428c10  89d0                     mov      eax, edx
00428c12  c1e003                   shl      eax, 3
00428c15  01d0                     add      eax, edx
00428c17  888c43abfb4d00           mov      byte ptr [ebx + eax*2 + 0x4dfbab], cl
00428c1e  eb3a                     jmp      0x428c5a
00428c20  30da                     xor      dl, bl
00428c22  eb02                     jmp      0x428c26
00428c24  fec2                     inc      dl
00428c26  31db                     xor      ebx, ebx
00428c28  88d3                     mov      bl, dl
00428c2a  83fb1a                   cmp      ebx, 0x1a
00428c2d  7d2b                     jge      0x428c5a
00428c2f  83fb0c                   cmp      ebx, 0xc
00428c32  740a                     je       0x428c3e
00428c34  83fb0d                   cmp      ebx, 0xd
00428c37  7405                     je       0x428c3e
00428c39  83fb0f                   cmp      ebx, 0xf
00428c3c  75e6                     jne      0x428c24
00428c3e  31c0                     xor      eax, eax
00428c40  8a442404                 mov      al, byte ptr [esp + 4]
00428c44  69d8d4010000             imul     ebx, eax, 0x1d4
00428c4a  31c0                     xor      eax, eax
00428c4c  88d0                     mov      al, dl
00428c4e  6bc012                   imul     eax, eax, 0x12
00428c51  888c03abfb4d00           mov      byte ptr [ebx + eax + 0x4dfbab], cl
00428c58  ebca                     jmp      0x428c24
00428c5a  31c0                     xor      eax, eax
00428c5c  8a442404                 mov      al, byte ptr [esp + 4]
00428c60  e88ae90100               call     0x4475ef
00428c65  eb1d                     jmp      0x428c84
00428c67  0fb6742404               movzx    esi, byte ptr [esp + 4]
00428c6c  69f6d4010000             imul     esi, esi, 0x1d4
00428c72  31d2                     xor      edx, edx
00428c74  88da                     mov      dl, bl
00428c76  89d0                     mov      eax, edx
00428c78  c1e003                   shl      eax, 3
00428c7b  01d0                     add      eax, edx
00428c7d  888c46abfb4d00           mov      byte ptr [esi + eax*2 + 0x4dfbab], cl
00428c84  83c40c                   add      esp, 0xc
00428c87  5f                       pop      edi
00428c88  5e                       pop      esi
00428c89  c3                       ret
