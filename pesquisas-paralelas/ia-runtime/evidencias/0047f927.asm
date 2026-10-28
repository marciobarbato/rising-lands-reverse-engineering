; iaCalculPlayer (ai-player); intact original SHA-256 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; interval 0x0047f927..0x0047fa88 (end exclusive); labels are original SBL names
0047f927  53                       push ebx
0047f928  51                       push ecx
0047f929  56                       push esi
0047f92a  57                       push edi
0047f92b  89c3                     mov ebx, eax
0047f92d  89d1                     mov ecx, edx
0047f92f  89c2                     mov edx, eax
0047f931  c1e204                   shl edx, 4
0047f934  83f804                   cmp eax, 4
0047f937  7533                     jne 0x47f96c
0047f939  e845b9ffff               call 0x47b283 ; -> AvanceMonstre
0047f93e  b8b0485100               mov eax, 0x5148b0
0047f943  01d0                     add eax, edx
0047f945  e8cad9ffff               call 0x47d314 ; -> iaSolver
0047f94a  89c2                     mov edx, eax
0047f94c  85c0                     test eax, eax
0047f94e  0f84d4000000             je 0x47fa28
0047f954  3d0e001a1a               cmp eax, 0x1a1a000e
0047f959  0f84c9000000             je 0x47fa28
0047f95f  85c0                     test eax, eax
0047f961  0f84c1000000             je 0x47fa28
0047f967  5f                       pop edi
0047f968  5e                       pop esi
0047f969  59                       pop ecx
0047f96a  5b                       pop ebx
0047f96b  c3                       ret
0047f96c  80ba90a9510000           cmp byte ptr [edx + 0x51a990], 0
0047f973  7407                     je 0x47f97c
0047f975  31c0                     xor eax, eax
0047f977  5f                       pop edi
0047f978  5e                       pop esi
0047f979  59                       pop ecx
0047f97a  5b                       pop ebx
0047f97b  c3                       ret
0047f97c  8b3c9da8fa4d00           mov edi, dword ptr [ebx*4 + 0x4dfaa8]
0047f983  89de                     mov esi, ebx
0047f985  85ff                     test edi, edi
0047f987  7530                     jne 0x47f9b9
0047f989  668b045d28194e00         mov ax, word ptr [ebx*2 + 0x4e1928]
0047f991  25ffff0000               and eax, 0xffff
0047f996  7521                     jne 0x47f9b9
0047f998  fe8295a95100             inc byte ptr [edx + 0x51a995]
0047f99e  31c0                     xor eax, eax
0047f9a0  8a8295a95100             mov al, byte ptr [edx + 0x51a995]
0047f9a6  83f80a                   cmp eax, 0xa
0047f9a9  751b                     jne 0x47f9c6
0047f9ab  89d8                     mov eax, ebx
0047f9ad  e8e3430000               call 0x483d95 ; -> iagUnitDeleteAllGroups
0047f9b2  b819001a1a               mov eax, 0x1a1a0019
0047f9b7  eb0f                     jmp 0x47f9c8
0047f9b9  89f0                     mov eax, esi
0047f9bb  c1e004                   shl eax, 4
0047f9be  30d2                     xor dl, dl
0047f9c0  889095a95100             mov byte ptr [eax + 0x51a995], dl
0047f9c6  31c0                     xor eax, eax
0047f9c8  89de                     mov esi, ebx
0047f9ca  c1e604                   shl esi, 4
0047f9cd  3d19001a1a               cmp eax, 0x1a1a0019
0047f9d2  7509                     jne 0x47f9dd
0047f9d4  c68690a9510001           mov byte ptr [esi + 0x51a990], 1
0047f9db  eb98                     jmp 0x47f975
0047f9dd  89d8                     mov eax, ebx
0047f9df  e8522f0000               call 0x482936 ; -> iagUnitNoyau
0047f9e4  85c0                     test eax, eax
0047f9e6  7542                     jne 0x47fa2a
0047f9e8  89d8                     mov eax, ebx
0047f9ea  e84d4b0000               call 0x48453c ; -> iagVilleNoyau
0047f9ef  85c0                     test eax, eax
0047f9f1  7537                     jne 0x47fa2a
0047f9f3  89d8                     mov eax, ebx
0047f9f5  e889570000               call 0x485183 ; -> iagRessNoyau
0047f9fa  85c0                     test eax, eax
0047f9fc  752c                     jne 0x47fa2a
0047f9fe  89ca                     mov edx, ecx
0047fa00  89d8                     mov eax, ebx
0047fa02  e8d06c0000               call 0x4866d7 ; -> iagWarNoyau
0047fa07  85c0                     test eax, eax
0047fa09  751f                     jne 0x47fa2a
0047fa0b  b8b0485100               mov eax, 0x5148b0
0047fa10  01f0                     add eax, esi
0047fa12  e8fdd8ffff               call 0x47d314 ; -> iaSolver
0047fa17  89c2                     mov edx, eax
0047fa19  85c0                     test eax, eax
0047fa1b  740b                     je 0x47fa28
0047fa1d  3d0e001a1a               cmp eax, 0x1a1a000e
0047fa22  7404                     je 0x47fa28
0047fa24  85c0                     test eax, eax
0047fa26  7502                     jne 0x47fa2a
0047fa28  89d0                     mov eax, edx
0047fa2a  5f                       pop edi
0047fa2b  5e                       pop esi
0047fa2c  59                       pop ecx
0047fa2d  5b                       pop ebx
0047fa2e  c3                       ret
; 0x0047fa2f..0x0047fa88 not reached by any static path (padding or data):
0047fa2f  .byte 5352833c85a8fa4d0000753d668b1445
0047fa3f  .byte 28194e0081e2ffff0000752d89c2c1e2
0047fa4f  .byte 048a9a95a95100fec3889a95a9510088
0047fa5f  .byte da81e2ff00000083fa0a7518e8254300
0047fa6f  .byte 00b819001a1a5a5bc3c1e00430d28890
0047fa7f  .byte 95a9510031c05a5bc3
