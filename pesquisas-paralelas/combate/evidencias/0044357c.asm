; ResetOrdre; intervalo [0x0044357c, 0x00443688)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0044357c  53                       push     ebx
0044357d  51                       push     ecx
0044357e  52                       push     edx
0044357f  56                       push     esi
00443580  89c1                     mov      ecx, eax
00443582  31c0                     xor      eax, eax
00443584  6689c8                   mov      ax, cx
00443587  89c3                     mov      ebx, eax
00443589  c1e304                   shl      ebx, 4
0044358c  01c3                     add      ebx, eax
0044358e  c1e302                   shl      ebx, 2
00443591  01c3                     add      ebx, eax
00443593  a1a0194e00               mov      eax, dword ptr [0x4e19a0]
00443598  c1e302                   shl      ebx, 2
0044359b  01c3                     add      ebx, eax
0044359d  8b8383000000             mov      eax, dword ptr [ebx + 0x83]
004435a3  c1f818                   sar      eax, 0x18
004435a6  85c0                     test     eax, eax
004435a8  7528                     jne      0x4435d2
004435aa  8b8384000000             mov      eax, dword ptr [ebx + 0x84]
004435b0  c1f818                   sar      eax, 0x18
004435b3  85c0                     test     eax, eax
004435b5  751b                     jne      0x4435d2
004435b7  8a4301                   mov      al, byte ptr [ebx + 1]
004435ba  25ff000000               and      eax, 0xff
004435bf  83f810                   cmp      eax, 0x10
004435c2  740e                     je       0x4435d2
004435c4  c683a900000000           mov      byte ptr [ebx + 0xa9], 0
004435cb  c683a400000000           mov      byte ptr [ebx + 0xa4], 0
004435d2  8a4301                   mov      al, byte ptr [ebx + 1]
004435d5  3c0d                     cmp      al, 0xd
004435d7  746f                     je       0x443648
004435d9  31d2                     xor      edx, edx
004435db  6689ca                   mov      dx, cx
004435de  89d0                     mov      eax, edx
004435e0  c1e004                   shl      eax, 4
004435e3  01d0                     add      eax, edx
004435e5  c1e002                   shl      eax, 2
004435e8  01d0                     add      eax, edx
004435ea  8b15a0194e00             mov      edx, dword ptr [0x4e19a0]
004435f0  c1e002                   shl      eax, 2
004435f3  01d0                     add      eax, edx
004435f5  668b737c                 mov      si, word ptr [ebx + 0x7c]
004435f9  6689707e                 mov      word ptr [eax + 0x7e], si
004435fd  663b0d04634900           cmp      cx, word ptr [0x496304]
00443604  7522                     jne      0x443628
00443606  30d2                     xor      dl, dl
00443608  b9ffff0000               mov      ecx, 0xffff
0044360d  8815360f4e00             mov      byte ptr [0x4e0f36], dl
00443613  8815370f4e00             mov      byte ptr [0x4e0f37], dl
00443619  31d2                     xor      edx, edx
0044361b  66890d04634900           mov      word ptr [0x496304], cx
00443622  89153c0f4e00             mov      dword ptr [0x4e0f3c], edx
00443628  c6808800000000           mov      byte ptr [eax + 0x88], 0
0044362f  c6838200000000           mov      byte ptr [ebx + 0x82], 0
00443636  66c783b2000000ffff       mov      word ptr [ebx + 0xb2], 0xffff
0044363f  c6430202                 mov      byte ptr [ebx + 2], 2
00443643  5e                       pop      esi
00443644  5a                       pop      edx
00443645  59                       pop      ecx
00443646  5b                       pop      ebx
00443647  c3                       ret
00443648  31c0                     xor      eax, eax
0044364a  668b83c0000000           mov      ax, word ptr [ebx + 0xc0]
00443651  3dffff0000               cmp      eax, 0xffff
00443656  7481                     je       0x4435d9
00443658  e8a201feff               call     0x4237ff
0044365d  31c0                     xor      eax, eax
0044365f  668b83c0000000           mov      ax, word ptr [ebx + 0xc0]
00443666  e811d6fdff               call     0x420c7c
0044366b  84c0                     test     al, al
0044366d  0f8466ffffff             je       0x4435d9
00443673  31c0                     xor      eax, eax
00443675  31d2                     xor      edx, edx
00443677  668b83c0000000           mov      ax, word ptr [ebx + 0xc0]
0044367e  e8d96ffdff               call     0x41a65c
00443683  e951ffffff               jmp      0x4435d9
