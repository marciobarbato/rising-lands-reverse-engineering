; InputGame_custos_e_comando_de_aprendizagem: limite por trecho de contexto; não é função independente nem execução até RET, fim exclusivo 0x0042bf92.
; SHA-256 original: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Gerado por Capstone; não é pseudocódigo nem prova de semântica.
0042bec6  8a45fc                   mov      al, byte ptr [ebp - 4]
0042bec9  31d2                     xor      edx, edx
0042becb  8945d0                   mov      dword ptr [ebp - 0x30], eax
0042bece  e8e3e5feff               call     0x41a4b6
0042bed3  6689c2                   mov      dx, ax
0042bed6  81faffff0000             cmp      edx, 0xffff
0042bedc  0f840c010000             je       0x42bfee
0042bee2  89d0                     mov      eax, edx
0042bee4  e80be6feff               call     0x41a4f4
0042bee9  25ff000000               and      eax, 0xff
0042beee  83f814                   cmp      eax, 0x14
0042bef1  0f849b000000             je       0x42bf92
0042bef7  baffff0000               mov      edx, 0xffff
0042befc  8d4de4                   lea      ecx, [ebp - 0x1c]
0042beff  8d5de0                   lea      ebx, [ebp - 0x20]
0042bf02  30c0                     xor      al, al
0042bf04  8955ec                   mov      dword ptr [ebp - 0x14], edx
0042bf07  8845f8                   mov      byte ptr [ebp - 8], al
0042bf0a  8d55e8                   lea      edx, [ebp - 0x18]
0042bf0d  89f8                     mov      eax, edi
0042bf0f  e8ea870400               call     0x4746fe
0042bf14  8b45e8                   mov      eax, dword ptr [ebp - 0x18]
0042bf17  66a312064e00             mov      word ptr [0x4e0612], ax
0042bf1d  8b45e0                   mov      eax, dword ptr [ebp - 0x20]
0042bf20  66a314064e00             mov      word ptr [0x4e0614], ax
0042bf26  8b45e4                   mov      eax, dword ptr [ebp - 0x1c]
0042bf29  31db                     xor      ebx, ebx
0042bf2b  66a316064e00             mov      word ptr [0x4e0616], ax
0042bf31  8a25ae995000             mov      ah, byte ptr [0x5099ae]
0042bf37  66891d18064e00           mov      word ptr [0x4e0618], bx
0042bf3e  84e4                     test     ah, ah
0042bf40  0f847afeffff             je       0x42bdc0
0042bf46  803daf99500000           cmp      byte ptr [0x5099af], 0
0042bf4d  0f846dfeffff             je       0x42bdc0
0042bf53  8b45d0                   mov      eax, dword ptr [ebp - 0x30]
0042bf56  31db                     xor      ebx, ebx
0042bf58  31d2                     xor      edx, edx
0042bf5a  31c9                     xor      ecx, ecx
0042bf5c  668b5de4                 mov      bx, word ptr [ebp - 0x1c]
0042bf60  50                       push     eax
0042bf61  31c0                     xor      eax, eax
0042bf63  668b55e0                 mov      dx, word ptr [ebp - 0x20]
0042bf67  668b45e8                 mov      ax, word ptr [ebp - 0x18]
0042bf6b  e875b70300               call     0x4676e5
0042bf70  84c0                     test     al, al
0042bf72  0f8448feffff             je       0x42bdc0
0042bf78  6a00                     push     0
0042bf7a  ba23000000               mov      edx, 0x23
0042bf7f  8b45d0                   mov      eax, dword ptr [ebp - 0x30]
0042bf82  6a00                     push     0
0042bf84  89fb                     mov      ebx, edi
0042bf86  31c9                     xor      ecx, ecx
0042bf88  e8472d0300               call     0x45ecd4
0042bf8d  e92efeffff               jmp      0x42bdc0
