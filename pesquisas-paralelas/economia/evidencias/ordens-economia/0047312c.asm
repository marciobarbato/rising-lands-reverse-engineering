; SetDepotEnginSelect; original executable SHA-256: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
0047312c  56                       push esi
0047312d  57                       push edi
0047312e  83ec10                   sub esp, 0x10
00473131  88442404                 mov byte ptr [esp + 4], al
00473135  8854240c                 mov byte ptr [esp + 0xc], dl
00473139  891c24                   mov dword ptr [esp], ebx
0047313c  884c2408                 mov byte ptr [esp + 8], cl
00473140  31ff                     xor edi, edi
00473142  eb01                     jmp 0x473145
00473144  47                       inc edi
00473145  0fb6742404               movzx esi, byte ptr [esp + 4]
0047314a  c1e609                   shl esi, 9
0047314d  663bbe28875000           cmp di, word ptr [esi + 0x508728]
00473154  7338                     jae 0x47318e
00473156  31d2                     xor edx, edx
00473158  6689fa                   mov dx, di
0047315b  668b94562a875000         mov dx, word ptr [esi + edx*2 + 0x50872a]
00473163  31f6                     xor esi, esi
00473165  6689d6                   mov si, dx
00473168  89f0                     mov eax, esi
0047316a  e83e0cfdff               call 0x443dad
0047316f  84c0                     test al, al
00473171  74d1                     je 0x473144
00473173  89f0                     mov eax, esi
00473175  31c9                     xor ecx, ecx
00473177  31db                     xor ebx, ebx
00473179  31d2                     xor edx, edx
0047317b  8a4c2408                 mov cl, byte ptr [esp + 8]
0047317f  668b1c24                 mov bx, word ptr [esp]
00473183  8a54240c                 mov dl, byte ptr [esp + 0xc]
00473187  e8211cfdff               call 0x444dad
0047318c  ebb6                     jmp 0x473144
0047318e  83c410                   add esp, 0x10
00473191  5f                       pop edi
00473192  5e                       pop esi
00473193  c3                       ret
