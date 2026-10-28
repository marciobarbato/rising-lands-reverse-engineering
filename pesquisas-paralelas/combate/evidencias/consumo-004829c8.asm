; iagUnitSendMessage_entry; [0x004829c8, 0x00482a14)
; Original EXE SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
004829c8  51                       push     ecx
004829c9  56                       push     esi
004829ca  57                       push     edi
004829cb  55                       push     ebp
004829cc  89e5                     mov      ebp, esp
004829ce  83ec1c                   sub      esp, 0x1c
004829d1  89c6                     mov      esi, eax
004829d3  8855fc                   mov      byte ptr [ebp - 4], dl
004829d6  89da                     mov      edx, ebx
004829d8  31db                     xor      ebx, ebx
004829da  6689c3                   mov      bx, ax
004829dd  89df                     mov      edi, ebx
004829df  c1e704                   shl      edi, 4
004829e2  01df                     add      edi, ebx
004829e4  c1e702                   shl      edi, 2
004829e7  01df                     add      edi, ebx
004829e9  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
004829ee  c1e702                   shl      edi, 2
004829f1  8a0407                   mov      al, byte ptr [edi + eax]
004829f4  25ff000000               and      eax, 0xff
004829f9  8945e4                   mov      dword ptr [ebp - 0x1c], eax
004829fc  31c0                     xor      eax, eax
004829fe  8a45e4                   mov      al, byte ptr [ebp - 0x1c]
00482a01  e811aefeff               call     0x46d817
00482a06  25ff000000               and      eax, 0xff
00482a0b  83f802                   cmp      eax, 2
00482a0e  0f85a1040000             jne      0x482eb5
