; BatimentModifyTerrain [0x41ba49, 0x41bb8a)
; SHA-256 EXE: 6c556520c084b9300d9ac01900d1505126085c5f64b1ac5e5b615ea41c8543fb
; Desmontagem linear. Algumas regiões entre símbolos contêm tabelas; não são prova de fluxo.
0041ba49  51                     push     ecx
0041ba4a  56                     push     esi
0041ba4b  57                     push     edi
0041ba4c  55                     push     ebp
0041ba4d  83ec24                 sub      esp, 0x24
0041ba50  89c7                   mov      edi, eax
0041ba52  89d6                   mov      esi, edx
0041ba54  895c240c               mov      dword ptr [esp + 0xc], ebx
0041ba58  31c9                   xor      ecx, ecx
0041ba5a  6689d9                 mov      cx, bx
0041ba5d  89ca                   mov      edx, ecx
0041ba5f  c1e204                 shl      edx, 4
0041ba62  01ca                   add      edx, ecx
0041ba64  c1e202                 shl      edx, 2
0041ba67  01ca                   add      edx, ecx
0041ba69  bdc8a04900             mov      ebp, 0x49a0c8
0041ba6e  c1e202                 shl      edx, 2
0041ba71  01d5                   add      ebp, edx
0041ba73  31c9                   xor      ecx, ecx
0041ba75  8a5508                 mov      dl, byte ptr [ebp + 8]
0041ba78  88d1                   mov      cl, dl
0041ba7a  88542420               mov      byte ptr [esp + 0x20], dl
0041ba7e  89ca                   mov      edx, ecx
0041ba80  c1e202                 shl      edx, 2
0041ba83  29ca                   sub      edx, ecx
0041ba85  c1e202                 shl      edx, 2
0041ba88  01ca                   add      edx, ecx
0041ba8a  89742408               mov      dword ptr [esp + 8], esi
0041ba8e  668b0c958c5d4900       mov      cx, word ptr [edx*4 + 0x495d8c]
0041ba96  668b14958e5d4900       mov      dx, word ptr [edx*4 + 0x495d8e]
0041ba9e  30e4                   xor      ah, ah
0041baa0  89542404               mov      dword ptr [esp + 4], edx
0041baa4  31d2                   xor      edx, edx
0041baa6  8864241c               mov      byte ptr [esp + 0x1c], ah
0041baaa  89542410               mov      dword ptr [esp + 0x10], edx
0041baae  ba00010000             mov      edx, 0x100
0041bab3  81c5cc000000           add      ebp, 0xcc
0041bab9  29ca                   sub      edx, ecx
0041babb  894c2414               mov      dword ptr [esp + 0x14], ecx
0041babf  891424                 mov      dword ptr [esp], edx
0041bac2  eb0e                   jmp      0x41bad2 ;
0041bac4  8b5c2410               mov      ebx, dword ptr [esp + 0x10]
0041bac8  8b1424                 mov      edx, dword ptr [esp]
0041bacb  43                     inc      ebx
0041bacc  01d7                   add      edi, edx
0041bace  895c2410               mov      dword ptr [esp + 0x10], ebx
0041bad2  8b542410               mov      edx, dword ptr [esp + 0x10]
0041bad6  663b542404             cmp      dx, word ptr [esp + 4]
0041badb  0f8375420000           jae      0x41fd56
0041bae1  31f6                   xor      esi, esi
0041bae3  89742418               mov      dword ptr [esp + 0x18], esi
0041bae7  eb19                   jmp      0x41bb02 ;
0041bae9  8b742418               mov      esi, dword ptr [esp + 0x18]
0041baed  31d2                   xor      edx, edx
0041baef  8b0d747d5000           mov      ecx, dword ptr [0x507d74]
0041baf5  6689fa                 mov      dx, di
0041baf8  46                     inc      esi
0041baf9  47                     inc      edi
0041bafa  89742418               mov      dword ptr [esp + 0x18], esi
0041bafe  c6041100               mov      byte ptr [ecx + edx], 0
0041bb02  8b542418               mov      edx, dword ptr [esp + 0x18]
0041bb06  663b542414             cmp      dx, word ptr [esp + 0x14]
0041bb0b  73b7                   jae      0x41bac4
0041bb0d  31f6                   xor      esi, esi
0041bb0f  31d2                   xor      edx, edx
0041bb11  6689fe                 mov      si, di
0041bb14  668b542408             mov      dx, word ptr [esp + 8]
0041bb19  89f0                   mov      eax, esi
0041bb1b  89d1                   mov      ecx, edx
0041bb1d  e82fa70500             call     0x476251 ; SetTerrain
0041bb22  41                     inc      ecx
0041bb23  31d2                   xor      edx, edx
0041bb25  894c2408               mov      dword ptr [esp + 8], ecx
0041bb29  31c9                   xor      ecx, ecx
0041bb2b  668b542410             mov      dx, word ptr [esp + 0x10]
0041bb30  668b4c2414             mov      cx, word ptr [esp + 0x14]
0041bb35  0fafca                 imul     ecx, edx
0041bb38  31d2                   xor      edx, edx
0041bb3a  668b542418             mov      dx, word ptr [esp + 0x18]
0041bb3f  01d1                   add      ecx, edx
0041bb41  31d2                   xor      edx, edx
0041bb43  8a542420               mov      dl, byte ptr [esp + 0x20]
0041bb47  6bd234                 imul     edx, edx, 0x34
0041bb4a  8b92945d4900           mov      edx, dword ptr [edx + 0x495d94]
0041bb50  803c1100               cmp      byte ptr [ecx + edx], 0
0041bb54  7493                   je       0x41bae9
0041bb56  ba01000000             mov      edx, 1
0041bb5b  89f0                   mov      eax, esi
0041bb5d  e8cca60500             call     0x47622e ; SetCollision
0041bb62  31d2                   xor      edx, edx
0041bb64  8a54241c               mov      dl, byte ptr [esp + 0x1c]
0041bb68  52                     push     edx
0041bb69  01d2                   add      edx, edx
0041bb6b  bb03000000             mov      ebx, 3
0041bb70  8d0c2a                 lea      ecx, [edx + ebp]
0041bb73  31d2                   xor      edx, edx
0041bb75  89f0                   mov      eax, esi
0041bb77  668b542410             mov      dx, word ptr [esp + 0x10]
0041bb7c  e8b7250200             call     0x43e138 ; Chemin_ModifieZone
0041bb81  fe44241c               inc      byte ptr [esp + 0x1c]
0041bb85  e95fffffff             jmp      0x41bae9 ;
