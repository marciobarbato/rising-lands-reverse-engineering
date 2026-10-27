; BatimentGetCase; intervalo [0x0041aee2, 0x0041aff8)
; EXE original SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0041aee2  53                       push     ebx
0041aee3  51                       push     ecx
0041aee4  52                       push     edx
0041aee5  56                       push     esi
0041aee6  57                       push     edi
0041aee7  83ec18                   sub      esp, 0x18
0041aeea  89c1                     mov      ecx, eax
0041aeec  31d2                     xor      edx, edx
0041aeee  6689c2                   mov      dx, ax
0041aef1  89d0                     mov      eax, edx
0041aef3  c1e004                   shl      eax, 4
0041aef6  01d0                     add      eax, edx
0041aef8  c1e002                   shl      eax, 2
0041aefb  01d0                     add      eax, edx
0041aefd  bec8a04900               mov      esi, 0x49a0c8
0041af02  c1e002                   shl      eax, 2
0041af05  01c6                     add      esi, eax
0041af07  668b4602                 mov      ax, word ptr [esi + 2]
0041af0b  31d2                     xor      edx, edx
0041af0d  89442408                 mov      dword ptr [esp + 8], eax
0041af11  8a4608                   mov      al, byte ptr [esi + 8]
0041af14  88c2                     mov      dl, al
0041af16  89d0                     mov      eax, edx
0041af18  c1e002                   shl      eax, 2
0041af1b  29d0                     sub      eax, edx
0041af1d  bfffff0000               mov      edi, 0xffff
0041af22  c1e002                   shl      eax, 2
0041af25  31db                     xor      ebx, ebx
0041af27  01c2                     add      edx, eax
0041af29  31c9                     xor      ecx, ecx
0041af2b  c1e202                   shl      edx, 2
0041af2e  893c24                   mov      dword ptr [esp], edi
0041af31  668b828c5d4900           mov      ax, word ptr [edx + 0x495d8c]
0041af38  895c2410                 mov      dword ptr [esp + 0x10], ebx
0041af3c  89442404                 mov      dword ptr [esp + 4], eax
0041af40  668b828e5d4900           mov      ax, word ptr [edx + 0x495d8e]
0041af47  895c2414                 mov      dword ptr [esp + 0x14], ebx
0041af4b  8944240c                 mov      dword ptr [esp + 0xc], eax
0041af4f  eb01                     jmp      0x41af52
0041af51  41                       inc      ecx
0041af52  663b4c240c               cmp      cx, word ptr [esp + 0xc]
0041af57  7350                     jae      0x41afa9
0041af59  31db                     xor      ebx, ebx
0041af5b  eb01                     jmp      0x41af5e
0041af5d  43                       inc      ebx
0041af5e  8b542404                 mov      edx, dword ptr [esp + 4]
0041af62  6639d3                   cmp      bx, dx
0041af65  73ea                     jae      0x41af51
0041af67  89d0                     mov      eax, edx
0041af69  0fafc1                   imul     eax, ecx
0041af6c  31d2                     xor      edx, edx
0041af6e  01d8                     add      eax, ebx
0041af70  6689c2                   mov      dx, ax
0041af73  31c0                     xor      eax, eax
0041af75  8a4608                   mov      al, byte ptr [esi + 8]
0041af78  e8dffbffff               call     0x41ab5c
0041af7d  84c0                     test     al, al
0041af7f  74dc                     je       0x41af5d
0041af81  663b1c24                 cmp      bx, word ptr [esp]
0041af85  7303                     jae      0x41af8a
0041af87  891c24                   mov      dword ptr [esp], ebx
0041af8a  6639cf                   cmp      di, cx
0041af8d  7602                     jbe      0x41af91
0041af8f  89cf                     mov      edi, ecx
0041af91  663b4c2410               cmp      cx, word ptr [esp + 0x10]
0041af96  7604                     jbe      0x41af9c
0041af98  894c2410                 mov      dword ptr [esp + 0x10], ecx
0041af9c  663b5c2414               cmp      bx, word ptr [esp + 0x14]
0041afa1  76ba                     jbe      0x41af5d
0041afa3  895c2414                 mov      dword ptr [esp + 0x14], ebx
0041afa7  ebb4                     jmp      0x41af5d
0041afa9  31d2                     xor      edx, edx
0041afab  31c0                     xor      eax, eax
0041afad  668b542410               mov      dx, word ptr [esp + 0x10]
0041afb2  6689f8                   mov      ax, di
0041afb5  29c2                     sub      edx, eax
0041afb7  89d0                     mov      eax, edx
0041afb9  c1fa1f                   sar      edx, 0x1f
0041afbc  2bc2                     sub      eax, edx
0041afbe  d1f8                     sar      eax, 1
0041afc0  89c3                     mov      ebx, eax
0041afc2  31d2                     xor      edx, edx
0041afc4  31c0                     xor      eax, eax
0041afc6  668b1424                 mov      dx, word ptr [esp]
0041afca  668b442414               mov      ax, word ptr [esp + 0x14]
0041afcf  29d0                     sub      eax, edx
0041afd1  89c2                     mov      edx, eax
0041afd3  c1fa1f                   sar      edx, 0x1f
0041afd6  2bc2                     sub      eax, edx
0041afd8  d1f8                     sar      eax, 1
0041afda  89c2                     mov      edx, eax
0041afdc  89d8                     mov      eax, ebx
0041afde  01f8                     add      eax, edi
0041afe0  8b5c2408                 mov      ebx, dword ptr [esp + 8]
0041afe4  c1e008                   shl      eax, 8
0041afe7  01c3                     add      ebx, eax
0041afe9  8b0424                   mov      eax, dword ptr [esp]
0041afec  01d0                     add      eax, edx
0041afee  01d8                     add      eax, ebx
0041aff0  83c418                   add      esp, 0x18
0041aff3  e9262b0000               jmp      0x41db1e
