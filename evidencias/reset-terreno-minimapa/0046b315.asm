; TerrainReset; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0046b315  53                       push ebx
0046b316  51                       push ecx
0046b317  52                       push edx
0046b318  b11f                     mov cl, 0x1f
0046b31a  31d2                     xor edx, edx
0046b31c  eb09                     jmp 0x46b327
0046b31e  42                       inc edx
0046b31f  81fa00000100             cmp edx, 0x10000
0046b325  7351                     jae 0x46b378
0046b327  a1747d5000               mov eax, dword ptr [0x507d74]
0046b32c  c6040200                 mov byte ptr [edx + eax], 0
0046b330  b828000000               mov eax, 0x28
0046b335  e8a2510000               call 0x4704dc
0046b33a  88c3                     mov bl, al
0046b33c  a1ac7d5000               mov eax, dword ptr [0x507dac]
0046b341  80e303                   and bl, 3
0046b344  881c02                   mov byte ptr [edx + eax], bl
0046b347  a1a87d5000               mov eax, dword ptr [0x507da8]
0046b34c  c6040200                 mov byte ptr [edx + eax], 0
0046b350  31c0                     xor eax, eax
0046b352  8b98987d5000             mov ebx, dword ptr [eax + 0x507d98]
0046b358  c6041a00                 mov byte ptr [edx + ebx], 0
0046b35c  8b98887d5000             mov ebx, dword ptr [eax + 0x507d88]
0046b362  880c1a                   mov byte ptr [edx + ebx], cl
0046b365  8b98787d5000             mov ebx, dword ptr [eax + 0x507d78]
0046b36b  83c004                   add eax, 4
0046b36e  880c1a                   mov byte ptr [edx + ebx], cl
0046b371  83f810                   cmp eax, 0x10
0046b374  74a8                     je 0x46b31e
0046b376  ebda                     jmp 0x46b352
0046b378  31c0                     xor eax, eax
0046b37a  83c004                   add eax, 4
0046b37d  31d2                     xor edx, edx
0046b37f  66899050995000           mov word ptr [eax + 0x509950], dx
0046b386  83f850                   cmp eax, 0x50
0046b389  75ef                     jne 0x46b37a
0046b38b  5a                       pop edx
0046b38c  59                       pop ecx
0046b38d  5b                       pop ebx
0046b38e  c3                       ret
